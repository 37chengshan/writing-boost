# 有预算的写作闭环 (Budgeted Writing Loops)

> 循环用于修正可定位问题，不用于让模型无目的地“再想一遍”。所有默认数值以 [../runtime-contract.json](../runtime-contract.json) 为单一真源。

## 1. 两种 Loop

### Automatic Loop

系统在用户没有额外反馈时主动执行的闭环：

```text
当前产物
→ Gate 检查
→ 生成 issue set
→ 只修 issue set
→ Regression check
→ PASS / 下一轮
```

`loops=N` 表示**初始产物之后最多执行 N 个修订闭环**。初始产物本身不计入 N。

### Feedback Loop（用户反馈闭环）

用户看过任何中间产物或终稿后提出新意见：

```text
用户反馈
→ 归一化为 user_delta
→ 找最早受影响阶段
→ 冻结未被否定内容
→ 局部回退
→ 修改与验收
```

Feedback Loop 不消耗已经结束的 Automatic Loop 预算。用户继续给新意见，就继续新的反馈轮。

## 2. 参数覆盖

默认循环预算只读取 runtime contract 的 `loops_by_stage`：Shape=2、Draft=2、Review=2、Packaging=0。不存在第二套“全局默认值”；`--loops N` 只是用户显式覆盖。

用户可以：

- `--loops N`：统一覆盖所有支持自动循环的阶段（如 `--loops 0` 关闭自动循环）；
- `--shape-loops N`
- `--draft-loops N`
- `--review-loops N`
- `--package-loops N`

分阶段参数优先于全局参数。

例如：

```text
--loops 2 --review-loops 1
```

表示 Shape/Draft 使用 2，Review 使用 1。

`N=0` 只关闭该阶段的**自动**修订，不关闭之后由用户意见触发的 Feedback Loop。

## 3. Interaction Mode

默认 `auto`：Alignment 锁定后继续执行，不为了“更互动”而每阶段停下来。

用户选择 `checkpoint` 时，只在指定节点展示当前 artifact：

- `shape`：结构、字数预算、关键物象 / 证据映射；
- `draft`：草稿或指定章节；
- `review`：主会话已经去重合并的 findings / 修订摘要。

用户在 checkpoint 提意见后进入 Feedback Loop；用户说继续，则不额外消耗 feedback round。checkpoint 不增加 reviewer 数量，也不改变自动 loop budget。

## 4. 各阶段循环职责

### Alignment

不机械循环。回显《开稿对齐卡》后：

- 用户有纠偏 → 更新后重新锁定；
- 用户已明确授权“你定 / 直接写” → 补齐默认值后立即继续；
- 不为了达到两轮而重复问相同问题。

### Shape / Beats

每轮按固定 gate 检查：

1. 核心命题是否被结构覆盖；
2. 每个单元是否有独立功能；
3. 字数预算是否闭合；
4. 事实 / 时间 / POV / Quote ID 是否与账本一致；
5. 当前 style 要求的物象是否完成跨节回收规划；
6. 是否存在后文信息被提前消费。

第二轮不是重新起一个大纲，而是验证第一轮修复和回归。

### Draft / Rewrite

默认两类关注面：

- **Correctness pass**：事实、时间算术、实体属性、原话、POV、连续性、字数；
- **Editorial pass**：结构兑现、节拍、style、一致性、重复、烂梗、deslop、物象漂移。

`loops=1` 时把两类检查合并为一轮。
`loops>=2` 时前两轮按上述分工；额外轮只处理上一轮遗留 issue，不再开启新的无边界重写。

### Review

每轮最多两个 reviewer：

```text
review findings
→ 主会话去重与裁决
→ 修改
→ regression re-review
```

Round 1 可以全量找问题，并给 issue 分配稳定 ID。
Round 2 及以后首先验证旧问题是否关闭、是否产生回归；沿用原 Issue ID。只有新出现的 BLOCKER / MAJOR 才进入 issue set；新 MINOR 默认不再开 issue，除非用户明确要求精修。
已 FIXED issue 只有发生 regression 或出现新证据时才能 reopen。

这些收敛行为以 runtime contract 的 `loops` 字段为机器真源，severity / Issue ID 语义读取 [quality-gates.md](quality-gates.md)。

增加 loop 数量**不能增加 reviewer 数量**。

### Packaging

默认不自动循环。标题、摘要、社交版本先产出一版；用户不满意时只循环 Packaging。
若用户显式指定 `--package-loops N`，则可自动检查 POV、事实、平台字数和标题重复度后修订。

## 5. User Delta

不要把“我不喜欢”直接当成“全部重写”。

先把用户反馈规范成：

- **target**：用户要改变什么；
- **scope**：影响全文、某节、某句还是包装；
- **preserve**：用户没否定、必须冻结的部分；
- **acceptance**：怎样算这轮改对。

例：

```text
原反馈：开头太慢，但医院那段别动。

target: 前 300 字更快进入夜市冲突
scope: Stage 3/4 的 opening
preserve: 医院段及其事实、原话、物象
acceptance: 背景压缩，主冲突提前，不新增事实
```

## 6. 回退矩阵

| 用户反馈 | 最早回退点 |
| :--- | :--- |
| 目标、受众、平台、总字数、正文 POV 改变 | Alignment |
| 来源、事实、人物属性、原话、时间轴改变 | Evidence / Stage 2 |
| 信息顺序、重点、开头、章节结构改变 | Shape / Stage 3 |
| 句子、对白、语气、局部节奏改变 | Draft / Stage 4 |
| AI 味、重复、风格漂移 | Self-review / Stage 5 |
| reviewer 未关闭 BLOCKER / MAJOR | Review / Stage 6 |
| 标题、摘要、社交版问题 | Packaging |

回退到某阶段时，只重新执行该阶段以及真正受其影响的后续产物。**局部反馈不触发全流程重跑。**

## 7. Frozen Set

每一轮必须显式维护：

- `frozen_constraints`：字数、事实边界、POV、style 等已锁约束；
- `frozen_content`：用户明确要求保留、或上一轮已验收通过的内容；
- `issue_set`：本轮唯一允许主动修改的问题；
- `regressions`：本轮修改新引入的问题。

除非 user_delta 明确解冻，否则不得为了改善别处而顺手改 frozen set。

## 8. Loop State

使用 [../templates/loop-state.md](../templates/loop-state.md)，并把每轮实际修改追加到 [../templates/revision-log.md](../templates/revision-log.md)。至少记录：

- stage
- round / max_rounds
- loop_type: automatic / feedback
- user_delta
- frozen_constraints
- frozen_content
- issue_set
- changes_made
- regressions
- acceptance_result

## 9. 停止条件

Automatic Loop 满足任一条件即可提前停止：

- Gate 已通过且 BLOCKER / MAJOR = 0；
- 本轮没有新的实质修改；
- 连续一轮没有任何硬指标改善（OPEN BLOCKER / MAJOR 未下降，也没有关闭回归）；
- 剩余分歧只能由用户审美决定；
- 继续改会破坏 frozen set、事实守恒或字数锁；
- 已达到该阶段 loop budget。

Feedback Loop 在用户满意、用户改变任务、或用户明确停止时结束。

**停止不是失败。** 如果达到预算后仍有未解决问题，直接把未解决项交给用户，不用偷偷开启额外循环。
