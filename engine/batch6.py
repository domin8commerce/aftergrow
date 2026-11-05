"""Batch 6 (2026-11-05): make-hair-look-thicker is still at its 8-pin cap and the three haircut/hairstyle/over-50
articles are still unpublished (Shopify checked 2026-11-05), so the haircut and hairstyle boards get nothing new.
Dry scalp care (in season) goes first, then Fine thin hair over 50, then Thinning hair and one scalp-safety hook.
Every fact is on the linked page (read through Shopify 2026-11-05) and in the RUNBOOK fact sheet or page map.
Usage: python3 -I batch6.py <out_dir> [ID ...]"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pinengine as E
import batch2  # noqa: F401  (registers the 15 batch-2 layouts)
from queue_build import L, J, DRY, THIN, O50, SPA

DSC = J + "can-dry-scalp-cause-hair-loss"
WHY = J + "why-is-my-hair-so-dry"
CTH = J + "color-treated-hair-care"
SHR = J + "simple-hair-care-routine"
IMT = J + "is-my-hair-thinning"

PINS = [
    dict(id="M01", slug="can-a-dry-scalp-make-hair-fall-out", field="white", arch="list2", h_size=106, band_h=430,
         list_top=150, headline="Can a dry<br>scalp make<br>hair fall out?", item_size=46, gap=46,
         items=["Dryness alone: itching<br>and flakes.", "Hard scratching<br>can loosen hair.",
                "Some lookalikes can<br>come with shedding.", "Not improving?<br>See a dermatologist."],
         note="Sources: AAD, Cleveland Clinic."),
    dict(id="M02", slug="dry-scalp-or-dandruff-hard-to-tell-at-home", field="espresso", arch="definition", h_size=100,
         headline="Dry scalp or<br>dandruff? Hard<br>to tell at home.",
         terms=[("The AAD says", "even these two can be<br>tricky to tell apart"),
                ("At the appointment", "say what you notice:<br>itch, flakes, rash, pain")],
         sum="Store products not helping?", sum2="See a board-certified<br>dermatologist (AAD)."),
    dict(id="M03", slug="hair-drier-with-age-3-changes", field="butter", arch="contrast", h_size=108,
         headline="Hair feeling<br>drier with age?", brand_on="espresso",
         defs=[("Why", "Scalp oil typically drops<br>with age."),
               ("Washing", "You may need to wash<br>less often than before."),
               ("Fine, straight hair", "Conditioner on the ends, and<br>just a little leave-on product.")],
         tip="Sources: Cleveland Clinic,<br>a 2015 hair review."),
    dict(id="M04", slug="dry-hair-or-dry-scalp", field="porcelain", arch="contrast", h_size=112,
         headline="Dry hair, or<br>dry scalp?", brand_on="espresso",
         defs=[("Dry hair", "Rough, dull lengths. Use<br>conditioner after every wash."),
               ("Dry scalp", "Tight or flaky skin. That’s<br>the scalp, not the hair."),
               ("Both at once", "Oily roots with dry ends.")],
         tip="Different problems,<br>different fixes."),
    dict(id="M05", slug="colored-hair-sun-can-make-it-brittle", field="espresso", arch="contrast", h_size=108,
         headline="Colored hair?<br>Sun can make<br>it brittle.",
         defs=[("Sun", "A wide-brimmed hat, or a<br>leave-in with zinc oxide."),
               ("Pool", "Swim cap, rinse right after,<br>then a swimmers’ shampoo."),
               ("Heat", "Low or medium, with a<br>heat protectant.")],
         tip="Source: American Academy<br>of Dermatology."),
    dict(id="M06", slug="you-can-react-to-a-dye-youve-used-before", field="porcelain", arch="checklist", h_size=100,
         headline="You can react<br>to a dye you’ve<br>used before.",
         items=["Follow the label,<br>skin test included.", "Wear gloves and<br>use a timer.",
                "Never mix different<br>hair dye products."],
         note="Source: FDA."),
    dict(id="M07", slug="simple-hair-care-routine-in-order", field="white", arch="list2", h_size=104, band_h=430,
         list_top=150, headline="A simple hair<br>routine, in order.", item_size=44, gap=34,
         items=["1. Shampoo: into the scalp.", "2. Condition: ends, if fine.", "3. Dry: wrap or blot.",
                "4. Detangle: wide-tooth comb.", "5. Scalp step (optional): its label.", "6. Style: low or medium heat."],
         note="Sources: AAD, FDA."),
    dict(id="M08", slug="thinning-hard-to-judge-by-eye-keep-4-the-same", field="butter", arch="list2", h_size=104,
         band_h=430, list_top=150, headline="Thinning is hard<br>to judge by eye.<br>Keep 4 the same.",
         item_size=48, gap=48,
         items=["Time since your<br>last wash.", "Styling product,<br>or none.", "Where you part<br>your hair.",
                "The light, and where<br>you stand."],
         note="Then compare with an earlier photo."),
]

# id, slug, board, title, description, link, alt
COPY = [
    ("M01", PINS[0]["slug"], DRY, "Can a dry scalp make your hair fall out? What dermatologists say",
     "Dry scalp on its own: neither the AAD nor Cleveland Clinic says dryness alone causes hair loss; both describe itching and flakes. Hard scratching can loosen hair, and some lookalike conditions can come with shedding. Read when to see a dermatologist.",
     L(DSC, "dry-scalp", "M01"), "List card: a dry scalp alone means itching and flakes, hard scratching can loosen hair, some lookalikes come with shedding, see a dermatologist if it is not improving."),
    ("M02", PINS[1]["slug"], DRY, "Dry scalp or dandruff? Even these two are hard to tell apart at home",
     "Dry scalp or dandruff? The AAD says even these two can be tricky to tell apart without a dermatologist. Note what you see, like itching, flakes, a rash or pain, and if store products don’t help, see a board-certified dermatologist. Read more.",
     L(DSC, "dry-scalp", "M02"), "Definition card: the AAD says dry scalp and dandruff can be tricky to tell apart; note itch, flakes, rash or pain and see a dermatologist if products do not help."),
    ("M03", PINS[2]["slug"], O50, "Fine thin hair over 50 feeling drier? Why, and 3 changes to try",
     "Fine thin hair over 50 feeling drier? Cleveland Clinic says oil production typically drops with age, especially after menopause, so you may need to wash less often. For fine, straight hair: conditioner on the ends and only a little leave-on product. Read more.",
     L(WHY, "over-50", "M03"), "Card on hair that feels drier with age: scalp oil typically drops, you may need to wash less often, fine straight hair needs conditioner on the ends and little leave-on product."),
    ("M04", PINS[3]["slug"], DRY, "Dry scalp or dry hair? Two different problems with different fixes",
     "Dry scalp or dry hair? They’re different problems. Rough, dull lengths are your hair: use conditioner after every wash. A tight or flaky scalp is the skin of your scalp. Oily roots with dry ends means both at once. Read which fix fits you.",
     L(WHY, "dry-scalp", "M04"), "Card comparing dry hair, rough and dull lengths that need conditioner after every wash, with dry scalp, tight or flaky skin, and oily roots with dry ends."),
    ("M05", PINS[4]["slug"], O50, "Fine thin hair over 50 and colored? Sun can make dyed hair brittle",
     "Fine thin hair over 50 and colored? These AAD tips apply to any dyed hair: sun can make it weak, dry and brittle, so wear a wide-brimmed hat or a leave-in with zinc oxide. Swim cap and a rinse after the pool, low or medium heat. Save it for later.",
     L(CTH, "over-50", "M05"), "Card with three ways to protect colored hair: a wide-brimmed hat or zinc oxide leave-in for sun, a swim cap and rinse for the pool, low or medium heat."),
    ("M06", PINS[5]["slug"], SPA, "Hair dye allergy: you can react even to a dye you’ve used before",
     "Hair dye allergy can show up even with a dye you’ve used before without a problem, the FDA says. Follow every label direction, skin test included, wear gloves, time it, and never mix different hair dye products. Read the color-day scalp guide.",
     L(CTH, "scalp-care", "M06"), "Checklist of three FDA hair dye safety rules: follow the label including the skin test, wear gloves and use a timer, never mix different dye products."),
    ("M07", PINS[6]["slug"], O50, "Simple hair care routine for fine thin hair: 6 steps, in order",
     "A simple hair care routine for fine thin hair, in order: massage shampoo into your scalp, conditioner on the ends, wrap or blot dry, detangle with a wide-tooth comb, an optional scalp step, then style on low or medium heat (AAD). Read the full routine.",
     L(SHR, "over-50", "M07"), "Numbered list of a simple hair routine in order: shampoo, condition, dry, detangle, optional scalp step, style."),
    ("M08", PINS[7]["slug"], THIN, "Is my hair thinning? Why it’s hard to judge by eye, and 4 things to keep the same",
     "Is my hair thinning? Slow change is hard to spot when you see your hair every day. Keep four things the same each time you look: time since washing, styling product, your part and the light. Then compare with an earlier photo. Read more.",
     L(IMT, "thinning", "M08"), "List of four things to keep the same when checking for thinning hair: time since washing, styling product, where you part, the light."),
]

if __name__ == "__main__":
    E.PINS = PINS
    E.render(sys.argv[1], set(sys.argv[2:]) or None)
