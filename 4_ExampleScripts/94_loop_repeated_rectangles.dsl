# 94_loop_repeated_rectangles.dsl
# Demonstrates: repeated rectangles with changing position.

begin_frame loop_repeated_rectangles
  image width=420px; height=180px; colorspace=RGB; dpi=96; output-format=png;
  background(color=whitesmoke);

  var x;
  x = 25;

  do
    square(pos=(x, 45), width=36, height=90, color=navy, fill=lightgreen, line-width=2px);
    x = x + 55;
  while x <= 300;
end_frame
