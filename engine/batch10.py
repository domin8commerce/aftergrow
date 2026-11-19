"""Batch 10 (2026-11-19): the three haircut/hairstyle/over-50 articles are still unpublished (Shopify checked
2026-11-19), make-hair-look-thicker is at its 8-pin cap and batch 9 used the last planned angles for
Hairstyles for thin hair and Dry scalp care. Three Journal articles were verified through the Shopify connector
on 2026-11-19 and added to LIVE_PAGES and the page map: sun-protection-hair-scalp, why-scalp-care-matters and
how-many-hairs-a-day. They open new angles for Hairstyles for thin hair and Fine thin hair over 50 (the part in
the sun), Dry scalp care and Head spa at home (flakes and scalp signs, in season) and Thinning hair (how many
hairs a day, tracking). Plus one unused flyaways angle (when breakage needs a dermatologist). Every hook in the
bank is used, so the hooks here are new surprising facts from these pages. Every fact is on the linked page.
Usage: python3 -I batch10.py <out_dir> [ID ...]"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pinengine as E
import batch2  # noqa: F401  (registers the 15 batch-2 layouts)
from queue_build import L, J, THIN, O50, STYLE, SPA, HC, DRY

SUN = J + "sun-protection-hair-scalp"
WSC = J + "why-scalp-care-matters"
HMD = J + "how-many-hairs-a-day"
FLY = J + "how-to-tame-flyaways"

PINS = [
    dict(id="R01", slug="thin-hair-part-needs-sun-protection", field="espresso", arch="contrast", h_size=100,
         headline="Thin hair?<br>Your part needs<br>sun protection.",
         defs=[("Your hair", "Blocks some of the sun’s<br>rays, but not all."),
               ("Cover it", "A hat, or sunscreen<br>on your part."),
               ("Put it on", "Dry hair, the part<br>and the hairline.")],
         tip="Sources: AAD, Skin<br>Cancer Foundation."),
    dict(id="R02", slug="breakage-that-wont-stop-see-a-dermatologist", field="porcelain", arch="checklist", h_size=104,
         headline="Breakage that<br>won’t stop?",
         items=["Rinse-out conditioner<br>after every wash.", "A light leave-in on<br>mid strands to ends.",
                "Still breaking or<br>hard to manage?<br>See a dermatologist."],
         note="Source: American Academy of Dermatology."),
    dict(id="R03", slug="scalp-flakes-wash-more-often", field="butter", arch="list2", h_size=104,
         headline="Flakes in<br>your hair?", item_size=52, gap=56,
         items=["Not shampooing often<br>enough can cause them.", "So can the wrong conditioner<br>or oil for your hair type.",
                "Wash regularly first.<br>Still there? See a dermatologist."],
         note="Source: American Academy of Dermatology."),
    dict(id="R04", slug="4-scalp-signs-that-show-in-your-hair", field="white", arch="grid4", h_size=116,
         headline="4 scalp signs<br>in your hair.", label_size=50, cell_h=320, grid_top=90,
         cells=[dict(label="Flakes", sub="Wash regularly."),
                dict(label="Oily roots", sub="Wash as often as<br>hair gets oily."),
                dict(label="Buildup", sub="Shampoo on<br>the scalp."),
                dict(label="Itch", sub="Wash regularly.<br>Still there? See<br>a dermatologist.")],
         foot="Source: American Academy of Dermatology."),
    dict(id="R05", slug="30-to-150-hairs-a-day", field="porcelain", arch="bignum", h_size=104,
         headline="How many hairs<br>a day is normal?", big="30–150", big_label="hairs a day for most people.",
         bars=[("AAD", 40, "50 to 100 a day"), ("BAD", 82, "30 to 150 a day")],
         lines=["New hairs replace the ones that fall.", "A normal day is a range, not one number."]),
    dict(id="R06", slug="shedding-looks-heavier-on-wash-day", field="espresso", arch="definition", h_size=100,
         headline="Shedding can<br>look heavier on<br>wash day.",
         terms=[("Why", "extra hair shows most after<br>washing or brushing (BAD)"),
                ("So", "compare a wash day<br>with a wash day")],
         sum="Track it the same", sum2="way each time."),
    dict(id="R07", slug="what-a-shed-count-cant-tell-you", field="white", arch="split", h_size=100, band_h=470,
         split_top=150, marks=False, headline="Counting shed<br>hairs? Know<br>the limits.",
         left=("It can show", ["A rough trend<br>over weeks"]),
         right=("It can’t", ["Tell you<br>the cause", "Prove a<br>product worked"]),
         item_size=46, foot="Worried? See a dermatologist."),
    dict(id="R08", slug="sunscreen-on-your-part-where-and-when", field="butter", arch="checklist", h_size=104,
         headline="Sunscreen on<br>your part.",
         items=["On dry hair.", "Along the part<br>and the hairline.", "15 minutes<br>before you go out.",
                "Again every<br>2 hours."],
         note="Sources: AAD, Skin Cancer Foundation."),
    dict(id="R09", slug="check-your-scalp-in-your-skin-self-exam", field="porcelain", arch="list2", h_size=104,
         headline="Check your<br>scalp too.", item_size=52, gap=56,
         items=["Include it in your monthly<br>skin self-exam.", "Look for anything new,<br>changing or unusual.",
                "Worried? See a<br>dermatologist soon."],
         note="Source: The Skin Cancer Foundation."),
    dict(id="R10", slug="hair-products-with-spf-what-to-know", field="espresso", arch="contrast", h_size=100,
         headline="Hair products<br>with sun filters?",
         defs=[("They exist", "Some leave-ins, sprays<br>and powders have them."),
               ("Wet hair sprays", "Sunscreen on dry hair<br>may work better."),
               ("Simple fix", "A face sunscreen<br>works on your scalp.")],
         tip="Sources: AAD, Skin<br>Cancer Foundation."),
]

# id, slug, board, title, description, link, alt
COPY = [
    ("R01", PINS[0]["slug"], STYLE, "Hairstyles for thin hair: your part needs sun protection too",
     "Hairstyles for thin hair leave the part in the sun. Hair blocks some of the sun’s rays, not all. For thinning hair, the AAD says wear a wide-brimmed hat or use sunscreen on your scalp. The Skin Cancer Foundation says apply it to dry hair along the part and hairline. Read more.",
     L(SUN, "hairstyles", "R01"), "Card: hair blocks some of the sun’s rays but not all; cover it with a hat or sunscreen on the part; apply to dry hair along the part and hairline."),
    ("R02", PINS[1]["slug"], STYLE, "Hairstyles for thin hair keep breaking? When to see a dermatologist",
     "Hairstyles for thin hair keep breaking? The AAD suggests conditioner after every wash plus a light leave-in from mid strands to ends. If breakage or hard-to-manage hair continues after that, see a dermatologist. Read how to tame flyaways.",
     L(FLY, "hairstyles", "R02"), "Checklist: rinse-out conditioner after every wash, a light leave-in on mid strands to ends, and if hair still breaks or is hard to manage, see a dermatologist."),
    ("R03", PINS[2]["slug"], DRY, "Dry scalp or dandruff flakes? Not shampooing enough can cause them",
     "Flakes in your hair this winter? The AAD says flakes can come from not shampooing often enough, or from the wrong conditioner, oil or scalp moisturizer for your hair type. Wash regularly first, and see a dermatologist if they stay. Read more.",
     L(WSC, "dry-scalp", "R03"), "List: flakes can come from not shampooing often enough or the wrong conditioner or oil for your hair type; wash regularly, and see a dermatologist if they stay."),
    ("R04", PINS[3]["slug"], SPA, "Head spa at home: 4 scalp signs that show in your hair",
     "Head spa at home starts with reading your scalp. Flakes, oily roots, buildup and itch all show in your hair. The AAD’s first steps: wash regularly, wash as often as hair gets oily and put shampoo on the scalp. Read why scalp care matters.",
     L(WSC, "scalp-care", "R04"), "Grid of four scalp signs and a first step for each: flakes, wash regularly; oily roots, wash as often as hair gets oily; buildup, shampoo on the scalp; itch, wash regularly and see a dermatologist if it stays."),
    ("R05", PINS[4]["slug"], THIN, "Thinning hair or a normal day? Most people lose 30 to 150 hairs",
     "Thinning hair or a normal day? The British Association of Dermatologists says most people lose 30 to 150 scalp hairs a day, and new hairs replace them. The AAD gives 50 to 100. A normal day is a range. Read how to track shedding.",
     L(HMD, "thinning", "R05"), "Big number 30 to 150: most people lose 30 to 150 hairs a day (BAD); the AAD range is 50 to 100; new hairs replace the ones that fall."),
    ("R06", PINS[5]["slug"], THIN, "Thinning hair on wash day? Why shedding can look heavier after washing",
     "Thinning hair can look worse on wash day. The British Association of Dermatologists says extra hair is most noticeable after washing or brushing. So compare a wash day with a wash day, not with a day you skipped. Read how to track shedding.",
     L(HMD, "thinning", "R06"), "Definition card: shedding can look heavier on wash day because extra hair shows most after washing or brushing (BAD), so compare a wash day with a wash day."),
    ("R07", PINS[6]["slug"], THIN, "Thinning hair and shed counts: what counting hairs can’t tell you",
     "Thinning hair and counting shed hairs? A count shows a rough trend over weeks. It can’t tell you the cause, and since a shed often stops on its own (AAD), a lower count doesn’t prove a product worked. Read how to track it fairly.",
     L(HMD, "thinning", "R07"), "Split card: a shed count can show a rough trend over weeks; it can’t tell you the cause or prove a product worked."),
    ("R08", PINS[7]["slug"], O50, "Fine thin hair over 50? Sunscreen on your part: where and when",
     "Fine thin hair over 50 shows more of the part. Put sunscreen on dry hair along the part and the hairline, about 15 minutes before you go out, and again every 2 hours (AAD, Skin Cancer Foundation). Or wear a hat. Read the guide.",
     L(SUN, "over-50", "R08"), "Checklist for sunscreen on the part: on dry hair, along the part and hairline, 15 minutes before going out, again every 2 hours."),
    ("R09", PINS[8]["slug"], SPA, "Head spa at home: check your scalp in your monthly skin check",
     "Head spa at home is a good moment to look at your scalp. The Skin Cancer Foundation says to include it in your monthly skin self-exam, look for anything new, changing or unusual, and see a dermatologist soon if something worries you.",
     L(SUN, "scalp-care", "R09"), "List: include your scalp in your monthly skin self-exam, look for anything new, changing or unusual, and see a dermatologist if worried."),
    ("R10", PINS[9]["slug"], HC, "Hair products with sun filters: do they protect your scalp?",
     "Hair products with sun filters? The AAD says many leave-ins, sprays and powders include them. A Skin Cancer Foundation dermatologist thinks sunscreen on dry hair works better than sprays on wet hair, though both may add protection. A face sunscreen works on your scalp.",
     L(SUN, "ingredients", "R10"), "Card: some leave-ins, sprays and powders have sun filters; sunscreen on dry hair may work better than sprays on wet hair; a face sunscreen works on the scalp."),
]

if __name__ == "__main__":
    E.PINS = PINS
    E.render(sys.argv[1], set(sys.argv[2:]) or None)
