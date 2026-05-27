from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRAPPER_TEXT = (
    "Load `.agents/skills/frontend-no-slop/SKILL.md` for grounded frontend UI design, critique, "
    "component specs, accessibility review, and implementation planning. Prefer concrete interface "
    "decisions over vague style adjectives.\n"
)

ADAPTER_PATHS = [
    "adapters/AGENTS.md",
    "adapters/CLAUDE.md",
    "adapters/GEMINI.md",
    "adapters/.cursorrules",
    "adapters/.clinerules",
    "CLAUDE.md",
    "GEMINI.md",
    ".cursorrules",
    ".clinerules",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize consumer adapter files.")
    parser.add_argument("--check", action="store_true", help="Fail if adapters are not synchronized.")
    args = parser.parse_args()

    stale: list[str] = []
    for relative_path in ADAPTER_PATHS:
        path = ROOT / relative_path
        if args.check:
            current = path.read_text(encoding="utf-8") if path.exists() else ""
            if current != WRAPPER_TEXT:
                stale.append(relative_path)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(WRAPPER_TEXT, encoding="utf-8")

    if args.check and stale:
        for relative_path in stale:
            print(f"ERROR: adapter is out of sync: {relative_path}")
        return 1

    print("Wrapper files synchronized." if not args.check else "Wrapper files are synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
