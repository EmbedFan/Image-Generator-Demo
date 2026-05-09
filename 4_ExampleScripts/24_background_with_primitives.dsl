begin_frame background_with_primitives
  image width=400px; height=300px; colorspace=RGB; dpi=96; output-format=png;
  background(color=lightgray);

  # Draw layered primitives on background
  square(color=blue, fill=blue, pos=(50,50), width=150px, height=150px);
  circle(color=red, fill=red, center=(200,125), radius=60);
  square(color=green, fill=green, pos=(200,100), width=100px, height=100px);

  # Add label
  font(font-family="Arial", font-size=16px, color=black, text="Primitives Layered on Background", pos=(50,270));
end_frame