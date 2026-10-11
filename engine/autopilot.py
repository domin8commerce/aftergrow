"""Aftergrow Pinterest autopilot helper. Keeps queue.json and status.json in step with Tailwind.
The scheduled Claude session makes the Tailwind calls; this script decides what to do and records
what happened, so nothing depends on memory or interpretation. All times are UTC.

Run from the repo root:
  python3 -I engine/autopilot.py . status                       # mode, queue, canary budget, what to do next
  python3 -I engine/autopilot.py . reconcile <queued.json>      # compare Tailwind's queued posts with queue.json
  python3 -I engine/autopilot.py . resolve <ID> <sent|failed|deleted|missed> ["reason"]
  python3 -I engine/autopilot.py . next-canary                  # create_post payload for the next canary (blocked mode)
  python3 -I engine/autopilot.py . next-batch <N>               # create_post payloads for the next N pins (live mode)
  python3 -I engine/autopilot.py . scheduled <ID> <tailwind_post_id> <sendAt>
  python3 -I engine/autopilot.py . appeal <filed|approved|denied> [YYYY-MM-DD]

<queued.json> is the raw JSON that Tailwind list_posts (status "queued") returned, saved to a file.
<sendAt> may be unix seconds, unix milliseconds or ISO 8601, exactly as Tailwind returned it.
"""
import datetime as dt, json, pathlib, re, sys, urllib.request
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
PACE = 3                    # pins a day while the account is young (RUNBOOK: Pace and credits)
CANARY_BUDGET = 2           # blocked mode: at most 2 canary attempts in any 7 days
PROBATION_DAYS = 14         # after a block lifts, keep only a short queue for 14 days
RUN_DAYS = (0, 3)           # the scheduled task runs Monday and Thursday, 8:47 AM Eastern
SPAM = re.compile(r"spam|blocked", re.I)


def now():
    return dt.datetime.now(dt.timezone.utc)


def iso(t):
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_time(v):
    s = str(v).strip()
    if re.fullmatch(r"\d+(\.\d+)?", s):
        x = float(s)
        return dt.datetime.fromtimestamp(x / 1000 if x > 1e11 else x, dt.timezone.utc)
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(dt.timezone.utc)


def page(link):
    return link.split("?")[0].replace("https://getaftergrow.com", "")


class Repo:
    def __init__(self, root):
        self.root = pathlib.Path(root)
        self.q = json.loads((self.root / "queue.json").read_text())
        self.s = json.loads((self.root / "status.json").read_text())
        self.cfg = json.loads((self.root / "config.json").read_text())
        lp = self.root / "log.json"
        self.log = json.loads(lp.read_text()) if lp.exists() else []
        self.s.setdefault("attempts", [])

    def row(self, pid):
        r = next((r for r in self.q if r["id"] == pid), None)
        if r is None:
            raise SystemExit(f"ERROR {pid} is not in queue.json")
        return r

    def save(self, **event):
        if event:
            self.log.append(dict(at=iso(now()), **event))
        (self.root / "queue.json").write_text(json.dumps(self.q, indent=1, ensure_ascii=False) + "\n")
        (self.root / "status.json").write_text(json.dumps(self.s, indent=1, ensure_ascii=False) + "\n")
        (self.root / "log.json").write_text(json.dumps(self.log, indent=1, ensure_ascii=False) + "\n")

    # ---------------------------------------------------------------- facts the rules need
    def scheduled(self):
        return [r for r in self.q if r["status"] == "scheduled"]

    def ready(self):
        return sorted((r for r in self.q if r["status"] == "ready"), key=lambda r: r["order"])

    def attempt_for(self, post_id):
        return next((a for a in self.s["attempts"] if a.get("post_id") == post_id), None)

    def attempts_last_7_days(self):
        t = now()
        return [a for a in self.s["attempts"] if a["result"] in ("blocked", "failed_other", "sent")
                and t - dt.timedelta(days=7) <= parse_time(a["send_at_utc"]) <= t]

    def payload(self, r):
        return dict(accountId=self.cfg["tailwind_account_id"], mediaUrl=self.cfg["media_base"] + r["image"],
                    boardId=r["board_id"], title=r["title"], description=r["description"], url=r["link"],
                    altText=r["alt_text"], useNextOpenSlot=True)

    def next_run(self):
        t = now().astimezone(ET)
        for d in range(0, 8):
            day = (t + dt.timedelta(days=d)).date()
            run = dt.datetime(day.year, day.month, day.day, 8, 47, tzinfo=ET)
            if day.weekday() in RUN_DAYS and run > t:
                return run.astimezone(dt.timezone.utc)

    def in_probation(self):
        since = self.s.get("live_since")
        return bool(since) and now() < parse_time(since) + dt.timedelta(days=PROBATION_DAYS)

    def pins_to_schedule(self):
        """Live mode: how many more pins to queue now. In probation, only cover until a day after the
        next run, so a fresh block costs at most a few failed pins; after that keep 14 days queued."""
        horizon = self.next_run() + dt.timedelta(days=1) if self.in_probation() else now() + dt.timedelta(days=14)
        days = (horizon - now()).total_seconds() / 86400
        future = [r for r in self.scheduled() if parse_time(r["send_at_utc"]) > now()]
        return max(0, int(days * PACE + 0.5) - len(future))


