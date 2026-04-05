---
title: "The Disposable Tools Manifesto"
date: 2026-04-05T12:00:00+02:00
description: "I built 15 products in 6 months and made zero revenue. Here's what I learned about why SaaS is dying and what's replacing it."
keywords:
    - disposable tools
    - saas
    - ai tools
    - claude code
    - mcp
    - agent-ready tools
    - vibe coding
    - software economics
tags:
    - ai tools
    - saas
    - software economics
    - vibe-coding
draft: false
---

A friend of mine, Cristi Toma, told me something a few weeks ago that I haven't been able to shake. We were talking about AI tooling, evaluation, benchmarks, the usual. And he said: "I don't work on the tool. The tool is a means to an end, not the end. Disposable tooling."

Cristi is one of the smartest engineers I know. He built his own programming language at 14. And his take was simple: he doesn't build polished tool repositories. He builds what he needs, uses it, and moves on. The tool is not the product. The tool is scaffolding.

That sentence broke something in me. Because I've spent the last six months doing the exact opposite.

## 15 products. 0 revenue.

In the past six months, I've shipped roughly 8,000 GitHub contributions across 15 projects. MCP servers, browser extensions, CLI plugins, observation libraries, desktop apps. Here's a partial list:

- **agentprobe**: an observation library for AI coding agents. Four provider integrations, published on npm.
- **micode**: a structured AI coding workflow plugin for OpenCode. Version 0.9.1.
- **octto**: an interactive browser-based brainstorming tool. Version 0.3.1.
- **Cursor Cafe**: a pixel-art agent visualization extension for VS Code.
- **claudebin**: a session-sharing tool for Claude Code.
- **booking-mcp**: an MCP server that scrapes Booking.com for hotel search.
- **whoop-mcp**: an MCP server that scrapes Whoop's shop.

Every single one of these works. They're tested, documented, published. And every single one of them generates zero revenue.

I kept telling myself the next project would be different. That I was building a portfolio, learning in public, establishing credibility. But Cristi's words forced me to look at it honestly: I was building refined tools in a world that increasingly wants disposable ones.

## The IDE is now Claude

Here's what changed. Two years ago, if you wanted a tool to scrape Booking.com for hotel prices, you had two options: find a SaaS that does it, or spend a week building one. Today, you open Claude, describe what you need, and have a working scraper in 20 minutes. Not a prototype. A working tool.

I know this because I built booking-mcp. It took me significantly longer than 20 minutes. I wrote tests, set up a proper package, published it, integrated it as an MCP server. And someone with Claude Code could replicate 90% of its functionality in a single conversation.

The same applies to whoop-mcp. To agentprobe. To most of what I built. The honest truth: these are problems that no longer need permanent solutions. They need disposable ones.

Software became so cheap to produce that paying a monthly subscription for a simple tool makes less and less sense. Why subscribe to a SaaS that sort-of does what you need when you can generate exactly what you need, tailored to your specific problem, in minutes?

I did the research. I went looking for new SaaS products built with Lovable, Base44, or Bolt that have meaningful revenue. I couldn't find any. Yet Lovable and Base44 themselves are printing money. The platforms that help you build disposable tools are thriving. The disposable tools themselves are not businesses.

## From dev tools to agent-ready tools

But something else is happening that's more interesting than "SaaS is dead."

The value isn't gone. It moved. It shifted from developer tools (things humans use directly) to agent-ready tools (things AI agents use on behalf of humans).

The difference is subtle but important. A developer tool has a UI, documentation, onboarding. An agent-ready tool has an API, clear inputs and outputs, and can be called programmatically. The user never touches it. They say "Claude, deploy this" or "Claude, use this style" and the agent figures out which tools to invoke.

MCP is one implementation of this, but the pattern is broader. Any tool that an AI agent can discover, understand, and call autonomously is an agent-ready tool. The value proposition changed: you're not selling to a human who evaluates your landing page. You're making your capability available to an agent that evaluates your interface programmatically.

## The real opportunity: the environment

If disposable tools are the new normal, then the opportunity isn't in building better tools. It's in building the environment where disposable tools thrive.

Think about it. You generate a tool in Claude in 20 minutes. Great. Now what?

- Where do you run it? Your laptop? A server?
- How do you connect it to your other tools?
- How do you share it with your team?
- How do you preview what it does before trusting it?
- How do you keep costs down when you're spinning up tools daily?

Hosting, integrations, previews, cost reduction. The infrastructure layer for disposable tools. Nobody has built this well yet.

The analogy: containers didn't win because Docker was a great tool. Containers won because Kubernetes, AWS ECS, and the entire ecosystem around them made it trivial to run containers at scale. The container itself is disposable. The orchestration layer is the business.

Disposable tools need their Kubernetes.

## I don't have the answer

I'm not going to wrap this up with a neat conclusion, because I don't have one. I spent six months building tools that the world increasingly doesn't need in their polished, permanent form. That's a hard thing to admit when you've poured real effort into them.

What I do know:

The cost of producing software is approaching zero. That changes everything about how we think about tools, products, and what's worth paying for. The SaaS model built on "we'll maintain this tool so you don't have to" loses its value when maintaining it yourself takes minutes, not months.

Something new is forming. Agent-ready tools, disposable by design, running on infrastructure that doesn't exist yet. I don't know exactly what it looks like. But I know that building another polished MCP server isn't it.

Cristi was right. The tool is not the end. It never was.
