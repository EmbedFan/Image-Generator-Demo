# 04_simple_polygon.dsl
# Category 1 - Basic Primitives
# Demonstrates: polygon primitive — triangles, quadrilaterals, pentagons, and stroke-only polygons
# The path automatically closes from the last point back to the first.

begin_frame simple_polygon
  image width=680px; height=420px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  # --- Section header ---
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Triangles", pos=(20, 20));

  # Equilateral-like triangle, filled orange
  polygon(color=black, fill=orange,
          points=[(110, 40), (200, 160), (20, 160)]);

  # Right triangle, filled green
  polygon(color=darkgray, fill=lime, line-width=2px,
          points=[(250, 40), (390, 160), (250, 160)]);

  # Stroke-only triangle, dashed border
  polygon(color=red, fill=none, line-width=2px, line-type=dashed,
          points=[(440, 40), (560, 40), (560, 160)]);

  # --- Section header ---
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Quadrilaterals", pos=(20, 195));

  # Parallelogram
  polygon(color=navy, fill=lightblue, line-width=2px,
          points=[(40, 220), (200, 220), (170, 320), (10, 320)]);

  # Trapezoid
  polygon(color=purple, fill=RGBA(128,0,200,0.4), line-width=2px,
          points=[(250, 220), (430, 220), (400, 320), (280, 320)]);

  # Diamond (rotated square)
  polygon(color=black, fill=gold, line-width=1px,
          points=[(580, 220), (640, 270), (580, 320), (520, 270)]);

  # --- Section header ---
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Five and six sides", pos=(20, 355));

  # Pentagon (5 vertices, approximated)
  polygon(color=black, fill=tomato, line-width=2px,
          points=[(110, 380), (170, 370), (190, 420), (30, 420), (50, 370)]);

  # Hexagon (6 vertices, elongated)
  polygon(color=teal, fill=RGBA(0,128,128,0.35), line-width=2px,
          points=[(280, 365), (360, 365), (400, 395), (360, 420), (280, 420), (240, 395)]);

  # Star-like polygon (stroke only, dotted)
  polygon(color=red, fill=none, line-width=2px, line-type=dotted,
          points=[(530, 360), (560, 415), (490, 375), (570, 375), (500, 415)]);

end_frame
