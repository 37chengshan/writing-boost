# 模块化写作风格接口契约 (Modular Style Specification Contract)

> **版本**：`2.0.0`
> **核心原则**：契约只定义“风格插件必须说明什么”，不把某一种文风的具体数字硬编码进引擎核心。

## 1. 6-Layer Interface

每个风格插件必须说明：

```text
Manifest  ID / 名称 / 版本 / 体裁 / 适用载体
L1 Prose (L1 表层语言规范)         用词、句法、对话、标点、禁忌
L2 Structure (L2 篇章叙事结构)     开头承诺、推进方式、结尾方式
L3 Tension (L3 选题与反差张力)     选题、冲突、问题意识、题材边界
L4 Material (L4 素材与物象策略)    证据、场景、物象、感官细节如何使用
L5 Stance (L5 认知框架与道德立场)  叙述距离、价值立场、判断尺度
L6 Delivery (L6 排版与衍生包装)    段落、标题、平台转译与包装
```

## 2. Manifest

```yaml
id: "style-id-slug"
name: "风格名称"
version: "1.0.0"
genre: ["适用体裁"]
platforms: ["适用平台"]
default_length:
  target: 3500
  min: 3000
  max: 4000
```

`default_length` 只是用户没有指定字数时的建议。**用户开稿对齐卡中的字数锁永远优先。**

## 3. L1 Prose

风格文件应描述：

- 句长与段落节奏的**倾向**，不要求所有文本满足统一数字。
- 常用 / 少用词汇与句式。
- 对话、心理、叙述者声音。
- 标点和排版偏好。
- 本风格真正需要禁止或限制的模式，以及允许的例外。

## 4. L2 Structure

描述该风格如何：

- 建立开头阅读承诺；
- 展开信息、冲突或论证；
- 管理场景与转折；
- 收束结尾。

比例、Hook 窗口、场景数量等如有需要，由**具体 style** 自己定义。核心引擎不预设 15/70/15。

## 5. L3 Tension

定义：

- 适合回答哪类核心问题；
- 常用冲突轴或问题意识；
- 不适合的题材与伦理边界；
- 目标读者最关心的风险、欲望或困惑。

## 6. L4 Material

定义：

- 对来源与证据的要求；
- 场景、人物动作、物象与感官细节的偏好；
- 是否需要最低物象数量，如需要由该 style 自己给数值；
- 创作类任务的虚构 / 合成边界。**非虚构 style 只能在 `nonfiction-fidelity` 基础上收紧，不得放宽 `source_policy / reconstruction_policy / Claim Strength`。**

### Nonfiction Boundary

Style 是审美与组织层，不是事实豁免层。对纪实、调查、回忆录等事实性文本：

- style 可以要求更多来源、更少重构、更严格的原话保真；
- style 不得允许核心协议禁止的脑补；
- style 不得把 `ATTRIBUTED / INFERRED` 主张提升为无归属的确定事实；
- style 不得用“临场感”“电影感”“文学性”作为新增现场事实的理由。

## 7. L5 Stance

定义叙述者距离、判断尺度、共情方式和价值立场。不得把“零判断”“必须冷峻”等单一审美提升为所有 style 的全局规则。

## 8. L6 Delivery

定义：

- 段落与版式偏好；
- 标题策略；
- 平台特定转译；
- 是否需要摘要、导语、卡片、社交短版。

## 9. 优先级

当规则冲突时：

```text
用户当前明确要求
> 事实与信息守恒
> 开稿对齐卡
> 当前 style
> 作者风格档案
> 通用 deslop 建议
```

## 10. 调度

- `/writing-boost style list`
- `/writing-boost style info [style-id]`
- `/writing-boost write [主题] --style [style-id]`
- `/writing-boost style new [new-style-id]`
