# ------------------------------------------------------------
# File: 44_advanced_z_order.dsl
# Purpose:
#   Demonstrates layering with z-index across primitives and text.
# ------------------------------------------------------------

begin_frame advanced_z_order
  image width=760px; height=360px; colorspace=RGB; dpi=96; output-format=png
  background(color=#F8F9F9)

  font(color=#1F2D3A, font-size=18px, weight=bold,
       text="Category 11: Layering and z-index", pos=(24,26), z-index=50)

  square(color=#D5DBDB, fill=#ECF0F1, pos=(40,70), width=300px, height=220px, z-index=1)
  font(color=#566573, font-size=12px,
       text="Background card z-index=1", pos=(60,96), z-index=2)

  circle(color=#1F618D, fill=RGBA(52,152,219,0.70), center=(160,190), radius=78, z-index=10)
  square(color=#B03A2E, fill=RGBA(231,76,60,0.65), pos=(125,112), width=170px, height=150px, rotate=8, z-index=20)
  polygon(color=#117A65, fill=RGBA(46,204,113,0.72),
          points=[(200,90),(290,165),(215,250),(130,175)], z-index=30)
  font(color=white, font-size=16px, weight=bold,
       text="Top Layer", pos=(170,176), z-index=40)

  square(color=#D5D8DC, fill=white, pos=(400,70), width=300px, height=220px, z-index=1)
  font(color=#566573, font-size=12px,
       text="The same shapes are reordered by z-index.", pos=(420,96), z-index=2)

  polygon(color=#117A65, fill=RGBA(46,204,113,0.72),
          points=[(560,90),(650,165),(575,250),(490,175)], z-index=10)
  circle(color=#1F618D, fill=RGBA(52,152,219,0.70), center=(520,190), radius=78, z-index=20)
  square(color=#B03A2E, fill=RGBA(231,76,60,0.65), pos=(485,112), width=170px, height=150px, rotate=8, z-index=30)
  font(color=#1F2D3A, font-size=16px, weight=bold,
       text="Square on top", pos=(505,176), z-index=40)
end_frame
