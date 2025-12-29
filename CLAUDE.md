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
  - Enables robots.txt and sitemap generation

## Adding New Blog Posts

Create a new Markdown file in `content/post/` with YAML frontmatter. Hugo will automatically include it in the blog index when the dev server is running.

## Deployment

The production build command (`hugo --gc --minify`) generates a static site in the `public/` directory ready for deployment to any static hosting service.

GitHub Actions automatically builds and deploys on push to the `content` branch.
