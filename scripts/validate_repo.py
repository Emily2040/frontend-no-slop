from __future__ import annotations

import json
import re
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, validate
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / ".agents/skills/frontend-no-slop"
CANONICAL_PATH = ".agents/skills/frontend-no-slop/SKILL.md"
MAX_ROOT_SKILL_CHARS = 500
EXPECTED_AUTHOR = "Iamemily2050"
EXPECTED_REPO = "https://github.com/Emily2040/frontend-no-slop"
EXPECTED_LICENSE_LINE = "Copyright (c) 2026 Iamemily2050"
EXPECTED_DOCS_FOOTER_LINK = "https://github.com/Emily2040"
PLACEHOLDERS = ["your-org", "your-repo", "example.com", "your-username", "openai"]
WRAPPERS = [
    ROOT / "AGENTS.md",
    ROOT / "CLAUDE.md",
    ROOT / "GEMINI.md",
    ROOT / ".cursorrules",
    ROOT / ".clinerules",
]
REQUIRED_FILES = [
    ROOT / "SKILL.md",
    ROOT / "AGENTS.md",
    ROOT / "CLAUDE.md",
    ROOT / "GEMINI.md",
    ROOT / ".cursorrules",
    ROOT / ".clinerules",
    ROOT / "README.md",
    ROOT / "LICENSE",
    ROOT / ".gitignore",
    ROOT / "requirements-dev.txt",
    ROOT / "AUDIT_REPORT.md",
    ROOT / "CHANGELOG.md",
    ROOT / "docs/index.html",
    ROOT / "docs/assets/hero.svg",
    ROOT / "docs/assets/architecture.svg",
    ROOT / "docs/assets/workflow.svg",
    ROOT / "scripts/validate_repo.py",
    ROOT / "scripts/sync_adapters.py",
    ROOT / "scripts/quick_audit.sh",
    ROOT / "scripts/check_docs.py",
    ROOT / ".github/workflows/validate.yml",
    ROOT / "templates/frontend-brief.md",
    ROOT / "templates/ui-audit-prompt.md",
    SKILL_ROOT / "SKILL.md",
    SKILL_ROOT / "references/00-orchestrator.md",
    SKILL_ROOT / "skills/core/01-intake-and-grounding.md",
    SKILL_ROOT / "skills/core/02-slop-scrubber.md",
    SKILL_ROOT / "skills/core/03-layout-and-visual-logic.md",
    SKILL_ROOT / "skills/core/04-component-state-discipline.md",
    SKILL_ROOT / "skills/core/05-a11y-performance-content.md",
    SKILL_ROOT / "skills/core/06-page-type-lenses.md",
    SKILL_ROOT / "skills/core/07-output-contract.md",
    SKILL_ROOT / "registry/forbidden-slop.json",
    SKILL_ROOT / "registry/page-type-lenses.json",
    SKILL_ROOT / "registry/frontend-evidence-prompts.json",
    SKILL_ROOT / "schemas/authoring-base.json",
    SKILL_ROOT / "schemas/runtime-compact.json",
    SKILL_ROOT / "examples/landing-page-input.md",
    SKILL_ROOT / "examples/landing-page-output.json",
    SKILL_ROOT / "examples/dashboard-audit-input.md",
    SKILL_ROOT / "examples/dashboard-audit-output.json",
    SKILL_ROOT / "examples/invalid-landing-page-output.json",
    SKILL_ROOT / "examples/invalid-dashboard-audit-output.json",
]

errors: list[str] = []


def add_error(message: str) -> None:
    errors.append(message)


def check(condition: bool, message: str) -> None:
    if not condition:
        add_error(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    text = read_text(path)
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError(f"{path.relative_to(ROOT)} is missing YAML frontmatter")
    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict):
        raise ValueError(f"{path.relative_to(ROOT)} frontmatter did not parse to a mapping")
    return frontmatter, match.group(2)


def ensure_quoted_frontmatter(path: Path) -> None:
    text = read_text(path)
    for key in ("name", "description", "license"):
        pattern = rf'^{key}:\s+".+"$'
        check(
            re.search(pattern, text, re.MULTILINE) is not None,
            f"{path.relative_to(ROOT)} should quote the '{key}' frontmatter value",
        )


