---
title: "micode: context harnessing, planning and parallel execution for OpenCode"
date: 2025-12-20T00:00:00+03:00
description: "An OpenCode plugin that turns a single coding agent into an orchestrated team of 12 specialized sub-agents, enforcing a Brainstorm-Plan-Implement workflow with parallel execution and session continuity."
images: []
keywords:
    - micode
    - opencode
    - agentic programming
    - ai tools
    - developer tools
    - structured workflows
    - tdd
tags:
    - ai
    - tools
    - open-source
---

{{< github-stats repo="vtemian/micode" >}}

<video autoplay loop muted playsinline width="100%" style="margin-bottom: 2rem;">
  <source src="demo.mp4" type="video/mp4">
</video>

You describe a feature, the agent starts writing code, and for a while it feels like magic. Then context drifts. The agent forgets what it read three tool calls ago. It re-invents a utility that already exists in the codebase. It solves the wrong problem because nobody stopped to ask whether the approach was right.

The issue isn't that AI coding tools are bad. The issue is that they have no memory and no discipline.

**[micode](https://github.com/vtemian/micode)** is an [OpenCode](https://opencode.ai) plugin that fixes both.

## Context is Everything

The fundamental problem with AI coding assistants is context loss. Within a session, the agent's understanding degrades as the context window fills up. Between sessions, everything is gone. You come back tomorrow and the agent has no idea what happened yesterday, what decisions were made, or why the architecture looks the way it does.

micode attacks this from multiple angles:

- **Ledger system**: Running `/ledger` creates structured `CONTINUITY_{session}.md` files that capture decisions, progress, and open questions. On the next session, a hook automatically injects this context. `/search` lets you query past plans, designs, and ledgers.
- **Auto-Compact**: At 50% context usage, micode automatically summarizes the conversation to prevent context overflow while preserving the important bits.
- **Context Injector**: Automatically injects your `ARCHITECTURE.md` and `CODE_STYLE.md` into every agent's system prompt. The agent always knows your project's conventions.
- **Artifact indexing**: Every design document, plan, and ledger is automatically indexed and searchable across sessions.

## No Code Before a Plan

The core discipline: don't let the agent write code until you've agreed on what to build.

1. **Brainstorm** fires parallel research sub-agents to explore the codebase, ask questions, consider alternatives, and produce a written design document. Not a plan yet. A design. The "what" and "why" before the "how".

2. **Plan** transforms that design into bite-sized tasks (2-5 minutes each) with exact file paths, code examples, and test-first workflow. You review and approve before anything moves forward.

3. **Implement** executes in an isolated git worktree. Implementer-reviewer pairs run in parallel, 10-20 concurrent micro-tasks at a time. Each task follows TDD: write the test, watch it fail, write the code, watch it pass.

Human approval gates exist between each phase. The agent doesn't get to skip ahead.

## Specialized Agents, Not One Agent Doing Everything

micode decomposes work across 12 agents, each with its own system prompt, model configuration, and tools. The Brainstormer explores differently than the Implementer. The Codebase Locator has different capabilities than the Planner. The Reviewer checks work with different criteria than the one who wrote it.

This matters because a single agent context-switching between research, planning, coding, and reviewing produces worse results than specialized agents that each do one thing well.

## Why Structure Matters

The philosophy is deliberately opinionated:

1. Understand the codebase before proposing changes
2. Brainstorm before planning, plan before coding
3. Every decision needs human buy-in
4. Parallel investigation, not serial guessing
5. Isolated implementation via git worktrees
6. Every task gets both an implementer AND a reviewer
7. Context persists across sessions, always

The bet is simple: constraining the AI into a disciplined workflow produces better results than letting it freestyle. Planning over guessing. Memory over amnesia.

**[Source on GitHub](https://github.com/vtemian/micode)**

If you prefer brainstorming in a browser UI instead of the terminal, [octto](/project/octto/) adds a visual layer with 14 input types and parallel exploration branches. And if you want to share your agent sessions with colleagues, [claudebin](/project/claudebin/) turns them into permanent, embeddable URLs.

Stay curious ☕
