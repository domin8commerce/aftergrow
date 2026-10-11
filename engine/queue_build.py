"""Build the Aftergrow posting queue: copy for every pin, validated against the brand rules,
then sequenced strongest hook first so no board repeats inside any 3 pins in a row (3 pins a day).
Tailwind assigns the actual times (next open slot), so this file sets ORDER, not dates.
Usage (from the repo): python3 -I engine/queue_build.py <repo_root>"""
import csv, json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

U = "https://getaftergrow.com"
def L(path, camp, pid):
    return f"{U}{path}?utm_source=pinterest&utm_medium=social&utm_campaign={camp}&utm_content={pid}"

# Board names must match boards.json exactly.
HW, HC, SC, O40, HAB, CHK, PRD, PP = ("Hair shedding explained", "Hair care ingredients", "Scalp care routine",
    "Hair care tips for women over 40", "Healthy hair habits", "Hair progress photos", "Aftergrow Scalp Serum",
    "Postpartum hair care")
HIW, GUIDE, ING_P, CHK_P, PDP = "/pages/how-it-works", "/pages/month-three-guide", "/pages/ingredients", "/pages/the-check-in", "/products/scalp-serum"
# Pages verified live (real content) on 2026-10-11. A pin may only link to a page on this list.
LIVE_PAGES = {HIW, GUIDE, ING_P, CHK_P, PDP, "/blogs/journal/hair-serum-or-scalp-serum",
              "/blogs/journal/how-to-read-a-scalp-serum-label"}

# id, slug, board, title, description, link, alt
W1 = [
 ("A01", "why-hair-sheds-3-months-later", HW, "Why hair sheds 3 months after a big change: the timeline explained",
  "Hair shedding after a big change in the body often starts 2 to 4 months later. Here is the simple timeline: why it happens, how long it usually lasts and when to see a dermatologist. Save for later.",
  L(HIW, "shedding", "A01"), "Timeline infographic: hair shedding starts 2 to 4 months after a big change in the body and settles within 6 to 9 months for most people."),
 ("E02", "peptides-explained-simply", HC, "Peptides in scalp care, explained simply",
  "What are peptides in scalp care? Short chains of amino acids, used in skincare for years and now in scalp serums to condition the scalp and support the look of thicker hair. Plus how they appear on a label.",
  L(ING_P, "ingredients", "E02"), "Infographic explaining peptides as short chains of amino acids that condition the scalp, with example label names sh-Polypeptide and sh-Oligopeptide."),
 ("G02", "how-to-photograph-your-part", CHK, "How to photograph your part: 4 rules for a fair comparison",
  "How to photograph your part so you can compare fairly: same place, same part, same angle, same settings. Four rules that turn three photos into real evidence over 90 days.",
  L(CHK_P, "check-in", "G02"), "Illustration of a phone photographing a hair part from above, with four rules for consistent part photos and a week 0, 6 and 12 timeline."),
 ("A03", "shedding-when-to-see-a-dermatologist", HW, "Normal shedding vs. see a dermatologist: a simple checklist",
  "Not sure if your hair shedding is normal? This checklist shows the signs that mean it is time to see a dermatologist, and what usually passes on its own. Clear, calm and easy to save.",
  L(HIW, "shedding", "A03"), "Checklist of five signs that hair shedding needs a dermatologist: sudden heavy shedding, patches, scalp redness or pain, a widening part, shedding past 6 months."),
 ("E06", "fragrance-free-vs-unscented", HC, "Fragrance-free vs. unscented: the difference that matters for scalps",
  "Fragrance-free vs unscented: fragrance-free means no scent was added, while unscented products can contain a masking scent. Why it matters for a sensitive scalp, and the label words to check.",
  L(ING_P, "ingredients", "E06"), "Infographic comparing fragrance-free and unscented, with a tip to check labels for the words fragrance or parfum."),
 ("D04", "5-habits-to-retire-after-40", O40, "Hair care over 40: 5 things to stop doing",
  "Hair care over 40: five habits to retire and what to do instead, from tight ponytails and daily high heat to heavy oils on fine hair. Small swaps that help hair look fuller. Get the free guide.",
  L(GUIDE, "over-40", "D04"), "List of five hair habits to retire after 40, each crossed out with a gentler swap written below it."),
 ("A04", "hair-growth-cycle-3-stages", HW, "The hair growth cycle in 3 stages (and why shedding comes late)",
  "The hair growth cycle has three stages: growing for years, resting for about three months, then shedding. A big change pushes many hairs into resting at once, so the shed shows up months later.",
  L(HIW, "shedding", "A04"), "Cycle diagram of the three hair growth stages: growing for years, resting for about 3 months, shedding as a new hair starts."),
 ("B04", "5-gentle-habits-postpartum-hair", PP, "Postpartum hair: 5 gentle habits that help it look fuller",
  "Five gentle habits for postpartum hair shedding: loose styles, a wide-tooth comb, less heat, a clean scalp and patience. Small changes that help hair look fuller while the shed passes. Get the free guide.",
  L(GUIDE, "postpartum", "B04"), "Infographic listing five gentle postpartum hair habits on a butter-yellow background."),
 ("C01", "2-minute-scalp-care-routine", SC, "A 2-minute scalp care routine: part, drop, massage",
  "A two-minute scalp care routine you can keep: part dry hair, add a few drops of a lightweight scalp serum along the part, massage and leave it in. Once a day, no rinsing.",
  L(PDP, "scalp-care", "C01"), "Three-step scalp care routine: part clean dry hair, add a few drops along the part, massage for 1 to 2 minutes."),
 ("F01", "brush-shedding-hair-without-breakage", HAB, "How to brush shedding hair without breakage",
  "How to brush shedding hair without adding breakage: start at the ends and work up, use a wide-tooth comb on wet hair and soft bristles on dry hair. Four small habits that protect the hair you have.",
  L(GUIDE, "habits", "F01"), "Diagram of a hair strand showing brushing from the ends up to the roots, with four gentle brushing tips."),
]

