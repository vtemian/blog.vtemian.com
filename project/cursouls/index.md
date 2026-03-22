---
title: "cursouls: a pixel cafe for your AI agents"
date: 2026-03-20
author: Vlad Temian
url: https://blog.vtemian.com/project/cursouls/
description: "Born from Cafe Cursor meetups. A fun Cursor extension that gives your AI agents their own pixel cafe in the sidebar."
tags: [ai, tools, open-source, agentic-programming, cursor, typescript]
---

# cursouls: a pixel cafe for your AI agents


<video controls playsinline width="100%" style="margin-bottom: 2rem;">
  <source src="demo.mp4" type="video/mp4">
</video>

I run **Cafe Cursor** events as a Cursor ambassador. Developers gather at a real cafe, drink coffee, and talk about how they're building with Cursor. There's something about the format that works. People share screens, trade prompts, debug each other's agent workflows. The cafe is the context.

At some point the obvious question came up: your agents write code, fix bugs, and run tests all day. They're your hardest workers. Why don't *they* get a cafe?

**[Cursouls](https://cursouls.xyz)** is a fun project, not trying to solve a specific problem. It's a pixel cafe that lives in your sidebar, where each AI agent becomes a tiny character you can see. When they work, they animate. When they finish, they celebrate. When they fail, you know instantly. When they need clarification, they let you know. It's a digital Cafe Cursor for the agents themselves.

10x engineers monitor logs. You watch your guys vibe.

## What It Looks Like

Install the extension, open a workspace, and the cafe populates on its own. No configuration.

Each agent gets a unique pixel character skin and a random name when it joins. When an agent starts working, the character animates. When it finishes, it celebrates. When it fails, it looks distressed. When it needs clarification, it signals confusion. You hover over a character to see what it's working on. You drag to pan the scene. You click the barista counter because why not.

It works with **Cursor**, **Claude Code**, **Codex**, and **OpenCode** agents, all in the same cafe at once. Powered by [@agentprobe/core](https://www.npmjs.com/package/@agentprobe/core), which watches the transcript files these tools already leave behind. No API keys, no patches.

## How We Built It

The cafe is a pixel scene rendered from a single sprite atlas. Frame-by-frame animations driven by CSS background positioning. Framer Motion handles the draggable scene with spring physics. A dialog box with typewriter-effect text announces events as they happen. The whole thing feels like a game, not a panel.

We leaned into the vibe. Random aliases via Faker give each agent a memorable name. Four character skins. Furniture, plants, a barista counter. It's deliberately more whimsical than practical.

## Install

Search **"Cursouls"** in the Extensions panel (`Cmd+Shift+X`) and click Install. That's it.

Or build from source:

```bash
git clone https://github.com/wunderlabs-dev/cursouls.git
cd cursouls
npm install && npm run build
npx @vscode/vsce package --no-dependencies
```

Then `Cmd+Shift+P` > "Install from VSIX" > select `cursouls-0.1.7.vsix`.

---

Built by [Vlad Temian](https://x.com/vtemian) and [Marius Balaj](https://x.com/balajmarius) at [Wunderlabs](https://github.com/wunderlabs-dev). MIT licensed.

**[Website](https://cursouls.xyz)** · **[Source on GitHub](https://github.com/wunderlabs-dev/cursouls)** · **[VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=wunderlabs.cursouls)** · **[Open VSX](https://open-vsx.org/extension/wunderlabs/cursouls)**

For the observability library that powers Cursouls, see [agentprobe](/project/agentprobe/). For structured agent workflows, see [micode](/project/micode/). For sharing agent sessions, see [claudebin](/project/claudebin/).

Stay curious ☕

