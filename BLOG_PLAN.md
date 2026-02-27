# Blog Plan: Repositioning blog.vtemian.com

**Created:** 2026-02-21
**Status:** Active
**Supports:** [MASTER_PLAN.md](/Users/whitemonk/projects/dd/MASTER_PLAN.md)

---

## Goal

Transform blog.vtemian.com from a scattered personal blog into a focused portfolio that answers one question in 30 seconds: **"Who is Vlad Temian and what does he build?"**

Answer: *A systems engineer who builds agentic programming tools and writes about making agents reliable and accessible.*

---

## 1. Site Identity Updates

### config.toml

Current description:
> "I build systems. Over 15 years helping startups scale production infrastructure. Former CTO of qed.builders (acquired by The Sandbox). Long-time open-source contributor with a systems caretaker mindset."

**Proposed description:**
> "I build agentic programming tools. 15+ years of systems infrastructure experience, now focused on making AI agents reliable and accessible for developers. Former CTO, open-source builder, community organizer at agentic.tm."

**Update keywords/tags:**
```toml
keywords = ["vtemian", "agentic programming", "ai tools", "claude code", "developer tools", "open source"]
tags = ["vtemian", "agentic programming", "ai tools", "developer tools"]
```

### Homepage bio (layouts/_default/list.html)

Current:
> "I build systems and bypass permissions. Over 15 years helping startups scale production infrastructure. Former CTO of qed.builders (acquired by The Sandbox). Long-time open-source contributor with a systems caretaker mindset."

**Proposed:**
> "I build agentic programming tools. 15+ years helping startups scale production infrastructure. Former CTO of qed.builders (acquired by The Sandbox). Organizer at agentic.tm. I believe everyone should be able to ship ideas."

This connects the bio directly to the narrative without losing the credibility signals.

---

## 2. Project Pages to Add

Each project page follows the existing claude-notes format:
- `{{< github-stats >}}` shortcode at the top
- Problem statement (why this exists)
- Usage examples with code/screenshots/video
- Implementation notes (brief)
- GitHub link
- "Stay curious ☕"

### 2.1 micode (Priority: HIGH, 213 stars)

**Path:** `content/project/micode/index.md`

**Angle:** Your most mature project. The structured workflow (brainstorm/plan/implement) is opinionated and reflects your philosophy about how agentic development should work. This is the closest thing to a flagship.

**Sections:**
- Problem: AI coding tools are powerful but chaotic. No structure, no workflow, no quality gates.
- What micode does: structured brainstorm/plan/implement cycle, parallel micro-tasks, TDD enforcement, session continuity via ledger files
- Demo: show the workflow in action (video or claudebin embed)
- Philosophy: why structure matters in agentic development
- Link to GitHub

### 2.2 octto (Priority: HIGH, 141 stars)

**Path:** `content/project/octto/index.md`

**Angle:** "10 minutes of terminal typing to 2 minutes of clicking." Solves the UX problem of interacting with AI agents.

**Sections:**
- Problem: brainstorming with AI agents in a terminal is slow and painful
- What octto does: interactive browser UI with 14 input types, parallel exploration branches
- Demo: before/after comparison (terminal vs octto UI)
- How it works: three-agent architecture (bootstrapper, probe, octto)
- Link to GitHub

### 2.3 claudebin.com (Priority: MEDIUM, under Wunderlabs)

**Path:** `content/project/claudebin/index.md`

**Angle:** Already referenced in the vibe-infer post. Make it a proper project page. Frame it as infrastructure for the agentic programming community.

**Sections:**
- Problem: AI coding sessions are ephemeral. You can't share, reference, or learn from them.
- What claudebin does: publish, share, embed, continue Claude sessions
- Demo: embed a session, show the sharing flow
- Community angle: featured threads, how the community uses it
- Link to claudebin.com and GitHub

### 2.4 opencode-reskin (Priority: LOW, 5 stars)

**Path:** `content/project/opencode-reskin/index.md`

**Angle:** Smaller project, but demonstrates multi-agent architecture in practice. Good "show your work" piece.

**Sections:**
- Problem: reskinning a web project manually is tedious
- What it does: AI-powered style analysis and transformation planning
- Architecture: three specialized agents working together
- Link to GitHub

---

## 3. Editorial Calendar

### Content Pillars (every post connects to at least one)

1. **Building agentic tools** - lessons from shipping micode, octto, claudebin, etc.
2. **Agent reliability** - failure modes, trust, observability, production gotchas
3. **Agentic programming for developers** - workflows, comparisons, real-world usage
4. **Community insights** - patterns from agentic.tm meetups, what developers are struggling with

### Post Ideas (Priority Ordered)

**Batch 1 (Months 1-2): Establish the narrative**

