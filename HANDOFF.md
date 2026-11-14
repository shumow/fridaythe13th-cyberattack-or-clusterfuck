# Handoff

Status as of Saturday, 14 November 2026.

## Where things stand

- The piece lives in `README.md` in two layers: prose on top, a "Show the work" block under each section. The prose is the Friday-night draft; Dan is rewriting it.
- The working analysis is `analysis/independence-or-common-cause.md`, exported from the Claude Doc of the same name. Its earlier estimates are left as first written, with dated notes, and get revised once, when the root causes are published.
- `scripts/show_your_work.py` reproduces every number in the README.

## Open

1. **Dan's prose.** As each line arrives, put the technical block under it: the number, the derivation, the source, and how far the source can be trusted.
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
