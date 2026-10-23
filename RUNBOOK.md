# Aftergrow Pinterest runbook

This repository runs Aftergrow's Pinterest without manual work. A Claude scheduled task follows this file every Monday and Thursday at 9:43 AM Eastern, after the Meta run (8:47 AM) has pushed. George, the founder, makes the final calls and reads a five-line report after each run. Anything that needs his decision goes in line 4 of the report. Never guess on his behalf.

Pinterest account: **getaftergrow**. Tailwind account ID: **1658425**. Use no other account.

**Status, Oct 23, 2026:** Pinterest is **live**. The Oct 11 block has lifted: canary C01 published on Oct 23 with its link intact, after Pinterest's Shopify catalog sync published 6 product pins on Oct 22. Probation runs to Nov 6 (`autopilot.py` keeps the queue short). The Tailwind plan was cancelled by George and ends Nov 11, 2026 unless he reactivates it: put that in line 4 until it's resolved. Instagram and Facebook still run from **META.md**, which uses this file's **Fact sheet** and **Journal page map**, so keep them current.

## What is here

| Path | What it is |
|---|---|
| `status.json` | The mode, `live` or `blocked` (Pinterest is rejecting our links), plus canary attempts and the appeal status. |
| `queue.json` / `queue.csv` | Every pin and its order, board, board ID, title, description, link (UTM tagged) and alt text. Also its status (`ready`, `scheduled`, `posted`), Tailwind post ID and history. This is the single source of truth. |
| `boards.json` | The 8 boards, their descriptions and Tailwind board IDs. |
| `pins/` | Finished pins, 2000 x 3000 PNG, served publicly so Tailwind can fetch them. |
| `engine/autopilot.py` | Decides and records. It keeps `queue.json` and `status.json` in step with Tailwind. Every Tailwind action in this runbook goes through it. |
| `engine/queue_build.py` | Validates all copy, image text, links and boards, then orders the ready pins. |
| `engine/pinengine.py`, `engine/batch2.py` | The pin engine: brand fonts, exact palette, The Part symbol, 25 layouts, headless Chromium. |
| `log.json` | Every scheduling, failure, pause and appeal update, with times. |

`AP` below means `python3 -I engine/autopilot.py .`

## Start of every run, in this order

1. **Get the repo.** Call `add_repo` (owner `domin8commerce`, repo `aftergrow`, access `push`), run the clone command it returns, then call `register_repo_root`. Then `cd aftergrow && (cd engine && npm install)` to fetch the brand fonts (Chromium is preinstalled).
2. **Validate.** Run `python3 -I engine/queue_build.py .`. It must print `problems: none`. If it doesn't, fix the problem (or stop and report it) before touching Tailwind.
3. **Reconcile with Tailwind.** Call `list_posts` (status `queued`, limit 100), save the raw JSON response to `/tmp/queued.json`, and run `AP reconcile /tmp/queued.json`. Then act on every line it prints:
   - **`RESOLVE <ID>`.** `get_post` that post, then:
     - `sent`: `AP resolve <ID> sent`
     - `failed`: `AP resolve <ID> failed "<failureReason>: <failureMessage>"`
     - `deleted`: `AP resolve <ID> deleted`
     - still `queued`: `delete_post` it, then `AP resolve <ID> missed`
   - **`MISSED <ID>`.** `delete_post` that post, then `AP resolve <ID> missed`.
   - **`UNKNOWN` or `DUPLICATE`.** Follow the printed instruction. If unsure, stop and report.
   - **"SWITCHED TO BLOCKED"** (printed by a resolve). Delete every other queued post with `delete_post` and run `AP resolve <ID> deleted` for each. Keep none of them.
4. **Read the plan.** Run `AP status`. It prints the mode and exactly what to do next.
5. **Push.** Commit and push whatever changed.

Then do **Blocked mode** or **The weekly loop**, depending on the mode.

## Blocked mode

Pinterest blocked getaftergrow.com as spam on the first pin (Oct 11, 2026). The domain was registered Sept 30, 2026, and brand-new claimed domains were hit by the same block in Sept and Oct 2026. Only George can appeal, because it needs his Pinterest login. The form link is in `status.json`.

**Canaries.** A canary is one real pin used to test whether the block has lifted. There is at most one queued at a time, and at most 2 attempts in any 7 days. An attempt is a canary whose publish time passed; a deleted or missed canary doesn't count. Repeated blocked links look like spam and put the account at risk, so `autopilot.py` enforces these limits. Don't work around them. If George says Pinterest approved the appeal, run `AP appeal approved`; the next run then tests at once.

1. **If `status` says "schedule one canary":**
   - Run `AP next-canary`. It picks a ready pin that has never been blocked, on a page not yet tried in this block, and prints its `create_post` payload.
   - Call `create_post` with exactly that payload.
   - Run `AP scheduled <ID> <postId> <sendAt>` with the values `create_post` returned.
   - Schedule nothing else.
2. **Build inventory, don't schedule it.** If fewer than 42 pins are ready, make up to 10 new pins (see **Make** and the **Quality gate**), within the cap of 8 pins per landing page. Push them.
3. **Report.** Line 4 carries the appeal:
   - `appeal.filed_on` is empty: "File the Pinterest appeal (link in status.json) and tell Claude when it's filed." When George confirms, run `AP appeal filed <date>`.
   - Filed 7+ days ago and still blocked: "Reply to Pinterest's email and ask for a human review. Mention the domain is new and claimed through the Pinterest app for Shopify."
   - Never ask him to file a second appeal the same week.

### Paused after a denied appeal (since Oct 11, 2026)

Pinterest denied the appeal about 4 hours after George filed it. The reply was automated (pinbot@legal.pinterest.com). Testing again before something changes would only add blocked attempts, so the system is paused:
- No canaries before `retest_after` in `status.json` (`autopilot.py` enforces this).
- The Monday and Thursday runs are off. One check-in runs Nov 9, 2026, the day before Tailwind renews. It reminds George to re-appeal (the text is `reappeal_text` in `status.json`), reports the Tailwind plan and credits, and schedules nothing.
- What George can change meanwhile is listed in `reappeal_checklist` in `status.json`.