B2 = [
 ("A02", "how-much-hair-shedding-is-normal", HW, "How much hair shedding is normal? 50 to 100 hairs a day explained",
  "How much hair shedding is normal? Most people lose 50 to 100 hairs a day. During a shed it is more, for a few months. What is normal, what is not, and why photos beat counting hairs.",
  L(HIW, "shedding", "A02"), "Infographic: losing 50 to 100 hairs a day is normal; during a shed it is more for a few months."),
 ("A05", "telogen-effluvium-plain-english", HW, "Telogen effluvium explained in plain English",
  "Telogen effluvium is the medical name for shedding that follows a big change in the body. What the words mean, why many hairs rest and then shed together 2 to 4 months later, and why it is usually temporary.",
  L(HIW, "shedding", "A05"), "Explainer card defining telogen as the resting phase and effluvium as an outflow, noting the shed is usually temporary."),
 ("A06", "shedding-after-stress-illness-surgery", HW, "Hair shedding after stress, illness or surgery: what is happening",
  "Hair shedding after stress, illness, surgery or a new baby is common and usually temporary. Why it arrives 2 to 4 months after the hard part, and when to get it checked. Get the free Month-Three Guide.",
  L(GUIDE, "shedding", "A06"), "Infographic on shedding after a hard season: many hairs rest at once, shed 2 to 4 months later, and it usually passes."),
 ("A07", "why-your-part-looks-wider", HW, "Why your part looks wider (and what it usually means)",
  "A wider part is often the first thing women notice during a shed. Why it happens, when it usually settles, when a widening part needs a dermatologist, and how to track it with one photo every 6 weeks.",
  L(CHK_P, "shedding", "A07"), "Infographic explaining why a part can look wider during a shed and when to see a dermatologist."),
 ("A08", "hair-shedding-timeline-month-by-month", HW, "Hair shedding timeline: what to expect month by month",
  "What does a hair shed look like month by month? It often starts 2 to 4 months after a big change and settles within 6 to 9 months for most people. A simple timeline to save, with the sign to get it checked.",
  L(HIW, "shedding", "A08"), "Month-by-month ruler showing hair shedding starting at months 2 to 4 and settling by months 6 to 9."),
 ("A10", "5-questions-for-your-dermatologist", HW, "What to ask a dermatologist about hair shedding: 5 questions",
  "Going to a dermatologist about hair shedding? Bring these five questions, plus your part photos and a short list of recent changes. A simple prep list you can save and screenshot.",
  L(GUIDE, "shedding", "A10"), "Checklist of five questions to ask a dermatologist about hair shedding."),
 ("B01", "postpartum-shedding-peaks-around-month-4", PP, "Postpartum hair shedding: why it peaks around month 4",
  "Postpartum hair shedding usually peaks about four months after birth. Why pregnancy hair sheds later, how long it tends to last, and why most women see it ease by the baby's first birthday.",
  L(HIW, "postpartum", "B01"), "Curve showing postpartum shedding rising after birth, peaking around month 4 and easing by the first birthday."),
 ("B02", "postpartum-shedding-normal-or-not", PP, "Postpartum hair shedding: what is normal and what is not",
  "Postpartum hair shedding checklist: what is normal in the fourth trimester and beyond, and the signs that mean you should see a dermatologist. Calm, clear and worth saving.",
  L(HIW, "postpartum", "B02"), "Two-column checklist of normal postpartum shedding signs and signs to see a dermatologist."),
 ("B07", "postpartum-hair-photo-habit-week-0-6-12", PP, "A photo habit for postpartum hair: week 0, week 6, week 12",
  "A simple photo habit for postpartum hair: one photo of your part at week 0, week 6 and week 12, taken the same way. It shows real change a mirror cannot. Same window, same part, same angle.",
  L(CHK_P, "postpartum", "B07"), "Three photo frames labeled week 0, week 6 and week 12 for tracking postpartum hair."),
 ("C03", "how-to-apply-scalp-serum-part-method", SC, "How to apply a scalp serum: the part method",
  "How to apply a scalp serum so it reaches the scalp, not the lengths: part, add a few drops, move the part an inch over and repeat, then massage and leave it in. The part method, step by step.",
  L(PDP, "scalp-care", "C03"), "Diagram of three hair parts with drops along each and three steps for applying a scalp serum."),
 ("C04", "scalp-care-vs-hair-care", SC, "Scalp care vs. hair care: what is the difference?",
  "Scalp care vs hair care: hair care works on the strand, scalp care works on the skin your hair grows from. What each one does, and how a simple scalp-first routine fits in. Think of it as skincare for your scalp.",
  L("/blogs/journal/hair-serum-or-scalp-serum", "scalp-care", "C04"), "Split card comparing hair care for the strand with scalp care for the skin hair grows from."),
 ("C07", "edited-scalp-care-shelf-4-things", SC, "The edited scalp care shelf: 4 things, not 14",
  "You do not need a 14-step routine. An edited scalp care shelf has four things: a gentle cleanser, a leave-on serum, a wide-tooth comb and a soft towel. Simple routines are the ones you keep.",
  L(PDP, "scalp-care", "C07"), "Four line icons for a simple scalp care shelf: cleanser, leave-on serum, wide-tooth comb and towel."),
 ("D01", "fuller-looking-hair-over-40-6-habits", O40, "Fuller-looking hair over 40: 6 small daily habits",
  "Fuller-looking hair over 40 comes from small daily habits: scalp care, a smarter part, root volume, less heat and loose styles. Six habits to save and start this week.",
  L(GUIDE, "over-40", "D01"), "List of six daily habits for fuller-looking hair over 40."),
 ("D05", "low-effort-hair-routine-over-40", O40, "A low-effort hair routine for busy women over 40",
  "A low-effort hair routine for busy women over 40: wash every two to three days, two minutes of scalp care daily, one gentle mask a week and a part photo every six weeks. Simple and realistic.",
  L(PDP, "over-40", "D05"), "Weekly schedule graphic: daily scalp care, washing every 2 to 3 days, a weekly mask and a part photo every 6 weeks."),
 ("D06", "judge-your-hair-by-photos-not-moods", O40, "The part photo: how to judge your hair honestly",
  "The honest way to judge thinning or fuller-looking hair is a part photo taken the same way each time. Four rules for a fair comparison you can repeat every six weeks.",
  L(CHK_P, "over-40", "D06"), "Four rules for taking a consistent part photo."),
 ("E01", "rosemary-for-hair-honestly", HC, "Rosemary for hair: what it actually does on the scalp",
  "Rosemary for hair is everywhere. What it actually does in a scalp serum: a familiar botanical that gives the scalp a fresh, cared-for feel. How it appears on a label, and the honest explanation without the hype.",
  L(ING_P, "ingredients", "E01"), "Ledger-style card about rosemary extract: its label name, what it does and where to find it."),
 ("E03", "eucalyptus-for-scalp-fresh-feel", HC, "Eucalyptus for the scalp: the fresh-feel ingredient",
  "Eucalyptus leaf extract gives a scalp serum a fresh, clean feel. How it appears on an ingredient label, why it pairs well with rosemary, and where you will find it in a simple scalp care routine.",
  L(ING_P, "ingredients", "E03"), "Ledger-style card about eucalyptus leaf extract and its role in scalp care."),
 ("E04", "4-plant-extracts-in-scalp-care", HC, "4 plant extracts in scalp care and what each one does",
  "Four plant extracts you will see in scalp serums: saw palmetto, scutellaria root, soybean germ and wheat germ. What each one does on the scalp, in plain English, plus the soy and wheat allergen note.",
  L(ING_P, "ingredients", "E04"), "Grid of four plant extracts and their roles in scalp care, with soy and wheat allergen notes."),
 ("E05", "how-to-read-a-scalp-serum-label", HC, "How to read a scalp serum label in 4 steps",
  "How to read a scalp serum label: water first means a water-based formula, ingredients above 1% run from most to least, under 1% can be in any order, and fragrance or parfum means scent was added.",
  L("/blogs/journal/how-to-read-a-scalp-serum-label", "ingredients", "E05"), "Diagram of an ingredient label with four numbered tips for reading a scalp serum label."),
 ("E07", "free-from-list-explained", HC, "What is not in it: the free-from list, explained",
  "What does free-from actually mean on a scalp serum? Parabens, sulfates, silicones, phthalates, mineral oil and added fragrance, each explained in one line, so you know what you are avoiding.",
  L(ING_P, "ingredients", "E07"), "Grid explaining six free-from claims: parabens, sulfates, silicones, phthalates, mineral oil and added fragrance."),
 ("F05", "heat-styling-during-a-shed", HAB, "Heat styling during a shed: gentler settings that still work",
  "Heat styling during a hair shed: medium heat, fewer passes, heat protectant every time and air-drying most of the way first. Gentler settings that protect fine hair and still get the look. Get the free guide.",
  L(GUIDE, "habits", "F05"), "List of four gentler heat styling tips for fine or shedding hair."),
 ("G03", "three-photo-method-week-0-6-12", CHK, "Week 0, week 6, week 12: the three-photo method for tracking hair",
  "The three-photo method: week 0 before you start, week 6 as a midpoint and week 12 to compare and decide. Hair changes slowly, so photos taken the same way are the fair judge.",
  L(CHK_P, "check-in", "G03"), "Timeline with three points labeled week 0, week 6 and week 12 for tracking hair with photos."),
 ("H02", "whats-inside-aftergrow-scalp-serum", PRD, "What is inside Aftergrow: five peptides, six plant extracts, no added fragrance",
  "What is inside Aftergrow Scalp Serum: five peptides, rosemary, eucalyptus, saw palmetto, scutellaria root, soybean and wheat germ in a light water-based serum. No added fragrance, nothing to swallow. Contains soy and wheat.",
  L(ING_P, "product", "H02"), "Ledger listing the peptides and plant extracts in Aftergrow Scalp Serum, with no fragrance and nothing to swallow."),
 ("H03", "the-90-day-protocol", PRD, "The 90-Day Protocol: three bottles, the Check-in and a money-back guarantee",
  "The 90-Day Protocol from Aftergrow: three bottles, check-in emails at weeks 0, 6 and 12, free shipping and a money-back guarantee on your first order. Refills every 3 months; skip or cancel anytime.",
  L(PDP, "product", "H03"), "Graphic of the 90-Day Protocol: three months, three bottles and check-in emails at weeks 0, 6 and 12."),
]

