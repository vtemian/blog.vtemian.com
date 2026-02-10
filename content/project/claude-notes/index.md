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

I wanted to share a Claude Code session with someone. Show them the conversation. The prompts, the tool calls, the code edits. And I wanted to replay my own sessions later.

The problem: Claude Code stores everything as JSONL in `~/.claude/projects/`. Each line is a message, tool use, or tool result. Useful for machines. Useless for humans.

## The Solution

**[claude-notes](https://github.com/vtemian/claude-notes)** transforms those JSONL files into readable formats.

Export to HTML:

```bash
uvx claude-notes show --format html --output session.html
```

<video autoplay loop muted playsinline width="100%" style="margin-bottom: 2rem;">
  <source src="html-output.mp4" type="video/mp4">
</video>

Sometimes I just want to quickly scroll through a session without leaving the terminal. So there's also a terminal view:

```bash
uvx claude-notes show
```

<video autoplay loop muted playsinline width="100%" style="margin-bottom: 2rem;">
  <source src="terminal-output.mp4" type="video/mp4">
</video>

No installation needed. Just `uvx` and go.

## Example Output

Here's a real exported conversation. Scroll through it or [open full screen](/examples/claude-notes-conversation.html).

<iframe src="/examples/claude-notes-conversation.html" width="100%" height="600" style="border: 1px solid #ccc; border-radius: 8px;"></iframe>

You get timestamps, properly formatted tool calls, syntax highlighting. It just looks good.

## How It Works

Point it at a project, it finds your transcripts and renders them. That's it.

The code is simple. Python. Rich for terminal rendering. Jinja2 for HTML templates. Nothing fancy.

## Why I Built It

I wanted to share sessions with colleagues. "Look at this conversation I had." And I wanted to replay my own sessions. Go back and see how I solved something.

Now I export to HTML and send the file. Or open it myself to review what happened.

---

Try it:

```bash
uvx claude-notes show --format html --output my-session.html
```

Then open the HTML file. That's your session, readable.

**[View on GitHub](https://github.com/vtemian/claude-notes)**

Stay curious ☕
