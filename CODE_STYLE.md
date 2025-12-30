# Code Style Guide

## Naming Conventions

### Files and Directories

| Type | Convention | Example |
|------|------------|---------|
| CSS files | `_kebab-case.css` with underscore prefix | `_author.css`, `_base.css` |
| CSS directories | `_kebab-case/` with underscore prefix | `_globals/`, `_components/` |
| Hugo templates | `kebab-case.html` | `baseof.html`, `single.html` |
| Hugo partials | `snake_case.html` or `kebab-case.html` | `seo_schema.html`, `header.html` |
| Blog posts | `kebab-case.md` or `kebab-case/index.md` | `healthy-python-codebase.md` |
| Images | `kebab-case.png` | `github.png`, `linkedin.png` |

### CSS Classes

| Pattern | Convention | Example |
|---------|------------|---------|
| Component | `.component-name` | `.author`, `.article`, `.articles` |
| Modifier | `.component--modifier` | `.author--is-small`, `.container--is-large` |
| State | `.component--is-state` | `.author--is-small` |

Uses BEM-like convention with `--` for modifiers.

### CSS Variables

```css
/* Colors: descriptive names */
--white: #ffffff;
--black: #232333;
--grey: #a5a5a5;
--blue: #5694f1;
--pink: #eb298c;

/* Semantic modifiers */
--grey-lighter: #f2f2f2;

/* Typography */
--font-family-mono: "Roboto Mono", ...;
--font-size-base: 0.9em;
--font-size-small: 0.85em;
--font-size-medium: 1em;
--font-size-large: 1.5em;

/* Layout */
--container-width: 720px;
```

## File Organization

### CSS Import Order

```css
/* 1. Globals first */
@import "./_globals/_variables.css";
@import "./_globals/_reset.css";
@import "./_globals/_base.css";

/* 2. Components second */
@import "./_components/_author.css";
@import "./_components/_about.css";
/* ... */
```

### Hugo Template Structure

```html
{{ define "content" }}

{{ $resource := resources.Get "output/file.png" }}

<div class="container">
    <!-- Main content -->
</div>

{{ end }}
```

## Code Patterns

### CSS Nesting (PostCSS)

Use native CSS nesting syntax:

```css
.component {
  property: value;

  /* Nested elements */
  h1 {
    property: value;
  }

  /* Modifiers with & */
  &--is-modifier {
    property: value;
  }

  /* Pseudo-classes */
  &:hover {
    property: value;
  }
}
```

### Hugo Resource Loading

Always load bundled assets via `resources.Get`:

```html
{{ $styles := resources.Get "output/index.css" }}
<link rel="stylesheet" href="{{ $styles.Permalink }}" media="screen">

{{ $github := resources.Get "images/github.png" }}
<img src="{{ $github.Permalink | relURL }}" alt="GitHub" />
```

### Hugo Partials

Include partials with context:

```html
{{ partial "header" . }}
{{ partial "footer" . }}
```

### Blog Post Frontmatter

Use YAML format:

```yaml
---
title: "Post Title"
date: 2020-09-21T15:04:57+02:00
description: "Brief description"
keywords:
    - keyword1
    - keyword2
tags:
    - tag1
    - tag2
---
```

### Page Bundles for Posts with Images

For posts with images, use a directory structure:

```
content/post/my-post/
├── index.md          # Post content
├── image1.png        # Referenced as ![](image1.png)
└── image2.png
```

## Formatting

### Prettier Configuration

```json
{
  "printWidth": 120
}
```

### CSS Formatting

- 2-space indentation
- One property per line
- Opening brace on same line
- Closing brace on own line
- Blank line between rule sets

```css
.component {
  property: value;
  property: value;

  nested {
    property: value;
  }
}
```

### HTML Formatting

- 4-space indentation in Hugo templates
- Attributes on same line when short
- Hugo template tags on own lines

## Do's and Don'ts

### Do

- Use CSS custom properties for colors, fonts, and sizes
- Use BEM-like naming for CSS classes
- Use PostCSS nesting for component styles
- Load assets via Hugo's `resources.Get`
- Use YAML frontmatter for blog posts
- Use page bundles for posts with images
- Keep CSS components in separate files

### Don't

- Don't use inline styles
- Don't hardcode colors (use variables)
- Don't use JavaScript for styling
- Don't reference assets directly from static/ in templates
- Don't use JSON frontmatter (project uses YAML)
- Don't add content hashes to asset filenames (handled by parcel-namer-hashless)

## Testing

### Manual Testing

```bash
yarn dev    # Start dev server, check http://localhost:1313
```

### Parcel Build Test

```bash
yarn test   # Test Parcel CSS bundling only
```

## Commit Style

No specific commit message format enforced. Follow conventional practices:
- Use imperative mood ("Add feature" not "Added feature")
- Keep first line under 72 characters
- Reference issues when applicable
