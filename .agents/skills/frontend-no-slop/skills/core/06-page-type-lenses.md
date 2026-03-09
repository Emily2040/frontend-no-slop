# 06 — Page-Type Lenses

Use `registry/page-type-lenses.json` to choose the main lens for the request.

Rules:

1. Pick one primary page type and at most one secondary page type.
2. Apply the critical elements and failure modes from that lens.
3. Use `registry/frontend-evidence-prompts.json` if the brief is thin.
4. Do not force landing-page advice onto dashboards or app-shell advice onto docs.

Examples:

- A landing page must clarify promise, proof, objection handling, and CTA path.
- A dashboard must expose current state, filters, change over time, and meaningful actions.
- A settings surface must prevent accidental damage and explain side effects.
- Docs must optimize findability, scanability, examples, and copy-paste success.

If the page type is mixed, say so explicitly and show which lens governs the first viewport.
