"""Reels R1: the first 13 Reels-only scripts (Oct 13 to 25, 2026), one a day.

Each opens on a pain point a woman 35 to 60 actually feels, answers it with facts from the RUNBOOK fact sheet and
Journal page map only, and ends on a save-and-send ask. "Hair loss" never appears on screen.
Scene types: hook, say, big, checks, list, steps, vs, swaps, cta (see engine/reel2.py).
"""


def caps(answer, ig_end, fb_end):
    """Instagram and Facebook captions share the answer; Instagram ends on the ask, Facebook on the comment link."""
    return answer + "\n\n" + ig_end, answer + "\n\n" + fb_end


AAD = "American Academy of Dermatology"

_AG10 = caps(
    "Hair in the brush, hair in the drain. Is it just shedding?\n\n"
    "Shed hairs fall out at the end of their resting phase. Excessive shedding often stops on its own as the body readjusts, "
    "according to the American Academy of Dermatology. Shedding and hair loss aren't the same thing. A dermatologist "
    "can tell which you have, and some people have both.\n\n"
    "If shedding is still heavy after six months, see a dermatologist.",
    "Save this, and send it to someone who's worried about her brush.",
    "How to tell shedding from something more is in the first comment.")

_AG11 = caps(
    "Taking biotin for your hair? Read this before your next blood test.\n\n"
    "The FDA says biotin can cause falsely high or falsely low blood test results. Biotin is vitamin B7, so check every "
    "label for either name. And the FDA doesn't approve supplements before they're sold.\n\n"
    "Tell your doctor you take biotin before any blood test, and don't take a supplement instead of a prescription medicine.",
    "Save this, and send it to a friend who takes hair vitamins.",
    "What to ask before you take a hair supplement is in the first comment.")

_AG03 = caps(
    "How much hair shedding is normal? It's normal to shed 50 to 100 hairs a day, according to the American Academy of "
    "Dermatology.\n\n"
    "After a big change in the body, a shed can start two to four months later, and for most people it settles within six to "
    "nine months.\n\n"
    "Instead of counting hairs, take one photo of your part every six weeks, from the same window at the same angle.",
    "Save this, and send it to a friend who's been counting.",
    "Why shedding happens, and when it settles, is in the first comment.")

_AG04 = caps(
    "Rosemary oil, rosemary water and rosemary extract are not the same thing.\n\n"
    "Rosemary extract in a finished product is one ingredient in a set formula, with directions and warnings on the label. "
    "Rosemary essential oil should never go on skin neat, meaning undiluted, and some essential oils can cause an allergic skin "
    "reaction. Homemade rosemary water is on you: whoever makes a cosmetic is responsible for its safety, says the FDA.\n\n"
    "Trying a finished product? Patch test it first. We make no claims about what rosemary does for hair. This is about "
    "using it safely.",
    "Save this before the next rosemary trend, and send it to a rosemary fan.",
    "The full comparison is in the first comment.")

_AG13 = caps(
    "Checking your part in the mirror every day? There's a fairer way to see real change.\n\n"
    "Take one part photo every six weeks: week 0, week 6 and week 12. Use the same window and daylight, at the same time of "
    "day. Hold your phone above your head, camera down, about a foot away. No filter, flash or zoom, and dry hair parted in "
    "the same place every time.",
    "Save this for your next photo, and send it to someone who checks every day.",
    "How the six-week photo check works is in the first comment.")

_AG07 = caps(
    "Flakes on your shoulders again? Dry scalp and dandruff aren't the same thing.\n\n"
    "A dry scalp comes from a loss of moisture. Dandruff comes from excess oil, according to Cleveland Clinic. So it helps to "
    "know which one you have.\n\n"
    "For a dry scalp: keep showers to 5 to 10 minutes, choose fragrance-free products, and keep leave-in conditioner on your "
    "hair, not your scalp. If the itching won't stop, or you see a red rash or swelling, call a dermatologist.",
    "Save this for winter, and send it to someone with an itchy scalp.",
    "What to look for in a product for a dry scalp is in the first comment.")

