"""Aftergrow carousel engine: 4:5 Instagram and Facebook slides in the brand system.

A carousel is a list of slides. Each slide is one template plus its text. Every slide is rendered by
headless Chromium at 2160 x 2700 and saved as a 1440 x 1800 JPEG (4:5, the Instagram feed maximum).

Usage: python3 -I engine/carousel.py <out_dir> [carousel IDs]
Carousels live in engine/carousels_*.py as CAROUSELS = [dict(id=..., field=..., slides=[...]), ...].
"""
import html, importlib, io, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from pinengine import font_css, part, ESP, BUT, WHI, POR, STO, SAN, SIL  # noqa: E402

W, H = 1080, 1350
OUT_W, OUT_H = 1440, 1800
EUC = "#4F6F66"

FIELDS = {  # background, text, headline, secondary, mark, rule, highlight fill, highlight text
    "butter": (BUT, ESP, ESP, STO, ESP, "rgba(51,36,29,.22)", ESP, BUT),
    "espresso": (ESP, WHI, BUT, SAN, BUT, "rgba(217,204,191,.26)", BUT, ESP),
    "porcelain": (POR, ESP, ESP, STO, ESP, SIL, BUT, ESP),
    "white": (WHI, ESP, ESP, STO, ESP, SIL, BUT, ESP),
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px}
body{font-family:'SG','Helvetica Neue',Arial,sans-serif;-webkit-font-smoothing:antialiased;
     font-kerning:normal;text-rendering:geometricPrecision}
.s{position:relative;width:1080px;height:1350px;overflow:hidden;background:var(--bg);color:var(--fg);padding:84px 88px 62px;
    display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;align-items:center;height:40px;flex:0 0 auto;position:relative;z-index:2}
.mid{flex:1 1 auto;display:flex;flex-direction:column;justify-content:center;position:relative;z-index:2;padding:30px 0}
.mid.end{justify-content:flex-end;padding-bottom:56px}
.deco{position:absolute;z-index:1;right:-130px;top:-120px;opacity:var(--deco)}
.label{font-size:36px;font-weight:600;letter-spacing:-0.01em;color:var(--sub)}
.kicker{font-size:32px;font-weight:600;letter-spacing:-0.004em;color:var(--sub);display:flex;align-items:center;gap:14px}
.kicker i{display:block;width:14px;height:14px;border-radius:50%;background:var(--mark)}
.count{font-size:30px;font-weight:500;color:var(--sub);font-variant-numeric:tabular-nums}
.h1{font-weight:600;letter-spacing:-0.038em;line-height:.97;color:var(--head)}
.h2{font-weight:600;letter-spacing:-0.03em;line-height:1.02;color:var(--head)}
.lede{font-weight:500;letter-spacing:-0.016em;line-height:1.2;color:var(--sub)}
.body{font-weight:400;letter-spacing:-0.006em;line-height:1.3}
.b{font-weight:600}
mark{background:var(--hl);color:var(--hlt);padding:0 .14em;border-radius:.12em;-webkit-box-decoration-break:clone}
.tnum{font-variant-numeric:tabular-nums lining-nums}
.foot{flex:0 0 auto;display:flex;justify-content:space-between;align-items:center;position:relative;z-index:2}
.brand{display:flex;align-items:center;gap:14px;font-size:30px;font-weight:500;letter-spacing:-0.01em;color:var(--sub)}
.swipe{display:flex;align-items:center;gap:14px;font-size:30px;font-weight:600;letter-spacing:-0.01em;
       background:var(--hl);color:var(--hlt);padding:16px 26px 16px 30px;border-radius:999px}
