# Aftergrow on Instagram and Facebook: runbook

This file runs Aftergrow's organic Instagram and Facebook without manual work. A Claude scheduled task (`trig_01C3Cm6o5cGBYcnPHBRWi3ve`, prompt in `meta_autopilot_prompt.md`) follows it every Monday at 8:47 AM Eastern. George, the founder, makes the final calls and reads a five-line report after each run. Anything that needs his decision goes in line 4 of the report. Never guess on his behalf.

- Metricool brand: **blogId 7369576**, timezone **America/New_York**. Instagram **@getaftergrow**, Facebook Page **100613906395691**. Use no other brand.
- Pinterest is paused (domain blocked, appeal denied Oct 11, 2026). Don't touch it here. RUNBOOK.md covers it, and a one-time check-in runs on Nov 9.
- Facts come from the **Fact sheet** and the **Journal page map** in RUNBOOK.md. Nothing else may be stated.

## What success means

Website visits are the goal. Everything else is a signal on the way there.

| Level | Metric | Where it comes from |
|---|---|---|
| Goal | Website sessions from organic Instagram and Facebook | Shopify: `FROM sessions SHOW sessions GROUP BY utm_source, utm_medium, utm_campaign, utm_content SINCE -7d UNTIL today`. Count rows with `utm_medium = social` and `utm_source` in `facebook`, `ig`, `instagram`. The bio link is tagged `utm_source=ig&utm_content=link_in_bio`; Facebook comment links are tagged `utm_source=facebook&utm_content=<ID>` or `<ID>-reel`. Paid Meta ads use `utm_medium=paid_social` or `paid`: never count those. |
| Instagram | Profile visits and bio-link taps | Profile visits show only in the Instagram app (the API no longer reports them). Bio-link taps are the `link_in_bio` sessions above. Follows per post: `IGPO29`. |
| Instagram | Saves and shares per 1,000 people reached | Posts: `IGPO15` saved, `IGPO27` shares, `IGPO14` reach. Reels: `IGRE12` saved, `IGRE21` shares, `IGRE11` reach, `IGRE27` retention, `IGRE28` 3-second view rate. |
| Facebook | Shares, reach and comment-link sessions | Posts: `FBPO14` shares, `FBPO12` reach. Reels: `FBRE11` reach, `FBRE13` average time watched. |

Baseline on Oct 11, 2026: zero organic posts. Organic social sessions in the 30 days before: 4 from the Instagram bio link, none tagged from Facebook organic. Set numeric targets after 14 days of data, not before.

Match a Metricool post to its ID by the first 80 characters of its text (`IGPO03`, `IGRE03`, `FBPO03`, `FBRE05`) against the `ig` or `fb` caption in `engine/carousels_*.py`.

## What is here

| Path | What it is |
|---|---|
| `engine/carousels_*.py` | Every carousel: ID, pillar, landing page, slides, hashtags, Instagram caption, Facebook caption and the Facebook first comment. |
| `engine/carousel.py` | Renders 4:5 slides (1440 x 1800 JPEG) and checks every carousel: `python3 -I engine/carousel.py check` must print `problems: none`. |
| `engine/reel.py` | Turns a carousel into a 9:16 Reel with an original soundtrack: `python3 -I engine/reel.py reels <IDs>`. |
| `engine/meta.py` | The slot plan, the Metricool payloads and the posting log (`meta_log.json`). |
| `ig/<ID>/` and `reels/` | Finished slides and Reels, served publicly so Metricool can fetch them. Metricool copies them when a post is created. |

## The format

