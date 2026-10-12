"""Aftergrow on Instagram and Facebook: the posting plan, Metricool payloads and the posting log.

Reels only since Oct 12, 2026 (George's call after the first day: the Reel reached 113 people on Instagram, the
carousel 7). One Reel a day on each network. Reel scripts live in engine/reels_*.py and are rendered by engine/reel2.py.
Older carousels (engine/carousels_*.py) stay for the record; meta.py never plans a carousel any more.

Usage (from the repo root):
  python3 -I engine/meta.py plan [days]          the open slots in the next N days (default 14) and the Reel for each
  python3 -I engine/meta.py payload <ID> <instagram|facebook> reel <YYYY-MM-DDTHH:MM>
                                                  prints the "info" JSON for Metricool's createScheduledPost
  python3 -I engine/meta.py date <YYYY-MM-DDTHH:MM>   the same time with New York's UTC offset, for the "date" field
  python3 -I engine/meta.py logged <ID> <instagram|facebook> reel <YYYY-MM-DDTHH:MM> <metricool id> <uuid>
                                                  records a post Metricool accepted (do this right after each one)
  python3 -I engine/meta.py reid <uuid> <new metricool id>
                                                  after updateScheduledPost, which gives the post a new id
  python3 -I engine/meta.py status               what is logged so far

Metricool: blogId 7369576, timezone America/New_York. Times in this file are New York time.
"""
import datetime as dt, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
sys.path.insert(0, str(ROOT))
import carousel as C  # noqa: E402
import reel2 as R2  # noqa: E402

BLOG_ID = "7369576"
TZ = "America/New_York"
LOG = REPO / "meta_log.json"
NETWORKS = ("instagram", "facebook")
KINDS = ("post", "reel")

# One Reel a day on each network, New York time, Monday is 0. Facebook follows Metricool's audience curve for our
# Page (10:00 on weekdays, Wednesday 12:00 the highest, Sunday 18:00 the evening peak). Instagram Reels go out in the
# evening scroll; the first Reel (Sunday 8:40 PM) reached 16 times the carousel's audience. Revisit with data.
FB_TIMES = {0: "09:52", 1: "09:52", 2: "11:52", 3: "09:52", 4: "09:52", 5: "09:52", 6: "17:52"}
IG_TIME = "19:17"
SLOTS = {d: [("facebook", "reel", FB_TIMES[d]), ("instagram", "reel", IG_TIME)] for d in range(7)}

# Instrumentals from Instagram's music library for business accounts, found through Metricool's audio search
# (Oct 11 and 12, 2026). A Reel script can pin one with audio="<id>"; otherwise Reels rotate through these.
TRACKS = [("1033455569449469", "Peace", "LAVLO"),
          ("1386811643506297", "Home", "Giulio Cercato"),
          ("1579921342191993", "Motive (Instrumental)", "Giulio Cercato"),
          ("2271125906413476", "Gently", "Giulio Cercato"),
          ("1326560949104401", "Check This Out", "Giulio Cercato"),
          ("2477944699150252", "Peaceful Piano", "Dr. Pheel"),
          ("761736589642441", "Be Happy (Instrumental)", "Afro Sound Machine"),
          ("1549201939908190", "Orange Trees", "Jesse Robitaille"),
          ("592271352837708", "Beautiful", "Giulio Cercato"),
          ("587460186676938", "Guitar Peace", "Lance Taber")]


def read_log():
    return json.loads(LOG.read_text()) if LOG.exists() else {"posts": []}


def write_log(log):
    log["posts"].sort(key=lambda p: (p["at"], p["network"]))
    LOG.write_text(json.dumps(log, indent=1) + "\n")


def scripts():
    return {r["id"]: r for r in R2.load()}


def track_for(c):
    if c.get("audio"):
        return str(c["audio"])
    n = int("".join(ch for ch in c["id"] if ch.isdigit()) or 0)
    return TRACKS[(n - 1) % len(TRACKS)][0]


def reel_ready(cid):
    return all((REPO / "reels" / f).exists() for f in (f"{cid}.mp4", f"{cid}_cover.jpg"))