BANNED = ["weight loss", "lose weight", "diet", "slim", "before and after", "regrow", "stop hair loss", "prevent hair loss",
          "cure", "treat", "clinically proven", "miracle", "game-changer", "holy grail", "detox", "ozempic", "wegovy",
          "semaglutide", "glp", "—"]


BANNED += ["minoxidil", "finasteride", "rogaine", "propecia", "spironolactone", "dutasteride", "tirzepatide",
           "mounjaro", "zepbound", "liraglutide", "saxenda", "rybelsus", "zepbound", "weight-loss"]
CAPS_OK = {"AAD", "FAQ", "INCI"}
PAGE_CAP = 8  # at most this many pins per landing page until new pages exist (Tailwind: 3 to 5 designs per URL)


def banned_hits(text):
    hits = []
    for b in BANNED:
        pat = (r"\b" + re.escape(b)) if b[0].isalnum() else re.escape(b)
        if re.search(pat, text.lower()): hits.append(b)
    return hits


def style_hits(text, where):
    """Rules beyond the word list: no exclamation marks, no all-caps words, 'hair loss' only in descriptions."""
    hits = []
    if "!" in text: hits.append("exclamation mark")
    hits += [f"all caps '{w}'" for w in re.findall(r"\b[A-Z]{3,}\b", text) if w not in CAPS_OK]
    if where != "description" and "hair loss" in text.lower(): hits.append("'hair loss' outside a description")
    return hits


