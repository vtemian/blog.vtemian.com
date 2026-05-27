# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal blog built with Hugo (static site generator). Content is written in Markdown and styled with plain CSS processed through Hugo Pipes.

## Development Commands

**Start development server:**
```bash
hugo server -D
```
Hugo serves on http://localhost:1313 with live reload and draft posts enabled.

**Build for production:**
```bash
hugo --gc --minify
```
Hugo's production build with garbage collection and minification.

**Clean build artifacts:**
```bash
rm -rf public resources
```
Removes generated directories.

## Architecture

### Asset Pipeline (Hugo Pipes)

The project uses Hugo's native asset pipeline:

1. **Hugo Pipes** loads CSS from `assets/stylesheets/main.css`
2. **Hugo** minifies and fingerprints assets for cache busting in production
3. Final static site generated in `public/`

Assets are stored in `assets/`:
- `stylesheets/main.css` - All CSS in one file (plain CSS, no preprocessor)
- `images/` - Avatar and social icons

No external dependencies required - just Hugo.

### CSS Architecture

All CSS is in `assets/stylesheets/main.css`, organized into sections:
- Variables (CSS custom properties)
- Reset (modern CSS reset)
- Base (body, links, container, code)
- Components (author, articles, article, social, footer, table)

Uses plain CSS with CSS custom properties for theming.

### Hugo Structure

**Templates:**
- `layouts/_default/baseof.html` - Base template
- `layouts/_default/list.html` - List pages (blog index)
- `layouts/_default/single.html` - Single post pages
- `layouts/partials/` - Reusable template components (header, footer, SEO schema, etc.)

**Content:**
- `content/post/` - Blog posts in Markdown format
- Each post has YAML frontmatter (metaDataFormat = "yaml" in config.toml)

**Configuration:**
- `config.toml` - Hugo site configuration
  - Site URL: https://blog.vtemian.com/
  - Author: Vlad Temian
  - Social handles: `params.twitter`, `params.linkedin`, `params.github`, `params.email`
  - `params.avatar` (absolute URL) is used as the Person.image in JSON-LD
  - Enables robots.txt and sitemap generation

### SEO, Open Graph, and Structured Data

All page-level SEO lives in `layouts/partials/seo_schema.html` and emits:

1. Standard `<meta>` (charset, robots, canonical, keywords, description, author).
2. Open Graph + Twitter Card tags. The OG image URL is cache-busted with
   `?v={{ .Lastmod.Unix }}` so social platforms only refetch when the page
   actually changes (not on every build).
3. A site-wide JSON-LD `@graph` on every page containing a `Person`
   (`{baseURL}#person`), `WebSite` (`{baseURL}#website`), and `Blog`
   (`{baseURL}#blog`) node. Page-level entities reference these via `@id`.
4. A page-specific JSON-LD block, chosen by page type:
   - Home → `ProfilePage` with `mainEntity` = Person
   - `content/post/<slug>` → `BlogPosting` (part of Blog)
   - `content/talk/<slug>` → `Article` (+ `Event` if `event:` is in front matter)
   - `content/project/<slug>` → `CreativeWork`
   - Section / taxonomy list pages → `CollectionPage`
5. A `BreadcrumbList` adapted to whether the page is home, a section list,
   or a single page.

Sitemap is generated from `layouts/sitemap.xml` with per-section priorities
(home 1.0, sections 0.9, posts 0.8, talks/projects 0.7, taxonomy 0.4).
Robots rules live in `layouts/robots.txt` and reference the sitemap, `llms.txt`,
and `llms-full.txt`.

When adding a new content section, update both `seo_schema.html` (page-specific
JSON-LD branch) and `sitemap.xml` (priority) so the new section is treated
correctly.

## Writing Style

When writing or editing blog content:
- Never use em dashes (—). Use periods, commas, or restructure the sentence instead.
- Sign-off is "Stay curious ☕" (not "Cheers 🍺")

## Adding New Blog Posts

Create a new Markdown file in `content/post/` with YAML frontmatter. Hugo will automatically include it in the blog index when the dev server is running.

## Deployment

The production build command (`hugo --gc --minify`) generates a static site in the `public/` directory ready for deployment to any static hosting service.

GitHub Actions automatically builds and deploys on push to the `content` branch.
