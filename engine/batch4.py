"""Batch 4 (2026-10-29): the last 2 make-hair-look-thicker slots (page cap 8) go to the Haircuts and
Hairstyles boards, then dry scalp in season, then the hook bank ("I didn't know that about hair").
Every fact is from the RUNBOOK fact sheet or the Journal page map.
Usage: python3 -I batch4.py <out_dir> [ID ...]"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pinengine as E
import batch2  # noqa: F401  (registers the 15 batch-2 layouts)
from queue_build import L, J, CUTS, STYLE, DRY, THIN, SPA, HC

MHT = J + "make-hair-look-thicker"
DSC = J + "can-dry-scalp-cause-hair-loss"
DRYH = J + "why-is-my-hair-so-dry"
BRK = J + "breakage-or-shedding"
OSD = J + "oily-scalp-dry-hair"
WLF = J + "what-to-look-for-in-a-scalp-serum"
SUP = J + "scalp-serum-or-hair-supplement"
SVL = J + "hair-shedding-vs-hair-loss"

PINS = [
    dict(id="K01", slug="haircuts-for-thin-hair-what-a-cut-can-do", field="espresso", arch="split", h_size=108,
         marks=False, headline="What a new cut<br>can do, and<br>its limits.", split_top=110, item_size=39,
         left=("Can help", ["A shorter cut or layers may help thin hair look fuller.", "Color can add<br>volume to<br>each strand."]),
         right=("Its limit", ["Hiding thinning<br>with a new part<br>or hairstyle rarely<br>reaches the cause."]),
         foot="A widening part? See a dermatologist."),
    dict(id="K02", slug="hairstyles-for-thin-hair-2-signs-to-get-checked", field="porcelain", arch="list2", h_size=110,
         headline="Thin hair:<br>2 signs to<br>get checked.", item_size=58, gap=64, list_top=96,
         items=["A part that’s<br>getting wider.", "A ponytail that’s<br>getting thinner."],
         note="Both are reasons to see a<br>board-certified dermatologist (AAD)."),
    dict(id="K03", slug="dry-scalp-blow-drying-dries-it-more", field="butter", arch="contrast", h_size=114,
         headline="Blow-drying<br>can dry your<br>scalp more.", brand_on="espresso",
         defs=[("Blow-drying", "Can dry the scalp<br>even more."),
               ("Instead", "Let your hair air dry."),
               ("Itchy too?", "Keep nails short and smooth.<br>Remove scale gently.")],
         tip="Source: American Academy<br>of Dermatology."),
    dict(id="K04", slug="why-is-my-hair-so-dry-4-changes", field="white", arch="list2", h_size=112, band_h=430, list_top=150,
         headline="Why is my<br>hair so dry?<br>4 changes.", item_size=52, gap=52,
         items=["Wash about once or<br>twice a week.", "Conditioner after<br>every wash.", "Air dry when you can.",
                "Rinse right after<br>swimming."],
         note="Gentle care not helping? See a health care provider."),
    dict(id="K05", slug="100-brush-strokes-a-day-is-a-myth", field="white", arch="split", h_size=108, band_h=470,
         split_top=150, headline="100 brush<br>strokes a day<br>is a myth.", item_size=44,
         left=("The fact", ["Brush and comb only to style.", "Use a wide-tooth comb, gently."]),
         right=("The myth", ["Hair needs 100 strokes a day."]),
         foot="Source: American Academy of Dermatology."),
    dict(id="K06", slug="dry-shampoo-doesnt-clean-your-hair", field="espresso", arch="contrast", h_size=112,
         headline="Dry shampoo<br>doesn’t clean<br>your hair.",
         defs=[("The rule", "Wash after one<br>or two uses."),
               ("Too much?", "Hair turns dry,<br>stiff and gritty."),
               ("Itching or burning?", "Stop using it.")],
         tip="Source: American Academy<br>of Dermatology."),
    dict(id="K07", slug="hypoallergenic-has-no-legal-definition", field="porcelain", arch="definition", h_size=104,
         headline="“Hypoallergenic”<br>has no legal<br>definition.",
         terms=[("Hypoallergenic", "no federal standard, says the FDA"),
                ("Unscented", "may still contain fragrance")],
         sum="Read the ingredient list, not the front label.", sum2="Look for fragrance or parfum."),
    dict(id="K08", slug="biotin-can-throw-off-blood-tests", field="butter", arch="checklist", h_size=110,
         headline="Taking biotin?<br>It can throw off<br>blood tests.",
         items=["Results can read falsely<br>high or low.", "Check labels for biotin<br>(vitamin B7).",
                "Tell your doctor before<br>a blood test."],
         note="Source: FDA."),
    dict(id="K09", slug="1-in-3-no-cause-is-found", field="porcelain", arch="bignum", h_size=104,
         headline="Shedding with<br>no clear cause?", big="1 in 3",
         big_label="of people diagnosed with telogen<br>effluvium: no cause is found.",
         lines=["Source: British Association<br>of Dermatologists.", "Excessive shedding often<br>stops on its own (AAD)."]),
    dict(id="K10", slug="oily-roots-dry-ends-conditioner-on-scalp", field="butter", arch="list2", h_size=114,
         headline="Oily roots,<br>dry ends?", item_size=58, gap=64, list_top=110,
         items=["Shampoo on the<br>scalp only.", "Conditioner on<br>the ends only.", "Wash as often as<br>your scalp needs."],
         note="Conditioner on the scalp can make it<br>greasy, says Cleveland Clinic."),
]

# id, slug, board, title, description, link, alt
COPY = [
    ("K01", PINS[0]["slug"], CUTS, "Haircuts for thin hair: what a new cut or color can do, and its limits",
     "Haircuts for thin hair: a shorter cut or layers may help thinning hair look fuller, and dye can add volume to each strand, says Cleveland Clinic. Hiding thinning with a new part or hairstyle rarely reaches the cause (AAD). Read the guide.",
     L(MHT, "haircuts", "K01"), "Two columns: what a new haircut can do for thin hair, and what it rarely does, with a note to see a dermatologist about a widening part."),
    ("K02", PINS[1]["slug"], STYLE, "Hairstyles for thin hair: 2 signs it’s time to get checked",
     "Hairstyles for thin hair can hide a lot, but a widening part and a thinner ponytail are possible signs of female pattern hair loss, says the AAD. See a board-certified dermatologist. Read what helps hair look fuller meanwhile.",
     L(MHT, "hairstyles", "K02"), "List of two signs to see a dermatologist: a part that's getting wider and a ponytail that's getting thinner."),
    ("K03", PINS[2]["slug"], DRY, "Dry scalp? Blow-drying can dry it even more. Let it air dry",
     "Dry scalp tip from the American Academy of Dermatology: let your hair air dry, because blow drying can dry the scalp more. Keep nails short and smooth, and remove scale gently. An itch that isn’t improving needs a dermatologist. Save it.",
     L(DSC, "dry-scalp", "K03"), "Card explaining that blow-drying can dry the scalp more, with air drying and gentle scale removal as swaps."),
    ("K04", PINS[3]["slug"], DRY, "Why is my hair so dry? 4 changes that help dry hair",
     "Why is my hair so dry? MedlinePlus suggests washing dry hair about once or twice a week. Use conditioner after every wash, air dry when you can and rinse right after swimming. If gentle care doesn’t help, see a provider. Read more.",
     L(DRYH, "dry-hair", "K04"), "List of four changes for dry hair: wash about once or twice a week, condition every wash, air dry, rinse after swimming."),
    ("K05", PINS[4]["slug"], THIN, "Thinning hair tip: 100 brush strokes a day is a myth",
     "Thinning hair doesn’t need 100 brush strokes a day. That’s a myth, says the American Academy of Dermatology. Brush and comb only to style, gently, with a wide-tooth comb. Damaged hair is fragile and tends to break. Read more.",
     L(BRK, "breakage", "K05"), "Myth versus fact card: hair does not need 100 brush strokes a day; brush only to style with a wide-tooth comb."),
    ("K06", PINS[5]["slug"], SPA, "Dry shampoo doesn’t clean your hair: 3 dermatologist rules",
     "Dry shampoo doesn’t clean your hair, says the American Academy of Dermatology. Wash after one or two uses, go easy so hair isn’t left dry, stiff and gritty, and stop if you get itching or burning. Read the oily scalp guide.",
     L(OSD, "oily-scalp", "K06"), "Card stating dry shampoo doesn't clean hair, with three rules: wash after one or two uses, too much leaves hair gritty, stop if it itches."),
    ("K07", PINS[6]["slug"], HC, "Hypoallergenic hair products: the word has no legal definition",
     "Hypoallergenic on a hair product has no federal standard, says the FDA, and unscented may still contain fragrance. Read the ingredient list, not the front of the bottle, and look for fragrance or parfum. See eight checks before you buy.",
     L(WLF, "ingredients", "K07"), "Definition card: hypoallergenic has no federal standard and unscented may still contain fragrance."),
    ("K08", PINS[7]["slug"], HC, "Hair vitamins with biotin can throw off blood tests: what to know",
     "Hair vitamins with biotin can cause falsely high or low blood test results, the FDA says. Check the label for biotin (vitamin B7) and tell your doctor before a blood test. Read what to ask before you start a hair supplement.",
     L(SUP, "supplements", "K08"), "Checklist on biotin and blood tests: results can read falsely high or low, check labels, tell your doctor first."),
    ("K09", PINS[8]["slug"], THIN, "Thinning hair from a shed? For 1 in 3 with telogen effluvium, no cause is found",
     "Thinning hair from a shed, called telogen effluvium, doesn’t always have a clear cause: for 1 in 3 people diagnosed, none is found, says the British Association of Dermatologists. Learn shedding vs hair loss and when to see a dermatologist.",
     L(SVL, "shedding", "K09"), "Big number card: for 1 in 3 people diagnosed with telogen effluvium, no cause is found."),
    ("K10", PINS[9]["slug"], SPA, "Oily roots, dry ends? Conditioner on your scalp can make it greasy",
     "Oily scalp, dry hair? Shampoo the scalp only and put conditioner on the ends, because conditioner on the scalp can make it greasy, says Cleveland Clinic. Wash as often as your scalp needs, even every day. Read the full guide.",
     L(OSD, "oily-scalp", "K10"), "List for oily roots and dry ends: shampoo on the scalp only, conditioner on the ends only, wash as often as needed."),
]

if __name__ == "__main__":
    E.PINS = PINS
    E.render(sys.argv[1], set(sys.argv[2:]) or None)
