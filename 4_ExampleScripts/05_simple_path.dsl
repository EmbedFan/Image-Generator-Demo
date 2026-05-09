# 05_simple_path.dsl
# Category 1 - Basic Primitives
# Demonstrates: path primitive — open polylines with different shapes and styles
# path has stroke only; no fill is allowed.

begin_frame simple_path
  image width=640px; height=400px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  # --- Section header ---
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Open polylines (path)", pos=(20, 20));

  # Simple L-shape (two segments, right-angle turn)
  font(font-family="Arial", font-size=12px, color=darkgray,
       text="L-shape", pos=(20, 50));
  path(color=black, line-width=2px,
       points=[(20, 65), (20, 120), (160, 120)]);

  # Zigzag (alternating up/down)
  font(font-family="Arial", font-size=12px, color=darkgray,
       text="zigzag", pos=(200, 50));
  path(color=blue, line-width=2px,
       points=[(200, 120), (240, 65), (280, 120), (320, 65), (360, 120)]);

  # Smooth wave shape
  font(font-family="Arial", font-size=12px, color=darkgray,
       text="wave", pos=(400, 50));
  path(color=red, line-width=2px,
       points=[(400, 90), (430, 65), (460, 115), (490, 65), (520, 115), (560, 90)]);

  # --- Section header ---
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Line styles on paths", pos=(20, 160));

  # Dashed path
  font(font-family="Arial", font-size=12px, color=darkgray,
       text="dashed", pos=(20, 182));
  path(color=black, line-width=2px, line-type=dashed,
       points=[(20, 200), (80, 160), (160, 240), (240, 160), (320, 200)]);

  # Dotted path
  font(font-family="Arial", font-size=12px, color=darkgray,
       text="dotted", pos=(360, 182));
  path(color=navy, line-width=3px, line-type=dotted,
       points=[(360, 200), (420, 160), (500, 240), (580, 160), (620, 200)]);

  # --- Section header ---
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Multi-segment complex path", pos=(20, 270));

  # Staircase pattern (many right-angle segments)
  path(color=purple, line-width=3px,
       points=[(20, 310), (80, 310), (80, 340), (160, 340),
               (160, 310), (240, 310), (240, 380), (320, 380),
               (320, 310), (400, 310)]);

  # Irregular sketch-like path with varying directions
  path(color=orange, line-width=2px, line-type=dash-dot,
       points=[(430, 380), (480, 300), (520, 350), (560, 290), (600, 330), (630, 310)]);

end_frame
