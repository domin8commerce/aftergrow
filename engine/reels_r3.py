"""Reels R3: seven Reels for Nov 2 to 8, 2026, one a day.

Written on the Nov 2 run. From Oct 20 to Oct 31 Metricool refused to publish (account limit), so only AG14, AG21
and AG22 have numbers since the last run: about 110 reached each, a 3-second view rate of 15 to 18% and 2.4 to 2.6 s
average watch. Both measured Reels opened on a question, so this week leans on statement hooks ("stop doing this",
"that's a myth", a plain claim) to test whether they hold people past three seconds.
Seasonal first: dry and itchy scalp. One new page (natural-scalp-serum). A scalp-scrub Reel was cut: the types-of-scalp-treatments URL carries a banned word.
Facts come only from the RUNBOOK fact sheet and the Journal page map. "Hair loss" never appears on screen.
Scene types: hook, say, big, checks, list, steps, vs, swaps, cta (see engine/reel2.py).
"""
from reels_r1 import caps, AAD

CC = "Cleveland Clinic"

_AG23 = caps(
    "Itchy scalp? Don't scratch it hard.\n\n"
    "Scratching hard, or using force to remove scale, can loosen hair, says the American Academy of Dermatology.\n\n"
    "What the AAD advises instead: keep your nails short and filed smooth, remove scale gently, don't pick, and let your "
    "hair air dry, because blow drying can dry the scalp more.",
    "Save this for winter, and send it to a friend with an itchy scalp.",
    "Dry, itchy scalp and hair loss: what dermatologists say is in the first comment.")

_AG27 = caps(
    "Hair dye can make thin hair look fuller.\n\n"
    "Cleveland Clinic says dye can add volume to each strand, so hair seems fuller.\n\n"
    "If your hair is thinning, the American Academy of Dermatology suggests skipping at-home color and going to a salon "
    "that specializes in it. Book one service at a time, and stretch the time between touch-ups.",
    "Save this before your next appointment, and send it to a friend who's due for color.",
    "How to make thin hair look thicker, with products, cut and color, is in the first comment.")

_AG25 = caps(
    "Dry shampoo doesn't clean your hair.\n\n"
    "That's from the American Academy of Dermatology: dry shampoo doesn't clean hair, so wash after one or two uses.\n\n"
    "Too much leaves hair dry, stiff and gritty. And if you get itching or burning, stop using it.",
    "Save this, and send it to a friend who lives on dry shampoo.",
    "Oily roots, dry ends and dry shampoo: a simple routine is in the first comment.")

_AG24 = caps(
    "Dry scalp and more hair in the drain? Here's what dermatologists say.\n\n"
    "Neither the American Academy of Dermatology nor Cleveland Clinic says dryness on its own causes hair loss. Both "
    "describe itching and flakes. But some conditions that look like a dry scalp at first, such as scalp psoriasis or a "
    "fungal scalp infection, can come with hair loss.\n\n"
    "See a dermatologist if an itchy scalp isn't improving, comes with hair loss, a rash or pain, or if over-the-counter "
    "products don't help.",
    "Save this, and send it to someone with a dry, itchy scalp.",
    "Can a dry scalp cause hair loss? What dermatologists say is in the first comment.")

_AG26 = caps(
    "\"Natural\" on a hair label has no rule behind it.\n\n"
    "\"Organic\" does: USDA Organic means at least 95% organically produced ingredients, not counting water and salt. "
    "\"Made with organic ingredients\" means at least 70%.\n\n"
    "And the FDA says an ingredient's source doesn't decide its safety.",
    "Save this for your next shopping trip, and send it to a friend who buys clean beauty.",
    "\"Natural\" vs \"organic\" on a hair label, explained, is in the first comment.")

_AG29 = caps(
    "Hair in your brush? Check the end of the hair.\n\n"
    "A shed hair is usually full length, with a small white bulb at the root. A broken hair has no bulb and is usually "
    "shorter.\n\n"
    "Shedding 50 to 100 hairs a day is normal, says the American Academy of Dermatology. Damaged hair is fragile, so it "
    "tends to break.",
    "Save this, and send it to someone who's worried about her brush.",
    "Breakage or shedding? How to tell is in the first comment.")

