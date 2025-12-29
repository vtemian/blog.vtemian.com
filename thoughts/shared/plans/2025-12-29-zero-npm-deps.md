# Zero npm Dependencies Implementation Plan

**Goal:** Remove all npm dependencies from the Hugo blog - just Hugo, no Node.js tooling.

**Architecture:** Flatten all nested CSS to standard CSS, inline all CSS partials into a single main.css file, and remove Hugo's postCSS pipe. Hugo will process plain CSS directly with fingerprinting in production.

**Design:** Based on requirements from Vlad - no separate design document.

---

## Task 1: Flatten _base.css Nested CSS

**Files:**
- Modify: `assets/stylesheets/_globals/_base.css`

**Step 1: Read current file to understand nesting**

The file has one nested block at lines 14-19:
```css
a {
  ...
  &:hover {
    color: var(--white);
    background: var(--pink);
    border-bottom-color: var(--pink);
  }
}
```

**Step 2: Replace with flattened CSS**

Replace the entire `assets/stylesheets/_globals/_base.css` with:

```css
body {
  background: var(--white);
  color: var(--black);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-base);
  font-weight: 550;
  line-height: 1.3;
}

a {
  color: var(--black);
  text-decoration: none;
  border-bottom: 1px solid var(--blue);
}

a:hover {
  color: var(--white);
  background: var(--pink);
  border-bottom-color: var(--pink);
}

.container {
  width: 100%;
  padding: 20px;
  margin: 0 auto;
  box-sizing: border-box;
  max-width: var(--container-width);
}

code {
  font-family: var(--font-family-mono);
  font-size: var(--font-size-small);
  background: var(--grey-lighter);
  padding: 2px 4px;
}
```

**Step 3: Verify syntax**

