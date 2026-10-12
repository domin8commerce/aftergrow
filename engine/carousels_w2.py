"""Carousels AG09 to AG12: made on the Oct 12, 2026 Monday run.
Facts only from the RUNBOOK fact sheet and the Journal page map. "Hair loss" never appears on a slide."""

SAVE = dict(t="cta")


def both(answer, ig_end, fb_end):
    return answer + "\n\n" + ig_end, answer + "\n\n" + fb_end


_AG09 = both(
    "For dry hair, MedlinePlus suggests washing about once or twice a week.\n\n"
    "Use conditioner after every wash. Air dry when you can, and wrap your hair in a towel instead of rubbing it. If you use hot "
    "tools, use the lowest heat setting. And rinse your hair right after swimming.\n\n"
    "If gentle care doesn't help, see a health care provider.",
    "Save this for wash day, and send it to someone with dry hair.",
    "The full guide to dry hair is in the first comment.")

_AG10 = both(
    "Some shedding is normal: 50 to 100 hairs a day, according to the American Academy of Dermatology. Shed hairs fall out at the "
    "end of their resting phase, and excessive shedding often stops on its own as the body readjusts.\n\n"
    "Shedding and hair loss aren't the same thing. A dermatologist can tell which you have, and some "
    "people have both. For 1 in 3 people diagnosed with telogen effluvium, no cause is found, says the British Association of "
    "Dermatologists.\n\n"
    "If shedding is still heavy after six months, see a dermatologist.",
    "Save this, and send it to someone who's worried about her brush.",
    "How to tell shedding from something more is in the first comment.")

_AG11 = both(
    "Taking biotin? Tell your doctor before your next blood test. The FDA says biotin can cause falsely high or falsely low "
    "blood test results.\n\n"
    "Biotin is vitamin B7, so check the label of anything you take for either name. The FDA doesn't approve supplements before "
    "they're sold, and it says not to take supplements in place of prescription medicines.",
    "Save this, and send it to a friend who takes hair vitamins.",
    "What to ask before you take a hair supplement is in the first comment.")

_AG12 = both(
    "Fragrance-free doesn't mean irritation-free. A fragrance-free product can still irritate or contain an allergen.\n\n"
    "To switch, read the ingredient list, not the front label. Look for Fragrance, Parfum or Perfume. Products labeled unscented "
    "may still contain fragrance. Change one product at a time, and stop any product that gives you a rash, "
    "redness or a burn.",
    "Save this for your next shampoo run.",
    "Five steps to a fragrance-free hair routine are in the first comment.")

