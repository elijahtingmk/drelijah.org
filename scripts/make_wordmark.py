#!/usr/bin/env python3
"""Generate the "Dr. Elijah Ting" horizontal wordmark for the nav (on dark).

Composes the brand interlocking-helix mark (logo-helix-source.png, kept in its
own gold on both themes) with the name "Dr. Elijah Ting" in a bold serif,
cream (for dark backgrounds). Name-only, deliberately without a tagline —
the nav is too compressed to carry one legibly, and the positioning is
already stated in each page's hero and footer.

Output: assets/images/logo-wordmark-on-dark.png (transparent RGBA).

Run:  python3 scripts/make_wordmark.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

CREAM = (240, 233, 218, 255)   # warm cream wordmark color
BLACK = (26, 24, 19, 255)      # near-black ink for light backgrounds

# A bold serif close to the display face. Liberation Serif ships on most
# Linux images; swap to a Cormorant/Playfair TTF here for an exact match.
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
if not os.path.exists(SERIF_BOLD):
    # Try Mac Supplemental Georgia Bold
    SERIF_BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
if not os.path.exists(SERIF_BOLD):
    # Fallback to standard Georgia font
    SERIF_BOLD = "Georgia"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "images")

NAME = "Dr. Elijah Ting"


def build(theme="dark"):
    W, H = 4200, 900
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    # Color selection based on theme
    if theme == "dark":
        text_color = CREAM
        file_suffix = "on-dark"
    else:
        text_color = BLACK
        file_suffix = "on-light"

    name_size = 360
    name_font = ImageFont.truetype(SERIF_BOLD, name_size)

    nb = name_font.getbbox(NAME)
    name_h = nb[3] - nb[1]
    block_top = (H - name_h) // 2

    # exact brand mark (logo-helix-source.png): the interlocking gold helix,
    # already transparent and coloured — used as-is on both themes rather
    # than recoloured, since gold is the constant brand accent, not a
    # theme-adaptive monochrome shape.
    ring = Image.open(os.path.join(IMG, "logo-helix-source.png")).convert("RGBA")
    ring = ring.crop(ring.getbbox())
    ring_h = int(name_h * 1.12)
    ring_w = int(ring.width * ring_h / ring.height)
    ring_scaled = ring.resize((ring_w, ring_h), Image.LANCZOS)
    ring_x = 120
    canvas.alpha_composite(ring_scaled, (ring_x, (H - ring_h) // 2))

    text_x = ring_x + ring_w + int(name_size * 0.42)

    # name
    draw.text((text_x - nb[0], block_top - nb[1]), NAME, font=name_font, fill=text_color)

    # autocrop to content + padding, then downscale to a crisp delivery height
    bbox = canvas.getbbox()
    pad = 60
    bbox = (max(bbox[0] - pad, 0), max(bbox[1] - pad, 0),
            min(bbox[2] + pad, W), min(bbox[3] + pad, H))
    cropped = canvas.crop(bbox)

    target_h = 480
    ratio = target_h / cropped.height
    final = cropped.resize((int(cropped.width * ratio), target_h), Image.LANCZOS)

    out = os.path.join(IMG, f"logo-wordmark-{file_suffix}.png")
    final.save(out)
    print("wrote", out, final.size)


if __name__ == "__main__":
    build("dark")
    build("light")
