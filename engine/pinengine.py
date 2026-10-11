"""Aftergrow Pinterest pin engine, v2.

A pin = field (color scheme) + headline (+ optional deck) + one archetype body.
Real brand type (Schibsted Grotesk), exact hex colors, The Part symbol, rendered
by headless Chromium at 2000 x 3000 (2:3, double resolution for sharp text).

Usage: python3 -I pinengine.py <out_dir> [ID ...]
"""
import base64, math, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent
FONTS = ROOT / "node_modules/@fontsource/schibsted-grotesk/files"

ESP, BUT, WHI, POR = "#33241D", "#F3E2A0", "#FFFFFF", "#F4F5F1"
STO, SAN, SIL = "#675E58", "#D9CCBF", "#D5D6D1"

FIELDS = {  # bg, text, head, sub, mark, rule
    "butter": (BUT, ESP, ESP, STO, ESP, "rgba(51,36,29,.30)"),
    "espresso": (ESP, WHI, BUT, SAN, BUT, "rgba(217,204,191,.30)"),
    "white": (WHI, ESP, ESP, STO, ESP, SIL),
    "porcelain": (POR, ESP, ESP, STO, ESP, SIL),
}

PART = "M37.78 5.65 A46 46 0 1 1 32.78 7.34 L32.78 69.50 A2.50 2.50 0 0 0 37.78 69.50 Z"


def part(size, color):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 100 100"><path d="{PART}" fill="{color}"/></svg>'


_FONT_CSS = None


def font_css():
    global _FONT_CSS
    if _FONT_CSS is None:
        parts = []
        for w in (400, 500, 600, 700):
            b = base64.b64encode((FONTS / f"schibsted-grotesk-latin-{w}-normal.woff2").read_bytes()).decode()
            parts.append(f"@font-face{{font-family:'SG';font-weight:{w};font-style:normal;"
                         f"src:url(data:font/woff2;base64,{b}) format('woff2');}}")
        _FONT_CSS = "\n".join(parts)
    return _FONT_CSS


BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1000px;height:1500px}
body{font-family:'SG','Helvetica Neue',Arial,sans-serif;-webkit-font-smoothing:antialiased;
     font-kerning:normal;text-rendering:geometricPrecision}
.pin{position:relative;width:1000px;height:1500px;overflow:hidden;background:var(--bg);color:var(--fg);padding:92px 80px 0}
.h1{position:relative;z-index:2;font-weight:600;letter-spacing:-0.036em;line-height:.96;color:var(--head)}
.deck{position:relative;z-index:2;font-weight:600;letter-spacing:-0.022em;line-height:1.05;color:var(--sub);margin-top:20px}
.lead{font-weight:600;letter-spacing:-0.02em;line-height:1.1}
.copy{font-weight:400;line-height:1.28;letter-spacing:-0.004em}
.sub{color:var(--sub)}
.tnum{font-variant-numeric:tabular-nums lining-nums}
.brand{position:absolute;z-index:3;left:80px;bottom:58px;display:flex;align-items:center;gap:14px;
       font-weight:500;font-size:28px;letter-spacing:-0.01em}
"""


def page(p, head_html, body_html, css):
    bg, fg, head, sub, mark, rule = FIELDS[p["field"]]
    bf = FIELDS[p.get("brand_on", p["field"])]
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{font_css()}{BASE_CSS}{css}</style></head><body>
<div class="pin" style="--bg:{bg};--fg:{fg};--head:{head};--sub:{sub};--mark:{mark};--rule:{rule}">
{head_html}{body_html}
<div class="brand" style="color:{bf[3]};left:{p.get('brand_left', 80)}px">{part(44, bf[4])}<span>getaftergrow.com</span></div>
</div></body></html>"""


# ------------------------------------------------------------------ archetypes

