# 01_simple_line.dsl
# Category 1 - Basic Primitives
# Demonstrates: line primitive with solid, dashed, dotted, and dash-dot styles
# Each line is drawn horizontally across the canvas at a different vertical position.

begin_frame simple_line
  image width=800px; height=600px; colorspace=RGB; dpi=600; output-format=png;
  background(color=white);

  # --- Label row ---
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="solid", pos=(20, 50));
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="dashed", pos=(20, 110));
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="dotted", pos=(20, 170));
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="dash-dot", pos=(20, 230));

  # --- Solid line (default style, black, 2px) ---
  line(color=black, line-type=solid, line-width=2px, start=(120, 45), end=(560, 45));

  # --- Dashed line (blue, 2px) ---
  line(color=blue, line-type=dashed, line-width=2px, start=(120, 105), end=(560, 105));

  # --- Dotted line (red, 2px) ---
  line(color=red, line-type=dotted, line-width=2px, start=(120, 165), end=(560, 165));

  # --- Dash-dot line (green, 3px, heavier weight for visibility) ---
  line(color=green, line-type=dash-dot, line-width=3px, start=(120, 225), end=(560, 225));

  # --- Extra: diagonal line showing direction freedom ---
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="diagonal", pos=(20, 290));
  line(color=purple, line-type=solid, line-width=2px, start=(120, 270), end=(560, 310));

end_frame
