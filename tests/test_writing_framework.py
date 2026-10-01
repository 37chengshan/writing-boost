#!/usr/bin/env python3
"""Comprehensive test suite for writing skills integration, 2026 articles distillation, and agyskill deployment."""

import re
import unittest
from pathlib import Path

ROOT = Path("/Users/cc/code/writing")
AGYSKILL_DIR = ROOT / "agyskill"
AGENTS_SKILLS_DIR = ROOT / ".agents/skills"
DISTILLED_DIR = ROOT / "docs/知音Travel/distilled"
Y2026_DIR = ROOT / "docs/知音Travel/2026"
Y2026_H2_DIR = ROOT / "docs/知音Travel/2026-H2"


class TestWritingFramework(unittest.TestCase):
    def test_upstream_repositories_pulled(self):
        """Verify both GitHub links are cloned and present locally."""
        stop_slop = ROOT / "stop-slop"
        mattpocock = ROOT / "mattpocock-skills"

        self.assertTrue(stop_slop.is_dir(), "stop-slop directory missing")
        self.assertTrue((stop_slop / "SKILL.md").is_file(), "stop-slop/SKILL.md missing")
        self.assertTrue((stop_slop / "references/phrases.md").is_file(), "stop-slop phrases missing")

        self.assertTrue(mattpocock.is_dir(), "mattpocock-skills directory missing")
        agent_skill = mattpocock / "skills/productivity/writing-for-agents/SKILL.md"
        self.assertTrue(agent_skill.is_file(), "writing-for-agents/SKILL.md missing")

    def test_2026_articles_present_and_well_formed(self):
        """Verify all 11 articles from 2026 (10 in 2026/ + 1 in 2026-H2) are present with non-empty content."""
        files_2026 = [Y2026_DIR / f"{i}.md" for i in range(1, 11)] + [
            Y2026_H2_DIR / "2026-09-21_知音Travel_外卖小哥跑成世界冠军.md"
        ]

        for article_file in files_2026:
            self.assertTrue(article_file.is_file(), f"2026 article missing: {article_file}")
            text = article_file.read_text(encoding="utf-8")
            self.assertGreater(len(text), 500, f"Article too short: {article_file}")

        # Verify key entities in articles 2, 3, 4
        text_2 = (Y2026_DIR / "2.md").read_text(encoding="utf-8")
        self.assertIn("吴非", text_2)
        self.assertIn("新西兰", text_2)
        self.assertIn("内皮尔监狱", text_2)

        text_3 = (Y2026_DIR / "3.md").read_text(encoding="utf-8")
        self.assertIn("李艾", text_3)
        self.assertIn("李静", text_3)
        self.assertIn("围绝经期", text_3)

        text_4 = (Y2026_DIR / "4.md").read_text(encoding="utf-8")
        self.assertIn("贾浅浅", text_4)
        self.assertIn("张雪", text_4)
        self.assertIn("夏之光", text_4)
        self.assertIn("兜底", text_4)

        # Verify key entities in newly normalized 5 articles (6.md ~ 10.md)
        text_6 = (Y2026_DIR / "6.md").read_text(encoding="utf-8")
        self.assertIn("阿秋", text_6)
        self.assertIn("何生", text_6)
        self.assertIn("轮椅", text_6)
        self.assertIn("极光", text_6)

        text_7 = (Y2026_DIR / "7.md").read_text(encoding="utf-8")
        self.assertIn("沈珂", text_7)
        self.assertIn("洪湖", text_7)
        self.assertIn("藕汤面", text_7)
        self.assertIn("瞿家湾", text_7)

        text_8 = (Y2026_DIR / "8.md").read_text(encoding="utf-8")
        self.assertIn("冯晓梅", text_8)
        self.assertIn("龙岗", text_8)
        self.assertIn("存折", text_8)
        self.assertIn("裁员", text_8)

        text_9 = (Y2026_DIR / "9.md").read_text(encoding="utf-8")
        self.assertIn("林深", text_9)
        self.assertIn("神农架", text_9)
        self.assertIn("红桦", text_9)
        self.assertIn("大九湖", text_9)

        text_10 = (Y2026_DIR / "10.md").read_text(encoding="utf-8")
        self.assertIn("仙桃", text_10)
        self.assertIn("沔阳", text_10)
        self.assertIn("鳝鱼粉", text_10)
        self.assertIn("二八大杠", text_10)

    def test_2026_readme_indexes_and_catalog(self):
        """Verify docs/知音Travel/2026/README.md exists and properly catalogs all 10 articles in 2026/."""
        readme_2026 = Y2026_DIR / "README.md"
        self.assertTrue(readme_2026.is_file(), "docs/知音Travel/2026/README.md missing")
        content = readme_2026.read_text(encoding="utf-8")

        for i in range(1, 11):
            self.assertIn(f"[{i}.md]({i}.md)", content, f"{i}.md not indexed in 2026/README.md")

        # Punctuation rate checks in 2026/README.md
        self.assertIn("逗号率（，）：90.9% (10/11)", content)
        self.assertIn("引号率（“”）：18.2% (2/11)", content)
        self.assertIn("问号率（？）：9.1% (1/11)", content)
        self.assertIn("感叹号率（！）：18.2% (2/11)", content)

        account_readme = ROOT / "docs/知音Travel/README.md"
        self.assertTrue(account_readme.is_file(), "docs/知音Travel/README.md missing")
        ac_content = account_readme.read_text(encoding="utf-8")
        line_2026 = [line for line in ac_content.splitlines() if "2026/" in line][0]
        self.assertIn("10 篇", line_2026)
        self.assertNotIn("8 篇", line_2026, "Found stale '8 篇' in 2026 line of docs/知音Travel/README.md")
        self.assertIn("当前文章数：1293 篇", ac_content, "Total article count mismatch")

        main_readme = ROOT / "docs/README.md"
        self.assertTrue(main_readme.is_file(), "docs/README.md missing")
        main_content = main_readme.read_text(encoding="utf-8")
        self.assertIn("当前文章数：1293 篇", main_content, "Total article count mismatch in main README")

    def test_2026_statistical_accuracy(self):
        """Verify statistical data of 2026 articles matches real character counts."""
        files_10 = [Y2026_DIR / f"{i}.md" for i in range(1, 11)]
        files_11 = files_10 + [Y2026_H2_DIR / "2026-09-21_知音Travel_外卖小哥跑成世界冠军.md"]

        char_counts_10 = [len(p.read_text(encoding="utf-8")) for p in files_10]
        chinese_counts_10 = [
            len([c for c in p.read_text(encoding="utf-8") if "\u4e00" <= c <= "\u9fff"])
            for p in files_10
        ]
        self.assertEqual(sum(char_counts_10), 33335)
        self.assertEqual(sum(chinese_counts_10), 26523)
        self.assertEqual(round(sum(char_counts_10) / 10), 3334)
        self.assertEqual(round(sum(chinese_counts_10) / 10), 2652)

        char_counts_11 = [len(p.read_text(encoding="utf-8")) for p in files_11]
        chinese_counts_11 = [
            len([c for c in p.read_text(encoding="utf-8") if "\u4e00" <= c <= "\u9fff"])
            for p in files_11
        ]
        self.assertEqual(sum(char_counts_11), 37368)
        self.assertEqual(sum(chinese_counts_11), 29565)
        self.assertEqual(round(sum(char_counts_11) / 11), 3397)
        self.assertEqual(round(sum(chinese_counts_11) / 11), 2688)

        report = ROOT / "docs/知音Travel_风格演变与写作DNA蒸馏报告.md"
        report_content = report.read_text(encoding="utf-8")
        self.assertIn("3,334（中文字数 2,652）", report_content)
        self.assertIn("3,397（中文字数 2,688）", report_content)

    def test_distillation_report_exists_and_deeply_covers_2026(self):
        """Verify the 知音 Travel distillation report exists and has required sections including all 2026 additions."""
        report = ROOT / "docs/知音Travel_风格演变与写作DNA蒸馏报告.md"
        self.assertTrue(report.is_file(), "Distillation report missing")
        content = report.read_text(encoding="utf-8")

        # Verify key historical phases analyzed
        self.assertIn("2017–2018", content)
        self.assertIn("2019–2021", content)
        self.assertIn("2022–2023", content)
        self.assertIn("2024", content)
        self.assertIn("2026", content)

        # Verify 6-layer DNA
        self.assertIn("L1 表层语言", content)
        self.assertIn("L2 文章结构", content)
        self.assertIn("L3 选题逻辑", content)
        self.assertIn("L4 素材策略", content)
        self.assertIn("L5 认知框架", content)
        self.assertIn("L6 视觉", content)

        # Verify all 2026 sample entities and modes
        for entity in [
            "赵家驹",
            "重庆",
            "吴非",
            "李艾",
            "李静",
            "贾浅浅",
            "张雪",
            "碎银思维",
            "阿秋",
            "何生",
            "沈珂",
            "洪湖",
            "老温",
            "林深",
            "神农架",
            "鳝鱼粉",
            "模式 E",
            "模式 F",
            "模式 G",
            "模式 H",
            "模式 I",
            "模式 J",
            "模式 K",
            "模式 L",
        ]:
            self.assertIn(entity, content, f"Entity or mode missing from report: {entity}")

    def test_distilled_modular_files_coverage(self):
        """Verify the distilled modular files contain the latest 2026 structural patterns (A~L) and cognitive concepts."""
        writing_dna = DISTILLED_DIR / "Writing-DNA.md"
        structures = DISTILLED_DIR / "文章结构模板.md"
        perspectives = DISTILLED_DIR / "写作视角与认知框架.md"
        language_dna = DISTILLED_DIR / "语言DNA.md"

        for f in [writing_dna, structures, perspectives, language_dna]:
            self.assertTrue(f.is_file(), f"Distilled file missing: {f}")

        struct_content = structures.read_text(encoding="utf-8")
        for mode in [
            "模式 A",
            "模式 B",
            "模式 C",
            "模式 D",
            "模式 E：【阶层双轨·时代断裂与草根突围型】",
            "模式 F：【社会议题·群体隐痛与去病耻突围型】",
            "模式 G：【青年脱轨·反卷探寻与生活重建型】",
            "模式 H：【创伤互救·生死承诺与无障碍环球跋涉型】",
            "模式 I：【味觉寻根·孤女亲情抚慰与文旅美食叙事型】",
            "模式 J：【中年断崖·中产坍塌与亲情重构突围型】",
            "模式 K：【生态反转·体制脱轨与双向奔赴科考型】",
            "模式 L：【沉默父爱·小镇普工隐忍与市井风味共振型】",
        ]:
            self.assertIn(mode, struct_content, f"Mode missing from 文章结构模板.md: {mode}")

        persp_content = perspectives.read_text(encoding="utf-8")
        self.assertIn("碎银思维", persp_content)
        self.assertIn("无人兜底", persp_content)
        self.assertIn("去病耻感", persp_content)
        self.assertIn("中产破产三件套", persp_content)
        self.assertIn("八大反差张力法则", persp_content)
        self.assertIn("创伤重击与生命辽阔反差", persp_content)
        self.assertIn("体制狂热与山野科研反差", persp_content)
        self.assertIn("世俗平庸与亲情分量反差", persp_content)

        lang_content = language_dna.read_text(encoding="utf-8")
        self.assertIn("赵家驹", lang_content)
        self.assertIn("阿秋与何生", lang_content)
        self.assertIn("老温", lang_content)
        self.assertIn("仙桃父亲", lang_content)
        self.assertIn("沈珂与舅妈", lang_content)
        self.assertIn("林深与神农架", lang_content)

    def test_agyskill_and_agent_skills_structure(self):
        """Verify agyskill/ and .agents/skills/ have all required skills and valid YAML frontmatter."""
        required_skills = [
            "writing-boost",
            "boost",
            "writing-dna",
            "less-ai-tone",
            "stop-slop",
            "writing-for-agents",
            "story",
            "story-short-write",
            "story-long-write",
            "story-review",
            "story-deslop",
        ]

        for target_dir in [AGYSKILL_DIR, AGENTS_SKILLS_DIR]:
            self.assertTrue(target_dir.is_dir(), f"{target_dir} is not a directory")
            for skill_name in required_skills:
                skill_path = target_dir / skill_name
                self.assertTrue(skill_path.is_dir(), f"Skill directory missing: {skill_path}")
                skill_md = skill_path / "SKILL.md"
                self.assertTrue(skill_md.is_file(), f"SKILL.md missing: {skill_md}")

                content = skill_md.read_text(encoding="utf-8")
                # Frontmatter check
                self.assertTrue(
                    content.startswith("---"), f"{skill_md} must start with YAML frontmatter '---'"
                )
                self.assertIn("name:", content, f"{skill_md} frontmatter missing 'name'")
                self.assertIn(
                    "description:", content, f"{skill_md} frontmatter missing 'description'"
                )

    def test_boost_templates_support_2026_modes(self):
        """Verify writing-boost templates and pipeline actively support 2026 modes A through L."""
        wb_dir = AGYSKILL_DIR / "writing-boost"
        topic_eval = (wb_dir / "templates/topic-evaluation.md").read_text(encoding="utf-8")
        self.assertIn("模式 E", topic_eval)
        self.assertIn("模式 F", topic_eval)
        self.assertIn("模式 G", topic_eval)
        self.assertIn("模式 H", topic_eval)
        self.assertIn("模式 I", topic_eval)
        self.assertIn("模式 J", topic_eval)
        self.assertIn("模式 K", topic_eval)
        self.assertIn("模式 L", topic_eval)
        self.assertIn("无人兜底", topic_eval)
        self.assertIn("碎银", topic_eval)

        beat_sheet = (wb_dir / "templates/chapter-beat-sheet.md").read_text(encoding="utf-8")
        self.assertIn("模式 E：【阶层双轨·时代断裂与草根突围型】", beat_sheet)
        self.assertIn("模式 F：【社会议题·群体隐痛与去病耻突围型】", beat_sheet)
        self.assertIn("模式 G：【青年脱轨·反卷探寻与生活重建型】", beat_sheet)
        self.assertIn("模式 H：【创伤互救·生死承诺与无障碍环球跋涉型】", beat_sheet)
        self.assertIn("模式 I：【味觉寻根·孤女亲情抚慰与文旅美食叙事型】", beat_sheet)
        self.assertIn("模式 J：【中年断崖·中产坍塌与亲情重构突围型】", beat_sheet)
        self.assertIn("模式 K：【生态反转·体制脱轨与双向奔赴科考型】", beat_sheet)
        self.assertIn("模式 L：【沉默父爱·小镇普工隐忍与市井风味共振型】", beat_sheet)

        pipeline = (wb_dir / "references/story-pipeline.md").read_text(encoding="utf-8")
        self.assertIn("模式 H~L", pipeline)
        self.assertIn("八大反差张力轴", pipeline)
        self.assertIn("十二大结构模型", pipeline)
        self.assertIn("大浴巾", pipeline)
        self.assertIn("存折", pipeline)
        self.assertIn("红桦树皮", pipeline)
        self.assertIn("藕汤面", pipeline)
        self.assertIn("二八大杠", pipeline)

        zhiyin_dna = (wb_dir / "references/zhiyin-dna.md").read_text(encoding="utf-8")
        for mode in ["模式 H", "模式 I", "模式 J", "模式 K", "模式 L"]:
            self.assertIn(mode, zhiyin_dna)
        self.assertIn("沈珂与舅妈", zhiyin_dna)
        self.assertIn("林深与神农架", zhiyin_dna)

        # Ensure both agyskill/boost and .agents/skills/boost have identical synchronized content
        boost_dir = AGYSKILL_DIR / "boost"
        agent_boost_dir = AGENTS_SKILLS_DIR / "boost"
        for b_dir in [boost_dir, agent_boost_dir]:
            b_pipeline = (b_dir / "references/story-pipeline.md").read_text(encoding="utf-8")
            self.assertIn("模式 H~L", b_pipeline)
            self.assertIn("八大反差张力轴", b_pipeline)
            b_beats = (b_dir / "templates/chapter-beat-sheet.md").read_text(encoding="utf-8")
            self.assertIn("模式 H：【创伤互救·生死承诺与无障碍环球跋涉型】", b_beats)
            self.assertIn("模式 L：【沉默父爱·小镇普工隐忍与市井风味共振型】", b_beats)

    def test_boost_skills_feature_2026_elements(self):
        """Verify boost and writing-boost SKILL.md actively feature 2026 core contrasts, physical objects, and headlines."""
        for skill_dir in [AGYSKILL_DIR / "writing-boost", AGYSKILL_DIR / "boost", AGENTS_SKILLS_DIR / "boost"]:
            skill_md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("318", skill_md)
            self.assertIn("40岁大厂失业", skill_md)
            self.assertIn("神农架生态反转", skill_md)
            self.assertIn("拖身大浴巾", skill_md)
            self.assertIn("老父未动存折", skill_md)
            self.assertIn("红桦林中信", skill_md)
            self.assertIn("深夜骨头藕汤面", skill_md)
            self.assertIn("完美恋人意外坠落后", skill_md)
            self.assertIn("被嫌弃的爸爸", skill_md)

    def test_all_skills_markdown_links_integrity(self):
        """Verify NO broken markdown links exist across both agyskill and .agents/skills."""
        broken = []
        for base in [AGYSKILL_DIR, AGENTS_SKILLS_DIR]:
            for md_file in base.glob("**/*.md"):
                content = md_file.read_text(encoding="utf-8", errors="ignore")
                links = re.findall(r"\[.*?\]\((.*?)\)", content)
                for link in links:
                    if link.startswith("http") or link.startswith("mailto:") or link.startswith("{"):
                        continue
                    if link.startswith("file://"):
                        target = Path(link[7:])
                    else:
                        target = (md_file.parent / link.split("#")[0]).resolve()
                    if not target.exists():
                        broken.append((str(md_file), link, str(target)))

        self.assertEqual(len(broken), 0, f"Found broken links: {broken}")

    def test_modular_style_engine_contract_and_catalogue(self):
        """Verify the pluggable style engine implements 6-layer contract and supplies 5 production styles."""
        for base in [AGYSKILL_DIR / "writing-boost", AGYSKILL_DIR / "boost", AGENTS_SKILLS_DIR / "boost"]:
            contract_file = base / "styles/style-contract.md"
            self.assertTrue(contract_file.is_file(), f"style-contract.md missing in {base}")
            contract_text = contract_file.read_text(encoding="utf-8")
            self.assertIn("6-Layer Interface", contract_text)
            self.assertIn("L1 表层语言规范", contract_text)
            self.assertIn("L2 篇章叙事结构", contract_text)
            self.assertIn("L3 选题与反差张力", contract_text)
            self.assertIn("L4 素材与物象策略", contract_text)
            self.assertIn("L5 认知框架与道德立场", contract_text)
            self.assertIn("L6 排版与衍生包装", contract_text)

            styles_readme = base / "styles/README.md"
            self.assertTrue(styles_readme.is_file(), f"styles/README.md missing in {base}")

            expected_styles = [
                ("zhiyin-2026", "知音纪实特稿·极致反差与物象锚定"),
                ("investigative-feature", "深度调查特稿·硬核冷峻与证据闭环"),
                ("personal-memoir", "个人非虚构·克制内省与私人记忆"),
                ("tech-insider", "科技商业特稿·技术哲思与产业暗流"),
                ("literary-travelogue", "人文地理漫游·空间拓扑与历史余温"),
            ]

            for s_id, s_name in expected_styles:
                style_file = base / f"styles/{s_id}/style.md"
                self.assertTrue(style_file.is_file(), f"Style file missing: {style_file}")
                style_content = style_file.read_text(encoding="utf-8")
                self.assertIn(f'id: "{s_id}"', style_content)
                self.assertIn(s_name, style_content)
                self.assertIn("L1", style_content)
                self.assertIn("L2", style_content)
                self.assertIn("L3", style_content)
                self.assertIn("L4", style_content)
                self.assertIn("L5", style_content)
                self.assertIn("L6", style_content)

    def test_adversarial_review_council_subagents(self):
        """Verify the 5 adversarial and multi-dimensional review subagents exist with complete prompts and protocol."""
        for base in [AGYSKILL_DIR / "writing-boost", AGYSKILL_DIR / "boost", AGENTS_SKILLS_DIR / "boost"]:
            agents_dir = base / "agents"
            self.assertTrue(agents_dir.is_dir(), f"agents dir missing in {base}")

            council_proto = base / "references/review-council.md"
            self.assertTrue(council_proto.is_file(), f"references/review-council.md missing in {base}")
            proto_text = council_proto.read_text(encoding="utf-8")
            self.assertIn("devils-advocate", proto_text)
            self.assertIn("logic-inquisitor", proto_text)
            self.assertIn("slop-hunter", proto_text)
            self.assertIn("pacing-auditor", proto_text)
            self.assertIn("chief-editor", proto_text)

            expected_agents = [
                ("devils-advocate.md", ["廉价煽情", "爹味说教", "纸片人", "出戏时刻"]),
                ("logic-inquisitor.md", ["物理现实", "时间线", "信息守恒", "零幻觉"]),
                ("slop-hunter.md", ["不是……而是……", "假转折", "三元对称", "排比"]),
                ("pacing-auditor.md", ["前 15% 黄金抓手", "概念奠基", "电荷反转", "物象收束"]),
                ("chief-editor.md", ["加权终审", "冲突调和", "及格线", "退修三部曲手术方案"]),
            ]

            for fname, key_phrases in expected_agents:
                agent_path = agents_dir / fname
                self.assertTrue(agent_path.is_file(), f"Agent file missing: {agent_path}")
                agent_text = agent_path.read_text(encoding="utf-8")
                for phrase in key_phrases:
                    self.assertIn(phrase, agent_text, f"Missing phrase '{phrase}' in {agent_path}")

    def test_readme_beautification_and_assets(self):
        """Verify README follows beautify-github-readme standards with valid local SVG assets."""
        import xml.etree.ElementTree as ET

        readme_files = [
            ROOT / "README.md",
            AGYSKILL_DIR / "writing-boost/README.md",
        ]

        for readme in readme_files:
            self.assertTrue(readme.is_file(), f"README missing: {readme}")
            content = readme.read_text(encoding="utf-8")
            self.assertIn("writing-boost", content)
            self.assertIn("hero-banner.svg", content)
            self.assertIn("pipeline-architecture.svg", content)
            self.assertIn("Pluggable Style", content)
            self.assertIn("Adversarial Review Council", content)

        # Audit SVGs
        svg_files = [
            ROOT / "assets/readme/hero-banner.svg",
            ROOT / "assets/readme/pipeline-architecture.svg",
            AGYSKILL_DIR / "writing-boost/assets/readme/hero-banner.svg",
            AGYSKILL_DIR / "writing-boost/assets/readme/pipeline-architecture.svg",
        ]

        for svg_path in svg_files:
            self.assertTrue(svg_path.is_file(), f"SVG missing: {svg_path}")
            root = ET.parse(svg_path).getroot()
            self.assertIn("viewBox", root.attrib, f"Missing viewBox in {svg_path}")
            has_title = any(child.tag.rsplit("}", 1)[-1] == "title" for child in root.iter())
            self.assertTrue(has_title, f"Missing <title> in {svg_path}")
            for node in root.iter():
                tag = node.tag.rsplit("}", 1)[-1]
                self.assertNotIn(tag, {"script", "foreignObject"}, f"Unsafe tag <{tag}> in {svg_path}")


if __name__ == "__main__":
    unittest.main()

