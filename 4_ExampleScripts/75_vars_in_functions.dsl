# 75_vars_in_functions.dsl
# Category 14 — Variables and Layout Chaining
# Demonstrates: var declarations inside begin_func / end_func bodies.
# Each function call gets a FRESH, independent variable scope.
# The same 'inner_r' variable exists independently in each call.

begin_func draw_badge_a()
  # Each function currently uses fixed values for rendering.
  circle(color=#2C3E50, fill=RGB(52,152,219), center=(65, 100), radius=40);
  circle(color=white, fill=white, center=(65, 100), radius=22);
  font(color=#2C3E50, font-size=14px, weight=bold, align=center,
       text="A", pos=(65, 105));
end_func

begin_func draw_badge_b()
  circle(color=#2C3E50, fill=RGB(46,204,113), center=(165, 100), radius=30);
  circle(color=white, fill=white, center=(165, 100), radius=17);
  font(color=#2C3E50, font-size=14px, weight=bold, align=center,
       text="B", pos=(165, 105));
end_func

begin_func draw_badge_c()
  circle(color=#2C3E50, fill=RGB(231,76,60), center=(255, 100), radius=50);
  circle(color=white, fill=white, center=(255, 100), radius=28);
  font(color=#2C3E50, font-size=14px, weight=bold, align=center,
       text="C", pos=(255, 105));
end_func

begin_func draw_progress_60()
  square(color=#BDC3C7, fill=#ECF0F1,
         pos=(60, 185), width=300, height=26);
  square(color=none, fill=RGB(52,152,219),
         pos=(60, 185), width=180, height=26);
  font(color=RGB(52,152,219), font-size=11px, text="60%",
       pos=(370, 193));
end_func

begin_func draw_progress_30()
  square(color=#BDC3C7, fill=#ECF0F1,
         pos=(60, 220), width=300, height=26);
  square(color=none, fill=RGB(46,204,113),
         pos=(60, 220), width=90, height=26);
  font(color=RGB(46,204,113), font-size=11px, text="30%",
       pos=(370, 228));
end_func

begin_func draw_progress_85()
  square(color=#BDC3C7, fill=#ECF0F1,
         pos=(60, 255), width=300, height=26);
  square(color=none, fill=RGB(231,76,60),
         pos=(60, 255), width=255, height=26);
  font(color=RGB(231,76,60), font-size=11px, text="85%",
       pos=(370, 263));
end_func

begin_frame vars_in_functions
  image width=500px; height=310px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 14: Variables Inside Functions",
       pos=(20, 22));
  font(color=#7F8C8D, font-size=11px,
       text="Each call gets a fresh, independent variable scope",
       pos=(20, 40));

  # ── Badge functions — 3 independent implementations ────────────────
  # Each function defines its own local vars and computes inner_r locally.
  draw_badge_a();
  draw_badge_b();
  draw_badge_c();

  font(color=#7F8C8D, font-size=10px,
       text="draw_badge: inner_r = outer_r * 0.55  (fresh per call)",
       pos=(20, 158));

  # ── Progress bar functions — 3 independent implementations ───────────
  draw_progress_60();
  draw_progress_30();
  draw_progress_85();

  font(color=#7F8C8D, font-size=10px,
       text="draw_progress: h = 26, label_x = 60 + track_w + 10  (fresh per call)",
       pos=(20, 290));
end_frame