def a_timeline(p):
    rows = "".join(
        f"""<div class="row"><div class="when"><span class="unit">{r['unit']}</span>
        <span class="num tnum">{r['num']}</span></div><div class="dot{' on' if r.get('on') else ''}"></div>
        <div class="what"><p class="lead">{r['lead']}</p><p class="copy">{r['copy']}</p></div></div>"""
        for r in p["rows"])
    body = f"""<div class="tl"><div class="spine"></div>{rows}</div><p class="note">{p['note']}</p>"""
    css = """
.tl{position:relative;margin-top:74px}
.tl .spine{position:absolute;left:258px;top:56px;bottom:120px;width:5px;background:var(--fg)}
.tl .row{display:grid;grid-template-columns:220px 76px 1fr;align-items:start;min-height:244px}
.tl .when{text-align:right}
.tl .num{display:block;font-weight:600;font-size:122px;line-height:.86;letter-spacing:-0.05em}
.tl .unit{display:block;font-size:30px;font-weight:500;color:var(--sub);margin-bottom:12px}
.tl .dot{width:36px;height:36px;border-radius:50%;background:var(--bg);border:6px solid var(--fg);
         justify-self:center;margin-top:52px;position:relative;z-index:1}
.tl .dot.on{background:var(--fg)}
.tl .what{padding-top:36px}
.tl .what .lead{font-size:48px}
.tl .what .copy{font-size:34px;margin-top:12px;max-width:540px}
.note{position:absolute;left:80px;right:80px;bottom:146px;font-size:33px;font-weight:600;line-height:1.28;
      letter-spacing:-0.01em;border-top:5px solid var(--fg);padding-top:22px}
"""
    return body, css


