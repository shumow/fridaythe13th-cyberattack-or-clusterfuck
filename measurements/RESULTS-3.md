# Reclassified outages: interim results

18 November 2026. The protocol is `PROTOCOL-3.md`, committed before any searching. Every number below is printed by `python3 measurements/reclassified.py`; its output is in `reclassified-output.txt`. Model v1 is frozen and is not changed by anything here.

## Where it stands

| Part | Status | What it says so far |
| --- | --- | --- |
| R1. Looking for reclassified outages | Eight searches run, 74 results saved. No page opened. | Twelve candidate past cases. None has both dates fixed, so there is no delay figure yet. |
| R2. Following known outages forward | Not started. | |
| R3. Reports around a big outage | Not started. | |

**No number for the 4-day median exists yet.** The model's figure is still a judgment.

## Why it stopped

Twelve pages were requested and none could be opened: this container's network rules block the hosts. The protocol fixes a date only from an opened page, so every candidate is listed as unresolved. The search tool's own summaries name dates for some of them, and those are recorded in `r1_events.csv` marked "per summary", but they are not used.

## What the searches returned

- 44 of the 74 results (59%) are about this week's outages. The searches were written to find old reversals and mostly found this week's news instead. Query 7, on hospitals, is the only one with none; it returned 0 of 10.
- The twelve candidates are: Colt Technology Services, Dish Network, Collins Aerospace, Kettering Health, McLaren Health Care, CommonSpirit Health, UMC Health System, a Maryland hospital, Foxconn in Wisconsin, National Presto Industries, the City of St. Paul, and an earlier Microsoft outage of unknown date.
- On the summaries alone, one of them (National Presto) is not a reclassification, because the first account seen already says "cybersecurity incident". UMC may be the same.
- Of the five cases the protocol said the searcher expected, one came back (Collins Aerospace). Rackspace, Seattle-Tacoma airport, Ingram Micro and Marks & Spencer did not.
- Seven of the twelve are hospitals or health systems. That is the shape of the searches, not of the world: one query asked for hospitals, and it was the only one this week's news did not swamp.

## What can be said without the pages

Only this, and loosely: cases where a "technical issue" or "IT outage" became an acknowledged ransomware attack are easy to find, and in most of the ones found the organisation itself made the correction. How fast is the open question.

## Found on the way, and logged

These came out of the searches and went into `log/log.csv` as prospective rows: a ransomware group's leak-site claim naming JPMorgan Chase, Visa and Mastercard; Visa confirming a security incident at a third-party provider; the Director of National Intelligence's account of the NSA outage; statements by Rubio; and three leads not yet checked (the FBI assisting the FAA review, Wells Fargo, Gmail).

## Deviations from the protocol

- No page was opened, so no candidate was fixed and no statistic was computed. Twelve fetches were attempted in one batch; the protocol allows two per candidate and thirty in all.
- R2 and R3 were not started. R2 would run on search results that this week's coverage is currently swamping, and both are better done once pages can be read.
- The "about" label on each raw result (this week, candidate, other) was added while saving them; the protocol did not ask for it.

## Next

1. Get page access: the twelve hosts allowed in the environment, or the run moved to a machine with open network access.
2. Open the pages for the twelve candidates and fix the dates.
3. Run R2 and R3.
