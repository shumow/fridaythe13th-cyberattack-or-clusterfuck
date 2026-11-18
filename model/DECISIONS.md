# Decisions waiting for Dan

> **Answered, 18 November 2026 (night of the 17th, Pacific).** Dan, in a Code session:
>
> - Item 1: freeze now with the judgments, measure for version 2.
> - Item 2: keep the three states.
> - Item 3: keep the principle and the drafted numbers; show a sensitivity table with every ratio halved and doubled, later; and build an interface with sliders for the ratios.
> - Item 4: assumed for version 1, with the three observers spreading them ninefold; measured for version 2.
> - Item 4, the reclassification search (outages first called "not an attack" and later reclassified): approved. It starts with its own protocol, committed before any searching, once Dan has finished going through this list.
> - Item 5: let a campaign start before the ground stop. Count over the calendar window fixed in advance, 1 October to 30 November 2026, so the two October security incidents count; keep the 14 days after the ground stop for the attention analysis only. Answered after the freeze, so this is a version 2 change.
> - Item 6: three observers (calm, middle, suspicious). This is what version 1 has.
> - Item 7: take the outside counter (ThousandEyes) out of the model and keep it as a chart. Version 1's frozen rules still have a slot for it, so no `instrument` row is to be logged under version 1; version 2 removes the slot.
> - Item 8: set quiet-week visibility by class from measurement where there is one, and keep the tier figures elsewhere. A version 2 change. The only measured class so far is short airline groundings, 5 of 6.
> - Item 9: add both rules in version 2. An event caused by a logged event is recorded but not counted as an arrival. A report the organisation denies enters with a 0.2 chance of having happened. Dan also wants the statistic itself tracked: how many knock-ons and denied reports gather around each real event, over time, and whether that number looks suspicious. It feeds the news-wave layer. Tally at the freeze: 1 knock-on (Amtrak, 13 Nov); 2 denied-report items (the Weather Service on 13 Nov; the other banks on 16 Nov, where 6 organisations were named, 3 denied any issue, 1 confirmed only delayed transfers and 2 did not comment). No baseline exists yet for an ordinary week.
> - Item 10: use the fixed federal list in `measurements/PROTOCOL-2.md` in place of "any U.S. federal agency system". A version 2 change to the panel. Until then, runs under version 1 treat a federal outage as an event only if the agency is on that list, and log anything else federal as a `context` row tagged `[off panel]`, so the log does not have to be re-sorted later.
> - Raised by Dan before the freeze: the model has no place for a news wave or for misinformation. Agreed as the main addition for version 2; the gap is named in `MODEL-v1.md` under "What freezing does not fix". Until then phantoms and denied reports are logged as `context` rows.
> - The freeze and the log live on the branch `claude/stoic-feynman-pwhm51`.
> - Item 11: yes. The repo is the source of truth, and `scripts/validate.py` checks that from git history. Dan also wants changing stories and inconsistencies tracked, as bookkeeping for now (`bookkeeping/inconsistencies.csv`), with the fuller version left as an open item for future research in `HANDOFF.md`.
> - Items 12 and 13 are still open.

Written 17 November 2026. The model in this folder is a draft. It freezes when a commit adds `model/model_v1.sha256`, and that commit waits for the answers below. Until then no event from the week can be run through the model, so the log, the dated curves and chapter 3 all wait too. The measurements do not wait.

Each item gives what the draft does now, what the first measurements say about it, and the choices. The first choice listed is the one I would take. "Take the suggestions" is a complete answer.

## The one that sets the timetable

**1. Freeze now and improve by version, or measure first and freeze later?**

The draft's attack priors and visibility figures are judgments. Some of them can be measured, but only with the dated archive, which needs a session with network access.

- **Freeze now with the judgments, measure for version 2.** The rules already allow it: a change is a numbered version with a changelog and the whole log is rerun, so both curves show. Every day without a freeze turns more of the week's news into hindsight rows.
- **Measure first, freeze once.** One model, no version 2 on day three. The cost is that everything reported before the freeze is scored by rules written after seeing it.

