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
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

# Blog color palette (from main.css)
BG_COLOR = (241, 245, 249)       # --grey-lighter: #f1f5f9
TITLE_COLOR = (30, 41, 59)       # --black: #1e293b
DESC_COLOR = (100, 116, 139)     # --grey: #64748b
ACCENT_COLOR = (59, 130, 246)    # --blue: #3b82f6
URL_COLOR = (148, 163, 184)      # muted slate

W, H = 1200, 630
AVATAR_PATH = os.path.join(os.path.dirname(__file__), "avatar.png")
AUTHOR_NAME = "Vlad Temian"
BLOG_URL = "blog.vtemian.com"
OUTPUT_NAME = "og.png"


def get_font(size, bold=False):
    candidates = []
    if bold:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux (CI)
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",      # macOS
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",       # Linux (CI)
            "/System/Library/Fonts/Supplemental/Arial.ttf",           # macOS
        ]
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


def generate_og(title, description, reading_time, output_path):
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(56, bold=True)
    font_desc = get_font(24)
    font_meta = get_font(18)
    font_author = get_font(22)

    # Left accent bar
    draw.rectangle([(0, 0), (5, H)], fill=ACCENT_COLOR)

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

    # Author row - avatar + name + URL, all on one line
    if os.path.exists(AVATAR_PATH):
        avatar = Image.open(AVATAR_PATH).convert("RGB")
        avatar = avatar.resize((44, 44), Image.LANCZOS)
        mask = Image.new("L", (44, 44), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, 44, 44), fill=255)
        img.paste(avatar, (left, y), mask)
        draw.text((left + 55, y + 10), AUTHOR_NAME, font=font_author, fill=TITLE_COLOR)

        # Dot separator + URL + reading time
        name_bbox = draw.textbbox((left + 55, y + 10), AUTHOR_NAME, font=font_author)
        dot_x = name_bbox[2] + 16
        url_text = f"·  {BLOG_URL}"
        draw.text((dot_x, y + 10), url_text, font=font_author, fill=URL_COLOR)
        url_bbox = draw.textbbox((dot_x, y + 10), url_text, font=font_author)
        rt_x = url_bbox[2] + 16
        draw.text((rt_x, y + 10), f"·  {reading_time} min read", font=font_author, fill=URL_COLOR)

    img.save(output_path, "PNG")


def main():
    content_dir = os.path.join(os.path.dirname(__file__), "..", "content", "post")
    content_dir = os.path.abspath(content_dir)

    # Find all page bundles (directories with index.md)
    bundles = glob.glob(os.path.join(content_dir, "*/index.md"))
    # Also find standalone .md files
    standalones = glob.glob(os.path.join(content_dir, "*.md"))

    generated = 0

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
        basename = os.path.splitext(os.path.basename(md_path))[0]
        bundle_dir = os.path.join(content_dir, basename)

        if os.path.exists(bundle_dir):
            continue  # already a bundle

        # Don't auto-convert, just skip
        print(f"  Skipped (not a bundle): {basename}.md")

    print(f"Generated {generated} OG image(s)")


if __name__ == "__main__":
    main()
