# ⚡ writing-boost

**Alignment-first writing engineering · locked length · budgeted loops · pluggable styles · max-two cross review**

Version 3.2.0

`writing-boost` 把长文写作拆成一套有明确输入、事实边界、字数口径、循环预算、风格契约与终审门禁的流程。核心原则：

> **先对齐、再写；先锁尺子、再锁字数；关键阶段允许闭环，但不无限反刍；子代理只在终审出现，每轮最多两个。**

运行时默认数值统一由 [runtime-contract.json](runtime-contract.json) 管理，避免 README、SKILL、测试和 reviewer 各自维护一套数字。

## 开稿对齐

正文前锁定：

- 目标、读者、体裁 / 平台、核心命题
- 事实边界
- 正文 POV
- 原话处理：VERBATIM / LIGHT-CLEAN / PARAPHRASE
- 当前 style
- `target / min / max / count_mode`
- 循环预算
- 交付物、必须保留与避开项

用户已经说明的内容直接复用。用户说“你定 / 直接写”时，系统补合理默认值并回显，不反复盘问。

### Count mode

默认：

- 中文：`zh_units`，每个汉字计 1，连续英文 / 数字 token 计 1，标点与空白不计；
- 英文：`words`；
- 用户明确以公众号、平台后台等计数为准时：`platform`。

全流程必须使用同一个 `count_mode`，避免结构阶段和终审阶段换尺子。

## Budgeted Loops

完整协议见 [references/loop-policy.md](references/loop-policy.md)。

`loops=N` 表示**初始产物之后最多 N 个修订闭环**：

```text
Gate → issue set → 局部修改 → regression check → PASS / next round
```

当前默认值来自 runtime contract：

- Shape：2
- Draft：2
- Review：2
- Packaging：0

用户可以用：

```text
--loops N
--shape-loops N
--draft-loops N
--review-loops N
--package-loops N
```

用户后续不满意时进入 Feedback Loop：把意见转成 `user_delta`，只回退到最早受影响阶段，并冻结用户没有否定的内容。

## 非虚构事实账本

读取 [references/nonfiction-fidelity.md](references/nonfiction-fidelity.md) 与 [templates/nonfiction-ledger.md](templates/nonfiction-ledger.md)。

显式管理：

- 绝对时间轴
- “X 年前”等 Derived Facts
- 实体已知属性 / 禁止脑补属性
- Quote ID 与原话模式
- 核心物象的登场 / 动作 / 回收
- 正文与标题 POV

“旧车”不会自动变成具体品牌；“小哥”不会自动获得民族标签；光线、气味、天气、服装和微动作也不能因为“只是氛围”就自由虚构。

## 沙盒六类缺陷的对应防线

| 缺陷 | 防线 |
| :--- | :--- |
| 网文烂梗、爹味说教 | cliche patterns + Editorial |
| 年份算术硬伤 | nonfiction ledger + Integrity 复算 |
| 细节脑补、标签膨胀 | 实体属性锁 + Information Conservation |
| 后半程物象失踪 | beat sheet 物象账本 + Editorial |
| 标题 / 正文人称割裂 | Alignment POV lock + social packaging |
| 方言 / 原话被雅化 | Quote ID + VERBATIM 保真 |

## Review：最多两个 reviewer

唯一可调度：

- [Integrity Reviewer](agents/integrity-reviewer.md)：事实、来源、时间算术、实体属性、原话、连续性、POV、字数契约。
- [Editorial Reviewer](agents/editorial-reviewer.md)：读者体验、结构、节拍、style、AI 痕迹、网文烂梗、说教、对白颗粒度、物象漂移。

调度规则：

- 低风险短文本：0
- 单一风险：1
- 一般重要长稿：1–2
- 达到 runtime contract 长篇阈值的纪实 / 调查 / 人物报道：固定双审
- 每轮 reviewer 硬上限：2
- 最终裁决始终由主会话完成

当前默认长篇阈值：

- 中文 `zh_units >= 3000`
- 英文 `words >= 1800`

如果宿主支持显式选择不同 reviewer 模型，第一次需要异构双审时先询问用户允许哪些模型；不会静默使用外部或高价格模型。

旧五角色仅保留 deprecated stub，不再调度。

## 六阶段

1. 选题与命题
2. 素材与证据
3. 结构与字数预算
4. 分段 / 分场写作
5. 主会话自检与 deslop
6. 终审与交付

Explore 是可选前置探索，不计入六阶段。

## Style Engine

核心接口见 [styles/style-contract.md](styles/style-contract.md)。

预装：

- `zhiyin-2026`
- `investigative-feature`
- `personal-memoir`
- `tech-insider`
- `literary-travelogue`

15/70/15、三件物象、手机段落 2–4 行等只能属于具体 style，不能成为全局核心规则。

## Deterministic checks

[scripts/README.md](scripts/README.md)

```bash
python3 scripts/text_metrics.py draft.md --mode zh_units --target 3000
python3 scripts/lint_cliches.py draft.md
python3 scripts/check_skill_contract.py
```

脚本负责确定性问题，模型负责语义判断。固定短语扫描命中只是 review trigger，不等于自动删除真实引语。

## 去 AI 味

- [references/deslop-whitelist-zh.md](references/deslop-whitelist-zh.md)
- [references/cliche-blacklist-zh.md](references/cliche-blacklist-zh.md)
- [references/deslop-prose-en.md](references/deslop-prose-en.md)

优先级：

```text
用户明确要求
> 事实与信息守恒
> 开稿对齐卡
> 当前 style
> 作者风格档案
> 通用 deslop 建议
```

## 验证

```bash
python3 scripts/check_skill_contract.py
python3 -m unittest tests/test_writing_framework.py
```

所有测试与脚本均以 skill 自身目录为根，不依赖作者机器的绝对路径或外部语料库。
