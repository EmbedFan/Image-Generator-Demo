# 12_fill_vs_stroke.dsl
# Category 2 — Colors and Styling
# Demonstrates: fill and stroke combinations.
#   stroke only  — fill=none, color= set
#   fill only    — color=transparent (no visible stroke)
#   stroke+fill  — both color= and fill= set
#   thick stroke — large line-width with fill

begin_frame fill_vs_stroke
  image width=640px; height=370px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#F8F9FA);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 2: Fill vs Stroke Combinations",
       pos=(15, 18));

  # Column headers
  font(color=#7F8C8D, font-size=11px, align=center, text="stroke only\n(fill=none)", pos=(50, 48));
  font(color=#7F8C8D, font-size=11px, align=center, text="fill only\n(color=transparent)", pos=(190, 48));
  font(color=#7F8C8D, font-size=11px, align=center, text="stroke + fill", pos=(325, 48));
  font(color=#7F8C8D, font-size=11px, align=center, text="thick stroke\n+ fill", pos=(460, 48));

  # Row: circle
  font(color=#7F8C8D, font-size=11px, text="circle", pos=(10, 118));
  circle(color=#3498DB, fill=none,        center=(90, 120), radius=42, line-width=2px);
  circle(color=transparent, fill=#E74C3C, center=(230, 120), radius=42);
  circle(color=#2C3E50, fill=#F1C40F,     center=(365, 120), radius=42, line-width=2px);
  circle(color=#8E44AD, fill=#D7BDE2,     center=(500, 120), radius=42, line-width=8px);

  # Row: square
  font(color=#7F8C8D, font-size=11px, text="square", pos=(10, 210));
  square(color=#27AE60, fill=none,         pos=(48, 185), width=85px, height=55px, line-width=2px);
  square(color=transparent, fill=#E67E22,  pos=(188, 185), width=85px, height=55px);
  square(color=#2C3E50, fill=#AED6F1,      pos=(323, 185), width=85px, height=55px, line-width=2px);
  square(color=#C0392B, fill=#F5CBA7,      pos=(458, 185), width=85px, height=55px, line-width=8px);

  # Row: polygon (triangle)
  font(color=#7F8C8D, font-size=11px, text="polygon", pos=(10, 295));
  polygon(color=#16A085, fill=none,
          points=[(90,315),(48,265),(132,265)], line-width=2px);
  polygon(color=transparent, fill=#F39C12,
          points=[(230,315),(188,265),(272,265)]);
  polygon(color=#2C3E50, fill=#A9DFBF,
          points=[(365,315),(323,265),(407,265)], line-width=2px);
  polygon(color=#6C3483, fill=#D7BDE2,
          points=[(500,315),(458,265),(542,265)], line-width=8px);

  # Legend
  font(color=#7F8C8D, font-size=11px,
       text="color=transparent → invisible stroke. fill=none → transparent interior.",
       pos=(15, 343));
  font(color=#7F8C8D, font-size=11px,
       text="fill is not allowed on arc, line, or path primitives.",
       pos=(15, 358));
end_frame
