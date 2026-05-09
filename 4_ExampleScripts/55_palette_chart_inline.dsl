begin_palette palette
  axis      = #4A4A4A
  bar1      = #27AE60
  bar2      = #F39C12
  bar3      = #8E44AD
  label     = #2C3E50
end_palette

begin_frame chart_inline
  image width=760px; height=420px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);
  line(color=@axis, line-width=2px, start=(80,340), end=(680,340));
  line(color=@axis, line-width=2px, start=(80,80), end=(80,340));
  square(color=@bar1, fill=@bar1, pos=(140,240), width=100px, height=100px);
  square(color=@bar2, fill=@bar2, pos=(300,180), width=100px, height=160px);
  square(color=@bar3, fill=@bar3, pos=(460,120), width=100px, height=220px);
  font(color=@label, font-size=18px, text="Palette Bar Chart", pos=(80,40));
  font(color=@label, font-size=14px, text="Q1", pos=(170,360));
  font(color=@label, font-size=14px, text="Q2", pos=(330,360));
  font(color=@label, font-size=14px, text="Q3", pos=(490,360));
end_frame