---
title: "zag: a composable agent development environment, built in Zig"
date: 2026-06-03T00:00:00+03:00
lastmod: 2026-06-03T00:00:00+03:00
description: "A terminal-native AI coding agent built in Zig, where the window system is the platform. Modal vim editing, embedded Lua plugins, and a separate agent in every pane."
keywords:
    - zag
    - ai coding agent
    - terminal ai agent
    - zig ai agent
    - composable agent environment
    - neovim for ai agents
    - modal ai agent
    - lua plugin agent
    - tui ai agent
    - multi-pane ai agent
    - claude code alternative
    - opencode alternative
    - vim ai agent
    - agent window system
tags:
    - ai
    - tools
    - open-source
    - agentic-programming
    - zig
    - tui
images:
    - og.png
---

<video controls playsinline width="100%" style="margin-bottom: 2rem;">
  <source src="demo.mp4" type="video/mp4">
</video>

This is a personal, highly opinionated project in heavy development. I'm building it because I want to, the way you'd restore an old motorcycle in a garage. It's slow on purpose. If you're reading this, you're early.

**[zag](https://github.com/vtemian/zag)** is an AI coding agent where the window system is the platform. Almost every agent today owns the whole screen: one view, one conversation, navigation that replaces everything underneath it. zag inverts that. Splits, focus, and buffers are primitives the core guarantees. Everything above them, from the session tree to how a response renders to which system prompt a model gets, is a plugin.

Think Neovim's architecture, applied to AI agents.

## The Window System Is the Platform

Most agent TUIs are built around a single view. One pane owns the terminal, and moving somewhere new means tearing down what was there. That's a fine model for a chat box. It's a ceiling for anything ambitious, because plugins can never render their own UI; they can only feed text into the one view that exists.

zag starts from the opposite assumption. The core provides four things and stays out of the way for everything else:

| Layer | What the core owns |
|-------|--------------------|
| **Window system** | Binary-tree splits, focus, vim `h`/`j`/`k`/`l` navigation, floating windows |
| **Buffer abstraction** | A window holds a buffer; the core doesn't know or care what's inside |
| **Agent loop** | The LLM conversation engine: tools, streaming, conversation state |
| **Terminal rendering** | A selective dirty-rectangle ANSI diff renderer |

A buffer is a runtime-polymorphic interface: a pointer plus a vtable for rendering lines, handling keys, and reacting to resize and focus. The conversation view is just one implementation. So are scratch, text, and image buffers. The session sidebar, a git panel, a file browser: those aren't features zag ships. They're buffers a plugin writes. The parallel to Neovim is deliberate, where NERDTree, Fugitive, and Telescope are all plugins precisely because the editor never cared what lived inside a window.

This is the architecture I once proposed for an existing agent and couldn't build there, because its single-view routing was the wrong foundation. zag starts on the right one.

## A Separate Agent in Every Pane

Because panes are first-class, so are the agents inside them. In the demo above I split the screen and each pane runs its own agent loop on its own thread: its own LLM call, its own parallel tool execution, its own streaming response. Different panes can run different models at the same time. A Vim-style `/model` picker swaps provider and model mid-session, cancels the in-flight turn cleanly, and persists the choice.

The whole thing is modal. Sessions start in **insert** mode, where typing goes to the prompt. Press `Esc` for **normal** mode, where the same keys fire window bindings instead. Watch the keystroke overlay in the demo: `h`/`j`/`k`/`l` to move focus, `v`/`s` to split, all composable and all rebindable from a config file. No agent I know of treats modal interaction as a first-class concept. It should be.

## Why Zig

There's no silver bullet here, and the trade-off is real: Zig is a young language with a small ecosystem, and I'm learning it as I go. What I get in return is a single native binary with no runtime, small enough to ship as one file, with direct C interop and no FFI overhead when I need to call the operating system.

That last part matters more than it sounds. Kernel-level sandboxing, for instance, is a few syscalls away rather than a dependency. zag wraps `bash` in a macOS seatbelt profile or a Linux Landlock plus seccomp ruleset that denies access to your secrets by default. Terminal emulation comes from libghostty-vt, the battle-tested, SIMD-optimized core behind Ghostty, which means proper Unicode, grapheme clustering, and wide-character handling instead of a hand-rolled approximation.

## Everything Above the Primitives Is Lua

zag embeds Lua 5.4 and an async runtime. Blocking work (HTTP, subprocess, filesystem, an LLM call) runs on a worker pool and resumes your coroutine back on the main thread, so nothing stalls the UI. The model is, again, Neovim's: your `config.lua` is trusted code, and the plugin surface is wide.

You can register custom tools, define new providers, and hook thirteen agent events to observe, veto, or rewrite them. Blocking a destructive command is a few lines:

```lua
zag.hook("ToolPre", { pattern = "bash" }, function(evt)
  if evt.args.command:match("rm %-rf") then
    return { cancel = true, reason = "refused destructive rm" }
  end
end)
```

Tools, keymaps, slash commands, prompt layers, subagent definitions, and the window API are all reachable from Lua. The session sidebar and the model picker that ship with zag are themselves written against that surface, not baked into the core. That's the test: if the built-in views can't be expressed as plugins, the platform isn't real.

## What Runs Today

zag is early, but it isn't a sketch. What actually works:

- **Eight providers across three wire formats.** Anthropic Messages, OpenAI Chat Completions, and the OpenAI Responses API, covering Claude, GPT, OpenRouter, Groq, Moonshot (Kimi), and local Ollama, with OAuth sign-in for Claude Max/Pro and ChatGPT.
- **Per-pane streaming agents** with parallel tool execution and cooperative `Ctrl+C` cancellation.
- **Mid-turn steering.** Type while a turn is running and your message is queued as a system-reminder interrupt instead of dangling at the end.
- **Automatic context compaction**, a predictive cascade that keeps long sessions inside the window before they overflow.
- **Subagent delegation** via a built-in `task` tool, with per-subagent prompts, models, and tool allowlists.
- **Crash-safe sessions** as append-only JSONL with tail-only recovery and a browsable sidebar.
- **A headless eval mode and a PTY-driven simulator** that drive the real binary end to end against your real provider. No LLM mocks.

## Running It

```bash
zig build run     # first run drops into a provider onboarding wizard
```

On a clean machine zag walks you through picking a provider and model, stores credentials with mode `0600`, scaffolds a config, and drops you into the TUI. Source, build instructions, and the design devlog are on GitHub.

## What's Next

This is a rough shape, not a promise: a tree-sitter buffer for syntax-aware code browsing, domain buffers for git and diagnostics shipped as plugins, and libghostty-vt promoted to the main terminal backend. The active design work lives in the repo's plans directory, where I write down the trade-offs and the reasoning, not just the what.

---

**[Source on GitHub](https://github.com/vtemian/zag)** · Built with Neovim, Ghostty, and a lot of patience as inspiration. MIT licensed.

For real-time observability of agents like this one, see [agentprobe](/project/agentprobe/). For the structured brainstorm, plan, and implement workflow I run on top of agents, see [micode](/project/micode/).

Stay curious ☕
