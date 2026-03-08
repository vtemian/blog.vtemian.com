---
title: "micode: context harnessing, planning and parallel execution for OpenCode"
date: 2025-12-20T00:00:00+03:00
description: "micode: An orchestrated team of 12 specialized sub-agents for OpenCode. Enforcing a Brainstorm-Plan-Implement workflow with parallel execution and session continuity."
keywords:
    - micode
    - opencode
    - agentic programming
    - ai coding workflow
    - multi-agent orchestration
    - tdd with ai
    - llm memory
    - developer tools
    - structured coding agents
tags:
    - ai
    - tools
    - open-source
    - agentic-programming
    - workflow
images:
    - og.png
---

<video autoplay loop muted playsinline width="100%" style="margin-bottom: 2rem;">
  <source src="demo.mp4" type="video/mp4">
</video>

I built **micode** because I got tired of "magic" turning into "amnesia." You describe a feature, the agent starts writing code, and for a while it feels like a superpower. Then context drifts. The agent forgets a decision made three tool calls ago, or it re-invents a utility that already exists in the codebase. 

The issue isn't that AI coding tools are bad. The issue is that they have no memory and no discipline. **[micode](https://github.com/vtemian/micode)** is an [OpenCode](https://opencode.ai) plugin that enforces both.

## The "Memory" Problem: Continuity over Context

The fundamental problem with AI assistants is context loss. Within a session, understanding degrades as the window fills up. Between sessions, everything is gone. I spent too many mornings "re-explaining" the project to an agent that I had spent all of yesterday with. 

micode solves this via **Continuity Ledgers**:
- **Structured memory**: Running `/ledger` creates `CONTINUITY_{session}.md` files that capture architectural decisions, progress, and open questions.
- **Auto-Injection**: On the next session, a hook automatically injects the latest ledger. The agent "wakes up" exactly where it left off.
- **Context Guard**: It automatically injects your `ARCHITECTURE.md` and `CODE_STYLE.md` into every sub-agent's system prompt. No more hallucinations about which library to use.

## The Golden Workflow: No Code Before a Plan

AI agents are "lazy" by nature—they want to skip straight to implementation. micode enforces a mandatory 3-stage lifecycle that I've found to be the only way to get reliable results on complex features:

### 1. **Brainstorm** (The "What" and "Why")
Parallel research sub-agents explore the codebase, ask clarifying questions, and consider multiple architectures. The output is a **Design Document**, not a plan. We agree on the approach before we discuss the implementation.

### 2. **Plan** (The "How")
A specialized Planner agent transforms the design into bite-sized, deterministic tasks (2-5 minutes each) with exact file paths and test-first expectations. You review and approve this blueprint before a single line of code is written.

### 3. **Implement** (The Execution)
This is where the magic happens. micode spawns **Implementer-Reviewer pairs** in parallel—sometimes 10-20 concurrent micro-tasks at a time—using isolated git worktrees. Each pair follows a strict TDD loop: write the test, watch it fail, write the code, watch it pass.

Human approval gates exist between each phase. The agent doesn't get to freestyle; it follows the blueprint.

...
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
