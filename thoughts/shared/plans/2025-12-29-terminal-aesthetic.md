# Modern Monospace Aesthetic Implementation Plan

**Goal:** Polish the blog with a refined 2026 aesthetic - professional, clean, monospace with subtle texture and muted colors while keeping the light background.

**Architecture:** Pure CSS changes to `assets/stylesheets/main.css` plus one font import in `layouts/partials/header.html`. No JavaScript, no build changes.

**Design:** [thoughts/shared/designs/2025-12-29-terminal-aesthetic-design.md](../designs/2025-12-29-terminal-aesthetic-design.md)

---

## Task 1: Add IBM Plex Mono Font Import

**Files:**
- Modify: `layouts/partials/header.html` (add after line 2)

**Step 1: Add Google Fonts import for IBM Plex Mono**

In `layouts/partials/header.html`, find:

```html
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width,minimum-scale=1">
```

Add after line 2:

```html
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width,minimum-scale=1">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
```

**Step 2: Verify the change**

Run: `hugo server -D`
Open browser dev tools, check Network tab
Expected: IBM Plex Mono font files load from fonts.gstatic.com

**Step 3: Commit**

```bash
git add layouts/partials/header.html
git commit -m "feat(theme): add IBM Plex Mono font import"
```

---

## Task 2: Update CSS Variables for Muted Color Palette

**Files:**
- Modify: `assets/stylesheets/main.css` (lines 5-21)

**Step 1: Replace the Variables section with muted palette**

In `assets/stylesheets/main.css`, find lines 5-21:

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

Replace with:

```css
:root {
  --white: #ffffff;
  --black: #1e293b;
  --grey: #64748b;
  --grey-lighter: #f1f5f9;
  --blue: #3b82f6;

  --font-family-mono: "IBM Plex Mono", "Courier New", monospace;

  --font-size-base: 0.9em;
  --font-size-small: 0.85em;
  --font-size-medium: 1em;
  --font-size-large: 1.5em;

  --container-width: 720px;
}
```

**Step 2: Verify the change**

Run: `hugo server -D`
Expected: Text appears in IBM Plex Mono, colors are slightly softer/muted

**Step 3: Commit**

```bash
git add assets/stylesheets/main.css
git commit -m "feat(theme): update color palette to muted slate tones and IBM Plex Mono"
```

---

## Task 3: Add Noise Texture Overlay and Letter Spacing

**Files:**
- Modify: `assets/stylesheets/main.css` (lines 71-78)

**Step 1: Update body styles and add noise texture pseudo-element**

Find this block (around line 71-78):

```css
body {
  background: var(--white);
  color: var(--black);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-base);
  font-weight: 550;
  line-height: 1.3;
}
```

Replace with:

```css
body {
  background: var(--white);
  color: var(--black);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-base);
  font-weight: 500;
  line-height: 1.3;
  letter-spacing: 0.01em;
}

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

**Step 2: Verify the change**

Run: `hugo server -D`
Expected: Very subtle grain texture visible over the white background (look closely)

**Step 3: Commit**

```bash
git add assets/stylesheets/main.css
git commit -m "feat(theme): add subtle noise texture overlay and letter spacing"
```

---

## Task 4: Update Link Styles with Smooth Transitions

**Files:**
- Modify: `assets/stylesheets/main.css` (lines 80-90)

**Step 1: Replace link styles with transition-based hover**

Find this block (around line 80-90):

```css
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
```

Replace with:

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

**Step 2: Verify the change**

Run: `hugo server -D`
Hover over any link
Expected: Text smoothly transitions to blue on hover (no pink background)

**Step 3: Commit**

```bash
git add assets/stylesheets/main.css
git commit -m "feat(theme): update links with smooth color transition on hover"
```

---

## Task 5: Update Author Section with Solid Border

**Files:**
- Modify: `assets/stylesheets/main.css` (lines 111-118)

**Step 1: Replace dotted border with solid border**

Find this block (around line 111-118):

```css
.author {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  flex-direction: column;
  border-bottom: 3px dotted var(--black);
}
```

Replace with:

```css
.author {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  flex-direction: column;
  border-bottom: 1px solid var(--grey-lighter);
}
```

**Step 2: Verify the change**

Run: `hugo server -D`
Expected: Author section has thin solid grey border instead of thick dotted black

**Step 3: Commit**

```bash
git add assets/stylesheets/main.css
git commit -m "feat(theme): replace author section dotted border with solid"
```

---

## Task 6: Update Articles List with Solid Borders and Hover Effects

**Files:**
- Modify: `assets/stylesheets/main.css` (lines 175-213)

**Step 1: Update article list border**

Find this block (around line 175-181):

```css
.articles article {
  display: flex;
  margin-bottom: 0;
  padding-bottom: 8px;
  justify-items: center;
  border-bottom: 3px dotted var(--grey-lighter);
}
```

Replace with:

```css
.articles article {
  display: flex;
  margin-bottom: 0;
  padding-bottom: 8px;
  justify-items: center;
  border-bottom: 1px solid var(--grey-lighter);
}
```

**Step 2: Update article link hover states**

Find this block (around line 193-209):

```css
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
```

Replace with:

```css
.articles article a {
  flex: 1;
  display: flex;
  align-items: center;
  color: var(--black);
  justify-content: space-between;
  border-bottom: none;
  padding: 4px 0;
  transition: background-color 0.15s ease;
}

