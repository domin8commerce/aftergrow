# Pinterest keyword evidence

`pinterest-trends-2026-10-23.csv` is Pinterest's own search data, pulled from the Pinterest Trends API (through the Composio Pinterest connection, tool `PINTEREST_GET_KEYWORD_TRENDS`) on Oct 23, 2026.

## How it was pulled
- Market `US`, `trend_type: monthly` (ranked by last month's search volume), `limit` up to 50.
- Audience filter: `genders: [female]`, `ages: [35-44, 45-49, 50-54, 55-64]`.
- `normalize_against_group: true`, so the numbers inside ONE query share a scale (100 = the highest week of any keyword in that query). Numbers from different queries are not comparable.
- `include_demographics: true`, which gives the age split of everyone searching each keyword.

## How to read the columns
- `last4wk_rel` and `avg52wk_rel`: relative search volume, last 4 weeks and last 52 weeks.
- `yoy_pct`: growth versus a year ago, as Pinterest reports it.
- `share_35_64` and `share_45_64`: share of the keyword's searchers in those ages. This is the fit with Aftergrow's buyer.
- `peak_month`: the month with the highest average volume over the last year (publish 45 to 60 days before it).
- `query`: which pull it came from. **B0 is the cross-cluster benchmark**: one query holding every candidate cluster, so its rows can be ranked against each other.

## What it says (Oct 23, 2026)
1. For US women 35 to 64, Pinterest demand in this space is overwhelmingly **haircuts and hairstyles for thin, fine or thinning hair**. The two biggest phrases, "hairstyles for thin hair" and "thin hair haircuts", are 2 to 10 times anything else in the benchmark.
2. **"Fine thin hair over 50"** is up 2,500% year over year, with 51% of its searchers aged 45 to 64.
3. The "thinning hair" phrases skew older than the "thin hair" ones (59 to 72% of searchers aged 35 to 64).
4. **Dry and itchy scalp** searches skew 35 to 64 (58%) and peak in January and February.
5. **Head spa** and **scalp massage** are growing (+20%), and **rosemary water for hair** is up 400%.
6. **Little or no measurable demand:** hair shedding, telogen effluvium, scalp serum, peptides for hair, menopause hair. **"Hair loss" is suppressed:** the API returns nothing for it.
7. **Postpartum** searches are about haircuts and hairstyles, and 67 to 70% of searchers are 25 to 34, outside Aftergrow's buyer.
8. **GLP-1** searches on Pinterest are about meals and recipes. No hair terms appear.

## Re-run it
The monthly trend layer in RUNBOOK.md re-runs the same calls and saves `pinterest-trends-YYYY-MM-DD.csv` here, so changes can be compared month to month.
