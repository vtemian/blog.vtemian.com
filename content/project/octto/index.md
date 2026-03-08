---
title: "octto: browser UI for brainstorming with OpenCode agents"
date: 2026-01-02T00:00:00+03:00
description: "octto: A browser-based UX for agentic brainstorming. Replace terminal-based back-and-forth with 14 rich input types and parallel exploration branches."
keywords:
    - octto
    - opencode
    - agentic programming
    - ai ux
    - structured brainstorming
    - llm interface
    - human-in-the-loop
    - developer tools
    - ai gui
tags:
    - ai
    - tools
    - open-source
    - agentic-programming
    - ux
images:
    - og.png
---

<video autoplay loop muted playsinline width="100%" style="margin-bottom: 2rem;">
  <source src="demo.mp4" type="video/mp4">
</video>

Brainstorming with AI agents in a terminal is slow and painful. You type a paragraph, the agent asks a question, you type another paragraph... it's a 10-minute back-and-forth just to agree on an approach. Most of that time is spent in "prose-churn"—typing things that should have been a single click.

**[octto](https://github.com/vtemian/octto)** turns those 10 minutes of typing into 2 minutes of clicking.

## Agentic UI: Why Chat is a Bottleneck

We've been conditioned to think "AI = Chatbox," but prose is one of the most inefficient interfaces for structured decision-making. Chat is linear, ambiguous, and requires constant re-typing. 

I built **octto** on a different philosophy: **Agentic UI**. The agent shouldn't just talk to you; it should present you with the most efficient interface for the task at hand. 
- **Beyond Prose**: Instead of "Option B is better because...", just click a button.
- **Parallel Exploration**: Chat is serial. octto is tree-structured. It splits your request into 2-4 branches simultaneously.
- **Visual Synthesis**: Side-by-side diffs, drag-and-drop rankings, and rich sliders replace descriptive text.

## 14 Rich Input Types

octto replaces free-form text with a library of 14 structured inputs designed for fast "Human-in-the-Loop" decisions:
- **Decision Controls**: Radio buttons, checkboxes, and thumbs up/down for rapid approval.
- **Structured Ranking**: Drag items into a ranked list to set priorities.
- **Code Review**: Side-by-side diffs and syntax-highlighted editors.
- **Rich Media**: Image uploads and file pickers for direct context.
- **Dynamic Pros/Cons**: Option cards that summarize trade-offs visually.

...
## Parallel Exploration

The real speedup comes from parallel branching. Instead of exploring one question at a time, octto splits your request into 2-4 exploration branches. All initial questions appear at once. You answer them in any order. Some branches finish in 2 questions, others need 4. It's a tree-structured exploration, not a linear conversation.

Follow-up questions appear dynamically as you answer. A progress indicator shows remaining questions. Completed answers stay visible for context.

## Three-Agent Architecture

Three specialized agents orchestrate each session:

| Agent | Role |
|-------|------|
| **bootstrapper** | Splits your request into 2-4 exploration branches |
| **probe** | Evaluates each branch after you answer: needs more questions, or done? |
| **octto** | Orchestrates the overall session lifecycle |

The bootstrapper decomposes. The probe adapts. The octto agent manages the whole thing. Once all branches converge, a final plan is rendered for review, approval, and saved to `docs/plans/` in your project.

## Configuration

Simple setup: one line in your OpenCode config. You can customize the port, agent models, and inject project-specific instructions via "fragments". Fragments can be global or per-project, so you can tell the brainstorming agents "this project uses React, focus on component patterns" without repeating it every session.

**[Source on GitHub](https://github.com/vtemian/octto)**

octto handles the brainstorming phase. For the full structured workflow — brainstorm, plan, and parallel implementation with review — see [micode](/project/micode/).

Stay curious ☕
