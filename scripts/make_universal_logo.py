#!/usr/bin/env python3
import os
from PIL import Image, ImageFilter

def make_universal_logo():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dark_transparent_path = os.path.join(root, "assets", "images", "logo-wordmark-on-dark-transparent.png")
    
    if not os.path.exists(dark_transparent_path):
        print("Please run scripts/recolor_logo.py first to generate logo-wordmark-on-dark-transparent.png")
        return
        
    # Open the transparent dark logo (cream text + gold ring)
    logo = Image.open(dark_transparent_path).convert("RGBA")
    W, H = logo.size
    
    # To create a soft universal halo/shadow:
    # 1. Extract the alpha channel
    alpha = logo.split()[-1]
    
    # 2. Blur the alpha channel to create a soft glow mask
    # We will use a moderate radius so it looks like a high-end subtle shadow
    blur_radius = 8
    blurred_alpha = alpha.filter(ImageFilter.GaussianBlur(blur_radius))
    
    # 3. Create a solid dark background image matching the brand near-black
    # We use a very dark brown/black color with a slight transparency for the shadow
    shadow_color = (14, 13, 11, 220) # #0E0D0B with high opacity
    shadow_img = Image.new("RGBA", (W, H), shadow_color)
    
    # 4. Apply the blurred alpha to the solid shadow image
    shadow_img.putalpha(blurred_alpha)
    
    # 5. Composite the original logo over the soft shadow
    final = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    final.alpha_composite(shadow_img)
    final.alpha_composite(logo)
    
    # Save the universal logo
    out_path = os.path.join(root, "assets", "images", "logo-wordmark-universal.png")
    final.save(out_path, "PNG")
    print(f"Success! Generated universal logo with dynamic contrast shadow: {out_path}")

if __name__ == "__main__":
    make_universal_logo()
