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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


skill = read("SKILL.md")
readme = read("README.md")
pipeline = read("references/story-pipeline.md")
review = read("references/review-council.md")
loop_policy = read("references/loop-policy.md")
fidelity = read("references/nonfiction-fidelity.md")
style_contract = read("styles/style-contract.md")
ownership = read("references/ownership-map.md")
quality_gates = read("references/quality-gates.md")
integrity = read("agents/integrity-reviewer.md")
editorial = read("agents/editorial-reviewer.md")

version = CONTRACT["writing_boost_version"]
check(CONTRACT["schema_version"] >= 2, "runtime contract schema must support loop convergence / strong triggers")
check(f"version: {version}" in skill, "SKILL.md version differs from runtime-contract.json")
check(version in readme, "README version differs from runtime-contract.json")
check(CONTRACT["defaults"]["max_reviewers_per_round"] == 2, "max reviewers must remain 2")
check("loops" not in CONTRACT["defaults"], "ambiguous global loop default must not duplicate loops_by_stage")
check(CONTRACT["defaults"]["loops_by_stage"]["package"] == 0, "package auto-loop default must remain opt-in")
check(
    CONTRACT["review"]["reviewers"] == ["integrity-reviewer", "editorial-reviewer"],
    "reviewer registry must contain exactly Integrity + Editorial",
)
for stage in ["shape", "draft", "review", "package"]:
    check(CONTRACT["defaults"]["loops_by_stage"][stage] >= 0, f"invalid loop budget: {stage}")
check(
    CONTRACT["nonfiction_defaults"]["reconstruction_policy"] == "forbidden",
    "default nonfiction reconstruction policy must be forbidden",
)
check(
    CONTRACT["interaction_defaults"]["mode"] in {"auto", "checkpoint"},
    "invalid default interaction mode",
)
check(CONTRACT["loops"]["fixed_issue_reopens_only_on_regression"] is True, "fixed issues must reopen only on regression")
check(CONTRACT["loops"]["new_minor_after_round_1"] is False, "round 2+ must not spawn new MINOR by default")
check(CONTRACT["review"]["strong_trigger_requires_both_reviewers"] is True, "strong review trigger must force both reviewers")
check(CONTRACT["review"]["timeline_distinct_years_threshold"] >= 2, "timeline density threshold is invalid")

stages = re.findall(r"^## Stage ([1-6])：", pipeline, flags=re.MULTILINE)
check(stages == ["1", "2", "3", "4", "5", "6"], "story-pipeline must expose stages 1..6 exactly once")
for phrase in ["Artifact Lifecycle", "Claim Ledger", "Revision Log", "Delivery Receipt"]:
    check(phrase in pipeline, f"pipeline missing lifecycle concept: {phrase}")
for phrase in ["Automatic Loop", "Feedback Loop", "frozen_constraints", "regressions", "checkpoint"]:
    check(phrase in loop_policy, f"loop policy missing invariant: {phrase}")

check("主会话" in review and "硬上限：2" in review, "review protocol lost main-session/max-two invariant")
check("quality-gates.md" in review, "review protocol must delegate severity/strong-trigger semantics to quality gates")
for phrase in ["Strong Review Triggers", "Issue Identity", "IR-001", "ER-001", "NOTE"]:
    check(phrase in quality_gates, f"quality gates missing: {phrase}")
check("IR-001" in integrity and "RECHECK" in integrity, "Integrity reviewer lacks stable issue identity / recheck contract")
check("ER-001" in editorial and "RECHECK" in editorial, "Editorial reviewer lacks stable issue identity / recheck contract")
for reviewer in CONTRACT["review"]["reviewers"]:
    check((ROOT / "agents" / f"{reviewer}.md").is_file(), f"active reviewer missing: {reviewer}")

legacy_files = [
    "devils-advocate.md",
    "logic-inquisitor.md",
    "slop-hunter.md",
    "pacing-auditor.md",
    "chief-editor.md",
]
for name in legacy_files:
    text = read(f"agents/{name}")
    check("Deprecated" in text and "不要调用" in text, f"legacy agent not safely deprecated: {name}")
for legacy in ["devils-advocate", "logic-inquisitor", "slop-hunter", "pacing-auditor"]:
    check(legacy not in review, f"legacy reviewer leaked into active review protocol: {legacy}")

for phrase in [
    "Claim Ledger",
    "Strength conservation",
    "source_policy",
    "reconstruction_policy",
    "unknown_policy",
    "Quote ID",
    "物象账本",
]:
    check(phrase in fidelity, f"nonfiction fidelity missing: {phrase}")
check(
    "不得放宽 `source_policy / reconstruction_policy / Claim Strength`" in style_contract,
    "style contract may accidentally loosen nonfiction fidelity",
)

expected_styles = {
    "zhiyin-2026",
    "investigative-feature",
    "personal-memoir",
    "tech-insider",
    "literary-travelogue",
}
actual_styles = {
    p.name
    for p in (ROOT / "styles").iterdir()
    if p.is_dir() and (p / "style.md").is_file()
}
check(actual_styles == expected_styles, f"style registry drift: {sorted(actual_styles)}")

for rel in [
    "references/ownership-map.md",
    "references/cliche-patterns-zh.json",
    "references/quality-gates.md",
    "templates/revision-log.md",
    "templates/delivery-receipt.md",
    "scripts/text_metrics.py",
    "scripts/lint_cliches.py",
]:
    check((ROOT / rel).is_file(), f"required asset missing: {rel}")
check("runtime-contract.json" in ownership, "ownership map must name runtime-contract as numeric SSOT")

stale_public = ["五位一体对抗式终审委员会", "45/60", "5_adversarial_agents"]
for rel in ["README.md", "assets/readme/hero-banner.svg", "assets/readme/pipeline-architecture.svg"]:
    text = read(rel)
    for phrase in stale_public:
        check(phrase not in text, f"stale v2 architecture label in {rel}: {phrase}")

for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix not in {".md", ".py", ".json", ".svg"}:
        continue
    if path.resolve() == Path(__file__).resolve() or "tests/" in str(path.relative_to(ROOT)):
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    check("file:///Users/" not in text, f"machine-specific file URL in {path.relative_to(ROOT)}")
    check("/Users/cc/" not in text, f"machine-specific absolute path in {path.relative_to(ROOT)}")
    if path.suffix != ".md":
        continue
    for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        if link.startswith(("http://", "https://", "mailto:", "#")):
            continue
        local = link.split("#", 1)[0]
        if local:
            check((path.parent / local).resolve().exists(), f"broken link in {path.relative_to(ROOT)}: {link}")

if ERRORS:
    print(json.dumps({"pass": False, "errors": ERRORS}, ensure_ascii=False, indent=2))
    sys.exit(2)

print(
    json.dumps(
        {
            "pass": True,
            "version": version,
            "reviewers": CONTRACT["review"]["reviewers"],
            "loop_defaults": CONTRACT["defaults"]["loops_by_stage"],
        },
        ensure_ascii=False,
        indent=2,
    )
)