**The deadline either way.** Microsoft's final report is due after 20 November, and the FAA's root cause could come any day. Whatever is frozen before they arrive scores them by rules written first. Whatever is not, scores them in hindsight.

## The five open choices in `MODEL-v1.md`

**2. Are the three states right?** Benign; attack with an account that is honestly premature; attack with an account that stays wrong, no motive modelled.

- **Keep the three.** They are the two cases you asked for plus the innocent one.
- Collapse to two (benign, attack) and drop the question of whether the account stays wrong.

**3. What a statement is worth.** The draft's principle: a statement from the side responsible moves "premature" a lot and "stays wrong" hardly at all, because a wrong account would say the same thing. Only independent evidence moves "stays wrong".

- **Keep the principle and the drafted numbers**, and show a sensitivity table with every ratio halved and doubled.
- Keep the principle, and you set the anchors yourself: a preliminary published report (now 0.1 and 0.6), a regulator's finding (0.02 and 0.05).

**4. Attack priors: assumed or measured?** The draft assumes 2% to 5% by class.

- **Assumed for version 1, with the three observers spreading them ninefold; measured for version 2** from the archive's event list, class by class, wherever there are at least 20 events.
- Measured before any freeze. This is the long road in item 1.

The first measurements say one thing here. Seven federal systems turned up by accident and two were security incidents. That is a tilted sample, but 3% for federal systems is the prior most likely to be wrong.

The search you asked for on the 17th, for outages first called "not an attack" and later reclassified, has not been started. It would also give the number behind the draft's four-day median for an honest account to correct itself. Say the word and it starts with its own protocol.

**5. The campaign layer.** The draft counts events for 14 days after the ground stop, with a campaign adding 3 a week to a base rate centred on 2 a week.

- **Let a campaign start before the ground stop**: count over a calendar window fixed in advance, 1 October to 30 November. The two October security incidents (the bankruptcy courts' noticing system and FEC filing) then count. Keep the 14 days after the ground stop for the attention analysis only.
- Keep the window as drafted, starting at the ground stop.

**6. Three observers or one prior?**

- **Three** (calm, middle, suspicious). If they converge the evidence is doing the work.
- One.

## Four smaller ones the measurements raised

**7. The outside counter.** The draft lets a ThousandEyes z-score move the campaign odds up to fivefold. On 87 past weeks it reads high 26% of the time and did not rise in the weeks of the AWS, Azure or Cloudflare outages.

- **Take it out of the model** and keep it as a chart.
- Keep it, capped at a factor of 1.5.

**8. Quiet-week visibility.** The draft says a tier-B event has a 0.25 chance of being national news in a quiet week. For short airline groundings the measured figure is 5 of 6.

- **Set visibility by class from measurement where there is one**, and keep the tier figures elsewhere.
- Keep the tier figures.

**9. Knock-ons and denied reports.** Amtrak's outage was a knock-on of the ground stop. The Weather Service outage was denied by the agency. The draft has no rule for either.

- **Add both**: an event caused by a logged event is recorded but not counted as an arrival, and a report the organisation denies enters with a 0.2 chance of having happened.
- Leave them out of the log altogether.

**10. Federal systems.** The panel says "any U.S. federal agency system", which cannot be counted.

- **Use the fixed list in `measurements/PROTOCOL-2.md`.**
- Keep it open-ended and accept that its base rate is a guess.

## Three that are not about the model

**11. The source of truth.** On the 17th you asked for the rules to be written down before agents run, with "some sort of source of truth for validating". I took that to mean: the repo is the source of truth, rules are committed before the rows they score, and `scripts/validate.py` checks that from git history. Is that what you meant?

**12. Cisco or Juniper.** Chapter 2, on `main`, says the FAA's router was "reportedly Cisco". The FAA's own page of 15 November says Juniper.

- **Add a dated note to chapter 2 now.** A note is not a rewrite, and the public page is contradicted by the primary source.
- Hold it for the one-time revision with everything else.

**13. The Wall Street Journal's NSA story.** It is the best remaining check on whether the software-update account is independent of CNN's six sources, and it is behind a paywall.

- **Paste the text into a chat**, or
- let a session read it through the browser on your computer, signed in as you.
