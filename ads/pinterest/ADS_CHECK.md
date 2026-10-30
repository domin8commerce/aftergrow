# Aftergrow Pinterest ads: build log and check runbook

Ad account 549770879093 (USD). Campaign A launched Oct 29, 2026, 8:07 PM ET (Oct 30, 00:07 UTC), on George's go.

The scheduled task "Aftergrow Pinterest ads check (Tue & Fri)" reads this file on every run, follows "The check" below, and appends to "Check log" at the bottom.

## State of the account
- **Campaign A (Search lab), 626760182006:** ACTIVE at $5/day.
- **Paused:** the three older campaigns, which George paused on Oct 29:
  - Sponsored Product | Test | Oct 2026 (626760143882)
  - Consideration Pins Campaign | Boosted Pins Batch 1 (626760180766)
  - the automated campaign (626760180755)
- **Serum color:** George confirmed on Oct 29 that the real serum is amber/golden, like the video, so the video ad stays in.

## Campaign A: Search lab
- **Campaign** 626760182006 "AG | A | Search lab | Consideration":
  - objective Consideration;
  - campaign budget $5/day (campaign budget optimization is required on this account);
  - standard campaign, not Performance+.
- **Ad group** 2680092807543 "A1 | Women 35-65+ | Product keywords | Search":
  - search placement only;
  - US, English, women 35-65+, all devices;
  - automatic targeting off;
  - automatic bid, billed per click, standard pacing.
- **Keywords** (72): 29 phrase, 4 exact, 39 phrase negatives.
  - Phrase: thin hair products, products for thin hair, hair products for thin hair, best products for thin hair, thin fine hair, fine thin hair products, hair products for fine thin hair, fine hair products, volumizing products for fine hair, hair thickening products, hair thickening serum, thickening serum, hair serum for thin hair, hair serum for fine hair, scalp serum, scalp serum for thin hair, peptide serum for hair, peptide hair serum, lightweight hair serum, leave in scalp serum, scalp care products, scalp care routine, fragrance free hair products, head spa at home, how to make thin hair look thicker, how to make fine hair look fuller, fuller looking hair, fine thin hair over 50, hair care over 50.
  - Exact: thin hair products, scalp serum, hair thickening products, products for thin hair.
  - Negatives: men, mens, male, beard, boys, kids, toddler, baby, diy, recipe, homemade, wig, wigs, extensions, topper, braids, dog, cat, thick hair, long hair, weight loss, ozempic, glp-1, wegovy, mounjaro, minoxidil, rogaine, finasteride, transplant, prp, chemo, drawing, anime, tattoo, hair loss, alopecia, regrowth, regrow, postpartum.

### Ads
Every ad uses direct links (a click opens the landing page) and the "Shop now" button. All three were PENDING review when created.

| Ad ID | Name | Pin ID | Creative | utm_content | Organic link on the pin |
|---|---|---|---|---|---|
| 687322854477 | A1 \| VR02 \| Daily step \| 1:1 | 1108448527072618492 | 1500x1500 image, "A scalp serum. A daily step." | vr02 | /products/scalp-serum |
| 687322854478 | A1 \| VR09 \| Formula \| 1:1 | 1108448527072618494 | 1500x1500 image, "The formula deserves a closer read." | vr09 | /blogs/journal/how-to-read-a-scalp-serum-label |
| 687322854479 | A1 \| VIDEO01 \| Dropper 15s \| 9:16 | 1108448527072618581 | 15-second Runway video, dropper macro ending on the label | video01 | /blogs/journal/what-to-look-for-in-a-scalp-serum |

- **Paid destination:** `https://getaftergrow.com/products/scalp-serum?utm_source=pinterest&utm_medium=paid_social&utm_campaign=search-lab&utm_content=<vr02|vr09|video01>`
- **Pins:**
  - Board "Aftergrow Scalp Serum" (1108448595728308248).
  - Each pin carries Pinterest's "AI modified" disclosure. The video is Runway-generated and has C2PA metadata.
  - Organic links use `utm_source=pinterest&utm_medium=social&utm_campaign=organic&utm_content=<id>`. Saves of an ad send people to the organic link, so earned traffic counts as organic.