def image_text(pin):
    """Every piece of text a design puts on the image, without HTML."""
    out = []
    def walk(v):
        if isinstance(v, str): out.append(v)
        elif isinstance(v, (list, tuple)): [walk(x) for x in v]
        elif isinstance(v, dict): [walk(x) for x in v.values()]
    for k, v in pin.items():
        if k not in ("id", "slug", "field", "arch", "brand_on"):
            walk(v)
    text = " ".join(out)
    text = re.sub(r"<[^>]+>", " ", text).replace("&nbsp;", " ").replace("&amp;", "&")
    return re.sub(r"\s+", " ", text)


def validate(rows, board_names, pins_dir=None, designs=()):
    probs = []
    for pid, slug, board, title, desc, url, alt in rows:
        if len(title) > 100: probs.append(f"{pid} title {len(title)}")
        if not 150 <= len(desc) <= 280: probs.append(f"{pid} desc {len(desc)}")
        if len(alt) > 500: probs.append(f"{pid} alt")
        for f, where in ((title, "title"), (desc, "description"), (alt, "alt")):
            probs += [f"{pid} {where}: banned '{b}'" for b in banned_hits(f)]
            probs += [f"{pid} {where}: {h}" for h in style_hits(f, where)]
        if f"utm_content={pid}" not in url: probs.append(f"{pid} utm")
        path = url.split("?")[0].replace(U, "")
        if path not in LIVE_PAGES: probs.append(f"{pid} links to unverified page {path}")
        if board not in board_names: probs.append(f"{pid} board '{board}' not in boards.json")
        if pins_dir and not (pins_dir / f"aftergrow_pin_{pid}_{slug}_v1.png").exists():
            probs.append(f"{pid} image missing")
    for d in designs:
        t = image_text(d)
        probs += [f"{d['id']} image text: banned '{b}'" for b in banned_hits(t)]
        probs += [f"{d['id']} image text: {h}" for h in style_hits(t, "image")]
    per_page = {}
    for r in rows:
        p = r[5].split("?")[0].replace(U, "")
        per_page[p] = per_page.get(p, 0) + 1
    probs += [f"{p} has {n} pins; cap is {PAGE_CAP} until new pages exist" for p, n in per_page.items() if n > PAGE_CAP]
    return probs


