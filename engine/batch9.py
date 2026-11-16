"""Batch 9 (2026-11-16): the three haircut/hairstyle/over-50 articles are still unpublished (Shopify checked
2026-11-16) and make-hair-look-thicker is at its 8-pin cap, so Haircuts for thin hair gets nothing new.
Hairstyles for thin hair gets the last unused flyaways angle (heat-protectant leave-ins), Fine thin hair over 50
gets the unused texture angle (gray hair and sun). Dry scalp care still has no unused angle on its live pages.
Then lightly used pages: breakage-or-shedding (white bulb check), head spa season from mid-November
(how-to-clean-your-scalp, hair oiling from types-of-scalp-treatments), and the rosemary trend done honestly
(scalp-serum-or-scalp-oil, no claims about what rosemary does). Every fact is on the linked page.
IDs start at Q01 (P01-P09 clash with old product pins, see RUNBOOK).
Usage: python3 -I batch9.py <out_dir> [ID ...]"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pinengine as E
import batch2  # noqa: F401  (registers the 15 batch-2 layouts)
from queue_build import L, J, THIN, O50, STYLE, SPA, HC

FLY = J + "how-to-tame-flyaways"
TEX = J + "why-has-my-hair-texture-changed"
BRK = J + "breakage-or-shedding"
CLN = J + "how-to-clean-your-scalp"
TYP = J + "types-of-scalp-treatments"
OIL = J + "scalp-serum-or-scalp-oil"

PINS = [
    dict(id="Q01", slug="heat-protectant-leave-in-thin-hair", field="espresso", arch="contrast", h_size=100,
         headline="Heat styling<br>thin hair? Read<br>the leave-in.",
         defs=[("Look for", "“Heat protectant”<br>on the pack."),
               ("Fine hair", "A lighter leave-in,<br>the smallest amount."),
               ("Wash it out", "Within a week.")],
         tip="Source: American Academy<br>of Dermatology."),
    dict(id="Q02", slug="gray-hair-more-easily-damaged-by-sun", field="white", arch="definition", h_size=100,
         headline="Going gray?<br>Sun and weather<br>hit it harder.",
         terms=[("Gray hair", "more easily damaged by<br>weather and sunlight"),
                ("Timing", "when age changes start<br>varies a lot")],
         sum="Source: a 2018 review", sum2="of hair aging."),
    dict(id="Q03", slug="shedding-or-breakage-check-the-end", field="butter", arch="split", h_size=104, band_h=470,
         split_top=150, marks=False, headline="Shedding or<br>breakage? Check<br>the end.",
         left=("Shed hair", ["Usually<br>full length", "A small white<br>bulb at the root"]),
         right=("Broken hair", ["Usually shorter", "No bulb at<br>the end"]),
         item_size=46, foot="Damaged hair tends to break (AAD)."),
    dict(id="Q04", slug="scalp-buildup-what-helps", field="white", arch="grid4", h_size=120,
         headline="Scalp buildup:<br>what helps.", label_size=50, cell_h=320, grid_top=90,
         cells=[dict(label="Skin cells,<br>sweat, oil", sub="Shampoo on<br>the scalp."),
                dict(label="Lots of<br>styling product", sub="Clarify once or<br>twice a month."),
                dict(label="Leave-in on<br>the scalp", sub="Keep it on<br>your hair."),
                dict(label="Dry<br>shampoo", sub="Wash after one<br>or two uses.")],
         foot="Sources: Cleveland Clinic, AAD."),
    dict(id="Q05", slug="how-often-to-wash-your-scalp-by-hair-type", field="espresso", arch="list2", h_size=104,
         headline="How often to<br>wash your scalp.", item_size=54, gap=60,
         items=["It depends on<br>your hair type.", "Straight hair, oily scalp:<br>daily may suit you.",
                "Dry, curly or thick hair:<br>at least every 2 to 3 weeks."],
         note="Source: American Academy of Dermatology."),
    dict(id="Q06", slug="hair-oiling-the-careful-way", field="porcelain", arch="checklist", h_size=104,
         headline="Hair oiling?<br>Keep it off<br>your scalp.",
         items=["Start with<br>dry hair.", "A pea-sized<br>amount.", "Middle to ends,<br>not the scalp.",
                "20 minutes to an hour,<br>then wash it out."],
         note="Cleveland Clinic advises against oil on the scalp."),
    dict(id="Q07", slug="rosemary-extract-oil-or-water", field="porcelain", arch="contrast", h_size=100,
         headline="Rosemary extract,<br>oil or water?", brand_on="espresso",
         defs=[("Extract", "One ingredient in a set<br>formula, with directions."),
               ("Essential oil", "Never neat on skin. Some can<br>cause an allergic reaction."),
               ("Homemade water", "Whoever makes it is<br>responsible for its safety.")],
         tip="Know what you<br>put on your scalp."),
    dict(id="Q08", slug="scalp-serum-or-scalp-oil-4-label-checks", field="butter", arch="list2", h_size=104,
         band_h=430, list_top=150, headline="Scalp serum<br>or scalp oil?", item_size=50, gap=50,
         items=["The base it’s<br>made with.", "The finish it<br>leaves behind.", "Where it’s<br>meant to go.",
                "The directions<br>on the label."],
         note="Compare these four on any label."),
]

# id, slug, board, title, description, link, alt
COPY = [
    ("Q01", PINS[0]["slug"], STYLE, "Hairstyles for thin hair with heat? Some leave-ins say heat protectant",
     "Hairstyles for thin hair often mean a blow-dryer. The AAD says some leave-in conditioners also protect from heat, and the pack says “heat protectant”. Fine, straight hair needs a lighter leave-in; wash it out within a week. Read how to tame flyaways.",
     L(FLY, "hairstyles", "Q01"), "Card: look for heat protectant on a leave-in pack; fine hair needs a lighter leave-in in the smallest amount; wash it out within a week."),
    ("Q02", PINS[1]["slug"], O50, "Fine thin hair over 50 and going gray? Gray hair is more easily damaged by sun",
     "Fine thin hair over 50 and going gray? A 2018 review of hair aging says gray hair is more easily damaged by weather and sunlight. When age changes start varies a lot from person to person. Read why hair texture changes.",
     L(TEX, "over-50", "Q02"), "Definition card: gray hair is more easily damaged by weather and sunlight; when age changes start varies a lot."),
    ("Q03", PINS[2]["slug"], THIN, "Thinning hair: shedding or breakage? Check the end of the hair",
     "Thinning hair: shedding or breakage? Look at the end. A shed hair is usually full length with a small white bulb at the root. A broken hair has no bulb and is usually shorter. Damaged hair is fragile, so it tends to break (AAD). Read more.",
     L(BRK, "thinning", "Q03"), "Split card: a shed hair is usually full length with a small white bulb at the root; a broken hair is usually shorter with no bulb."),
    ("Q04", PINS[3]["slug"], SPA, "Head spa at home: what builds up on your scalp, and what helps",
     "Head spa at home starts with a clean scalp. Skin cells, sweat and oil build up (Cleveland Clinic), and so can styling products. Shampoo on the scalp, clarify once or twice a month if you use lots of product, and wash after one or two dry shampoos (AAD). Read more.",
     L(CLN, "scalp-care", "Q04"), "Grid of four kinds of scalp buildup and what helps: shampoo on the scalp, clarify once or twice a month if you use lots of product, keep leave-in on hair, wash after dry shampoo."),
    ("Q05", PINS[4]["slug"], SPA, "Head spa at home: how often to wash your scalp, by hair type",
     "How often should you wash your scalp? The AAD says it depends on your hair: straight hair with an oily scalp may want a daily shampoo, while dry, textured, curly or thick hair needs it at least once every 2 to 3 weeks. Read how to clean your scalp.",
     L(CLN, "scalp-care", "Q05"), "List: how often to wash your scalp depends on hair type; straight hair with an oily scalp may suit daily; dry, curly or thick hair at least every 2 to 3 weeks."),
    ("Q06", PINS[5]["slug"], SPA, "Hair oiling at home: the careful way, and why to skip your scalp",
     "Hair oiling at home, the careful way: Cleveland Clinic advises against putting oil directly on your scalp. Start with dry hair, use a pea-sized amount from the middle to the ends, leave it 20 minutes to an hour, then wash it out. Read more.",
     L(TYP, "scalp-care", "Q06"), "Checklist for hair oiling: dry hair, a pea-sized amount, middle to ends and not the scalp, 20 minutes to an hour, then wash it out."),
    ("Q07", PINS[6]["slug"], HC, "Rosemary water for hair, rosemary oil or extract: what’s the difference?",
     "Rosemary water for hair, oil or extract? An extract in a finished product is one ingredient in a set formula, with directions. Essential oils shouldn’t go on skin neat, and some can cause an allergic reaction. Homemade water is its maker’s responsibility (FDA). Read more.",
     L(OIL, "ingredients", "Q07"), "Card comparing rosemary extract, one ingredient in a set formula; essential oil, never neat on skin; homemade water, the maker is responsible for safety."),
    ("Q08", PINS[7]["slug"], HC, "Scalp serum or scalp oil? 4 things to compare on the label",
     "Scalp serum or scalp oil? Before you choose, compare four things on each label: the base it is made with, the finish it leaves, where it is meant to go and the directions. Read the full comparison, plus what to know about essential oils.",
     L(OIL, "ingredients", "Q08"), "List of four things to compare on a scalp serum or scalp oil label: the base, the finish, where it goes, the directions."),
]

if __name__ == "__main__":
    E.PINS = PINS
    E.render(sys.argv[1], set(sys.argv[2:]) or None)