.rule{height:4px;background:var(--rule);border-radius:2px}
"""


def esc(t):
    """Escape text but keep the small HTML we allow: <br>, <b>, <mark>, &nbsp;, &ndash;."""
    t = html.escape(t, quote=False)
    for tag in ("br", "b", "/b", "mark", "/mark"):
        t = t.replace(f"&lt;{tag}&gt;", f"<{tag}>")
    return re.sub(r"&amp;(#\d+|[a-z]+);", r"&\1;", t)  # keep entities such as &nbsp; &ndash; &#39;


def arrow(color, w=34):
    return (f'<svg width="{w}" height="{w}" viewBox="0 0 34 34"><path d="M6 17 H27 M19 9 L27 17 L19 25" fill="none" '
            f'stroke="{color}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def check(color, ring, w=46):
    return (f'<svg width="{w}" height="{w}" viewBox="0 0 46 46"><circle cx="23" cy="23" r="20" fill="none" stroke="{ring}" '
            f'stroke-width="3"/><path d="M14 23.5 L20.5 30 L32 17" fill="none" stroke="{color}" stroke-width="4" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>')


# ------------------------------------------------------------------ slide templates
# Each returns (inner_html, extra_css, align). Text fields may use <br>, <b>, <mark> and &nbsp;.
# The inner block sits in .mid, which fills the slide between the top line and the footer.

def bookmark(color, w=64):
    return (f'<svg width="{w}" height="{w}" viewBox="0 0 64 64"><path d="M17 9 H47 V56 L32 44 L17 56 Z" fill="none" '
            f'stroke="{color}" stroke-width="5" stroke-linejoin="round"/></svg>')


def plane(color, w=64):
    return (f'<svg width="{w}" height="{w}" viewBox="0 0 64 64"><path d="M8 30 L56 9 L41 56 L31 36 Z M31 36 L56 9" fill="none" '
            f'stroke="{color}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/></svg>')


def t_cover(s, c):
    sub = f'<p class="lede" style="font-size:{s.get("sub_size", 46)}px;margin-top:44px;max-width:880px">{esc(s["sub"])}</p>' if s.get("sub") else ""
    return (f'<h1 class="h1" style="font-size:{s.get("size", 148)}px">{esc(s["title"])}</h1>{sub}', "", "end")


def t_statement(s, c):
    num = (f'<div class="badge tnum">{esc(s["num"])}</div>') if s.get("num") else ""
    label = f'<p class="label" style="margin-bottom:30px">{esc(s["label"])}</p>' if s.get("label") else ""
    body = f'<p class="body" style="font-size:{s.get("body_size", 50)}px;margin-top:48px;max-width:900px">{esc(s["body"])}</p>' if s.get("body") else ""
    css = """.badge{width:132px;height:132px;border-radius:50%;background:var(--hl);color:var(--hlt);display:flex;align-items:center;
justify-content:center;font-size:72px;font-weight:600;letter-spacing:-0.04em;margin-bottom:56px}"""
    return (f'{num}{label}<h2 class="h2" style="font-size:{s.get("size", 100)}px">{esc(s["title"])}</h2>{body}', css, "center")


def t_timeline(s, c):
    rows = []
    for st in s["steps"]:
        on = st.get("on")
        dot = (f'<span class="dot" style="background:{"var(--hl)" if on else "var(--bg)"};'
               f'border-color:{"var(--hl)" if on else "var(--fg)"}"></span>')
        rows.append(f'<div class="st">{dot}<div><p class="when tnum">{esc(st["when"])}</p>'
                    f'<p class="what">{esc(st["what"])}</p>'
                    + (f'<p class="more">{esc(st["more"])}</p>' if st.get("more") else "") + "</div></div>")
    css = """
