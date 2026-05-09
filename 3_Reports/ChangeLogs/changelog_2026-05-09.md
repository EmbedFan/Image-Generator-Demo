# Changelog 2026-05-09

### 2026-05-09 06:44:42 - GPT-5 Codex - documentation update for FEA-009
- File: `2_Docs/my_vision.md`
- Action: Updated
- Details: Added the vision-level split between default object scaling on resize and the new opt-in layout-resize behavior.

### 2026-05-09 06:44:42 - GPT-5 Codex - documentation update for FEA-009
- File: `2_Docs/requirements.md`
- Action: Updated
- Details: Clarified existing object-instance sizing as the default mode and added REQ-0044 through REQ-0044.3 for opt-in layout resizing.

### 2026-05-09 06:44:42 - GPT-5 Codex - documentation update for FEA-009
- File: `2_Docs/system_design.md`
- Action: Updated
- Details: Extended the object instantiator design with separate default and layout-resize execution paths plus updated traceability notes.

### 2026-05-09 06:44:42 - GPT-5 Codex - documentation update for FEA-009
- File: `2_Docs/FEA-009-prompt-decoupled-object-resizing-scaling-behavior.md`
- Action: Created
- Details: Added the new feature prompt document describing the problem, behavior modes, use cases, and documentation impact.

### 2026-05-09 06:44:42 - GPT-5 Codex - planning activity log update
- File: `3_Reports/ChangeLogs/activity_planning.md`
- Action: Updated
- Details: Recorded the documentation activity for FEA-009 and the affected core project documents.

### 2026-05-09 07:04:51 - GPT-5 Codex - feature implementation for FEA-009
- File: `imagegen/rendering/object_instantiator.py`
- Action: Updated
- Details: Added `resize-mode=layout` support so object-instance width/height can redefine layout space without implicit content scaling, while explicit `scale` remains a separate geometric transform.

### 2026-05-09 07:04:51 - GPT-5 Codex - feature implementation for FEA-009
- File: `imagegen/semantic_validator.py`
- Action: Updated
- Details: Validated `resize-mode`, unwrapped expression-wrapped object scale/rotate values, and limited the width/height-plus-scale warning to the default resize path.

### 2026-05-09 07:04:51 - GPT-5 Codex - feature implementation for FEA-009
- File: `imagegen/rendering/bbox_renderer.py`
- Action: Updated
- Details: Updated object-instance AABB logic so layout-resize mode still applies explicit `scale` when width/height overrides are present.

### 2026-05-09 07:04:51 - GPT-5 Codex - feature implementation for FEA-009
- File: `4_ExampleScripts/99_object_layout_resize_panel.dsl`
- Action: Created
- Details: Added a focused example comparing default object scaling, `resize-mode=layout`, and `resize-mode=layout` plus explicit scale.

### 2026-05-09 07:04:51 - GPT-5 Codex - documentation alignment for FEA-009 implementation
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Added `resize-mode` to the object-instance grammar/reference section and documented how precedence changes in layout mode.

### 2026-05-09 07:04:51 - GPT-5 Codex - documentation alignment for FEA-009 implementation
- File: `2_Docs/DSL_user_guide.md`
- Action: Updated
- Details: Added user-facing examples for `resize-mode=layout`, including combined layout resize plus explicit `scale`.

### 2026-05-09 07:04:51 - GPT-5 Codex - implementation activity log update
- File: `3_Reports/ChangeLogs/activity_implementation.md`
- Action: Updated
- Details: Recorded the code, example, documentation, and verification work for the FEA-009 implementation.
