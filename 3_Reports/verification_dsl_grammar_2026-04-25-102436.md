# Verification — DSL Grammar Description

| Field | Value |
|---|---|
| **Description** | Verification of 2_Docs/DSL_grammar_description.md against 2_Docs/requirements.md and 2_Docs/my_vision.md |
| **Created at** | 2026-04-25 10:24:36 |
| **File version** | 2.2 |
| **Created by** | Claude Sonnet 4.6 |

---

## 1. Scope

Verified document: `2_Docs/DSL_grammar_description.md` (v1.6 semantic correctness review — 2026-04-25)  
Reference documents: `2_Docs/requirements.md` (v1.5), `2_Docs/my_vision.md`

> **Note:** Previous verifications (v1.0–v1.5) resolved 20 issues. This update covers the semantic correctness review of v1.6 (11 new issues found and resolved; document bumped to v1.7).

Verification checks:
- Coverage: every requirement mapped to a document section
- EBNF correctness: grammar rules are internally consistent and complete
- Internal consistency: prose, tables, and EBNF agree with each other
- Example correctness: code examples conform to the grammar

---

## 2. Coverage Check — Requirements vs Document Sections

| Req ID | Title | Covered | Section(s) |
|---|---|---|---|
| REQ-0001 | Script Processing Engine | ✓ | §1, §4 |
| REQ-0001.1 | Single-Frame Output | ✓ | §5, §17.1 |
| REQ-0001.2 | Multi-Frame Output | ✓ | §5, §6, §17.2 |
| REQ-0002 | Frame Declaration | ✓ | §5, §3 EBNF `<frame>` |
| REQ-0002.1 | Frame Hold Time | ✓ | §5 table |
| REQ-0002.2 | Frame Mode | ✓ | §5 table |
| REQ-0002.3 | Frame Colorspace | ✓ | §5 table |
| REQ-0003 | Image Canvas Definition | ✓ | §6 |
| REQ-0004.1 | Solid Color Background | ✓ | §7.1 |
| REQ-0004.2 | Gradient Background | ✓ | §7.2 |
| REQ-0004.3 | Image Background | ✓ | §7.3 |
| REQ-0005 | Primitive: line | ✓ | §8.1 |
| REQ-0006 | Primitive: circle | ✓ | §8.2 |
| REQ-0007 | Primitive: square | ✓ | §8.3 |
| REQ-0008 | Primitive: polygon | ✓ | §8.4 |
| REQ-0009 | Primitive: path | ✓ | §8.5 |
| REQ-0010 | Primitive: pie | ✓ | §8.6 |
| REQ-0010.1 | Primitive: arc | ✓ | §8.7 |
| REQ-0011 | Primitive: connector | ✓ | §9 |
| REQ-0011.1 | Connector Multi-Segment Points | ✓ | §9.1 |
| REQ-0011.2 | Connector Type | ✓ | §9.2 |
| REQ-0011.3 | Connector Caps | ✓ | §9.3 |
| REQ-0011.4 | Connector Cap Size | ✓ | §9.3 |
| REQ-0011.5 | Connector Corner Style | ✓ | §9.4 |
| REQ-0011.6 | Connector Label | ✓ | §9.5 |
| REQ-0011.7 | Connector Animation Flag | ✓ | §9.6 |
| REQ-0011.8 | Connector Pattern | ✓ | §9.6 |
| REQ-0011.9 | Connector Pattern Speed | ✓ | §9.6 |
| REQ-0012 | Primitive: font | ✓ | §10 |
| REQ-0013 | Primitive: image | ✓ | §11 |
| REQ-0014 | Object Template Definition | ✓ | §12 |
| REQ-0014.1 | Object Instantiation | ✓ | §12.3 |
| REQ-0014.2 | Clipping and Masking | ✓ | §12.2 |
| REQ-0014.3 | Nested Objects | ✓ | §12.4 |
| REQ-0014.4 | Object Border Shadow | ✓ | §12.2 |
| REQ-0015 | Function Declaration | ✓ | §13 |
| REQ-0015.1 | Function Parameter Expressions | ✓ | §13.3 |
| REQ-0015.2 | Function Composition | ✓ | §13.1 |
| REQ-0016 | Script Inclusion | ✓ | §14 |
| REQ-0016.1 | Include Path Resolution | ✓ | §14 |
| REQ-0016.2 | Recursive Includes | ✓ | §14 |
| REQ-0017 | Transformations | ✓ | §8.0 |
| REQ-0018 | Z-Order Layering | ✓ | §8.0 |
| REQ-0019 | Coordinate System | ✓ | §8.0.1 |
| REQ-0020 | Color Format Support | ✓ | §15.1, §3 EBNF `<color>` |
| REQ-0021 | Unit Measurements | ✓ | §15.3, §3 EBNF `<unit>` |
| REQ-0022 | Line Type Styles | ✓ | §15.2 |
| REQ-0023 | String Handling and Escaping | ✓ | §2.6 |
| REQ-0024 | Statement Delimiters | ✓ | §2.4 |
| REQ-0025 | Type Validation and Error Handling | ✓ | §18 |
| REQ-0025.1 | Optional Parameter Defaults | ✓ | §16.2 |
| REQ-0027 | Supported Output Formats | ✓ | §6 |
| REQ-0028 | DSL Script Grammar | ✓ | §3 |
| REQ-0029 | Output File Naming | ✓ | §6 `output-format` |
| REQ-0031 | Error Messages | ✓ | §18.3 |
| REQ-0032 | External Image Asset Support | ✓ | §7.3, §11 |
| REQ-0033 | Modular Script Composition | ✓ | §14 |

**Coverage result: 100% — all DSL-facing requirements are addressed.**

