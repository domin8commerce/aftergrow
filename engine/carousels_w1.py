"""Carousels AG01 to AG08: the first two weeks on Instagram and Facebook.
Facts only from the RUNBOOK fact sheet and the Journal page map. "Hair loss" never appears on a slide."""

U = "https://getaftergrow.com"
DERM = dict(t="checklist", title="See a dermatologist if",
            items=["The shedding is sudden.", "It comes out in patches.", "It&#39;s still heavy after six&nbsp;months."])
SAVE = dict(t="cta")

CAROUSELS = [
 dict(id="AG01", pillar="shedding", kicker="Hair shedding, explained", field="butter", page="/pages/how-it-works",
      slides=[
        dict(t="cover", title="Why hair sheds<br>months after<br>a big change.",
             sub="It shows up when you think the hard part is over. Here&#39;s the timeline."),
        dict(t="statement", num="1", title="Hair grows for years, then rests for about&nbsp;three&nbsp;months.",
             body="After the rest, it falls out and a new hair starts in the same follicle."),
        dict(t="statement", num="2", title="A big change in the body can send many hairs into rest at&nbsp;once.",
             body="Childbirth, illness, surgery, a high fever or a very stressful time are common triggers."),
        dict(t="timeline", title="The timeline.", steps=[
            dict(when="Month 0", what="The big change."),
            dict(when="Months 2 to 4", what="The shed starts.", more="More hair in the brush and the shower.", on=True),
            dict(when="Months 6 to 9", what="It settles.", more="For most people, on its own.")]),
        DERM,
        dict(t="sources", items=[("American Academy of Dermatology", "Public guide to hair shedding"),
                                 ("getaftergrow.com", "How it works: the month-three shed")]),
        SAVE],
      hashtags=["hairshedding", "telogeneffluvium", "hairhealth", "scalpcare", "hairtips"],
      ig="Hair shedding that starts months after a big change in the body is common, and it has a name: telogen effluvium.\n\n"
         "Every hair grows for years, then rests for about three months before it falls out. A big change, like childbirth, "
         "illness, surgery or a very stressful time, can send many hairs into that resting phase at once. So the shed shows up "
         "two to four months later, often when you think the hard part is over. For most people it settles within six to nine months.\n\n"
         "If it's sudden, patchy or still heavy after six months, see a dermatologist.\n\n"
         "Save this for later, and send it to someone who's going through it.",
      fb="Hair shedding that starts months after a big change in the body is common, and it has a name: telogen effluvium.\n\n"
         "Every hair grows for years, then rests for about three months before it falls out. A big change, like childbirth, "
         "illness, surgery or a very stressful time, can send many hairs into that resting phase at once. So the shed shows up "
         "two to four months later, often when you think the hard part is over. For most people it settles within six to nine months.\n\n"
         "If it's sudden, patchy or still heavy after six months, see a dermatologist.\n\n"
         "The full explanation is in the first comment.",
      fb_comment="How hair shedding works, in plain English: {link}"),

 dict(id="AG02", pillar="habits", kicker="Breakage or shedding?", field="espresso", page="/blogs/journal/breakage-or-shedding",
      slides=[
        dict(t="cover", title="Breakage<br>or shedding?", size=150,
             sub="Look at the end of the hair. One detail tells you which&nbsp;one&nbsp;it&nbsp;is."),
        dict(t="compare", title="What the hair tells you.",
             left=dict(head="Shed hair", items=["Comes out from the root", "Usually full length", "A small white bulb at the end"]),
             right=dict(head="Broken hair", items=["Snapped along the strand", "Usually a shorter piece", "No bulb"])),
        dict(t="bignum", label="What&#39;s normal", num="50&ndash;100", caption="hairs a day.",
             lines=["That&#39;s normal shedding, says the American Academy of Dermatology."]),
        dict(t="swaps", title="Habits that break hair, and the fix.", size=80, rows=[
            ("Rubbing hair dry with a towel", "Wrap it, then let it air dry"),
            ("Brushing straight hair while wet", "Wait until it&#39;s partly dry"),
            ("Hot tools most days", "Once a week or less"),
            ("Tight ponytails and buns", "Looser styles, covered elastics"),
            ("Skipping conditioner", "Condition after every shampoo")]),
        dict(t="statement", title="Brushing 100 strokes a day is a&nbsp;myth.",
             body="Brush only to style, gently, with a wide-tooth comb. That&#39;s the American Academy of Dermatology&#39;s advice."),
        dict(t="sources", items=[("American Academy of Dermatology", "10 hair care habits that can damage your hair"),
                                 ("Aftergrow Journal", "Breakage or shedding? How to tell from the hairs you find")]),
        SAVE],
      hashtags=["hairbreakage", "hairshedding", "healthyhair", "haircaretips", "hairhealth"],
      ig="Breakage or shedding? Check the end of the hair.\n\n"
         "A shed hair comes out from the root, so it's usually full length with a small white bulb at the end. A broken hair has "
         "no bulb. It snapped somewhere along the strand, so it's usually a shorter piece.\n\n"
         "Shedding 50 to 100 hairs a day is normal, according to the American Academy of Dermatology. Everyday habits can break hair, "
         "and habits can change.\n\n"
         "Which one are you finding more of? Tell us below.\n\n"
         "Save this for wash day.",
      fb="Breakage or shedding? Check the end of the hair.\n\n"
         "A shed hair comes out from the root, so it's usually full length with a small white bulb at the end. A broken hair has "
         "no bulb. It snapped somewhere along the strand, so it's usually a shorter piece.\n\n"
         "Shedding 50 to 100 hairs a day is normal, according to the American Academy of Dermatology. Everyday habits can break hair, "
         "and habits can change.\n\n"
         "The full guide, with more habits to change, is in the first comment.",
      fb_comment="Breakage or shedding? How to tell from the hairs you find: {link}"),

 dict(id="AG03", pillar="shedding", kicker="How much is normal?", field="butter", page="/pages/how-it-works",
      slides=[
        dict(t="cover", title="How much hair<br>shedding is<br>normal?", size=128,
             sub="The number dermatologists use, and a better habit than counting."),
        dict(t="bignum", label="A normal day", num="50&ndash;100", caption="hairs a day.",
             lines=["That&#39;s normal shedding, says the American Academy of Dermatology."]),
        dict(t="statement", title="During a shed, it&#39;s more than that, for a few&nbsp;months.",
             body="It often starts two to four months after a big change in the body and settles within six to nine months for most&nbsp;people."),
        dict(t="statement", title="Counting hairs is stressful. Photos are&nbsp;fairer.",
             body="Take one photo of your part every six weeks: same window, same part, same&nbsp;angle."),
        DERM,
        dict(t="sources", items=[("American Academy of Dermatology", "Public guide to hair shedding"),
                                 ("getaftergrow.com", "How it works: the month-three shed")]),
        SAVE],
      hashtags=["hairshedding", "hairhealth", "thinninghair", "scalpcare", "hairtips"],
      ig="How much hair shedding is normal? It's normal to shed 50 to 100 hairs a day, according to the American Academy of Dermatology.\n\n"
         "During a shed it's more than that, for a few months. It often starts two to four months after a big change in the body "
         "and settles within six to nine months for most people.\n\n"
         "Instead of counting hairs, take one photo of your part every six weeks, the same way each time. It's a fairer way to see real change.\n\n"
         "Save this, and send it to a friend who's been counting.",
      fb="How much hair shedding is normal? It's normal to shed 50 to 100 hairs a day, according to the American Academy of Dermatology.\n\n"
         "During a shed it's more than that, for a few months. It often starts two to four months after a big change in the body "
         "and settles within six to nine months for most people.\n\n"
         "Instead of counting hairs, take one photo of your part every six weeks, the same way each time.\n\n"
         "More on why shedding happens is in the first comment.",
      fb_comment="Why shedding happens, and when it settles: {link}"),

 dict(id="AG04", pillar="ingredients", kicker="Rosemary, honestly", field="espresso", page="/blogs/journal/scalp-serum-or-scalp-oil",
      slides=[
        dict(t="cover", title="Rosemary oil,<br>rosemary water,<br>rosemary extract.", size=112,
             sub="Not the same thing. Here&#39;s the difference, and what to check&nbsp;first."),
        dict(t="statement", label="In a finished product", title="Rosemary extract is one ingredient in a set&nbsp;formula.",
             body="It comes with directions and warnings on the label."),
        dict(t="statement", label="From a bottle", title="Rosemary essential oil never goes on skin&nbsp;neat.",
             body="Neat means undiluted. Some essential oils can cause an allergic skin reaction."),
        dict(t="statement", label="Made at home", title="Homemade rosemary water is on&nbsp;you.",
             body="Whoever makes a cosmetic is responsible for its safety, says the FDA. Throw it out if the color or smell&nbsp;changes."),
        dict(t="checklist", title="Before you try&nbsp;one", items=[
            "Patch test a finished product: a few drops behind the ear, then wait 24&nbsp;hours.",
            "Change one product at a&nbsp;time.",
            "Stop if you get a rash, redness or a&nbsp;burn."]),
        dict(t="sources", items=[("Aftergrow Journal", "Scalp serum or scalp oil?"),
                                 ("DermNet", "Allergic contact dermatitis to essential oils"),
                                 ("U.S. FDA", "Using cosmetics safely")],
             note="Education, not medical advice. We make no claims about what rosemary does for hair."),
        SAVE],
      hashtags=["rosemaryforhair", "rosemarywater", "scalpcare", "haircare", "cleanbeauty"],
      ig="Rosemary for hair is everywhere right now. But rosemary oil, rosemary water and rosemary extract are three different things.\n\n"
         "Rosemary extract in a finished product is one ingredient in a set formula, with directions and warnings on the label. "
         "Rosemary essential oil should never go on skin neat, meaning undiluted, and some essential oils can cause an allergic skin reaction. Homemade rosemary "
         "water is on you: whoever makes a cosmetic is responsible for its safety, says the FDA.\n\n"
         "Trying a finished product? Patch test first: a few drops behind the ear, then wait 24 hours.\n\n"
         "Save this before you try the next rosemary trend.",
      fb="Rosemary for hair is everywhere right now. But rosemary oil, rosemary water and rosemary extract are three different things.\n\n"
         "Rosemary extract in a finished product is one ingredient in a set formula, with directions and warnings on the label. "
         "Rosemary essential oil should never go on skin neat, meaning undiluted, and some essential oils can cause an allergic skin reaction. Homemade rosemary "
         "water is on you: whoever makes a cosmetic is responsible for its safety, says the FDA.\n\n"
         "Trying a finished product? Patch test first: a few drops behind the ear, then wait 24 hours.\n\n"
         "The full comparison is in the first comment.",
      fb_comment="Rosemary extract vs. rosemary oil vs. rosemary water, compared: {link}"),

 dict(id="AG05", pillar="over-40", kicker="Hair care over 40", field="butter", page="/blogs/journal/make-hair-look-thicker",
      slides=[
        dict(t="cover", title="5 hair habits<br>to retire<br>after 40.", sub="Small swaps that are gentler on your hair."),
        dict(t="swaps", title="Retire this. Try this.", rows=[
            ("Shampoo on the lengths", "Shampoo on the scalp only"),
            ("Long-hold styling products", "Styles that don&#39;t need them"),
            ("Color touch-ups close together", "More time between them"),
            ("Color and a perm on one day", "One service at a time"),
            ("Judging by the mirror alone", "A part photo every 6 weeks")]),
        dict(t="statement", title="Fine hair? Conditioner goes on the&nbsp;ends.",
             body="Dry or curly hair can take it along the whole length."),
        dict(t="checklist", title="See a dermatologist if", items=[
            "Your part is getting wider.", "Your ponytail feels thinner.", "Shedding lasts more than six&nbsp;months."]),
        dict(t="sources", items=[("American Academy of Dermatology", "10 hair care habits that can damage your hair"),
                                 ("Aftergrow Journal", "How to make thinning hair look thicker")]),
        SAVE],
      hashtags=["haircareover40", "finehair", "thinninghair", "healthyhair", "hairtips"],
      ig="Hair care over 40: five habits to retire, and what to do instead.\n\n"
         "Shampoo your scalp, not the lengths. Pick styles that don't need long-hold products. Stretch the time between color "
         "touch-ups, and book one chemical service at a time. And judge your hair with a part photo every six weeks, not the "
         "bathroom mirror.\n\n"
         "If your part is getting wider or your ponytail feels thinner, see a dermatologist.\n\n"
         "Save this, and send it to a friend who'll try it with you.",
      fb="Hair care over 40: five habits to retire, and what to do instead.\n\n"
         "Shampoo your scalp, not the lengths. Pick styles that don't need long-hold products. Stretch the time between color "
         "touch-ups, and book one chemical service at a time. And judge your hair with a part photo every six weeks, not the "
         "bathroom mirror.\n\n"
         "If your part is getting wider or your ponytail feels thinner, see a dermatologist.\n\n"
         "More ways to make fine hair look fuller are in the first comment.",
      fb_comment="How to make thin hair look thicker: products, cut and color: {link}"),

 dict(id="AG06", pillar="postpartum", kicker="Postpartum hair", field="espresso", page="/blogs/journal/why-is-my-hair-falling-out",
      slides=[
        dict(t="cover", title="Postpartum<br>shedding usually<br>peaks around<br>month&nbsp;4.", size=116,
             sub="Here&#39;s what&#39;s normal, month by&nbsp;month."),
        dict(t="timeline", title="What to expect.", steps=[
            dict(when="A few months after birth", what="Extra shedding starts."),
            dict(when="About month 4", what="It usually peaks.", on=True),
            dict(when="By the first birthday", what="Most women see normal fullness return.")]),
        dict(t="statement", title="It&#39;s called telogen effluvium.",
             body="It means excessive hair shedding, and it&#39;s common after giving birth."),
        dict(t="list", title="Two dermatologist tips", size=80, items=[
            "Use shampoo and conditioner that add volume.", "Try a new hairstyle."],
             note="From the American Academy of Dermatology."),
        dict(t="checklist", title="See a dermatologist if", items=[
            "It comes out in patches.", "It isn&#39;t back to normal fullness after a&nbsp;year.", "You&#39;re not sure it&#39;s only a&nbsp;shed."]),
        dict(t="sources", items=[("American Academy of Dermatology", "Dermatologist tips for new moms"),
                                 ("Aftergrow Journal", "Why is my hair suddenly falling out?")],
             note="Education, not medical advice. If your hair isn&#39;t back to its normal fullness after a year, see a&nbsp;dermatologist."),
        SAVE],
      hashtags=["postpartumhair", "postpartum", "newmom", "hairshedding", "momlife"],
      ig="Postpartum hair shedding usually peaks about four months after giving birth, according to the American Academy of Dermatology.\n\n"
         "It's called telogen effluvium, which means excessive hair shedding, and it's common. Most women see their hair return to "
         "its normal fullness by their child's first birthday.\n\n"
         "Two dermatologist tips for the months in between: use a shampoo and conditioner that add volume, and try a new hairstyle.\n\n"
         "Save this, and send it to a new mom who needs to hear it.",
      fb="Postpartum hair shedding usually peaks about four months after giving birth, according to the American Academy of Dermatology.\n\n"
         "It's called telogen effluvium, which means excessive hair shedding, and it's common. Most women see their hair return to "
         "its normal fullness by their child's first birthday.\n\n"
         "Two dermatologist tips for the months in between: use a shampoo and conditioner that add volume, and try a new hairstyle.\n\n"
         "Why shedding comes months later is explained in the first comment.",
      fb_comment="Why hair sheds a few months after a big event, like giving birth: {link}"),

 dict(id="AG07", pillar="scalp-care", kicker="Dry scalp season", field="butter", page="/blogs/journal/scalp-serum-for-dry-scalp",
      slides=[
        dict(t="cover", title="Dry scalp<br>or dandruff?", size=132, sub="Two flaky problems. Two&nbsp;different&nbsp;causes."),
        dict(t="statement", label="Dry scalp", title="A loss of moisture.",
             body="That&#39;s what causes a dry scalp, according to Cleveland Clinic.", size=96),
        dict(t="statement", label="Dandruff", title="Excess oil.",
             body="That&#39;s what causes dandruff. So the fix for one isn&#39;t the fix for the other.", size=96),
        dict(t="list", title="Dry scalp habits", items=[
            "Keep showers to 5&nbsp;to&nbsp;10&nbsp;minutes.",
            "Choose fragrance-free products, and read the ingredient list.",
            "Leave-in conditioner goes on your hair, not your scalp."],
             note="From the American Academy of Dermatology and the FDA."),
        dict(t="checklist", title="Call a dermatologist if", items=[
            "The itching won&#39;t stop.", "You have a red rash.", "Your skin is swollen, warm or&nbsp;painful."]),
        dict(t="sources", items=[("Cleveland Clinic", "Dry scalp: causes and prevention"),
                                 ("American Academy of Dermatology", "Is your dry scalp something more serious?"),
                                 ("Aftergrow Journal", "Scalp serum for a dry scalp")], note="Education, not medical advice."),
        SAVE],
      hashtags=["dryscalp", "dandruff", "scalpcare", "itchyscalp", "winterhaircare"],
      ig="Dry scalp or dandruff? They're easy to mix up, but the causes are different.\n\n"
         "A dry scalp comes from a loss of moisture. Dandruff comes from excess oil, according to Cleveland Clinic. So the fix for "
         "one isn't the fix for the other.\n\n"
         "For a dry scalp: keep showers to 5 to 10 minutes, choose fragrance-free products, and keep leave-in conditioner on your hair, "
         "not your scalp. If the itching won't stop, or you see a red rash or swelling, call a dermatologist.\n\n"
         "Save this for winter.",
      fb="Dry scalp or dandruff? They're easy to mix up, but the causes are different.\n\n"
         "A dry scalp comes from a loss of moisture. Dandruff comes from excess oil, according to Cleveland Clinic. So the fix for "
         "one isn't the fix for the other.\n\n"
         "For a dry scalp: keep showers to 5 to 10 minutes, choose fragrance-free products, and keep leave-in conditioner on your hair, "
         "not your scalp. If the itching won't stop, or you see a red rash or swelling, call a dermatologist.\n\n"
         "What to look for in a product for a dry scalp is in the first comment.",
      fb_comment="Scalp serum for a dry scalp: what to look for: {link}"),

 dict(id="AG08", pillar="scalp-care", kicker="Wash day", field="espresso", page="/blogs/journal/oily-scalp-dry-hair",
      slides=[
        dict(t="cover", title="Oily roots,<br>dry ends?", size=132, sub="Wash for your scalp.<br>Condition for your ends."),
        dict(t="statement", num="1", title="Wash as often as your scalp&nbsp;needs.",
             body="Even every day, if the oil bothers you."),
        dict(t="statement", num="2", title="Shampoo goes on the scalp&nbsp;only.",
             body="It cleans the oil and spares your dry&nbsp;ends."),
        dict(t="statement", num="3", title="Conditioner goes on the&nbsp;ends.",
             body="On the scalp it can make things greasy, says Cleveland Clinic."),
        dict(t="list", title="Dry shampoo, the dermatologist way", size=72, items=[
            "It doesn&#39;t clean hair. Wash after one or two uses.",
            "Too much can leave hair dry, stiff and gritty.",
            "Itching or burning? Stop&nbsp;using&nbsp;it."],
             note="From the American Academy of Dermatology."),
        dict(t="sources", items=[("American Academy of Dermatology", "Dry shampoo: tips for your best results"),
                                 ("Cleveland Clinic", "How often should you wash your hair?"),
                                 ("Aftergrow Journal", "Oily scalp but dry hair?")], note="Education, not medical advice."),
        SAVE],
      hashtags=["oilyscalp", "washday", "haircaretips", "dryshampoo", "scalpcare"],
      ig="Oily roots and dry ends? Wash for your scalp and condition for your ends.\n\n"
         "Wash as often as your scalp needs, even every day if the oil bothers you. Put shampoo on the scalp only, so it cleans the "
         "oil and spares your ends. Conditioner goes on the ends; on the scalp it can make things greasy, says Cleveland Clinic.\n\n"
         "And dry shampoo doesn't clean hair, so wash after one or two uses, says the American Academy of Dermatology.\n\n"
         "Save this for wash day.",
      fb="Oily roots and dry ends? Wash for your scalp and condition for your ends.\n\n"
         "Wash as often as your scalp needs, even every day if the oil bothers you. Put shampoo on the scalp only, so it cleans the "
         "oil and spares your ends. Conditioner goes on the ends; on the scalp it can make things greasy, says Cleveland Clinic.\n\n"
         "And dry shampoo doesn't clean hair, so wash after one or two uses, says the American Academy of Dermatology.\n\n"
         "A simple routine for oily roots and dry ends is in the first comment.",
      fb_comment="Oily scalp but dry hair? A simple routine: {link}"),
]
