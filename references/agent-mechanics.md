# Agent 写作与 Skill 架构原则

> 本文件只描述 writing-boost 自己的提示词工程原则。具体默认数字统一由 [../runtime-contract.json](../runtime-contract.json) 管理。

## 1. Information hierarchy

`SKILL.md` 只保留所有分支都要知道的主干和硬不变量。

- **In-file step**：必须顺序执行的步骤。
- **In-file reference**：所有分支都会使用的极简规则。
- **Disclosed reference**：只在某一分支触发的详细协议、模板和 style。

不要因为一条规则重要就复制到五个文件。重要规则应该有**单一 owner + 强指针**。

## 2. Completion criteria

完成标准必须能被观察或验证。例如：

- 对齐卡的必需字段已经锁定；
- 字数脚本返回 PASS；
- 所有相对时间都有绝对锚点和计算结果；
- 非虚构引号都能找到 Quote ID；
- review 的 BLOCKER / MAJOR 已清零。

“写得更深”“更有感染力”“像人一点”不能单独作为完成标准。

## 3. Positive target over negation

优先描述要达到的文本状态：

- “结尾停在来源支持的动作 / 物象 / 现实后果上”
  优于
  “不要升华”。
- “只写账本里已知的实体属性”
  优于
  “不要脑补”。

硬安全线和事实边界可以使用禁止语句，但同时给出正向替代行为。

## 4. Deterministic before semantic

能由程序稳定完成的工作不消耗 reviewer：

- 字数 → `scripts/text_metrics.py`
- 高风险固定短语 → `scripts/lint_cliches.py`
- skill 架构不变量 → `scripts/check_skill_contract.py`

模型负责需要语境的部分：事实解释、结构、人物、节拍、修辞功能和冲突意见。

## 5. Context budget

每次只加载当前阶段的 reference。

例如写 Draft 时无需同时加载完整 review-council；Review 时也无需重新载入全部风格蒸馏语料，只加载：

1. 对齐卡；
2. 当前 style；
3. 当前稿件；
4. 对应 reviewer prompt；
5. 必要事实账本。

## 6. Loop discipline

循环不是“重新生成”。

每轮只允许修改当前 `issue_set`，并维护 `frozen_constraints` 与 `frozen_content`。详见 [loop-policy.md](loop-policy.md)。

## 7. Reviewer isolation

子代理只存在于 review 阶段，并且每轮最多两个。

- Integrity：事实 / 约束 / 连续性。
- Editorial：读者 / 结构 / 风格。

两个 reviewer 不互相读取对方的中间推理；主会话收集最终 findings 后合并。这样比五个角色反复读全文更节省上下文，也降低同一问题重复报告。

## 8. No hidden reasoning requirement

面对用户的“思想流程对齐”，输出的是**可核对的工作契约和决策结果**，不是内部推理链。用户应当能看到目标、假设、约束、预算和修改理由，但不需要看到模型私有思维过程。
