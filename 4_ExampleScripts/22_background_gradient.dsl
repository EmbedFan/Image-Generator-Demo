begin_frame background_gradient
  image width=400px; height=300px; colorspace=RGB; dpi=96; output-format=png;
  background(color1=white, color2=navy, start=(0,0), end=(400,300));

  # Draw some primitives on the gradient background
  circle(color=yellow, fill=yellow, center=(100,100), radius=40);
  square(color=orange, fill=orange, pos=(200,150), width=80px, height=80px);

  # Add label
  font(font-family="Arial", font-size=18px, color=white, text="Gradient Background", pos=(100,250));
end_frame