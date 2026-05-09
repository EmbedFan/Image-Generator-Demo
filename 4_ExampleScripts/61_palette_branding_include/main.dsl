include "lib/branding_colors.dsl"

begin_frame branding_include
  image width=760px; height=420px; colorspace=RGB; dpi=96; output-format=png;
  background(color=@bg);
  square(color=@primary, fill=@secondary, pos=(80,80), width=280px, height=240px);
  circle(color=@accent, fill=none, center=(560,200), radius=100, line-width=12px);
  font(color=@text, font-size=26px, text="Branding Palette Include", pos=(80,40));
end_frame