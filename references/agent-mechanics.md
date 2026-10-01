# Agent 写作指令与技能架构规范 (Writing-for-Agents Principles)

> 来源沉淀：Matt Pocock's `writing-for-agents`  
> 核心目标：消除 Agent 写作的“过早完工（Premature Completion）”与“上下文漂移”，保障工业级确定性输出。

---

## 一、信息层级与渐进式披露 (Information Hierarchy)

1. **梯队架构**：
   - **Tier 1 (In-file Step)**：主技能文件 `SKILL.md` 中只写必须顺序执行的核心主干步骤。
   - **Tier 2 (In-file Reference)**：同文件中的极简判定规则与硬性约束。
   - **Tier 3 (Disclosed Reference)**：详细对照表、深度模板、专业领域规则推至 `references/`，按需指向。
2. **上下文指针设计 (Context Pointers)**：
   - 前置关键词（Front-load leading words）：指针描述第一句话明确告知触发条件与适用分支。
   - 分支唯一性（One trigger per branch）：避免多组同义词堆砌，每个指针指代一个独立决策路径。

---

## 二、完成标准与硬门禁 (Demanding Completion Criteria)

1. **消灭模糊界限**：
   - 禁用“写得足够详细”、“理解文章精髓”等不可衡量表述。
   - 必须使用**客观可验证判定**：“列出至少 3 个具体物理物象”、“逐行对照白名单清除 0 处翻案腔”、“通过 5 维度 40 分及格线”。
2. **抵抗过早完工引力 (Anti-Premature Completion)**：
   - 当后续步骤暴露给 Agent 时，模型倾向于草草收尾当前步骤。
   - 采用硬门禁阻断：在完成前序步骤的交付物（如人物卡、节拍表）前，严禁直接生成正文。

---

## 三、先导词体系 (Leading Words)

使用经过模型预训练强锚定的核心引导词：
- **`tight`（紧实）**：拒绝任何松散修饰与水词，每个动词直接推动动作。
- **`ground-truth`（现场客观事实）**：每个描写必须能指出材料来源，拒绝无中生有。
- **`in-the-room`（临场置身感）**：将读者置于真实的物理空间，感知温湿度、声响与肢体动作。
- **`red-gate`（红线关卡）**：一旦命中白名单中的翻案腔或假转折，立即报错并强制重写。
- **`prune`（修剪）**：无情剔除所有未带来真实增量行为的无效废话（No-ops）。
