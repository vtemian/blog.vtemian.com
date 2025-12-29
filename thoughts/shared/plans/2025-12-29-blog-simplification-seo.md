# Blog Simplification and SEO Optimization Implementation Plan

**Goal:** Remove Parcel bundler, switch to Hugo Pipes for asset processing, and fix all SEO issues.

**Architecture:** Replace the two-stage build (Parcel → Hugo) with Hugo's native asset pipeline (Hugo Pipes with PostCSS). This eliminates 9+ npm dependencies while maintaining identical CSS output. SEO fixes include adding DOCTYPE, lang attribute, canonical links, Twitter Cards, and fixing broken JSON-LD.

**Design:** [thoughts/shared/designs/2025-12-29-blog-simplification-seo-design.md](../designs/2025-12-29-blog-simplification-seo-design.md)

---

## Phase 1: Build System Migration (Hugo Pipes)

### Task 1.1: Update package.json

**Files:**
- Modify: `package.json`

**Step 1: Update package.json with simplified dependencies and scripts**

Replace the entire `package.json` with:

```json
{
  "name": "blog-vtemian",
  "version": "3.0.0",
  "description": "Personal blog built with Hugo",
  "author": "Vlad Temian",
  "license": "MIT",
  "scripts": {
    "dev": "hugo server -D",
    "build": "hugo --minify",
    "clean": "rimraf public resources"
  },
  "devDependencies": {
    "postcss": "^8.5.6",
    "postcss-cli": "^11.0.1",
    "postcss-nested": "^7.0.2",
    "rimraf": "^6.1.2"
  }
}
```

**Step 2: Verify the change**

Run: `cat package.json`
Expected: File shows simplified scripts and only 4 devDependencies

**Step 3: Reinstall dependencies**

Run: `rm -rf node_modules && yarn install`
Expected: Successful installation with fewer packages

---

### Task 1.2: Update stylesheets.html for Hugo Pipes

**Files:**
- Modify: `layouts/partials/stylesheets.html`

**Step 1: Replace stylesheets.html with Hugo Pipes version**

Replace the entire file content with:

```html
{{ $css := resources.Get "stylesheets/main.css" }}
{{ $css = $css | postCSS }}
{{ if hugo.IsProduction }}
  {{ $css = $css | minify | fingerprint }}
{{ end }}
<link rel="stylesheet" href="{{ $css.RelPermalink }}" media="screen">
```

**Step 2: Verify the change**

Run: `cat layouts/partials/stylesheets.html`
Expected: File shows Hugo Pipes processing with postCSS

---

### Task 1.3: Update list.html to use Hugo Pipes for images

**Files:**
- Modify: `layouts/_default/list.html`

