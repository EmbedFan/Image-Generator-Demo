begin_frame background_image
  image width=400px; height=300px; colorspace=RGB; dpi=96; output-format=png;
  background(src="sample_logo.png", mode=fit);

  # Draw some primitives on the image background
  circle(color=red, center=(100,100), radius=30, line-width=3px);
  square(color=blue, pos=(250,50), width=60px, height=60px, line-width=3px);

  # Add label
  font(font-family="Arial", font-size=16px, color=black, text="Image Background (fit mode)", pos=(80,270));
end_frame