_AG14 = caps(
    "Suddenly finding more hair everywhere? The pattern tells you a lot.\n\n"
    "A shed usually comes from all over the scalp, says the British Association of Dermatologists. Round patches point to "
    "another cause. A shed often starts a few months after a big event.\n\n"
    "Don't stop a medicine on your own, and ask whether a blood test for low nutrients makes sense. See a dermatologist if it's "
    "sudden, patchy or lasts more than six months.",
    "Save this, and send it to someone who's worried.",
    "Why hair suddenly falls out, and the first steps, are in the first comment.")

_AG09 = caps(
    "Hair feeling like straw lately? Simple changes that help dry hair.\n\n"
    "MedlinePlus suggests washing about once or twice a week for dry hair. Use conditioner after every wash, air dry when you "
    "can, and rinse right after swimming. Wrap your hair in a towel instead of rubbing it, and if you use hot tools, use the "
    "lowest heat setting, says the American Academy of Dermatology.\n\n"
    "If gentle care doesn't help, see a health care provider.",
    "Save this for wash day, and send it to someone with dry hair.",
    "The full guide to dry hair is in the first comment.")

_AG15 = caps(
    "Four words on hair product labels that mean less than you think.\n\n"
    "\"Hypoallergenic\" has no federal standard, and \"unscented\" may still contain fragrance, says the FDA. \"Natural\" has "
    "no rule, and the FDA says an ingredient's source doesn't decide its safety. \"Made with organic ingredients\" means at "
    "least 70% organically produced ingredients, while the USDA Organic seal means at least 95%, not counting water and salt.\n\n"
    "Read the ingredient list, not the front of the bottle.",
    "Save this for your next shopping trip, and send it to the friend who reads every label.",
    "Eight checks before you buy a scalp serum are in the first comment.")

_AG06 = caps(
    "Postpartum hair shedding usually peaks about four months after giving birth, according to the American Academy of "
    "Dermatology.\n\n"
    "Most women see their hair return to its normal fullness by their child's first birthday. Two "
    "dermatologist tips for the months in between: use a shampoo and conditioner that add volume, and try a new haircut. "
    "Some haircuts make hair look fuller.\n\n"
    "If your hair isn't back to its normal fullness after a year, see a dermatologist.",
    "Save this, and send it to a new mom who needs to hear it.",
    "Why hair sheds a few months after a big event, like giving birth, is in the first comment.")

_AG12 = caps(
    "Itchy scalp after a gentle shampoo? Fragrance-free doesn't mean irritation-free.\n\n"
    "A fragrance-free product can still irritate or contain an allergen. Read the ingredient list, not the front label, and "
    "look for Fragrance, Parfum or Perfume.\n\n"
    "Switching products? Change one at a time, and stop any product that gives you a rash, redness or a burn.",
    "Save this for your next shampoo run, and send it to someone with a sensitive scalp.",
    "Five steps to a fragrance-free hair routine are in the first comment.")

_AG05 = caps(
    "Hair care over 40: five habits to retire, and what to do instead.\n\n"
    "Shampoo your scalp, not the lengths. Pick styles that don't need long-hold products. Stretch the time between color "
    "touch-ups, and book one chemical service at a time. And judge your hair with a part photo every six weeks, not the "
    "bathroom mirror.\n\n"
    "If your part is getting wider or your ponytail feels thinner, see a dermatologist.",
    "Save this, and send it to a friend who'll try it with you.",
    "How to make thin hair look thicker, with products, cut and color, is in the first comment.")

_AG08 = caps(
    "Oily roots and dry ends? Wash for your scalp and condition for your ends.\n\n"
    "Wash as often as your scalp needs, even every day if the oil bothers you. Put shampoo on the scalp only, and conditioner "
    "on the ends: on the scalp it can make things greasy, says Cleveland Clinic.\n\n"
    "And dry shampoo doesn't clean hair, so wash after one or two uses, says the American Academy of Dermatology.",
    "Save this for wash day.",
    "A simple routine for oily roots and dry ends is in the first comment.")

