# Create DSL language user guide

Act as professional developer and tech-writer

---

## Before anything else — load skills

Read all three skill files now, before any other action:
1. `.github/skills/report-management/SKILL.md`
2. `.github/skills/get-current-timestamp-for-filename/SKILL.md`
3. `.github/skills/get-current-timestamp-for-document/SKILL.md`

---

## Task
  
  Create a user guide for DSL language defined in this project.
  The output too large so slice the work into lesser parts.
  Create the output file in smaller part. Create output sections - described "Structure of DSL User Guide" section caption by caption.
  To work comprehensive firs create a todo list for every little working part. 

---

## Restrictions

  - Do not guess anything, use the provided inputs as an information source.
  - If do not know anythig, any thing not clear, ask a question.

--

## Input

  Read file:
    - 2_Docs\DSL_grammar_description.md
    - 2_Docs\requirements.md
    - 2_Docs\system_design.md

  ** CRITICAL: Do not use any other files! **

---

## Output
 
 Write the human readable user guide into file: 2_Docs\DSL_scripting_user_guide.md

--

## Structure of DSL User Guide

### 1. Introduction
   - Overview of Technical Image Generator DSL
   - What can be created (images, animations, technical diagrams)
   - Key capabilities summary
   - System requirements

### 2. Getting Started
   - Installation and setup
   - First script (Hello World example)
   - Running the generator (CLI usage)
   - Output formats

### 3. Language Fundamentals
   - DSL Syntax basics
   - Comments and whitespace
   - Case sensitivity
   - Statement terminators (newlines vs semicolons)
   - Parameters and values
   - Units system (px, pt, em, cm, mm, %)

### 4. Frame Definition
   - Frame syntax (begin_frame/end_frame)
   - Image parameters (width, height, colorspace, dpi, output-format)
   - Frame parameters (hold-time, frame-mode)
   - Single vs multi-frame scripts
   - Example: Creating a simple frame

### 5. Colors and Styling
   - Color formats (RGB, RGBA, hex, named colors)
   - Color syntax and validation
   - Line styles (solid, dashed, dotted, dash-dot)
   - Line width specification
   - Stroke vs fill

### 6. Primitives - Drawing Shapes
   - **Line** - Rendering line segments
   - **Circle** - Creating circles with optional fill
   - **Square** - Drawing rectangles
   - **Polygon** - Multi-point closed shapes
   - **Path** - Open polylines
   - **Pie** - Arc and pie slices
   - **Connector** - Lines with arrow endpoints
   - **Text/Font** - Rendering text with typography options
   - **Image** - Embedding external images
   - For each: syntax, parameters, examples

### 7. Object Templates and Reuse
   - Defining objects (begin_obj/end_obj)
   - Object parameters
   - Nesting objects within objects
   - Object instantiation
   - Parameter overrides
   - Template defaults vs instance values
   - Example: Creating reusable UI components

### 8. Transformations
   - Scale transformation (REQ-0018)
   - Skew transformation (REQ-0017)
   - Rotate transformation (REQ-0016)
   - Transform order and stacking
   - Combining multiple transforms
   - Examples with visual descriptions

### 9. Clipping and Masking
   - Rectangular clipping (bounds)
   - Shape-based clipping (circle, square, polygon)
   - Combining multiple clips
   - Practical use cases
   - Examples

### 10. Backgrounds
   - Solid color backgrounds
   - Gradient backgrounds (linear interpolation)
   - Image backgrounds with sizing modes (fit, stretch, clip)
   - Image opacity
   - Z-order (backgrounds render first)
   - Examples

### 11. Functions
   - Function definition syntax
   - Function parameters
   - Function calls and invocation
   - Parameter substitution
   - Scope and visibility
   - Nested function calls
   - Circular call prevention
   - Examples

### 12. Script Inclusion and Modularity
   - Include directive syntax
   - Relative vs absolute paths
   - Multiple includes
   - Circular reference detection
   - Include scope and visibility
   - Organizing large projects
   - Best practices for modularity
   - Examples

### 13. Backgrounds - Advanced
   - Supported image formats (PNG, JPEG, GIF, SVG)
   - Image path resolution
   - Sizing modes explained (fit, stretch, clip)
   - Opacity and transparency
   - Error handling for missing images

### 14. Animation
   - Frame timing (hold-time parameter)
   - Animation modes (one-run vs cyclic-run)
   - Multi-frame GIF generation
   - Frame sequencing
   - Examples: Creating simple animations

### 15. Complete Examples
   - Simple shape composition
   - Complex diagram with nested objects
   - Animated sequence
   - Button UI component with reuse
   - Multi-file project with includes
   - Real-world technical diagram

### 16. Error Messages and Troubleshooting
   - Common syntax errors
   - Validation errors
   - File I/O errors
   - Rendering errors
   - How to read error messages
   - Tips for debugging

### 17. Parameter Reference
   - Complete parameter list by primitive type
   - Required vs optional parameters
   - Valid value ranges
   - Unit conversion table
   - Default values
   - Type specifications

### 18. Quick Reference
   - Syntax cheat sheet
   - Primitive types quick reference
   - Common patterns
   - Color palette reference
   - Unit conversion quick reference

### 19. Best Practices
   - Naming conventions
   - Code organization
   - Performance tips
   - When to use objects vs functions
   - When to use includes
   - Common pitfalls to avoid

### 20. Appendix
   - Glossary of terms
   - Color name reference
   - Font families and fallback chains
   - Arrow types reference
   - Line style patterns
   - Coordinate system explanation

--
