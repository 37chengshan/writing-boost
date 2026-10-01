# writing-boost 模块化风格仓库 (Pluggable Style Registry)

> 本目录存放 `writing-boost` 架构下的所有模块化风格插件。每个风格均严格遵循 [`style-contract.md`](style-contract.md) 六层 DNA 接口契约。

---

## 1. 预装风格矩阵 (Built-in Style Catalogue)

| 风格 ID | 风格全称 | 核心题材定位 | 情感温度与语调 | 规范文档入口 |
| :--- | :--- | :--- | :--- | :--- |
| `zhiyin-2026` *(Flagship)* | 知音纪实特稿·极致反差与物象锚定 | 时代人物、草根突围、真实社会特稿 | 苍凉温热 · 粗粝克制 · 平视众生 | [`styles/zhiyin-2026/style.md`](zhiyin-2026/style.md) |
| `investigative-feature` | 深度调查特稿·硬核冷峻与证据闭环 | 严肃调查、商业黑幕、复杂公共议题 | 极度冷峻 · 手术刀式精准 · 证据闭环 | [`styles/investigative-feature/style.md`](investigative-feature/style.md) |
| `personal-memoir` | 个人非虚构·克制内省与私人记忆 | 家族回忆录、亲情散文、自我生命史 | 温润沉郁 · 隐忍内省 · 去抒情化 | [`styles/personal-memoir/style.md`](personal-memoir/style.md) |
| `tech-insider` | 科技商业特稿·技术哲思与产业暗流 | 商业深度剖析、硅谷/中国科技叙事 | 极客锐利 · 理性推演 · 反公关通稿 | [`styles/tech-insider/style.md`](tech-insider/style.md) |
| `literary-travelogue` | 人文地理漫游·空间拓扑与历史余温 | 文化地理漫记、深度文旅散文、地方志 | 苍茫博大 · 诗意凝视 · 拒绝打卡攻略 | [`styles/literary-travelogue/style.md`](literary-travelogue/style.md) |

---

## 2. 交互与指令调度

通过 `/writing-boost` 可随时查询、切换或新建风格：

```bash
# 查看所有已安装风格及其核心参数
/writing-boost style list

# 查看指定风格的详细六层 DNA 规范
/writing-boost style info zhiyin-2026

# 使用指定风格启动写稿流水线
/writing-boost write "失业四十岁开房吞药" --style zhiyin-2026
/writing-boost write "大模型算力墙与资本暗战" --style tech-insider

# 基于契约脚手架创建你的新自定义风格
/writing-boost style new my-custom-style
```

---

## 3. 自定义风格开发指南

想要扩展自己的写作风格（例如：金融犯罪特稿、悬疑犯罪纪实、二次元轻小说特稿等），只需在 `styles/` 下新建子目录，并实现 [`style-contract.md`](style-contract.md) 中定义的六层接口：

1. **Manifest**：定义 ID、名称、体裁定位与语调。
2. **L1**：设定句长节奏、动词比重、方言保留度与禁用词表。
3. **L2**：定义开篇 15% Hook、中段 70% 推进节拍与终局收尾规则。
4. **L3**：规划该风格最擅长的核心反差张力轴。
5. **L4**：明确承重物象与物理现场置身感法则。
6. **L5**：确立世界观底层基底与道德反说教防线。
7. **L6**：定义段落排版厚度、标题公式与多端社交转译模板。
