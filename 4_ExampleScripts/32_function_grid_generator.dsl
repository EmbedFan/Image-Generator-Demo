# ------------------------------------------------------------
# File: 32_function_grid_generator.dsl
# Purpose:
#   Demonstrates a function that generates a small grid pattern
#   using repeated function calls with calculated positions.
# ------------------------------------------------------------

begin_func tile_row(x, y, size, gap)
  square(color=#2C3E50, line-width=1px, fill=RGB(93,173,226),
         pos=(x + 0 * gap, y), width=size, height=size)
  square(color=#2C3E50, line-width=1px, fill=RGB(133,193,233),
         pos=(x + 1 * gap, y), width=size, height=size)
  square(color=#2C3E50, line-width=1px, fill=RGB(174,214,241),
         pos=(x + 2 * gap, y), width=size, height=size)
  square(color=#2C3E50, line-width=1px, fill=RGB(214,234,248),
         pos=(x + 3 * gap, y), width=size, height=size)
end_func

begin_frame function_grid_generator
  image width=640px; height=300px; colorspace=RGB; dpi=96; output-format=png
  background(color=#F8F9F9)

  font(color=#2C3E50, font-size=16px, weight=bold,
       text="Category 7: Function Grid Generator", pos=(20, 24))

  tile_row(40, 70, 46, 56)
  tile_row(40, 126, 46, 56)
  tile_row(40, 182, 46, 56)
  tile_row(40, 238, 46, 56)

  font(color=#566573, font-size=12px,
       text="A function can generate repeated layout patterns by combining",
       pos=(320, 120))
  font(color=#566573, font-size=12px,
       text="parameterized drawing with arithmetic expressions.",
       pos=(320, 138))
end_frame
