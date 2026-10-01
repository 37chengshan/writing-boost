# 多视角对抗式审查委员会运行规范 (Adversarial Review Council Protocol)

> 本规范定义了 `writing-boost` 在阶段 5（交叉质检与终审）中，如何调度专职审查子代理委员会对稿件进行法医级、对抗式、多维度的质检与裁决。

---

## 1. 审查委员会架构与分工

审查委员会由 **4 个专职质检子代理 + 1 个裁决仲裁总编辑** 组成，形成分立制衡、红黑对抗的质检矩阵：

```
                           ┌────────────────────────┐
                           │      待审查稿件 / 章节   │
                           └───────────┬────────────┘
                                       │
        ┌──────────────────┬───────────┴───────────┬──────────────────┐
        ▼                  ▼                       ▼                  ▼
┌───────────────┐  ┌───────────────┐       ┌───────────────┐  ┌───────────────┐
│devils-advocate│  │logic-inquisitor│      │  slop-hunter  │  │pacing-auditor │
│ 毒舌反驳者     │  │ 逻辑事实质检官 │      │ AI味假转折猎手 │  │ 节拍共情体检官 │
│ (廉价煽情/爹味)│  │ (时空因果/守恒)│      │ (翻案腔/排比)  │  │ (前15%Hook/余韵)│
└───────┬───────┘  └───────┬───────┘       └───────┬───────┘  └───────┬───────┘
        │                  │                       │                  │
        └──────────────────┼───────────────────────┴──────────────────┘
                           ▼
               ┌───────────────────────┐
               │     chief-editor      │
               │   总编辑裁决与仲裁官   │
               │ (加权打分·手术方案·终决)│
               └───────────┬───────────┘
                           ▼
          [ PASS 准印 / REVISE 退修 / REJECT 枪毙 ]
```

### 子代理档案与提示词入口

| 子代理标识 | 角色名称 | 核心质检靶点 | 提示词规范入口 |
| :--- | :--- | :--- | :--- |
| `devils-advocate` | 毒舌反驳者与怀疑论审判官 | 廉价煽情、道德爹味、纸片人脸谱化、廉价和解、读者出戏点 | [`agents/devils-advocate.md`](../agents/devils-advocate.md) |
| `logic-inquisitor` | 逻辑与物理事实质检官 | 物理现实、生理极限、时间线悖论、信息守恒（零虚构）、空间瞬移 | [`agents/logic-inquisitor.md`](../agents/logic-inquisitor.md) |
| `slop-hunter` | AI味与假转折猎手 | “不是……而是……”翻案腔、喉头虚词、机械三元排比、破折号滥用 | [`agents/slop-hunter.md`](../agents/slop-hunter.md) |
| `pacing-auditor` | 节拍与共情体检官 | 前 15% 黄金 Hook、概念奠基（Grounding）、场景电荷反转、结尾物象收束 | [`agents/pacing-auditor.md`](../agents/pacing-auditor.md) |
| `chief-editor` | 主编总评与裁定仲裁官 | 汇总四路报告、裁决审查分歧、评定加权终审分数、下达退修三部曲手术单 | [`agents/chief-editor.md`](../agents/chief-editor.md) |

---

## 2. 调度执行模式 (Execution Modes)

为适应不同的 Agent 运行环境（多代理并发环境 vs 单进程会话环境），委员会支持双模调度：

### 模式 A：并发子代理会审 (Full Parallel Spawn Mode)
- **触发条件**：当前运行时支持子代理调用（如 Claude Code Task/Subagent、OpenCode、Codex CLI、Antigravity `invoke_subagent` 或 Agent MCP）。
- **执行流程**：
  1. 宿主 Agent 读取待审稿件原文及相关事实素材。
  2. 并发向 `devils-advocate`、`logic-inquisitor`、`slop-hunter`、`pacing-auditor` 发送请求，传入稿件与审查规范。
  3. 各子代理独立输出结构化 Findings。
  4. 宿主 Agent 收集四份报告，统一作为上下文传给 `chief-editor`。
  5. `chief-editor` 输出最终的《终审裁决书》及《加权成绩单》。

### 模式 B：单会话分步会诊降级 (Sequential Solo Review Mode)
- **触发条件**：当前运行于嵌套子代理中，或宿主平台不支持子代理派发。
- **执行流程**：
  - 宿主 Agent 在单一上下文中，按照“毒舌反驳 $\rightarrow$ 逻辑核验 $\rightarrow$ 去AI味扫描 $\rightarrow$ 节拍体检 $\rightarrow$ 主编裁决”的固定顺序，轮流切换思维模式（Perspective Switching），完整填报 5 份标准报告。

---

## 3. 终审通关及格线与一票否决权

委员会设立两级硬门禁，严禁妥协与放水：

1. **量化门禁**：
   - 6 项评估指标总分 $\ge 45/60$。
   - 任何单项指标不得低于 7 分。
2. **一票否决红线 (Veto Red-Gates)**：
   - 若 `logic-inquisitor` 判定存在事实虚构或严重时空逻辑悖论 $\rightarrow$ **一票退修**。
   - 若 `slop-hunter` 判定千字包含 $\ge 3$ 处翻案腔或核心段落充斥机械排比 $\rightarrow$ **一票退修**。
   - 若 `devils-advocate` 判定存在消费苦难与虚假道德升华 $\rightarrow$ **一票退修**。
   - 若 `pacing-auditor` 判定开篇 200 字无有效抓手或严重拖沓 $\rightarrow$ **一票退修**。
