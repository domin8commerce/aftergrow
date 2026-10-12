"""Aftergrow Reels v2: short, animated, hook-first Reels for Instagram and Facebook.

A Reel is a script of scenes (engine/reels_*.py). Every frame is drawn by headless Chromium from one HTML page whose
render(t) function places every element for time t, so the motion is exact and repeatable:
  - the hook is readable on the very first frame, and the rest of it rises in within half a second;
  - lines rise in one after another, key words get a highlighter sweep, checkmarks draw themselves;
  - scenes swipe left, and a thin bar at the top shows how much is left;
  - all text stays inside the band Instagram leaves clear (account name on top, caption and buttons at the bottom).
1080 x 1920, 30 fps, H.264. The soundtrack in the file is our own (Facebook plays it); on Instagram the post uses a
track from Instagram's library instead, with the video's own sound turned off.

Usage (from the repo root):
  python3 -I engine/reel2.py check [IDs]              brand and format rules for every Reel script
  python3 -I engine/reel2.py render <out_dir> [IDs]    writes <ID>.mp4 and <ID>_cover.jpg
  python3 -I engine/reel2.py frames <out_dir> <ID>     a contact sheet of frames, for review
"""
import hashlib, html, importlib, io, json, pathlib, re, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from pinengine import font_css, part, ESP, BUT, WHI, POR, STO, SAN, SIL  # noqa: E402

W, H, FPS = 1080, 1920, 30
T_SWIPE = 0.32      # scene-to-scene swipe, seconds
REVEAL = 0.5        # one element rising in, seconds
SR = 44100

