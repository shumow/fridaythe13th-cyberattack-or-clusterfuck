# The news wave: third round, first night

Wednesday 18 November 2026, 06:30 UTC (Tuesday night, Pacific). The protocol is `PROTOCOL-3.md`, committed and pushed at 06:16 UTC, before the first request at 06:17. Numbers below are printed by `python3 measurements/nw_analyze.py` (saved in `nw_analyze-output.txt`) and by `python3 measurements/analyze.py`. Nothing here is on `main`, nothing has been run through the model, and the model is still a draft.

> **Update, 18 November 2026, 19:20 UTC.** N1 has since been answered and analysed. Everything from here to the addendum at the end is the first night's account, left as written. The Coverage row below is superseded by that addendum.

## Where things stand

| Rate | Counter | Status | What it says so far |
| --- | --- | --- | --- |
| Events | The outside counter (part A) | The week of the ground stop is now published | An ordinary week |
| Coverage | The news archive (N1, N2) | Not measured. The gate did not pass | Nothing |
| What one reader sees | None | Not measured. Shelved | Nothing |

The news wave is still not measured. Its ratio needs both of the first two rows, and one exists.

## Events: the outside counter now has the week

Network World's running page is now dated 17 November and has an entry for 9 to 15 November. It was read twice with differently worded instructions, and the two reads agree: 419 outages worldwide and 282 in the United States. The page puts that at 7% fewer worldwide than the week before and 21% more in the United States (234 the week before). There is no entry yet for 16 to 22 November.

- **By the first protocol's statistic.** Against the eight weeks from 14 September, mean 263.4 and standard deviation 85.6: z = 0.22. That reads "ordinary". It ranks 19th of the 46 weeks of 2026 published so far.
- **By this round's baseline.** Against the twelve weeks from 17 August, mean 323.1: the week stands at 0.87 times the baseline, z = −0.35, 8th of 13. This is the denominator of the multiplier.

So the only fixed counter in hand saw no more outages than usual in the week of the pair. Read that with `RESULTS.md` part A beside it: this counter did not rise in the weeks of the AWS, Azure or Cloudflare outages of late 2025 either, and it cannot see a private network. As summarised by the reader, its entry for the week names two outages, Microsoft's on the 12th and AT&T's on the 10th, and not the ground stop. "Ordinary" means it saw the usual number of failures on public network paths. It does not mean that no more large systems failed.

## Coverage: the gate did not pass

Two attempts at the first query, at 06:17:07 and 06:18:07 UTC. Neither reached the archive. This session's own outbound proxy refused the connection to `api.gdeltproject.org` with a 403, which its status page records as a policy denial. That is a different stop from the second round's: there the host was allowed and the archive rate-limited the address. Here the host is not allowed at all.

The protocol says to stop at that point, so nothing else was sent and no other route was tried. Both attempts are in `nw_requests.csv`.

What is ready for a session that can reach the archive, or for anyone's own machine:

```
python3 measurements/nw_fetch.py
python3 measurements/nw_analyze.py > measurements/nw_analyze-output.txt
```

The first sends the five requests of N1 and writes `nw_series.csv`. The second prints every statistic in the protocol and draws `news-wave.png`. Both use the standard library; the chart also needs matplotlib.

## Found on the way

- **An AT&T outage on Tuesday 10 November.** The counter's entry for the week describes an AT&T outage that affected downstream providers and customers in several regions for 50 minutes over a two-hour period. AT&T is on the panel and 50 minutes is over the rule's 30. It is not in `data/outages.csv` and has not been in any count of the week. Seen only through the reader's summary of Network World's page; not opened at source, and its national coverage is unknown. It is three days before the ground stop.
- **Two lengths for the Microsoft outage.** The same entry gives it 20 hours 25 minutes, ending about 8:55 am Eastern on the 13th. Microsoft's preliminary report gives a window of 23 hours 50 minutes. They measure different things, from outside and from inside.

Neither changes anything on `main`. Both wait for the log and the one-time revision.

