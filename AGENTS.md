# 决策档案馆 — AGENTS.md

## 这是什么
一个纯 CLI 工具，帮你记录人生所有重要决定并评估结果。
- 换工作 ✅ 分手 ✅ 买东西 ✅ 投资 ✅ 半年后复盘
- 你做对了什么？你总在哪种情况下判断失误？

## 快速上手
```bash
python3 scripts/decision_archives.py add          # 交互式记录
python3 scripts/decision_archives.py list         # 看所有决策
python3 scripts/decision_archives.py review <id>  # 复盘
python3 scripts/decision_archives.py insights     # 看成长故事
```

## 文件结构
```
decision-archives/
├── scripts/
│   └── decision_archives.py   ← 主程序（纯 stdlib）
├── data/
│   └── decisions.json         ← 数据文件
├── dashboard.html             ← HTML 可视化仪表盘
├── CLAUDE.md                  ← Claude Code 指令
├── .cursorrules               ← Cursor 指令
├── .github/copilot-instructions.md  ← Copilot 指令
├── README.md                  ← GitHub 首页
└── SKILL.md                   ← Hermes Agent 指令
```

## 关键设计
- **纯 Python 标准库** — 不需要 pip install，开箱即用
- **跨平台** — macOS/Linux/Windows 三端一致
- **双模式** — 交互式（手把手）和 CLI 参数（脚本/自动化）
- **数据安全** — 删除需 YES 确认，数据单文件存 JSON

## 所有命令
| 命令 | 用途 |
|------|------|
| `add` | 记录新决策 |
| `list` | 列出所有 |
| `pending` | 待复盘列表 |
| `review <id>` | 复盘评估 |
| `insights` | 成长叙事画像 |
| `stats` | 统计概览 |
| `score` | 评分排名 |
| `delete <id>` | 删除决策 |
| `export [csv]` | 导出 JSON/CSV |
| `dashboard` | 打开仪表盘 |