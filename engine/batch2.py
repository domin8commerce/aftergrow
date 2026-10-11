"""Batch 2: 24 more pins on the same engine. Usage: python3 -I batch2.py <out_dir> [ID ...]"""
import math, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pinengine as E
from pinengine import ESP, BUT, WHI, POR, STO, SAN, PART

EUC = "#4F6F66"


def band_css(h):
    return f".topband{{position:absolute;z-index:1;left:0;right:0;top:0;height:{h}px;background:#F3E2A0}}" if h else ""


def band_div(p):
    return '<div class="topband"></div>' if p.get("band_h") else ""


# ------------------------------------------------------------------ new archetypes

def a_bignum(p):
    lines = "".join(f'<p class="bl">{t}</p>' for t in p["lines"])
    bars = "".join(f'<div class="bar"><p class="bk">{k}</p><div class="bt"><div class="bf" style="width:{w}%"></div></div><p class="bv">{v}</p></div>'
                   for k, w, v in p.get("bars", []))
    body = f"""<div class="bn"><p class="big tnum">{p['big']}</p><p class="bigl">{p['big_label']}</p></div>
    <div class="bars">{bars}</div><div class="bls">{lines}</div>"""
    css = """
.bn{margin-top:46px}
.big{font-size:236px;font-weight:600;letter-spacing:-0.06em;line-height:.9;color:var(--head)}
.bigl{font-size:54px;font-weight:600;letter-spacing:-0.024em;margin-top:6px}
.bars{margin-top:70px;display:flex;flex-direction:column;gap:30px}
.bar .bk{font-size:34px;font-weight:600;letter-spacing:-0.014em}
.bar .bt{height:44px;margin-top:12px;border:5px solid #33241D;border-radius:24px;overflow:hidden;background:#FFFFFF}
.bar .bf{height:100%;background:#33241D;border-radius:0 20px 20px 0}
.bar .bv{font-size:30px;font-weight:500;color:#675E58;margin-top:8px}
.bls{position:absolute;left:80px;right:80px;bottom:150px;border-top:5px solid var(--fg);padding-top:26px;
     display:flex;flex-direction:column;gap:18px}
.bl{font-size:42px;font-weight:500;letter-spacing:-0.016em;line-height:1.15}
"""
    return body, css


def a_definition(p):
    rows = "".join(f'<div class="drow"><p class="term">{t}</p><p class="mean">{m}</p></div>' for t, m in p["terms"])
    body = f"""<div class="defs2">{rows}</div><div class="sum"><p class="s1">{p['sum']}</p><p class="s2">{p['sum2']}</p></div>"""
    css = """
.defs2{margin-top:70px;border-top:6px solid var(--fg)}
.drow{padding:40px 0 42px;border-bottom:2px solid var(--rule)}
.drow .term{font-size:84px;font-weight:600;letter-spacing:-0.036em;line-height:1}
.drow .mean{font-size:46px;font-weight:500;letter-spacing:-0.016em;line-height:1.15;margin-top:14px;color:var(--sub)}
.sum{position:absolute;left:80px;right:80px;bottom:150px}
.s1{font-size:42px;font-weight:500;line-height:1.2;letter-spacing:-0.016em}
.s2{font-size:56px;font-weight:600;letter-spacing:-0.026em;margin-top:18px;color:var(--head)}
"""
    return body, css


def a_list2(p):
    """List with optional Butter top band on light fields, optional note."""
    items = "".join(f'<li><span class="m"></span><span>{t}</span></li>' for t in p["items"])
    note = f'<p class="note">{p["note"]}</p>' if p.get("note") else ""
    body = f"""{band_div(p)}<ul class="dl">{items}</ul>{note}"""
    css = band_css(p.get("band_h")) + """
.dl{list-style:none;position:relative;z-index:2;margin-top:%dpx;display:flex;flex-direction:column;gap:%dpx}
.dl li{display:grid;grid-template-columns:30px 1fr;gap:30px;align-items:start;font-size:%dpx;font-weight:500;
       line-height:1.12;letter-spacing:-0.02em}
.dl .m{width:24px;height:24px;border-radius:50%%;background:var(--mark);margin-top:%dpx}
.note{position:absolute;left:80px;right:80px;bottom:146px;font-size:34px;font-weight:600;line-height:1.26;
      letter-spacing:-0.012em;border-top:5px solid var(--fg);padding-top:22px}
""" % (p.get("list_top", 84), p.get("gap", 48), p.get("item_size", 52), int(p.get("item_size", 52) * .34))
    return body, css


