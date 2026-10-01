# 六阶段写作管线

> 前置条件：已经完成《开稿对齐卡》和字数锁。Explore 是可选探索，不计入六阶段。

## Artifact Lifecycle

| Stage | 主要输入 | 稳定输出 / checkpoint artifact |
| :--- | :--- | :--- |
| 1 Topic | Alignment Card + 原料 | Topic brief / 核心命题 |
| 2 Evidence | Topic brief + 来源 | Nonfiction Ledger / 创作设定账本 |
| 3 Shape | Ledger + style + length lock | Beat Sheet + 字数预算 |
| 4 Draft | Beat Sheet + Ledger | Draft v0 |
| 5 Self-review | Draft v0 + loop state | Revised Draft + Revision Log |
| 6 Final review | Revised Draft + Ledger | Review Scorecard + Final + Delivery Receipt |

回退时优先回到**最早失效的稳定 artifact**，不要把其前面的已验收产物一起推倒。


## Stage 1：选题与命题

**输入**：对齐卡、用户材料、探索碎片。

完成前必须明确：

- 一句话核心命题；
- 目标读者真正关心的问题；
- 文章需要建立的阅读承诺；
- 当前 style；
- 本文不处理的范围。

**完成标准**：不用“深度、价值、共鸣”等空词，也能用 1–2 句话说明文章为什么值得读。

## Stage 2：素材与证据

对非虚构，读取 [nonfiction-fidelity.md](nonfiction-fidelity.md) 并生成 [../templates/nonfiction-ledger.md](../templates/nonfiction-ledger.md)：

- 锁定 `source_policy / reconstruction_policy / unknown_policy`；
- 建立 Source Index 与 Claim Ledger，分别记录 FACT / CAUSAL / MOTIVE / PSYCHOLOGY / INTERPRETATION 的证据强度；
- 建立绝对时间轴，所有“X 年前 / X 年后 / 持续 N 年”先做显式算术再进入正文；
- 建立事实 / 引语 / 数字 / 来源清单；
- 建立实体属性锁，品牌、族群、颜色、年龄、地点、物件属性未知时明确写入“禁止脑补”；
- 原话标记为 VERBATIM / LIGHT-CLEAN / PARAPHRASE；
- 建立核心物象账本，记录首次出现、中段动作、后段回收及来源；
- 标出 UNKNOWN / RECONSTRUCTED 项，不把素材缺口用模型想象补齐。

对小说 / 创作：

- 建立人物状态、世界规则、已知事件和本次允许新增的边界。

**完成标准**：正文计划中的关键事实或关键设定都有来源 / 授权；关键因果、动机和心理主张没有超过 Claim Ledger 的证据强度；所有相对时间都有绝对锚点；引号内对白都有 Quote ID；关键实体不存在待模型自由补全的属性空洞。

## Stage 3：结构与字数预算

读取 [alignment-and-length.md](alignment-and-length.md) 和当前 style。

把对齐卡中的 `target` 按同一 `count_mode / count_scope` 拆成段落 / 场景预算：

| 单元 | 功能 | 预计字数 | 必须承载的信息 / 场景 |
| :--- | :--- | ---: | :--- |
| 1 | | | |
| 2 | | | |

规则：

- 所有预算总和落在 runtime contract 的结构预算容差内，并使用对齐卡锁定的同一 `count_mode`。
- 结构比例服从当前 style，不使用全局 15/70/15。
- 每个单元必须有功能，不能为凑字数制造空段。
- 若当前 style 使用物象锚定，每个主要单元至少登记 1 个**来源支持的物象动作 / 状态变化 / 回收点**；不能只在开头摆出物件，后半程遗忘。
- 结构完成后按 [loop-policy.md](loop-policy.md) 执行 shape loop；默认轮数读取 runtime contract，用户可全局或用 `--shape-loops N` 单独覆盖。

**完成标准**：删掉任何一个单元都会明确损失信息、推进、证据或情绪功能；物象账本没有只登场不回收的核心物象；字数预算闭合。

## Stage 4：分段 / 分场写作

按结构单元推进，不一次把后面所有段落提前写完。

每完成一个主要结构节点，检查：

- 是否偏离核心命题；
- 是否引入无来源事实、属性、现场氛围或动作；
- 是否把 `ATTRIBUTED / INFERRED` 的因果、动机或心理写成了无归属的确定事实；
- 相对时间是否来自 Stage 2 的 Derived Facts，而不是凭感觉写“几年前”；
- 引号对白是否来自已登记原话，是否被过度雅化；
- 当前段落是否完成登记的物象动作 / 回收；
- POV 是否仍与对齐卡一致；
- 已用字数 vs 预算；
- 是否提前消费了后文的信息或结论。

累计长度偏差超过 runtime contract 的 `cumulative_budget_drift_ratio` 时，在下一单元调整；不要用重复解释硬凑。

## Stage 5：主会话自检与 Deslop

以 Stage 4 初稿为基线，按 runtime contract 执行 draft loop；用户可用 `--loops N` 或 `--draft-loops N` 覆盖：

- **Loop 1（硬正确性）**：信息守恒、时间算术、实体属性、原话保真、POV、连续性、字数。
- **Loop 2（编辑质量）**：重复与无功能段落、当前 style、一致性、物象回收、高置信 deslop、网文烂梗与说教句。

每轮只改可定位问题；已经有效的段落冻结，不为了“有变化”重写。

短文本和低风险稿件到这里通常已经可以交付；重要非虚构长稿仍必须进入 Stage 6。

## Stage 6：终审与交付

只有这一阶段允许 reviewer。读取 [review-council.md](review-council.md)。

根据风险调用 0 / 1 / 2 个 reviewer：

- Integrity：事实、约束、时间算术、属性溯源、原话、连续性；
- Editorial：读者、结构、节拍、风格、烂梗、说教与 AI 痕迹。

**命中 [quality-gates.md](quality-gates.md) 的 Strong Review Trigger 时固定调用两个 reviewer。** 具体数值与 flags 从 runtime contract 读取；review loop 数服从 runtime contract 或用户覆盖，每轮 reviewer 上限始终为 2。

主会话合并 findings 并最终修改；每轮修改写入 [../templates/revision-log.md](../templates/revision-log.md)。若 `delivery_receipt != hidden`，交付正文后附 [../templates/delivery-receipt.md](../templates/delivery-receipt.md) 的简版回执。

**最终门禁**（severity 语义见 [quality-gates.md](quality-gates.md)）：

- BLOCKER = 0；
- 字数落入验收区间；
- 事实边界未被突破；
- 当前 style 没有被通用规则覆盖；
- 用户要求的交付物全部存在。
