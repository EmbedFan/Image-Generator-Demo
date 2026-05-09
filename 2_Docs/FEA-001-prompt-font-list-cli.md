# FEA-001 Implementation Plan — Font List CLI

| Field | Value |
|---|---|
| **Description** | Implementation plan for the --list-fonts CLI command: system font enumeration with DSL names, styles, sizes, and Hungarian glyph detection |
| **Created at** | 2026-05-02 08:12:13 |
| **File version** | 1.0 |
| **Created by** | Claude Sonnet 4.6 |

---

## 1. Feature Overview

**Feature ID:** FEA-001  
**Title:** Font List CLI Command  
**Related requirements:** REQ-0034, REQ-0034.1, REQ-0034.2, REQ-0034.3, REQ-0034.4

Add a `--list-fonts` flag to `imagegen.py` that scans all fonts installed on the current system and prints a structured report to stdout. For each font family the report shows:

- The exact `font-family` name to use in DSL scripts
- Available style variants (normal, bold, italic, bold-italic)
- Whether the font is scalable or bitmap (with pixel sizes if bitmap)
- Whether the font contains all 18 Hungarian-specific glyphs

---

## 2. CLI Interface

### 2.1 New Invocation Form

```
python imagegen.py --list-fonts
```

- Mutually exclusive with `<input-file>` — specifying both is a usage error (exit code 1).
- Outputs to **stdout** only; no DSL processing, no image output.
- Exit code `0` on success.

### 2.2 Output Format

One block per font family, blank line between entries, sorted alphabetically:

```
Font: Arial
  DSL name : Arial
  Styles   : normal, bold, italic, bold-italic
  Sizes    : scalable
  Hungarian: yes

Font: Courier New
  DSL name : Courier New
  Styles   : normal, bold, italic, bold-italic
  Sizes    : scalable
  Hungarian: yes

Font: FixedSys
  DSL name : FixedSys
  Styles   : normal
  Sizes    : 8, 9, 10, 12
  Hungarian: no
```

---

## 3. Implementation Steps

### Step 1 — Add `--list-fonts` Argument to CLI

**File:** `imagegen.py`

Add to the `argparse` setup:

```python
parser.add_argument(
    '--list-fonts',
    action='store_true',
    help='List all available system fonts and exit'
)
```

In the main execution block, before DSL processing:

```python
if args.list_fonts:
    if args.input_file:
        print("error: --list-fonts cannot be used together with an input file", file=sys.stderr)
        sys.exit(1)
    from font_discovery import list_fonts
    list_fonts()
    sys.exit(0)
```

---

### Step 2 — Create `font_discovery.py`

**File:** `font_discovery.py` (new file alongside `imagegen.py`)

#### 2a. Font Enumeration

Use `matplotlib.font_manager` for cross-platform discovery (Windows, macOS, Linux):

```python
from matplotlib import font_manager

def collect_families():
    fm = font_manager.FontManager()
    families = {}
    for entry in fm.ttflist:
        families.setdefault(entry.name, []).append(entry)
    return families
```

Each `FontEntry` has: `.name` (family name = DSL-usable string), `.fname` (file path),
`.style` (`'normal'` | `'italic'`), `.weight` (400 = regular, 700 = bold).

#### 2b. Style Mapping

Map `(style, weight)` pairs to DSL style labels:

| `entry.style` | `entry.weight` | Label |
|---|---|---|
| `normal` | 400 | `normal` |
| `normal` | 700 | `bold` |
| `italic` | 400 | `italic` |
| `italic` | 700 | `bold-italic` |

Collect unique labels per family; sort output order: normal → bold → italic → bold-italic.

#### 2c. Size Classification

Inspect the representative font file using `fonttools.ttLib.TTFont`:

```python
from fonttools.ttLib import TTFont

def get_size_info(font_path):
    try:
        tt = TTFont(font_path, lazy=True)
        if 'EBLC' in tt or 'CBLC' in tt:
            table = tt.get('EBLC') or tt.get('CBLC')
            sizes = sorted({bs.ppemX for bs in table.strikes})
            return ', '.join(str(s) for s in sizes)
        return 'scalable'
    except Exception:
        return 'scalable'
```

Use the `normal` variant file as the representative; fall back to any available file.

#### 2d. Hungarian Glyph Detection

Check for the 18 required code points using the `cmap` table:

```python
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

def has_hungarian_glyphs(font_path):
    try:
        tt = TTFont(font_path, lazy=True)
        cmap = tt.getBestCmap()
        if cmap is None:
            return False
        return all(cp in cmap for cp in HUNGARIAN_CODEPOINTS)
    except Exception:
        return False
```

For a font family: report `yes` if **any** variant file passes the check; `no` otherwise.

#### 2e. Main Output Function

```python
STYLE_ORDER = ['normal', 'bold', 'italic', 'bold-italic']

WEIGHT_STYLE_MAP = {
    ('normal', 400): 'normal',
    ('normal', 700): 'bold',
    ('italic', 400): 'italic',
    ('italic', 700): 'bold-italic',
}

def get_styles(entries):
    labels = set()
    for e in entries:
        label = WEIGHT_STYLE_MAP.get((e.style, e.weight))
        if label:
            labels.add(label)
    return [s for s in STYLE_ORDER if s in labels]

def get_reference_file(entries):
    for e in entries:
        if WEIGHT_STYLE_MAP.get((e.style, e.weight)) == 'normal':
            return e.fname
    return entries[0].fname

def list_fonts():
    families = collect_families()
    for name in sorted(families, key=str.casefold):
        entries = families[name]
        styles = get_styles(entries)
        ref_file = get_reference_file(entries)
        sizes = get_size_info(ref_file)
        hungarian = any(has_hungarian_glyphs(e.fname) for e in entries)
        print(f"Font: {name}")
        print(f"  DSL name : {name}")
        print(f"  Styles   : {', '.join(styles) if styles else 'unknown'}")
        print(f"  Sizes    : {sizes}")
        print(f"  Hungarian: {'yes' if hungarian else 'no'}")
        print()
```

---

### Step 3 — Add Python Dependencies

**File:** `requirements.txt` (create or update in project root)

```
matplotlib>=3.5
fonttools>=4.0
```

`matplotlib` provides cross-platform font enumeration.  
`fonttools` is needed for bitmap size detection and Hungarian glyph checking.

---

## 4. Files to Create / Modify

| Action | File | Notes |
|---|---|---|
| Modify | `imagegen.py` | Add `--list-fonts` argparse flag; add mutual-exclusivity check; dispatch to `font_discovery.list_fonts()` |
| Create | `font_discovery.py` | Font enumeration, style detection, size info, Hungarian check, stdout output |
| Modify | `requirements.txt` | Add `matplotlib>=3.5`, `fonttools>=4.0` |

---

## 5. Testing Plan

| Test | Input | Expected Output |
|---|---|---|
| Basic invocation | `python imagegen.py --list-fonts` | Font list printed to stdout; exit 0 |
| Mutual exclusivity | `python imagegen.py --list-fonts input.dsl` | Error to stderr; exit 1 |
| Scalable font | Any TrueType font on system | `Sizes: scalable` |
| Bitmap font (if present) | System bitmap font | `Sizes: 8, 10, 12, ...` |
| Full Hungarian support | Arial or Times New Roman (Windows) | `Hungarian: yes` |
| Missing Hungarian chars | Icon / symbol font | `Hungarian: no` |
| Style variants | Font with all 4 variants | Reports all 4 styles |
| Style variants partial | Font with only Regular + Bold | Reports `normal, bold` only |
| Alphabetical order | Full system scan | Font names sorted A–Z (case-insensitive) |
