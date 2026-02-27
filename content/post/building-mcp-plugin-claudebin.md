---
title: "Building an MCP Plugin for Claude Code"
date: 2026-02-27T10:00:00+02:00
description: "A technical deep dive into building claudebin as an MCP server for Claude Code. Covers the JSON-RPC wire protocol, session extraction, device authorization, and an honest comparison with OpenCode's direct plugin model."
keywords:
    - mcp
    - model context protocol
    - claude code plugin
    - mcp server
    - json-rpc
    - claudebin
    - opencode
    - agentic programming
tags:
    - mcp
    - agentic-programming
    - typescript
    - deep-dive
---

Claude Code sessions live as `.jsonl` files under `~/.claude/projects/`. They're ephemeral. You debug a race condition, the agent rewrites three files, and then it's gone. [Claudebin](https://claudebin.com) turns any session into a shareable URL. Run `/claudebin:share`, get back a permanent link.

This post is about what's underneath. Building an MCP server, shipping it as a Claude Code plugin, and where the architecture shines vs where it falls apart.

## MCP: JSON-RPC 2.0 Over stdio

The [Model Context Protocol](https://modelcontextprotocol.io/) sits on top of [JSON-RPC 2.0](https://www.jsonrpc.org/specification). Claude Code spawns your server as a child process, pipes stdin/stdout, and exchanges newline-delimited JSON. No HTTP, no WebSockets, no port allocation. One child process per MCP server, lifecycle tied to the parent.

When Claude Code starts your server, it sends an `initialize` request:

```json
→ {"jsonrpc":"2.0","id":1,"method":"initialize","params":{
    "protocolVersion":"2024-11-05",
    "capabilities":{"roots":{"listChanged":true}},
    "clientInfo":{"name":"claude-code","version":"1.0.0"}}}

← {"jsonrpc":"2.0","id":1,"result":{
    "protocolVersion":"2024-11-05",
    "capabilities":{"tools":{}},
    "serverInfo":{"name":"claudebin","version":"1.0.0"}}}

→ {"jsonrpc":"2.0","method":"notifications/initialized"}
```

Capability negotiation. The client declares what it supports, the server responds with its own. Claudebin only declares `tools`. The third message is a notification (no `id`, no response expected), signaling the handshake is complete.

Then Claude discovers tools via `tools/list` and invokes them via `tools/call`. The tool response uses MCP's content block format:

```json
← {"jsonrpc":"2.0","id":3,"result":{
    "content":[{"type":"text","text":"https://claudebin.com/threads/abc123"}]}}
```

MCP separates *protocol errors* (malformed JSON-RPC) from *tool errors* (your code ran but failed). Tool errors return a successful response with `isError: true`. The distinction matters because Claude can reason about tool errors and retry. Protocol errors are opaque.

One gotcha with the long-lived process model: `console.log` goes to stdout and corrupts the JSON-RPC stream. This bites every new MCP developer. Use `console.error` for debugging.

## Session Extraction

The genuinely hard part of claudebin is figuring out where Claude stores sessions and extracting the right one.

Sessions are `.jsonl` files under `~/.claude/projects/`. The directory name is a normalized project path. `/Users/vlad/projects/my-app` becomes `Users-vlad-projects-my-app`. Every non-alphanumeric character maps to a dash:

```typescript
function normalizeProjectPath(projectPath: string): string {
  return projectPath.replace(/^\//, "").replace(/[^a-zA-Z0-9]/g, "-");
}
```

This is undocumented. I found it by reading Claude Code's source and verifying against the filesystem. Getting it wrong means a silent "session not found" error.

The directory contains multiple files:

```
~/.claude/projects/Users-vlad-projects-my-app/
├── default.jsonl          # Main conversation
├── agent-a1b2c3d4.jsonl   # Subagent session (Task tool)
├── agent-e5f6g7h8.jsonl   # Another subagent
```

Claudebin filters out `agent-*` files and picks the most recent by `mtime`. Each JSONL line is a self-contained message object (user message, assistant response, tool call, tool result). The file is read as a UTF-8 string and sent as-is to the backend for rendering.

The memory trade-off: Node.js strings are UTF-16 internally, so a 50MB session becomes ~100MB of heap. Add JSON serialization for the HTTP body and you hit ~200MB peak. A streaming upload would fix this, but for typical sessions (100KB-5MB) it wasn't worth the complexity. The 50MB limit is a client-side safety valve.

## Device Authorization

MCP servers run in a terminal. No browser window, no OAuth redirect URI. Claudebin uses a pattern similar to [RFC 8628 (Device Authorization Grant)](https://datatracker.ietf.org/doc/html/rfc8628):

```
Plugin                         Backend                      Browser
  │                              │                            │
  ├── POST /api/auth/start ────→ │                            │
  ← { code: "abc", url: "..." } │                            │
  ├── exec("open", url) ────────────────────────────────────→ │
  │                              │                    User logs in
  │                              │ ←── POST /api/auth/verify ─┤
  ├── GET /api/auth/poll?code= → │                            │
  │   (every 2s, up to 5min)     │                            │
  ← { accessToken, refreshToken }│                            │
```

The one-time code correlates the CLI and browser session. Tokens are cached in `~/.claudebin/config.json` with `0o600` permissions (same pattern as `~/.ssh/`). Before every share, claudebin checks the cached token. If it's within 5 minutes of expiry, it refreshes proactively rather than failing mid-upload.

Both auth and session publishing use async polling. Rather than duplicate the retry logic, claudebin has a generic `poll<T>()` with configurable interval, timeout, and a type guard callback. Auth polls for 5 minutes (user might be slow). Session processing polls for 2 minutes. No backoff, fixed 2-second interval. For a single-user CLI tool generating 30 req/min during a poll, this is fine.

Why not WebSockets? Connection lifecycle management, stateful load balancing, maintaining a persistent socket alongside the stdio event loop. The polling implementation is 20 lines. A robust WebSocket client is 200+. For a 5-15 second wait, 2 seconds of overhead is acceptable.

## The Indirection Problem

Let's be honest about what happens when a user types `/claudebin:share`:

```
"/claudebin:share"
  → Claude reads commands/share.md (markdown with YAML frontmatter)
  → Markdown body becomes instructions injected into Claude's context
  → Claude interprets instructions and decides to call the MCP tool
  → Claude constructs a tools/call JSON-RPC message
  → Serialized over stdio to the child process
  → MCP SDK deserializes, Zod validates, dispatches to handler
  → Handler runs, result serialized back
  → Claude reads response, formats for user
```

Four layers of indirection between "user wants to share" and "code runs."

Compare this to [OpenCode](https://opencode.ai/) (the platform [micode](https://github.com/vtemian/micode) extends):

```
"/init"
  → Command config maps to agent "project-initializer" with a template
  → Agent calls tools via typed function dispatch
```

In OpenCode, a tool is a TypeScript function registered in-process. No IPC, no serialization, no child process:

```typescript
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

Commands map deterministically to agents. `/init` always routes to `project-initializer`. Always. The template is filled via string substitution, not LLM inference.

In Claude Code, the slash command is natural language that Claude *interprets*. The dispatch is non-deterministic. Claude usually gets it right, but the path goes through model reasoning. If instructions are ambiguous, Claude might ask questions instead of calling the tool.

### The Trade-offs

|                       | MCP (Claude Code)          | Direct Plugin (OpenCode)        |
|-----------------------|----------------------------|---------------------------------|
| Tool dispatch         | LLM inference              | Hash map lookup                 |
| State sharing         | Filesystem/external only   | In-process context              |
| Language support      | Any (JSON-RPC over stdio)  | JS/TS only (Bun runtime)       |
| Process isolation     | Yes (child process)        | No (shared process)             |
| Portability           | Claude Code, Cursor, Zed...| OpenCode only                   |
| Debug experience      | Multi-layer, stderr only   | Standard debugging              |
| Latency overhead      | ~1-2s (model thinking)     | Negligible                      |

MCP earns its keep on language agnosticism and ecosystem portability. Claudebin is TypeScript. My [booking-mcp](https://github.com/vtemian/dd/tree/main/tools/booking-mcp) and [whoop-mcp](https://github.com/vtemian/dd/tree/main/tools/whoop-mcp) servers are Python with Playwright. MCP doesn't care. OpenCode plugins must be JS/TS compiled for Bun.

Process isolation matters too. An MCP server that crashes doesn't take down Claude Code. A segfaulting native module in an OpenCode plugin kills the entire process.

But the developer experience is worse. When your tool doesn't receive the right arguments, you have to figure out which of four layers failed. Did Claude misinterpret the markdown? Did it construct the wrong arguments? Did Zod reject valid input? You end up writing to a debug file and tailing it in another terminal because `console.log` corrupts stdout.

### The Honest Assessment

MCP is the right choice when you value portability over performance. It's the wrong choice when you need tight integration, state sharing, and deterministic dispatch.

I've shipped 3 MCP servers and an OpenCode plugin with 22 agents. If a tool needs to work across editors, MCP is the only game in town. If it only needs one platform, skip the protocol and go direct.

MCP is to agent tooling what REST was to web services in 2008. Verbose, imperfect, too much ceremony for simple cases. But it's becoming the standard. Building against a standard, even an imperfect one, compounds over time.

The code is at [github.com/wunderlabs-dev/claudebin](https://github.com/wunderlabs-dev/claudebin).

Stay curious ☕