## Deviations from the protocol

- `nw_analyze.py` was written after the protocol and before any archive data existed. Its arithmetic was checked on made-up counts kept outside the repo. It has never seen a real answer from the archive, so the first real run may need its parser adjusted; that would be a change of plumbing, not of any statistic.
- Part N2 (headlines) has no script yet. It is to be written once N1 has run.
- `analyze.py` had an off-by-one in the rank of a target week, which could not show until a target week had a value. Fixed.
- The first-round tallies in `analyze-output.txt` that run over "every past week" now include the week of 9 November: 88 weeks, not 87. `RESULTS.md` part A keeps the figures as written on the 17th. None of the percentages it cites changes.
- The two retrieval times entered in `a_instrument.csv` are good to a couple of minutes.

## What this bears on in the model draft

The model is not changed. One observation for decision 7 in `model/DECISIONS.md`: the outside counter reads "ordinary" for the week everyone is asking about. Whether that is evidence of anything depends on whether the counter is kept in the model at all, and its record says it should not be.

## Next

1. **N1**, from any shell that can reach the archive: the two commands above.
2. **N2**, the headline count, once N1 has run.
3. **The outside counter**, again when 16 to 22 November is published.
4. **For the log, once the model is frozen:** the AT&T outage of 10 November, after it is opened at source.

## Addendum, 18 November 2026, 19:20 UTC: N1 was answered, by a thinned archive

The five requests of N1 were answered between 10:11 and 11:13 UTC on 18 November, from Dan's own machine. `nw_analyze.py` was run on them at about 19:00 UTC; its output is in `nw_analyze-output.txt` and its chart in `news-wave.png`. No query was rejected as malformed, so the accepted forms in `nw_accepted.json` are the registered ones.

**Read this first.** The archive returned 69 of the 93 days, and on many of those its count of all articles monitored (`norm`) is a few percent of normal. Every number below is computed from what it returned, as the protocol says, and every one is weaker than it looks.

| | Usual | The week of 9 to 15 November |
| --- | --- | --- |
| Days returned | 7 | 7 |
| All articles monitored, the week | 770,000 to 960,000 in a full week | 94,151 |
| The same, 13, 14 and 15 November | about 100,000 a day | 5,213, 3,545 and 1,819 |
| `OUT_IT` articles, the week | 300 to 600 in a full week | 120 |

Missing altogether: 14 to 19 September, 26 September, 3 to 5, 7, 9 and 11 to 14 October, 28 October to 2 November, and 16 and 17 November. Five of the twelve baseline weeks have five days or fewer; the weeks of 5 and 26 October have 2 and 3 `OUT_IT` articles between them. The after period, 13 to 17 November, is three days, not five.

### The registered statistics

| Statistic | Twelve baseline weeks | 9 to 15 November | Against baseline |
| --- | --- | --- | --- |
| 1. `OUT_IT` per 10,000 monitored | mean 4.56, range 1.80 to 7.45 | 12.75 | 2.80 times; z = +5.4; rank 1 of 13 |
| 1. `OUT_IT`, raw count | mean 256 a week | 120 | z = −0.7; rank 9 of 13 |
| 2. `ATT` per 10,000 monitored | mean 11.87, range 6.18 to 22.77 | 16.25 | 1.37 times; z = +1.0; rank 2 of 13 |
| 2. `ATT`, raw count | mean 652 a week | 153 | z = −1.0; rank 9 of 13 |
| 3. Framing share, `BOTH` / `OUT_IT` | pooled 8.8%; weeks 0.0% to 16.7%, median 7.1% | 29.2% (35 of 120) | z = +3.9; rank 1 of 13 |
| 3. The same, `BOTH_STRICT` | pooled 5.9%; weeks 0.0% to 14.7%, median 3.7% | 28.3% | z = +4.7; rank 1 of 13 |
| 4. The multiplier | | 3.20 | coverage at 2.80 times, the outside counter at 0.87 |
| 5. `OUT_IT` as a share of `OUT_PLAIN` | 42.7% | 75.6% over 13 to 15 November | |

