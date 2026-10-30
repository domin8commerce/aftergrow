# Aftergrow Pinterest ads: build log and check runbook

Ad account 549770879093 (USD). Both campaigns launched on George's go:
- Campaign A launched Oct 29, 2026, at 8:07 PM ET (Oct 30, 00:07 UTC).
- Campaign B launched Oct 29, 2026, at 8:45 PM ET (Oct 30, 00:45 UTC).
- Campaign C launched Oct 30, 2026, at 7:37 AM ET (11:37 UTC).

Checks are manual, as George chose on Oct 29 (he declined a scheduled task). When George asks for a check, follow "The check" below and add an entry to "Check log" at the bottom. The planned rhythm is Tuesday and Friday.

## State of the account
- **Campaign A (Search lab), 626760182006:** ACTIVE at $5/day.
- **Campaign B (Buyer hunt), 626760182396:** ACTIVE at $10/day.
- **Campaign C (Retargeting), 626760186484:** ACTIVE at $3/day. It only delivers once its audiences have enough matched people.
- **Total Pinterest spend:** $18/day, the cap in the plan. Anything above that needs George's yes.
- **Paused:** the three older campaigns, which George paused on Oct 29:
  - Sponsored Product | Test | Oct 2026 (626760143882)
  - Consideration Pins Campaign | Boosted Pins Batch 1 (626760180766)
  - the automated campaign (626760180755)
- **Serum color:** George confirmed on Oct 29 that the real serum is amber/golden, like the video, so the video ads stay in.

## Campaign A: Search lab
- **Campaign** 626760182006 "AG | A | Search lab | Consideration":
  - objective Consideration;
  - campaign budget $5/day (this account requires campaign budget optimization);
  - standard campaign, not Performance+.
- **Ad group** 2680092807543 "A1 | Women 35-65+ | Product keywords | Search":
  - search placement only;
  - US, English, women 35-65+, all devices;
  - automatic targeting off;
  - automatic bid, billed per click, standard pacing.
- **Keywords** (72): 29 phrase, 4 exact and 39 phrase negatives.
  - Phrase: thin hair products, products for thin hair, hair products for thin hair, best products for thin hair, thin fine hair, fine thin hair products, hair products for fine thin hair, fine hair products, volumizing products for fine hair, hair thickening products, hair thickening serum, thickening serum, hair serum for thin hair, hair serum for fine hair, scalp serum, scalp serum for thin hair, peptide serum for hair, peptide hair serum, lightweight hair serum, leave in scalp serum, scalp care products, scalp care routine, fragrance free hair products, head spa at home, how to make thin hair look thicker, how to make fine hair look fuller, fuller looking hair, fine thin hair over 50, hair care over 50.
  - Exact: thin hair products, scalp serum, hair thickening products, products for thin hair.
  - Negatives: men, mens, male, beard, boys, kids, toddler, baby, diy, recipe, homemade, wig, wigs, extensions, topper, braids, dog, cat, thick hair, long hair, weight loss, ozempic, glp-1, wegovy, mounjaro, minoxidil, rogaine, finasteride, transplant, prp, chemo, drawing, anime, tattoo, hair loss, alopecia, regrowth, regrow, postpartum.

### Ads (A)
| Ad ID | Name | Pin ID | Creative | utm_content | Organic link on the pin |
|---|---|---|---|---|---|
| 687322854477 | A1 \| VR02 \| Daily step \| 1:1 | 1108448527072618492 | 1500x1500 image, "A scalp serum. A daily step." | vr02 | /products/scalp-serum |
| 687322854478 | A1 \| VR09 \| Formula \| 1:1 | 1108448527072618494 | 1500x1500 image, "The formula deserves a closer read." | vr09 | /blogs/journal/how-to-read-a-scalp-serum-label |
| 687322854479 | A1 \| VIDEO01 \| Dropper 15s \| 9:16 | 1108448527072618581 | 15-second Runway video: dropper macro, ending on the label | video01 | /blogs/journal/what-to-look-for-in-a-scalp-serum |

