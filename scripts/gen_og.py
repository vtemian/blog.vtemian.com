#!/usr/bin/env python3
"""Generate OG images for blog posts that don't already have one.

Reads frontmatter from each post, generates a 1200x630 social card with
title, description, reading time, author avatar, and blog URL.

Runs as a build step before Hugo. Output goes into the post's page bundle
directory so Hugo can pick it up via Resources.GetMatch.
"""
import glob
import math
import os
import re
import textwrap

from PIL import Image, ImageDraw, ImageFont

# Blog color palette (from main.css)
BG_COLOR = (252, 252, 252)       # --color-bg: #fcfcfc
TITLE_COLOR = (44, 59, 73)       # --color-ink: #2c3b49
DESC_COLOR = (96, 100, 111)      # --color-muted: #60646F
MUTED_COLOR = (138, 153, 168)    # --color-link: #8a99a8
BORDER_COLOR = (232, 232, 236)   # --color-border: #E8E8EC

W, H = 1200, 630
AVATAR_PATH = os.path.join(os.path.dirname(__file__), "avatar.png")
AUTHOR_NAME = "Vlad Temian"
BLOG_URL = "blog.vtemian.com"
OUTPUT_NAME = "og.png"


FONTS_DIR = os.path.join(os.path.dirname(__file__), "fonts")


def get_font(size, bold=False):
    weight = "Bold" if bold else "Regular"
    candidates = [
        os.path.join(FONTS_DIR, f"Geist-{weight}.ttf"),              # bundled Geist
        f"/usr/share/fonts/truetype/dejavu/DejaVuSans-{weight}.ttf", # Linux (CI)
    ]
    if bold:
        candidates.append("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
    else:
        candidates.append("/System/Library/Fonts/Supplemental/Arial.ttf")
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def parse_frontmatter(content):
    """Extract title, description, and word count from markdown with YAML frontmatter."""
    fm_match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not fm_match:
        return None

    fm_text = fm_match.group(1)
    body = fm_match.group(2)

    title = ""
    desc = ""

    for line in fm_text.split("\n"):
        if line.startswith("title:"):
            title = line.split(":", 1)[1].strip().strip('"').strip("'")
        elif line.startswith("description:"):
            desc = line.split(":", 1)[1].strip().strip('"').strip("'")

    word_count = len(re.findall(r"\w+", body))
    reading_time = max(1, math.ceil(word_count / 200))

    return {"title": title, "description": desc, "reading_time": reading_time}


def measure_block(draw, title, description, reading_time, fonts):
    """Measure total height of content block for vertical centering."""
    font_title, font_desc, font_meta = fonts
    total = 0

    # Title
    wrapped_title = textwrap.wrap(title, width=28)
    for line in wrapped_title:
        bbox = draw.textbbox((0, 0), line, font=font_title)
        total += (bbox[3] - bbox[1]) + 8
    total += 16  # gap after title

    # Description
    if description:
        wrapped_desc = textwrap.wrap(description, width=60)
        for line in wrapped_desc[:3]:
            bbox = draw.textbbox((0, 0), line, font=font_desc)
            total += (bbox[3] - bbox[1]) + 6
        total += 20  # gap after desc

    # Author row
    total += 50

    return total


def make_squircle_mask(size, radius=10):
    """Create a squircle (rounded-rect) alpha mask."""
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [(0, 0), (size - 1, size - 1)], radius=radius, fill=255
    )
    return mask


def generate_og(title, description, reading_time, output_path):
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(56, bold=True)
    font_desc = get_font(24)
    font_meta = get_font(18)
    font_author = get_font(22)

    # Measure content height for vertical centering
    total_h = measure_block(draw, title, description, reading_time,
                            (font_title, font_desc, font_meta))
    y = max(40, (H - total_h) // 2)
    left = 60

    # Title
    wrapped_title = textwrap.wrap(title, width=28)
    for line in wrapped_title:
        draw.text((left, y), line, font=font_title, fill=TITLE_COLOR)
        bbox = draw.textbbox((left, y), line, font=font_title)
        y = bbox[3] + 8
    y += 16

    # Description
    if description:
        wrapped_desc = textwrap.wrap(description, width=60)
        for line in wrapped_desc[:3]:
            draw.text((left, y), line, font=font_desc, fill=DESC_COLOR)
            bbox = draw.textbbox((left, y), line, font=font_desc)
            y = bbox[3] + 6
    y += 20

    # Author row - avatar + name + URL + reading time
    if os.path.exists(AVATAR_PATH):
        avatar = Image.open(AVATAR_PATH).convert("RGB")
        avatar = avatar.resize((44, 44), Image.LANCZOS)
        mask = make_squircle_mask(44, radius=10)
        img.paste(avatar, (left, y), mask)
        draw.text((left + 55, y + 10), AUTHOR_NAME, font=font_author, fill=TITLE_COLOR)

        name_bbox = draw.textbbox((left + 55, y + 10), AUTHOR_NAME, font=font_author)
        dot_x = name_bbox[2] + 16
        url_text = f"·  {BLOG_URL}"
        draw.text((dot_x, y + 10), url_text, font=font_author, fill=MUTED_COLOR)
        url_bbox = draw.textbbox((dot_x, y + 10), url_text, font=font_author)
        rt_x = url_bbox[2] + 16
        draw.text((rt_x, y + 10), f"·  {reading_time} min read", font=font_author, fill=MUTED_COLOR)

    # Subtle bottom separator line
    draw.line([(left, H - 30), (W - left, H - 30)], fill=BORDER_COLOR, width=1)

    img.save(output_path, "PNG")


def main():
    content_dirs = [
        os.path.join(os.path.dirname(__file__), "..", "content", "post"),
        os.path.join(os.path.dirname(__file__), "..", "content", "project"),
        os.path.join(os.path.dirname(__file__), "..", "content", "talk"),
    ]
    
    generated = 0
    
    for content_dir in content_dirs:
        content_dir = os.path.abspath(content_dir)
        if not os.path.exists(content_dir):
            continue
            
        # Find all page bundles (directories with index.md)
        bundles = glob.glob(os.path.join(content_dir, "**/index.md"), recursive=True)
        # Also find standalone .md files
        standalones = glob.glob(os.path.join(content_dir, "*.md"))

        for md_path in bundles:
            post_dir = os.path.dirname(md_path)
            output_path = os.path.join(post_dir, OUTPUT_NAME)

            if os.path.exists(output_path):
                continue

            with open(md_path, "r") as f:
                content = f.read()

            meta = parse_frontmatter(content)
            if not meta or not meta["title"]:
                continue

            generate_og(meta["title"], meta["description"], meta["reading_time"], output_path)
            generated += 1
            print(f"  Generated: {os.path.relpath(output_path, content_dir)}")

        # For standalone .md files, convert to bundle first
        for md_path in standalones:
            if os.path.basename(md_path) == "_index.md":
                continue
            basename = os.path.splitext(os.path.basename(md_path))[0]
            bundle_dir = os.path.join(content_dir, basename)

            if os.path.exists(bundle_dir):
                continue  # already a bundle

            # Don't auto-convert, just skip
            print(f"  Skipped (not a bundle): {basename}.md")

    print(f"Generated {generated} OG image(s)")


if __name__ == "__main__":
    main()