def url_ok(url):
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status == 200 and resp.headers.get("Content-Type", "").startswith("image/")
    except Exception:
        return False


# -------------------------------------------------------------------- commands
def cmd_status(R):
    s, sch = R.s, R.scheduled()
    print(f"MODE {s['mode']}  (since {s.get('since') or s.get('live_since') or '-'})")
    print(f"appeal: filed_on={s['appeal'].get('filed_on')} result={s['appeal'].get('result')}"
          + (f"  paused until {s['retest_after']}" if s.get("retest_after") else ""))
    print(f"queue: {len(R.ready())} ready, {len(sch)} scheduled, {sum(r['status'] == 'posted' for r in R.q)} posted")
    for r in sch:
        late = " (TIME PASSED: get_post it, then resolve)" if parse_time(r["send_at_utc"]) <= now() else ""
        print(f"  scheduled {r['id']} post {r['post_id']} at {r['send_at_utc']} role={r.get('role', 'pin')}{late}")
    if s["mode"] == "blocked":
        used = R.attempts_last_7_days()
        print(f"canary attempts in last 7 days: {len(used)}/{CANARY_BUDGET}: " + ", ".join(a['id'] for a in used))
        ok, why = can_canary(R)
        print(f"NEXT: {'schedule one canary (run next-canary)' if ok else 'no new canary: ' + why}")
    else:
        print(f"probation: {R.in_probation()}  next run: {iso(R.next_run())}")
        print(f"NEXT: schedule {R.pins_to_schedule()} more pins (run next-batch with that number)")
    counts = {}
    for r in R.q:
        counts[page(r["link"])] = counts.get(page(r["link"]), 0) + 1
    print("pins per landing page (cap 8): " + ", ".join(f"{p} {n}" for p, n in sorted(counts.items(), key=lambda x: -x[1])))


def can_canary(R):
    if R.s["mode"] != "blocked":
        return False, "mode is live"
    if any(r.get("role") == "canary" for r in R.scheduled()):
        return False, "a canary is already queued"
    if R.s["appeal"].get("result") == "approved":
        return True, "appeal approved: test now"
    paused = R.s.get("retest_after")
    if paused and now() < parse_time(paused):
        return False, f"paused after the appeal was denied; no canary before {paused}"
    used = R.attempts_last_7_days()
    if len(used) >= CANARY_BUDGET:
        nxt = min(parse_time(a["send_at_utc"]) for a in used) + dt.timedelta(days=7)
        return False, f"{len(used)} attempts in the last 7 days; next allowed after {iso(nxt)}"
    return True, "budget available"


