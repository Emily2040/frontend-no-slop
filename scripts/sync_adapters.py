from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRAPPER_TEXT = (
    "Load `.agents/skills/frontend-no-slop/SKILL.md` for grounded frontend UI design, critique, "
    "component specs, accessibility review, and implementation planning. Prefer concrete interface "
    "decisions over vague style adjectives.\n"
)

for relative_path in ["AGENTS.md", "CLAUDE.md", "GEMINI.md", ".cursorrules", ".clinerules"]:
    (ROOT / relative_path).write_text(WRAPPER_TEXT, encoding="utf-8")

print("Wrapper files synchronized.")
