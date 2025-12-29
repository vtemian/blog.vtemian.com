# Terminal Aesthetic Redesign Implementation Plan

**Goal:** Transform the blog from a light brutalist theme to a dark terminal aesthetic with green text, cyan accents, subtle glow effects, and noise texture overlay.

**Architecture:** Pure CSS changes to `assets/stylesheets/main.css` plus one highlight.js theme swap in `layouts/partials/header.html`. No JavaScript, no build changes, no new dependencies.

**Design:** [thoughts/shared/designs/2025-12-29-terminal-aesthetic-design.md](../designs/2025-12-29-terminal-aesthetic-design.md)

---

## Task 1: Update CSS Variables for Terminal Color Palette

**Files:**
- Modify: `assets/stylesheets/main.css` (lines 5-21)

**Step 1: Replace the Variables section with terminal colors**

In `assets/stylesheets/main.css`, replace lines 5-21:

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

With this new terminal palette:

```css
:root {
  /* Terminal color palette */
  --background: #0a0a0a;
  --foreground: #00ff00;
  --foreground-dim: #00aa00;
  --surface: #1a1a1a;
  --border: #333333;
  --accent: #00ffff;
  --glow-green: rgba(0, 255, 0, 0.4);
  --glow-cyan: rgba(0, 255, 255, 0.5);

  /* Legacy aliases for compatibility */
  --white: #ffffff;
  --black: var(--foreground);
  --grey: var(--foreground-dim);
  --grey-lighter: var(--surface);
  --blue: var(--accent);
  --pink: var(--accent);

  --font-family-mono: "Roboto Mono", "Courier New", monospace;

  --font-size-base: 0.9em;
  --font-size-small: 0.85em;
  --font-size-medium: 1em;
  --font-size-large: 1.5em;

  --container-width: 720px;
}
```

**Step 2: Verify the change**

Run: `hugo server -D`
Expected: Site loads with green text on dark background

**Step 3: Commit**

```bash
git add assets/stylesheets/main.css
git commit -m "feat(theme): add terminal color palette variables"
```

---

## Task 2: Update Body Base Styles with Dark Background and Noise Texture

**Files:**
- Modify: `assets/stylesheets/main.css` (lines 71-78)

**Step 1: Replace the body styles in the Base section**

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
  background: var(--background);
  color: var(--foreground);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-base);
  font-weight: 550;
  line-height: 1.3;
  letter-spacing: 0.02em;
}

/* Noise texture overlay for terminal grain effect */
body::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 9999;
  opacity: 0.03;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
}
```

**Step 2: Verify the change**

Run: `hugo server -D`
Expected: Dark background with subtle grain texture visible

**Step 3: Commit**

```bash
git add assets/stylesheets/main.css
git commit -m "feat(theme): add dark background with noise texture overlay"
```

---

## Task 3: Update Link Styles with Glow Effects

**Files:**
- Modify: `assets/stylesheets/main.css` (lines 80-90)

**Step 1: Replace the link styles**

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
  color: var(--foreground);
  text-decoration: none;
  border-bottom: 1px solid var(--accent);
  transition: all 0.2s ease;
}

a:hover {
  color: var(--accent);
  background: transparent;
  border-bottom-color: var(--accent);
  text-shadow: 0 0 8px var(--glow-cyan);
}
```

**Step 2: Verify the change**

Run: `hugo server -D`
Expected: Links have cyan underline, glow cyan on hover (no pink background)

**Step 3: Commit**

```bash
git add assets/stylesheets/main.css
git commit -m "feat(theme): update links with cyan glow hover effect"
```

---

## Task 4: Update Code Block Styles

**Files:**
- Modify: `assets/stylesheets/main.css` (lines 100-105)

**Step 1: Replace the code styles**

Find this block (around line 100-105):

```css
code {
  font-family: var(--font-family-mono);
  font-size: var(--font-size-small);
  background: var(--grey-lighter);
  padding: 2px 4px;
}
```

Replace with:

```css
code {
  font-family: var(--font-family-mono);
  font-size: var(--font-size-small);
  background: var(--surface);
  padding: 2px 6px;
  border: 1px solid var(--border);
  border-radius: 3px;
  color: var(--foreground);
}

pre {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 16px;
  overflow-x: auto;
}

pre code {
  background: transparent;
  border: none;
  padding: 0;
}
```

**Step 2: Verify the change**

Run: `hugo server -D`
Expected: Code blocks have dark background with subtle border

**Step 3: Commit**

```bash
git add assets/stylesheets/main.css
git commit -m "feat(theme): style code blocks for dark terminal theme"
```

---

## Task 5: Update Author Section with Solid Borders

**Files:**
- Modify: `assets/stylesheets/main.css` (lines 111-165)

**Step 1: Update the author section border and add avatar glow**

Find this line (around line 117):

```css
  border-bottom: 3px dotted var(--black);
```

