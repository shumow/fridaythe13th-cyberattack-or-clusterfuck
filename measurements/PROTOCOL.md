# Measuring the frequency illusion: protocol

Written and committed on 17 November 2026, before any of the counting below was done. Frequency illusion means the events did not get more common, the noticing did. So each measurement needs a counter that does not follow the news.

These are measurements the model will consume. They are not model rules, so they can run before the model is frozen. Nothing here goes on `main` until the model is settled.

What had already been seen when this was written: the titles of one search for an outage-tracking series, including one that reads "Internet outages increase 14% in mid-November". No counts.

## A. A fixed-threshold instrument

**Question.** Did a counter that was already running, with its own fixed method, see more outages in the week of the ground stop than in the weeks before?

**Source, in order of preference.** ThousandEyes' weekly U.S. outage counts as recorded in Network World's running 2026 outage report; failing that, ThousandEyes' own posts; failing that, any other weekly series with a published method.

**Data.** The U.S. count and the global count for every week from 14 September 2026 to the latest published. Baseline: the eight complete weeks from 14 September to 8 November. Target: the week of 9 to 15 November, and 16 to 22 November once published. If the source's weeks are cut differently, use its own weeks containing 12 and 13 November.

**Statistic.** z = (target − baseline mean) / baseline sample standard deviation. Also the target's rank among all the 2026 weeks the source gives.

**Reading.** Below 1: ordinary. 1 to 2: mildly high. 2 or more: elevated.

**Known weakness.** It watches network paths to internet-facing services. A bank's internal bug, an airline's dispatch system or a classified network would not register.

## B. The inclusion rule applied backwards

**Question.** Under one rule, fixed first, how many events does an ordinary week hold, and how many of them made national news?

**Qualifying event.** An organisation on the panel in `model/model_v1.json`; an IT or communications system down or degraded for at least 30 minutes; reported by any published source. Coverage is recorded separately and is not part of qualifying.

**National coverage.** At least one search result about the event from a national outlet's own domain: apnews.com, reuters.com, bloomberg.com, nytimes.com, wsj.com, washingtonpost.com, cnn.com, nbcnews.com, abcnews.go.com, abcnews.com, cbsnews.com, foxnews.com, npr.org, cnbc.com, usatoday.com, axios.com, time.com.

**Weeks.** Monday to Sunday. Baseline weeks come from `measurements/sample_weeks.py`: 26 of the 104 weeks from 11 November 2024 to 2 November 2026, drawn with a fixed seed, in a fixed order. Target weeks: 9 to 15 November 2026 and 16 to 22 November 2026 (partial).

**Search method, identical for every week.** One web search per sector per week, standard mode, no domain filters, with these exact templates, where the date is the Monday:

1. `airline Amtrak system outage ground stop technology issue week of {Month D, YYYY}`
2. `bank outage online banking payments Zelle down week of {Month D, YYYY}`
3. `cloud internet outage AWS Azure Google Cloud Cloudflare Microsoft 365 Verizon AT&T T-Mobile week of {Month D, YYYY}`
4. `federal government agency computer system outage down week of {Month D, YYYY}`

**Counting.** Only what the search returns counts. Nothing is added from memory or from what is already known about a week, the target weeks included. A result counts toward an event when its title names a panel organisation and an outage, and the event falls inside the week. When the title leaves the date or the organisation unclear, the page may be opened, at most two pages per week. Events are deduplicated by organisation and day. Duration is recorded as confirmed only when a title or an opened page states it; otherwise the event is a candidate.

**Statistic.** Qualifying events per week, candidates and confirmed, and the share with national coverage, baseline against target.

**Pilot.** The first two baseline weeks of the list and both target weeks: sixteen searches. A full run takes all 26.

**Known weaknesses.** Search engines favour recent pages, so an old quiet week may return less for the same effort; the pilot is partly a test of that. A title-only count misses events whose headlines do not name the organisation. Two baseline weeks give a rate with very wide error.

## C. Like for like

**Question.** Would this week's smaller events have been national news in an ordinary week?

**This pass: airlines.** The comparison event is United's outage of 16 November 2026: a top-ten U.S. airline, a system-wide technology disruption, between 30 minutes and 3 hours.

**Step 1, find comparable events without leaning on national coverage.** Three web searches, standard mode, restricted to trade and enthusiast sites that report airline disruptions at a low bar (viewfromthewing.com, simpleflying.com, onemileatatime.com, paddleyourownkanoo.com, aerotime.aero, thepointsguy.com, liveandletsfly.com, airlive.net):

1. `United Airlines ground stop technology issue`
2. `American Airlines Delta ground stop technology issue outage`
3. `Southwest Alaska Airlines JetBlue ground stop technology issue outage`

Keep events at a panel airline dated 11 November 2024 to 8 November 2026 whose title or page indicates a system-wide technology disruption of 3 hours or less. Take the five most recent.

**Step 2, measure coverage.** For each kept event, one web search restricted to the national outlets' domains listed under B: `{airline} outage ground stop {Month D, YYYY}`. Count the distinct national outlets with a story on it.

**Statistic.** The share of comparable events with at least one national outlet, and the median number of outlets.

**Known weaknesses.** Five cases. Trade sites have their own threshold. A search today cannot tell a story published within 48 hours from a later one unless the page is opened.

**Next passes, same shape.** Banks (the comparison is Chase on 16 November), rail, and federal systems.

## Reporting

Every search query, every result counted and every judgment call goes in `measurements/` as CSV, with the date and time it was run. Results are written up in `measurements/RESULTS.md`.
