"""Contact sheet + feed-size thumbnails. Usage: python3 -I sheet.py <dir> <out.png> [col_w] [cols]"""
import sys, pathlib
from PIL import Image

d = pathlib.Path(sys.argv[1])
out = sys.argv[2]
col_w = int(sys.argv[3]) if len(sys.argv) > 3 else 380
cols = int(sys.argv[4]) if len(sys.argv) > 4 else 5
files = sorted(d.glob("aftergrow_pin_*.png"), key=lambda f: f.name)
order = sys.argv[5].split(",") if len(sys.argv) > 5 else None
if order:
    files = [f for o in order for f in files if f"_{o}_" in f.name]
g = 24
row_h = int(col_w * 1.5)
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * col_w + (cols + 1) * g, rows * row_h + (rows + 1) * g), (255, 255, 255))
for i, f in enumerate(files):
    im = Image.open(f).convert("RGB").resize((col_w, row_h), Image.LANCZOS)
    r, c = divmod(i, cols)
    sheet.paste(im, (g + c * (col_w + g), g + r * (row_h + g)))
sheet.save(out)
print(out, sheet.size, len(files))