### Restart (George says Pinterest approved the domain)

1. Run `AP appeal approved`, then `AP status`. It allows a canary at once.
2. Do **Blocked mode** step 1: the canary.
3. Re-arm the scheduled task with `update_trigger`. Use the cron and prompt in `autopilot_prompt.md`.
4. When a run finds the canary published, it does **Release**.

### Release (the canary published)

`AP resolve <ID> sent` prints "BLOCK LIFTED" and switches the mode to `live`, with 14 days of probation.

1. Run `AP status`. It prints how many pins to schedule now. During probation it only covers until a day after the next run, so a new block would cost a few failed pins at most.
2. Run `AP next-batch <N>`. It prints one `create_post` payload per line, in queue order, and skips any pin whose image isn't reachable yet.
3. Call `create_post` for each, **one call at a time, in the printed order**. After each one, run `AP scheduled <ID> <postId> <sendAt>`.
4. Confirm with `list_posts` (status `queued`), then commit and push.

## The weekly loop (live mode)

1. **Start of every run.** Done above. Reconcile catches everything that published or failed.
2. **Learn** (Mondays only, once 21+ pins have been live 21+ days).
   - Pull `list_top_pins` with `contentType: ORGANIC` over the last 90 days, three times: by `SAVE`, by `OUTBOUND_CLICK` and by `IMPRESSION`.
   - Use `get_pin_analytics` (the Pinterest pin ID, not the Tailwind post ID) for any pin you need full numbers on.
   - Match pins to queue rows by `utm_content` in the link.
3. **Decide** with the rules in **The reload engine** below.
4. **Make** new pins (see **Make**). Stop at 10 per run; quality beats volume.
5. **Quality gate** on every new pin. If a pin fails, it doesn't ship.
6. **Push the pins first.** Commit and push `pins/` and `engine/`. `next-batch` checks every image URL and skips any that isn't live yet.
7. **Schedule.** Run `AP status` for the number, then `AP next-batch <N>`. Call `create_post` once per pin, in order, and run `AP scheduled ...` after each.
8. **Commit and push** `queue.json`, `queue.csv`, `status.json` and `log.json`.
9. **Report** to George in five lines (format at the bottom).

## The reload engine: what keeps the machine fed, and why

### What the data says, and what we do about it

- **Pinterest is a hits business.** In Tailwind's 2025 study of about 1.2 million Pins from 17,000+ accounts, the top 1% of Pins drove over 50% of impressions and clicks on Pins from the last 90 days. The bottom 80% drove under 10%. **So we find the few winners and multiply them.** We don't spread effort evenly.
- **Fresh designs drive the traffic.** In the same study, over 90% of traffic to brand websites came from original Pins (Creates), not re-saves. **So spare credits go to new designs of proven ideas, not to re-pinning one image to many boards.**
- **Pins compound slowly.** Winning Pins in that study averaged 18 new saves when under 90 days old, 44 at 90 days to 1 year, and 68 at 1 to 2 years. Engagement peaked between years one and two. **So we judge early pins on rates, not totals, and never delete a published pin for underperforming.**
- **Pace.** Tailwind's guidance is 3 to 5 Pins a day for new accounts and 5 to 10 after 6 months. It also recommends 3 to 5 different designs per URL, each aimed at a different keyword.

### Decision rules

- **Readable pin:** at least 500 impressions, or live at least 30 days. Only judge readable pins.
- **Save rate** = saves / impressions. **Outbound click rate** = outbound clicks / impressions.
- **Winner:** a readable pin in the top 20% by save rate or by outbound click rate, with at least 3 saves or 3 outbound clicks. Below that floor it's luck.
- **Each winner gets 3 fresh variants** over the next 2 weeks, never more than 2 variants of one pin in any 7 days.
- **Board review every 4 weeks:**
  - A board with 15+ readable pins and zero saves gets no new pins for 4 weeks. Its share moves to the best board.
  - A board whose save rate is at least 1.5 times the account median gets 1 extra pin in every 10.
- **70 / 30.** 70% of new pins exploit: variants of winners and the best boards. 30% explore: new keywords from the bank below, new layouts and trend tests.
- **Before there is data** (first 30 live days): ship the planned queue, plus keyword-coverage variants (different keywords for the same page).

### Variant recipe

- **Keep:** the landing page (same URL, new `utm_content` ID such as `A01b`), the facts and the board.
- **Change at least 3 of:**
  - the headline angle (a new long-tail keyword in the first 40 characters of the title)
  - the layout
  - the field color
  - the hook type (number, question, myth vs. fact, checklist or timeline)
  - the wording of the title and description
- **Never** ship a recolor of the same headline. Tailwind warns against posting many near-identical Pins in one week.

### Trend layer (first run of each month)

- **Pull Pinterest's own search data, not press releases.** Load the Composio tools (ToolSearch "composio", then COMPOSIO_SEARCH_TOOLS for "pinterest keyword trends"). Run `PINTEREST_GET_KEYWORD_TRENDS` with the parameters in `research/README.md` (US, female, ages 35-44 to 55-64, normalized, demographics on). Run it twice for the board clusters below, once with `trend_type: monthly` and once with `growing`. Save the rows as `research/pinterest-trends-YYYY-MM-DD.csv` and compare them with the last file.
- **Explore pins.** Make up to 4 a month for rising terms. A term qualifies when it's up year over year or month over month, at least 45% of its searchers are 35 to 64, and it fits a board, a live page and the fact sheet.
- **If Composio isn't available in the run,** say so in line 4 of the report and use Pinterest's newsroom trend reports instead.
- **Openings in the Oct 23, 2026 data:**
  - "fine thin hair over 50" +2,500%
  - "haircuts for thinning hair" +100%
  - "rosemary water for hair" +400%
  - "itchy scalp" +70%
  - "head spa" +20%
  - "peptides for women" +400%. Most of these searches are about injectable peptides; only ingredient education fits us.
