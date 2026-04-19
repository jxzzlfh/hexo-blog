"""One-off: fetch Memos in date range via memos skill module."""
from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

SKILL = Path(r"C:\Users\lifenghua\.claude\skills\memos\memos.py")
TZ = ZoneInfo("Asia/Shanghai")
START = datetime(2026, 4, 13, 0, 0, 0, tzinfo=TZ)
END = datetime(2026, 4, 19, 23, 59, 59, 999999, tzinfo=TZ)


def load_memos_module():
    spec = importlib.util.spec_from_file_location("memos_skill", SKILL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse_iso(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def local_dt(utc: datetime) -> datetime:
    return utc.astimezone(TZ)


def in_window(utc: datetime) -> bool:
    local = local_dt(utc)
    return START <= local <= END


def main():
    ms = load_memos_module()
    out: list[dict] = []
    page_token = None
    while True:
        kwargs: dict = {"pageSize": 1000, "orderBy": "display_time desc"}
        if page_token:
            kwargs["pageToken"] = page_token
        res = ms.list_memos(**kwargs)
        memos = res.get("memos") or []
        if not memos:
            break
        min_utc = None
        for m in memos:
            dt = parse_iso(m["displayTime"])
            if min_utc is None or dt < min_utc:
                min_utc = dt
            if in_window(dt):
                out.append(m)
        next_tok = res.get("nextPageToken")
        # 已按时间倒序；本页最早一条若早于窗口起点，更旧页不可能落入窗口
        if min_utc and local_dt(min_utc) < START:
            break
        if not next_tok:
            break
        page_token = next_tok

    out.sort(key=lambda x: parse_iso(x["displayTime"]))
    Path(sys.argv[1]).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(len(out), "memos written")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: memos_week_fetch.py <out.json>", file=sys.stderr)
        sys.exit(1)
    main()
