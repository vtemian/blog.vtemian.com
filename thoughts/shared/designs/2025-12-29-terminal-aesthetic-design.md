---
date: 2025-12-29
topic: "Terminal Aesthetic Redesign"
status: validated
---

## Problem Statement

The current blog has a brutalist/developer minimalist design with a light theme. The goal is to transform it into a dark terminal aesthetic similar to nof1.ai - simple, professional, readable, with subtle terminal-inspired effects.

## Constraints

- Pure CSS changes only - no JavaScript, no build process changes
- Must remain readable for long-form technical blog posts
- Keep existing layout structure (single column, 720px max)
- No theme toggle - dark mode only
- No new dependencies

## Approach

Transform the existing CSS variables and add minimal new styles to achieve a terminal aesthetic. The key is restraint - enough visual interest to feel "terminal" without becoming gimmicky or hurting readability.

## Architecture

No structural changes. All modifications happen in `assets/stylesheets/`:
- `_globals/_variables.css` - New color palette
- `_globals/_base.css` - Background, noise texture, base typography
- `_components/*` - Update colors to use new variables, add subtle effects

## Components

### Color System

Replace current palette with terminal colors:

| Variable | Current | New | Purpose |
|----------|---------|-----|---------|
| `--background` | (implicit white) | `#000000` | Page background |
| `--black` | `#232333` | `#00ff00` | Rename to `--foreground`, primary text |
| `--grey` | `#a5a5a5` | `#00aa00` | Secondary text (dates, muted content) |
| `--grey-lighter` | `#f2f2f2` | `#1a1a1a` | Borders, code backgrounds |
| `--blue` | `#5694f1` | `#00ffff` | Link underlines (cyan accent) |
| `--pink` | `#eb298c` | `#00ffff` | Hover states (cyan accent) |

New variables to add:
- `--glow-color: rgba(0, 255, 0, 0.4)` - For text-shadow glow effects
- `--noise-opacity: 0.03` - Subtle noise texture intensity

### Noise Texture Overlay

Add SVG noise filter as pseudo-element on body:

```
body::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("data:image/svg+xml,..."); /* inline SVG noise */
  pointer-events: none;
  z-index: 9999;
  opacity: var(--noise-opacity);
}
```

This creates the subtle grain effect seen on nof1.ai without external assets.

### Typography Adjustments

- Keep Roboto Mono (already terminal-appropriate)
- Add subtle letter-spacing increase (`0.02em`) for terminal feel
- Add text-shadow glow on headings: `0 0 10px var(--glow-color)`

### Link Behavior

Current: Black text with blue underline, pink background on hover
New: Green text with cyan underline, cyan glow on hover

```
a {
  color: var(--foreground);
  border-bottom: 1px solid var(--blue);
  transition: all 0.2s ease;
}

a:hover {
  color: var(--blue);
  text-shadow: 0 0 8px var(--blue);
}
```

### Code Blocks

- Background: `--grey-lighter` (dark grey `#1a1a1a`)
- Text: Bright green for contrast
- Consider switching highlight.js theme from `atom-one-light` to a dark theme like `atom-one-dark` or `monokai`

### Borders

Replace dotted borders with solid subtle ones:
- Current: `3px dotted var(--grey-lighter)` 
- New: `1px solid var(--grey-lighter)` or `1px solid #333`

The dotted pattern feels more "cute minimalist" than "terminal".

## Data Flow

No changes - purely presentational.

## Error Handling

N/A - CSS only.

## Testing Strategy

1. Visual inspection on development server (`yarn dev`)
2. Check all pages: homepage, individual posts
3. Verify code block readability with syntax highlighting
4. Test on mobile viewport
5. Ensure images (avatar, post images) still look good on dark background

## Open Questions

1. **Avatar image** - Current avatar may need adjustment for dark background (add subtle border or glow?)
2. **Social icons** - May need to invert or replace if they're dark icons on transparent background
3. **Highlight.js theme** - Switch to dark theme (requires changing CDN URL in header partial)

## Summary of Changes

Files to modify:
1. `assets/stylesheets/_globals/_variables.css` - New color palette
2. `assets/stylesheets/_globals/_base.css` - Dark background, noise texture, transitions
3. `assets/stylesheets/_components/_author.css` - Update colors
4. `assets/stylesheets/_components/_articles.css` - Update colors, hover states
5. `assets/stylesheets/_components/_article.css` - Update colors, code blocks
6. `assets/stylesheets/_components/_social.css` - Possibly invert icons
7. `assets/stylesheets/_components/_footer.css` - Update colors
8. `layouts/partials/header.html` - Change highlight.js to dark theme
