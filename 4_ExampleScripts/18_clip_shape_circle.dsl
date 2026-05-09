begin_obj clipped_circle
  width: 200px;
  height: 200px;
  clip-shape: circle;  # Clip to circle inscribed in bounding box
  # Draw content that extends beyond clip bounds
  square(color=green, fill=green, pos=(0,0), width=200px, height=200px);
  circle(color=yellow, fill=yellow, center=(100,100), radius=60);
end_obj

begin_frame clip_shape_circle
  image width=400px; height=300px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  # Place the clipped object
  clipped_circle(pos=(100,50));

  # Add label
  font(font-family="Arial", font-size=16px, color=black, text="Circular Clipping", pos=(120,280));
end_frame