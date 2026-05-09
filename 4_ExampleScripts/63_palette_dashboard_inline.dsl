begin_palette dashboard_theme
  panel      = #34495E
  panel_fill = #5D6D7E
  accent     = #F7DC6F
  text       = #1B2631
  bg         = #F2F4F4
end_palette

begin_frame dashboard_inline
  image width=800px; height=450px; colorspace=RGB; dpi=96; output-format=png;
  background(color=@bg);
  square(color=@panel, fill=@panel_fill, pos=(40,60), width=220px, height=140px);
  square(color=@panel, fill=@panel_fill, pos=(300,60), width=220px, height=140px);
  square(color=@panel, fill=@panel_fill, pos=(560,60), width=220px, height=140px);
  circle(color=@accent, fill=@accent, center=(160,270), radius=40);
  circle(color=@accent, fill=none, center=(420,270), radius=40, line-width=10px);
  circle(color=@accent, fill=@accent, center=(680,270), radius=40);
  font(color=@text, font-size=24px, text="Dashboard Palette Inline", pos=(40,30));
  font(color=@text, font-size=16px, text="Panel colors and accents use aliases", pos=(40,210));
end_frame