begin_palette palette
  bg1      = #08632c
  bg2      = #1B79D8
  highlight = RGBA(255, 215, 0, 0.95)
  fill1    = #FFFFFF
  fill2    = #13940d
end_palette

begin_frame gradient_palette
  image width=700px; height=420px; colorspace=RGB; dpi=96; output-format=png;
  background(color1=@bg1, color2=@bg2, start=(0,0), end=(700,420));
  circle(color=@fill1, fill=@fill2, center=(210,210), radius=110);
  square(color=@highlight, fill=fill1, pos=(360,120), width=250px, height=180px, line-width=8px);
  font(color=@fill1, font-size=28px, text="Gradient + Palette", pos=(50,380));
end_frame