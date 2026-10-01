<div align="center">

# ⚡ writing-boost

### Alignment-first · Locked Length · Budgeted Loops · Pluggable Styles · Max-two Cross Review

[![writing-boost](https://img.shields.io/badge/writing--boost-3.3.0-blue.svg?style=for-the-badge)](SKILL.md)
[![Runtime Contract](https://img.shields.io/badge/runtime-contract--driven-0ea5e9?style=for-the-badge)](runtime-contract.json)
[![Review](https://img.shields.io/badge/review-max_2_reviewers-a855f7?style=for-the-badge)](references/review-council.md)
[![Style Engine](https://img.shields.io/badge/styles-pluggable-10b981?style=for-the-badge)](styles/style-contract.md)
[![Evolution Governance](https://img.shields.io/badge/evolution-router_governed-f59e0b?style=for-the-badge)](#外部演化治理体系-external-evolution-governance)

<p align="center">
  <img src="assets/readme/hero-banner.svg" alt="Writing Boost v3.3" width="100%" />
</p>

**把写作做成一个可以对齐、计量、循环、审查和回归验证的工程流程。**

</div>

---

`writing-boost` 把长文写作拆成一套有明确输入、事实边界、字数口径、循环预算、风格契约与终审门禁的工程流程。核心原则：

> **先对齐、再写；先锁尺子、再锁字数；关键阶段允许闭环，但不无限反刍；子代理只在终审出现，每轮最多两个。**

运行时默认数值统一由 [runtime-contract.json](runtime-contract.json) 集中管理，避免 README、SKILL、测试和 reviewer 各自维护一套数字。

---

## 架构与管线

```text
User brief
   │
   ▼
Alignment Card
目标 / 读者 / POV / 事实边界 / style / 字数口径 / loop budget
   │
   ▼
Evidence → Shape → Draft → Self-review
             ↻        ↻
       budgeted loops
   │
   ▼
Final Review
├─ Integrity Reviewer (事实 / 时间算术 / 实体 / 引语 / POV)
└─ Editorial Reviewer (读者体验 / 节奏 / style / 去AI味)
   │
   ▼
Main Session Synthesizer (唯一终审裁决者)
   │
   ▼
Delivery / Packaging
```

<p align="center">
  <img src="assets/readme/pipeline-architecture.svg" alt="Writing Boost v3.3 Pipeline" width="100%" />
</p>

### 几个硬不变量

- **命令隔离**：本技能命令统一为 `writing-boost`（`/writing-boost`），避免与系统级通用能力命名冲突。
- **子代理边界**：子代理只在终审阶段使用；前期探索、塑形、起草均在主会话进行。
- **终审限额**：单轮最多两个 reviewer，绝不调度臃肿多子代理。
- **最终裁决权**：主会话永远负责最终裁决和成稿改写。
- **预算闭环**：Shape / Draft / Review 默认使用有预算的 loop，用户可随时指定覆盖。
- **信息守恒**：非虚构所有看似“现场”的细节都受信息守恒约束，禁止脑补虚构。
- **统一量尺**：字数必须同时锁定 `target / band / count_mode`，全流程一把尺子。
- **风格解耦**：风格特有数字归属具体 style，不反向污染核心契约。

---

## 开稿对齐

在正文动笔前，必须明确锁定：

- **目标与读者**：写作目的、目标读者画像、体裁与发布平台、核心命题
- **事实边界**：来源素材范围、不可逾越的边界
- **正文视角**：POV（第一人称 / 第三人称等）
- **原话处理**：`VERBATIM`（逐字保真）/ `LIGHT-CLEAN`（轻度理顺）/ `PARAPHRASE`（转述）
- **当前风格**：指定启用的 style 模块
- **字数契约**：`target / min / max / count_mode`
- **循环预算**：各阶段迭代预算
- **交付清单**：正文、标题组合、摘要、物象回收表、必须保留与避开项

用户已经说明的内容直接复用。用户说“你定 / 直接写”时，系统补充合理默认值并主动回显，不反复无效盘问。

### 计数模式 (Count Mode)

默认口径：

- **中文**：`zh_units`，每个汉字计 1，连续英文/数字 token 计 1，标点与空白不计；
- **英文**：`words`，按空格分词统计；
- **平台模式**：用户明确以公众号或平台后台字数为准时采用 `platform`。

全流程必须使用同一种 `count_mode`，避免结构规划与终审验收时产生口径偏差。

---

## 预算闭环 (Budgeted Loops)

完整协议详见 [references/loop-policy.md](references/loop-policy.md)。

`loops=N` 表示**初始产物产出后最多允许 N 轮定向修订闭环**：

```text
产物生成 → 门禁判定 → 缺陷清单 → 局部针对性修订 → 回归检查 → PASS / 进入下一阶段
```

运行时默认预算（来自 `runtime-contract.json`）：
- **Shape**：2 轮
- **Draft**：2 轮
- **Review**：2 轮
- **Packaging**：0 轮（默认一次成型）

支持命令行灵活覆盖：

```bash
--loops N          # 覆盖全局关键阶段
--shape-loops N    # 仅覆盖塑形阶段
--draft-loops N    # 仅覆盖草稿阶段
--review-loops N   # 仅覆盖终审阶段
--package-loops N  # 覆盖包装阶段
```

若用户在成稿后提出修改意见，触发 **Feedback Loop**：将意见解析为 `user_delta`，仅局部回退至最早受影响阶段，并冻结未受影响的正文资产，拒绝无休止的全篇推倒重来。

---

## 非虚构事实账本与沙盒防线

参考 [references/nonfiction-fidelity.md](references/nonfiction-fidelity.md) 与 [templates/nonfiction-ledger.md](templates/nonfiction-ledger.md)。

显式管理并锁定：
- **绝对时间轴**：锁定具体年份、月份与事件顺序
- **Derived Facts 算术复核**：“X 年前 / 后”等推导数字必须符合数学严密性（如 `2026 - 2017 = 9`）
- **实体属性锁**：区分已知属性与 UNKNOWN 属性，禁止擅自脑补车型品牌、族群标签等
- **Quote ID**：逐条登记核心人物引语及其原话保真级别
- **物象回收账本**：核心物象的登场、物理动作与文末回收
- **POV 锁**：正文视角与标题视角强一致，严防为了吸引眼球在标题偷换第一人称

### 沙盒测试六类缺陷对应的防线

| 缺陷类别 | 对应机制与防线 |
| :--- | :--- |
| **网文烂梗、爹味说教** | `references/cliche-blacklist-zh.md` + Editorial Reviewer 拦截 |
| **年份算术硬伤** | `templates/nonfiction-ledger.md` + Integrity Reviewer 强制复算 |
| **细节脑补、标签膨胀** | 实体属性锁 + Information Conservation 信息守恒硬约束 |
| **后半程物象失踪** | `templates/chapter-beat-sheet.md` 物象账本 + Editorial 追踪 |
| **标题 / 正文人称割裂** | Alignment POV lock + `references/social-packaging.md` 视角强绑定 |
| **方言 / 原话被雅化** | Quote ID 追踪 + `VERBATIM` 逐字保真模式 |

---

## 终审架构：最多两个 Reviewer

终审协议见 [references/review-council.md](references/review-council.md)。

唯一可调度的双审查席位：
- **[Integrity Reviewer](agents/integrity-reviewer.md)**：专职事实、来源、时间算术、实体属性、原话保真、逻辑连续性、POV 视角与字数契约。
- **[Editorial Reviewer](agents/editorial-reviewer.md)**：专职读者体验、结构节拍、风格契约、去 AI 痕迹、网文烂梗、说教感、对白颗粒度与物象漂移。

### 调度规则与门禁

- **低风险短文本**：0 个 reviewer（主会话自审交付）
- **单一维度风险**：1 个针对性 reviewer
- **重要长稿**：1–2 个 reviewer
- **长篇纪实 / 调查 / 人物报道**（`zh_units >= 3000` 或 `words >= 1800`）：**固定双审**
- **硬性上限**：单轮 reviewer 数量严控不超过 2 个
- **主会话终局裁决**：Reviewer 只出具结构化问题清单与缺陷等级（BLOCKER / MAJOR / MINOR），改稿与最终交付始终由主会话执行

> 若宿主环境支持显式分配不同模型，首次需要异构双审时，系统会主动询问用户允许调用的模型范围与预算，绝不擅自消耗外部高资费配额。

---

## 外部演化治理体系 (External Evolution Governance)

为防止技能在日常写作使用中产生未经检验的自反思漂移或提示词退化，`writing-boost` 严格遵循**工程执行与演化治理分离**的架构原则：

```text
正常写作任务                                用户明确提出 Skill 优化/评测需求
    │                                                   │
    ▼                                                   ▼
writing-boost (无自我修改权)                  skill-evolution-router (唯一演化入口)
    │                                                   │
    ├─ Alignment Card                                   ├─ 1. 建立最小可复现失败证据 (Failing Case)
    ├─ Fact Ledger                                      ├─ 2. 单一选择后端引擎 (Select Exactly ONE Backend)
    ├─ Budgeted Loops (Shape/Draft)                     │     ├─ SkillHone: 单点缺陷/脚本破坏/API漂移修复
    └─ Max-2 Review (Integrity + Editorial)             │     ├─ skill-evolver: 冻结基准测试/多轮演进搜索 (L1 Gate)
                                                        │     └─ skill-evolution: 跨会话用户纠偏挖掘
                                                        ├─ 3. 确定性门禁验证 (Contract + Unit Tests)
                                                        ├─ 4. Proposal-Only: 呈现 Diff 与验证报告
                                                        └─ 5. 人工确认: 必须获得用户显式授权后才可落地
```

### 1. 演化职责外部解耦
- `writing-boost` 专注于写作交付，**本身不具备自我修改或改写自身代码的权限**。
- 不会因单次成稿受到的偶然负反馈而随意污染全局规则；写作中的反馈只沉淀为候选失败样本（Candidate Samples）。

### 2. 单一入口：`skill-evolution-router`
- 当用户要求“优化 writing-boost / 修复 writing-boost / 运行 benchmark”时，由专门的演化路由网关统一处理。
- 底层演化引擎解耦为三个专属 backend，并从运行时技能池收敛隐藏（`runtime_exposed: false`），由 router 视任务特征**单一选取**，避免多引擎争抢或级联失控：
  - **SkillHone**（单点精准修复）：针对缺失文件、破坏的脚本、失效引用、API 漂移或可重现断言失败进行闭环修补；
  - **skill-evolver**（基准搜索与演化）：基于稳定评测集与 FishSerrie L1 Gate，执行多轮候选演进搜索与保留/舍弃判定；
  - **skill-evolution**（会话反馈采矿）：从跨会话的用户纠偏、负反馈与写作偏好中提炼演化规则提案。

### 3. Proposal-Only 变更门禁与人机控制权
- 所有演化流程默认严格采用**提案模式（Proposal-Only）**：
  1. **证据优先**：必须先建立可重现的最小失败用例（Minimal Failing Case）或明确的评测指标；
  2. **原子突变**：针对问题提出最小 scope 的原子改动；
  3. **确定性门禁**：必须全量通过 L1 Gate、静态契约检查与单元测试套件；
  4. **提交审查**：生成完整的变更 diff 与验证证据报告供用户审查。
- **绝对操作红线**：修改规范（canonical）技能、执行 auto-apply、提交 git commit、合并 merge 或推送到远程仓库，**均必须获得用户明确授权**，严禁无人值守静默改写或越权提交。

### 4. 评测独立性与模型异构隔离
- 语义与风格评测不得由生成模型自行打分验收；必须依赖冻结验证集（Holdout Sets）或独立评测席。
- 如需调用不同模型家族进行异构评审，必须先征求用户允许的模型范围与成本预算，严禁静默调用高资费外部模型。

---

## 风格引擎 (Style Engine)

核心接口契约详见 [styles/style-contract.md](styles/style-contract.md)。

预装风格模块：
- `zhiyin-2026`：当代成熟纪实特稿风格（短促动词、实物锚定、零网文烂梗、方言与生活颗粒）
- `investigative-feature`：深度调查特稿风格
- `personal-memoir`：个人非虚构回忆录风格
- `tech-insider`：科技与商业深度报道风格
- `literary-travelogue`：文学性文旅散文风格

> 15/70/15 结构配比、三件核心物象、手机屏 2–4 行短段落等属于具体 style 的内置实现，绝不作为全局强制规则。

---

## 去 AI 味防线 (Deslop)

- [references/deslop-whitelist-zh.md](references/deslop-whitelist-zh.md)
- [references/cliche-blacklist-zh.md](references/cliche-blacklist-zh.md)
- [references/deslop-prose-en.md](references/deslop-prose-en.md)

规则优先级梯次：

```text
用户显式要求
  > 事实真实与信息守恒
    > 开稿对齐卡 (Alignment Card)
      > 当前风格契约 (Style Contract)
        > 作者个性化档案
          > 通用 Deslop 建议
```

---

## 确定性工具链与本地验证

包含在 [scripts/README.md](scripts/README.md) 中：

```bash
# 1. 静态契约自检 (验证架构不变式、路径规范与链接完整性)
python3 scripts/check_skill_contract.py

# 2. 确定性文本计量 (字数、标点比例、段落长度)
python3 scripts/text_metrics.py draft.md --mode zh_units --target 3000

# 3. 陈词滥调与 AI 痕迹严格扫描
python3 scripts/lint_cliches.py draft.md --strict

# 4. 运行自包含单元契约测试套件
python3 -m unittest discover -s tests -p 'test_*.py'
```

所有测试与脚本均以 skill 自身目录为根，不依赖外部环境的绝对路径，确保在任何宿主环境中均能直接验证。
