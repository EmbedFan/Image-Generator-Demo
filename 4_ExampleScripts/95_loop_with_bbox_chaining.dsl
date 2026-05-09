# 95_loop_with_bbox_chaining.dsl
# Demonstrates: named primitive + bbox access inside a loop.

begin_frame loop_bbox_chaining
  image width=520px; height=170px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  var x, i;
  x = 20;
  i = 0;

  do
    box = square(pos=(x, 50), width=70, height=50, color=black, fill=lightyellow, line-width=2px);
    x = box.bbox.x + box.bbox.width + 18;
    i = i + 1;
  while i < 5;
end_frame