Replace with:

```css
  border-bottom: 1px solid var(--border);
```

**Step 2: Add glow effect to author name**

Find this block (around line 125-129):

```css
.author h1 {
  font-weight: 700;
  margin: 15px 0 10px;
  font-size: var(--font-size-large);
}
```

Replace with:

```css
.author h1 {
  font-weight: 700;
  margin: 15px 0 10px;
  font-size: var(--font-size-large);
  text-shadow: 0 0 10px var(--glow-green);
}
```

**Step 3: Add subtle glow to avatar**

Find this block (around line 131-135):

```css
.author img {
  width: 100px;
  height: 100px;
  border-radius: 100px;
}
```

Replace with:

```css
.author img {
  width: 100px;
  height: 100px;
  border-radius: 100px;
  border: 2px solid var(--border);
  box-shadow: 0 0 15px var(--glow-green);
}
```

**Step 4: Verify the change**

Run: `hugo server -D`
Expected: Author name glows green, avatar has subtle green glow border, solid border instead of dotted

**Step 5: Commit**

```bash
git add assets/stylesheets/main.css
git commit -m "feat(theme): update author section with glow effects and solid border"
```

---

## Task 6: Update Articles List with Solid Borders and Hover Effects

**Files:**
- Modify: `assets/stylesheets/main.css` (lines 167-214)

**Step 1: Update article list border**

Find this line (around line 180):

```css
  border-bottom: 3px dotted var(--grey-lighter);
```

Replace with:

```css
  border-bottom: 1px solid var(--border);
```

**Step 2: Update article link hover states**

Find this block (around line 193-205):

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
  color: var(--foreground);
  justify-content: space-between;
  border-bottom: none;
  padding: 8px 0;
  transition: all 0.2s ease;
}

.articles article a:hover {
  color: var(--accent);
  background: transparent;
  text-shadow: 0 0 8px var(--glow-cyan);
}

.articles article a:hover time {
  color: var(--accent);
}
```

**Step 3: Verify the change**

Run: `hugo server -D`
Expected: Article links glow cyan on hover, no pink background, solid borders

**Step 4: Commit**

```bash
git add assets/stylesheets/main.css
git commit -m "feat(theme): update article list with glow hover and solid borders"
```

---

## Task 7: Update Single Article Styles

**Files:**
- Modify: `assets/stylesheets/main.css` (lines 216-303)

**Step 1: Add glow to article headings**

Find this block (around line 239-243):

```css
.article h1 {
  font-weight: 700;
  margin-bottom: 0px;
  font-size: var(--font-size-large);
}
```

Replace with:

```css
.article h1 {
  font-weight: 700;
  margin-bottom: 0px;
  font-size: var(--font-size-large);
  text-shadow: 0 0 10px var(--glow-green);
}
```

**Step 2: Add subtle glow to h2 headings**

Find this block (around line 245-250):

```css
.article h2 {
  font-weight: 700;
  font-size: var(--font-size-medium);
  margin-bottom: 15px;
  margin-top: 30px;
}
```

Replace with:

```css
.article h2 {
  font-weight: 700;
  font-size: var(--font-size-medium);
  margin-bottom: 15px;
  margin-top: 30px;
  text-shadow: 0 0 6px var(--glow-green);
}
```

**Step 3: Update hr and blockquote colors**

Find this block (around line 277-281):

```css
.article hr {
  height: 1px;
  border: none;
  background: var(--grey-lighter);
}
```

Replace with:

```css
.article hr {
  height: 1px;
  border: none;
  background: var(--border);
}
```

Find this block (around line 292-298):

```css
.article blockquote {
  margin-left: -25px;
  padding-left: 25px;
  font-style: italic;
  font-size: var(--font-size-medium);
  border-left: 5px solid var(--black);
}
```

Replace with:

```css
.article blockquote {
  margin-left: -25px;
  padding-left: 25px;
  font-style: italic;
  font-size: var(--font-size-medium);
  border-left: 3px solid var(--accent);
  color: var(--foreground-dim);
}
```

**Step 4: Verify the change**

Run: `hugo server -D`
Expected: Article headings glow, blockquotes have cyan border

**Step 5: Commit**

```bash
git add assets/stylesheets/main.css
git commit -m "feat(theme): update article headings with glow and blockquote styling"
```

---

## Task 8: Update Social Icons with Invert Filter

**Files:**
- Modify: `assets/stylesheets/main.css` (lines 305-328)

**Step 1: Add invert filter to social icons**

Find this block (around line 325-328):

```css
.social img {
  width: 20px;
  height: 20px;
}
```

Replace with:

```css
.social img {
  width: 20px;
  height: 20px;
  filter: invert(1) sepia(1) saturate(5) hue-rotate(85deg);
  transition: filter 0.2s ease;
}