def validate_skill_file(path: Path, enforce_author: bool = False) -> None:
    try:
        frontmatter, body = parse_frontmatter(path)
    except ValueError as exc:
        add_error(str(exc))
        return

    allowed_keys = {"name", "description", "license", "metadata"}
    extra = set(frontmatter.keys()) - allowed_keys
    check(not extra, f"{path.relative_to(ROOT)} has unsupported frontmatter keys: {sorted(extra)}")

    for key in ("name", "description", "license"):
        check(isinstance(frontmatter.get(key), str), f"{path.relative_to(ROOT)} frontmatter key '{key}' must be a string")

    metadata = frontmatter.get("metadata")
    check(isinstance(metadata, dict), f"{path.relative_to(ROOT)} must contain a metadata object")

    if isinstance(metadata, dict):
        if enforce_author:
            check(metadata.get("author") == EXPECTED_AUTHOR, f"{path.relative_to(ROOT)} metadata.author must be '{EXPECTED_AUTHOR}'")
            check(metadata.get("repo") == EXPECTED_REPO, f"{path.relative_to(ROOT)} metadata.repo must be '{EXPECTED_REPO}'")
        else:
            check("author" in metadata, f"{path.relative_to(ROOT)} metadata.author is required")
            check("repo" in metadata, f"{path.relative_to(ROOT)} metadata.repo is required")

    check(bool(body.strip()), f"{path.relative_to(ROOT)} body must not be empty")
    ensure_quoted_frontmatter(path)


def validate_json_file(path: Path) -> object:
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        add_error(f"{path.relative_to(ROOT)} is not valid JSON: {exc}")
        return {}


def validate_svg(path: Path) -> None:
    check(read_text(path).lstrip().startswith("<svg"), f"{path.relative_to(ROOT)} does not appear to be an SVG file")


def broken_internal_links(markdown_path: Path) -> list[str]:
    broken: list[str] = []
    text = read_text(markdown_path)
    targets = re.findall(r'!\[[^\]]*\]\(([^)]+)\)|\[[^\]]+\]\(([^)]+)\)', text)
    flattened = [a or b for a, b in targets]
    for target in flattened:
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        normalized = target.split("#", 1)[0]
        if not normalized:
            continue
        if not (markdown_path.parent / normalized).exists():
            broken.append(normalized)
    return broken


def should_scan(path: Path) -> bool:
    blocked = {".git", ".venv", "venv", "node_modules", "__pycache__"}
    return not any(part in blocked for part in path.parts)


def scan_placeholders() -> None:
    for path in ROOT.rglob("*"):
        if path.is_dir() or not should_scan(path):
            continue
        if path.suffix.lower() not in {".md", ".json", ".html", ".yml", ".yaml"}:
            continue
        text = read_text(path).lower()
        for token in PLACEHOLDERS:
            check(token not in text, f"{path.relative_to(ROOT)} contains placeholder token '{token}'")


def scan_surrogates() -> None:
    pattern = re.compile(r"\\ud[89ab][0-9a-f]{2}", re.IGNORECASE)
    for path in ROOT.rglob("*"):
        if path.is_dir() or not should_scan(path):
            continue
        if path.suffix.lower() not in {".md", ".yml", ".yaml", ".json", ".html"}:
            continue
        check(pattern.search(read_text(path)) is None, f"{path.relative_to(ROOT)} contains a surrogate escape sequence")


def check_no_cache_or_strays() -> None:
    bad_names = {"__pycache__", ".DS_Store", "Skill.md"}
    for path in ROOT.rglob("*"):
        if not should_scan(path):
            continue
        if path.name in bad_names:
            add_error(f"Disallowed file or directory present: {path.relative_to(ROOT)}")

    for readme in (ROOT / ".agents/skills").rglob("README.md"):
        add_error(f"README.md is not allowed inside skill directories: {readme.relative_to(ROOT)}")


def validate_examples() -> None:
    full_schema = validate_json_file(SKILL_ROOT / "schemas/authoring-base.json")
    compact_schema = validate_json_file(SKILL_ROOT / "schemas/runtime-compact.json")
    full_example = validate_json_file(SKILL_ROOT / "examples/landing-page-output.json")
    compact_example = validate_json_file(SKILL_ROOT / "examples/dashboard-audit-output.json")

    try:
        Draft202012Validator.check_schema(full_schema)
    except Exception as exc:
        add_error(f"authoring-base.json is not a valid JSON Schema: {exc}")

    try:
        Draft202012Validator.check_schema(compact_schema)
    except Exception as exc:
        add_error(f"runtime-compact.json is not a valid JSON Schema: {exc}")

    try:
        validate(instance=full_example, schema=full_schema)
    except Exception as exc:
        add_error(f"landing-page-output.json does not validate against authoring-base.json: {exc}")

    try:
        validate(instance=compact_example, schema=compact_schema)
    except Exception as exc:
        add_error(f"dashboard-audit-output.json does not validate against runtime-compact.json: {exc}")


