# Quality Gates

> 本文件定义 Hard / Soft Gate、severity 与 strong-review trigger 的**语义**。所有数值阈值只从 [../runtime-contract.json](../runtime-contract.json) 读取，避免双写。

## 1. Hard Gates

命中任一项时不能直接交付：

- **Alignment**：目标、读者、事实边界、POV、字数或交付物仍存在会实质改变成稿的未决歧义。
- **Length**：实际长度落在锁定验收区间之外。
- **Fidelity**：非虚构出现 UNKNOWN 细节写成事实、无来源引语、错误时间计算、实体属性脑补或 Claim Strength 膨胀。
- **POV**：标题与正文人称冲突，且未明确标记为不同版本。
- **Review**：仍存在未解决 BLOCKER。
- **Delivery**：用户明确要求的正文 / 标题 / 摘要 / 引用 / 平台版本缺项。

## 2. Strong Review Triggers

是否强制 Integrity + Editorial 双审，由 runtime contract 的阈值与 flags 决定。语义如下：

- **long nonfiction**：达到当前 count_mode 对应长篇阈值；
- **high_stakes_fact_domain**：医疗、法律、财务、技术安全等，错误成本显著高于普通叙事；
- **timeline_dense**：明确年份达到 runtime contract 阈值，或大量使用“X 年前 / 后 / 持续 N 年”；
- **quote_or_number_dense**：人物引语、金额、百分比、日期、统计数字密集，容易发生跨段污染；
- **cross_domain_major_issues**：Stage 5 同时出现 Integrity 与 Editorial 两个关注面的 MAJOR；
- **user_requests_deep_cross_review**：用户明确要求深度、法医级、交叉审核。

长篇阈值是**默认强触发器，不是唯一触发器**。短稿只要命中高风险 flag，也应双审。

## 3. Soft Gates

以下问题允许交付，但应在当前循环预算内尽量修正：

- 局部重复；
- 轻微节奏不均；
- 非关键句风格漂移；
- 单个不影响事实的陈词滥调；
- 包装版本的偏好分歧。

Soft Gate 不得单独驱动无限循环。

## 4. Severity Definition

### BLOCKER

会导致事实错误、职业伦理风险、用户契约违背，或使正文无法按要求使用。

### MAJOR

明显影响理解、可信度、结构推进、目标读者体验或主风格。

### MINOR

局部瑕疵；修正有益，但不影响文章成立。

### NOTE

偏好性建议或可选替代。NOTE 不进入自动修订队列，除非用户明确采纳。

## 5. Issue Identity

每个 reviewer finding 必须有稳定 Issue ID：

- Integrity：`IR-001`, `IR-002` …
- Editorial：`ER-001`, `ER-002` …

同一位置、同一根因、同一修复目标视为同一个 issue。下一轮不得仅因措辞不同创建新 ID。

已 FIXED issue 只有在**发生回归**或出现新证据时才能 reopen。

Round 2 及以后：

- 优先验证旧 issue 是否关闭；
- 新出现的 BLOCKER / MAJOR 可以新增；
- 默认不再为新 MINOR 开 issue，除非用户明确要求精修。

这些收敛规则以 runtime contract 的 `loops` 字段为机器真源。

## 6. Regression Rule

每轮修改后至少回查：

- 新增 / 删除事实是否改变来源边界；
- 时间、数字、人名、引用是否因改句而出错；
- 字数是否越界；
- POV 是否漂移；
- 已冻结有效段落是否被无理由重写；
- 修一个问题是否重新引入上一轮已关闭 issue。

变更记录使用 [../templates/revision-log.md](../templates/revision-log.md)，当前 round 状态使用 [../templates/loop-state.md](../templates/loop-state.md)。
