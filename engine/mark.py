"""Record what Tailwind did with a pin, so queue.json stays the single source of truth.

Usage (from the repo root):
  python3 -I engine/mark.py . scheduled   <ID> <tailwind_post_id> <send_at_unix> [canary]
  python3 -I engine/mark.py . posted      <ID> [pinterest_pin_id]
  python3 -I engine/mark.py . failed      <ID> <reason>   # never published: back to ready, failure kept in history
  python3 -I engine/mark.py . unscheduled <ID> <reason>   # deleted from Tailwind before publishing: back to ready
Every call also appends one line to log.json.
"""
import datetime as dt, json, pathlib, sys


def now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main(argv):
    repo, action, pid = pathlib.Path(argv[1]), argv[2], argv[3]
    qp, lp = repo / "queue.json", repo / "log.json"
    q = json.loads(qp.read_text())
    log = json.loads(lp.read_text()) if lp.exists() else []
    row = next((r for r in q if r["id"] == pid), None)
    if row is None:
        raise SystemExit(f"{pid} is not in queue.json")
    ev = dict(at=now(), id=pid, action=action)
    if action == "scheduled":
        send = dt.datetime.fromtimestamp(int(argv[5]), dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        row.update(status="scheduled", post_id=argv[4], send_at_utc=send)
        if len(argv) > 6 and argv[6] == "canary":
            row["role"] = "canary"
        ev.update(post_id=argv[4], send_at_utc=send, role=row.get("role", "pin"))
    elif action == "posted":
        row["status"] = "posted"
        row.pop("role", None)
        if len(argv) > 4:
            row["pinterest_pin_id"] = argv[4]
            ev["pinterest_pin_id"] = argv[4]
    elif action in ("failed", "unscheduled"):
        reason = argv[4] if len(argv) > 4 else ""
        row.setdefault("history", []).append(dict(at=now(), event=action, post_id=row.get("post_id"), reason=reason))
        for k in ("post_id", "send_at_utc", "role"):
            row.pop(k, None)
        row["status"] = "ready"
        ev["reason"] = reason
    else:
        raise SystemExit(f"unknown action {action}")
    log.append(ev)
    qp.write_text(json.dumps(q, indent=1, ensure_ascii=False) + "\n")
    lp.write_text(json.dumps(log, indent=1, ensure_ascii=False) + "\n")
    print(pid, row["status"])


if __name__ == "__main__":
    main(sys.argv)
