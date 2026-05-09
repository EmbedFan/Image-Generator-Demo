# 88_connector_animated_patterns.dsl
# Category 16 — Advanced Connector Features
# Demonstrates: animated=true connector in a multi-frame GIF.
# The pattern advances pattern-speed pixels per frame automatically.
# All four pattern types shown across four animation frames.
# Output: 88_connector_animated_patterns.gif (cyclic loop)

begin_frame frame_dash
  hold-time=120; frame-mode=cyclic-run;
  image width=560px; height=280px; colorspace=RGB; dpi=96; output-format=gif;
  background(color=white);

  font(color=#2C3E50, font-size=14px, weight=bold,
       text="Animated Patterns (GIF) — pattern=dash", pos=(20, 18));

  square(color=#2C3E50, fill=#D5E8D4, pos=(20, 110), width=80px, height=40px);
  font(color=#2C3E50, font-size=11px, weight=bold, align=center,
       text="Source", pos=(60, 135));

  square(color=#2C3E50, fill=#DAE8FC, pos=(460, 110), width=80px, height=40px);
  font(color=#2C3E50, font-size=11px, weight=bold, align=center,
       text="Target", pos=(500, 135));

  connector(color=#3498DB, line-width=3px,
            start=(100, 130), end=(460, 130),
            animated=true, pattern=dash,
            pattern-length=12px, pattern-gap=6px,
            pattern-color=#85C1E9,
            pattern-speed=6px,
            end-cap=triangle, cap-size=medium);

  font(color=#7F8C8D, font-size=10px,
       text="pattern=dash  |  pattern-speed=6px  |  animated=true",
       pos=(20, 245));
  font(color=#7F8C8D, font-size=10px,
       text="Frame 1/4 — pattern advances +6px each frame",
       pos=(20, 260));
end_frame

begin_frame frame_dot
  hold-time=120; frame-mode=cyclic-run;
  image width=560px; height=280px; colorspace=RGB; dpi=96; output-format=gif;
  background(color=white);

  font(color=#2C3E50, font-size=14px, weight=bold,
       text="Animated Patterns (GIF) — pattern=dot", pos=(20, 18));

  square(color=#2C3E50, fill=#D5E8D4, pos=(20, 110), width=80px, height=40px);
  font(color=#2C3E50, font-size=11px, weight=bold, align=center,
       text="Source", pos=(60, 135));

  square(color=#2C3E50, fill=#FAE5D3, pos=(460, 110), width=80px, height=40px);
  font(color=#2C3E50, font-size=11px, weight=bold, align=center,
       text="Target", pos=(500, 135));

  connector(color=#E74C3C, line-width=3px,
            start=(100, 130), end=(460, 130),
            animated=true, pattern=dot,
            pattern-length=6px, pattern-gap=10px,
            pattern-color=#F1948A,
            pattern-speed=8px,
            end-cap=filled-circle, cap-size=medium);

  font(color=#7F8C8D, font-size=10px,
       text="pattern=dot  |  pattern-speed=8px  |  animated=true",
       pos=(20, 245));
  font(color=#7F8C8D, font-size=10px,
       text="Frame 2/4",
       pos=(20, 260));
end_frame

begin_frame frame_arrow
  hold-time=120; frame-mode=cyclic-run;
  image width=560px; height=280px; colorspace=RGB; dpi=96; output-format=gif;
  background(color=white);

  font(color=#2C3E50, font-size=14px, weight=bold,
       text="Animated Patterns (GIF) — pattern=arrow", pos=(20, 18));

  square(color=#2C3E50, fill=#D5E8D4, pos=(20, 110), width=80px, height=40px);
  font(color=#2C3E50, font-size=11px, weight=bold, align=center,
       text="Source", pos=(60, 135));

  square(color=#2C3E50, fill=#D5F5E3, pos=(460, 110), width=80px, height=40px);
  font(color=#2C3E50, font-size=11px, weight=bold, align=center,
       text="Target", pos=(500, 135));

  connector(color=#27AE60, line-width=3px,
            start=(100, 130), end=(460, 130),
            animated=true, pattern=arrow,
            pattern-length=16px, pattern-gap=8px,
            pattern-color=#82E0AA,
            pattern-speed=6px,
            end-cap=triangle, cap-size=medium);

  font(color=#7F8C8D, font-size=10px,
       text="pattern=arrow  |  pattern-speed=6px  |  animated=true",
       pos=(20, 245));
  font(color=#7F8C8D, font-size=10px,
       text="Frame 3/4 — directional arrows flow from source to target",
       pos=(20, 260));
end_frame

begin_frame frame_zigzag
  hold-time=120; frame-mode=cyclic-run;
  image width=560px; height=280px; colorspace=RGB; dpi=96; output-format=gif;
  background(color=white);

  font(color=#2C3E50, font-size=14px, weight=bold,
       text="Animated Patterns (GIF) — pattern=zigzag", pos=(20, 18));

  square(color=#2C3E50, fill=#EBD5F5, pos=(20, 110), width=80px, height=40px);
  font(color=#2C3E50, font-size=11px, weight=bold, align=center,
       text="Source", pos=(60, 135));

  square(color=#2C3E50, fill=#EBD5F5, pos=(460, 110), width=80px, height=40px);
  font(color=#2C3E50, font-size=11px, weight=bold, align=center,
       text="Target", pos=(500, 135));

  connector(color=#8E44AD, line-width=3px,
            start=(100, 130), end=(460, 130),
            animated=true, pattern=zigzag,
            pattern-length=10px, pattern-gap=4px,
            pattern-color=#D7BDE2,
            pattern-speed=5px,
            end-cap=diamond, cap-size=medium);

  font(color=#7F8C8D, font-size=10px,
       text="pattern=zigzag  |  pattern-speed=5px  |  animated=true",
       pos=(20, 245));
  font(color=#7F8C8D, font-size=10px,
       text="Frame 4/4 — 4 frames total, cyclic-run loops forever",
       pos=(20, 260));
end_frame
