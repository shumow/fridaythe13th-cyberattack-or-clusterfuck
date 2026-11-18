# Chapter 2, 17 November 2026: the cluster

> "The first casualty when war comes is truth." Attributed to Senator Hiram Johnson, 1918. The attribution is traditional and poorly documented, which suits the chapter.

Friday's analysis is left exactly as it was written, in [`independence-or-common-cause.md`](independence-or-common-cause.md) and in the README. This chapter records what changed by Tuesday and what it does to the argument. Every number here comes out of [`scripts/the_week_after.py`](../scripts/the_week_after.py); its output is in [`week-after-output.txt`](week-after-output.txt).

## The short version

- Both of Friday's outages now have an account on the record, and the accounts do not share a vendor, a change or a mechanism. The same-vendor-update branch is closed on what is public.
- The week added a bank outage, a reported outage of the NSA's classified network, and one confirmed attack: a supply-chain compromise that put malicious code on 178 websites, including CNN, Fox News and NPR.
- Four comparable outages in five days is a 1.6% event over two years, about 2.1 sigma, at the rate fitted here. Three is a 25% event. Which of those you are looking at depends on whether the last two belong in the count, and that is a choice made after seeing them.
- Day-one denials are worth about a factor of two across all four events combined. The strongest account per event is worth about a factor of thirty. Both factors are built from assumed ratios: across the ranges given for them, the first runs from 1.1 to 7 and the second from 4 to 500. The ordering holds; the size does not. The one outage with no checkable account, and none coming, is NSA Net.
- The news channel was attacked, but not when it mattered for the NSA story: CNN's site was clean 17.5 hours before a copy of that story was published elsewhere.

## What is now on the record

