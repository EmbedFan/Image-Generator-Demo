# 09_simple_image.dsl
# Category 1 - Basic Primitives
# Demonstrates: image(src=...) drawing primitive — sizing, aspect-ratio, opacity, and rotate
#
# BEFORE RUNNING: place sample image files in the same directory as this script:
#   sample_wide.png    — a landscape-oriented image (e.g. 400x250 px)
#   sample_logo.png    — a small square logo        (e.g. 128x128 px)
#
# The engine supports PNG, JPEG, GIF, and SVG source files.

begin_frame simple_image
  image width=700px; height=520px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#F0F0F0);

  # ============================================================
  # Section 1: Natural size (no width/height) vs. explicit size
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Natural size vs. explicit size", pos=(20, 18));

  # Natural size — image rendered at its own pixel dimensions
  image(src="sample_logo.png", pos=(20, 35));
  font(font-family="Arial", font-size=11px, color=darkgray,
       text="natural size", pos=(20, 175));

  # Width only — height auto-scales to preserve aspect ratio
  image(src="sample_logo.png", pos=(170, 35), width=80px);
  font(font-family="Arial", font-size=11px, color=darkgray,
       text="width=80px\n(auto height)", pos=(170, 150));

  # Both width and height explicit (may stretch)
  image(src="sample_logo.png", pos=(300, 35), width=100px, height=60px);
  font(font-family="Arial", font-size=11px, color=darkgray,
       text="width=100 height=60\n(explicit, may stretch)", pos=(300, 110));

  # ============================================================
  # Section 2: Opacity
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Opacity (0.0 invisible -> 1.0 opaque)", pos=(20, 210));

  image(src="sample_wide.png", pos=(20,  230), width=140px, opacity=1.0);
  font(font-family="Arial", font-size=11px, color=darkgray, text="opacity=1.0", pos=(20, 310));

  image(src="sample_wide.png", pos=(180, 230), width=140px, opacity=0.6);
  font(font-family="Arial", font-size=11px, color=darkgray, text="opacity=0.6", pos=(180, 310));

  image(src="sample_wide.png", pos=(340, 230), width=140px, opacity=0.3);
  font(font-family="Arial", font-size=11px, color=darkgray, text="opacity=0.3", pos=(340, 310));

  image(src="sample_wide.png", pos=(500, 230), width=140px, opacity=0.1);
  font(font-family="Arial", font-size=11px, color=darkgray, text="opacity=0.1", pos=(500, 310));

  # ============================================================
  # Section 3: Rotation via transform
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Rotation (rotate= in degrees, no unit suffix)", pos=(20, 345));

  image(src="sample_logo.png", pos=(60,  380), width=80px, rotate=0);
  font(font-family="Arial", font-size=11px, color=darkgray,
       text="rotate=0",  pos=(55, 475));

  image(src="sample_logo.png", pos=(220, 380), width=80px, rotate=15);
  font(font-family="Arial", font-size=11px, color=darkgray,
       text="rotate=15", pos=(215, 475));

  image(src="sample_logo.png", pos=(380, 380), width=80px, rotate=45);
  font(font-family="Arial", font-size=11px, color=darkgray,
       text="rotate=45", pos=(375, 475));

  image(src="sample_logo.png", pos=(540, 380), width=80px, rotate=90);
  font(font-family="Arial", font-size=11px, color=darkgray,
       text="rotate=90", pos=(535, 475));

end_frame
