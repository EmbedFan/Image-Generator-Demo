# ------------------------------------------------------------
# File: 46_advanced_font_fallback.dsl
# Purpose:
#   Demonstrates comma-separated font family fallback chains.
# ------------------------------------------------------------

begin_frame advanced_font_fallback
  image width=820px; height=360px; colorspace=RGB; dpi=96; output-format=png
  background(color=#FBFCFC)

  font(color=#1F2D3A, font-size=18px, weight=bold,
       text="Category 11: Font fallback chains", pos=(24,26))

  square(color=#D6DBDF, fill=white, pos=(40,72), width=740px, height=248px)

  font(color=#566573, font-size=12px,
       text="Each text line provides a preferred font plus fallbacks.",
       pos=(60,96))

  font(font-family="Segoe UI, Arial, sans-serif", font-size=28px,
       color=#2C3E50, weight=bold,
       text="Primary UI Heading", pos=(60,140))

  font(font-family="Georgia, Times New Roman, serif", font-size=22px,
       color=#7B241C, style=italic,
       text="Editorial subtitle with serif fallback", pos=(60,184))

  font(font-family="Consolas, Courier New, monospace", font-size=20px,
       color=#1F618D,
       text="status_code = READY;", pos=(60,226))

  font(font-family="Fira Sans, Helvetica, Arial, sans-serif", font-size=16px,
       color=#117864,
       text="Fallback chains keep layout stable across different machines.",
       pos=(60,272))

  font(color=#85929E, font-size=12px,
       text="Syntax example: font-family=\"Preferred, Fallback, Generic\"",
       pos=(430,300))
end_frame
