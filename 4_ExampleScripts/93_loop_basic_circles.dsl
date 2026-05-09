# 93_loop_basic_circles.dsl
# Demonstrates: basic do ... while loop in a frame body.

begin_frame loop_basic_circles
  image width=320px; height=160px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  var i;
  i = 0;

  do
    circle(color=black, fill=lightblue, center=(40 + i * 50, 80), radius=14);
    i = i + 1;
  while i < 5;
end_frame
