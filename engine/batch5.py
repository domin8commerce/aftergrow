"""Batch 5 (2026-11-02): make-hair-look-thicker is at its 8-pin cap and the three haircut/hairstyle/over-50
articles are not published yet, so the haircut and hairstyle boards get nothing new this run. Dry scalp care
(in season) goes first, then Fine thin hair over 50 and Thinning hair from three newly verified Journal pages
(color-treated-hair-care, simple-hair-care-routine, is-my-hair-thinning, read through Shopify 2026-11-02),
then the hook bank. Every fact is from the RUNBOOK fact sheet or the Journal page map.
Usage: python3 -I batch5.py <out_dir> [ID ...]"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pinengine as E
import batch2  # noqa: F401  (registers the 15 batch-2 layouts)
from queue_build import L, J, DRY, THIN, O50, HC, SPA

DSC = J + "can-dry-scalp-cause-hair-loss"
CTH = J + "color-treated-hair-care"
SHR = J + "simple-hair-care-routine"
IMT = J + "is-my-hair-thinning"
FFR = J + "fragrance-free-hair-routine"
NSS = J + "natural-scalp-serum"
HTR = J + "how-to-read-a-scalp-serum-label"

PINS = [
    dict(id="L01", slug="dry-scalp-or-something-else", field="porcelain", arch="split", h_size=108, band_h=470,
         split_top=150, headline="Dry scalp, or<br>something<br>else?", item_size=40,
         left=("Dry scalp", ["Itching.", "Flakes."]),
         right=("Lookalikes", ["Scalp psoriasis.", "A fungal scalp<br>infection."]),
         foot="Not sure? See a dermatologist."),
    dict(id="L02", slug="dyeing-your-hair-scalp-rules", field="butter", arch="checklist", h_size=104,
         headline="Hair dye day?<br>Don’t scratch<br>your scalp first.",
         items=["No scratching or brushing<br>your scalp for 3 days.", "Irritated or sunburned<br>scalp? Don’t dye.",
                "Rinse your scalp well<br>after dyeing."],
         note="Source: FDA."),
    dict(id="L03", slug="coloring-hair-3-rules", field="espresso", arch="contrast", h_size=108,
         headline="Coloring<br>your hair?<br>3 rules.",
         defs=[("Shade", "Stay within 3 shades<br>of your natural color."),
               ("Direction", "Darker is typically<br>better than lighter."),
               ("Touch-ups", "In winter, every 8 to<br>10&nbsp;weeks or longer.")],
         tip="Source: American Academy<br>of Dermatology."),
    dict(id="L04", slug="fine-thin-hair-wash-every-1-to-2-days", field="white", arch="bignum", h_size=104,
         headline="Fine, thin hair:<br>how often to wash?", big="1 to 2",
         big_label="days between washes<br>for thin, fine hair (a rough guide).",
         lines=["Source: Cleveland Clinic.", "Wash as often as your hair<br>gets dirty or oily (AAD)."]),
    dict(id="L05", slug="is-my-hair-thinning-4-checks", field="porcelain", arch="list2", h_size=110, band_h=430,
         list_top=150, headline="Is my hair<br>thinning?<br>4 checks.", item_size=50, gap=50,
         items=["A part that’s<br>getting wider.", "Scalp showing<br>on top.", "A thinner ponytail.",
                "Hair receding near<br>your temples."],
         note="Shedding 50 to 100 hairs a day is normal (AAD)."),
    dict(id="L06", slug="straight-hair-dont-brush-it-wet", field="butter", arch="contrast", h_size=112,
         headline="Straight hair?<br>Don’t brush<br>it wet.", brand_on="espresso",
         defs=[("Straight hair", "Let it dry partway, then<br>use a wide-tooth comb."),
               ("Thick, curly hair", "Comb it in the shower, before<br>you rinse out conditioner."),
               ("Either way", "Start at the ends<br>and work up.")],
         tip="Source: American Academy<br>of Dermatology."),
    dict(id="L07", slug="fragrance-free-isnt-irritation-free", field="espresso", arch="definition", h_size=104,
         headline="Fragrance-free<br>doesn’t mean<br>irritation-free.",
         terms=[("Fragrance-free", "can still irritate or contain an allergen"),
                ("On the label", "look for fragrance, parfum or perfume")],
         sum="Change one product at a time.", sum2="Rash, redness or burning?<br>Stop using it (FDA)."),
    dict(id="L08", slug="natural-on-a-hair-label-has-no-rule", field="porcelain", arch="definition", h_size=104,
         headline="“Natural” on<br>a hair label<br>has no rule.",
         terms=[("USDA Organic", "at least 95% organic ingredients"),
                ("Made with organic", "at least 70% organic ingredients")],
         sum="Water and salt aren’t counted.", sum2="An ingredient’s source doesn’t<br>decide its safety (FDA)."),
    dict(id="L09", slug="ingredients-under-1-percent-any-order", field="butter", arch="bignum", h_size=104,
         headline="Reading a<br>hair label?", big="1%",
         big_label="or less: these ingredients can be<br>listed in any order.",
         lines=["Above that, ingredients run<br>from most to least.", "Source: FDA."]),
]

# id, slug, board, title, description, link, alt
COPY = [
    ("L01", PINS[0]["slug"], DRY, "Dry scalp or something else? What an ordinary dry scalp looks like",
     "Dry scalp on its own usually means itching and flakes. Some conditions, like scalp psoriasis or a fungal scalp infection, can look like a dry scalp at first and can come with hair loss. A dermatologist can tell. Read the guide.",
     L(DSC, "dry-scalp", "L01"), "Two columns: a dry scalp means itching and flakes; lookalikes such as scalp psoriasis and a fungal scalp infection."),
    ("L02", PINS[1]["slug"], SPA, "Scalp care before you dye your hair: don’t scratch for 3 days",
     "Scalp care before color day: the FDA says don’t scratch or brush your scalp for three days before you dye, and don’t dye if your scalp is irritated, sunburned or damaged. Rinse your scalp well after. Read the full guide.",
     L(CTH, "scalp-care", "L02"), "Checklist of three FDA scalp rules for hair dye day: no scratching or brushing for 3 days, no dyeing an irritated or sunburned scalp, rinse well after."),
    ("L03", PINS[2]["slug"], O50, "Fine thin hair over 50? 3 dermatologist tips for coloring any hair",
     "Fine thin hair over 50 and planning color? The AAD’s tips apply to any colored hair: stay within three shades of your natural color, darker is typically better than lighter, and in winter space touch-ups to every 8 to 10 weeks or longer. Save it for your next appointment.",
     L(CTH, "over-50", "L03"), "Card with three hair color rules: within three shades, darker over lighter, touch-ups every 8 to 10 weeks or longer in winter."),
    ("L04", PINS[3]["slug"], O50, "Fine thin hair: how often to wash it? Every 1 to 2 days, as a guide",
     "Fine thin hair: Cleveland Clinic’s rough guide is a wash every one to two days. The AAD says wash as often as your hair gets dirty or oily, and use conditioner after every shampoo. Read how to build a simple routine.",
     L(SHR, "over-50", "L04"), "Big number card: wash thin, fine hair every 1 to 2 days as a rough guide, or as often as it gets dirty or oily."),
    ("L05", PINS[4]["slug"], THIN, "Is my hair thinning? 4 things to check at home",
     "Is my hair thinning? Check for a part that’s getting wider, scalp showing on top, a thinner ponytail and hair receding near your temples. Shedding 50 to 100 hairs a day is normal. A dermatologist can tell you the cause. Read more.",
     L(IMT, "thinning", "L05"), "List of four at-home checks for thinning hair: a wider part, scalp showing on top, a thinner ponytail, receding temples."),
    ("L06", PINS[5]["slug"], THIN, "Thinning hair? Don’t brush straight hair while it’s wet (AAD tip)",
     "Thinning hair or not, the AAD lists brushing straight hair while it’s wet among habits that can damage hair. Let it dry partway, then comb gently with a wide-tooth comb. Thick, curly hair: comb it in the shower before you rinse out conditioner.",
     L(SHR, "thinning", "L06"), "Card on detangling: let straight hair dry partway before a wide-tooth comb, comb curly hair in the shower, start at the ends."),
    ("L07", PINS[6]["slug"], HC, "Fragrance-free hair care doesn’t mean irritation-free: what to check",
     "Fragrance-free hair care can still irritate or contain an allergen. Check the ingredient list for fragrance, parfum or perfume, change one product at a time, and stop any product that gives a rash, redness or burning (FDA). Read more.",
     L(FFR, "ingredients", "L07"), "Definition card: fragrance-free can still irritate or contain an allergen; look for fragrance, parfum or perfume on the label."),
    ("L08", PINS[7]["slug"], HC, "Natural hair products: the word natural on a label has no rule",
     "Natural hair products: “natural” on a label has no rule behind it. USDA Organic means at least 95% organically produced ingredients, not counting water and salt; “made with organic ingredients” means at least 70%. Read more.",
     L(NSS, "ingredients", "L08"), "“Natural” on a hair label has no rule; definition card comparing USDA Organic, at least 95 percent organic ingredients, with made with organic, at least 70 percent."),
    ("L09", PINS[8]["slug"], HC, "Hair product labels: ingredients at 1% or less can be in any order",
     "Hair product labels list ingredients from most to least, but those at 1% or less can be listed in any order. So among those small amounts, the order tells you little. Learn how to read a scalp serum label, step by step.",
     L(HTR, "ingredients", "L09"), "Big number card: ingredients at 1 percent or less can be listed in any order on a label."),
]

if __name__ == "__main__":
    E.PINS = PINS
    E.render(sys.argv[1], set(sys.argv[2:]) or None)
