# ------------------------------------------------------------
# File: 47_advanced_clipping_with_transforms.dsl
# Purpose:
#   Demonstrates object-level clipping combined with transformed
#   inner primitives.
# ------------------------------------------------------------

begin_obj clipped_transform_card
  width: 220px;
  height: 220px;
  clip-shape: circle;
  square(color=#2E86C1, fill=#AED6F1, pos=(0,0), width=220px, height=220px);
  square(color=#7D3C98, fill=RGBA(155,89,182,0.45),
         pos=(32,34), width=156px, height=64px, rotate=18);
  square(color=#C0392B, fill=RGBA(231,76,60,0.40),
         pos=(28,104), width=170px, height=58px, rotate=346);
  polygon(color=#117864, fill=RGBA(46,204,113,0.58),
          points=[(110,18),(192,110),(110,202),(28,110)], rotate=12);
  circle(color=#F1C40F, fill=RGBA(241,196,15,0.72), center=(110,110), radius=42, scale=1.2);
end_obj

begin_obj clipped_bounds_card
  width: 220px;
  height: 220px;
  clip-bounds: (30px,30px,190px,190px);
  square(color=#2E86C1, fill=#D4E6F1, pos=(0,0), width=220px, height=220px);
  polygon(color=#1F618D, fill=RGBA(52,152,219,0.40),
          points=[(20,30),(200,30),(170,190),(50,190)], rotate=348);
  square(color=#C0392B, fill=RGBA(231,76,60,0.45),
         pos=(44,44), width=140px, height=140px, rotate=20);
  font(color=#1F2D3A, font-size=18px, weight=bold,
       text="CLIP", pos=(76,102), rotate=352);
end_obj

begin_frame advanced_clipping_with_transforms
  image width=760px; height=380px; colorspace=RGB; dpi=96; output-format=png
  background(color=#F8F9F9)

  font(color=#1F2D3A, font-size=18px, weight=bold,
       text="Category 11: Clipping with transforms", pos=(24,26))

  clipped_transform_card(pos=(80,90))
  clipped_bounds_card(pos=(410,90))

  font(color=#566573, font-size=12px,
       text="Left: circular clip containing rotated and scaled shapes.",
       pos=(74,334))
  font(color=#566573, font-size=12px,
       text="Right: rectangular clip-bounds trims transformed content.",
       pos=(400,334))
end_frame
