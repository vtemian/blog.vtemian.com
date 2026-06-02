---
title: "Claude Code Isn't About Code"
date: 2026-06-02T08:00:00+02:00
description: "The people getting the most out of Claude Code aren't writing code. Some notes on where the value moved, picking up where the disposable tools manifesto left off."
keywords:
    - claude code
    - agent-ready tools
    - tool registry
    - ai-native company
    - disposable tools
    - horseless carriages
    - weak links
    - software economics
    - yc
tags:
    - ai tools
    - software economics
    - agentic-programming
    - ai
draft: false
---

Claude Code isn't a coding tool. The people using it best right now barely touch code. They run factory floors, legal teams, HR, finance, operations. They don't think of it as software. They think of it as *the thing that does the work*.

That took me two months to see. In April I wrote that I'd shipped 20+ tools, made zero revenue, and watched the value move from tools humans use to [tools agents use](/post/disposable-tools-manifesto/). I ended on three words: I don't have the answer.

Then YC published theirs.

## YC stopped building tools

In ["Inside YC's AI Playbook"](https://www.youtube.com/watch?v=B246K_G7mHU), Pete Koomen, Garry Tan, and Jared walk through how YC rebuilt itself internally. YC has always run on its own software, sitting on a single Postgres database that holds everything that matters: every company, every founder, every financial transaction, every note in their internal CRM.

A year ago, the loop looked like every company you've worked at. The finance team would describe a workflow (booking journal entries, logging priced rounds) to software engineers. The engineers would go build purpose-built, deterministic software encoding that workflow. Then they'd hand it back. Koomen's word for it: *inefficient*.

So they killed the loop. Instead of building finance software, they gave the finance team agents and a registry of tools. The first tool that changed everything was almost embarrassingly simple: read-only SQL access to the production database. Jared built it, felt like he was breaking the rules, and pushed it out late at night. It worked extremely well.

{{< diagram-loop >}}

They started with about 20 tools. **At the time of the talk, there were more than 350.** Every team adds their own. Finance books journal entries. Others manage office hours and events. And the same registry feeds both YC's internal agents and Claude Code running on individual laptops.

The effect was a textbook case of [Jevons paradox](https://en.wikipedia.org/wiki/Jevons_paradox). When asking a complex question stopped costing several hours of someone else's SQL time, people didn't just answer the old questions faster. They asked far more questions, and far harder ones, because *asking became cheap*.

## The inversion that makes it work

The reason this is a real shift and not just internal tooling is captured in Koomen's earlier essay, ["AI Horseless Carriages"](https://koomen.dev/essays/horseless-carriages/). His critique was of AI bolted onto existing software as a feature, like Gmail's email writer, where the developer keeps all the control and hides it from the user.

The crux is one sentence, and it's worth reading slowly. **AI-native software is the agent wrapping deterministic tools, not deterministic software wrapping an AI.** Control shifts from the developer to the user.

{{< diagram-inversion >}}

Flip that around and the strategy falls out of it. You stop building the interface. You stop building another finance SaaS, another ERP screen, another internal operations dashboard with its carefully designed flows. Those are horseless carriages: the old shape, with an engine bolted on.

Instead you build small, deterministic, well-scoped tools, you put them in a registry, and you let humans drive the agent that composes them. The plant manager, the lawyer, the HR lead. They get to build whatever they need in the moment, in plain language, without waiting on an engineering backlog. The interface was the constraint. *Removing it is the product.*

This is the answer I was groping for in April. The environment where disposable tools thrive is not hosting and previews and billing dashboards, or not only that. It's a layer of unified context plus a shared tool registry plus a harness that lets agents compose them. The tools inside that layer are disposable by design. The registry and the context are the durable thing. YC built a private one and called it raising the floor: a new hire absorbs the institutional knowledge of the best people in the org through the tools and transcripts, instead of six months of ramp.

There's a price of admission, and the talk is honest about it. You have to be willing to spend somewhere between $10,000 and $100,000 a year on tokens, sometimes more. Garry Tan's framing is that this buys you a one-time time warp: you get to live in 2028 now, and in two years it costs a hundredth as much and everyone does it. That's the optimistic read. Now for the other one.

## Why your economy won't feel this for a decade

If software is this transformative, where's the growth? A talk that dropped the same week, from a very different room, has the answer.

In ["A.I. and Our Economic Future"](https://www.youtube.com/watch?v=xBpGn3BDcOY), Stanford economist Chad Jones offers a model built on a single idea: weak links. A chain is only as strong as its weakest link. Business success requires completing many tasks, and if you make 17 of 20 links incredibly strong, the chain is still limited by the three you didn't touch.

That insight produces an elegant and slightly deflating formula. Infinite automation of a task raises GDP by roughly that task's share of GDP. Software is about 2% of GDP. So if software became infinitely abundant and free tomorrow, we'd be about 2% richer. Not 100 times richer. *Two percent.* Everything else stays a bottleneck.

{{< diagram-weak-links >}}

His killer chart makes it concrete. We carry computers with 100 million times the transistors we had in the 1970s. Yet the share of GDP paid to computing power peaked at about 4.5% in 2000 and has since fallen by a third, to 3%. The price collapse dominates the quantity explosion. **The abundant link loses its share. Value flows to whatever stays scarce.**

That is the mechanism underneath my manifesto, stated more rigorously than I managed. Disposable tools don't become businesses because software is now the cheap, plentiful link. The returns accrue to the scarce weak links: the context, the judgment, the orchestration layer, the human deciding what to ask. I felt that the value had moved. Jones gives you the equation for where it moves and why.

He has the receipts too. In 2016, Geoffrey Hinton said we should stop training radiologists because AI would replace them within five years. A decade later we have more radiologists, and they're paid more. Jobs are bundles of tasks. Automate 75% of them and the remaining 25% become the scarce, valuable, well-paid part. The weak link is wherever the human still has to stand.

## Both talks are right

Here is the tension, and I think it's the whole point. YC says you can live in 2028 today. Jones says the explosion takes 30 years, not three.

They're both correct, at different scales. Inside a single high-trust organization that is willing to tear down its own weak links (locked-down context, command-and-control approvals, siloed tools, the engineering bottleneck between a question and its answer), the 10x is real and available *right now*. YC is the proof. Across the whole economy, the weak links are everywhere and mostly human, and strengthening all of them takes *decades*. Both things are true at once.

That gap is the opportunity, and it has an expiration date. The org that removes its own weak links now gets to operate years ahead of competitors who are still commissioning another internal dashboard. Not because they have a better model. Everyone has the same models. Because they stopped building interfaces and started building a registry.

## The answer, finally

In April I wrote that the tool is not the end, and I left it there because I couldn't name what was. I can now.

Stop building specialized dashboards, interfaces, and flows. Stop building another SaaS for finance, another internal tool for operations, another ERP nobody enjoys. Build small deterministic tools, put them in a registry, give them to agents, and let people drive. The interface was scaffolding. The agent wraps the tools. The human holds the leash.

The tool was never the product. The loop is: a person, an agent, and a registry of tools, composing whatever the moment needs and throwing it away when the moment passes. Claude Code isn't about code. *It never was.*

Stay curious ☕