def a_ledger(p):
    n, x0, x1 = 9, 28, 812
    pts = [(x0 + (x1 - x0) * i / (n - 1), 64 + 30 * math.sin(i * 0.95)) for i in range(n)]
    els = [f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{BUT}" stroke-width="6"/>'
           for a, b in zip(pts, pts[1:])]
    els += [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="26" fill="{BUT if i % 3 == 1 else ESP}" stroke="{BUT}" stroke-width="6"/>'
            for i, (x, y) in enumerate(pts)]
    svg = f'<svg class="chain" width="840" height="128" viewBox="0 0 840 128">{"".join(els)}</svg>'
    rows = "".join(f'<div class="lrow"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in p["rows"])
    body = f"""{svg}<div class="ledger">{rows}</div>"""
    css = """
.chain{display:block;margin:52px 0 30px}
.ledger{border-bottom:2px solid var(--rule)}
.lrow{display:grid;grid-template-columns:236px 1fr;gap:16px;border-top:2px solid var(--rule);padding:28px 0 30px}
.lrow .k{font-size:31px;font-weight:500;color:var(--sub);padding-top:7px;line-height:1.2}
.lrow .v{font-size:45px;font-weight:500;line-height:1.16;letter-spacing:-0.016em}
.lrow .v .label{font-weight:600;color:var(--head)}
"""
    return body, css


def a_viewfinder(p):
    L, T, W, H, s = 34, 74, 212, 320, 34
    corners = "".join(
        f'<path d="M{cx} {cy + dy * s} L{cx} {cy} L{cx + dx * s} {cy}" fill="none" stroke="{ESP}" '
        f'stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
        for cx, cy, dx, dy in ((L, T, 1, 1), (L + W, T, -1, 1), (L, T + H, 1, -1), (L + W, T + H, -1, -1)))
    grid = ""
    for i in (1, 2):
        gx, gy = L + W * i / 3, T + H * i / 3
        grid += (f'<line x1="{gx:.1f}" y1="{T}" x2="{gx:.1f}" y2="{T + H}" stroke="{ESP}" stroke-opacity=".18" stroke-width="2"/>'
                 f'<line x1="{L}" y1="{gy:.1f}" x2="{L + W}" y2="{gy:.1f}" stroke="{ESP}" stroke-opacity=".18" stroke-width="2"/>')
    ps = 156
    sym = (f'<g transform="translate({L + W / 2 - ps / 2:.1f},{T + H / 2 - ps / 2:.1f}) scale({ps / 100})">'
           f'<path d="{PART}" fill="{ESP}"/></g>')
    shutter = f'<circle cx="{L + W / 2}" cy="{T + H + 58}" r="26" fill="none" stroke="{ESP}" stroke-width="7"/>'
    screen = (f'<svg width="280" height="500" viewBox="0 0 280 500"><rect width="280" height="500" rx="44" fill="{BUT}"/>'
              f'<rect x="102" y="22" width="76" height="16" rx="8" fill="{ESP}"/>{grid}{corners}{sym}{shutter}</svg>')
    rules = "".join(f'<div class="rule"><p class="lead">{a}</p><p class="copy sub">{b}</p></div>' for a, b in p["rules"])
    ticks = f"""<svg width="840" height="56" viewBox="0 0 840 56">
      <line x1="6" y1="28" x2="834" y2="28" stroke="{ESP}" stroke-width="6"/>
      <line x1="6" y1="6" x2="6" y2="50" stroke="{ESP}" stroke-width="8" stroke-linecap="round"/>
      <line x1="420" y1="6" x2="420" y2="50" stroke="{ESP}" stroke-width="8" stroke-linecap="round"/>
      <line x1="834" y1="6" x2="834" y2="50" stroke="{ESP}" stroke-width="8" stroke-linecap="round"/></svg>"""
    body = f"""<div class="vf"><div class="phone">{screen}</div><div class="rules">{rules}</div></div>
    <div class="weeks"><p class="wcap">{p['weeks_caption']}</p>{ticks}
    <div class="wl tnum"><span>Week 0</span><span>Week 6</span><span>Week 12</span></div></div>"""
    css = """
.vf{display:grid;grid-template-columns:300px 1fr;gap:48px;margin-top:62px;align-items:start}
.phone{width:300px;height:520px;border:10px solid #33241D;border-radius:54px;display:flex;align-items:center;
       justify-content:center;background:#33241D}
.rules{display:flex;flex-direction:column;gap:22px}
.rule .lead{font-size:46px}
.rule .copy{font-size:31px;margin-top:6px}
.weeks{position:absolute;left:80px;right:80px;bottom:146px}
.wcap{font-size:33px;font-weight:600;letter-spacing:-0.012em;margin-bottom:16px}
.wl{display:flex;justify-content:space-between;font-size:32px;font-weight:600;margin-top:10px;letter-spacing:-0.01em}
"""
    return body, css


def a_checklist(p):
    items = "".join(f'<li><span class="box"></span><span>{t}</span></li>' for t in p["items"])
    body = f"""<ul class="checks">{items}</ul><p class="note">{p['note']}</p>"""
    css = """
.checks{list-style:none;margin-top:84px;display:flex;flex-direction:column;gap:46px}
.checks li{display:grid;grid-template-columns:60px 1fr;gap:32px;align-items:start;font-size:53px;font-weight:500;
           line-height:1.1;letter-spacing:-0.02em}
.checks .box{width:58px;height:58px;border:6px solid var(--mark);border-radius:10px;margin-top:0}
.note{position:absolute;left:80px;right:80px;bottom:146px;font-size:33px;font-weight:500;line-height:1.3;
      color:var(--sub);border-top:3px solid var(--rule);padding-top:24px}
"""
    return body, css


def a_contrast(p):
    defs = "".join(f'<div class="def"><p class="term">{t}</p><p class="copy">{d}</p></div>' for t, d in p["defs"])
    body = f"""<div class="defs">{defs}</div><div class="band"><p class="tip">{p['tip']}</p></div>"""
    css = """
.defs{margin-top:60px;border-top:6px solid var(--fg)}
.def{padding:30px 0 32px;border-bottom:2px solid var(--rule)}
.def .term{font-size:56px;font-weight:600;letter-spacing:-0.026em;line-height:1.04}
.def .copy{font-size:39px;margin-top:10px;line-height:1.22}
.band{position:absolute;left:0;right:0;bottom:0;height:316px;background:#33241D;padding:60px 80px 0}
.tip{font-size:52px;font-weight:600;letter-spacing:-0.024em;line-height:1.1;color:#F3E2A0}
"""
    return body, css


def a_swap(p):
    rows = "".join(f'<li><p class="old">{o}</p><p class="new">{n}</p></li>' for o, n in p["rows"])
    body = f"""<div class="topband"></div><ul class="swaps">{rows}</ul>"""
    css = """
.topband{position:absolute;z-index:1;left:0;right:0;top:0;height:%dpx;background:#F3E2A0}
.swaps{list-style:none;position:relative;z-index:2;margin-top:%dpx;display:flex;flex-direction:column;gap:46px}
.swaps .old{font-size:37px;font-weight:500;color:#675E58;text-decoration:line-through;text-decoration-thickness:4px;
            text-decoration-color:#33241D;letter-spacing:-0.012em}
.swaps .new{font-size:52px;font-weight:600;letter-spacing:-0.024em;margin-top:6px;line-height:1.08}
""" % (p["band_h"], p["list_top"])
    return body, css


def a_cycle(p):
    cx, cy, r, nr = 460, 360, 250, 68
    angles = (-90, 30, 150)
    els = []
    els.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ESP}" stroke-width="6"/>')
    for a in (-30, 90, 210):
        t = math.radians(a)
        x, y = cx + r * math.cos(t), cy + r * math.sin(t)
        els.append(f'<g transform="translate({x:.1f},{y:.1f}) rotate({a + 90})"><path d="M-17 -19 L11 0 L-17 19" '
                   f'fill="none" stroke="{ESP}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></g>')
    for i, ((label, sub, style), a) in enumerate(zip(p["nodes"], angles)):
        t = math.radians(a)
        x, y = cx + r * math.cos(t), cy + r * math.sin(t)
        fill, numc = {"solid": (ESP, BUT), "butter": (BUT, ESP), "hollow": (POR, ESP)}[style]
        els.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{nr}" fill="{fill}" stroke="{ESP}" stroke-width="7"/>')
        els.append(f'<text x="{x:.1f}" y="{y + 20:.1f}" text-anchor="middle" font-family="SG" font-weight="600" '
                   f'font-size="58" fill="{numc}">{i + 1}</text>')
    svg = f'<svg width="920" height="720" viewBox="0 0 920 720" class="cyc">{"".join(els)}</svg>'
    pos = [(642, 66, "left"), (cx + r * math.cos(math.radians(30)), 578, "center"),
           (cx + r * math.cos(math.radians(150)), 578, "center")]
    labels = "".join(
        f'<div class="nl" style="left:{lx:.0f}px;top:{ly}px;text-align:{al};{"transform:translateX(-50%);" if al == "center" else ""}">'
        f'<p class="lead">{lab}</p><p class="copy sub">{sub}</p></div>'
        for (lab, sub, _), (lx, ly, al) in zip(p["nodes"], pos))
    body = f"""<div class="cwrap">{svg}{labels}</div><p class="note">{p['note']}</p>"""
    css = """
.cwrap{position:relative;margin-top:36px;height:720px}
.cyc{position:absolute;left:0;top:0}
.nl{position:absolute;white-space:nowrap}
.nl .lead{font-size:48px}
.nl .copy{font-size:33px;margin-top:6px}
.note{position:absolute;left:80px;right:80px;bottom:146px;font-size:34px;font-weight:600;line-height:1.26;
      letter-spacing:-0.012em;border-top:5px solid var(--fg);padding-top:22px}
"""
    return body, css


