"""Reels R2: seven Reels for Oct 26 to Nov 1, 2026, one a day.

Written on the Oct 19 run. Every v2 Reel so far reached under 300 people, so the format stays; this week also varies
the hook type (a question, a "that's a myth" line, a number) to learn which opening holds people past three seconds.
Facts come only from the RUNBOOK fact sheet and the Journal page map. "Hair loss" never appears on screen.
Scene types: hook, say, big, checks, list, steps, vs, swaps, cta (see engine/reel2.py).
"""
from reels_r1 import caps, AAD

_AG16 = caps(
    "Ponytail pulled tight every day? Dermatologists list it as a habit that can damage hair.\n\n"
    "That's pulling hair back tightly, in a ponytail, bun or cornrows, says the American Academy of Dermatology. "
    "Damaged hair is fragile, so it tends to break.\n\n"
    "Instead, wear your hair loosely pulled back, and use covered rubber bands made for styling hair.",
    "Save this, and send it to a friend who lives in a ponytail.",
    "How to tell breakage from shedding is in the first comment.")

_AG18 = caps(
    "Essential oil on your scalp? Three things to know first.\n\n"
    "Essential oils evaporate easily, says DermNet, and some can cause an allergic skin reaction. Don't put a neat, "
    "meaning undiluted, essential oil on your skin.\n\n"
    "And if a product changes color or smell, throw it out.",
    "Save this before you try one, and send it to a friend who loves oils.",
    "Serum or oil, and what to compare on the label, is in the first comment.")

_AG19 = caps(
    "Scalp serum: wet hair or dry? Start with the label.\n\n"
    "Follow your serum's directions. For Aftergrow, that's a few drops on a clean, dry scalp. Make a part where you can see "
    "the skin, put the drops there, and massage for 1 to 2 minutes. No rinsing.\n\n"
    "New serum? Patch test first: a few drops behind the ear, then wait 24 hours.",
    "Save this for tonight, and send it to a friend who just bought a serum.",
    "How to use a scalp serum, step by step, is in the first comment.")

_AG17 = caps(
    "100 brush strokes a day? That's a myth, says the American Academy of Dermatology.\n\n"
    "Hair never needs 100 strokes. Brush and comb only to style it, and use a wide-tooth comb, gently.\n\n"
    "Straight hair? Let it dry a bit before you comb it. Textured hair or tight curls? Comb while it's damp, with a "
    "wide-tooth comb.",
    "Save this, and send it to someone who still counts strokes.",
    "Breakage or shedding, and the habits that cause breakage, are in the first comment.")

_AG20 = caps(
    "Fine hair? Where your conditioner goes matters.\n\n"
    "For fine or straight hair, put conditioner on the ends. For dry or curly hair, use it through the whole length.\n\n"
    "Stretch the time between color touch-ups. Hair fibers, colored sprays and wigs are cosmetic camouflage. If your part is getting wider or your ponytail feels thinner, see a "
    "dermatologist.",
    "Save this for wash day, and send it to a friend with fine hair.",
    "How to make thin hair look thicker, with products, cut and color, is in the first comment.")

_AG21 = caps(
    "Is an ingredient list in order? Mostly. Here's the catch.\n\n"
    "Ingredients run from most to least. But ingredients at 1% or less can be listed in any order.\n\n"
    "Look for \"Fragrance\" or \"Parfum\": that means added fragrance. And \"unscented\" products may still contain "
    "fragrance, says the FDA.",
    "Save this for your next shopping trip, and send it to a friend who reads every label.",
    "How to read a scalp serum label is in the first comment.")

_AG22 = caps(
    "Hair serum or scalp serum? The difference is where it goes.\n\n"
    "A hair serum is for the lengths and ends. A scalp serum is for the skin of your scalp. For Aftergrow, that's a few "
    "drops on a clean, dry scalp, massaged in for 1 to 2 minutes, with no rinsing.\n\n"
    "Using both? Scalp serum first, then the hair serum on the lengths.",
    "Save this, and send it to a friend with a crowded shelf.",
    "Hair serum or scalp serum, explained, is in the first comment.")

