begin_frame transparency_demo_extended
  image width=1200px; height=900px; colorspace=RGB; dpi=96; output-format=png;

  background(color=RGBA(117,219,222,1));

  # === LINE ===
  line(color=RGBA(255,0,0,0.75), line-width=4px,
       start=(50,50), end=(300,50), show-bbox=true);

  line(color=RGBA(255,128,0,0.75), line-width=3px,
       start=(50,80), end=(300,120), show-bbox=true);

  # === CIRCLE ===
  circle(color=RGBA(0,0,0,0.75), line-width=2px,
         fill=RGBA(0,255,0,0.75),
         center=(150,200), radius=60,
         show-bbox=true);

  circle(color=RGBA(0,0,0,0.75), line-width=2px,
         fill=RGBA(0,200,100,0.75),
         center=(300,200), radius=40,
         show-bbox=true);

  # === SQUARE ===
  square(color=RGBA(0,0,0,0.75), line-width=2px,
         fill=RGBA(0,0,255,0.75),
         pos=(450,150), width=120px, height=80px,
         show-bbox=true);

  square(color=RGBA(0,0,0,0.75), line-width=2px,
         fill=RGBA(0,100,255,0.75),
         pos=(600,150), width=80px, height=120px,
         show-bbox=true);

  # === POLYGON ===
  polygon(color=RGBA(0,0,0,0.75), line-width=2px,
          fill=RGBA(255,165,0,0.75),
          points=[(750,150),(850,250),(700,250)],
          show-bbox=true);

  polygon(color=RGBA(0,0,0,0.75), line-width=2px,
          fill=RGBA(255,200,0,0.75),
          points=[(900,150),(1000,200),(950,280),(850,250)],
          show-bbox=true);

  # === PATH ===
  path(color=RGBA(128,0,128,0.75), line-width=3px,
       points=[(50,350),(150,300),(250,350),(350,300)],
       show-bbox=true);

  path(color=RGBA(200,0,200,0.75), line-width=2px,
       points=[(400,350),(500,320),(600,360),(700,310)],
       show-bbox=true);

  # === PIE ===
  pie(color=RGBA(0,0,0,0.75), line-width=2px,
      fill=RGBA(255,0,255,0.75),
      center=(150,550), radius=70,
      start-angle=0, end-angle=120,
      show-bbox=true);

  pie(color=RGBA(0,0,0,0.75), line-width=2px,
      fill=RGBA(200,0,200,0.75),
      center=(300,550), radius=50,
      start-angle=180, end-angle=300,
      show-bbox=true);

  # === ARC ===
  arc(color=RGBA(0,128,128,0.75), line-width=4px,
      center=(450,550), radius=70,
      start-angle=45, end-angle=270,
      show-bbox=true);

  arc(color=RGBA(0,180,180,0.75), line-width=3px,
      center=(600,550), radius=50,
      start-angle=0, end-angle=180,
      show-bbox=true);

  # === CONNECTOR ===
  connector(color=RGBA(0,0,0,0.75), line-width=2px,
            start=(750,450), end=(1000,450),
            end-cap=triangle,
            label="Connector A",
            show-bbox=true);

  connector(color=RGBA(50,50,50,0.75), line-width=2px,
            start=(750,500), end=(1000,550),
            end-cap=triangle,
            label="Connector B",
            show-bbox=true);

  # === FONT ===
  font(font-family="Arial", font-size=24px,
       color=RGBA(0,0,0,0.75),
       text="Transparency 75%",
       pos=(750,600),
       show-bbox=true);

  font(font-family="Arial", font-size=18px,
       color=RGBA(0,0,0,0.75),
       text="More elements",
       pos=(750,640),
       show-bbox=true);

  # === IMAGE ===
  image(src="example.png", pos=(950,150),
        width=120px, height=120px,
        opacity=0.75,
        show-bbox=true);

  image(src="example.png", pos=(950,300),
        width=80px, height=80px,
        opacity=0.75,
        show-bbox=true);

end_frame