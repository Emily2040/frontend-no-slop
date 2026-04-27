from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INDEX = DOCS / "index.html"


class DocsParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.has_skip_link = False
        self.main_ids: set[str] = set()
        self.image_sources: list[str] = []
        self.has_description = False
        self.has_og_title = False
        self.has_og_description = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        mapping = {k: v for k, v in attrs}

        if tag == "a" and mapping.get("href", "").startswith("#"):
            cls = mapping.get("class", "") or ""
            if "skip-link" in cls:
                self.has_skip_link = True

        if tag == "main" and mapping.get("id"):
            self.main_ids.add(mapping["id"])

        if tag == "img" and mapping.get("src"):
            self.image_sources.append(mapping["src"])

        if tag == "meta":
            if mapping.get("name") == "description":
                self.has_description = True
            if mapping.get("property") == "og:title":
                self.has_og_title = True
            if mapping.get("property") == "og:description":
                self.has_og_description = True


def main() -> int:
    if not INDEX.exists():
        print("ERROR: docs/index.html is missing")
        return 1

    parser = DocsParser()
    parser.feed(INDEX.read_text(encoding="utf-8", errors="replace"))

    errors: list[str] = []

    if not parser.main_ids:
        errors.append("docs/index.html must include a <main id=...> landmark")

    if not parser.has_skip_link:
        errors.append("docs/index.html must include a visible skip-link anchor")

    if not parser.has_description:
        errors.append("docs/index.html must include <meta name=\"description\">")

    if not parser.has_og_title or not parser.has_og_description:
        errors.append("docs/index.html must include og:title and og:description metadata")

    for src in parser.image_sources:
        if src.startswith(("http://", "https://", "data:")):
            continue
        if not (DOCS / src).exists():
            errors.append(f"docs/index.html references missing image: {src}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Docs check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