.tl{position:relative;margin-top:72px;display:flex;flex-direction:column;gap:64px}
.tl:before{content:"";position:absolute;left:25px;top:34px;bottom:40px;width:5px;background:var(--rule)}
.st{position:relative;display:grid;grid-template-columns:56px 1fr;gap:40px}
.dot{display:block;width:56px;height:56px;border-radius:50%;border:6px solid;margin-top:4px;position:relative;z-index:1}
.when{font-size:38px;font-weight:600;color:var(--sub);letter-spacing:-0.01em}
.what{font-size:66px;font-weight:600;letter-spacing:-0.03em;line-height:1.04;margin-top:8px}
.more{font-size:44px;line-height:1.28;margin-top:14px;opacity:.88}
"""
    return (f'<h2 class="h2" style="font-size:{s.get("size", 88)}px">{esc(s["title"])}</h2><div class="tl">{"".join(rows)}</div>', css, "center")


def t_compare(s, c):
    def col(side, hl):
        items = "".join(f'<li>{esc(t)}</li>' for t in side["items"])
        return f'<div class="card{" on" if hl else ""}"><p class="ch">{esc(side["head"])}</p><ul>{items}</ul></div>'
    css = """
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-top:70px}
.card{border:5px solid var(--fg);border-radius:34px;padding:46px 38px 50px}
.card.on{background:var(--hl);border-color:var(--hl);color:var(--hlt)}
.ch{font-size:54px;font-weight:600;letter-spacing:-0.026em;line-height:1.04;padding-bottom:30px;margin-bottom:34px;border-bottom:5px solid currentColor}
.card ul{list-style:none;display:flex;flex-direction:column;gap:34px}
.card li{font-size:46px;font-weight:500;line-height:1.2;letter-spacing:-0.014em}
"""
    note = f'<p class="body" style="font-size:40px;margin-top:44px;color:var(--sub)">{esc(s["note"])}</p>' if s.get("note") else ""
    return (f'<h2 class="h2" style="font-size:{s.get("size", 88)}px">{esc(s["title"])}</h2>'
            f'<div class="cmp">{col(s["left"], False)}{col(s["right"], True)}</div>{note}', css, "center")


def t_bignum(s, c):
    css = """
.big{font-size:244px;font-weight:600;letter-spacing:-0.06em;line-height:.86;color:var(--head);white-space:nowrap}
.bigl{font-size:80px;font-weight:600;letter-spacing:-0.034em;line-height:1.04;margin-top:40px}
"""
    lines = "".join(f'<p class="body" style="font-size:48px;margin-top:24px">{esc(t)}</p>' for t in s.get("lines", []))
    label = f'<p class="label" style="margin-bottom:54px">{esc(s["label"])}</p>' if s.get("label") else ""
    return (f'{label}<p class="big tnum">{esc(s["num"])}</p><p class="bigl">{esc(s["caption"])}</p>'
            f'<div class="rule" style="margin:64px 0 22px"></div>{lines}', css, "center")


def t_checklist(s, c):
    f = FIELDS[c["slide_field"]]
    items = "".join(f'<li>{check(f[1], f[5], 58)}<span>{esc(t)}</span></li>' for t in s["items"])
    css = """
.ck{list-style:none;margin-top:72px;display:flex;flex-direction:column;gap:52px}
.ck li{display:grid;grid-template-columns:58px 1fr;gap:34px;align-items:start;font-size:60px;font-weight:500;
       letter-spacing:-0.022em;line-height:1.14}
.ck svg{margin-top:6px}
"""
    note = f'<p class="body" style="font-size:42px;margin-top:70px;color:var(--sub)">{esc(s["note"])}</p>' if s.get("note") else ""
    return (f'<h2 class="h2" style="font-size:{s.get("size", 92)}px">{esc(s["title"])}</h2><ul class="ck">{items}</ul>{note}', css, "center")


def t_swaps(s, c):
    n = len(s["rows"])
    old, new, gap = (40, 50, 30) if n >= 5 else (44, 56, 40)
    rows = "".join(f'<div class="sw"><p class="old">{esc(a)}</p><div class="new">{arrow("currentColor", 40)}<span>{esc(b)}</span></div></div>'
                   for a, b in s["rows"])
    css = f"""
