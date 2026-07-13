#!/usr/bin/env python3
"""
🏛️ 决策档案馆 — Decision Archives v1.0.0

记录你人生所有重要决定，评估结果，生成成长叙事与决策者画像。

用法:
    python3 decision_archives.py add          # 记录新决策
    python3 decision_archives.py list         # 列出所有决策
    python3 decision_archives.py review <id>  # 复盘评估
    python3 decision_archives.py pending      # 待复盘列表
    python3 decision_archives.py insights     # 成长叙事
    python3 decision_archives.py stats        # 统计概览
    python3 decision_archives.py score        # 评分排名
    python3 decision_archives.py delete <id>  # 删除决策
    python3 decision_archives.py export       # 导出全部数据
"""

import json
import os
import sys
import uuid
from datetime import datetime, date, timedelta
from textwrap import wrap

# ── 路径 ──────────────────────────────────────────────
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(SKILL_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "decisions.json")

os.makedirs(DATA_DIR, exist_ok=True)

# ── 类别 ──────────────────────────────────────────────
CATEGORIES = {
    "career":     "💼 职业",
    "love":       "❤️  感情",
    "finance":    "💰 财务",
    "lifestyle":  "🏠 生活",
    "health":     "🏥 健康",
    "education":  "📚 教育",
    "other":      "📌 其他",
}

RISK_LEVELS = {"low": "🟢 低风险", "medium": "🟡 中等风险", "high": "🔴 高风险"}

# ── 数据持久化 ────────────────────────────────────────

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"decisions": [], "version": "1.0.0"}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def find_decision(data, identifier):
    """按 id 或标题前缀查找决策"""
    for d in data["decisions"]:
        if d["id"] == identifier:
            return d
    # 按标题模糊匹配
    matches = [d for d in data["decisions"] if identifier.lower() in d["title"].lower()]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        print(f"⚠️ 找到 {len(matches)} 个匹配，请用 ID 精确指定：")
        for m in matches:
            print(f"   {m['id'][:8]} — {m['title']}")
        return None
    return None


# ── 交互式输入 ────────────────────────────────────────

def ask(prompt, default=None, required=False, multiline=False):
    """交互式提问，支持默认值和多行输入。"""
    if default:
        prompt = f"{prompt} [{default}]"
    prompt = f"> {prompt}: "
    if multiline:
        print(prompt)
        print("  (输入 END 结束)")
        lines = []
        while True:
            line = input("  ")
            if line.strip().upper() == "END":
                break
            lines.append(line)
        value = "\n".join(lines).strip()
    else:
        value = input(prompt).strip()

    if not value and default:
        return default
    if not value and required:
        print("  ⚠️ 此项必填，请重新输入。")
        return ask(prompt, default, required, multiline)
    return value


def pick_option(prompt, options):
    """从选项列表中选一个。"""
    print(f"\n{prompt}")
    keys = list(options.keys())
    for i, k in enumerate(keys, 1):
        print(f"  {i}. {options[k]}")
    while True:
        choice = input("  请输入编号 (1-{})：".format(len(keys))).strip()
        if choice.isdigit() and 1 <= int(choice) <= len(keys):
            return keys[int(choice) - 1]
        print(f"  ⚠️ 请输入 1-{len(keys)} 之间的数字。")


# ── 命令实现 ──────────────────────────────────────────