**Step 1: Update image resource paths from output/ to images/**

Replace the entire file content with:

```html
{{ define "content" }}

{{ $avatar := resources.Get "images/avatar.png" }}
{{ $github := resources.Get "images/github.png" }}
{{ $linkedin := resources.Get "images/linkedin.png" }}
{{ $twitter := resources.Get "images/x.png" }}
{{ $rss := resources.Get "images/rss.png" }}

<div class="container">
    <aside class="author">
        <img src="{{ $avatar.RelPermalink }}" alt="Avatar" />

        <h1>{{ .Site.Params.author }} </h1>
        <p class="social">
            <a href="https://github.com/vtemian">
                <img src="{{ $github.RelPermalink }}" alt="github" />
            </a>

            <a href="https://www.linkedin.com/in/vtemian">
                <img src="{{ $linkedin.RelPermalink }}" alt="linkedin" />
            </a>

            <a href="https://www.twitter.com/vtemian">
                <img src="{{ $twitter.RelPermalink }}" alt="twitter" />
            </a>

            <a href="index.xml">
                <img src="{{ $rss.RelPermalink }}" alt="rss" />
            </a>

            <a href="/resume.pdf" class="resume">
                CV
            </a>

        </p>

        <section class="about">
            <p>I build systems and <strong>bypass permissions</strong>. Over <strong>15 years</strong> helping startups scale production infrastructure. Former <strong>CTO</strong> of <a href="https://www.linkedin.com/company/qed-builders-software/" target="_blank" rel="noopener noreferrer">qed.builders</a> (acquired by <a href="https://www.linkedin.com/company/thesandbox-game/" target="_blank" rel="noopener noreferrer">The Sandbox</a>). Long-time open-source contributor with a <strong>systems caretaker</strong> mindset.</p>
        </section>

    </aside>

    <main class="articles">
	    {{ range where (.Site.RegularPages.ByDate.Reverse) "Section" "post" }}
	    <article>
		<a href="{{ .RelPermalink }}">
		    <h2>{{ .Title }}</h2>
		    <time>{{ .Date.Format "02 Jan 2006" }}</time>
		</a>
	    </article>
	    {{ end }}
    </main>

    {{ partial "footer" .}}

</div>

{{ end }}
```

**Step 2: Verify the change**

Run: `grep "resources.Get" layouts/_default/list.html`
Expected: Shows `resources.Get "images/avatar.png"` (not `output/`)

---

### Task 1.4: Update single.html to use Hugo Pipes for images

**Files:**
- Modify: `layouts/_default/single.html`

**Step 1: Update image resource path from output/ to images/**

Replace the entire file content with:

```html
{{ define "content" }}

{{ $avatar := resources.Get "images/avatar.png" }}

<div class="container container--is-large">
    <main class="article">
        <article>
            <header>
                <a href="/">&larr; Go back</a>
                <h1>{{ .Title }}</h1>

                <aside class="author author--is-small">
                    <img src="{{ $avatar.RelPermalink }}" alt="Avatar" />
                    <div>
                        <h4>{{ .Site.Params.author }} </h4>
                        <p>{{ .Date.Format "02 Jan 2006" }}</p>
                    </div>
                </aside>
            </header>
            <p>
                {{ .Content }}
            </p>
        </article>
    </main>
    {{ partial "footer" .}}
</div>

{{ end }}
```

**Step 2: Verify the change**

Run: `grep "resources.Get" layouts/_default/single.html`
Expected: Shows `resources.Get "images/avatar.png"` (not `output/`)

---

### Task 1.5: Verify Hugo Pipes build works

**Step 1: Clean previous build artifacts**

Run: `yarn clean`
Expected: Removes public/ and resources/ directories

**Step 2: Run development server**

Run: `yarn dev`
Expected: Hugo server starts without errors, site accessible at http://localhost:1313

**Step 3: Verify CSS loads correctly**

Open browser to http://localhost:1313, check:
- Page has styling (not unstyled HTML)
- No console errors about missing CSS
- Images load correctly

**Step 4: Stop dev server and commit**

```bash
git add package.json layouts/partials/stylesheets.html layouts/_default/list.html layouts/_default/single.html
git commit -m "feat(build): migrate from Parcel to Hugo Pipes for asset processing"
```

---

## Phase 2: SEO Fixes

### Task 2.1: Fix baseof.html - Add DOCTYPE and lang attribute

**Files:**
- Modify: `layouts/_default/baseof.html`

**Step 1: Update baseof.html with proper DOCTYPE and lang**

Replace the entire file content with:

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        {{ partial "header" .}}
        <meta name="google-site-verification" content="2qk_e0y84NNSVpaorKgeNURYF9Ni3UyJvPq9GZdGEgs" />
    </head>

    <body>
        {{ block "content" .}}{{ end }}
    </body>
</html>
```

**Step 2: Verify the change**

Run: `head -3 layouts/_default/baseof.html`
Expected: Shows `<!DOCTYPE html>` and `<html lang="en">`

---

### Task 2.2: Fix header.html - Remove duplicates, clean up fonts

**Files:**
- Modify: `layouts/partials/header.html`

**Step 1: Update header.html - remove duplicate meta tags and unused fonts**

Replace the entire file content with:

```html
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width,minimum-scale=1">

<link rel="stylesheet"
      href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/10.0.1/styles/atom-one-light.min.css">
<script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/10.0.1/highlight.min.js"></script>
<script>hljs.initHighlightingOnLoad();</script>

{{ partial "seo_schema" . }}

<title>{{.Title}}</title>

{{ partial "stylesheets.html" . }}
```

**Step 2: Verify the change**

Run: `cat layouts/partials/header.html`
Expected: 
- No `<meta charset="utf-8">` (moved to seo_schema.html)
- No `<meta content=... name="keywords">` (duplicate)
- No Google Fonts link (unused fonts removed)
- No `{{ partial "scripts.html" . }}` (removed)

---

### Task 2.3: Rewrite seo_schema.html - Fix JSON-LD, add Twitter Cards, cleanup

**Files:**
- Modify: `layouts/partials/seo_schema.html`

**Step 1: Replace seo_schema.html with fixed and cleaned version**

Replace the entire file content with:

```html
<meta charset="utf-8">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{{ .Permalink }}">

{{/* Favicon */}}
{{ $avatar := resources.Get "images/avatar.png" }}
<link rel="icon" type="image/png" href="{{ $avatar.RelPermalink }}">
<link rel="apple-touch-icon" href="{{ $avatar.RelPermalink }}">

