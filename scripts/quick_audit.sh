#!/usr/bin/env bash
set -euo pipefail

echo "1) YAML Parse Test"
python3 - <<'PY'
import yaml, re
content = open('SKILL.md', encoding='utf-8').read()
m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
print(yaml.safe_load(m.group(1)))
PY

echo
echo "2) Character Count (must be < 500)"
wc -c SKILL.md

echo
echo "3) Placeholder Scan"
grep -rniE 'your-org|your-repo|example\.com|your-username|openai' --include="*.md" --include="*.json" --include="*.html" . || true

echo
echo "4) Cache Check"
find . -name "__pycache__" -o -name ".DS_Store" | head -20

echo
echo "5) Author Consistency"
grep -rniE 'Iamemily2050|Emily2040' SKILL.md README.md LICENSE docs/index.html

echo
echo "6) Broken Internal Links"
python3 - <<'PY'
import re
from pathlib import Path

def check(path_str: str):
    path = Path(path_str)
    text = path.read_text(encoding='utf-8')
    matches = re.findall(r'!\[[^\]]*\]\(([^)]+)\)|\[[^\]]+\]\(([^)]+)\)', text)
    targets = [a or b for a, b in matches]
    for target in targets:
        if not target or target.startswith(('http://', 'https://', 'mailto:', '#')):
            continue
        target = target.split('#', 1)[0]
        if target and not (path.parent / target).exists():
            print(f"BROKEN: {path} -> {target}")

for file_name in ['README.md', 'SKILL.md']:
    check(file_name)
PY

echo
echo "7) YAML Surrogate Scan"
grep -rni '\\ud[89ab]' --include="*.md" --include="*.yml" --include="*.yaml" . || true

echo
echo "8) Validator"
python3 scripts/validate_repo.py