def cmd_next_canary(R):
    ok, why = can_canary(R)
    if not ok:
        raise SystemExit(f"NO CANARY: {why}")
    since = parse_time(R.s["since"])
    tried = {a["page"] for a in R.s["attempts"] if parse_time(a["send_at_utc"]) >= since}
    blocked_before = {r["id"] for r in R.q if any(SPAM.search(h.get("reason", "")) for h in r.get("history", []))}
    fresh = [r for r in R.ready() if r["id"] not in blocked_before]
    for pool in ([r for r in fresh if page(r["link"]) not in tried], fresh, R.ready()):
        for r in pool:
            if url_ok(R.cfg["media_base"] + r["image"]):
                print(json.dumps(dict(id=r["id"], page=page(r["link"]), create_post=R.payload(r)), ensure_ascii=False))
                return
    raise SystemExit("NO CANARY: no ready pin with a reachable image")


def cmd_next_batch(R, n):
    if R.s["mode"] != "live":
        raise SystemExit("NO BATCH: mode is blocked (use next-canary)")
    out = []
    for r in R.ready():
        if len(out) == n:
            break
        if url_ok(R.cfg["media_base"] + r["image"]):
            out.append(dict(id=r["id"], create_post=R.payload(r)))
        else:
            print(f"SKIP {r['id']}: image not reachable yet (push pins/ first)", file=sys.stderr)
    for o in out:
        print(json.dumps(o, ensure_ascii=False))


def cmd_scheduled(R, pid, post_id, send_at):
    r, t = R.row(pid), parse_time(send_at)
    if r["status"] == "scheduled" and r.get("post_id") == post_id:
        print(f"{pid} already recorded")
        return
    if r["status"] != "ready":
        raise SystemExit(f"ERROR {pid} is {r['status']}, not ready. Do not schedule it twice.")
    r.update(status="scheduled", post_id=post_id, send_at_utc=iso(t))
    ev = dict(id=pid, action="scheduled", post_id=post_id, send_at_utc=iso(t))
    if R.s["mode"] == "blocked":
        r["role"] = "canary"
        ev["role"] = "canary"
        R.s["attempts"].append(dict(id=pid, page=page(r["link"]), post_id=post_id, send_at_utc=iso(t), result="pending"))
    R.save(**ev)
    print(f"{pid} scheduled {iso(t)}" + (" as canary" if r.get("role") else ""))


def cmd_resolve(R, pid, outcome, reason=""):
    r = R.row(pid)
    if r["status"] != "scheduled":
        raise SystemExit(f"ERROR {pid} is {r['status']}; only scheduled pins can be resolved")
    a, post_id, t = R.attempt_for(r["post_id"]), r["post_id"], r["send_at_utc"]
    back = lambda event: (r.setdefault("history", []).append(dict(at=iso(now()), event=event, post_id=post_id, reason=reason)),
                          [r.pop(k, None) for k in ("post_id", "send_at_utc", "role")], r.update(status="ready"))
    msg = ""
    if outcome == "sent":
        r["status"] = "posted"
        r.pop("role", None)
        if a:
            a["result"] = "sent"
        if R.s["mode"] == "blocked":
            R.s.update(mode="live", live_since=t, last_success_at=t)
            R.s["since"] = None
            msg = "BLOCK LIFTED. Mode is live, probation for 14 days. Run status, then next-batch."
        else:
            R.s["last_success_at"] = t
    elif outcome == "failed" and SPAM.search(reason):
        back("failed")
        if a:
            a["result"] = "blocked"
        else:
            R.s["attempts"].append(dict(id=pid, page=page(r["link"]), post_id=post_id, send_at_utc=t, result="blocked"))
        if R.s["appeal"].get("result") == "approved":
            R.s["appeal"]["result"] = f"approved, but still blocked on {t[:10]}"
        if R.s["mode"] == "live":
            R.s.update(mode="blocked", since=t)
            msg = ("SWITCHED TO BLOCKED. Delete every other queued post in Tailwind with delete_post, then run "
                   "resolve <ID> deleted for each. Do not keep any of them as a canary.")
    elif outcome == "failed":
        back("failed")
        if a:
            a["result"] = "failed_other"
        msg = "Not a spam block. Fix the cause in the copy or image before it is scheduled again."
    elif outcome in ("deleted", "missed"):
        back("unscheduled" if outcome == "deleted" else "missed")
        if a:
            a["result"] = outcome
    else:
        raise SystemExit("outcome must be sent, failed, deleted or missed")
    R.save(id=pid, action=f"resolved {outcome}", post_id=post_id, reason=reason)
    print(f"{pid} -> {r['status']}. {msg}".strip())


