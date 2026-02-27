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


def generate_og(title, description, reading_time, output_path):
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(58, bold=True)
    font_desc = get_font(26)
    font_meta = get_font(20)
    font_author = get_font(24)

    # Title - wrap and draw
    y = 55
    wrapped_title = textwrap.wrap(title, width=28)
    for line in wrapped_title:
        draw.text((60, y), line, font=font_title, fill=TITLE_COLOR)
        bbox = draw.textbbox((60, y), line, font=font_title)
        y = bbox[3] + 8

    # Reading time pill
    y += 18
    rt_text = f"{reading_time} min read"
    rt_bbox = draw.textbbox((0, 0), rt_text, font=font_meta)
    rt_w = rt_bbox[2] - rt_bbox[0] + 24
    rt_h = rt_bbox[3] - rt_bbox[1] + 14
    draw.rounded_rectangle(
        [(60, y), (60 + rt_w, y + rt_h)],
        radius=4,
        fill=ACCENT_COLOR,
    )
    draw.text((60 + 12, y + 5), rt_text, font=font_meta, fill=(255, 255, 255))
    y += rt_h + 22

    # Description
    if description:
        wrapped_desc = textwrap.wrap(description, width=55)
        for line in wrapped_desc[:3]:  # max 3 lines
            draw.text((60, y), line, font=font_desc, fill=DESC_COLOR)
            bbox = draw.textbbox((60, y), line, font=font_desc)
            y = bbox[3] + 6

    # Author avatar (circular)
    if os.path.exists(AVATAR_PATH):
        avatar = Image.open(AVATAR_PATH).convert("RGB")
        avatar = avatar.resize((60, 60), Image.LANCZOS)
        mask = Image.new("L", (60, 60), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, 60, 60), fill=255)
        avatar_x = W - 250
        avatar_y = H - 95
        img.paste(avatar, (avatar_x, avatar_y), mask)
        draw.text((avatar_x + 75, avatar_y + 15), AUTHOR_NAME, font=font_author, fill=TITLE_COLOR)

    # Blog URL bottom-left
    draw.text((60, H - 45), BLOG_URL, font=font_meta, fill=URL_COLOR)

    # Subtle top accent line
    draw.rectangle([(0, 0), (W, 4)], fill=ACCENT_COLOR)

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