- **Creative files:**
  - GitHub domin8commerce/aftergrow, folder ads/pinterest/search-lab/ (commit fd5f3ee).
  - Backups: VR08 ("30 mL") and VR14 ("This is the scalp step").
- **Rejected for ads:**
  - INFLUENCER 1.mp4: growth claim, "cleans your scalp", possible AI avatar.
  - AG IMAGES set: AI women, before/afters, "Hormones Stole My Hair".

## Paid vs organic in Shopify (no developer needed)
| Traffic | utm_source | utm_medium |
|---|---|---|
| Paid Pinterest ads | pinterest | paid_social |
| Organic pins (autopilot and the pins above) | pinterest | social |
| Pinterest app catalog ads | Pinterest | PaidSocial (campaign ID in utm_campaign, ad group ID in utm_content) |

ShopifyQL, tested on Oct 29:

```
FROM sessions SHOW sessions, sessions_with_cart_additions, sessions_that_completed_checkout
WHERE utm_source = 'pinterest' OR utm_source = 'Pinterest'
GROUP BY utm_source, utm_medium, utm_campaign, utm_content SINCE -30d UNTIL today ORDER BY sessions DESC
```

## API notes
- **Composio:** the pinterest_ads proxy takes paths without `/v5`. The PINTEREST_ADS_LIST_CAMPAIGNS tool returns empty, so use a raw GET instead.
- **Campaign budget:** ad-group budgets fail with error 2454. Use a campaign budget, and set the ad group's budget_type to CBO_ADGROUP.
- **Outbound clicks:** the API has no outbound-click optimization field. optimization_goal_metadata only takes conversion, frequency and scrollup metadata. Direct links are on, so paid clicks land on the site.
- **Pins:**
  - Images: PINTEREST_CREATE_PIN with an image_url.
  - Video:
    1. PINTEREST_REGISTER_MEDIA.
    2. Multipart POST of the file to the S3 upload_url, with every upload_parameter (returns 204).
    3. Poll PINTEREST_GET_MEDIA until "succeeded" (about 80 seconds).
    4. PINTEREST_CREATE_PIN with a video_id and cover_image_url.
- **Ads:** POST /ad_accounts/{id}/ads accepts a destination_url that differs from the pin link. grid_click_type is read-only and comes back as DIRECT_TO_DESTINATION.
- **Keywords:** POST /ad_accounts/{id}/keywords with {"parent_id": ad group, "keywords": [{match_type, value}]}.

## How the Search lab is judged
- **Days 1-14: no edits** except emergencies:
  - a rejected ad;
  - a broken link;
  - spend with zero clicks over two days;
  - an obvious junk search term, which gets a negative keyword.
- **Read each check:**
  - impressions, CTR, CPC and outbound clicks per ad and per keyword;
  - search terms;
  - paid sessions, add to carts and orders in Shopify.
- **Break-even CPC** at 1-2% of clicks buying: $0.35-0.70 for a $35 CPA; $0.60-1.20 for a $60 CPA.
- **Creative:** review at about 10,000 impressions. Pause an ad whose CTR is under half the best ad's.
- **Campaign:** zero purchases after 3x target CPA means rebuild or kill, after a one-week wait for late buyers. That is $105 at a $35 target, about 21 days at $5/day.
- **Scale:** only after 10 purchases at or under target. Raise budgets in 20-30% steps, from Dec 26.

## The check (Tuesday and Friday)
All Pinterest calls go through `COMPOSIO_REMOTE_WORKBENCH` with `proxy_execute(method, endpoint, "pinterest_ads", query_params=..., body=...)`. Paths take no `/v5` prefix. Each call below worked on Oct 29.

1. **Status.**
   - `GET /ad_accounts/549770879093/campaigns` (page_size 50): the status of every campaign.
   - `GET /ad_accounts/549770879093/ads` with `campaign_ids=626760182006`: `review_status`, `rejected_reasons` and `rejection_labels` for each ad.
