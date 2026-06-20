#!/usr/bin/env python3
"""Generate the "Dr. Elijah Ting" horizontal wordmark for the nav (on dark).

Composes the brand open-ring mark with a two-line lockup:
  - "Dr. Elijah Ting" in a bold serif, cream (for dark backgrounds)
  - "WORKPLACE RESILIENCE" in letter-spaced terracotta small caps

Output: assets/images/logo-wordmark-on-dark.png (transparent RGBA).

Run:  python3 scripts/make_wordmark.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

CREAM = (240, 233, 218, 255)   # warm cream wordmark color
TERRA = (192, 108, 84, 255)    # --terracotta #C06C54

# A bold serif close to the display face. Liberation Serif ships on most
# Linux images; swap to a Cormorant/Playfair TTF here for an exact match.
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "images")

NAME = "Dr. Elijah Ting"
SUB = "WORKPLACE RESILIENCE"


def build():
    W, H = 5200, 1400
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    name_size, sub_size = 360, 132
    name_font = ImageFont.truetype(SERIF_BOLD, name_size)
    sub_font = ImageFont.truetype(SERIF_BOLD, sub_size)
    sub_track = int(sub_size * 0.42)   # letter-spacing between caps

    nb = name_font.getbbox(NAME)
    name_h = nb[3] - nb[1]

    gap_name_sub = int(sub_size * 0.55)
    block_h = name_h + gap_name_sub + sub_size
    block_top = (H - block_h) // 2

    # exact brand ring (logo-ring-source.png): recolour the black mark to
    # cream via its alpha channel, then trim to the mark's bounding box so
    # sizing is consistent regardless of canvas padding.
    src = Image.open(os.path.join(IMG, "logo-ring-source.png")).convert("RGBA")
    ring = Image.new("RGBA", src.size, CREAM)
    ring.putalpha(src.split()[-1])
    ring = ring.crop(ring.getbbox())
    ring_h = int(block_h * 1.12)
    ring_w = int(ring.width * ring_h / ring.height)
    ring_scaled = ring.resize((ring_w, ring_h), Image.LANCZOS)
    ring_x = 120
    canvas.alpha_composite(ring_scaled, (ring_x, (H - ring_h) // 2))

    text_x = ring_x + ring_w + int(name_size * 0.42)

    # name (cream)
    draw.text((text_x - nb[0], block_top - nb[1]), NAME, font=name_font, fill=CREAM)

    # subtitle (terracotta, manually tracked), left-aligned to the name
    sub_y = block_top + name_h + gap_name_sub
    x = text_x
    for ch in SUB:
        draw.text((x, sub_y - sub_font.getbbox(ch)[1]), ch, font=sub_font, fill=TERRA)
        x += sub_font.getlength(ch) + sub_track

    # autocrop to content + padding, then downscale to a crisp delivery height
    bbox = canvas.getbbox()
    pad = 60
    bbox = (max(bbox[0] - pad, 0), max(bbox[1] - pad, 0),
            min(bbox[2] + pad, W), min(bbox[3] + pad, H))
    cropped = canvas.crop(bbox)

    target_h = 480
    ratio = target_h / cropped.height
    final = cropped.resize((int(cropped.width * ratio), target_h), Image.LANCZOS)

    out = os.path.join(IMG, "logo-wordmark-on-dark.png")
    final.save(out)
    print("wrote", out, final.size)


if __name__ == "__main__":
    build()
