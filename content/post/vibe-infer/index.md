---
title: "vibe-infer: Learning GPU Programming with Claude Code"
date: 2026-02-18T12:00:00+02:00
description: "Everyone talks about AI-assisted learning. Here's what it actually looks like. From zero WebGPU knowledge to a working MNIST classifier in 155 messages."
keywords:
    - gpu programming
    - webgpu
    - wgsl
    - claude code
    - ai assisted learning
    - vibe coding
    - mnist
    - compute shaders
    - neural networks from scratch
tags:
    - gpu programming
    - ai tools
    - webgpu
    - wgsl
    - vibe-coding
    - learning
draft: false
---

Everyone has a story about how AI helped them learn something. "I asked ChatGPT to explain monads and it finally clicked." But these stories are almost always sanitized after the fact. You get the polished takeaway, but you lose the "messy middle"—the confusion, the corrections, and the specific failure modes that actually lead to understanding.

This post is the opposite of the "vibe coding" trend where the AI writes the code and you just ship it. I call this repo [vibe-infer](https://github.com/vtemian/vibe-infer) as a piece of intentional irony. I wrote every single line of GPU code. The AI was my tutor, not my ghostwriter.

This is the receipt: 155 messages, captured in full, from zero WebGPU knowledge to a working MNIST classifier running compute shaders in the browser.

## Why GPU Programming?

GPU programming requires a fundamentally different mental model from writing regular application code. On a CPU, you think sequentially: fetch data, process it, return a result. On a GPU, thousands of threads execute the same instruction simultaneously across different data. You stop thinking about loops and start thinking about thread indices, workgroups, and memory barriers.

[WebGPU](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API) is the modern browser API for GPU compute. Not just graphics rendering, but general-purpose parallel computation. The shader language is [WGSL](https://www.w3.org/TR/WGSL/), which looks like Rust but with its own type system and execution model. Buffers are raw bytes. There are no arrays in the JavaScript sense. You manage memory layout, type alignment, and dispatch dimensions manually.

I wanted to build a neural network from scratch on the GPU. Not by importing a framework, but by writing every compute shader by hand. Matrix multiplication, ReLU activation, softmax normalization, forward pass chaining. The goal was understanding the machinery, not just producing a working demo.

## The Approach: Claude as Tutor

I used [Claude Code](https://claude.ai/code), Anthropic's agentic coding tool, as a pair programming partner. But the first thing I established was the dynamic: Claude guides, I write. It explains concepts, reviews my code, catches mistakes. It does not write GPU code for me. (I've written a deeper dive into why Claude Code's choice of [MCP for its plugin architecture](https://blog.vtemian.com/post/mcp-is-great-for-tools-terrible-for-agents/) makes it great for tools but presents challenges for more complex agentic behaviors).

<iframe style="width:100%;height:1000px;border:none;" src="https://claudebin.com/threads/jmdbMowNTz/embed?from=7&to=10"></iframe>

With the ground rules set, three dynamics emerged.

**I write the GPU code, Claude reviews it.** Every compute shader, every buffer allocation, every dispatch call was written by my hands. Claude's role was code reviewer: catching syntax errors, pointing out API misuse, explaining GPU-specific type requirements. When I used `0` instead of `0.0` in a WGSL shader, Claude didn't just flag it. It explained why WGSL enforces strict typing and what happens when type coercion fails on the GPU.

**Claude handles the boilerplate.** HTML scaffolding, CSS layout, the canvas drawing interface. None of that teaches GPU programming. Offloading it meant I could spend 100% of my mental energy on the hard, interesting parts: how workgroups distribute threads, why uniform buffers need 16-byte alignment, how reduction operations work in softmax.

**My pace, my depth.** Unlike a course with a fixed curriculum, I controlled when to go deeper and when to move on. If workgroup scheduling fascinated me, I could ask Claude to explain dispatch dimensions three different ways. If I already understood buffer creation, I could skip ahead. The curriculum emerged from the conversation, shaped by my curiosity and my gaps.

## The Journey: 8 Lessons from Zero to Inference

The session naturally organized itself into eight progressive lessons, each building on the last until I had a full neural network running on the GPU.

### **The Softmax Wall: A Deep Dive into WGSL**

The hardest part wasn't the matrix multiplication; it was Softmax. Unlike a simple ReLU, where every thread is independent, Softmax requires every output element to know about every *other* element in the vector.

On a CPU, this is a simple loop. On a GPU, you have to worry about numerical stability. If you naively exponentiate a value like `80`, you get a number larger than the maximum value for a 32-bit float. The entire network collapses into `NaN`.

I had to implement a **numerically stable Softmax**, which involves finding the maximum value in a vector first, subtracting it from every element, and *then* exponentiating. This is how the actual WGSL kernel looks:

```wgsl
@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) global_id: vec3<u32>) {
    let i = global_id.x;
    if (i >= params.input_size) { return; }

    // 1. Find max (for numerical stability)
    var max_val = -3.402823466e+38f; // min float
    for (var k = 0u; k < params.input_size; k = k + 1u) {
        max_val = max(max_val, input[k]);
    }

    // 2. Compute sum of exponentials
    var sum = 0.0f;
    for (var k = 0u; k < params.input_size; k = k + 1u) {
        sum = sum + exp(input[k] - max_val);
    }

    // 3. Normalize and output
    output[i] = exp(input[i] - max_val) / sum;
}
```

This isn't the most optimized way to do it (a parallel reduction would be faster), but it's the version where I finally understood how GPU memory barriers and float limits work. Claude didn't just give me this code; it watched me struggle with `NaN` outputs for thirty messages until I understood *why* I needed the `max_val` subtraction.

It started with **WebGPU Bootstrap**: acquiring a GPU adapter and device. The "hello world" of GPU programming. Then a **First Compute Shader** that added two numbers on the GPU. Simple, but it proved the entire pipeline worked: buffer creation, shader compilation, command encoding, dispatch, and result readback.

**Matrix Multiplication** was where things got real. This is the core operation of neural networks, and on the GPU, each thread computes a single element of the output matrix. You index into flat memory using `row * numColumns + col` because GPU buffers have no concept of rows or columns. Just raw bytes.

**ReLU Activation** was a welcome breather. An "embarrassingly parallel" operation where every element is independent. No coordination between threads, no shared state. Just `max(value, 0.0)` across thousands of elements simultaneously.

**Softmax** was the hardest shader. Unlike ReLU, every output element depends on every other element. You need three passes: find the maximum (for numerical stability), compute exponentials and their sum, then normalize. Getting this right meant understanding reduction operations, race conditions, and why naively exponentiating large numbers produces infinity.

The **Forward Pass** chained all kernels together. The critical insight here: keep data on the GPU between operations. Reading results back to JavaScript after each step would kill performance. One command encoder, multiple compute passes, data flowing between buffers without ever touching the CPU.

**Real Weights** brought the system to life. A Python script trained a 784-to-128-to-10 network on MNIST (97.5% accuracy), exported the weights as raw binary, and loaded them into GPU buffers. The final lesson was an **Interactive Canvas Demo**: draw a digit, watch the GPU classify it in real-time.

Here's what the learning actually looked like. I implemented the matrix multiplication kernel, and Claude reviewed my code line by line.

<iframe style="width:100%;height:1000px;border:none;" src="https://claudebin.com/threads/jmdbMowNTz/embed?from=55&to=62"></iframe>

Buffer sizes in bytes, not elements. Uniform buffers need 16-byte alignment. Missing builtin parameters for thread identification. These are GPU-specific gotchas that a textbook mentions in a footnote. A tutor catches them in your actual code and explains why they matter.

## What Made This Different

Two things separated this from reading documentation or watching a YouTube tutorial.

**The learning was personalized.** I didn't follow someone else's idea of what order to learn things. When Claude introduced softmax and I didn't fully grasp why subtracting the maximum before exponentiation prevents overflow, I asked it to explain numerical stability from first principles. We went down that rabbit hole until it clicked. When I already understood ReLU from prior ML experience, we spent thirty seconds on it and moved on. No filler, no padding, no waiting for the rest of the class.

This is the part that surprised me most. I could verify my understanding in real-time. The loop looked like this: I write a shader, Claude reads it, finds the bugs I can't see yet, and explains not just *what's* wrong but *why* GPU programming works that way. It's not Q&A. It's closer to a code review where the reviewer happens to be infinitely patient and knows every corner of the WebGPU spec.

The difference from vibe coding is worth stating plainly. In vibe coding, the AI writes the code and you ship it. Here, I wrote the code and the AI made sure I understood it. Every bug Claude caught was a concept I internalized. Every correction was a lesson I wouldn't need to learn again. The understanding compounds in a way that copy-pasting from an AI chat never does.

## The Result

And then it worked.

<iframe style="width:100%;height:900px;border:none;" src="https://claudebin.com/threads/jmdbMowNTz/embed?from=130&to=136"></iframe>

Digit 7, classified at 99.95% confidence. Eight lessons of compute shaders, buffer management, and type wrestling, running entirely in the browser. No backend, no ML framework, no CUDA. Just WebGPU, WGSL, and a neural network I built from scratch.

You can [try the live demo](https://vtemian.github.io/vibe-infer/) or browse [the source code](https://github.com/vtemian/vibe-infer). Every GPU line was written by hand. The repo includes a [LESSONS.md](https://github.com/vtemian/vibe-infer/blob/main/LESSONS.md) file summarizing what each lesson covered.

The entire 155-message session is captured and browsable at [claudebin.com](https://claudebin.com/threads/jmdbMowNTz). I built [claudebin](https://github.com/wunderlabs-dev/claudebin.com) with [Balaj Marius](https://balajmarius.com/) as an open-source tool for sharing Claude Code sessions. If you're using Claude Code and want to share a session with your team or publicly, it's one command to publish and get a shareable link.

Stay curious ☕
