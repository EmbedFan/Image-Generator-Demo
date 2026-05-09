begin_obj clipped_combined
  width: 200px;
  height: 200px;
  clip-bounds: (25px,25px,175px,175px);  # Rectangular clip
  clip-shape: circle;  # Circular clip - intersection of both
  # Draw content that extends beyond clip bounds
  square(color=cyan, fill=cyan, pos=(0,0), width=200px, height=200px);
  polygon(color=magenta, fill=magenta, points=[(50,50),(150,50),(150,150),(50,150)]);
end_obj

begin_frame clip_combined
  image width=400px; height=300px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  # Place the clipped object
  clipped_combined(pos=(100,50));

  # Add label
  font(font-family="Arial", font-size=16px, color=black, text="Combined Clipping (Bounds + Shape)", pos=(70,280));
end_frame