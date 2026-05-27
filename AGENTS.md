# Repository Instructions

This repository maintains the portable Frontend No-Slop skill. The consumer adapter text lives in `adapters/`; do not copy this maintainer file into downstream projects.

## Maintainer Workflow

- Canonical skill source: `.agents/skills/frontend-no-slop/SKILL.md`.
- Consumer adapters must route to `.agents/skills/frontend-no-slop/SKILL.md`.
- When adapter text changes, run `python scripts/sync_adapters.py` and commit the updated adapter files.
- Before opening a PR, run:
  - `python -m pip install -r requirements-dev.lock`
  - `python scripts/validate_repo.py`
  - `python scripts/sync_adapters.py --check`
  - `python scripts/check_docs.py`

## Release Rules

- Keep the canonical skill `metadata.version` aligned with `CHANGELOG.md`.
- Add a dated changelog entry for every released version.
- Update examples, schemas, and eval fixtures together when changing output contracts.
- Keep `IMPROVEMENT_REVIEW.md` historical; use `ROADMAP.md` for current work.

## Schema Rules

- `page_type` values must stay aligned with `.agents/skills/frontend-no-slop/registry/page-type-lenses.json`.
- JSON examples must validate against their matching schemas.
- Invalid example fixtures must fail validation.
- Do not add unsupported template-placeholder tokens; the validator owns the exact banned list.
