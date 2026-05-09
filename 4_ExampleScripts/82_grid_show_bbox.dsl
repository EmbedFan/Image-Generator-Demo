# 82_grid_show_bbox.dsl
# Category 15 — Grid System
# Demonstrates: show-bbox=true debug overlay.
# A dashed bounding-box outline is drawn around each primitive after rendering.
# Outline color is automatically chosen for contrast (black or white).
# Use show-bbox during layout design, then remove it before final output.

begin_obj info_card
  width: 150px; height: 90px;
  background: #3498DB;
  border: solid 1px #2980B9;
  shadow: 2px 2px 4px RGBA(0,0,0,0.2);
  font(color=white, font-size=13px, weight=bold,
       text="Card", pos=(10, 18));
  font(color=RGBA(255,255,255,0.8), font-size=10px,
       text="Object instance", pos=(10, 36));
end_obj

begin_frame grid_show_bbox
  image width=640px; height=360px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#F0F4F8);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 15: show-bbox=true Debug Overlay",
       pos=(15, 18));
  font(color=#7F8C8D, font-size=11px,
       text="Dashed outline shows the computed bounding box of each element.",
       pos=(15, 38));

  # ── Primitives with show-bbox=true ────────────────────────────────────

  # circle: bbox is a square enclosing the circle (diameter x diameter)
  circle(color=#2980B9, fill=#85C1E9,
         center=(90, 130), radius=45, show-bbox=true);
  font(color=#2C3E50, font-size=10px, align=center,
       text="circle", pos=(90, 195));

  # square: bbox is the rectangle itself
  square(color=#E74C3C, fill=#F1948A,
         pos=(175, 100), width=90px, height=60px, show-bbox=true);
  font(color=#2C3E50, font-size=10px, align=center,
       text="square", pos=(220, 175));

  # polygon: bbox spans from min to max vertex
  polygon(color=#27AE60, fill=#82E0AA,
          points=[(320,90),(390,90),(370,160),(340,160)],
          show-bbox=true);
  font(color=#2C3E50, font-size=10px, align=center,
       text="polygon", pos=(355, 178));

  # rotated square: bbox wraps the rotated element
  square(color=#8E44AD, fill=#D7BDE2,
         pos=(430, 95), width=70px, height=60px,
         rotate=30, show-bbox=true);
  font(color=#2C3E50, font-size=10px, align=center,
       text="square rotate=30", pos=(465, 185));

  # font: bbox wraps the text block
  font(color=#2C3E50, font-size=20px, weight=bold,
       text="Text Block",
       pos=(80, 240), show-bbox=true);

  # path: bbox spans all vertices
  path(color=#E67E22, line-width=3px,
       points=[(300,220),(360,260),(420,220),(480,255)],
       show-bbox=true);

  # arc: bbox is the full circle enclosing it
  arc(color=#16A085, line-width=3px,
      center=(560, 250), radius=40,
      start-angle=0, end-angle=270,
      show-bbox=true);

  # Object instance: bbox wraps the rendered object
  info_card(pos=(80, 295), show-bbox=true);
  font(color=#2C3E50, font-size=10px,
       text="object instance", pos=(80, 394));

  font(color=#E74C3C, font-size=11px,
       text="show-bbox is NOT valid on background() or grid() — validation error.",
       pos=(15, 340));
end_frame
