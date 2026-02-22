---
title: "opencode-reskin: multi-agent CSS analysis for OpenCode"
date: 2026-01-02T01:00:00+03:00
description: "An OpenCode plugin that analyzes a web project's visual styling and generates a concrete transformation plan to match a target design system. Three agents, zero guesswork."
images: []
keywords:
    - opencode-reskin
    - opencode
    - agentic programming
    - ai tools
    - developer tools
    - css
    - design systems
tags:
    - ai
    - tools
    - open-source
---

{{< github-stats repo="vtemian/opencode-reskin" >}}

<video autoplay loop muted playsinline width="100%" style="margin-bottom: 2rem;">
  <source src="demo.mp4" type="video/mp4">
</video>

Reskinning a web project manually is tedious. You open the target design, then spend hours hunting through CSS files, Tailwind configs, and component styles, trying to figure out what needs to change and where. It's the kind of work that's simple in theory but death by a thousand paper cuts in practice.

**[opencode-reskin](https://github.com/vtemian/opencode-reskin)** automates the analysis and planning.

## One Command, Full Plan

```bash
/skin nof1
```

That's it. The plugin scans your project's current styling, compares it against the target skin definition, and produces a markdown checklist of exact changes:

```
Change --background: #0f172a -> #ffffff in src/styles/globals.css
Change font-family: Inter -> IBM Plex Sans in tailwind.config.ts
Change border-radius: 0.5rem -> 0.25rem in src/components/Card.tsx
```

It plans, it does not execute. You review the checklist, then apply the changes yourself or hand them off to another agent. Full control over what actually gets modified.

## Three Agents Working in Parallel

| Agent | Role |
|-------|------|
| **reskin** | Orchestrator. Spawns subagents, compares findings against the skin definition, generates the transformation plan |
| **style-analyzer** | Scans CSS files, Tailwind config, and design tokens |
| **component-scanner** | Finds UI components, identifies styling patterns, detects the framework |

Both analysis agents run concurrently, so the workflow stays fast even on large projects.

## Skins as Data

Skin definitions are declarative files defining colors (palette and semantic), typography (fonts and scale), spacing, border radius, and optionally data visualization styles, component overrides, and design guidelines. Adding a new skin is just dropping a new definition file into the `skins/` directory.

The plugin ships with one skin (`nof1`, a neutral dashboard style), but the system is designed to be extended.

**[Source on GitHub](https://github.com/vtemian/opencode-reskin)**

Stay curious ☕
