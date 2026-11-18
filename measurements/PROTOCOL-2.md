# Measuring the frequency illusion: protocol, second round

Written and committed on 17 November 2026 (Pacific), before any of the counting below. `PROTOCOL.md` stays as it was. This file replaces its part B, whose search method failed (see `RESULTS.md`), redoes the coverage step of part C with a dated archive, and adds a bank pass to part C.

What had been seen when this was written: everything in `RESULTS.md`, and the documentation of the archive named below. No query had been sent to the archive. The shell of the session that wrote this could not reach it.

Who runs what:

- Part C1 (finding past bank outages) is run by the text session that wrote this, straight after this file is committed.
- Parts B2 and C2 need a shell with network access. They are for a Claude Code session.

## The archive

GDELT's DOC 2.0 API, `https://api.gdeltproject.org/api/v2/doc/doc`, free and without a key. Facts from its documentation, read on 18 November 00:30 UTC and not yet tested:

- `query` takes words, quoted phrases, one level of `(a OR b)` groups, a minus sign to exclude, and operators such as `sourcecountry:US`, `sourcelang:english`, `domainis:nytimes.com`.
- `mode=ArtList` returns matching articles (title, URL, domain, time first seen), at most 250 per request with `maxrecords=250`. `sort=DateAsc` puts the oldest first.
- `mode=TimelineVolRaw` returns the count of matching articles per time step and, in CSV or JSON, a `norm` column with all articles monitored in that step. Steps are daily for spans over a week.
- `startdatetime` and `enddatetime` take `YYYYMMDDHHMMSS`, in UTC.
- Timelines reach back to 1 January 2017. Whether article lists reach back more than three months is unclear from the documentation. Gate 2 tests it.
- The API is rate limited and the limit is not published. Send one request at a time, wait at least 6 seconds between requests, and on a refusal wait 60 seconds and try once more.

## Gates, in order, before any sampled week is touched

1. **Network.** One request to the endpoint from the shell. If it is refused, write that in `HANDOFF.md`, push, and stop. Do not work around a refusal.
2. **Reach.** For each calibration event below, request `ArtList` for the event's day and the two days after, with that event's sector query. The gate passes for a period if at least one returned article is about the event. If article lists do not reach events older than three months, use the fallback baseline in B2 and say so.
3. **Recall.** Run the B2 procedure on the week of each calibration event. An event is found if it comes out as a counted event. Report recall by class. If a class finds fewer than half of its calibration events, report that class's weekly counts as unusable and do not compute a rate from them.

**Calibration events.** Ten dated events outside the sampled and target weeks: American Airlines, 24 Dec 2024; Education Department (StudentAid.gov), 12 Mar 2025; Zelle, 2 May 2025; Amazon Web Services, 20 Oct 2025; Microsoft Azure, 29 Oct 2025; Cloudflare, 18 Nov 2025; Cloudflare, 5 Dec 2025; Microsoft 365, 22 Jan 2026; American Airlines, 28 Jul 2026; Federal Election Commission, 26 Oct 2026.

Query syntax may be debugged on calibration weeks only. Once it works, commit the exact query strings to `measurements/b2_queries.json`, then start on the sampled weeks. No query changes after that commit.

## B2. The inclusion rule applied to past weeks

**Question.** Under one rule, how many events does an ordinary week hold, how many did the weeks of 9 and 16 November 2026 hold, and how many of each were covered nationally within 48 hours?

**Weeks.** Baseline: the 26 seeded weeks printed by `python3 measurements/sample_weeks.py`, all of them. Target: the weeks of 9 and 16 November 2026. The week of 16 November is counted up to the time of the run; record that time. Fallback, if Gate 2 fails for older periods: the twelve weeks from 17 August to 8 November 2026 as the baseline, all twelve.

**Organisations searched.** The panel in `model/model_v1.json`, with these search names. Federal systems cannot be searched as "any agency", so a fixed list stands in for them; an outage at an agency off the list is missed in every week alike.

- Airlines and rail: American Airlines, Delta Air Lines, United Airlines, Southwest Airlines, Alaska Airlines, Hawaiian Airlines, JetBlue, Spirit Airlines, Frontier Airlines, Allegiant, Sun Country, Amtrak.
- Banks and payments: JPMorgan, Chase Bank, Bank of America, Citibank, Wells Fargo, U.S. Bank, PNC, Truist, Capital One, Goldman Sachs, TD Bank, Visa, Mastercard, American Express, Zelle, Fedwire, FedACH, FedNow, The Clearing House.
- Telecom: Verizon, AT&T, T-Mobile, Comcast, Xfinity, Charter, Spectrum, Starlink.
- Cloud: Amazon Web Services, AWS, Microsoft 365, Azure, Outlook, Google Cloud, Google Workspace, Gmail, Cloudflare, Akamai, Fastly, Oracle Cloud.
- Markets: New York Stock Exchange, NYSE, Nasdaq, CME, DTCC.
- Federal: FAA, IRS, Social Security, Veterans Affairs, StudentAid, FAFSA, Education Department, State Department, Customs and Border Protection, TSA, Postal Service, National Weather Service, NOAA, Medicare, HealthCare.gov, FEMA, Pentagon, Defense Department, NSA, FBI, Homeland Security, Treasury, Federal Reserve, SEC, EDGAR, FCC, USCIS, PACER, federal courts, Federal Election Commission, Login.gov, SAM.gov, Census Bureau, NASA, CDC, FDA, Justice Department.

**Outage words.** outage, outages, "ground stop", "technology issue", "technical issue", "system failure", "systems down", glitch, "service disruption", offline, cyberattack, "cyber incident", "cybersecurity incident". Attack words are in the list because the rule counts systems that went down, whatever the cause.