def cmd_add(fields=None):
    """记录新决策。fields 为 dict 时使用非交互模式。"""
    print("\n" + "=" * 50)
    print("  🏛️  记录新决策")
    print("=" * 50)

    if fields:
        # 非交互模式
        category = fields.get("category", "other")
        title = fields.get("title", "未命名决策")
        decision = fields.get("decision", "")
        alternatives_raw = fields.get("alternatives", "无")
        rationale = fields.get("rationale", "")
        expected = fields.get("expected", "")
        risk = fields.get("risk", "medium")
        tags_raw = fields.get("tags", "")
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
        review_date = fields.get("review_date", (date.today() + timedelta(days=180)).isoformat())

        print(f"  类别: {CATEGORIES.get(category, category)}")
        print(f"  标题: {title}")
        print(f"  风险: {RISK_LEVELS.get(risk, risk)}")
        print(f"  复盘: {review_date}")
    else:
        # 交互模式
        category = pick_option("选择类别：", CATEGORIES)
        title = ask("决策标题（eg. 从A公司跳槽到B公司）", required=True)
        decision = ask("你做了什么选择", required=True, multiline=True)
        alternatives_raw = ask("你放弃的其他选项（逗号分隔）", default="无")
        rationale = ask("选择理由（为什么选这个）", required=True, multiline=True)
        expected = ask("你预期会怎样", required=True, multiline=True)
        risk = pick_option("风险等级：", RISK_LEVELS)
        tags_raw = ask("标签（逗号分隔，可选）", default="")
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

        # 默认 6 个月后复盘
        review_date = (date.today() + timedelta(days=180)).isoformat()
        review_choice = ask(f"复盘日期（默认 6 个月后: {review_date}），直接回车或输入其他日期", default=review_date)
        try:
            datetime.strptime(review_choice, "%Y-%m-%d")
            review_date = review_choice
        except ValueError:
            print(f"  ⚠️ 日期格式无效，使用默认: {review_date}")

    entry = {
        "id": str(uuid.uuid4()),
        "date_made": date.today().isoformat(),
        "category": category,
        "title": title,
        "decision_made": decision,
        "alternatives": [a.strip() for a in alternatives_raw.split(",") if a.strip()],
        "rationale": rationale,
        "expected_outcome": expected,
        "risk_level": risk,
        "review_date": review_date,
        "status": "pending",
        "review": None,
        "tags": tags,
        "created_at": datetime.now().isoformat(),
    }

    data = load_data()
    data["decisions"].append(entry)
    save_data(data)

    print("\n" + "─" * 50)
    print(f"  ✅ 决策已存档！")
    print(f"  📋 ID: {entry['id'][:8]}...")
    print(f"  📅 复盘日期: {review_date}")
    print(f"  📊 共 {len(data['decisions'])} 个决策")
    print("─" * 50)


def cmd_list():
    """列出所有决策"""
    data = load_data()
    decisions = data.get("decisions", [])
    if not decisions:
        print("\n📭 还没有记录任何决策。用 `add` 开始记录吧。")
        return

    print("\n" + "=" * 60)
    print(f"  📋 决策列表（共 {len(decisions)} 个）")
    print("=" * 60)

    for d in sorted(decisions, key=lambda x: x["date_made"], reverse=True):
        cat_icon = CATEGORIES.get(d["category"], "📌")
        reviewed = d["review"] is not None
        emoji = "✅" if reviewed else "⏳"
        rating_str = f" ★{d['review']['rating']}" if d.get("review") and d["review"].get("rating") else ""
        print(f"\n  {emoji} [{d['id'][:8]}] {cat_icon} {d['title']}{rating_str}")
        print(f"     📅 {d['date_made']}  |  风险: {RISK_LEVELS.get(d['risk_level'], d['risk_level'])}")
        if d["review_date"]:
            due = "⚠️ 超期" if date.today().isoformat() > d["review_date"] and not reviewed else ""
            print(f"     🔄 复盘: {d['review_date']} {due}")
        if d.get("tags"):
            print(f"     🏷️  {' '.join('#' + t for t in d['tags'])}")


def cmd_pending():
    """显示待复盘决策"""
    data = load_data()
    today = date.today().isoformat()

    due = [d for d in data["decisions"]
           if d["status"] == "pending" and d["review_date"] and d["review_date"] <= today]
    upcoming = [d for d in data["decisions"]
                if d["status"] == "pending" and d["review_date"] and d["review_date"] > today]

    if not due and not upcoming:
        print("\n🎉 没有待复盘的决策。")
        return

    if due:
        print("\n" + "=" * 60)
        print(f"  ⏰ 已到期待复盘（{len(due)} 个）")
        print("=" * 60)
        for d in sorted(due, key=lambda x: x["review_date"]):
            cat_icon = CATEGORIES.get(d["category"], "📌")
            days_over = (date.today() - datetime.strptime(d["review_date"], "%Y-%m-%d").date()).days
            print(f"\n  🔴 [{d['id'][:8]}] {cat_icon} {d['title']}")
            print(f"     超期 {days_over} 天 | 风险: {RISK_LEVELS.get(d['risk_level'], d['risk_level'])}")
            print(f"     当初预期: {d['expected_outcome'][:60]}...")
            print(f"     使用: review {d['id'][:8]}")

    if upcoming:
        print("\n" + "─" * 60)
        print(f"  📅 即将到期（{len(upcoming)} 个）")
        print("─" * 60)
        for d in sorted(upcoming, key=lambda x: x["review_date"]):
            cat_icon = CATEGORIES.get(d["category"], "📌")
            days_left = (datetime.strptime(d["review_date"], "%Y-%m-%d").date() - date.today()).days
            print(f"  [{d['id'][:8]}] {cat_icon} {d['title']} — 还剩 {days_left} 天")


