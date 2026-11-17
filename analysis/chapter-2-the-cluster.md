# Chapter 2, 17 November 2026: the cluster

> "The first casualty when war comes is truth." Attributed to Senator Hiram Johnson, 1918. The attribution is traditional and poorly documented, which suits the chapter.

Friday's analysis is left exactly as it was written, in [`independence-or-common-cause.md`](independence-or-common-cause.md) and in the README. This chapter records what changed by Tuesday and what it does to the argument. Every number here comes out of [`scripts/the_week_after.py`](../scripts/the_week_after.py); its output is in [`week-after-output.txt`](week-after-output.txt).

## The short version

- Both of Friday's outages now have an account on the record, and the accounts do not share a vendor, a change or a mechanism. The same-vendor-update branch is closed on what is public.
- The week added a bank outage, a reported outage of the NSA's classified network, and one confirmed attack: a supply-chain compromise that put malicious code on 178 websites, including CNN, Fox News and NPR.
- Four comparable outages in five days is a 1.6% event over two years, about 2.1 sigma, at the rate fitted here. Three is a 25% event. Which of those you are looking at depends on whether the last two belong in the count, and that is a choice made after seeing them.
- Day-one denials are worth about a factor of two across all four events combined. The specific, checkable accounts are worth about a factor of twenty-five. The one outage with no checkable account, and none coming, is NSA Net.
- The news channel was attacked, but not when it mattered for the NSA story: CNN's site was clean 17.5 hours before a copy of that story was published elsewhere.

## What is now on the record