2. **Numbers since launch, and for the last 7 days.**
   - Endpoint: `GET /ad_accounts/549770879093/ads/analytics`.
   - Parameters: `ad_ids=687322854477,687322854478,687322854479`, `granularity=TOTAL` (or `DAY` for spend per day), `start_date` / `end_date` as YYYY-MM-DD, with the start no earlier than 2026-10-29.
   - Columns: `SPEND_IN_DOLLAR,PAID_IMPRESSION,CLICKTHROUGH_1,OUTBOUND_CLICK_1,CTR,OUTBOUND_CTR_1,ECPC_IN_DOLLAR,COST_PER_OUTBOUND_CLICK_IN_DOLLAR,TOTAL_PAGE_VISIT,TOTAL_CHECKOUT,TOTAL_CHECKOUT_VALUE_IN_MICRO_DOLLAR`.
   - An empty list means there is no delivery yet.
3. **Keywords.**
   - Endpoint: `GET /ad_accounts/549770879093/ad_groups/targeting_analytics`.
   - Parameters: `ad_group_ids=2680092807543`, `targeting_types=KEYWORD`, `granularity=TOTAL`, and the same date range.
   - Columns: `SPEND_IN_DOLLAR,PAID_IMPRESSION,CLICKTHROUGH_1,OUTBOUND_CLICK_1,CTR`.
   - The API has no search-term report. Search terms are only in Ads Manager.
4. **Shopify, the source of truth for orders.** Use `run-analytics-query`:
   `FROM sessions SHOW sessions, sessions_with_cart_additions, sessions_that_reached_checkout, sessions_that_completed_checkout WHERE utm_campaign = 'search-lab' GROUP BY utm_content SINCE 2026-10-29 UNTIL today`
5. **Product page.** Check that https://getaftergrow.com/products/scalp-serum loads, using WebFetch.

### What the check may do without asking
Only an emergency pause of campaign 626760182006: `PATCH /ad_accounts/549770879093/campaigns` with `[{"id":"626760182006","status":"PAUSED"}]`. Do it when any of these happens:
- the product page doesn't load;
- one day's spend is over $10;
- Pinterest reports a domain or spam block;
- an ad's destination URL has changed.

Say so at the top of the report.

### What needs George's yes (propose with a one-word reply, never do it unasked)
- Changing a budget, a bid or the targeting.
- Pausing or adding ads, keywords or negatives.
- Starting any other campaign.
- Changing pins or the website.

### Decision rules
- **Until Nov 13 (the first 14 days): no performance changes.** Report only. A rejected ad is the exception: report the reason and propose the fix. The backups are VR08 ("30 mL") and VR14 ("This is the scalp step"). They are in George's Drive and not hosted yet.
- **From Nov 13: one change round a week, on the Friday run.**
  - Ads: once ads have about 10,000 paid impressions each, propose pausing any ad whose CTR is under half the best ad's.
  - Keywords: propose archiving any keyword with $5 or more spent and zero outbound clicks.
  - Clicks: if the average cost per click stays above $1.20 for 14 days, flag it. New creative is the first fix.
- **Kill line.** $105 spent (3x a $35 target CPA) with zero Shopify purchases from `utm_campaign=search-lab`: wait one more week for late buyers, then propose a rebuild or a kill.
- **Scale.** Only after 10 purchases at or under target, and not before Dec 26. Propose a 20-30% budget step, or a duplicate at the higher budget.

### Report (five lines, plain English; George scans)
1. **Status:** campaign and ad status, review results, and any emergency action taken.
2. **Numbers:** spend, impressions, clicks, CTR, CPC and outbound clicks, since launch and for the last 7 days, with the best and worst ad. Shopify paid sessions, add to carts, checkouts and orders.
3. **Keywords:** the top keywords by clicks, and keywords spending with no clicks.
4. **Needs George:** each decision written as a one-word reply ("Reply yes to pause VR09"), or "nothing".
5. **Next check:** the date, plus what the next check will look at.

## Check log
(The scheduled check appends one dated entry per run: date, spend to date, impressions, clicks, CTR, CPC, Shopify orders, actions taken, and decisions asked.)

- 2026-10-29: launched. 3 ads pending review. $0 spent.
