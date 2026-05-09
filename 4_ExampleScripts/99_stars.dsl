# --- reusable star object ---
begin_obj star
  width: 40px;
  height: 40px;

  polygon(
    color=black,
    fill=gold,
    line-width=1px,
    points=[
      (20,0),
      (25,14),
      (40,14),
      (28,23),
      (32,38),
      (20,30),
      (8,38),
      (12,23),
      (0,14),
      (15,14)
    ]
  );
end_obj


# --- frame with stars on a circle ---
begin_frame star_circle
  image width=500px; height=500px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  # center (250,250), radius ≈ 150

  star(pos=(400,250));  # 0°
  star(pos=(356,356));  # 45°
  star(pos=(250,400));  # 90°
  star(pos=(144,356));  # 135°
  star(pos=(100,250));  # 180°
  star(pos=(144,144));  # 225°
  star(pos=(250,100));  # 270°
  star(pos=(356,144));  # 315°

end_frame