.sws{{margin-top:56px;display:flex;flex-direction:column;gap:{gap}px}}
.sw{{padding-bottom:{gap - 4}px;border-bottom:4px solid var(--rule)}}
.sw:last-child{{border-bottom:0;padding-bottom:0}}
.old{{font-size:{old}px;font-weight:500;color:var(--sub);text-decoration:line-through;text-decoration-thickness:3px}}
.new{{display:flex;align-items:center;gap:20px;margin-top:12px;font-size:{new}px;font-weight:600;letter-spacing:-0.022em;line-height:1.1}}
"""
    return (f'<h2 class="h2" style="font-size:{s.get("size", 88)}px">{esc(s["title"])}</h2><div class="sws">{rows}</div>', css, "center")


def t_list(s, c):
    items = "".join(f'<li><span class="n tnum">{i}</span><span>{esc(t)}</span></li>' for i, t in enumerate(s["items"], 1))
    css = """
.ls{list-style:none;margin-top:70px;display:flex;flex-direction:column;gap:50px}
.ls li{display:grid;grid-template-columns:84px 1fr;gap:16px;align-items:baseline;font-size:58px;font-weight:500;
       letter-spacing:-0.022em;line-height:1.15}
.ls .n{font-size:48px;font-weight:600;color:var(--sub)}
"""
    note = f'<p class="body" style="font-size:42px;margin-top:66px;color:var(--sub)">{esc(s["note"])}</p>' if s.get("note") else ""
    return (f'<h2 class="h2" style="font-size:{s.get("size", 92)}px">{esc(s["title"])}</h2><ul class="ls">{items}</ul>{note}', css, "center")


def t_sources(s, c):
    items = "".join(f'<li><p class="sn">{esc(a)}</p><p class="sp">{esc(b)}</p></li>' for a, b in s["items"])
    css = """
.src{list-style:none;margin-top:64px;display:flex;flex-direction:column;gap:36px}
.src li{padding-bottom:34px;border-bottom:4px solid var(--rule)}
.sn{font-size:50px;font-weight:600;letter-spacing:-0.022em;line-height:1.1}
.sp{font-size:40px;color:var(--sub);margin-top:8px;line-height:1.25}
"""
    note = (f'<p class="body" style="font-size:40px;margin-top:52px;color:var(--sub)">'
            f'{esc(s.get("note", "Education, not medical advice. If shedding is sudden, patchy or lasts more than six months, see a dermatologist."))}</p>')
    return (f'<h2 class="h2" style="font-size:{s.get("size", 78)}px">{esc(s.get("title", "Where this comes from"))}</h2>'
            f'<ul class="src">{items}</ul>{note}', css, "center")


def t_cta(s, c):
    f = FIELDS[c["slide_field"]]
    css = """
.ctr{display:grid;grid-template-columns:84px 1fr;gap:34px;align-items:start}
.cta1{font-size:128px;font-weight:600;letter-spacing:-0.042em;line-height:.97;color:var(--head)}
.cta2{font-size:72px;font-weight:600;letter-spacing:-0.03em;line-height:1.04}
.ctr svg{margin-top:14px}
.guide{margin-top:96px;padding-top:50px;border-top:5px solid var(--rule)}
.g1{font-size:46px;font-weight:600;letter-spacing:-0.018em}
.g2{font-size:46px;color:var(--sub);margin-top:10px}
"""
    return (f'<div class="ctr">{bookmark(f[2], 84)}<p class="cta1">{esc(s.get("title", "Save this<br>for later."))}</p></div>'
            f'<div class="ctr" style="margin-top:64px">{plane(f[1], 84)}<p class="cta2">{esc(s.get("line", "Send it to someone<br>who needs it."))}</p></div>'
            f'<div class="guide"><p class="g1">{esc(s.get("guide", "The free Month-Three Guide"))}</p>'
            f'<p class="g2">{esc(s.get("where", "getaftergrow.com"))}</p></div>', css, "center")


TEMPLATES = dict(cover=t_cover, statement=t_statement, timeline=t_timeline, compare=t_compare, bignum=t_bignum,
                 checklist=t_checklist, swaps=t_swaps, list=t_list, sources=t_sources, cta=t_cta)


def slide_field(c, s, i, n):
    """Covers and the last slide use the carousel's hero field; the middle uses the inside field."""
    if s.get("field"):
        return s["field"]
    if i == 0 or s["t"] == "cta":
        return c["field"]
    return c.get("inside", "porcelain")


