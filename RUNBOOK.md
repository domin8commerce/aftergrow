# Aftergrow Pinterest runbook

This repository runs Aftergrow's Pinterest without manual work. A Claude scheduled task follows this file every Monday and Thursday morning (US Eastern). George, the founder, makes the final calls and reads a five-line report after each run. Anything that needs his decision goes in line 4 of the report. Never guess on his behalf.

Pinterest account: **getaftergrow**. Tailwind account ID: **1658425**. Use no other account.

## What is here

| Path | What it is |
|---|---|
| `status.json` | The current mode: `live` (normal) or `blocked` (Pinterest is rejecting our links). **Read this first, every run.** |
| `queue.json` / `queue.csv` | Every pin: order, board, board ID, title, description, link (UTM tagged), alt text, status (`ready`, `scheduled`, `posted`), Tailwind post ID, history. The single source of truth. |
| `boards.json` | The 8 boards, their descriptions and Tailwind board IDs. |
| `pins/` | Finished pins, 2000 x 3000 PNG, served publicly so Tailwind can fetch them. |
| `engine/` | The pin engine (brand fonts, exact palette, The Part symbol, headless Chromium). `pinengine.py` and `batch2.py` hold 25 layouts. `queue_build.py` validates and orders the queue. `mark.py` records what Tailwind did. |
| `log.json` | Every scheduling, failure and pause, with times. |

## Start of every run

```
add_repo domin8commerce/aftergrow (push access), clone it, register it
cd aftergrow && (cd engine && npm install)      # brand fonts; Chromium is preinstalled
python3 -I engine/queue_build.py .              # must print "problems: none"
```

Then read `status.json`. If `mode` is `blocked`, do **Blocked mode** and stop there. If it is `live`, do **The weekly loop**.

## Blocked mode

Pinterest blocked getaftergrow.com as spam on the first pin (Oct 11, 2026). The domain was registered Sept 30, 2026. Brand-new claimed domains were hit by the same block in Sept and Oct 2026. Only George can appeal (it needs his Pinterest login). The form link is in `status.json`.

1. **Check the canaries.** For every row with `role: canary`, call Tailwind `get_post`.
   - `sent`: **the block is lifted.** Run `mark.py . posted <ID>`, set `mode` to `live` and `last_success_at` in `status.json`, then go to **Release**.
   - `failed` with a spam reason: run `mark.py . failed <ID> "<reason>"`. Still blocked.
   - `queued`: leave it.
2. **Keep exactly one canary in flight.** If no canary is queued in the future and fewer than 2 canary attempts happened in the last 7 days, schedule one. Pick the first `ready` pin in queue order whose link is a different page from the last failed canary. Use `create_post` with `useNextOpenSlot: true`, then run `mark.py . scheduled <ID> <postId> <sendAt> canary`.
3. **Never more than one canary queued.** Repeated blocked links look like spam to Pinterest and put the account at risk.
4. **Build inventory, don't schedule it.** If the ready queue holds fewer than 42 pins (14 days at 3 a day), make new pins with **Make** and the **Quality gate** below so the relaunch is strong.
5. **Report.** In line 4, say how many days the block has lasted. If it has been 7 or more days with no change, ask George to reply to Pinterest's email asking for a human review. Don't ask him to file a second appeal.

### Release (the run that finds the block lifted)

Schedule every `ready` pin in queue order with `create_post` (`useNextOpenSlot: true`, `boardId`, `title`, `description`, `url` = `link`, `altText`, `mediaUrl` = the `media_base` in `config.json` + `image`), **one call at a time** so slots fill in order. After each one, run `mark.py . scheduled <ID> <postId> <sendAt>`. Verify with `list_posts` (status `queued`). If the very next publish fails as spam again, go back to Blocked mode at once and delete the rest of the queue.

## The weekly loop (live mode)

1. **Health.** Call `list_posts` for `failed` and `missed` over the last 7 days.
   - A spam failure means: set `mode` to `blocked`, delete every queued post except the next one (it becomes the canary), mark them all `unscheduled`, and report.
   - Any other failure: fix the cause and reschedule.
   - Then call `list_posts` for `sent` and mark those pins `posted`, saving the Pinterest pin ID when the post shows one.
2. **Learn** (Mondays only, once 21+ pins have been live 21+ days). Pull `list_top_pins` with `contentType: ORGANIC`, last 90 days, three times: by `SAVE`, by `OUTBOUND_CLICK` and by `IMPRESSION`. Use `get_pin_analytics` for any pin you need full numbers on. Match pins to queue rows by `utm_content` in the link.
3. **Decide** with the rules in **The reload engine** below.
4. **Make** new pins (see **Make**). Each run stops at 10 new pins; quality beats volume.
5. **Quality gate** on every new pin. If a pin fails, it does not ship.
6. **Schedule.** Keep at least 14 days of pins queued at the current pace. Scheduling works the same as Release.
7. **Commit and push** `queue.json`, `queue.csv`, `status.json`, `log.json`, `pins/` and `engine/`.
8. **Report** to George in five lines (format at the bottom).

