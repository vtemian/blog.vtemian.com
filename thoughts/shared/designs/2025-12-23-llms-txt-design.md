---
date: 2025-12-23
topic: "llms.txt for blog discovery"
status: validated
---

## Problem Statement

Enable LLMs to discover and understand the blog content by providing a machine-readable index of posts following the llms.txt specification.

## Constraints

- Must auto-generate at build time (no manual maintenance)
- Must use existing frontmatter data (title, date, description)
- Must follow the llms.txt spec format
- No code changes to existing templates or styles

## Approach

Create a Hugo template that generates `/llms.txt` at build time. The template iterates through all posts and outputs structured metadata in the llms.txt spec format.

Chosen over alternatives:
- Static file: Rejected because it requires manual updates when posts change
- Full content inclusion: Rejected as overkill for discovery use case

## Architecture

Single new Hugo template file that hooks into Hugo's custom output format system.

## Components

**layouts/llms.txt**
- Hugo template that generates the llms.txt content
- Iterates through all posts in reverse chronological order
- Extracts title, permalink, and description from each post's frontmatter

**config.toml additions**
- Define custom output format for llms.txt (media type: text/plain)
- Add llms.txt to home page outputs

## Data Flow

1. Hugo build process triggers
2. Home page outputs include llms.txt format
3. Template queries all posts via `.Site.RegularPages`
4. For each post: extract title, permalink, description
5. Output formatted text following llms.txt spec
6. File written to `public/llms.txt`

## Output Format

```
# Vlad Temian's Blog

> [Site description from config]

## Posts

- [Post Title](https://blog.vtemian.com/post/slug/): Post description from frontmatter
- [Post Title](https://blog.vtemian.com/post/slug/): Post description from frontmatter
...
```

## Error Handling

- Posts without descriptions: Output title and URL only, omit description
- Empty blog: Output header with empty posts section

## Testing Strategy

1. Run `yarn build` and verify `public/llms.txt` exists
2. Verify file contains expected header with site title and description
3. Verify all posts appear with correct titles, URLs, and descriptions
4. Verify posts are in reverse chronological order
5. Verify output follows llms.txt spec format

## Open Questions

None - design validated by Vlad.
