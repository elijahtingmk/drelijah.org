#!/usr/bin/env python3
"""Refresh the social-media cover banners with the current nav wordmark
(gold interlocking helix + "Dr. Elijah Ting", no tagline), on the brand's
near-black background (#0E0D0B) at each platform's existing canvas size.

Each target's logo height and horizontal center were measured from the
banner it replaces, so the placement (including LinkedIn's rightward shift
clear of the profile-photo overlap in the bottom-left) matches what was
already there - only the artwork inside is refreshed.

Requires assets/images/logo-wordmark-on-dark.png to already be built by
make_wordmark.py.

Run: python3 scripts/make_cover_banners.py
"""
import os
from PIL import Image

BG = (14, 13, 11)  # matches --bg in main.css

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "images")
SOCIAL = os.path.join(ROOT, "assets", "social-media")

# (filename, canvas_w, canvas_h, logo_height, logo_center_x)
TARGETS = [
    ("fb-cover-banner.png", 1640, 924, 140, 1640 // 2),
    ("linkedin-cover-banner.png", 1584, 396, 116, 911),
    ("google-workspace-banner.png", 1600, 400, 128, 1600 // 2),
    ("whatsapp-business-banner.png", 1280, 480, 110, 1280 // 2),
]


def build(filename, W, H, logo_h, center_x):
    wordmark = Image.open(os.path.join(IMG, "logo-wordmark-on-dark.png")).convert("RGBA")
    wordmark = wordmark.crop(wordmark.getbbox())
    ratio = logo_h / wordmark.height
    logo = wordmark.resize((int(wordmark.width * ratio), logo_h), Image.LANCZOS)

    canvas = Image.new("RGB", (W, H), BG)
    x = center_x - logo.width // 2
    y = (H - logo.height) // 2
    canvas.paste(logo, (x, y), logo)

    out = os.path.join(SOCIAL, filename)
    canvas.save(out)
    print("wrote", out, canvas.size)


if __name__ == "__main__":
    for filename, w, h, logo_h, cx in TARGETS:
        build(filename, w, h, logo_h, cx)