CAROUSELS = [
 dict(id="AG09", pillar="habits", kicker="Dry hair season", field="butter", page="/blogs/journal/why-is-my-hair-so-dry",
      slides=[
        dict(t="cover", title="Why is my<br>hair so dry?", size=140,
             sub="Four small changes that help dry&nbsp;hair."),
        dict(t="statement", num="1", title="Wash once or twice a&nbsp;week.",
             body="That&#39;s what MedlinePlus suggests for dry&nbsp;hair."),
        dict(t="statement", num="2", title="Condition after every&nbsp;wash.",
             body="Every time you shampoo, follow with conditioner."),
        dict(t="statement", num="3", title="Air dry when you&nbsp;can.",
             body="Wrap your hair in a towel instead of rubbing it. Using hot tools? Pick the lowest heat&nbsp;setting."),
        dict(t="statement", num="4", title="Rinse right after&nbsp;swimming.",
             body="As soon as you get out of the&nbsp;water."),
        dict(t="sources", items=[("MedlinePlus", "U.S. National Library of Medicine"),
                                 ("American Academy of Dermatology", "10 hair care habits that can damage your hair"),
                                 ("Aftergrow Journal", "Our guide to dry hair")],
             note="Education, not medical advice. If gentle care doesn&#39;t help, see a health care&nbsp;provider."),
        SAVE],
      hashtags=["dryhair", "dryhairtips", "haircaretips", "washday", "winterhaircare"],
      ig=_AG09[0], fb=_AG09[1],
      fb_comment="Why is my hair so dry? Causes and four changes that help: {link}"),

 dict(id="AG10", pillar="shedding", kicker="Shedding, or more?", field="espresso", page="/blogs/journal/hair-shedding-vs-hair-loss",
      slides=[
        dict(t="cover", title="Shedding,<br>or something<br>more?", size=132,
             sub="What&#39;s normal, and who can tell the&nbsp;difference."),
        dict(t="statement", label="Shedding", title="Hairs fall out at the end of their resting&nbsp;phase.",
             body="Shedding 50 to 100 a day is normal, says the American Academy of Dermatology."),
        dict(t="bignum", label="No cause found", num="1 in 3", caption="people diagnosed with telogen effluvium.",
             lines=["For them, no cause is found, says the British Association of Dermatologists."]),
        dict(t="statement", title="A dermatologist can tell which you&nbsp;have.",
             body="And some people have&nbsp;both."),
        dict(t="checklist", title="See a dermatologist if", items=[
            "Shedding is still heavy after six&nbsp;months.",
            "You can&#39;t tell if it&#39;s shedding or something&nbsp;more."]),
        dict(t="sources", items=[("American Academy of Dermatology", "Public guide to hair shedding"),
                                 ("British Association of Dermatologists", "Patient information on telogen effluvium"),
                                 ("Aftergrow Journal", "Our guide to shedding")],
             note="Education, not medical advice. If shedding is still heavy after six months, see a&nbsp;dermatologist."),
        SAVE],
      hashtags=["hairshedding", "telogeneffluvium", "thinninghair", "hairhealth", "hairfacts"],
      ig=_AG10[0], fb=_AG10[1],
      fb_comment="Hair shedding or something more? How to tell: {link}"),

 dict(id="AG11", pillar="supplements", kicker="Hair vitamins", field="butter", page="/blogs/journal/scalp-serum-or-hair-supplement",
      slides=[
        dict(t="cover", title="Taking<br>biotin?", size=170,
             sub="Tell your doctor before your next blood&nbsp;test."),
        dict(t="statement", title="Biotin can skew blood test&nbsp;results.",
             body="It can cause falsely high or falsely low results, says the&nbsp;FDA."),
        dict(t="statement", title="Check the label for biotin, or vitamin&nbsp;B7.",
             body="They&#39;re the same thing. Look for both&nbsp;names."),
        dict(t="statement", title="The FDA doesn&#39;t approve supplements before they&#39;re&nbsp;sold.",
             body="So read the label, and know what you&#39;re&nbsp;taking."),
        dict(t="checklist", title="Ask your doctor first", items=[
            "Tell them you take biotin before any blood&nbsp;test.",
            "Never swap a prescription medicine for a&nbsp;supplement.",
            "Bring the label so they can see what&#39;s in&nbsp;it."]),
        dict(t="sources", items=[("U.S. Food and Drug Administration", "Safety information on biotin and lab tests"),
                                 ("U.S. Food and Drug Administration", "Consumer information on supplements"),
                                 ("Aftergrow Journal", "Questions to ask before a hair supplement")],
             note="Education, not medical advice. Ask your doctor before you start or stop any&nbsp;supplement."),
        SAVE],
      hashtags=["biotin", "hairvitamins", "hairsupplements", "healthyhair", "haircaretips"],
      ig=_AG11[0], fb=_AG11[1],
      fb_comment="Questions to ask before you take a hair supplement: {link}"),

 dict(id="AG12", pillar="ingredients", kicker="Fragrance-free, honestly", field="espresso", page="/blogs/journal/fragrance-free-hair-routine",
      slides=[
        dict(t="cover", title="Fragrance-free<br>isn&#39;t irritation&#8209;free.", size=104,
             sub="How to switch, and what to watch&nbsp;for."),
        dict(t="statement", label="Read the list", title="Look for Fragrance, Parfum or&nbsp;Perfume.",
             body="Read the ingredient list, not the front of the&nbsp;bottle."),
        dict(t="statement", label="Unscented", title="Unscented may still contain&nbsp;fragrance.",
             body="It doesn&#39;t always mean fragrance&#8209;free."),
        dict(t="statement", label="Fragrance-free", title="It can still irritate, or contain an&nbsp;allergen.",
             body="Front-label words aren&#39;t a safety&nbsp;standard."),
        dict(t="checklist", title="Switching? Go slowly.", items=[
            "Change one product at a&nbsp;time.",
            "Read the full ingredient&nbsp;list.",
            "Stop if you get a rash, redness or a&nbsp;burn."]),
        dict(t="sources", items=[("U.S. FDA", "Consumer guidance on cosmetics and allergens"),
                                 ("Aftergrow Journal", "Our guide to a fragrance-free routine")],
             note="Education, not medical advice."),
        SAVE],
      hashtags=["fragrancefree", "fragrancefreehaircare", "sensitivescalp", "cleanbeauty", "scalpcare"],
      ig=_AG12[0], fb=_AG12[1],
      fb_comment="Switch to a fragrance-free hair routine in five steps: {link}"),
]
