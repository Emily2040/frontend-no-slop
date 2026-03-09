# Frontend No-Slop Orchestrator

When this skill is invoked, do the following:

1. Identify the task mode: `design`, `critique`, `refactor`, `implementation-plan`, `design-system`, or `copy-rewrite`.
2. Identify the main page or surface type.
3. Load `skills/core/01-intake-and-grounding.md`.
4. Load `registry/forbidden-slop.json` and `skills/core/02-slop-scrubber.md`.
5. Load `skills/core/03-layout-and-visual-logic.md` for page flow, hierarchy, spacing, responsive structure, and visual reasoning.
6. Load `skills/core/04-component-state-discipline.md` for interactive components, forms, data tables, menus, dialogs, and state coverage.
7. Load `skills/core/05-a11y-performance-content.md` when the task touches accessibility, copy, semantics, responsiveness, or performance.
8. Load `registry/page-type-lenses.json`, `registry/frontend-evidence-prompts.json`, and `skills/core/06-page-type-lenses.md`.
9. Load `skills/core/07-output-contract.md` and choose the output shape:
   - `schemas/authoring-base.json` for deep specs, handoff plans, and larger design responses.
   - `schemas/runtime-compact.json` for audits, quick critiques, and short machine-readable output.

Non-negotiable rules:

- Ground every claim in the prompt, code, screenshot, repository context, or a clearly labeled low-risk assumption.
- Do not invent brands, metrics, customer quotes, testimonials, motion, or product capabilities.
- Translate abstract taste language into layout, hierarchy, copy, semantics, accessibility, state, and implementation details.
- Surface empty, loading, error, success, disabled, and mobile states whenever they matter.
- Prefer practical advice that can survive contact with a real codebase.

Before finalizing, self-check:

- Is the output specific enough to build?
- Did any sentence hide behind style adjectives?
- Are the main user task, primary CTA, responsive behavior, and state coverage explicit?
- Did you note accessibility and performance risks instead of hand-waving them away?