- **Paid destination:** `https://getaftergrow.com/products/scalp-serum?utm_source=pinterest&utm_medium=paid_social&utm_campaign=search-lab&utm_content=<vr02|vr09|video01>`
- **Creative files:** ads/pinterest/search-lab/ in this repo.

## Campaign B: Buyer hunt
- **Campaign** 626760182396 "AG | B | Buyer hunt | Sales":
  - objective Sales (`SALES`, standard ad, not catalog, not Performance+);
  - campaign budget $10/day.
- **Ad group** 2680092808018 "B1 | Women 35-65+ | Hair interests + expanded | All placements":
  - optimized for **Checkout** on conversion tag 2614320036145;
  - automatic bid, billed per 1,000 impressions;
  - all placements, all devices;
  - US, English, women 35-65+;
  - interests as a starting hint: Hair Care, Hair Products, Hair Maintenance, Hair Oil;
  - expanded targeting on (`auto_targeting_enabled`), so Pinterest can widen beyond the hint.
  - No keywords. No purchaser exclusion: there are no audiences, and the store has one customer.
- **Why B starts blind:** Pinterest has never received a Checkout event from the store, because nothing has sold since the tag was installed. B starts with no purchase history to learn from. Judge it at the kill line, not in week one.

### Ads (B)
| Ad ID | Name | Pin ID | Creative | utm_content | Lands on |
|---|---|---|---|---|---|
| 687322855849 | B1 \| Heavy isn't the brief \| 9:16 | 1108448527072600098 | "Heavy isn't the brief." Cast-iron dropper next to the bottle. Existing pin on George's "Hair Scalp Serum" board | heavy | product page |
| 687322855850 | B1 \| Rinse step \| 9:16 | 1108448527072584503 | "The rinse step? Not in these directions." Routine icons. Existing pin, approved once as an ad in the paused Boosted campaign | rinse | product page |
| 687322855851 | B1 \| VIDEO01 \| Dropper 15s \| 9:16 | 1108448527072618581 | Same video pin as A | video01 | product page |
| 687322855902 | B1 \| Offer \| 90-Day Protocol \| 2:3 | 1108448527072620974 | New offer pin: "Three bottles. Ninety days. $36 a bottle, free shipping. Skip or cancel anytime." Fine print: "Renews at $108 every 3 months until canceled." | offer90 | product page with `?plan=autorefill`, which preselects the Protocol |

- **Paid destination:** `https://getaftergrow.com/products/scalp-serum?utm_source=pinterest&utm_medium=paid_social&utm_campaign=buyer-hunt&utm_content=<heavy|rinse|video01|offer90>`. The offer ad adds `plan=autorefill`.
- **Offer pin:**
  - Rendered by ads/pinterest/buyer-hunt/render_offer.py with the brand font, from the Drive photo "Aftergrow Scalp Serum Trio (1).png".
  - Facts checked against the live product and subscription pages on Oct 29: $108 for 3 bottles, $36 a bottle, $1.20 a day, free US shipping, skip or cancel anytime, renews every 3 months until canceled.
  - The guarantee wording on the site is inconsistent: "90 days" on the homepage, while the FAQ says "email within 120 days of delivery" and only the first order is refunded. The image leaves the guarantee out. The pin description uses the site's own sentence: "Your first order is covered by the 90-Day Guarantee."
- **Why these creatives (George approved, Oct 29):**
  - "Heavy isn't the brief" goes straight at the objection women with fine hair have to oils (they weigh hair down) and sets Aftergrow apart from rosemary oil.
  - The rinse-step pin answers the effort objection.
  - The video is the strongest motion asset for the home feed.
  - The offer ad is the only one that sells the $108 Protocol.
- **Not used:**
  - VR02 and VR09: already in A.
  - AG IMAGES: before/afters, "Hormones Stole My Hair", "Calling all GLP-1 users", AI women and AI hair.
  - "Silver belongs in the picture" (AI woman) and VR07 (AI hand).
  - The two Agent videos: product-only.
  - The hands B-roll George mentioned is not in the Drive.
  - The other VR and Pinterest images are kept as backups.

