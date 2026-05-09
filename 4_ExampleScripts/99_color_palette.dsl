# =========================================================
# AIM:
# Demonstrate palette-based coloring, transparency, and layout.
# - Four rectangles (squares) with different colors and opacity
# - Each rectangle contains a green triangle at its center
# - A central circle placed at the average center of the rectangles
# - All colors referenced via palette (@alias)
# =========================================================

# ---------------------------------------------------------
# Palette definition (ONLY color literals allowed here)
# ---------------------------------------------------------
begin_palette demo_colors
  bg          = RGB(245,245,245)
  rect1_fill  = RGBA(255,0,0,0.4)
  rect2_fill  = RGBA(0,255,0,0.5)
  rect3_fill  = RGBA(0,0,255,0.6)
  rect4_fill  = RGBA(255,165,0,0.7)
  rect_line   = RGB(50,50,50)
  triangle    = RGB(0,180,0)
  circle_fill = RGBA(120,0,120,0.75)
end_palette

# ---------------------------------------------------------
# Frame definition
# ---------------------------------------------------------
begin_frame palette_demo

  # Canvas setup
  image width=800px; height=800px; colorspace=RGBA; dpi=96; output-format=png;

  # Background color
  background(color=@bg);

  # -------------------------------------------------------
  # Base geometry
  # A = 100px (square size)
  # Gap = 2*A = 200px
  # Rectangle centers:
  # (200,200), (600,200), (200,600), (600,600)
  # Center of these = (400,400)
  # -------------------------------------------------------

  # -------------------------------------------------------
  # Rectangle 1 (top-left)
  # -------------------------------------------------------
  square(color=@rect_line, fill=@rect1_fill,
         pos=(150,150), width=100px, height=100px);

  # Triangle at rectangle center (200,200)
  polygon(color=@triangle, fill=@triangle,
          points=[(200,180),(220,220),(180,220)]);

  # -------------------------------------------------------
  # Rectangle 2 (top-right)
  # -------------------------------------------------------
  square(color=@rect_line, fill=@rect2_fill,
         pos=(550,150), width=100px, height=100px);

  # Triangle at rectangle center (600,200)
  polygon(color=@triangle, fill=@triangle,
          points=[(600,180),(620,220),(580,220)]);

  # -------------------------------------------------------
  # Rectangle 3 (bottom-left)
  # -------------------------------------------------------
  square(color=@rect_line, fill=@rect3_fill,
         pos=(150,550), width=100px, height=100px);

  # Triangle at rectangle center (200,600)
  polygon(color=@triangle, fill=@triangle,
          points=[(200,580),(220,620),(180,620)]);

  # -------------------------------------------------------
  # Rectangle 4 (bottom-right)
  # -------------------------------------------------------
  square(color=@rect_line, fill=@rect4_fill,
         pos=(550,550), width=100px, height=100px);

  # Triangle at rectangle center (600,600)
  polygon(color=@triangle, fill=@triangle,
          points=[(600,580),(620,620),(580,620)]);

  # -------------------------------------------------------
  # Central circle
  # Center = average of rectangle centers = (400,400)
  # -------------------------------------------------------
  circle(color=@rect_line, fill=@circle_fill,
         center=(400,400), radius=90px);

end_frame