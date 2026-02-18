# vibe-infer Article Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Write a blog article showcasing AI-assisted learning through a GPU programming journey with Claude Code, using embedded claudebin conversations as proof.

**Architecture:** Hugo blog post in `content/post/vibe-infer/index.md` using YAML frontmatter, raw HTML iframes for claudebin embeds, and personal narrative + technical tone. The article has 7 sections with 3 claudebin embeds at key moments.

**Tech Stack:** Hugo static site generator, Markdown with YAML frontmatter, claudebin embed iframes

---

## Context

### Design Decisions (from brainstorming)

- **Audience:** Developer tooling enthusiasts
- **Thesis:** "Show, don't tell" - people talk about AI-assisted learning but rarely show the process. This article shows it with embedded proof.
- **Tone:** Personal narrative + technical. More first-person than the blockchain article, but still precise.
- **Claudebin promotion:** Organic mention. Claudebin appears naturally as "here's how I captured this session." Not a sales pitch.
- **Vibe coding contrast:** Woven throughout (not a dedicated section). The name "vibe-infer" is intentional irony because Vlad wrote the GPU code himself. Claude tutored, didn't author.
- **Key surprise:** Real-time verification of understanding. Claude reviewed Vlad's code, caught GPU-specific mistakes, and explained datatypes/patterns.
- **Embeds:** 3 key moments (premise, process, payoff). Each wrapped in narrative context so the article reads fine without clicking them.

### Embed Codes (ranges need Vlad's verification)

```html
<!-- Embed 1: Ground Rules - Vlad: "you don't write code, just guide me" / Claude: "I'm your GPS, you're driving" -->
<iframe style="width:100%;height:500px;border:none;" src="https://claudebin.com/threads/jmdbMowNTz/embed?from=7&to=10"></iframe>

<!-- Embed 3: Bug Hunt - Claude identifies 5+ bugs in matmul code -->
<iframe style="width:100%;height:500px;border:none;" src="https://claudebin.com/threads/jmdbMowNTz/embed?from=55&to=62"></iframe>

<!-- Embed 5: It Works - MNIST digit 7 at 99.95% confidence -->
<iframe style="width:100%;height:500px;border:none;" src="https://claudebin.com/threads/jmdbMowNTz/embed?from=130&to=136"></iframe>
```

**Important:** The `from`/`to` ranges are approximate. Vlad must verify and adjust these before the article goes live.

### Writing Style Reference

From CLAUDE.md:
- Semi-formal, educational tone balancing precision with accessibility
- Varied sentence lengths: shorter declarative to introduce, longer for context
- Ground abstract concepts with concrete examples
- Use transitional phrases ("Let's explain...", "Of course...", "There's no silver bullet")
- Keep paragraphs 3-5 sentences
- No em dashes. Use periods, commas, or restructure.
- Sign-off: "Stay curious ☕"

### Frontmatter Reference (from existing posts)

```yaml
---
title: "Title Here"
date: 2026-02-18T12:00:00+02:00
description: "SEO description"
keywords:
    - keyword1
    - keyword2
tags:
    - tag1
    - tag2
---
```

---

### Task 1: Create article file with frontmatter

**Files:**
- Create: `content/post/vibe-infer/index.md`

**Step 1: Create the directory and file**

```markdown
---
title: "vibe-infer: Learning GPU Programming with an AI Tutor, Not an AI Author"
date: 2026-02-18T12:00:00+02:00
description: "Everyone talks about AI-assisted learning. Here's what it actually looks like. A 155-message journey from zero WebGPU knowledge to a working MNIST classifier, with the entire conversation captured and browsable."
keywords:
    - gpu programming
    - webgpu
    - claude code
    - ai assisted learning
    - vibe coding
    - mnist
    - compute shaders
tags:
    - gpu programming
    - ai tools
    - webgpu
    - learning
draft: true
---
```

**Step 2: Verify with Hugo**

Run: `hugo server -D` and check http://localhost:1313 - the article should appear in the post list.

**Step 3: Commit**

```bash
git add content/post/vibe-infer/index.md
git commit -m "Add vibe-infer article skeleton"
```

---

### Task 2: Write Section 1 - The Hook

**Files:**
- Modify: `content/post/vibe-infer/index.md`

**Step 1: Write the hook section**

Append after frontmatter. This section should:
- Open with the observation that everyone claims AI helps them learn, but the proof is always anecdotal
- Mention the "I asked ChatGPT and it explained X" pattern as shallow
- Set up the promise: here's a 155-message session captured in full, showing the actual messy learning process
- Brief, punchy. 2-3 paragraphs max.