# Reels are 1080 x 1920. Instagram's buttons, caption and audio label cover the bottom of the screen and the
# account name sits at the top, so the slide content lives in the band between them.
REEL_H = 1920
REEL_CSS = """html,body{height:1920px}.s{height:1920px;padding:250px 88px 540px}
.deco{top:60px}"""


def build_slide(c, i, fmt="feed"):
    s, n = c["slides"][i], len(c["slides"])
    fld = slide_field(c, s, i, n)
    c = dict(c, slide_field=fld)
    bg, fg, head, sub, mark, rule, hl, hlt = FIELDS[fld]
    inner, css, align = TEMPLATES[s["t"]](s, c)
    deco_op = {"butter": ".09", "espresso": ".10", "porcelain": ".06", "white": ".06"}[fld]
    deco = f'<div class="deco">{part(560, mark)}</div>' if i == 0 else ""
    kicker = f'<p class="kicker"><i></i>{esc(c["kicker"])}</p>'
    right = f'<div class="swipe">Swipe {arrow(hlt, 30)}</div>' if i == 0 else (f'<div class="count">{i + 1} / {n}</div>' if i < n - 1 else "")
    if fmt == "reel":
        css, right = css + REEL_CSS, ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{font_css()}{CSS}{css}</style></head><body>
