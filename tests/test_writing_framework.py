#!/usr/bin/env python3
"""Self-contained behavioral contract tests for writing-boost v3.3."""

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads((ROOT / "runtime-contract.json").read_text(encoding="utf-8"))


class WritingBoostV33Tests(unittest.TestCase):
    def read(self, rel: str) -> str:
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_version_and_runtime_contract(self):
        skill = self.read("SKILL.md")
        self.assertEqual(CONTRACT["writing_boost_version"], "3.3.0")
        self.assertIn("version: 3.3.0", skill)
        self.assertEqual(CONTRACT["defaults"]["max_reviewers_per_round"], 2)
        self.assertEqual(CONTRACT["review"]["reviewers"], ["integrity-reviewer", "editorial-reviewer"])
        self.assertEqual(CONTRACT["defaults"]["loops_by_stage"]["shape"], 2)
        self.assertEqual(CONTRACT["defaults"]["loops_by_stage"]["draft"], 2)
        self.assertEqual(CONTRACT["defaults"]["loops_by_stage"]["review"], 2)
        self.assertEqual(CONTRACT["defaults"]["loops_by_stage"]["package"], 0)
        self.assertNotIn("loops", CONTRACT["defaults"], "global loop default would duplicate loops_by_stage")
        self.assertGreaterEqual(CONTRACT["schema_version"], 2)
        self.assertTrue(CONTRACT["loops"]["fixed_issue_reopens_only_on_regression"])
        self.assertFalse(CONTRACT["loops"]["new_minor_after_round_1"])
        self.assertTrue(CONTRACT["review"]["strong_trigger_requires_both_reviewers"])

    def test_alignment_locks_measurement_and_feedback_state(self):
        card = self.read("templates/alignment-card.md")
        protocol = self.read("references/alignment-and-length.md")
        for phrase in ["alignment_revision", "正文人称 / POV", "原话处理", "source_policy", "count_mode", "count_scope", "循环预算", "interaction_mode"]:
            self.assertIn(phrase, card)
        self.assertIn("zh_units", protocol)
        self.assertIn("platform", protocol)
        self.assertIn("--review-loops", protocol)
        self.assertIn("runtime-contract.json", protocol)
        self.assertEqual(CONTRACT["interaction_defaults"]["mode"], "auto")
        self.assertEqual(CONTRACT["nonfiction_defaults"]["source_policy"], "closed_corpus")

    def test_loop_policy_has_budget_freeze_and_regression(self):
        loop = self.read("references/loop-policy.md")
        for phrase in [
            "Automatic Loop",
            "Feedback Loop",
            "--shape-loops",
            "--draft-loops",
            "--review-loops",
            "--package-loops",
            "frozen_constraints",
            "frozen_content",
            "issue_set",
            "regressions",
            "局部反馈不触发全流程重跑",
            "Interaction Mode",
            "revision-log.md",
        ]:
            self.assertIn(phrase, loop)

    def test_nonfiction_fidelity_covers_sandbox_defects(self):
        fidelity = self.read("references/nonfiction-fidelity.md")
        ledger = self.read("templates/nonfiction-ledger.md")
        evidence = self.read("templates/character-evidence-card.md")
        for phrase in [
            "SOURCE",
            "DERIVED",
            "RECONSTRUCTED",
            "UNKNOWN",
            "时间轴",
            "实体属性锁",
            "原话保真",
            "叙事人称锁",
            "物象账本",
            "Claim Ledger",
            "Strength conservation",
            "source_policy",
        ]:
            self.assertIn(phrase, fidelity)
        self.assertIn("2026 - 2017 = 9", fidelity)
        self.assertIn("Quote ID", ledger)
        self.assertIn("禁止脑补", ledger)
        self.assertIn("Derived Facts", evidence)
        self.assertIn("Claim Ledger", ledger)
        self.assertIn("Open Gaps", ledger)

    def test_review_topology_and_thresholds(self):
        review = self.read("references/review-council.md")
        self.assertIn("integrity-reviewer", review)
        self.assertIn("editorial-reviewer", review)
        self.assertIn("硬上限：2", review)
        self.assertIn("runtime-contract.json", review)
        self.assertEqual(CONTRACT["review"]["long_nonfiction_thresholds"]["zh_units"], 3000)
        self.assertEqual(CONTRACT["review"]["long_nonfiction_thresholds"]["words"], 1800)

    def test_reviewers_cover_required_risks(self):
        integrity = self.read("agents/integrity-reviewer.md")
        editorial = self.read("agents/editorial-reviewer.md")
        quality = self.read("references/quality-gates.md")
        for phrase in ["2026 - 2017 = 9", "实体属性锁", "Quote ID", "物象与连续性", "POV", "IR-001", "RECHECK"]:
            self.assertIn(phrase, integrity)
        for phrase in ["网文烂梗", "原话颗粒度", "物象长程回收", "ER-001", "RECHECK"]:
            self.assertIn(phrase, editorial)
        for phrase in ["Strong Review Triggers", "Issue Identity", "IR-001", "ER-001", "NOTE"]:
            self.assertIn(phrase, quality)

    def test_legacy_agents_are_non_dispatchable(self):
        for name in [
            "devils-advocate.md",
            "logic-inquisitor.md",
            "slop-hunter.md",
            "pacing-auditor.md",
            "chief-editor.md",
        ]:
            text = self.read("agents/" + name)
            self.assertIn("Deprecated", text)
            self.assertIn("不要调用", text)

    def test_pipeline_has_exactly_six_stages(self):
        pipeline = self.read("references/story-pipeline.md")
        stages = re.findall(r"^## Stage ([1-6])：", pipeline, flags=re.MULTILINE)
        self.assertEqual(stages, ["1", "2", "3", "4", "5", "6"])
        self.assertIn("count_mode", pipeline)
        self.assertIn("Derived Facts", pipeline)
        self.assertIn("固定调用两个 reviewer", pipeline)
        self.assertIn("BLOCKER = 0", pipeline)
        self.assertIn("Artifact Lifecycle", pipeline)
        self.assertIn("Revision Log", pipeline)
        self.assertIn("Delivery Receipt", pipeline)

    def test_style_core_does_not_inherit_zhiyin_numbers(self):
        contract = self.read("styles/style-contract.md")
        styles_readme = self.read("styles/README.md")
        self.assertIn("核心引擎不预设 15/70/15", contract)
        self.assertNotIn("开篇 15% Hook、中段 70%", styles_readme)
        self.assertIn("数字归属", styles_readme)
        self.assertIn("不得放宽 `source_policy / reconstruction_policy / Claim Strength`", contract)

    def test_maintenance_assets_and_ownership(self):
        ownership = self.read("references/ownership-map.md")
        self.assertIn("runtime-contract.json", ownership)
        self.assertIn("quality-gates.md", ownership)
        self.assertTrue((ROOT / "references/quality-gates.md").is_file())
        self.assertTrue((ROOT / "templates/revision-log.md").is_file())
        self.assertTrue((ROOT / "templates/delivery-receipt.md").is_file())
        self.assertTrue((ROOT / "scripts/check_skill_contract.py").is_file())

    def test_cliche_machine_source_and_linter_exist(self):
        pattern_doc = json.loads(self.read("references/cliche-patterns-zh.json"))
        phrases = {x["phrase"] for x in pattern_doc["patterns"]}
        self.assertIn("现实亮出了獠牙", phrases)
        self.assertIn("雪崩呼啸而至", phrases)
        self.assertIn("市井的泥土里，有着实打实的温度", phrases)
        self.assertTrue((ROOT / "scripts/lint_cliches.py").is_file())

    def test_text_metrics_definition(self):
        script_path = ROOT / "scripts/text_metrics.py"
        spec = importlib.util.spec_from_file_location("text_metrics", script_path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        result = module.metrics("北大 ABC 2026，夜市。")
        self.assertEqual(result["han_chars"], 4)
        self.assertEqual(result["latin_number_tokens"], 2)
        self.assertEqual(result["zh_units"], 6)

    def test_contract_checker_executes(self):
        checker = ROOT / "scripts/check_skill_contract.py"
        res = subprocess.run(
            [sys.executable, str(checker)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(res.returncode, 0, res.stdout + "\n" + res.stderr)
        payload = json.loads(res.stdout)
        self.assertTrue(payload["pass"])
        self.assertEqual(payload["version"], "3.3.0")

    def test_cliche_linter_strict_and_quote_exemption(self):
        linter = ROOT / "scripts/lint_cliches.py"
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            unquoted = tmpdir / "unquoted.md"
            quoted = tmpdir / "quoted.md"
            unquoted.write_text("现实亮出了獠牙。", encoding="utf-8")
            quoted.write_text("受访者原话：“现实亮出了獠牙”。", encoding="utf-8")

            bad = subprocess.run(
                [sys.executable, str(linter), str(unquoted), "--strict"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(bad.returncode, 2, bad.stdout + "\n" + bad.stderr)
            bad_payload = json.loads(bad.stdout)
            self.assertGreaterEqual(bad_payload["unquoted_high_risk_count"], 1)

            ok = subprocess.run(
                [sys.executable, str(linter), str(quoted), "--strict"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(ok.returncode, 0, ok.stdout + "\n" + ok.stderr)
            ok_payload = json.loads(ok.stdout)
            self.assertEqual(ok_payload["unquoted_high_risk_count"], 0)

    def test_text_metrics_markdown_prose_removes_non_prose_markup(self):
        script_path = ROOT / "scripts/text_metrics.py"
        spec = importlib.util.spec_from_file_location("text_metrics_markdown", script_path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        sample = """---
title: metadata
---
正文 [链接](https://example.com)。
~~~python
print("不计入")
~~~
![图](image.png)
"""
        prose = module.markdown_prose(sample)
        self.assertIn("正文 链接", prose)
        self.assertNotIn("metadata", prose)
        self.assertNotIn("不计入", prose)
        self.assertNotIn("image.png", prose)

    def test_no_machine_specific_paths(self):
        offenders = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix not in {".md", ".py", ".json"}:
                continue
            if path == Path(__file__) or path == ROOT / "scripts/check_skill_contract.py":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "file:///Users/" in text or "/Users/cc/" in text:
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual([], offenders)

    def test_internal_markdown_links_resolve(self):
        broken = []
        for md_file in ROOT.rglob("*.md"):
            text = md_file.read_text(encoding="utf-8", errors="ignore")
            for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                if link.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                local = link.split("#", 1)[0]
                if local and not (md_file.parent / local).resolve().exists():
                    broken.append((str(md_file.relative_to(ROOT)), link))
        self.assertEqual([], broken, "Broken local links: " + repr(broken))


if __name__ == "__main__":
    unittest.main()
