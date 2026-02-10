---
title: "claude-notes: claude code sessions to html"
date: 2025-06-25T19:46:00+03:00
description: "A CLI tool to transform Claude Code transcripts into readable HTML. Built because I wanted to share and replay my coding sessions."
images:
    - screenshot.png
keywords:
    - claude code
    - claude notes
    - ai tools
    - developer tools
    - cli
    - python
    - open source
tags:
    - ai
    - tools
    - open-source
---

{{< github-stats repo="vtemian/claude-notes" >}}

I wanted to send a Claude Code session to a colleague. Show them the back-and-forth, the tool calls, how we solved a tricky bug together. But Claude Code stores everything as JSONL in `~/.claude/projects/`. Raw JSON lines. Not something you can just send to someone.

So I built **[claude-notes](https://github.com/vtemian/claude-notes)**.

```bash
uvx claude-notes show --format html --output session.html
```

<video autoplay loop muted playsinline width="100%" style="margin-bottom: 2rem;">
  <source src="html-output.mp4" type="video/mp4">
</video>

I also find myself wanting to scroll through past sessions in the terminal. Sometimes I forget how I solved something and want to look it up quickly:

```bash
uvx claude-notes show
```

<video autoplay loop muted playsinline width="100%" style="margin-bottom: 2rem;">
  <source src="terminal-output.mp4" type="video/mp4">
</video>

## Example

Here's an actual exported session. Scroll through it or [open full screen](/examples/claude-notes-conversation.html).

<iframe src="/examples/claude-notes-conversation.html" width="100%" height="600" style="border: 1px solid #ccc; border-radius: 8px;"></iframe>

## Implementation

Nothing fancy. Python with Rich for terminal rendering and Jinja2 for HTML templates. Point it at a project directory, it finds the JSONL files and renders them.

I use it mostly to replay my own sessions. Go back to see how something was debugged. Or export to HTML and send to someone when I want to show them an interesting conversation.

**[Source on GitHub](https://github.com/vtemian/claude-notes)**

Stay curious ☕
