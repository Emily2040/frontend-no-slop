# Frontend No-Slop: 10 concrete ways to improve the repo

This review is grounded in the current repository content and focuses on implementation-ready improvements.

## 1) Add a visible "Quick start" path in `README.md`
- **Why:** The README explains architecture well, but a first-time user still has to infer the shortest path from clone to first successful run.
- **Improve:** Add a short 3-step block near the top: clone, copy adapter + `.agents`, run `python scripts/validate_repo.py`.
- **Impact:** Reduces setup friction and support questions.

## 2) Add explicit "when not to use this skill" guidance
- **Why:** README says what the skill is for, but not where it should be avoided (e.g., backend API design, database tuning, branding-only tasks).
- **Improve:** Add a concise "Non-goals" section in `README.md`.
- **Impact:** Better routing and fewer irrelevant invocations.

## 3) Expand the frontend brief template to capture success criteria
- **Why:** `templates/frontend-brief.md` captures context but not measurable acceptance checks.
- **Improve:** Add sections for "Acceptance criteria" and "Out-of-scope".
- **Impact:** Outputs become testable and less ambiguous.

## 4) Expand the audit prompt template to require evidence links
- **Why:** `templates/ui-audit-prompt.md` asks what to cover, but not where findings come from.
- **Improve:** Add a required "Evidence" line per finding (file path, screenshot region, or URL).
- **Impact:** More defensible audits and easier review.

## 5) Improve docs page accessibility with skip link + landmark labels
- **Why:** `docs/index.html` has semantic structure but no skip link and limited navigational affordances for keyboard/screen reader users.
- **Improve:** Add a skip link at top, `aria-label` on `main`, and clearer heading hierarchy for sections.
- **Impact:** Better keyboard navigation and screen reader usability.

## 6) Add Open Graph and description metadata in docs page
- **Why:** `docs/index.html` currently has title + viewport, but no social preview metadata or description.
- **Improve:** Add `<meta name="description">`, Open Graph title/description/image tags.
- **Impact:** Better shareability and discoverability.

## 7) Add a lightweight docs CI check for HTML validity and link health
- **Why:** The existing validator focuses on skill files and JSON schemas; docs HTML can regress silently.
- **Improve:** Add a workflow step to run an HTML checker and a local/internal link checker on `docs/`.
- **Impact:** Prevents docs drift and broken landing-page experience.

## 8) Harden validator file scanning against non-UTF8 files
- **Why:** `scripts/validate_repo.py` reads many files as UTF-8 directly; future binary or mixed-encoding additions can fail hard.
- **Improve:** Use guarded text reading (with controlled fallback) for global scans, or scope scans to known text files only.
- **Impact:** More resilient CI with fewer false failures.

## 9) Add negative tests for schema/output contract violations
- **Why:** Validator currently checks that current examples pass schemas, but doesn't assert expected failures.
- **Improve:** Add intentionally invalid fixture outputs and ensure validation rejects them.
- **Impact:** Stronger guarantees that schemas catch malformed agent output.

## 10) Add versioned changelog + migration notes
- **Why:** The repo has a clear structure and CI, but no explicit changelog for downstream users pinning versions.
- **Improve:** Add `CHANGELOG.md` (keep-a-changelog style) plus "breaking changes" notes when schema or workflow expectations shift.
- **Impact:** Safer upgrades and easier adoption in multi-agent environments.

