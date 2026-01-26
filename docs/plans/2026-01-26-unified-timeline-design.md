# Unified Timeline Design

**Date:** 2026-01-26
**Status:** Approved

## Problem

Talks are hidden on a separate page. Visitors don't discover them.

## Solution

Merge posts and talks into a single timeline on the homepage, sorted by date. Each item shows a colored badge to distinguish content type.

## Scope

**Building:**
- Unified timeline merging posts + talks by date
- Colored badge per item (blue for post, green for talk)
- Each item shows: badge, title, description, date

**Not building:**
- Filtering tabs
- "Thoughts" content type (defer until needed)
- Talk-specific metadata in feed (event name, slides - stay on detail page)

## Technical Approach

**Hugo query:**
```go
{{ $posts := where .Site.RegularPages "Section" "post" }}
{{ $talks := where .Site.RegularPages "Section" "talk" }}
{{ $all := $posts | union $talks }}
{{ range $all.ByDate.Reverse }}
```

**HTML structure:**
```html
<article class="feed-item feed-item--{{ .Section }}">
  <a href="{{ .RelPermalink }}">
    <span class="feed-item__badge">{{ .Section }}</span>
    <h2>{{ .Title }}</h2>
    <p>{{ .Params.description }}</p>
    <time>{{ .Date.Format "02 Jan 2006" }}</time>
  </a>
</article>
```

## Visual Design

- Badge: uppercase, small (0.7em), rounded corners, white text on colored bg
- Post badge: blue (`var(--blue)`)
- Talk badge: green (`#10b981`)
- Layout: badge left, content right
- Hover: light grey background

## Files to Modify

- `layouts/_default/list.html` - Update query and HTML
- `assets/stylesheets/main.css` - Add feed item styles

## What Stays the Same

- Author sidebar
- Footer
- `/talk/` dedicated page
- Single page template
- RSS feed (posts only)
