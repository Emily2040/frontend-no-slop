# 07 — Output Contract

Choose the output format that best fits the request.

## Use `schemas/authoring-base.json` when:
- the user wants a full page plan
- the answer will feed a design or engineering handoff
- multiple sections or components need detailed state coverage

## Use `schemas/runtime-compact.json` when:
- the task is an audit or critique
- the user wants a short machine-readable artifact
- the answer needs quick prioritization

Formatting rules:

- If the user asks for JSON, output valid JSON only.
- If the user wants prose, mirror the same fields in markdown sections.
- Keep evidence and assumptions separate.
- Put the strongest, most actionable changes first.
- Include risk and next-step sequencing.

Final pass:
- Remove any banned phrase.
- Make sure each recommendation is testable on a screen or in code.
- Keep the answer specific enough that another person could implement it without guessing the intent.