<div class="s" style="--bg:{bg};--fg:{fg};--head:{head};--sub:{sub};--mark:{mark};--rule:{rule};--hl:{hl};--hlt:{hlt};--deco:{deco_op}">
{deco}<div class="top">{kicker}</div>
<div class="mid{' end' if align == 'end' else ''}">{inner}</div>
<div class="foot"><div class="brand">{part(42, mark)}<span>getaftergrow.com</span></div>{right}</div>
</div></body></html>"""


def plain(t):
    t = re.sub(r"<br\s*/?>", " ", t)
    t = re.sub(r"<[^>]+>", "", t).replace("&nbsp;", " ").replace("&ndash;", "-")
    return re.sub(r"\s+", " ", t).strip()


def slide_text(s):
    """All words on a slide, for alt text and for the banned-word check."""
    out = []
    def walk(v):
        if isinstance(v, str): out.append(v)
        elif isinstance(v, (list, tuple)): [walk(x) for x in v]
        elif isinstance(v, dict): [walk(x) for k, x in v.items() if k not in ("t", "field", "on", "size", "top", "sub_size", "body_size")]
    walk({k: v for k, v in s.items() if k not in ("t", "field", "size", "top", "sub_size", "body_size")})
    return plain(" ".join(x for x in out if isinstance(x, str)))


SOURCES_NOTE = "Education, not medical advice. If shedding is sudden, patchy or lasts more than six months, see a dermatologist."


def alt_for(s):
    """What a screen reader should hear for one slide, including the words a template adds by default."""
    p = lambda t: html.unescape(plain(t))
    end = lambda t: t if t[-1:] in ".?!:" else t + "."
    t = s["t"]
    if t == "cover":
        out = [end(p(s["title"]))] + ([p(s["sub"])] if s.get("sub") else [])
    elif t == "statement":
        head = (f"{p(s['num'])}. " if s.get("num") else "") + (f"{p(s['label'])}: " if s.get("label") else "")
        out = [head + end(p(s["title"]))] + ([p(s["body"])] if s.get("body") else [])
    elif t == "timeline":
        out = [end(p(s["title"]))] + [f"{p(x['when'])}: {end(p(x['what']))}" + (f" {p(x['more'])}" if x.get("more") else "")
                                     for x in s["steps"]]
    elif t == "compare":
        out = [end(p(s["title"]))] + [f"{p(x['head'])}: " + "; ".join(p(i) for i in x["items"]) + "."
                                     for x in (s["left"], s["right"])]
    elif t == "bignum":
        out = [(f"{p(s['label'])}: " if s.get("label") else "") + f"{p(s['num'])} {end(p(s['caption']))}"] + [p(x) for x in s.get("lines", [])]
    elif t == "checklist":
        out = [p(s["title"]) + ":"] + [p(i) for i in s["items"]] + ([p(s["note"])] if s.get("note") else [])
    elif t == "swaps":
        out = [end(p(s["title"]))] + [f"Instead of {p(a)[0].lower() + p(a)[1:]}: {end(p(b))}" for a, b in s["rows"]]
    elif t == "list":
        out = [p(s["title"]) + ":"] + [f"{i}. {p(x)}" for i, x in enumerate(s["items"], 1)] + ([p(s["note"])] if s.get("note") else [])
    elif t == "sources":
        out = [p(s.get("title", "Where this comes from")) + ":"] + [f"{p(a)}, {end(p(b))}" for a, b in s["items"]] + [p(s.get("note", SOURCES_NOTE))]
    elif t == "cta":
        out = [p(s.get("title", "Save this for later.")), p(s.get("line", "Send it to someone who needs it.")),
               f"{p(s.get('guide', 'The free Month-Three Guide'))} is at {p(s.get('where', 'getaftergrow.com'))}."]
    else:
        out = [html.unescape(slide_text(s))]
    return re.sub(r"(\d)-(\d)", r"\1 to \2", " ".join(x for x in out if x))


def alt_texts(c):
    n = len(c["slides"])
    return [f"Slide {i + 1} of {n}. {alt_for(s)}"[:1000] for i, s in enumerate(c["slides"])]


def load(only=None):
    out = []
    for f in sorted(ROOT.glob("carousels_*.py")):
        m = importlib.import_module(f.stem)
        out += [c for c in m.CAROUSELS if not only or c["id"] in only]
    return out


def render(out_dir, only=None):
    from playwright.sync_api import sync_playwright
    from PIL import Image
    out = pathlib.Path(out_dir)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        for c in load(only):
            d = out / c["id"]
            d.mkdir(parents=True, exist_ok=True)
            for i in range(len(c["slides"])):
                pg.set_content(build_slide(c, i), wait_until="load")
                pg.evaluate("document.fonts.ready")
                pg.wait_for_timeout(80)
                png = pg.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
                im = Image.open(io.BytesIO(png)).convert("RGB").resize((OUT_W, OUT_H), Image.LANCZOS)
                im.save(d / f"{c['id']}_{i + 1:02d}.jpg", "JPEG", quality=90, optimize=True, progressive=True)
            print("rendered", c["id"], len(c["slides"]), "slides")
        br.close()


RAW = "https://raw.githubusercontent.com/domin8commerce/aftergrow/main/"
IG_CAPTION_MAX = 2200
IG_HASHTAG_MAX = 5  # Instagram's limit since December 2025
IG_SLIDES_MAX = 20


def link(c, network, kind="post"):
    """The tracked landing-page link, so Shopify can attribute the visit to the network, topic, post and format."""
    return (f"https://getaftergrow.com{c['page']}?utm_source={network}&utm_medium=social"
            f"&utm_campaign={c['pillar']}&utm_content={c['id']}{'-reel' if kind == 'reel' else ''}")


# The Instagram bio link goes to /products/scalp-serum today (Shopify sessions, utm_content=link_in_bio), so the
# caption sends people to the profile without promising what the link holds. When George adds the Month-Three
# Guide to the bio links, switch to: "The free Month-Three Guide is at the link in our bio."
BIO_LINE = "Follow @getaftergrow for more hair care, explained simply."


def ig_text(c):
    """Instagram caption: the copy, one line that sends people to the profile, then at most 5 hashtags."""
    return c["ig"] + "\n\n" + c.get("bio_line", BIO_LINE) + "\n\n" + " ".join("#" + h for h in c["hashtags"])


def media_urls(c):
    return [f"{RAW}ig/{c['id']}/{c['id']}_{i + 1:02d}.jpg" for i in range(len(c["slides"]))]


def validate(only=None):
    """Brand and platform rules for every carousel. Prints problems and returns how many there are."""
    from queue_build import banned_hits, style_hits, LIVE_PAGES
    problems, seen = [], set()
    for c in load(only):
        cid = c["id"]
        if cid in seen: problems.append(f"{cid}: duplicate id")
        seen.add(cid)
        for k in ("pillar", "kicker", "field", "page", "slides", "hashtags", "ig", "fb", "fb_comment"):
            if not c.get(k): problems.append(f"{cid}: missing {k}")
        if c.get("page") not in LIVE_PAGES: problems.append(f"{cid}: page {c.get('page')} is not in LIVE_PAGES")
        if not 3 <= len(c["slides"]) <= IG_SLIDES_MAX: problems.append(f"{cid}: {len(c['slides'])} slides")
        if c["slides"][0]["t"] != "cover" or c["slides"][-1]["t"] != "cta": problems.append(f"{cid}: needs a cover first and the CTA last")
        for i, s in enumerate(c["slides"], 1):
            if s["t"] not in TEMPLATES: problems.append(f"{cid} slide {i}: unknown template {s['t']}")
            words = slide_text(s) + " " + plain(c["kicker"])
            for h in banned_hits(words) + style_hits(words, "image"):
                problems.append(f"{cid} slide {i}: {h}")
        for i, a in enumerate(alt_texts(c), 1):
            if re.search(r"&(#\d+|[a-z]+);|<", a): problems.append(f"{cid} alt text {i}: leftover HTML")
            if len(a) < 30: problems.append(f"{cid} alt text {i}: too short")
            for h in banned_hits(a) + style_hits(a, "image"):
                problems.append(f"{cid} alt text {i}: {h}")
        tags = c["hashtags"]
        if len(tags) > IG_HASHTAG_MAX: problems.append(f"{cid}: {len(tags)} hashtags, the limit is {IG_HASHTAG_MAX}")
        if len(set(tags)) != len(tags): problems.append(f"{cid}: repeated hashtag")
        for h in tags:
            if not re.fullmatch(r"[a-z0-9]+", h): problems.append(f"{cid}: hashtag '{h}' must be lowercase letters and numbers")
        for name, text in (("ig", ig_text(c)), ("fb", c["fb"]), ("fb_comment", c["fb_comment"].format(link=link(c, "facebook")))):
            for h in banned_hits(text) + style_hits(text, "description"):
                problems.append(f"{cid} {name}: {h}")
        if len(ig_text(c)) > IG_CAPTION_MAX: problems.append(f"{cid}: Instagram caption is {len(ig_text(c))} characters")
        if "{link}" not in c["fb_comment"]: problems.append(f"{cid}: fb_comment has no {{link}}")
        if "first comment" not in c["fb"]: problems.append(f"{cid}: the Facebook caption should point to the first comment")
        if "http" in c["ig"] or "http" in c["fb"]: problems.append(f"{cid}: links go in the bio (Instagram) or the first comment (Facebook)")
    for p in problems: print("PROBLEM", p)
    print("problems:", len(problems) or "none")
    return len(problems)


if __name__ == "__main__":
    if sys.argv[1:2] == ["check"]:
        sys.exit(1 if validate(set(sys.argv[2:]) or None) else 0)
    render(sys.argv[1], set(sys.argv[2:]) or None)
