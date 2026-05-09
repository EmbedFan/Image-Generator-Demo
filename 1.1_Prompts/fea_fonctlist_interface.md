# Add Feature FEA-NNN Prompt

Act as a senior software architect.

You are tasked with adding a new feature to the project documents.

---

## FORMAT OF FEATURE REQUEST FILENAMES

  - The first feature request filename is 2_Docs\FEA-001-prompt-<subject>.md
  - The second feature request filename is 2_Docs\FEA-002-prompt-<subject>.md
  - Name files analog the rule above

---

## INPUT DESCRIPTION

Ask the user for the feature description they want to add.

Feature ID: The next feature number, calculated as the maximum existing feature number + 1.

---

## Before anything else — load skills

Read the following skill files now, before any other action:
1. `.github/skills/report-management/SKILL.md`
2. `.github/skills/get-current-timestamp-for-filename/SKILL.md`
3. `.github/skills/get-current-timestamp-for-document/SKILL.md`

---

## TASK

1. Prompt the user for the feature description.
2. Add the feature with ID FEA-001 to the following documents:
   - `2_Docs/my_vision.md`
   - `2_Docs/requirements.md`
   - `2_Docs/system_design.md`
3. For each document, integrate the feature appropriately (e.g., append to relevant sections or create new sections if needed).
4. Update the documents using the report management skill for tracking changes.

---

## RULES

- Follow the feature addition process strictly.
- Do NOT invent details not provided by the user.
- Ensure the feature is clearly described and integrated coherently.
- Use the report management skill to log the changes in the changelog and activity logs.
- **Do not implement code**

---

## OUTPUT

  - Provide a summary of the changes made to each document.
  - 2_Docs\FEA-002-prompt-<subject>.md