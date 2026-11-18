# The news wave: third round, first night

Wednesday 18 November 2026, 06:30 UTC (Tuesday night, Pacific). The protocol is `PROTOCOL-3.md`, committed and pushed at 06:16 UTC, before the first request at 06:17. Numbers below are printed by `python3 measurements/nw_analyze.py` (saved in `nw_analyze-output.txt`) and by `python3 measurements/analyze.py`. Nothing here is on `main`, nothing has been run through the model, and the model is still a draft.

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

## Files

| File | What it holds |
| --- | --- |
| `PROTOCOL-3.md` | The plan, committed before any request |
| `INSTRUMENTS.md` | The running list of what each counter can and cannot see, and how it can be fooled |
| `nw_queries.json` | The fixed query strings |
| `nw_fetch.py`, `nw_requests.csv` | The requests, and the log of every attempt |
| `nw_analyze.py`, `nw_analyze-output.txt` | The script behind every number here, and its output |
| `a_instrument.csv` | Now with the week of 9 to 15 November |
