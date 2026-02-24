---
title: "claudebin: share and embed Claude Code sessions"
date: 2026-02-01T00:00:00+03:00
description: "A free, open-source tool for publishing Claude Code terminal sessions as shareable, embeddable, and resumable web URLs. One command, permanent link."
images: []
keywords:
    - claudebin
    - claude code
    - agentic programming
    - ai tools
    - developer tools
    - session sharing
tags:
    - ai
    - tools
    - open-source
---

{{< github-stats repo="wunderlabs-dev/claudebin.com" >}}

<video controls playsinline width="100%" style="margin-bottom: 2rem;">
  <source src="demo.mp4" type="video/mp4">
</video>

Claude Code sessions live and die inside the terminal. You spend an hour debugging a tricky issue with an agent, arrive at a solution, and then there's no way to share the conversation. No way to link it in a PR description. No way to show a colleague how you got there. The JSONL files in `~/.claude/projects/` aren't something you send to someone.

**[claudebin](https://claudebin.com)** fixes this with a single slash command.

## One Command, Permanent Link

```bash
/claudebin:share
```

The plugin authenticates via GitHub OAuth, uploads the session data, parses it into structured messages, generates a title, and returns a URL. The full conversation is preserved: prompts, responses, tool calls, file edits, bash commands, syntax highlighting, timestamps.

Sessions can be public (searchable, listed on the homepage) or unlisted (accessible only via direct link).

## Embedding Sessions

Claudebin sessions are embeddable. Select a range of messages and drop them into a blog post, a PR description, or documentation. The embed renders the conversation with full fidelity, the same syntax highlighting, tool call formatting, and message structure as the web view.

This blog already uses claudebin embeds. They're a natural way to show how a problem was solved rather than just describing it.

## Resumable Conversations

Every shared session includes a command to resume it locally. Someone reads your session, sees an interesting approach, and picks up where you left off in their own terminal. Sessions become reusable starting points, not just read-only artifacts.

## How It Works

Two repositories make up the system:

The **web app** (Next.js, Supabase, Vercel) handles rendering, search, profiles, and the embed API. The **plugin** (Claude Code MCP) handles authentication, upload, and processing.

The flow: `/claudebin:share` uploads JSONL to storage, a pipeline parses messages and generates a title via LLM, and you get a URL back. Full-text search works across all public sessions.

Built by [Wunderlabs](https://github.com/wunderlabs-dev). Free, MIT licensed, not affiliated with Anthropic.

**[Source on GitHub](https://github.com/wunderlabs-dev/claudebin.com)** | **[claudebin.com](https://claudebin.com)**

claudebin grew out of [claude-notes](/project/claude-notes/), a CLI tool I built earlier to convert Claude Code transcripts to HTML. claude-notes solved the local case; claudebin makes sessions shareable, searchable, and embeddable on the web. Pair it with [micode](/project/micode/) for structured agent workflows, and you get a full loop: plan, implement, and share the evidence.

Stay curious ☕