> REQ-0026 (Python implementation), REQ-0030 (CLI), are out-of-scope for a grammar description and correctly omitted.

---

## 3. Issues Found

### Issue 1 — ~~HIGH~~ RESOLVED: Undefined `<key>` token in `<frame-attr>` and `<obj-attr>` EBNF rules

**Status: FIXED** in `DSL_grammar_description.md` v1.1

**Location:** Section 3, EBNF rules `<frame-attr>` and `<obj-attr>`

**Description:**
Both rules contained a catch-all first alternative that referenced `<key>`, which was never defined anywhere in the grammar:

```ebnf
<frame-attr> ::= <key> '=' <value> <terminator>   (* <key> is undefined *)
<obj-attr>   ::= <key> ':' <value> <terminator>    (* <key> is undefined *)
```

This made the grammar technically incomplete and would confuse a parser generator.

**Fix applied:**
The catch-all `<key>` alternatives were removed entirely from both rules. The `<frame-attr>` rule now lists only its three valid named alternatives (`hold-time`, `frame-mode`, `colorspace`). The `<obj-attr>` rule now enumerates all valid object attributes explicitly (`width`, `height`, `background`, `border`, `shadow`, `clip-bounds`, `clip-shape`).

---

### Issue 2 — ~~HIGH~~ RESOLVED: `shadow`, `clip-bounds`, and `clip-shape` missing from `<obj-attr>` EBNF

**Status: FIXED** in `DSL_grammar_description.md` v1.1

**Location:** Section 3, EBNF rule `<obj-attr>`

**Description:**
The `<obj-attr>` rule only enumerated `width`, `height`, `background`, and `border`. Three attributes documented in Section 12.2 — `shadow`, `clip-bounds`, `clip-shape` — were absent from the formal grammar rule.

**Fix applied:**
All three attributes were added as explicit alternatives in the `<obj-attr>` rule. The rule now reads:

```ebnf
<obj-attr>         ::= 'width' ':' <length>
                     | 'height' ':' <length>
                     | 'background' ':' <color>
                     | 'border' ':' <border-value>
                     | 'shadow' ':' <shadow-value>
                     | 'clip-bounds' ':' '(' <length> ',' <length> ',' <length> ',' <length> ')'
                     | 'clip-shape' ':' <identifier>
```

---

### Issue 3 — ~~HIGH~~ RESOLVED: `shadow` incorrectly nested inside `<border-value>` in EBNF

**Status: FIXED** in `DSL_grammar_description.md` v1.1

**Location:** Section 3, EBNF rule `<border-value>`

**Description:**
The grammar incorrectly defined `shadow` as an optional tail of the `border` attribute:

```ebnf
<border-value> ::= <line-type> <length> <color>
                     ('shadow' ':' <shadow-value>)?
```

Per REQ-0014.4 and the examples in Section 12.5, `shadow` is a **separate** object attribute, not a continuation of `border`.

**Fix applied:**
`<border-value>` simplified to:
```ebnf
<border-value> ::= <line-type> <length> <color>
```
`shadow` is now a standalone `<obj-attr>` alternative (resolved together with Issue 2):
```ebnf
| 'shadow' ':' <shadow-value>
```

---

### Issue 4 — ~~MEDIUM~~ RESOLVED: `none` not included in `<color>` / `<named-color>` EBNF

**Status: FIXED** in `DSL_grammar_description.md` v1.1

**Location:** Section 3, EBNF rule `<color>`; Section 15.1

**Description:**
`none` was used throughout the document as the default fill value (`fill=none`) but did not appear in the formal `<color>` EBNF rule, making the grammar incomplete for a parser generator.

**Fix applied:**
`none` added as an explicit alternative in the `<color>` rule, with a fill-only annotation:

```ebnf
<color> ::= <named-color>
          | 'none'                          (* fill-only: transparent / no paint *)
          | '#' [0-9A-Fa-f]{6}
          | 'RGB'  '(' <byte> ',' <byte> ',' <byte> ')'
          | 'RGBA' '(' <byte> ',' <byte> ',' <byte> ',' <number-0-1> ')'
```

Section 15.1 prose also updated to clarify `none` is valid for `fill` and `background` properties only.

---

### Issue 5 — ~~MEDIUM~~ RESOLVED: `output-format` default inconsistency between Section 16.2 and Example 17.2

**Status: FIXED** in `DSL_grammar_description.md` v1.1

**Location:** Section 6 parameter table; Section 16.2 defaults table; Section 17.2 notes

**Description:**
Section 16.2 stated `output-format` defaults to `png`, while Example 17.2 note said `default output-format=gif` for a multi-frame script — a direct contradiction.

**Fix applied:**
The rule is: the engine selects the default based on frame count — `png` for a single frame, `gif` for multiple frames. Both Section 6 and Section 16.2 now explicitly state:

> When omitted, the engine defaults to `png` for a single frame and `gif` for multiple frames.

Section 17.2 note is consistent with this rule (3 frames → default `gif`).

---

### Re-verification Issues (v1.1 — 2026-04-25)

---

### Issue 6 — ~~MEDIUM~~ RESOLVED: `transparent` and `none` semantic difference not documented

**Status: FIXED** in `DSL_grammar_description.md` v1.2

**Location:** Section 15.1 Color Values

**Description:**
The document listed `transparent` as an unrestricted named color and `none` as a fill/background-only no-paint token without explaining their semantic difference. An implementer could treat them as synonyms.

**Fix applied:**
Section 15.1 prose expanded with two explicit bullet points:

- `none` — no-paint token; valid for `fill` and `background` properties **only**; using it on a stroke property (`color=none`) is a **parse error**.
- `transparent` — standard named color (equivalent to `RGBA(0,0,0,0)`); may be used on **any** color property (stroke, fill, or background); not restricted to fill/background.

