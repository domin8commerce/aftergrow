# Autopilot scheduled task: prompt and schedule

Restore this when Pinterest unblocks the domain (RUNBOOK, "Restart"). Use `update_trigger` on the existing task with cron `CRON_TZ=America/New_York 47 8 * * 1,4` (Mondays and Thursdays, 8:47 AM Eastern) and this prompt:

---

Run Aftergrow's Pinterest autopilot. This is a scheduled run and nobody is watching. George, the founder of Aftergrow (getaftergrow.com), reads only your final report.

Setup:
1. Call add_repo with owner "domin8commerce", repo "aftergrow", access "push". Run the clone command it returns, then call register_repo_root for that directory.
2. Read RUNBOOK.md in the repo from top to bottom and follow it exactly. It is the source of truth for the start-of-run steps (validate, reconcile with Tailwind, status), blocked mode, release, the weekly loop, the decision rules, the quality gate, the fact sheet and the report format. This prompt only starts it.
3. The Tailwind tools may need loading first (search for "tailwind" with ToolSearch).

Rules that override everything else:
- Use only the Tailwind Pinterest account with ID 1658425 (username getaftergrow).
- Every scheduling decision and record goes through engine/autopilot.py (status, reconcile, resolve, next-canary, next-batch, scheduled). Do what its output says. Never schedule a pin it did not hand you, and never edit queue.json or status.json by hand.
- In blocked mode, schedule at most the one canary that next-canary gives you. Never route around a Pinterest link block. That means no other domains, no redirects, no link shorteners and no posting the link through other apps.
- Only state facts that are on the RUNBOOK fact sheet. Only link to pages in LIVE_PAGES in engine/queue_build.py.
- Make at most 10 new pins per run. Ship only pins that pass the quality gate: look at every render at full size and at 236 px wide, and queue_build.py must print "problems: none". Push new pins before scheduling them.
- Call create_post one pin at a time, in the order given, with useNextOpenSlot: true. Record each with "python3 -I engine/autopilot.py . scheduled <ID> <postId> <sendAt>".
- Commit and push every change to main with a clear message, using the commit attribution lines your environment gives you.
- If something needs George's decision, put it in line 4 of the report. Don't guess. Don't change the brand rules, the board names or the website.

Finish with the five-line report from the RUNBOOK, in plain English. If the SendUserMessage tool is available, send the report with it as well.
