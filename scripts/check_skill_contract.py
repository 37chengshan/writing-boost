#!/usr/bin/env python3
"""Self-audit critical writing-boost invariants using only the standard library."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads((ROOT / "runtime-contract.json").read_text(encoding="utf-8"))
ERRORS: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
pipeline = (ROOT / "references" / "story-pipeline.md").read_text(encoding="utf-8")
review = (ROOT / "references" / "review-council.md").read_text(encoding="utf-8")

check(
    f'version: {CONTRACT["writing_boost_version"]}' in skill,
    "SKILL.md version differs from runtime-contract.json",
)
check(
    CONTRACT["defaults"]["max_reviewers_per_round"] == 2,
    "max_reviewers_per_round must remain 2",
)
check(
    CONTRACT["review"]["reviewers"] == ["integrity-reviewer", "editorial-reviewer"],
    "runtime reviewer registry must contain exactly Integrity + Editorial",
)
check(
    len(re.findall(r"^## Stage [1-6]：", pipeline, flags=re.MULTILINE)) == 6,
    "story-pipeline must expose exactly six numbered stages",
)
check("主会话" in review and "硬上限：2" in review, "review protocol lost main-session/max-two invariant")

for legacy in ["devils-advocate", "logic-inquisitor", "slop-hunter", "pacing-auditor"]:
    check(legacy not in review, f"legacy reviewer leaked back into review protocol: {legacy}")

for path in ROOT.rglob("*.md"):
    text = path.read_text(encoding="utf-8", errors="ignore")
    check("file:///Users/" not in text, f"machine-specific file URL in {path.relative_to(ROOT)}")
    for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        if link.startswith(("http://", "https://", "mailto:", "#")):
            continue
        local = link.split("#", 1)[0]
        if not local:
            continue
        check((path.parent / local).resolve().exists(), f"broken link in {path.relative_to(ROOT)}: {link}")

if ERRORS:
    print(json.dumps({"pass": False, "errors": ERRORS}, ensure_ascii=False, indent=2))
    sys.exit(2)

print(json.dumps({"pass": True, "version": CONTRACT["writing_boost_version"]}, ensure_ascii=False, indent=2))
