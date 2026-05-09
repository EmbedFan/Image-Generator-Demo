# 02_simple_circle.dsl
# Category 1 - Basic Primitives
# Demonstrates: circle primitive — filled, stroke-only, custom line-width, and RGBA semi-transparent fill

begin_frame simple_circle
  image width=620px; height=340px; colorspace=RGBA; dpi=96; output-format=png;
  background(color=white);

  # --- Row labels ---
  font(font-family="Arial", font-size=13px, color=black, weight=bold,
       text="filled + border", pos=(10, 95));
  font(font-family="Arial", font-size=13px, color=black, weight=bold,
       text="stroke only", pos=(10, 195));
  font(font-family="Arial", font-size=13px, color=black, weight=bold,
       text="semi-transparent", pos=(10, 295));

  # === Row 1: circles with solid fill ===

  # Yellow fill, black border, default line-width
  circle(color=black, fill=yellow, center=(200, 80), radius=55);

  # Blue fill, navy border, thicker border
  circle(color=navy, fill=blue, center=(370, 80), radius=55, line-width=4px);

  # Red fill, no visible border (transparent stroke)
  circle(color=transparent, fill=red, center=(540, 80), radius=55);

  # === Row 2: stroke-only circles (fill=none) ===

  # Thin black outline
  circle(color=black, fill=none, center=(200, 180), radius=55, line-width=1px);

  # Thick blue outline
  circle(color=blue, fill=none, center=(370, 180), radius=55, line-width=5px);

  # Dashed red outline
  circle(color=red, fill=none, center=(540, 180), radius=55, line-width=2px,
         line-type=dashed);

  # === Row 3: semi-transparent fills using RGBA ===

  # 50% transparent green fill
  circle(color=black, fill=RGBA(0,200,0,0.5), center=(200, 280), radius=55);

  # Overlapping circles to show transparency interaction
  circle(color=black, fill=RGBA(255,0,0,0.5), center=(350, 280), radius=55);
  circle(color=black, fill=RGBA(0,0,255,0.5), center=(410, 280), radius=55);

  # Small circle inside a larger one
  circle(color=gray, fill=lightgray, center=(540, 280), radius=55);
  circle(color=black, fill=white, center=(540, 280), radius=25);

end_frame
