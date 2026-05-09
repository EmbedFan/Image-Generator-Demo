# 96_loop_in_function.dsl
# Demonstrates: do ... while loop inside begin_func / end_func body.

begin_func dot_row(start_x, y)
  var i;
  i = 0;

  do
    circle(color=black, fill=red, center=(start_x + i * 28, y), radius=9);
    i = i + 1;
  while i < 6;
end_func

begin_frame loop_in_function
  image width=280px; height=140px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  dot_row(50, 70);
end_frame