def a_ruler(p):
    W, x0 = 840, 20
    usable = W - 2 * x0
    mx = lambda m: x0 + usable * m / 12
    els = []
    for a, b, fill, stroke in p["spans"]:
        els.append(f'<rect x="{mx(a):.1f}" y="62" width="{mx(b) - mx(a):.1f}" height="78" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="6"/>')
    els.append(f'<line x1="{x0}" y1="140" x2="{W - x0}" y2="140" stroke="{ESP}" stroke-width="6" stroke-linecap="round"/>')
    for m in range(13):
        big = m in (0, 3, 6, 9, 12)
        els.append(f'<line x1="{mx(m):.1f}" y1="140" x2="{mx(m):.1f}" y2="{172 if big else 158}" stroke="{ESP}" stroke-width="{5 if big else 3}" stroke-linecap="round"/>')
        if big:
            els.append(f'<text x="{mx(m):.1f}" y="216" text-anchor="middle" font-family="SG" font-weight="600" font-size="36" fill="{ESP}">{m}</text>')
    els.append(f'<circle cx="{mx(0):.1f}" cy="101" r="20" fill="{ESP}"/>')
    for a, b, lab in p.get("span_labels", []):
        els.append(f'<text x="{(mx(a) + mx(b)) / 2:.1f}" y="40" text-anchor="middle" font-family="SG" font-weight="600" font-size="32" fill="{ESP}">{lab}</text>')

    els.append(f'<text x="{W / 2}" y="268" text-anchor="middle" font-family="SG" font-weight="500" font-size="30" fill="{STO}">months after the change</text>')
    svg = f'<svg width="{W}" height="290" viewBox="0 0 {W} 290">{"".join(els)}</svg>'
    rows = "".join(f'<div class="rr"><p class="rk tnum">{k}</p><p class="rv">{v}</p></div>' for k, v in p["rows"])
    body = f"""<div class="rul">{svg}</div><div class="rrs">{rows}</div>"""
    css = """
.rul{margin-top:72px}
.rrs{margin-top:44px;border-top:5px solid var(--fg)}
.rr{display:grid;grid-template-columns:300px 1fr;gap:18px;padding:28px 0;border-bottom:2px solid var(--rule);align-items:baseline}
.rk{font-size:38px;font-weight:600;letter-spacing:-0.02em;white-space:nowrap}
.rv{font-size:40px;font-weight:500;line-height:1.18;letter-spacing:-0.014em}
"""
    return body, css


def a_curve(p):
    W, H = 840, 330
    bx, by = 20, 270
    px, py = 20 + (W - 40) * p.get("peak_m", 3.5) / 12, 64
    ex = W - 20
    path = (f"M{bx} {by} C {bx + 120} {by - 10}, {px - 110} {py}, {px} {py} "
            f"S {px + 260} {by - 70}, {ex} {by - 6}")
    els = [f'<path d="{path} L {ex} {by} Z" fill="{ESP}" fill-opacity=".10"/>',
           f'<path d="{path}" fill="none" stroke="{ESP}" stroke-width="7" stroke-linecap="round"/>',
           f'<line x1="{bx}" y1="{by}" x2="{ex}" y2="{by}" stroke="{ESP}" stroke-width="5"/>',
           f'<line x1="{px}" y1="{py}" x2="{px}" y2="{by}" stroke="{ESP}" stroke-width="3" stroke-dasharray="6 9"/>',
           f'<circle cx="{px}" cy="{py}" r="16" fill="{ESP}"/>']
    svg = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(els)}</svg>'
    labs = (f'<p class="cl" style="left:0;top:{H + 12}px">{p["l_start"]}</p>'
            f'<p class="cl" style="left:{px:.0f}px;top:{py - 74}px;transform:translateX(-50%);font-weight:600;font-size:42px;color:#33241D">{p["l_peak"]}</p>'
            f'<p class="cl" style="right:0;top:{H + 12}px;text-align:right">{p["l_end"]}</p>')
    items = "".join(f'<li><span class="m"></span><span>{t}</span></li>' for t in p["items"])
    body = f"""<div class="cv">{svg}{labs}</div><ul class="dl">{items}</ul>"""
    css = """
.cv{position:relative;margin-top:120px;height:390px}
.cl{position:absolute;font-size:34px;font-weight:500;color:#675E58;white-space:nowrap}
.dl{list-style:none;margin-top:70px;display:flex;flex-direction:column;gap:26px}
.dl li{display:grid;grid-template-columns:26px 1fr;gap:26px;align-items:start;font-size:46px;font-weight:500;line-height:1.14;letter-spacing:-0.018em}
.dl .m{width:20px;height:20px;border-radius:50%;background:var(--fg);margin-top:17px}
"""
    return body, css