Key points to hit:
- The gap between "AI helps me learn" claims and actual evidence
- This article shows the receipts
- GPU programming as the domain (intimidating, unfamiliar to author)

Tone: confident, slightly provocative opening. Not arrogant, but direct.

**Step 2: Verify rendering**

Run: `hugo server -D` and check the article renders correctly.

**Step 3: Commit**

```bash
git add content/post/vibe-infer/index.md
git commit -m "Add article hook section"
```

---

### Task 3: Write Section 2 - The Setup (Why GPU Programming?)

**Files:**
- Modify: `content/post/vibe-infer/index.md`

**Step 1: Write the setup section**

This section should:
- Explain why GPU programming specifically. It's genuinely hard, involves new mental models, unfamiliar APIs.
- Mention WebGPU as the target: runs in the browser, compute shaders, WGSL language
- Briefly list what makes it intimidating: workgroups, thread scheduling, buffer management, type strictness
- Set up the question: can AI tools make this learnable in a single session?

Key points:
- GPU programming requires a fundamentally different mental model from CPU code
- WebGPU is the modern browser API for GPU compute (not just graphics)
- The goal was understanding, not just working code

2-3 paragraphs. Technical but accessible.

**Step 2: Verify rendering**

**Step 3: Commit**

```bash
git add content/post/vibe-infer/index.md
git commit -m "Add article setup section"
```

---

### Task 4: Write Section 3 - The Approach + Embed 1

**Files:**
- Modify: `content/post/vibe-infer/index.md`

**Step 1: Write the approach section with embed**

This section explains how the learning worked. Three dynamics:

1. **"I write, Claude reviews"** - Vlad wrote every line of GPU code. Claude caught syntax errors, API misuse, GPU-specific type issues. First vibe coding contrast woven in naturally here: the repo is called vibe-infer as intentional irony. The reality is the opposite of vibe coding.

2. **"Claude handles the boilerplate"** - HTML, CSS, canvas drawing interface. This freed Vlad to focus entirely on the hard, interesting parts (compute shaders, buffer management, parallel execution).

3. **"My pace, my depth"** - Unlike a course or textbook, Vlad controlled when to go deeper and when to move on. Ask for the same concept explained three different ways. Dive into workgroup scheduling because it's fascinating. Skip CSS layout because who cares.

After explaining the approach, insert Embed 1 with narrative wrapper:

```markdown
The first thing I established was the ground rules. Claude would guide, not write. I'm the driver, it's the GPS.

<iframe style="width:100%;height:500px;border:none;" src="https://claudebin.com/threads/jmdbMowNTz/embed?from=7&to=10"></iframe>

With the dynamic set, we started with the basics: getting a WebGPU adapter and device.
```

**Step 2: Verify the iframe renders**

Run: `hugo server -D` and check the article. The iframe should load the claudebin embed.

**Step 3: Commit**

```bash
git add content/post/vibe-infer/index.md
git commit -m "Add article approach section with first embed"
```

---

### Task 5: Write Section 4 - The Journey + Embed 3

**Files:**
- Modify: `content/post/vibe-infer/index.md`

**Step 1: Write the journey section with embed**

Briefly walk through the 8-lesson progression. This should NOT be a full tutorial. It's a narrative summary showing the arc:

1. **WebGPU Bootstrap** - Getting a GPU device. The "hello world."
2. **First Compute Shader** - A simple addition on the GPU. Proof the pipeline works.
3. **Matrix Multiplication** - The core operation of neural networks. Parallel threads, each computing one output element.
4. **ReLU Activation** - "Embarrassingly parallel." Each element independent.
5. **Softmax** - The hardest shader. Reduction operations, numerical stability, three-pass computation.
6. **Forward Pass** - Chaining all kernels together. Keeping data on GPU between operations.
7. **Real Weights** - Loading PyTorch-trained MNIST weights. 97.5% accuracy.
8. **Interactive Demo** - Drawing digits on a canvas, real-time classification.

After the progression summary, insert Embed 3 with narrative wrapper. This is the "code review as learning" moment:

```markdown
The real learning happened in the back-and-forth. Here's what it looked like when I implemented matrix multiplication. I wrote the code, Claude reviewed it, and caught five bugs I would have spent hours debugging on my own.

<iframe style="width:100%;height:500px;border:none;" src="https://claudebin.com/threads/jmdbMowNTz/embed?from=55&to=62"></iframe>

Buffer sizes in bytes, not elements. Uniform buffers need 16-byte alignment. Missing builtin parameters. These are GPU-specific gotchas that a textbook might mention in a footnote, but a tutor catches in your actual code.
```

**Step 2: Verify rendering**

**Step 3: Commit**

