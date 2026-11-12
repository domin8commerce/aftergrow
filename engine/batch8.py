"""Batch 8 (2026-11-12): the three haircut/hairstyle/over-50 articles are still unpublished (Shopify checked
2026-11-12), make-hair-look-thicker is at its 8-pin cap, and Dry scalp care has no unused angle on its live pages.
Two newly verified Journal pages (read through Shopify 2026-11-12) open the priority boards again:
how-to-tame-flyaways feeds Hairstyles for thin hair, and why-has-my-hair-texture-changed feeds Fine thin hair
over 50. simple-hair-care-routine adds three more. Every fact is on the linked page.
Usage: python3 -I batch8.py <out_dir> [ID ...]"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pinengine as E
import batch2  # noqa: F401  (registers the 15 batch-2 layouts)
from queue_build import L, J, THIN, O50, STYLE

FLY = J + "how-to-tame-flyaways"
TEX = J + "why-has-my-hair-texture-changed"
SHR = J + "simple-hair-care-routine"

PINS = [
    dict(id="P01", slug="flyaways-on-fine-hair-leave-in-steps", field="white", arch="checklist", h_size=104,
         headline="Flyaways on<br>fine hair?<br>Try this.",
         items=["A leave-in conditioner,<br>on damp hair.", "The smallest amount<br>that does the job.",
                "Mid strands to ends,<br>where it’s frizzy.", "Keep it off<br>your scalp."],
         note="Fine hair needs a lighter leave-in. Steps: AAD."),
    dict(id="P02", slug="dont-leave-rinse-off-conditioner-in", field="butter", arch="contrast", h_size=100,
         headline="Rinse-off<br>conditioner?<br>Rinse it off.", brand_on="espresso",
         defs=[("The trick", "Rinse-off conditioner and<br>water in a spray bottle."),
               ("Why not", "It often has detergent.<br>Left in, it can damage hair."),
               ("Instead", "A real leave-in conditioner,<br>a small amount.")],
         tip="Source: American Academy<br>of Dermatology."),
    dict(id="P03", slug="heat-styling-thin-hair-low-heat", field="porcelain", arch="list2", h_size=104, band_h=430,
         list_top=150, headline="Heat styling<br>thin hair?", item_size=50, gap=56,
         items=["Low or medium<br>heat setting.", "A heat protectant<br>product first.",
                "About once a week,<br>or less."],
         note="Source: American Academy of Dermatology."),
    dict(id="P04", slug="strand-width-peaked-near-40", field="espresso", arch="bignum", h_size=96,
         headline="Hair feels finer<br>after 40? What<br>one study found.", big="40",
         big_label="Near this age, strand width<br>in women peaked, then fell.",
         lines=["The largest study in a 2018 review.", "When it starts varies a lot."]),
    dict(id="P05", slug="why-has-my-hair-texture-changed-5-causes", field="white", arch="list2", h_size=100,
         band_h=430, list_top=150, headline="Why has my hair<br>texture changed?", item_size=48, gap=46,
         items=["Age: finer strands,<br>more frizz or wave.", "Hormones: listed<br>by MedlinePlus.",
                "Heat styling: brittle,<br>frizzy, dull hair.", "Color, bleach, perms:<br>drier, weaker lengths.",
                "A recent shed: short<br>new hairs at the front."],
         note="Patches, scaling, itching or pain?<br>See a dermatologist."),
    dict(id="P06", slug="hair-can-get-curvier-with-age-frizz", field="porcelain", arch="definition", h_size=100,
         headline="More frizz<br>with age? One<br>possible reason.",
         terms=[("Curvier", "one study found hair<br>got curvier with age"),
                ("Frizz", "neighboring hairs curving<br>in different ways")],
         sum="Source: a 2018 review", sum2="of hair aging."),
    dict(id="P07", slug="short-hairs-along-your-part-broken-or-new", field="butter", arch="contrast", h_size=104,
         headline="Short hairs<br>along your part?", brand_on="espresso",
         defs=[("Broken pieces", "Damaged hair is fragile,<br>so it tends to break (AAD)."),
               ("Still short", "New hairs keep growing in,<br>so some are shorter (MedlinePlus)."),
               ("Which one?", "A mirror alone usually<br>can’t tell you.")],
         tip="Often one of<br>these two things."),
    dict(id="P08", slug="finer-hair-at-the-front-after-menopause", field="espresso", arch="contrast", h_size=100,
         headline="Finer hair at<br>the front after<br>menopause?",
         defs=[("Past menopause", "Finer front hair than women<br>before it, whatever their age."),
               ("What it suggests", "An effect of<br>menopause hormones."),
               ("Questions?", "Ask your clinician.")],
         tip="Source: a 2018 review<br>of hair aging."),
    dict(id="P09", slug="one-new-product-at-a-time", field="white", arch="contrast", h_size=104,
         headline="New hair<br>products? One<br>at a time.", brand_on="espresso",
         defs=[("The rule", "Add one new product at<br>a time (FDA)."),
               ("Scalp step", "Optional. Use it the<br>way its label says."),
               ("Fine hair", "Conditioner on<br>the ends (AAD).")],
         tip="Sources: FDA,<br>AAD."),
    dict(id="P10", slug="towel-dry-wrap-or-blot-dont-rub", field="porcelain", arch="swap", h_size=110,
         headline="Thin hair?<br>Stop rubbing<br>it dry.", band_h=520, list_top=140,
         rows=[("Rubbing hair with a towel", "Wrap it or blot it"),
               ("Brushing straight hair wet", "Let it dry a bit, then<br>a wide-tooth comb"),
               ("Detangling from the roots", "Start at the ends")]),
]

# id, slug, board, title, description, link, alt
COPY = [
    ("P01", PINS[0]["slug"], STYLE, "Hairstyles for thin hair: how to tame flyaways on fine hair",
     "Hairstyles for thin hair look neater without flyaways. The AAD names a leave-in conditioner: on damp hair, the smallest amount that works, from mid strands to ends, and kept off your scalp. Fine hair needs a lighter one. Read the steps.",
     L(FLY, "hairstyles", "P01"), "Checklist for flyaways on fine hair: a leave-in conditioner on damp hair, the smallest amount, mid strands to ends, keep it off your scalp."),
    ("P02", PINS[1]["slug"], STYLE, "Hairstyles for thin hair: don’t leave rinse-off conditioner in",
     "Styling thin hair with rinse-off conditioner and water in a spray bottle? The AAD says rinse-off conditioner often contains detergent, so leaving it in can damage your hair. Use a real leave-in, in a small amount. Read how to tame flyaways.",
     L(FLY, "hairstyles", "P02"), "Card: rinse-off conditioner in a spray bottle often has detergent and can damage hair if left in; use a real leave-in conditioner instead."),
    ("P03", PINS[2]["slug"], STYLE, "Hairstyles for thin hair with heat: 3 dermatologist rules",
     "Hairstyles for thin hair with a blow-dryer or flat iron? The AAD says use low or medium heat with a heat protectant product, and heat tools about once a week or less. Save these three rules and read the simple hair care routine.",
     L(SHR, "hairstyles", "P03"), "List of three heat styling rules for thin hair: low or medium heat, a heat protectant first, about once a week or less."),
    ("P04", PINS[3]["slug"], O50, "Fine thin hair over 50? In one study, strand width in women peaked near 40",
     "Fine thin hair over 50 and feeling finer? A 2018 review of hair aging says that in the largest study it describes, strand diameter in women rose to a peak near age 40 and then fell. When it starts varies a lot. Read why hair texture changes.",
     L(TEX, "over-50", "P04"), "Big number 40: in the largest study in a 2018 review, strand width in women peaked near age 40 and then fell."),
    ("P05", PINS[4]["slug"], O50, "Why has my hair texture changed? 5 common causes to check",
     "Why has your hair texture changed? Common causes are age, hormones, heat styling, color or bleach and perms, and a recent shed. Each leaves different signs. Patches, scaling, itching or pain mean see a dermatologist. Read which cause fits.",
     L(TEX, "over-50", "P05"), "List of five causes of a change in hair texture: age, hormones, heat styling, chemical services and a recent shed, with a note to see a dermatologist."),
    ("P06", PINS[5]["slug"], O50, "Fine thin hair over 50 getting frizzy? Hair can get curvier with age",
     "Fine thin hair over 50 and more frizz than before? A 2018 review of hair aging cites a study that found hair became curvier with age. Frizz happens when neighboring hairs curve in different ways. Read why hair texture changes.",
     L(TEX, "over-50", "P06"), "Definition card: one study found hair got curvier with age; frizz is neighboring hairs curving in different ways."),
    ("P07", PINS[6]["slug"], THIN, "Thinning hair or flyaways? Short hairs along your part can be broken or new",
     "Thinning hair or just short hairs along your part? They’re often broken pieces, since damaged hair is fragile (AAD), or hairs that are still short, because new hairs keep growing in (MedlinePlus). A mirror usually can’t tell. Read more.",
     L(FLY, "thinning", "P07"), "Card: short hairs along the part can be broken pieces, because damaged hair tends to break, or still short, because new hairs keep growing in; a mirror usually can’t tell which."),
    ("P08", PINS[7]["slug"], O50, "Fine thin hair over 50 and past menopause? Finer hair at the front",
     "Fine thin hair over 50 and past menopause? A 2018 review says women past menopause had finer hair at the front of the scalp than women before it, whatever their age, which suggests an effect of menopause hormones. Ask your clinician. Read more.",
     L(TEX, "over-50", "P08"), "Card: a 2018 review found finer hair at the front of the scalp in women past menopause, suggesting menopause hormones; ask your clinician."),
    ("P09", PINS[8]["slug"], O50, "Fine thin hair over 50? Add new hair products one at a time",
     "Fine thin hair over 50 and a new product to try? The FDA says add one new product at a time. A scalp step is optional and goes on the way its label says, and fine hair gets conditioner on the ends (AAD). Read the simple routine.",
     L(SHR, "over-50", "P09"), "Card: add one new hair product at a time; a scalp step is optional and follows its label; conditioner on the ends of fine hair."),
    ("P10", PINS[9]["slug"], STYLE, "Hairstyles for thin hair start at drying: stop rubbing it with a towel",
     "Hairstyles for thin hair start before styling. The AAD says wrap or blot your hair instead of rubbing it, let straight hair dry a bit before a wide-tooth comb, and start detangling at the ends. Read the simple hair care routine.",
     L(SHR, "hairstyles", "P10"), "Swap list: rubbing hair with a towel becomes wrap or blot; brushing straight hair wet becomes dry partway then a wide-tooth comb; start detangling at the ends."),
]

if __name__ == "__main__":
    E.PINS = PINS
    E.render(sys.argv[1], set(sys.argv[2:]) or None)
