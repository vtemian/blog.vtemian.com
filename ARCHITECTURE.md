# Architecture

## Overview

Personal blog for Vlad Temian built with Hugo (static site generator) and Parcel (asset bundler). The site is deployed to GitHub Pages via GitHub Actions.

## Tech Stack

| Category | Technology |
|----------|------------|
| Static Site Generator | Hugo 0.136.2 |
| Asset Bundler | Parcel 2.16.1 |
| CSS Processing | PostCSS with postcss-nested |
| Syntax Highlighting | highlight.js (CDN) |
| Fonts | Google Fonts (Karla, Rubik, Inconsolata) |
| Package Manager | Yarn (Berry) |
| Hosting | GitHub Pages |
| CI/CD | GitHub Actions |

## Directory Structure

```
blog.vtemian.com/
├── assets/                    # Source assets (processed by Parcel)
│   ├── images/               # Source images (avatar, social icons)
│   ├── javascript/           # JS source (currently empty main.js)
│   ├── stylesheets/          # CSS source files
│   │   ├── _globals/         # Variables, reset, base styles
│   │   └── _components/      # Component-specific styles
│   ├── output/               # Parcel output (bundled assets)
│   └── index.js              # Parcel entry point
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
├── config.toml               # Hugo configuration
└── package.json              # Node.js dependencies and scripts
```

## Build Pipeline

The project uses a two-stage build process:

```
┌─────────────────────────────────────────────────────────────────┐
│                        BUILD PIPELINE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Stage 1: Parcel                                                │
│  ┌─────────────────┐      ┌─────────────────┐                  │
│  │ assets/index.js │ ──▶  │ assets/output/  │                  │
│  │ - main.css      │      │ - index.css     │                  │
│  │ - images/*.png  │      │ - index.js      │                  │
│  └─────────────────┘      │ - *.png         │                  │
│                           └─────────────────┘                  │
│                                  │                              │
│  Stage 2: Hugo                   ▼                              │
│  ┌─────────────────┐      ┌─────────────────┐                  │
│  │ content/        │      │                 │                  │
│  │ layouts/        │ ──▶  │    public/      │                  │
│  │ assets/output/  │      │                 │                  │
│  │ static/         │      └─────────────────┘                  │
│  └─────────────────┘                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Configuration

- **Parcel** uses `parcel-namer-hashless` to output files without content hashes for stable Hugo references
- **PostCSS** enables nested CSS syntax via `postcss-nested`
- **Hugo** uses YAML frontmatter format (`metaDataFormat = "yaml"`)

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
| `scripts.html` | JS script tag |
| `get-page-images.html` | Extract images for OG tags |

### CSS Architecture

CSS is organized in a modular structure:

```
stylesheets/
├── main.css              # Entry point (imports all)
├── _globals/
│   ├── _variables.css    # CSS custom properties
│   ├── _reset.css        # Meyer reset
│   └── _base.css         # Base element styles
└── _components/
    ├── _author.css       # Author sidebar
    ├── _about.css        # About section
    ├── _articles.css     # Article list
    ├── _article.css      # Single article
    ├── _social.css       # Social links
    ├── _footer.css       # Footer
    └── _table.css        # Tables
```

## Data Flow

### Page Request Flow

```
1. User requests URL
2. GitHub Pages serves static HTML from public/
3. Browser loads:
   - HTML (Hugo-generated)
   - CSS (Parcel-bundled, from assets/output/)
   - JS (highlight.js from CDN)
   - Fonts (Google Fonts CDN)
```

### Content Flow

```
1. Author writes Markdown in content/post/
2. Hugo processes Markdown with templates
3. Templates reference bundled assets via resources.Get
4. Hugo outputs complete HTML to public/
```

## External Integrations

| Service | Purpose |
|---------|---------|
| GitHub Pages | Static hosting |
| Google Fonts | Typography (Karla, Rubik, Inconsolata) |
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
yarn dev          # Start dev server (Hugo + Parcel watch)
                  # Serves at http://localhost:1313
```

### Production Build

```bash
yarn build        # Build for production
                  # Output: public/
```

### Deployment

Automatic via GitHub Actions on push to `content` branch:
1. Checkout code
2. Setup Hugo 0.136.2 and Node.js 20.17.0
3. Install dependencies (`yarn`)
4. Build (`yarn build`)
5. Deploy `public/` to `master` branch
6. GitHub Pages serves from `master`

### Clean

```bash
yarn clean        # Remove public/, assets/output/, static/output/, resources/
```