.social a:hover img {
  filter: invert(1) sepia(1) saturate(5) hue-rotate(130deg);
}
```

**Step 2: Update resume link styling**

Find this block (around line 318-323):

```css
.social a.resume {
  margin-left: 10px;
  margin-top: 2px;
  font-weight: 600;
  font-size: 1.2rem;
}
```

Replace with:

```css
.social a.resume {
  margin-left: 10px;
  margin-top: 2px;
  font-weight: 600;
  font-size: 1.2rem;
  color: var(--foreground);
  border-bottom: 1px solid var(--accent);
}

.social a.resume:hover {
  color: var(--accent);
  text-shadow: 0 0 8px var(--glow-cyan);
}
```

**Step 3: Verify the change**

Run: `hugo server -D`
Expected: Social icons appear green, turn cyan on hover

**Step 4: Commit**

```bash
git add assets/stylesheets/main.css
git commit -m "feat(theme): invert social icons for dark theme"
```

---

## Task 9: Update Footer with Solid Border

**Files:**
- Modify: `assets/stylesheets/main.css` (lines 330-339)

**Step 1: Update footer border**

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
  border-top: 1px solid var(--border);
  color: var(--foreground-dim);
  font-size: var(--font-size-small);
}

.footer a {
  color: var(--foreground-dim);
  border-bottom-color: var(--border);
}

.footer a:hover {
  color: var(--accent);
}
```

**Step 2: Verify the change**

Run: `hugo server -D`
Expected: Footer has solid border, dimmer text, links work correctly

**Step 3: Commit**

```bash
git add assets/stylesheets/main.css
git commit -m "feat(theme): update footer with solid border and dim styling"
```

---

## Task 10: Update Table Styles

**Files:**
- Modify: `assets/stylesheets/main.css` (lines 341-362)

**Step 1: Update table colors for dark theme**

Find this block (around line 351-361):

```css
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

Replace with:

```css
th,
td {
  border: 1px solid var(--border);
  padding: 0.6rem;
  text-align: left;
}

th {
  font-weight: 700;
  background: var(--surface);
  color: var(--accent);
}
```

**Step 2: Verify the change**

Run: `hugo server -D`
Expected: Tables have dark background, cyan headers

**Step 3: Commit**

```bash
git add assets/stylesheets/main.css
git commit -m "feat(theme): update table styles for dark theme"
```

---

## Task 11: Switch Highlight.js to Dark Theme

**Files:**
- Modify: `layouts/partials/header.html` (line 5)

**Step 1: Change highlight.js theme from atom-one-light to atom-one-dark**

Find this line (line 5):

```html
<link rel="stylesheet"
      href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/10.0.1/styles/atom-one-light.min.css">
```

Replace with:

```html
<link rel="stylesheet"
      href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/10.0.1/styles/atom-one-dark.min.css">
```

**Step 2: Verify the change**

Run: `hugo server -D`
Navigate to a blog post with code blocks
Expected: Code syntax highlighting uses dark theme colors

**Step 3: Commit**

```bash
git add layouts/partials/header.html
git commit -m "feat(theme): switch to dark syntax highlighting theme"
```

---

## Task 12: Final Verification and Cleanup

**Step 1: Full visual inspection**

Run: `hugo server -D`

Check all pages:
- [ ] Homepage: Dark background, green text, avatar glows, social icons visible
- [ ] Article list: Hover effects work, solid borders
- [ ] Single post: Headings glow, code blocks readable, images visible
- [ ] Tables: Dark background, cyan headers
- [ ] Footer: Solid border, links work

**Step 2: Check mobile viewport**

Open browser dev tools, test at 375px width:
- [ ] Layout still works
- [ ] Text readable
- [ ] No horizontal scroll

**Step 3: Build for production**

Run: `hugo --gc --minify`
Expected: Build completes without errors

**Step 4: Final commit (if any fixes needed)**

```bash
git add -A
git commit -m "feat(theme): complete terminal aesthetic redesign"
```

---

## Summary of Changes

| File | Changes |
|------|---------|
| `assets/stylesheets/main.css` | New color palette, dark background, noise texture, glow effects, solid borders, inverted icons |
| `layouts/partials/header.html` | Switch highlight.js to atom-one-dark theme |

## Color Reference

| Element | Color | Hex |
|---------|-------|-----|
| Background | Black | `#0a0a0a` |
| Primary text | Green | `#00ff00` |
| Secondary text | Dim green | `#00aa00` |
| Accent/links | Cyan | `#00ffff` |
| Surfaces | Dark grey | `#1a1a1a` |
| Borders | Grey | `#333333` |
| Green glow | Transparent green | `rgba(0, 255, 0, 0.4)` |
| Cyan glow | Transparent cyan | `rgba(0, 255, 255, 0.5)` |

## Rollback

If issues are discovered:

```bash
git revert HEAD~11..HEAD
```

This reverts all 11 commits from this implementation.