def cmd_review(identifier):
    """复盘评估一个决策"""
    data = load_data()
    entry = find_decision(data, identifier)
    if not entry:
        print(f"\n❌ 未找到决策: {identifier}")
        return

    print("\n" + "=" * 50)
    print(f"  🔄 复盘决策: {entry['title']}")
    print("=" * 50)

    # 展示当初的记录
    cat_icon = CATEGORIES.get(entry["category"], "📌")
    print(f"\n📋 当初的记录:")
    print(f"  {cat_icon} 类别: {entry['category']}")
    print(f"  📅 日期: {entry['date_made']}")
    print(f"  🎯 选择: {entry['decision_made']}")
    if entry.get("alternatives") and entry["alternatives"] != ["无"]:
        print(f"  🔄 放弃的选项: {', '.join(entry['alternatives'])}")
    print(f"  💡 理由: {entry['rationale']}")
    print(f"  🔮 预期: {entry['expected_outcome']}")
    print(f"  ⚡ 风险: {RISK_LEVELS.get(entry['risk_level'], entry['risk_level'])}")

    if entry["review"]:
        print(f"\n⚠️ 这个决策已经复盘过了。是否重新评估？(y/n)")
        if input("> ").strip().lower() != "y":
            return

    # 复盘填写
    print("\n📝 现在来评估结果：")
    outcome = ask("实际结果怎么样", required=True, multiline=True)
    surprises = ask("有什么意料之外的事", default="无", multiline=True)

    print("\n评分 (1-5 星):")
    print("  1 = 完全错了 ❌")
    print("  2 = 不太对 😕")
    print("  3 = 还行 😐")
    print("  4 = 基本对了 👍")
    print("  5 = 太对了 🎯")
    while True:
        rating_str = input("> 评分 (1-5): ").strip()
        if rating_str.isdigit() and 1 <= int(rating_str) <= 5:
            rating = int(rating_str)
            break
        print("  ⚠️ 请输入 1-5 的数字。")

    lessons = ask("你学到了什么", required=True, multiline=True)
    would_change = ask("如果重来，会怎么选", default="和当初一样", multiline=True)

    entry["review"] = {
        "review_date": date.today().isoformat(),
        "outcome": outcome,
        "rating": rating,
        "lessons": lessons,
        "surprises": surprises,
        "would_change": would_change,
    }
    entry["status"] = "reviewed"

    save_data(data)
    print("\n" + "─" * 50)
    star_str = "★" * rating + "☆" * (5 - rating)
    print(f"  ✅ 复盘完成！评分: {rating}/5 {star_str}")
    print(f"  📖 教训已存档: {lessons[:50]}...")
    print("─" * 50)


