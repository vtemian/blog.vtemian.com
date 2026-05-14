---
title: "Fight Slop with Clarity"
date: 2026-05-14
author: Vlad Temian
url: https://blog.vtemian.com/post/fight-slop-with-clarity/
description: "AI made slop cheap. We made more of it, faster. Clarity is the only input that doesn't degrade when you multiply it."
tags: [ai tools, vibe-coding, software economics]
---

# Fight Slop with Clarity


AI made slop cheap. We made more of it, faster. I made my share. Here's the part I missed.

**Slop isn't what AI produces. Slop is what any multiplier produces when there's no clarity behind it.** Simon Willison, who [popularized *AI slop*](https://simonwillison.net/2024/May/8/slop/), drew the parallel directly: slop is to AI-generated content what spam became for email. The model isn't the problem. *The clarity behind it is.*

The model is a multiplier. Whatever clarity you bring, it scales. Whatever fog you bring, it scales the same. The output looks impressive in both cases. Only one of them is signal.

The fight isn't against AI. It isn't against slop either, not directly. The fight is for clarity. Clarity is the only input that, when multiplied at industrial speed, doesn't degrade. Everything else turns into noise.

## The AI Productivity Gap

The faster AI helps you build, the less you ship that matters. *Volume goes up. Signal goes down.* [METR's 2025 randomized trial](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) caught the pattern at scale: experienced developers using AI tools were **19% slower** at completing real issues in their own codebases. The strange part wasn't the slowdown. It was that, even after shipping the work, they still believed they'd been **20% faster**. A forty-point gap between perception and reality, and the perception held even with the evidence in front of them. I lived a smaller version of that and called it progress.

## I've Seen This Before. So Have You.

Every company I've worked at hit the same wall. Things break. Someone proposes a procedure. The procedure works for a month. Then a use case appears that the procedure didn't anticipate. Someone improvises. Someone else writes a new procedure to cover the gap. The procedure stack grows. Compliance drops. The procedures stop describing what people *do* and start describing what people *pretend* to do. [Goodhart's Law](https://en.wikipedia.org/wiki/Goodhart%27s_law) in office form: when a measure becomes a target, it ceases to be a good measure. The work is the same as before, just buried under more documentation.

The procedure wasn't the fix. Clarity about what we were trying to protect was the fix. Without that, the procedure was a layer of fog dressed up as control. **There was no AI in this room.** We have been making slop by hand for decades, in meetings, in procedures, in code. AI didn't invent the pattern. It just made the multiplier cheap enough to use everywhere.

If you've played Factorio, you know this feeling at the level of muscle memory. You build a base. It works for a while. You unlock a new tier of technology. The new tech demands more inputs, faster throughput, different geometries. Your old base can't handle it. You bolt new belts onto the old layout. The base survives, technically, but moving anything through it takes ten times longer. You unlock another tier. You bolt more belts. At some point you realize the only fix is to tear the whole thing down and design it again from the start.

Nobody who has played Factorio thinks the next technology tier solves the spaghetti. The spaghetti is a clarity problem. **Tier 5 just makes the spaghetti more expensive.**

That's exactly what I did to my own work. I unlocked AI as the new tier. I bolted it onto a base that was never clear in the first place. What was I building? For whom? Solving what? I didn't have answers. I had *energy*. So I shipped. The AI multiplied the shipping. The shipping multiplied the unclarity. The base got louder, busier, and no closer to a thing anyone needed.

This is what slop looks like from the inside. Not bad code. Not low-effort prompts. Genuine work, technically correct, multiplied without a question to anchor it.

## Clarity is Infrastructure, Not Aesthetic

We talk about clarity like it's a writing virtue. Use shorter sentences. Cut adjectives. That's not what I mean.

Clarity is the answer to a small set of unsexy questions. What problem am I actually solving? Whose problem is it? What does success look like, concretely, that I'd recognize when I see it? What am I willing to not build to keep this clear?

These questions are slow. They don't ship anything. They feel like procrastination next to the warm dopamine of generating another tool. But they are the only input that, when fed into a multiplier, produces signal instead of noise.

Kentaro Toyama, who spent two decades watching technology interventions either work or [amplify dysfunction](https://www.si.umich.edu/about-umsi/news/toyama-ai-amplifies-good-and-bad-society) in international development, formalized this as the Law of Amplification: technology's primary effect is to amplify human forces. *"ChatGPT helps honest writers brainstorm and helps bad students cheat."* The model is neutral. The forces it scales aren't.

**Without clarity, AI is the most expensive way ever invented to be busy.**

## A Test

Here's the operational version, the one you can use today on any tool you're considering, building, or shipping.

**If a tool sells itself as a replacement for thinking clearly, it's a tarpit.** The more you use it, the deeper the dysfunction it's covering for, and the less likely you are to ever climb out.

**If a tool sells itself as an amplifier for someone who already thinks clearly, it works.** The clearer the user, the better the output. The multiplier finally has something worth multiplying. (I wrote about how to build this kind of [amplifier in Harness Engineering](/post/harness-engineering/)).

[Andrej Karpathy coined *vibe coding*](https://x.com/karpathy/status/1886192184808149383) in February 2025: *"I just see stuff, say stuff, run stuff, and copy paste stuff, and it mostly works."* A year later he [refined the framing](https://thenewstack.io/vibe-coding-is-passe/), introducing *agentic engineering* for production work. I documented my own transition from "vibing" to systematic learning in my [vibe-infer case study](/post/vibe-infer/). The slop-friendly version was for throwaways. The serious version requires thinking first. The person who named the vibe ended up at the same place: clarity is the part you can't outsource.

This applies to AI. It applies to project management software. It applies to the procedures at every company you've ever worked at. The version of any thesis that survives is the one built for users who already know what problem they're solving. Not for users who reach for AI to figure out what their problem is.

## The Only Input

The fight isn't against AI. It's against everything that lets us avoid clarity. Including the multiplier we love most.

Tools come and go. Multipliers get bigger. *Clarity is the only input that doesn't decay when scaled.* Bring it, or watch the slop scale instead.

### Key Takeaways

*   **AI is a Multiplier:** It scales whatever you feed it. Feed it fog, you get slop. Feed it clarity, you get signal.
*   **The Perception Gap:** Developers using AI often *feel* 20% faster while actually being 19% slower due to the overhead of managing unvetted output.
*   **Clarity as Infrastructure:** Thinking is not procrastination. It is the only input that doesn't degrade at industrial speeds.
*   **The Tarpit Test:** If a tool tries to replace your thinking, avoid it. If it amplifies your existing clarity, use it.

Stay curious ☕

