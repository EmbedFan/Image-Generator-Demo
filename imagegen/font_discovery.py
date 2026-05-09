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
"""Font discovery for the --list-fonts CLI command.

Enumerates all fonts installed on the current system without external
dependencies — uses only fontTools (already required) and the standard library.

Reports per font family:
  - DSL-usable font-family name
  - Available style variants (normal, bold, italic, bold-italic)
  - Size type (scalable, or comma-separated bitmap pixel sizes)
  - Hungarian glyph coverage (all 18 required code points present)
"""

from __future__ import annotations

import os
import pathlib
import sys

HUNGARIAN_CODEPOINTS = [
    0x00C1, 0x00E1,  # Á á
    0x00C9, 0x00E9,  # É é
    0x00CD, 0x00ED,  # Í í
    0x00D3, 0x00F3,  # Ó ó
    0x00D6, 0x00F6,  # Ö ö
    0x0150, 0x0151,  # Ő ő
    0x00DA, 0x00FA,  # Ú ú
    0x00DC, 0x00FC,  # Ü ü
    0x0170, 0x0171,  # Ű ű
]

_STYLE_ORDER = ["normal", "bold", "italic", "bold-italic"]

_FONT_EXTENSIONS = {".ttf", ".otf", ".ttc", ".TTF", ".OTF", ".TTC"}


# ---------------------------------------------------------------------------
# Font file discovery
# ---------------------------------------------------------------------------

def _get_font_dirs() -> list[pathlib.Path]:
    dirs: list[pathlib.Path] = []
    if os.name == "nt":
        windir = pathlib.Path(os.environ.get("WINDIR", r"C:\Windows"))
        dirs.append(windir / "Fonts")
        localappdata = os.environ.get("LOCALAPPDATA", "")
        if localappdata:
            dirs.append(pathlib.Path(localappdata) / "Microsoft" / "Windows" / "Fonts")
    elif sys.platform == "darwin":
        dirs += [
            pathlib.Path("/Library/Fonts"),
            pathlib.Path("/System/Library/Fonts"),
            pathlib.Path.home() / "Library" / "Fonts",
        ]
    else:
        dirs += [
            pathlib.Path("/usr/share/fonts"),
            pathlib.Path("/usr/local/share/fonts"),
            pathlib.Path.home() / ".fonts",
            pathlib.Path.home() / ".local" / "share" / "fonts",
        ]
    return [d for d in dirs if d.is_dir()]


def _find_font_files() -> list[str]:
    seen: set[str] = set()
    for d in _get_font_dirs():
        for path in d.rglob("*"):
            if path.suffix in _FONT_EXTENSIONS and path.is_file():
                resolved = str(path.resolve())
                seen.add(resolved)
    return sorted(seen)


# ---------------------------------------------------------------------------
# Metadata extraction
# ---------------------------------------------------------------------------

def _read_font_metadata(font_path: str) -> tuple[str, str] | None:
    """Return (family_name, style_label) from a font file, or None on error."""
    try:
        from fontTools.ttLib import TTFont
        tt = TTFont(font_path, lazy=True)
        names = tt["name"]
        # Prefer Preferred Family (16) over Family (1)
        family = names.getDebugName(16) or names.getDebugName(1) or ""
        # Prefer Preferred Subfamily (17) over Subfamily (2)
        subfamily = names.getDebugName(17) or names.getDebugName(2) or "Regular"
        family = family.strip()
        if not family:
            return None
        return family, _subfamily_to_style(subfamily.strip())
    except Exception:
        return None


def _subfamily_to_style(subfamily: str) -> str:
    s = subfamily.lower()
    is_bold = any(w in s for w in ("bold", "heavy", "black", "extrabold", "semibold", "demibold"))
    is_italic = "italic" in s or "oblique" in s
    if is_bold and is_italic:
        return "bold-italic"
    if is_bold:
        return "bold"
    if is_italic:
        return "italic"
    return "normal"


# ---------------------------------------------------------------------------
# Font file index — lazy-built cache for renderer use
# ---------------------------------------------------------------------------

# Structure: { family_name_lower: { style_label: file_path } }
_FAMILY_INDEX: dict[str, dict[str, str]] | None = None


def _build_index() -> dict[str, dict[str, str]]:
    global _FAMILY_INDEX
    if _FAMILY_INDEX is not None:
        return _FAMILY_INDEX
    index: dict[str, dict[str, str]] = {}
    for font_path in _find_font_files():
        meta = _read_font_metadata(font_path)
        if meta is None:
            continue
        family_name, style_label = meta
        style_map = index.setdefault(family_name.lower(), {})
        style_map.setdefault(style_label, font_path)
    _FAMILY_INDEX = index
    return index


def find_font_file(family: str, style_label: str = "normal") -> str | None:
    """Return the file path for the best matching font variant, or None.

    Matching is case-insensitive on family name.  If the exact style variant
    is not available the function falls back to 'normal', then to any variant.
    """
    index = _build_index()
    style_map = index.get(family.lower())
    if not style_map:
        return None
    return (
        style_map.get(style_label)
        or style_map.get("normal")
        or next(iter(style_map.values()))
    )


# ---------------------------------------------------------------------------
# Size and glyph checks
# ---------------------------------------------------------------------------

def _get_size_info(font_path: str) -> str:
    try:
        from fontTools.ttLib import TTFont
        tt = TTFont(font_path, lazy=True)
        bitmap_table = tt.get("EBLC") or tt.get("CBLC")
        if bitmap_table is not None:
            sizes = sorted({strike.bitmapSizeTable.ppemX for strike in bitmap_table.strikes})
            return ", ".join(str(s) for s in sizes)
        return "scalable"
    except Exception:
        return "scalable"


def _has_hungarian_glyphs(font_path: str) -> bool:
    try:
        from fontTools.ttLib import TTFont
        tt = TTFont(font_path, lazy=True)
        cmap = tt.getBestCmap()
        if cmap is None:
            return False
        return all(cp in cmap for cp in HUNGARIAN_CODEPOINTS)
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def list_fonts() -> None:
    """Print a structured font report to stdout."""
    # Build families dict: name → {style_label → font_path}
    families: dict[str, dict[str, str]] = {}
    for font_path in _find_font_files():
        meta = _read_font_metadata(font_path)
        if meta is None:
            continue
        family_name, style_label = meta
        families.setdefault(family_name, {})
        # Keep first encountered file per style (stable across runs)
        families[family_name].setdefault(style_label, font_path)

    for name in sorted(families, key=str.casefold):
        style_map = families[name]
        styles = [s for s in _STYLE_ORDER if s in style_map]
        ref_file = style_map.get("normal") or next(iter(style_map.values()))
        sizes = _get_size_info(ref_file)
        hungarian = any(_has_hungarian_glyphs(p) for p in style_map.values())
        print(f"Font: {name}")
        print(f"  DSL name : {name}")
        print(f"  Styles   : {', '.join(styles) if styles else 'unknown'}")
        print(f"  Sizes    : {sizes}")
        print(f"  Hungarian: {'yes' if hungarian else 'no'}")
        print()
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
