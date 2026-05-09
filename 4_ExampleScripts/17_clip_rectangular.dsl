begin_obj clipped_content
  width: 200px;
  height: 200px;
  clip-bounds: (50px,50px,150px,150px);
  # Draw content that extends beyond clip bounds
  square(color=blue, fill=blue, pos=(20,20), width=160px, height=160px);
  circle(color=red, fill=red, center=(40,40), radius=80);
end_obj

begin_frame clip_rectangular
  image width=400px; height=300px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  # Place the clipped object
  clipped_content(pos=(100,50));

  # Add label
  font(font-family="Arial", font-size=16px, color=black, text="Rectangular Clipping", pos=(100,280));
end_frame