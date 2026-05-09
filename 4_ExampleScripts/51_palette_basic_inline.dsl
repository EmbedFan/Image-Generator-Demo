begin_palette palette
  primary   = #1F77B4
  secondary = #FF7F0E
  accent    = #2CA02C
  bg        = #F7F7F7
  outline   = #4C4C4C
end_palette

begin_frame basic_palette
  image width=640px; height=360px; colorspace=RGB; dpi=96; output-format=png;
  background(color=@bg);
  square(color=@outline, fill=@primary, pos=(40,40), width=220px, height=120px);
  circle(color=@secondary, fill=@accent, center=(420,100), radius=60);
  line(color=@outline, line-width=4px, start=(40,200), end=(600,200));
  font(color=@outline, font-size=20px, text="Basic Palette Inline", pos=(40,260));
end_frame
