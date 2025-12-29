# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal blog built with Hugo (static site generator). Content is written in Markdown and styled with custom CSS processed through Hugo Pipes.

## Development Commands

**Start development server:**
```bash
yarn dev
```
Hugo serves on http://localhost:1313 with live reload and draft posts enabled.

**Build for production:**
```bash
yarn build
```
Hugo's production build with minification.

**Clean build artifacts:**
```bash
yarn clean
```
Removes `public/` and `resources/` directories.

## Architecture

### Asset Pipeline (Hugo Pipes)

The project uses Hugo's native asset pipeline:

1. **Hugo Pipes** processes CSS through PostCSS (handles nested syntax)
2. **Hugo** fingerprints assets for cache busting in production
3. Final static site generated in `public/`

Assets are stored in `assets/`:
- `stylesheets/main.css` - CSS entry point (uses postcss-nested)
- `images/` - Avatar and social icons

No external bundler required - Hugo handles everything.

### CSS Architecture

Located in `assets/stylesheets/`, the CSS is organized into:

- `_globals/` - Variables, reset, base styles
- `_components/` - Component-specific styles (author, articles, article, social, footer, table)
- `main.css` - Imports all partials in order

Uses PostCSS with `postcss-nested` for nested CSS syntax.

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

The production build command (`yarn build`) generates a static site in the `public/` directory ready for deployment to any static hosting service.
