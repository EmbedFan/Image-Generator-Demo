# ImageGenerator Demo

This repository is a demonstration project for using AI during a complex software design and implementation process.

It showcases not only a working software artifact, but also the structured path used to create it: prompts, requirements, system design, implementation guidance, reports, and example outputs. The result is a transparent, traceable development workflow where AI is used as a practical engineering partner rather than a black box.

## What This Demo Contains

The demo centers around a Technical Image Generator implemented in Python. The project includes:

- A runnable CLI entry point in `imagegen.py`
- The core Python package in `imagegen/`
- Documentation covering requirements, design, grammar, and user guidance in `2_Docs/`
- Prompt assets used across the development lifecycle in `1.1_Prompts/` and `1.2_WorkingPrompts/`
- Verification reports and change logs in `3_Reports/`
- Example scripts in `4_ExampleScripts/`
- Include assets in `5_Includes/`

## Why This Project Exists

This demo is intended to show how AI can support a serious software effort in a disciplined way.

Instead of using AI only for isolated code generation, this project demonstrates a broader workflow:

- turning vision into structured requirements
- transforming requirements into system design
- implementing code from documented architecture
- generating reference documentation and examples
- reviewing, verifying, and iterating with traceability

The repository is therefore both:

- a software project
- a process demonstration for AI-assisted engineering

## Project Structure

- `1.1_Prompts/`: step-by-step prompts for requirements, design, implementation, reference generation, examples, and verification
- `1.2_WorkingPrompts/`: working prompt material used during generation workflows
- `2_Docs/`: main project documentation, including requirements, system design, DSL grammar, user guide, and API reference
- `3_Reports/`: verification artifacts, completeness reviews, gap reports, and changelogs
- `4_ExampleScripts/`: example DSL scripts for the image generator
- `5_Includes/`: shared include files used by scripts
- `imagegen/`: Python implementation of the engine
- `imagegen.py`: CLI entry point
- `requirements.txt`: Python dependency list

## How To Run

1. Create and activate a Python 3.10+ environment.
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the generator with a DSL script:

```powershell
python imagegen.py <input.dsl>
```

4. Optionally list available fonts:

```powershell
python imagegen.py --list-fonts
```

## Recommended Reading Order

If you want to understand the full AI-assisted workflow, this is a good reading path:

1. `2_Docs/my_vision.md`
2. `2_Docs/requirements.md`
3. `2_Docs/system_design.md`
4. `2_Docs/implementation.md`
5. `2_Docs/DSL_grammar_description.md`
6. `2_Docs/DSL_user_guide.md`
7. `3_Reports/`

If you want to focus on the runnable product first, start with:

1. `imagegen.py`
2. `imagegen/`
3. `4_ExampleScripts/`
4. `2_Docs/DSL_user_guide.md`

## What This Demonstrates About AI

This demo highlights several practical uses of AI in software engineering:

- requirements elaboration
- architecture drafting
- code generation and refactoring
- technical documentation generation
- example creation
- verification support
- iteration with explicit project memory in reports and changelogs

The key idea is that AI becomes more valuable when the work is structured, reviewed, and documented at every stage.

## Demo Scope

This is a public demo version of the project. It is designed to communicate the workflow, structure, and engineering approach clearly, while remaining useful as a standalone technical artifact.

## Author

Created by Attila Gallai using an AI-aided software development process.
