# 91_output_images_format.dsl
# Category 17 — Colorspaces, Output Formats, and Units
# Demonstrates: output-format=images — each frame is saved as a separate PNG file.
# File names are derived from the begin_frame identifier:
#   begin_frame step_one   → step_one.png
#   begin_frame step_two   → step_two.png
#   begin_frame step_three → step_three.png
# (No animated GIF is produced; individual PNG files are emitted instead.)

begin_frame step_one
  image width=400px; height=240px; colorspace=RGBA; dpi=96; output-format=images;
  background(color=#EBF5FB);

  font(color=#2980B9, font-size=16px, weight=bold,
       text="output-format=images — Frame 1 of 3",
       pos=(20, 22));
  font(color=#7F8C8D, font-size=11px,
       text="File: step_one.png",
       pos=(20, 42));

  # Visual: step indicator
  circle(color=#2980B9, fill=#3498DB, center=(60, 130), radius=35);
  font(color=white, font-size=22px, weight=bold, align=center,
       text="1", pos=(60, 140));

  line(color=#BDC3C7, line-width=2px, line-type=dashed,
       start=(100, 130), end=(200, 130));
  circle(color=#BDC3C7, fill=#ECF0F1, center=(230, 130), radius=35);
  font(color=#BDC3C7, font-size=22px, weight=bold, align=center,
       text="2", pos=(230, 140));

  line(color=#BDC3C7, line-width=2px, line-type=dashed,
       start=(270, 130), end=(340, 130));
  circle(color=#BDC3C7, fill=#ECF0F1, center=(370, 130), radius=25);
  font(color=#BDC3C7, font-size=22px, weight=bold, align=center,
       text="3", pos=(370, 140));

  font(color=#2C3E50, font-size=12px,
       text="Step One: Initialize", pos=(20, 200));
  font(color=#7F8C8D, font-size=11px,
       text="Each begin_frame produces a separate PNG named <frame-id>.png",
       pos=(20, 218));
end_frame

begin_frame step_two
  image width=400px; height=240px; colorspace=RGBA; dpi=96; output-format=images;
  background(color=#EAFAF1);

  font(color=#27AE60, font-size=16px, weight=bold,
       text="output-format=images — Frame 2 of 3",
       pos=(20, 22));
  font(color=#7F8C8D, font-size=11px,
       text="File: step_two.png",
       pos=(20, 42));

  circle(color=#BDC3C7, fill=#ECF0F1, center=(60, 130), radius=35);
  font(color=#BDC3C7, font-size=22px, weight=bold, align=center,
       text="1", pos=(60, 140));

  line(color=#27AE60, line-width=2px, start=(100, 130), end=(190, 130));
  circle(color=#27AE60, fill=#2ECC71, center=(230, 130), radius=35);
  font(color=white, font-size=22px, weight=bold, align=center,
       text="2", pos=(230, 140));

  line(color=#BDC3C7, line-width=2px, line-type=dashed,
       start=(270, 130), end=(340, 130));
  circle(color=#BDC3C7, fill=#ECF0F1, center=(370, 130), radius=25);
  font(color=#BDC3C7, font-size=22px, weight=bold, align=center,
       text="3", pos=(370, 140));

  font(color=#2C3E50, font-size=12px,
       text="Step Two: Process", pos=(20, 200));
  font(color=#7F8C8D, font-size=11px,
       text="Use output-format=images when you need per-frame files instead of a GIF.",
       pos=(20, 218));
end_frame

begin_frame step_three
  image width=400px; height=240px; colorspace=RGBA; dpi=96; output-format=images;
  background(color=#FEF9E7);

  font(color=#F39C12, font-size=16px, weight=bold,
       text="output-format=images — Frame 3 of 3",
       pos=(20, 22));
  font(color=#7F8C8D, font-size=11px,
       text="File: step_three.png",
       pos=(20, 42));

  circle(color=#BDC3C7, fill=#ECF0F1, center=(60, 130), radius=35);
  font(color=#BDC3C7, font-size=22px, weight=bold, align=center,
       text="1", pos=(60, 140));

  line(color=#F39C12, line-width=2px, start=(100, 130), end=(190, 130));
  circle(color=#BDC3C7, fill=#ECF0F1, center=(230, 130), radius=35);
  font(color=#BDC3C7, font-size=22px, weight=bold, align=center,
       text="2", pos=(230, 140));

  line(color=#F39C12, line-width=2px, start=(270, 130), end=(340, 130));
  circle(color=#F39C12, fill=#F1C40F, center=(370, 130), radius=35);
  font(color=white, font-size=22px, weight=bold, align=center,
       text="3", pos=(370, 140));

  font(color=#2C3E50, font-size=12px,
       text="Step Three: Complete", pos=(20, 200));
  font(color=#7F8C8D, font-size=11px,
       text="RGBA frames always produce .png; RGB frames would produce .jpeg files.",
       pos=(20, 218));
end_frame
