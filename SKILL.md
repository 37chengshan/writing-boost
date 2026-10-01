---
name: writing-boost
description: 对齐优先的系统化写作工程框架。先锁定目标、读者、事实边界、风格、交付物与字数，再进入素材、结构、写作、去 AI 味和终审；终审阶段最多调用两个交叉 reviewer，主会话负责最终裁决。用于特稿、调查、真实故事、回忆录、科技商业长文、文旅与其他长文写作。
metadata:
  version: 3.3.0
  author: Writing Lab System
  pillars:
    - alignment-first
    - locked-length
    - pluggable-style-engine
    - two-reviewer-cross-review
    - information-conservation
    - evidence-based-deslop
    - budgeted-loops
    - nonfiction-fidelity
---

# writing-boost

把写作当成一个有明确输入、约束、循环预算和验收标准的工程流程。**先与用户对齐，再写；先锁字数，再拆结构；结构/正文/终审按 runtime contract 默认双循环；子代理只用于终审，最多两个。**

## 0. 总原则

以下规则始终有效：

1. **Alignment first**：进入正文前必须完成《开稿对齐卡》。用户已经给出的信息直接复用，不重复追问。
2. **Length lock**：正文前锁定 `target / acceptance_band / count_mode / count_scope`。写完后才换尺子或估字数属于流程失败。
3. **Ground truth**：非虚构与改写任务遵守信息守恒，不新增无来源事实、数字、引语、因果、心理和限定强度。
4. **Style is a plugin**：具体节奏、Hook 比例、物象数量、段落厚度由当前 style 决定，核心引擎不写死一种审美。
5. **Progressive disclosure**：只加载当前阶段需要的 reference；不要把所有规范一次性塞进上下文。
6. **Review is exceptional**：写作、改写、deslop 默认由主会话完成；只有 review 阶段可派 reviewer，硬上限 2。
7. **Main session decides**：reviewer 只提供 findings；最终合并、取舍和改稿由主会话完成。
8. **Budgeted loops**：默认值和分阶段循环预算以 [`runtime-contract.json`](runtime-contract.json) 为单一真源。用户可用 `--loops N` 全局覆盖，也可分别指定 `--shape-loops / --draft-loops / --review-loops / --package-loops`。用户反馈只回退到最早受影响阶段，不整线重跑。读取 [references/loop-policy.md](references/loop-policy.md)。
9. **Nonfiction fidelity**：纪实稿所有看似“现场”的细节也属于事实，必须有来源、确定性推导或明确重构授权；关键因果、动机和心理还必须遵守 Claim Strength。默认 source policy 读取 runtime contract。详见 [references/nonfiction-fidelity.md](references/nonfiction-fidelity.md)。

## 1. 开稿：先对齐用户

只要用户要的是成稿、改写后的完整稿件或结构性重写，第一步读取：

- [references/alignment-and-length.md](references/alignment-and-length.md)
- [templates/alignment-card.md](templates/alignment-card.md)

先把已经明确的信息填进《开稿对齐卡》，至少锁定：

- 目标
- 目标读者
- 体裁 / 平台
- 核心命题
- 事实边界 + `source_policy / reconstruction_policy / unknown_policy`
- 正文人称 / POV
- 原话处理方式
- 风格
- **目标字数、验收区间、`count_mode` 与 `count_scope`**
- **循环预算**（默认值来自 runtime contract；可全局或分阶段覆盖）
- interaction mode / checkpoints
- 交付物
- 必须保留 / 避开

### 缺信息时

- 只问会实质改变成稿的缺口。
- 用户说“你定”“直接写”“不用问”时，补齐合理默认值，**明确回显默认值后立即执行**。
- 不展示内部推理过程，只展示可供用户纠偏的契约结论。

### 完成标准

在进入 shape / write 前，必须能用一句话回答：

> 我们正在为谁，用什么体裁，在什么事实边界内，写一篇解决什么问题、目标多少字、最终交付什么的文章？

答不出来就还没有完成对齐。

## 2. 路由

| 用户意图 | 执行 | 按需加载 |
| :--- | :--- | :--- |
| `/writing-boost` | 建立对齐卡并决定下一步 | alignment-and-length |
| `explore` | 扩素材，不直接写成稿 | grounding-and-beats, raw-fragments |
| `shape` / `beats` | 在字数锁内拆结构与内容预算；loop 预算来自 runtime contract | grounding-and-beats, chapter-beat-sheet, loop-policy |
| `write` | 运行六阶段写作管线；正文按 runtime contract 执行修订闭环 | story-pipeline + 当前 style + loop-policy |
| `style` | 查询 / 新建风格 | styles/style-contract.md, styles/README.md |
| `distill` | 蒸馏作者 / 刊物 DNA | writing-dna-distillation |
| `deslop` | 最小改动去生成式套路 | deslop-whitelist-zh 或 deslop-prose-en |
| `review` | 按风险调用 0/1/2 reviewer | review-council + reviewer prompt |
| `package` | 标题与平台转译 | social-packaging |

