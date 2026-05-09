begin_palette diagram_palette
  node_bg      = #E8DAEF
  node_border  = #8E44AD
  connector_clr= #5B2C6F
  accent       = #F5B041
  bg           = #FEF9E7
end_palette

begin_frame complex_diagram
  image width=820px; height=460px; colorspace=RGB; dpi=96; output-format=png;
  background(color=@bg);
  square(color=@node_border, fill=@node_bg, pos=(80,120), width=180px, height=120px);
  square(color=@node_border, fill=@node_bg, pos=(320,80), width=180px, height=120px);
  square(color=@node_border, fill=@node_bg, pos=(560,120), width=180px, height=120px);
  connector(color=@connector_clr, line-width=4px, start=(200,180), end=(320,140), end-cap=triangle);
  connector(color=@connector_clr, line-width=4px, start=(500,140), end=(560,180), end-cap=triangle);
  circle(color=@accent, fill=@accent, center=(410,180), radius=18);
  font(color=@node_border, font-size=18px, text="Data Source", pos=(100,160));
  font(color=@node_border, font-size=18px, text="Processor", pos=(340,120));
  font(color=@node_border, font-size=18px, text="Output", pos=(580,160));
  font(color=@connector_clr, font-size=22px, text="Palette Complex Diagram", pos=(80,40));
end_frame