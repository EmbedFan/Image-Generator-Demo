# 07_simple_connector.dsl
# Category 1 - Basic Primitives
# Demonstrates: connector primitive — arrowhead caps, connector types, labels, cap sizes

begin_frame simple_connector
  image width=700px; height=540px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  # ============================================================
  # Section 1: End-cap shapes (all cap types, straight line)
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Arrowhead / cap shapes", pos=(20, 18));

  # triangle
  connector(color=black, line-width=1px, start=(20, 50), end=(180, 50), end-cap=triangle);
  font(font-family="Arial", font-size=11px, color=darkgray, text="triangle", pos=(20, 65));

  # open-triangle
  connector(color=black, line-width=1px, start=(20, 95), end=(180, 95), end-cap=open-triangle);
  font(font-family="Arial", font-size=11px, color=darkgray, text="open-triangle", pos=(20, 110));

  # circle (hollow)
  connector(color=black, line-width=1px, start=(20, 140), end=(180, 140), end-cap=circle);
  font(font-family="Arial", font-size=11px, color=darkgray, text="circle", pos=(20, 155));

  # filled-circle
  connector(color=black, line-width=1px, start=(20, 185), end=(180, 185), end-cap=filled-circle);
  font(font-family="Arial", font-size=11px, color=darkgray, text="filled-circle", pos=(20, 200));

  # diamond (hollow)
  connector(color=black, line-width=1px, start=(20, 230), end=(180, 230), end-cap=diamond);
  font(font-family="Arial", font-size=11px, color=darkgray, text="diamond", pos=(20, 245));

  # filled-diamond
  connector(color=black, line-width=1px, start=(20, 275), end=(180, 275), end-cap=filled-diamond);
  font(font-family="Arial", font-size=11px, color=darkgray, text="filled-diamond", pos=(20, 290));

  # square (hollow)
  connector(color=black, line-width=1px, start=(20, 320), end=(180, 320), end-cap=square);
  font(font-family="Arial", font-size=11px, color=darkgray, text="square", pos=(20, 335));

  # filled-square
  connector(color=black, line-width=1px, start=(20, 365), end=(180, 365), end-cap=filled-square);
  font(font-family="Arial", font-size=11px, color=darkgray, text="filled-square", pos=(20, 380));

  # ============================================================
  # Section 2: Both-end caps + cap sizes
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Both caps + cap sizes", pos=(240, 18));

  # Bidirectional arrow (triangle on both ends)
  connector(color=black, line-width=2px,
            start=(240, 55), end=(450, 55),
            start-cap=triangle, end-cap=triangle);
  font(font-family="Arial", font-size=11px, color=darkgray,
       text="start+end triangle", pos=(240, 70));

  # Cap size: small
  connector(color=navy, line-width=1px,
            start=(240, 100), end=(450, 100),
            end-cap=triangle, cap-size=small);
  font(font-family="Arial", font-size=11px, color=darkgray,
       text="cap-size=small", pos=(240, 115));

  # Cap size: medium (default)
  connector(color=navy, line-width=1px,
            start=(240, 140), end=(450, 140),
            end-cap=triangle, cap-size=medium);
  font(font-family="Arial", font-size=11px, color=darkgray,
       text="cap-size=medium", pos=(240, 155));

  # Cap size: large
  connector(color=navy, line-width=1px,
            start=(240, 180), end=(450, 180),
            end-cap=triangle, cap-size=large);
  font(font-family="Arial", font-size=11px, color=darkgray,
       text="cap-size=large", pos=(240, 195));

  # ============================================================
  # Section 3: Connector types (straight / step / curved)
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Connector types", pos=(240, 230));

  # straight (default)
  connector(color=black, line-width=2px,
            points=[(240, 270), (450, 310)],
            connector-type=straight, end-cap=triangle);
  font(font-family="Arial", font-size=11px, color=darkgray,
       text="straight", pos=(240, 325));

  # step (right-angle routing)
  connector(color=blue, line-width=2px,
            points=[(240, 370), (350, 370), (450, 420)],
            connector-type=step, end-cap=triangle);
  font(font-family="Arial", font-size=11px, color=darkgray,
       text="step", pos=(240, 435));

  # curved (Catmull-Rom spline, needs >= 3 points)
  connector(color=red, line-width=2px,
            points=[(240, 460), (340, 440), (400, 490), (450, 470)],
            connector-type=curved, end-cap=open-triangle);
  font(font-family="Arial", font-size=11px, color=darkgray,
       text="curved", pos=(240, 505));

  # ============================================================
  # Section 4: Labeled connector
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Labeled connector", pos=(490, 230));

  connector(color=black, line-width=1px,
            start=(490, 270), end=(680, 270),
            end-cap=triangle,
            label="data flow", label-pos=center, label-font-size=12px);

end_frame