## 3. 六阶段写作管线

对齐完成后读取 [references/story-pipeline.md](references/story-pipeline.md)。

六阶段是：

1. 选题与命题
2. 素材与证据
3. 结构与字数预算
4. 分段 / 分场写作
5. 主会话自检与 deslop
6. 终审与交付

Explore 属于可选前置探索，不计入六阶段，因此不再出现“阶段 0 到 6 却叫六阶段”的歧义。

每一阶段必须有可检查的完成标准，未通过不得假装完成。结构、正文和终审的循环语义统一遵循 [references/loop-policy.md](references/loop-policy.md)。

非虚构任务在 Stage 2 必须生成 [templates/nonfiction-ledger.md](templates/nonfiction-ledger.md)：Source Index、Claim Ledger、绝对时间轴、派生时间算术、实体属性、原话模式、物象回收账本和 POV 都在这里锁定。

## 4. 风格

读取 [styles/style-contract.md](styles/style-contract.md)。当前预装：

- `zhiyin-2026`
- `investigative-feature`
- `personal-memoir`
- `tech-insider`
- `literary-travelogue`

用户明确风格 > 当前 style > 通用写作建议。

风格文件可以规定具体结构比例、句长倾向、物象策略、段落节奏；核心引擎不替 style 写这些数字。

## 5. 去 AI 味

中文读取 [references/deslop-whitelist-zh.md](references/deslop-whitelist-zh.md)，英文 / 通用 prose 读取 [references/deslop-prose-en.md](references/deslop-prose-en.md)。

执行顺序：

1. 先保事实、观点、限定词与结构功能。
2. 再处理高置信、可定位的生成式套路。
3. 需要语义判断的项目以当前 style 为准。
4. 只改解决问题所需的最小范围。
5. 改后重新检查字数锁。

`stop-slop` 的激进规则只作为可选编辑参考，不升级为全局硬禁令。

## 6. 终审：最多两个 reviewer

读取 [references/review-council.md](references/review-council.md)。

可用 reviewer 只有两类：

- [agents/integrity-reviewer.md](agents/integrity-reviewer.md)
- [agents/editorial-reviewer.md](agents/editorial-reviewer.md)

按风险选择 0 / 1 / 2 个。**任何时候都不得超过 2 个，也不得再派 chief-editor 子代理。** 是否强制双审同时参考 `runtime-contract.json` 的长篇阈值与 strong-trigger flags，并按 [references/quality-gates.md](references/quality-gates.md) 解释；因此短稿在医疗 / 法律 / 财务 / 技术安全、密集时间线或用户明确要求深度交叉审核时也可强制 Integrity + Editorial。review 循环次数同样服从 runtime contract 或用户覆盖。

如果宿主支持给 reviewer 选择不同模型，并且本次需要双路交叉审核：

- 先告诉用户不同模型可能减少相关性盲点；
- 如果用户尚未授权模型，询问“可以用哪些模型做审查”；
- 最多使用两个用户允许的模型；
- 不静默使用外部或更高价格模型。

主会话根据 findings 填写 [templates/review-scorecard.md](templates/review-scorecard.md)，循环修改追加到 [templates/revision-log.md](templates/revision-log.md)。交付前按需生成 [templates/delivery-receipt.md](templates/delivery-receipt.md)；若用户明确“只要正文”，回执不展示。

## 7. 确定性工具

当宿主可执行本 skill 内脚本时，优先使用：

- `scripts/text_metrics.py`：字数与验收区间；
- `scripts/lint_cliches.py`：高风险纪实套话定位；
- `scripts/check_skill_contract.py`：架构不变量和链接自检。

脚本只处理确定性问题，不能替代语义审稿。

## 8. 最终验收

Hard / Soft Gate 与 severity 统一读取 [references/quality-gates.md](references/quality-gates.md)。交付前必须全部满足：

- 对齐卡没有被悄悄改写；
- 实际字数落在锁定验收区间；
- 非虚构事实与限定词没有无依据变化；
- 当前 style 的关键约束已执行；
- 所有 BLOCKER 已清零；
- 交付物齐全。

如果无法满足某项，明确告诉用户哪一项未满足，不用“整体不错”掩盖。
