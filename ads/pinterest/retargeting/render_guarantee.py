"""Render the retargeting guarantee pin (R1) at 2000 x 3000 (2:3, 2x), saved as JPEG.

Photo: ads/pinterest/search-lab/AG_A_runway_cover.jpg (cover frame of the Runway video).
Copy checked against getaftergrow.com/pages/the-90-day-guarantee on Oct 30, 2026:
"Ninety days to decide." / "If you don't love how your hair looks, email us and we refund your first order."
Claim "Within 120 days of delivery"; "Shipping costs are not refunded"; one guarantee per customer.

Usage: python3 -I render_guarantee.py   (run from this folder)
"""
import base64, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "engine"))
from pinengine import font_css, part  # brand font (Schibsted Grotesk) and The Part mark

from PIL import Image
from playwright.sync_api import sync_playwright

ESP, STO = "#33241D", "#5E544D"
BG = "#ECDFCE"  # sampled from the photo's left edge

photo_path = HERE.parent / "search-lab" / "AG_A_runway_cover.jpg"
photo = "data:image/jpeg;base64," + base64.b64encode(photo_path.read_bytes()).decode()

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{font_css()}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1000px;height:1500px;background:{BG}}}
body{{font-family:'SG','Helvetica Neue',Arial,sans-serif;-webkit-font-smoothing:antialiased;font-kerning:normal;
     text-rendering:geometricPrecision;color:{ESP}}}
.pin{{position:relative;width:1000px;height:1500px;overflow:hidden}}
.photo{{position:absolute;left:300px;top:60px;width:799px;height:1421px;background:url({photo}) 0 0/799px 1421px no-repeat;
       -webkit-mask-image:linear-gradient(to right,transparent 0,#000 230px),
                          linear-gradient(to bottom,transparent 0,#000 90px,#000 1320px,transparent 100%);
       -webkit-mask-composite:source-in;mask-composite:intersect}}
.col{{position:absolute;left:80px;top:92px;width:450px;z-index:2}}
.eyebrow{{font-weight:600;font-size:24px;letter-spacing:.16em;color:{STO}}}
.h1{{margin-top:26px;font-weight:600;font-size:106px;letter-spacing:-0.04em;line-height:.95}}
.deck{{margin-top:30px;font-weight:600;font-size:38px;letter-spacing:-0.02em;line-height:1.14}}
.fine{{position:absolute;left:80px;width:430px;bottom:132px;z-index:2;font-weight:400;font-size:22px;line-height:1.32;color:{STO}}}
.brand{{position:absolute;z-index:2;left:80px;bottom:58px;display:flex;align-items:center;gap:14px;
       font-weight:500;font-size:28px;letter-spacing:-0.01em;color:{STO}}}
</style></head><body><div class="pin">
<div class="photo"></div>
<div class="col">
<p class="eyebrow">THE 90-DAY GUARANTEE</p>
<h1 class="h1">Ninety<br>days to<br>decide.</h1>
<p class="deck">Don&rsquo;t love how your hair looks? We refund your first order.</p>
</div>
<p class="fine">Claim within 120 days of delivery. Shipping isn&rsquo;t refunded. One per customer.</p>
<div class="brand">{part(44, ESP)}<span>getaftergrow.com</span></div>
</div></body></html>"""

png = HERE / "_render.png"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1000, "height": 1500}, device_scale_factor=2)
    pg.set_content(html, wait_until="load")
    pg.wait_for_timeout(300)
    pg.screenshot(path=str(png))
    b.close()
img = Image.open(png).convert("RGB")
img.save(HERE / "AG_C_guarantee_2000x3000.jpg", quality=92, optimize=True, progressive=True)
png.unlink()
img.resize((236, 354), Image.LANCZOS).save(HERE / "preview_236.png")  # feed-size check; not committed
print("AG_C_guarantee_2000x3000.jpg", img.size)
