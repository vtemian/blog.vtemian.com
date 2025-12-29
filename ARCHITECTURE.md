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
