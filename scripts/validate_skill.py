#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "seo" / "SKILL.md"


def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main():
    if not SKILL.exists():
        fail(f"missing {SKILL}")
    text = SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        fail("SKILL.md frontmatter is not closed")
    fm = parts[1]
    name_m = re.search(r"^name:\s*([^\n]+)$", fm, re.M)
    desc_m = re.search(r"^description:\s*([^\n]+)$", fm, re.M)
    if not name_m or not desc_m:
        fail("name and description are required")
    name = name_m.group(1).strip().strip('"\'')
    desc = desc_m.group(1).strip().strip('"\'')
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail("name must be lowercase kebab-case")
    if name != SKILL.parent.name:
        fail("name must match skill directory")
    if not (1 <= len(name) <= 64):
        fail("name must be 1-64 chars")
    if not (1 <= len(desc) <= 1024):
        fail("description must be 1-1024 chars")
    if len(text.splitlines()) >= 500:
        fail("root SKILL.md should remain under 500 lines")
    refs = re.findall(r"`(references/[^`]+\.md)`", text)
    missing = sorted({r for r in refs if not (SKILL.parent / r).exists()})
    if missing:
        fail("missing referenced files: " + ", ".join(missing))
    for script in ["scripts/seo_scan.py", "scripts/repo_seo_scan.py", "scripts/site_check.py"]:
        if not (SKILL.parent / script).exists():
            fail(f"missing {script}")
    print("SEO skill validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
