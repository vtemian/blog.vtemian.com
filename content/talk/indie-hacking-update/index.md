---
title: "Riding Existing Waves: My Indie Hacking Journey with Sisif.ai"
date: 2026-01-22T15:00:00+02:00
description: "How I went from 0 paying customers to growing MRR by abandoning traditional marketing and riding existing distribution waves"
images:
    - revenue-chart.png
event: "Indie TM #2"
event_url: ""
slides: ""
video: ""
keywords:
    - indie hacking
    - sisif.ai
    - ai video generation
    - n8n
    - distribution
    - saas
    - side project
    - marketing
tags:
    - indie-hacking
    - saas
    - ai
    - marketing
---

I sold my company in late 2024. After 15 years of building production code, being CTO at QED (acquired by The Sandbox), and working with companies like Gorgias, I had one clear lesson: **product drives value, not technical implementation**.

So I started a side project. Something I could build and ship fast. Something that solves a real problem.

## The Side Project: Sisif.ai

**[sisif.ai](https://sisif.ai)** is an AI video generation API. Text prompt in, video out. Simple.

![Sisif.ai demo](sisif-scroll.gif)

Most AI video tools are built for clicking around in browsers. But developers want to automate — batch generation, workflow integration, programmatic control. That's the gap I saw.

Three steps: submit a text prompt, receive a webhook when it's done, download your video. Multiple resolutions. Pay per use, no subscription required.

I started building in December 2024 and launched in early 2025. Built it with **SaaS Pegasus**, a Django boilerplate by Cory Zue — who's been building in public since 2017 and runs at a $122/hour effective rate. No AI coding agents for this one. Just good old Django.

## The Marketing Playbook (That Didn't Work)

I did everything the indie hacking playbook says:

- **Twitter/X content** — posted regularly, shared progress
- **ProductHunt launch** — prepared the launch, gathered supporters
- **SEO** — added llms.txt, optimized pages
- **Building in public** — shared the journey

The result?

- **0** paying customers
- **8** followers
- ProductHunt: crickets
- SEO: too early to tell

### Two Months of Twitter: A Reality Check

I committed to **two months of consistent Twitter posting**. Daily updates. Progress screenshots. Building in public threads. Engagement with other indie hackers. The kind of content that supposedly builds audiences.

After 60 days: **8 followers**. Not 8,000. Eight. Most of them were bots or other indie hackers doing the same thing. Zero customers came from Twitter. Zero meaningful conversations. Zero inbound interest.

The accounts that "blow up" on Twitter? They either got lucky with timing, had an existing audience from somewhere else, or have been grinding for years. There's no shortcut. And for a solo founder with a product to ship, spending 2+ hours daily on tweets that reach nobody is a terrible ROI.

### The ProductHunt Launch That Wasn't

I prepared a proper ProductHunt launch. Lined up supporters. Created assets. Picked a launch day. Did everything the guides recommend.

Launch day came. And... nothing. No traction. No upvotes from strangers. The supporters I gathered weren't enough to break through. ProductHunt's algorithm buried the launch before it had a chance.

Here's what I learned: **ProductHunt is a lottery**. The winners are either products with existing audiences (who bring their own traffic) or products that get lucky with the algorithm. For a new product from an unknown founder? The odds are stacked against you.

The harsh reality of indie hacking. Traditional marketing is slow. Twitter takes years to build. ProductHunt is a lottery. SEO needs months to compound.

## The Pivot: Ride Existing Waves

I stopped building from scratch. Instead, I asked: **where are the users already?**

The answer was **n8n** — the workflow automation tool. Thousands of users building automations, looking for integrations. They don't need to find me. I need to be where they already are.

### The n8n Strategy

I published **2 workflow templates** on the n8n creator hub:

1. **TikTok video creation pipeline** — GPT-4o-mini generates the script, Sisif.ai creates the video, posts automatically
2. **Instagram Reels automation** — same stack, different output format

![n8n TikTok workflow](n8n-tiktok-workflow.png)

The results? **15,000 views** on the TikTok template. **4,000 views** on the Instagram one. That's **19,000 eyeballs** on my product — more than I'd get from years of tweeting.

These aren't vanity metrics. n8n users are exactly my target audience: developers and technical founders who want to automate video creation. They're already in a buying mindset — they're looking for tools to plug into their workflows.

The conversion funnel is simple: user discovers template → tries it → needs API access → signs up for Sisif.ai. No cold outreach. No content calendar. No algorithm to game.

### Why This Works

This is **riding existing waves**. Instead of building an audience from zero, you tap into platforms where your users already hang out:

- **n8n** has thousands of users searching for workflow integrations
- **Zapier** and **Make** have similar marketplaces
- **GitHub** templates get discovered organically

SEO? Write for big sites that already rank. Distribution? Let users find you through tools they already use. The math is simple: it's easier to capture 0.1% of 100,000 users than to build 100 users from scratch.

## Pricing Evolution

My first pricing was wrong. **$9/month** single plan. Too cheap, wrong incentives.

I switched to tiered pricing:

- **Alpha Tester**: $10/month (100 tokens)
- **Starter Pack**: $50/month (1,000 tokens)
- **Pro Creator**: $200/month (5,000 tokens)

Higher tiers = higher revenue per customer. The change increased MRR 4x.

![Revenue growth](revenue-chart.png)

## Lessons Learned

After months of building and marketing sisif.ai, here's what stuck:

**Distribution beats product.** Build where users already are. The best product nobody knows about loses to the mediocre product everyone finds.

**Ride existing waves.** n8n, marketplaces, integrations. Don't fight for attention. Go where attention already exists.

**Price for value.** Tiered pricing forces you to think about customer segments. Not everyone needs the same thing. Charge accordingly.

**Traditional marketing is slow.** Twitter/ProductHunt/SEO didn't work yet. Maybe they will. But I needed results now. Existing platforms delivered.

---

Find me at [@vtemian](https://twitter.com/vtemian) or check out [sisif.ai](https://sisif.ai).
