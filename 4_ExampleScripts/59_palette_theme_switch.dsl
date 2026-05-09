begin_palette theme_palette
  primary   = #2E86C1
  secondary = #AED6F1
  accent    = #F5B041
  bg        = #EBF5FB
  text      = #1B4F72
end_palette

begin_frame theme_switch
  image width=720px; height=420px; colorspace=RGB; dpi=96; output-format=png;
  background(color=@bg);
  square(color=@primary, fill=@secondary, pos=(80,80), width=240px, height=240px);
  circle(color=@accent, fill=none, center=(520,210), radius=100, line-width=12px);
  font(color=@text, font-size=24px, text="Theme Switch Palette", pos=(80,360));
end_frame