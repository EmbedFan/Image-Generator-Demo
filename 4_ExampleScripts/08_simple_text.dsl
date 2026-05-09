# 08_simple_text.dsl
# Category 1 - Basic Primitives
# Demonstrates: font primitive — sizes, weights, styles, alignments, colors, and multi-line text

begin_frame simple_text
  image width=680px; height=520px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  # ============================================================
  # Section 1: Font sizes
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Font sizes", pos=(20, 22));

  font(font-family="Arial", font-size=10px, color=black, text="10px — small caption",  pos=(20, 45));
  font(font-family="Arial", font-size=14px, color=black, text="14px — body text",       pos=(20, 65));
  font(font-family="Arial", font-size=20px, color=black, text="20px — subheading",      pos=(20, 92));
  font(font-family="Arial", font-size=28px, color=black, text="28px — heading",         pos=(20, 127));
  font(font-family="Arial", font-size=40px, color=black, text="40px — display",         pos=(20, 178));

  # ============================================================
  # Section 2: Weight and style
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Weight and style", pos=(20, 235));

  font(font-family="Arial", font-size=18px, color=black, weight=normal, style=normal,
       text="normal weight, normal style", pos=(20, 258));
  font(font-family="Arial", font-size=18px, color=black, weight=bold,   style=normal,
       text="bold weight, normal style",   pos=(20, 282));
  font(font-family="Arial", font-size=18px, color=black, weight=normal, style=italic,
       text="normal weight, italic style", pos=(20, 306));
  font(font-family="Arial", font-size=18px, color=black, weight=bold,   style=italic,
       text="bold weight, italic style",   pos=(20, 330));

  # ============================================================
  # Section 3: Text color
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Colors", pos=(20, 365));

  font(font-family="Arial", font-size=16px, color=red,     text="red text",      pos=(20, 387));
  font(font-family="Arial", font-size=16px, color=blue,    text="blue text",     pos=(130, 387));
  font(font-family="Arial", font-size=16px, color=green,   text="green text",    pos=(240, 387));
  font(font-family="Arial", font-size=16px, color=#FF6600, text="#FF6600 text",  pos=(365, 387));
  font(font-family="Arial", font-size=16px, color=RGBA(128,0,128,0.7),
       text="RGBA purple 70%", pos=(520, 387));

  # ============================================================
  # Section 4: Alignment (left / center / right)
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Alignment", pos=(20, 415));

  # Vertical guide line at x=340 to show anchor point for all three
  line(color=lightgray, line-type=dashed, line-width=1px, start=(340, 430), end=(340, 510));

  font(font-family="Arial", font-size=16px, color=navy, align=left,
       text="align=left",   pos=(340, 450));
  font(font-family="Arial", font-size=16px, color=navy, align=center,
       text="align=center", pos=(340, 474));
  font(font-family="Arial", font-size=16px, color=navy, align=right,
       text="align=right",  pos=(340, 498));

  # ============================================================
  # Section 5: Multi-line text
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Multi-line (\\n)", pos=(20, 415));

  font(font-family="Arial", font-size=14px, color=darkgray,
       text="Line one\nLine two\nLine three\nLine four", pos=(20, 440));

end_frame
