include "lib/colors.dsl"

begin_frame library_palette
  image width=720px; height=420px; colorspace=RGB; dpi=96; output-format=png;
  background(color=@bg);
  circle(color=@primary, fill=@secondary, center=(180,210), radius=100);
  square(color=@accent, fill=none, pos=(360,120), width=260px, height=190px, line-width=6px);
  font(color=@text, font-size=24px, text="Palette Library Include", pos=(40,60));
end_frame