begin_palette ui_theme
  bg         = #F4F6F7
  panel      = #1F618D
  panel_fill = #5499C7
  button     = #F4D03F
  text       = #17202A
end_palette

begin_frame ui_theme_example
  image width=760px; height=420px; colorspace=RGB; dpi=96; output-format=png;
  background(color=@bg);
  square(color=@panel, fill=@panel_fill, pos=(60,80), width=240px, height=260px);
  square(color=@button, fill=@button, pos=(340,120), width=240px, height=80px, line-width=4px);
  font(color=@text, font-size=22px, text="UI Theme Palette", pos=(60,40));
  font(color=@text, font-size=16px, text="Panel and button colors come from the same palette.", pos=(60,360));
end_frame