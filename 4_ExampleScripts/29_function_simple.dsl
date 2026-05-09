# ------------------------------------------------------------
# File: 29_function_simple.dsl
# Purpose:
#   Demonstrates a basic function with parameters.
#   The function draws a labeled circular badge at a given position.
#   Shows how to reuse drawing logic with different arguments.
# ------------------------------------------------------------

# ------------------------------------------------------------
# Function definition
# Parameters:
#   x, y        -> center position of the badge
#   label_text  -> text displayed inside the badge
# ------------------------------------------------------------
begin_func badge(x, y, label_text)

  # Outer circle (badge border + fill)
  circle(
    color=black,
    line-width=2px,
    fill=RGB(220,235,255),
    center=(x, y),
    radius=30
  )

  # Inner text (slightly offset for visual centering)
  font(
    font-family="Arial",
    font-size=14px,
    color=black,
    weight=bold,
    align=center,
    text=label_text,
    pos=(x, y)
  )

end_func

# ------------------------------------------------------------
# Frame demonstrating multiple function calls
# ------------------------------------------------------------
begin_frame function_simple_example
  image width=500px; height=200px; colorspace=RGB; dpi=96; output-format=png

  background(color=white)

  # Call the function multiple times with different parameters
  badge(80, 100, "A")
  badge(200, 100, "B")
  badge(320, 100, "C")
  badge(440, 100, "D")

end_frame