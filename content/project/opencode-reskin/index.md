---
title: "opencode-reskin: multi-agent CSS analysis for OpenCode"
date: 2026-01-02T01:00:00+03:00
description: "opencode-reskin: Multi-agent CSS analysis and design system migration for OpenCode. Automatically generate a transformation plan to reskin any web project."
keywords:
    - opencode-reskin
    - opencode
    - agentic programming
    - ai design system
    - css orchestration
    - style transformation
    - multi-agent design
    - developer tools
    - tailwind migration
tags:
    - ai
    - tools
    - open-source
    - agentic-programming
    - design-systems
images:
    - og.png
---

<video autoplay loop muted playsinline width="100%" style="margin-bottom: 2rem;">
  <source src="demo.mp4" type="video/mp4">
</video>

Reskinning a web project manually is "death by a thousand paper cuts." You spend hours hunting through Tailwind configs, global CSS files, and component-level styles, trying to figure out what needs to change to match a new design system. It's tedious, error-prone, and exactly the kind of work humans shouldn't be doing.

**[opencode-reskin](https://github.com/vtemian/opencode-reskin)** automates the "archaeology" and planning.

## One Command, Deterministic Plan

```bash
/skin nof1
```

The plugin scans your project, compares it against a target design system (skin), and produces a **concrete transformation plan**. No guesswork. No "maybe." You get a markdown checklist of exact changes:
- `Change --background: #0f172a -> #ffffff in src/styles/globals.css`
- `Change font-family: Inter -> IBM Plex Sans in tailwind.config.ts`
- `Change border-radius: 0.5rem -> 0.25rem in src/components/Card.tsx`

## The Multi-Agent Strategy: Why it Matters

A single LLM prompt often fails at large-scale design migrations because it can't hold the entire CSS/Component tree in context. **opencode-reskin** solves this by orchestrating three specialized agents:

- **Style Analyzer**: Scans global CSS, Tailwind configs, and design tokens to build the "base" styling profile.
- **Component Scanner**: Identifies UI patterns and framework-specific styling (e.g., Shadcn, Radix) to see how styles are actually consumed.
- **The Orchestrator**: Compares both findings against the target skin and generates the final, unified checklist.

By splitting the "Base CSS" from the "Component Consumption," the tool avoids the hallucinations common in single-agent architectures.

...
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

Another OpenCode plugin in the same family: [micode](/project/micode/) applies the multi-agent pattern to the full development workflow, not just styling.

Stay curious ☕