```bash
git add content/post/vibe-infer/index.md
git commit -m "Add article journey section with bug hunt embed"
```

---

### Task 6: Write Section 5 - What Made This Different

**Files:**
- Modify: `content/post/vibe-infer/index.md`

**Step 1: Write the insights section**

Two interconnected insights:

**Personalized pacing:**
- Unlike a Udemy course or textbook, there's no predetermined pace
- You can ask Claude to re-explain a concept five different ways until it clicks
- You can go deep into workgroup scheduling because it fascinates you
- You can skip the CSS layout discussion entirely because that's not what you're here to learn
- The curriculum emerged from the conversation, not from someone else's idea of what order you should learn things

**Real-time verification:**
- The learning loop is: write code -> Claude reviews -> catches mistakes -> explains why -> you fix -> you understand
- This is fundamentally different from chatbot Q&A. Claude isn't answering hypotheticals. It's reading your actual code, finding real bugs, and teaching through your mistakes.
- The type strictness example: using `0` instead of `0.0` in WGSL. A textbook tells you "WGSL is strongly typed." A tutor catches it in your code and explains what went wrong.

The vibe coding contrast lands naturally here: "This isn't copy-paste from AI output. I wrote every shader. Claude made sure I understood what I wrote."

3-4 paragraphs. This is the thesis section. It should be the strongest writing in the article.

**Step 2: Verify rendering**

**Step 3: Commit**

```bash
git add content/post/vibe-infer/index.md
git commit -m "Add article insights section"
```

---

### Task 7: Write Section 6 - The Result + Embed 5

**Files:**
- Modify: `content/post/vibe-infer/index.md`

**Step 1: Write the result section with embed**

The payoff:
- 8 lessons completed in a single session
- From `navigator.gpu.requestAdapter()` to a working MNIST classifier
- Every GPU line handwritten
- 97.5% model accuracy, running in the browser via WebGPU
- Interactive canvas demo: draw a digit, get real-time classification

Insert Embed 5 with narrative wrapper:

```markdown
And then it worked.

<iframe style="width:100%;height:500px;border:none;" src="https://claudebin.com/threads/jmdbMowNTz/embed?from=130&to=136"></iframe>

Digit 7, classified at 99.95% confidence. Eight lessons of compute shaders, buffer management, and type wrestling, running entirely in the browser.
```

Link to the live demo: https://vtemian.github.io/vibe-infer/
Link to the repo: https://github.com/vtemian/vibe-infer

**Step 2: Verify rendering**

**Step 3: Commit**

```bash
git add content/post/vibe-infer/index.md
git commit -m "Add article result section with final embed"
```

---

### Task 8: Write Section 7 - Claudebin Mention + Sign-off

**Files:**
- Modify: `content/post/vibe-infer/index.md`

**Step 1: Write the organic claudebin mention and sign-off**

Claudebin mention (2-3 sentences, factual, organic):
- "The entire 155-message session is captured and browsable."
- Mention claudebin as an open-source tool built with Marius for sharing Claude Code sessions
- Link to the full thread: https://claudebin.com/threads/jmdbMowNTz
- Link to claudebin repo: https://github.com/wunderlabs-dev/claudebin.com
- Brief note: if you're using Claude Code and want to share sessions, claudebin is open source

Sign-off:
```
Stay curious ☕
```

**Step 2: Verify full article rendering**

Run: `hugo server -D` and read through the entire article. Check:
- All 3 iframes load
- No broken links
- Article appears in post list
- Formatting is consistent

**Step 3: Commit**

```bash
git add content/post/vibe-infer/index.md
git commit -m "Add claudebin mention and sign-off, complete article draft"
```

---

### Task 9: Vlad review and embed range verification

**Files:**
- Modify: `content/post/vibe-infer/index.md`

**Step 1: Verify embed ranges**

Vlad must check each embed by visiting:
1. https://claudebin.com/threads/jmdbMowNTz/embed?from=7&to=10 - Should show "you don't write code" / GPS metaphor
2. https://claudebin.com/threads/jmdbMowNTz/embed?from=55&to=62 - Should show matmul bug hunt
3. https://claudebin.com/threads/jmdbMowNTz/embed?from=130&to=136 - Should show MNIST digit 7 success

Adjust `from`/`to` values as needed to capture the right messages.

**Step 2: Read through full article for voice/tone**

Since this is personal narrative, Vlad should verify the tone feels authentic.

**Step 3: Remove `draft: true` when satisfied**

Change `draft: true` to `draft: false` in frontmatter.

**Step 4: Final commit**

```bash
git add content/post/vibe-infer/index.md
git commit -m "Finalize vibe-infer article for publication"
```