---

### Issue 7 — ~~MEDIUM~~ RESOLVED: Background EBNF implies fixed parameter ordering, contradicting order-independence design principle

**Status: FIXED** in `DSL_grammar_description.md` v1.3

**Location:** Section 3, EBNF rule `<background-params>`

**Description:**
The §1 design principle states parameters are named and order-independent. The old background EBNF rules (`<solid-bg-params>`, `<gradient-bg-params>`, `<image-bg-params>`) enumerated parameters in a fixed positional sequence, contradicting this.

**Fix applied:**
`<background-params>` rewritten to use `<named-param-list>` (the same order-independent mechanism used by all primitives). A comment block documents how the engine distinguishes the three background forms by key presence:

```ebnf
<background-params> ::= <named-param-list>
  (* Parameters are order-independent. Engine distinguishes forms by key presence:
       solid:    'color' present
       gradient: 'color1' and 'color2' present
       image:    'src' present *)
```

The three fixed-order sub-rules (`<solid-bg-params>`, `<gradient-bg-params>`, `<image-bg-params>`) are removed.

---

### Issue 8 — ~~LOW~~ RESOLVED: `output-format=images` file naming convention absent from §6

**Status: FIXED** in `DSL_grammar_description.md` v1.4

**Location:** Section 6 parameter table (`output-format`)

**Description:**
Section 6 described `output-format=images` as producing "one file per frame" but omitted the naming convention required by REQ-0029 (`<frame-id>.png` / `<frame-id>.jpeg`).

**Fix applied:**
The `output-format` description in the §6 parameter table expanded to include the naming rule:

