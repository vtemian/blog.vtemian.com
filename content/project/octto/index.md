---
title: "octto: browser UI for brainstorming with OpenCode agents"
date: 2026-01-02T00:00:00+03:00
description: "An OpenCode plugin that replaces terminal-based brainstorming with a browser UI. 14 rich input types, parallel exploration branches, and a 5x speedup over typing."
images: []
keywords:
    - octto
    - opencode
    - agentic programming
    - ai tools
    - developer tools
    - brainstorming
    - ui
tags:
    - ai
    - tools
    - open-source
---

{{< github-stats repo="vtemian/octto" >}}

<video autoplay loop muted playsinline width="100%" style="margin-bottom: 2rem;">
  <source src="demo.mp4" type="video/mp4">
</video>

Brainstorming with AI agents in a terminal is slow and painful. You type a paragraph, the agent asks a question, you type another paragraph, it asks another question. Ten minutes of back-and-forth just to agree on an approach. Most of that time is spent typing things that could have been a single click.

**[octto](https://github.com/vtemian/octto)** opens a browser window instead.

## Stop Typing, Start Clicking

When you describe an idea to the agent, octto opens a browser UI that presents structured, visual questions. Instead of typing "I think option B is better because...", you click a radio button. Instead of describing priority order in prose, you drag items into a ranked list. Instead of explaining a code preference, you review a side-by-side diff and click approve.

14 input types replace free-form text: radio buttons, checkboxes, sliders, drag-to-rank, star ratings, thumbs up/down, option cards with pros and cons, side-by-side code diffs, syntax-highlighted code editors, text fields, image uploads, and file pickers.

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
