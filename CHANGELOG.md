# Changelog

All notable changes to this project are documented in this file.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Compatibility matrix and release checklist in `README.md`.
- Current roadmap in `ROADMAP.md`.
- Generated bitmap hero infographic at `docs/assets/hero-infographic.png`.

## [2.0.0] - 2026-05-27

### Added
- Cross-platform adapter templates under `adapters/`.
- `requirements-dev.lock` for repeatable CI installs.
- Eval suite schema and static eval cases.
- Page-type lenses for forms, modal dialogs, design systems, and app shells.
- WCAG 2.2, WAI-ARIA APG, and Core Web Vitals guidance in the core accessibility/performance module.

### Changed
- GitHub Actions now validates the `master` default branch, supports manual runs, sets read-only permissions, uses pip caching, and runs on Python 3.11 and 3.12.
- `AGENTS.md` is now maintainer guidance for this repository instead of a consumer adapter.
- `scripts/sync_adapters.py` supports `--check`.
- `scripts/validate_repo.py` validates adapter sync, schema/page-type alignment, and eval fixtures.
- Breaking: `page_type` fields in output schemas now use a fixed enum aligned with the page-type registry.
- Placeholder scanning no longer treats legitimate OpenAI references as placeholders.

## [1.1.0] - 2026-03-09

### Added
- Quick-start section and explicit non-goals in `README.md`.
- Acceptance criteria and out-of-scope sections in `templates/frontend-brief.md`.
- Evidence and severity requirements in `templates/ui-audit-prompt.md`.
- Accessibility and metadata upgrades in `docs/index.html`.
- Docs validation script `scripts/check_docs.py` and CI workflow integration.
- Negative schema fixtures for validation hardening.

### Changed
- `scripts/validate_repo.py` now includes safer text reading and validates negative fixtures.