FIELDS = {  # background, text, headline, secondary, mark color, rule, highlight fill, highlight text
    "butter": (BUT, ESP, ESP, STO, ESP, "rgba(51,36,29,.18)", ESP, BUT),
    "espresso": (ESP, WHI, BUT, SAN, BUT, "rgba(243,226,160,.22)", BUT, ESP),
    "porcelain": (POR, ESP, ESP, STO, ESP, "rgba(51,36,29,.13)", BUT, ESP),
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:#000}
body{font-family:'SG','Helvetica Neue',Arial,sans-serif;-webkit-font-smoothing:antialiased;font-kerning:normal;
     text-rendering:geometricPrecision}
.scene{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden;background:var(--bg);color:var(--fg);
       will-change:transform}
.kick{position:absolute;left:88px;top:270px;font-size:34px;font-weight:600;letter-spacing:-0.006em;color:var(--sub);
      display:flex;align-items:center;gap:14px}
.kick i{display:block;width:14px;height:14px;border-radius:50%;background:var(--mark)}
.box{position:absolute;left:88px;top:350px;width:860px;height:1010px;display:flex;flex-direction:column;justify-content:center}
.foot{position:absolute;left:88px;top:1376px;display:flex;align-items:center;gap:14px;font-size:30px;font-weight:500;
      letter-spacing:-0.01em;color:var(--sub)}
.deco{position:absolute;right:-150px;top:150px;opacity:var(--deco);will-change:transform}
.r{will-change:transform,opacity}
.mk{position:relative;display:inline-block;white-space:nowrap;margin:0 -.1em}
.mka,.mkb{display:inline-block;padding:0 .1em;border-radius:.12em}
.mkb{position:absolute;left:0;top:0;color:var(--hlt);clip-path:inset(0 100% 0 0);
     background:linear-gradient(to bottom,transparent 0,transparent 13%,var(--hl) 13%,var(--hl) 97%,transparent 97%)}
.hook{font-weight:700;letter-spacing:-0.045em;line-height:.98;color:var(--head)}
.hook .ln{display:block;white-space:nowrap}
.sub{font-size:48px;font-weight:500;letter-spacing:-0.016em;line-height:1.22;color:var(--sub);margin-top:48px}
.label{font-size:38px;font-weight:600;letter-spacing:-0.01em;color:var(--sub);margin-bottom:28px}
.title{font-weight:700;letter-spacing:-0.035em;line-height:1.02;color:var(--head)}
.body{font-size:56px;font-weight:400;letter-spacing:-0.012em;line-height:1.28;margin-top:40px}
.src{font-size:32px;font-weight:500;color:var(--sub);margin-top:46px;display:flex;align-items:center;gap:12px}
.src:before{content:"";display:block;width:34px;height:4px;border-radius:2px;background:var(--sub);opacity:.7}
.badge{width:120px;height:120px;border-radius:50%;background:var(--hl);color:var(--hlt);display:flex;align-items:center;
       justify-content:center;font-size:64px;font-weight:700;letter-spacing:-0.04em;margin-bottom:48px}
.big{font-size:250px;font-weight:700;letter-spacing:-0.06em;line-height:.86;color:var(--head);white-space:nowrap}
.bigcap{font-size:84px;font-weight:700;letter-spacing:-0.035em;line-height:1.04;margin-top:34px}
.items{list-style:none;display:flex;flex-direction:column;gap:46px;margin-top:64px}
.items li{display:grid;grid-template-columns:72px 1fr;gap:28px;align-items:start;font-size:60px;font-weight:600;
          letter-spacing:-0.025em;line-height:1.12}
.items .n{font-size:52px;font-weight:700;color:var(--sub);line-height:1.25}
.items svg{margin-top:2px}
.tl{position:relative;margin-top:70px;display:flex;flex-direction:column;gap:62px}
.tl .rail{position:absolute;left:27px;top:30px;width:6px;border-radius:3px;background:var(--rule)}
.tl .railfill{position:absolute;left:27px;top:30px;width:6px;border-radius:3px;background:var(--mark)}
.st{position:relative;display:grid;grid-template-columns:60px 1fr;gap:38px}
.st .dot{display:block;width:60px;height:60px;border-radius:50%;border:7px solid var(--fg);background:var(--bg);
         position:relative;z-index:1;margin-top:2px}
.st .when{font-size:38px;font-weight:600;color:var(--sub);letter-spacing:-0.01em}
.st .what{font-size:66px;font-weight:700;letter-spacing:-0.03em;line-height:1.05;margin-top:6px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:70px}
.card{border:6px solid var(--fg);border-radius:38px;padding:44px 36px 50px;min-height:430px}
.card.on{background:var(--hl);border-color:var(--hl);color:var(--hlt)}
.card .ch{font-size:56px;font-weight:700;letter-spacing:-0.03em;line-height:1.02;padding-bottom:28px;margin-bottom:30px;
          border-bottom:5px solid currentColor}
.card p{font-size:54px;font-weight:600;letter-spacing:-0.02em;line-height:1.12}
.sw{padding:30px 0;border-bottom:5px solid var(--rule)}
.sw:last-child{border-bottom:0}
.sw .old{position:relative;display:inline-block;font-size:44px;font-weight:500;color:var(--sub)}
.sw .old .strike{position:absolute;left:0;top:52%;height:5px;border-radius:3px;background:var(--sub);width:0}
.sw .new{display:flex;align-items:center;gap:22px;margin-top:14px;font-size:60px;font-weight:700;letter-spacing:-0.028em;
         line-height:1.08}
.cta1{font-size:132px;font-weight:700;letter-spacing:-0.045em;line-height:.97;color:var(--head)}
.cta2{font-size:72px;font-weight:700;letter-spacing:-0.032em;line-height:1.05}
.ctarow{display:grid;grid-template-columns:92px 1fr;gap:32px;align-items:start}
.ctarow svg{margin-top:16px}
.follow{display:inline-flex;align-self:flex-start;align-items:center;gap:16px;margin-top:84px;font-size:46px;font-weight:700;
        letter-spacing:-0.02em;background:var(--hl);color:var(--hlt);padding:22px 36px 24px;border-radius:999px}
.fine{font-size:30px;font-weight:500;color:var(--sub);margin-top:44px}
#bar{position:absolute;left:88px;top:226px;width:904px;height:8px;border-radius:4px;overflow:hidden;z-index:10}
#bar i{display:block;height:100%;width:0;border-radius:4px}
"""


def esc(t):
    """Escape text but keep the small HTML we allow: <br>, <b>, <mark>, and entities such as &nbsp;."""
    t = html.escape(t, quote=False)
    for tag in ("br", "b", "/b", "mark", "/mark"):
        t = t.replace(f"&lt;{tag}&gt;", f"<{tag}>")
    t = re.sub(r"&amp;(#\d+|[a-z]+);", r"&\1;", t)
    return re.sub(r"<mark>(.*?)</mark>", r'<span class="mk"><span class="mka">\1</span><span class="mkb">\1</span></span>', t)


def plain(t):
    t = re.sub(r"<br\s*/?>", " ", t)
    t = re.sub(r"<[^>]+>", "", t).replace("&nbsp;", " ").replace("&ndash;", "-").replace("&#8209;", "-")
    return html.unescape(re.sub(r"\s+", " ", t)).strip()


def tick(color, ring, w=66):
    return (f'<svg width="{w}" height="{w}" viewBox="0 0 66 66"><circle cx="33" cy="33" r="29" fill="none" stroke="{ring}" '
            f'stroke-width="4.5"/><path class="tk" d="M20 34 L29.5 43.5 L47 24" fill="none" stroke="{color}" stroke-width="6.5" '
            f'stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>')


def arrow(color, w=46):
    return (f'<svg width="{w}" height="{w}" viewBox="0 0 34 34"><path d="M6 17 H27 M19 9 L27 17 L19 25" fill="none" '
            f'stroke="{color}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def bookmark(color, w=92):
    return (f'<svg width="{w}" height="{w}" viewBox="0 0 64 64"><path d="M17 9 H47 V56 L32 44 L17 56 Z" fill="none" '
            f'stroke="{color}" stroke-width="5" stroke-linejoin="round"/></svg>')


def plane(color, w=92):
    return (f'<svg width="{w}" height="{w}" viewBox="0 0 64 64"><path d="M8 30 L56 9 L41 56 L31 36 Z M31 36 L56 9" fill="none" '
            f'stroke="{color}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/></svg>')


# ------------------------------------------------------------------ scenes
# Each builder returns inner HTML. Elements with class "r" rise in, in document order; <mark> sweeps after its line.

def s_hook(s, f):
    lines = "".join(f'<span class="ln r">{esc(x)}</span>' for x in s["lines"])
    sub = f'<p class="sub r">{esc(s["sub"])}</p>' if s.get("sub") else ""
    return f'<h1 class="hook fit" data-max="{s.get("size", 150)}">{lines}</h1>{sub}'


def s_say(s, f):
    out = ""
    if s.get("num"):
        out += f'<div class="badge r">{esc(s["num"])}</div>'
    if s.get("label"):
        out += f'<p class="label r">{esc(s["label"])}</p>'
    n = len(plain(s["title"]))
    size = s.get("size") or (112 if n <= 28 else 100 if n <= 44 else 88 if n <= 64 else 78)
    out += f'<h2 class="title r fit" data-max="{size}">{esc(s["title"])}</h2>'
    if s.get("body"):
        out += f'<p class="body r">{esc(s["body"])}</p>'
    if s.get("source"):
        out += f'<p class="src r">{esc(s["source"])}</p>'
    return out


def s_big(s, f):
    out = f'<p class="label r">{esc(s["label"])}</p>' if s.get("label") else ""
    out += f'<div class="big r fit" data-max="{s.get("size", 250)}">{esc(s["num"])}</div>'
    cap = f' style="font-size:{s["capsize"]}px"' if s.get("capsize") else ""   # to keep a caption's lines whole
    out += f'<p class="bigcap r"{cap}>{esc(s["caption"])}</p>'
    if s.get("body"):
        out += f'<p class="body r">{esc(s["body"])}</p>'
    if s.get("source"):
        out += f'<p class="src r">{esc(s["source"])}</p>'
    return out


def s_checks(s, f):
    items = "".join(f'<li class="r">{tick(f[1], f[5])}<span>{esc(x)}</span></li>' for x in s["items"])
    src = f'<p class="src r">{esc(s["source"])}</p>' if s.get("source") else ""
    return f'<h2 class="title r fit" data-max="{s.get("size", 96)}">{esc(s["title"])}</h2><ul class="items">{items}</ul>{src}'


def s_list(s, f):
    items = "".join(f'<li class="r"><span class="n">{i}</span><span>{esc(x)}</span></li>' for i, x in enumerate(s["items"], 1))
    src = f'<p class="src r">{esc(s["source"])}</p>' if s.get("source") else ""
    return f'<h2 class="title r fit" data-max="{s.get("size", 96)}">{esc(s["title"])}</h2><ul class="items">{items}</ul>{src}'


def s_steps(s, f):
    rows = "".join(f'<div class="st r"><span class="dot"></span><div><p class="when">{esc(w)}</p>'
                   f'<p class="what">{esc(x)}</p></div></div>' for w, x in s["steps"])
    return (f'<h2 class="title r fit" data-max="{s.get("size", 96)}">{esc(s["title"])}</h2>'
            f'<div class="tl"><span class="rail"></span><span class="railfill"></span>{rows}</div>')


def s_vs(s, f):
    def card(c, on):
        return f'<div class="card r{" on" if on else ""}"><p class="ch">{esc(c[0])}</p><p>{esc(c[1])}</p></div>'
    src = f'<p class="src r">{esc(s["source"])}</p>' if s.get("source") else ""
    return (f'<h2 class="title r fit" data-max="{s.get("size", 96)}">{esc(s["title"])}</h2>'
            f'<div class="vs">{card(s["left"], False)}{card(s["right"], True)}</div>{src}')


def s_swaps(s, f):
    rows = "".join(f'<div class="sw r"><span class="old">{esc(a)}<span class="strike"></span></span>'
                   f'<div class="new">{arrow("currentColor")}<span>{esc(b)}</span></div></div>' for a, b in s["rows"])
    src = f'<p class="src r">{esc(s["source"])}</p>' if s.get("source") else ""
    return f'<h2 class="title r fit" data-max="{s.get("size", 96)}">{esc(s["title"])}</h2><div style="margin-top:40px">{rows}</div>{src}'


def s_cta(s, f):
    line1 = s.get("title", "Save this<br>for later.")
    line2 = s.get("line", "Send it to someone who needs&nbsp;it.")
    return (f'<div class="ctarow r">{bookmark(f[2])}<p class="cta1 fit" data-max="132">{esc(line1)}</p></div>'
            f'<div class="ctarow r" style="margin-top:62px">{plane(f[1])}<p class="cta2">{esc(line2)}</p></div>'
            f'<div class="follow r">Follow @getaftergrow</div>'
            f'<p class="fine r">Education, not medical advice.</p>')


SCENES = dict(hook=s_hook, say=s_say, big=s_big, checks=s_checks, list=s_list, steps=s_steps, vs=s_vs, swaps=s_swaps,
              cta=s_cta)


def scene_words(s, everything=False):
    """The words a viewer has to read in a scene (the small source line is a glance, not a read).
    everything=True also returns the source and label lines, for the banned-word check."""
    skip = ("t", "field", "size", "dur") + (() if everything else ("source",))
    out = []
    def walk(v):
        if isinstance(v, str): out.append(v)
        elif isinstance(v, (list, tuple)): [walk(x) for x in v]
        elif isinstance(v, dict): [walk(x) for k, x in v.items() if k not in skip]
    walk({k: v for k, v in s.items() if k not in skip})
    return plain(" ".join(out))


def reveal_count(s):
    t = s["t"]
    n = {"hook": len(s.get("lines", [])) + (1 if s.get("sub") else 0),
         "checks": 1 + len(s.get("items", [])), "list": 1 + len(s.get("items", [])),
         "steps": 1 + len(s.get("steps", [])), "vs": 3, "swaps": 1 + len(s.get("rows", [])), "cta": 4}.get(t)
    if n is None:
        n = sum(1 for k in ("num", "label", "title", "body", "caption") if s.get(k)) + (1 if t == "big" else 0)
    return n + (1 if s.get("source") else 0)


def duration(s, i):
    """Seconds on screen, including the swipe out: time to read it at about 3.4 words a second, plus the reveals."""
    words = len(re.findall(r"[A-Za-z0-9']+", scene_words(s)))
    if s["t"] == "hook":
        return round(min(3.2, 1.7 + words * 0.11), 2)
    if s["t"] == "cta":
        return 3.0
    d = 0.5 + reveal_count(s) * 0.18 + words / 4.0
    return round(min(4.4, max(2.4, d)), 2)


def scene_field(r, s, i, n):
    if s.get("field"):
        return s["field"]
    return r["field"] if (i == 0 or s["t"] == "cta") else "porcelain"


def timeline(r):
    durs = [s.get("dur") or duration(s, i) for i, s in enumerate(r["scenes"])]
    starts, acc = [], 0.0
    for d in durs:
        starts.append(round(acc, 3))
        acc += d
    return starts, durs, round(acc, 3)


JS = r"""
const T = %(swipe)s, R = %(reveal)s, TOTAL = %(total)s, FIELDS = %(fields)s;
const easeOut = x => 1 - Math.pow(1 - x, 3);
const easeIO = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const cl = x => Math.max(0, Math.min(1, x));
let S = [];
function fits(el, box) {
  box.style.justifyContent = 'flex-start';
  const ok = el.scrollWidth <= 862 && box.scrollHeight <= 1012;
  box.style.justifyContent = '';
  return ok;
}
function fit() {
  document.querySelectorAll('.fit').forEach(el => {
    let size = +el.dataset.max; el.style.fontSize = size + 'px';
    const box = el.closest('.box');
    while (size > 40 && !fits(el, box)) { size -= 2; el.style.fontSize = size + 'px'; }
  });
}
function setup() {
  fit();
  S = [...document.querySelectorAll('.scene')].map((el, i) => {
    const start = +el.dataset.start, dur = +el.dataset.dur, first = i === 0;
    const items = [...el.querySelectorAll('.r')].map((x, k) => {
      // the whole hook is readable on frame one; the highlighter and the sub-line bring the motion
      let at = first ? (x.classList.contains('ln') ? -9 : 0.45) : 0.04 + k * 0.2;
      if (x.tagName === 'LI' || x.classList.contains('st') || x.classList.contains('sw')) at += 0.12 * k;
      return {el: x, at};
    });
    const marks = [...el.querySelectorAll('.mkb')].map(m => {
      const host = items.find(it => it.el.contains(m));
      return {el: m, at: first ? 0.2 : (host ? host.at : 0) + 0.38};
    });
    const ticks = [...el.querySelectorAll('.tk')].map(p => {
      const host = items.find(it => it.el.contains(p)); return {el: p, at: (host ? host.at : 0) + 0.3};
    });
    const strikes = [...el.querySelectorAll('.strike')].map(p => {
      const host = items.find(it => it.el.contains(p)); return {el: p, at: (host ? host.at : 0) + 0.32};
    });
    const dots = [...el.querySelectorAll('.st .dot')].map(p => {
      const host = items.find(it => it.el.contains(p)); return {el: p, at: (host ? host.at : 0) + 0.25};
    });
    const tl = el.querySelector('.tl'), fill = el.querySelector('.railfill'), rail = el.querySelector('.rail');
    let railH = 0;
    if (tl) { const rows = tl.querySelectorAll('.st'); const last = rows[rows.length - 1];
      railH = last.offsetTop + 30 - 30; rail.style.height = railH + 'px'; }
    return {el, start, dur, items, marks, ticks, strikes, dots, fill, railH, deco: el.querySelector('.deco'),
            box: el.querySelector('.box'), first};
  });
}
function render(t) {
  const last = S.length - 1;
  let cur = 0;
  S.forEach((sc, i) => {
    const s = sc.start, e = s + sc.dur;
    let x = 0;
    if (i > 0 && t < s - T) x = 1;
    else if (i > 0 && t < s) x = 1 - easeIO((t - (s - T)) / T);
    else if (i < last && t >= e) x = -1;
    else if (i < last && t >= e - T) x = -easeIO((t - (e - T)) / T);
    sc.el.style.transform = 'translateX(' + (x * 100) + '%%)';
    sc.el.style.visibility = (x <= -1 || x >= 1) ? 'hidden' : 'visible';
    if (t >= s - T / 2) cur = i;
    const lt = t - s;
    sc.items.forEach(it => { const q = easeOut(cl((lt - it.at) / R));
      it.el.style.opacity = q; it.el.style.transform = 'translateY(' + ((1 - q) * 46) + 'px)'; });
    sc.marks.forEach(m => { m.el.style.clipPath = 'inset(0 ' + ((1 - easeOut(cl((lt - m.at) / 0.45))) * 100) + '%% 0 0)'; });
    sc.ticks.forEach(k => { k.el.style.strokeDashoffset = 1 - easeOut(cl((lt - k.at) / 0.35)); });
    sc.strikes.forEach(k => { k.el.style.width = (easeOut(cl((lt - k.at) / 0.35)) * 100) + '%%'; });
    sc.dots.forEach(k => { const on = cl((lt - k.at) / 0.25);
      k.el.style.background = on > 0.5 ? 'var(--mark)' : 'var(--bg)'; k.el.style.borderColor = on > 0.5 ? 'var(--mark)' : 'var(--fg)'; });
    if (sc.fill) { const last = sc.dots.length ? sc.dots[sc.dots.length - 1].at : 0;
      sc.fill.style.height = (sc.railH * easeOut(cl(lt / Math.max(0.3, last)))) + 'px'; }
    if (sc.deco) sc.deco.style.transform = 'rotate(' + (-8 + lt * 5) + 'deg) scale(' + (1.02 - 0.02 * cl(lt / 2)) + ')';
    if (sc.first && sc.box) sc.box.style.transform = 'scale(' + (1.03 - 0.03 * easeOut(cl(lt / 1.6))) + ')';
  });
  const f = FIELDS[cur];
  const bar = document.getElementById('bar');
  bar.style.background = f[0]; bar.firstChild.style.background = f[1];
  bar.firstChild.style.width = (cl(t / TOTAL) * 100) + '%%';
}
"""


def build_html(r):
    starts, durs, total = timeline(r)
    n = len(r["scenes"])
    layers, bars = [], []
    for i, s in enumerate(r["scenes"]):
        fld = scene_field(r, s, i, n)
        f = FIELDS[fld]
        bg, fg, head, sub, mark, rule, hl, hlt = f
        inner = SCENES[s["t"]](s, f)
        deco = f'<div class="deco">{part(620, mark)}</div>' if i == 0 else ""
        deco_op = {"butter": ".10", "espresso": ".11", "porcelain": ".06"}[fld]
        kicker = f'<p class="kick"><i></i>{esc(r["kicker"])}</p>'
        layers.append(
            f'<div class="scene" data-start="{starts[i]}" data-dur="{durs[i]}" style="--bg:{bg};--fg:{fg};--head:{head};'
            f'--sub:{sub};--mark:{mark};--rule:{rule};--hl:{hl};--hlt:{hlt};--deco:{deco_op}">{deco}{kicker}'
            f'<div class="box">{inner}</div>'
            f'<div class="foot">{part(40, mark)}<span>getaftergrow.com</span></div></div>')
        bars.append([rule, mark])
    js = JS % dict(swipe=T_SWIPE, reveal=REVEAL, total=total, fields=json.dumps(bars))
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{font_css()}{CSS}</style></head><body>'
            f'{"".join(layers)}<div id="bar"><i></i></div><script>{js}</script></body></html>'), starts, durs, total


# ------------------------------------------------------------------ soundtrack (Facebook plays it; Instagram swaps in library music)
def _hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


CHORDS = [[53, 60, 64, 67, 72],   # F major 9 (F C E G C)
          [50, 57, 60, 65, 69],   # D minor 9-ish (D A C F A)
          [46, 53, 57, 62, 65],   # B-flat major 7 (Bb F A D F)
          [48, 55, 60, 62, 67]]   # C sus 2 (C G C D G)


def soundtrack(starts, total, seed, bpm=82):
    """Warm chords that change on every scene, a soft pulse, light plucks and a whoosh on every swipe."""
    import numpy as np
    from scipy.signal import butter, fftconvolve, sosfilt
    rng = np.random.default_rng(seed)
    n = int((total + 2.5) * SR)
    t = np.arange(n) / SR
    pad = np.zeros(n)
    bass = np.zeros(n)
    pluck = np.zeros((n, 2))
    perc = np.zeros(n)
    bounds = list(starts) + [total + 2.0]
    for k in range(len(starts)):
        notes = CHORDS[k % len(CHORDS)]
        a, b = bounds[k], bounds[k + 1]
        i0, i1 = int(max(0, a - 0.05) * SR), min(n, int((b + 0.6) * SR))
        tt = t[i0:i1] - a
        env = np.clip((tt + 0.05) / 0.35, 0, 1) * np.clip((b + 0.6 - a - tt) / 0.6, 0, 1)
        for m in notes:
            for det in (-0.0019, 0.0019):
                ph = rng.uniform(0, 2 * np.pi)
                f0 = _hz(m) * (1 + det)
                pad[i0:i1] += env * (np.sin(2 * np.pi * f0 * tt + ph) + 0.18 * np.sin(4 * np.pi * f0 * tt + ph)) * 0.032
        bass[i0:i1] += env * np.sin(2 * np.pi * _hz(notes[0] - 12) * tt) * 0.17
    beat = 60.0 / bpm
    for j in range(int(total / (beat / 2)) + 2):
        tb = j * beat / 2
        b0 = int(tb * SR)
        if b0 >= n:
            break
        k = max(0, sum(1 for s in starts if s <= tb) - 1)
        notes = CHORDS[k % len(CHORDS)]
        if j % 2 == 0:  # a soft kick on the beat
            m = min(n - b0, int(0.32 * SR))
            kt = np.arange(m) / SR
            freq = 48 + 70 * np.exp(-kt / 0.035)
            perc[b0:b0 + m] += np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-kt / 0.11) * (0.34 if j % 4 == 0 else 0.22)
        m = min(n - b0, int(0.05 * SR))  # a quiet shaker on every eighth
        perc[b0:b0 + m] += rng.standard_normal(m) * np.exp(-np.arange(m) / SR / 0.010) * (0.022 if j % 2 else 0.012)
        if rng.random() < 0.55:  # a light pluck from the chord
            f0 = _hz(rng.choice(notes[1:]) + 12)
            m = min(n - b0, int(1.4 * SR))
            pt = np.arange(m) / SR
            tone = (np.sin(2 * np.pi * f0 * pt) + 0.32 * np.sin(4 * np.pi * f0 * pt) + 0.08 * np.sin(6 * np.pi * f0 * pt))
            tone *= np.exp(-pt / 0.42) * np.minimum(1, pt / 0.003) * rng.uniform(0.045, 0.07)
            pan = rng.uniform(0.3, 0.7)
            pluck[b0:b0 + m, 0] += tone * (1 - pan) * 2
            pluck[b0:b0 + m, 1] += tone * pan * 2
    whoosh = np.zeros(n)
    for s in starts[1:]:
        a = s - T_SWIPE - 0.12
        i0 = int(max(0, a) * SR)
        m = min(n - i0, int(0.62 * SR))
        wt = np.arange(m) / SR
        noise = rng.standard_normal(m)
        env = np.sin(np.pi * np.clip(wt / 0.62, 0, 1)) ** 2
        lo = sosfilt(butter(2, [500, 2600], "band", fs=SR, output="sos"), noise)
        hi = sosfilt(butter(2, [2600, 7000], "band", fs=SR, output="sos"), noise)
        mixw = np.clip(wt / 0.62, 0, 1)
        whoosh[i0:i0 + m] += (lo * (1 - mixw) + hi * mixw) * env * 0.11
    pad = sosfilt(butter(2, 3800, "low", fs=SR, output="sos"), pad)
    kick = sosfilt(butter(2, 180, "low", fs=SR, output="sos"), perc)       # the kick lives below 180 Hz
    shaker = sosfilt(butter(2, [5500, 9500], "band", fs=SR, output="sos"), perc)
    tonal = np.stack([pad + bass] * 2, axis=1) + pluck                      # only the tonal parts get reverb,
    ir_t = np.arange(int(2.2 * SR)) / SR                                     # so the noise never smears into hiss
    wet = np.stack([fftconvolve(tonal[:, c], rng.standard_normal(len(ir_t)) * np.exp(-ir_t / 0.7), mode="full")[:n]
                    for c in (0, 1)], axis=1)
    wet *= np.abs(tonal).max() / (np.abs(wet).max() + 1e-9)
    dry = tonal * 0.82 + wet * 0.3 + np.stack([kick + shaker + whoosh] * 2, axis=1)
    mix = dry[:int(total * SR)]
    fi, fo = int(0.05 * SR), int(1.2 * SR)
    mix[:fi] *= np.linspace(0, 1, fi)[:, None]
    mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return mix / (np.abs(mix).max() + 1e-9) * 0.89


# ------------------------------------------------------------------ rendering
def load(only=None):
    out = []
    for f in sorted(ROOT.glob("reels_*.py")):
        m = importlib.import_module(f.stem)
        out += [r for r in m.REELS if not only or r["id"] in only]
    return out


def _open_page(pw, r):
    br = pw.chromium.launch()
    pg = br.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    doc, starts, durs, total = build_html(r)
    pg.set_content(doc, wait_until="load")
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(120)
    pg.evaluate("setup()")
    return br, pg, starts, durs, total


def make(r, out_dir):
    from playwright.sync_api import sync_playwright
    from scipy.io import wavfile
    import numpy as np
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp, sync_playwright() as pw:
        tmp = pathlib.Path(tmp)
        br, pg, starts, durs, total = _open_page(pw, r)
        seed = int(hashlib.sha1(r["id"].encode()).hexdigest()[:8], 16)
        wavfile.write(tmp / "a.wav", SR, (soundtrack(starts, total, seed) * 32767).astype(np.int16))
        frames = int(round(total * FPS))
        enc = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
             "-i", str(tmp / "a.wav"), "-filter_complex", "[1:a]loudnorm=I=-14:TP=-1.5:LRA=7[a]", "-map", "0:v", "-map", "[a]",
             "-c:v", "libx264", "-preset", "slow", "-tune", "animation", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p",
             "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-ac", "2", "-movflags", "+faststart",
             "-t", f"{total:.3f}", str(out_dir / f"{r['id']}.mp4")], stdin=subprocess.PIPE)
        for k in range(frames):
            pg.evaluate(f"render({k / FPS:.4f})")
            enc.stdin.write(pg.screenshot(type="png", clip={"x": 0, "y": 0, "width": W, "height": H}))
        enc.stdin.close()
        if enc.wait() != 0:
            raise SystemExit(f"{r['id']}: ffmpeg failed")
        pg.evaluate(f"render({max(0.0, durs[0] - T_SWIPE - 0.08):.3f})")  # the hook, fully built: the cover
        from PIL import Image
        Image.open(io.BytesIO(pg.screenshot(type="png"))).convert("RGB").save(out_dir / f"{r['id']}_cover.jpg", "JPEG",
                                                                                quality=92, optimize=True)
        br.close()
    return total


def frames_sheet(r, out_png, cols=6, thumb=270):
    """Frames at the middle of every scene, at the first frame and halfway through each swipe."""
    from playwright.sync_api import sync_playwright
    from PIL import Image
    with sync_playwright() as pw:
        br, pg, starts, durs, total = _open_page(pw, r)
        times = [0.0, 0.25]
        for s, d in zip(starts, durs):
            times += [s + 0.3, s + d * 0.75]
        times += [s - T_SWIPE / 2 for s in starts[1:2]]
        ims = []
        for tm in times:
            pg.evaluate(f"render({tm:.3f})")
            ims.append(Image.open(io.BytesIO(pg.screenshot(type="png"))).convert("RGB").resize((thumb, int(thumb * H / W))))
        br.close()
    rows = (len(ims) + cols - 1) // cols
    th = int(thumb * H / W)
    sheet = Image.new("RGB", (cols * (thumb + 10) + 10, rows * (th + 10) + 10), (40, 40, 40))
    for i, im in enumerate(ims):
        sheet.paste(im, (10 + (i % cols) * (thumb + 10), 10 + (i // cols) * (th + 10)))
    sheet.save(out_png)
    return times, total


# ------------------------------------------------------------------ checks
IG_HASHTAG_MAX = 5


def ig_text(r):
    return r["ig"] + "\n\n" + r.get("follow", "Follow @getaftergrow for more hair care, explained simply.") + "\n\n" + \
        " ".join("#" + h for h in r["hashtags"])


def validate(only=None):
    from queue_build import banned_hits, style_hits, LIVE_PAGES
    problems, seen = [], set()
    for r in load(only):
        rid = r["id"]
        if rid in seen: problems.append(f"{rid}: duplicate id")
        seen.add(rid)
        for k in ("pillar", "kicker", "field", "page", "scenes", "hashtags", "ig", "fb", "fb_comment"):
            if not r.get(k): problems.append(f"{rid}: missing {k}")
        if r.get("page") not in LIVE_PAGES: problems.append(f"{rid}: page {r.get('page')} is not in LIVE_PAGES")
        sc = r["scenes"]
        if sc[0]["t"] != "hook" or sc[-1]["t"] != "cta": problems.append(f"{rid}: needs a hook first and the CTA last")
        starts, durs, total = timeline(r)
        if not 12 <= total <= 24: problems.append(f"{rid}: {total} seconds; keep Reels between 12 and 24")
        hook_words = len(re.findall(r"[A-Za-z0-9']+", plain(" ".join(sc[0]["lines"]))))
        if hook_words > 10: problems.append(f"{rid}: the hook has {hook_words} words; 10 at most")
        for ln in sc[0]["lines"]:
            if len(plain(ln)) > 16: problems.append(f"{rid}: hook line '{plain(ln)}' is over 16 characters, so the type gets small")
        for i, s in enumerate(sc, 1):
            if s["t"] not in SCENES: problems.append(f"{rid} scene {i}: unknown type {s['t']}")
            words = scene_words(s, everything=True) + " " + plain(r["kicker"])
            if len(re.findall(r"[A-Za-z0-9']+", scene_words(s))) > 26: problems.append(f"{rid} scene {i}: over 26 words")
            for h in banned_hits(words) + style_hits(words, "image"):
                problems.append(f"{rid} scene {i}: {h}")
        tags = r["hashtags"]
        if len(tags) > IG_HASHTAG_MAX: problems.append(f"{rid}: {len(tags)} hashtags")
        for h in tags:
            if not re.fullmatch(r"[a-z0-9]+", h): problems.append(f"{rid}: hashtag '{h}'")
        link = f"https://getaftergrow.com{r['page']}"
        for name, text in (("ig", ig_text(r)), ("fb", r["fb"]), ("fb_comment", r["fb_comment"].format(link=link))):
            for h in banned_hits(text) + style_hits(text, "description"):
                problems.append(f"{rid} {name}: {h}")
        if "{link}" not in r["fb_comment"]: problems.append(f"{rid}: fb_comment has no {{link}}")
        if "first comment" not in r["fb"]: problems.append(f"{rid}: the Facebook caption should point to the first comment")
        if "http" in r["ig"] or "http" in r["fb"]: problems.append(f"{rid}: no links in captions")
    for p in problems: print("PROBLEM", p)
    print("problems:", len(problems) or "none")
    return len(problems)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["check"]:
        sys.exit(1 if validate(set(a[1:]) or None) else 0)
    if a[:1] == ["frames"]:
        r = load({a[2]})[0]
        times, total = frames_sheet(r, pathlib.Path(a[1]) / f"{r['id']}_frames.png")
        print(r["id"], total, "seconds; frames at", [round(x, 2) for x in times])
        sys.exit(0)
    if a[:1] == ["render"]:
        for r in load(set(a[2:]) or None):
            print(r["id"], make(r, a[1]), "seconds")
        sys.exit(0)
    raise SystemExit(__doc__)
