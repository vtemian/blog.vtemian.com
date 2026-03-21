---
title: "cursouls: ambient awareness for your AI agents"
date: 2026-03-20
author: Vlad Temian
url: https://blog.vtemian.com/project/cursouls/
description: "Born from Cafe Cursor meetups. A Cursor extension that gives your AI agents their own pixel cafe in the sidebar. Glance at it to see who's working, who's done, and who needs attention."
tags: [ai, tools, open-source, agentic-programming, cursor, typescript]
---

# cursouls: ambient awareness for your AI agents


<video controls playsinline width="100%" style="margin-bottom: 2rem;">
  <source src="demo.mp4" type="video/mp4">
</video>

I run **Cafe Cursor** events as a Cursor ambassador. Developers gather at a real cafe, drink coffee, and talk about how they're building with Cursor. There's something about the format that works. People share screens, trade prompts, debug each other's agent workflows. The cafe is the context.

At some point the obvious question came up: your agents write code, fix bugs, and run tests all day. They're your hardest workers. Why don't *they* get a cafe?

**[Cursouls](https://cursouls.xyz)** is the answer. A pixel cafe that lives in your sidebar, where each AI agent becomes a tiny character you can see. When they work, they animate. When they finish, they celebrate. When they fail, you know instantly. When they need clarification, they let you know. It's a digital Cafe Cursor for the agents themselves.

10x engineers monitor logs. You watch your guys vibe.

## Read the Room, Not the Logs

Six visual states, zero configuration. Install the extension, open a workspace, and the cafe populates automatically as agents join.

| Your agent is...       | The cafe shows...                                    |
| ---------------------- | ---------------------------------------------------- |
| Starting a new task    | Character spawns into the cafe (48-frame entrance)   |
| Writing or editing code| Character works busily at their spot                 |
| Idle, between tasks    | Character hangs out, waiting for the next job        |
| Task completed         | Character celebrates (unique 39-frame animation)     |
| Task failed            | Character shows visible distress                     |
| Needs clarification    | Character signals confusion, waiting for your input  |

Hover over a character to see its task summary as a scrolling marquee. Drag to pan the scene with spring physics. Click the barista counter because why not.

## Every Major AI Agent, One Cafe

Most extensions lock you into a single AI provider. Cursouls works with all of them at once, side by side in the same scene.

- **Cursor** agents
- **Claude Code** agents
- **Codex** agents
- **OpenCode** agents

This is powered by [@agentprobe/core](https://www.npmjs.com/package/@agentprobe/core), which handles provider detection and lifecycle tracking automatically. Cursouls is a pure consumer of AgentProbe's event stream. Swap the provider, same pixel character.

## The Cafe Is Alive

This is not a static dashboard. The cafe is a pixel scene with furniture, plants, a barista counter, and room to breathe.

Each agent gets one of 4 unique character skins. A dialog box with typewriter-effect text announces events as they happen. Random aliases (via Faker) give agents memorable names when they join. The whole thing feels like a game, not a panel.

Under the hood, a sprite atlas drives frame-by-frame animations. CSS background positioning renders each frame from a single sheet. Framer Motion handles the draggable scene with elastic spring physics. React context distributes agent state. Zod validates every message crossing the extension/webview bridge.

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

