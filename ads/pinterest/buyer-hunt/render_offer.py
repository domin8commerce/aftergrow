"""Render the Buyer hunt offer pin (90-Day Protocol) at 2000 x 3000 (2:3, 2x).

Source photo: Drive PINTEREST/Aftergrow Scalp Serum Trio (1).png, captured at 1047 px.
Facts checked against getaftergrow.com on Oct 29, 2026: $108 for 3 bottles, "$36 per bottle",
free US standard shipping, "Skip or cancel anytime", "Renews $108 every 3 months until canceled".

Usage: python3 -I render_offer.py   (run from this folder; writes AG_B_offer90_2000x3000.png)
"""
import base64, io, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "engine"))
from pinengine import font_css, part  # brand font (Schibsted Grotesk) and The Part mark

from PIL import Image
from playwright.sync_api import sync_playwright

ESP, STO = "#33241D", "#675E58"
BG = "#F6F9F7"  # sampled from the photo's seamless background

src = Image.open(HERE / "src_trio_1047.png").convert("RGB")
crop = src.crop((60, 262, 987, 985))  # the three bottles and their shadows
buf = io.BytesIO()
crop.save(buf, "PNG")
photo = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{font_css()}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1000px;height:1500px;background:{BG}}}
body{{font-family:'SG','Helvetica Neue',Arial,sans-serif;-webkit-font-smoothing:antialiased;font-kerning:normal;
     text-rendering:geometricPrecision;color:{ESP}}}
.pin{{position:relative;width:1000px;height:1500px;overflow:hidden;padding:88px 80px 0}}
.eyebrow{{font-weight:600;font-size:26px;letter-spacing:.16em;color:{STO}}}
.h1{{margin-top:26px;font-weight:600;font-size:120px;letter-spacing:-0.04em;line-height:.95}}
.deck{{margin-top:26px;font-weight:600;font-size:44px;letter-spacing:-0.02em;line-height:1.12}}
.photo{{position:absolute;left:0;top:520px;width:1000px;height:780px;
       background:url({photo}) center/1000px auto no-repeat;
       -webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 6%,#000 94%,transparent 100%)}}
.fine{{position:absolute;left:80px;right:80px;bottom:132px;font-weight:400;font-size:24px;
      letter-spacing:-0.004em;line-height:1.3;color:{STO}}}
.brand{{position:absolute;left:80px;bottom:58px;display:flex;align-items:center;gap:14px;
       font-weight:500;font-size:28px;letter-spacing:-0.01em;color:{STO}}}
</style></head><body><div class="pin">
<p class="eyebrow">THE 90-DAY PROTOCOL</p>
<h1 class="h1">Three bottles.<br>Ninety days.</h1>
<p class="deck">$36 a bottle, free shipping.<br>Skip or cancel anytime.</p>
<div class="photo"></div>
<p class="fine">Renews at $108 every 3 months until canceled.</p>
<div class="brand">{part(44, ESP)}<span>getaftergrow.com</span></div>
</div></body></html>"""

out = HERE / "AG_B_offer90_2000x3000.png"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1000, "height": 1500}, device_scale_factor=2)
    pg.set_content(html, wait_until="load")
    pg.wait_for_timeout(300)
    pg.screenshot(path=str(out), full_page=False)
    b.close()
img = Image.open(out)
print(out.name, img.size)
img.resize((236, 354), Image.LANCZOS).save(HERE / "preview_236.png")
