# Handoff

## Status, 18 November 2026, 10:05 UTC: model v1 is frozen and the log is running

On the branch `claude/stoic-feynman-pwhm51` (not yet merged into `model-v1-draft`).

- **Frozen.** Commit `1e33a38` added `model/model_v1.sha256` at 10:00 UTC on Dan's word: freeze now with the judgments, measure for version 2. The rules are the draft as written. `model/DECISIONS.md` records what was answered.
- **Logged.** `log/log.csv` holds 28 retrospective rows (everything public before the freeze) and then prospective rows. Outputs are in `output/`. `python3 scripts/validate.py` passes.
- **Every two hours** a scheduled task wakes the Code session. Each run: search for new outages at panel organisations and for new statements about the logged events; add rows (prospective, `known_at` equal to `logged_at`); if nothing is new add one `checkpoint` row; rerun `python3 scripts/pipeline.py` and `python3 scripts/validate.py`; commit, push, and add one dated line to the list below.
- **Rules for the log.** Rows are only added. No `instrument` rows: Dan took the outside counter out of the model (item 7). The three frozen files never change. Reports that are denied, knock-ons, organisations off the panel and news-wave items go in as `context` rows. Nothing goes to `main`.
- **Version 2, agreed so far:** a news-wave and misinformation layer (Dan's point, the main addition); the suggested changes in items 5 and 7 to 10 of `DECISIONS.md`; measured attack priors and visibility; a sensitivity table with every ratio halved and doubled; an interface with sliders.
- **Still stopped:** the second-round measurements (`PROTOCOL-2.md`). The archive rate-limits this container; see the dated note in the next block.

### Run log

- 18 Nov 10:01 UTC. First run. 5 counted events, 3 after the ground stop. P(campaign): calm 0.03%, middle 0.3%, suspicious 3.4%. P(at least one attack): 3.0%, 8.9%, 27%. Found since the last notes: an Apple services outage on Tuesday afternoon, blamed on an internal update (off the panel, context row).

Status as of Saturday, 14 November 2026.

## Task waiting for a Claude Code session (written 17 November 2026, 16:50 Pacific)

For a session whose shell can reach the internet. The text session that wrote this could not: on 18 November at 00:28 UTC its request to the archive was refused by the egress proxy with HTTP 403. Dan has said he is turning network access on.

**Start here.** `git fetch origin && git checkout model-v1-draft`. This block exists only on that branch. Read `measurements/RESULTS.md` for what the first round found and `measurements/PROTOCOL-2.md` for what to run.

**The job.**

1. Test the network yourself, do not assume. One request from the shell:
   `curl -sS -m 30 'https://api.gdeltproject.org/api/v2/doc/doc?query=outage&mode=timelinevolraw&format=csv&timespan=1w' | head`
   If it is refused, add one dated line under this block with the error, push, and stop. Do not route around a refusal and do not report another failed pilot.
2. If it works, run `PROTOCOL-2.md` in its own order: the three gates, part B2 (the backwards count), part C2 (coverage within 48 hours for the airline and bank events), part A (one re-read). Expect about 500 requests at one every six seconds, so under an hour of waiting plus the reading.
3. Write `measurements/RESULTS-2.md`, commit and push to `model-v1-draft`, then replace this block with a short dated status.

**Rules.**

- Work on `model-v1-draft` only. Nothing goes to `main`: no data, no merge.
- Do not freeze the model: no `model/model_v1.sha256`, no `log/`, no `output/`, and no change to `model/model_v1.json`, `model/MODEL-v1.md` or `scripts/pipeline.py`. The open choices are Dan's and are listed in `model/DECISIONS.md`.
- Do not edit `data/outages.csv`, the README or the chapters. Corrections wait for the one-time revision.
- `PROTOCOL-2.md` was committed before any counting. Do not edit it. Where it cannot be followed as written, do the nearest thing and list the deviation in `RESULTS-2.md`. Commit the query strings before touching a sampled week, as it says.
- Every number in a write-up comes from a script in the repo. Record which pages were opened and which were seen only as a title.

**18 November 2026, 02:25 UTC, Code session (branch `claude/stoic-feynman-pwhm51`).** The network gate passed once the archive's host was allowed, but the run is stopped before Gate 2. The archive rate-limits this container's outbound address: of 26 logged attempts between 01:38 and 02:22 UTC, spaced from 6.5 seconds to 2 minutes apart, 2 were answered (the rest HTTP 429 or a reset connection). Both answers were "Your query was too short or too long", for the airline query with twelve names (about 600 characters) and with six (393). No query has worked, no sampled week has been touched, and `b2_queries.json` does not exist. The initial test and its retries outside the logger (five requests, one answered) are not in `b2_requests.csv`. Waiting for Dan.

## Update, Tuesday 17 November 2026, evening: the measurements (branch `model-v1-draft`)

This block is on the branch `model-v1-draft` only (draft pull request #2). `main` has no model, no measurements and no new data.

- **State of the model.** `model/` and `scripts/pipeline.py` are a draft. Nothing is frozen: there is no `model/model_v1.sha256`, no `log/`, no `output/`. The open choices at the end of `model/MODEL-v1.md` wait for Dan.
- **Measurements.** `measurements/PROTOCOL.md` was committed before any counting. First results and every deviation are in `measurements/RESULTS.md`; the numbers come from `python3 measurements/analyze.py`.
  - A (ThousandEyes weekly counts): baseline in hand, the week of 9 to 15 November not published as of 18 November 00:00 UTC. To finish: re-read the Network World 2026 page, fill the target row of `a_instrument.csv`, rerun.
  - B (the inclusion rule applied to past weeks): the pilot shows the search method cannot do the job. Needs a replacement instrument before the 28-row table can be redone.
  - C (like for like): done for airlines. For banks the first step is done: four past outages found, written up in an addendum to `RESULTS.md`. Coverage for both is to be redone with the dated archive.
- **Second round.** `measurements/PROTOCOL-2.md`, committed before its counting, replaces the failed search method with a dated news archive. It is the task at the top of this file.
- **Decisions.** Everything that waits for Dan is in `model/DECISIONS.md`, thirteen items, each with a suggested answer.
- **Found on the way, not yet applied anywhere.** (1) The FAA published its own account on 15 November; it names Juniper routers and two sites, where chapter 2 says "reportedly Cisco". (2) Amtrak's outage was Friday 13 November, during the ground stop; `data/outages.csv` has it on the 16th. (3) A reported Weather Service outage on the 13th was denied by the agency. (4) Two federal systems were taken offline by security incidents in October. All four are written up in `measurements/RESULTS.md` under "Found on the way". They wait for the one-time revision and, once the model is frozen, for the log.
- **Of the open items below:** item 3 of the first list (router vendor and site at source) is answered by the FAA's page. Item 4 (Mullin) is half answered: ISMG quotes him on "zero evidence" of a cyberattack; his "not connected" remark still rests on CNN.
- **This session's limits.** The shell has no network access, so nothing could be installed or fetched by script. The search tool returns titles and links only and refuses a filter made of national news domains.

## Update, Tuesday 17 November 2026

- Added chapter 2, the cluster: `analysis/chapter-2-the-cluster.md`, `scripts/the_week_after.py`, `data/`, and a new README section with placeholder prose. Friday's text is untouched apart from a dated banner at the top of the README.
- Both of Friday's outages now have accounts on the record. They share no vendor or update, so the same-vendor branch is closed on what is public.
- Friday's numbers are still not revised: Microsoft's report is preliminary (final after 20 November) and the FAA's cause is unconfirmed.
- Open, in order of how much they matter: (1) the base rate of nationally reported outages at the low bar, measured from an outage tracker for a fixed list of organisations; (2) the final Microsoft report and FAA findings, then the one-time revision; (3) the FAA router vendor and site at source; (4) the Wall Street Journal's NSA report read in full; (5) replace the ten rows of `data/outages.csv` that are from memory; (6) Dan's prose for the new section.
- The status dated 14 November below is kept as it was.

## Where things stand

- The piece lives in `README.md` in two layers: prose on top, a "Show the work" block under each section. The prose is the Friday-night draft; Dan is rewriting it.
- The working analysis is `analysis/independence-or-common-cause.md`, exported from the Claude Doc of the same name. Its earlier estimates are left as first written, with dated notes, and get revised once, when the root causes are published.
- `scripts/show_your_work.py` reproduces every number in the README.

## Open

1. **Dan's prose.** As each line arrives, put the technical block under it: the number, the derivation, the source, and how far the source can be trusted.
   - **Banked line, Dan, 18 November 2026, for "So which is it?" (the closing section), verbatim from voice:** "The honest position is we don't know yet, and because we're doing science here, we will never truly know. We have scientific models that we hope make good predictions, and if they stop making good predictions, we revise them."
   - **Style.** The README now opens with Dan's own prose. The rewrite of every other section follows that voice. Dan writes or refines each section; the session cleans up and keeps the "Show the work" blocks.
2. **The DOOM line.** The README has a visible placeholder in the Friday the 13th section for Dan to fill in himself.
3. **Root causes.** Neither Microsoft nor the FAA or L3Harris has published one. When they do: compare vendor and version of the network change on each side, then revise the analysis once.
4. **Mullin's denial.** Still rests on CNN alone. Find a transcript or wire story that can be opened.
5. **Friday deploys.** The README says the mechanism is an argument, not a measurement. Find data on change-failure rates by weekday, or keep the caveat.
6. **Measured inputs.** A proper count of major Microsoft 365 outages from incident records; the five-year table of cloud and identity outages; the per-exposure failure rate; what tooling the FAA network contractors run.
7. **Source verification.** CNN, NBC News and the Reuters factbox refuse automated reads; claims from them are cited from search excerpts. The analysis lists which pages were opened in full.

## History: the handoff notes from the working doc

**Status after the November 13 text session.** Done: the high-level picture and its diagram (The big picture), the timeline (item 8), the FAA-exposure and root-cause checks (items 9 and 5), and a second pass on the numbers (part of item 7). Found: officials and Microsoft both deny a link; an update on the L3Harris-run network is the reported cause on the FAA side; neither root cause is published. Still open: item 1 beyond the three pages that could be opened in full (see Sources), items 2, 3, 4 and 6, and a re-check of item 5 once Microsoft's post-incident report and an official FAA account appear.

**Status after the second text pass (Friday night, November 13).** (1) Done: the common-cause box now holds three branches, with the same vendor update drawn as open. (2) Vendor and version comparison cannot be run, since neither side has named either; the advisory scan found one candidate, Arista's EOS advisory of November 10, with nothing tying it to either outage. (3) Microsoft's statement has an independent second source (PEOPLE); Mullin's does not, and still rests on CNN alone. (4) Done: the Posterior, the bottom-up estimate and the first-pass numbers carry provenance notes and are otherwise untouched. Details are under Check results in The big picture. Changes made in the first text pass, before instruction (4), remain: the Setup wording on the denials and the incident's duration, and one duration cell in the first-pass table.

**Next for the text agent (added in voice, November 13, after the first text pass).** Two things. (1) Redraw the common-cause box in the block diagram to hold three branches, not two: an attacker, a shared carrier or routing fault, and the same vendor update applied on both sides (see the paragraph "A third common cause the diagram does not yet draw" under Where the uncertainty sits). Mark the third branch as open, not ruled out: the day-one denials do not reach it. Keep every existing label and its id; only the box and its lines change. (2) Run the two checks under that paragraph: compare vendor and version of the network change on each side once root causes exist, and scan vendor advisories for the week of November 9 for a router or network-OS patch with a reboot or crash defect. Report what was found in the link table and in the Status paragraph above.

**Also (same voice session).** (3) The two statements that now carry the argument, Mullin's "not connected" and Microsoft's "no indication that the FAA nationwide ground stop is related", are cited from search excerpts of CNN and NBC pages that refuse automated reading. Find a second, readable source for each before leaning on them further: a wire-service story, a transcript, or the FAA's and Microsoft's own posts on X. (4) Do not revise the earlier analysis yet. Leave the Posterior, the bottom-up estimate and the first-pass numbers in place as written, and add a note beside each saying that later reporting (the denials, the network-update account, the Microsoft rollback) bears on it but that the provenance of that reporting is not yet settled: the denials are unverified excerpts, the update account is from unnamed sources to one outlet, and the Microsoft change is described by Microsoft as correlated, not causal. The reasoning should be revised once, when the root causes are published and the statements are confirmed, not piecemeal as each unconfirmed item lands; a reader should be able to see what we believed on each day and why.

**Audience.** Fellow mathematicians and academic and industrial researchers in computer science, mathematics and data science. The piece is largely informal and meant to be infotaining: an enjoyable examination of a real coincidence, not a paper. Write for people who know Bayesian inference and point processes already, so no tutorial on the methods, but keep the assumptions, the sourcing, and the sensitivity of the conclusion to each guessed number honest and visible, since that is where the fun is for this crowd.

**Tone.** Lead with the Friday the 13th joke (already at the top of the doc) and keep that lightness throughout; the rigour is in the assumptions, not the prose.

**Primary task: a high-level causal picture, before any mechanism hunting.** Dan's instruction: reason first at the level of large shapes, where we are more certain, and keep specific causal mechanisms secondary. Do not over-suspect. Take the official statements as given (not a cyberattack on either side; a telecom issue at the FAA; capacity and configuration at Microsoft) and draw a block diagram of the big nodes and the influences between them. The nodes, roughly: the Microsoft 365 outage; the telecom and network-contractor layer (L3Harris, Verizon, AT&T, mid-transition to FENS); the FAA's air traffic network; the ground stop; and, outside the picture, the attacker node that the statements rule out. For each edge, state qualitatively how strong it is and why: for example, the telecom layer is a significant node to examine because government contractors and carriers were demonstrably exposed to the outage (see Government impact), not because of any specific mechanism yet. Give a short reasoned assessment of which large-scale paths are live, which are closed by the statements, and where the uncertainty actually sits. Only after that picture is stable should the measured-numbers work below begin.

**Secondary: replace the placeholder numbers with measured values.** The doc is a problem statement with placeholder numbers; once the high-level picture is settled, tighten it. In order of value:

1. **Verify the sources.** Open every linked page and check each cited figure, quote and date against the page, not the summary this was built from. Fix anything wrong.
2. **Count Microsoft 365 major outages properly.** Use the Microsoft 365 service health history, StatusGator and UptimeRobot archives to build a complete list of multi-hour, multi-service incidents for 2024 to 2026. Define "major" once and apply it consistently. Replace the lambda\_M figure and recompute P(D | H0).
3. **Build the five-year outage table for h.** List major cloud and identity outages (Microsoft, AWS, Google, Cloudflare, CrowdStrike, Okta) from 2021 onward and mark which produced a documented aviation or critical-infrastructure failure. Compute h.
4. **Estimate r from this week.** Count documented operational failures attributed to the November 2026 outage (government agencies, airlines, health systems) and divide by a reasonable estimate of exposed organisations. State the definition of "operational failure" used.
5. **Check for root-cause publications.** Search for any FAA, L3Harris, Verizon, AT&T or Microsoft post-incident report on the November 13 ground stop or the November 12 to 13 outage. If the FAA names a cause, most of this doc's uncertainty collapses.
6. **Investigate the coupling c.** Look for public evidence of what operations tooling the FAA network contractors use (FedRAMP listings, procurement records, job postings). Even one confirmed Microsoft 365 or Entra dependency at L3Harris, Verizon or AT&T network operations raises c to near 1.
7. **Recompute the posterior** with the measured values, show the sensitivity to each, and rewrite the Posterior section with the result.

8) **Timeline (secondary).** Build an hour-by-hour timeline of both incidents in Eastern time. If the Microsoft outage was substantially resolved before the FAA telecom fault, the operational path narrows to a recovery-window effect, a weaker claim.
9) **FAA exposure (secondary).** Search for any FAA, DOT or contractor statement mentioning Microsoft, and check whether the FAA itself was among the organisations affected by the outage.

Treat items 1 to 9 as refinements. The high-level diagram and its reasoning are the deliverable; the mechanistic detail comes later, if at all.

Keep all formulas as display LaTeX blocks. Keep the distinction between sourced and unsourced claims explicit.

## Earlier to-do list from the working doc

- [ ] Open every linked page in the Sources section and verify each cited figure, quote and date against the page itself, not the search summary.
- [ ] Replace the approximate Microsoft 365 outage rate with a count from actual incident records.
- [ ] Check whether the FAA or its contractors have published a root cause for the November 13 ground stop, and whether Microsoft has published one for the outage.