## Campaign C: Retargeting
- **Campaign** 626760186484 "AG | C | Retargeting | Consideration":
  - objective Consideration;
  - campaign budget $3/day;
  - standard campaign, not Performance+.
- **Ad group** 2680092815578 "C1 | Site visitors 60d + cart 180d + pin engagers | purchasers excluded | All placements":
  - billed per click, automatic bid, all placements;
  - expanded targeting off;
  - US and English only, with no age or gender limits, because the audience already defines who sees it.
- **Audiences** (created Oct 30 with `prefill: true`, which backfills from past tag data; status INITIALIZING at launch):

  | Audience | ID | Rule | Use |
  |---|---|---|---|
  | AG \| Site visitors 60d | 2542623641406 | tag pagevisit, 60 days | include |
  | AG \| Add to cart 180d | 2542623641408 | tag addtocart, 180 days | include |
  | AG \| Pin engagers | 2542623641410 | anyone who engaged with getaftergrow.com pins | include |
  | AG \| Purchasers 180d (exclude) | 2542623641409 | tag checkout, 180 days | exclude |

  - Pin engagers is an addition to the plan. Every one of them is a Pinterest user, so it fills C faster than site visitors alone, most of whom came from Meta, TikTok and direct traffic.
  - The plan also called for checkout starters, but the API's audience events don't include InitiateCheckout. Anyone who started checkout added to cart first, so the cart audience covers them.
  - API format that works: `{"visitor_source_id": "2614320036145", "retention_days": 60, "event": "pagevisit", "prefill": true}`. The ID must be a string, not a list. Engagement audiences reject `retention_days`.

### Ads (C)
| Ad ID | Name | Pin ID | Creative | utm_content | Lands on |
|---|---|---|---|---|---|
| 687322899212 | C1 \| R1 Guarantee \| 2:3 | 1108448527072652806 | New pin: "Ninety days to decide. Don't love how your hair looks? We refund your first order." Fine print: claim within 120 days of delivery, shipping not refunded, one per customer | guarantee | product page |
| 687322899213 | C1 \| R2 Offer 90-Day Protocol \| 2:3 | 1108448527072620974 | Same offer pin as B | offer90 | product page with `?plan=autorefill` |

- **Paid destination:** `https://getaftergrow.com/products/scalp-serum?utm_source=pinterest&utm_medium=paid_social&utm_campaign=retargeting&utm_content=<guarantee|offer90>`. R2 adds `plan=autorefill`.
- **R1 copy:** checked against /pages/the-90-day-guarantee on Oct 30. The headline is the page's own ("Ninety days to decide.").
  - The image is rendered by ads/pinterest/retargeting/render_guarantee.py from the Runway video's cover frame.
  - The organic link on the pin goes to the guarantee page.

## Pins and creative rules
- New pins go on the board "Aftergrow Scalp Serum" (1108448595728308248), with Pinterest's "AI modified" disclosure.
- Organic links use `utm_source=pinterest&utm_medium=social&utm_campaign=organic&utm_content=<id>`. A saved ad sends people to the organic link, so earned traffic counts as organic.
- No AI people or AI "after" hair. No weight-loss, GLP-1 or hormone language. No before/afters. No fear questions.

## Paid vs organic in Shopify (no developer needed)
| Traffic | utm_source | utm_medium |
|---|---|---|
| Paid Pinterest ads (A and B) | pinterest | paid_social |
| Organic pins (the autopilot and the pins above) | pinterest | social |
| Pinterest app catalog ads | Pinterest | PaidSocial (campaign ID in utm_campaign, ad group ID in utm_content) |

ShopifyQL, tested on Oct 29:

```
FROM sessions SHOW sessions, sessions_with_cart_additions, sessions_that_completed_checkout
WHERE utm_source = 'pinterest' OR utm_source = 'Pinterest'
GROUP BY utm_source, utm_medium, utm_campaign, utm_content SINCE -30d UNTIL today ORDER BY sessions DESC
```