REELS = [
 dict(id="AG16", audio="2271125906413476", pillar="habits", kicker="Breakage check", field="espresso", page="/blogs/journal/breakage-or-shedding",
      scenes=[
        dict(t="hook", lines=["Ponytail", "pulled <mark>tight</mark>", "every day?"], sub="It&#39;s on the dermatologists&#39;&nbsp;list."),
        dict(t="say", title="Pulling hair back tightly can <mark>damage</mark>&nbsp;hair.",
             body="A ponytail, a bun or&nbsp;cornrows.", source=AAD),
        dict(t="say", title="Damaged hair is fragile, so it tends to&nbsp;break.", source=AAD),
        dict(t="checks", title="Try this&nbsp;instead", items=[
            "Wear hair loosely pulled&nbsp;back.", "Use covered bands made for&nbsp;hair."], source=AAD),
        dict(t="cta", line="Send it to a friend who lives in a&nbsp;ponytail.")],
      hashtags=["hairbreakage", "ponytail", "healthyhair", "haircaretips", "hairhabits"],
      ig=_AG16[0], fb=_AG16[1], fb_comment="Breakage or shedding? How to tell, and the habits that cause breakage: {link}"),

 dict(id="AG18", audio="1549201939908190", pillar="ingredients", kicker="Oils, carefully", field="butter", page="/blogs/journal/scalp-serum-or-scalp-oil",
      scenes=[
        dict(t="hook", lines=["Essential oil", "on your", "<mark>scalp</mark>?"], sub="Three things to know&nbsp;first."),
        dict(t="say", num="1", title="Essential oils <mark>evaporate</mark>&nbsp;easily.", source="DermNet"),
        dict(t="say", num="2", title="Some can cause an allergic skin&nbsp;reaction.",
             body="Don&#39;t put neat, undiluted oils on&nbsp;skin."),
        dict(t="say", num="3", title="Changed color or&nbsp;smell?", body="Throw it&nbsp;out."),
        dict(t="cta", title="Save this before you try&nbsp;one.", line="Send it to a friend who loves&nbsp;oils.")],
      hashtags=["essentialoils", "scalpcare", "scalpoil", "hairoil", "haircaretips"],
      ig=_AG18[0], fb=_AG18[1], fb_comment="Scalp serum or scalp oil? What to compare on the label: {link}"),

 dict(id="AG19", audio="1386811643506297", pillar="routine", kicker="Scalp serum, how to", field="espresso", page="/blogs/journal/how-to-use-a-scalp-serum",
      scenes=[
        dict(t="hook", lines=["Scalp serum:", "wet hair", "or <mark>dry</mark>?"], sub="Start with the&nbsp;label."),
        dict(t="say", title="Follow your serum&#39;s&nbsp;<mark>directions</mark>.",
             body="For Aftergrow: a few drops on a clean, dry&nbsp;scalp."),
        dict(t="steps", title="The&nbsp;routine", steps=[
            ("First", "Part it so you see&nbsp;skin."), ("Then", "A few drops&nbsp;there."),
            ("Last", "Massage 1 to 2&nbsp;minutes.")]),
        dict(t="checks", title="New serum?", items=[
            "A few drops behind the&nbsp;ear.", "Wait 24&nbsp;hours."]),
        dict(t="cta", title="Save this for&nbsp;tonight.", line="Send it to a friend who just bought a&nbsp;serum.")],
      hashtags=["scalpserum", "scalpcare", "scalpcareroutine", "haircareroutine", "patchtest"],
      ig=_AG19[0], fb=_AG19[1], fb_comment="How to use a scalp serum, step by step: {link}"),

 dict(id="AG17", audio="1033455569449469", pillar="habits", kicker="Brushing myths", field="butter", page="/blogs/journal/breakage-or-shedding",
      scenes=[
        dict(t="hook", lines=["100 strokes", "a day?", "That&#39;s a <mark>myth</mark>."], sub="Here&#39;s what dermatologists say&nbsp;instead."),
        dict(t="say", title="Hair never needs 100 brush&nbsp;strokes.", body="Brush and comb only to style&nbsp;it.", source=AAD),
        dict(t="say", title="Use a <mark>wide-tooth</mark> comb,&nbsp;gently.", source=AAD),
        dict(t="vs", title="Combing after a&nbsp;wash", left=("Straight hair", "Let it dry a&nbsp;bit first"),
             right=("Textured or tight curls", "Comb while&nbsp;damp"), source=AAD),
        dict(t="cta", line="Send it to someone who still counts&nbsp;strokes.")],
      hashtags=["hairbrushing", "hairmyths", "hairbreakage", "healthyhair", "haircaretips"],
      ig=_AG17[0], fb=_AG17[1], fb_comment="Breakage or shedding? How to tell, and the habits that cause breakage: {link}"),

 dict(id="AG20", audio="592271352837708", pillar="over-40", kicker="Fine hair", field="espresso", page="/blogs/journal/make-hair-look-thicker",
      scenes=[
        dict(t="hook", lines=["Fine hair?", "Where the", "<mark>conditioner</mark>", "goes matters."], sub="One rule for fine hair, one for&nbsp;curly."),
        dict(t="vs", title="Conditioner goes&nbsp;on", left=("Fine or straight", "The&nbsp;ends"),
             right=("Dry or curly", "The whole&nbsp;length")),
        dict(t="say", title="Stretch the time between color&nbsp;touch&#8209;ups."),
        dict(t="say", label="Cosmetic camouflage", title="Hair fibers, colored sprays and&nbsp;wigs."),
        dict(t="checks", title="See a dermatologist&nbsp;if", items=[
            "Your part is getting&nbsp;wider.", "Your ponytail feels&nbsp;thinner."]),
        dict(t="cta", title="Save this for wash&nbsp;day.", line="Send it to a friend with fine&nbsp;hair.")],
      hashtags=["finehair", "finehairtips", "thinhair", "conditioner", "haircareover40"],
      ig=_AG20[0], fb=_AG20[1], fb_comment="How to make thin hair look thicker: products, cut and color: {link}"),

 dict(id="AG21", audio="1579921342191993", pillar="ingredients", kicker="Label check", field="butter", page="/blogs/journal/how-to-read-a-scalp-serum-label",
      scenes=[
        dict(t="hook", lines=["Ingredient list", "in <mark>order</mark>?"], sub="Mostly. Here&#39;s the&nbsp;catch."),
        dict(t="say", title="Ingredients run from most to&nbsp;least."),
        dict(t="big", label="The catch", num="1%", caption="or less can be listed<br>in any&nbsp;order.", capsize=76),
        dict(t="say", title="&ldquo;Fragrance&rdquo; or &ldquo;Parfum&rdquo; means added&nbsp;fragrance."),
        dict(t="say", title="&ldquo;Unscented&rdquo; may still contain&nbsp;<mark>fragrance</mark>.", source="U.S. FDA"),
        dict(t="cta", line="Send it to the friend who reads every&nbsp;label.")],
      hashtags=["ingredientcheck", "readthelabel", "scalpcare", "fragrancefree", "haircare"],
      ig=_AG21[0], fb=_AG21[1], fb_comment="How to read a scalp serum label: {link}"),

 dict(id="AG22", audio="1326560949104401", pillar="routine", kicker="Serum basics", field="espresso", page="/blogs/journal/hair-serum-or-scalp-serum",
      scenes=[
        dict(t="hook", lines=["Hair serum", "or <mark>scalp</mark>", "serum?"], sub="The difference is where it&nbsp;goes."),
        dict(t="vs", title="Where it&nbsp;goes", left=("Hair serum", "Lengths and&nbsp;ends"),
             right=("Scalp serum", "The skin of your&nbsp;scalp")),
        dict(t="say", label="Aftergrow", title="A few drops on a clean, dry&nbsp;<mark>scalp</mark>.",
             body="Massage 1 to 2 minutes. No&nbsp;rinsing."),
        dict(t="steps", title="Using&nbsp;both?", steps=[
            ("First", "Scalp serum on the&nbsp;scalp."), ("Then", "Hair serum on the&nbsp;lengths.")]),
        dict(t="cta", line="Send it to a friend with a crowded&nbsp;shelf.")],
      hashtags=["scalpserum", "hairserum", "scalpcare", "haircareroutine", "haircaretips"],
      ig=_AG22[0], fb=_AG22[1], fb_comment="Hair serum or scalp serum? The difference, explained: {link}"),
]