# Strongest hooks first: search demand evidence, then how saveable the format is, then brand fit.
PRIORITY = ["A01", "C01", "B01", "A02", "E01", "D04", "A04", "B04", "E02", "A03", "C04", "F01",
            "A08", "G02", "E06", "D01", "H02", "A05", "B02", "C03", "E05", "A06", "F05", "D05",
            "E03", "A07", "G03", "C07", "E04", "B07", "A10", "H03", "D06", "E07"]


def sequence(rows, fields, window=3, lookahead=4, prefix=()):
    """Order pins so no board repeats inside any `window` consecutive pins (so never twice in a day
    at 3 a day, wherever the day boundary falls). Prefer, but do not force: a different landing page
    and a different background color from the pin before. `prefix` = rows already scheduled, so the
    first new pins also avoid the boards of the last scheduled ones."""
    by_id = {r[0]: r for r in list(rows) + list(prefix)}
    left = [p for p in PRIORITY if p in {r[0] for r in rows}] + [r[0] for r in rows if r[0] not in PRIORITY]
    out = [r[0] for r in prefix][-(window - 1):]
    start, warnings = len(out), []
    while left:
        recent = out[-(window - 1):]
        ok = [p for p in left if by_id[p][2] not in {by_id[q][2] for q in recent}]
        if not ok:  # only one board left: place it anyway and say so
            warnings.append(f"{left[0]} repeats its board within {window} pins (too many pins on one board)")
            ok = [left[0]]
        def soft(p):
            prev = out[-1] if out else None
            same_page = any(by_id[p][5].split("?")[0] == by_id[q][5].split("?")[0] for q in recent)
            same_field = prev is not None and fields.get(p) == fields.get(prev)
            return same_page or same_field
        # A board with c pins left needs (c - 1) * window + 1 slots to stay spaced out.
        # If that is all the slots left, it has to go now or it will bunch up at the end.
        count = {}
        for p in left:
            count[by_id[p][2]] = count.get(by_id[p][2], 0) + 1
        critical = [p for p in ok if (count[by_id[p][2]] - 1) * window + 1 >= len(left)]
        pick = critical[0] if critical else next((p for p in ok[:lookahead] if not soft(p)), ok[0])
        out.append(pick)
        left.remove(pick)
    return out[start:], warnings


