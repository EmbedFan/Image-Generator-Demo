begin_palette palette
  heading = #2E4057
  body    = #4E5D6C
  accent  = #E74C3C
  highlight = #F1C40F
  bg      = #F8F9FA
end_palette

begin_frame text_palette
  image width=680px; height=380px; colorspace=RGB; dpi=96; output-format=png;
  background(color=@bg);
  font(color=@heading, font-size=32px, weight=bold, text="Palette Text Styles", pos=(40,70));
  font(color=@body, font-size=18px, text="Use named colors for headings, body text, and highlights.", pos=(40,120));
  font(color=@accent, font-size=18px, text="Accent color draws attention.", pos=(40,160));
  square(color=@accent, fill=@highlight, pos=(40,220), width=220px, height=110px);
  font(color=@bg, font-size=16px, text="The overlay box uses palette colors.", pos=(55,260));
end_frame