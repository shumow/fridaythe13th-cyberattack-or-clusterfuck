# Measuring the news wave: protocol, fourth round (the bulk table)

Written on 18 November 2026, before any query on the bulk table that reads a title or counts a theme. `PROTOCOL.md`, `PROTOCOL-2.md` and `PROTOCOL-3.md` stay as they were. This file adds one instrument, a local copy of GDELT's article index, and fixes how it will be counted. It takes nothing away from the third round, whose series is in hand and is still to be analysed and reported as written.

## Why a fourth round

`PROTOCOL-3.md` says that if the gate is refused twice, there is "no third attempt and no other route to the same data". Both were done, at Dan's instruction: the search API was asked again overnight until it answered, and the underlying records were downloaded in bulk. This file is that other route, so it is a departure from the third round and is recorded here as one.

The reason is in the API's own answer. It returned 69 of the 93 days. Its count of all articles monitored has a median near 103,000 a day and falls to 5,213, 3,545 and 1,819 on 13, 14 and 15 November; 16 and 17 November are absent. The bulk files for the same days are complete. The registered statistics from the API will be reported, but they rest on a thinned index on the days that matter.

## What had been seen when this was written

Everything listed in `PROTOCOL-3.md`, and in addition:

- **From the search API's overnight answers:** the number of days returned; the daily `norm` values; each query's total over the whole period (`OUT_IT` 3,189, `BOTH` 304, `ATT` 7,976, `BOTH_STRICT` 215, `OUT_PLAIN` 7,365); and eight daily values of `BOTH_STRICT`, printed while checking the format of one raw answer: 0 on 17 August, 4 on 18 August, 0 on 13, 20 and 21 September, 24 on 14 November and 4 on 15 November. The last two are from the after period and from days with a collapsed `norm`. `nw_analyze.py` has not been run.
- **From the bulk table:** row counts per day, for all sources and for U.S. sources; the share of rows with a title; the column names; that every URL is distinct; and the daily count of titles containing `weather`, which Codex ran as its one permitted smoke test.
- **Theme names only:** the list of distinct theme names containing `CYBER`, `OUTAGE`, `HACK` or `BLACKOUT`, with no counts and no dates. This was needed to fix the theme lists below.
- **Not seen:** any title, any count of titles matching an outage or attack word, any count of any theme, for any day.

## The instrument

GDELT 2.0 Global Knowledge Graph, English feed, every 15-minute file from 17 August to 18 November 2026 at 10:00 UTC: 8,969 files, all checksums matched, 9,003,620 rows. Built by `gdelt-local/` on a remote host and copied to `gdelt-local/data/`, which is not in git. Its `REPORT.md` and `manifest.csv` are the record of what was fetched.

One row is one article URL. The fields used are `day_utc`, `source_country`, `title` and `themes`.

How this differs from the search API, and so from the third round:

- **Titles, not text.** A title match is a headline. The third round's queries matched anywhere in the article.
- **Themes stand in for text.** GDELT assigns themes from the article body by machine. A theme is the nearest thing in this table to "the article mentions it", and it is someone else's classifier.
- **The day is the day GDELT processed the article,** not the day it was published.
- **Source country comes from GDELT's May 2018 lookup.** It covers 97.6% of rows. Outlets founded or renamed since are left without a country.

## Gates, before any counting

1. **Columns.** Compare the seven column positions used by `gdelt-local/gdelt.py` with the GKG 2.1 codebook kept in `gdelt-local/data/reference/`. If any is wrong, stop.
2. **Titles are titles.** Read 20 rows drawn at random, with a fixed seed, from 18 November only, a partial day that no statistic uses. The gate passes if at least 18 of the 20 titles are plainly the headline of the page at that URL. This is the only reading of titles before counting.
3. **Totals.** The table's rows per day equal `daily_totals.parquet`. Already confirmed.

If a gate fails, write that in `HANDOFF.md` and stop. Do not repair the table and carry on in the same session.

## Population

- **Primary:** rows with `source_country = 'US'` and a title.
- **Sensitivity:** all rows with a title, any country, because the lookup is old. Every statistic is given both ways.

The lookup is not patched. No domain is added to it by hand.

## Patterns

Fixed in `bulk_queries.json`, committed with this file. Titles are lower-cased and their whitespace collapsed, as in the third round's part N2, and the first two patterns are N2's, unchanged.

| Name | Applied to | Pattern or list |
| --- | --- | --- |
| `OUT` | title | `\b(outages?\|ground stop)\b` |
| `ATT` | title | `\bcyber[ -]?attacks?\b\|\bhack(s\|ed\|ers?\|ing)?\b` |
| `ATT_STRICT` | title | `\bcyber[ -]?attacks?\b` |
| `NOT_TECH` | title | `\b(power\|electric\|electrical\|electricity\|utility\|utilities\|storms?\|hurricanes?\|tornado(es)?\|weather\|winds?\|snow\|ice\|wildfires?\|water\|gas)\b` |
| `ATT` themes | themes | `CYBER_ATTACK`, `WB_2457_CYBER_CRIME`, `TAX_FNCACT_HACKER`, `TAX_FNCACT_HACKERS` |
| `ATT_STRICT` themes | themes | `CYBER_ATTACK` |
| `POWER` themes | themes | `POWER_OUTAGE`, `MANMADE_DISASTER_POWER_OUTAGE`, `MANMADE_DISASTER_POWER_OUTAGES`, `MANMADE_DISASTER_POWER_BLACKOUT` |

A theme list matches when any of its names is one of the row's semicolon-separated themes, compared whole.