def load_batches():
    """Week 1 + batch 2 copy lives in this file. Every later batch is engine/batchN.py (N >= 3)
    with PINS (designs, same format as batch2.PINS) and COPY (rows in the same format as B2)."""
    import importlib, pinengine, batch2
    pins, rows = list(pinengine.PINS) + list(batch2.PINS), list(W1) + list(B2)
    for f in sorted(ROOT.glob("batch*.py"), key=lambda p: int(re.sub(r"\D", "", p.stem) or 0)):
        if int(re.sub(r"\D", "", f.stem) or 0) >= 3:
            m = importlib.import_module(f.stem)
            pins += list(m.PINS)
            rows += list(m.COPY)
    return pins, rows


def build(repo):
    pins, rows = load_batches()
    fields = {p["id"]: p["field"] for p in pins}
    boards = json.loads((repo / "boards.json").read_text())
    board_id = {b["name"]: b["tailwind_board_id"] for b in boards}
    probs = validate(rows, set(board_id), repo / "pins", designs=pins)
    ids = [r[0] for r in rows]
    probs += [f"duplicate id {i}" for i in sorted({i for i in ids if ids.count(i) > 1})]
    probs += [f"{p['id']} has a design but no copy" for p in pins if p["id"] not in ids]
    old = {}
    if (repo / "queue.json").exists():
        old = {r["id"]: r for r in json.loads((repo / "queue.json").read_text())}
    # Scheduled and posted pins keep their place; only ready pins are (re)sequenced behind them.
    kept = sorted((r for r in rows if old.get(r[0], {}).get("status") in ("scheduled", "posted")),
                  key=lambda r: old[r[0]].get("order", 0))
    ready = [r for r in rows if r not in kept]
    seq, warnings = sequence(ready, fields, prefix=kept)
    for w in warnings:
        print("warning:", w)
    order = [r[0] for r in kept] + seq
    by_id = {r[0]: r for r in rows}
    q = []
    for n, pid in enumerate(order, 1):
        _, slug, board, title, desc, link, alt = by_id[pid]
        row = dict(order=n, id=pid, image=f"aftergrow_pin_{pid}_{slug}_v1.png", board=board, board_id=board_id[board],
                   title=title, description=desc, link=link, alt_text=alt, field=fields.get(pid), status="ready")
        prev = old.get(pid, {})
        if prev.get("status") in ("scheduled", "posted"):
            for k in ("status", "post_id", "send_at_utc", "role", "pinterest_pin_id"):
                if k in prev: row[k] = prev[k]
        if prev.get("history"): row["history"] = prev["history"]
        q.append(row)
    return q, probs


if __name__ == "__main__":
    repo = pathlib.Path(sys.argv[1]).resolve()
    q, probs = build(repo)
    print("problems:", probs or "none")
    ready = [r for r in q if r["status"] == "ready"]
    print(f"{len(q)} pins: {len(q) - len(ready)} scheduled or posted, {len(ready)} ready. Ready, in order, 3 a day:")
    for i in range(0, len(ready), 3):
        print(f"  day {i // 3 + 1:>2}: " + " | ".join(f"{r['id']} {r['board'][:18]:<18}" for r in ready[i:i + 3]))
    if probs:
        raise SystemExit("fix the problems above; queue.json not written")
    (repo / "queue.json").write_text(json.dumps(q, indent=1, ensure_ascii=False) + "\n")
    with open(repo / "queue.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Order", "Pin", "Image file", "Board", "Pin title", "Description", "Link", "Alt text", "Status"])
        for r in q:
            w.writerow([r["order"], r["id"], r["image"], r["board"], r["title"], r["description"], r["link"],
                        r["alt_text"], r["status"]])
    print(len(q), "pins | boards:", len({r["board"] for r in q}))
