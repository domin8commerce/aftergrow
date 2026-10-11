# Aftergrow Pinterest runbook

This repository runs Aftergrow's Pinterest without manual work. A Claude scheduled task follows this file every Monday and Thursday at 8:47 AM Eastern. George, the founder, makes the final calls and reads a five-line report after each run. Anything that needs his decision goes in line 4 of the report. Never guess on his behalf.

Pinterest account: **getaftergrow**. Tailwind account ID: **1658425**. Use no other account.

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

- **Check for new reports.** Look at Pinterest's newsroom for new trend reports and Pinterest Predicts. Add up to 4 explore pins for rising terms that fit our boards and our fact sheet.
- **Current openings.** Pinterest's Beauty Trend Report, published Oct 6, 2026, lists these increases. Pinterest doesn't state the market or the comparison period.
  - "rosemary water for hair" +269%
  - "aloe vera for hair mask" +80%
  - "coconut oil for hair benefits" +42%
  - "scalp treatment aesthetic" +38%
  - "scalp scrub recipe" +31%
  - "scalp detox" +21%
- **Rosemary.** It's in our formula, so the rosemary cluster is the biggest open trend we can honestly own. It needs a Journal article first (see Backlog).
- **Banned words.** The brand book bans "treatment" and "detox". Only George can change that.
- **Seasonal.** Publish 45 to 60 days before the moment, per Tailwind's guidance:
  - New Year hair routine: from mid-November.
  - Postpartum push before Mother's Day: from mid-March.
  - Back-to-routine September: from mid-July.
- The pack claims postpartum searches peak in January and scalp care rises in late summer. **That isn't verified.** Test it against our own data before acting on it.

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

Every pin needs a page that answers it. Today 7 live pages carry all 34 pins, and `queue_build.py` caps each page at 8 pins. Each new Journal article opens a new keyword cluster and 5 to 10 new pins. **When the planned queue and the variants run low, the bottleneck is pages, not pins.** Ask George for the next article from the Backlog in line 4 of the report.

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

## Fact sheet (checked Oct 11, 2026; pins may state only these)

- **American Academy of Dermatology**, "Do you have hair loss or hair shedding?":
  - "It's normal to shed between 50 and 100 hairs a day."
  - Excessive shedding is noticed "a few months after the stressful event."
  - "Within six to nine months, the hair tends to regain its normal fullness."
  - The medical term is telogen effluvium.
  - Triggers include giving birth, high fever, an operation, recovering from an illness, lots of stress and stopping birth-control pills. AAD also lists losing 20 pounds or more; pins never say that.
- **American Academy of Dermatology**, "Hair loss in new moms":
  - "Hair shedding usually peaks about four months after giving birth."
  - "Most women see their hair return to its normal fullness by their child's first birthday."
- **/pages/how-it-works:**
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

## Boards and the evidence behind them (checked Oct 11, 2026)

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

| Ideas | The page they need |
|---|---|
| Rosemary cluster (4 to 6 pins) | A Journal article on rosemary for hair: what it is, how it's used, its honest limits. This is the highest-value page to build (+269% trend). |
| A09, C06, F03 | Short answers on the FAQ page (myths, morning or night, silk pillowcases) |
| B03, B05, B06 | A postpartum Journal article covering timing, baby hairs and a gentle routine, with "Pregnant or nursing? Ask your clinician first." |
| C02, F02 | A Journal article on scalp massage and wash-day scalp care |
| D02, D03, D07 | A Journal article on hair changes after 40 and styling for fuller-looking hair |
| F04 | A Journal article on nutrition questions to ask a clinician |
| G01 | A printable 90-day tracker PDF on the Month-Three Guide page |
| H01, C08 | A real product photo (never an invented label) |
| C05 | George's call on the word "detox" (banned in the brand book, rising on Pinterest) |

## Never

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
5. **Credits:** credits left (`get_account_usage`) and the next reset date.