{{/* Keywords */}}
<meta name="keywords" content="{{ if .Params.Keywords }}{{ delimit .Params.Keywords ", " }}{{ else }}{{ delimit .Site.Params.keywords ", " }}{{ end }}">

{{/* Description */}}
{{ $description := .Description | default .Summary | default .Site.Params.description | plainify | htmlUnescape }}
<meta name="description" content="{{ trim $description "\n\r\t " }}">

{{/* Open Graph */}}
<meta property="og:url" content="{{ .Permalink }}">
<meta property="og:site_name" content="{{ .Site.Title }}">
<meta property="og:title" content="{{ .Title }}">
<meta property="og:description" content="{{ trim $description "\n\r\t " }}">
<meta property="og:locale" content="en_US">

{{- if .IsPage }}
<meta property="og:type" content="article">
{{ $ISO8601 := "2006-01-02T15:04:05-07:00" }}
<meta property="article:published_time" content="{{ .PublishDate.Format $ISO8601 }}">
<meta property="article:modified_time" content="{{ .Lastmod.Format $ISO8601 }}">
{{- range .GetTerms "tags" | first 6 }}
<meta property="article:tag" content="{{ .Page.Title | plainify }}">
{{- end }}
{{- else }}
<meta property="og:type" content="website">
{{- end }}

{{/* Open Graph Image - use post image or fallback to avatar */}}
{{- $ogImage := $avatar }}
{{- with .Params.images }}
  {{- $firstImage := index . 0 }}
  {{- with $.Resources.GetMatch $firstImage }}
    {{- $ogImage = . }}
  {{- end }}
{{- end }}
<meta property="og:image" content="{{ $ogImage.Permalink }}">

{{/* Twitter Card */}}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{ .Title }}">
<meta name="twitter:description" content="{{ trim $description "\n\r\t " }}">
<meta name="twitter:image" content="{{ $ogImage.Permalink }}">

{{/* JSON-LD Structured Data */}}
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "mainEntityOfPage": {
         "@type": "WebPage",
         "@id": "{{ .Permalink }}"
    },
    "headline": "{{ .Title }}",
    "description": "{{ trim $description "\n\r\t " }}",
    "inLanguage": "en-US",
    "author": {
        "@type": "Person",
        "name": "{{ .Site.Params.author }}"
    },
    "publisher": {
        "@type": "Person",
        "name": "{{ .Site.Params.author }}"
    },
    "datePublished": "{{ .PublishDate.Format "2006-01-02T15:04:05-07:00" }}",
    "dateModified": "{{ .Lastmod.Format "2006-01-02T15:04:05-07:00" }}",
    "url": "{{ .Permalink }}",
    "wordCount": {{ .WordCount }},
    "keywords": [{{ range $i, $tag := .Params.tags }}{{ if $i }}, {{ end }}"{{ $tag }}"{{ end }}]
}
</script>
```

**Step 2: Verify the change**

Run: `grep -c "twitter:card" layouts/partials/seo_schema.html`
Expected: `1` (Twitter Card meta tag present)

Run: `grep "author" layouts/partials/seo_schema.html | head -3`
Expected: Shows `.Site.Params.author` (not `.Site.Author`)

---

### Task 2.4: Simplify get-page-images.html

**Files:**
- Modify: `layouts/partials/get-page-images.html`

**Step 1: Replace with simplified version**

Replace the entire file content with:

```html
{{- $imgs := slice }}
{{- $avatar := resources.Get "images/avatar.png" }}

