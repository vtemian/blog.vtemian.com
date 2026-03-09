---
title: "agentprobe: real-time observability library for AI coding agents"
date: 2026-03-09T00:00:00+03:00
description: "agentprobe is a TypeScript library that turns AI coding agent transcripts into normalized, real-time event streams. Provider-agnostic building blocks for dashboards, TUIs, Cursor plugins, OpenCode extensions, and multi-agent tooling."
keywords:
    - agentprobe
    - ai agent observability
    - coding agent monitoring
    - typescript observability library
    - cursor agent monitoring
    - claude code observability
    - opencode plugin
    - ai coding agent dashboard
    - multi-agent orchestration
    - real-time agent events
    - agent lifecycle events
    - provider agnostic ai tools
    - cursor plugin development
    - tui for coding agents
tags:
    - ai
    - tools
    - open-source
    - agentic-programming
    - typescript
images:
    - og.png
---

You want to build a dashboard that shows what your coding agents are doing. Or a TUI. Or a Cursor plugin. Or an OpenCode extension. The first thing you need is a clean, real-time stream of agent state: who's running, who's idle, who just finished, who just failed.

Every AI coding tool stores transcripts differently. Cursor dumps JSONL files with mixed formats. Claude Code has its own structure. OpenCode another. Parsing each one, tracking state changes, handling edge cases. That's plumbing you shouldn't repeat in every tool you build.

**[agentprobe](https://github.com/vtemian/agentprobe)** is a TypeScript library that handles the plumbing. Transcripts in, normalized events out. Building blocks for whatever you want to build on top.

## Building Blocks, Not a Product

agentprobe isn't a tool you run. It's a library other tools import. A few lines to start:

```typescript
import { createObserver } from "@agentprobe/core";

const observer = createObserver({
  workspacePaths: ["/path/to/your/project"],
});

observer.subscribe((event) => {
  console.log(event.change.kind, event.agent.id, event.agent.status);
});

await observer.start();
```

Single `subscribe()` call. One event shape with `change`, `agent`, and `snapshot`. No ceremony.

Factory functions, not classes. Dual ESM and CJS builds. Full TypeScript types with declaration maps. Zod validation at provider boundaries. Published on npm as `@agentprobe/core` with three entry points: the full package (defaults to Cursor), a core-only import for custom providers, and individual provider imports.

## Provider-Agnostic Core

The library separates the runtime from the data source. The core knows how to watch, diff, and emit events. Providers know how to find and parse transcripts. The two connect through a single interface: `TranscriptProvider`.

Every provider implements the same pipeline:

| Step | Responsibility |
|------|---------------|
| **discover** | Find transcript sources (files, APIs, sockets) |
| **read** | Load and parse raw transcript data |
| **normalize** | Transform into canonical agent snapshots |
| **watch** *(optional)* | Subscribe to filesystem or stream changes |

Cursor is the first provider. Claude Code, OpenCode, and Codex are next. The consumer code doesn't change. Swap the provider, keep the same event stream.

## What Comes Out

Every agent, regardless of source, is normalized into a canonical snapshot:

```typescript
interface CanonicalAgentSnapshot {
  id: string;
  name: string;
  kind: "local" | "remote";
  isSubagent: boolean;
  status: "running" | "idle" | "completed" | "error";
  taskSummary: string;
  startedAt?: number;
  updatedAt: number;
  source: string;
  metadata?: Record<string, unknown>;
}
```

On top of snapshots, the library emits lifecycle events: `joined`, `statusChanged`, `left`. Heartbeats are filtered out at the observer level so consumers only see meaningful changes. This diffing happens inside the library, not in your code.

Status inference is the tricky part. Not every tool reports explicit agent state. Cursor's conversation-only transcripts, for example, contain no status field at all. agentprobe derives status from conversation patterns: recent assistant activity means "running," error keywords mean "error," completion phrases followed by silence mean "completed." Time-based quiet windows (5s for streaming, 30s for agent completion) handle the transitions. The consumer gets a clean `running | idle | completed | error` regardless of how messy the source data is.

## What You Can Build

agentprobe is infrastructure. Here's what sits on top:

- **Cursor plugins** that show agent activity in the sidebar
- **OpenCode extensions** with real-time agent status
- **TUIs** that visualize multiple agents across workspaces
- **Dashboards** like Cursor Cafe, where you showcase what your agents are working on
- **Notification systems** that alert when an agent errors or completes
- **Orchestration hooks** that trigger the next step when an agent finishes

The library handles transcript discovery, incremental parsing, file watching with debounce, and concurrency safety via monotonic lifecycle tokens. You focus on the experience.

**[Source on GitHub](https://github.com/vtemian/agentprobe)** · **[npm: @agentprobe/core](https://www.npmjs.com/package/@agentprobe/core)**

For the structured workflow that agentprobe can observe, context harnessing, planning, and parallel execution, see [micode](/project/micode/). For brainstorming in a browser UI, see [octto](/project/octto/).

Stay curious ☕
