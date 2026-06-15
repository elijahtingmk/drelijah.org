#!/usr/bin/env python3
"""Generate the Elijah Ting open-ring mark + favicon set.

The mark is a crescent-thickness ring: an outer circle with an inner
circle offset upward subtracted from it. That yields a ring that is thick
at the bottom, tapers to fine points near the top, and leaves a small
opening at the top (the "open ring").
"""
import math
from PIL import Image, ImageDraw

# Brand palette (matches site CSS)
BROWN = (14, 13, 11, 255)     # --bg #0E0D0B
CREAM = (240, 233, 218, 255)  # warm cream wordmark color
BLACK = (26, 24, 19, 255)     # near-black ink for light backgrounds

SS = 2000  # supersample working canvas


def ring_mask(rc_frac=0.40, w_frac=0.078, gap_deg=27.0, rot_deg=8.0,
              taper=0.12, weight_amp=0.13, weight_phase=190.0, margin=0.0):
    """Open-ring (enso) mask as a tapered circular-arc stroke.

    Drawn as a filled band along a circle of radius `rc_frac*SS`, spanning
    360-gap_deg degrees with a `gap_deg` opening centred at top. The half
    width tapers to a point at both ends (`taper` = fraction of the arc over
    which it eases in) and carries a gentle low-frequency weight variation
    (`weight_amp`) so one flank reads heavier, like a brush stroke.
    """
    m = Image.new("L", (SS, SS), 0)
    d = ImageDraw.Draw(m)
    cx = cy = SS / 2
    Rc = SS * rc_frac
    w_max = SS * w_frac

    span = 360.0 - gap_deg
    n = 400

    def pt(theta_from_top_deg, radius):
        a = math.radians(theta_from_top_deg + rot_deg)
        return (cx + radius * math.sin(a), cy - radius * math.cos(a))

    def half_w(t):
        # taper to a point within `taper` of each end
        edge = min(t / taper, (1 - t) / taper, 1.0)
        edge = max(edge, 0.0)
        # ease the taper (smoothstep) for soft brush tips
        edge = edge * edge * (3 - 2 * edge)
        theta = (gap_deg / 2) + t * span
        wob = 1 + weight_amp * math.cos(math.radians(theta - weight_phase))
        return w_max * edge * wob

    outer, inner = [], []
    for i in range(n + 1):
        t = i / n
        theta = (gap_deg / 2) + t * span
        hw = half_w(t)
        outer.append(pt(theta, Rc + hw))
        inner.append(pt(theta, Rc - hw))
    poly = outer + inner[::-1]
    d.polygon(poly, fill=255)
    return m


def colorize(mask, color):
    """RGBA image: `color` where mask, transparent elsewhere."""
    img = Image.new("RGBA", mask.size, (color[0], color[1], color[2], 0))
    solid = Image.new("RGBA", mask.size, color)
    img.paste(solid, (0, 0), mask)
    return img


def rounded_rect_bg(size, color, radius_frac=0.22):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rad = int(size * radius_frac)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=rad, fill=color)
    return img


def resize(img, size):
    return img.resize((size, size), Image.LANCZOS)


def favicon_tile(size, pad_frac=0.16, rounded=True):
    """Cream ring on a brown square at `size`px.

    rounded=True gives a rounded-corner tile on transparent (nice in
    browser tabs); rounded=False gives a full-bleed opaque square (correct
    for apple-touch / android-chrome, which apply their own masking).
    """
    if rounded:
        bg = rounded_rect_bg(SS, BROWN)
    else:
        bg = Image.new("RGBA", (SS, SS), BROWN)
    ring = colorize(ring_mask(), CREAM)
    pad = int(SS * pad_frac)
    inner = resize(ring, SS - 2 * pad)
    bg.alpha_composite(inner, (pad, pad))
    return resize(bg, size)


def ring_png(size, color, pad_frac=0.04):
    ring = colorize(ring_mask(), color)
    pad = int(SS * pad_frac)
    inner = resize(ring, SS - 2 * pad)
    canvas = Image.new("RGBA", (SS, SS), (0, 0, 0, 0))
    canvas.alpha_composite(inner, (pad, pad))
    return resize(canvas, size)


def write_assets(root):
    import os
    fav = os.path.join(root, "assets", "favicons")
    img = os.path.join(root, "assets", "images")
    os.makedirs(fav, exist_ok=True)
    os.makedirs(img, exist_ok=True)

    # --- favicon set ---
    # browser-tab favicons: rounded tile on transparent
    rounded = favicon_tile(SS, rounded=True)
    for size, name in [(16, "favicon-16x16.png"), (32, "favicon-32x32.png")]:
        resize(rounded, size).save(os.path.join(fav, name))
    rounded.resize((48, 48), Image.LANCZOS).save(
        os.path.join(fav, "favicon.ico"),
        sizes=[(16, 16), (32, 32), (48, 48)])
    # home-screen icons: full-bleed opaque square (OS masks the corners)
    square = favicon_tile(SS, rounded=False)
    for size, name in [(180, "apple-touch-icon.png"),
                       (192, "android-chrome-192x192.png"),
                       (512, "android-chrome-512x512.png")]:
        resize(square, size).save(os.path.join(fav, name))

    # --- standalone ring marks (transparent) ---
    ring_png(1024, CREAM).save(os.path.join(img, "logo-ring-on-dark.png"))
    ring_png(1024, BLACK).save(os.path.join(img, "logo-ring-on-light.png"))
    # rounded brown app-tile at hi-res too (handy for social avatars)
    resize(favicon_tile(SS, rounded=True), 1024).save(
        os.path.join(img, "logo-ring-tile-1024.png"))
    print("assets written under", root)


def contact_sheet(path):
    sizes = [16, 32, 48, 64, 180]
    pad = 16
    w = sum(sizes) + pad * (len(sizes) + 1)
    sheet = Image.new("RGBA", (w, 220), (235, 235, 235, 255))
    x = pad
    for s in sizes:
        tile = resize(favicon_tile(SS), s)
        sheet.alpha_composite(tile, (x, 16))
        x += s + pad
    # big ring marks below
    sheet.alpha_composite(resize(ring_png(160, BLACK), 160), (pad, 16))
    sheet2 = Image.new("RGBA", (700, 360), (255, 255, 255, 255))
    sheet2.alpha_composite(resize(ring_png(330, BLACK), 330), (10, 14))
    dark = Image.new("RGBA", (340, 360), BROWN)
    dark.alpha_composite(resize(ring_png(330, CREAM), 330), (5, 14))
    sheet2.alpha_composite(dark, (355, 0))
    sheet.convert("RGB").save(path)
    sheet2.convert("RGB").save(path.replace(".png", "_rings.png"))
    print("wrote", path)


if __name__ == "__main__":
    import sys
    if "preview" in sys.argv:
        prev = Image.new("RGBA", (1080, 540), (255, 255, 255, 255))
        prev.alpha_composite(resize(ring_png(512, BLACK), 512), (8, 14))
        prev.alpha_composite(favicon_tile(512), (560, 14))
        prev.convert("RGB").save("/tmp/logo_preview.png")
        print("wrote /tmp/logo_preview.png")
    if "sheet" in sys.argv:
        contact_sheet("/tmp/contact.png")
    if "build" in sys.argv:
        import os
        write_assets(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
