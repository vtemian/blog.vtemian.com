---
title: "The Disposable Tools Manifesto"
date: 2026-04-05T08:00:00+02:00
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

A friend of mine told me something a few weeks ago that I haven't been able to shake. We were talking about AI tooling, evaluation, benchmarks, the usual. And he said: "I don't work on the tool. The tool is a means to an end, not the end. Disposable tooling."

His take was simple: he doesn't build polished tool repositories. He builds what he needs, uses it, and moves on. The tool is not the product. The tool is scaffolding.

That sentence broke something in me. Because I've spent the last six months doing the exact opposite.

## 15 products. 0 revenue.

In the past six months, I've shipped roughly 8,000 GitHub contributions across 15 projects. MCP servers, browser extensions, CLI plugins, observation libraries, desktop apps. Here's a partial list:

- **[claudebin](https://claudebin.com/)** ([write-up](/project/claudebin/)): a session-sharing tool for Claude Code.
- **[agentprobe](https://www.npmjs.com/package/agentprobe)** ([write-up](/project/agentprobe/)): an observation library for AI coding agents. Four provider integrations, published on npm.
- **micode** ([write-up](/project/micode/)): a structured AI coding workflow plugin for OpenCode. Version 0.9.1.
- **octto** ([write-up](/project/octto/)): an interactive browser-based brainstorming tool. Version 0.3.1.
- **[claude-notes](https://github.com/vtemian/claude-notes)** ([write-up](/project/claude-notes/)): a CLI tool to transform Claude Code JSONL transcripts into readable, searchable HTML.
- **[wunderlabs](https://wunderlabs.dev/)**: Lovable for existing codebases.
- **[cursouls](https://cursouls.xyz/)** ([write-up](/project/cursouls/)): a pixel-art agent visualization extension for VS Code.

Every single one of these works. They're tested, documented, published. And every single one of them generates zero revenue.

I kept telling myself the next project would be different. That I was building a portfolio, learning in public, establishing credibility. But my friend's words forced me to look at it honestly: I was building refined tools in a world that increasingly wants disposable ones.

## The IDE is now Claude

Here's what changed. A year ago, if you wanted a script to parse your bank statements into a spreadsheet, you had two options: find a SaaS that does it (and pay $15/month), or spend an evening writing a parser. Today, you open Claude, paste a sample statement, and have a working parser in 10 minutes. Not a prototype. A working tool, tailored to your exact bank format.

That's a trivial example. But the same applies to everything I built. Someone with Claude Code could replicate 90% of claudebin's functionality in a single conversation. Same for agentprobe. For micode. For most of what I shipped. The honest truth: these are problems that no longer need permanent solutions. They need disposable ones.

Software became so cheap to produce that paying a monthly subscription for a simple tool makes less and less sense. Andrej Karpathy [called it "vibe coding"](https://x.com/karpathy/status/1886192184808149383): you describe what you want, the AI builds it, and you move on. Why subscribe to a SaaS that sort-of does what you need when you can generate exactly what you need, tailored to your specific problem, in minutes?

I did the research. I went looking for new SaaS products built with [Lovable](https://lovable.dev), [Base44](https://base44.com), or [Bolt](https://bolt.new) that have meaningful revenue at scale. I found micro-wins (a few paying customers here, a handful of lifetime deals there), but nothing approaching a real SaaS business. Yet the platforms themselves are printing money: Lovable hit [$300M ARR](https://sacra.com/c/lovable/) and a $6.6B valuation. Bolt.new [reached $40M ARR](https://www.nocode.mba/articles/bolt-vs-lovable) in its first six months. The platforms that help you build disposable tools are thriving. The disposable tools themselves are not businesses.

## From dev tools to agent-ready tools

But something else is happening that's more interesting than "SaaS is dead."

The value isn't gone. It moved. It shifted from developer tools (things humans use directly) to agent-ready tools (things AI agents use on behalf of humans).

The difference is subtle but important. A developer tool has a UI, documentation, onboarding. An agent-ready tool has an API, clear inputs and outputs, and can be called programmatically. The user never touches it. They say "Claude, deploy this" or "Claude, use this style" and the agent figures out which tools to invoke.

MCP is one implementation of this, and it's growing fast: [97 million monthly SDK downloads](https://www.pento.ai/blog/a-year-of-mcp-2025-review), 10,000+ public servers, and [governance under the Linux Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation) with backing from Anthropic, OpenAI, Google, Microsoft, and AWS. Projects like [OpenClaw](https://github.com/openclaw/openclaw) are attempting to be distribution layers for agent tools, routing MCP-compatible skills to millions of users across WhatsApp, Telegram, and Slack. But the pattern is broader than any single protocol or runtime. Any tool that an AI agent can discover, understand, and call autonomously is an agent-ready tool. The value proposition changed: you're not selling to a human who evaluates your landing page. You're making your capability available to an agent that evaluates your interface programmatically.

## The real opportunity: the environment

If disposable tools are the new normal, then the opportunity isn't in building better tools. It's in building the environment where disposable tools thrive.

Think about it. You generate a tool in Claude in 20 minutes. Great. Now what?

- Where do you run it? Your laptop? A server?
- How do you connect it to your other tools?
- How do you share it with your team?
- How do you preview what it does before trusting it?
- How do you keep costs down when you're spinning up tools daily?

Hosting, integrations, previews, cost reduction. The infrastructure layer for disposable tools. Some companies are starting to build pieces of this. [E2B](https://e2b.dev) raised [$35M to build secure sandboxes](https://e2b.dev/blog/series-a) for AI-generated code, using Firecracker microVMs that spin up in under 200ms. They're [used by 88% of Fortune 100 companies](https://venturebeat.com/ai/how-e2b-became-essential-to-88-of-fortune-100-companies-and-raised-21-million). [Val Town](https://www.val.town/) lets you deploy small functions without worrying about infrastructure. But nobody has put the full picture together yet.

The analogy: containers didn't win because Docker was a great tool. Containers won because Kubernetes, AWS ECS, and the entire ecosystem around them made it trivial to run containers at scale. The container itself is disposable. The orchestration layer is the business. Docker popularized containers but [failed to capture the orchestration layer](https://techcrunch.com/2019/11/13/mirantis-acquires-docker-enterprise/), had to sell its enterprise business, and nearly died. The value accrued to the platform, not the tool.

Disposable tools need their Kubernetes.

## I don't have the answer

I'm not going to wrap this up with a neat conclusion, because I don't have one. I spent six months building tools that the world increasingly doesn't need in their polished, permanent form. That's a hard thing to admit when you've poured real effort into them.

What I do know:

The cost of producing software is approaching zero. Google reported that [25% of its new code](https://blog.google/technology/ai/google-gemini-ai-update-december-2024/) is now AI-generated. GitHub's research showed developers [complete tasks 55% faster](https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/) with Copilot. That changes everything about how we think about tools, products, and what's worth paying for. The SaaS model built on "we'll maintain this tool so you don't have to" loses its value when maintaining it yourself takes minutes, not months.

Something new is forming. Agent-ready tools, disposable by design, running on infrastructure that doesn't exist yet. I don't know exactly what it looks like. But I know that building another polished developer tool isn't it.

My friend was right. The tool is not the end. It never was.
