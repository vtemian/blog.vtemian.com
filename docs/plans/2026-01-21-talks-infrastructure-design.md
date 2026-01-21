# Talks Infrastructure Design

**Date:** 2026-01-21
**Status:** Approved

## Overview

Add presentation/talk support to the blog using Marp (Markdown to slides) with a WebGL animated backdrop effect, mirroring the approach used by Armin Ronacher.

## Requirements

- Talks live on the blog but aren't linked from navigation
- Same tech stack as https://mitsuhiko.github.io/talks/me-and-the-machine/
- Scalable to multiple talks
- Local development and CI deployment

## Folder Structure

```
blog.vtemian.com/
├── talks/
│   ├── Makefile                    # Shared, builds all talks
│   ├── inject-backdrop.js          # WebGL effect injection (ported from Armin)
│   ├── waves.mp4                   # Shared backdrop video
│   ├── .gitignore                  # Ignore built HTML
│   │
│   └── indie-hacking-update/
│       └── indie-hacking-update.md
│
├── static/
│   └── talks/                      # Built by CI, gitignored
│       └── indie-hacking-update/
│           └── index.html
```

## Build Process

### Makefile (talks/Makefile)

Auto-discovers talks by folder name:

```makefile
TALKS := $(wildcard */.)
TALK_NAMES := $(TALKS://.=)

all: $(TALK_NAMES)

$(TALK_NAMES):
	npx @marp-team/marp-cli --html $@/$@.md -o $@/$@.html
	node inject-backdrop.js $@/$@.html
	mkdir -p ../static/talks/$@
	cp $@/$@.html ../static/talks/$@/index.html
	cp waves.mp4 ../static/talks/$@/

clean:
	rm -f */*.html
```

### Adding a New Talk

1. Create `talks/new-talk/new-talk.md`
2. Run `make`
3. Commit and push

## Visual Design

### Color Palette (Armin's warm tones)

- Background: `#f5f0e8` (cream)
- Text: `#3d3428` (dark brown)
- Accent: `#d4a050` (gold)
- Quote slides: `#2e2a1a` (dark brown background)

### Typography

- Font: Google Sans Code (monospace)

### Backdrop

- WebGL canvas with Atkinson dithering algorithm
- Video texture from `waves.mp4`
- Fixed position behind slides

## Marp Template

```markdown
---
marp: true
theme: default
paginate: false
---

<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans+Mono&display=swap');

section {
  font-family: 'Google Sans Code', monospace;
  background-color: #f5f0e8;
  color: #3d3428;
}

blockquote {
  border-left: 4px solid #d4a050;
  padding-left: 1em;
}

section.quote {
  background-color: #2e2a1a;
  color: #f5f0e8;
}
</style>

# Talk Title

Author Name

---

## Slide Title

Content...

---

<!-- _class: quote -->

> Quote text

```

## Deployment

### Local Development

```bash
cd talks
make                    # builds to static/talks/
cd ..
hugo server -D          # preview at localhost:1313/talks/indie-hacking-update/
```

Built HTML stays in `.gitignore` for local dev.

### CI Deployment

GitHub Actions builds talks before Hugo:

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'

- name: Build talks
  run: |
    cd talks
    npm install @marp-team/marp-cli
    make

- name: Build Hugo
  run: hugo --gc --minify
```

### What Gets Committed

- `talks/indie-hacking-update/indie-hacking-update.md` - source
- `talks/Makefile` - build script
- `talks/inject-backdrop.js` - WebGL injection
- `talks/waves.mp4` - backdrop video
- `static/talks/*` - gitignored, built by CI

## Output

- URL: `blog.vtemian.com/talks/indie-hacking-update/`
- Not linked from blog navigation (unlisted but accessible)

## Dependencies

- Node.js (for Marp CLI)
- `@marp-team/marp-cli` (installed via npx/npm)

## Files to Create

1. `talks/Makefile`
2. `talks/inject-backdrop.js` (port from Armin)
3. `talks/waves.mp4` (copy from Armin)
4. `talks/.gitignore`
5. `talks/indie-hacking-update/indie-hacking-update.md`
6. Update `.github/workflows/` for Node.js + talks build
7. Update root `.gitignore` for `static/talks/`