def a_list(p):
    items = "".join(f'<li><span class="m"></span><span>{t}</span></li>' for t in p["items"])
    body = f"""<ul class="dl">{items}</ul><p class="note">{p['note']}</p>"""
    css = """
.dl{list-style:none;margin-top:96px;display:flex;flex-direction:column;gap:60px}
.dl li{display:grid;grid-template-columns:30px 1fr;gap:30px;align-items:start;font-size:52px;font-weight:500;
       line-height:1.1;letter-spacing:-0.02em}
.dl .m{width:24px;height:24px;border-radius:50%;background:var(--fg);margin-top:18px}
.note{position:absolute;left:80px;right:80px;bottom:146px;font-size:36px;font-weight:600;line-height:1.24;
      letter-spacing:-0.014em;border-top:5px solid var(--fg);padding-top:22px}
"""
    return body, css


def a_steps(p):
    rows = "".join(f'<div class="st"><span class="n tnum">{i + 1}</span><div><p class="lead">{a}</p>'
                   f'<p class="copy sub">{b}</p></div></div>' for i, (a, b) in enumerate(p["steps"]))
    body = f"""<div class="steps">{rows}</div><p class="foot">{p['foot']}</p>"""
    css = """
.steps{margin-top:72px;display:flex;flex-direction:column;gap:40px}
.st{display:grid;grid-template-columns:150px 1fr;gap:28px;align-items:start;padding-top:32px;border-top:2px solid var(--rule)}
.st .n{font-size:172px;font-weight:600;line-height:.78;letter-spacing:-0.05em;color:var(--head)}
.st .lead{font-size:50px}
.st .copy{font-size:35px;margin-top:10px}
.foot{position:absolute;left:80px;right:80px;bottom:146px;font-size:50px;font-weight:600;letter-spacing:-0.024em;
      color:var(--head)}
"""
    return body, css


