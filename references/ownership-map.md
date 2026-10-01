# Rule Ownership Map

> 每条行为规则只有一个 authoritative owner。其他文件只做指针或摘要；修改行为时先改 owner，再由测试发现过期摘要。

| 规则 | 唯一 Owner | 其他文件允许做什么 |
| :--- | :--- | :--- |
| 版本、loop 默认值、reviewer 上限、长度容差、长篇阈值 | `runtime-contract.json` | 展示当前值，但测试必须校验一致 |
| 开稿字段、字数锁、count mode / scope | `references/alignment-and-length.md` | SKILL 只保留入口摘要 |
| Automatic / Feedback loop 语义 | `references/loop-policy.md` | templates 只记录状态 |
| 非虚构 SOURCE / Claim Strength / Quote / POV / 物象规则 | `references/nonfiction-fidelity.md` | ledger 只提供数据结构 |
| 六阶段输入输出与 gate | `references/story-pipeline.md` | SKILL 只列阶段名 |
| reviewer 拓扑与模型授权 | `references/review-council.md` | reviewer prompt 只描述各自职责 |
| Style 接口 | `styles/style-contract.md` | 每个 style 只实现接口 |
| 知音具体数字和审美 | `styles/zhiyin-2026/style.md` | 核心 contract 不复制 |
| 中文 deslop 语义规则 | `references/deslop-whitelist-zh.md` | reviewer 按需引用 |
| 中文固定高风险短语精确列表 | `references/cliche-patterns-zh.json` | markdown 只解释上下文 |
| Packaging POV / 平台转译 | `references/social-packaging.md` | style 可追加平台偏好 |

## 修改纪律

1. 找到 owner。
2. 只在 owner 修改行为。
3. 若摘要中必须出现同一数值，用测试验证它仍和 owner 一致。
4. 模板不创造新规则，只承载 owner 定义的数据。
5. deprecated 文件不得重新成为 owner。