## API notes
- **Composio:** the pinterest_ads proxy takes paths without `/v5`. The PINTEREST_ADS_LIST_CAMPAIGNS tool returns empty, so use a raw GET.
- **Budgets:** ad group budgets fail with error 2454. Use a campaign budget, and set the ad group's budget_type to CBO_ADGROUP.
- **Outbound clicks:** the API has no outbound-click optimization field. Direct links are on, so paid clicks land on the site.
- **Sales campaigns:** use `objective_type` SALES with `intended_promotion_type` STANDARD_AD. In the ad group, set billable_event IMPRESSION and `optimization_goal_metadata.conversion_tag_v3_goal_metadata` = {conversion_event: CHECKOUT, conversion_tag_id: 2614320036145}.
- **Interest IDs:**

  | Interest | ID |
  |---|---|
  | Hair | 903411883690 |
  | Hair Care | 906530425452 |
  | Hair Products | 926154720595 |
  | Hair Maintenance | 933467251433 |
  | Hair Oil | 927576809326 |
  | Hair Spray | 918638206733 |

  Look up others with `GET /resources/targeting/interests/{id}`.
- **Pins:**
  - Image pins: PINTEREST_CREATE_PIN with an image_url.
  - Video pins, in order:
    1. Run PINTEREST_REGISTER_MEDIA.
    2. POST the file as multipart to the S3 upload_url (returns 204).
    3. Poll PINTEREST_GET_MEDIA until it says "succeeded".
    4. Run PINTEREST_CREATE_PIN with video_id and cover_image_url.
- **Ads:**
  - POST /ad_accounts/{id}/ads accepts a destination_url that differs from the pin link.
  - The same pin can run in several campaigns.
  - grid_click_type is read-only and comes back as DIRECT_TO_DESTINATION.
- **Keywords:** POST /ad_accounts/{id}/keywords with {"parent_id": ad group, "keywords": [{match_type, value}]}.
- **Getting images out of George's Drive:** the Drive is not public and the sandbox can't reach Drive, Shopify's CDN or i.pinimg.com.
  1. Open `https://drive.google.com/u/0/drive-usercontent/<FILE_ID>=w2400-k-rw-v1-nu?auditContext=thumbnail` in a new Chrome tab.
  2. Fit the image to the window.
  3. Capture it with the Chrome `zoom` action and `save_to_disk`.

## The check (Tuesday and Friday)
All Pinterest calls go through `COMPOSIO_REMOTE_WORKBENCH`, using `proxy_execute(method, endpoint, "pinterest_ads", query_params=..., body=...)`.

1. **Status.**
   - `GET /ad_accounts/549770879093/campaigns` (page_size 50).
   - `GET /ad_accounts/549770879093/ads` with `campaign_ids=626760182006,626760182396,626760186484`: review_status and rejected_reasons for each ad.
   - `GET /ad_accounts/549770879093/audiences`: the status and size of C's audiences. C can't deliver until they're READY with enough matched people (roughly 100 or more).
2. **Numbers since launch, and for the last 7 days.**
   - Call `GET /ad_accounts/549770879093/ads/analytics` with:
     - `ad_ids` = the nine ad IDs above;
     - `granularity=TOTAL`, or `DAY` for spend per day;
     - `start_date` no earlier than 2026-10-29.
   - Columns: `SPEND_IN_DOLLAR,PAID_IMPRESSION,CLICKTHROUGH_1,OUTBOUND_CLICK_1,CTR,OUTBOUND_CTR_1,ECPC_IN_DOLLAR,COST_PER_OUTBOUND_CLICK_IN_DOLLAR,TOTAL_PAGE_VISIT,TOTAL_CHECKOUT,TOTAL_CHECKOUT_VALUE_IN_MICRO_DOLLAR`.
   - Campaign totals: `GET /ad_accounts/549770879093/campaigns/analytics` with `campaign_ids`.
   - An empty list means there is no delivery yet.
3. **Keywords (A only).**
   - Call `GET /ad_accounts/549770879093/ad_groups/targeting_analytics` with `ad_group_ids=2680092807543`, `targeting_types=KEYWORD` and `granularity=TOTAL`.
   - Columns: `SPEND_IN_DOLLAR,PAID_IMPRESSION,CLICKTHROUGH_1,OUTBOUND_CLICK_1,CTR`.
   - Search terms are only in Ads Manager.
