# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal blog built with Hugo (static site generator) and uses Parcel for asset bundling. Content is written in Markdown and styled with custom CSS.

## Development Commands

**Start development server:**
```bash
yarn dev
```
This runs both Hugo's development server (`dev:hugo`) and Parcel's watch mode (`dev:parcel`) concurrently. Hugo serves on http://localhost:1313 with live reload.

**Build for production:**
```bash
yarn build
```
This runs Parcel bundling followed by Hugo's production build with minification.

**Clean build artifacts:**
```bash
yarn clean
```
Removes `public/`, `assets/output/`, `static/output/`, and `resources/` directories.

**Test Parcel bundling:**
```bash
yarn test
```
Builds main.css to test Parcel configuration without running Hugo.

## Architecture

### Asset Pipeline (Hugo + Parcel)

The project uses a two-stage build process:

1. **Parcel** bundles assets from `assets/` → `assets/output/`
2. **Hugo** consumes bundled assets and generates the final site in `public/`

Assets entry point: `assets/index.js` imports:
- `stylesheets/main.css` (CSS entry point)
- Images (avatar, social icons)

Parcel is configured (`parcel-namer-hashless`) to output files without content hashes for stable Hugo references.

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

### Static Assets

After Parcel bundling, assets are referenced by Hugo templates via the bundled files in `assets/output/`.

## Adding New Blog Posts

Create a new Markdown file in `content/post/` with YAML frontmatter. Hugo will automatically include it in the blog index when the dev server is running.

## Deployment

The production build command (`yarn build`) generates a static site in the `public/` directory ready for deployment to any static hosting service.