def validate_negative_examples() -> None:
    full_schema = validate_json_file(SKILL_ROOT / "schemas/authoring-base.json")
    compact_schema = validate_json_file(SKILL_ROOT / "schemas/runtime-compact.json")
    invalid_full = validate_json_file(SKILL_ROOT / "examples/invalid-landing-page-output.json")
    invalid_compact = validate_json_file(SKILL_ROOT / "examples/invalid-dashboard-audit-output.json")

    try:
        validate(instance=invalid_full, schema=full_schema)
        add_error("invalid-landing-page-output.json unexpectedly passed authoring-base.json")
    except ValidationError:
        pass

    try:
        validate(instance=invalid_compact, schema=compact_schema)
        add_error("invalid-dashboard-audit-output.json unexpectedly passed runtime-compact.json")
    except ValidationError:
        pass


def validate_author_consistency() -> None:
    root_frontmatter, _ = parse_frontmatter(ROOT / "SKILL.md")
    metadata = root_frontmatter["metadata"]
    check(metadata.get("author") == EXPECTED_AUTHOR, "SKILL.md metadata.author does not match the expected author")
    check(metadata.get("repo") == EXPECTED_REPO, "SKILL.md metadata.repo does not match the expected repo")

    license_text = read_text(ROOT / "LICENSE")
    check(EXPECTED_LICENSE_LINE in license_text, "LICENSE does not contain the expected copyright line")

    readme = read_text(ROOT / "README.md")
    check("Created by **Iamemily2050**" in readme, "README.md is missing the expected author heading")
    for token in [
        "https://github.com/Emily2040",
        "https://Iamemily2050.com",
        "https://x.com/iamemily2050",
        "https://instagram.com/iamemily2050",
    ]:
        check(token in readme, f"README.md is missing author link {token}")

    docs_index = read_text(ROOT / "docs/index.html")
    check(EXPECTED_DOCS_FOOTER_LINK in docs_index, "docs/index.html footer must link to the GitHub profile")


def validate_wrappers() -> None:
    for wrapper in WRAPPERS:
        check(CANONICAL_PATH in read_text(wrapper), f"{wrapper.relative_to(ROOT)} must route to {CANONICAL_PATH}")


def validate_gitignore() -> None:
    gitignore = read_text(ROOT / ".gitignore")
    for token in ["__pycache__", ".DS_Store"]:
        check(token in gitignore, f".gitignore must exclude {token}")


def validate_required_files() -> None:
    for path in REQUIRED_FILES:
        check(path.exists(), f"Missing required file: {path.relative_to(ROOT)}")


def validate_root_size() -> None:
    size = len(read_text(ROOT / "SKILL.md"))
    check(size <= MAX_ROOT_SKILL_CHARS, f"Root SKILL.md must be <= {MAX_ROOT_SKILL_CHARS} characters, found {size}")


def validate_markdown_links() -> None:
    for path in [ROOT / "README.md", ROOT / "SKILL.md"]:
        for broken in broken_internal_links(path):
            add_error(f"{path.relative_to(ROOT)} has broken internal link: {broken}")


def main() -> int:
    validate_required_files()
    check_no_cache_or_strays()

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    validate_skill_file(ROOT / "SKILL.md", enforce_author=True)
    validate_skill_file(SKILL_ROOT / "SKILL.md", enforce_author=False)
    validate_root_size()
    validate_wrappers()
    validate_markdown_links()
    validate_author_consistency()
    validate_gitignore()
    validate_svg(ROOT / "docs/assets/hero.svg")
    validate_svg(ROOT / "docs/assets/architecture.svg")
    validate_svg(ROOT / "docs/assets/workflow.svg")

    for json_path in [
        SKILL_ROOT / "registry/forbidden-slop.json",
        SKILL_ROOT / "registry/page-type-lenses.json",
        SKILL_ROOT / "registry/frontend-evidence-prompts.json",
        SKILL_ROOT / "schemas/authoring-base.json",
        SKILL_ROOT / "schemas/runtime-compact.json",
        SKILL_ROOT / "examples/landing-page-output.json",
        SKILL_ROOT / "examples/dashboard-audit-output.json",
        SKILL_ROOT / "examples/invalid-landing-page-output.json",
        SKILL_ROOT / "examples/invalid-dashboard-audit-output.json",
    ]:
        validate_json_file(json_path)

    scan_placeholders()
    scan_surrogates()
    validate_examples()
    validate_negative_examples()

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