## The reload engine: what keeps the machine fed, and why

### What the data says (and what we do about it)

- **Pinterest is a hits business.** In Tailwind's 2025 study of about 1.2 million Pins from 17,000+ accounts, the top 1% of Pins drove over 50% of impressions and clicks on Pins from the last 90 days. The bottom 80% drove under 10%. **So we find the few winners and multiply them.** We don't spread effort evenly.
- **Fresh designs drive the traffic.** In the same study, over 90% of traffic to brand websites came from original Pins (Creates), not re-saves. **So spare credits go to new designs of proven ideas, not to re-pinning one image to many boards.**
- **Pins compound slowly.** Winning Pins in that study averaged 18 new saves when under 90 days old, 44 at 90 days to 1 year, and 68 at 1 to 2 years. Engagement peaked between years one and two. **So we judge early pins on rates, not totals, and we never delete a published pin for underperforming.**
- **Pace.** Tailwind's guidance is 3 to 5 Pins a day for new accounts and 5 to 10 after 6 months, with 3 to 5 different designs per URL, each aimed at a different keyword.

### Decision rules

- **Readable pin:** at least 500 impressions, or live at least 30 days. Only judge readable pins.
- **Save rate** = saves / impressions. **Outbound click rate** = outbound clicks / impressions.
- **Winner:** a readable pin in the top 20% by save rate or by outbound click rate, with at least 3 saves or 3 outbound clicks. (Below that floor it's luck.)
- **Each winner gets 3 fresh variants** over the next 2 weeks, never more than 2 variants of one pin in any 7 days.
- **Board review every 4 weeks:**
  - A board with 15+ readable pins and zero saves gets no new pins for 4 weeks. Its share moves to the best board.
  - A board whose save rate is at least 1.5 times the account median gets 1 extra pin in every 10.
- **70 / 30.** 70% of new pins exploit: variants of winners and the best boards. 30% explore: new keywords from the bank below, new layouts, trend tests.
- **Before there is data** (first 30 live days): ship the planned queue, plus keyword-coverage variants (3 to 5 designs per landing page, each for a different keyword).

### Variant recipe

- **Keep:** the landing page (same URL, new `utm_content` ID such as `A01b`), the facts and the board.
- **Change at least 3 of:** the headline angle (a new long-tail keyword in the first 40 characters of the title), the layout, the field color, the hook type (number, question, myth vs. fact, checklist, timeline), and the title and description wording.
- **Never** ship a recolor of the same headline. Tailwind warns against many near-identical Pins in one week.

### Trend layer (first run of each month)

- Check Pinterest's newsroom for new trend reports and Pinterest Predicts. Add up to 4 explore pins for rising terms that fit our boards and our fact sheet.
- **Current openings.** Pinterest's Beauty Trend Report, published Oct 6, 2026, lists these increases. Pinterest does not state the market or the comparison period.
  - "rosemary water for hair" +269%
  - "aloe vera for hair mask" +80%
  - "coconut oil for hair benefits" +42%
  - "scalp treatment aesthetic" +38%
  - "scalp scrub recipe" +31%
  - "scalp detox" +21%
- **Rosemary is in our formula.** The rosemary cluster is the biggest open trend we can honestly own, but it needs a Journal article first (see Backlog).
- **"Treatment" and "detox" are banned by the brand book.** Only George can change that.
- **Seasonal.** Publish 45 to 60 days before the moment, per Tailwind's guidance:
  - New Year hair routine: from mid-November.
  - Postpartum push before Mother's Day: from mid-March.
  - Back-to-routine September: from mid-July.
- The pack's claims that postpartum searches peak in January and scalp care rises in late summer are **not verified**. Test them against our own data before acting on them.

### Pace and credits

The Tailwind plan gives 300 credits a month. One credit is one pin to one board. The next reset is Nov 10, 2026. Plan as if unused credits do not carry over. Deleting a queued post does not refund its credit.

| Phase | Pins a day | Credits a month | Share of plan |
|---|---|---|---|
| Launch, first 30 live days | 3 | ~91 | 30% |
| After 30 live days, if save rate holds and 14 days are queued | 5 | ~152 | 51% |
| After 6 months | 8 to 10 | ~243 to 300 | 81 to 100% |

- **To raise the pace,** add timeslots with `create_timeslot` (afternoons and evenings, never two within an hour), then schedule more.
- **Re-saves** (`intervalBoards`) are allowed only for proven winners, to the second most relevant board, 7+ days apart. They get at most 10% of monthly credits.
- **Monthly board audit:** spend 1 credit per board on `get_board_keyword_relevance` for its main keyword, once boards have 10+ pins.

### Landing pages are the fuel

Every pin needs a page that answers it. Today 7 live pages carry all 34 pins. Each new Journal article opens a new keyword cluster and 5 to 10 new pins. **When the planned queue and the variants run low, the bottleneck is pages, not pins.** Ask George for the next article from the Backlog in line 4 of the report.

## Make

- **New designs** go in a new file `engine/batchN.py` (N = 3, 4, ...). Copy the header and the `__main__` block of `engine/batch2.py`, and `import batch2` so all 25 layouts are available.
- **The file defines** `PINS` (designs, same format as `batch2.PINS`) and `COPY`, a list of rows `(id, slug, board, title, description, link, alt)`. Import `L` and the board and page constants from `queue_build`.
- **Render** with `python3 -I engine/batchN.py pins <IDs>`, then run `python3 -I engine/queue_build.py .`. It finds the new batch, validates it and orders the ready queue.
- **Start from a working pin.** Each layout has its own fields, so copy the dict of a pin that already uses the layout and change the text. Never invent field names.

| Layout | Copy from |
|---|---|
| timeline | A01 |
| ledger | E02 |
| viewfinder | G02 |
| checklist | A03, A10 |
| contrast | E06 |
| swap | D04 |
| cycle | A04 |
| list | B04 |
| steps | C01 |
| strand | F01 |
| bignum | A02 |
| definition | A05 |
| list2 | A06, A07, D01, D06, F05 |
| ruler | A08 |
| curve | B01 |
| split | B02, C04 |
| frames | B07 |
| parts | C03 |
| grid4 | C07, E04 |
| schedule | D05 |
| ledger2 | E01, E03, H02 |
| label | E05 |
| grid6 | E07 |
| weekline | G03 |
| protocol | H03 |

The first ten layouts live in `pinengine.py`. The rest live in `batch2.py`.
- **Fields:** `butter`, `espresso`, `white` and `porcelain`. Use `<br>` for deliberate line breaks and `&nbsp;` to keep "6&nbsp;months" together.

## Quality gate (every new pin, before it is pushed)

- **Look at it twice:** full size, and at 236 px wide. The headline must read at feed size.
- **Every word on the image matches the copy.** No line ends with a single stranded word.
- **Banned anywhere:** weight loss, diet, slim, before and after, regrow, stop or prevent hair loss, cure, treat (and treatment), clinically proven, miracle, holy grail, detox, game-changer, any drug name or drug class, GLP-1, em dashes, exclamation marks, emoji, all caps. "Hair loss" may appear in descriptions only.
- **Claims and proof:** cosmetic claims only, and only facts from the **Fact sheet** below. No review counts, ratings, customer numbers, before and after, or AI people as customers.
- **Title:** under 100 characters, with the keyword in the first 40.
- **Description:** 150 to 280 characters, keyword in the first sentence, a soft call to action.
- **Alt text:** describes the image.
- **Links:** only pages in `LIVE_PAGES` in `engine/queue_build.py`. Before adding a page, fetch it and confirm it loads with real content.
- `queue_build.py` must print `problems: none`.

## Fact sheet (checked Oct 11, 2026; pins may state only these)

- **American Academy of Dermatology**, "Do you have hair loss or hair shedding?":
  - "It's normal to shed between 50 and 100 hairs a day."
  - Excessive shedding is noticed "a few months after the stressful event."
  - "Within six to nine months, the hair tends to regain its normal fullness."
  - The medical term is telogen effluvium.
  - Triggers include giving birth, high fever, an operation, recovering from an illness, lots of stress and stopping birth-control pills. (AAD also lists losing 20 pounds or more. Pins never say that.)
- **American Academy of Dermatology**, "Hair loss in new moms":
  - "Hair shedding usually peaks about four months after giving birth."
  - "Most women see their hair return to its normal fullness by their child's first birthday."
- **getaftergrow.com/pages/how-it-works:**
  - Hair often sheds "two to four months after a big change in the body."
  - For most people it "settles on its own within six to nine months."
  - Each hair "rests for about three months before it falls out."
  - "If shedding is still heavy after six months, see a dermatologist."
- **getaftergrow.com product and ingredients pages:**
  - Five peptides and six plant extracts: eucalyptus, soybean germ, wheat germ, scutellaria root, rosemary, saw palmetto.
  - Water-based and fragrance-free (no ingredient added just for scent). Contains soy and wheat.
  - Directions: "Apply a few drops to a clean, dry scalp. Massage for 1 to 2 minutes. Do not rinse. Use once a day."
  - Subscription: $108 for 3 bottles every 3 months, free shipping, skip or cancel anytime.
  - Refund on the first order.

## Boards and the evidence behind them (checked Oct 11, 2026)

Tailwind returns a search volume of 0 for all 32 of our saved keywords, so no tool here gives real volume numbers. The evidence below combines four sources:
- Pinterest's own trend report
- Pinterest topic pages, which exist only for searched topics
- Tailwind's keyword data, which scores buying intent for terms it recognizes
- a look at what ranks today

| Board | Main searches | Evidence |
|---|---|---|
| Hair shedding explained | hair shedding, how much hair shedding is normal, telogen effluvium, hair shedding timeline | Pinterest topic pages exist for "hair shedding" and "hair shedding remedies". Tailwind recognizes "hair shedding". The top results today are small blogs, which is winnable. AAD covers the facts. |
| Postpartum hair care | postpartum hair shedding, postpartum hair care, postpartum hair loss (descriptions only) | Pinterest topic page "hairstyles for postpartum hair". "Postpartum hair care" scores 0.57 buying intent in Tailwind, among our highest. AAD has a dedicated page. |
| Scalp care routine | scalp care routine, how to apply scalp serum, scalp care vs hair care | Pinterest's Skinvested trend: "scalp treatment aesthetic" +38%, "scalp scrub recipe" +31%. Tailwind recognizes "scalp care routine". |
| Hair care tips for women over 40 | hair care tips for women over 40 and 50, aging hair care, fine hair tips | Pinterest topic page "aging hair care". Renamed from "Hair care over 40", which Tailwind did not recognize, to lead with the head phrase "hair care tips". |
| Hair care ingredients | rosemary for hair, peptides for hair, how to read ingredient labels, fragrance-free | Ingredient searches are the fastest-growing hair-care terms in Pinterest's 2026 report (rosemary water +269%). "Rosemary for hair" scores 0.62 in Tailwind, our second highest. |
| Healthy hair habits | healthy hair tips, how to brush shedding hair, heat styling for fine hair | Tailwind recognizes "healthy hair habits". Top-ranking pins in the niche tag #HealthyHairTips. |
| Hair progress photos | hair progress photos, 90 day hair routine | Renamed from the branded "The Aftergrow Check-in", which nobody searches. This has the weakest evidence of the 8. Judge it on our own data after 60 live days. |
| Aftergrow Scalp Serum | scalp serum, peptide scalp serum, fragrance-free scalp serum | "Scalp serum" has our highest buying-intent score in Tailwind (0.63). |

**Keyword bank for explore pins:** why is my hair shedding, hair shedding after stress, hair shedding 3 months later, how long does postpartum shedding last, scalp massage, wash day scalp care, fine hair tips, fragrance free hair care, peptides for hair, eucalyptus for scalp, rosemary water for hair (after the Journal article exists), hair care tips for women over 50.

## Backlog: ideas held until a page answers them

| Ideas | The page they need |
|---|---|
| Rosemary cluster (4 to 6 pins) | A Journal article: rosemary for hair, what it is, how it is used, honest limits. Highest-value page to build (+269% trend). |
| A09, C06, F03 | Short answers on the FAQ page (myths, morning or night, silk pillowcases) |
| B03, B05, B06 | A postpartum Journal article (timing, baby hairs, a gentle routine with "Pregnant or nursing? Ask your clinician first.") |
| C02, F02 | A Journal article on scalp massage and wash-day scalp care |
| D02, D03, D07 | A Journal article on hair changes after 40 and styling for fuller-looking hair |
| F04 | A Journal article on nutrition questions to ask a clinician |
| G01 | A printable 90-day tracker PDF on the Month-Three Guide page |
| H01, C08 | A real product photo (never an invented label) |
| C05 | George's call on the word "detox" (banned in the brand book, rising on Pinterest) |

## Never

- Never route around a Pinterest block: no other domains, redirects, link shorteners, or posting the link through other apps.
- Never save one image to many boards on the same day.
- Never delete a published pin.
- Never invent proof, people or results.
- Never change the brand rules, the boards' names or George's site. Ask him in the report.

## The five-line report

1. **Mode and schedule:** live or blocked, what was scheduled (how many, which dates).
2. **What's working:** top 3 pins by saves and by outbound clicks, with rates, or "no readable pins yet".
3. **What was made:** new pins and variants, and why.
4. **Needs George:** appeal status, a page to build, a brand-word call. Or "nothing".
5. **Credits:** credits left and the next reset date.
