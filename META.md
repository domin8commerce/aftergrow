# Aftergrow on Instagram and Facebook: runbook

This file runs Aftergrow's organic Instagram and Facebook without manual work. A Claude scheduled task (`trig_01C3Cm6o5cGBYcnPHBRWi3ve`, prompt in `meta_autopilot_prompt.md`) follows it every Monday at 8:47 AM Eastern. George, the founder, makes the final calls and reads a five-line report after each run. Anything that needs his decision goes in line 4 of the report. Never guess on his behalf.

- Metricool brand: **blogId 7369576**, timezone **America/New_York**. Instagram **@getaftergrow**, Facebook Page **100613906395691**. Use no other brand.
- **Reels only** since Oct 12, 2026 (George's decision). On day one the Reel reached 113 people on Instagram and the carousel reached 7. Never schedule a carousel.
- Pinterest is paused (domain blocked, appeal denied Oct 11, 2026). Don't touch it here. RUNBOOK.md covers it, and a one-time check-in runs on Nov 9.
- Facts come from the **Fact sheet** and the **Journal page map** in RUNBOOK.md. Nothing else may be stated.

## What success means

Website visits are the goal. Everything else is a signal on the way there.

| Level | Metric | Where it comes from |
|---|---|---|
| Goal | Website sessions from organic Instagram and Facebook | Shopify: `FROM sessions SHOW sessions GROUP BY utm_source, utm_medium, utm_campaign, utm_content SINCE -7d UNTIL today`. Count rows with `utm_medium = social` and `utm_source` in `facebook`, `ig`, `instagram`. The bio link is tagged `utm_source=ig&utm_content=link_in_bio`; Facebook comment links are tagged `utm_source=facebook&utm_content=<ID>-reel`. Paid Meta ads use `utm_medium=paid_social` or `paid`: never count those. |
| Instagram | Profile visits, follows and bio-link taps | Profile visits show only in the Instagram app (the API no longer reports them). Bio-link taps are the `link_in_bio` sessions above. |
| Instagram | Does the Reel hold people? | `IGRE28` 3-second view rate, `IGRE24` average watch time (compare with the Reel's length), `IGRE11` reach, `IGRE23` views. |
| Instagram | Is it worth keeping and sharing? | `IGRE12` saves and `IGRE21` shares per 1,000 reached. |
| Facebook | Reach, watch time and comment-link sessions | `FBRE11` reach, `FBRE10` views, `FBRE13` average time watched. |

Baselines: before Oct 11, 2026, 4 organic social sessions in 30 days (all from the Instagram bio link). First Reel (AG01, Oct 11): 113 reached, 3-second view rate 16.8%, average watch 3.8 s of 31 s. That Reel was a carousel turned into video; the v2 Reels below were built to fix the first three seconds. Set numeric targets after 14 days of v2 data, not before.

Match a Metricool Reel to its ID by the first 80 characters of its text (`IGRE03`, `FBRE05`) against the `ig` or `fb` caption in `engine/reels_*.py`.

## What is here

| Path | What it is |
|---|---|
| `engine/reels_*.py` | Every Reel script: ID, pillar, landing page, music, scenes, hashtags, Instagram caption, Facebook caption and first comment. The order in the file is the posting order. |
| `engine/reel2.py` | The Reel engine. `check` validates scripts; `frames <dir> <ID>` draws a review sheet; `render reels <IDs>` writes `reels/<ID>.mp4` and `reels/<ID>_cover.jpg`. |
| `engine/meta.py` | The slot plan, the Metricool payloads and the posting log (`meta_log.json`). |
| `reels/` | Finished Reels and covers, served publicly so Metricool can fetch them. Metricool copies them when a post is created or updated. |
| `engine/carousels_*.py`, `engine/carousel.py`, `engine/reel.py`, `ig/` | The carousel era (Oct 11 and 12). Kept for the record and for their vetted facts; never planned again. |

## The format

- **One Reel a day on each network.** Instagram at 19:17; Facebook at its audience peak (9:52, Wednesday 11:52, Sunday 17:52). `meta.py plan` fills the slots from the scripts in file order.
- **15 to 22 seconds, 4 to 6 scenes, one idea per scene.** Scene types: `hook`, `say`, `big`, `checks`, `list`, `steps`, `vs`, `swaps`, `cta`.
- **The hook wins or loses the Reel.** It is readable on the first frame, names a moment the viewer recognizes ("More hair in the drain lately?", "Flakes on your shoulders again?"), is at most 10 words, and each hook line is at most 16 characters so the type stays huge. The sub-line promises the answer. Never say the viewer has a condition, and never promise a result.
- **Motion:** lines rise in one after another, one key word per scene gets the highlighter (`<mark>`), checkmarks draw, scenes swipe left, and a progress bar at the top shows how short it is. All text stays between y 260 and 1400 so Instagram's name, caption and buttons never cover it.
- **Sources on screen:** a small source line under the fact it supports. Credit only what the Fact sheet credits to that source.
- **The last scene asks for the save and the send,** with a send line written for the topic ("Send it to a friend who takes hair vitamins.").
- **Music:** Instagram plays a track from Instagram's library (`audio` in the script, else `TRACKS` in `meta.py`), with the video's own sound off. Facebook plays our original soundtrack, which changes chord on every scene and whooshes on every swipe.
- **Captions:** Instagram leads with the hook line, gives the answer in two short paragraphs, ends with the save-and-send line, the follow line and 5 hashtags. Facebook carries no link: the link goes in the first comment (Facebook is testing a cap on link posts for Pages without Meta Verified, and comment links don't count). The caption never promises what the bio link holds unless George confirms it.
- `isAiGenerated` stays false: designed graphics, no realistic AI imagery.

## Monday run, in this order

1. **Get the repo.** `add_repo` (owner `domin8commerce`, repo `aftergrow`, access `push`), run the clone command it returns, `register_repo_root`, then `cd aftergrow && (cd engine && npm install)` for the brand fonts. Load the Metricool and Shopify tools with ToolSearch.
2. **Check what went out.** `getScheduledPosts` from 8 days ago to 15 days ahead (brandId 7369576, America/New_York). Compare with `python3 -I engine/meta.py status`. Any post with an error status goes in line 4 of the report, with the error text. Don't re-send a failed post blindly: fix the cause first.
3. **Read the numbers.** `getAnalyticsDataByMetrics` for the last 14 days: Instagram `IGRE02, IGRE03, IGRE11, IGRE23, IGRE24, IGRE28, IGRE12, IGRE21, IGRE10, IGRE07`; Facebook `FBRE02, FBRE05, FBRE11, FBRE10, FBRE13`. Then the Shopify query in **What success means**.
4. **Decide** with the rules below.
5. **Write** 7 new Reel scripts (one week) in a new `engine/reels_rN.py`, IDs continuing from the highest ID in the repo. Follow **Make**. If fewer than 14 unused topics are left in the Journal page map, say so in line 4: George's team needs to publish more Journal articles.
6. **Check.** `python3 -I engine/reel2.py check` must print `problems: none`. Then have a separate agent (one that didn't write them) fact-check every scene, caption and first comment against the Fact sheet and Journal page map, including whether each source line credits the right source. Fix or cut anything it can't match. On Oct 11 and 12 this check caught a patch-test tip that contradicted its own slide, a reversed claim ("all over = usually a shed"), and source lines crediting facts to the wrong body. If a fact is true but missing, check the source page and add it to the Fact sheet first.
7. **Look.** For every Reel, `python3 -I engine/reel2.py frames <tmp> <ID>` and read the sheet: hook big and complete by 0.6 s, no line cut off, no text under the progress bar or below y 1400, highlighter on the right word. Then render, and pull 6 frames from the MP4 to confirm the encode.
8. **Render and push** `reels/<ID>.mp4` and `reels/<ID>_cover.jpg`, then confirm one raw URL per Reel returns 200 and matches the local file before scheduling.
9. **Schedule.** `python3 -I engine/meta.py plan 14`. For each line with an ID: `meta.py payload <ID> <network> reel <time>`, pass that JSON to `createScheduledPost` (blogId 7369576, `date` from `meta.py date <time>`), then `meta.py logged <ID> <network> reel <time> <id> <uuid>` from the response. One post per call. Never schedule more than 14 days ahead.
10. **Commit and push** `meta_log.json` and everything new.
11. **Report** (five lines, below).

## Decision rules

- Under 300 people reached per Reel, the numbers are noise. Keep the plan, report the counts and wait.
- **Hook test first.** If the 3-second view rate (`IGRE28`) is under 40%, the opening is the problem: change the hook type next week (a question, a number, a "stop doing this" line) before changing anything else.
- **Hold test second.** If average watch time is under 30% of the Reel's length, cut words and scenes.
- **Value test third.** Score each Reel by saves plus shares per 1,000 reached. A winner is in the top quarter and at least twice the median: make one variant of each winner the following week (same facts, new hook).
- A topic in the bottom quarter twice in a row is retired for a month.
- Keep 70% of new Reels on proven pillars and 30% on new topics.
- Timing: after three weeks, compare Instagram reach for Reels at 19:17 with a one-week test at 12:17. Move if one wins by 25% or more (change `IG_TIME` in `meta.py`).
- If website sessions from organic social stay near zero for four weeks while reach grows, tell George in line 4: the bio link or landing pages are the problem, not the Reels.

## Make

- One Reel = one question a woman 35 to 60 actually asks, opened with the moment she notices it (the drain, the brush, the part in the mirror, flakes on a black sweater, a label she doesn't trust), answered with sourced facts, closed with a reason to save or send it.
- Pick topics from the Journal page map: seasonal first (dry hair and dry scalp until February), then trend tie-ins, then the rest, then variants of winners. Each Reel links to the one page that answers it (`page`), which must be in `LIVE_PAGES`.
- State only facts on the Fact sheet or listed for that page in the Journal page map.
- Captions: plain English, no exclamation marks, no emoji, no all caps. "Hair loss" only in captions, never on screen. Hashtags: 5, lowercase, specific to the topic, never banned words.
- The serum appears only in routine content (how to use a scalp serum, what to look for) and never as an answer to shedding, postpartum or dermatologist topics.

## Never

- Never schedule a carousel or an image post.
- Never put a link in a Facebook caption, and never use link shorteners or other domains.
- Never state a fact that isn't on the Fact sheet or the Journal page map. No product claims, no before and after, no AI people, no fake reviews.
- Never use the banned words in `engine/queue_build.py` (BANNED), drug names or "GLP-1".
- Never boost a post or spend money. Boosting is George's call; suggest it in line 4 when a Reel clearly wins.
- Never delete or edit a published post. Never touch Pinterest or Tailwind from this runbook.

## Five-line report

1. **Shipped:** Reels that went out last week and what is scheduled (counts, plus anything that failed).
2. **Numbers:** organic social website sessions this week vs last week; Instagram reach, 3-second view rate, average watch time, saves, shares and follows; Facebook reach and views.
3. **Winner and loser:** the best and worst Reel by the rules above, with the numbers.
4. **George:** decisions or one-time fixes only he can make, or "Nothing needed."
5. **Next:** the topics coming up.
