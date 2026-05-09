# 98_loop_guard_error_example.dsl
# Negative example: this loop never updates i, so the guard must fire.

begin_frame loop_guard_error
  image width=180px; height=120px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  var i;
  i = 0;

  do
    circle(color=black, fill=red, center=(40, 40), radius=10);
  while i < 5;
end_frame