Pooled over 13 to 15 November, the framing share is 35.6% (32 of 90).

By day, `BOTH` over `OUT_IT`: 0/2, 1/10, 2/9 and 0/9 on the 9th to the 12th; 4/26, 24/57 and 4/7 on the 13th to the 15th. Nothing for the 16th or 17th.

### What can be said

- **The rate and the count disagree, and the archive is why.** Per article monitored, outage coverage was 2.8 times baseline; in raw articles it was under half. The raw count measures the hole in the archive. The rate is the registered statistic, and it holds only if the articles the archive kept that week are a fair sample of the ones it lost. Nothing here tests that.
- **The framing share is the sturdier result, and it agrees with the bulk table.** A share of outage articles does not depend on how many articles the archive kept, only on which. It reads 29% in the week of the pair against 9% at baseline. The fourth round's theme measure, from a complete table and a different method, reads 30% against 8% (`RESULTS-4.md`). Two instruments, about the same answer.
- **It rests on 35 articles.** And 24 of those are from one day, the 14th.
- **The multiplier here is 3.2; the bulk table's is 28 to 86.** They are not the same quantity. This one counts articles that mention an outage anywhere in the text; that one counts headlines. Text mentions of "outage" are common in ordinary weeks, so the baseline is higher and the ratio smaller. The thinned archive may also understate the rise. Neither number should be quoted without saying which it is.
- **Attack coverage is not clearly up:** 1.37 times baseline per article monitored, second of thirteen, z about +1, with the after period's two fullest days missing.

As in `PROTOCOL-3.md`: a match is a word and not a claim, the counter in the multiplier is a weak witness, and twelve weeks from one autumn are a thin baseline.

### Part N2

Not run. The protocol allows it only if all five requests of N1 were answered without a refusal, and they were refused eleven times during the overnight run before all five were answered. Its one statistic, the share of outage headlines that reach for an attack, was computed from the bulk table instead and is in `RESULTS-4.md`, section 3.

### Departures from the protocol, this addendum

- **The gate rule was set aside twice, at Dan's instruction.** After two refusals the protocol says to stop, with no third attempt and no other route. A third attempt was made with waits of 30 and 60 seconds, and then `nw_fetch.py --overnight` asked every 15 minutes until each query was answered. After the first night's two attempts, that is 21 more: 16 refused with HTTP 429 and 5 answered. Every one is in `nw_requests.csv`. The queries, periods and statistics did not change.
- **The other route was taken too.** The bulk table is `PROTOCOL-4.md` and `RESULTS-4.md`.
- **Seen before this analysis was run:** the per-query totals, the daily `norm` values, and eight daily values of `BOTH_STRICT`, as listed in `PROTOCOL-4.md`. And all of `RESULTS-4.md`, which was finished first.
- **The script needed no change.** `nw_analyze.py` ran on the real answers as it was written. The chart was drawn by running it in the project's virtual environment, which has matplotlib.
- **Missing days are left out, not filled.** A week's figures come from the days the archive returned. The script does this and the protocol did not say otherwise; it matters a great deal here, so it is stated.

## Files

| File | What it holds |
| --- | --- |
| `PROTOCOL-3.md` | The plan, committed before any request |
| `INSTRUMENTS.md` | The running list of what each counter can and cannot see, and how it can be fooled |
| `nw_queries.json` | The fixed query strings |
| `nw_fetch.py`, `nw_requests.csv` | The requests, and the log of every attempt |
| `nw_analyze.py`, `nw_analyze-output.txt` | The script behind every number here, and its output |
| `a_instrument.csv` | Now with the week of 9 to 15 November |
| `nw_series.csv`, `nw_accepted.json`, `nw_raw/`, `nw_overnight.log` | The archive's five answers, the accepted query forms, the raw bodies and the overnight run's log |
| `news-wave.png` | The chart from `nw_analyze.py` |
