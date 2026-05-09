# DSL Object Library — Normalized to 500x500 Bounding Box
# All objects are scaled and positioned to fit exactly within a 500x500 coordinate system.

#
# Warning icon (scaled from ~96x96 → 500x500)
#
begin_obj warning_icon
  polygon(color=black, line-width=16px, fill=yellow,
          points=[(250,31),(469,438),(31,438)]);

  square(color=black, line-width=5px, fill=black,
         pos=(234,167), width=42px, height=156px);

  square(color=black, line-width=5px, fill=black,
         pos=(234,354), width=42px, height=42px);
end_obj


#
# Error icon 1 (scaled from ~64x64 → 500x500)
#
begin_obj error_icon_1
  polygon(
    color=black,
    line-width=16px,
    fill=red,
    points=[
      (172,31),(328,31),(469,172),(469,328),
      (328,469),(172,469),(31,328),(31,172)
    ]
  );

  polygon(
    color=white,
    fill=white,
    points=[
      (156,125),(188,94),(344,250),(313,281)
    ]
  );

  polygon(
    color=white,
    fill=white,
    points=[
      (313,125),(344,156),(188,313),(156,281)
    ]
  );
end_obj


#
# Error icon (STOP text)
#
begin_obj error_icon
  polygon(
    color=white,
    line-width=16px,
    fill=red,
    points=[
      (172,31),(328,31),(469,172),(469,328),
      (328,469),(172,469),(31,328),(31,172)
    ]
  );

  font(
    font-family="DejaVu Sans",
    font-size=125px,
    color=white,
    weight=bold,
    align=center,
    text="STOP",
    pos=(62,180)
  );
end_obj


#
# Info icon (scaled from ~64x64 → 500x500)
#
begin_obj info_icon
  circle(
    color=black,
    line-width=16px,
    fill=blue,
    center=(250,250),
    radius=219
  );

  font(
    font-family="DejaVu Sans",
    font-size=375px,
    color=yellow,
    weight=bold,
    align=center,
    text="i",
    pos=(195,47)
  );
end_obj