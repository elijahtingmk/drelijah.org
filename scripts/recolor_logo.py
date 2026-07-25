#!/usr/bin/env python3
import os
import math
from PIL import Image

def process_logo():
    # Paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(root, "assets", "images", "logo-wordmark-on-dark.png")
    
    if not os.path.exists(img_path):
        print(f"Error: Original logo not found at {img_path}")
        return
        
    # Open original image
    src = Image.open(img_path).convert("RGB")
    W, H = src.size
    
    # Background color of logo-wordmark-on-dark.png
    bg_color = (13, 14, 9) # Hex #0D0E09 / #0E0D0B
    
    # Create new canvases
    canvas_dark = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas_light = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    
    # Brand Colors
    BLACK = (26, 24, 19, 255) # Near-black ink for light backgrounds
    
    # We will uncomposite the foreground from the background
    # C = a * F + (1 - a) * C_bg
    # -> a = (C - C_bg) / (F - C_bg)
    # We can estimate a based on color distance from the background.
    for x in range(W):
        for y in range(H):
            r, g, b = src.getpixel((x, y))
            
            # Compute distance from background
            diff_r = r - bg_color[0]
            diff_g = g - bg_color[1]
            diff_b = b - bg_color[2]
            dist = math.sqrt(diff_r*diff_r + diff_g*diff_g + diff_b*diff_b)
            
            # Thresholds for transparency mapping
            # Very close to background -> completely transparent
            # Further away -> opaque or semi-transparent
            low_thresh = 4.0
            high_thresh = 35.0
            
            if dist <= low_thresh:
                alpha = 0
            elif dist >= high_thresh:
                alpha = 255
            else:
                alpha = int(255 * (dist - low_thresh) / (high_thresh - low_thresh))
                
            if alpha > 0:
                # Uncomposite foreground color
                # F = (C - (1 - a) * C_bg) / a
                a_frac = alpha / 255.0
                fr = int(max(0, min(255, (r - (1.0 - a_frac) * bg_color[0]) / a_frac)))
                fg = int(max(0, min(255, (g - (1.0 - a_frac) * bg_color[1]) / a_frac)))
                fb = int(max(0, min(255, (b - (1.0 - a_frac) * bg_color[2]) / a_frac)))
                
                # Dark background version: keep original uncomposited foreground colors
                canvas_dark.putpixel((x, y), (fr, fg, fb, alpha))
                
                # Light background version:
                if x < 320:
                    # Keep the gold/bronze infinity loop as is, but uncomposited
                    canvas_light.putpixel((x, y), (fr, fg, fb, alpha))
                else:
                    # It's text!
                    # Distinguish between main name (cream/off-white) and subtitle (gold/terracotta)
                    # Cream text is very bright with very low saturation.
                    # Subtitle is gold/bronze which is more saturated.
                    brightness = (fr + fg + fb) / 3.0
                    saturation = max(fr, fg, fb) - min(fr, fg, fb)
                    
                    if brightness > 180 and saturation < 30:
                        # Recolor "Dr. Elijah Ting" (cream) to brand BLACK
                        canvas_light.putpixel((x, y), (BLACK[0], BLACK[1], BLACK[2], alpha))
                    else:
                        # Keep subtitle (gold/bronze) as is, or slightly darken for readability on light bg
                        # Gold on white is elegant, but let's make it a tiny bit richer/darker
                        d_fr = int(fr * 0.9)
                        d_fg = int(fg * 0.8)
                        d_fb = int(fb * 0.7)
                        canvas_light.putpixel((x, y), (d_fr, d_fg, d_fb, alpha))
            else:
                canvas_dark.putpixel((x, y), (0, 0, 0, 0))
                canvas_light.putpixel((x, y), (0, 0, 0, 0))
                
    # Save the output images
    out_dark = os.path.join(root, "assets", "images", "logo-wordmark-on-dark-transparent.png")
    out_light = os.path.join(root, "assets", "images", "logo-wordmark-on-light-transparent.png")
    
    canvas_dark.save(out_dark, "PNG")
    canvas_light.save(out_light, "PNG")
    
    print(f"Success! Generated transparent logos:")
    print(f"  Dark theme logo: {out_dark}")
    print(f"  Light theme logo: {out_light}")

if __name__ == "__main__":
    process_logo()