def cmd_reconcile(R, path):
    posts = json.loads(pathlib.Path(path).read_text())
    posts = posts.get("posts", posts) if isinstance(posts, dict) else posts
    by_post = {r.get("post_id"): r for r in R.scheduled()}
    seen, problems = set(), 0
    for p in posts:
        m = re.search(r"utm_content=([A-Za-z0-9]+)", p.get("url", ""))
        pid = m.group(1) if m else None
        r = next((x for x in R.q if x["id"] == pid), None)
        if r is None:
            print(f"UNKNOWN Tailwind post {p['id']} ({p.get('url')}): not one of ours. Stop and report it.")
            problems += 1
            continue
        seen.add(p["id"])
        if r["status"] == "scheduled" and r.get("post_id") == p["id"]:
            continue
        if r["status"] == "ready":
            cmd_scheduled(R, pid, p["id"], p["sendAt"])
            print(f"RECORDED {pid}: it was queued in Tailwind but missing from queue.json")
            continue
        print(f"DUPLICATE {pid}: Tailwind post {p['id']} but queue.json has {r['status']} {r.get('post_id')}. "
              f"Delete Tailwind post {p['id']} with delete_post, then re-run reconcile.")
        problems += 1
    for post_id, r in by_post.items():
        if post_id not in seen:
            print(f"RESOLVE {r['id']}: post {post_id} is no longer queued. get_post it, then "
                  f"resolve {r['id']} sent|failed|deleted with the failure reason.")
    for r in R.scheduled():
        if r.get("post_id") in seen and parse_time(r["send_at_utc"]) < now() - dt.timedelta(hours=2):
            print(f"MISSED {r['id']}: still queued 2+ hours after its time. delete_post {r['post_id']}, "
                  f"then resolve {r['id']} missed.")
    print("reconcile:", "problems above, stop and report" if problems else "ok")


def cmd_appeal(R, what, day=None):
    day = day or now().date().isoformat()
    if what == "filed":
        R.s["appeal"]["filed_on"] = day
    elif what in ("approved", "denied"):
        R.s["appeal"]["result"] = f"{what} {day}" if what == "denied" else "approved"
    else:
        raise SystemExit("appeal filed|approved|denied")
    R.save(action=f"appeal {what}", day=day)
    print("appeal:", R.s["appeal"])


if __name__ == "__main__":
    a = sys.argv
    if len(a) < 3:
        raise SystemExit(__doc__)
    R, c = Repo(a[1]), a[2]
    if c == "status": cmd_status(R)
    elif c == "reconcile": cmd_reconcile(R, a[3])
    elif c == "resolve": cmd_resolve(R, a[3], a[4], a[5] if len(a) > 5 else "")
    elif c == "next-canary": cmd_next_canary(R)
    elif c == "next-batch": cmd_next_batch(R, int(a[3]))
    elif c == "scheduled": cmd_scheduled(R, a[3], a[4], a[5])
    elif c == "appeal": cmd_appeal(R, a[3], a[4] if len(a) > 4 else None)
    else: raise SystemExit(__doc__)
