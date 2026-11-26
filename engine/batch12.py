"""Batch 12 (2026-11-26): the three haircut/hairstyle/over-50 articles are still unpublished (Shopify checked
2026-11-26) and make-hair-look-thicker is at its cap. Two older Journal articles were verified today through the
Shopify connector and added to LIVE_PAGES: how-fast-does-hair-grow (a new page for Haircuts and Hairstyles for thin
hair: growth rate, length stuck because ends break) and seasonal-hair-shedding (Thinning hair, in season now).
Haircut/hairstyle boards first: the last two thin-hairline-styling slots (braids, what a new cut can and can't do),
two from how-fast-does-hair-grow and one static/flyaways angle from how-to-tame-flyaways. Then dry scalp in season
from why-scalp-care-matters (dandruff that won't go away, shampoo on the scalp). Then two seasonal shedding pins.
Every fact is on the linked page.
Usage: python3 -I batch12.py <out_dir> [ID ...]"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pinengine as E
import batch2  # noqa: F401  (registers the 15 batch-2 layouts)
from queue_build import L, J, THIN, STYLE, CUTS, DRY

HL = J + "thin-hairline-styling"
GROW = J + "how-fast-does-hair-grow"
FLY = J + "how-to-tame-flyaways"
WSC = J + "why-scalp-care-matters"
SEAS = J + "seasonal-hair-shedding"

PINS = [
    dict(id="T01", slug="braids-on-thin-hair-3-rules", field="butter", arch="list2", h_size=110,
         headline="Braids on<br>thin hair?", item_size=50, gap=56,
         items=["Choose thicker braids<br>and keep them short.",
                "Take them out within<br>6 to 8 weeks.",
                "After a tight style: loose<br>braids or natural hair<br>for a few months."],
         note="If it hurts, it’s too tight. Source: AAD."),
    dict(id="T02", slug="new-cut-thinner-hairline-look-not-cause", field="white", arch="split", h_size=100, band_h=470,
         split_top=150, marks=False, headline="A new cut for<br>a thinner<br>hairline?",
         left=("Changes", ["The look: cut,<br>color, spray,<br>fiber powder"]),
         right=("Rarely reaches", ["The cause:<br>see a<br>dermatologist"]),
         item_size=54, foot="It’s never too early to ask (AAD)."),
    dict(id="T03", slug="how-much-hair-grows-in-a-year", field="porcelain", arch="grid4", h_size=110,
         headline="How much hair<br>grows in a year?", label_size=54, cell_h=300, grid_top=96,
         cells=[dict(label="1 month", sub="About half an inch."),
                dict(label="3 months", sub="About 1.5 inches."),
                dict(label="6 months", sub="About 3 inches."),
                dict(label="12 months", sub="About 6 inches.")],
         foot="At about half an inch a month (MedlinePlus). Speed varies. Trims take some away."),
    dict(id="T04", slug="stuck-at-one-length-ends-breaking", field="espresso", arch="contrast", h_size=104,
         headline="Hair stuck at<br>one length?",
         defs=[("At the root", "Hair can keep<br>growing."),
               ("At the ends", "They can snap off<br>just as fast."),
               ("Keep your length", "Conditioner, a gentle<br>comb, less heat.")],
         tip="Habit tips: AAD."),
    dict(id="T05", slug="leave-in-for-static-and-flyaways", field="butter", arch="definition", h_size=104,
         headline="Static and<br>flyaways on<br>fine hair?",
         terms=[("A leave-in", "can diminish frizz,<br>static and flyaways"),
                ("How", "damp hair, a small amount,<br>mid strands to ends")],
         sum="Fine, straight hair:", sum2="a lighter leave-in (AAD)."),
    dict(id="T06", slug="flakes-that-wont-go-away-3-signs", field="white", arch="checklist", h_size=104,
         headline="Flakes that<br>won’t go away?",
         items=["Dandruff won’t go away,<br>or it’s severe.", "Changing your hair care<br>hasn’t helped.",
                "You’re worried<br>about thinning."],
         note="See a board-certified dermatologist."),
    dict(id="T07", slug="shampoo-your-scalp-not-the-length", field="porcelain", arch="swap", h_size=116,
         headline="Shampoo<br>your scalp.", band_h=470, list_top=250,
         rows=[("Rubbing it into the length", "Put it on your scalp"),
               ("Washing less for flakes", "Regular washing usually<br>helps mild dandruff"),
               ("A fixed wash schedule", "Wash as hair gets oily")]),
    dict(id="T08", slug="seasonal-shedding-two-studies", field="espresso", arch="definition", h_size=100,
         headline="Shedding more<br>after summer?",
         terms=[("Two studies", "most resting hairs in<br>summer or early autumn"),
                ("Resting hairs", "are the ones<br>that shed next")],
         sum="Neither study summary", sum2="gives a number of weeks."),
    dict(id="T09", slug="seasonal-shed-or-something-else", field="butter", arch="checklist", h_size=100,
         headline="Seasonal shed<br>or something<br>else?",
         items=["Look back a few months<br>for a trigger.", "Check the hairs: short<br>ones may be broken.",
                "Compare photos,<br>not memory."],
         note="Not easing, or past 6 months? Ask a dermatologist."),
]

# id, slug, board, title, description, link, alt
COPY = [
    ("T01", PINS[0]["slug"], STYLE, "Hairstyles for thin hair and braids: 3 rules from dermatologists",
     "Hairstyles for thin hair and braids: the AAD suggests thicker braids kept short, taken out within 6 to 8 weeks, and after a tight style, loose braids or natural hair for a few months. A painful style is too tight. Read how to style around a thinner hairline.",
     L(HL, "hairstyles", "T01"), "List of three braid rules for thin hair: thicker braids kept short, out within 6 to 8 weeks, and after a tight style, loose braids or natural hair for a few months."),
    ("T02", PINS[1]["slug"], CUTS, "Haircuts for a thinning hairline: what a new cut can and can’t do",
     "Haircuts for a thinning hairline change the look, and so can color, colored sprays and fiber powder. The AAD says changing where the scalp shows rarely gets to the cause, and it’s never too early to see a dermatologist. Read how to style around it.",
     L(HL, "haircuts", "T02"), "Split card: a new cut, color, spray or fiber powder changes the look of a thinner hairline; the cause needs a dermatologist."),
    ("T03", PINS[2]["slug"], CUTS, "Haircuts for thin hair: how much hair grows in 3, 6 and 12 months",
     "Haircuts for thin hair, planned ahead: at about half an inch a month (MedlinePlus), hair grows about 1.5 inches in 3 months, 3 in 6 months and 6 in a year. That’s simple arithmetic, not a measurement, and trims take some away. Read more.",
     L(GROW, "haircuts", "T03"), "Grid of hair growth at about half an inch a month: half an inch in 1 month, 1.5 inches in 3, 3 inches in 6, 6 inches in 12."),
    ("T04", PINS[3]["slug"], STYLE, "Hairstyles for thin hair stuck at one length? The ends may be breaking",
     "Hairstyles for thin hair stuck at one length? Hair can keep growing at the root while the ends break off just as fast. The AAD lists conditioner after washing, gentle combing with a wide-tooth comb and less heat to keep the length you have. Read more.",
     L(GROW, "hairstyles", "T04"), "Card: hair can keep growing at the root while the ends can snap off just as fast; keep your length with conditioner, a gentle comb and less heat."),
    ("T05", PINS[4]["slug"], STYLE, "Hairstyles for thin hair full of static? What a leave-in does",
     "Hairstyles for thin hair full of static? The AAD says a leave-in conditioner can diminish frizz, static and flyaway strands. Use the smallest amount on damp hair, mid strands to ends, off the scalp, and wash it out within a week. Read more.",
     L(FLY, "hairstyles", "T05"), "Definition card: a leave-in can diminish frizz, static and flyaways; use a small amount on damp hair from mid strands to ends; fine, straight hair needs a lighter one."),
    ("T06", PINS[5]["slug"], DRY, "Dry scalp flakes that won’t go away? 3 signs to see a dermatologist",
     "Dry scalp flakes that won’t go away? See a board-certified dermatologist if dandruff doesn’t go away or is severe, if changing your hair care doesn’t help, or if you’re worried about thinning. Read why scalp care matters.",
     L(WSC, "dry-scalp", "T06"), "Checklist of three signs to see a dermatologist about flakes: dandruff that won’t go away or is severe, changing hair care hasn’t helped, worry about thinning."),
    ("T07", PINS[6]["slug"], DRY, "Flakes or buildup? Put shampoo on your scalp, not the length",
     "Flakes or buildup? The AAD says shampoo on the scalp washes away built-up products, dead skin and excess oil, while rubbing it into the length can damage hair. Regular washing usually helps mild dandruff. Read why scalp care matters.",
     L(WSC, "dry-scalp", "T07"), "Swap list: rubbing shampoo into the length becomes putting it on the scalp; washing less for flakes becomes regular washing, which usually helps mild dandruff; a fixed schedule becomes washing as hair gets oily."),
    ("T08", PINS[7]["slug"], THIN, "Hair shedding after summer? What two studies found about the seasons",
     "Hair shedding more after summer? Two studies found the most resting hairs, the ones that shed next, in summer or early autumn. Neither study summary gives a number of weeks for a seasonal shed. If it doesn’t ease, ask a dermatologist. Read more.",
     L(SEAS, "thinning", "T08"), "Definition card: two studies found the most resting hairs in summer or early autumn; resting hairs shed next; neither study summary gives a number of weeks."),
    ("T09", PINS[8]["slug"], THIN, "Seasonal hair shedding or something else? 3 checks first",
     "Seasonal hair shedding? The season alone can’t tell you. Look back a few months for a trigger like illness with a high fever, an operation or lots of stress (AAD), check if short hairs are broken and compare photos. Not easing or past six months? Ask a dermatologist.",
     L(SEAS, "thinning", "T09"), "Checklist: look back a few months for a trigger, check whether short hairs are broken, compare photos not memory; not easing or past 6 months, ask a dermatologist."),
]

if __name__ == "__main__":
    E.PINS = PINS
    E.render(sys.argv[1], set(sys.argv[2:]) or None)