| Event | Account | Who, when | Standing |
| --- | --- | --- | --- |
| Microsoft 365, 12 to 13 Nov | A latent defect in Microsoft's own networking gateway: lock contention on Windows servers under load, introduced by a fix rolled out worldwide since July 2026. Triggered by a Teams traffic failover about 15 hours earlier, with nearly 14% of gateway capacity already out. Impact 16:20 UTC Thursday to 16:10 UTC Friday. | Microsoft, preliminary post-incident report, 15 Nov. Final report due after 20 Nov. | Read through two summaries, [365Fanatic](https://www.365fanatic.com/m365-outage-12-november-2026/) and [Cyber Security News](https://cybersecuritynews.com/microsoft-outage-incident-report), both opened. The report itself sits in the Microsoft 365 admin centre and was not read. |
| FAA ground stop, 13 Nov | During routine work replacing copper lines with fibre, a newly installed router at a remote FAA site flooded the network with more than 1,000 connection attempts every four to five seconds. L3Harris was doing the work. Whether it was user error, installer error or a faulty router is not established. | Transportation Secretary Duffy and FAA Administrator Bedford, news conference, 14 Nov. | [Scripps News](https://www.scrippsnews.com/life/travel/what-caused-the-faa-ground-stop-officials-point-to-router-failure), opened. [Wikipedia's article](https://en.wikipedia.org/wiki/2026_FAA_nationwide_ground_stop) adds, citing CBS News, that the routers were Cisco; citing The Guardian, that the site was in southern Arkansas; and citing Reuters, that Bedford said the maintenance link does not fully explain the root cause. Those three were not opened at their sources. |
| JPMorgan Chase, 16 Nov | A software bug in on-premise hardware systems slowed online banking from about 9 am Eastern. Other banks were affected only where a transaction touched Chase. | Chase statement; spokesman Joe Evangelisti on record. | [Tech Times](https://www.techtimes.com/articles/330883/20261117/chase-outage-bank-says-premise-hardware-bug-slowed-rival-banks-only-through-chase-transactions.htm), opened, relaying AP, Reuters and Barron's. |
| NSA Net, reported 17 Nov | The NSA's classified internal network is down. No cause given. No evidence of a cyberattack "at this point". Staff arrivals staggered. | Six unnamed people, to CNN. No NSA statement. | [WRAL's copy of the CNN Wire story](https://www.wral.com/news/local/national-security-communications-network-outage-november-2026/), opened. A [Jerusalem Post](https://www.jpost.com/international/article-915216) page relaying CNN was opened; its headline credits the Wall Street Journal with a software-update explanation, but the page text as fetched does not mention it. The Journal's own report was seen only as a headline. |
| Optimizely, 16 Nov | Attacker code was written into customers' Optimizely project JavaScript and served on 178 organisations' sites. It swapped cryptocurrency addresses, skimmed cards, stole cookies, and pushed iOS exploit kits. First seen 04:21 UTC; monitored snippets clean by 23:11 UTC. How the attacker got in is not known. | Report URI (Scott Helme); confirmed by Optimizely. | [Report URI](https://blog.report-uri.com/worlds-largest-brands-infected-with-malware-via-optimizely/) and [Malwarebytes](https://www.malwarebytes.com/blog/news/2026/11/cnn-bbc-zoom-and-other-sites-served-malicious-code-in-supply-chain-attack), both opened. |
| Mullin, 16 or 17 Nov | Says with "98 percent certainty" this is not a cyberattack and that nothing points to the events being connected. Relays an unnamed expert's view that an AI system overloaded older FAA systems; the FAA has denied that its AI tool caused the outage. | Homeland Security Secretary Mullin. | [Townhall via WCBM](https://wcbm.com/national-headline/markwayne-mullin-addresses-fears-of-a-cyberattack-after-a-string-of-major-us-outages/), opened. The Fox News page was not opened. |

Not re-verified and no longer bearing on the question: Microsoft's out-of-band fix for Windows activation failures. Microsoft's own account puts the faulty change in July, not on Patch Tuesday.

## What this does to Friday

Friday's text stays as written. These are the points on which it is now known to be wrong, outdated or settled.

| Friday said | Now |
| --- | --- |
| The ground stop landed inside an open Microsoft incident. | Microsoft's impact ended at 16:10 UTC on Friday, 4 hours 44 minutes before the ground stop. The incident records stayed open for administrative reasons. |
| Microsoft's change may have shipped on Patch Tuesday and propagated in stages. | Right about the shape, wrong about the date. The change was a gateway fix rolled out since July; it sat for more than three months before a traffic shift exposed it. |
| The same vendor update on both sides is open; Arista's advisory is a candidate. | Microsoft's failure was in its own Windows-based gateway software. The FAA's was a router in a copper-to-fibre job, reportedly Cisco. No shared vendor, no shared update. Closed on the public accounts. |
| The only path left runs through the contractors' own email and chat. | Weaker still. Microsoft's impact was over before the FAA work failed, and the FAA mechanism is a router flooding a network, not a coordination failure. |
| Two production networks were changed by their owners and fell over. | Stands, and is now on the record for both. |
| The Friday superstition covers the FAA side only. | Stands. The FAA work was on Friday. Microsoft's trigger was a Wednesday-night failover onto a three-month-old defect. |

The one-time revision of Friday's numbers still waits. Microsoft's report is preliminary and the FAA's cause is unconfirmed.

## The hypotheses, restated for a cluster

- **H_ind:** independent failures, honestly described.
- **H_prem:** at least one denial is honest but premature; something else will turn up.
- **H_coord:** the denials are coordinated cover for one campaign.

## How unusual is four in five days?

**Definition.** A "major outage" is a failure lasting hours, reported nationally, of a U.S. cloud platform, telecom carrier, aviation system, bank or payment rail, or federal network. That is tier A in [`data/outages.csv`](../data/outages.csv). Tier B adds large consumer platforms and events described only in passing.

**The count.** 28 rows from 17 November 2024 to 17 November 2026: 22 before this week, 6 this week. The list is thin after January 2026, so the rate is fitted on the 440 days that are well covered: 12.4 per year for tier A, 16.6 per year for both tiers.

**The test.** Simulate two years of a Poisson process at rate λ, slide a five-day window along it, and record the largest count. Repeat 100,000 times. The window is free to land anywhere, so choosing it after the fact is already paid for.

| λ per year | 2 or more | 3 or more | 4 or more | 5 or more | 6 or more |
| --- | --- | --- | --- | --- | --- |
| 5 | 0.464 | 0.022 | 0.001 | 0.000 | 0.000 |
| 8 | 0.775 | 0.079 | 0.003 | 0.000 | 0.000 |
| 12 | 0.958 | 0.229 | 0.014 | 0.001 | 0.000 |
| 16 | 0.995 | 0.437 | 0.042 | 0.002 | 0.000 |
| 20 | 1.000 | 0.646 | 0.092 | 0.006 | 0.000 |
| 30 | 1.000 | 0.949 | 0.338 | 0.043 | 0.004 |
| 40 | 1.000 | 0.997 | 0.668 | 0.141 | 0.016 |
| 60 | 1.000 | 1.000 | 0.982 | 0.569 | 0.131 |

At the fitted tier A rate of 12.4 per year: three or more in five days happens in 24.9% of two-year stretches, four or more in 1.6%, which is 2.1 sigma.

**What the window does not pay for.** It pays for where the window sits. It does not pay for deciding, after the fact, which events count.

- Friday's pair alone is a 96% event. Two major outages within five days of each other happen in nearly every two-year stretch, and the list shows it: Alaska Airlines and Starlink four days apart in July 2025, AWS and Azure nine days apart in October 2025.
- Adding Chase makes three: 25%.
- Adding NSA Net makes four: 1.6%. But an outage of a classified internal network is public only because six people talked. Comparable outages in the previous two years would not be in the list at all.
- Adding United and Amtrak, which the same week's coverage also mentions, makes six. At the fitted loose rate of 16.6 per year that is essentially impossible. That says the loose list is wrong, not that the week is: the base list was built from "biggest outages" roundups, and this week's events were collected with the bar on the floor.

So the question the arithmetic cannot answer from this data is the base rate at the low bar. If nationally reported outages at U.S. banks, airlines, railways, clouds and carriers run at 30 a year, four in five days is a 34% event. At 60 a year, six in five days is 13%. That rate is measurable and has not been measured here.

**Also not modelled.** Outages are not Poisson. They share dependencies and they share attention: after a ground stop, every slow banking app is national news. Both make clusters more common than this table says.

## The denials as evidence

For each statement, the likelihood ratio is the probability of hearing it if the event was an attack, divided by the probability of hearing it if it was not. A statement that would be made either way has a ratio near one and carries no information. The ratios below are assumptions, in [`data/denials.csv`](../data/denials.csv) with the reasoning for each.

| Event | Strongest statement | Ratio |
| --- | --- | --- |
| Microsoft 365 | Day one: no indication of malicious activity | 0.9 |
| Microsoft 365 | Preliminary report with a specific internal mechanism | 0.15 |
| FAA | Day one: no indication of a nefarious act | 0.9 |
| FAA | Named officials, specific mechanism, cause still unconfirmed | 0.4 |
| Chase | Same-day company statement, loose mechanism | 0.7 |
| NSA Net | Unnamed sources: no evidence at this point | 0.9 |
| All | Mullin: 98 percent certainty, the homeland is secure | 1.0 |

Against the hypothesis that all four were attacks, the day-one denials multiply to 0.51. The strongest statement per event multiplies to 0.038. A generic denial is nearly worthless and four of them are worth a factor of two. A published mechanism that customers and engineers can check is worth far more, and two of the four events now have one.

The ratios do not rescue the weakest link. NSA Net has the least informative denial, the least checkable account, and no root cause will ever be published. If residual suspicion belongs anywhere, it belongs there, and it will stay there.

## Is the news itself intact?

The channel was attacked. The question is whether that touches any of the four stories.

- **Who was hit.** Ten of the 178 organisations are news and media. Three large U.S. news sites are among them: CNN, Fox News and NPR. Against an assumed reference list of ten large U.S. news sites, that is 30%. In Report URI's sweep, 186 of 1,611 monitored Optimizely snippets were infected, 11.5%.
- **What the code could do.** It could change what a visitor sees: Report URI says the address swapping rewrites page text, form fields and links. What it was built to change was cryptocurrency addresses, not headlines.
- **When.** The code was live for at most 18 hours 50 minutes, from 04:21 to 23:11 UTC on Monday. The NSA story was republished by WRAL at 16:41 UTC on Tuesday, 17.5 hours after the monitored snippets were clean. The outlet with the exclusive was on the list; it was not serving attacker code when the exclusive ran.
- **The Chase story is the one that overlaps.** The outage began at about 14:00 UTC on Monday, inside the window. CNN's coverage that day went out on a site that was serving attacker code. Chase's account does not depend on CNN: AP, Reuters and Barron's carried it.
- **Out-of-band check, per story.** Microsoft: the company's own admin centre and status channels. FAA: a televised news conference. Chase: company statements to several wires. NSA Net: CNN's six sources, a syndicated wire copy that did not pass through CNN's web page, and a Wall Street Journal report seen here only as a headline.

"The outlet with the exclusive was on the hacked list" is true, has roughly a three-in-ten chance of being true for any large U.S. outlet that week, and fails on timing. The ordinary provenance problem remains: one newsroom, six unnamed sources.

## How to recreate this

Everything was done on 17 November 2026.

1. **Run the numbers.** From the repo root: `python3 scripts/the_week_after.py`. Standard library only, about 12 seconds, seed 20261117, 100,000 runs per rate. Pass a smaller number as the first argument for a quicker run. Compare with `analysis/week-after-output.txt`.
2. **The outage list.** `data/outages.csv`, one row per event. The `source_status` column says how each row is known: `opened` (the page was read), `excerpt` (seen only in a search result), or `memory` (from the model's own recall, no page). Ten of the 28 rows are `memory`. The two roundups used were the [Reuters factbox of 13 November 2026](https://www.omanobserver.om/article/1199619/business/major-tech-outages-in-recent-years) and [Tom's Guide's ten most impactful outages of 2025](https://www.tomsguide.com/computing/internet/the-10-most-impactful-outages-of-2025). To redo it properly: fix a list of organisations in advance, pull every incident above a fixed report threshold from an outage tracker for the two years, and refit.
3. **The rate.** Events before 12 November 2026, divided by days since 17 November 2024, gives a lower bound. The fitted rate uses only events up to 31 January 2026, because the list is known to be thin after that.
4. **The scan.** For each run, draw exponential gaps at rate λ/365 per day until 730 days pass, then take the largest number of events whose first and last are at most five days apart. The script prints a first-order check of the simulation.
5. **The denials.** `data/denials.csv`. Change any ratio and rerun; the script prints the products and the posterior for three priors.
6. **The Optimizely list.** `data/optimizely-affected.txt`, taken from the Report URI page through an automated summary. Check the names against the page. The reference list of ten large U.S. news sites is in the script and is an assumption.
7. **Search queries used.** "NSA classified network NSANet outage six sources no evidence of cyberattack"; "Optimizely compromise malicious JavaScript Report URI Scott Helme 178 organizations list"; "Chase outage November 16 2026 cause update own systems not cyberattack Bank of America Wells Fargo"; "Microsoft 365 outage post-incident review root cause network configuration change EX1550543 MO1550821"; "FAA ground stop November 13 root cause findings L3Harris network update Duffy statement investigation"; "NSA network outage Wall Street Journal software update NSANet cause"; "Mullin homeland is secure outages no indication cyberattack"; "Factbox major tech outages in recent years Reuters November 2026".
8. **Pages that refused an automated read.** NPR and CNBC on the FAA cause, CNN throughout, the Wall Street Journal, Fox News. Claims that rest on them are marked above.

## Still open

- The base rate of nationally reported outages at the low bar. This is the number the cluster question turns on.
- Microsoft's final report and the FAA's findings. Then revise Friday's numbers once.
- The router vendor and site on the FAA side, at source rather than through Wikipedia.
- The Wall Street Journal's NSA report, read in full: is it independent of CNN's six sources?
- A measured reference list of news sites for the overlap, in place of the assumed ten.
