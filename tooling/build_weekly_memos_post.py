# -*- coding: utf-8 -*-
"""Build Hexo weekly digest from memos_week JSON."""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Shanghai")
MAX_BODY_CHARS = 4500
MEMOS_ENV = Path(r"C:\Users\lifenghua\.claude\skills\memos\.env")


def load_memos_url() -> str:
    import os

    if os.environ.get("MEMOS_URL"):
        return os.environ["MEMOS_URL"].rstrip("/")
    if MEMOS_ENV.is_file():
        for line in MEMOS_ENV.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("MEMOS_URL="):
                return line.split("=", 1)[1].strip().strip('"').strip("'").rstrip("/")
    return ""


def first_heading(content: str) -> str:
    for line in (content or "").splitlines():
        s = line.strip()
        if s.startswith("#"):
            return re.sub(r"^#+\s*", "", s).strip()[:80]
    return ""


def classify(m: dict) -> str:
    tags = [t.lower() for t in (m.get("tags") or [])]
    text = (m.get("content") or "") + "\n" + (m.get("snippet") or "")
    low = text.lower()

    if any(x in tags for x in ["深度阅读", "批判性思维", "信息消费"]):
        return "阅读与思辨"
    if "36kr.com" in text or "36氪" in text:
        return "阅读摘录"
    if "noteseed" in low or "note seed" in low:
        return "项目 · NoteSeed"
    if "hexo" in low and "skill" in low:
        return "工具与流程 · Hexo"
    if "memos" in low and ("skill" in low or "更新日志" in text):
        return "工具与流程 · Memos"
    if any(
        k in text
        for k in [
            "Claude Code",
            "Cursor",
            "Routines",
            "Hermes",
            "Agent",
            "Skill",
            "MCP",
            "AI 编程",
            "大模型",
        ]
    ):
        return "AI 与工程实践"
    if any(k in text for k in ["创业", "赚钱", "商业", "产品", "增长"]):
        return "产品与商业思考"
    if any(k in text for k in ["学习", "知识", "笔记", "认知"]):
        return "学习与知识管理"
    return "随笔与摘录"


def uid(name: str) -> str:
    return name.replace("memos/", "") if name.startswith("memos/") else name


def main():
    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    memos_url = (
        sys.argv[3].rstrip("/")
        if len(sys.argv) > 3 and sys.argv[3]
        else load_memos_url()
    )

    data = json.loads(src.read_text(encoding="utf-8"))
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for m in data:
        by_cat[classify(m)].append(m)

    order = sorted(by_cat.keys(), key=lambda x: (0 if x.startswith("项目") else 1, x))
    lines: list[str] = []
    lines.append("---")
    lines.append("title: 周记 · Memos 摘录（2026-04-13 ~ 2026-04-19）")
    lines.append("date: 2026-04-19 20:00:00")
    lines.append("updated: 2026-04-19 20:00:00")
    lines.append("tags:")
    lines.append("  - 周记")
    lines.append("  - Memos")
    lines.append("categories:")
    lines.append("  - 周记")
    lines.append(
        "excerpt: 汇总本周 Memos 中按主题整理的技术笔记、阅读摘录与随笔，便于检索与复盘。"
    )
    lines.append("---")
    lines.append("")
    lines.append(
        "> 本文由 [Memos](https://usememos.com/) 中 **2026-04-13 ~ 2026-04-19**（北京时间）发布的笔记自动汇总生成，按主题归类；每条保留原文要点，并附回链。"
    )
    lines.append("")

    for cat in order:
        items = sorted(
            by_cat[cat], key=lambda x: x.get("displayTime") or ""
        )
        lines.append(f"## {cat}")
        lines.append("")
        for m in items:
            dt = m.get("displayTime", "")
            title = first_heading(m.get("content") or "") or (m.get("snippet") or "（无标题）")[:120]
            title = title.replace("\n", " ").strip()
            link = ""
            if memos_url:
                link = f"{memos_url}/memos/{uid(m.get('name', ''))}"
            lines.append(f"### {title}")
            lines.append("")
            lines.append(f"- **时间**：{dt}")
            if link:
                lines.append(f"- **原文**：[在 Memos 中打开]({link})")
            lines.append("")
            body = (m.get("content") or "").strip()
            if len(body) > MAX_BODY_CHARS:
                body = (
                    body[:MAX_BODY_CHARS].rstrip()
                    + "\n\n…\n\n（篇幅过长，完整正文请在上方 Memos 原文链接中查看。）"
                )
            lines.append(body)
            lines.append("")
            lines.append("---")
            lines.append("")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", out, "categories:", len(order), "memos:", len(data))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "usage: build_weekly_memos_post.py <memos.json> <out.md> [MEMOS_URL]",
            file=sys.stderr,
        )
        sys.exit(1)
    main()
