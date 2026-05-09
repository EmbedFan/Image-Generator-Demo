include "lib/icon_palette.dsl"

begin_obj icon_shape
  circle(color=@icon_border, fill=@icon_fill, center=center, radius=radius, line-width=1);
end_obj

begin_frame icon_library_include
  image width=720px; height=420px; colorspace=RGB; dpi=96; output-format=png;
  background(color=@bg);
  icon_shape(center=(180,210), radius=60);
  icon_shape(center=(360,210), radius=60);
  icon_shape(center=(540,210), radius=60);
  font(color=@text, font-size=22px, text="Icon Library Include", pos=(40,40));
end_frame