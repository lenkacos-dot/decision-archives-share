---
name: decision-archives
version: 2.0.0
description: >
  🏛️ 决策档案馆 — 记录人生重要决定，定时复盘评估，生成成长叙事与决策者画像。
  纯标准库、零依赖、跨平台，适合任何 AI agent 使用。
triggers:
  - "决策"
  - "档案馆"
  - "复盘"
  - "决策记录"
  - "决策评估"
  - "决策报告"
  - "决策洞察"
  - "decision"
  - "archive"
  - "review decision"
---

# 🏛️ 决策档案馆

> 记录你的决定，定期复盘，看清自己的决策模式，成为更好的决策者。

## 兼容性

- 适用于任何能执行本地脚本的 AI agent。
- 所有数据保存在项目目录内，不依赖云端平台。
- 支持中英文命令 + `--json` 输出模式。

## Agent 调用指南

### 核心原则

- 加 `--json` 标志后，所有命令输出纯 JSON，方便 Agent 解析。
- 不加 `--json` 则输出人类可读的富文本。
- JSON 模式下不需要交互确认。

### 记录决策（JSON 模式，非交互）

```bash
python3 scripts/decision_archives.py add --json \
  --title "跳槽到B公司" \
  --category career \
  --decision "接受了B公司的offer" \
  --rationale "薪资涨30%，团队更小更灵活" \
  --expected "能接触到更多核心业务" \
  --risk high \
  --tags 跳槽,职业发展

# 返回:
# {"status":"success","record":{...},"total":1}
```

### 复盘评估（JSON 模式，非交互）

```bash
python3 scripts/decision_archives.py review <id> --json \
  --outcome "在B公司成长了很多，但加班严重" \
  --rating 4 \
  --lessons "薪资不是唯一因素，工作生活平衡也很重要" \
  --surprises "没想到加班这么严重"

# 返回:
# {"status":"success","record":{...}}
```

### 查询与洞察

```bash
# 待复盘列表
python3 scripts/decision_archives.py pending --json

# 统计概览
python3 scripts/decision_archives.py stats --json

# 决策者画像与成长叙事
python3 scripts/decision_archives.py insights --json

# 评分排名
python3 scripts/decision_archives.py score --json

# 导出
python3 scripts/decision_archives.py export --format csv
python3 scripts/decision_archives.py export --json
```

## 目录结构

```
decision-archives/
├── SKILL.md
├── _meta.json
├── dashboard.html              # 可视化仪表盘
├── scripts/
│   └── decision_archives.py    # 全功能 CLI（中英文命令 + --json）
└── data/
    └── decisions.json          # 决策数据（自动创建）
```

## CLI 参考

```bash
python3 scripts/decision_archives.py add       [--json] [--title <标题>] [--category <类别>] [--decision <选择>] [--rationale <理由>] [--expected <预期>] [--risk <low|medium|high>] [--tags <t1,t2>]
python3 scripts/decision_archives.py list      [--json]
python3 scripts/decision_archives.py pending   [--json]
python3 scripts/decision_archives.py review <id> [--json] [--rating <1-5>] [--outcome <结果>] [--lessons <教训>]
python3 scripts/decision_archives.py insights  [--json]
python3 scripts/decision_archives.py stats     [--json]
python3 scripts/decision_archives.py score     [--json]
python3 scripts/decision_archives.py delete <id> [--json]
python3 scripts/decision_archives.py export [--format csv|json]
python3 scripts/decision_archives.py dashboard
python3 scripts/decision_archives.py -h, --help
```

### 命令别名

| 内部命令 | 中文别名 | 英文别名 |
|----------|----------|----------|
| add | 记录, 添加, 新增 | add, new |
| list | 列表, 清单, 全部 | list, ls, all |
| pending | 待复盘, 待回顾 | pending |
| review | 复盘, 回顾, 评估 | review, evaluate |
| insights | 洞察, 画像, 成长叙事, 决策模式 | insights, profile |
| stats | 统计, 概况 | stats, stat |
| score | 评分, 排名 | score, ranking |
| delete | 删除 | delete, del, rm |
| export | 导出 | export |
| dashboard | 仪表盘, 看板 | dashboard |

### 类别

`career` 💼 职业 | `love` ❤️ 感情 | `finance` 💰 财务 | `lifestyle` 🏠 生活 | `health` 🏥 健康 | `education` 📚 教育 | `other` 📌 其他

### 风险等级

`low` 🟢 低风险 | `medium` 🟡 中等风险 | `high` 🔴 高风险

## JSON 输出规范

### add --json

```json
{"status": "success", "record": {"id": "...", "date_made": "2026-07-14", "category": "career", "title": "...", "decision_made": "...", "risk_level": "high", "status": "pending", ...}, "total": 1}
```

### review --json

```json
{"status": "success", "record": {"id": "...", "status": "reviewed", "review": {"review_date": "...", "outcome": "...", "rating": 4, "lessons": "...", "surprises": "...", "would_change": "..."}}}
```

### pending --json

```json
{"due": [...], "upcoming": [...], "due_count": 2, "upcoming_count": 3}
```

### insights --json

```json
{"empty": false, "total": 10, "reviewed_count": 5, "pending_count": 5, "avg_rating": 3.8, "decision_type": "平衡型", "type_description": "...", "best_decisions": [...], "worst_decisions": [...], "category_accuracy": {...}, "risk_accuracy": {...}, "failure_pattern": {...}, "trend": {"trend": "略有进步", "early_avg": 3.2, "late_avg": 4.0, "diff": 0.8}, "timeline": [...]}
```

### 错误输出

```json
{"status": "error", "error": "缺少 --title。用法: add --title <标题> ..."}
```

## 工作流

1. **记录决策**：用户做出重要决定时，用 `add` 记录详情
2. **定期复盘**：到复盘日期后，用 `review` 评估结果（1-5 星评分）
3. **查看洞察**：积累 3+ 条已复盘后，用 `insights` 查看决策者画像
4. **可视化**：用 `dashboard` 打开 HTML 仪表盘查看图表

## 设计原则

- 评分 1-5 星制，简单直观
- 风险加权绩效分，高风险决策如果做好了，贡献更大
- 不评判决策好坏，只记录和反思
- 所有数据本地存储，隐私安全