{{/* Use images from frontmatter if specified */}}
{{- with .Params.images }}
  {{- range . }}
    {{- with $.Resources.GetMatch . }}
      {{- $imgs = $imgs | append . }}
    {{- end }}
  {{- end }}
{{- end }}

{{/* Fallback to avatar if no images found */}}
{{- if not $imgs }}
  {{- $imgs = $imgs | append $avatar }}
{{- end }}

{{- return $imgs }}
```

**Step 2: Verify the change**

Run: `wc -l layouts/partials/get-page-images.html`
Expected: ~17 lines (down from 47)

---

### Task 2.5: Verify SEO fixes and commit

**Step 1: Run development server**

Run: `yarn dev`
Expected: Hugo server starts without errors

**Step 2: View page source and verify**

Open http://localhost:1313 in browser, view page source, check:
- `<!DOCTYPE html>` at the very beginning
- `<html lang="en">`
- `<link rel="canonical" href="...">` present
- `<meta name="twitter:card" ...>` present
- JSON-LD has proper author format (not empty)

**Step 3: Commit SEO fixes**

```bash
git add layouts/_default/baseof.html layouts/partials/header.html layouts/partials/seo_schema.html layouts/partials/get-page-images.html
git commit -m "fix(seo): add DOCTYPE, lang, canonical, Twitter Cards, fix JSON-LD"
```

---

## Phase 3: Content Fixes

### Task 3.1: Fix serverless-hosting-platform.md description

**Files:**
- Modify: `content/post/serverless-hosting-platform.md`

**Step 1: Update frontmatter with proper description**

Change line 4 from:
```yaml
description: ""
```

To:
```yaml
description: "Building a serverless hosting platform using Knative, Tekton, and Kubernetes on bare metal - from cluster setup to automated CI/CD deployments"
```

**Step 2: Verify the change**

Run: `head -5 content/post/serverless-hosting-platform.md`
Expected: Shows non-empty description

---

### Task 3.2: Fix 2019.md typo

**Files:**
- Modify: `content/post/2019.md`

**Step 1: Fix typo in description**

Change line 4 from:
```yaml
description: "2019 - the beging"
```

To:
```yaml
description: "2019 - the beginning"
```

**Step 2: Verify the change**

Run: `grep "description" content/post/2019.md`
Expected: Shows "beginning" (not "beging")

---

### Task 3.3: Fix healthy-python-codebase.md description

**Files:**
- Modify: `content/post/healthy-python-codebase.md`

**Step 1: Update frontmatter with better description**

Change line 4 from:
```yaml
description: "Healthy Python Codebase"
```

To:
```yaml
description: "Guidelines for maintaining a healthy Python codebase: consistency, explicit code, fail-fast patterns, testing strategies, and practical refactoring examples"
```

**Step 2: Verify the change**

Run: `head -5 content/post/healthy-python-codebase.md`
Expected: Shows descriptive description (not just title repeat)

---

### Task 3.4: Commit content fixes

**Step 1: Commit all content changes**

```bash
git add content/post/serverless-hosting-platform.md content/post/2019.md content/post/healthy-python-codebase.md
git commit -m "fix(content): improve descriptions and fix typos"
```

---

## Phase 4: CSS Cleanup

### Task 4.1: Replace Meyer reset with modern minimal reset

**Files:**
- Modify: `assets/stylesheets/_globals/_reset.css`

**Step 1: Replace with modern minimal reset**

Replace the entire file content with:

```css
/* Modern CSS Reset */
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
```

**Step 2: Verify the change**

Run: `wc -l assets/stylesheets/_globals/_reset.css`
Expected: ~40 lines (down from 129)

---

### Task 4.2: Remove duplicate CSS variable

**Files:**
- Modify: `assets/stylesheets/_globals/_variables.css`

**Step 1: Remove duplicate --container-width-large**

The current file has:
```css
--container-width: 720px;
--container-width-large: 720px;
```

Both have the same value. Keep only `--container-width` and update `_base.css` to use it.

Replace the entire `_variables.css` content with:

```css
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
```

**Step 2: Update _base.css to remove --is-large modifier**

In `assets/stylesheets/_globals/_base.css`, change:

```css
.container {
  width: 100%;
  padding: 20px;
  margin: 0 auto;
  box-sizing: border-box;
  max-width: var(--container-width);

  &--is-large {
    max-width: var(--container-width-large);
  }
}
```

To:

```css
.container {
  width: 100%;
  padding: 20px;
  margin: 0 auto;
  box-sizing: border-box;
  max-width: var(--container-width);
}
```

**Step 3: Update single.html to remove unused class**

In `layouts/_default/single.html`, change:
```html
<div class="container container--is-large">
```

To:
```html
<div class="container">
```

**Step 4: Verify the changes**

Run: `grep "container-width-large" assets/stylesheets/_globals/_variables.css`
Expected: No output (variable removed)

---

### Task 4.3: Merge _about.css into _author.css

**Files:**
- Modify: `assets/stylesheets/_components/_author.css`
- Delete: `assets/stylesheets/_components/_about.css`
- Modify: `assets/stylesheets/main.css`

**Step 1: Add about styles to _author.css**

Replace the entire `_author.css` content with:

```css
.author {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  flex-direction: column;
  border-bottom: 3px dotted var(--black);

  p {
    color: var(--grey);
    font-size: var(--font-size-small);
  }

  h1 {
    font-weight: 700;
    margin: 15px 0 10px;
    font-size: var(--font-size-large);
  }

  img {
    width: 100px;
    height: 100px;
    border-radius: 100px;
  }

  &--is-small {
    margin-bottom: 0px;
    padding-bottom: 0px;
    flex-direction: row;
    border-bottom: none;

    img {
      width: 50px;
      height: 50px;
      margin-right: 15px;
    }
  }
}