def a_strand(p):
    # Butter panel on the left (its edge sits on the 34% line), strand diagram inside, tips on the right.
    top, bot = 520, 1300
    h = bot - top
    els = [f'<path d="M110 20 C 128 {h * .25:.0f}, 92 {h * .5:.0f}, 112 {h * .72:.0f} S 120 {h - 60:.0f}, 110 {h - 20}" '
           f'fill="none" stroke="{ESP}" stroke-width="7" stroke-linecap="round"/>']
    ys = [h - 80, h / 2, 80]
    for (num, label), y in zip(p["points"], ys):
        els.append(f'<circle cx="112" cy="{y:.0f}" r="44" fill="{WHI}" stroke="{ESP}" stroke-width="7"/>')
        els.append(f'<text x="112" y="{y + 17:.0f}" text-anchor="middle" font-family="SG" font-weight="600" '
                   f'font-size="48" fill="{ESP}">{num}</text>')
    svg = f'<svg width="260" height="{h}" viewBox="0 0 260 {h}">{"".join(els)}</svg>'
    lab = "".join(f'<p class="pl" style="top:{top + y - 20:.0f}px">{label}</p>' for (_, label), y in zip(p["points"], ys))
    tips = "".join(f'<div class="tip"><p class="lead">{a}</p><p class="copy sub">{b}</p></div>' for a, b in p["tips"])
    body = f"""<div class="panel"></div><div class="sv" style="top:{top}px">{svg}</div>{lab}
    <div class="tips" style="top:{top + 10}px">{tips}</div>"""
    css = """
.panel{position:absolute;z-index:0;left:0;top:470px;bottom:0;width:372px;background:#F3E2A0}
.sv{position:absolute;z-index:1;left:44px}
.pl{position:absolute;z-index:1;left:214px;font-size:30px;font-weight:600;color:#33241D;letter-spacing:-0.01em;
    width:140px;line-height:1.05}
.tips{position:absolute;left:424px;right:72px;display:flex;flex-direction:column;gap:46px}
.tip .lead{font-size:47px}
.tip .copy{font-size:33px;margin-top:8px}
"""
    return body, css


ARCH = dict(timeline=a_timeline, ledger=a_ledger, viewfinder=a_viewfinder, checklist=a_checklist,
            contrast=a_contrast, swap=a_swap, cycle=a_cycle, list=a_list, steps=a_steps, strand=a_strand)


def build(p):
    body, css = ARCH[p["arch"]](p)
    head = f'<h1 class="h1" style="font-size:{p["h_size"]}px">{p["headline"]}</h1>'
    if p.get("deck"):
        head += f'<p class="deck" style="font-size:{p.get("deck_size", 50)}px">{p["deck"]}</p>'
    return page(p, head, body, css)