Run: `hugo --gc --minify 2>&1 | head -20`
Expected: No CSS parsing errors (may fail on other files, that's OK for now)

---

## Task 2: Flatten _author.css Nested CSS

**Files:**
- Modify: `assets/stylesheets/_components/_author.css`

**Step 1: Analyze nesting structure**

Current nesting:
- `.author { p { } }` -> `.author p { }`
- `.author { h1 { } }` -> `.author h1 { }`
- `.author { img { } }` -> `.author img { }`
- `.author { &--is-small { } }` -> `.author--is-small { }`
- `.author--is-small { img { } }` -> `.author--is-small img { }`
- `.about { p { } }` -> `.about p { }`
- `.about { strong { } }` -> `.about strong { }`

**Step 2: Replace with flattened CSS**

Replace the entire `assets/stylesheets/_components/_author.css` with:

```css
.author {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  flex-direction: column;
  border-bottom: 3px dotted var(--black);
}

.author p {
  color: var(--grey);
  font-size: var(--font-size-small);
}

.author h1 {
  font-weight: 700;
  margin: 15px 0 10px;
  font-size: var(--font-size-large);
}

.author img {
  width: 100px;
  height: 100px;
  border-radius: 100px;
}

.author--is-small {
  margin-bottom: 0px;
  padding-bottom: 0px;
  flex-direction: row;
  border-bottom: none;
}

.author--is-small img {
  width: 50px;
  height: 50px;
  margin-right: 15px;
}

.about {
  margin-top: 25px;
  margin-bottom: 10px;
  padding: 0;
  font-size: var(--font-size-medium);
  line-height: 1.7;
  text-align: left;
}

.about p {
  color: var(--black);
}

.about strong {
  font-weight: 700;
}
```

**Step 3: Verify syntax**

Run: `hugo --gc --minify 2>&1 | head -20`
Expected: No CSS parsing errors for this file

---

## Task 3: Flatten _articles.css Nested CSS

**Files:**
- Modify: `assets/stylesheets/_components/_articles.css`

**Step 1: Analyze nesting structure**

Current deep nesting:
- `.articles { article { } }` -> `.articles article { }`
- `.articles article { &:last-child { } }` -> `.articles article:last-child { }`
- `.articles article { h2 { } }` -> `.articles article h2 { }`
- `.articles article { a { } }` -> `.articles article a { }`
- `.articles article a { &:hover { } }` -> `.articles article a:hover { }`
- `.articles article a:hover { time { } }` -> `.articles article a:hover time { }`
- `.articles article { time { } }` -> `.articles article time { }`

**Step 2: Replace with flattened CSS**

Replace the entire `assets/stylesheets/_components/_articles.css` with:

```css
.articles {
  margin: 0;
}

.articles article {
  display: flex;
  margin-bottom: 0;
  padding-bottom: 8px;
  justify-items: center;
  border-bottom: 3px dotted var(--grey-lighter);
}

.articles article:last-child {
  border-bottom: none;
}

.articles article h2 {
  font-weight: 700;
  font-size: var(--font-size-medium);
  line-height: 1.3;
}

.articles article a {
  flex: 1;
  display: flex;
  align-items: center;
  color: var(--black);
  justify-content: space-between;
  border-bottom: none;
}

.articles article a:hover {
  color: var(--white);
  background: var(--pink);
}

.articles article a:hover time {
  color: var(--white);
}

.articles article time {
  color: var(--grey);
}
```

**Step 3: Verify syntax**

Run: `hugo --gc --minify 2>&1 | head -20`
Expected: No CSS parsing errors for this file

---

## Task 4: Flatten _article.css Nested CSS

**Files:**
- Modify: `assets/stylesheets/_components/_article.css`

**Step 1: Analyze nesting structure**

Current nesting:
- `.article { header { } }` -> `.article header { }`
- `.article header { h1 { } }` -> `.article header h1 { }`
- `.article header { p { } }` -> `.article header p { }`
- `.article header { img { } }` -> `.article header img { }`
- `.article { h1 { } }` -> `.article h1 { }`
- `.article { h2 { } }` -> `.article h2 { }`
- `.article { h3 { } }` -> `.article h3 { }`
- `.article { p, hr, img, blockquote, pre { } }` -> `.article p, .article hr, ...`
- `.article { ul { } }` -> `.article ul { }`
- `.article { li { } }` -> `.article li { }`
- `.article { hr { } }` -> `.article hr { }`
- `.article { img { } }` -> `.article img { }`
- `.article { strong { } }` -> `.article strong { }`
- `.article { blockquote { } }` -> `.article blockquote { }`
- `.article { li:not(:last-of-type) a:only-child { } }` -> `.article li:not(:last-of-type) a:only-child { }`

**Step 2: Replace with flattened CSS**

Replace the entire `assets/stylesheets/_components/_article.css` with:

```css
.article {
  line-height: 1.3;
}

.article header {
  margin-bottom: 35px;
}

.article header h1 {
  margin-bottom: 10px;
}

.article header p {
  margin-bottom: 0px;
}

.article header img {
  margin-bottom: 0px;
}

.article h1 {
  font-weight: 700;
  margin-bottom: 0px;
  font-size: var(--font-size-large);
}

.article h2 {
  font-weight: 700;
  font-size: var(--font-size-medium);
  margin-bottom: 15px;
  margin-top: 30px;
}

.article h3 {
  font-weight: 700;
  font-size: var(--font-size-medium);
  margin-bottom: 15px;
  margin-top: 25px;
}

.article p,
.article hr,
.article img,
.article blockquote,
.article pre {
  margin-bottom: 15px;
}

.article ul {
  list-style: circle;
  padding-left: 50px;
  margin-bottom: 10px;
}

.article li {
  margin-bottom: 10px;
}

.article hr {
  height: 1px;
  border: none;
  background: var(--grey-lighter);
}

.article img {
  height: auto;
  max-width: 100%;
}

.article strong {
  font-weight: 600;
}

.article blockquote {
  margin-left: -25px;
  padding-left: 25px;
  font-style: italic;
  font-size: var(--font-size-medium);
  border-left: 5px solid var(--black);
}

.article li:not(:last-of-type) a:only-child {
  margin-bottom: -10px;
  display: block;
}
```

**Step 3: Verify syntax**

Run: `hugo --gc --minify 2>&1 | head -20`
Expected: No CSS parsing errors for this file

---

## Task 5: Flatten _social.css Nested CSS

**Files:**
- Modify: `assets/stylesheets/_components/_social.css`

**Step 1: Analyze nesting structure**

Current nesting:
- `.social { a { } }` -> `.social a { }`
- `.social a { &.resume { } }` -> `.social a.resume { }`
- `.social { img { } }` -> `.social img { }`

**Step 2: Replace with flattened CSS**

Replace the entire `assets/stylesheets/_components/_social.css` with:

```css
.social {
  display: flex;
  flex-flow: row;
}

.social a {
  margin-left: 5px;
}

.social a.resume {
  margin-left: 10px;
  margin-top: 2px;
  font-weight: 600;
  font-size: 1.2rem;
}

.social img {
  width: 20px;
  height: 20px;
}
```

**Step 3: Verify syntax**

Run: `hugo --gc --minify 2>&1 | head -20`
Expected: No CSS parsing errors for this file

---

## Task 6: Verify All CSS Files Are Flat

**Files:**
- Verify: All CSS files in `assets/stylesheets/`

**Step 1: Check for remaining nested syntax**

Run: `grep -r '&' assets/stylesheets/`
Expected: No output (no `&` selectors remaining)

Run: `grep -rE '^\s+[a-z]+\s*\{' assets/stylesheets/`
Expected: No output (no nested element selectors)

**Step 2: Commit flattened CSS**

```bash
git add assets/stylesheets/
git commit -m "refactor(css): flatten all nested CSS to standard syntax

Removes postcss-nested dependency by converting:
- & selectors to explicit parent selectors
- Nested element blocks to descendant selectors

Prepares for removal of all npm dependencies."
```

---

## Task 7: Inline All CSS Into main.css

**Files:**
- Modify: `assets/stylesheets/main.css`
- Delete: All files in `assets/stylesheets/_globals/` and `assets/stylesheets/_components/`

**Step 1: Create consolidated main.css**

Replace `assets/stylesheets/main.css` with all CSS inlined (order matters):

```css
/* ==========================================================================
   Variables
   ========================================================================== */

:root {
  --white: #ffffff;
  --black: #232333;
  --grey: #a5a5a5;
  --grey-lighter: #f2f2f2;
  --blue: #5694f1;
  --pink: #eb298c;

  --font-family-mono: "Roboto Mono", "Courier New", monospace;

  --font-size-base: 0.9em;
  --font-size-small: 0.85em;
  --font-size-medium: 1em;
  --font-size-large: 1.5em;

  --container-width: 720px;
}

/* ==========================================================================
   Reset
   ========================================================================== */

*, *::before, *::after {
  box-sizing: border-box;
}

* {
  margin: 0;
  padding: 0;
}

html {
  -webkit-text-size-adjust: 100%;
}

body {
  min-height: 100vh;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

img, picture, video, canvas, svg {
  display: block;
  max-width: 100%;
}

input, button, textarea, select {
  font: inherit;
}

p, h1, h2, h3, h4, h5, h6 {
  overflow-wrap: break-word;
}

a {
  text-decoration-skip-ink: auto;
}

ol, ul {
  list-style: none;
}

/* ==========================================================================
   Base
   ========================================================================== */

body {
  background: var(--white);
  color: var(--black);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-base);
  font-weight: 550;
  line-height: 1.3;
}

a {
  color: var(--black);
  text-decoration: none;
  border-bottom: 1px solid var(--blue);
}

a:hover {
  color: var(--white);
  background: var(--pink);
  border-bottom-color: var(--pink);
}

.container {
  width: 100%;
  padding: 20px;
  margin: 0 auto;
  box-sizing: border-box;
  max-width: var(--container-width);
}

code {
  font-family: var(--font-family-mono);
  font-size: var(--font-size-small);
  background: var(--grey-lighter);
  padding: 2px 4px;
}

/* ==========================================================================
   Author
   ========================================================================== */

.author {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  flex-direction: column;
  border-bottom: 3px dotted var(--black);
}

.author p {
  color: var(--grey);
  font-size: var(--font-size-small);
}

.author h1 {
  font-weight: 700;
  margin: 15px 0 10px;
  font-size: var(--font-size-large);
}

.author img {
  width: 100px;
  height: 100px;
  border-radius: 100px;
}

.author--is-small {
  margin-bottom: 0px;
  padding-bottom: 0px;
  flex-direction: row;
  border-bottom: none;
}

.author--is-small img {
  width: 50px;
  height: 50px;
  margin-right: 15px;
}

.about {
  margin-top: 25px;
  margin-bottom: 10px;
  padding: 0;
  font-size: var(--font-size-medium);
  line-height: 1.7;
  text-align: left;
}

.about p {
  color: var(--black);
}

.about strong {
  font-weight: 700;
}

/* ==========================================================================
   Articles (list)
   ========================================================================== */

.articles {
  margin: 0;
}

.articles article {
  display: flex;
  margin-bottom: 0;
  padding-bottom: 8px;
  justify-items: center;
  border-bottom: 3px dotted var(--grey-lighter);
}

.articles article:last-child {
  border-bottom: none;
}

.articles article h2 {
  font-weight: 700;
  font-size: var(--font-size-medium);
  line-height: 1.3;
}

.articles article a {
  flex: 1;
  display: flex;
  align-items: center;
  color: var(--black);
  justify-content: space-between;
  border-bottom: none;
}

.articles article a:hover {
  color: var(--white);
  background: var(--pink);
}

.articles article a:hover time {
  color: var(--white);
}

.articles article time {
  color: var(--grey);
}

/* ==========================================================================
   Article (single)
   ========================================================================== */

.article {
  line-height: 1.3;
}

.article header {
  margin-bottom: 35px;
}

.article header h1 {
  margin-bottom: 10px;
}

.article header p {
  margin-bottom: 0px;
}

.article header img {
  margin-bottom: 0px;
}

.article h1 {
  font-weight: 700;
  margin-bottom: 0px;
  font-size: var(--font-size-large);
}

.article h2 {
  font-weight: 700;
  font-size: var(--font-size-medium);
  margin-bottom: 15px;
  margin-top: 30px;
}

.article h3 {
  font-weight: 700;
  font-size: var(--font-size-medium);
  margin-bottom: 15px;
  margin-top: 25px;
}

.article p,
.article hr,
.article img,
.article blockquote,
.article pre {
  margin-bottom: 15px;
}

.article ul {
  list-style: circle;
  padding-left: 50px;
  margin-bottom: 10px;
}

.article li {
  margin-bottom: 10px;
}

.article hr {
  height: 1px;
  border: none;
  background: var(--grey-lighter);
}

.article img {
  height: auto;
  max-width: 100%;
}

.article strong {
  font-weight: 600;
}

.article blockquote {
  margin-left: -25px;
  padding-left: 25px;
  font-style: italic;
  font-size: var(--font-size-medium);
  border-left: 5px solid var(--black);
}

.article li:not(:last-of-type) a:only-child {
  margin-bottom: -10px;
  display: block;
}

/* ==========================================================================
   Social
   ========================================================================== */

.social {
  display: flex;
  flex-flow: row;
}

.social a {
  margin-left: 5px;
}

.social a.resume {
  margin-left: 10px;
  margin-top: 2px;
  font-weight: 600;
  font-size: 1.2rem;
}

.social img {
  width: 20px;
  height: 20px;
}

/* ==========================================================================
   Footer
   ========================================================================== */

.footer {
  padding-top: 40px;
  border-top: 3px dotted var(--black);
  color: var(--grey);
  font-size: var(--font-size-small);
}

/* ==========================================================================
   Table
   ========================================================================== */

table {
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 25px;
}

th,
td {
  border: 1px solid var(--grey-lighter);
  padding: 0.6rem;
  text-align: left;
}

th {
  font-weight: 700;
  background: var(--grey-lighter);
}
```

**Step 2: Delete partial CSS files**

```bash
rm -rf assets/stylesheets/_globals/
rm -rf assets/stylesheets/_components/
```

**Step 3: Verify file structure**

Run: `ls -la assets/stylesheets/`
Expected: Only `main.css` remains

---

## Task 8: Update stylesheets.html to Remove PostCSS

**Files:**
- Modify: `layouts/partials/stylesheets.html`

**Step 1: Replace PostCSS pipeline with plain CSS**

Replace the entire `layouts/partials/stylesheets.html` with:

```html
{{ $css := resources.Get "stylesheets/main.css" }}
{{ if hugo.IsProduction }}
  {{ $css = $css | minify | fingerprint }}
{{ end }}
<link rel="stylesheet" href="{{ $css.RelPermalink }}" media="screen">
```

**Step 2: Verify Hugo builds successfully**

Run: `hugo --gc --minify`
Expected: Build completes without errors

**Step 3: Verify CSS is served correctly**

Run: `hugo server -D &; sleep 3; curl -s http://localhost:1313/ | grep -o 'href="[^"]*\.css[^"]*"' | head -1; kill %1`
Expected: Shows CSS link with fingerprint hash in production mode

---

## Task 9: Remove npm Configuration Files

**Files:**
- Delete: `package.json`
- Delete: `yarn.lock`
- Delete: `.yarn/`
- Delete: `.postcssrc`
- Delete: `.yarnrc.yml`

**Step 1: Remove all npm-related files**

```bash
rm package.json
rm yarn.lock
rm -rf .yarn/
rm .postcssrc
rm .yarnrc.yml
```

**Step 2: Verify files are removed**

Run: `ls -la | grep -E 'package|yarn|postcss'`
Expected: No output (files are gone)

**Step 3: Verify Hugo still builds**

Run: `hugo --gc --minify`
Expected: Build completes successfully

---

## Task 10: Update .gitignore

**Files:**
- Modify: `.gitignore`

**Step 1: Remove node_modules reference, keep other ignores**

Replace the entire `.gitignore` with:

```
.DS_Store
.idea/

public/
.hugo_build.lock
```

**Step 2: Verify .gitignore is correct**

Run: `cat .gitignore`
Expected: Shows updated content without node_modules

---

## Task 11: Update GitHub Actions Workflow

**Files:**
- Modify: `.github/workflows/publish.yml`

**Step 1: Remove Node.js setup and yarn commands**

Replace the entire `.github/workflows/publish.yml` with:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - content

jobs:
  build-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout the code
      uses: actions/checkout@v4

    - name: Setup Hugo
      uses: peaceiris/actions-hugo@v3
      with:
        hugo-version: '0.136.2'

    - name: Build
      run: hugo --gc --minify

    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v4
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./public
        publish_branch: master
        cname: blog.vtemian.com
```

**Step 2: Verify YAML syntax**

Run: `cat .github/workflows/publish.yml | head -20`
Expected: Shows valid YAML without Node.js steps

---

## Task 12: Update CLAUDE.md Documentation

**Files:**
- Modify: `CLAUDE.md`

**Step 1: Replace with updated documentation**

Replace the entire `CLAUDE.md` with:

```markdown
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
```

**Step 2: Verify documentation is updated**

Run: `head -30 CLAUDE.md`
Expected: Shows updated content without yarn/npm references

---

## Task 13: Update ARCHITECTURE.md Documentation

**Files:**
- Modify: `ARCHITECTURE.md`

**Step 1: Replace with updated documentation**

Replace the entire `ARCHITECTURE.md` with:

```markdown
# Architecture

## Overview

Personal blog for Vlad Temian built with Hugo (static site generator). The site is deployed to GitHub Pages via GitHub Actions.

## Tech Stack

| Category | Technology |
|----------|------------|
| Static Site Generator | Hugo 0.136.2 |
| CSS Processing | Hugo Pipes (minify, fingerprint) |
| Syntax Highlighting | highlight.js (CDN) |
| Fonts | Google Fonts (Roboto Mono) |
| Hosting | GitHub Pages |
| CI/CD | GitHub Actions |

## Directory Structure

```
blog.vtemian.com/
├── assets/                    # Source assets (processed by Hugo)
│   ├── images/               # Source images (avatar, social icons)
│   └── stylesheets/          # CSS source
│       └── main.css          # All styles in one file
├── content/                   # Blog content (Markdown)
│   └── post/                 # Blog posts
│       └── {post-name}/      # Post with images (page bundle)
│       └── {post-name}.md    # Simple post (no images)
├── layouts/                   # Hugo templates
│   ├── _default/             # Base templates
│   │   ├── baseof.html       # Root template
│   │   ├── list.html         # Blog index page
│   │   └── single.html       # Individual post page
│   └── partials/             # Reusable template fragments
├── static/                    # Static files (copied as-is)
├── public/                    # Hugo output (generated site)
├── .github/workflows/         # CI/CD configuration
└── config.toml               # Hugo configuration
```

## Build Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                        BUILD PIPELINE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Hugo Build                                                     │
│  ┌─────────────────┐      ┌─────────────────┐                  │
│  │ content/        │      │                 │                  │
│  │ layouts/        │ ──▶  │    public/      │                  │
│  │ assets/         │      │                 │                  │
│  │ static/         │      └─────────────────┘                  │
│  └─────────────────┘                                           │
│                                                                 │
│  Hugo Pipes processes CSS:                                      │
│  - Minification (production)                                    │
│  - Fingerprinting (cache busting)                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Configuration

- **Hugo** uses YAML frontmatter format (`metaDataFormat = "yaml"`)
- **CSS** is plain CSS with CSS custom properties (no preprocessor)

## Core Components

### Templates

| Template | Purpose |
|----------|---------|
| `baseof.html` | Root HTML structure, includes header partial |
| `list.html` | Homepage with author info and article list |
| `single.html` | Individual blog post layout |

### Partials

| Partial | Purpose |
|---------|---------|
| `header.html` | Meta tags, fonts, highlight.js, SEO schema |
| `footer.html` | Copyright, highlight.js init |
| `seo_schema.html` | OpenGraph and JSON-LD structured data |
| `stylesheets.html` | CSS link tag |
| `get-page-images.html` | Extract images for OG tags |

### CSS Architecture

All CSS is in `assets/stylesheets/main.css`, organized into sections:

```
main.css
├── Variables        # CSS custom properties
├── Reset           # Modern CSS reset
├── Base            # Body, links, container, code
├── Author          # Author sidebar component
├── Articles        # Article list component
├── Article         # Single article component
├── Social          # Social links component
├── Footer          # Footer component
└── Table           # Table styles
```

## Data Flow

### Page Request Flow

```
1. User requests URL
2. GitHub Pages serves static HTML from public/
3. Browser loads:
   - HTML (Hugo-generated)
   - CSS (Hugo-processed, fingerprinted)
   - JS (highlight.js from CDN)
   - Fonts (Google Fonts CDN)
```

### Content Flow

```
1. Author writes Markdown in content/post/
2. Hugo processes Markdown with templates
3. Hugo Pipes processes CSS (minify, fingerprint)
4. Hugo outputs complete HTML to public/
```

## External Integrations

| Service | Purpose |
|---------|---------|
| GitHub Pages | Static hosting |
| Google Fonts | Typography (Roboto Mono) |
| Cloudflare CDN | highlight.js for syntax highlighting |
| Google Search Console | Site verification |

## Configuration

### Hugo (`config.toml`)

- `baseURL`: https://blog.vtemian.com/
- `enableRobotsTXT`: true
- `canonifyURLs`: true
- `metaDataFormat`: yaml

### Environment Variables

None required. All configuration is file-based.

## Build & Deploy

### Development

```bash
hugo server -D    # Start dev server with drafts
                  # Serves at http://localhost:1313
```

### Production Build

```bash
hugo --gc --minify    # Build for production
                      # Output: public/
```

### Deployment

Automatic via GitHub Actions on push to `content` branch:
1. Checkout code
2. Setup Hugo 0.136.2
3. Build (`hugo --gc --minify`)
4. Deploy `public/` to `master` branch
5. GitHub Pages serves from `master`

### Clean

```bash
rm -rf public resources    # Remove generated directories
```
```

**Step 2: Verify documentation is updated**

Run: `head -40 ARCHITECTURE.md`
Expected: Shows updated content without Parcel/npm references

---

## Task 14: Commit All Changes

**Step 1: Stage all changes**

```bash
git add -A
```

**Step 2: Review staged changes**

Run: `git status`
Expected: Shows deleted npm files, modified CSS, modified docs

**Step 3: Commit**

```bash
git commit -m "refactor: remove all npm dependencies

- Flatten nested CSS to standard CSS syntax
- Inline all CSS partials into single main.css
- Remove PostCSS pipeline from Hugo
- Delete package.json, yarn.lock, .yarn/, .postcssrc, .yarnrc.yml
- Update GitHub Actions to use Hugo only
- Update CLAUDE.md and ARCHITECTURE.md documentation

The blog now requires only Hugo to build - no Node.js tooling."
```

---

## Task 15: Final Verification

**Step 1: Clean and rebuild**

```bash
rm -rf public resources
hugo --gc --minify
```

Expected: Build completes successfully

**Step 2: Start dev server and verify visually**

```bash
hugo server -D
```

Expected: Site loads at http://localhost:1313 with correct styling

**Step 3: Verify no npm files remain**

Run: `ls -la | grep -E 'package|yarn|node|postcss'`
Expected: No output

Run: `find . -name "node_modules" -type d`
Expected: No output

**Step 4: Verify CSS is being served**

Run: `curl -s http://localhost:1313/ | grep -o 'href="/stylesheets/[^"]*"'`
Expected: Shows CSS path like `href="/stylesheets/main.css"`

---

## Summary

| Task | Description | Files Changed |
|------|-------------|---------------|
| 1 | Flatten _base.css | 1 modified |
| 2 | Flatten _author.css | 1 modified |
| 3 | Flatten _articles.css | 1 modified |
| 4 | Flatten _article.css | 1 modified |
| 5 | Flatten _social.css | 1 modified |
| 6 | Verify & commit CSS | 0 (commit only) |
| 7 | Inline CSS into main.css | 1 modified, 9 deleted |
| 8 | Update stylesheets.html | 1 modified |
| 9 | Remove npm files | 5 deleted |
| 10 | Update .gitignore | 1 modified |
| 11 | Update GitHub Actions | 1 modified |
| 12 | Update CLAUDE.md | 1 modified |
| 13 | Update ARCHITECTURE.md | 1 modified |
| 14 | Final commit | 0 (commit only) |
| 15 | Final verification | 0 (verify only) |

**Total: 5 files modified, 14 files deleted, 0 files created**
