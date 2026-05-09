# 10_color_formats.dsl
# Category 2 - Colors and Styling
# Demonstrates: all supported color formats — named, hex (#RRGGBB), RGB(), RGBA(), none, transparent
# Each swatch is a filled square with a label below it.

begin_frame color_formats
  image width=700px; height=520px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#F8F8F8);

  # ============================================================
  # Section 1: Named colors
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Named colors", pos=(20, 10));

  square(color=black, fill=red,       pos=(20,  30), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="red",       pos=(20, 90));

  square(color=black, fill=green,     pos=(110, 30), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="green",     pos=(110, 90));

  square(color=black, fill=blue,      pos=(200, 30), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="blue",      pos=(200, 90));

  square(color=black, fill=orange,    pos=(290, 30), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="orange",    pos=(290, 90));

  square(color=black, fill=purple,    pos=(380, 30), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="purple",    pos=(380, 90));

  square(color=black, fill=teal,      pos=(470, 30), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="teal",      pos=(470, 90));

  square(color=black, fill=gold,      pos=(560, 30), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="gold",      pos=(560, 90));

  # Extended CSS Color Level 3 named colors
  square(color=black, fill=tomato,        pos=(20,  110), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="tomato",        pos=(20,  170));

  square(color=black, fill=cornflowerblue, pos=(110, 110), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="cornflower\nblue", pos=(110, 170));

  square(color=black, fill=slategray,     pos=(200, 110), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="slategray",     pos=(200, 170));

  square(color=black, fill=lime,          pos=(290, 110), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="lime",          pos=(290, 170));

  square(color=black, fill=navy,          pos=(380, 110), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="navy",          pos=(380, 170));

  square(color=black, fill=silver,        pos=(470, 110), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="silver",        pos=(470, 170));

  square(color=black, fill=pink,          pos=(560, 110), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="pink",          pos=(560, 170));

  # ============================================================
  # Section 2: Hex colors (#RRGGBB — 6 digits only, no shorthand)
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Hex colors  #RRGGBB (6 digits only)", pos=(20, 196));

  square(color=black, fill=#FF0000, pos=(20,  215), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="#FF0000", pos=(20,  275));

  square(color=black, fill=#00FF00, pos=(110, 215), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="#00FF00", pos=(110, 275));

  square(color=black, fill=#0000FF, pos=(200, 215), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="#0000FF", pos=(200, 275));

  square(color=black, fill=#FF5733, pos=(290, 215), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="#FF5733", pos=(290, 275));

  square(color=black, fill=#28B463, pos=(380, 215), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="#28B463", pos=(380, 275));

  square(color=black, fill=#1A5276, pos=(470, 215), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="#1A5276", pos=(470, 275));

  square(color=black, fill=#F0F0F0, pos=(560, 215), width=70px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="#F0F0F0", pos=(560, 275));

  # ============================================================
  # Section 3: RGB() format
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="RGB(r, g, b)  — components 0-255", pos=(20, 292));

  square(color=black, fill=RGB(255, 0,   0),   pos=(20,  313), width=100px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="RGB(255,0,0)",   pos=(20,  373));

  square(color=black, fill=RGB(0,   180, 0),   pos=(140, 313), width=100px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="RGB(0,180,0)",   pos=(140, 373));

  square(color=black, fill=RGB(0,   0,   220), pos=(260, 313), width=100px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="RGB(0,0,220)",   pos=(260, 373));

  square(color=black, fill=RGB(200, 150, 80),  pos=(380, 313), width=100px, height=50px);
  font(font-family="Arial", font-size=11px, color=black, text="RGB(200,150,80)", pos=(380, 373));

  # ============================================================
  # Section 4: RGBA() format + fill=none + transparent
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="RGBA(r,g,b,a)  alpha 0.0-1.0 | fill=none | transparent", pos=(20, 391));

  # RGBA with varying alpha over a colored background
  square(color=transparent, fill=#FF6600, pos=(20, 413), width=660px, height=55px);

  square(color=black, fill=RGBA(0,0,200,1.0), pos=(30,  418), width=80px, height=40px);
  font(font-family="Arial", font-size=10px, color=white, text="alpha=1.0", pos=(35, 443));

  square(color=black, fill=RGBA(0,0,200,0.75), pos=(125, 418), width=80px, height=40px);
  font(font-family="Arial", font-size=10px, color=white, text="alpha=0.75", pos=(128, 443));

  square(color=black, fill=RGBA(0,0,200,0.5),  pos=(220, 418), width=80px, height=40px);
  font(font-family="Arial", font-size=10px, color=white, text="alpha=0.5",  pos=(226, 443));

  square(color=black, fill=RGBA(0,0,200,0.25), pos=(315, 418), width=80px, height=40px);
  font(font-family="Arial", font-size=10px, color=black, text="alpha=0.25", pos=(318, 443));

  # fill=none — no fill paint (stroke still visible)
  square(color=black, fill=none,        pos=(415, 418), width=80px, height=40px, line-width=2px);
  font(font-family="Arial", font-size=10px, color=black, text="fill=none",   pos=(420, 443));

  # transparent — same as RGBA(0,0,0,0), valid everywhere
  square(color=black, fill=transparent, pos=(510, 418), width=80px, height=40px, line-width=2px);
  font(font-family="Arial", font-size=10px, color=black, text="transparent", pos=(513, 443));

  # Section footer note
  font(font-family="Arial", font-size=11px, color=darkgray, style=italic,
       text="Note: fill=none is valid for fill/background only. Use transparent for stroke color when invisible stroke is needed.",
       pos=(20, 490));

end_frame
