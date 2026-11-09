"""Reels R4: six Reels for Nov 9 to 15, 2026 (one slot left empty).

Written on the Nov 9 run. Nov 1 to 8 all published (Metricool's account limit did not recur). Instagram: about 110 to
125 reached per Reel, a 3-second view rate of 12.6 to 29%, 2.0 to 3.1 s average watch. Under 300 reached, so the
numbers are noise; the plan holds. The two best openers (AG27 dye, 29%; AG25 dry shampoo, 22%) were surprising,
sourced statements, so this week leans on those: a number, a "don't", a label word.
Seasonal first: dry scalp and dry hair. New pages: is-my-hair-thinning and simple-hair-care-routine.
A dye-day Reel (FDA: don't scratch or brush your scalp for three days before dyeing) was cut: the
color-treated-hair-care URL carries a banned word.
AG34 (tight ponytails) was written and cut after the fact-check: it repeats AG16, a finished Reel that never
published (Metricool account limit, Oct 26). AG34's slot is left empty.
Facts come only from the RUNBOOK fact sheet and the Journal page map. "Hair loss" never appears on screen.
"""
from reels_r1 import caps, AAD

CC = "Cleveland Clinic"
FDA = "U.S. FDA"

_AG30 = caps(
    "Dry scalp? Keep showers to 5 to 10 minutes.\n\n"
    "That's one of the American Academy of Dermatology's tips for a dry scalp. Another: leave-in conditioner goes on "
    "your hair only.\n\n"
    "Choose fragrance-free and check the ingredient list, as the FDA suggests. Call a dermatologist for itching that "
    "won't stop, a red rash, or swollen, warm or painful skin.",
    "Save this for winter, and send it to a friend with a dry scalp.",
    "Dry scalp or dandruff, and the habits that help a dry scalp, are in the first comment.")

_AG32 = caps(
    "\"Thickening\" on a hair label? Read it twice.\n\n"
    "Looking fuller and growing hair aren't the same claim. The FDA says a claim to restore hair growth is a drug claim.\n\n"
    "What can make hair look fuller: a shampoo that helps hair hold moisture, says the American Academy of Dermatology, "
    "and one that adds volume without sulfate detergents, says Cleveland Clinic. Pick products made for your hair type, "
    "such as fine hair.",
    "Save this for your next shopping trip, and send it to a friend with fine, thin hair.",
    "How to make thin hair look thicker, with products, cut and color, is in the first comment.")

_AG33 = caps(
    "Thinning? Don't trust your memory.\n\n"
    "Compare with an earlier photo of the same view, and keep the wash timing, product, part and light the same. "
    "Cleveland Clinic lists seeing scalp skin through your hair, a part on top that gets wider and tying up smaller "
    "ponytails among signs in women.\n\n"
    "Other causes can look alike, says the American Academy of Dermatology. A dermatologist can tell you the cause.",
    "Save this for your next photo, and send it to a friend who keeps checking her part.",
    "Is my hair thinning? Four checks are in the first comment.")

_AG31 = caps(
    "Drier hair after menopause? Here's one thing that changes.\n\n"
    "Cleveland Clinic says oil production typically drops with age, especially after menopause. For fine, straight "
    "hair over 50: conditioner on the ends and, per a 2015 hair cosmetics review, a small amount of any leave-on product.\n\n"
    "Use conditioner after every wash, and air dry when you can. If gentle care doesn't help, see a health care provider.",
    "Save this for wash day, and send it to a friend who's noticed the change.",
    "Why is my hair so dry? Common causes, and what to change, are in the first comment.")

_AG35 = caps(
    "Straight hair? Don't comb it wet.\n\n"
    "Wrap or blot your hair instead of rubbing it. Then, the American Academy of Dermatology says, let straight hair "
    "dry partway and comb gently with a wide-tooth comb, starting at the ends.\n\n"
    "Curly hair is different: comb it in the shower, before you rinse out the conditioner.",
    "Save this for wash day, and send it to a friend who combs straight out of the shower.",
    "A simple hair care routine, in order, is in the first comment.")

