"""Batch 7 (2026-11-09): make-hair-look-thicker is still at its 8-pin cap and the three haircut/hairstyle/over-50
articles are still unpublished (Shopify checked 2026-11-09), so the haircut and hairstyle boards get nothing new.
Dry scalp care has no unused angle left on its live pages without repeating J02-J04, K03, K04, L01, M01-M04.
So: Fine thin hair over 50 first, then Thinning hair from two pages with few pins, then Head spa at home (in season
from mid-November) from two newly verified pages (how-to-clean-your-scalp, why-is-my-hair-greasy, read through
Shopify 2026-11-09) and types-of-scalp-treatments, and one rosemary safety pin. Every fact is on the linked page.
Usage: python3 -I batch7.py <out_dir> [ID ...]"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pinengine as E
import batch2  # noqa: F401  (registers the 15 batch-2 layouts)
from queue_build import L, J, THIN, O50, HC, SPA

SHR = J + "simple-hair-care-routine"
CTH = J + "color-treated-hair-care"
WHF = J + "why-is-my-hair-falling-out"
CLN = J + "how-to-clean-your-scalp"
GRS = J + "why-is-my-hair-greasy"
TST = J + "types-of-scalp-treatments"
SSO = J + "scalp-serum-or-scalp-oil"
HSL = J + "hair-shedding-vs-hair-loss"

PINS = [
    dict(id="N01", slug="lots-of-styling-product-clarify-monthly", field="espresso", arch="contrast", h_size=104,
         headline="Lots of product?<br>Clarify 1 to 2<br>times a month.",
         defs=[("How often", "A clarifying shampoo once<br>or twice a month."),
               ("Where", "Massage it into<br>your scalp."),
               ("After", "Conditioner on the ends<br>if your hair is fine.")],
         tip="Sources: Cleveland Clinic,<br>AAD."),
    dict(id="N02", slug="perm-and-color-one-service-at-a-time", field="butter", arch="list2", h_size=104, band_h=430,
         list_top=150, headline="Perm and color?<br>One service<br>at a time.", item_size=50, gap=56,
         items=["Perm or relax 2 weeks<br>before you color.", "Bleached, relaxed or<br>permed? Wait 14 days.",
                "Conditioner after<br>every shampoo."],
         note="Sources: AAD, FDA."),
    dict(id="N03", slug="hair-suddenly-falling-out-first-steps", field="white", arch="checklist", h_size=100,
         headline="Hair suddenly<br>falling out?<br>First steps.",
         items=["Think back: a big event<br>a few months ago?", "Don’t stop a medicine<br>on your own.",
                "A blood test can show<br>a low nutrient.", "Sudden, patchy, or 6+<br>months? Dermatologist."],
         note="A shed often starts months after the event."),
    dict(id="N04", slug="all-over-or-in-patches", field="porcelain", arch="split", h_size=108, band_h=470,
         split_top=150, headline="Thinning all<br>over, or in<br>patches?", item_size=48,
         left=("All over", ["Typical of a<br>shed (BAD)."]),
         right=("Round patches", ["Point to<br>another cause."]),
         foot="Patchy or sudden? See a dermatologist."),
    dict(id="N05", slug="smelly-scalp-most-common-cause-buildup", field="butter", arch="contrast", h_size=102,
         headline="Smelly scalp?<br>Most often,<br>it’s buildup.", brand_on="espresso",
         defs=[("What builds up", "Skin cells, sweat<br>and scalp oil."),
               ("What helps", "Shampoo on your scalp, as<br>often as it gets oily."),
               ("Lots of product?", "A clarifying shampoo once<br>or twice a month.")],
         tip="Sources: Cleveland Clinic,<br>AAD."),
    dict(id="N06", slug="why-hair-gets-greasy-so-fast", field="porcelain", arch="list2", h_size=104, band_h=430,
         list_top=150, headline="Why does hair<br>get greasy fast?", item_size=46, gap=46,
         items=["Fine, straight hair<br>carries oil down easily.", "Conditioner on the<br>scalp can add grease.",
                "Gels, sprays, creams and<br>serums can build up.", "A thick film of oil<br>looks oily and heavy."],
         note="Sources: Cleveland Clinic, a 2015 hair review."),
    dict(id="N07", slug="greasy-hair-daily-washing-may-be-fine", field="white", arch="contrast", h_size=104,
         headline="Greasy hair?<br>Daily washing<br>may be fine.", brand_on="espresso",
         defs=[("Oily scalp", "Wash daily if it bothers<br>you (Cleveland Clinic)."),
               ("Straight hair", "A 2021 review: daily washing,<br>less oily shine."),
               ("Curly hair", "Cleveland Clinic advises<br>against washing daily.")],
         tip="Straight hair, oily scalp?<br>You may wash daily (AAD)."),
    dict(id="N08", slug="scalp-scrub-go-gentle", field="espresso", arch="checklist", h_size=112,
         headline="Scalp scrub?<br>Go gentle.",
         items=["Use small,<br>circular motions.", "For about<br>30 seconds.", "Rinse with<br>lukewarm water."],
         note="A scrub removes dead skin cells. Steps: AAD."),
    dict(id="N09", slug="rosemary-water-at-home-know-this-first", field="porcelain", arch="definition", h_size=100,
         headline="Rosemary water<br>at home? Know<br>this first.",
         terms=[("The FDA says", "whoever makes a cosmetic,<br>even at home, owns its safety"),
                ("Essential oils", "some cause skin allergies.<br>Never put them on skin neat.")],
         sum="Changed color or smell?", sum2="Throw it out."),
    dict(id="N10", slug="shedding-or-something-more", field="butter", arch="contrast", h_size=108,
         headline="Shedding, or<br>something more?", brand_on="espresso",
         defs=[("Shedding", "Hairs fall out at the end<br>of their resting phase."),
               ("Normal", "50 to 100 hairs<br>a day (AAD)."),
               ("Not sure?", "A dermatologist can tell.<br>Some people have both.")],
         tip="Excess shedding often<br>stops on its own (AAD)."),
]

# id, slug, board, title, description, link, alt
COPY = [
    ("N01", PINS[0]["slug"], O50, "Fine thin hair over 50 and lots of styling product? Clarify once or twice a month",
     "Fine thin hair over 50 and a shelf of styling products? Cleveland Clinic suggests a clarifying shampoo once or twice a month if you use many. Massage it into your scalp, then conditioner on the ends (AAD). Read the simple routine.",
     L(SHR, "over-50", "N01"), "Card: if you use lots of styling product, a clarifying shampoo once or twice a month, massaged into the scalp, then conditioner on the ends of fine hair."),
    ("N02", PINS[1]["slug"], O50, "Fine thin hair over 50 and coloring? Perm and color one service at a time",
     "Fine thin hair over 50 and coloring? These tips apply to any colored hair: one service at a time, perm or relax 2 weeks before color (AAD), wait 14 days after bleaching, relaxing or perming (FDA), and conditioner after every shampoo. Read more.",
     L(CTH, "over-50", "N02"), "List card: perm or relax 2 weeks before color, wait 14 days after bleaching, relaxing or perming, conditioner after every shampoo."),
    ("N03", PINS[2]["slug"], THIN, "Why is my hair suddenly falling out? 4 first steps to take",
     "Why is your hair suddenly falling out? Often it’s a shed that starts a few months after a big event. Don’t stop a medicine on your own, a blood test can show a low nutrient, and see a dermatologist if it’s sudden, patchy or lasts over six months.",
     L(WHF, "thinning", "N03"), "Checklist of four first steps when hair is suddenly falling out: think back a few months, don't stop a medicine yourself, a blood test, see a dermatologist if sudden, patchy or over 6 months."),
    ("N04", PINS[3]["slug"], THIN, "Thinning hair all over, or in patches? What the pattern can tell you",
     "Thinning hair all over or in patches? A shed usually comes from all over the scalp, says the British Association of Dermatologists, while round patches point to another cause. Patchy, sudden or lasting over six months: see a dermatologist. Read more.",
     L(WHF, "thinning", "N04"), "Split card: thinning all over the scalp is typical of a shed; round patches point to another cause; see a dermatologist if patchy or sudden."),
    ("N05", PINS[4]["slug"], SPA, "Smelly scalp? The most common cause is buildup, and how to clean it",
     "Smelly scalp? Cleveland Clinic says the most common cause is a buildup of skin cells, sweat and scalp oil. Shampoo on your scalp as often as it gets oily, and if you use a lot of styling products, clarify once or twice a month. Read how to clean your scalp.",
     L(CLN, "scalp-care", "N05"), "Card: a smelly scalp is most often buildup of skin cells, sweat and oil; shampoo on the scalp as often as it gets oily; clarify once or twice a month if you use lots of product."),
    ("N06", PINS[5]["slug"], SPA, "Why does my hair get greasy so fast? 4 things that add to it",
     "Why does your hair get greasy so fast? Fine, straight hair carries scalp oil down the strand easily (2015 review). Conditioner on the scalp and styling products that build up add to it (Cleveland Clinic). A thick film of oil leaves hair looking heavy. Read what helps.",
     L(GRS, "scalp-care", "N06"), "List of four reasons hair gets greasy fast: fine straight hair carries oil, conditioner on the scalp, styling product buildup, a thick film of oil looks heavy."),
    ("N07", PINS[6]["slug"], SPA, "Greasy hair? Washing it every day may be fine, especially if it’s straight",
     "Greasy hair and an oily scalp? Cleveland Clinic says you may wash daily if it bothers you. A 2021 review found daily washing left straight hair less oily, and called overcleaning worries unfounded in those studies. Curly hair differs. Read more.",
     L(GRS, "scalp-care", "N07"), "Card: with an oily scalp you may wash daily; a 2021 review found less oily shine on straight hair washed daily; Cleveland Clinic advises against washing curly hair daily."),
    ("N08", PINS[7]["slug"], SPA, "Head spa at home: how to use a scalp scrub gently, in about 30 seconds",
     "Head spa at home with a scalp scrub? A scrub removes dead skin cells and rinses off. The AAD says exfoliate with small circular motions for about 30 seconds, then rinse with lukewarm water. Read which scalp product does what.",
     L(TST, "scalp-care", "N08"), "Checklist for a gentle scalp scrub: small circular motions, about 30 seconds, rinse with lukewarm water."),
    ("N09", PINS[8]["slug"], HC, "Rosemary water for hair at home? 3 safety points to know first",
     "Making rosemary water for hair at home? The FDA says whoever makes a cosmetic, including at home, is responsible for its safety. Some essential oils can cause an allergic skin reaction, so never put them on skin neat, and toss anything that changes color or smell.",
     L(SSO, "ingredients", "N09"), "Definition card: whoever makes a cosmetic at home is responsible for its safety; some essential oils cause skin allergies, never use them neat; throw out anything that changes color or smell."),
    ("N10", PINS[9]["slug"], THIN, "Thinning hair: shedding or something more? A dermatologist can tell",
     "Thinning hair can be shedding, hair loss or both. Shedding happens when hairs reach the end of their resting phase, and 50 to 100 a day is normal (AAD). A dermatologist can tell which you have, and some people have both. Read the difference.",
     L(HSL, "thinning", "N10"), "Card: shedding is hairs falling out at the end of their resting phase, 50 to 100 a day is normal, a dermatologist can tell, some people have both."),
]

if __name__ == "__main__":
    E.PINS = PINS
    E.render(sys.argv[1], set(sys.argv[2:]) or None)