def a_split(p):
    def col(head, items, mark):
        lis = "".join(f'<li>{mark}<span>{t}</span></li>' for t in items)
        return f'<div class="col"><p class="ch">{head}</p><ul>{lis}</ul></div>'
    ok = (f'<svg width="34" height="34" viewBox="0 0 34 34"><path d="M5 18 L13 26 L29 8" fill="none" stroke="{p.get("ok_color", EUC)}" '
          f'stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    no = (f'<svg width="34" height="34" viewBox="0 0 34 34"><path d="M8 8 L26 26 M26 8 L8 26" fill="none" stroke="{p.get("no_color", ESP)}" '
          f'stroke-width="5" stroke-linecap="round"/></svg>')
    m1 = ok if p.get("marks", True) else '<span class="dot"></span>'
    m2 = no if p.get("marks", True) else '<span class="dot"></span>'
    foot = f'<p class="foot">{p["foot"]}</p>' if p.get("foot") else ""
    body = f"""{band_div(p)}<div class="split">{col(p['left'][0], p['left'][1], m1)}{col(p['right'][0], p['right'][1], m2)}</div>{foot}"""
    css = band_css(p.get("band_h")) + """
.split{position:relative;z-index:2;margin-top:%dpx;display:grid;grid-template-columns:1fr 1fr;gap:44px}
.col{border-top:6px solid var(--fg);padding-top:26px}
.ch{font-size:54px;font-weight:600;letter-spacing:-0.026em;margin-bottom:30px;color:var(--head);line-height:1.04}
.col ul{list-style:none;display:flex;flex-direction:column;gap:34px}
.col li{display:grid;grid-template-columns:38px 1fr;gap:16px;align-items:start;font-size:%dpx;font-weight:500;line-height:1.16;letter-spacing:-0.016em}
.col li svg{margin-top:4px}
.col .dot{width:18px;height:18px;border-radius:50%%;background:var(--mark);margin-top:16px}
.foot{position:absolute;left:80px;right:80px;bottom:146px;font-size:40px;font-weight:600;letter-spacing:-0.02em;line-height:1.2;
      border-top:5px solid var(--fg);padding-top:24px;color:var(--head)}
""" % (p.get("split_top", 76), p.get("item_size", 37))
    return body, css


def a_frames(p):
    fr = ""
    for wk in ("Week 0", "Week 6", "Week 12"):
        fr += (f'<div class="fr"><div class="ph"><svg width="150" height="150" viewBox="0 0 100 100"><path d="{PART}" fill="{ESP}"/></svg>'
               f'</div><p class="wk tnum">{wk}</p></div>')
    lines = "".join(f'<p class="fl">{t}</p>' for t in p["lines"])
    body = f"""<div class="frs">{fr}</div><div class="fls">{lines}</div>"""
    css = """
.frs{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:84px}
.ph{height:420px;border:7px solid #33241D;border-radius:20px;background:#FFFFFF;display:flex;align-items:center;justify-content:center}
.wk{font-size:46px;font-weight:600;letter-spacing:-0.022em;margin-top:20px}
.fls{position:absolute;left:80px;right:80px;bottom:150px;border-top:5px solid var(--fg);padding-top:26px;display:flex;flex-direction:column;gap:14px}
.fl{font-size:44px;font-weight:600;letter-spacing:-0.022em;line-height:1.12}
"""
    return body, css


def a_parts(p):
    cx, cy, r = 200, 200, 186
    els = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BUT}" stroke-width="7"/>']
    xs = (128, 200, 272)
    for i, x in enumerate(xs):
        half = math.sqrt(r * r - (x - cx) ** 2) - 26
        els.append(f'<line x1="{x}" y1="{cy - half:.0f}" x2="{x}" y2="{cy + half * .55:.0f}" stroke="{BUT}" stroke-width="6" stroke-linecap="round"/>')
        for k in range(3):
            y = cy - half + 40 + k * 64
            els.append(f'<circle cx="{x}" cy="{y:.0f}" r="9" fill="{BUT}"/>')
        els.append(f'<text x="{x}" y="{cy + half * .55 + 58:.0f}" text-anchor="middle" font-family="SG" font-weight="600" font-size="40" fill="{BUT}">{i + 1}</text>')
    svg = f'<svg width="400" height="460" viewBox="0 0 400 460">{"".join(els)}</svg>'
    steps = "".join(f'<div class="ps"><p class="pn tnum">{i + 1}</p><div><p class="lead">{a}</p><p class="copy sub">{b}</p></div></div>'
                    for i, (a, b) in enumerate(p["steps"]))
    body = f"""<div class="pw"><div>{svg}</div><div class="pss">{steps}</div></div><p class="foot">{p['foot']}</p>"""
    css = """
.pw{display:grid;grid-template-columns:400px 1fr;gap:36px;margin-top:70px;align-items:start}
.pss{display:flex;flex-direction:column;gap:34px;padding-top:6px}
.ps{display:grid;grid-template-columns:50px 1fr;gap:10px;align-items:start}
.pn{font-size:56px;font-weight:600;line-height:.9;color:#F3E2A0}
.ps .lead{font-size:40px}
.ps .copy{font-size:30px;margin-top:8px}
.foot{position:absolute;left:80px;right:80px;bottom:150px;font-size:46px;font-weight:600;letter-spacing:-0.022em;color:var(--head);
      border-top:2px solid var(--rule);padding-top:26px}
"""
    return body, css


