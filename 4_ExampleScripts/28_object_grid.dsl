
# ------------------------------------------------------------
# File: 28_object_grid.dsl
# Purpose:
#   Demonstrates creating a reusable object (tile) and arranging
#   multiple instances in a grid layout using object reuse.
#   This example shows manual grid placement (no variables/grid system),
#   emphasizing object instantiation and consistent spacing.
# ------------------------------------------------------------

# ------------------------------------------------------------
# Reusable tile object definition
# ------------------------------------------------------------
begin_obj tile
  width: 100px;
  height: 80px;
  background: RGB(240,240,255);
  border: solid 1px #888888;
  shadow: 2px 2px 4px RGBA(0,0,0,0.2);

  square(fill=background, color=black, pos=(0,0), width=width, height=height, line-width=2px, shadow=shadow);
  # Title text inside tile
  font(font-family="Arial", font-size=12px, color=black,
       weight=bold, text="Tile", pos=(10,20));

  # Decorative circle
  circle(color=#666666, line-width=1px, fill=RGB(180,200,255),
         center=(80,60), radius=10);
end_obj

# ------------------------------------------------------------
# Frame rendering a grid of tiles
# ------------------------------------------------------------
begin_frame object_grid_example
  image width=600px; height=400px; colorspace=RGB; dpi=96; output-format=png;

  # Background
  background(color=RGB(245,245,245));

  # ----------------------------------------------------------
  # Grid layout (3 rows x 4 columns)
  # Spacing: 20px horizontal, 20px vertical
  # Tile size: 100x80
  # ----------------------------------------------------------

  # Row 1
  tile(pos=(20,20));
  tile(pos=(140,20));
  tile(pos=(260,20));
  tile(pos=(380,20));

  # Row 2
  tile(pos=(20,120));
  tile(pos=(140,120));
  tile(pos=(260,120));
  tile(pos=(380,120));

  # Row 3
  tile(pos=(20,220));
  tile(pos=(140,220));
  tile(pos=(260,220));
  tile(pos=(380,220));

end_frame