| Event | Account | Who, when | Standing |
| --- | --- | --- | --- |
| Microsoft 365, 12 to 13 Nov | A latent defect in Microsoft's own networking gateway: lock contention on Windows servers under load, introduced by a fix rolled out worldwide since July 2026. Triggered by a Teams traffic failover about 15 hours earlier, with nearly 14% of gateway capacity already out. Impact 16:20 UTC Thursday to 16:10 UTC Friday. | Microsoft, preliminary post-incident report, 15 Nov. Final report due after 20 Nov. | Read through two summaries, [365Fanatic](https://www.365fanatic.com/m365-outage-12-november-2026/) and [Cyber Security News](https://cybersecuritynews.com/microsoft-outage-incident-report), both opened. The report itself sits in the Microsoft 365 admin centre and was not read. |
| FAA ground stop, 13 Nov | During routine work replacing copper lines with fibre, a newly installed router at an FAA site in El Dorado, Arkansas, flooded the network with more than 1,000 connection attempts every four to five seconds, disrupting 17 of the 22 regional centres. L3Harris was doing the work. The new routers are Juniper, replacing Cisco units about 25 years old. On 17 Nov the FAA paused the installations and turned off the Juniper routers already in. The root cause is not established: whether user error, installer error or a faulty router is unknown. | Transportation Secretary Duffy and FAA Administrator Bedford, news conference, 14 Nov; FAA, 17 Nov. | [Scripps News](https://www.scrippsnews.com/life/travel/what-caused-the-faa-ground-stop-officials-point-to-router-failure), [CNBC, 14 Nov](https://www.cnbc.com/2026/11/14/root-cause-of-nationwide-ground-stop-is-unknown-faa-says.html), [CNBC, 17 Nov](https://www.cnbc.com/2026/11/17/faa-ground-stop-routers.html) and [AP via HuffPost](https://www.huffpost.com/entry/ap-us-nationwide-ground-stop_n_6afca1d4e4b0e902c23b50fc), all opened. The accounts do not agree on the equipment: [CBS News](https://www.cbsnews.com/news/faa-issues-nationwide-ground-stop/), opened, reports that the FAA believed the faulty equipment was the old Cisco 600 series routers, that its sources gave conflicting explanations, and that Mullin said on Friday night that new security patches overwhelmed the routers. Bedford, in CNBC: "We couldn't explain the instability." The Reuters report in which he is said to call the maintenance account incomplete is behind a paywall and was not opened. |
| JPMorgan Chase, 16 Nov | A software bug in on-premise hardware systems slowed online banking from about 9 am Eastern. Other banks were affected only where a transaction touched Chase. | Chase statement; spokesman Joe Evangelisti on record. | [Tech Times](https://www.techtimes.com/articles/330883/20261117/chase-outage-bank-says-premise-hardware-bug-slowed-rival-banks-only-through-chase-transactions.htm), opened, relaying AP, Reuters and Barron's. |
| NSA Net, reported 17 Nov | The NSA's classified internal network is down. No evidence of a cyberattack "at this point". Staff arrivals staggered. Later the same day, unnamed sources gave a cause: the network was offline while software was patched. One of them says it has been unstable for weeks. | Six unnamed people, to CNN. Then one person to the Wall Street Journal, four of six people to Nextgov, and one unnamed official to MS NOW. No NSA statement; the agency did not answer requests for comment. | [WRAL's copy of the CNN Wire story](https://www.wral.com/news/local/national-security-communications-network-outage-november-2026/), [Nextgov](https://www.nextgov.com/digital-government/2026/11/classified-nsa-communications-network-down-people-familiar-say/417277/), a Reuters story on the [Jerusalem Post](https://www.jpost.com/international/article-915216) that relays the Journal, and the [New Republic](https://newrepublic.com/post/218091/outage-nsa-communications-national-security-agency), all opened. The Journal's own report was not opened. Nextgov does not say whether its six people are CNN's six. |
| Optimizely, 16 Nov | Attacker code was written into customers' Optimizely project JavaScript and served on 178 organisations' sites. It swapped cryptocurrency addresses, skimmed cards, stole cookies, and pushed iOS exploit kits. First seen 04:21 UTC; monitored snippets clean by 23:11 UTC. How the attacker got in is not known. | Report URI (Scott Helme); confirmed by Optimizely. | [Report URI](https://blog.report-uri.com/worlds-largest-brands-infected-with-malware-via-optimizely/) and [Malwarebytes](https://www.malwarebytes.com/blog/news/2026/11/cnn-bbc-zoom-and-other-sites-served-malicious-code-in-supply-chain-attack), both opened. |
| Mullin, 16 or 17 Nov | Says with "98 percent certainty" this is not a cyberattack and that nothing points to the events being connected. Relays an unnamed expert's view that an AI system overloaded older FAA systems; senior officials have denied that the FAA's AI tool caused the outage. | Homeland Security Secretary Mullin. | [Townhall via WCBM](https://wcbm.com/national-headline/markwayne-mullin-addresses-fears-of-a-cyberattack-after-a-string-of-major-us-outages/), opened. The opened pages disagree on where he said it: the New Republic says Fox News on Monday, Reuters says CNBC on Tuesday. The Fox News, Hill and Mediaite pages refused a read. |
| Mullin, 13 Nov | The Microsoft outage and the ground stop are "separate issues"; no indication "as of yet" of a nefarious act. Said outside the White House and again at a Friday-night briefing with Duffy. | Homeland Security Secretary Mullin. | [CBS News](https://www.cbsnews.com/news/faa-issues-nationwide-ground-stop/) on its own reporting and [KCRA](https://www.kcra.com/article/microsoft-outlook-outage-faa-ground-stop-connected/74428537), both opened. On Friday this rested on CNN alone; it no longer does. |

Not re-verified and no longer bearing on the question: Microsoft's out-of-band fix for Windows activation failures. Microsoft's own account puts the faulty change in July, not on Patch Tuesday.

## What this does to Friday

Friday's text stays as written. These are the points on which it is now known to be wrong, outdated or settled.

| Friday said | Now |
| --- | --- |
| The ground stop landed inside an open Microsoft incident. | Microsoft's impact ended at 16:10 UTC on Friday, 4 hours 44 minutes before the ground stop. The incident records stayed open for administrative reasons. |
| Microsoft's change may have shipped on Patch Tuesday and propagated in stages. | Right about the shape, wrong about the date. The change was a gateway fix rolled out since July; it sat for more than three months before a traffic shift exposed it. |
| The same vendor update on both sides is open; Arista's advisory is a candidate. | Microsoft's failure was in its own Windows-based gateway software. The FAA's was a router in a copper-to-fibre job: a new Juniper unit by most accounts, the old Cisco ones by CBS's. Neither is Microsoft's software and neither is Arista. No shared vendor, no shared update. Closed on the public accounts, with the caveat that the FAA's root cause is not established and Mullin's Friday-night mention of security patches has not been explained. |
| The only path left runs through the contractors' own email and chat. | Weaker still. Microsoft's impact was over before the FAA work failed, and the FAA mechanism is a router flooding a network, not a coordination failure. |
| Two production networks were changed by their owners and fell over. | Stands, and is now on the record for both. |
| Mullin's denial rests on CNN alone. | CBS News and KCRA carry it on their own reporting. |
| The Friday superstition covers the FAA side only. | Stands. The FAA work was on Friday. Microsoft's trigger was a Wednesday-night failover onto a three-month-old defect. |

The one-time revision of Friday's numbers still waits. Microsoft's report is preliminary and the FAA's cause is unconfirmed.

## The hypotheses, restated for a cluster

- **H_ind:** independent failures, honestly described.
- **H_prem:** at least one denial is honest but premature; something else will turn up.
- **H_coord:** the denials are coordinated cover for one campaign.

## How unusual is four in five days?

**Definition.** A "major outage" is a failure lasting hours, reported nationally, of a U.S. cloud platform, telecom carrier, aviation system, bank or payment rail, or federal network. That is tier A in [`data/outages.csv`](../data/outages.csv). Tier B adds large consumer platforms and events described only in passing.

**The count.** 28 rows from 17 November 2024 to 17 November 2026: 22 before this week, 6 this week. The list is thin after January 2026, so the rate is fitted on the 440 days that are well covered: 12.4 per year for tier A, 16.6 per year for both tiers.

Every row now has a page behind it: 24 were opened and 4 are known from search excerpts. Checking the ten rows that were first written from memory moved one date (PlayStation Network, 7 February 2025, not 2 February), renamed one facility (the April 2025 failure was at Philadelphia TRACON, which handles Newark's airspace) and trimmed several durations and causes to what the pages say. No row changed tier or left the fitting window, so the rates did not move.

The list is still incomplete, and not only after January 2026. One of the checking searches turned up a Verizon outage in August 2025 that is not in it. It was not added: adding events as they happen to surface is the same selection problem the next section is about. It does mean 12.4 a year is a floor even for the stretch called well covered.

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
- Adding NSA Net makes four: 1.6%. But an outage of a classified internal network is public only because six people talked. Comparable outages in the previous two years would not be in the list at all. And if the sources are right that it was taken offline to be patched, it is planned maintenance that overran or was noticed, which the definition was not written to count.
- The tiers are not applied evenly. United's ground stop in August 2025 is tier A; United's halt to departures this Monday is tier B, because it was described only in passing. Promote it and the strict count is five, which the fitted rate produces in 0.1% of two-year stretches.
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
| NSA Net | Unnamed sources to several newsrooms: offline for a software patch | 0.8 |
| All | Mullin: 98 percent certainty, the homeland is secure | 1.0 |

Against the hypothesis that all four were attacks, the day-one denials multiply to 0.51. The strongest statement per event multiplies to 0.034. A generic denial is nearly worthless and four of them are worth a factor of two. A published mechanism that customers and engineers can check is worth far more, and one of the four events now has one: Microsoft's. The FAA has a named mechanism with the root cause still open, which is why its ratio is 0.4 and not 0.15.

**How much rests on the guesses.** All of it, so each ratio carries a low and a high in the file, and the script multiplies those too.

| | Central | Low to high |
| --- | --- | --- |
| Day-one denials, product | 0.51 | 0.14 to 0.90 |
| Strongest statement per event, product | 0.034 | 0.002 to 0.252 |
| Day-one denials, as a factor | 2 | 1.1 to 7 |
| Strongest statements, as a factor | 30 | 4 to 500 |

What survives the ranges is the ordering: specific accounts beat generic denials at every setting. What does not survive is the size. "A factor of thirty" is one point in an interval two orders of magnitude wide, and no measurement stands behind either end. A measured version would need a list of past outages with day-one denials, scored by whether an attack was later established. That list has not been built.

**What the products assume.** They multiply across events, which treats the four organisations' statements as independent given the hypothesis. That is fair against "four separate attacks". It is not a test of H_coord at all: if the denials are coordinated cover, every one of them would be issued either way, every ratio is 1, and the product is 1. Denials cannot test the hypothesis that the denials are coordinated. Only the checkable mechanisms can, and only where outsiders can check them.

The ratios do not rescue the weakest link. NSA Net now has a cause on offer, a software patch, from unnamed people at several newsrooms. It still has the least checkable account, and no root cause will ever be published. If residual suspicion belongs anywhere, it belongs there, and it will stay there.

## Is the news itself intact?

The channel was attacked. The question is whether that touches any of the four stories.

- **Who was hit.** Ten of the 178 organisations are news and media. Three large U.S. news sites are among them: CNN, Fox News and NPR. Against an assumed reference list of ten large U.S. news sites, that is 30%. In Report URI's sweep, 186 of 1,611 monitored Optimizely snippets were infected, 11.5%.
- **What the code could do.** It could change what a visitor sees: Report URI says the address swapping rewrites page text, form fields and links. What it was built to change was cryptocurrency addresses, not headlines.
- **When.** The code was live for at most 18 hours 50 minutes, from 04:21 to 23:11 UTC on Monday. The NSA story was republished by WRAL at 16:41 UTC on Tuesday, 17.5 hours after the monitored snippets were clean. The outlet with the exclusive was on the list; it was not serving attacker code when the exclusive ran.
- **The Chase story is the one that overlaps.** The outage began at about 14:00 UTC on Monday, inside the window. CNN's coverage that day went out on a site that was serving attacker code. Chase's account does not depend on CNN: AP, Reuters and Barron's carried it.
- **Out-of-band check, per story.** Microsoft: the company's own admin centre and status channels. FAA: a televised news conference. Chase: company statements to several wires. NSA Net: CNN's six sources, a syndicated wire copy that did not pass through CNN's web page, Nextgov's six people, and one person each to the Wall Street Journal and MS NOW.

"The outlet with the exclusive was on the hacked list" is true, has roughly a three-in-ten chance of being true for any large U.S. outlet that week, and fails on timing. The ordinary provenance problem remains, in a milder form than this chapter first said: several newsrooms now, but every source unnamed, no way to tell how many distinct people that is, and nothing on the record from the NSA.

## How to recreate this

Everything was done on 17 November 2026.

1. **Run the numbers.** From the repo root: `python3 scripts/the_week_after.py`. Standard library only, about 12 seconds, seed 20261117, 100,000 runs per rate. Pass a smaller number as the first argument for a quicker run. Compare with `analysis/week-after-output.txt`.
2. **The outage list.** `data/outages.csv`, one row per event. The `source_status` column says how each row is known: `opened` (the page was read) or `excerpt` (seen only in a search result). Ten rows were first written from the model's own recall with no page; each was then checked against a page on 17 November, and the `source` column names it. Where a detail in a row comes from an excerpt and not from the opened page, the `source` column says so. The two roundups used were the [Reuters factbox of 13 November 2026](https://www.omanobserver.om/article/1199619/business/major-tech-outages-in-recent-years) and [Tom's Guide's ten most impactful outages of 2025](https://www.tomsguide.com/computing/internet/the-10-most-impactful-outages-of-2025). To redo it properly: fix a list of organisations in advance, pull every incident above a fixed report threshold from an outage tracker for the two years, and refit.
3. **The rate.** Events before 12 November 2026, divided by days since 17 November 2024, gives a lower bound. The fitted rate uses only events up to 31 January 2026, because the list is known to be thin after that.
4. **The scan.** For each run, draw exponential gaps at rate λ/365 per day until 730 days pass, then take the largest number of events whose first and last are at most five days apart. The script prints a first-order check of the simulation.
5. **The denials.** `data/denials.csv`. Each row has a central ratio, a low and a high, and a `stage` (`day_one`, `later`, or `blanket` for a statement about everything at once). Change any of them and rerun; the script reads all of it from the file and prints the products, their ranges, and the posterior for three priors.
6. **The Optimizely list.** `data/optimizely-affected.txt`, taken from the Report URI page through an automated summary. Check the names against the page. The reference list of ten large U.S. news sites is in the script and is an assumption.
7. **Search queries used.** "NSA classified network NSANet outage six sources no evidence of cyberattack"; "Optimizely compromise malicious JavaScript Report URI Scott Helme 178 organizations list"; "Chase outage November 16 2026 cause update own systems not cyberattack Bank of America Wells Fargo"; "Microsoft 365 outage post-incident review root cause network configuration change EX1550543 MO1550821"; "FAA ground stop November 13 root cause findings L3Harris network update Duffy statement investigation"; "NSA network outage Wall Street Journal software update NSANet cause"; "Mullin homeland is secure outages no indication cyberattack"; "Factbox major tech outages in recent years Reuters November 2026".
8. **Pages that refused an automated read.** On the first pass: NPR and CNBC on the FAA cause, CNN throughout, the Wall Street Journal, Fox News. On the second pass CNBC and CBS News opened. Still refusing or paywalled: CNN, the Wall Street Journal, Fox News, The Hill, Mediaite, the Washington Times, the South China Morning Post, technology.org, the Detroit News copy of Reuters on Bedford, and ThousandEyes. No paywall was worked around. Claims that rest on those pages are marked above.

## Still open

- The base rate of nationally reported outages at the low bar. This is the number the cluster question turns on.
- Microsoft's final report and the FAA's findings. Then revise Friday's numbers once.
- On the FAA side, which equipment failed: the new Juniper router or the old Cisco ones. The site is settled: El Dorado, Arkansas. A second site in Texas appears in search excerpts and on no page that was opened.
- What Mullin meant on Friday night by security patches overwhelming the routers, which no later account repeats.
- How many distinct people are behind the NSA patching account, and the Wall Street Journal's report read in full.
- A measured likelihood ratio for day-one denials, from past outages scored by what was later established.
- The complete outage list. The ten rows once held from memory are checked; the gaps are the events that were never in it.
- A measured reference list of news sites for the overlap, in place of the assumed ten.