- **Rosemary.** It's in our formula, so the rosemary cluster is a trend we can honestly own. The scalp-serum-or-scalp-oil page allows no claims about what rosemary does for hair. A full cluster needs a dedicated Journal article (see Backlog).
- **Banned words.** The brand book bans "treatment" and "detox". Only George can change that.
- **Seasonal.** Publish 45 to 60 days before each peak. Peaks are taken from the Oct 23 data:
  - Dry and itchy scalp peaks January to February: publish from now through February.
  - "Hairstyles for thin hair" peaks in November: publish now.
  - "Head spa" and "scalp massage" peak in January: publish from mid-November.
  - New Year hair routine: from mid-November.
  - Postpartum searches peak in March, but they come from 25 to 34 year olds (see Boards).

### Pace and credits

The Tailwind plan gives 300 credits a month. One credit is one pin to one board. The next reset is Nov 10, 2026. Plan as if unused credits don't carry over. Deleting a queued post doesn't refund its credit.

| Phase | Pins a day | Credits a month | Share of plan |
|---|---|---|---|
| Launch, first 30 live days | 3 | ~91 | 30% |
| After 30 live days, if save rate holds and 14 days are queued | 5 | ~152 | 51% |
| After 6 months | 8 to 10 | ~243 to 300 | 81 to 100% |

- **To raise the pace,** change `PACE` in `engine/autopilot.py`, then add timeslots with `create_timeslot` (afternoons and evenings, never two within an hour).
- **Re-saves** (`intervalBoards`) are allowed only for proven winners, to the second most relevant board, 7+ days apart. They get at most 10% of monthly credits.
- **Monthly board audit:** once boards have 10+ pins, spend 1 credit per board on `get_board_keyword_relevance` for its main keyword.

### Landing pages are the fuel

Every pin needs a page that answers it.

**Since Oct 12, ten more Journal articles have gone up.** They aren't in `LIVE_PAGES` yet. Read each one through the Shopify connector (`graphql_query`: `articles(first: 1, query: "handle:<handle>") { nodes { title body publishedAt } }`), or with WebFetch when it isn't blocked by a permission prompt. Confirm it's published, has real content that answers the pin, and isn't about weight loss. Then add it to `LIVE_PAGES` and to the page map with its facts and the date. Never add `hair-shedding-timeline-and-care` (weight-loss surgery). The new articles, by the board they serve:
- Thinning hair: `is-my-hair-thinning`
- Dry scalp care: `can-dry-scalp-cause-hair-loss`
- Head spa at home: `how-to-clean-your-scalp` and `why-is-my-hair-greasy`
- Fine thin hair over 50: `simple-hair-care-routine` and `color-treated-hair-care`
- Hair care ingredients: `vitamins-in-hair-serums`, `hyaluronic-acid-hair-serum` and `homemade-hair-serum`

**The highest-demand topics still have no page:** best haircuts for thin hair, hairstyles for thinning hair, and fine thin hair over 50. Ask George for those three articles first (line 4).

As of Oct 11, 2026 there were 21 live pages: 5 site pages and 16 Journal articles. The first 34 pins use only 7 of them, and `queue_build.py` caps each page at 8 pins. **The next pins come from the Journal page map below.** Each new Journal article opens a new keyword cluster and 5 to 10 more pins. When the map runs low, ask George for the next article from the Backlog in line 4 of the report.

## Journal page map (what to make next)

Each page below loads with real, sourced content. The facts listed for a page are on that page, so pins may state them; that adds to the **Fact sheet**. **Pick angles in this order (Oct 23 data):**
1. The empty high-demand boards: Haircuts for thin hair and Hairstyles for thin hair, from `make-hair-look-thicker`.
2. Dry scalp care while it's in season (now through February), from `can-dry-scalp-cause-hair-loss`, `scalp-serum-for-dry-scalp` and `why-is-my-hair-so-dry`.
3. Fine thin hair over 50.
4. The rest.

Never put "hair loss" in a title or on an image (descriptions only). Never say "treatment" or "detox" (brand book).