REELS = [
 dict(id="AG10", audio="1033455569449469", pillar="shedding", kicker="Shedding, or more?", field="espresso", page="/blogs/journal/hair-shedding-vs-hair-loss",
      scenes=[
        dict(t="hook", lines=["More hair", "in the drain", "<mark>lately</mark>?"],
             sub="Shedding, or something more? Here&#39;s how to&nbsp;tell."),
        dict(t="say", title="Shed hairs fall out at the end of their resting&nbsp;phase.",
             body="A shed often stops on its own, says the American Academy of&nbsp;Dermatology."),
        dict(t="big", label="No cause found", num="1 in 3", caption="people diagnosed with<br>telogen&nbsp;effluvium.", capsize=76,
             source="British Association of Dermatologists"),
        dict(t="checks", title="See a dermatologist&nbsp;if", items=[
            "It&#39;s still heavy after six&nbsp;months.", "You can&#39;t tell if it&#39;s shedding or something&nbsp;more."]),
        dict(t="cta", line="Send it to someone who&#39;s&nbsp;worried.")],
      hashtags=["hairshedding", "telogeneffluvium", "thinninghair", "hairhealth", "hairfacts"],
      ig=_AG10[0], fb=_AG10[1], fb_comment="Hair shedding or something more? How to tell: {link}"),

 dict(id="AG11", audio="1579921342191993", pillar="supplements", kicker="Hair vitamins", field="butter", page="/blogs/journal/scalp-serum-or-hair-supplement",
      scenes=[
        dict(t="hook", lines=["Taking <mark>biotin</mark>", "for your hair?"], sub="Read this before your next blood&nbsp;test."),
        dict(t="say", title="Biotin can cause <mark>falsely high or low</mark> blood test&nbsp;results.", source="U.S. FDA"),
        dict(t="say", title="Check every label for biotin, or vitamin&nbsp;B7.", body="Same thing, two&nbsp;names."),
        dict(t="say", title="The FDA doesn&#39;t approve supplements before they&#39;re&nbsp;sold."),
        dict(t="checks", title="Ask your doctor&nbsp;first", items=[
            "Tell them you take biotin before any blood&nbsp;test.",
            "Don&#39;t take a supplement instead of a prescription&nbsp;medicine."], source="U.S. FDA"),
        dict(t="cta", line="Send it to a friend who takes hair&nbsp;vitamins.")],
      hashtags=["biotin", "hairvitamins", "hairsupplements", "healthyhair", "haircaretips"],
      ig=_AG11[0], fb=_AG11[1], fb_comment="Questions to ask before you take a hair supplement: {link}"),

 dict(id="AG03", audio="1386811643506297", pillar="shedding", kicker="How much is normal?", field="espresso", page="/pages/how-it-works",
      scenes=[
        dict(t="hook", lines=["How much", "shedding is", "<mark>normal</mark>?"], sub="Dermatologists have a&nbsp;number."),
        dict(t="big", label="A normal day", num="50&ndash;100", caption="hairs a day.", source=AAD),
        dict(t="say", title="After a big change, a shed can start <mark>2 to 4 months</mark>&nbsp;later.",
             body="For most people, it settles within 6 to 9&nbsp;months.", source="getaftergrow.com, How it works"),
        dict(t="say", title="Stop counting hairs.", body="Take one part photo every six weeks instead. Same window, same&nbsp;angle."),
        dict(t="cta", line="Send it to someone who&#39;s been&nbsp;counting.")],
      hashtags=["hairshedding", "hairhealth", "thinninghair", "scalpcare", "hairtips"],
      ig=_AG03[0], fb=_AG03[1], fb_comment="Why shedding happens, and when it settles: {link}"),

 dict(id="AG04", audio="1549201939908190", pillar="ingredients", kicker="Rosemary, honestly", field="espresso", page="/blogs/journal/scalp-serum-or-scalp-oil",
      scenes=[
        dict(t="hook", lines=["Rosemary", "oil, water", "or <mark>extract</mark>?"], sub="Not the same thing. Here&#39;s the&nbsp;difference."),
        dict(t="say", label="Extract", title="One ingredient in a set formula.", body="With directions and warnings on the&nbsp;label."),
        dict(t="say", label="Essential oil", title="Never goes on skin&nbsp;<mark>neat</mark>.",
             body="Some essential oils can cause an allergic skin&nbsp;reaction."),
        dict(t="say", label="Homemade water", title="Whoever makes it is responsible for its&nbsp;<mark>safety</mark>.",
             source="U.S. FDA"),
        dict(t="checks", title="Before you try&nbsp;one", items=[
            "Patch test a finished product&nbsp;first.", "Stop at a rash, redness or&nbsp;burn."]),
        dict(t="cta", line="Send it to a rosemary&nbsp;fan.")],
      hashtags=["rosemaryforhair", "rosemarywater", "scalpcare", "haircare", "cleanbeauty"],
      ig=_AG04[0], fb=_AG04[1], fb_comment="Rosemary extract vs. rosemary oil vs. rosemary water, compared: {link}"),

 dict(id="AG13", audio="1326560949104401", pillar="progress", kicker="Track it fairly", field="butter", page="/pages/the-check-in",
      scenes=[
        dict(t="hook", lines=["Checking", "your part", "<mark>every day</mark>?"], sub="There&#39;s a fairer way than the&nbsp;mirror."),
        dict(t="say", title="Take one part photo every <mark>six weeks</mark>.", body="Week 0, week 6, week 12. Then&nbsp;compare."),
        dict(t="list", title="The photo&nbsp;rules", items=[
            "Same window, daylight, same time of&nbsp;day.", "Phone above your head, camera&nbsp;down.",
            "About a foot&nbsp;away.", "No filter, flash or&nbsp;zoom."]),
        dict(t="say", title="Dry hair, parted in the same place every&nbsp;time."),
        dict(t="cta", title="Save this for<br>photo&nbsp;day.", line="Send it to someone who checks every&nbsp;day.")],
      hashtags=["hairshedding", "thinninghair", "hairhealth", "haircaretips", "hairprogress"],
      ig=_AG13[0], fb=_AG13[1], fb_comment="The six-week part photo, step by step: {link}"),

 dict(id="AG07", audio="2271125906413476", pillar="scalp-care", kicker="Dry scalp season", field="butter", page="/blogs/journal/scalp-serum-for-dry-scalp",
      scenes=[
        dict(t="hook", lines=["Flakes on", "your shoulders", "<mark>again</mark>?"], sub="Dry scalp and dandruff aren&#39;t the same&nbsp;thing."),
        dict(t="vs", title="Different&nbsp;causes.", left=("Dry scalp", "A loss of moisture"),
             right=("Dandruff", "Excess oil"), source="Cleveland Clinic"),
        dict(t="list", title="For a dry&nbsp;scalp", items=[
            "Keep showers to 5 to 10&nbsp;minutes.", "Choose fragrance-free&nbsp;products.",
            "Leave-in conditioner on hair, not&nbsp;scalp."], source="American Academy of Dermatology and the FDA"),
        dict(t="checks", title="Call a dermatologist&nbsp;if", items=[
            "The itching won&#39;t&nbsp;stop.", "You have a red&nbsp;rash.", "Skin is swollen, warm or&nbsp;painful."]),
        dict(t="cta", title="Save this for&nbsp;winter.", line="Send it to someone with an itchy&nbsp;scalp.")],
      hashtags=["dryscalp", "dandruff", "scalpcare", "itchyscalp", "winterhaircare"],
      ig=_AG07[0], fb=_AG07[1], fb_comment="Scalp serum for a dry scalp: what to look for: {link}"),

 dict(id="AG14", audio="1033455569449469", pillar="shedding", kicker="Read the pattern", field="espresso", page="/blogs/journal/why-is-my-hair-falling-out",
      scenes=[
        dict(t="hook", lines=["More hair", "everywhere,", "<mark>all at once</mark>?"], sub="The pattern tells you a&nbsp;lot."),
        dict(t="vs", title="Where it comes&nbsp;from", left=("A shed", "Usually all over the scalp"),
             right=("Round patches", "Point to another cause"), source="British Association of Dermatologists"),
        dict(t="list", title="First&nbsp;steps", items=[
            "Don&#39;t stop a medicine on your&nbsp;own.", "Ask about a blood test for low&nbsp;nutrients."]),
        dict(t="checks", title="See a dermatologist&nbsp;if", items=[
            "It&#39;s&nbsp;sudden.", "It&#39;s&nbsp;patchy.", "It lasts over six&nbsp;months."]),
        dict(t="cta", line="Send it to someone who&#39;s&nbsp;worried.")],
      hashtags=["hairshedding", "thinninghair", "hairhealth", "telogeneffluvium", "hairfacts"],
      ig=_AG14[0], fb=_AG14[1], fb_comment="Why is my hair suddenly falling out? Causes and first steps: {link}"),

 dict(id="AG09", audio="761736589642441", pillar="habits", kicker="Dry hair season", field="butter", page="/blogs/journal/why-is-my-hair-so-dry",
      scenes=[
        dict(t="hook", lines=["Hair feeling", "like <mark>straw</mark>", "lately?"], sub="Simple changes that help dry&nbsp;hair."),
        dict(t="list", title="For dry&nbsp;hair", items=[
            "Wash once or twice a&nbsp;week.", "Condition after every&nbsp;wash.", "Air dry when you&nbsp;can.",
            "Rinse right after&nbsp;swimming."], source="MedlinePlus and the American Academy of Dermatology"),
        dict(t="say", title="Towel? <mark>Wrap</mark>, don&#39;t&nbsp;rub.", body="Then let it air&nbsp;dry.", source=AAD),
        dict(t="say", title="Hot tools? Lowest heat&nbsp;setting.", body="And use them once a week, or even less&nbsp;often.", source=AAD),
        dict(t="cta", title="Save this for wash&nbsp;day.", line="Send it to someone with dry&nbsp;hair.")],
      hashtags=["dryhair", "dryhairtips", "haircaretips", "washday", "winterhaircare"],
      ig=_AG09[0], fb=_AG09[1], fb_comment="Why is my hair so dry? Causes and four changes that help: {link}"),

 dict(id="AG15", audio="1579921342191993", pillar="ingredients", kicker="Label check", field="espresso", page="/blogs/journal/what-to-look-for-in-a-scalp-serum",
      scenes=[
        dict(t="hook", lines=["4 label words", "that mean less", "than you&nbsp;think."], sub="Read this before your next hair&nbsp;product."),
        dict(t="say", label="Hypoallergenic", title="Has no federal&nbsp;standard.", source="U.S. FDA"),
        dict(t="say", label="Unscented", title="May still contain&nbsp;<mark>fragrance</mark>.", source="U.S. FDA"),
        dict(t="say", label="Natural", title="Has no&nbsp;rule.", body="And an ingredient&#39;s source doesn&#39;t decide its safety, says the&nbsp;FDA."),
        dict(t="say", label="Made with organic ingredients", title="Means at least&nbsp;70%.",
             body="The USDA Organic seal means at least 95%, not counting water and&nbsp;salt."),
        dict(t="cta", line="Send it to the friend who reads every&nbsp;label.")],
      hashtags=["cleanbeauty", "haircare", "ingredientcheck", "scalpcare", "beautytips"],
      ig=_AG15[0], fb=_AG15[1], fb_comment="Eight checks before you buy a scalp serum: {link}"),

 dict(id="AG06", audio="592271352837708", pillar="postpartum", kicker="Postpartum hair", field="espresso", page="/blogs/journal/why-is-my-hair-falling-out",
      scenes=[
        dict(t="hook", lines=["Postpartum", "shedding usually", "peaks around", "<mark>month&nbsp;4</mark>."], sub="Here&#39;s what&#39;s&nbsp;normal."),
        dict(t="steps", title="What to&nbsp;expect", steps=[
            ("A few months after birth", "Extra shedding starts."), ("About month 4", "It usually peaks."),
            ("By the first birthday", "Fullness returns for most.")]),
        dict(t="list", title="Two dermatologist&nbsp;tips", items=[
            "Shampoo and conditioner that add&nbsp;volume.", "A new haircut. Some make hair look&nbsp;fuller."], source=AAD),
        dict(t="checks", title="See a dermatologist&nbsp;if", items=[
            "It comes out in&nbsp;patches.", "It isn&#39;t back to normal fullness after a&nbsp;year."]),
        dict(t="cta", line="Send it to a new&nbsp;mom.")],
      hashtags=["postpartumhair", "postpartum", "newmom", "hairshedding", "momlife"],
      ig=_AG06[0], fb=_AG06[1], fb_comment="Why hair sheds a few months after a big event, like giving birth: {link}"),

 dict(id="AG12", audio="2477944699150252", pillar="ingredients", kicker="Fragrance-free, honestly", field="butter", page="/blogs/journal/fragrance-free-hair-routine",
      scenes=[
        dict(t="hook", lines=["Itchy scalp", "after a", "<mark>gentle</mark> shampoo?"], sub="Fragrance-free isn&#39;t irritation&#8209;free."),
        dict(t="say", title="Fragrance-free products can still&nbsp;irritate.", body="Or contain an&nbsp;allergen."),
        dict(t="say", title="Read the list, not the front&nbsp;label.", body="Look for Fragrance, Parfum or&nbsp;Perfume."),
        dict(t="checks", title="Switching? Go&nbsp;slowly.", items=[
            "Change one product at a&nbsp;time.", "Stop at a rash, redness or&nbsp;burn."]),
        dict(t="cta", title="Save this for your next shampoo&nbsp;run.", line="Send it to someone with a sensitive&nbsp;scalp.")],
      hashtags=["fragrancefree", "fragrancefreehaircare", "sensitivescalp", "cleanbeauty", "scalpcare"],
      ig=_AG12[0], fb=_AG12[1], fb_comment="Switch to a fragrance-free hair routine in five steps: {link}"),

 dict(id="AG05", audio="1326560949104401", pillar="over-40", kicker="Hair care over 40", field="butter", page="/blogs/journal/make-hair-look-thicker",
      scenes=[
        dict(t="hook", lines=["5 hair habits", "to retire", "after&nbsp;40."], sub="Four from dermatologists, plus one photo&nbsp;habit."),
        dict(t="swaps", title="Retire this. Try&nbsp;this.", rows=[
            ("Shampoo on the lengths", "Scalp only"), ("Long-hold products", "Styles that don&#39;t need them"),
            ("Touch-ups close together", "More time between them")], source=AAD),
        dict(t="swaps", title="Two&nbsp;more.", rows=[
            ("Color and a perm on one day", "One service at a time"), ("Judging by the mirror", "A part photo every 6 weeks")]),
        dict(t="checks", title="See a dermatologist&nbsp;if", items=[
            "Your part is getting&nbsp;wider.", "Your ponytail feels&nbsp;thinner."]),
        dict(t="cta", line="Send it to a friend who&#39;ll try it with&nbsp;you.")],
      hashtags=["haircareover40", "finehair", "thinninghair", "healthyhair", "hairtips"],
      ig=_AG05[0], fb=_AG05[1], fb_comment="How to make thin hair look thicker: products, cut and color: {link}"),

 dict(id="AG08", audio="587460186676938", pillar="scalp-care", kicker="Wash day", field="espresso", page="/blogs/journal/oily-scalp-dry-hair",
      scenes=[
        dict(t="hook", lines=["Oily roots.", "Dry ends.", "<mark>Both</mark>?"], sub="Wash for your scalp. Condition for your&nbsp;ends."),
        dict(t="list", title="Three wash&#8209;day&nbsp;rules", items=[
            "Wash as often as your scalp&nbsp;needs.", "Shampoo on the scalp&nbsp;only.",
            "Conditioner on the ends&nbsp;only."], source="Cleveland Clinic and the American Academy of Dermatology"),
        dict(t="list", title="Dry shampoo?", items=[
            "It doesn&#39;t clean. Wash after 1 or 2&nbsp;uses.", "Itching or burning?&nbsp;Stop."], source=AAD),
        dict(t="cta", title="Save this for wash&nbsp;day.")],
      hashtags=["oilyscalp", "washday", "haircaretips", "dryshampoo", "scalpcare"],
      ig=_AG08[0], fb=_AG08[1], fb_comment="Oily scalp but dry hair? A simple routine: {link}"),
]