- [ ] **"Why I'm betting on agentic programming"**
  Manifesto post. Why you believe everyone should ship ideas. What agentic programming means. Where the space is going. This is the post you link from your Twitter bio.

- [ ] **"What developers actually struggle with in AI coding tools"**
  Synthesize insights from agentic.tm meetups. Real pain points, not theoretical ones. The reliability/trust angle emerges naturally here.

- [ ] **"Building micode: structured workflows for agentic development"**
  Deep dive into the philosophy behind micode. Why brainstorm-before-code matters. How parallel micro-tasks work. Not a README. The "why" behind the design decisions.

**Batch 2 (Months 2-4): Build depth**

- [ ] **"The failure modes nobody talks about in AI coding assistants"**
  Agent reliability piece. Context loss, hallucinated APIs, cascading errors. Your systems background applied to AI tools. This is the kind of post that gets shared on Hacker News.

- [ ] **"How I use Claude Code on a production codebase"**
  Practical, workflow-focused. Not "look how cool AI is." Real strategies for reliability: the superpowers skills system, verification steps, structured debugging. Show the discipline.

- [ ] **"10 minutes of typing to 2 minutes of clicking: why I built octto"**
  The UX problem with terminal-based AI interactions. How octto solves it. Design decisions.

**Batch 3 (Months 4-6): Establish authority**

- [ ] **"Agent observability: what we're missing"**
  Systems thinking applied to AI agents. How do you know what an agent did? How do you debug failures? How do you build trust? This is your sweet spot.

- [ ] **"Running an agentic programming meetup: what I've learned"**
  Community-building + technical insights. What talks resonated. What questions keep coming up. Position yourself as someone who understands the ecosystem, not just one tool.

- [ ] **"Comparing agentic coding tools: Claude Code vs Cursor vs Copilot Agents"**
  Opinionated comparison from someone who builds plugins for multiple tools. Not a feature matrix. Real-world strengths and weaknesses.

### Writing Cadence

**Target: 2 posts/month minimum.**

One post can be a project page (lower effort, high value for portfolio).
One post should be an opinion/insight piece (builds the thought leadership angle).

---

## 4. Content to Phase Out

Don't delete existing posts. But stop writing new posts about:
- Blockchain internals (parallel transaction execution, etc.)
- Python language features (multiple inheritance)
- Technical interview advice
- General serverless/Kubernetes topics

**Exception:** Any of these topics reframed through the agentic programming lens is fine. "Using AI agents to modernize a Kubernetes deployment" would work.

---

## 5. Distribution Strategy

### Twitter/X (daily)
- Share blog post key insights as threads
- Engage with AI agent tooling builders (LangChain, CrewAI, Anthropic, OpenAI communities)
- Share agentic.tm meetup highlights
- Hot takes on AI coding tool news

### agentic.tm (weekly-ish)
- Every meetup generates at least one blog post or Twitter thread
- Record talks and post them (YouTube or blog embeds)
- Start a newsletter for the community (monthly minimum)

### Cross-promotion
- claudebin embeds in blog posts (already doing this with vibe-infer, great pattern)
- Project pages link to each other where relevant
- Blog posts reference your tools when naturally relevant (not forced)

---

## 6. Technical Improvements

### Projects Index Page
Currently `content/project/_index.md` exists but is minimal. Consider whether the default Hugo list template is sufficient or if a custom `layouts/project/list.html` would better showcase the portfolio. The homepage feed already shows projects with badges, so this may not be urgent.

### SEO
- Update meta descriptions to reflect the agentic programming focus
- Add OpenGraph images for project pages (screenshots/demos)
- The `llms.txt` and `llms-full.txt` output formats are great, keep them

### Resume/CV
- Update `/resume.pdf` to reflect the agentic programming narrative
- Link to project pages and community work

---

## 7. Metrics (How to Know It's Working)

After 3 months:
- [ ] 4+ project pages live
- [ ] 6+ focused blog posts published
- [ ] Blog traffic trend (check analytics if available)
- [ ] Twitter follower growth in AI/dev tooling community
- [ ] At least one post shared outside your immediate network

After 6 months:
- [ ] Someone you don't know references your blog or projects
- [ ] Invited to speak or guest on a podcast about agentic programming
- [ ] agentic.tm has an online presence beyond local meetups

---

## Execution Order

1. **Update site identity** (config.toml description + homepage bio) - 30 min
2. **Add micode project page** - 1-2 hours
3. **Add octto project page** - 1-2 hours
4. **Add claudebin project page** - 1 hour
5. **Write the manifesto post** ("Why I'm betting on agentic programming") - half a day
6. **Write the meetup insights post** - half a day
7. **Add opencode-reskin project page** - 1 hour
8. **Continue with editorial calendar...**
