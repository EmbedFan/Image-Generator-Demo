# ------------------------------------------------------------
# File: 30_function_parametric_drawing.dsl
# Purpose:
#   Demonstrates a function with calculated (parametric) positions.
#   The function draws a horizontal sequence of circles using
#   arithmetic expressions based on input parameters.
# ------------------------------------------------------------

# ------------------------------------------------------------
# Function definition
# Parameters:
#   start_x   -> starting X position
#   y         -> Y position for all circles
#   count     -> number of circles
#   gap       -> spacing between circles
#   radius    -> circle radius
# ------------------------------------------------------------
begin_func circle_row(start_x, y, count, gap, radius)

  # Draw circles using calculated positions
  # Each circle position is computed using arithmetic expressions
  circle(color=black, line-width=1px, fill=RGB(200,220,255),
         center=(start_x + 0 * gap, y), radius=radius)

  circle(color=black, line-width=1px, fill=RGB(200,220,255),
         center=(start_x + 1 * gap, y), radius=radius)

  circle(color=black, line-width=1px, fill=RGB(200,220,255),
         center=(start_x + 2 * gap, y), radius=radius)

  circle(color=black, line-width=1px, fill=RGB(200,220,255),
         center=(start_x + 3 * gap, y), radius=radius)

  circle(color=black, line-width=1px, fill=RGB(200,220,255),
         center=(start_x + 4 * gap, y), radius=radius)

end_func

# ------------------------------------------------------------
# Frame demonstrating parametric function usage
# ------------------------------------------------------------
begin_frame function_parametric_example
  image width=600px; height=250px; colorspace=RGB; dpi=96; output-format=png

  background(color=RGB(245,245,245))

  # First row
  circle_row(80, 80, 5, 80, 25)

  # Second row with different parameters
  circle_row(50, 160, 8, 60, 20)

end_frame