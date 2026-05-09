# DSL object llibrary

#
# Warning icon 
#
begin_obj warning_icon
  polygon(color=black, line-width=3px, fill=yellow,
          points=[(48,6),(90,84),(6,84)]);

  square(color=black, line-width=1px, fill=black,
         pos=(45,32), width=8px, height=30px);

  square(color=black, line-width=1px, fill=black,
         pos=(45,68), width=8px, height=8px);
end_obj

#
# Error icon
#
begin_obj error_icon_1
  # Red octagon (stop sign)
  polygon(
    color=black,
    line-width=2px,
    fill=red,
    points=[
      (22,4),(42,4),(60,22),(60,42),
      (42,60),(22,60),(4,42),(4,22)
    ]
  );

  # White cross (X)

  # diagonal 1
  polygon(
    color=white,
    fill=white,
    points=[
      (20,16),(24,12),(44,32),(40,36)
    ]
  );

  # diagonal 2
  polygon(
    color=white,
    fill=white,
    points=[
      (40,16),(44,20),(24,40),(20,36)
    ]
  );
end_obj

#
# Error icon
#
begin_obj error_icon
  # Red octagon
  polygon(
    color=white,
    line-width=3px,
    fill=red,
    points=[
      (22,4),(42,4),(60,22),(60,42),
      (42,60),(22,60),(4,42),(4,22)
    ]
  );

  # STOP text (centered)
  font(
    font-family="DejaVu Sans",
    font-size=16px,
    color=white,
    weight=bold,
    align=center,
    text="STOP",
    pos=(8,23)
  );
end_obj


#
# Info icon
#
begin_obj info_icon
  # Blue circle
  circle(
    color=black,
    line-width=2px,
    fill=blue,
    center=(32,32),
    radius=28
  );

  # Yellow "I" using font (baseline-centered tuning)
  font(
    font-family="DejaVu Sans",
    font-size=48px,
    color=yellow,
    weight=bold,
    align=center,
    text="i",
    pos=(25,6)
  );
end_obj