_AG36 = caps(
    "Fine, thin hair? Wash every 1 to 2 days.\n\n"
    "That's Cleveland Clinic's rough guide. The American "
    "Academy of Dermatology's rule: wash based on how often your hair gets dirty or oily.\n\n"
    "Massage shampoo into your scalp, and use conditioner after every shampoo, on the ends if your hair is fine or "
    "straight. Lots of styling products? Cleveland Clinic suggests a clarifying shampoo once or twice a month.",
    "Save this for wash day, and send it to a friend with fine hair.",
    "A simple hair care routine, in order, is in the first comment.")

REELS = [
 dict(id="AG30", audio="1386811643506297", pillar="scalp-care", kicker="Dry scalp season", field="butter", page="/blogs/journal/scalp-serum-for-dry-scalp",
      scenes=[
        dict(t="hook", lines=["Dry scalp?", "Keep showers", "to <mark>10</mark> minutes."], sub="Three more dry scalp&nbsp;tips."),
        dict(t="big", label="Shower time", num="5 to 10", caption="minutes, for a dry&nbsp;scalp.", capsize=76, source=AAD),
        dict(t="say", title="Leave-in conditioner goes on your <mark>hair</mark> only.", source=AAD),
        dict(t="say", title="Choose <mark>fragrance&#8209;free</mark>.", body="And check the ingredient&nbsp;list.", source=FDA),
        dict(t="checks", title="Call a dermatologist&nbsp;for", items=[
            "Itching that won&#39;t&nbsp;stop.", "A red&nbsp;rash.", "Swollen, warm or painful&nbsp;skin."]),
        dict(t="cta", title="Save this for&nbsp;winter.", line="Send it to a friend with a dry&nbsp;scalp.")],
      hashtags=["dryscalp", "itchyscalp", "winterhaircare", "scalpcare", "dryscalptips"],
      ig=_AG30[0], fb=_AG30[1], fb_comment="Dry scalp or dandruff? The difference, and dry scalp habits: {link}"),

 dict(id="AG32", audio="587460186676938", pillar="over-40", kicker="Label words", field="espresso", page="/blogs/journal/make-hair-look-thicker",
      scenes=[
        dict(t="hook", lines=["&ldquo;Thickening&rdquo;", "on the label?", "Read it <mark>twice</mark>."], sub="Looking fuller and growing hair aren&#39;t the same&nbsp;claim."),
        dict(t="say", title="A claim to restore hair growth is a <mark>drug</mark> claim.", source=FDA),
        dict(t="say", title="Shampoo can make hair <mark>look</mark> fuller.",
             body="One that helps hair hold moisture makes it look fuller and&nbsp;thicker.", source=AAD),
        dict(t="checks", title="Look&nbsp;for", items=[
            "A shampoo that adds&nbsp;volume.", "No sulfate&nbsp;detergents.", "Made for your hair type, like fine&nbsp;hair."],
             source="Cleveland Clinic and American Academy of Dermatology"),
        dict(t="cta", title="Save this for your next shopping&nbsp;trip.", line="Send it to a friend with fine, thin&nbsp;hair.")],
      hashtags=["thinhair", "finehair", "volumizingshampoo", "haircareover40", "readthelabel"],
      ig=_AG32[0], fb=_AG32[1], fb_comment="How to make thin hair look thicker: products, cut and color: {link}"),

 dict(id="AG33", audio="1549201939908190", pillar="thinning", kicker="Is it thinning?", field="butter", page="/blogs/journal/is-my-hair-thinning",
      scenes=[
        dict(t="hook", lines=["Thinning?", "Don&#39;t trust", "your <mark>memory</mark>."], sub="Compare photos instead. Here&#39;s&nbsp;how."),
        dict(t="say", title="Compare with an earlier photo of the <mark>same</mark> view.", body="Not with what you&nbsp;remember."),
        dict(t="checks", title="Keep these the&nbsp;same", items=["Wash&nbsp;timing.", "Product.", "Part.", "Light."]),
        dict(t="checks", title="Signs to&nbsp;notice", items=[
            "Scalp skin showing through your&nbsp;hair.", "A part on top that gets&nbsp;wider.", "Smaller ponytails when you tie it&nbsp;up."],
             source=CC),
        dict(t="say", title="Other causes can look&nbsp;<mark>alike</mark>.", source=AAD),
        dict(t="say", title="A dermatologist can tell you the&nbsp;cause."),
        dict(t="cta", title="Save this for your next&nbsp;photo.", line="Send it to a friend who keeps checking her&nbsp;part.")],
      hashtags=["thinninghair", "hairthinning", "thinhair", "hairpart", "haircareover40"],
      ig=_AG33[0], fb=_AG33[1], fb_comment="Is my hair thinning? Four checks: {link}"),

 dict(id="AG31", audio="2477944699150252", pillar="over-40", kicker="Dry hair over 50", field="espresso", page="/blogs/journal/why-is-my-hair-so-dry",
      scenes=[
        dict(t="hook", lines=["Drier hair", "after", "<mark>menopause</mark>?"], sub="Here&#39;s one thing that changes, and what to&nbsp;do."),
        dict(t="say", title="Oil production typically <mark>drops</mark> with&nbsp;age.", body="Especially after&nbsp;menopause.", source=CC),
        dict(t="checks", title="Fine, straight hair over&nbsp;50?", items=[
            "Conditioner on the&nbsp;ends.", "A small amount of any leave&#8209;on&nbsp;product."],
             source="Cleveland Clinic and a 2015 hair cosmetics review"),
        dict(t="say", title="Conditioner after <mark>every</mark> wash.", body="And air dry when you&nbsp;can."),
        dict(t="say", label="Still dry?", title="If gentle care doesn&#39;t help, see a health care&nbsp;provider."),
        dict(t="cta", title="Save this for wash&nbsp;day.", line="Send it to a friend who&#39;s noticed the&nbsp;change.")],
      hashtags=["dryhair", "menopausehair", "haircareover50", "finehair", "winterhaircare"],
      ig=_AG31[0], fb=_AG31[1], fb_comment="Why is my hair so dry? Common causes, and four changes that help: {link}"),

 dict(id="AG35", audio="1033455569449469", pillar="routine", kicker="Wash day", field="butter", page="/blogs/journal/simple-hair-care-routine",
      scenes=[
        dict(t="hook", lines=["Straight hair?", "Don&#39;t comb", "it <mark>wet</mark>."], sub="What dermatologists suggest&nbsp;instead."),
        dict(t="say", title="Wrap or <mark>blot</mark>. Don&#39;t&nbsp;rub.", source=AAD),
        dict(t="say", title="Let it dry a <mark>bit</mark> first.", body="Then comb gently with a wide-tooth&nbsp;comb.", source=AAD),
        dict(t="say", title="Start combing at the&nbsp;<mark>ends</mark>.", source=AAD),
        dict(t="say", label="Curly hair?", title="Comb in the shower, before you rinse out the&nbsp;conditioner.", source=AAD),
        dict(t="cta", title="Save this for wash&nbsp;day.", line="Send it to a friend who combs straight out of the&nbsp;shower.")],
      hashtags=["washday", "haircaretips", "straighthair", "hairbreakage", "haircareroutine"],
      ig=_AG35[0], fb=_AG35[1], fb_comment="A simple hair care routine, in order: {link}"),

 dict(id="AG36", audio="761736589642441", pillar="routine", kicker="Fine hair", field="butter", page="/blogs/journal/simple-hair-care-routine",
      scenes=[
        dict(t="hook", lines=["Fine, thin hair?", "Wash every", "<mark>1 to 2</mark> days."], sub="That&#39;s Cleveland Clinic&#39;s rough&nbsp;guide."),
        dict(t="say", label="The rule underneath", title="Wash as often as your hair gets dirty or&nbsp;<mark>oily</mark>.", source=AAD),
        dict(t="checks", title="On wash&nbsp;day", items=[
            "Massage shampoo into your&nbsp;scalp.", "Conditioner after every&nbsp;shampoo.", "On the ends, if hair is fine or&nbsp;straight."],
             source=AAD),
        dict(t="say", label="Lots of styling products?", title="Clarifying shampoo once or twice a&nbsp;<mark>month</mark>.", source=CC),
        dict(t="cta", title="Save this for wash&nbsp;day.", line="Send it to a friend with fine&nbsp;hair.")],
      hashtags=["finehair", "thinhair", "washday", "haircareroutine", "haircaretips"],
      ig=_AG36[0], fb=_AG36[1], fb_comment="A simple hair care routine, in order: {link}"),
]