def cmd_insights():
    """生成成长叙事与决策者画像"""
    data = load_data()
    decisions = data.get("decisions", [])
    reviewed = [d for d in decisions if d["review"] is not None]

    if not reviewed:
        print("\n📭 还没有已复盘的决策。先用 `review` 评估一些决策吧。")
        if decisions:
            print(f"   你有 {len(decisions)} 个待复盘的决策。")
        return

    print("\n" + "=" * 60)
    print("  🧠 决策者画像 — 成长叙事")
    print("=" * 60)

    # ── 基础统计 ──
    total = len(decisions)
    reviewed_count = len(reviewed)
    pending_count = total - reviewed_count
    ratings = [d["review"]["rating"] for d in reviewed]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0

    cat_acc = {}  # 各类别准确率
    for d in reviewed:
        cat = d["category"]
        if cat not in cat_acc:
            cat_acc[cat] = {"count": 0, "total_rating": 0}
        cat_acc[cat]["count"] += 1
        cat_acc[cat]["total_rating"] += d["review"]["rating"]

    risk_acc = {}
    for d in reviewed:
        rl = d["risk_level"]
        if rl not in risk_acc:
            risk_acc[rl] = {"count": 0, "total_rating": 0}
        risk_acc[rl]["count"] += 1
        risk_acc[rl]["total_rating"] += d["review"]["rating"]

    # ── 决策者类型 ──
    high_risk_count = sum(1 for d in decisions if d["risk_level"] == "high")
    low_risk_count = sum(1 for d in decisions if d["risk_level"] == "low")
    risk_ratio = high_risk_count / total if total > 0 else 0

    if risk_ratio > 0.5:
        decision_type = "🔥 冒险型决策者"
        type_desc = "你倾向于高风险高回报的选择。大胆，但注意控制损失。"
    elif risk_ratio < 0.2:
        decision_type = "🛡️ 谨慎型决策者"
        type_desc = "你倾向于稳妥的选择。稳健，但可能错过一些机会。"
    else:
        decision_type = "⚖️ 平衡型决策者"
        type_desc = "你在风险和稳健之间寻找平衡。成熟的选择风格。"

    # 基于评分判断准确型/直觉型
    avg_high_risk_rating = 0
    if "high" in risk_acc and risk_acc["high"]["count"] > 0:
        avg_high_risk_rating = risk_acc["high"]["total_rating"] / risk_acc["high"]["count"]
    avg_low_risk_rating = 0
    if "low" in risk_acc and risk_acc["low"]["count"] > 0:
        avg_low_risk_rating = risk_acc["low"]["total_rating"] / risk_acc["low"]["count"]

    if avg_rating >= 4.0:
        type_desc += ' 你的判断准确率很高，属于"分析型"——你做了功课才下决定。'
    elif avg_rating >= 3.0:
        type_desc += " 你的判断准确率中等，偶尔会靠直觉，有时失误。"
    else:
        type_desc += " 你的判断准确率偏低，可能需要更多信息收集。"

    # ── 输出画像 ──
    print(f"\n  📊 决策者类型: {decision_type}")
    print(f"  {type_desc}")
    print(f"\n  📈 整体评分: {avg_rating:.2f} / 5.0")
    star_bar = "▓" * int(avg_rating * 10) + "░" * (50 - int(avg_rating * 10))
    print(f"               [{star_bar}]")

    print(f"\n  📋 概况:")
    print(f"     总决策: {total} 个")
    print(f"     已复盘: {reviewed_count} 个")
    print(f"     待复盘: {pending_count} 个")
    print(f"     高风险决策: {high_risk_count} 个")

    # ── 最佳 / 最差决策 ──
    sorted_by_rating = sorted(reviewed, key=lambda d: d["review"]["rating"], reverse=True)
    best = sorted_by_rating[:3]
    worst = [d for d in sorted_by_rating if d["review"]["rating"] <= 2][:3]

    if best:
        print(f"\n  🏆 最佳决策 TOP {min(3, len(best))}:")
        for i, d in enumerate(best, 1):
            cat_icon = CATEGORIES.get(d["category"], "📌")
            print(f"    {i}. ★{d['review']['rating']} {cat_icon} {d['title']} ({d['date_made']})")
            print(f"       {d['review']['lessons'][:60]}...")

    if worst:
        print(f"\n  💀 最差决策 TOP {min(3, len(worst))}:")
        for i, d in enumerate(worst, 1):
            cat_icon = CATEGORIES.get(d["category"], "📌")
            print(f"    {i}. ★{d['review']['rating']} {cat_icon} {d['title']} ({d['date_made']})")
            print(f"       {d['review']['lessons'][:60]}...")

    # ── 各类别准确率 ──
    print(f"\n  📊 各类别决策准确率:")
    for cat, data2 in sorted(cat_acc.items(), key=lambda x: x[1]["total_rating"] / x[1]["count"], reverse=True):
        avg_c = data2["total_rating"] / data2["count"]
        cat_icon = CATEGORIES.get(cat, "📌")
        bar = "▓" * int(avg_c * 10) + "░" * (50 - int(avg_c * 10))
        print(f"    {cat_icon} {cat}: {avg_c:.2f}/5 [{bar}] ({data2['count']}次)")

    # ── 失误模式分析 ──
    low_rating = [d for d in reviewed if d["review"]["rating"] <= 2]
    if low_rating:
        print(f"\n  🔍 失误模式分析:")
        # 按类别看失误
        fail_by_cat = {}
        for d in low_rating:
            fail_by_cat.setdefault(d["category"], 0)
            fail_by_cat[d["category"]] += 1
        worst_cat = max(fail_by_cat, key=fail_by_cat.get) if fail_by_cat else None
        if worst_cat:
            fail_count = fail_by_cat[worst_cat]
            cat_icon = CATEGORIES.get(worst_cat, "📌")
            print(f"     ⚠️ 你在 {cat_icon} {worst_cat} 类决策中最容易失误 ({fail_count}次)")

        # 按风险看失误
        fail_by_risk = {}
        for d in low_rating:
            fail_by_risk.setdefault(d["risk_level"], 0)
            fail_by_risk[d["risk_level"]] += 1
        worst_risk = max(fail_by_risk, key=fail_by_risk.get) if fail_by_risk else None
        if worst_risk:
            print(f"     ⚠️ 你在 {RISK_LEVELS.get(worst_risk, worst_risk)} 决策中最容易失误")

        # 找共同教训
        lessons_list = [d["review"]["lessons"] for d in low_rating]
        print(f"     📝 失误教训摘录:")
        for d in low_rating:
            lsn = d["review"]["lessons"]
            print(f"       · {d['title']}: {lsn[:80]}...")

    # ── 进步趋势 ──
    if len(reviewed) >= 3:
        sorted_by_time = sorted(reviewed, key=lambda d: d["review"]["review_date"])
        mid = len(sorted_by_time) // 2
        early_half = sorted_by_time[:mid]
        late_half = sorted_by_time[mid:]
        early_avg = sum(d["review"]["rating"] for d in early_half) / len(early_half)
        late_avg = sum(d["review"]["rating"] for d in late_half) / len(late_half)

        print(f"\n  📈 决策力趋势:")
        diff = late_avg - early_avg
        if diff > 0.3:
            trend = "📈 明显进步"
        elif diff > 0.1:
            trend = "↗️ 略有进步"
        elif diff > -0.1:
            trend = "➡️ 持平"
        elif diff > -0.3:
            trend = "↘️ 略有退步"
        else:
            trend = "📉 明显退步"

        print(f"     {trend} (早期: {early_avg:.2f} → 近期: {late_avg:.2f})")
        if diff < 0:
            print(f"     💡 建议: 回顾近期低分决策，是否在重复相同的错误？")

    # ── 时间线 ──
    print(f"\n  📖 人生决策时间线:")
    for d in sorted(decisions, key=lambda x: x["date_made"]):
        cat_icon = CATEGORIES.get(d["category"], "📌")
        review_status = "✅" if d["review"] else "⏳"
        rating_str = f" ★{d['review']['rating']}" if d.get("review") and d["review"].get("rating") else ""
        print(f"     {d['date_made']} {review_status} {cat_icon} {d['title']}{rating_str}")

    # ── 金句 ──
    print(f"\n  💬 成长金句:")
    quotes = []
    if avg_rating >= 4.0:
        quotes.append("你的判断力很强，但记住：好决策不总有好结果，好结果不总靠好决策。")
    elif avg_rating <= 2.5:
        quotes.append("失误是成长的路标。你最大的优势不是不犯错，而是能从错误中迭代。")
    if low_rating:
        quotes.append("最贵的一课通常来自最低分的决定。你已经付了学费，别浪费。")
    if best:
        best_lesson = best[0]["review"]["lessons"]
        quotes.append(f"你最好的决定教会你: {best_lesson[:40]}...")
    for q in quotes:
        print(f"     \"{q}\"")

    print("\n" + "=" * 60)


