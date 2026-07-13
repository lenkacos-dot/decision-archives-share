# 决策档案馆 — Copilot Instructions

## 项目类型
纯 Python CLI 工具，标准库零依赖，跨平台。

## 核心命令
- `python3 scripts/decision_archives.py add` 记录决策
- `python3 scripts/decision_archives.py review <id>` 复盘
- `python3 scripts/decision_archives.py insights` 成长叙事
- `python3 scripts/decision_archives.py export csv` CSV 导出

## 数据
存储于 `data/decisions.json`，结构见 `CLAUDE.md`。

## 原则
- 纯标准库，不加外部依赖
- 跨平台兼容（macOS/Linux/Windows）
- 交互式 + CLI 参数双模式
- 最小实现，消除重复代码