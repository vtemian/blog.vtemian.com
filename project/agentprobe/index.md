---
title: "agentprobe: real-time observability for Cursor, Claude Code and other AI agents"
date: 2026-03-09
author: Vlad Temian
url: https://blog.vtemian.com/project/agentprobe/
description: "Monitor AI coding agents like Cursor and Claude Code in real-time. AgentProbe is a TypeScript library that parses transcripts into event streams for dashboards, TUIs, and multi-agent monitoring."
tags: [ai, tools, open-source, agentic-programming, typescript, observability]
---

# agentprobe: real-time observability for Cursor, Claude Code and other AI agents


You want to build a dashboard that shows what your coding agents are doing. Or a TUI. Or a Cursor plugin. Or an OpenCode extension. The biggest challenge with AI agents today is **trust**. How do you know what your agent is doing when it's deep in a 50-file refactoring? You need a clean, real-time stream of agent state: who's running, who's idle, who just finished, who just failed.

Every AI coding tool stores transcripts differently. **Cursor** dumps JSONL files with mixed formats. **Claude Code** has its own structure. **OpenCode** another. Parsing each one, tracking state changes, and handling edge cases is plumbing you shouldn't repeat in every tool you build.

**[AgentProbe](https://github.com/vtemian/agentprobe)** is a TypeScript library that handles the plumbing. Transcripts in, normalized events out. Building blocks for whatever you want to build on top.

## Passive Observability: Why We Parse Transcripts

Most observability tools like LangSmith or AgentOps require "active" instrumentation. You have to wrap your LLM calls or instrument the agent's code. But what if you don't own the code?

Tools like **Cursor** and **Claude Code** are proprietary or complex to modify. You can't easily inject tracing code into them. **AgentProbe** takes a different approach: **Passive Observability**. It watches the artifacts these tools *already* leave behind (transcripts, logs, files) and reconstructs the agent's lifecycle from those signals.

This makes it the perfect library for building **Cursor plugins**, **AI dashboards**, or **multi-agent orchestration hooks** without needing to modify the agents themselves.

## Building Blocks, Not a Product

AgentProbe isn't a tool you run. It's a library other tools import. A few lines to start monitoring your workspace:

```typescript
import { createObserver } from "@agentprobe/core";

const observer = createObserver({
  workspacePaths: ["/path/to/your/project"],
});

observer.subscribe((event) => {
  // Real-time events for Cursor, Claude Code, and more
  console.log(event.change.kind, event.agent.id, event.agent.status);
});

await observer.start();
```

Single `subscribe()` call. One event shape with `change`, `agent`, and `snapshot`. No ceremony.

Factory functions, not classes. Dual ESM and CJS builds. Full TypeScript types with declaration maps. Zod validation at provider boundaries. Published on npm as `@agentprobe/core` with three entry points: the full package (defaults to Cursor), a core-only import for custom providers, and individual provider imports.

## Observe Any Agent: Cursor, Claude Code, and OpenCode Support

The library separates the runtime from the data source. The core knows how to watch, diff, and emit events. Providers know how to find and parse transcripts. The two connect through a single interface: `TranscriptProvider`.

Every provider implements the same pipeline:

| Step | Responsibility |
|------|---------------|
| **discover** | Find transcript sources (files, APIs, sockets) |
| **read** | Load and parse raw transcript data |
| **normalize** | Transform into canonical agent snapshots |
| **watch** *(optional)* | Subscribe to filesystem or stream changes |

**Cursor** is the first fully supported provider. **Claude Code**, **OpenCode**, and **Codex** are next. The consumer code doesn't change. Swap the provider, keep the same event stream.

## Normalized Event Data: What Comes Out

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

### Status Inference

Status inference is the tricky part. Not every tool reports explicit agent state. Cursor's conversation-only transcripts, for example, contain no status field at all. AgentProbe derives status from conversation patterns: recent assistant activity means "running," error keywords mean "error," completion phrases followed by silence mean "completed." Time-based quiet windows (5s for streaming, 30s for agent completion) handle the transitions. The consumer gets a clean `running | idle | completed | error` regardless of how messy the source data is.

## What You Can Build with AgentProbe

AgentProbe is infrastructure for the next generation of AI agent developer tools:

- **Cursor plugins** that show agent activity in the sidebar
- **OpenCode extensions** with real-time agent status
- **TUIs** that visualize multiple agents across workspaces
- **Dashboards** like Cursor Cafe, where you showcase what your agents are working on
- **Notification systems** that alert when an agent errors or completes
- **Orchestration hooks** that trigger the next step when an agent finishes

The library handles transcript discovery, incremental parsing, file watching with debounce, and concurrency safety via monotonic lifecycle tokens. You focus on the experience.

## Frequently Asked Questions (FAQ)

### How do I monitor Cursor agent activity?
You can use AgentProbe to watch the `.cursor` directory in your workspace. It parses the JSONL transcript files and emits real-time events whenever the agent starts or stops working.

### Can I track multi-agent workflows?
Yes. AgentProbe is designed for multi-agent environments. It tracks individual agents by ID and can distinguish between sub-agents and main agents across multiple workspace paths.

### Is AgentProbe open-source?
Yes, AgentProbe is MIT licensed and available on GitHub and npm.

---

**[Source on GitHub](https://github.com/vtemian/agentprobe)** · **[npm: @agentprobe/core](https://www.npmjs.com/package/@agentprobe/core)**

For the structured workflow that AgentProbe can observe, including context harnessing, planning, and parallel execution, see [micode](/project/micode/). For brainstorming in a browser UI, see [octto](/project/octto/).

Stay curious ☕