def cmd_stats():
    """统计概览"""
    data = load_data()
    decisions = data.get("decisions", [])
    if not decisions:
        print("\n📭 还没有记录任何决策。")
        return

    reviewed = [d for d in decisions if d["review"] is not None]
    total = len(decisions)
    reviewed_count = len(reviewed)
    pending_count = total - reviewed_count

    print("\n" + "=" * 50)
    print(f"  📊 决策档案馆概况")
    print("=" * 50)
    print(f"\n  总决策: {total}")
    print(f"  已复盘: {reviewed_count} ({reviewed_count/total*100:.0f}%)")
    print(f"  待复盘: {pending_count}")
    if reviewed_count > 0:
        ratings = [d["review"]["rating"] for d in reviewed]
        print(f"  平均评分: {sum(ratings)/len(ratings):.2f}/5")
        print(f"  最高评分: {max(ratings)}")
        print(f"  最低评分: {min(ratings)}")

    # 类别分布
    print(f"\n  类别分布:")
    cat_count = {}
    for d in decisions:
        cat_count[d["category"]] = cat_count.get(d["category"], 0) + 1
    for cat, count in sorted(cat_count.items(), key=lambda x: x[1], reverse=True):
        cat_icon = CATEGORIES.get(cat, "📌")
        bar = "█" * count + "░" * (20 - count)
        print(f"    {cat_icon} {cat}: {count} {bar}")

    # 风险分布
    print(f"\n  风险分布:")
    risk_count = {}
    for d in decisions:
        risk_count[d["risk_level"]] = risk_count.get(d["risk_level"], 0) + 1
    for rl in ["low", "medium", "high"]:
        count = risk_count.get(rl, 0)
        print(f"    {RISK_LEVELS.get(rl, rl)}: {count}")

    # 每月决策数
    print(f"\n  月度决策数:")
    monthly = {}
    for d in decisions:
        m = d["date_made"][:7]
        monthly[m] = monthly.get(m, 0) + 1
    for m, count in sorted(monthly.items()):
        bar = "▊" * count
        print(f"    {m}: {count} {bar}")