- Every carousel goes out twice on each network: first as a carousel (saves and shares), then a day or more later as a Reel (reach to people who don't follow us yet).
- Slots (New York time): carousels Mon, Wed, Fri, Sun; Reels Tue, Thu, Sat. Facebook goes out at its audience peak (9:52, Wednesday 11:52, Sunday 17:52). Instagram tests midday (11:47) for carousels against the evening (19:17) for Reels until there is data. `meta.py plan` fills the slots.
- Instagram captions end with the save-and-send line, the follow line and at most 5 hashtags (Instagram's limit). The caption never promises what the bio link holds unless George confirms it.
- Facebook captions carry no link. The link goes in the first comment (Facebook is testing a cap on link posts for Pages without Meta Verified, and comment links don't count).
- Music: Instagram Reels use a track from Instagram's music library (`TRACKS` in `meta.py`, rotated). Facebook Reels play our original soundtrack. Carousels can't carry music through the API.
- `isAiGenerated` stays false: these are designed graphics with no realistic AI imagery. If that ever changes, set it to true.

## Monday run, in this order

1. **Get the repo.** `add_repo` (owner `domin8commerce`, repo `aftergrow`, access `push`), run the clone command it returns, `register_repo_root`, then `cd aftergrow && (cd engine && npm install)` for the brand fonts. Load the Metricool and Shopify tools with ToolSearch.
2. **Check what went out.** `getScheduledPosts` from 8 days ago to 15 days ahead (brandId 7369576, America/New_York). Compare with `python3 -I engine/meta.py status`. Any post with an error status goes in line 4 of the report, with the error text. Don't re-send a failed post blindly: fix the cause first.
3. **Read the numbers.** `getAnalyticsDataByMetrics` for the last 14 days: posts `IGPO02, IGPO03, IGPO14, IGPO15, IGPO27, IGPO29, IGPO08`; Reels `IGRE02, IGRE03, IGRE11, IGRE12, IGRE21, IGRE27, IGRE28`; Facebook `FBPO02, FBPO03, FBPO12, FBPO14` and `FBRE02, FBRE05, FBRE11, FBRE13`. Then the Shopify query in **What success means**.
4. **Decide** with the rules below.
5. **Make** 4 new carousels in a new `engine/carousels_wN.py`, IDs continuing from the last one. Follow **Make**.
6. **Check and render.** `carousel.py check` must print `problems: none`. Then have a separate agent (one that didn't write them) fact-check every slide, caption and first comment against the Fact sheet and Journal page map, and fix or cut anything it can't match to a line there. On Oct 11 this check caught a patch-test tip that contradicted its own slide and several claims credited to the AAD that weren't on the sheet. If a fact is true but missing, check the source page and add it to the Fact sheet first. Render to `ig/`, then look at every slide (a contact sheet at full size and at 236 px wide): no orphan words, nothing cut off, nothing touching the footer. Build the Reels into `reels/` and look at one frame per slide.
7. **Push** the new slides and Reels, then confirm one raw URL per carousel returns 200 before scheduling.
8. **Schedule.** `python3 -I engine/meta.py plan 14`. For each line with an ID: `meta.py payload <ID> <network> <kind> <time>`, pass that JSON to `createScheduledPost` (blogId 7369576, `date` from `meta.py date <time>`, which adds New York's offset), then `meta.py logged <ID> <network> <kind> <time> <id> <uuid>` from the response. One post per call. Never schedule more than 14 days ahead.
9. **Commit and push** `meta_log.json` and everything new.
10. **Report** (five lines, below).

## Decision rules

- Under 300 people reached per post, the numbers are noise. Keep the plan, report the counts and wait.
- Score each post by saves plus shares per 1,000 reached (Instagram) and shares plus comment-link sessions (Facebook).
- A winner is in the top quarter and at least twice the median. Make one variant of each winner the following week: same topic, new cover hook and a new angle, or the other format.
- A topic in the bottom quarter twice in a row is retired for a month.
- Keep 70% of new carousels on proven pillars and 30% on new topics.
- Reels: if retention (`IGRE27`) is under 30% or the 3-second view rate (`IGRE28`) is under 40%, shorten the slides and sharpen the cover before making more.
- Timing: after four weeks, compare Instagram reach at 11:47 and 19:17. If one wins by 25% or more, move both formats there (change `SLOTS` in `meta.py`).
- If the website sessions from organic social stay at zero for four weeks while reach grows, tell George in line 4: the bio link or landing pages are the problem, not the posts.

## Make

- One carousel = one question a woman 35 to 60 actually asks, answered in 7 slides: cover, five content slides (one of them a "see a dermatologist if" checklist when it fits), sources, and the save-and-send slide.
- Pick topics from the Journal page map in order: seasonal first (dry hair and dry scalp until February), then trend tie-ins, then the rest. Each carousel links to the one page that answers it (`page`), which must be in `LIVE_PAGES`.
- State only facts on the Fact sheet or listed for that page in the Journal page map, and name the source on the slide.
- Templates: `cover`, `statement`, `timeline`, `compare`, `bignum`, `checklist`, `swaps`, `list`, `sources`, `cta`. Covers alternate butter and espresso.
- Captions: plain English, no exclamation marks, no emoji, no all caps. "Hair loss" only in captions, never on slides. Instagram: the answer in the first line, the save-and-send line last. Facebook: the same answer, ending with where the link is ("...is in the first comment.").
- Hashtags: 5, lowercase, specific to the topic (for example `hairshedding`, `dryscalp`, `postpartumhair`), never banned words.
- The serum appears only in routine content (how to use a scalp serum, what to look for) and never as an answer to shedding, postpartum or dermatologist topics.

## Never

- Never put a link in a Facebook caption, and never use link shorteners or other domains.
- Never state a fact that isn't on the Fact sheet or the Journal page map. No product claims, no before and after, no AI people, no fake reviews.
- Never use the banned words in `engine/queue_build.py` (BANNED), drug names or "GLP-1".
- Never boost a post or spend money. Boosting is George's call; suggest it in line 4 when a post clearly wins.
- Never delete or edit a published post. Never touch Pinterest or Tailwind from this runbook.

## Five-line report

1. **Shipped:** what went out last week and what is scheduled (counts, plus anything that failed).
2. **Numbers:** organic social website sessions this week vs last week; Instagram follows, saves and shares; Facebook reach and shares.
3. **Winner and loser:** the best and worst post by the scoring rule, with the number.
4. **George:** decisions or one-time fixes only he can make, or "Nothing needed."
5. **Next:** the topics coming up.