4. **Shopify, the source of truth for orders.** Run this with `run-analytics-query`:
   `FROM sessions SHOW sessions, sessions_with_cart_additions, sessions_that_reached_checkout, sessions_that_completed_checkout WHERE utm_medium = 'paid_social' AND utm_source = 'pinterest' GROUP BY utm_campaign, utm_content SINCE 2026-10-29 UNTIL today`
5. **Product page.** Check that https://getaftergrow.com/products/scalp-serum loads, using WebFetch.

### What a check may do without asking
Only an emergency pause of the affected campaign, sent as `PATCH /ad_accounts/549770879093/campaigns` with `[{"id":"<campaign id>","status":"PAUSED"}]`. Pause when:
- the product page doesn't load;
- one day's spend is over 2x the campaign's budget ($10 for A, $20 for B, $6 for C);
- Pinterest reports a domain or spam block;
- an ad's destination URL has changed.

Say so at the top of the report.

### What needs George's yes
Propose these with a one-word reply. Never do them unasked.
- Changing a budget, a bid or targeting.
- Pausing or adding ads, keywords or negatives.
- Starting any other campaign.
- Changing pins or the website.

### Decision rules
- **Until Nov 13 (the first 14 days): no performance changes.** Report only. A rejected ad is the exception: report the reason and propose the fix.
  - Backups for A: VR08 and VR14.
  - Backups for B: "A lightweight peptide serum for fuller-looking hair" (pin 1108448527072599991), VR04 and VR10.
- **From Nov 13: one change round a week, on Friday.**
  - Ads: once an ad has about 10,000 paid impressions, propose pausing it if its CTR is under half the best ad's.
  - A's keywords: propose archiving any keyword that has spent $5 or more with zero outbound clicks.
  - A's clicks: if the average cost per click is above $1.20 for 14 days, flag it. New creative is the first fix.
- **Kill lines** (zero Shopify purchases from that utm_campaign):
  - A: $105 spent, which is 3x a $35 target.
  - B: $120 spent, which is 3x the $40 blended target.
  - C: $60 spent. Retargeting should buy cheaper than prospecting, so its line is lower.
  - C's audiences: if they're still too small to deliver on Nov 6, report it and propose shifting C's $3 into B.
  - When a campaign hits its line, wait one more week for late buyers, then propose a rebuild or a kill.
- **Scale:** only after 10 purchases at or under target, and not before Dec 26. Propose a 20-30% budget step, or a duplicate at the higher budget.
- **B's protocol share:** track it alongside cost per order. A Protocol order ($108) pays back at about twice the cost per order of a single bottle.

### Report (five lines, plain English; George scans)
1. **Status:** campaign and ad status, review results, and any emergency action.
2. **Numbers:** for each campaign, since launch and over the last 7 days: spend, impressions, clicks, CTR, CPC and outbound clicks. Name the best and worst ad. Add Shopify paid sessions, add to carts, checkouts and orders.
3. **Keywords (A):** the top keywords by clicks, and the keywords spending with no clicks.
4. **Needs George:** each decision as a one-word reply, or "nothing".
5. **Next check:** the date, and what it will look at.

## Check log
(Each check adds one dated entry with spend to date, impressions, clicks, CTR, CPC, Shopify orders, actions taken and decisions asked.)

- 2026-10-29: A launched. 3 ads pending review. $0 spent.
- 2026-10-29: B launched. 4 ads pending review. $0 spent. Total Pinterest spend is now $15/day.
- 2026-10-30, 7:40 AM ET:
  - All 7 ads in A and B are APPROVED.
  - C launched with 2 ads pending review and 4 audiences INITIALIZING. Total Pinterest spend is now $18/day.
  - First delivery, B only: $3.24, 196 impressions, 1 outbound click.
    - Heavy: 120 impressions, 1 click.
    - Rinse: 48 impressions.
    - Offer: 24 impressions.
    - Video: 4 impressions.
  - A: no delivery reported yet. Too early to read.