def cmd_score():
    """评分排名"""
    data = load_data()
    reviewed = [d for d in data.get("decisions", []) if d["review"] is not None]
    if not reviewed:
        print("\n📭 还没有已复盘的决策。")
        return

    print("\n" + "=" * 60)
    print("  🏆 决策评分排名")
    print("=" * 60)

    sorted_d = sorted(reviewed, key=lambda d: d["review"]["rating"], reverse=True)
    for i, d in enumerate(sorted_d, 1):
        cat_icon = CATEGORIES.get(d["category"], "📌")
        star_str = "★" * d["review"]["rating"] + "☆" * (5 - d["review"]["rating"])
        print(f"\n  #{i} {star_str} {cat_icon} {d['title']}")
        print(f"     {d['date_made']} | {RISK_LEVELS.get(d['risk_level'], d['risk_level'])}")
        print(f"     结果: {d['review']['outcome'][:60]}...")


def cmd_delete(identifier):
    """删除一个决策"""
    data = load_data()
    entry = find_decision(data, identifier)
    if not entry:
        print(f"\n❌ 未找到决策: {identifier}")
        return

    print(f"\n⚠️ 确定要删除这个决策吗？")
    print(f"  [{entry['id'][:8]}] {entry['title']} ({entry['date_made']})")
    confirm = input("输入 YES 确认删除: ").strip()
    if confirm != "YES":
        print("取消删除。")
        return

    data["decisions"] = [d for d in data["decisions"] if d["id"] != entry["id"]]
    save_data(data)
    print(f"✅ 已删除: {entry['title']}")


def cmd_export():
    """导出全部数据"""
    data = load_data()
    print(json.dumps(data, ensure_ascii=False, indent=2))


# ── 主入口 ────────────────────────────────────────────

def parse_cli_add_args(args):
    """从 CLI 参数解析添加决策所需的字段（非交互模式）"""
    fields = {}
    i = 0
    while i < len(args):
        if args[i] in ("-c", "--category") and i + 1 < len(args):
            fields["category"] = args[i + 1]
            i += 2
        elif args[i] in ("-t", "--title") and i + 1 < len(args):
            fields["title"] = args[i + 1]
            i += 2
        elif args[i] in ("-d", "--decision") and i + 1 < len(args):
            fields["decision"] = args[i + 1]
            i += 2
        elif args[i] in ("-a", "--alternatives") and i + 1 < len(args):
            fields["alternatives"] = args[i + 1]
            i += 2
        elif args[i] in ("-r", "--rationale") and i + 1 < len(args):
            fields["rationale"] = args[i + 1]
            i += 2
        elif args[i] in ("-e", "--expected") and i + 1 < len(args):
            fields["expected"] = args[i + 1]
            i += 2
        elif args[i] in ("-k", "--risk") and i + 1 < len(args):
            fields["risk"] = args[i + 1]
            i += 2
        elif args[i] in ("-g", "--tags") and i + 1 < len(args):
            fields["tags"] = args[i + 1]
            i += 2
        elif args[i] in ("-p", "--review-date") and i + 1 < len(args):
            fields["review_date"] = args[i + 1]
            i += 2
        else:
            i += 1
    return fields


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "add":
        # 如果有结构化参数就用非交互模式
        cli_fields = parse_cli_add_args(sys.argv[2:])
        if cli_fields:
            cmd_add(cli_fields)
        else:
            cmd_add()
    elif command == "list":
        cmd_list()
    elif command == "pending":
        cmd_pending()
    elif command == "review":
        if len(sys.argv) < 3:
            print("用法: decision_archives.py review <id 或标题>")
            return
        cmd_review(sys.argv[2])
    elif command == "insights":
        cmd_insights()
    elif command == "stats":
        cmd_stats()
    elif command == "score":
        cmd_score()
    elif command == "delete":
        if len(sys.argv) < 3:
            print("用法: decision_archives.py delete <id 或标题>")
            return
        cmd_delete(sys.argv[2])
    elif command == "export":
        cmd_export()
    else:
        print(f"未知命令: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()