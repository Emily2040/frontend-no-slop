# Changelog

All notable changes to this project are documented in this file.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Quick-start section and explicit non-goals in `README.md`.
- Acceptance criteria and out-of-scope sections in `templates/frontend-brief.md`.
- Evidence + severity requirements in `templates/ui-audit-prompt.md`.
- Accessibility and metadata upgrades in `docs/index.html`.
- Docs validation script `scripts/check_docs.py` and CI workflow integration.
- Negative schema fixtures for validation hardening.

### Changed
- `scripts/validate_repo.py` now includes safer text reading and validates negative fixtures.
