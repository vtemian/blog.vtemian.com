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

```mermaid
flowchart LR
    CC[Claude Code] -->|stdin: JSON-RPC| MCP[MCP Server process]
    MCP -->|stdout: JSON-RPC| CC
    CC -->|stdin: JSON-RPC| MCP2[Another MCP Server]
    MCP2 -->|stdout: JSON-RPC| CC
```

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

```mermaid
sequenceDiagram
    participant P as Plugin
    participant B as Backend
    participant Br as Browser

    P->>B: POST /api/auth/start
    B-->>P: { code, authUrl }
    P->>Br: exec("open", authUrl)
    Br->>B: User logs in + POST /api/auth/verify
    B->>B: Mark code as verified
    loop Every 2s, up to 5min
        P->>B: GET /api/auth/poll?code=abc
    end
    B-->>P: { accessToken, refreshToken, expiresAt }
```

The one-time code correlates the CLI and browser session. Tokens are cached in `~/.claudebin/config.json` with `0o600` permissions (same pattern as `~/.ssh/`). Before every share, claudebin checks the cached token. If it's within 5 minutes of expiry, it refreshes proactively rather than failing mid-upload.

Both auth and session publishing use async polling. Rather than duplicate the retry logic, claudebin has a generic `poll<T>()` with configurable interval, timeout, and a type guard callback. Auth polls for 5 minutes (user might be slow). Session processing polls for 2 minutes. No backoff, fixed 2-second interval. For a single-user CLI tool generating 30 req/min during a poll, this is fine.

Why not WebSockets? Connection lifecycle management, stateful load balancing, maintaining a persistent socket alongside the stdio event loop. The polling implementation is 20 lines. A robust WebSocket client is 200+. For a 5-15 second wait, 2 seconds of overhead is acceptable.

## Two Plugin Models, Two Philosophies

I've also built [micode](https://github.com/vtemian/micode), a plugin for [OpenCode](https://opencode.ai/) with 22 specialized agents. The experience of building for both platforms exposed a fundamental design disagreement about what a "plugin" should be.

In Claude Code, a plugin is a separate process that the LLM talks to over a protocol. In OpenCode, a plugin is code that runs inside the agent runtime. This isn't a minor implementation detail. It shapes everything.

```mermaid
flowchart LR
    subgraph Claude Code
        U1[User: /share] --> MD[Markdown file]
        MD --> LLM[LLM interprets]
        LLM --> RPC[JSON-RPC over stdio]
        RPC --> ZOD[Zod validates]
        ZOD --> FN1[Handler runs]
    end

    subgraph OpenCode
        U2[User: /init] --> CFG[Config lookup]
        CFG --> AGT[Agent receives prompt]
        AGT --> FN2[Tool executes]
    end
```

### Dispatch: Deterministic vs Probabilistic

When you type `/claudebin:share` in Claude Code, the slash command is a markdown file. Claude reads it, interprets the natural language instructions, and *decides* to call the MCP tool. The dispatch goes through model reasoning. It's probabilistic. Claude usually gets it right. Usually.

When you type `/init` in OpenCode, a config object maps the command to an agent:

```typescript
config.command = {
  init: {
    agent: "project-initializer",
    template: `Initialize this project. $ARGUMENTS`,
  },
};
```

String substitution. Hash map lookup. Deterministic. `/init` always routes to `project-initializer`. There is no interpretation step.

For claudebin, a single-tool plugin, this means Claude spends 1-2 seconds reasoning about which tool to call when there's only one option. That's model inference time burned on a decision with exactly one valid answer.

### Hooks: Observing vs Hoping

This is where the gap gets wide. OpenCode plugins have lifecycle hooks. You can intercept and modify behavior at 11+ points: before/after tool execution, on message receive, on context compaction, on permission prompts.

In micode, the `tool.execute.after` hook truncates tool output to stay within context limits. The `chat.params` hook injects project context files before each LLM call. The `experimental.chat.system.transform` hook modifies the system prompt dynamically based on what the agent is doing.

```typescript
return {
  "tool.execute.after": async (input, output) => {
    await tokenAwareTruncation(input, output);
    await artifactAutoIndex(input, output);
  },
  "chat.params": async (input, output) => {
    await injectProjectContext(input, output);
    await loadContinuityLedger(input, output);
  },
};
```

Claude Code plugins can't do any of this. Your MCP server is a black box behind a pipe. You get a request, you return a response. You can't observe what Claude is doing, intercept other tools, modify the system prompt, or react to session events. You can't even know how much context is left.

This matters in practice. Micode tracks file operations across tool calls and auto-indexes artifacts. It detects when context is running low and triggers a ledger dump. It enforces code style patterns by injecting constraints into the system prompt. None of this is possible through MCP. You'd have to rely on Claude's built-in behavior and hope it does the right thing.

### State: Shared vs Isolated

OpenCode plugins share the runtime. Tools access a `ToolContext` with session ID, abort signals, and plugin state. One tool can read what another tool wrote. Agents spawn subagents that inherit context.

MCP servers are isolated processes. If two tools need shared state, they go through the filesystem. There's no session context, no abort propagation, no shared memory. Claudebin manages its own auth state in `~/.claudebin/config.json` because there's nowhere else to put it.

For simple tools like claudebin, isolation is fine. You call one function, get one result. But for a system like micode where 22 agents coordinate, spawn subagents in parallel, share continuity ledgers, and track progress across tasks, process isolation would be a straitjacket.

### So Which One Wins?

Neither. They solve different problems.

|                       | MCP (Claude Code)          | Direct Plugin (OpenCode)        |
|-----------------------|----------------------------|---------------------------------|
| Tool dispatch         | LLM inference              | Hash map lookup                 |
| Lifecycle hooks       | None                       | 11+ hook points                 |
| State sharing         | Filesystem only            | In-process context              |
| Language support      | Any (JSON-RPC over stdio)  | JS/TS only (Bun runtime)       |
| Process isolation     | Yes                        | No                              |
| Portability           | Claude Code, Cursor, Zed   | OpenCode only                   |
| Agent orchestration   | Single agent, sequential   | Multi-agent, parallel spawning  |

MCP is the right model for tools. Standalone utilities that do one thing, work across editors, and benefit from isolation. A hotel scraper, a session sharer, a code search engine. Write it in any language, ship it everywhere.

OpenCode's model is the right one for agent systems. When you need hooks, state, parallel agents, deterministic routing, and deep integration with the runtime. When the plugin isn't a utility but a workflow engine.

The problem is that Claude Code only offers MCP. If you want to build anything beyond a simple tool, you're fighting the architecture. You can't observe, you can't intercept, you can't orchestrate. You get a pipe and a JSON schema.

OpenCode only offers direct plugins. If you want a Python tool, you're wrapping it in a subprocess yourself. If you want cross-editor portability, you're out of luck.

The ideal platform would offer both. MCP for portable tools, direct plugins for deep integration. Neither does that today.

The code is at [github.com/wunderlabs-dev/claudebin](https://github.com/wunderlabs-dev/claudebin).

Stay curious ☕
