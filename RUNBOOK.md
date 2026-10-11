# Aftergrow Pinterest: weekly runbook

This repository runs Aftergrow's Pinterest with no manual work. A Claude scheduled task follows this file every week. George, the founder, makes the final calls and reads the weekly report.

## What is here

| Path | What it is |
|---|---|
| `pins/` | Finished pins, 2000 x 3000 PNG (2:3). Served publicly from GitHub so Tailwind can fetch them. |
| `queue.json` | Every pin with board, title, description, link (UTM tagged), alt text, send time and status (`ready`, `scheduled`, `posted`). |
| `boards.json` | The 8 boards with their descriptions and Tailwind board IDs once created. |
| `engine/` | The pin engine: brand fonts (Schibsted Grotesk), exact palette, The Part symbol, rendered by headless Chromium. `npm install` in `engine/`, then `python3 -I engine/batch2.py <out_dir> [IDs]`. |
| `log.json` | What was scheduled, when, and the Tailwind post IDs. |

## Every weekly run

1. **Boards.** In Tailwind, list boards. Create any board from `boards.json` that is missing (`create_board`, public, with its description). Save the board IDs back to `boards.json`.
2. **Schedule.** For every `ready` pin in `queue.json`, call Tailwind `create_post` with:
   - `mediaUrl`: `https://raw.githubusercontent.com/<owner>/aftergrow-pins/main/pins/<image>`
   - `boardId` from `boards.json`, `title`, `description`, `url` = `link` (never change a link), `altText`, `sendAt` = `send_at_utc`.
   - If a `send_at_utc` is in the past, move it to the next free 1:00 PM or 8:30 PM Eastern slot, keeping two pins a day and never the same board twice in one day.
   - Mark the pin `scheduled` with its Tailwind post ID. Commit and push.
3. **Learn (from 30 days after the first pin).** Pull Tailwind analytics for the last 30 days: `list_top_pins` by SAVE and by OUTBOUND_CLICK. For the top 3 pins, make one fresh variant each with the engine: change the field color and the headline angle, keep the link and the facts. Add them to `queue.json` as `ready`.
4. **Refill.** When fewer than 14 `ready` pins remain, build the next ideas from the backlog below, but only ideas whose landing page now answers the pin.
5. **Report to George** in five lines: what was scheduled, the top 3 pins by saves and clicks, what was made new, anything blocked, Tailwind credits left.

## Quality gate (every new pin, before it is pushed)

- Render at 2000 x 3000. Look at it full size and at 236 px wide: the headline must read at feed size.
- Check every word on the image against the copy. No stranded single word at the end of a line.
- Banned anywhere: weight loss, diet, slim, before and after, regrow, stop or prevent hair loss, cure, treat, clinically proven, miracle, holy grail, detox, any drug name or drug class, em dashes, exclamation marks, emoji, all caps.
- Cosmetic claims only. Facts only from: American Academy of Dermatology, Harvard Health, and getaftergrow.com's own pages.
- No fake proof: no review counts, ratings, customer numbers or AI people as customers.
- Title under 100 characters with the keyword in the first 40. Description 150 to 280 characters.

## Backlog (held until a landing page answers them)

| Ideas | What they need |
|---|---|
| A09, C06, F03 | Short answers on the FAQ page (myths, morning or night, silk pillowcases) |
| B03, B05, B06 | A postpartum Journal article (timing, baby hairs, a gentle routine with "Pregnant or nursing? Ask your clinician first.") |
| C02, F02 | A Journal article on scalp massage and wash-day scalp care |
| D02, D03, D07 | A Journal article on hair changes after 40 and styling for fuller-looking hair |
| F04 | A Journal article on nutrition questions to ask a clinician |
| G01 | A printable 90-day tracker PDF on the Month-Three Guide page |
| H01, C08 | A real product photo (never an invented label) |
| C05 | George's call on the word "detox" (banned in the brand book, rising on Pinterest) |
