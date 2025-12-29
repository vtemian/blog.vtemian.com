---
date: 2025-12-29
topic: "Blog Simplification and SEO Optimization"
status: validated
---

## Problem Statement

The blog has accumulated unnecessary complexity:
- Parcel bundler with 12 npm dependencies for a site with ~400 lines of CSS and zero JavaScript
- Unused dependencies (Tailwind, postcss-modules, etc.)
- SEO issues: missing Twitter Cards, broken JSON-LD, no canonical tags, duplicate meta tags
- Template bloat: audio/video/series handling that's never used

The goal is to simplify the build pipeline and fix all SEO issues in one cleanup.

## Constraints

- Must work with existing GitHub Actions deployment (push to `content` branch → deploy to GitHub Pages)
- `yarn build` must still produce valid output in `public/`
- No breaking changes to existing URLs
- Keep highlight.js for code syntax highlighting (loaded from CDN)

## Approach

**Full cleanup in one pass:**

1. Remove Parcel entirely, switch to Hugo's native asset pipeline (Hugo Pipes)
2. Fix all SEO issues in templates
3. Clean up unused template code and CSS
4. Update content frontmatter where needed

This approach chosen over incremental because:
- Hugo Pipes does exactly what Parcel is doing
- Zero JavaScript means the entire JS bundling pipeline is waste
- One testing cycle instead of multiple
- Blog is simple enough that risk is manageable

## Architecture

### Before
```
assets/index.js → Parcel → assets/output/ → Hugo → public/
(12 npm dependencies, two-stage build)
```

### After
```
assets/stylesheets/ → Hugo Pipes (PostCSS) → public/
assets/images/ → Hugo → public/
(2-3 npm deps: postcss, postcss-nested)
```

## Components

### Build System

| Component | Responsibility |
|-----------|----------------|
| Hugo Pipes | CSS processing with PostCSS, image fingerprinting, cache busting |
| PostCSS | Nested CSS syntax transformation (only plugin needed) |
| Hugo templates | Reference assets via Hugo's `resources.Get` pipeline |
| GitHub Actions | Runs `hugo --minify`, deploys `public/` to master branch |

### Files to Delete

| File/Directory | Reason |
|----------------|--------|
| `assets/index.js` | Parcel entry point, no longer needed |
| `assets/javascript/main.js` | Empty file |
| `assets/output/` | Entire Parcel output directory |
| `.parcelrc` | Parcel configuration |
| `layouts/partials/scripts.html` | Loads empty JS bundle |

### Files to Modify

| File | Changes |
|------|---------|
| `package.json` | Remove Parcel and unused deps, simplify scripts to just `hugo` commands |
| `layouts/partials/stylesheets.html` | Use Hugo Pipes instead of static reference to `assets/output/` |
| `layouts/_default/baseof.html` | Add DOCTYPE, lang attribute |
| `layouts/partials/header.html` | Remove duplicate meta tags, remove unused Google Fonts |
| `layouts/partials/seo_schema.html` | Add Twitter Cards, fix JSON-LD, remove unused audio/video/Facebook logic |
| `layouts/partials/get-page-images.html` | Simplify from 47 lines to ~10 lines |
| `assets/stylesheets/_reset.css` | Replace 129-line Meyer reset with minimal modern reset |
| `assets/stylesheets/_variables.css` | Remove duplicate `--container-width-large` variable |

### CSS Consolidation

Merge `_about.css` (17 lines) into `_author.css` (39 lines) - both style the same header section.

## Data Flow

1. Developer runs `yarn build` (or GitHub Actions triggers on push)
2. Hugo reads CSS from `assets/stylesheets/main.css`
3. Hugo Pipes processes CSS through PostCSS (handles nested syntax)
4. Hugo fingerprints CSS for cache busting (e.g., `main.abc123.css`)
5. Hugo processes images from `assets/images/` with fingerprinting
6. Templates output proper `<link>` and `<img>` tags with fingerprinted URLs
7. Final static site generated in `public/`
8. GitHub Actions deploys `public/` to master branch

## SEO Fixes

