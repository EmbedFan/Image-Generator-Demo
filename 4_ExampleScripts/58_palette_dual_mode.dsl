include "58_palette_dual_mode/lib/extra_colors.dsl"

begin_palette local_palette
  highlight = #FF6F61
  note      = #2F4F4F
end_palette

begin_frame dual_palette
  image width=700px; height=420px; colorspace=RGB; dpi=96; output-format=png;
  background(color=@bg);
  square(color=@secondary, fill=@primary, pos=(80,80), width=220px, height=220px);
  circle(color=@highlight, fill=@note, center=(500,210), radius=100);
  font(color=@text, font-size=20px, text="Dual Palette Mode", pos=(80,340));
end_frame