| Page (`/blogs/journal/...`) | Board | Searches | Pin angles | Facts on the page |
|---|---|---|---|---|
| `hair-shedding-vs-hair-loss` | Thinning hair | hair shedding vs hair loss (descriptions), is my hair shedding or falling out | 1. Shedding or something more: the difference (split). 2. Why only a dermatologist can tell (checklist). 3. Myths about shedding (held idea A09). | Shedding: hairs fall out at the end of their resting phase. 50 to 100 a day is normal (AAD). Excessive shedding often stops on its own as the body readjusts (AAD). A dermatologist can tell which you have, and some people have both. For 1 in 3 people diagnosed with telogen effluvium, no cause is found (BAD). |
| `why-is-my-hair-falling-out` | Thinning hair | why is my hair falling out, sudden hair shedding | 1. Why is my hair suddenly falling out? First steps (checklist). 2. All over or in patches: what the pattern says. | Often a shed that starts a few months after a big event. A shed usually comes from all over the scalp (BAD); round patches point to another cause. Don't stop a medicine on your own. A blood test can show whether you're low in a nutrient. See a dermatologist if shedding is sudden, patchy or lasts more than six months. |
| `breakage-or-shedding` | Thinning hair | hair breakage vs shedding, white bulb on hair | 1. Breakage or shedding? Check the end of the hair (strand). 2. Habits that cause breakage (list). 3. "100 strokes a day" is a myth. | A shed hair is usually full length with a small white bulb at the root. A broken hair has no bulb and is usually shorter. Damaged hair is fragile, so it tends to break (AAD). Hot tools once a week or less (AAD). 100 strokes a day is a myth (AAD). |
| `make-hair-look-thicker` | Haircuts for thin hair, Hairstyles for thin hair, Fine thin hair over 50 | haircuts for thinning hair (+100%), thin hair haircuts, hairstyles for thinning hair, fine thin hair over 50 (+2,500%), hair toppers for thinning hair | 1. Haircuts for thin hair: a shorter cut or layers (Cleveland Clinic). 2. What to ask your stylist when hair is thinning: color at a salon that specializes in it, one service at a time, longer between touch-ups, a style that doesn't pull. 3. Hairstyles for thinning hair: 5 swaps that look fuller (loose styles with covered bands, lowest heat, a volume shampoo, conditioner on the ends, colored spray at the part). 4. Cover a wider part: colored hair spray, fiber powder, wigs and toppers (DermNet, NHS). 5. Hair color and thinning hair: dye adds volume to each strand (Cleveland Clinic). 6. Fine thin hair over 50: 4 changes that look fuller, plus the one sign to see a dermatologist. 7. "Thickening" on a label: look or growth? (held idea D03/D07 styling fits here too) | Cleveland Clinic: a shampoo that adds volume, without sulfate detergents; a shorter cut, layers or new styling techniques "may help hide hair loss" (on images say "may help thinning hair look fuller"); dye "can add volume to each strand, so hair seems fuller". AAD: thinning hair is fragile, so be gentle; a shampoo that helps hair hold moisture makes hair look fuller and thicker; products made for your hair type, such as fine hair; conditioner after every shampoo (fine or straight hair: the ends; dry or curly: the whole length); choose a style that doesn't pull or need long-hold products; wear hair loosely pulled back with covered bands; lowest blow-dryer heat or air dry, curling irons, flat irons and hot combs for special occasions; for thinning hair skip at-home color and go to a salon that specializes in it; stretch the time between touch-ups and book one service at a time; a widening part and a thinner ponytail are possible signs of female pattern hair loss, so see a board-certified dermatologist; hiding thinning with a new part or hairstyle rarely reaches the cause. DermNet: colored hair sprays cover thinning areas; hair bulking fiber powder and wigs are other options. NHS: synthetic wigs are easier to look after but can be itchy and hot; real-hair wigs look more natural but cost more. FDA: a claim to restore hair growth is a drug claim. Never name a specific cut (bob, lob, shag, pixie) as making hair look fuller until a page states it. |
| `why-is-my-hair-so-dry` | Dry scalp care | why is my hair so dry, dry hair tips, dry hair in winter | 1. Why is my hair so dry? Common causes. 2. Four changes that help dry hair. 3. Dry hair or dry scalp? | MedlinePlus suggests washing about once or twice a week for dry hair. Use conditioner after every wash. Air dry when you can. Rinse right after swimming. Silicones form a thin film around each strand (2025 review). If gentle care doesn't help, see a health care provider. |
| `oily-scalp-dry-hair` | Head spa at home | oily scalp dry hair, oily roots dry ends | 1. Oily roots, dry ends: shampoo the scalp, condition the ends (held idea F02). 2. Dry shampoo: three dermatologist rules. | Wash as often as your scalp needs, even every day. Shampoo on the scalp only. Conditioner on the scalp can make it greasy (Cleveland Clinic). Dry shampoo doesn't clean hair; wash after one or two uses (AAD). Too much leaves hair dry, stiff and gritty. Stop if you get itching or burning. |
| `types-of-scalp-treatments` | Head spa at home | scalp scrub (trend +31%), scalp oil, scalp care products | 1. Serum, scrub, mask or oil: which does what (grid). 2. How to use a scalp scrub gently. 3. Hair oiling, the careful way. | A scrub removes dead skin cells and rinses off. Exfoliate with small circular motions for about 30 seconds, then rinse with lukewarm water (AAD). Cleveland Clinic advises against oil directly on the scalp. For oil: dry hair, a pea-sized amount, middle to ends, 20 minutes to an hour, then wash out. |
| `scalp-serum-or-scalp-oil` | Hair care ingredients | rosemary water for hair (trend +269%), rosemary oil, essential oils for scalp | 1. Rosemary extract, oil or water: what's the difference? 2. Essential oils on your scalp: three things to know. 3. Serum or oil: four things to compare on the label. | Rosemary extract in a finished product is one ingredient in a set formula, with directions and warnings on the label. Essential oils evaporate easily (DermNet), and some can cause an allergic skin reaction; don't put neat, undiluted oils on skin. Whoever makes a cosmetic, including at home, is responsible for its safety (FDA). Throw out cosmetics that change color or smell. Compare base, finish, where it goes and directions. **No claims about what rosemary does for hair.** |
| `fragrance-free-hair-routine` | Hair care ingredients | fragrance free hair care, fragrance free shampoo | 1. Switch to fragrance-free in five steps. 2. Fragrance-free isn't irritation-free. | Check the list for Fragrance, Parfum or Perfume. A fragrance-free product can still irritate or contain an allergen. Front-label words aren't a safety standard. Change one product at a time. Stop any product that gives a rash, redness or burn (FDA). The FDA groups common cosmetic allergens into five groups. |
| `natural-scalp-serum` | Hair care ingredients | natural hair products, organic hair care, clean hair care | 1. "Natural" vs "organic" on a hair label: what the words mean. 2. Is natural always gentler? | The FDA says an ingredient's source doesn't decide its safety. USDA "Organic": at least 95% organically produced ingredients, not counting water and salt. "Made with organic ingredients": at least 70%, and the front can name up to three. "Natural" has no rule. |
| `scalp-serum-or-hair-supplement` | Hair care ingredients | hair vitamins, biotin | 1. Taking biotin? Tell your doctor before a blood test. 2. Questions to ask before a hair supplement (held idea F04). 3. Serum or supplement: format and routine (no prices, no brands). | The FDA doesn't approve dietary supplements before they're sold. Biotin can cause falsely high or low blood test results (FDA). Check the label for biotin (vitamin B7). Don't take supplements instead of prescription medicines (FDA). |
| `scalp-serum-for-dry-scalp` | Dry scalp care | dry scalp, dry scalp vs dandruff, itchy scalp, winter | 1. Dry scalp or dandruff? The one difference. 2. Dry scalp habits. 3. When an itchy scalp needs a dermatologist. | A loss of moisture causes a dry scalp; excess oil causes dandruff (Cleveland Clinic). Call a dermatologist for itching that won't stop, a red rash, or swollen, warm or painful skin. Choose fragrance-free and check the ingredient list (FDA). Leave-in conditioner goes on hair only (AAD). Keep showers to 5 to 10 minutes (AAD). |
| `can-dry-scalp-cause-hair-loss` (verified 2026-10-23 through the Shopify connector) | Dry scalp care | itchy scalp (+70%), dry scalp, dry scalp treatment diy (58% aged 35 to 64, peaks Jan-Feb) | 1. Dry, itchy scalp and shedding: what dermatologists say (no "hair loss" in the title or on the image). 2. Itchy scalp: 4 signs it's time to see a dermatologist (checklist). 3. Scratching an itchy scalp: what the AAD advises (short, smooth nails; remove scale gently; don't pick; air dry). 4. What an ordinary dry scalp looks like, and what it doesn't (itching and flakes only). | Neither the AAD nor the Cleveland Clinic dry scalp page says dryness on its own causes hair loss; both describe itching and flakes. Some conditions that look like a dry scalp at first can come with hair loss (scalp psoriasis, a fungal scalp infection). The AAD says even dandruff and a dry scalp can be tricky to tell apart without a dermatologist. Scratching hard, or using force to remove scale, can loosen hair (AAD). AAD tips: keep nails short and filed smooth; remove scale gently; don't pick; let hair air dry, because blow drying can dry the scalp more. See a dermatologist if an itchy scalp isn't improving or comes with hair loss, a rash or pain; if skin becomes painful or swollen or drains fluid (a sign of infection, Cleveland Clinic); or if over-the-counter products don't help (AAD). |
| `what-to-look-for-in-a-scalp-serum` | Aftergrow Scalp Serum | how to choose a scalp serum | 1. Eight checks before you buy a scalp serum. 2. "Hypoallergenic" has no federal definition. 3. Judge a serum fairly: same place, light, part and angle. | "Unscented" may still contain fragrance (FDA). "Hypoallergenic" has no federal standard (FDA). Ingredients at 1% or less can be in any order. Wash as often as your hair gets dirty or oily (AAD). |
| `how-to-use-a-scalp-serum` | Head spa at home | how to use scalp serum, wet or dry hair | 1. Wet or dry hair? Before or after washing? 2. Patch test first: behind the ear, 24 hours. | Follow your serum's label. Aftergrow: a few drops on a clean, dry scalp. Make a part where you can see the skin. Patch test: a few drops behind the ear, wait 24 hours. |

