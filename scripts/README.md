# Deterministic checks

这些脚本只负责可确定计算，不代替语义审稿。

- `text_metrics.py`：统一字数口径并验证目标区间。
- `lint_cliches.py`：定位中文纪实高风险套话；命中只是 review trigger，不自动删除原话或引用。
- `check_skill_contract.py`：检查版本、六阶段、双 reviewer、绝对路径和内部链接等架构不变量。

示例：

```bash
python3 scripts/text_metrics.py draft.md --mode zh_units --target 3000
python3 scripts/lint_cliches.py draft.md
python3 scripts/check_skill_contract.py
```

`zh_units` 的定义来自根目录 `runtime-contract.json`：每个汉字计 1；连续英文/数字 token 计 1；空白和标点不计。Markdown 稿件若只想统计可见正文，可加 `--markdown-prose` 去掉 frontmatter、代码块、图片语法、链接目标和 HTML 标签。若目标平台有自己的计数器，应在开稿对齐卡选择 `platform`，以平台结果为准。
