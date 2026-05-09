# FEA-007 — Variable Support and Bounding Box Extraction
#
# Demonstrates:
#   1. Variable declarations: var x, y;
#   2. Named primitives:      rect1 = square(...)
#   3. Bbox assignment:       x = rect1.bbox.x
#   4. Arithmetic on variables in drawing params: pos=(x + gap, cy)
#
# Layout: three squares chained horizontally using bbox-based positioning.
# A circle is centered on the first square using its bbox.

begin_frame fea007_demo
    image width=600 height=200 output-format=png;

    background(color=#1e1e2e);

    # Step 1 — draw first block and capture its bbox
    var gap;
    gap = 20;

    block1 = square(pos=(20, 70), width=120, height=60, fill=#89b4fa, color=none);

    var bx, by, bw, bh;
    bx = block1.bbox.x;
    by = block1.bbox.y;
    bw = block1.bbox.width;
    bh = block1.bbox.height;

    # Step 2 — place second block immediately after the first (+gap)
    block2 = square(pos=(bx + bw + gap, by), width=100, height=bh, fill=#a6e3a1, color=none);

    var bx2, bw2;
    bx2 = block2.bbox.x;
    bw2 = block2.bbox.width;

    # Step 3 — place third block after second
    block3 = square(pos=(bx2 + bw2 + gap, by), width=80, height=bh, fill=#fab387, color=none);

    # Step 4 — overlay circle centered on block1
    var cx, cy;
    cx = bx + bw / 2;
    cy = by + bh / 2;
    circle(center=(cx, cy), radius=25, color=#cdd6f4, line-width=2, fill=none);

    # Labels (font nodes are not named — they use frame-level variables in their positions)
    font(text="block1", pos=(bx + 5, by + bh + 14), font-size=11, color=#cdd6f4);
    font(text="block2", pos=(bx2 + 5, by + bh + 14), font-size=11, color=#cdd6f4);

end_frame