`hair-serum-or-scalp-serum` (C04) and `how-to-read-a-scalp-serum-label` (E05) already have one pin each and take more angles from the Fact sheet.

## Hooks that get saved and shared (George, Oct 23: "holy shit, I didn't know that about hair")

Every run, at least 3 of the new pins come from this bank. Each headline is a true, sourced fact that surprises, and the pin pays it off. That makes people save it and send it to a friend. Never exaggerate, never scare, and never claim beyond the source.

| Hook (headline idea) | Source | Page | Board |
|---|---|---|---|
| 100 brush strokes a day is a myth | AAD | `breakage-or-shedding` | Thinning hair |
| Dry shampoo doesn't clean your hair | AAD | `oily-scalp-dry-hair` | Head spa at home |
| "Hypoallergenic" has no legal definition | FDA | `what-to-look-for-in-a-scalp-serum` | Hair care ingredients |
| Taking biotin? It can throw off your blood tests | FDA | `scalp-serum-or-hair-supplement` | Hair care ingredients |
| "Natural" on a hair label has no rule behind it | FDA | `natural-scalp-serum` | Hair care ingredients |
| Hair color can make thin hair look thicker | Cleveland Clinic | `make-hair-look-thicker` | Fine thin hair over 50 |
| A widening part is a reason to see a dermatologist, not to switch shampoo | AAD | `make-hair-look-thicker` | Thinning hair |
| Your ponytail could be thinning your hair (tight styles pull on fragile hair) | AAD | `make-hair-look-thicker` | Hairstyles for thin hair |
| A shorter cut or layers can make thin hair look fuller | Cleveland Clinic | `make-hair-look-thicker` | Haircuts for thin hair |
| Scratching an itchy scalp can loosen hair | AAD | `can-dry-scalp-cause-hair-loss` | Dry scalp care |
| Blow-drying can dry your scalp even more | AAD | `can-dry-scalp-cause-hair-loss` | Dry scalp care |
| For 1 in 3 people with telogen effluvium, no cause is found | BAD | `hair-shedding-vs-hair-loss` | Thinning hair |
| Conditioner on your scalp can make it greasy | Cleveland Clinic | `oily-scalp-dry-hair` | Head spa at home |
| Ingredients under 1% can be listed in any order | FDA | `how-to-read-a-scalp-serum-label` | Hair care ingredients |
| A hair growth claim makes a cosmetic a drug, legally | FDA | `make-hair-look-thicker` | Hair care ingredients |
| Fragrance-free isn't irritation-free | FDA | `fragrance-free-hair-routine` | Hair care ingredients |
| Wet hair breaks more easily: let it dry a bit before you comb | AAD | Fact sheet | Thinning hair |

**Formats that carry a hook:**
- myth vs fact (`contrast` or `split`)
- crossed-out habit and its swap (`swap`)
- one big number (`bignum`)
- label callouts (`label`)

