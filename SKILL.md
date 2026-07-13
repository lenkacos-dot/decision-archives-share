---
name: decision-archives
version: "1.0.0"
description: "人生决策档案馆 — 记录所有重要决定（换工作、分手、投资、买房、跳槽等），评估结果，半年后复盘：你做对了什么？总在哪种情况下失误？生成成长叙事。当用户需要记录决策、复盘决策、分析决策模式、成长回忆录时激活。"
triggers:
  - "记下这个决定"
  - "记录一个决策"
  - "决策档案馆"
  - "复盘"
  - "回顾决策"
  - "决策分析"
  - "成长叙事"
  - "我做了什么决定"
  - "决策模式"
  - "人生决定"
  - "判断失误"
  - "decision archive"
  - "review decision"
  - "decision insights"
tags: [life-management, journaling, reflection, decision-making, personal-growth, growth-narrative]
---

# 🏛️ 决策档案馆 — Decision Archives v1.0.0

> **记录你人生所有重要决定，并评估结果。**  
> 半年后，系统告诉你：你做对了什么？你总在哪种情况下判断失误？  
> 这是你的成长叙事引擎。

---

## 一句话

你做一个决定 → 记下来 → 半年后回来评估 → 系统给你生成**决策者画像**。

---

## 触发条件

| 你想做什么 | 说这句就行 | 背后执行 |
|---|---|---|
| 记录新决策 | "记下这个决定" / "记录决策" / "存档一个决定" | `scripts/decision_archives.py add` |
| 查看所有决策 | "我的决策" / "决策列表" / "所有决定" | `scripts/decision_archives.py list` |
| 评估一个决策 | "复盘xxx" / "回顾决策" / "评估一下" | `scripts/decision_archives.py review <id或title>` |
| 待评估队列 | "有哪些需要复盘的" / "待回顾" | `scripts/decision_archives.py pending` |
| 成长叙事 | "我的决策画像" / "我是什么决策者" / "决策模式分析" | `scripts/decision_archives.py insights` |
| 统计概览 | "决策统计" / "决策数据" / "档案馆概况" | `scripts/decision_archives.py stats` |
| 评分系统 | "决策评分" / "最佳决策" / "最差决定" | `scripts/decision_archives.py score` |

---

## 工作流

```
你用决策.jpg 了重要决定
  └─ agent 调用 scripts/decision_archives.py add
       ├─ 填类别（职业/感情/财务/生活/健康/教育/其他）
       ├─ 填标题和决策内容
       ├─ 填备选方案（有哪些选项你放弃了）
       ├─ 填选择理由 + 预期结果
       ├─ 填风险等级（低/中/高）
       └─ ✅ 保存，告诉用户6个月后回来看

6 个月后你问"有什么要复盘的"
  └─ agent 调用 scripts/decision_archives.py pending
       ├─ 显示所有到期但未评估的决策
       └─ "xx 决定到期了，要来评估结果吗？"

你评估一个决策
  └─ agent 调用 scripts/decision_archives.py review <id>
       ├─ 显示当初的记录（当时你选了啥、为啥、期望啥）
       ├─ 填实际结果（1-5星）
       ├─ 填学到了什么
       └─ ✅ 存档，进入复盘完成

你要看成长叙事
  └─ agent 调用 scripts/decision_archives.py insights
       ├─ 你的决策者画像（谨慎型/冒险型/直觉型/分析型）
       ├─ 最佳决策 TOP 3（评分最高）
       ├─ 最差决策 TOP 3（评分最低）
       ├─ 失误模式分析（你在哪种情境下总翻车）
       ├─ 趋势（你的决策力在进步吗）
       └─ 成长故事线（按时间轴展示你做过的所有决定）
```

---

## 数据模型

每个决策包含以下字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | UUID | 唯一标识 |
| `date_made` | ISO日期 | 做决定的时间 |
| `category` | 枚举 | career / love / finance / lifestyle / health / education / other |
| `title` | str | 短标题（eg. "从A公司跳槽到B公司"） |
| `decision_made` | str | 你做了什么选择 |
| `alternatives` | list[str] | 你放弃的其他选项 |
| `rationale` | str | 选择理由 |
| `expected_outcome` | str | 你当初预期会怎样 |
| `risk_level` | enum | low / medium / high |
| `review_date` | ISO | 预计复盘日期（默认+6个月） |
| `status` | enum | pending / reviewed / archived |
| `review` | object or null | 复盘数据↓ |
| `review.review_date` | ISO | 实际复盘日期 |
| `review.outcome` | str | 实际结果描述 |
| `review.rating` | int | 1-5星（5=完全对, 1=完全错） |
| `review.lessons` | str | 你学到了什么 |
| `review.surprises` | str | 意料之外的事 |
| `review.would_change` | str | 如果重来会怎么选 |
| `tags` | list[str] | 自定义标签 |

---

## 核心功能

### 1️⃣ 记录决策 `add`
交互式录入，每一步都让用户填空。省去记参数的学习成本。

### 2️⃣ 定期复盘 `pending` + `review`
- 默认 6 个月后提醒复盘
- 复盘时展示"当时你是怎么想的"，防止**记忆偏差**
- 评分 1-5，记录教训

### 3️⃣ 决策者画像 `insights`
基于所有已复盘决策，分析你的决策风格：

- **类型判断**：你的决策是偏保守（低风险为主）还是偏激进？
- **准确率**：不同类别的决策正确率（职业决定准不准？感情决定呢？）
- **失误模式**：你在什么情境下总翻车？（eg. "每次在压力大时做的决定，3次里错2次"）
- **进步曲线**：越新的决策评分越高吗？你在成长吗？
- **故事线**：按时间轴串联你的人生关键节点

### 4️⃣ 评分系统 `score`
每个决策都有"当初判断准确度"评分。可以直接问"我最好的决定是什么"。

---

## 使用示例

```bash
# 记录一个决定
python3 ~/.hermes/skills/decision-archives/scripts/decision_archives.py add
# → 交互式问答，一步步填

# 查看待复盘
python3 ~/.hermes/skills/decision-archives/scripts/decision_archives.py pending
# → 显示所有到期未评估的决策

# 复盘一个决策
python3 ~/.hermes/skills/decision-archives/scripts/decision_archives.py review abc123
# → 展示"当时你怎么想的"，然后互动填结果

# 成长叙事
python3 ~/.hermes/skills/decision-archives/scripts/decision_archives.py insights
# → 生成完整的决策者画像和成长故事线

# 统计概览
python3 ~/.hermes/skills/decision-archives/scripts/decision_archives.py stats

# 决策评分排名
python3 ~/.hermes/skills/decision-archives/scripts/decision_archives.py score
```

---

## 配套文件

```
decision-archives/
├── SKILL.md              ← 本文件
├── _meta.json            ← 元数据
├── scripts/
│   └── decision_archives.py  ← 核心脚本
└── data/
    └── decisions.json    ← 数据持久化（自动创建）
```

---

## 为什么你要用这个 skill

- 🔍 **对抗记忆偏差**：人过半年会美化/扭曲当初的选择，你记下的是当时真实的想法
- 📈 **可量化的成长**：不是"我感觉我进步了"，而是"我今年决策评分比去年高0.7分"
- 🧠 **发现盲区**：你可能不知道自己在"小金额低频决策"上准确率只有 20%
- 📖 **人生故事本**：几年后翻出来看，是一条完整的时间线："2026年我做了12个重要决定"