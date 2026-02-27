---
title: "Building an MCP Plugin for Claude Code: A Deep Dive with Claudebin"
date: 2026-02-27T10:00:00+02:00
description: "How I built a session-sharing plugin using the Model Context Protocol. From stdio transport and JSON-RPC wire protocol to device authorization, async polling, and an honest comparison with OpenCode's direct plugin model."
keywords:
    - mcp
    - model context protocol
    - claude code
    - claude code plugin
    - mcp server
    - json-rpc
    - claudebin
    - opencode
    - agent tooling
    - agentic programming
tags:
    - mcp
    - agentic-programming
    - typescript
    - deep-dive
---

Claude Code sessions are ephemeral. You have a 45-minute conversation where you debug a gnarly race condition, the agent rewrites three files, and then it's gone. Buried in a `.jsonl` file somewhere under `~/.claude/projects/`. No way to share it, reference it, or learn from it later.

That bothered me enough to build [claudebin](https://claudebin.com), a plugin that turns any Claude Code session into a permanent, shareable URL. Run `/claudebin:share`, get back `claudebin.com/threads/abc123`. Done.

But this post isn't about claudebin the product. It's about what I learned building an MCP server that ships as a Claude Code plugin. If you're thinking about extending Claude Code with custom tools, this is the practical guide I wish I had.

## MCP Under the Hood: JSON-RPC 2.0 Over stdio

The Model Context Protocol is a thin layer on top of [JSON-RPC 2.0](https://www.jsonrpc.org/specification). Claude Code spawns your server as a child process, connects its stdin/stdout to a pipe, and exchanges newline-delimited JSON messages. No HTTP, no WebSockets, no port allocation. The process model is deliberately simple: one child process per MCP server, lifecycle tied to the parent.

Let's look at what actually goes over the wire. When Claude Code starts your server, the first thing it sends is an `initialize` request:

```json
→ {"jsonrpc":"2.0","id":1,"method":"initialize","params":{
    "protocolVersion":"2024-11-05",
    "capabilities":{"roots":{"listChanged":true}},
    "clientInfo":{"name":"claude-code","version":"1.0.0"}
  }}

← {"jsonrpc":"2.0","id":1,"result":{
    "protocolVersion":"2024-11-05",
    "capabilities":{"tools":{}},
    "serverInfo":{"name":"claudebin","version":"1.0.0"}
  }}

→ {"jsonrpc":"2.0","method":"notifications/initialized"}
```

This is a capability negotiation handshake. The client declares what it supports (root listing, sampling, etc.), the server responds with its capabilities. Claudebin only declares `tools`. It doesn't provide resources or prompts. The third message is a notification (no `id` field, no response expected), signaling the handshake is complete.

After initialization, Claude discovers available tools via `tools/list`:

```json
→ {"jsonrpc":"2.0","id":2,"method":"tools/list"}

← {"jsonrpc":"2.0","id":2,"result":{
    "tools":[{
      "name":"share",
      "description":"Share the current Claude Code session to Claudebin",
      "inputSchema":{
        "type":"object",
        "properties":{
          "project_path":{"type":"string","description":"Absolute path to the project directory"},
          "title":{"type":"string","description":"Optional title for the session"},
          "is_public":{"type":"boolean","default":true,"description":"Whether the session appears in public listings"}
        },
        "required":["project_path"]
      }
    }]
  }}
```

That `inputSchema` is a standard JSON Schema object. Claude uses it to understand what arguments your tool expects. The property names, types, and descriptions all feed into the model's tool-use reasoning. When a user runs `/claudebin:share`, Claude reads this schema, infers that `project_path` should be the current working directory, and constructs the `tools/call` request:

```json
→ {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{
    "name":"share",
    "arguments":{"project_path":"/Users/vlad/projects/dd","is_public":true}
  }}

← {"jsonrpc":"2.0","id":3,"result":{
    "content":[{"type":"text","text":"https://claudebin.com/threads/abc123"}]
  }}
```

The response uses MCP's content block format, an array of typed content items. Your tool can return `text`, `image` (base64-encoded), or `resource` (URI references). Claudebin returns a plain text URL. Error responses use the `isError` flag:

```json
← {"jsonrpc":"2.0","id":3,"result":{
    "content":[{"type":"text","text":"Session file not found"}],
    "isError":true
  }}
```

This is an important distinction. MCP separates *protocol errors* (malformed JSON-RPC, unknown method) from *tool errors* (your tool ran but failed). Protocol errors use JSON-RPC's `error` field. Tool errors use a successful response with `isError: true`. The reason: Claude can reason about tool errors and retry or adjust. Protocol errors are opaque failures.

All of this wire protocol detail is handled by the SDK. You never construct these messages manually. But understanding what's beneath the abstraction matters, especially when debugging why Claude isn't passing the arguments you expect, or why your tool's response isn't rendering correctly.

## The Process Model and Server Lifecycle

When Claude Code encounters an MCP server in its configuration, it spawns it as a child process using the command specified in `.mcp.json`. The stdio transport means the process stays alive for the duration of the Claude Code session. It's not a request/response fork-per-call model. The server initializes once, registers its tools, and then sits in an event loop waiting for JSON-RPC messages on stdin.

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { registerTools } from "./tools/index.js";

const server = new McpServer({
  name: "claudebin",
  version: "1.0.0",
});

registerTools(server);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
```

The `StdioServerTransport` wraps `process.stdin` and `process.stdout` into a message-oriented stream. Under the hood, it buffers incoming bytes, splits on newlines, parses each line as JSON-RPC, and dispatches to the appropriate handler. Outgoing messages are serialized, newline-terminated, and flushed to stdout.

One implication of the long-lived process model: anything you `console.log` goes to stdout and corrupts the JSON-RPC stream. This is the first thing that bites new MCP developers. Use `console.error` (which goes to stderr) for debug logging, or better yet, use the SDK's built-in logging that routes through the MCP protocol itself.

## Zod as a Schema Bridge

Claudebin registers its tool with Zod schemas for input validation:

```typescript
import { z } from "zod";

server.tool(
  "share",
  "Share the current Claude Code session to Claudebin",
  {
    project_path: z.string().describe("Absolute path to the project directory"),
    title: z.string().optional().describe("Optional title for the session"),
    is_public: z.boolean().default(true)
      .describe("Whether the session appears in public listings"),
  },
  async ({ project_path, title, is_public }) => {
    // handler logic
  }
);
```

Zod schemas serve triple duty here. First, they generate the JSON Schema returned in `tools/list`. The MCP SDK calls `zodToJsonSchema()` internally to produce the `inputSchema` that Claude reads. Second, they validate incoming arguments at runtime before your handler executes. If Claude sends a malformed `project_path`, Zod throws before your code runs. Third, they provide TypeScript type inference. The handler callback gets fully typed parameters without manual type assertions.

The `.describe()` calls are more important than they look. Those strings become the `description` field in the JSON Schema, and they're what Claude reads to decide how to populate the arguments. A vague description like "path" means Claude might pass a relative path or a file path. "Absolute path to the project directory" tells Claude exactly what's needed. The quality of your Zod descriptions directly affects tool-use accuracy.

## Parsing Claude's Session Storage

The core challenge of claudebin isn't the MCP protocol. It's reverse-engineering how Claude Code persists sessions locally and extracting the right data.

Claude Code stores conversations as `.jsonl` files under `~/.claude/projects/`. Each line is a self-contained JSON object representing a conversation turn. The directory name is a deterministic transformation of the project's absolute path:

```typescript
function normalizeProjectPath(projectPath: string): string {
  return projectPath.replace(/^\//, "").replace(/[^a-zA-Z0-9]/g, "-");
}
```

`/Users/vlad/projects/my-app` becomes `Users-vlad-projects-my-app`. Every non-alphanumeric character, including dots, underscores, and tildes, maps to a dash. This is an undocumented implementation detail I found by reading Claude Code's source and verifying against the filesystem. Getting it wrong means your plugin silently produces a "session not found" error with no useful diagnostic.

The directory structure under a project looks like this:

```
~/.claude/projects/Users-vlad-projects-my-app/
├── default.jsonl          # Main conversation
├── agent-a1b2c3d4.jsonl   # Subagent session (Task tool)
├── agent-e5f6g7h8.jsonl   # Another subagent
└── ...
```

Claude spawns subagent sessions when it uses the Task tool internally. Each gets its own `agent-*` prefixed JSONL file. These are implementation artifacts, not user-facing conversations. Claudebin filters them out and picks the most recent non-agent session by `mtime`:

```typescript
const sessionDir = path.join(
  os.homedir(), ".claude", "projects",
  normalizeProjectPath(projectPath)
);

const files = await fs.readdir(sessionDir);
const jsonlFiles = files
  .filter(f => f.endsWith(".jsonl") && !f.startsWith("agent-"));

const withStats = await Promise.all(
  jsonlFiles.map(async (f) => ({
    name: f,
    mtime: (await fs.stat(path.join(sessionDir, f))).mtimeMs,
  }))
);
withStats.sort((a, b) => b.mtime - a.mtime);
const content = await fs.readFile(
  path.join(sessionDir, withStats[0].name), "utf-8"
);
```

The JSONL content itself is a sequence of message objects: user messages, assistant responses, tool calls, tool results. Each line is independently valid JSON, which means you can process sessions line-by-line without loading the entire file into a parsed object graph. Claudebin doesn't take advantage of this today. It reads the full file as a UTF-8 string and sends it as-is to the backend for parsing. The backend handles the JSONL-to-rendered-HTML transformation.

### The Memory Trade-off

Reading the entire file into a single `string` allocation means the V8 heap needs to hold the full session content. Node.js strings are UTF-16 internally, so a 50MB UTF-8 file becomes ~100MB of heap. Add the JSON serialization for the HTTP request body and you're looking at ~200MB peak allocation for a max-size session. The `--max-old-space-size` default of 4GB means this isn't a practical concern, but it's the kind of detail that matters if you're building for constrained environments.

A streaming alternative would use `fs.createReadStream()` piped through a multipart upload. The backend would need to accept chunked transfers and reassemble. For claudebin's typical session size (100KB-5MB), the complexity wasn't justified. The 50MB client-side limit exists as a safety valve.

## Device Authorization: Auth Without a Redirect URI

MCP servers run inside a terminal. There's no browser window to redirect to, no localhost server to catch an OAuth callback. The standard Authorization Code flow with PKCE doesn't work because there's no redirect URI.

Claudebin uses a pattern similar to [RFC 8628 (Device Authorization Grant)](https://datatracker.ietf.org/doc/html/rfc8628): the server generates a one-time code, opens the user's browser to a verification page, and polls for completion.

The flow in detail:

```
Plugin                         Backend                      Browser
  │                              │                            │
  ├── POST /api/auth/start ────→ │                            │
  │                              ├── Generate code + URL      │
  ← { code: "abc", url: "..." } │                            │
  │                              │                            │
  ├── exec("open", url) ────────────────────────────────────→ │
  │                              │                            ├── User logs in
  │                              │ ←── POST /api/auth/verify ─┤
  │                              ├── Mark code as verified    │
  │                              │                            │
  ├── GET /api/auth/poll?code= → │                            │
  │   (every 2s, up to 5min)     ├── Code verified?           │
  ← { accessToken, refreshToken, │   Yes → return tokens      │
  │   expiresAt }                │                            │
```

The one-time `code` is the correlation key between the CLI process and the browser session. It's generated server-side, never sent over the browser URL as a secret. The URL contains the code for the user to verify, but the actual token exchange happens server-to-server on the poll endpoint.

```typescript
async function authenticateViaBrowser(): Promise<AuthTokens> {
  const { code, authUrl } = await api.startAuth();
  await openUrl(authUrl);

  return poll<AuthTokens>({
    fn: () => api.pollAuth(code),
    isReady: (result) => result !== null,
    interval: AUTH_POLL_INTERVAL,    // 2 seconds
    timeout: AUTH_TIMEOUT,           // 5 minutes
    timeoutError: "Authentication timed out",
  });
}
```

Cross-platform URL opening is one of those details that looks trivial but has edge cases:

```typescript
async function openUrl(url: string): Promise<void> {
  const escaped = url.replace(/"/g, '\\"');
  const cmd = process.platform === "darwin"
    ? `open "${escaped}"`
    : process.platform === "win32"
      ? `start "" "${escaped}"`
      : `xdg-open "${escaped}"`;

  exec(cmd);
}
```

The Windows `start` command needs an empty string as the window title before the URL. Without it, URLs containing spaces or special characters are misinterpreted as the title argument. The shell escaping handles URLs with query parameters, but there are known issues with URLs containing single quotes on Linux where `xdg-open` passes through `sh -c`.

### Token Lifecycle and Secure Storage

Nobody wants to open a browser every time they share a session. Claudebin implements a three-tier token resolution strategy:

```typescript
async function getValidToken(): Promise<string> {
  const config = loadConfig();

  // Tier 1: Valid cached token
  if (config.accessToken && !isExpiringSoon(config.expiresAt)) {
    return config.accessToken;
  }

  // Tier 2: Refresh expired token
  if (config.refreshToken) {
    const refreshed = await api.refreshToken(config.refreshToken);
    if (refreshed) {
      saveConfig(refreshed);
      return refreshed.accessToken;
    }
  }

  // Tier 3: Full browser auth flow
  return authenticateViaBrowser();
}
```

The `isExpiringSoon` check uses a 5-minute buffer (`TOKEN_REFRESH_BUFFER_MS = 300_000`). If your token expires in 4 minutes, the refresh happens proactively rather than failing mid-upload. This is important because session publishing involves a multi-step sequence (upload, then poll for processing) and a token that expires between those steps would leave the session in a partially-published state.

Tokens are persisted to `~/.claudebin/config.json`:

```typescript
function saveConfig(tokens: AuthTokens): void {
  const dir = path.join(os.homedir(), ".claudebin");
  fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
  fs.writeFileSync(
    path.join(dir, "config.json"),
    JSON.stringify(tokens),
    { mode: 0o600 }
  );
}
```

The `0o700` directory permission and `0o600` file permission restrict access to the current user only. This is the same pattern SSH uses for `~/.ssh/`. On macOS and Linux, this prevents other users on a shared machine from reading your tokens. On Windows, these permissions are effectively ignored. `fs.writeFileSync` doesn't enforce POSIX permissions on NTFS. A more robust Windows implementation would use ACLs via `icacls`, but that's outside claudebin's scope for now.

The access token TTL is 1 hour. The refresh token has a longer lifetime (server-configured). If the refresh token is also expired or revoked, the full browser flow triggers again. In practice, most users hit Tier 1 (cached token) for weeks before needing a refresh.

## Generic Polling with Typed Callbacks

Both auth and session publishing use async polling. The backend processes sessions asynchronously (parsing JSONL, rendering syntax-highlighted HTML, generating metadata), and the client needs to wait. Rather than duplicate the retry logic, claudebin uses a generic `poll<T>()` utility parameterized over the result type:

```typescript
interface PollOptions<T> {
  fn: () => Promise<T | null>;
  isReady: (result: T | null) => result is T;
  interval: number;
  timeout: number;
  timeoutError: string;
}

async function poll<T>(opts: PollOptions<T>): Promise<T> {
  const deadline = Date.now() + opts.timeout;

  while (Date.now() < deadline) {
    try {
      const result = await opts.fn();
      if (opts.isReady(result)) return result;
    } catch {
      // Transient network errors: retry silently
      // Fatal errors (4xx): fn should throw a non-retryable error
    }
    await new Promise(r => setTimeout(r, opts.interval));
  }

  throw new Error(opts.timeoutError);
}
```

The `isReady` callback uses a TypeScript type guard (`result is T`). This narrows the return type so callers get `T`, not `T | null`. The two polling sites configure different parameters:

| Use case | Interval | Timeout | Rationale |
|----------|----------|---------|-----------|
| Auth completion | 2s | 5min | User may be slow logging in, typing 2FA |
| Session processing | 2s | 2min | Backend parsing shouldn't take longer |

The error handling inside the loop is intentionally coarse. Network errors (DNS failure, connection reset, 502) are swallowed and retried. The next poll attempt will likely succeed. This is a pragmatic choice: distinguishing transient from fatal errors in a `fetch()` call is surprisingly complex (is a 500 transient or permanent? depends on the backend). The timeout acts as the safety net.

There's no backoff. The 2-second fixed interval means claudebin generates at most 30 requests/minute against the backend during a poll. For a single-user CLI tool, this is negligible. A client library serving thousands of concurrent users would need exponential backoff with jitter, but that's a different problem.

### Why Not WebSockets?

WebSockets would eliminate the polling latency entirely. The backend pushes a notification when processing is complete. But they introduce:

1. **Connection lifecycle management.** Heartbeats, reconnection, state synchronization after disconnect.
2. **Infrastructure complexity.** WebSocket connections are stateful. Load balancers need sticky sessions or a pub/sub layer (Redis, NATS).
3. **Client complexity.** The MCP server would need to maintain a persistent WebSocket alongside the stdio event loop.

For a flow where the user waits 5-15 seconds, adding 0-2 seconds of polling overhead doesn't justify the architectural cost. The polling implementation is 20 lines. A robust WebSocket client is 200+.

## The Indirection Problem: Why This Architecture Frustrates Me

Let me be honest about the developer experience. Here's what happens when a user types `/claudebin:share` in Claude Code:

```
User types "/claudebin:share"
  → Claude reads commands/share.md (a markdown file with YAML frontmatter)
  → Markdown body becomes instructions injected into Claude's context
  → Claude interprets the instructions and decides to call the MCP tool
  → Claude constructs a tools/call JSON-RPC message
  → Message is serialized, newline-terminated, written to the child process's stdin
  → MCP SDK deserializes, validates against Zod schema, dispatches to handler
  → Handler runs, returns result
  → Result serialized back over stdout as JSON-RPC response
  → Claude reads the response and formats it for the user
```

That's **four layers of indirection** between "user wants to share" and "code runs." A markdown file instructs an LLM to construct a JSON-RPC message to send over stdio to a child process that validates it with Zod before executing a function.

Compare this to how OpenCode (the platform [micode](https://github.com/vtemian/micode) extends) handles the same concept:

```
User types "/init"
  → Command config maps "/init" to agent "project-initializer" with a template
  → Agent receives the template as a prompt
  → Agent calls tools directly via typed function dispatch
```

In OpenCode, a tool is a TypeScript function registered in-process:

```typescript
import { tool } from "@opencode-ai/plugin/tool";

export const ast_grep_search = tool({
  description: "Search code patterns using AST-aware matching",
  args: {
    pattern: tool.schema.string().describe("AST pattern"),
    lang: tool.schema.enum(LANGUAGES).describe("Target language"),
  },
  execute: async (args, context) => {
    const result = await runSg(args);
    return formatMatches(result.matches);
  },
});
```

No IPC. No serialization boundary. No child process. The tool runs in the same process as the agent, with full access to the `ToolContext` (session ID, abort signals, permission prompts). The agent calls the tool, the tool returns a string. One hop.

Commands map directly to agents with a template:

```typescript
config.command = {
  init: {
    description: "Initialize project",
    agent: "project-initializer",
    template: `Initialize this project. $ARGUMENTS`,
  },
};
```

No intermediate markdown file that an LLM has to interpret. No hope that the model correctly infers `project_path` from context. The routing is deterministic.

### Where MCP Pays Its Indirection Tax

The cost of MCP's architecture shows up in specific, concrete ways:

**Debugging is painful.** When your tool doesn't receive the right arguments, you have to figure out which layer failed. Did Claude misinterpret the slash command markdown? Did it construct the wrong arguments? Did the JSON-RPC serialization lose something? Did Zod reject a valid input? Each layer has its own failure mode, and `console.log` goes to stderr (not stdout, remember, stdout is the JSON-RPC channel). You end up writing to a debug file and tailing it in another terminal.

**Latency is visible.** The LLM has to reason about which tool to call, construct the arguments, and generate the JSON. All of which costs tokens and time. In OpenCode, tool dispatch is a function lookup in a hash map. In MCP, it's an LLM inference step. For claudebin's single-tool use case, this overhead is ~1-2 seconds of model thinking time before the actual work starts.

**State sharing is impossible.** Each MCP server runs in its own process. If two MCP tools need to share state (say, an auth token) they can't. They have to go through the filesystem or an external service. OpenCode plugins run in-process and share the plugin context object directly.

**Error recovery depends on the model.** If an MCP tool returns `isError: true`, Claude has to decide what to do. Maybe it retries. Maybe it tells the user. Maybe it hallucinates a workaround. In OpenCode, error handling is programmatic. The agent's prompt can include explicit retry logic, or the tool can throw a typed error that the orchestrator catches.

### Where MCP Earns Its Keep

There's no silver bullet, and MCP's indirection buys real things:

**Language agnosticism.** Claudebin is TypeScript. My [booking-mcp](https://github.com/vtemian/dd/tree/main/tools/booking-mcp) server is Python with Playwright. My [whoop-mcp](https://github.com/vtemian/dd/tree/main/tools/whoop-mcp) server is also Python. MCP doesn't care. If it speaks JSON-RPC over stdio, it works. OpenCode plugins must be JavaScript/TypeScript compiled for Bun. If your tool needs Python (ML inference, browser automation with Playwright, scientific computing), you're wrapping it in a subprocess anyway.

**Process isolation.** An MCP server that crashes doesn't take down Claude Code. A segfaulting native module in an OpenCode plugin kills the entire process. For tools that do dangerous things (browser automation, shell execution, network scraping), isolation isn't overhead. It's a feature.

**Ecosystem portability.** An MCP server works with Claude Code, Cursor, Windsurf, Zed, and any other client that implements the protocol. An OpenCode plugin works with OpenCode. I've shipped 3 MCP servers that work across editors. That portability has real value.

**Composability without coordination.** Claude can orchestrate multiple MCP tools from different authors without those tools knowing about each other. The LLM acts as the integration layer. In OpenCode, composing tools across plugins requires the plugin authors to agree on interfaces, or the orchestrator agent needs explicit knowledge of each tool's behavior.

### The Honest Assessment

MCP is the right choice when you're building tools for a broad ecosystem and you value portability over performance. It's the wrong choice when you're building a tightly integrated agent system where latency, state sharing, and deterministic dispatch matter.

I've shipped MCP servers and OpenCode plugins. The MCP developer experience is worse for simple tools. Too much ceremony, too many layers. But for tools that need to work everywhere and can't assume a specific runtime, it's the only game in town.

The real question is whether the industry converges on MCP as the universal standard (like LSP did for language servers) or whether competing plugin models fragment the ecosystem. Right now, Anthropic's push for MCP has momentum. But if I'm building a tool that only needs to work in one editor, I'd skip MCP and go direct every time.

## Bundling: Zero-Install Distribution

MCP servers need to work on any machine with Claude Code installed. You can't assume the user has run `npm install` or even has your dependencies available. Claudebin solves this by bundling everything into a single JavaScript file using tsup:

```typescript
// tsup.config.ts
export default defineConfig({
  entry: ["src/index.ts"],
  format: ["esm"],
  target: "es2022",
  noExternal: [/.*/],  // Bundle ALL dependencies
});
```

The `noExternal: [/.*/]` regex tells tsup to inline every dependency (the MCP SDK, Zod, and all transitive dependencies) into a single output file. The result is a self-contained `dist/index.js` that runs with `node dist/index.js` and nothing else.

This matters because the alternative is shipping a `node_modules` directory (or requiring the user to `npm install`). The MCP SDK alone pulls in `content-type`, `raw-body`, `eventsource`, and several other packages. Bundling eliminates version conflicts between plugins. If two MCP servers depend on different Zod versions, they each have their own copy inlined.

The trade-off: the bundle is larger (~200KB vs ~15KB of source). And tree-shaking doesn't help much because the MCP SDK's module structure doesn't support dead code elimination well. You're shipping the full SDK even though claudebin only uses `McpServer` and `StdioServerTransport`.

The `.mcp.json` file tells Claude Code how to spawn the server:

```json
{
  "mcpServers": {
    "claudebin": {
      "command": "node",
      "args": ["dist/index.js"],
      "type": "stdio"
    }
  }
}
```

Claude Code reads this on startup, spawns `node dist/index.js` as a child process, connects stdin/stdout pipes, and sends the `initialize` handshake. The `type: "stdio"` is currently the only supported transport for local MCP servers. HTTP-based transports exist in the spec but aren't used by Claude Code for plugins.

Compare this to OpenCode's distribution model: plugins are npm packages loaded at runtime via Bun's module resolution. `"plugin": ["micode"]` in the config triggers `import("micode")`. No bundling needed. Bun resolves the package from `node_modules`. The downside is you need `npm install` or `bun add` as a setup step. The upside is you get proper tree-shaking, shared dependencies, and hot-reloading during development.

## Slash Commands: LLM as Dispatch Layer

MCP tools are powerful but not discoverable. Users don't know what tools exist unless they ask Claude or read docs. Slash commands bridge this gap, but the way they work reveals a fundamental architectural choice.

Claudebin registers `/claudebin:share` through a markdown file in the `commands/` directory:

```yaml
---
name: share
description: Share the current session to claudebin.com
allowed-tools:
  - mcp: claudebin
---

Share the current Claude Code session to Claudebin.
Authenticates automatically if needed.
```

The YAML frontmatter defines command metadata and permissions. The `allowed-tools` field is a security boundary. It restricts which MCP tools this command can invoke, preventing the markdown body from instructing Claude to call arbitrary tools.

The markdown body is the interesting part. It's not a function call. It's not a routing directive. It's **natural language instructions injected into Claude's context**. When the user types `/claudebin:share`, Claude reads this markdown and decides, through inference, to call the `share` MCP tool with the current project path.

This means the "dispatch" is non-deterministic. Claude usually gets it right, but the path from slash command to tool invocation goes through the model's reasoning. If the instructions are ambiguous, Claude might ask clarifying questions instead of calling the tool. If the model is having a bad day, it might pass the wrong arguments.

OpenCode's command system is deterministic:

```typescript
init: {
  description: "Initialize project",
  agent: "project-initializer",
  template: `Initialize this project. $ARGUMENTS`,
}
```

`/init` always routes to `project-initializer`. Always. The template is filled with `$ARGUMENTS` via string substitution, not LLM inference. The agent receives the prompt and runs. There's no intermediate interpretation step.

The trade-off: Claude Code's approach is more flexible. A slash command can orchestrate complex multi-tool workflows through natural language instructions without writing routing code. OpenCode's approach is more reliable. The mapping from command to agent is a direct lookup, not a model inference. For a single-tool plugin like claudebin, the flexibility is wasted. For a hypothetical plugin that needs to conditionally call different tools based on project state, Claude's interpretation layer would shine.

## What I'd Do Differently

**Add tests from day one.** The codebase is 600 lines of TypeScript with zero tests. For a v1 that shipped quickly, that was a conscious trade-off. But the path normalization logic, token lifecycle management, and file filtering are all pure functions that are trivial to unit test and painful to debug in production. The first bug report I got was a path normalization edge case on Windows. Tests would have caught it.

**Consider streaming for large sessions.** The current approach reads the entire session into a V8 string, which means ~2x the file size in heap due to UTF-16 encoding. A `ReadableStream` piped through a multipart upload would handle arbitrarily large sessions with constant memory. The backend already accepts chunked transfers.

**Build a local preview.** Right now, you publish to see what your session looks like rendered. A local preview mode (even just a `localhost:3000` server that renders the JSONL) would tighten the feedback loop significantly.

**Abstract the polling into a cancellable operation.** The current `poll()` doesn't support cancellation. If the user hits Ctrl+C during a 5-minute auth timeout, the process exits uncleanly. An `AbortController` integration would let the polling loop respond to signals gracefully.

## The Takeaway: 600 Lines, Four Layers, One URL

The entire claudebin MCP server is ~600 lines of TypeScript across 8 files. It handles device authorization, session extraction from an undocumented local format, async publishing with typed polling, and cross-platform URL opening. The MCP SDK handles the protocol plumbing (JSON-RPC framing, capability negotiation, schema generation) so your code focuses on domain logic.

But those 600 lines sit inside an architecture that's both impressive and frustrating. MCP gives you language-agnostic tool definition, process isolation, and cross-editor portability. It also gives you four layers of indirection, non-deterministic dispatch, and a debugging experience that makes you miss `console.log`.

I've shipped 3 MCP servers (claudebin, [booking-mcp](https://github.com/vtemian/dd/tree/main/tools/booking-mcp), [whoop-mcp](https://github.com/vtemian/dd/tree/main/tools/whoop-mcp)) and an [OpenCode plugin](https://github.com/vtemian/micode) with 22 agents and direct tool dispatch. Both models work. MCP wins on portability and isolation. Direct plugins win on latency, debuggability, and developer experience.

If you're building a tool that needs to work across Claude Code, Cursor, and Zed, MCP is the right choice. The ceremony is the price of admission. If you're building for a single platform and you want tight integration with the agent runtime, skip the protocol layer and go direct.

MCP is to agent tooling what REST was to web services in 2008. It's not perfect. It's verbose. The indirection feels unnecessary for simple cases. But it's becoming the standard, and building against a standard, even an imperfect one, compounds over time.

The code is open source at [github.com/wunderlabs-dev/claudebin](https://github.com/wunderlabs-dev/claudebin). If you're building your own MCP plugin, steal whatever's useful.

Stay curious ☕
