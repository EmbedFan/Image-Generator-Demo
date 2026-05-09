# 89_colorspace_gray.dsl
# Category 17 — Colorspaces, Output Formats, and Units
# Demonstrates: colorspace=GRAY canvas.
# All color values are converted to single-channel luminance using
# CCIR 601 weighting: Y = 0.299*R + 0.587*G + 0.114*B
# Named colors, hex, RGB(), and RGBA() are all converted.
# Note: the alpha channel in RGBA() is discarded during GRAY conversion.

begin_frame colorspace_gray
  image width=620px; height=380px; colorspace=GRAY; dpi=96; output-format=png;
  background(color=white);

  font(color=black, font-size=15px, weight=bold,
       text="Category 17: colorspace=GRAY — CCIR 601 Luminance Conversion",
       pos=(15, 18));
  font(color=black, font-size=11px,
       text="Y = 0.299*R + 0.587*G + 0.114*B   (all colors converted to grayscale)",
       pos=(15, 38));

  # ── Named colors → their CCIR 601 luminance values ───────────────────
  # red:     Y ≈ 0.299 * 255 = 76 (dark gray)
  square(color=black, fill=red,    pos=(15,  70), width=80px, height=55px);
  font(color=black, font-size=10px, align=center,
       text="red", pos=(55, 135));
  font(color=black, font-size=9px, align=center,
       text="Y≈76 (dark)", pos=(55, 148));

  # green:   Y ≈ 0.587 * 255 = 150 (medium gray)
  square(color=black, fill=green,  pos=(105, 70), width=80px, height=55px);
  font(color=black, font-size=10px, align=center,
       text="green", pos=(145, 135));
  font(color=black, font-size=9px, align=center,
       text="Y≈150 (mid)", pos=(145, 148));

  # blue:    Y ≈ 0.114 * 255 = 29 (very dark)
  square(color=black, fill=blue,   pos=(195, 70), width=80px, height=55px);
  font(color=black, font-size=10px, align=center,
       text="blue", pos=(235, 135));
  font(color=black, font-size=9px, align=center,
       text="Y≈29 (darkest)", pos=(235, 148));

  # yellow:  Y = 0.299*255 + 0.587*255 ≈ 226 (very light)
  square(color=black, fill=yellow, pos=(285, 70), width=80px, height=55px);
  font(color=black, font-size=10px, align=center,
       text="yellow", pos=(325, 135));
  font(color=black, font-size=9px, align=center,
       text="Y≈226 (light)", pos=(325, 148));

  # white:   Y = 255 (pure white)
  square(color=black, fill=white,  pos=(375, 70), width=80px, height=55px);
  font(color=black, font-size=10px, align=center,
       text="white", pos=(415, 135));
  font(color=black, font-size=9px, align=center,
       text="Y=255", pos=(415, 148));

  # black:   Y = 0 (pure black)
  square(color=black, fill=black,  pos=(465, 70), width=80px, height=55px);
  font(color=black, font-size=10px, align=center,
       text="black", pos=(505, 135));
  font(color=black, font-size=9px, align=center,
       text="Y=0", pos=(505, 148));

  # ── Hex colors ────────────────────────────────────────────────────────
  font(color=black, font-size=12px, weight=bold,
       text="Hex colors — same CCIR 601 conversion:", pos=(15, 175));

  square(color=black, fill=#FF5733, pos=(15, 195), width=70px, height=50px);
  font(color=black, font-size=9px, align=center, text="#FF5733", pos=(50, 255));

  square(color=black, fill=#33FF57, pos=(95, 195), width=70px, height=50px);
  font(color=black, font-size=9px, align=center, text="#33FF57", pos=(130, 255));

  square(color=black, fill=#3357FF, pos=(175, 195), width=70px, height=50px);
  font(color=black, font-size=9px, align=center, text="#3357FF", pos=(210, 255));

  square(color=black, fill=#FF33A1, pos=(255, 195), width=70px, height=50px);
  font(color=black, font-size=9px, align=center, text="#FF33A1", pos=(290, 255));

  # ── RGB() and RGBA() ──────────────────────────────────────────────────
  font(color=black, font-size=12px, weight=bold,
       text="RGB() and RGBA() — alpha discarded in GRAY mode:", pos=(15, 278));

  square(color=black, fill=RGB(200,100,50), pos=(15, 298), width=90px, height=50px);
  font(color=black, font-size=9px, align=center,
       text="RGB(200,100,50)", pos=(60, 358));

  square(color=black, fill=RGBA(50,150,250,0.9), pos=(115, 298), width=90px, height=50px);
  font(color=black, font-size=9px, align=center,
       text="RGBA(50,150,250,0.9)", pos=(160, 358));
  font(color=black, font-size=9px, align=center,
       text="alpha discarded", pos=(160, 369));

  # Gradient background demo (gradient also converted to gray)
  square(color=black, fill=none, pos=(320, 275), width=280px, height=90px);
  font(color=black, font-size=10px, text="Gradient (color1=red, color2=blue):", pos=(325, 280));
  # Note: background is single; show gradient with a separate visual cue
  polygon(color=none, fill=RGB(200,50,50),
          points=[(325,300),(500,300),(500,360),(325,360)]);
  polygon(color=none, fill=RGB(50,50,200),
          points=[(500,300),(600,300),(600,360),(500,360)]);
  font(color=black, font-size=9px, align=center,
       text="red→blue gradient: different gray values", pos=(462, 372));
end_frame
