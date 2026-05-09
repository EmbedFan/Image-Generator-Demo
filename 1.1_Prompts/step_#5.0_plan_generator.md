# AI Prompt – Test Implementation Plan Generator (REQ-XXXX)

## Role
Act as a **senior software architect, QA architect, and senior developer**.

---

## Before anything else — load skills

Read all three skill files now, before any other action:
1. `.github/skills/report-management/SKILL.md`
2. `.github/skills/get-current-timestamp-for-filename/SKILL.md`
3. `.github/skills/get-current-timestamp-for-document/SKILL.md`

---

## Task
Generate a **short, structured, implementation-oriented test plan** from a prebuilt requirement document that uses **REQ-XXXX identifiers**.

---

## Input
- A requirement document containing items formatted like:
  - `REQ-0001`
  - `REQ-0002`
- Each requirement may include:
  - Title
  - Description
  - Priority
  - Acceptance Criteria
  - Notes

---

## Goal
Create a **concise test implementation plan** that maps requirements into **practical testing work**.

---

## Instructions

1. Read all `REQ-XXXX` requirements.
2. Group related requirements into **logical test modules**.
3. For each module, define:
   - **Module name**
   - **Covered requirement IDs**
   - **Test objective**
   - **Recommended test level**:
     - Unit
     - Integration
     - System
     - UI
     - Regression
   - **Short implementation approach**
   - **Key dependencies / prerequisites**
4. Identify:
   - Untestable or ambiguous requirements
   - Missing testability details
   - High-risk areas requiring early testing
5. Keep the output:
   - Short
   - Technical
   - Implementation-focused
6. Do **not** rewrite the full requirement document.
7. Always reference requirements using **REQ-XXXX IDs**.

---

## Output Format

# Test Implementation Plan

## 1. Overview
Short summary of overall test strategy.

---

## 2. Test Modules

For each module provide:

- **Module:**
- **Requirement IDs:**
- **Objective:**
- **Test Level:**
- **Implementation Notes:**
- **Dependencies:**

---

## 3. Risks and Gaps

- Ambiguous requirements
- Missing acceptance details
- High-risk areas

---

## 4. Recommended Execution Order

Provide a short, ordered list describing the suggested testing sequence.

---

## Important Notes

- Be **precise and practical**
- Keep the plan **concise**
- Maintain **requirement traceability**
- Do **not invent requirements** not present in the source document