**Requests.** For each week, the window runs from Monday 00:00 UTC to the Wednesday nine days later, so that reports of a Sunday event are caught. For each sector, `ArtList` with the query `(names) (outage words) sourcecountry:US sourcelang:english`, `maxrecords=250`, `sort=DateAsc`. If the names do not fit one query, split them into groups in list order; the split is fixed by the commit of `b2_queries.json`. If a request returns 250 articles, halve its window and repeat, down to six hours; a six-hour window that still returns 250 is kept and flagged as saturated.

**Counting, by script.** Keep an article when its title contains a search name and an outage word. Group kept articles by organisation and by the date of the earliest article. Each group is a candidate.

**Judging, by reading.** For each candidate open at most two articles, the earliest from two different domains. It is a counted event when the articles show an IT or communications system at the organisation down or degraded for at least 30 minutes, beginning inside the Monday-to-Sunday week. Record the sentence that fixes the date and the one that fixes the duration. If the duration is not stated the event is a candidate, counted separately. An event caused by another counted event is marked as a knock-on and counted separately. An outage that the organisation denies is marked as denied and counted separately. The same written rule applies to every week. A random fifth of all candidates, drawn with seed 20261117, is judged a second time by a separate agent that does not see the first verdicts; report the agreement.

**National coverage.** For each counted event, one more `ArtList` request for the organisation's names and the outage words over the three days from the event's date. The event has national coverage if a national outlet's own domain (the list in `PROTOCOL.md`) has an article whose title names the organisation, first seen within 48 hours of the earliest article about the event. Record the number of distinct national domains and the number of distinct U.S. domains.

**The coverage series.** Separately from events: `TimelineVolRaw` for each sector query over 11 November 2024 to 22 November 2026, summed by Monday-to-Sunday week, with `norm`. If the full span is refused, request it by quarter.

**Statistics, fixed now.**

1. Counted events per week: the 26 baseline values, their mean and variance, and the two target values. For each target week, its rank among the baseline weeks and the Poisson tail probability at the baseline mean. Give the same with candidates included, and with knock-ons and denied reports excluded.
2. The share of counted events with national coverage, baseline against target, with Wilson intervals.
3. Weekly coverage volume from the series, as matching articles and as a share of `norm`: each target week's z-score against the 26 baseline weeks and its rank among all weeks in the span.
4. The gap the whole exercise is after: (target coverage ÷ baseline mean coverage) ÷ (target events ÷ baseline mean events). Above 1 means coverage rose more than events did.
5. Recall on the known events that fall inside sampled weeks: Microsoft, 1 Mar 2025; the federal health record system, 4 Mar 2025; United, 6 Aug 2025; United, 23 Sep 2025; JetBlue, 10 Mar 2026; Southwest, 9 Oct 2026; the Bankruptcy Noticing Center, 9 Oct 2026. Two more are known only from memory: Starlink, 24 Jul 2025, and Verizon, 14 Jan 2026. None of these is to be looked up before the count.

**Known weaknesses.** The archive holds what its crawlers saw, in machine translation for other languages, and its coverage of any one outlet can change over two years; `norm` corrects for volume, not for which outlets were crawled. Title matching misses stories whose headline does not name the organisation. The judge can see which weeks are the target weeks. The federal list is a stand-in.

## C1. Like for like, banks: finding the comparable events

**The comparison.** JPMorgan Chase on 16 November 2026: online banking slowed for most of a day.

**Comparable event.** A bank or payment network on the panel whose online banking, mobile app, cards or transfers were down or degraded for customers across the country for three hours or more, dated 11 November 2024 to 8 November 2026.

**Search.** Three web searches, standard mode, restricted to trade sites that report bank outages at a low bar (americanbanker.com, bankingdive.com, paymentsdive.com, pymnts.com, finextra.com, thefinancialbrand.com, bankautomationnews.com, ciodive.com):

1. `bank online banking outage customers unable to access accounts`
2. `Chase Bank of America Wells Fargo Citi outage mobile app down`
3. `Zelle Capital One TD Bank Truist PNC U.S. Bank outage payments down`

If the tool refuses the site filter, run the same three queries without it. Open at most ten pages to fix dates and durations. Keep every event that meets the rule, mark those whose duration is not confirmed, and take the five most recent confirmed ones for the coverage step.

**Coverage, old method, for comparison with the airline pass only.** One unfiltered web search per kept event, `{bank} outage {Month D, YYYY}`, counting national outlets' own domains and wire or network copies among the results.

**Rail and federal passes are dropped for now.** The Amtrak outage turned out to belong to the ground stop itself, and a classified network has no comparable public record.

## C2. Like for like: coverage within 48 hours, by the archive

For each event in `c_like_for_like.csv` and in the bank list from C1, the national-coverage request described under B2. Report, for airlines and for banks, the share of events with national coverage and the median number of national domains, with Wilson intervals.

## A. The outside counter: finish

Re-read Network World's 2026 report. If it has an entry for 9 to 15 November, enter the U.S. and global counts in the target row of `a_instrument.csv`, rerun `analyze.py` and update `RESULTS.md`. Nothing else about A changes.

## Reporting

Save every request (URL, time, HTTP status, SHA-256 of the response) in `measurements/b2_requests.csv`. Commit the raw responses, gzipped, if they come to under 20 MB in all; otherwise commit only the hashes and say where the responses are kept. Candidates and verdicts go in `measurements/b2_candidates.csv`, counted events in `measurements/b2_events.csv`, the weekly series in `measurements/b2_series.csv`. Numbers are produced by a script under `measurements/` and written up in `measurements/RESULTS-2.md`, with every deviation from this file listed.
