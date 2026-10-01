# 双路交叉终审协议 (Two-Reviewer Cross Review)

> 子代理只允许出现在 review 阶段；任何一次审查最多调用两个 reviewer。主会话始终负责最终合并与改稿，不再额外派遣 chief-editor 子代理。

## 1. 两个正交 Reviewer

| Reviewer | 负责 | 不负责 |
| :--- | :--- | :--- |
| [integrity-reviewer](../agents/integrity-reviewer.md) | 来源、信息守恒、事实、时间空间因果、连续性、用户契约 | 文风偏好、修辞审美 |
| [editorial-reviewer](../agents/editorial-reviewer.md) | 读者体验、结构节拍、风格一致性、AI 痕迹、煽情与说教 | 外部事实核验 |

主会话是 synthesizer。它负责去重、判断冲突、决定修改优先级，并执行最终修改。**不要再 spawn 第三个“主编”代理。**

## 2. 0 / 1 / 2 动态调度

### 0 reviewer

以下情况主会话自己检查即可：

- 短文本、局部润色、标题、摘要；
- 低风险改写；
- 只做确定性 deslop 扫描；
- 用户明确要求快速处理且不需要交叉审核。

### 1 reviewer

只派最相关的一路：

- 事实密集、调查、纪实、技术 / 医学 / 法律约束多：优先 Integrity。
- 纯文学、品牌语气、去 AI 味、节拍与读感：优先 Editorial。

### 2 reviewers

同时派两路用于：

- **达到 runtime contract 当前 `count_mode` 的非虚构长篇阈值时，纪实特稿、调查、人物报道最终交付强制双审**；当前默认中文 `zh_units >= 3000`，英文 `words >= 1800`。
- 其他重要长稿最终交付；
- 用户明确要求“深度审查 / 交叉审核”；
- 同时存在事实风险与明显编辑风险；
- 第一轮主会话发现问题跨越两个关注面。

**硬上限：2。** reviewer 不能再派子代理。强制双审指“两个正交 reviewer”，不是恢复五人委员会。

## 3. 不同模型的交叉审核

如果宿主运行时支持为 reviewer **显式选择不同模型**：

1. 在第一次需要双路终审时告诉用户：不同模型家族可能降低相关性盲点。
2. 若用户尚未指定，先询问用户允许用于审查的模型名单 / 额度范围。
3. 最多选两个模型，分别承担 Integrity 与 Editorial。
4. 不得静默切到外部模型、更高价格模型或用户未授权的模型。

如果宿主不能选择 reviewer 模型：

- 使用当前可用模型的隔离上下文；
- 仍保持两个 reviewer 的关注面独立；
- 不要把这种情况描述成“异构模型交叉审核”。

## 4. 合并规则

主会话按以下顺序合并：

1. `BLOCKER`：事实越界、信息新增、用户契约违反、严重连续性错误。
2. `MAJOR`：明显影响理解、可信度、目标读者体验或风格一致性的问题。
3. `MINOR`：局部可优化但不影响交付的问题。
4. 两 reviewer 冲突时，优先级为：
   - 用户明确要求
   - 事实 / 信息守恒
   - 已锁定 style
   - 编辑建议
5. reviewer 的建议不是命令。主会话必须回看原文后再修改。

## 5. Review Loop

review 阶段遵循 [loop-policy.md](loop-policy.md)（review → 主会话修订 → re-review）。默认 review loop 数读取 [`../runtime-contract.json`](../runtime-contract.json)；用户可用 `--loops N` 或 `--review-loops N` 覆盖。

- Round 1：全量查 BLOCKER / MAJOR / MINOR，主会话修订。
- Round 2：重点复核上一轮修复和回归，不重新无差别发散新审美意见。
- 用户指定更多轮时，每轮仍最多两个 reviewer；不得通过增加 agent 数量代替循环。
- 用户在任何轮提出新意见时，把意见作为 `user_delta`，只回退到最早受影响阶段。

## 6. 终止条件

- 所有 BLOCKER 清零。
- 字数仍在锁定验收区间内。
- 修改没有引入新的事实、观点或限定强度变化。
- 本轮没有新的 MAJOR，或剩余问题仅属无法由契约裁决的审美分歧。
- 达到用户指定循环预算后停止；仍有分歧时明确交给用户，不继续自动 spawn。