**Titles.** Put the board's search phrase, or the hook containing it, in the first 40 characters. Check phrases against `research/`. Examples:
- "Thinning hair or normal shedding? Losing 100 hairs a day is normal"
- "Fine thin hair over 40 or 50? Stop these 5 habits"

## Promotion (Pinterest ads) readiness

Pinterest ads ban weight-loss content, and ad review checks the landing page. `/pages/how-it-works` says "such as fast weight loss", so pins linking there are not for promotion until George changes that line. Every other live page is fine to promote. Flag it in line 4 when a winner links to how-it-works.

## Make

- **New designs** go in a new file `engine/batchN.py` (N = 3, 4, ...). Copy the header and the `__main__` block of `engine/batch2.py`, and `import batch2` so all 25 layouts are available.
- **The file defines** `PINS` (designs, same format as `batch2.PINS`) and `COPY`, a list of rows `(id, slug, board, title, description, link, alt)`. Import `L` and the board and page constants from `queue_build`.
- **Render** with `python3 -I engine/batchN.py pins <IDs>`, then run `python3 -I engine/queue_build.py .`. It finds the new batch, validates it and orders the ready queue.
- **Start from a working pin.** Each layout has its own fields, so copy the dict of a pin that already uses that layout and change the text. Never invent field names.

| Layout in `pinengine.py` | Copy from | Layout in `batch2.py` | Copy from |
|---|---|---|---|
| timeline | A01 | bignum | A02 |
| ledger | E02 | definition | A05 |
| viewfinder | G02 | list2 | A06, A07, D01, D06, F05 |
| checklist | A03, A10 | ruler | A08 |
| contrast | E06 | curve | B01 |
| swap | D04 | split | B02, C04 |
| cycle | A04 | frames | B07 |
| list | B04 | parts | C03 |
| steps | C01 | grid4 | C07, E04 |
| strand | F01 | schedule | D05 |
| | | ledger2 | E01, E03, H02 |
| | | label | E05 |
| | | grid6 | E07 |
| | | weekline | G03 |
| | | protocol | H03 |

- **Fields** are `butter`, `espresso`, `white` and `porcelain`. Use `<br>` for deliberate line breaks and `&nbsp;` to keep "6&nbsp;months" together.

## Quality gate (every new pin, before it is pushed)

- **Look at it twice.** View the render at full size and at 236 px wide; the headline must read at feed size. Every word on the image matches the copy. No line ends with a single stranded word.
- **Run `queue_build.py`.** It must print `problems: none`. It checks:
  - title, description and alt text lengths
  - banned words in the copy and on the image
  - drug names, exclamation marks and all-caps words
  - "hair loss" outside descriptions
  - UTM tags, boards and image files
  - links to unverified pages, and more than 8 pins on one page
- **Banned anywhere:**
  - weight loss, diet, slim, before and after, regrow
  - stop or prevent hair loss, cure, treat (and treatment)
  - clinically proven, miracle, holy grail, detox, game-changer
  - any drug name or drug class, GLP-1
  - em dashes, exclamation marks, emoji, all caps
  - "Hair loss" may appear in descriptions only.
