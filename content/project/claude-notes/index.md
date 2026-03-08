---
title: "claude-notes: claude code sessions to html"
date: 2025-06-25T19:46:00+03:00
description: "claude-notes: A local CLI tool to transform Claude Code JSONL transcripts into readable, searchable HTML. Replay and document your AI coding sessions."
keywords:
    - claude code
    - claude-notes
    - ai tools
    - jsonl to html
    - claude session viewer
    - developer tools
    - cli
    - python
    - uvx
    - open source
tags:
    - ai
    - tools
    - open-source
    - documentation
    - python
images:
    - og.png
---

Claude Code is fast, but it's hard to look back. I found myself frequently wanting to show a colleague the exact "messy middle" of a session—the specific tool call or terminal output that finally led to a solution. 

But Claude stores everything as raw `.jsonl` files in `~/.claude/projects/`. Not exactly something you can link in a PR.

**[claude-notes](https://github.com/vtemian/claude-notes)** is a local CLI tool that turns those JSON lines into readable, searchable, and shareable HTML.

## Debugging Replay: Seeing the Process

The value isn't just in the final code; it's in the **process**. By converting the transcript into a clean HTML view, I can "replay" the debugging logic:
- Which bash commands did the agent run?
- What were the specific tool outputs it reacted to?
- Where did it hallucinate, and how was it corrected?

## A Modern Python Workflow

I built this with **Python**, **Rich** (for the terminal view), and **Jinja2** (for the HTML output). The distribution is built for modern developer speed using `uvx`. No environment setup, no `pip install`. 

**Render to HTML:**
```bash
uvx claude-notes show --format html --output session.html
```

**Quick Terminal Replay:**
```bash
uvx claude-notes show
```

<video autoplay loop muted playsinline width="100%" style="margin-bottom: 2rem;">
  <source src="html-output.mp4" type="video/mp4">
</video>

## Actual Exported Session

Below is a live export of a Claude Code session. You can [open it full screen](/examples/claude-notes-conversation.html).

<iframe src="/examples/claude-notes-conversation.html" width="100%" height="600" style="border: 1px solid #ccc; border-radius: 8px;"></iframe>

...
## Implementation

Nothing fancy. Python with Rich for terminal rendering and Jinja2 for HTML templates. Point it at a project directory, it finds the JSONL files and renders them.

I use it mostly to replay my own sessions. Go back to see how something was debugged. Or export to HTML and send to someone when I want to show them an interesting conversation.

**[Source on GitHub](https://github.com/vtemian/claude-notes)**

claude-notes was the starting point. The need to share sessions led to [claudebin](/project/claudebin/) — a web platform where sessions become permanent, searchable, embeddable URLs with a single command.

Stay curious ☕
