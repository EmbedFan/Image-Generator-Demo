begin_palette icon_palette
  icon_primary = #1ABC9C
  icon_secondary = #16A085
  icon_accent = #F39C12
  bg = #FCFCFC
  strokes = #34495E
end_palette

begin_frame icon_set
  image width=680px; height=420px; colorspace=RGB; dpi=300; output-format=png;
  background(color=@bg);
  circle(color=@strokes, fill=@icon_primary, center=(140,140), radius=60);
  square(color=@strokes, fill=@icon_secondary, pos=(270,80), width=120px, height=120px);
  polygon(color=@strokes, fill=@icon_accent, points=[(520,80),(600,200),(440,200)]);
  font(color=@strokes, font-size=20px, text="Palette Icon Set", pos=(40,360));
end_frame