## Measures

| Name | A row counts when | Third-round counterpart |
| --- | --- | --- |
| `OUT_T` | its title matches `OUT` | `OUT_PLAIN` |
| `OUT_TECH` | its title matches `OUT` and not `NOT_TECH` | `OUT_IT` |
| `OUT_TECH_TH` | its title matches `OUT` and it has no `POWER` theme | `OUT_IT`, second way |
| `ATT_T` | its title matches `ATT` | `ATT` |
| `BOTH_T` | it is in `OUT_TECH` and its title matches `ATT` | part N2 |
| `BOTH_T_STRICT` | it is in `OUT_TECH` and its title matches `ATT_STRICT` | part N2, strict |
| `BOTH_TH` | it is in `OUT_TECH` and it has an `ATT` theme | `BOTH` |
| `BOTH_TH_STRICT` | it is in `OUT_TECH` and it has the `CYBER_ATTACK` theme | `BOTH_STRICT` |

`OUT_TECH` is the primary outage measure. `OUT_TECH_TH` removes electricity by GDELT's theme instead of by title words, and is reported beside it to show how much the choice matters.

Every measure is counted twice per day: over all rows, and over distinct titles so that a syndicated story counts once.

## Periods

As in `PROTOCOL-3.md`. Days are UTC days.

- **Baseline:** the twelve Monday-to-Sunday weeks from 17 August to 8 November.
- **The week of the pair:** 9 to 15 November.
- **After:** 13 to 17 November, five days. The 9th to the 12th are listed day by day and belong to neither side of the before-and-after comparison.
- **Headline window:** 2 to 17 November, for the one statistic carried over from part N2.
- **Not used:** 18 November, a partial day.

## Statistics, fixed now

1. **Weekly headline coverage.** `OUT_TECH` rows divided by all rows in the population, for each baseline week and for 9 to 15 November. The target week's z-score against the twelve baseline weeks (sample standard deviation) and its rank among the thirteen. The same from raw counts, and the same over distinct titles. 16 and 17 November as two daily values beside the baseline's daily mean.
2. **The same for `ATT_T`.**
3. **The headline framing share.** `BOTH_T` divided by `OUT_TECH`. Pooled over the baseline; pooled over 13 to 17 November; the twelve weekly baseline values (lowest, median, highest) and the z-score of 9 to 15 November against them; each day from 9 November. The same with `BOTH_T_STRICT`. And the comparison part N2 registered: 2 to 12 November against 13 to 17 November.
4. **The theme framing share.** Statistic 3 again with `BOTH_TH` and `BOTH_TH_STRICT`. This is the nearest this table comes to the third round's statistic 3.
5. **The multiplier.** (Target week's coverage ÷ baseline mean coverage) ÷ (target week's outside count ÷ baseline mean outside count), with coverage from statistic 1 and the outside count from the U.S. column of `a_instrument.csv`, as in the third round's statistic 4.
6. **What the exclusion removes.** `OUT_TECH` as a share of `OUT_T`, and `OUT_TECH_TH` as a share of `OUT_T`, baseline against after.
7. **Against the search API.** For the days the API returned with a `norm` of at least 20% of its median: the rank correlation between the API's daily `OUT_IT` share and this table's daily `OUT_TECH` share. And for every day the API returned, its `norm` beside this table's U.S. row count. Descriptive only; nothing is decided by it.

No statistic has a pass mark. The write-up gives the numbers and says which row of the table in `PROTOCOL-3.md` (a real cluster, a news wave, a frequency illusion) each is consistent with.

**Chart.** One figure from the script: the thirteen weeks, headline coverage and the outside count each as an index with the baseline mean at 1, and the weekly headline and theme framing shares under them.

## Known weaknesses, written before counting

- A headline is a narrow net. Most stories about an outage do not say "outage" in the title, and fewer still say "cyberattack" beside it. Counts for `BOTH_T` may be too small for a weekly z-score to mean anything; if a baseline week has fewer than 20 `OUT_TECH` rows, say so beside the share.
- As in the third round, a match is a word, not a claim. "Officials rule out cyberattack in outage" counts in `BOTH_T`.
- `NOT_TECH` is a guess at what marks an electricity or weather story. It will drop "Microsoft outage hits utilities" and keep "outage" stories about electricity that never say "power". `OUT_TECH_TH` is the check on it, and it has the opposite fault: nobody here knows what makes GDELT assign a power theme.
- Themes are GDELT's machine tags. Their rules are not published in a form checked here, and they can change.
- "hack" matches a golfer and a life hack. `ATT_STRICT` leaves it out.
- One event in the after period was a real attack, found on 16 November. Stories about it raise `ATT_T` honestly.
- The day is GDELT's processing day. A story published late on the 12th can land on the 13th.
- The U.S. filter uses a 2018 lookup. The all-countries figures are the check.
- A wire story on two hundred sites is two hundred rows. The distinct-title counts are the check.
- Twelve baseline weeks from one autumn, with hurricane season in them. `NOT_TECH` removes the word "hurricane", not the season.
- Some results from the search API were seen before this was written, as listed above, including two after-period values. The patterns here were taken from the third round and not tuned to them, but the reader should know.

## Reporting

Counts come from `measurements/bulk_analyze.py`, which reads `bulk_queries.json` and the table, and writes the daily counts to `bulk_series.csv` and its printed output to `bulk_analyze-output.txt`. The script is to be written and tested on made-up rows before it is pointed at the table. Results go in `RESULTS-4.md`, with every departure from this file listed, beside the third round's results in `RESULTS-3.md`.