.about {
  margin-top: 25px;
  margin-bottom: 10px;
  padding: 0;
  font-size: var(--font-size-medium);
  line-height: 1.7;
  text-align: left;

  p {
    color: var(--black);
  }

  strong {
    font-weight: 700;
  }
}
```

**Step 2: Update main.css to remove _about.css import**

Replace the entire `main.css` content with:

```css
@import "./_globals/_variables.css";
@import "./_globals/_reset.css";
@import "./_globals/_base.css";

@import "./_components/_author.css";
@import "./_components/_articles.css";
@import "./_components/_article.css";
@import "./_components/_social.css";
@import "./_components/_footer.css";
@import "./_components/_table.css";
```

**Step 3: Delete _about.css**

Run: `rm assets/stylesheets/_components/_about.css`

**Step 4: Verify the changes**

Run: `grep "_about" assets/stylesheets/main.css`
Expected: No output (import removed)

---

### Task 4.4: Verify CSS changes and commit

**Step 1: Run development server**

Run: `yarn dev`
Expected: Hugo server starts without errors

**Step 2: Verify styling in browser**

Open http://localhost:1313, check:
- Page styling looks identical to before
- About section still styled correctly
- Container width unchanged

**Step 3: Commit CSS cleanup**

```bash
git add assets/stylesheets/ layouts/_default/single.html
git commit -m "refactor(css): simplify reset, merge about into author, remove unused variable"
```

---

## Phase 5: File Cleanup

### Task 5.1: Delete Parcel-related files

**Files:**
- Delete: `assets/index.js`
- Delete: `assets/javascript/main.js`
- Delete: `assets/javascript/` (directory)
- Delete: `assets/output/` (directory)
- Delete: `.parcelrc`
- Delete: `layouts/partials/scripts.html`

**Step 1: Delete all Parcel-related files**

```bash
rm assets/index.js
rm -rf assets/javascript
rm -rf assets/output
rm .parcelrc
rm layouts/partials/scripts.html
```

**Step 2: Verify deletions**

Run: `ls assets/`
Expected: Only `images/` and `stylesheets/` directories remain

Run: `ls layouts/partials/`
Expected: No `scripts.html` file

**Step 3: Commit deletions**

```bash
git add -A
git commit -m "chore: remove Parcel bundler and related files"
```

---

## Phase 6: Final Verification

### Task 6.1: Full build test

**Step 1: Clean and rebuild**

```bash
yarn clean
yarn build
```

Expected: Build completes without errors

**Step 2: Verify output structure**

Run: `ls public/`
Expected: Contains index.html, post/, sitemap.xml, robots.txt, etc.

Run: `ls public/*.css 2>/dev/null || find public -name "*.css" | head -3`
Expected: CSS file exists in public directory

**Step 3: Check for broken links in output**

Run: `grep -r "output/" public/ | head -5`
Expected: No output (no references to old output/ directory)

---

### Task 6.2: SEO validation checklist

**Step 1: Validate HTML structure**

Run: `head -20 public/index.html`
Expected:
- First line is `<!DOCTYPE html>`
- `<html lang="en">`
- `<meta charset="utf-8">`
- `<link rel="canonical" ...>`

**Step 2: Validate Twitter Cards**

Run: `grep "twitter:" public/index.html`
Expected: Shows twitter:card, twitter:title, twitter:description, twitter:image

**Step 3: Validate JSON-LD**

Run: `grep -A 5 '"@type": "BlogPosting"' public/index.html`
Expected: Shows proper author object with name field

---

### Task 6.3: Update documentation

**Files:**
- Modify: `CLAUDE.md`

**Step 1: Update CLAUDE.md to reflect new build system**

Find and replace the "Asset Pipeline" section. Change:

```markdown
### Asset Pipeline (Hugo + Parcel)

The project uses a two-stage build process:

1. **Parcel** bundles assets from `assets/` → `assets/output/`
2. **Hugo** consumes bundled assets and generates the final site in `public/`

Assets entry point: `assets/index.js` imports:
- `stylesheets/main.css` (CSS entry point)
- Images (avatar, social icons)

Parcel is configured (`parcel-namer-hashless`) to output files without content hashes for stable Hugo references.
```

To:

```markdown
### Asset Pipeline (Hugo Pipes)

The project uses Hugo's native asset pipeline:

1. **Hugo Pipes** processes CSS through PostCSS (handles nested syntax)
2. **Hugo** fingerprints assets for cache busting in production
3. Final static site generated in `public/`

Assets are stored in `assets/`:
- `stylesheets/main.css` - CSS entry point (uses postcss-nested)
- `images/` - Avatar and social icons

No external bundler required - Hugo handles everything.
```

**Step 2: Commit documentation update**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md for Hugo Pipes migration"
```

---

## Rollback Plan

If issues are discovered after deployment:

1. **Revert all commits:**
   ```bash
   git revert HEAD~6..HEAD
   ```

2. **Restore node_modules:**
   ```bash
   yarn install
   ```

3. **Verify old build works:**
   ```bash
   yarn build
   ```

The old Parcel-based build will be restored.

---

## Summary of Changes

| Category | Before | After |
|----------|--------|-------|
| npm dependencies | 12 packages | 4 packages |
| Build stages | 2 (Parcel → Hugo) | 1 (Hugo only) |
| CSS reset | 129 lines (Meyer) | ~40 lines (modern) |
| SEO: DOCTYPE | Missing | Present |
| SEO: lang attribute | Missing | Present |
| SEO: Canonical | Missing | Present |
| SEO: Twitter Cards | Missing | Present |
| SEO: JSON-LD author | Broken | Fixed |
| Google Fonts | 4 fonts loaded | 0 (unused removed) |
| CSS files | 8 | 7 (_about merged) |

---

## Verification Commands Summary

```bash
# Build test
yarn clean && yarn build

# Check for old references
grep -r "output/" public/

# Validate DOCTYPE
head -1 public/index.html

# Validate Twitter Cards
grep "twitter:card" public/index.html

# Validate canonical
grep 'rel="canonical"' public/index.html

# Check CSS loads
curl -s http://localhost:1313 | grep -o 'href="[^"]*\.css"'
```
