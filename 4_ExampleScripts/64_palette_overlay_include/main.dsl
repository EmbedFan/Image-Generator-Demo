include "lib/overlay_colors.dsl"

begin_frame overlay_include
  image width=720px; height=420px; colorspace=RGBA; dpi=96; output-format=png;
  background(color=@bg);
  square(color=@panel, fill=@panel, pos=(80,80), width=240px, height=180px, opacity=1.0);
  square(color=@overlay, fill=@overlay, pos=(180,140), width=240px, height=180px, opacity=0.65);
  circle(color=@accent, fill=@accent, center=(520,210), radius=80, opacity=0.9);
  font(color=@text, font-size=22px, text="Overlay Palette Include", pos=(80,320));
end_frame