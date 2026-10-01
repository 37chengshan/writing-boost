# writing-boost 模块化风格仓库

> 每个 style 实现 [style-contract.md](style-contract.md)。Contract 定义接口；具体数字和审美只能由 style 自己拥有。

## 预装 Style

| ID | 定位 | 入口 |
| :--- | :--- | :--- |
| `zhiyin-2026` | 纪实人物 / 社会特稿 | [zhiyin-2026/style.md](zhiyin-2026/style.md) |
| `investigative-feature` | 调查与证据闭环 | [investigative-feature/style.md](investigative-feature/style.md) |
| `personal-memoir` | 个人非虚构 / 回忆 | [personal-memoir/style.md](personal-memoir/style.md) |
| `tech-insider` | 科技商业深度写作 | [tech-insider/style.md](tech-insider/style.md) |
| `literary-travelogue` | 人文地理 / 文旅 | [literary-travelogue/style.md](literary-travelogue/style.md) |

## 使用

```text
/writing-boost style list
/writing-boost style info zhiyin-2026
/writing-boost write "主题" --style tech-insider
/writing-boost style new my-custom-style
```

## 新 Style 最小实现

新目录必须说明：

1. **Manifest**：ID、名称、版本、适用体裁 / 平台、建议篇幅。
2. **L1 Prose**：用词、句法、对白、标点与真正的 style-specific 禁忌。
3. **L2 Structure**：开头如何建立阅读承诺、中段如何推进、结尾如何收束。
4. **L3 Tension**：适合的问题、冲突轴、题材边界。
5. **L4 Material**：证据、场景、物象和感官细节如何使用。
6. **L5 Stance**：叙述距离、判断尺度、共情方式。
7. **L6 Delivery**：段落、标题、平台转译与交付形式。

### 数字归属

如果一个 style 需要：

- 开头占 15%；
- 3 件核心物象；
- 手机段落 2–4 行；
- 5 组标题；

这些数字就写在**该 style 文件**里。

不要把任何一个 style 的数字反向写回 `style-contract.md`、`SKILL.md` 或其他 style。

## 用户约束优先

Style 的建议篇幅不是最终字数。真正的 `target / min / max / count_mode` 来自《开稿对齐卡》。

用户明确要求与 style 冲突时，按以下优先级：

```text
用户明确要求
> 事实与信息守恒
> 开稿对齐卡
> 当前 style
> 作者风格档案
> 通用 deslop 建议
```