# ------------------------------------------------------------------ Week 1
PINS = [
    dict(id="A01", slug="why-hair-sheds-3-months-later", field="butter", arch="timeline", h_size=114,
         headline="Why your hair<br>sheds 3 months<br>later.",
         rows=[dict(unit="Month", num="0", lead="A big change<br>in the body.",
                    copy="After a baby, illness, surgery or stress, many hairs switch to resting at once."),
               dict(unit="Months", num="2–4", on=True, lead="The resting hairs shed.",
                    copy="More hair in the brush<br>and the shower."),
               dict(unit="Months", num="6–9", lead="It settles.", copy="For most people, on its own.")],
         note="Still heavy after 6 months, or patchy?<br>See a dermatologist."),
    dict(id="E02", slug="peptides-explained-simply", field="espresso", arch="ledger", h_size=126,
         headline="Peptides,<br>explained<br>simply.",
         rows=[("What they are", "Short chains of amino acids."),
               ("Used in", "Skincare, for years. Now scalp care too."),
               ("What they do", "Condition the scalp<br>and support the look<br>of thicker hair."),
               ("On a label", '<span class="label">sh-Polypeptide-1, -9, -11<br>sh-Oligopeptide-2, -10</span>')]),
    dict(id="G02", slug="how-to-photograph-your-part", field="porcelain", arch="viewfinder", h_size=114,
         headline="How to<br>photograph<br>your part.",
         rules=[("Same place.", "The same window, in daylight, at the same time of day."),
                ("Same part.", "Dry hair, parted straight back from your forehead."),
                ("Same angle.", "Phone above your head, camera facing down."),
                ("Same settings.", "No filter, no flash, no zoom.")],
         weeks_caption="Take one at week 0, week 6 and week 12."),
    dict(id="A03", slug="shedding-when-to-see-a-dermatologist", field="espresso", arch="checklist", h_size=114,
         headline="Shedding:<br>when to see a<br>dermatologist.",
         items=["Sudden, heavy shedding", "Patches or bald spots", "Redness, scaling,<br>pain or itching",
                "A part that keeps widening", "Shedding that lasts<br>past 6&nbsp;months"],
         note="Shedding that starts 2 to 4 months after a big change, then slowly eases, is usually temporary."),
    dict(id="E06", slug="fragrance-free-vs-unscented", field="butter", arch="contrast", h_size=114,
         headline="Fragrance-free<br>is not<br>unscented.", brand_on="espresso",
         defs=[("Fragrance-free", "Nothing is added to give it a smell."),
               ("Unscented", "Can contain a masking scent<br>that hides other smells."),
               ("On the label", "“Fragrance” or “parfum”<br>means a scent was added.")],
         tip="Sensitive scalp?<br>Choose fragrance-free."),
    dict(id="D04", slug="5-habits-to-retire-after-40", field="white", arch="swap", h_size=120,
         headline="5 habits<br>to retire<br>after 40.", band_h=520, list_top=140,
         rows=[("Tight ponytails every day", "Loose styles and soft clips"),
               ("Daily high heat", "Medium heat, fewer passes"),
               ("Skipping the scalp", "Two minutes of scalp care a day"),
               ("Heavy oils on fine hair", "A lightweight leave-on"),
               ("Judging by the mirror alone", "A part photo every 6 weeks")]),
    dict(id="A04", slug="hair-growth-cycle-3-stages", field="porcelain", arch="cycle", h_size=122,
         headline="Hair grows<br>in cycles.", deck="Shedding comes late.", deck_size=60,
         nodes=[("Growing", "for years", "solid"), ("Resting", "about 3 months", "butter"),
                ("Shedding", "as a new hair starts", "hollow")],
         note="A big change can send many hairs into resting at once. About 3 months later, they shed together."),
    dict(id="B04", slug="5-gentle-habits-postpartum-hair", field="butter", arch="list", h_size=106,
         headline="5 gentle habits<br>for postpartum<br>hair.",
         items=["Loose styles, not tight ponytails.", "A wide-tooth comb on wet hair.", "Less heat for a few months.",
                "A clean, comfortable scalp.", "Patience: hair grows<br>about half an inch a month."],
         note="For most women, hair is back to normal<br>by the baby’s first birthday."),
    dict(id="C01", slug="2-minute-scalp-care-routine", field="espresso", arch="steps", h_size=126,
         headline="Part. Drop.<br>Massage.<br>Two minutes.",
         steps=[("Part clean, dry hair.", "Where you want it to look fuller."),
                ("Add a few drops<br>along the part.", "On the scalp, not the lengths."),
                ("Massage for 1 to 2 minutes.", "Leave it in. Style as usual.")],
         foot="Once a day. Nothing to rinse."),
    dict(id="F01", slug="brush-shedding-hair-without-breakage", field="white", arch="strand", h_size=108,
         headline="Brush shedding<br>hair without<br>breakage.", brand_on="butter",
         points=[("1", "Ends"), ("2", "Mid-<br>lengths"), ("3", "Roots")],
         brand_left=56,
         tips=[("Start at the ends,<br>work up.", "Short strokes, never<br>from the roots down."),
               ("Wide-tooth comb<br>on wet hair.", "Go slowly. Wet hair<br>needs a gentle hand."),
               ("Soft bristles<br>on dry hair.", "Smooth it. Don’t tug."),
               ("Hold the mid-lengths.", "So the pull stays off the scalp.")]),
]


def render(out_dir, only=None):
    from playwright.sync_api import sync_playwright
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 1000, "height": 1500}, device_scale_factor=2)
        for p in [p for p in PINS if not only or p["id"] in only]:
            pg.set_content(build(p), wait_until="load")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(100)
            f = out / f"aftergrow_pin_{p['id']}_{p['slug']}_v1.png"
            pg.screenshot(path=str(f), clip={"x": 0, "y": 0, "width": 1000, "height": 1500})
            print("rendered", f.name)
        br.close()


if __name__ == "__main__":
    render(sys.argv[1], set(sys.argv[2:]) or None)
