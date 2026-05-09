begin_frame transparency_demo
  image width=900px; height=650px; colorspace=RGB; dpi=96; output-format=png;

  # Transparent background (important for RGBA demo)
  background(color=RGB(117,219,222));
#  background(color=white);

  # === LINE (stroke only) ===
  line(color=RGBA(255,0,0,0.75), line-width=4px,
       start=(50,50), end=(300,50), show-bbox=true);

  # === CIRCLE ===
  circle(color=RGBA(0,0,0,0.75), line-width=2px,
         fill=RGBA(0,255,0,0.75),
         center=(150,150), radius=60,
         show-bbox=true);

  # === SQUARE (RECTANGLE) ===
  square(color=RGBA(0,0,0,0.75), line-width=2px,
         fill=RGBA(0,0,255,0.75),
         pos=(300,100), width=120px, height=80px,
         show-bbox=true);

  # === POLYGON ===
  polygon(color=RGBA(0,0,0,0.75), line-width=2px,
          fill=RGBA(255,165,0,0.75),
          points=[(500,100),(600,200),(450,200)],
          show-bbox=true);

  # === PATH (stroke only) ===
  path(color=RGBA(128,0,128,0.75), line-width=3px,
       points=[(50,300),(150,250),(250,300),(350,250)],
       show-bbox=true);

  # === PIE ===
  pie(color=RGBA(0,0,0,0.75), line-width=2px,
      fill=RGBA(255,0,255,0.75),
      center=(150,450), radius=70,
      start-angle=0, end-angle=120,
      show-bbox=true);

  # === ARC (stroke only) ===
  arc(color=RGBA(0,128,128,0.75), line-width=4px,
      center=(350,450), radius=70,
      start-angle=45, end-angle=270,
      show-bbox=true);

  # === CONNECTOR ===
  connector(color=RGBA(0,0,0,0.75), line-width=2px,
            start=(500,350), end=(750,350),
            end-cap=triangle,
            label="Connector",
            show-bbox=true);

  # === TEXT (FONT) ===
  font(font-family="Arial", font-size=24px,
       color=RGBA(0,0,0,0.75),
       text="Transparency 75%",
       pos=(500,450),
       show-bbox=true);

  # === IMAGE (external placeholder) ===
  image(src="example.png", pos=(650,100),
        width=120px, height=120px,
        opacity=0.75,
        show-bbox=true);

end_frame