> `images` produces one file per frame named `<frame-id>.png` or `<frame-id>.jpeg` (matching the frame's colorspace; RGBA uses `.png`)

§2 Coverage table: REQ-0029 updated to ✓ (fully covered).

---

### Re-verification Issues (v1.4 — 2026-04-25)

---

### Issue 9 — ~~HIGH~~ RESOLVED: Arithmetic expression grammar missing from EBNF

**Status: FIXED** in `DSL_grammar_description.md` v1.5

**Location:** Section 3, EBNF value-type rules; Section 13.3

**Description:**
Section 13.3 documents that function parameters support arithmetic operators (`+`, `-`, `*`, `/`) within function bodies (e.g., `pos=(x+10, y+5)`, `pos=(x1+(x2-x1)/2, y1+(y2-y1)/2-14)`). However, the formal EBNF had no `<expr>` rule. The `<value>`, `<length>`, and `<point>` rules only allowed numeric literals or identifiers — not compound arithmetic expressions. A parser generator following the EBNF would reject valid function bodies.

**Fix applied:**
Four new EBNF rules added to Section 3, under a new `(* Arithmetic expressions — function bodies only *)` comment block:

```ebnf
<expr>             ::= <expr-term> (('+' | '-') <expr-term>)*
<expr-term>        ::= <expr-factor> (('*' | '/') <expr-factor>)*
<expr-factor>      ::= <length>
                     | <identifier>            (* function parameter reference *)
                     | '(' <expr> ')'
<expr-point>       ::= '(' <expr> ',' <expr> ')'
```

An explanatory comment block was added stating that within `begin_func … end_func` bodies, `<value>`/`<point>`/`<length>` in named params may be replaced by `<expr>`/`<expr-point>`. A matching note was added to the `<func-decl>` rule.

---

### Issue 10 — ~~MEDIUM~~ RESOLVED: `<image-def>` EBNF does not allow trailing terminator

**Status: FIXED** in `DSL_grammar_description.md` v1.5

**Location:** Section 3, EBNF rule `<image-def>`

**Description:**
The rule `'image' <image-param> (<terminator> <image-param>)*` treats `<terminator>` as a **separator** between parameters. A trailing semicolon after the last parameter — as used in every example in the document — would violate this grammar. Examples throughout the document (§5, §6, §17.1–§17.7) consistently write:

```
image width=400px; height=200px; colorspace=RGB; dpi=96; output-format=png;
```

The trailing `;` after `output-format=png` was unparseable under the old rule.

**Fix applied:**
Added optional trailing terminator to the rule:

```ebnf
<image-def> ::= 'image' <image-param> (<terminator> <image-param>)* <terminator>?
```

---

### Issue 11 — ~~LOW~~ RESOLVED: `<frame-attr>` and `<obj-attr>` lack terminator in EBNF

**Status: FIXED** in `DSL_grammar_description.md` v1.5

**Location:** Section 3, EBNF rules `<frame>` and `<obj-template>`

**Description:**
The `<frame>` rule used `<frame-attr>*` and `<obj-template>` used `<obj-attr>*` — with no terminator handling. Yet §2.4 states all statements end with `\n` or `;`, and examples consistently show frame and object attribute statements with trailing semicolons (`hold-time=1000;`, `width: 200px;`). This was inconsistent with the `<drawing-commands>` rule which already uses `(<drawing-stmt> <terminator>?)*`.

**Fix applied:**
Both containing rules updated to use the same optional-terminator pattern:

```ebnf
(* in <frame> *)
(<frame-attr> <terminator>?)*

(* in <obj-template> *)
(<obj-attr> <terminator>?)*
```

---

### Issue 12 — ~~LOW~~ RESOLVED: `image` duplicated in §2.8 reserved keywords list

**Status: FIXED** in `DSL_grammar_description.md` v1.5

**Location:** Section 2.8, Keywords

**Description:**
`image` appeared in the §2.8 reserved keywords list twice — once as a standalone line and once at the end of the primitives line. While both occurrences refer to the same keyword, the duplication was confusing and inconsistent.

**Fix applied:**
Removed the duplicate occurrence; `image` now appears once in the list.

---

### Re-verification Issues (v1.5 — 2026-04-25)

---

### Issue 13 — ~~HIGH~~ RESOLVED: `<string>` non-terminal referenced in EBNF but never defined

**Status: FIXED** in `DSL_grammar_description.md` v1.6

**Location:** Section 3, EBNF rule `<value>`

**Description:**
The `<value>` rule lists `<string>` as an alternative, but no `<string> ::= ...` production rule existed anywhere in the EBNF block. Section 2.6 defines string literals informally in prose only. A parser generator following the EBNF would fail to compile.

**Fix applied:**
Two new EBNF rules added to Section 3, under a `(* String literal *)` comment block:

```ebnf
<string>      ::= '"' <string-char>* '"'
<string-char> ::= <any-UTF8-char-except-backslash-and-double-quote>
               | '\\' ('"' | '\\' | 'n' | 't')
```

---

### Issue 14 — ~~HIGH~~ RESOLVED: `<line-type>` non-terminal referenced in EBNF but never defined

**Status: FIXED** in `DSL_grammar_description.md` v1.6

**Location:** Section 3, EBNF rule `<border-value>`

**Description:**
`<border-value> ::= <line-type> <length> <color>` references `<line-type>` as a non-terminal, but no `<line-type> ::= ...` production existed in the EBNF block. Section 15.2 defines line types in a prose table only (`solid`, `dashed`, `dotted`, `dash-dot`). A parser generator following the EBNF would fail to compile.

**Fix applied:**
Added `<line-type>` production rule at the end of the EBNF block:

```ebnf
<line-type> ::= 'solid' | 'dashed' | 'dotted' | 'dash-dot'
```

---

### Issue 15 — ~~MEDIUM~~ RESOLVED: `<number>` referenced in EBNF block but defined only in §2.7 prose

**Status: FIXED** in `DSL_grammar_description.md` v1.6

**Location:** Section 3, EBNF block; Section 2.7

**Description:**
`<number>` is used in three EBNF rules (`<frame-attr>`, `<image-param>`, `<length>`) but its production `[0-9]+ ('.' [0-9]+)?` appeared only in the §2.7 prose code block, not inside the formal EBNF block in §3. A self-contained EBNF section must define all referenced non-terminals.

**Fix applied:**
Added `<number>` production rule at the end of the EBNF block:

```ebnf
<number> ::= [0-9]+ ('.' [0-9]+)?
```

---

### Issue 16 — ~~MEDIUM~~ RESOLVED: `<number>` redundant in `<value>` — subsumed by `<length>`

**Status: FIXED** in `DSL_grammar_description.md` v1.6

**Location:** Section 3, EBNF rule `<value>`

**Description:**
The `<value>` rule listed both `<number>` and `<length>` as alternatives. Since `<length> ::= <number> <unit>?` with an optional unit, `<length>` already matches any bare `<number>` (unit absent). This made `<number>` a redundant and ambiguous alternative that would cause a parser conflict (shift/reduce or predict/predict ambiguity).

**Fix applied:**
Removed `<number>` from the `<value>` alternatives. `<length>` (which subsumes all bare numbers via optional unit) is retained. The `<value>` rule now starts directly with `<length>`.

---

### Issue 17 — ~~MEDIUM~~ RESOLVED: `<number-0-1>` EBNF rule matches empty string

**Status: FIXED** in `DSL_grammar_description.md` v1.6

**Location:** Section 3, EBNF rule `<number-0-1>`

**Description:**
The old rule `<number-0-1> ::= [0-9]* ('.' [0-9]+)?` has both parts optional: `[0-9]*` can match zero digits and `('.' [0-9]+)?` can be absent. Combined, the rule matches the empty string — making `RGBA(0,0,0,)` (empty alpha) syntactically valid, which it should not be.

**Fix applied:**
Replaced with a two-alternative rule that requires at least one digit:

```ebnf
<number-0-1> ::= [0-9]+ ('.' [0-9]*)?
              |  '.' [0-9]+
              (* 0.0–1.0; at least one digit required *)
```

---

### Issue 18 — ~~LOW~~ RESOLVED: `{n}` repetition notation not documented in EBNF legend

**Status: FIXED** in `DSL_grammar_description.md` v1.6

**Location:** Section 3, EBNF notation legend; `<color>` rule

**Description:**
The `<color>` rule uses `'#' [0-9A-Fa-f]{6}` — the `{6}` is a regex-style fixed-repetition count. The EBNF notation legend listed `*`, `+`, `?`, `( )`, `[ ]` but omitted `{n}`. An implementer unfamiliar with regex notation would not know what `{6}` means.

**Fix applied:**
Added `{n}` to the notation legend:

```
{n}  exactly n repetitions
```

---

### Issue 19 — ~~MEDIUM~~ RESOLVED: Examples use unquoted `font-family=Arial` contrary to `string` type

**Status: FIXED** in `DSL_grammar_description.md` v1.6

**Location:** Section 5 example; Section 12.5 example; Section 17.3 example

**Description:**
Section 10 specifies `font-family` as type `string`, which requires double-quote delimiters per the string grammar. However, three examples used unquoted `font-family=Arial`:

- §5: `font(font-family=Arial, ...)` — should be `"Arial"`
- §12.5: `font(font-family=Arial, ...)` — should be `"Arial"`
- §17.3: `font(font-family=Arial, ...)` — should be `"Arial"`

Unquoted identifiers are not strings and would be a parse error under the grammar.

**Fix applied:**
All three occurrences corrected to `font-family="Arial"`.

---

### Issue 20 — ~~LOW~~ RESOLVED: §4 prose “defined before it is used” contradicts two-pass execution model

**Status: FIXED** in `DSL_grammar_description.md` v1.6

**Location:** Section 4, first paragraph

**Description:**
The opening sentence of §4 stated:

> Statements may appear in any order, subject to the constraint that a name must be **defined before it is used**.

However, the two-pass execution model described in the same section (Pass 1 collects all object/function definitions, Pass 2 executes frames) makes ALL object templates and function declarations available before any frame is executed — regardless of their position in the file. Forward references are therefore valid, directly contradicting the “defined before use” constraint.

**Fix applied:**
Replaced the contradictory sentence with an accurate description of the two-pass model:

> Thanks to the two-pass processing model, object templates and function declarations may appear in **any order** relative to their call sites within the same script. `include` directives are resolved in Pass 1; any referenced file must exist and be readable at parse time.

---

### Issue 21 — ~~HIGH~~ RESOLVED: Transform application order references undefined `translate` parameter

**Status: FIXED** in `DSL_grammar_description.md` v1.7

**Location:** Section 8.0, transform application order sentence

**Description:**
§8.0 stated: “Transform application order: **translate → scale → skew → rotate**.” However, no `translate` parameter is defined anywhere in the transform parameter table or the rest of the document. The four defined transform parameters are `rotate`, `skew-x`, `skew-y`, and `scale`. An implementer following the spec would find an undefined step in the transform pipeline.

**Fix applied:**
Replaced “translate” with “position” and added a clarifying note: position is established by each primitive’s own positioning parameter (`pos`, `center`, `start`/`end`, or `points`) — not by a separate transform parameter.

---

### Issue 22 — ~~HIGH~~ RESOLVED: Identifier-hyphen vs subtraction operator ambiguity

**Status: FIXED** in `DSL_grammar_description.md` v1.7

**Location:** Section 2.5 (Identifiers), Section 13.3 (Arithmetic Expressions)

**Description:**
Identifiers may contain hyphens (`[A-Za-z_][A-Za-z0-9_-]*`). The arithmetic expression grammar in function bodies uses `-` as subtraction. The combination creates a lexical ambiguity: `x-10` could be parsed as the identifier `x-10` or the expression `x − 10`. No disambiguation rule existed.

**Fix applied:**
Added a disambiguation note to both §2.5 and §13.3: inside expression contexts, `-` is treated as part of an identifier only when **not preceded by whitespace** (maximal-munch). To express subtraction, surround `-` with at least one space on each side.

---

### Issue 23 — ~~MEDIUM~~ RESOLVED: Circular `include` causes undefined behaviour

**Status: FIXED** in `DSL_grammar_description.md` v1.7

**Location:** Section 14 (Include Statement), Section 18.1 (Parse Errors)

**Description:**
§14 stated “there is no depth limit” for nested includes but said nothing about circular includes (A includes B includes A), which would cause infinite recursion at parse time. The error table in §18.1 also had no entry for this condition.

**Fix applied:**
Added sentence to §14: circular includes are detected at parse time and result in a parse error. Added corresponding error entry to §18.1 error table.

---

### Issue 24 — ~~MEDIUM~~ RESOLVED: Zero-parameter functions and zero-argument calls impossible per grammar

**Status: FIXED** in `DSL_grammar_description.md` v1.7

**Location:** Section 3 EBNF, `<param-names>` and `<arg-list>` rules

**Description:**
`<param-names> ::= <identifier> (',' <identifier>)*` requires ≥1 parameter. `<arg-list> ::= <value> (',' <value>)*` requires ≥1 argument. Zero-parameter functions (e.g., `begin_func draw_box()`) and their zero-argument calls are valid use cases but impossible per the grammar.

**Fix applied:**
Both rules updated to include an empty alternative (`| (* empty *)`).

---

### Issue 25 — ~~MEDIUM~~ RESOLVED: `%` unit undefined when object template has no dimensions

**Status: FIXED** in `DSL_grammar_description.md` v1.7

**Location:** Section 15.3 (Unit Measurements), `%` row

**Description:**
§15.3 defined `%` as “percentage of parent container”. Object template `width` and `height` are optional. When a template declares no dimensions, there is no parent container size to resolve `%` against. The fallback was undefined.

**Fix applied:**
Added note to the `%` row: when inside an object template that declares no `width`/`height`, `%` resolves relative to the canvas dimensions.

---

### Issue 26 — ~~MEDIUM~~ RESOLVED: `none` on stroke property called “parse error” but grammar accepts it

**Status: FIXED** in `DSL_grammar_description.md` v1.7

**Location:** Section 15.1 (Color Values), Section 18.1 (Parse Errors)

**Description:**
§15.1 stated: “Using `none` on a stroke property is a **parse error**.” However, the EBNF `<color>` rule includes `none` as a valid alternative unconditionally — so it is syntactically legal. The rejection must happen at semantic validation, not during parsing. Also missing from the §18.1 error table.

**Fix applied:**
Changed “parse error” to “semantic error” in §15.1 with a clarifying note. Added entry to §18.1 error table.

---

### Issue 27 — ~~MEDIUM~~ RESOLVED: Connector `points` + `start`/`end` conflict has no defined error

**Status: FIXED** in `DSL_grammar_description.md` v1.7

**Location:** Section 9.1 (Connector Points / Routing), Section 18.1 (Parse Errors)

**Description:**
§9.1 stated “either `points` or both `start`+`end` must be supplied” but defined no behaviour when BOTH are provided simultaneously. No error was listed in §18.1.

**Fix applied:**
Added to §9.1 footnote: specifying both is a parse error. Added entry to §18.1 error table.

---

### Issue 28 — ~~MEDIUM~~ RESOLVED: Function argument count mismatch has no defined error

**Status: FIXED** in `DSL_grammar_description.md` v1.7

**Location:** Section 18.1 (Parse Errors)

**Description:**
§13.2 states arguments are passed positionally. But no error condition was defined for too-few or too-many arguments at a call site. This is a fundamental semantic constraint that must be enforced by the engine.

**Fix applied:**
Added entry to §18.1 error table: function argument count mismatch → `'<name>' expects <n> argument(s), got <m>`.

---

### Issue 29 — ~~LOW~~ RESOLVED: `hold-time` and `dpi` typed as “integer” but grammar uses `<number>`

**Status: FIXED** in `DSL_grammar_description.md` v1.7

**Location:** Section 5 frame attribute table (`hold-time`), Section 6 image canvas table (`dpi`)

**Description:**
Both parameters are described as “integer” in their prose tables, but the EBNF uses `<number>` (which allows decimals). No `<integer>` type exists in the grammar. So `hold-time=500.5` or `dpi=96.5` are syntactically valid despite the integer description.

**Fix applied:**
Changed type label to `number` in both tables and added note: decimal values are truncated to integer.

---

### Issue 30 — ~~LOW~~ RESOLVED: §12.4 says “nested object coordinates” but should cover all drawing commands

**Status: FIXED** in `DSL_grammar_description.md` v1.7

**Location:** Section 12.4 (Nested Objects)

**Description:**
§12.4 stated: “Nested object coordinates are relative to the parent object’s top-left corner.” The phrase “nested object coordinates” is ambiguous — it should explicitly cover ALL drawing commands inside a template (primitives, function calls), not just nested object instantiations.

**Fix applied:**
Rewrote to: “All drawing-command coordinates inside an object template — primitives, nested object instantiations, and function calls — are relative to the object’s own top-left corner.”

---

### Issue 31 — ~~LOW~~ RESOLVED: `fill` on `line` and `path` missing from error table

**Status: FIXED** in `DSL_grammar_description.md` v1.7

**Location:** Section 18.1 (Parse Errors)

**Description:**
§8.1 says `line` is “Stroke only — no fill” and §8.5 says the same for `path`. §8.7 explicitly states “Specifying `fill` on an `arc` is a parse error” and §18.1 has an entry for it. But the analogous errors for `line` and `path` were absent from the error table.

**Fix applied:**
Added `fill` on `line` and `fill` on `path` entries to the §18.1 error table.

---

## 4. Issue Summary

| # | Severity | Location | Description | Status |
|---|---|---|---|---|
| 1 | ~~High~~ | §3 EBNF `<frame-attr>`, `<obj-attr>` | Undefined `<key>` token | **RESOLVED** |
| 2 | ~~High~~ | §3 EBNF `<obj-attr>` | `shadow`, `clip-bounds`, `clip-shape` missing | **RESOLVED** |
| 3 | ~~High~~ | §3 EBNF `<border-value>` | `shadow` incorrectly nested inside `border` | **RESOLVED** |
| 4 | ~~Medium~~ | §3 `<named-color>`, §15.1 | `none` not in color grammar | **RESOLVED** |
| 5 | ~~Medium~~ | §16.2 table, §17.2 notes | `output-format` default contradiction | **RESOLVED** |
| 6 | ~~Medium~~ | §15.1, §3 `<named-color>` | `transparent` vs `none` semantics undocumented | **RESOLVED** |
| 7 | ~~Medium~~ | §3 `<gradient-bg-params>`, `<image-bg-params>` | Background EBNF implies fixed param ordering | **RESOLVED** |
| 8 | ~~Low~~ | §6 `output-format`, §2 Coverage | `output-format=images` file naming missing | **RESOLVED** |
| 9 | ~~High~~ | §3 EBNF value rules; §13.3 | Arithmetic expression grammar missing from EBNF | **RESOLVED** |
| 10 | ~~Medium~~ | §3 EBNF `<image-def>` | `<image-def>` doesn't allow trailing terminator | **RESOLVED** |
| 11 | ~~Low~~ | §3 EBNF `<frame>`, `<obj-template>` | `<frame-attr>` and `<obj-attr>` lack terminator | **RESOLVED** |
| 12 | ~~Low~~ | §2.8 Keywords | `image` duplicated in reserved keywords list | **RESOLVED** |
| 13 | ~~High~~ | §3 EBNF `<value>` | `<string>` referenced but never defined in EBNF | **RESOLVED** |
| 14 | ~~High~~ | §3 EBNF `<border-value>` | `<line-type>` referenced but never defined in EBNF | **RESOLVED** |
| 15 | ~~Medium~~ | §3 EBNF block, §2.7 | `<number>` not defined in EBNF block | **RESOLVED** |
| 16 | ~~Medium~~ | §3 EBNF `<value>` | `<number>` redundant in `<value>` (subsumed by `<length>`) | **RESOLVED** |
| 17 | ~~Medium~~ | §3 EBNF `<number-0-1>` | `<number-0-1>` matches empty string | **RESOLVED** |
| 18 | ~~Low~~ | §3 notation legend, `<color>` | `{n}` notation not documented in EBNF legend | **RESOLVED** |
| 19 | ~~Medium~~ | §5, §12.5, §17.3 examples | Unquoted `font-family=Arial` contradicts `string` type | **RESOLVED** |
| 20 | ~~Low~~ | §4 prose | "Defined before use" contradicts two-pass execution model | **RESOLVED** |
| 21 | ~~High~~ | §8.0 transform order | `translate` listed in transform order but no such parameter exists | **RESOLVED** |
| 22 | ~~High~~ | §2.5, §13.3 | Identifier-hyphen vs subtraction operator ambiguity in expressions | **RESOLVED** |
| 23 | ~~Medium~~ | §14, §18.1 | Circular `include` causes undefined behaviour (no detection rule) | **RESOLVED** |
| 24 | ~~Medium~~ | §3 EBNF `<param-names>`, `<arg-list>` | Zero-parameter functions and zero-argument calls impossible | **RESOLVED** |
| 25 | ~~Medium~~ | §15.3 `%` unit | `%` undefined when object template declares no `width`/`height` | **RESOLVED** |
| 26 | ~~Medium~~ | §15.1, §18.1 | `none` on stroke called “parse error” but grammar accepts it syntactically | **RESOLVED** |
| 27 | ~~Medium~~ | §9.1, §18.1 | Connector `points` + `start`/`end` conflict has no defined error | **RESOLVED** |
| 28 | ~~Medium~~ | §18.1 | Function argument count mismatch has no defined error | **RESOLVED** |
| 29 | ~~Low~~ | §5 `hold-time`, §6 `dpi` | Parameters typed as “integer” but EBNF allows decimals | **RESOLVED** |
| 30 | ~~Low~~ | §12.4 | “Nested object coordinates” should cover all drawing commands | **RESOLVED** |
| 31 | ~~Low~~ | §18.1 | `fill` on `line` and `path` missing from error table | **RESOLVED** |

**High issues: 0 (open) + 8 (resolved) | Medium issues: 0 (open) + 14 (resolved) | Low issues: 0 (open) + 9 (resolved)**

**All 31 issues resolved. Document is ready for use.**

---

## 5. Recommendation

Issues 1–12 are fully resolved. The EBNF structural errors, default-value contradictions, background ordering, output naming, terminator handling, and keyword duplication have all been corrected.

Eight new issues were identified during re-verification of v1.5:

- **Issue 13** (High): ~~`<string>` referenced in `<value>` EBNF but never defined.~~ **RESOLVED.**
- **Issue 14** (High): ~~`<line-type>` referenced in `<border-value>` EBNF but never defined.~~ **RESOLVED.**
- **Issue 15** (Medium): ~~`<number>` used in EBNF block but only defined in §2.7 prose.~~ **RESOLVED.**
- **Issue 16** (Medium): ~~`<number>` redundant in `<value>` alternatives (subsumed by `<length>`).~~ **RESOLVED.**
- **Issue 17** (Medium): ~~`<number-0-1>` matches empty string; at-least-one-digit constraint missing.~~ **RESOLVED.**
- **Issue 18** (Low): ~~`{n}` repetition notation undocumented in EBNF legend.~~ **RESOLVED.**
- **Issue 19** (Medium): ~~Unquoted `font-family=Arial` in §5, §12.5, §17.3 examples contradicts `string` type.~~ **RESOLVED.**
- **Issue 20** (Low): ~~§4 "defined before it is used" contradicts the two-pass execution model.~~ **RESOLVED.**

Eleven new issues were identified during semantic correctness review of v1.6:

- **Issue 21** (High): ~~`translate` listed in transform order but not defined as a parameter.~~ **RESOLVED.**
- **Issue 22** (High): ~~Identifier-hyphen vs subtraction ambiguity in expression contexts.~~ **RESOLVED.**
- **Issue 23** (Medium): ~~Circular `include` not detected; undefined behaviour.~~ **RESOLVED.**
- **Issue 24** (Medium): ~~Zero-parameter functions and zero-argument calls impossible per grammar.~~ **RESOLVED.**
- **Issue 25** (Medium): ~~`%` unit undefined when object template has no explicit dimensions.~~ **RESOLVED.**
- **Issue 26** (Medium): ~~`none` on stroke labelled “parse error” but grammar accepts it syntactically.~~ **RESOLVED.**
- **Issue 27** (Medium): ~~Connector `points` + `start`/`end` conflict undefined.~~ **RESOLVED.**
- **Issue 28** (Medium): ~~Function argument count mismatch has no defined error.~~ **RESOLVED.**
- **Issue 29** (Low): ~~`hold-time`/`dpi` typed as integer but grammar uses `<number>`.~~ **RESOLVED.**
- **Issue 30** (Low): ~~§12.4 coordinate scope limited to “nested objects” instead of all drawing commands.~~ **RESOLVED.**
- **Issue 31** (Low): ~~`fill` on `line` and `path` missing from §18.1 error table.~~ **RESOLVED.**

All 31 issues are resolved. The document (`DSL_grammar_description.md` v1.7) is ready for use as the basis for parser generation and implementation.

---
## Changelog

### 2026-04-25 11:32:44 — Resolve Issue 1
- Issue 1 (High — undefined `<key>` token) marked as RESOLVED. Fix was applied to `2_Docs/DSL_grammar_description.md` v1.1: catch-all `<key>` alternatives removed from `<frame-attr>` and `<obj-attr>` EBNF rules.
- Issue summary table updated with Status column.
- File version bumped to 1.1.

### 2026-04-25 11:37:39 — Resolve Issue 2
- Issue 2 (High — `shadow`, `clip-bounds`, `clip-shape` missing from `<obj-attr>` EBNF) marked as RESOLVED. Fix was applied to `2_Docs/DSL_grammar_description.md` v1.1: all three attributes added as explicit alternatives in the `<obj-attr>` rule.
- Issue summary table updated.
- File version bumped to 1.2.

### 2026-04-25 11:38:57 — Resolve Issue 3
- Issue 3 (High — `shadow` incorrectly nested inside `<border-value>`) marked as RESOLVED. Fix was applied to `2_Docs/DSL_grammar_description.md` v1.1: `<border-value>` simplified to `<line-type> <length> <color>`; `shadow` moved to standalone `<obj-attr>` alternative.
- Issue summary table updated: all High issues now resolved.
- File version bumped to 1.3.

### 2026-04-25 11:40:06 — Resolve Issue 4
- Issue 4 (Medium — `none` not in `<color>` EBNF) marked as RESOLVED. Fix was applied to `2_Docs/DSL_grammar_description.md` v1.1: `'none'` added as an explicit `<color>` alternative with fill-only annotation; Section 15.1 prose clarified.
- Issue summary table updated.
- File version bumped to 1.4.

### 2026-04-25 11:41:09 — Resolve Issue 5
- Issue 5 (Medium — `output-format` default contradiction) marked as RESOLVED. Fix was applied to `2_Docs/DSL_grammar_description.md` v1.1: Section 6 and Section 16.2 now both state the context-sensitive default rule (single-frame → `png`; multi-frame → `gif`); consistent with Section 17.2 example note.
- All 5 issues resolved. Issue summary table updated with final counts.
- File version bumped to 1.5.

### 2026-04-25 11:46:12 — Re-verification of DSL grammar description v1.1
- Verified `2_Docs/DSL_grammar_description.md` v1.1 against `2_Docs/requirements.md` v1.5 and `2_Docs/my_vision.md`.
- §1 Scope updated to reflect v1.1 re-verification.
- §2 Coverage: REQ-0029 updated to ⚠ (partial — naming convention missing).
- 3 new issues found: Issue 6 (Medium — `transparent`/`none` semantics), Issue 7 (Medium — background EBNF parameter ordering), Issue 8 (Low — output file naming).
- §3 new issues added, §4 summary table extended with rows 6–8, stats and recommendation updated.
- File version bumped to 1.6.

### 2026-04-25 11:49:42 — Resolve Issue 6
- Issue 6 (Medium — `transparent`/`none` semantic difference undocumented) marked as RESOLVED. Fix applied to `2_Docs/DSL_grammar_description.md` v1.2: Section 15.1 expanded with explicit bullet points distinguishing `none` (no-paint, fill/background-only, parse error on stroke) from `transparent` (general named color, any property).
- Issue summary table updated. §5 Recommendation updated.
- File version bumped to 1.7.

### 2026-04-25 11:52:21 — Resolve Issue 7
- Issue 7 (Medium — background EBNF parameter ordering contradicts order-independence principle) marked as RESOLVED. Fix applied to `2_Docs/DSL_grammar_description.md` v1.3: `<background-params>` rewritten to use `<named-param-list>`; three fixed-order sub-rules removed; comment block added to document key-presence disambiguation.
- Issue summary table updated: all Medium issues resolved.
- File version bumped to 1.8.

### 2026-04-25 12:43:00 — Semantic correctness review of DSL grammar description v1.6 (Issues 21–31)
- Performed semantic correctness review of `2_Docs/DSL_grammar_description.md` v1.6.
- 11 new issues found (21–31): 2 High, 6 Medium, 3 Low — all resolved in DSL grammar doc v1.7.
- §1 Scope updated to reflect v1.6 semantic review.
- §3 extended with Issue 21–31 blocks. §4 summary table extended to 31 rows (8H/14M/9L all resolved). §5 recommendation updated.
- Report file version bumped to 2.2.

### 2026-04-25 12:08:40 — Re-verification of DSL grammar description v1.5 (Issues 13–20)
- Verified `2_Docs/DSL_grammar_description.md` v1.5 against `2_Docs/requirements.md` v1.5 and `2_Docs/my_vision.md`.
- §1 Scope updated to reflect v1.5 re-verification.
- 8 new issues found and resolved: Issue 13 (High — `<string>` undefined), Issue 14 (High — `<line-type>` undefined), Issue 15 (Medium — `<number>` not in EBNF block), Issue 16 (Medium — `<number>` redundant in `<value>`), Issue 17 (Medium — `<number-0-1>` matches empty), Issue 18 (Low — `{n}` notation undocumented), Issue 19 (Medium — unquoted font-family in examples), Issue 20 (Low — §4 forward-reference contradiction).
- §3 extended with Issue 13–20 blocks; §4 summary table extended to 20 rows; stats updated to 6H/8M/6L all resolved; §5 recommendation updated.
- Report file version bumped to 2.1.

### 2026-04-25 12:01:19 — Re-verification of DSL grammar description v1.4 (Issues 9–12)
- Verified `2_Docs/DSL_grammar_description.md` v1.4 against `2_Docs/requirements.md` v1.5 and `2_Docs/my_vision.md`.
- §1 Scope updated to reflect v1.4 re-verification.
- 4 new issues found and resolved: Issue 9 (High — arithmetic expression grammar missing), Issue 10 (Medium — `<image-def>` trailing terminator), Issue 11 (Low — frame/obj attr terminators), Issue 12 (Low — duplicate `image` keyword).
- §3 new issue blocks added; §4 summary table extended with rows 9–12; stats updated to 4 High / 4 Medium / 4 Low all resolved.
- §5 Recommendation updated to reflect all 12 issues resolved.
- File version bumped to 2.0.

### 2026-04-25 11:54:44 — Resolve Issue 8
- Issue 8 (Low — `output-format=images` file naming convention absent) marked as RESOLVED. Fix applied to `2_Docs/DSL_grammar_description.md` v1.4: `<frame-id>.png`/`.jpeg` naming rule added to §6 `output-format` parameter table; §2 Coverage REQ-0029 updated to ✓.
- All 8 issues resolved. Issue summary table, stats, and recommendation updated.
- File version bumped to 1.9.
