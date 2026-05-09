begin_frame background_solid
  image width=400px; height=300px; colorspace=RGB; dpi=96; output-format=png;
  background(color=lightblue);

  # Draw some primitives on the solid background
  circle(color=red, fill=red, center=(100,100), radius=50);
  square(color=green, fill=green, pos=(200,50), width=100px, height=100px);

  # Add label
  font(font-family="Arial", font-size=18px, color=black, text="Solid Background", pos=(120,250));
end_frame