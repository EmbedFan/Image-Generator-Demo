# FEA-006 Prompt — Named Color Palette Support in DSL

| Field | Value |
|---|---|
| **Feature ID** | FEA-006 |
| **Title** | Named Color Palette Support in DSL |
| **Created at** | 2026-05-03 20:46:05 |
| **File version** | 1.0 |
| **Created by** | Claude Sonnet 4.6 |

---

## Feature Description

Introduce a **palette definition mechanism** in the DSL to allow reusable, named color definitions that can be referenced throughout the script using a consistent and readable syntax.

Currently, all colors must be defined inline using named colors, hex values, or RGB/RGBA notation. This leads to repetition of color values, reduced readability, difficulty maintaining consistent styling across large scripts, and lack of theming capability.

A palette system enables centralized color management, improved readability, easier maintenance and updates, and reusable styling via `include`.

---

## Proposed Syntax

### Palette Definition

```dsl
begin_palette <palette_name>
  <color_name> = <color_value>
  ...
end_palette
```

### Example Definition

```dsl
begin_palette default_colors
  primary   = RGB(35,66,200)
  secondary = RGB(200,200,200)
  accent    = RGBA(255,0,0,0.6)
  bg        = #F5F5F5
end_palette
```

### Usage Example

```dsl
background(color=@bg)

circle(
  color=@primary,
  fill=@accent,
  center=(200,200),
  radius=80
)
```

---

## Requirements

- Palette blocks are declared at script top-level using `begin_palette <name>` … `end_palette`.
- Each entry is `<alias> = <color_value>` where the value is any valid color format (named, hex, RGB, RGBA).
- Palette entries are referenced in any color parameter using `@<alias>` syntax.
- Multiple palettes are allowed per script; aliases from all palettes share a single global namespace.
- Palettes defined in included files are merged into the global alias namespace.
- Alias name collisions across palettes (local or included) are a parse error.
- Referencing an undefined alias (`@unknown`) is a parse error.
- Scripts without any `begin_palette` block are fully backward compatible.

---

## Goal

Provide centralized, reusable color management that reduces repetition, improves script readability, and enables consistent theming across frames and modular include-based libraries.

---

## Documents Updated

- `2_Docs/my_vision.md`
- `2_Docs/requirements.md`
- `2_Docs/system_design.md`