### Critical Fixes

| Issue | Fix |
|-------|-----|
| Missing DOCTYPE | Add `<!DOCTYPE html>` to `baseof.html` |
| Missing lang attribute | Add `lang="en"` to `<html>` tag |
| No canonical link | Add `<link rel="canonical" href="{{ .Permalink }}">` |
| Broken JSON-LD author | Change from `site.Author` to `site.Params.author` |
| Invalid JSON-LD | Fix trailing comma in keywords array |
| Duplicate charset | Remove from `header.html` (keep in `seo_schema.html`) |
| Duplicate keywords | Remove from `header.html` (keep in `seo_schema.html`) |

### New Additions

| Addition | Implementation |
|----------|----------------|
| Twitter Card meta tags | Add `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image` |
| Default og:image | Use `avatar.png` as fallback when post has no images |
| Favicon | Reference `avatar.png` as favicon and apple-touch-icon |

### Template Cleanup

Remove from `seo_schema.html`:
- Audio handling (~10 lines) - never used
- Video handling (~10 lines) - never used
- Series handling (~5 lines) - never used
- Facebook app_id/admin logic (~10 lines) - not configured

### Google Fonts Cleanup

Current `header.html` loads: Karla, Rubik, Inconsolata, Roboto Mono

CSS only uses: Roboto Mono

Remove: Karla, Rubik, Inconsolata from Google Fonts request

### Content Fixes

| Post | Fix |
|------|-----|
| `serverless-hosting-platform.md` | Add real description (currently empty) |
| `2019.md` | Fix typo "beging" → "beginning" |
| `healthy-python-codebase.md` | Write better description (currently just repeats title) |
| All posts missing `images` | Add `images: ["image.png"]` frontmatter for social sharing |

## Error Handling

- **PostCSS failure**: Hugo build fails with clear error message
- **Missing images**: Hugo errors on missing resources at build time
- **Invalid frontmatter**: Hugo catches during build
- **Template errors**: Hugo fails fast with line numbers

All errors caught at build time, before deployment.

## Testing Strategy

### Local Testing

1. Run `yarn dev` after changes
2. Verify all pages render correctly in browser
3. Check browser console for errors
4. Verify CSS loads and applies correctly

### SEO Validation

1. **HTML validity**: W3C Markup Validator (check DOCTYPE, lang, structure)
2. **Open Graph**: Facebook Sharing Debugger (paste URL, verify preview)
3. **Twitter Cards**: Twitter Card Validator (verify rich preview)
4. **JSON-LD**: Google Rich Results Test (paste URL, verify structured data)
5. **Canonical**: View source, confirm `<link rel="canonical">` present

### Deployment Testing

1. Push to `content` branch
2. Verify GitHub Actions workflow succeeds
3. Check live site renders correctly
4. Re-run SEO validators on live URLs

## npm Dependencies

### Before (12 packages)
```
parcel
parcel-namer-hashless
postcss
postcss-cli
postcss-import
postcss-modules
postcss-nested
@fullhuman/postcss-purgecss
tailwindcss
typeface-roboto
cross-env
npm-run-all
rimraf
```

### After (3 packages)
```
postcss
postcss-nested
postcss-cli (for Hugo Pipes)
```

Note: `cross-env`, `npm-run-all`, `rimraf` may be kept for convenience but are optional.

## package.json Scripts

### Before
```json
{
  "dev": "run-p dev:*",
  "dev:hugo": "hugo server -D",
  "dev:parcel": "parcel watch assets/index.js --dist-dir assets/output",
  "build": "parcel build assets/index.js --dist-dir assets/output && hugo --minify",
  "clean": "rimraf public assets/output static/output resources"
}
```

### After
```json
{
  "dev": "hugo server -D",
  "build": "hugo --minify",
  "clean": "rimraf public resources"
}
```

## Open Questions

None - all questions resolved during design discussion.

## Decisions Made

1. **Default og:image**: Use `avatar.png` as fallback for posts without images
2. **Favicon**: Use `avatar.png` as favicon and apple-touch-icon