- **Claims and proof.** Cosmetic claims only, and only facts from the **Fact sheet** below. No review counts, ratings, customer numbers, before and after, or AI people as customers.
- **Title:** under 100 characters, with the keyword in the first 40.
- **Description:** 150 to 280 characters, with the keyword in the first sentence and a soft call to action.
- **Alt text:** describes the image.
- **Links.** Only pages in `LIVE_PAGES` in `engine/queue_build.py`. To add a page, read it with WebFetch (the shell can't reach getaftergrow.com). Confirm it loads with real content that answers the pin, then add it to `LIVE_PAGES` with the date.

## Fact sheet (checked Oct 11, 2026; pins may state only these, plus the facts in the Journal page map)

- **American Academy of Dermatology**, "Do you have hair loss or hair shedding?":
  - "It's normal to shed between 50 and 100 hairs a day."
  - Excessive shedding is noticed "a few months after the stressful event."
  - "Within six to nine months, the hair tends to regain its normal fullness."
  - The medical term is telogen effluvium.
  - Triggers include giving birth, high fever, an operation, recovering from an illness, lots of stress and stopping birth-control pills. AAD also lists losing 20 pounds or more; pins never say that.
- **American Academy of Dermatology**, "Hair loss in new moms" (page title "Hair loss in new moms: Dermatologist tips"; on slides call it "Dermatologist tips for new moms"):
  - "Hair shedding usually peaks about four months after giving birth."
  - "Most women see their hair return to its normal fullness by their child's first birthday."
  - "If your hair does not regain its normal fullness after one year, you may want to see a dermatologist." (checked Oct 11, 2026)
  - Tips: "Use shampoo and conditioner that add volume." Use conditioner mainly on the ends. "Try a new hairstyle." "Some haircuts make hair look fuller." (checked Oct 11, 2026)
- **American Academy of Dermatology**, "10 hair care habits that can damage your hair" (checked Oct 11, 2026; habit, then the fix):
  - Rubbing shampoo into the length: "Gently massage shampoo into your scalp."
  - Skipping conditioner: "Use conditioner after every shampoo."
  - Rubbing hair dry with a towel: "Wrap your hair in a towel to absorb the water." "Let your hair air dry."
  - Brushing wet hair: straight hair, "Let your hair dry a bit before you gently comb it with a wide-tooth comb"; textured hair or tight curls, comb while damp with a wide-tooth comb.
  - Hot tools: "Use the lowest heat setting." "Use these tools less frequently, aiming for once a week, or even less often."
  - Long-hold styling products: "Try a hairstyle that does not require this product."
  - Pulling hair back tightly (ponytail, bun, cornrows): "Wear hair loosely pulled back." "Use covered rubber bands made especially for styling hair."
  - Color, perms, relaxers: stretch the time between touch-ups (every 8 to 10 weeks or longer in winter); "Have only one service"; if more than one, perm or relax 2 weeks before color.
  - "Hair never needs 100 brush strokes a day. That's a myth." "Brush and comb your hair only to style it." Use a wide-tooth comb, gently.
- **/pages/how-it-works:**
  - "Each hair on your head grows for years, then rests for about three months before it falls out." (checked Oct 11, 2026)
  - "New hairs grow from the same follicles, but they take months to reach length."
  - "A shock to the body sends many hairs into the resting phase at once."
  - Hair often sheds "two to four months after a big change in the body."
  - For most people it "settles on its own within six to nine months."
  - Each hair "rests for about three months before it falls out."
  - "If shedding is still heavy after six months, see a dermatologist."
- **/pages/ingredients:**
  - Five peptides that condition the scalp and support the look of thicker hair. Results vary.
  - Six plant extracts: eucalyptus (a fresh, clean scalp feel), soybean germ, wheat germ, scutellaria root, rosemary (a fresh feel) and saw palmetto.
  - Water-based.
  - Free from: added fragrance, parabens, sulfates, silicones, phthalates and mineral oil. Fragrance-free means no ingredient is added just for scent; it doesn't mean allergen-free.
  - Contains soy and wheat.
- **/products/scalp-serum:**
  - "For fuller-looking hair."
  - Directions: "Apply a few drops to a clean, dry scalp. Massage for 1 to 2 minutes. Do not rinse. Use once a day."
  - The 90-Day Protocol: $108 for 3 bottles every 3 months, free shipping, skip or cancel anytime, refund on the first order.
- **/pages/the-check-in:**
  - A part photo at week 0 (when the bottles arrive), week 6 and week 12, then choose: keep going, take a break, or use the guarantee. Aftergrow sends reminders.
  - Photo rules: same window, daylight, same time of day; phone above the head, camera down, about a foot away; no filter, flash or zoom; dry hair parted in the same place.
- **/blogs/journal/how-to-read-a-scalp-serum-label:**
  - Ingredients run from most to least, and those at 1% or less can be in any order.
  - "Fragrance" or "Parfum" means added fragrance, and "unscented" products may still contain fragrance.
  - Aftergrow's list starts with water.
- **/blogs/journal/hair-serum-or-scalp-serum:**
  - "The difference is where it goes": a hair serum for the lengths and ends, a scalp serum for the skin of the scalp.
  - Use the scalp serum first, then the hair serum on the lengths.

## Boards and the evidence behind them

### Pinterest's own search data (Oct 23, 2026)

Since Oct 23 we have real numbers: Pinterest Trends, for US women aged 35 to 64, pulled through Composio. They're saved in `research/pinterest-trends-2026-10-23.csv`, and `research/README.md` explains them. They overturn most of the Oct 11 board evidence below.

- **Where the demand is.** By far the biggest demand is **haircuts and hairstyles for thin, fine or thinning hair**. "Hairstyles for thin hair" and "thin hair haircuts" lead the cross-cluster benchmark. The "thinning hair" phrases skew to our buyer: 59 to 72% of their searchers are 35 to 64. "Haircuts for thinning hair" is up 100% year over year.
- **"Fine thin hair over 50"** is up 2,500% year over year, with 51% of searchers aged 45 to 64. "Hair over 50" draws 83% of its searchers from ages 35 to 64.
- **Dry and itchy scalp** draws 58% of its searchers from ages 35 to 64 and peaks January to February. **Head spa** and **scalp massage** are growing.
- **No measurable demand:** hair shedding, telogen effluvium, scalp serum, peptides for hair, menopause hair. "Hair loss" is suppressed (no data at all).
- **Postpartum hair** searchers are 67 to 70% aged 25 to 34, outside our buyer. GLP-1 searches on Pinterest are meals and recipes, not hair.

### The boards since Oct 23, 2026 (restructured with George's yes)

| Board | Tailwind board ID | Was | Why |
|---|---|---|---|
| Hairstyles for thin hair | 1108448595728308247 | Hair progress photos | The biggest search in our space; peaks in November |
| Haircuts for thin hair | 1108448595728308242 | Postpartum hair care | Second biggest; "haircuts for thinning hair" +100%, up to 72% of searchers aged 35 to 64 |
| Fine thin hair over 50 | 1108448595728308244 | Hair care tips for women over 40 | +2,500% year over year; 51% of searchers aged 45 to 64 |
| Thinning hair | 1108448595728308241 | Hair shedding explained | "Thinning hair" has demand and skews older; "hair shedding" shows none |
| Dry scalp care | 1108448595728308246 | Healthy hair habits | 58% of searchers aged 35 to 64; peaks January to February |
| Head spa at home | 1108448595728308243 | Scalp care routine | "Head spa" and "scalp massage" +20% |
| Hair care ingredients | 1108448595728308245 | (same) | Rosemary water +400%, peptides +400% for women |
| Aftergrow Scalp Serum | 1108448595728308248 | (same) | Brand and product |

- The four postpartum pins (B01, B02, B04, B07) stay on `HOLD`. Their old board is now "Haircuts for thin hair", so postpartum would need a new board first, and that's George's call.
- F01 and G02 moved to Thinning hair, F05 to Hairstyles for thin hair, and G03 to Aftergrow Scalp Serum.
- **Demand gap.** The three biggest boards (haircuts, hairstyles, fine thin hair over 50) have one landing page between them, `make-hair-look-thicker`, which is capped at 8 pins. Line 4 asks George for three articles until they exist: best haircuts for thin hair, hairstyles for thinning hair, and fine thin hair over 50.

### Evidence as of Oct 11, 2026 (kept for the record)

Tailwind returns a search volume of 0 for all 32 of our saved keywords, so no tool here gives real volume numbers. The evidence below combines four sources:
- Pinterest's own trend report
- Pinterest topic pages, which exist only for searched topics
- Tailwind's keyword data, which scores buying intent for terms it recognizes
- what ranks today

| Board | Main searches | Evidence |
|---|---|---|
| Hair shedding explained | hair shedding, how much hair shedding is normal, telogen effluvium, hair shedding timeline | Pinterest topic pages exist for "hair shedding" and "hair shedding remedies". Tailwind recognizes "hair shedding". The top results today are small blogs, which is winnable. AAD covers the facts. |
| Postpartum hair care | postpartum hair shedding, postpartum hair care, postpartum hair loss (descriptions only) | There's a Pinterest topic page for "hairstyles for postpartum hair". "Postpartum hair care" scores 0.57 buying intent in Tailwind, among our highest. AAD has a dedicated page. |
| Scalp care routine | scalp care routine, how to apply scalp serum, scalp care vs hair care | Pinterest's Skinvested trend shows "scalp treatment aesthetic" +38% and "scalp scrub recipe" +31%. Tailwind recognizes "scalp care routine". |
| Hair care tips for women over 40 | hair care tips for women over 40 and 50, aging hair care, fine hair tips | There's a Pinterest topic page for "aging hair care". Renamed from "Hair care over 40", which Tailwind didn't recognize, to lead with the head phrase "hair care tips". |
| Hair care ingredients | rosemary for hair, peptides for hair, how to read ingredient labels, fragrance-free | Ingredient searches are the fastest-growing hair-care terms in Pinterest's 2026 report (rosemary water +269%). "Rosemary for hair" scores 0.62 in Tailwind, our second highest. |
| Healthy hair habits | healthy hair tips, how to brush shedding hair, heat styling for fine hair | Tailwind recognizes "healthy hair habits". Top-ranking pins in the niche tag #HealthyHairTips. |
| Hair progress photos | hair progress photos, 90 day hair routine | Renamed from the branded "The Aftergrow Check-in", which nobody searches. This has the weakest evidence of the 8. Judge it on our own data after 60 live days. |
| Aftergrow Scalp Serum | scalp serum, peptide scalp serum, fragrance-free scalp serum | "Scalp serum" has our highest buying-intent score in Tailwind (0.63). |

**Keyword bank for explore pins:** why is my hair shedding, hair shedding after stress, hair shedding 3 months later, how long does postpartum shedding last, scalp massage, wash day scalp care, fine hair tips, fragrance free hair care, peptides for hair, eucalyptus for scalp, rosemary water for hair (after the Journal article exists), hair care tips for women over 50.

## Backlog: ideas held until a page answers them

**Unlocked by Journal articles that already exist** (build them from the page map):
- A09 (shedding myths): `hair-shedding-vs-hair-loss`
- D03 and D07 (fuller-looking styling): `make-hair-look-thicker`
- F02 (wash-day habits): `oily-scalp-dry-hair`
- F04 (questions for a clinician): `scalp-serum-or-hair-supplement`
- The first rosemary pins: `scalp-serum-or-scalp-oil`

**Still held:**

| Ideas | The page they need |
|---|---|
| Postpartum cluster: B03, B05, B06 | A postpartum Journal article covering timing, baby hairs and a gentle routine, with "Pregnant or nursing? Ask your clinician first." The postpartum board has no page of its own yet. This is the most valuable page to write next. |
| Rosemary, full cluster | A dedicated Journal article on rosemary for hair: what it is, how it's used, its honest limits. Highest trend value (+269%). |
| C02 | A Journal article on scalp massage |
| D02 | A Journal article on how hair changes in your 40s and 50s |
| C06, F03 | Short answers on the FAQ page (morning or night, silk pillowcases) |
| G01 | A printable 90-day tracker PDF on the Month-Three Guide page |
| H01, C08 | A real product photo (never an invented label) |
| C05 | George's call on the word "detox" (banned in the brand book, rising on Pinterest) |

## Catalog pins (the Pinterest app for Shopify)

The Pinterest app for Shopify publishes product pins on its own, from the product's images, to the board "Products". On Oct 22, 2026 it published 6, one per image on the product page. Four of them break this file's quality gate:
- a "Month 0 / Month 3" hairline before-and-after
- "Clinically Tested" with 90/87/82% figures from a 31-person self-assessment
- "Fuller, thicker, denser-looking hair in as little as 6 weeks"
- a review quoting a "receding hairline", "hair coming back in thicker" and "holy grail"

These are the same claims flagged on Oct 11 as the likely cause of the spam block. **On Oct 23, 2026, with George's yes:**
- The 4 pins were deleted.
- The 4 images were detached from all three Shopify products. They're still in Shopify Files and can be re-attached.

Each run, check board "Products" with `list_board_pins` (board 1108448595728304895). If the app publishes a pin with a before-and-after, a percentage result, a timed result or a growth or regrowth claim, put it in line 4. Never delete catalog pins without George's yes.

## Never

- Never link a pin to a page about weight loss or weight-loss surgery (for example `/blogs/journal/hair-shedding-timeline-and-care`), even if the page is otherwise live. Pinterest bans weight-loss content in ads and treats it strictly in organic.
- Never route around a Pinterest block: no other domains, redirects or link shorteners, and don't post the link through other apps.
- Never schedule more than one canary at a time, and never outside `AP next-canary`.
- Never save one image to many boards on the same day.
- Never delete a published pin.
- Never invent proof, people or results.
- Never change the brand rules, the board names or George's site. Ask him in the report.

## The five-line report

1. **Mode and schedule:** live or blocked, and what was scheduled (how many, which dates). In blocked mode, say whether a canary is queued and when.
2. **What's working:** the top 3 pins by saves and by outbound clicks, with rates. Or "no readable pins yet".
3. **What was made:** new pins and variants, and why.
4. **Needs George:** appeal action, a page to build, a brand-word call. Or "nothing".
5. **Credits:** credits left (`get_account_usage`) and the next reset date. Also the plan (`list_subscriptions`): if it shows a pending cancellation, give the end date, and line 4 says "Tailwind is cancelled and ends <date>. Reactivate it or the autopilot stops scheduling."