ICONS = {
    "cleanser": '<rect x="22" y="26" width="36" height="58" rx="8"/><path d="M32 26 V14 H48 V26"/><path d="M48 14 H58"/>',
    "serum": '<rect x="20" y="40" width="40" height="46" rx="8"/><path d="M30 40 V30 H50 V40"/><path d="M36 30 V12 Q40 4 44 12 V30"/>',
    "comb": '<rect x="8" y="22" width="64" height="16" rx="5"/><path d="M14 38 V64 M24 38 V64 M34 38 V64 M44 38 V64 M54 38 V64 M64 38 V64"/>',
    "towel": '<path d="M6 14 H74"/><rect x="16" y="14" width="48" height="62" rx="5"/><path d="M16 60 H64"/><path d="M28 14 V40"/>',
}


def a_grid4(p):
    cells = ""
    for c in p["cells"]:
        icon = (f'<svg width="130" height="146" viewBox="0 0 80 90" fill="none" stroke="#33241D" stroke-width="4" '
                f'stroke-linecap="round" stroke-linejoin="round">{ICONS[c["icon"]]}</svg>') if c.get("icon") else ""
        sub = f'<p class="gs">{c["sub"]}</p>' if c.get("sub") else ""
        cells += f'<div class="gc">{icon}<p class="gl">{c["label"]}</p>{sub}</div>'
    foot = f'<p class="foot">{p["foot"]}</p>' if p.get("foot") else ""
    body = f"""<div class="g4">{cells}</div>{foot}"""
    css = """
.g4{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:%dpx}
.gc{border-top:6px solid var(--fg);padding-top:24px;min-height:%dpx}
.gl{font-size:%dpx;font-weight:600;letter-spacing:-0.022em;line-height:1.1;margin-top:14px}
.gs{font-size:38px;font-weight:500;line-height:1.2;margin-top:12px;color:var(--sub)}
.foot{position:absolute;left:80px;right:80px;bottom:146px;font-size:40px;font-weight:600;letter-spacing:-0.02em;line-height:1.2;
      border-top:5px solid var(--fg);padding-top:24px}
""" % (p.get("grid_top", 80), p.get("cell_h", 250), p.get("label_size", 46))
    return body, css


def a_schedule(p):
    rows = "".join(f'<div class="sr"><p class="sk">{k}</p><p class="sv">{v}</p></div>' for k, v in p["rows"])
    body = f"""<div class="sch">{rows}</div><p class="foot">{p['foot']}</p>"""
    css = """
.sch{margin-top:80px;border-top:2px solid var(--rule)}
.sr{display:grid;grid-template-columns:320px 1fr;gap:24px;padding:38px 0;border-bottom:2px solid var(--rule);align-items:baseline}
.sk{font-size:40px;font-weight:600;letter-spacing:-0.02em;color:var(--head)}
.sv{font-size:46px;font-weight:500;letter-spacing:-0.02em;line-height:1.14}
.foot{position:absolute;left:80px;right:80px;bottom:150px;font-size:36px;font-weight:500;color:var(--sub);line-height:1.25}
"""
    return body, css


