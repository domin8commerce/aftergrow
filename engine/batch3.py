"""Batch 3 (2026-10-26): the empty high-demand boards first (Haircuts / Hairstyles for thin hair,
Fine thin hair over 50, all from make-hair-look-thicker), then dry scalp while it's in season.
Every fact is from the RUNBOOK fact sheet or the Journal page map.
Usage: python3 -I batch3.py <out_dir> [ID ...]"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pinengine as E
import batch2  # noqa: F401  (registers the 15 batch-2 layouts)
from queue_build import L, J, CUTS, STYLE, O50, DRY

MHT = J + "make-hair-look-thicker"
DSC = J + "can-dry-scalp-cause-hair-loss"
SDS = J + "scalp-serum-for-dry-scalp"

PINS = [
    dict(id="I01", slug="haircuts-for-thin-hair-shorter-cut-or-layers", field="butter", arch="list2", h_size=112,
         headline="Thin hair?<br>A shorter cut<br>or layers.", item_size=58, gap=64, list_top=96,
         items=["A shorter cut.", "Layers.", "New styling<br>techniques."],
         note="Each may help thinning hair look fuller,<br>says Cleveland Clinic."),
    dict(id="I02", slug="haircuts-for-thinning-hair-ask-your-stylist", field="porcelain", arch="checklist", h_size=112,
         headline="Thinning hair?<br>Ask your<br>stylist for:",
         items=["A shorter cut or layers", "Color at a salon,<br>not at home", "One service per visit",
                "Longer between touch-ups", "A style that doesn’t pull"],
         note="A widening part is a reason to see a dermatologist, not just a new stylist."),
    dict(id="I03", slug="hairstyles-for-thinning-hair-5-swaps", field="white", arch="swap", h_size=116,
         headline="Hairstyles for<br>thin hair:<br>5 swaps.", band_h=520, list_top=140,
         rows=[("A tight ponytail", "Hair loosely pulled back"),
               ("Bare rubber bands", "Covered bands made for hair"),
               ("High heat", "The lowest setting, or air dry"),
               ("Long-hold products", "A style that doesn’t need them"),
               ("Conditioner everywhere", "Fine hair: conditioner on the ends")]),
    dict(id="I04", slug="4-ways-to-cover-a-wider-part", field="espresso", arch="grid4", h_size=116,
         headline="4 ways to cover<br>a wider part.", label_size=50, cell_h=300, grid_top=96,
         cells=[dict(label="Colored<br>hair spray", sub="Covers thinning areas."),
                dict(label="Fiber<br>powder", sub="Hair bulking fibers."),
                dict(label="Synthetic<br>wig", sub="Easier to look after.<br>Can be itchy and hot."),
                dict(label="Real-hair<br>wig", sub="Looks more natural.<br>Costs more.")],
         foot="A part that keeps widening? See a dermatologist too."),
    dict(id="I05", slug="hair-color-can-make-thin-hair-look-fuller", field="espresso", arch="ledger2", h_size=108,
         headline="Hair color can<br>make thin hair<br>look fuller.", val_size=46, row_pad=36,
         rows=[("What dye does", "Can add volume to each<br>strand, so hair<br>seems fuller."),
               ("Where", "A salon, not a home kit."),
               ("How often", "Stretch the time between touch-ups."),
               ("Per visit", "One service at a time.")],
         foot="Sources: Cleveland Clinic, American Academy of Dermatology."),
    dict(id="I06", slug="fine-thin-hair-over-50-4-changes", field="white", arch="list2", h_size=112, band_h=430, list_top=150,
         headline="Fine thin hair<br>over 50:<br>4 changes.", item_size=52, gap=52,
         items=["A volume shampoo<br>without sulfates.", "Conditioner on the ends.", "The lowest heat,<br>or air dry.",
                "A shorter cut or layers."],
         note="A widening part? See a dermatologist."),
    dict(id="J01", slug="itchy-scalp-scratching-can-loosen-hair", field="white", arch="swap", h_size=116,
         headline="Itchy scalp?<br>Scratching hard<br>can loosen hair.", band_h=520, list_top=140,
         rows=[("Scratching hard", "Nails short and filed smooth"),
               ("Pulling off scale", "Remove scale gently"),
               ("Picking at flakes", "Hands off. Don’t pick."),
               ("Blow-drying", "Let your hair air dry")]),
    dict(id="J02", slug="itchy-scalp-4-signs-see-a-dermatologist", field="espresso", arch="checklist", h_size=114,
         headline="Itchy scalp:<br>when to see a<br>dermatologist.",
         items=["Itching that isn’t improving", "A rash or pain", "Skin that’s swollen,<br>painful or draining",
                "Store-bought products<br>haven’t helped"],
         note="An ordinary dry scalp means itching and flakes. The signs above are worth a check."),
    dict(id="J03", slug="dry-scalp-vs-dandruff-the-difference", field="butter", arch="contrast", h_size=114,
         headline="Dry scalp<br>is not<br>dandruff.", brand_on="espresso",
         defs=[("Dry scalp", "Caused by a loss<br>of moisture."),
               ("Dandruff", "Caused by excess oil."),
               ("Itching won’t stop?", "A red rash, or warm,<br>swollen skin? Call a dermatologist.")],
         tip="Choose fragrance-free.<br>Check the ingredient list."),
    dict(id="J04", slug="dry-scalp-3-winter-habits", field="porcelain", arch="list2", h_size=118,
         headline="Dry scalp?<br>3 habits for<br>winter.", item_size=58, gap=64, list_top=96,
         items=["Showers of 5 to<br>10 minutes.", "Leave-in conditioner<br>on hair, not scalp.",
                "Fragrance-free, with the<br>ingredient list checked."],
         note="Itching that won’t stop? Call a dermatologist."),
]

# id, slug, board, title, description, link, alt
COPY = [
    ("I01", PINS[0]["slug"], CUTS, "Haircuts for thin hair: a shorter cut or layers can make it look fuller",
     "Haircuts for thin hair don’t need to be complicated. Cleveland Clinic says a shorter cut, layers or new styling techniques may help thinning hair look fuller. Read what else helps, and the sign that means see a dermatologist.",
     L(MHT, "haircuts", "I01"), "Butter-yellow card listing a shorter cut, layers and new styling techniques as ways thin hair may look fuller."),
    ("I02", PINS[1]["slug"], CUTS, "Haircuts for thinning hair: 5 things to ask your stylist",
     "Haircuts for thinning hair start with the right ask. A shorter cut or layers, color at a salon instead of at home, one service per visit, longer between touch-ups and a style that doesn’t pull. Save it for your next appointment.",
     L(MHT, "haircuts", "I02"), "Checklist of five things to ask a stylist about thinning hair, from a shorter cut to a style that doesn't pull."),
    ("I03", PINS[2]["slug"], STYLE, "Hairstyles for thinning hair: 5 swaps, starting with your ponytail",
     "Hairstyles for thinning hair should be gentle, because thinning hair is fragile. Five swaps dermatologists suggest: loosely pulled back, covered bands, the lowest heat, no long-hold products and conditioner on the ends. Read the full guide.",
     L(MHT, "hairstyles", "I03"), "Five hair habits crossed out, each with a gentler swap below, starting with a tight ponytail."),
    ("I04", PINS[3]["slug"], STYLE, "Hairstyles for thinning hair: 4 ways to cover a wider part",
     "Hairstyles for thinning hair can get help from colored hair spray, hair bulking fiber powder or a wig, synthetic or real hair. What each one offers, and why a widening part is also worth a dermatologist visit. Read the guide.",
     L(MHT, "hairstyles", "I04"), "Four tiles comparing colored hair spray, fiber powder, a synthetic wig and a real-hair wig for covering a wider part."),
    ("I05", PINS[4]["slug"], O50, "Fine thin hair over 50? Hair color can make it look fuller",
     "Fine thin hair over 50 can look fuller with color: dye can add volume to each strand, says Cleveland Clinic. The AAD suggests a salon, not a home kit, one service at a time and longer between touch-ups. Read the full guide.",
     L(MHT, "over-50", "I05"), "Ledger card explaining how hair color adds volume to each strand, with salon and touch-up tips."),
    ("I06", PINS[5]["slug"], O50, "Fine thin hair over 50: 4 changes that may help it look fuller",
     "Fine thin hair over 50 is fragile, so be gentle: try a volume shampoo without sulfates, conditioner on the ends, the lowest heat and a shorter cut or layers. A widening part is a reason to see a dermatologist. Read more.",
     L(MHT, "over-50", "I06"), "List of four changes for fine thin hair over 50, with a note to see a dermatologist about a widening part."),
    ("J01", PINS[6]["slug"], DRY, "Itchy scalp? Scratching hard can loosen hair. Do this instead",
     "Itchy scalp tips from the American Academy of Dermatology: scratching hard or forcing off scale can loosen hair. Keep nails short and smooth, remove scale gently, don’t pick and let hair air dry. Save these for dry scalp season.",
     L(DSC, "dry-scalp", "J01"), "Four itchy scalp habits crossed out, each with a gentler swap: smooth nails, gentle scale removal, no picking, air drying."),
    ("J02", PINS[7]["slug"], DRY, "Itchy scalp: 4 signs it’s time to see a dermatologist",
     "Itchy scalp that isn’t improving, or comes with a rash, pain or hair loss, is worth a dermatologist visit. So is swollen or draining skin, or store-bought products that haven’t helped. Read what an ordinary dry scalp looks like.",
     L(DSC, "dry-scalp", "J02"), "Checklist of four signs an itchy scalp needs a dermatologist, on an espresso background."),
    ("J03", PINS[8]["slug"], DRY, "Dry scalp vs dandruff: the one difference to know",
     "Dry scalp vs dandruff: a dry scalp comes from a loss of moisture, dandruff from excess oil, says Cleveland Clinic. Choose fragrance-free products and check the list. Itching that won’t stop needs a dermatologist. Read more.",
     L(SDS, "dry-scalp", "J03"), "Card contrasting dry scalp, caused by a loss of moisture, with dandruff, caused by excess oil."),
    ("J04", PINS[9]["slug"], DRY, "Dry scalp in winter: 3 simple habits to try",
     "Dry scalp in winter? Keep showers to 5 to 10 minutes, put leave-in conditioner on hair only, and choose fragrance-free products with the ingredient list checked. Itching that won’t stop needs a dermatologist. Save for winter.",
     L(SDS, "dry-scalp", "J04"), "List of three dry scalp habits for winter: short showers, leave-in conditioner on hair only, fragrance-free products."),
]

if __name__ == "__main__":
    E.PINS = PINS
    E.render(sys.argv[1], set(sys.argv[2:]) or None)
