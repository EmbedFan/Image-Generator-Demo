# ------------------------------------------------------------
# File: 45_advanced_opacity.dsl
# Purpose:
#   Demonstrates transparent and semi-transparent elements
#   using RGBA fills and strokes.
# ------------------------------------------------------------

begin_frame advanced_opacity
  image width=760px; height=360px; colorspace=RGB; dpi=96; output-format=png
  background(color=#FDFEFE)

  font(color=#1F2D3A, font-size=18px, weight=bold,
       text="Category 11: Transparency with RGBA colors", pos=(24,26))

  square(color=#D5D8DC, fill=#F8F9F9, pos=(40,72), width=300px, height=230px)
  font(color=#566573, font-size=12px,
       text="Overlapping panels blend because the fills include alpha.",
       pos=(58,98))
  square(color=RGBA(52,152,219,0.85), fill=RGBA(52,152,219,0.35),
         pos=(70,125), width=130px, height=120px)
  square(color=RGBA(46,204,113,0.85), fill=RGBA(46,204,113,0.35),
         pos=(145,145), width=130px, height=120px)
  square(color=RGBA(231,76,60,0.85), fill=RGBA(231,76,60,0.35),
         pos=(110,182), width=130px, height=120px)

  square(color=#D5D8DC, fill=#F8F9F9, pos=(400,72), width=300px, height=230px)
  font(color=#566573, font-size=12px,
       text="Semi-transparent accents can sit on top of opaque UI blocks.",
       pos=(418,98))
  square(color=#2C3E50, fill=#2C3E50, pos=(432,128), width=236px, height=44px)
  font(color=white, font-size=15px, weight=bold,
       text="Revenue Summary", pos=(454,143))
  circle(color=RGBA(52,152,219,0.92), fill=RGBA(52,152,219,0.45),
         center=(480,228), radius=52)
  circle(color=RGBA(241,196,15,0.92), fill=RGBA(241,196,15,0.45),
         center=(542,212), radius=52)
  circle(color=RGBA(155,89,182,0.92), fill=RGBA(155,89,182,0.45),
         center=(604,236), radius=52)
end_frame
