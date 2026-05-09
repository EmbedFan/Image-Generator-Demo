# ------------------------------------------------------------
# File: 31_function_nested_calls.dsl
# Purpose:
#   Demonstrates nested function calls.
#   One function (labeled_box) draws a box with text.
#   Another function (connect_boxes) draws two boxes and connects them.
#   Shows how functions can call other functions to build complex drawings.
# ------------------------------------------------------------

# ------------------------------------------------------------
# Function: labeled_box
# Draws a rectangle with centered text
# Parameters:
#   x, y        -> top-left position
#   w, h        -> width and height
#   label_text  -> text inside the box
# ------------------------------------------------------------
begin_func labeled_box(x, y, w, h, label_text)

  # Draw box
  square(
    color=black,
    line-width=1px,
    fill=RGB(220,235,255),
    pos=(x, y),
    width=w,
    height=h
  )

  # Draw centered text (approximate centering)
  font(
    font-family="Arial",
    font-size=12px,
    color=black,
    align=center,
    text=label_text,
    pos=(x + w / 2, y + h / 2)
  )

end_func

# ------------------------------------------------------------
# Function: connect_boxes
# Calls labeled_box twice and connects them
# Parameters:
#   x1, y1  -> first box position
#   x2, y2  -> second box position
# ------------------------------------------------------------
begin_func connect_boxes(x1, y1, x2, y2)

  # Draw first box
  labeled_box(x1, y1, 120, 60, "Box A")

  # Draw second box
  labeled_box(x2, y2, 120, 60, "Box B")

  # Draw connector between centers of the boxes
  connector(
    color=black,
    line-width=2px,
    start=(x1 + 60, y1 + 30),
    end=(x2 + 60, y2 + 30),
    end-cap=triangle
  )

end_func

# ------------------------------------------------------------
# Frame demonstrating nested function calls
# ------------------------------------------------------------
begin_frame function_nested_calls_example
  image width=700px; height=300px; colorspace=RGB; dpi=96; output-format=png

  background(color=white)

  # First pair of connected boxes
  connect_boxes(50, 120, 250, 120)

  # Second pair with different positions
  connect_boxes(350, 50, 550, 180)

end_frame