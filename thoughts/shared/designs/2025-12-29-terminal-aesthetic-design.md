---
date: 2025-12-29
topic: "Modern Monospace Aesthetic Redesign"
status: validated
---

## Problem Statement

The current blog has a solid brutalist/developer minimalist design. The goal is to refine it with a more modern "2026" aesthetic similar to nof1.ai's light mode - professional, clean, monospace, with subtle texture and muted colors.

## Constraints

- Pure CSS changes only - no JavaScript, no build process changes
- Keep light/white background
- Keep existing layout structure (single column, 720px max)
- No new dependencies (except possibly a font swap)

## Approach

Polish pass on existing design:
1. Add subtle noise texture overlay for visual depth
2. Switch from Roboto Mono to IBM Plex Mono (more refined)
3. Replace pink accent with muted blue
4. Add smooth transitions on hover states
5. Clean up borders (solid instead of dotted)

## Architecture

No structural changes. All modifications happen in `assets/stylesheets/` and one partial.

## Components

### Color System

| Variable | Current | New | Purpose |
|----------|---------|-----|---------|
| `--white` | `#ffffff` | `#ffffff` | Keep |
| `--black` | `#232333` | `#1e293b` | Slightly softer black (slate-800) |
| `--grey` | `#a5a5a5` | `#64748b` | Muted slate grey |
| `--grey-lighter` | `#f2f2f2` | `#f1f5f9` | Subtle warm grey |
| `--blue` | `#5694f1` | `#3b82f6` | Keep similar blue for links |
| `--pink` | `#eb298c` | `#1e293b` | Replace with dark text on hover (inverted) |

New variable:
- `--noise-opacity: 0.03` - Subtle noise texture intensity

### Noise Texture Overlay

Add SVG noise filter as pseudo-element on body - same technique as nof1.ai but very subtle:

```css
body::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.03;
  pointer-events: none;
  z-index: 9999;
}
```

### Typography

Switch font family:
- Current: `"Roboto Mono", "Courier New", monospace`
- New: `"IBM Plex Mono", "Courier New", monospace`

Add Google Font import in header partial or use system monospace fallback.

Slight letter-spacing refinement: `0.01em` for body text.

### Link Behavior

Current: Black text with blue underline, pink background on hover
New: Black text with blue underline, blue text on hover (no background change)

```css
a {
  color: var(--black);
  text-decoration: none;
  border-bottom: 1px solid var(--blue);
  transition: color 0.15s ease;
}

a:hover {
  color: var(--blue);
}
```

### Article List Hover

Current: Pink background, white text
New: Subtle grey background, keep text colors

```css
.articles article:hover {
  background-color: var(--grey-lighter);
}
```

### Borders

Replace dotted with solid:
- Current: `3px dotted var(--grey-lighter)`
- New: `1px solid var(--grey-lighter)`

More refined, less playful.

### Transitions

Add smooth transitions throughout (currently none):
- Links: `transition: color 0.15s ease`
- Hover states: `transition: background-color 0.15s ease`

## Data Flow

No changes - purely presentational.

## Error Handling

N/A - CSS only.

## Testing Strategy

1. Visual inspection on development server (`hugo server -D`)
2. Check all pages: homepage, individual posts
3. Verify readability and contrast
4. Test on mobile viewport

## Summary of Changes

Files to modify:
1. `assets/stylesheets/_globals/_variables.css` - Updated color palette
2. `assets/stylesheets/_globals/_base.css` - Noise texture, transitions, font
3. `assets/stylesheets/_components/_author.css` - Solid borders
4. `assets/stylesheets/_components/_articles.css` - Hover states, solid borders
5. `assets/stylesheets/_components/_article.css` - Solid borders
6. `assets/stylesheets/_components/_footer.css` - Solid borders
7. `layouts/partials/header.html` - Add IBM Plex Mono font import
