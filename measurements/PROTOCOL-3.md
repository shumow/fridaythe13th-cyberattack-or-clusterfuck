# Reclassified outages: protocol

Written and committed on 18 November 2026, before any of the searching below. Asked for by Dan on 17 November and approved on the 18th. `PROTOCOL.md` and `PROTOCOL-2.md` stay as they are. Model v1 was frozen at 10:00 UTC today; nothing here changes it. The results are for version 2.

## Questions

1. When an organisation's first public account of an outage is not an attack ("technical issue", "no evidence of a cyberattack"), how often is the outage later acknowledged to be an attack?
2. When that happens, how long does it take? Model v1 assumes a median of 4 days for an honestly premature account to correct itself. That number was a judgment.
3. Who corrects the account: the organisation, a regulator or court filing, or the press?

## What had been seen when this was written

Nothing was searched for this. From the model's own recall, and not checked, these outages are believed to have started with a non-attack account and ended as attacks: Rackspace hosted Exchange (December 2022), Seattle-Tacoma airport (August 2024), Ingram Micro (July 2025), Marks & Spencer (April 2025), Collins Aerospace airport check-in (September 2025). They are listed so that a reader knows what the searcher expected to find. They enter the results only if a search below returns them and an opened page confirms them. From this repo: the two October 2026 federal incidents in `bycatch.csv`, which were described as security incidents from the first public notice and so are not reclassifications.

## Definitions

- **Outage.** An IT or communications system at a named organisation down or degraded for customers, staff or the public for at least 30 minutes.
- **First account.** The earliest public statement about the cause by the organisation or by officials speaking for it, as quoted on an opened page.
- **Non-attack first account.** One that gives a benign cause, or says there is no evidence or indication of an attack, or describes only a "technical", "system", "network" or "IT" issue without mentioning security. A first account that says "cybersecurity incident" or "unauthorised activity" is an attack account, and the event is not a reclassification.
- **Reclassified.** A later public acknowledgment, by the organisation, a regulator, a court or securities filing, or law enforcement, that the outage was caused by an attack. A press report citing unnamed sources is recorded as "reported, not acknowledged" and counted separately.
- **Delay.** Days from the first account to the first acknowledgment. If only the outage's start is dated, days from the start, marked as such.
- **Window.** Outages beginning 1 January 2019 to 8 November 2026. Any country; the organisation's country is recorded, and results are given for all and for U.S. only.

## Part R1. Looking for reclassified outages (gives the delay)

Eight web searches, extended mode, no domain filter, these exact strings:

1. `outage initially blamed on technical issue later confirmed cyberattack`
2. `company first said "technical issue" later confirmed ransomware attack outage`
3. `"no evidence of a cyberattack" outage later revealed to be a cyberattack`
4. `"system outage" later disclosed as cybersecurity incident SEC filing 8-K`
5. `airline airport outage "technical issue" later confirmed cyberattack`
6. `bank payment outage initially called glitch later confirmed cyberattack`
7. `hospital health system "IT outage" later confirmed ransomware`
8. `government agency outage "technical difficulties" later confirmed hack`

Every result is saved with its title and link. A result is a candidate when its title or summary names an organisation and suggests a changed account. For each candidate, open at most two pages to fix the first account, its date, the acknowledgment and its date. Open at most 30 pages in all, taking candidates in the order the searches return them. A candidate that cannot be fixed within the budget is listed as unresolved.

**Statistic.** For reclassified events with both dates: the number, the median delay, the quartiles and the range; the share acknowledged within 4 days and within 14 days; the split by who corrected. The same for U.S. organisations only. A bootstrap interval for the median if there are at least 8 events; otherwise the values are listed and no interval is given.

**What this cannot give.** A rate. The searches find cases that were written up as reversals, which favours large, slow and embarrassing ones. Fast corrections within a day may not be written up as reversals at all, so the delay will be biased long. Attacks whose account never changed are invisible by construction, which is the model's "stays wrong" state and the reason it has no measured number.

## Part R2. Following known outages forward (gives a rate)

**The list, fixed now.** Every row of `data/outages.csv` dated before 9 November 2026 (22 rows), the six airline groundings in `c_like_for_like.csv`, the four bank events in `c_banks.csv`, and the rows of `bycatch.csv` inside the window. Duplicates across files count once. No event is added or removed after this commit.

**For each event.** One web search, standard mode: `{organisation} outage {Month YYYY} cause`. From the results and at most one opened page, record the first account, whether it was a non-attack account, and whether any later acknowledgment of an attack exists. Events from memory with no page behind them are kept and marked.

**Statistic.** Among events whose first account was a non-attack account: the number later reclassified, the share, and a Wilson interval; if the number is zero, the rule-of-three upper bound. Given for all and by class where a class has at least 5 events.

**What this cannot give.** A rate for outages in general. The list was built from "biggest outages" roundups, memory and three accidental searches. It is the list the rest of this repo uses, which is why it is the one followed.

## Part R3. Reports that gather around a big outage (descriptive only)

Dan asked on 18 November to track knock-ons and denied reports and to see whether their number looks suspicious. This week has one knock-on and two denied-report items around two real events. For a first comparison, three earlier anchors: the FAA NOTAM ground stop of 11 January 2023, the CrowdStrike outage of 19 July 2024, and the Amazon Web Services outage of 20 October 2025.

For each anchor, two web searches, standard mode:

1. `{anchor, Month D YYYY} false reports outage denied "not affected"`
2. `{anchor, Month D YYYY} other outages same day unrelated rumor cyberattack`

Record each distinct organisation reported as down within 48 hours of the anchor that either denied it or was a knock-on of the anchor. Open at most two pages per anchor. Report the counts beside this week's. Three anchors chosen by memory are an illustration, not a baseline, and the write-up says so.

## Reporting

Queries, every result, pages opened and judgments go in `measurements/` as `r1_raw_results.csv`, `r1_events.csv`, `r2_events.csv`, `r3_reports.csv` and `r_pages_opened.csv`, with times. Pages are read through an automated reader that returns a summary and short quotes; a row says whether its page was opened or seen only as a search result. Numbers come from `measurements/reclassified.py` and are written up in `measurements/RESULTS-3.md`, with every deviation from this file listed.