.articles article a:hover {
  background-color: var(--grey-lighter);
}

.articles article a:hover time {
  color: var(--grey);
}
```

**Step 3: Verify the change**

Run: `hugo server -D`
Hover over article links
Expected: Subtle grey background on hover, smooth transition, solid borders

**Step 4: Commit**

```bash
git add assets/stylesheets/main.css
git commit -m "feat(theme): update article list with solid borders and subtle hover"
```

---

## Task 7: Update Footer with Solid Border

**Files:**
- Modify: `assets/stylesheets/main.css` (lines 334-339)

**Step 1: Replace dotted border with solid border**

Find this block (around line 334-339):

```css
.footer {
  padding-top: 40px;
  border-top: 3px dotted var(--black);
  color: var(--grey);
  font-size: var(--font-size-small);
}
```

Replace with:

```css
.footer {
  padding-top: 40px;
  margin-top: 40px;
  border-top: 1px solid var(--grey-lighter);
  color: var(--grey);
  font-size: var(--font-size-small);
}
```

**Step 2: Verify the change**

Run: `hugo server -D`
Expected: Footer has thin solid grey border instead of thick dotted black

**Step 3: Commit**

```bash
git add assets/stylesheets/main.css
git commit -m "feat(theme): replace footer dotted border with solid"
```

---

## Task 8: Final Verification

**Step 1: Full visual inspection**

Run: `hugo server -D`

Check all pages:
- [ ] Homepage: Light background, IBM Plex Mono font, subtle noise texture
- [ ] Author section: Solid grey border, muted colors
- [ ] Article list: Solid borders, subtle grey hover effect (no pink)
- [ ] Links: Blue underline, blue text on hover with smooth transition
- [ ] Footer: Solid grey border
- [ ] Overall: Professional, refined, muted aesthetic

**Step 2: Check mobile viewport**

Open browser dev tools, test at 375px width:
- [ ] Layout still works
- [ ] Text readable
- [ ] No horizontal scroll
- [ ] Hover states work on touch

**Step 3: Build for production**

Run: `hugo --gc --minify`
Expected: Build completes without errors

---

## Summary of Changes

| File | Changes |
|------|---------|
| `layouts/partials/header.html` | Add IBM Plex Mono Google Font import |
| `assets/stylesheets/main.css` | Muted color palette, IBM Plex Mono, noise texture, solid borders, smooth transitions |

## Color Reference

| Variable | Old Value | New Value | Purpose |
|----------|-----------|-----------|---------|
| `--black` | `#232333` | `#1e293b` | Softer slate-800 for text |
| `--grey` | `#a5a5a5` | `#64748b` | Muted slate grey |
| `--grey-lighter` | `#f2f2f2` | `#f1f5f9` | Subtle warm grey for backgrounds |
| `--blue` | `#5694f1` | `#3b82f6` | Slightly more saturated blue |
| `--pink` | `#eb298c` | (removed) | No longer used |

## Visual Changes Summary

| Element | Before | After |
|---------|--------|-------|
| Font | Roboto Mono | IBM Plex Mono |
| Background | Plain white | White with 3% noise texture |
| Link hover | Pink background | Blue text color |
| Article hover | Pink background | Subtle grey background |
| Borders | 3px dotted | 1px solid |
| Transitions | None | 0.15s ease on hover states |

## Rollback

If issues are discovered:

```bash
git revert HEAD~7..HEAD
```

This reverts all 7 commits from this implementation.
