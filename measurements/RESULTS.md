# Measuring the frequency illusion: first results

Tuesday 17 November 2026, evening Pacific. The protocol is `PROTOCOL.md`, committed at 23:34 UTC, before any counting. Every number below is printed by `python3 measurements/analyze.py`; its output is saved in `analyze-output.txt`. Nothing here is on `main`, nothing has been run through the model, and the model is still a draft.

Pages marked "opened" were read through an automated reader that returns a summary and short quotes, not the page text. Check anything that matters against the page.

## Where things stand

| Measurement | Status | What it says so far |
| --- | --- | --- |
| A. A counter that was already running | Baseline in hand. The week of the ground stop is not published yet. | Nothing about this week yet. The counter turns out to be a weak witness. |
| B. One inclusion rule applied to past weeks | Pilot done: 16 searches, 241 results. | The search method fails and cannot give a base rate. |
| C. Like for like, airlines | Done for airlines: 6 past groundings. | United's outage would have been national news in an ordinary week. |

The frequency illusion is not measured yet: neither the event rate nor the coverage rate for this week exists as a number. What the first pass does show is where our own count of the week was inflated and where the baseline it was compared with was too thin. Both are under "Found on the way".

## A. A counter that was already running

**Source.** ThousandEyes' weekly counts of network outages, as recorded in Network World's running reports for [2026](https://www.networkworld.com/article/4113326/2026-network-outage-report-and-internet-health-check.html) and [2025](https://www.networkworld.com/article/3630303/2025-global-network-outage-report-and-internet-health-check.html). Each page was read twice with differently worded instructions, and the two reads agree on all 95 weeks. Two weeks in December 2025 are not on the page.

**Result.** The eight baseline weeks, 14 September to 8 November, average 263.4 U.S. outages a week with a standard deviation of 85.6. The week of the ground stop will read "mildly high" above 349 and "elevated" above 435. The 2026 page is dated 12 November and has no entry yet for 9 to 15 November.

**How much that reading will be worth.** Before any target value exists, the protocol's own statistic was applied to every earlier week it can be computed for (87 weeks).

- It cries wolf. 26% of past weeks read "mildly high" or more and 9% read "elevated". Independent noise would give 19% and 5.0%. The level drifts: the median weekly count runs from 65 in the last quarter of 2025 to 377 in the third quarter of 2026.
- It does not notice big outages. Of the 13 weeks that hold a tier-A row of `data/outages.csv`, 3 (23%) read "mildly high" or more. Of the other 74 weeks, 20 (27%) do. The weeks of the AWS outage of 20 October 2025, the Azure outage of 29 October 2025 and the Cloudflare outage of 18 November 2025 had counts of 99, 45 and 31, each below its own baseline (z of −1.09, −2.21 and −1.10).

The counter tallies outage events seen on network paths, most of them small, and an outage that takes down half the web is one event. So whatever it reads for 9 to 15 November will say little about whether more large systems failed that week. Ten of the 28 rows in `data/outages.csv` are from memory; leaving out the weeks known only from memory does not change the picture (8 weeks: 1 reads high, 3 read low).

## B. One inclusion rule applied to past weeks

**What was run.** The pilot as specified: four sector searches for each of four weeks. The baseline weeks are the first two of the seeded list, 17 March 2025 and 2 December 2024. The target weeks are 9 November and 16 November 2026.

| Week of | Results | About an event inside the week | Outside it | Cannot be placed | Events by the rule | Events already in our table, returned |
| --- | --- | --- | --- | --- | --- | --- |
| 2 Dec 2024 (baseline) | 60 | 0 | 31 | 29 | 0 | none to check |
| 17 Mar 2025 (baseline) | 60 | 0 | 19 | 41 | 0, and 1 unresolved | none to check |
| 9 Nov 2026 (target) | 59 | 21 | 11 | 27 | 4 | 3 of 3 |
| 16 Nov 2026 (target, two days old) | 62 | 0 | 31 | 31 | 0 | 0 of 3 |

The "3 of 3" counts Amtrak, which our table files under the wrong day (below).

At face value that is no events in a quiet week and four in the week of the ground stop. The pilot itself shows why that reading is wrong.

1. **The search does not search by date.** For the March 2025 week the airline query returned eleven results, every one about 13 November 2026. For the December 2024 week it returned the American Airlines ground stop of 24 December, three weeks late, in 12 of 17 results. None of the 120 baseline results is about an event inside the week asked for.
2. **It misses events that happened.** For the week of 16 November it returned nothing on Chase, United or NSA Net.
3. **It counts a report as an event.** One of the four "events" of 9 November is a National Weather Service outage that the agency denied the same afternoon (below).
4. **It cannot see national coverage.** One result in 241 sits on a national outlet's own domain. Even the ground stop scores zero.

So the count follows whatever is prominent, which is the thing this measurement was meant to factor out. The 28-row table cannot be rebuilt this way.

**What could replace it.** None of these was run; each needs something this session lacks.

- For coverage: a news archive that filters by publication date, queried the same way for every week. GDELT's article search does this. It needs network access from a script, which this session's shell does not have.
- For events, class by class, records that do not pass through the news: the FAA command centre's advisory archive, which should list ground stops with a reason (not checked), and the cloud providers' own incident histories. For banks and federal systems there is no such record, and the fallback is the trade press read by date.

## C. Like for like: would United's outage have been news anyway?

**What was run.** Three searches restricted to trade and enthusiast sites, then one coverage search per event. They found six system-wide technology groundings at panel airlines in two years. Four are confirmed at three hours or less: Southwest on 9 October 2026, American on 28 July 2026, JetBlue on 10 March 2026 and United on 23 September 2025. Two more have no confirmed duration: United on 6 August 2025 and American on 24 December 2024.

**Result.**

| Group | Events | A national outlet's own domain in the results | A national wire or network story visible |
| --- | --- | --- | --- |
| Confirmed at three hours or less | 4 | 0 | 3 (75%, interval 30% to 95%) |
| All six | 6 | 1 | 5 (83%, interval 44% to 97%) |

Short airline groundings are covered nationally as a matter of routine. The one exception is Southwest's two-hour outage of 9 October 2026. Six in two years is at least 3.0 a year, which makes one in any given five days a 4.0% event. United's outage on 16 November belongs to a class that recurs and gets reported. Its being in the news is not evidence of a lowered bar. Tying it to the other outages is a separate step, and this does not test that.

The first column is nearly empty for the same reason as in B: the search tool rarely returns the national outlets' own pages. The second column is a looser reading added after seeing that, so treat it as descriptive.

## Found on the way

These came out of the searches above. They are not part of any measurement.

### Three corrections to our own record of the week

1. **Amtrak was Friday, not Monday.** `data/outages.csv` files an Amtrak disruption under 16 November with the note "date not given". [FOX 5](https://www.fox5ny.com/news/amtrak-outage-ticket-booking-faa-ground-stop-november-13-2026) dates it: the booking system failed on Friday 13 November from shortly before 5 pm Eastern and was returning to normal around 9 pm, during the ground stop. Amtrak gave two explanations, increased demand and, on X, a "system-wide update". On its timing and on Amtrak's first explanation it looks like a knock-on of the ground stop, not a separate event three days later. The "system-wide update" is unexplained.
2. **The Weather Service "outage" rests on one undated notice, and the agency denied it.** A [political.org story](https://political.org/2026/11/13/national-weather-service-reports-nationwide-internet-and-communications-problems-as-faa-halts-flights/) quoted a notice that "The NWS has been experiencing nation-wide internet and communications issues". Sinclair's [National News Desk](https://cbsaustin.com/news/nation-world/national-weather-service-pushes-back-on-reports-of-nationwide-radar-outage-nws-radar-communications-issues-internet-federal-aviation-administration-faa-flights-ground-stop-airports-disruption) reported the agency's reply on X that afternoon: "In case you heard otherwise, there is no radar outage and radar.weather.gov is fully operational!" It blamed outdated information on isolated web pages. The notice sat on the Los Angeles office's page and showed no posting time. So within two hours of the ground stop, a notice of unknown age on one office's page was being reported as a second federal outage. What is not established is whether the agency had any communications trouble that day: its denial covers the radars and the radar site.
3. **The FAA's own page names Juniper routers.** Chapter 2 says "reportedly Cisco", from CBS News as relayed by Wikipedia and never opened at source. The FAA's page is the primary source (next section). The disagreement is unexplained.

Nothing on `main` was edited. These wait for the one-time revision.

### The FAA's own account, published 15 November

[Nationwide Ground Stop: Questions and Answers](https://www.faa.gov/newsroom/nationwide-ground-stop-questions-and-answers), dated Sunday 15 November 2026, read twice. This project had not opened it before.

- The trouble began at about 3:30 pm Eastern on 13 November, and traffic resumed at 8:15 pm.
- Legacy equipment became unstable when "data began flooding the FAA FTI network", at about 1,000 connection attempts every four to five seconds. Instability began at 17 of 22 en-route centres and spread to several approach controls.
- The first findings point to two sites: a radar site in Amarillo, Texas, and a radio site in El Dorado, Arkansas. L3Harris had been working at El Dorado, including deploying a new router. Blocking both sites stabilised the network.
- As a precaution the FAA disabled broadcasting on all new routers. It says it disabled "the functionality" on the originating Juniper routers and on more than 60 other Juniper routers, and has paused installing them. The root cause is still under investigation.
- "Based on all available evidence, we have no indication that this was a cyberattack or an outside nefarious actor."
- The page says the FAA's new SMART system was not the cause. It does not mention Microsoft.

This answers the open question of the router's vendor and site from the FAA itself. When the log starts, it is a statement by the responsible side with a specific mechanism and an open root cause.

### Events the remembered table lacks

While looking for other weeks, the searches turned up 15 dated events at panel organisations. Twelve fall inside the two-year window, and 8 of those are absent from `data/outages.csv`: the American Airlines ground stop of 24 December 2024 and seven federal systems (`bycatch.csv`). Two of the seven are described as security incidents, both in October 2026:

- **Bankruptcy Noticing Center**, run by BAE for the federal courts: offline from 9 October 2026, public notice on 15 October, called a "cybersecurity incident" by the courts' administrative office ([The Register](https://www.theregister.com/security/2026-10-16/attack-on-bae-managed-system-disrupts-us-bankruptcy-courts/5303487)).
- **Federal Election Commission** electronic filing: offline from 26 October 2026. Reuters, citing an internal email, reported that the agency shut its internet-facing services because an unauthorised party was trying to break in. The FEC had not confirmed that as of 28 October ([The Next Web](https://thenextweb.com/news/fec-hacker-breach-filing-system-offline)).

Two of seven is an accidental sample, tilted towards whatever gets written about. It is not a rate.

Measurement C adds to the gap: of its six airline groundings, 5 are absent from the table. Together that is at least 12 events at panel organisations in two years that a table built from memory and "biggest outages" roundups does not hold. The rates chapter 2 fitted from that table are too low for the bar the model draft sets.

### Sources that can be read

- [ISMG's story](https://www.govinfosecurity.com/us-flights-halted-as-faa-communications-systems-fail-a-33394) of 13 November quotes Mullin directly: "We've seen zero evidence" of a cyberattack, and, asked about AI, "You just can't rule out anything at this point". That is a second readable source for his cyberattack statement. It does not carry his "not connected" remark about Microsoft, which still rests on CNN.
- Not opened: a [Fortune piece](https://fortune.com/2026/11/13/microsoft-outage-courts-police-hospitals-it-monoculture/) on what the Microsoft outage did to courts, police and hospitals, and a [Network World piece](https://www.networkworld.com/article/4249392/microsoft-outage-a-cascading-failure-that-started-with-an-undetected-bug-2.html) on its cause.

## Deviations from the protocol

- **A.** The whole series back to 30 December 2024 was collected, not 2026 only. The two checks on the statistic were added after seeing the series and before any target value exists.
- **B.** The March 2025 week was searched twice; the first set of results was not kept word for word, so the second is the record. The protocol did not say which pages to open, and the choice was mine. Dates were read from URLs and from other results in the same list as well as from titles. Eleven pages were read outside the two-per-week budget to follow leads; they change no count, and they are what exposed the Weather Service item. The check against events already in our table was added afterwards. One page, Fortune's on the Social Security outages, could not be read at all.
- **C.** The search tool refused a filter made of the national outlets' domains, so the coverage searches ran unfiltered and national domains were counted among the results. The looser "wire or network story visible" reading was added after seeing how rarely those domains appear. Four events met the three-hour rule, not five. The times in `c_like_for_like.csv` are the midpoint of a three-minute bound taken from file and commit timestamps.

## What this bears on in the model draft

The model is not changed. These are observations for the open choices.

1. **The outside counter.** The draft lets a ThousandEyes z-score move the campaign odds by up to a factor of five either way. On its record that is far too much.
2. **Quiet-week visibility.** The draft gives a tier-B event a 0.25 chance of being national news in a quiet week. For airline groundings the measured figure is 5 of 6.
3. **Knock-ons and phantoms.** The draft has no rule for an event caused by another logged event (Amtrak), and its lowest rung for "did this happen" is 0.85, too high for a report the organisation denies (the Weather Service).
4. **Federal systems.** The panel takes any federal agency system, which is a much larger and busier class than the remembered table suggests. The attack prior for that class (3% in the draft) is the number most worth measuring before the freeze.
5. **The window.** The campaign layer counts events after the ground stop. The two October security incidents sit before it.

## Next

1. **A.** Re-read the 2026 page after its next update, enter the week of 9 to 15 November in `a_instrument.csv`, rerun `analyze.py`.
2. **B.** Choose a replacement instrument. A dated news archive needs network access or a run on Dan's machine.
3. **C.** Banks, with Chase on 16 November as the comparison, then rail and federal systems.
4. **For the log, once the model is frozen:** the FAA page of 15 November, Amtrak on its right day, the Weather Service report and denial, and the two October incidents as context.
5. **For the one-time revision:** "reportedly Cisco" in chapter 2 and the Amtrak row in `data/outages.csv`.

## Files

| File | What it holds |
| --- | --- |
| `PROTOCOL.md` | The plan, committed before counting |
| `sample_weeks.py` | The seeded list of baseline weeks |
| `a_instrument.csv` | 95 weekly counts and the unpublished target weeks |
| `b_raw_results.csv` | All 241 search results, each labelled with what it is about and whether it falls in the week asked for |
| `b_pages_opened.csv` | Every page opened, why, and what it said |
| `b_backwards.csv` | The events judged for each week, with the reasons |
| `c_like_for_like.csv` | The six airline groundings and their coverage |
| `bycatch.csv` | Dated events turned up by accident |
| `analyze.py`, `analyze-output.txt` | The script behind every number here, and its output |