def a_ledger2(p):
    rows = "".join(f'<div class="lrow"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in p["rows"])
    foot = f'<p class="lfoot">{p["foot"]}</p>' if p.get("foot") else ""
    body = f"""<div class="ledger">{rows}</div>{foot}"""
    css = """
.ledger{margin-top:%dpx;border-top:5px solid var(--fg);border-bottom:2px solid var(--rule)}
.lrow{display:grid;grid-template-columns:250px 1fr;gap:18px;border-top:2px solid var(--rule);padding:%dpx 0}
.lrow:first-child{border-top:0}
.lrow .k{font-size:31px;font-weight:500;color:var(--sub);padding-top:8px;line-height:1.2}
.lrow .v{font-size:%dpx;font-weight:500;line-height:1.18;letter-spacing:-0.016em}
.lrow .v b{font-weight:600;color:var(--head)}
.lfoot{position:absolute;left:80px;right:80px;bottom:150px;font-size:44px;font-weight:600;letter-spacing:-0.022em;color:var(--head)}
""" % (p.get("ledger_top", 76), p.get("row_pad", 30), p.get("val_size", 44))
    return body, css


def a_label(p):
    # a simple label card with list bars and four numbered callouts
    L = []
    L.append('<rect x="4" y="4" width="372" height="600" rx="22" fill="#FFFFFF" stroke="#33241D" stroke-width="6"/>')
    L.append('<text x="40" y="78" font-family="SG" font-weight="600" font-size="34" fill="#33241D">Ingredients</text>')
    widths = [250, 210, 280, 190, 230, 160, 240, 120, 200, 150, 170, 110]
    for i, w in enumerate(widths):
        y = 120 + i * 36
        L.append(f'<rect x="40" y="{y}" width="{w}" height="14" rx="7" fill="#33241D" fill-opacity="{.85 if i < 2 else .28}"/>')
    L.append('<rect x="40" y="556" width="200" height="16" rx="8" fill="#F3E2A0" stroke="#33241D" stroke-width="3"/>')
    for n, y in ((1, 127), (2, 127 + 0), (3, 380), (4, 564)):
        pass
    marks = [(1, 127), (2, 235), (3, 415), (4, 564)]
    for n, y in marks:
        L.append(f'<circle cx="330" cy="{y}" r="26" fill="#33241D"/>')
        L.append(f'<text x="330" y="{y + 11}" text-anchor="middle" font-family="SG" font-weight="600" font-size="30" fill="#F3E2A0">{n}</text>')
    svg = f'<svg width="380" height="610" viewBox="0 0 380 610">{"".join(L)}</svg>'
    notes = "".join(f'<div class="ln"><p class="lnn tnum">{i + 1}</p><div><p class="lead">{a}</p><p class="copy sub">{b}</p></div></div>'
                    for i, (a, b) in enumerate(p["notes"]))
    body = f"""<div class="lw"><div>{svg}</div><div class="lns">{notes}</div></div>"""
    css = """
.lw{display:grid;grid-template-columns:380px 1fr;gap:36px;margin-top:66px;align-items:start}
.lns{display:flex;flex-direction:column;gap:40px}
.ln{display:grid;grid-template-columns:44px 1fr;gap:10px;align-items:start}
.lnn{font-size:44px;font-weight:600;line-height:1;color:var(--head)}
.ln .lead{font-size:39px}
.ln .copy{font-size:30px;margin-top:6px}
"""
    return body, css


def a_grid6(p):
    ban = ('<svg width="44" height="44" viewBox="0 0 44 44"><circle cx="22" cy="22" r="18" fill="none" stroke="#33241D" stroke-width="5"/>'
           '<path d="M10 34 L34 10" stroke="#33241D" stroke-width="5" stroke-linecap="round"/></svg>')
    cells = "".join(f'<div class="c6">{ban}<p class="c6l">{a}</p><p class="c6s">{b}</p></div>' for a, b in p["cells"])
    body = f"""<div class="g6">{cells}</div>"""
    css = """
.g6{display:grid;grid-template-columns:1fr 1fr;column-gap:36px;row-gap:46px;margin-top:76px}
.c6{border-top:5px solid var(--fg);padding-top:22px}
.c6l{font-size:48px;font-weight:600;letter-spacing:-0.022em;margin-top:12px}
.c6s{font-size:35px;font-weight:500;line-height:1.2;margin-top:8px;color:var(--sub)}
"""
    return body, css


def a_weekline(p):
    W = 840
    xs = (40, 420, 800)
    els = [f'<line x1="40" y1="60" x2="800" y2="60" stroke="{BUT}" stroke-width="8" stroke-linecap="round"/>']
    for x in xs:
        els.append(f'<circle cx="{x}" cy="60" r="34" fill="{ESP}" stroke="{BUT}" stroke-width="8"/>')
    svg = f'<svg width="{W}" height="120" viewBox="0 0 {W} 120">{"".join(els)}</svg>'
    cols = "".join(f'<div class="wc" style="text-align:{al}"><p class="wn tnum">{w}</p><p class="wt">{t}</p></div>'
                   for (w, t), al in zip(p["weeks"], ("left", "center", "right")))
    body = f"""<div class="wl2">{svg}<div class="wcs">{cols}</div></div><p class="foot">{p['foot']}</p>"""
    css = """
.wl2{margin-top:205px}
.wcs{display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px;margin-top:26px}
.wn{font-size:66px;font-weight:600;letter-spacing:-0.034em;color:var(--head)}
.wt{font-size:42px;font-weight:500;line-height:1.2;margin-top:12px}
.foot{position:absolute;left:80px;right:80px;bottom:150px;font-size:40px;font-weight:600;letter-spacing:-0.02em;line-height:1.22;
      border-top:2px solid var(--rule);padding-top:26px}
"""
    return body, css


def a_protocol(p):
    blocks = "".join(f'<div class="mb"><p class="mbt tnum">Month {i}</p><p class="mbs">Bottle {i}</p></div>' for i in (1, 2, 3))
    ticks = f"""<svg width="840" height="56" viewBox="0 0 840 56">
      <line x1="6" y1="28" x2="834" y2="28" stroke="{ESP}" stroke-width="6"/>
      <line x1="6" y1="6" x2="6" y2="50" stroke="{ESP}" stroke-width="8" stroke-linecap="round"/>
      <line x1="420" y1="6" x2="420" y2="50" stroke="{ESP}" stroke-width="8" stroke-linecap="round"/>
      <line x1="834" y1="6" x2="834" y2="50" stroke="{ESP}" stroke-width="8" stroke-linecap="round"/></svg>"""
    items = "".join(f'<li><span class="m"></span><span>{t}</span></li>' for t in p["items"])
    body = f"""<div class="mbs3">{blocks}</div><div class="pt">{ticks}<div class="ptl tnum"><span>Week 0</span><span>Week 6</span><span>Week 12</span></div>
    <p class="ptc">Check-in emails</p></div><ul class="dl">{items}</ul><p class="fine">{p['fine']}</p>"""
    css = """
.mbs3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:64px}
.mb{border:6px solid #33241D;border-radius:18px;padding:22px 22px 24px;background:#FFFFFF}
.mbt{font-size:40px;font-weight:600;letter-spacing:-0.02em}
.mbs{font-size:30px;font-weight:500;color:#675E58;margin-top:6px}
.pt{margin-top:34px}
.ptl{display:flex;justify-content:space-between;font-size:30px;font-weight:600;margin-top:8px}
.ptc{font-size:28px;font-weight:500;color:#675E58;margin-top:4px;text-align:center}
.dl{list-style:none;margin-top:44px;display:flex;flex-direction:column;gap:22px}
.dl li{display:grid;grid-template-columns:24px 1fr;gap:24px;align-items:start;font-size:43px;font-weight:500;line-height:1.14;letter-spacing:-0.018em}
.dl .m{width:20px;height:20px;border-radius:50%;background:#33241D;margin-top:16px}
.fine{position:absolute;left:80px;right:80px;bottom:150px;font-size:32px;font-weight:600;line-height:1.25;border-top:5px solid var(--fg);padding-top:20px}
"""
    return body, css


E.ARCH.update(bignum=a_bignum, definition=a_definition, list2=a_list2, ruler=a_ruler, curve=a_curve, split=a_split,
              frames=a_frames, parts=a_parts, grid4=a_grid4, schedule=a_schedule, ledger2=a_ledger2, label=a_label,
              grid6=a_grid6, weekline=a_weekline, protocol=a_protocol)

# ------------------------------------------------------------------ batch 2 pins
PINS = [
    dict(id="A02", slug="how-much-hair-shedding-is-normal", field="butter", arch="bignum", h_size=104,
         headline="How much shedding<br>is normal?", big="50–100", big_label="hairs a day is normal.",
         bars=[("A normal day", 34, "50 to 100 hairs"), ("During a shed", 82, "More, for a few months")],
         lines=["It usually settles on its own.", "Count less. Compare photos instead."]),
    dict(id="A05", slug="telogen-effluvium-plain-english", field="porcelain", arch="definition", h_size=112,
         headline="Telogen effluvium,<br>in plain English.",
         terms=[("Telogen", "the resting phase of a hair"), ("Effluvium", "an outflow, a shedding")],
         sum="Many hairs rest at once, then shed together 2 to 4 months later.", sum2="Usually temporary."),
    dict(id="A06", slug="shedding-after-stress-illness-surgery", field="espresso", arch="list2", h_size=118,
         headline="Shedding after<br>a hard season.", item_size=58, gap=64,
         items=["Stress, illness, surgery<br>or a new baby.", "Many hairs switch to<br>resting at once.",
                "The shed arrives<br>2 to 4 months later.", "It usually passes."],
         note="Sudden, patchy or lasting past 6 months?<br>See a dermatologist."),
    dict(id="A07", slug="why-your-part-looks-wider", field="white", arch="list2", h_size=118, band_h=430, list_top=150,
         headline="Why your part<br>looks wider.", item_size=52, gap=60,
         note="Shedding is common, and usually temporary.",
         items=["More hairs rest at once,<br>so the part looks thinner.",
                "It usually settles<br>in 6 to 9 months.",
                "If it keeps widening,<br>see a dermatologist.",
                "Track it with one photo<br>every 6 weeks."]),
    dict(id="A08", slug="hair-shedding-timeline-month-by-month", field="porcelain", arch="ruler", h_size=110,
         headline="A shedding timeline,<br>month by month.",
         spans=[(2, 4, BUT, ESP), (6, 9, "rgba(51,36,29,.12)", ESP)],
         span_labels=[(2, 4, "Shed starts"), (6, 9, "Settles")],
         rows=[("Month 0", "A big change in the body."), ("Months 2 to 4", "The shed starts."),
               ("Months 6 to 9", "It settles for most people."), ("Past 6 months", "Still heavy? See a dermatologist.")]),
    dict(id="A10", slug="5-questions-for-your-dermatologist", field="porcelain", arch="checklist", h_size=112,
         headline="5 questions<br>for your<br>dermatologist.",
         items=["Is this shedding,<br>or something else?", "Do I need any blood tests?", "What should I expect<br>over 6 months?",
                "Which habits help right now?", "When should I come back?"],
         note="Bring your part photos and a short list of recent changes."),
    dict(id="B01", slug="postpartum-shedding-peaks-around-month-4", field="butter", arch="curve", h_size=104, peak_m=4,
         headline="Postpartum<br>shedding peaks<br>around month&nbsp;4.", l_start="Birth", l_peak="About month 4", l_end="First birthday",
         items=["Pregnancy keeps more hairs growing.", "After birth, they rest together.",
                "The shed peaks about 4&nbsp;months in.", "Most see it ease by the first birthday."]),
    dict(id="B02", slug="postpartum-shedding-normal-or-not", field="white", arch="split", h_size=104, band_h=470, split_top=150,
         headline="Postpartum<br>shedding: normal<br>or not?",
         left=("Normal", ["More hair in the<br>brush and shower", "Short new hairs at the hairline", "A shed that eases over months"]),
         right=("See a dermatologist", ["Patches or bald spots", "A painful or scaly scalp", "Still heavy after<br>12&nbsp;months"]),
         item_size=42, foot="For most women, hair is back to normal by the baby’s first birthday."),
    dict(id="B07", slug="postpartum-hair-photo-habit-week-0-6-12", field="butter", arch="frames", h_size=112,
         headline="Three photos<br>beat the mirror.",
         lines=["Same window. Same part. Same angle.", "Then compare them side by side."]),
    dict(id="C03", slug="how-to-apply-scalp-serum-part-method", field="espresso", arch="parts", h_size=110,
         headline="The part method<br>for scalp serum.",
         steps=[("Part, then add a few drops along it.", "Right on the scalp."), ("Move the part an inch over.", "Repeat across the top."),
                ("Massage, then leave it in.", "1 to 2 minutes.")],
         foot="It reaches the scalp, not the lengths."),
    dict(id="C04", slug="scalp-care-vs-hair-care", field="espresso", arch="split", h_size=118, marks=False,
         headline="Scalp care is<br>not hair care.", split_top=110,
         item_size=46,
         left=("Hair care", ["Works on the strand.", "Shampoo, masks, oils for the lengths."]),
         right=("Scalp care", ["Works on the skin your hair grows from.", "A leave-on serum, a gentle massage."]),
         foot="Think of it as skincare, for your scalp."),
    dict(id="C07", slug="edited-scalp-care-shelf-4-things", field="butter", arch="grid4", h_size=140,
         headline="4 things,<br>not 14.", cell_h=330, grid_top=76, label_size=50,
         cells=[dict(icon="cleanser", label="A gentle<br>cleanser"), dict(icon="serum", label="A leave-on<br>scalp serum"),
                dict(icon="comb", label="A wide-tooth<br>comb"), dict(icon="towel", label="A soft<br>towel")],
         foot="Simple routines are the ones you keep."),
    dict(id="D01", slug="fuller-looking-hair-over-40-6-habits", field="white", arch="list2", h_size=112, band_h=430, list_top=150,
         headline="Fuller-looking<br>hair over 40.", item_size=52, gap=46,
         note="Start with one. Add one a week.",
         items=["Care for the scalp like skin.", "Part on the fuller side.", "Volume at the roots,<br>not the ends.",
                "Lower heat, fewer passes.", "Loose styles most days.", "A part photo every 6 weeks."]),
    dict(id="D05", slug="low-effort-hair-routine-over-40", field="espresso", arch="schedule", h_size=112,
         headline="A low-effort<br>routine that<br>works.",
         rows=[("Every day", "Two minutes of scalp care"), ("Every 2 to 3 days", "Wash"), ("Once a week", "One gentle mask"),
               ("Every 6 weeks", "A part photo")],
         foot="Realistic for a busy week. Easy to keep for 90 days."),
    dict(id="D06", slug="judge-your-hair-by-photos-not-moods", field="butter", arch="list2", h_size=112,
         headline="Judge your hair<br>by photos,<br>not moods.", item_size=54, gap=58, list_top=96,
         items=["Same window,<br>same time of day.", "Dry hair, parted straight back.", "Phone above your head,<br>camera facing down.",
                "No filter, no flash, no zoom."],
         note="Repeat every 6 weeks, then compare."),
    dict(id="E01", slug="rosemary-for-hair-honestly", field="espresso", arch="ledger2", h_size=132,
         headline="Rosemary,<br>honestly.", val_size=48, row_pad=40,
         rows=[("On the label", "<b>Rosmarinus Officinalis (Rosemary) Extract</b>"), ("What it does", "A fresh, cared-for feel on the scalp."),
               ("Where to find it", "Leave-on scalp serums."), ("The honest part", "No hype. Just a good ingredient.")]),
    dict(id="E03", slug="eucalyptus-for-scalp-fresh-feel", field="butter", arch="ledger2", h_size=112,
         headline="Eucalyptus,<br>for a fresh<br>scalp feel.", val_size=46, row_pad=36,
         rows=[("On the label", "<b>Eucalyptus Globulus Leaf Extract</b>"), ("What it does", "A fresh, clean feel on the scalp."),
               ("Pairs with", "Rosemary."), ("Where to find it", "Leave-on scalp serums.")]),
    dict(id="E04", slug="4-plant-extracts-in-scalp-care", field="white", arch="grid4", h_size=116,
         headline="4 plant extracts,<br>4 jobs.", label_size=54, cell_h=300, grid_top=96,
         cells=[dict(label="Saw palmetto", sub="A scalp-care botanical."), dict(label="Scutellaria root", sub="Helps hold moisture."),
                dict(label="Soybean germ", sub="Conditioning.<br>Contains soy."), dict(label="Wheat germ", sub="Conditioning.<br>Contains wheat.")],
         foot="Every ingredient, listed in label order."),
    dict(id="E05", slug="how-to-read-a-scalp-serum-label", field="porcelain", arch="label", h_size=108,
         headline="How to read a<br>scalp serum label.",
         notes=[("Water first?", "It’s the base. Lightweight and water-based."),
                ("Most to least.", "Above 1%, the list<br>runs by amount."),
                ("Under 1%, any order.", "Low on the list<br>isn’t a red flag."),
                ("“Fragrance” or “parfum”?", "A scent was added. Check allergens too.")]),
    dict(id="E07", slug="free-from-list-explained", field="butter", arch="grid6", h_size=112,
         headline="The free-from<br>list, explained.",
         cells=[("Parabens", "A family of preservatives."), ("Sulfates", "Strong, foamy cleansers."),
                ("Silicones", "Coat hair for slip and shine."), ("Phthalates", "Often found in fragrance."),
                ("Mineral oil", "A petroleum-based oil."), ("Added fragrance", "Added just for scent.")]),
    dict(id="F05", slug="heat-styling-during-a-shed", field="espresso", arch="list2", h_size=124,
         headline="Gentler heat,<br>same result.", item_size=60, gap=66,
         items=["Medium heat, fewer passes.", "Heat protectant every time.", "Air-dry most of the way first.",
                "Two heat-free days a week."],
         note="Small changes that protect fine hair during a shed."),
    dict(id="G03", slug="three-photo-method-week-0-6-12", field="espresso", arch="weekline", h_size=114,
         headline="Three photos.<br>Ninety days.<br>Your call.",
         weeks=[("Week 0", "Before your<br>first drops."), ("Week 6", "A fair<br>midpoint."), ("Week 12", "Compare,<br>then decide.")],
         foot="Hair changes slowly. Photos taken the same way are the fair judge."),
    dict(id="H02", slug="whats-inside-aftergrow-scalp-serum", field="espresso", arch="ledger2", h_size=84,
         headline="Five peptides.<br>Six plant extracts.<br>No fragrance.", val_size=41, row_pad=29, ledger_top=64,
         rows=[("Peptides", "<b>sh-Polypeptide-1, -9, -11<br>sh-Oligopeptide-2, -10</b>"),
               ("Plant extracts", "Rosemary, eucalyptus, saw palmetto, scutellaria root, soybean germ, wheat germ"),
               ("Base", "Water. Lightweight,<br>non-greasy."), ("Fragrance", "None."), ("Pills to swallow", "None.")],
         foot="Contains soy and wheat."),
    dict(id="H03", slug="the-90-day-protocol", field="butter", arch="protocol", h_size=120,
         headline="The 90-Day<br>Protocol.",
         items=["3 bottles, one for each month.", "Check-in emails at weeks 0, 6 and 12.", "Free shipping.",
                "Love how your hair looks, or get your<br>money back on your first order."],
         fine="Refills every 3 months. Skip or cancel anytime."),
]

if __name__ == "__main__":
    E.PINS = PINS
    E.render(sys.argv[1], set(sys.argv[2:]) or None)
