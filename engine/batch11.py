"""Batch 11 (2026-11-23): the three haircut/hairstyle/over-50 articles are still unpublished (Shopify checked
2026-11-23), but thin-hairline-styling went up today (verified through the Shopify connector 2026-11-23). It is
the first new page for Hairstyles for thin hair and Haircuts for thin hair since make-hair-look-thicker hit its
cap, so six pins come from it (hairstyles, haircuts, thinning, over 50). Two dry scalp pins in season from
scalp-serum-for-dry-scalp (winter air, itch-relief products: new angles on that page). One thinning pin from
stress-and-hair-shedding (verified 2026-11-23) and one head spa pin from the unused why-scalp-care-matters
wash-frequency angle. Every fact is on the linked page.
Usage: python3 -I batch11.py <out_dir> [ID ...]"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pinengine as E
import batch2  # noqa: F401  (registers the 15 batch-2 layouts)
from queue_build import L, J, THIN, O50, STYLE, SPA, CUTS, DRY

HL = J + "thin-hairline-styling"
DSS = J + "scalp-serum-for-dry-scalp"
STR = J + "stress-and-hair-shedding"
WSC = J + "why-scalp-care-matters"

PINS = [
    dict(id="S01", slug="if-it-hurts-its-too-tight", field="porcelain", arch="definition", h_size=112,
         headline="If it hurts,<br>it’s too tight.",
         terms=[("Tight styles", "often show early<br>at your hairline"),
                ("So", "loosen it and<br>switch it up")],
         sum="Source: AAD.", sum2="Change it right away."),
    dict(id="S02", slug="style-around-a-thinner-hairline", field="butter", arch="list2", h_size=104,
         headline="Style around a<br>thinner hairline.", item_size=50, gap=56,
         items=["Let the front fall softly:<br>a loose side part or fringe.",
                "Move your part to change<br>where the scalp shows.",
                "Colored spray or fiber<br>powder where it shows."],
         note="Styling changes the look, not the cause."),
    dict(id="S03", slug="soft-fringe-covers-more-hairline", field="espresso", arch="contrast", h_size=100,
         headline="Thin at the front?<br>Let it fall<br>forward.",
         defs=[("Pulled back", "Shows more of<br>the hairline."),
               ("Fringe or side part", "Falls forward and<br>covers more of it."),
               ("Keep it loose", "No pins or tension<br>at the edges.")],
         tip="Still thinning?<br>See a dermatologist."),
    dict(id="S04", slug="signs-your-style-is-too-tight", field="white", arch="checklist", h_size=104,
         headline="Is your style<br>too tight?",
         items=["Short, broken hairs<br>around your forehead.", "Pain from tightly<br>pulled hair.",
                "Thin or bare patches<br>where hair is pulled tight."],
         note="Loosen it and see a dermatologist. Source: AAD."),
    dict(id="S05", slug="hairline-sign-to-get-checked-soon", field="espresso", arch="definition", h_size=100,
         headline="One hairline sign<br>to get checked<br>soon.",
         terms=[("What you see", "a thin band of bare skin<br>along the front and sides"),
                ("Often with", "thinner eyebrows")],
         sum="Usually diagnosed in women<br>after menopause.", sum2="See a dermatologist soon."),
    dict(id="S06", slug="hat-or-scarf-pull-hair-back-loosely", field="porcelain", arch="swap", h_size=116,
         headline="Hat or scarf<br>this winter?", band_h=470, list_top=250,
         rows=[("Hair pulled tight underneath", "Pull it back loosely"),
               ("Any covering", "Silk or satin is gentler"),
               ("Tugging to style it", "Brush only enough to style")]),
    dict(id="S07", slug="dry-scalp-in-winter-air", field="butter", arch="list2", h_size=110,
         headline="Dry scalp<br>in winter?", item_size=50, gap=54,
         items=["Cold, dry air can<br>dry your scalp.", "Run a humidifier<br>at home.",
                "Check your hair products:<br>some can dry the scalp.", "A gentle shampoo,<br>and wash less often."],
         note="Sources: AAD, Cleveland Clinic."),
    dict(id="S08", slug="itch-relief-products-ask-first", field="white", arch="split", h_size=100, band_h=470,
         split_top=150, marks=False, headline="Dry, itchy scalp?<br>Careful with<br>itch relief.",
         left=("Ask first", ["Before you use<br>itch relief"]),
         right=("Why", ["Some can make<br>very dry skin<br>itch more"]),
         item_size=46, foot="Ask your dermatologist. AAD, on dry skin."),
    dict(id="S09", slug="stress-still-going-shedding-can-last", field="butter", arch="contrast", h_size=100,
         headline="Still under<br>stress? A shed<br>can last longer.",
         defs=[("Stress ends", "Shedding stops as the<br>body readjusts."),
               ("Stress stays", "Shedding can be<br>long lived."),
               ("Heavy past 6 months", "See your doctor.")],
         tip="Sources: AAD, British<br>Association of Dermatologists."),
    dict(id="S10", slug="washing-5-to-6-times-a-week-one-study", field="espresso", arch="definition", h_size=104,
         headline="Does washing<br>often hurt<br>your hair?",
         terms=[("One study", "5 to 6 washes a week,<br>no objective harm"),
                ("How you wash", "shampoo on the scalp,<br>not rubbed into the length")],
         sum="Wash as often as hair gets", sum2="dirty or oily (AAD)."),
]

# id, slug, board, title, description, link, alt
COPY = [
    ("S01", PINS[0]["slug"], STYLE, "Hairstyles for thin hair: if it hurts, it’s too tight",
     "Hairstyles for thin hair should never hurt. The American Academy of Dermatology says a painful style is too tight, and your hairline is one of the first places tight styles show. Loosen it and switch it up. Read how to style around a thinner hairline.",
     L(HL, "hairstyles", "S01"), "Definition card: if a hairstyle hurts it is too tight; tight styles often show early at the hairline, so loosen it and switch it up."),
    ("S02", PINS[1]["slug"], STYLE, "Hairstyles for a thinning hairline: 3 ways to style around it",
     "Hairstyles for a thinning hairline: let the front fall softly with a loose side part or fringe, move your part, and use colored spray or fiber powder where the scalp shows. Styling changes the look, not the cause, so see a dermatologist too. Read more.",
     L(HL, "hairstyles", "S02"), "List of three ways to style around a thinner hairline: a loose side part or fringe, a new part, colored spray or fiber powder."),
    ("S03", PINS[2]["slug"], CUTS, "Haircuts for thin hair at the front: a fringe covers more of the hairline",
     "Haircuts for thin hair at the front: a loose side part or a fringe that falls forward covers more of the hairline than hair pulled straight back. Keep it loose, with no pins or tension at the edges. Still thinning? See a dermatologist. Read more.",
     L(HL, "haircuts", "S03"), "Card comparing hair pulled back, which shows more hairline, with a fringe or side part that falls forward and covers more, kept loose with no tension."),
    ("S04", PINS[3]["slug"], THIN, "Thinning hairline? 3 signs your hairstyle is too tight",
     "Thinning hairline? The AAD says your hairline is one of the first places hair loss from tight styles shows. Watch for short, broken hairs around your forehead, pain from tightly pulled hair and patches of hair loss where hair is pulled tight. Loosen it and see a dermatologist.",
     L(HL, "thinning", "S04"), "Checklist of three signs a hairstyle is too tight: short broken hairs around the forehead, pain from pulled hair, thin or bare patches where hair is pulled tight."),
    ("S05", PINS[4]["slug"], O50, "Hair over 50: one hairline sign to show a dermatologist soon",
     "Over 50 with a thin band of bare skin along the front and sides of your hairline, often with thinner eyebrows? The AAD says frontal fibrosing alopecia often starts this way, usually in women after menopause, and can cause permanent hair loss. See a dermatologist soon.",
     L(HL, "over-50", "S05"), "Definition card: a thin band of bare skin along the front and sides of the hairline, often with thinner eyebrows, usually diagnosed in women after menopause; see a dermatologist soon."),
    ("S06", PINS[5]["slug"], STYLE, "Hairstyles for thin hair under a hat or scarf: 3 winter swaps",
     "Hairstyles for thin hair under a winter hat or scarf: the AAD says a covering that rubs can add to hair loss from pulling, especially over hair pulled back tight. Pull it back loosely, choose a silk or satin covering and brush only enough to style. Read more.",
     L(HL, "hairstyles", "S06"), "Swap list: hair pulled tight under a hat becomes pulled back loosely; any covering becomes silk or satin; tugging becomes brushing only enough to style."),
    ("S07", PINS[6]["slug"], DRY, "Dry scalp in winter? Cold, dry air is part of it: 4 changes to try",
     "Dry scalp in winter? The AAD says low humidity and cold climates can dry the scalp. Cleveland Clinic suggests a humidifier at home, a gentle shampoo and washing less often, and the AAD says some hair products can dry the scalp, so check yours. Read the dry scalp guide.",
     L(DSS, "dry-scalp", "S07"), "List for a dry scalp in winter: cold dry air can dry the scalp, run a humidifier, check hair products that can dry the scalp, a gentle shampoo and washing less often."),
    ("S08", PINS[7]["slug"], DRY, "Dry, itchy scalp? Ask a dermatologist before itch-relief products",
     "Dry, itchy scalp? For dry skin in general, the AAD says ask your dermatologist before you use a product that promises itch relief, because many contain ingredients that can make dryness and itch worse. Read what to look for on a dry scalp label.",
     L(DSS, "dry-scalp", "S08"), "Split card: ask a dermatologist first about products that promise itch relief, because some can make very dry skin itch more."),
    ("S09", PINS[8]["slug"], THIN, "Hair shedding after stress? Why it can last longer if stress stays",
     "More hair shedding after a hard time? The AAD says excessive shedding stops as your body readjusts, but if the stress stays, shedding can be long lived. Heavy shedding past six months is chronic, says the British Association of Dermatologists: see your doctor. Read more.",
     L(STR, "thinning", "S09"), "Card: when stress ends, shedding stops as the body readjusts; when stress stays, shedding can be long lived; heavy shedding past 6 months, see your doctor."),
    ("S10", PINS[9]["slug"], SPA, "Head spa at home: does washing often hurt your hair? One study says no",
     "Head spa at home and washing often? In one study, 5 to 6 washes a week did no objective harm to hair (three of its five authors work for a shampoo maker). The AAD says wash as often as hair gets dirty or oily, with shampoo on the scalp. Read more.",
     L(WSC, "scalp-care", "S10"), "Definition card: in one study 5 to 6 washes a week did no objective harm; put shampoo on the scalp, not rubbed into the length; wash as often as hair gets dirty or oily."),
]

if __name__ == "__main__":
    E.PINS = PINS
    E.render(sys.argv[1], set(sys.argv[2:]) or None)
