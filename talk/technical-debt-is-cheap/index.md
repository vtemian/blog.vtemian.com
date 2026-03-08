---
title: "Technical Debt is Cheap"
date: 2025-10-27
author: Vlad Temian
url: https://blog.vtemian.com/talk/technical-debt-is-cheap/
description: "Can AI tools tackle a 2,000-line legacy Laravel controller in 3 hours? A case study in AI-driven refactoring and modernizing technical debt."
tags: [ai, productivity, refactoring, laravel, case-study]
---

# Technical Debt is Cheap


March 17th, 2025. My regular work was done for the day. I had three hours before I needed to stop.

A friend had recommended Claude Code a few days earlier. "Think of it like having a really junior developer on your team." I was skeptical. I'd used Copilot for autocomplete, played with ChatGPT. Wasn't sold on Cursor.

But I had this project. The one everyone has. Making money for years, users depend on it, and every time someone opens the codebase they quietly close their laptop and find something else to do.

So I pointed Claude Code at it. Not because I had to. Not because anyone asked. Just to see if the hype was real.

## The Codebase: A Shared Trauma

The project was a classic legacy Laravel app—the kind that makes money, has real users, and keeps you awake at night. Controllers weren't controllers; they were **2,000-line novels**. 

- **Naming Chaos:** Files literally named `HomeController-2.php` and `HomeController - Copie.php`.
- **Linguistic Debt:** Variables in Romanian (`$prenume_utilizator`), comments in English, and error messages in... who knows.
- **Frontend Hell:** jQuery nested so deep it felt like a fractal. HTML strings embedded directly in PHP. One missing tag and the entire world explodes.

No validation. No tests. Deployed via FTP. I'm not shaming this codebase—it was actually adding real value. But the interest on this technical debt was compounding every month.

## The Three-Hour Transformation

I set a timer. Paid $20 for API tokens. No designer, no DevOps team. Just me and an agentic tool.

### 1. **Infrastructure: From FTP to Docker**
Something that usually takes a full afternoon was done before I finished my first coffee. Dockerfiles, `docker-compose.yml`, and environment variable mapping appeared in minutes. We moved from "raw files on a server" to a modern, containerized local dev environment.

### 2. **Refactoring: Decomposing the Monolith**
That 2,000-line controller? Claude analyzed the business logic, identified the boundaries, and split it into focused controllers and extracted service classes. It was like watching a sculptor carve a statue out of a block of marble. It translated the Romanian variables, added type hints, and generated clean doc blocks.

### 3. **The Economics: Refactoring as a Commodity**
This is the real takeaway: **AI has changed the interest rate on technical debt.** 

If the cost to fix a legacy app drops from "three weeks for a team" to "three hours for one person," then technical debt is no longer a scary liability—it's an asset you haven't processed yet. We can now afford to modernization projects that were previously too expensive to justify.

...

## The "Human-in-the-Loop" Catch

You still need to know what you're doing.

AI tools amplify what you already know. They take the grunt work—the tedious refactoring, the boilerplate, the repetitive transformations—and compress hours into minutes. But Claude didn't replace my judgment. I made every architectural decision. I validated every change. 

Without senior Laravel or Docker experience, you'll just get plausible-looking garbage. But with it? You're a force multiplier of one.

---

You have a project gathering dust. You know the one. Too scary to touch, too expensive to rewrite.

Pick it. Set a three-hour timer. See what happens.

Stay curious ☕

