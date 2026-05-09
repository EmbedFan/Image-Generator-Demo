# FEA-002 Implementation Plan — UTF-8 Encoding Fix

| Field | Value |
|---|---|
| **Description** | Fix for corrupted Hungarian and non-ASCII characters in generated images caused by DSL files not being read with explicit UTF-8 encoding |
| **Created at** | 2026-05-02 17:30:45 |
| **File version** | 1.0 |
| **Created by** | Claude Sonnet 4.6 |

---

## 1. Feature Overview

**Feature ID:** FEA-002  
**Title:** UTF-8 Encoding Fix  
**Related requirements:** REQ-0035, REQ-0035.1  
**Type:** Bug fix

### Problem

DSL files containing non-ASCII characters (Hungarian: ő, ű, á, é, etc.) render as `?` or garbage in the output image. Root cause: the engine opens DSL files using the platform's default system encoding (`cp1252` on Windows, for example) instead of explicitly specifying UTF-8. Characters outside the ASCII range are misinterpreted before they reach the renderer.

### Fix

Change every `open(path)` call that reads DSL source to `open(path, encoding='utf-8')`. Strip the optional UTF-8 BOM (`﻿`) that some editors prepend. Wrap `UnicodeDecodeError` as `DslIOError` with a descriptive message so the user knows which file has the wrong encoding.

---

## 2. Files to Modify

| File | Change |
|---|---|
| `imagegen/orchestrator.py` | Main DSL file read: add BOM strip; add `UnicodeDecodeError` → `DslIOError` |
| `imagegen/resolver.py` | Included `.dsl` file read: add BOM strip; add `UnicodeDecodeError` → `DslIOError` |

> `imagegen/lexer.py` does **not** read files — it tokenises a string already passed in.  
> Do **not** change image asset loading (Pillow handles binary files; encoding is irrelevant there).

---

## 3. Implementation Steps

### Step 1 — Fix DSL file reading in the Lexer

**File:** `imagegen/lexer.py`

Locate the `open()` call that reads the DSL source file. Change:

```python
# BEFORE (platform-default encoding — silently corrupts non-ASCII)
with open(path) as fh:
    source = fh.read()

# AFTER
try:
    with open(path, encoding='utf-8') as fh:
        source = fh.read()
except UnicodeDecodeError as exc:
    raise DslIOError(
        f"{path}: file is not valid UTF-8 "
        f"(byte position ~{exc.start}); save the file as UTF-8 and retry"
    ) from exc
```

### Step 2 — Strip UTF-8 BOM

Immediately after reading, strip the optional BOM that some editors (e.g., Notepad on Windows) prepend:

```python
source = source.lstrip('﻿')
```

This must happen **before** tokenisation so the BOM character does not confuse the lexer.

### Step 3 — Fix included file reading in the Resolver

**File:** `imagegen/resolver.py`

Apply the same fix to the `open()` call that reads `include`-d files. The error message should identify the included file by path:

```python
try:
    with open(include_path, encoding='utf-8') as fh:
        source = fh.read().lstrip('﻿')
except UnicodeDecodeError as exc:
    raise DslIOError(
        f"{include_path}: included file is not valid UTF-8 "
        f"(byte position ~{exc.start}); save the file as UTF-8 and retry"
    ) from exc
```

---

## 4. Files to Create / Modify

| Action | File | Notes |
|---|---|---|
| Modify | `imagegen/orchestrator.py` | BOM strip on main DSL read; `UnicodeDecodeError` → `io_error()` with byte position |
| Modify | `imagegen/resolver.py` | BOM strip on included file read; `UnicodeDecodeError` → `io_error()` with byte position |

---

## 5. Testing Plan

| Test | Input | Expected Result |
|---|---|---|
| UTF-8 file with Hungarian chars | `font(..., text="Árvíztűrő tükörfúrógép")` | All characters render correctly in output image |
| UTF-8 BOM present | File starts with BOM (`\xef\xbb\xbf`) | BOM stripped silently; script parses and renders normally |
| Wrong encoding (Latin-1) | File saved as Windows-1252 containing ő | `DslIOError` with file path and byte position; exit code 3 |
| Wrong encoding in included file | Included file saved as Latin-1 | `DslIOError` identifying the included file path |
| ASCII-only file | Standard script with no non-ASCII characters | No change in behavior |
| Other Unicode (emoji, CJK) | `text="✓ Done"` | Renders correctly if the chosen font supports those glyphs |

---

## 6. Notes

- **No DSL syntax change** — purely an engine file-reading fix; existing scripts are unaffected.
- **Users** should save `.dsl` files as UTF-8. Most modern editors default to UTF-8.
- **VS Code** saves UTF-8 by default. **Notepad** on Windows may add a BOM — handled transparently by Step 2.
- **Legacy Notepad** (pre-Windows 10 1903) saves as ANSI by default — affected users must manually switch encoding to UTF-8 in the Save dialog.
