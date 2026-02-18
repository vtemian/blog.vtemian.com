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

Everyone has a story about how AI helped them learn something. "I asked ChatGPT to explain monads and it finally clicked." Cool. But where's the actual session? Where's the messy back-and-forth where you got confused, the AI corrected you, and you iterated until understanding emerged?

Most AI-assisted learning stories are sanitized after the fact. You get the polished takeaway, not the process. The repo is called [vibe-infer](https://github.com/vtemian/vibe-infer) and that's intentional irony, because what happened here is the opposite of vibe coding. I wrote every line of GPU code. The AI was my tutor, not my ghostwriter.

This article shows the receipts. 155 messages, captured in full, from zero WebGPU knowledge to a working MNIST classifier running compute shaders in the browser.

## Why GPU Programming?

GPU programming requires a fundamentally different mental model from writing regular application code. On a CPU, you think sequentially: fetch data, process it, return a result. On a GPU, thousands of threads execute the same instruction simultaneously across different data. You stop thinking about loops and start thinking about thread indices, workgroups, and memory barriers.

[WebGPU](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API) is the modern browser API for GPU compute. Not just graphics rendering, but general-purpose parallel computation. The shader language is [WGSL](https://www.w3.org/TR/WGSL/), which looks like Rust but with its own type system and execution model. Buffers are raw bytes. There are no arrays in the JavaScript sense. You manage memory layout, type alignment, and dispatch dimensions manually.

I wanted to build a neural network from scratch on the GPU. Not by importing a framework, but by writing every compute shader by hand. Matrix multiplication, ReLU activation, softmax normalization, forward pass chaining. The goal was understanding the machinery, not just producing a working demo.

## The Approach: Claude as Tutor

I used [Claude Code](https://claude.ai/code), Anthropic's agentic coding tool, as a pair programming partner. But the first thing I established was the dynamic: Claude guides, I write. It explains concepts, reviews my code, catches mistakes. It does not write GPU code for me.

<iframe style="width:100%;height:500px;border:none;" src="https://claudebin.com/threads/jmdbMowNTz/embed?from=7&to=10"></iframe>

With the ground rules set, three dynamics emerged.

**I write the GPU code, Claude reviews it.** Every compute shader, every buffer allocation, every dispatch call was written by my hands. Claude's role was code reviewer: catching syntax errors, pointing out API misuse, explaining GPU-specific type requirements. When I used `0` instead of `0.0` in a WGSL shader, Claude didn't just flag it. It explained why WGSL enforces strict typing and what happens when type coercion fails on the GPU.

**Claude handles the boilerplate.** HTML scaffolding, CSS layout, the canvas drawing interface. None of that teaches GPU programming. Offloading it meant I could spend 100% of my mental energy on the hard, interesting parts: how workgroups distribute threads, why uniform buffers need 16-byte alignment, how reduction operations work in softmax.

**My pace, my depth.** Unlike a course with a fixed curriculum, I controlled when to go deeper and when to move on. If workgroup scheduling fascinated me, I could ask Claude to explain dispatch dimensions three different ways. If I already understood buffer creation, I could skip ahead. The curriculum emerged from the conversation, shaped by my curiosity and my gaps.
