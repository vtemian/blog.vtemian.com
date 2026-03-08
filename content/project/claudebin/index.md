---
title: "claudebin: share and embed Claude Code sessions"
date: 2026-02-01T00:00:00+03:00
description: "claudebin: Publish, share, and embed Claude Code terminal sessions as permanent web URLs. The missing share button for agentic development."
keywords:
    - claudebin
    - claude code
    - agentic programming
    - mcp server
    - ai tools
    - session sharing
    - anthropic claude
    - share claude code
tags:
    - ai
    - tools
    - open-source
    - agentic-programming
    - mcp
images:
    - og.png
---

<video controls playsinline width="100%" style="margin-bottom: 2rem;">
  <source src="demo.mp4" type="video/mp4">
</video>

Claude Code sessions are high-value artifacts that live and die in the terminal. You spend an hour debugging a race condition with an agent, arrive at a clean solution, and then... it's gone. The JSONL files in `~/.claude/projects/` aren't something you can easily share with a colleague or link in a PR.

**[claudebin](https://claudebin.com)** is the "share button" for Claude Code.

## One Command, Permanent Link

```bash
/claudebin:share
```

The plugin authenticates via GitHub OAuth, extracts the current session, and returns a shareable, embeddable web URL. Full fidelity: prompts, responses, tool calls, bash outputs, and file edits are all preserved with syntax highlighting and structured formatting.

## The Technical Archaeology

Building claudebin required reverse-engineering how Claude Code manages local state. Sessions aren't stored with human-readable names; they're normalized project paths.

I found that `/Users/vlad/projects/my-app` maps to `-Users-vlad-projects-my-app` in the filesystem. Every non-alphanumeric character is a dash. Inside those folders, claudebin has to filter out ephemeral `agent-*` sub-sessions and pick the correct `default.jsonl` by `mtime`.

This is the "messy middle" of building for agentic tools. claudebin handles the project path normalization (Regex), file discovery, and memory-safe JSONL parsing so you don't have to.

## Embedding & Resuming

**Embed Everywhere:** select a message range and drop it into a blog post or documentation. The embed renders the conversation exactly as it appeared in the terminal.

**Resumable Sessions:** Every shared thread includes a command to resume it locally. See a cool approach? One command, and you're picking up where the original author left off in your own local terminal.

## Architecture

- **Web App:** Next.js, Supabase, Vercel. Handles rendering, search, and the embed API.
- **MCP Server:** A Node.js plugin that Claude Code pipes JSON-RPC to over stdio.
- **Title Generation:** An LLM pipeline analyzes the first few messages to generate a relevant, searchable title.

Built by [Vlad Temian](https://vtemian.com) and [Balaj Marius](https://balajmarius.com/) at [Wunderlabs](https://github.com/wunderlabs-dev). Free, MIT licensed, not affiliated with Anthropic.

**[Source on GitHub](https://github.com/wunderlabs-dev/claudebin.com)** | **[claudebin.com](https://claudebin.com)**

Stay curious ☕
