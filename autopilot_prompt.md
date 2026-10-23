# Autopilot scheduled task: prompt and schedule

The live scheduled task is "Aftergrow Pinterest autopilot (Mon & Thu)", cron `CRON_TZ=America/New_York 43 9 * * 1,4` (Mondays and Thursdays, 9:43 AM Eastern, after the Meta run at 8:47 AM). If it ever has to be recreated, use this prompt:

---

Run Aftergrow's Pinterest autopilot. This is a scheduled run and nobody is watching. George, the founder of Aftergrow (getaftergrow.com), reads only your final report.

Setup:
1. Call add_repo with owner "domin8commerce", repo "aftergrow", access "push". Run the clone command it returns, then call register_repo_root for that directory. Then run `cd engine && npm install` inside the repo for the brand fonts (Chromium is preinstalled).
2. Read RUNBOOK.md in the repo from top to bottom and follow it exactly. It is the source of truth for:
   - the start-of-run steps (validate, reconcile with Tailwind, status)
   - blocked mode and release
   - the weekly loop and the decision rules
   - the trend layer
   - the quality gate, the fact sheet and the Journal page map
   - the report format

   This prompt only starts it.
3. Load the tools you need with ToolSearch:
   - "tailwind" for Tailwind
   - "shopify graphql" to read Journal articles
   - "composio" for the monthly Pinterest Trends pull (first run of each month)

Rules that override everything else:
- **Account.** Use only the Tailwind Pinterest account with ID 1658425 (username getaftergrow).
- **Scheduling goes through autopilot.py.** Every scheduling decision and record goes through engine/autopilot.py (status, reconcile, resolve, next-canary, next-batch, scheduled). Do what its output says. Never schedule a pin it did not hand you, and never edit queue.json or status.json by hand.
- **Don't change the setup.** Pins on HOLD in engine/queue_build.py stay held. Never change the HOLD list, the board names, the brand rules or the website.
- **Blocked mode.** Schedule at most the one canary that next-canary gives you. Never route around a Pinterest link block: no other domains, no redirects, no link shorteners and no posting the link through other apps.
- **Facts and links.** Only state facts that are on the RUNBOOK fact sheet or in the Journal page map. Only link to pages in LIVE_PAGES in engine/queue_build.py. Never link to a page about weight loss or weight-loss surgery.
- **New pins.** Make at most 10 per run, following the order at the top of the Journal page map: the haircut and hairstyle boards first, then dry scalp. Ship only pins that pass the quality gate:
  - look at every render at full size and at 236 px wide
  - have a separate agent fact-check the batch against the page facts
  - queue_build.py must print "problems: none"

  Push new pins and confirm their raw GitHub URLs return 200 before scheduling them.
- **Scheduling calls.** Call create_post one pin at a time, in the order given, with useNextOpenSlot: true. Record each with "python3 -I engine/autopilot.py . scheduled <ID> <postId> <sendAt>".
- **Published pins.** Never delete or edit a published pin, including the catalog pins on the board "Products". Flag problems in line 4 instead.
- **Tailwind plan.** Check it with list_subscriptions and get_account_usage. If it shows a pending cancellation, line 4 says: "Tailwind is cancelled and ends <date>. Reactivate it or the autopilot stops scheduling."
- **Git.** Commit and push every change to main with a clear message, using the commit attribution lines your environment gives you. If the push is rejected, fetch, rebase and push again.
- **Decisions.** If something needs George's decision, put it in line 4 of the report. Don't guess.

Finish with the five-line report from the RUNBOOK, in plain English. If the SendUserMessage tool is available, send the report with it as well.
