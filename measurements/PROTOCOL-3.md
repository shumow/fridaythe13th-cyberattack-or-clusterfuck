# Measuring the news wave: protocol, third round

Written and committed on 17 November 2026 (Pacific), before any of the counting below. `PROTOCOL.md` and `PROTOCOL-2.md` stay as they were. This file adds a vocabulary, one new measurement (how often an outage story reaches for the word "cyberattack") and a short-query version of the coverage series. It takes nothing away from the second round, whose parts B2 and C2 are still to run.

What had been seen when this was written: everything in `RESULTS.md`, including the outside counter's 95 weekly values up to 8 November; the second round's request log (26 attempts, two answers, both a syntax error, no counts); and the titles of one web search made by voice on the evening of 17 November for the ground stop and the Microsoft outage. No count from the news archive, for any query, for any day.

## Three rates, three explanations

Until today this folder used "frequency illusion" for the whole question. The piece now separates three things, because they have three different counters (Dan, by voice, 17 November):

| What happened | Events | Coverage | What one reader sees |
| --- | --- | --- | --- |
| A real cluster | up | up | up |
| A news wave | flat | up | up |
| Frequency illusion | flat | flat | up, or unchanged and only noticed more |

- **Events**: how many systems failed. Counted by the outside counter (part A, in hand, a weak witness) and by the second round's counted events (part B2, not run yet).
- **Coverage**: how many stories were published. Counted here.
- **What one reader sees**: how many of those stories reached one person. Not measured. A tool for it was considered and shelved; `INSTRUMENTS.md` says why.

The rows are not exclusive: events and coverage can both rise. The ratio in statistic 4 says by how much coverage outran events.

"News wave" is the name the piece uses for the middle row. The older names for it are listed in `INSTRUMENTS.md`.

## The archive

GDELT's DOC 2.0 API, as in `PROTOCOL-2.md`: one request at a time, at least 6.5 seconds apart, and on a refusal one more try after 60 seconds. Every attempt is logged to `nw_requests.csv` and every answered body is kept, gzipped, in `nw_raw/`. `nw_fetch.py` does this by reusing `b2_fetch.py` with its own log and folder.

**The gate.** The first request below is the gate. If it is refused twice, stop: add a dated line to `HANDOFF.md` and leave the rest for a session whose address the archive answers. No third attempt and no other route to the same data.

**Why not the second round's queries.** They carry up to nineteen organisation names and thirteen outage words each, and the archive answered the only two that got through with "too short or too long". Fixing them belongs to the second round and its calibration weeks. The queries here name no organisation, so they count outage stories in general, not stories about the panel.

## N1. The coverage series

**Queries.** Fixed in `nw_queries.json`, committed with this file. Each has ` sourcecountry:US sourcelang:english` appended. Two groups side by side mean both must match.

| Name | Query |
| --- | --- |
| `OUT_IT` | `(outage OR outages OR "ground stop") (network OR internet OR software OR online OR website OR systems)` |
| `BOTH` | `OUT_IT` and `(cyberattack OR cyberattacks OR "cyber attack" OR hack OR hacked OR hackers)` |
| `ATT` | `(cyberattack OR cyberattacks OR "cyber attack" OR hack OR hacked OR hackers)` |
| `BOTH_STRICT` | `OUT_IT` and `(cyberattack OR cyberattacks OR "cyber attack")` |
| `OUT_PLAIN` | `(outage OR outages OR "ground stop")` |

The second group in `OUT_IT` is there because "outage" in American news is mostly electricity and "ground stop" is mostly weather. `OUT_PLAIN` is run last to show how much that group removes.

**Requests.** In the order of the table, one each: `mode=TimelineVolRaw`, `format=json`, `startdatetime=20260817000000`, `enddatetime=20261118000000`. That is 93 UTC days, 17 August to 17 November 2026. Five requests in all.

**If a query is rejected as malformed.** A rejection carries no counts. Drop the last term of the query's last group and send it again, and repeat until it is accepted. Record every rejected form. The accepted form is then used for every period alike.

**Periods.** Days are UTC days.