def payload(cid, network, kind, when):
    """The createScheduledPost "info" object. Reels come from the Reel scripts; a carousel ID is accepted only for the
    record (meta.py no longer plans carousels)."""
    assert network in NETWORKS and kind in KINDS, (network, kind)
    info = dict(autoPublish=True, draft=False, shortener=False, smartLinkData={"ids": []},
                providers=[{"network": network}], publicationDate={"dateTime": when + ":00", "timezone": TZ})
    S = scripts()
    if kind == "reel" and cid in S:
        r = S[cid]
        if not reel_ready(cid):
            raise SystemExit(f"{cid}: no Reel yet (render it with engine/reel2.py render reels {cid}, then push)")
        info.update(media=[f"{C.RAW}reels/{cid}.mp4"], videoThumbnailUrl=f"{C.RAW}reels/{cid}_cover.jpg")
        if network == "instagram":
            info.update(text=R2.ig_text(r), firstCommentText="")
            info["instagramData"] = {"type": "REEL", "isAiGenerated": False, "showReelOnFeed": True,
                                     "audioConfiguration": {"audioId": track_for(r), "audioVolume": 100, "videoVolume": 0}}
        else:
            info.update(text=r["fb"], firstCommentText=r["fb_comment"].format(link=C.link(r, "facebook", "reel")))
            info["facebookData"] = {"type": "REEL"}
        return info
    c = {x["id"]: x for x in C.load()}[cid]   # legacy: carousel posts and v1 Reels
    if kind == "post":
        info.update(media=C.media_urls(c), mediaAltText=C.alt_texts(c))
    else:
        info.update(media=[f"{C.RAW}reels/{cid}.mp4"], videoThumbnailUrl=f"{C.RAW}reels/{cid}_cover.jpg")
    if network == "instagram":
        info.update(text=C.ig_text(c), firstCommentText="")
        ig = {"type": "POST" if kind == "post" else "REEL", "isAiGenerated": False}
        if kind == "reel":
            ig.update(showReelOnFeed=True, audioConfiguration={"audioId": track_for(c), "audioVolume": 100, "videoVolume": 0})
        info["instagramData"] = ig
    else:
        info.update(text=c["fb"], firstCommentText=c["fb_comment"].format(link=C.link(c, "facebook", kind)))
        info["facebookData"] = {"type": "POST" if kind == "post" else "REEL"}
    return info


def plan(days=14, now=None):
    """Fill the open slots from now on with Reel scripts, in the order they appear in engine/reels_*.py.
    A Reel goes out once per network. A slot is open when nothing is logged for that network on that day."""
    from zoneinfo import ZoneInfo
    now = now or dt.datetime.now(ZoneInfo(TZ)).replace(tzinfo=None)  # slots are New York time; the runner may be on UTC
    log = read_log()
    done = {(p["id"], p["network"]) for p in log["posts"] if p["kind"] == "reel"}
    taken = {(p["network"], p["at"][:10]) for p in log["posts"]}
    queue = [r["id"] for r in R2.load() if reel_ready(r["id"])]
    out = []
    for d in range(days + 1):
        day = (now + dt.timedelta(days=d)).date()
        for network, kind, hhmm in SLOTS[day.weekday()]:
            at = f"{day.isoformat()}T{hhmm}"
            if at <= now.strftime("%Y-%m-%dT%H:%M") or (network, day.isoformat()) in taken:
                continue
            pick = next((cid for cid in queue if (cid, network) not in done), None)
            if pick:
                done.add((pick, network))
                taken.add((network, day.isoformat()))
            out.append((at, network, kind, pick))
    return out


def main(a):
    cmd = a[0] if a else "status"
    if cmd == "plan":
        for at, network, kind, cid in sorted(plan(int(a[1]) if len(a) > 1 else 14)):
            print(at, network.ljust(9), kind.ljust(4), cid or "EMPTY (write and render more Reels)")
    elif cmd == "date":
        from zoneinfo import ZoneInfo
        print(dt.datetime.fromisoformat(a[1]).replace(tzinfo=ZoneInfo(TZ)).isoformat())
    elif cmd == "payload":
        cid, network, kind, when = a[1:5]
        print(json.dumps(payload(cid, network, kind, when)))
    elif cmd == "logged":
        cid, network, kind, when, mid = a[1:6]
        uuid = a[6] if len(a) > 6 else ""
        log = read_log()
        if any(p["id"] == cid and p["network"] == network and p["kind"] == kind for p in log["posts"]):
            raise SystemExit(f"{cid} {network} {kind} is already logged")
        log["posts"].append(dict(id=cid, network=network, kind=kind, at=when, metricool_id=mid, uuid=uuid,
                                 logged=dt.datetime.now().strftime("%Y-%m-%dT%H:%M")))
        write_log(log)
        print("logged", cid, network, kind, when)
    elif cmd == "reid":
        uuid, mid = a[1:3]
        log = read_log()
        hits = [p for p in log["posts"] if p.get("uuid") == uuid]
        if len(hits) != 1:
            raise SystemExit(f"uuid {uuid}: {len(hits)} log entries")
        hits[0]["metricool_id"] = mid
        write_log(log)
        print("new id", hits[0]["id"], hits[0]["network"], hits[0]["kind"], mid)
    elif cmd == "status":
        log = read_log()
        for p in log["posts"]:
            print(p["at"], p["network"].ljust(9), p["kind"].ljust(4), p["id"], p["metricool_id"])
        print(len(log["posts"]), "posts logged")
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