_AG28 = caps(
    "Thin hair? Ask your stylist about a shorter cut or layers.\n\n"
    "Cleveland Clinic says a shorter cut, layers or new styling techniques may help hide hair loss. Ask for a style that "
    "doesn't pull and doesn't need long-hold products, as the American Academy of Dermatology advises.\n\n"
    "If your part is getting wider, see a board-certified dermatologist. A new part or hairstyle rarely reaches the cause.",
    "Save this before your next haircut, and send it to a friend who's booking one.",
    "How to make thin hair look thicker, with products, cut and color, is in the first comment.")

REELS = [
 dict(id="AG23", audio="2477944699150252", pillar="scalp-care", kicker="Itchy scalp", field="butter", page="/blogs/journal/can-dry-scalp-cause-hair-loss",
      scenes=[
        dict(t="hook", lines=["Itchy scalp?", "Don&#39;t scratch", "<mark>hard</mark>."], sub="Here&#39;s what dermatologists say&nbsp;instead."),
        dict(t="say", title="Scratching hard can <mark>loosen</mark>&nbsp;hair.",
             body="So can using force to remove&nbsp;scale.", source=AAD),
        dict(t="checks", title="Try this&nbsp;instead", items=[
            "Keep nails short and filed&nbsp;smooth.", "Remove scale&nbsp;gently.", "Don&#39;t&nbsp;pick."], source=AAD),
        dict(t="say", title="Let your hair <mark>air dry</mark>.",
             body="Blow drying can dry the scalp even&nbsp;more.", source=AAD),
        dict(t="cta", title="Save this for&nbsp;winter.", line="Send it to a friend with an itchy&nbsp;scalp.")],
      hashtags=["itchyscalp", "dryscalp", "scalpcare", "winterhaircare", "scalphealth"],
      ig=_AG23[0], fb=_AG23[1], fb_comment="Dry, itchy scalp and hair loss: what dermatologists say: {link}"),

 dict(id="AG27", audio="761736589642441", pillar="over-40", kicker="Color and thin hair", field="espresso", page="/blogs/journal/make-hair-look-thicker",
      scenes=[
        dict(t="hook", lines=["Hair dye can", "make thin hair", "look <mark>fuller</mark>."], sub="Here&#39;s&nbsp;why."),
        dict(t="say", title="Dye can add <mark>volume</mark> to each&nbsp;strand.", body="So hair seems&nbsp;fuller.", source=CC),
        dict(t="checks", title="If your hair is&nbsp;thinning", items=[
            "Skip at-home&nbsp;color.", "Go to a salon that specializes in&nbsp;it.", "Book one service at a&nbsp;time."], source=AAD),
        dict(t="say", title="Stretch the time between&nbsp;touch&#8209;ups.", source=AAD),
        dict(t="cta", line="Send it to a friend who&#39;s due for&nbsp;color.")],
      hashtags=["thinhair", "haircolor", "finehair", "haircareover40", "thinhairtips"],
      ig=_AG27[0], fb=_AG27[1], fb_comment="How to make thin hair look thicker: products, cut and color: {link}"),

 dict(id="AG25", audio="1549201939908190", pillar="scalp-care", kicker="Dry shampoo", field="butter", page="/blogs/journal/oily-scalp-dry-hair",
      scenes=[
        dict(t="hook", lines=["Dry shampoo", "doesn&#39;t <mark>clean</mark>", "your hair."], sub="Three dermatologist rules for using&nbsp;it."),
        dict(t="say", num="1", title="Wash after one or two&nbsp;<mark>uses</mark>.", source=AAD),
        dict(t="say", num="2", title="Too much leaves hair dry, stiff and&nbsp;gritty."),
        dict(t="say", num="3", title="Itching or&nbsp;burning?", body="Stop using&nbsp;it."),
        dict(t="cta", line="Send it to a friend who lives on dry&nbsp;shampoo.")],
      hashtags=["dryshampoo", "washday", "oilyscalp", "scalpcare", "haircaretips"],
      ig=_AG25[0], fb=_AG25[1], fb_comment="Oily scalp but dry hair? A simple routine, with dry shampoo rules: {link}"),

 dict(id="AG24", audio="2271125906413476", pillar="scalp-care", kicker="Dry scalp season", field="espresso", page="/blogs/journal/can-dry-scalp-cause-hair-loss",
      scenes=[
        dict(t="hook", lines=["Dry scalp", "and more hair", "in the <mark>drain</mark>?"], sub="What dermatologists&nbsp;say."),
        dict(t="say", title="A dry scalp means itching and&nbsp;<mark>flakes</mark>.",
             body="Neither source says dryness alone causes&nbsp;shedding.", source="American Academy of Dermatology and Cleveland Clinic"),
        dict(t="say", label="But", title="Some conditions that look like a dry scalp at first can come with&nbsp;shedding.",
             body="Scalp psoriasis. A fungal scalp&nbsp;infection."),
        dict(t="checks", title="See a dermatologist&nbsp;if", items=[
            "Your itchy scalp isn&#39;t&nbsp;improving.", "It comes with a rash or&nbsp;pain.", "Over-the-counter products don&#39;t&nbsp;help."], source=AAD),
        dict(t="cta", line="Send it to someone with a dry, itchy&nbsp;scalp.")],
      hashtags=["dryscalp", "itchyscalp", "scalpcare", "hairshedding", "winterhaircare"],
      ig=_AG24[0], fb=_AG24[1], fb_comment="Can a dry scalp cause hair loss? What dermatologists say: {link}"),

 dict(id="AG26", audio="1033455569449469", pillar="ingredients", kicker="Label words", field="butter", page="/blogs/journal/natural-scalp-serum",
      scenes=[
        dict(t="hook", lines=["&ldquo;Natural&rdquo;", "on the label?", "No <mark>rule</mark>."], sub="Here&#39;s what the words&nbsp;mean."),
        dict(t="big", label="USDA Organic", num="95%", caption="organic ingredients at least,<br>not counting water and&nbsp;salt.", capsize=66),
        dict(t="say", title="&ldquo;Made with organic ingredients&rdquo;: at least&nbsp;<mark>70%</mark>."),
        dict(t="say", title="An ingredient&#39;s source doesn&#39;t decide its&nbsp;safety.", source="U.S. FDA"),
        dict(t="cta", title="Save this for your next shopping&nbsp;trip.", line="Send it to a friend who buys clean&nbsp;beauty.")],
      hashtags=["naturalhaircare", "organichaircare", "cleanbeauty", "readthelabel", "haircare"],
      ig=_AG26[0], fb=_AG26[1], fb_comment="\"Natural\" vs \"organic\" on a hair label: what the words mean: {link}"),

 dict(id="AG29", audio="1386811643506297", pillar="shedding", kicker="Breakage check", field="espresso", page="/blogs/journal/breakage-or-shedding",
      scenes=[
        dict(t="hook", lines=["Hair in", "your brush?", "Check the <mark>end</mark>."], sub="One detail gives you a&nbsp;clue."),
        dict(t="vs", title="Look at the&nbsp;end", left=("Shed hair", "Usually full length, white&nbsp;bulb"),
             right=("Broken hair", "No bulb, usually&nbsp;shorter")),
        dict(t="big", label="Normal shedding", num="50 to 100", caption="hairs a&nbsp;day.", capsize=76, source=AAD),
        dict(t="say", title="Damaged hair is fragile, so it tends to&nbsp;<mark>break</mark>.", source=AAD),
        dict(t="cta", line="Send it to someone who&#39;s worried about her&nbsp;brush.")],
      hashtags=["hairshedding", "hairbreakage", "thinninghair", "haircaretips", "hairfacts"],
      ig=_AG29[0], fb=_AG29[1], fb_comment="Breakage or shedding? How to tell from the hairs you find: {link}"),

 dict(id="AG28", audio="587460186676938", pillar="over-40", kicker="Haircuts for thin hair", field="butter", page="/blogs/journal/make-hair-look-thicker",
      scenes=[
        dict(t="hook", lines=["Thin hair?", "Ask about a", "<mark>shorter</mark> cut."], sub="Or layers. Here&#39;s&nbsp;why."),
        dict(t="say", title="A shorter cut or layers may help thinning hair look&nbsp;<mark>fuller</mark>.",
             body="Or new styling&nbsp;techniques.", source=CC),
        dict(t="checks", title="Ask your stylist&nbsp;for", items=[
            "A style that doesn&#39;t&nbsp;pull.", "One that skips long-hold&nbsp;products."], source=AAD),
        dict(t="say", label="Part getting wider?", title="See a board-certified&nbsp;dermatologist.",
             body="A new hairstyle rarely reaches the&nbsp;cause.", source=AAD),
        dict(t="cta", title="Save this before your next&nbsp;haircut.", line="Send it to a friend who&#39;s booking&nbsp;one.")],
      hashtags=["thinhair", "haircutsforthinhair", "finehair", "thinhairtips", "haircareover40"],
      ig=_AG28[0], fb=_AG28[1], fb_comment="How to make thin hair look thicker: products, cut and color: {link}"),
]
