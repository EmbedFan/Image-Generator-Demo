Act as a senior software architect.

Your task is to transform a raw feature description into a structured requirement document.

---

## Before anything else — load skills

Read all three skill files now, before any other action:
1. `.github/skills/report-management/SKILL.md`
2. `.github/skills/get-current-timestamp-for-filename/SKILL.md`
3. `.github/skills/get-current-timestamp-for-document/SKILL.md`

---

## INPUT DESCRIPTION

<PASTE CONTENT OF input_description.md>

---

## TASK

Generate a structured requirement document.

---

## CONSTRAINTS

- Use REQ-0001 incremental ID format
- When required by the granularity use sub requirements, use REQ-0001.1 ... REQ-0001.n 
- Each requirement must be testable and unambiguous
- Avoid vague terms
- Use observable behavior

---

## FOR EACH REQUIREMENT INCLUDE

- ID
- Title
- Description
- Priority (High / Medium / Low)
- Acceptance Criteria
- Dependencies (if any)
- Notes (optional)

---

## STRUCTURE

- Functional
- Non-Functional
- Data
- UI/UX
- Integration

---

## OUTPUT

- Markdown
- Use tables
- No explanations outside the document
