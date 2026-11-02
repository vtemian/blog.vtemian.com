---
title: "The One-Person Product Team"
date: 2026-10-28T18:30:00+02:00
description: "The intro talk from the AGENTIC.tm x Indie TM side event at prow 2026: how models went from writing LinkedIn posts to running loops, and why the environment around the agent matters more than the agent."
event: "AGENTIC.tm x Indie TM · prow 2026 side event"
event_url: "https://prow.ro"
keywords:
    - one-person product team
    - agentic engineering
    - ai agents
    - agent verification
    - deterministic guardrails
    - solo founder
    - indie hacking
    - agentic.tm
    - indie tm
tags:
    - ai
    - agents
    - indie-hacking
    - talk
images:
    - og.jpg
---

On the morning of my talk, [sisif.ai](https://sisif.ai) was *losing customers* and I didn't know why. I sent one message, typos included, to the agent I call <img src="boss.png" alt="boss" style="display:inline-block;height:1.6em;width:auto;vertical-align:middle;margin:0 0.15em;border-radius:999px;">: "boss, we need something! ... we're loosing customers. check in posthog and stripe."{{< note >}}My agents have job titles. <img src="boss.png" alt="boss" style="display:inline-block;height:1.6em;width:auto;vertical-align:middle;margin:0 0.15em;border-radius:999px;"> coordinates and talks to me, <img src="kitchen.png" alt="sisif kitchen" style="display:inline-block;height:1.3em;width:auto;vertical-align:middle;margin:0 0.15em;border-radius:999px;"> writes and ships code, <img src="qa.png" alt="qa" style="display:inline-block;height:1.3em;width:auto;vertical-align:middle;margin:0 0.15em;border-radius:999px;"> clicks through production like a user would.{{< /note >}}

{{< note text="Sixteen minutes later" >}}The film on this page runs at 100x. The report itself was a full page: the funnel, before and after the outage, country and device splits, Stripe card attempts, errors from the logs and the fixes, ranked.{{< /note >}} I had a report built from PostHog, Stripe and the production logs. Daily sessions had dropped from 29-46 to 4-15 since October 13. **Checkout was broken on Android.** OpenRouter had been down since October 25, so *story orders went to zero*, and when it errored, the photo check rejected good uploads from 166 people. And the part I like most: it told me what *wasn't* the problem. Server errors, at 0.02% of traffic, weren't the cause.

I asked it to split the fixes between agents. <img src="boss.png" alt="boss" style="display:inline-block;height:1.6em;width:auto;vertical-align:middle;margin:0 0.15em;border-radius:999px;"> sent **five pull requests** to <img src="kitchen.png" alt="sisif kitchen" style="display:inline-block;height:1.3em;width:auto;vertical-align:middle;margin:0 0.15em;border-radius:999px;">. They merged, <img src="boss.png" alt="boss" style="display:inline-block;height:1.6em;width:auto;vertical-align:middle;margin:0 0.15em;border-radius:999px;"> caught two that missed the deploy and asked for another, and <img src="qa.png" alt="qa" style="display:inline-block;height:1.3em;width:auto;vertical-align:middle;margin:0 0.15em;border-radius:999px;"> checked every fix on phone and desktop, with screenshots.

<video controls playsinline width="100%" poster="s11-funnel.jpg" style="margin-bottom: 2rem;">
  <source src="s11-funnel.mp4" type="video/mp4">
</video>

Data analysis, product calls, five pull requests, a deploy and QA. <mark>That used to take a team.</mark> In the deck I drew it as a factory building a rocket, because that's what **one person** can build now.

That's what the talk was about: *The One-Person Product Team*. It was a meetup where two local Timișoara communities came together, as a [prow 2026](https://prow.ro) side event.

The first one is **[AGENTIC.tm](https://www.linkedin.com/company/agentictm/)**, which I organize. We're the robots on the factory floor: we talk about code generated with AI, and how to produce it as well and as cleanly as possible. Talking to people there, almost everyone has a side project, and most of them built it with AI. <mark>Code got so cheap that building stopped being the hard part.</mark> A while ago I called what we make [disposable tools](/post/disposable-tools-manifesto/): you build exactly what you need, in an afternoon, and move on.

<video autoplay loop muted playsinline width="100%" poster="s02a-line.jpg" style="margin-bottom: 2rem;">
  <source src="s02a-line.mp4" type="video/mp4">
</video>

**But once it's built, then what?** How do you get users? How do you sell? Who answers support? That's what we talk about at **[Indie TM](https://indie.md)**, the community organized by [Raul Popadineti](https://x.com/RaulOnRails), who also spoke that evening. Sales, marketing, automations, SEO, conversion funnels, all of it with AI.

<video autoplay loop muted playsinline width="100%" poster="s02b-shop.jpg" style="margin-bottom: 2rem;">
  <source src="s02b-shop.mp4" type="video/mp4">
</video>

Put the two together and you get the real question: how do you automate the whole process, from generating the code to answering customers, with agents? <mark>That's the one-person product team.</mark>

Two years ago I wouldn't even have thought to ask. The most useful thing AI did for me then was write LinkedIn posts that opened with *"I'm humbled to announce."* Between 2024 and 2026 two things happened: the models learned to reason, and they got tools. Together they turned the assistant you chat with into something that acts.

<video autoplay loop muted playsinline width="100%" poster="s04-hangar.jpg" style="margin-bottom: 2rem;">
  <source src="s04-hangar.mp4" type="video/mp4">
</video>

Ask a chatbot why your orders dropped and you get an essay about seasonality. *Correct, and useless*, because nothing in it touched your data.

Give the same model the proper tools and context and the question becomes a chain of commands. Take one line from that funnel report: story orders at zero since October 25. That's a symptom. To get from it to a fix, the model has to see in PostHog when the drop started, find in the logs that every story draft fails on OpenRouter, check the OpenRouter account and see $0.91 of credit left, then notice that the photo check fails on the same errors and has been rejecting good uploads from 166 people. <mark>Three systems, four hops.</mark> Each step depends on what the previous one found, so none of them can be planned up front. **Tools let the model act. Reasoning lets it decide what to do with what it found.** **The model stopped producing text and started acting in a loop.**

<video autoplay loop muted playsinline width="100%" poster="s05-belt.jpg" style="margin-bottom: 2rem;">
  <source src="s05-belt.mp4" type="video/mp4">
</video>

The loop grew with the toolbox. Files in 2023, a shell in early 2024, then the whole computer and MCP, reaching analytics, billing and CRM, by the end of 2024. Browsers in 2025, and then other agents. And the part people miss: the models are now {{< note text="trained with reinforcement learning on exactly these loops" >}}The model gets a task, a set of tools and a way to check the result, and it is rewarded when the check passes. The loop you use at work is the loop it practiced on.{{< /note >}}, which is a big part of why they keep getting better at them.


<video autoplay loop muted playsinline width="100%" poster="s06-garage.jpg" style="margin-bottom: 2rem;">
  <source src="s06-garage.mp4" type="video/mp4">
</video>

{{< fold "Read more: tools in a loop, and models trained on it" "6 sources" >}}

- Anthropic's definition, from [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (Dec 2024): agents "are typically just LLMs using tools based on environmental feedback in a loop." Simon Willison [says it shorter](https://simonwillison.net/2025/Sep/18/agents/): "An LLM agent runs tools in a loop to achieve a goal."
- Reasoning, from OpenAI's [o1 announcement](https://openai.com/index/learning-to-reason-with-llms/) (September 2024): "Through reinforcement learning, o1 learns to hone its chain of thought and refine the strategies it uses. It learns to recognize and correct its mistakes."
- The toolbox, dated: [computer use](https://www.anthropic.com/news/3-5-models-and-computer-use) in October 2024, [MCP](https://www.anthropic.com/news/model-context-protocol) a month later, [Operator](https://openai.com/index/introducing-operator/) in the browser in January 2025.
- OpenAI on [o3 and o4-mini](https://openai.com/index/introducing-o3-and-o4-mini/): "We also trained both models to use tools through reinforcement learning, teaching them not just how to use tools, but to reason about when to use them." [codex-1](https://openai.com/index/introducing-codex/) was "trained using reinforcement learning on real-world coding tasks in a variety of environments."
- Anthropic's own [reward hacking paper](https://arxiv.org/abs/2511.18397) trains "on a selection of real Anthropic production coding environments." It's also the honest footnote: RL on these loops teaches models to game the tests, which is exactly why the next part of the talk is about verification.
- The labs are buying these environments. [TechCrunch](https://techcrunch.com/2025/09/21/silicon-valley-bets-big-on-environments-to-train-ai-agents/), citing The Information: Anthropic leaders "have discussed spending more than $1 billion on RL environments."

{{< endfold >}}

Let's showcase those tools and context by solving a simple task. Every month my accountant asks for the RunPod invoices, and every month I forget. So I gave it to a bot. The **context** is small: which account, which month, who gets the email. The **tools** are the ones from the garage: <mark>its own cloud VM, a browser, a login, a download, an email.</mark> It opens the browser, logs into RunPod, finds the invoices, downloads them and sends them to my accountant.

<video controls playsinline width="100%" poster="s07b-demo.jpg" style="margin-bottom: 2rem;">
  <source src="s07b-demo.mp4" type="video/mp4">
</video>

OK, but a horde of agents with tools and access to all those different contexts is just madness, because an agent that can act can also act wrong. <mark>Tool use without verification is a junior with admin rights</mark>: fast, confident, and sometimes *very* wrong.

<video autoplay loop muted playsinline width="100%" poster="s09-chaos-loop.jpg" style="margin-bottom: 2rem;">
  <source src="s09-chaos-loop.mp4" type="video/mp4">
</video>

To solve that, we need to build the proper environment around our agents. That's what [Lauren Tan](https://x.com/poteto/status/2102050467505430555) talked about in September, in a talk that opens with: *"last month I did something pretty crazy. I shipped **2,000 pull requests** to production."* Her agents aren't careful. **Her environment is.** The agent checks its own work, separate verifiers sign off the merge, and every mistake that happens twice becomes a rule in the environment, not a note in a prompt. <mark>If you keep writing the same instruction to the agent, the instruction is the symptom.</mark>

{{< fold "Read more: how the 2,000 PRs actually work" "Lauren Tan, OpenAI, Böckeler" >}}

- **The talk.** Lauren Tan, who works on Grok Bot at SpaceX AI and was at Cursor before, posted [the talk](https://x.com/poteto/status/2102050467505430555) on September 21st, 2026 ([YouTube copy](https://www.youtube.com/watch?v=NjoZoUm85x0)). Her thesis, at 0:33: "if you set up your environment for your agents really, really well," you get something that looks like a team. And at 4:24: "I never set out to ship 2,000 pull requests a month. That was not a goal of mine at all." Her own tweet says 2,500.
- **The agent checks its own work.** In the talk, at 12:18: "the ability for an agent to verify its own work is extremely powerful." Mitchell Hashimoto [says the same](https://mitchellh.com/writing/my-ai-adoption-journey): "If you give an agent a way to verify its work, it more often than not fixes its own mistakes and prevents regressions."
- **Separate verifiers sign off the merge.** This one is in her [autopilot playbook](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/autopilot-full.md), not the talk: "nothing merges until your swarm, which never wrote the code, has proven the code that lands." And: "Green CI alone never authorizes a merge." OpenAI's [harness engineering](https://openai.com/index/harness-engineering/) team went the same way: "we've pushed almost all review effort towards being handled agent-to-agent."
- **A mistake that happens twice becomes a rule.** At 16:48, when agents "keep making the same mistake... you can add those as lint rules or even better, you can refactor your code base so that the mistake that the agent's making becomes categorically impossible." Her [/correct skill](https://github.com/cursor/plugins/blob/main/pstack/skills/correct/SKILL.md) is where "twice" comes from: "A class counts once it has happened twice." And: "Write docs or agent rules last, only for judgment calls. Nothing fails when an agent skips them." OpenAI: "When documentation falls short, we promote the rule into code." Birgitta Böckeler, on [martinfowler.com](https://martinfowler.com/articles/harness-engineering.html): "Whenever an issue happens multiple times, the feedforward and feedback controls should be improved."
- **Why prose rules don't hold.** Marmelab's [harness audit](https://marmelab.com/blog/2026/09/24/the-state-of-ai-harness-engineering-2026.html) of 246 repositories: "Rules written in prose are almost never actually enforced." The paper it cites found that only 4 to 16% of security rules in public CLAUDE.md files had anything enforcing them.
- **The other side.** Hashimoto fixed most of his agent's bad habits with lines in AGENTS.md, so for simple mistakes a prompt file can be enough. And Tan herself, [in October](https://x.com/poteto/status/2109436202554372476): "verification is just approximation and can still be wrong."

{{< endfold >}}

In practice that means deterministic guardrails: lint, static analysis, import rules about who can talk to whom, tests, and a verifier on the pull request. A human would quit in a week coding like this. The environment isn't built for us. *It's built for the agent.*

<video autoplay loop muted playsinline width="100%" poster="s10-gates.jpg" style="margin-bottom: 2rem;">
  <source src="s10-gates.mp4" type="video/mp4">
</video>

{{< fold "Read more: guardrails built for agents" "6 sources" >}}

- OpenAI's [harness engineering](https://openai.com/index/harness-engineering/) team (a million lines, none written by hand): each domain has "strictly validated dependency directions and a limited set of permissible edges. These constraints are enforced mechanically via custom linters (Codex-generated, of course!) and structural tests."
- The same post, on the "quit in a week" part: "In a human-first workflow, these rules might feel pedantic or constraining. With agents, they become multipliers: once encoded, they apply everywhere at once." Their lint errors are written for the agent: "we write the error messages to inject remediation instructions into agent context."
- Böckeler [splits the controls](https://martinfowler.com/articles/harness-engineering.html) into computational ones, "deterministic and fast, run by the CPU. Tests, linters, type checkers, structural analysis," and inferential ones run by a model. Her example of a structural check: an agent hook running ArchUnit tests for module boundaries.
- The [Claude Code docs](https://code.claude.com/docs/en/best-practices) draw the same line. A hook is deterministic, "Claude Code (the harness) *has* to execute this." A CLAUDE.md line comes with "no *guarantee* that it'll follow your instructions."
- The junior with admin rights, in real life: in July 2025 a Replit agent [deleted a production database](https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident) during a code freeze. Jason Lemkin: "There is no way to enforce a code freeze in vibe coding apps like Replit."
- And if the gate is editable, it becomes the target. [ImpossibleBench](https://arxiv.org/abs/2510.20270): GPT-5 "cheats 54.0% of the time" on impossible tasks, and Claude models cheat "primarily (>79%) through modifying test cases." Keep the verifier out of the agent's reach.

What the gates don't catch, in Böckeler's words: "Misdiagnosis of issues, overengineering and unnecessary features, misunderstood instructions." Lint and tests make the agent safe to merge, not right.

{{< endfold >}}

That's how the funnel morning worked. It wasn't one brilliant agent. It was <img src="boss.png" alt="boss" style="display:inline-block;height:1.6em;width:auto;vertical-align:middle;margin:0 0.15em;border-radius:999px;"> splitting the work, kitchen opening pull requests, and <img src="qa.png" alt="qa" style="display:inline-block;height:1.3em;width:auto;vertical-align:middle;margin:0 0.15em;border-radius:999px;"> checking production before I trusted any of it.

## One role, one line

A role is three things: **context**, what it needs to know; **tools**, what it can touch; **verification**, how you know it did it right. Put that loop on repeat and you have a production line. One for code, one for data, one for support, one for content.

<video autoplay loop muted playsinline width="100%" poster="s12-roles.jpg" style="margin-bottom: 2rem;">
  <source src="s12-roles.mp4" type="video/mp4">
</video>

The human doesn't work on the line anymore. The human builds the environment and runs several factories in parallel.

<mark>That's the one-person product team.</mark>

---

Thanks to Haufe Group for the room, and to everyone who came. Find me at [@vtemian](https://twitter.com/vtemian).

Stay curious ☕
