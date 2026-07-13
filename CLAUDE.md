# 决策档案馆 — CLAUDE.md

## 项目概述
CLI 工具，记录人生重要决定，评估结果，生成成长叙事。纯 Python 标准库，零外部依赖。

## 命令速查

```bash
# 记录
python3 scripts/decision_archives.py add                          # 交互式
python3 scripts/decision_archives.py add -c career -t "标题" ...  # CLI 模式

# 查询
python3 scripts/decision_archives.py list        # 列表
python3 scripts/decision_archives.py pending     # 待复盘

# 复盘
python3 scripts/decision_archives.py review <id_or_title>

# 分析
python3 scripts/decision_archives.py insights    # 成长叙事
python3 scripts/decision_archives.py stats       # 统计
python3 scripts/decision_archives.py score       # 评分排名

# 导出
python3 scripts/decision_archives.py export      # JSON
python3 scripts/decision_archives.py export csv  # CSV

# 仪表盘
python3 scripts/decision_archives.py dashboard   # 打开 HTML

# 管理
python3 scripts/decision_archives.py delete <id>
```

## 架构
- `scripts/decision_archives.py` — 主程序（~800 行，纯 stdlib）
- `data/decisions.json` — 数据文件
- `dashboard.html` — Chart.js 可视化仪表盘

## 数据模型
```json
{
  "id": "uuid",
  "date_made": "2026-07-13",
  "category": "career|love|finance|lifestyle|health|education|other",
  "title": "从A公司跳槽到B公司",
  "decision_made": "接受了B公司offer",
  "alternatives": ["留在A公司", "等更好的机会"],
  "rationale": "A公司发展遇到瓶颈",
  "expected_outcome": "职业生涯更大发展空间",
  "risk_level": "low|medium|high",
  "review_date": "2027-01-13",
  "status": "pending|reviewed",
  "review": null | {
    "review_date": "2027-01-13",
    "outcome": "发展不错，薪资涨了",
    "rating": 3,
    "lessons": "跳槽是正确的选择",
    "surprises": "工作压力比预期大",
    "would_change": "和当初一样"
  },
  "tags": ["跳槽", "薪资"],
  "matrix": null | {
    "dimensions": ["收益","风险","可行性","直觉","时间成本"],
    "options": [
      {"name": "接受了B公司offer", "scores": {"收益": 5, "风险": 2, ...}},
      {"name": "留在A公司", "scores": {"收益": 2, "风险": 4, ...}}
    ]
  },
  "created_at": "2026-07-13T10:00:00"
}
```

## 设计原则（Ponytail）
1. **纯标准库** — 零外部依赖，`pip install` 不需要
2. **跨平台** — macOS / Linux / Windows
3. **增量扫描** — 无状态恢复
4. **最小实现** — 能跑的代码不写两遍

## 数据安全
- `data/decisions.json` 是唯一持久化存储
- 操作前建议备份：`cp data/decisions.json data/backup.json`
