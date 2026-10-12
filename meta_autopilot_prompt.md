# Meta autopilot scheduled task: prompt and schedule

Scheduled task "Aftergrow Meta autopilot (Mondays)", ID `trig_01C3Cm6o5cGBYcnPHBRWi3ve`, created Oct 11, 2026: cron `CRON_TZ=America/New_York 47 8 * * 1` (Mondays, 8:47 AM Eastern), runs approved automatically, with this prompt. If you change the prompt, update both this file and the task (`update_trigger`).

---

Run Aftergrow's Instagram and Facebook autopilot. This is a scheduled run and nobody is watching. George, the founder of Aftergrow (getaftergrow.com), reads only your final report.

Setup:
1. Call add_repo with owner "domin8commerce", repo "aftergrow", access "push". Run the clone command it returns, then call register_repo_root for that directory. Then run `cd engine && npm install` inside the repo for the brand fonts.
2. Read META.md in the repo from top to bottom and follow its "Monday run" exactly. It is the source of truth for checking what went out, reading the numbers, the decision rules, making carousels and Reels, scheduling, and the report. For facts, read the "Fact sheet" and "Journal page map" sections of RUNBOOK.md. Ignore RUNBOOK's Pinterest steps.
3. Load the Metricool tools (search "metricool" with ToolSearch) and the Shopify analytics tool (search "shopify analytics").

Rules that override everything else:
- Use only Metricool brand 7369576 (Instagram @getaftergrow, Facebook Page 100613906395691), timezone America/New_York.
- Every post goes through engine/meta.py: `plan` decides the slots, `payload` builds the post, `date` gives the time with New York's offset, and `logged` records the id and uuid Metricool returns. Never schedule a post that meta.py did not plan, and never more than 14 days ahead.
- State only facts on the RUNBOOK fact sheet or in the Journal page map. Link only to pages in LIVE_PAGES in engine/queue_build.py.
- Make at most 4 new carousels per run. Ship only carousels where `python3 -I engine/carousel.py check` prints "problems: none" and every slide looks right at full size and at 236 px wide. Push new slides and Reels, and confirm their raw URLs return 200, before scheduling.
- Never put a link in a Facebook caption (links go in the first comment), never boost or spend money, never edit or delete a published post, and never touch Pinterest or Tailwind.
- Commit and push every change to main with a clear message, using the commit attribution lines your environment gives you.
- If something needs George's decision, put it in line 4 of the report. Don't guess. Don't change the brand rules or the website.

Finish with the five-line report from META.md, in plain English. If the SendUserMessage tool is available, send the report with it as well.
