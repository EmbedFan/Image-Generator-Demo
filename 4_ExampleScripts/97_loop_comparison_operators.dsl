# 97_loop_comparison_operators.dsl
# Demonstrates: all supported comparison operators.

begin_frame loop_comparison_operators
  image width=680px; height=260px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  var i, x;

  i = 0;
  x = 25;
  do
    square(pos=(x, 25), width=26, height=26, color=black, fill=lightblue);
    i = i + 1;
    x = x + 34;
  while i < 4;

  i = 0;
  x = 25;
  do
    circle(color=black, fill=lightgreen, center=(x + 13, 95), radius=13);
    i = i + 1;
    x = x + 34;
  while i <= 3;

  i = 4;
  x = 25;
  do
    square(pos=(x, 140), width=26, height=26, color=black, fill=lightyellow);
    i = i - 1;
    x = x + 34;
  while i > 0;

  i = 4;
  x = 25;
  do
    circle(color=black, fill=lightpink, center=(x + 13, 210), radius=13);
    i = i - 1;
    x = x + 34;
  while i >= 1;

  i = 0;
  x = 265;
  do
    square(pos=(x, 25), width=26, height=26, color=black, fill=plum);
    i = i + 1;
    x = x + 34;
  while i == 4;

  i = 0;
  x = 265;
  do
    circle(color=black, fill=lightsalmon, center=(x + 13, 95), radius=13);
    i = i + 1;
    x = x + 34;
  while i != 4;
end_frame
