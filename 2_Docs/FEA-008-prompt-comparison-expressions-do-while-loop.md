# FEA-008 - Comparison Expressions and `do ... while` Loop Support

| Field | Value |
|---|---|
| **Description** | Add numeric comparison expressions and a safe bounded `do ... while` loop to the DSL |
| **Created at** | 2026-05-07 21:04:48 |
| **File version** | 1.0 |
| **Created by** | GPT-5 Codex |

---

## Overview

This feature extends the DSL with a small, safe control-flow capability for repeated drawing and layout logic. The work is intentionally split into two layers:

1. Add numeric comparison expressions.
2. Add a bounded `do ... while` loop that depends on those comparison expressions.

The goal is to support repeated drawing patterns without turning the DSL into a general-purpose programming language.

---

## Problem Statement

The current DSL supports arithmetic expressions, reusable functions, reusable objects, and sequential variable-driven layout chaining, but it does not support repeated execution.

As a result, repeated drawing must currently be written by hand or generated externally. This makes counter-based rendering patterns verbose and harder to maintain.

The missing prerequisite for a loop is boolean comparison. The engine can evaluate arithmetic expressions, but it cannot currently decide conditions such as:

- `i < 5`
- `counter <= max_count`
- `current_x + width < canvas_limit`
- `gap != 0`

---

## Proposed Feature

### 1. Comparison Expressions

Add comparison operators for numeric expressions:

- `==`
- `!=`
- `<`
- `<=`
- `>`
- `>=`

These operators compare two numeric expressions and produce a boolean result. The first implementation only needs these comparisons anywhere a `do ... while` condition is evaluated.

Example:

```dsl
i < 5
current_x + width <= limit
gap != 0
```

### 2. `do ... while` Loop

Add a post-condition loop that executes the body first and checks the comparison condition after each iteration.

Conceptual syntax:

```dsl
do
  statements
while condition;
```

Example:

```dsl
begin_frame loop_demo
  image width=400px; height=200px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  var i;
  i = 0;

  do
    circle(color=black, fill=blue, center=(50 + i * 40, 100), radius=12);
    i = i + 1;
  while i < 5;
end_frame
```

This draws five circles.

---

## Scope Rules

The loop is intentionally limited in the first version.

Allowed scopes:

- `begin_frame ... end_frame`
- `begin_func ... end_func`

Forbidden scopes:

- `begin_obj ... end_obj`
- `begin_palette ... end_palette`
- top-level script scope

Using `do ... while` in a forbidden scope must produce a clear parse error with file and line information.

---

## Runtime Safety

Each `do ... while` loop must be protected by a fixed engine-level max-iteration guard.

First-version rule:

- default maximum iteration count: `1000`

If the guard is exceeded, execution stops with a runtime error such as:

```text
main.dsl:42: error: do-while loop exceeded maximum iteration count 1000
```

This keeps the feature safe even when the condition never becomes false.

---

## Execution Rules

Inside a permitted scope, loop body statements execute sequentially in declaration order. The loop body may contain:

- variable declarations if valid in that scope
- variable assignments
- primitive drawing commands
- named primitive drawing commands
- bbox access after the named primitive has been rendered
- function calls
- object instances, if already valid in the containing scope

The condition is evaluated after each full body execution. The loop stops when the comparison evaluates to false.

---

## Validation and Error Cases

The implementation should reject or report:

- loop without condition
- condition that is not a comparison expression
- unsupported comparison operator
- malformed comparison expression
- loop in object body
- loop in palette body
- loop at top level
- loop exceeding max-iteration guard

All loop-related errors should include file name and line number.

---

## Documentation Updates Required

The following documents should be updated alongside the feature:

| Document | Required update |
|---|---|
| `2_Docs/my_vision.md` | Add comparison expressions and bounded `do ... while` to the language vision |
| `2_Docs/requirements.md` | Add formal requirements and extend grammar coverage |
| `2_Docs/system_design.md` | Add parser, evaluator, loop executor, and guard behavior |
| `2_Docs/DSL_grammar_description.md` | Add comparison grammar, loop grammar, scope restrictions, and error examples |
| `2_Docs/DSL_user_guide.md` | Add examples, function usage, and common mistakes |

---

## Example Scripts Requested

Add 4-6 focused examples:

1. `93_loop_basic_circles.dsl`
2. `94_loop_repeated_rectangles.dsl`
3. `95_loop_with_bbox_chaining.dsl`
4. `96_loop_in_function.dsl`
5. `97_loop_comparison_operators.dsl`
6. `98_loop_guard_error_example.dsl` (optional negative example)

---

## Acceptance Criteria

The feature is considered complete when:

- comparison expressions parse and evaluate correctly
- `do ... while` works in frame bodies
- `do ... while` works in function bodies
- `do ... while` is rejected in object bodies
- `do ... while` is rejected at top level
- infinite loops are stopped by the max-iteration guard
- errors are clear and include file and line information
- 4-6 example scripts are added
- grammar, guide, requirements, and system-design docs are updated
- existing scripts continue to work unchanged

---

## Documents Updated

| Document | Planned changes |
|---|---|
| `2_Docs/my_vision.md` | Add looping and comparison language goals |
| `2_Docs/requirements.md` | Add REQ-0042 through REQ-0043.5; extend grammar requirement |
| `2_Docs/system_design.md` | Add comparison evaluator and loop executor section |
| `2_Docs/DSL_grammar_description.md` | Add comparison and loop grammar plus errors |
| `2_Docs/DSL_user_guide.md` | Add loop examples and common mistakes |