- Baseline: the twelve Monday-to-Sunday weeks from 17 August to 8 November, the same twelve as the second round's fallback baseline.
- The week of the pair: 9 to 15 November. The Microsoft outage began on the 12th at 16:17 UTC and the ground stop on the 13th at 20:54 UTC.
- After: 13 to 17 November, five days. The 9th to the 12th are listed day by day and belong to neither side of the before-and-after comparison.

**Statistics, fixed now.**

1. Weekly coverage: `OUT_IT` articles divided by `norm`, for each baseline week and for 9 to 15 November. The target week's z-score against the twelve baseline weeks (sample standard deviation) and its rank among the thirteen. The same from raw article counts. 16 and 17 November as two daily values beside the baseline's daily mean.
2. The same for `ATT`.
3. The framing share: `BOTH` divided by `OUT_IT`. Pooled over the baseline; pooled over 13 to 17 November; the twelve weekly baseline values (lowest, median, highest) and the z-score of 9 to 15 November against them; each day from 9 November. The same with `BOTH_STRICT`.
4. The multiplier: (target week's coverage ÷ baseline mean coverage) ÷ (target week's outside count ÷ baseline mean outside count). Coverage is statistic 1. The outside count is the U.S. column of `a_instrument.csv` over the same twelve weeks. Above 1 means coverage rose more than the counter did. If the counter has no value for 9 to 15 November the multiplier is not computed. When the second round's counted events exist, its statistic 4 replaces this one.
5. The share of `OUT_PLAIN` that `OUT_IT` keeps, baseline against after.

**Chart.** One figure from the script: the thirteen weeks, coverage and the outside count each as an index with the baseline mean at 1, and the weekly framing share under them.

## N2. Headlines

Run only if all five requests of N1 were answered without a refusal.

**Requests.** For each UTC day from 2 to 17 November 2026, sixteen days: `mode=ArtList`, the accepted `OUT_IT` query, `maxrecords=250`, `sort=DateAsc`. A day that returns 250 is requested again as four six-hour windows; a window that still returns 250 is kept and flagged as saturated.

**Counting, by script.** Titles are lower-cased and their spaces collapsed. An outage headline matches `\b(outages?|ground stop)\b`. It reaches for an attack when it also matches `\bcyber[ -]?attacks?\b|\bhack(s|ed|ers?|ing)?\b`. Counted twice: over all articles, and over distinct titles so that a syndicated story counts once.

**Statistic.** The share of outage headlines that reach for an attack: 2 to 12 November against 13 to 17 November, and each day.

## Known weaknesses, written before counting

- N1 matches the text of an article, not its claim. A story that quotes an official saying there is no sign of a cyberattack counts in `BOTH` exactly as a story alleging one does. The share measures how often the word rides along with an outage, which is what a reader meets, and cannot tell assertion from denial.
- One event in the after period was an attack: the compromise of a marketing tool on 178 organisations' websites, found on 16 November. Stories about it raise `ATT` honestly, and `BOTH` wherever they also mention the week's outages.
- "hack" also matches "life hack" and a golfer's swing. That noise should be about the same every week, and `BOTH_STRICT` leaves the word out.
- Three groups that must all match somewhere in a long article is a loose net. `OUT_IT` will keep some storm stories and drop some outage stories that never say "network".
- The archive holds what its crawlers saw. A wire story carried by two hundred station sites is two hundred articles. `norm` corrects for total volume, not for which outlets were crawled.
- Twelve baseline weeks, all from one autumn, with hurricane season in them.
- The multiplier divides by a counter that `RESULTS.md` found does not rise in weeks with a known major outage. It is the only fixed counter in hand, and the write-up must say so beside the number.
- Everything here can be gamed by someone who can publish pages the archive crawls. That is `INSTRUMENTS.md`.

## Reporting

`nw_requests.csv` and `nw_raw/` as above. The daily series goes in `nw_series.csv`, headline counts in `nw_headlines.csv`. Numbers come from `nw_analyze.py` and are written up in `RESULTS-3.md`, with every deviation from this file listed.
