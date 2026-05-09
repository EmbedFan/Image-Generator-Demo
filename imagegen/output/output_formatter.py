# =============================================================================
# DSL-demo-v1.x
# This version is a public demo version: DSL-demo-v1.x
#
# Created by Attila Gallai using AI aided software development process
# Copyright Attila Gallai (C) 1995 - 2026
#
# -----------------------------------------------------------------------------
# Minimal MIT License
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, subject to the following condition:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# =============================================================================
"""Output Formatter (REQ-0027, REQ-0029, REQ-0001.1, REQ-0001.2).

Output format resolution rules:
  - Format is taken from the first frame's ImageDef.output_format.
  - Conflicting output-format on subsequent frames → warning, first frame wins.
  - Output is written to the same directory as the input .dsl file unless
    output_path is provided (REQ-0029).

Format → file rules:
  png     → <script-stem>.png   (RGB, RGBA, GRAY all supported)
  jpeg    → <script-stem>.jpeg  (RGB only; RGBA/GRAY caught by validator)
  gif     → <script-stem>.gif   (animated; hold-time per frame; loop from first frame's frame-mode)
  images  → <frame-id>.png or <frame-id>.jpeg per frame
            RGBA/GRAY → always .png; RGB → .jpeg (REQ-0001.1)
            Duplicate frame-id → silent overwrite + warning
"""

from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

from PIL import Image

if TYPE_CHECKING:
    from imagegen.ast_nodes import FrameDef
    from imagegen.error_reporter import ErrorReporter


class OutputFormatter:
    def __init__(self, reporter: ErrorReporter) -> None:
        self._reporter = reporter

    def write(
        self,
        frames: list[tuple[FrameDef, Image.Image]],
        script_stem: str,
        output_path: pathlib.Path | None,
        base_dir: pathlib.Path,
    ) -> None:
        """Determine output format from first frame and write all output files.

        Conflicting output-format on subsequent frames: warning emitted, first wins.
        """
        if not frames:
            return

        first_frame_def, first_image = frames[0]
        output_format = first_frame_def.image_def.output_format

        # Warn about conflicting output-format on subsequent frames
        for frame_def, _ in frames[1:]:
            if frame_def.image_def.output_format != output_format:
                self._reporter.warning(
                    frame_def.source_file, frame_def.line,
                    f"output-format '{frame_def.image_def.output_format}' ignored; "
                    f"using '{output_format}' from first frame '{first_frame_def.name}'"
                )

        if output_format == "png":
            path = self._resolve_output_path(script_stem, output_path, base_dir, ".png")
            self._write_png(first_image, path)

        elif output_format == "jpeg":
            path = self._resolve_output_path(script_stem, output_path, base_dir, ".jpeg")
            self._write_jpeg(first_image, path)

        elif output_format == "gif":
            path = self._resolve_output_path(script_stem, output_path, base_dir, ".gif")
            self._write_gif(frames, path)

        elif output_format == "images":
            out_dir: pathlib.Path
            if output_path is not None:
                out_dir = output_path if output_path.is_dir() else output_path.parent
            else:
                out_dir = base_dir
            self._write_images(frames, out_dir)

        else:
            # Unknown format — fall back to png
            self._reporter.warning(
                first_frame_def.source_file, first_frame_def.line,
                f"unknown output-format '{output_format}'; falling back to 'png'"
            )
            path = self._resolve_output_path(script_stem, output_path, base_dir, ".png")
            self._write_png(first_image, path)

    def _write_png(self, image: Image.Image, path: pathlib.Path) -> None:
        dpi = image.info.get("dpi", (96, 96))
        image.save(str(path), format="PNG", dpi=dpi)

    def _write_jpeg(self, image: Image.Image, path: pathlib.Path) -> None:
        dpi = image.info.get("dpi", (96, 96))
        # JPEG does not support alpha — convert RGBA → RGB if needed
        out = image.convert("RGB") if image.mode == "RGBA" else image
        out.save(str(path), format="JPEG", dpi=dpi, quality=95)

    def _write_gif(
        self,
        frames: list[tuple[FrameDef, Image.Image]],
        path: pathlib.Path,
    ) -> None:
        """Write animated GIF.

        hold-time per frame → delay in centiseconds (GIF unit = 10 ms).
        frame-mode from first frame determines loop:
          'cyclic-run' → loop=0 (loop forever)
          'one-run'    → loop=1 (play once)
        """
        first_frame_def = frames[0][0]
        loop = 0 if first_frame_def.frame_mode == "cyclic-run" else 1

        pil_frames = []
        durations = []
        for frame_def, img in frames:
            pil_frames.append(img.convert("P"))          # GIF requires palette mode
            durations.append(int(frame_def.hold_time))   # ms

        if not pil_frames:
            return

        pil_frames[0].save(
            str(path),
            format="GIF",
            save_all=True,
            append_images=pil_frames[1:],
            loop=loop,
            duration=durations,
        )

    def _write_images(
        self,
        frames: list[tuple[FrameDef, Image.Image]],
        output_dir: pathlib.Path,
    ) -> None:
        """Write each frame as a separate file.

        RGBA/GRAY → .png; RGB → .jpeg (REQ-0001.1).
        Duplicate frame-id → silent overwrite + warning.
        """
        seen: set[str] = set()
        for frame_def, img in frames:
            frame_id = frame_def.name
            if img.mode in ("RGBA", "L"):
                ext = ".png"
            else:
                ext = ".jpeg"
            filename = frame_id + ext
            if filename in seen:
                self._reporter.warning(
                    frame_def.source_file, frame_def.line,
                    f"duplicate frame-id '{frame_id}' in 'images' mode; overwriting"
                )
            seen.add(filename)
            dest = output_dir / filename
            if ext == ".png":
                self._write_png(img, dest)
            else:
                self._write_jpeg(img, dest)

    def _resolve_output_path(
        self,
        script_stem: str,
        output_path: pathlib.Path | None,
        base_dir: pathlib.Path,
        extension: str,
    ) -> pathlib.Path:
        """Determine the output file path.

        If output_path is given and is a directory, use it with <script-stem><ext>.
        If output_path is given as a file path, use it directly.
        Otherwise, write next to the input .dsl file (REQ-0029).
        """
        if output_path is None:
            return base_dir / (script_stem + extension)
        if output_path.is_dir():
            return output_path / (script_stem + extension)
        return output_path
# =============================================================================
# DSL-demo-v1.x
# This version is a public demo version: DSL-demo-v1.x
#
# Created by Attila Gallai using AI aided software development process
# Copyright Attila Gallai (C) 1995 - 2026
#
# -----------------------------------------------------------------------------
# Minimal MIT License
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, subject to the following condition:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# =============================================================================
