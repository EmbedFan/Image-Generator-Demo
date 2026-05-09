# Note: clip-shape=polygon is not supported by the DSL; showing square clipping instead
begin_obj clipped_square
  width: 200px;
  height: 200px;
  clip-shape: square;  # Clip to bounding box rectangle
  # Draw content that extends beyond clip bounds
  circle(color=purple, fill=purple, center=(50,50), radius=70);
  circle(color=orange, fill=orange, center=(150,150), radius=70);
end_obj

begin_frame clip_shape_polygon
  image width=400px; height=300px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  # Place the clipped object
  clipped_square(pos=(100,50));

  # Add label
  font(font-family="Arial", font-size=16px, color=black, text="Square Clipping (Polygon not supported)", pos=(80,280));
end_frame