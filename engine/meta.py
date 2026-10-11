"""Aftergrow on Instagram and Facebook: the posting plan, Metricool payloads and the posting log.

Every carousel goes out twice on each network: first as a carousel (built for saves and shares), then a few
days later as a Reel with music (built for reach to people who don't follow us yet).

Usage (from the repo root):
  python3 -I engine/meta.py plan [days]          the open slots in the next N days (default 14) and what goes in each
  python3 -I engine/meta.py payload <ID> <instagram|facebook> <post|reel> <YYYY-MM-DDTHH:MM>
                                                  prints the "info" JSON for Metricool's createScheduledPost
  python3 -I engine/meta.py logged <ID> <instagram|facebook> <post|reel> <YYYY-MM-DDTHH:MM> <metricool id>
                                                  records a post Metricool accepted (do this right after each one)
  python3 -I engine/meta.py status               what is logged so far

Metricool: blogId 7369576, timezone America/New_York. Times in this file are New York time.
"""
import datetime as dt, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
sys.path.insert(0, str(ROOT))
import carousel as C  # noqa: E402

BLOG_ID = "7369576"
TZ = "America/New_York"
LOG = REPO / "meta_log.json"
NETWORKS = ("instagram", "facebook")
KINDS = ("post", "reel")

# Weekly slots, New York time. Monday is 0. Facebook times follow Metricool's audience curve for our Page
# (peak at 10:00 on weekdays, Wednesday 12:00 the highest, Sunday 18:00 the evening peak). Instagram has no
# data yet, so it tests a midday window (carousels) against an evening window (Reels) until it does.
SLOTS = {
    0: [("facebook", "post", "09:52"), ("instagram", "post", "11:47")],
    1: [("facebook", "reel", "09:52"), ("instagram", "reel", "19:17")],
    2: [("facebook", "post", "11:52"), ("instagram", "post", "11:47")],
    3: [("facebook", "reel", "09:52"), ("instagram", "reel", "19:17")],
    4: [("facebook", "post", "09:52"), ("instagram", "post", "11:47")],
    5: [("facebook", "reel", "09:52"), ("instagram", "reel", "10:47")],
    6: [("facebook", "post", "17:52"), ("instagram", "post", "19:17")],
}
REEL_MIN_GAP_DAYS = 2  # a Reel goes out at least this many days after its carousel on the same network


def read_log():
    return json.loads(LOG.read_text()) if LOG.exists() else {"posts": []}


def write_log(log):
    LOG.write_text(json.dumps(log, indent=1) + "\n")


def reel_url(cid):
    return f"{C.RAW}reels/{cid}.mp4"


def reel_ready(c):
    return (REPO / "reels" / f"{c['id']}.mp4").exists() and bool(c.get("audio"))


def payload(cid, network, kind, when):
    """The createScheduledPost "info" object for one carousel on one network."""
    assert network in NETWORKS and kind in KINDS, (network, kind)
    c = {x["id"]: x for x in C.load()}[cid]
    info = dict(autoPublish=True, draft=False, shortener=False, smartLinkData={"ids": []},
                providers=[{"network": network}], publicationDate={"dateTime": when + ":00", "timezone": TZ})
    if kind == "post":
        info.update(media=C.media_urls(c), mediaAltText=C.alt_texts(c))
    else:
        if not reel_ready(c):
            raise SystemExit(f"{cid}: no Reel yet (reels/{cid}.mp4 and an 'audio' id are both needed)")
        info.update(media=[reel_url(cid)], videoThumbnailUrl=C.media_urls(c)[0])
    if network == "instagram":
        info.update(text=C.ig_text(c), firstCommentText="")
        ig = {"type": "POST" if kind == "post" else "REEL", "isAiGenerated": False}
        if kind == "reel":
            ig.update(showReelOnFeed=True, audioConfiguration={"audioId": str(c["audio"]), "audioVolume": 100, "videoVolume": 0})
        info["instagramData"] = ig
    else:
        info.update(text=c["fb"], firstCommentText=c["fb_comment"].format(link=C.link(c, "facebook")))
        info["facebookData"] = {"type": "POST" if kind == "post" else "REEL"}
    return info


def plan(days=14, now=None):
    """Fill the open slots from tomorrow on: carousels in ID order, then each one's Reel two or more days later."""
    now = now or dt.datetime.now()
    log = read_log()
    done = {(p["id"], p["network"], p["kind"]): p["at"] for p in log["posts"]}
    taken = {(p["network"], p["at"][:10]) for p in log["posts"]}
    cars = [c for c in C.load()]
    out = []
    for d in range(days + 1):
        day = (now + dt.timedelta(days=d)).date()
        for network, kind, hhmm in SLOTS[day.weekday()]:
            at = f"{day.isoformat()}T{hhmm}"
            if at <= now.strftime("%Y-%m-%dT%H:%M") or (network, day.isoformat()) in taken:
                continue
            pick = None
            for c in cars:
                key = (c["id"], network, kind)
                if key in done:
                    continue
                if kind == "post":
                    pick = c
                    break
                posted = done.get((c["id"], network, "post"))
                if posted and reel_ready(c) and dt.date.fromisoformat(posted[:10]) + dt.timedelta(days=REEL_MIN_GAP_DAYS) <= day:
                    pick = c
                    break
            if pick:
                done[(pick["id"], network, kind)] = at
                taken.add((network, day.isoformat()))
                out.append((at, network, kind, pick["id"]))
            else:
                out.append((at, network, kind, None))
    return out


def main(a):
    cmd = a[0] if a else "status"
    if cmd == "plan":
        for at, network, kind, cid in plan(int(a[1]) if len(a) > 1 else 14):
            print(at, network.ljust(9), kind.ljust(4), cid or "EMPTY (make more carousels or Reels)")
    elif cmd == "payload":
        cid, network, kind, when = a[1:5]
        print(json.dumps(payload(cid, network, kind, when)))
    elif cmd == "logged":
        cid, network, kind, when, mid = a[1:6]
        log = read_log()
        if any(p["id"] == cid and p["network"] == network and p["kind"] == kind for p in log["posts"]):
            raise SystemExit(f"{cid} {network} {kind} is already logged")
        log["posts"].append(dict(id=cid, network=network, kind=kind, at=when, metricool_id=mid,
                                 logged=dt.datetime.now().strftime("%Y-%m-%dT%H:%M")))
        log["posts"].sort(key=lambda p: p["at"])
        write_log(log)
        print("logged", cid, network, kind, when)
    elif cmd == "status":
        log = read_log()
        for p in log["posts"]:
            print(p["at"], p["network"].ljust(9), p["kind"].ljust(4), p["id"], p["metricool_id"])
        print(len(log["posts"]), "posts logged")
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
