# Model v1

> **DRAFT for review, 17 November 2026. Not frozen.** Every number below is a judgment made today, after seeing the week's reports. No data has been logged or run through it. It becomes model v1 only when a commit adds `model/model_v1.sha256`; until then it may change.

## What it answers

1. How likely is a coordinated campaign this week?
2. For each outage, how likely is it that the cause was an attack, and if so, is the public account honestly premature or will it stay wrong?
3. How likely is it that at least one of the outages was an attack?
4. How much of the cluster is attention: how many of the logged events would have been national news in a quiet week, and how often would a week like this one show this many with nothing unusual going on?

## The log

One file, `log/log.csv`, one row per event, statement or measurement. Rows are only ever added. A mistake is fixed by a `correction` row that names the row it supersedes.

| Column | Meaning |
| --- | --- |
| `row_id` | 1, 2, 3 ... |
| `logged_at` | when the row was written |
| `phase` | `retrospective` if it was known before the freeze, `prospective` after |
| `kind` | `event`, one of the statement kinds below, `existence`, `instrument`, `correction`, `checkpoint`, `context` |
| `event_id` | which outage the row is about |
| `known_at` | when it became public (retrospective) or when it was logged (prospective); the model's clock |
| `occurred_at` | when the outage began or the statement was made |
| `org`, `class`, `tier`, `counted` | for events: who, which class, which tier, and whether it meets the inclusion rule |
| `value`, `supersedes` | extra fields for some kinds |
| `source`, `source_status` | where it comes from, and whether that page was `opened`, read in a `browser`, seen through a `relay`, seen as an `excerpt`, or recalled from `memory` |

**Inclusion rule.** An event counts when the organisation is on the panel, an IT or communications system was down or degraded for at least 30 minutes, and a national outlet or wire reported it within 48 hours. The panel and the outlet list are fixed in `model_v1.json`: federal agencies, eleven airlines and Amtrak, sixteen banks and payment rails, six carriers, seven cloud providers, four market operators.

**Tiers.** A: a nationwide interruption affecting the public for three hours or more. B: a partial or short disruption at one organisation. C: an internal system, public only through leaks.

## Three states per event

- **Benign.** An accident or a self-inflicted failure.
- **Attack, account premature.** It was an attack and the organisation does not know yet.
- **Attack, account stays wrong.** It was an attack and the public account remains incorrect, for whatever reason. No motive is modelled.

| Class | P(attack) before any statement | P(account stays wrong, given attack) |
| --- | --- | --- |
| Cloud and SaaS | 5% | 15% |
| Aviation system (federal) | 2% | 30% |
| Airline operations | 3% | 15% |
| Bank or payment rail | 3% | 15% |
| Rail | 2% | 25% |
| Telecom, markets | 3% | 15% |
| Federal civil | 3% | 30% |
| Federal classified | 5% | 80% |

The low "stays wrong" share for listed companies rests on disclosure law: a company that knows it was attacked and says otherwise is exposed. The high share for a classified network rests on the opposite: nothing obliges disclosure.

## What a statement is worth

Each kind has two likelihood ratios: the probability of seeing it if the event was an attack with a premature account, and if it was an attack with an account that stays wrong, each divided by the probability of seeing it if the event was benign.

| Kind | Against "premature" | Against "stays wrong" |
| --- | --- | --- |
| `denial_generic`: "no indication", on the day | 0.9 | 1.0 |
| `mechanism_anonymous`: unnamed sources give a cause | 0.7 | 0.95 |
| `mechanism_named`: a named official or the organisation gives a specific cause | 0.4 | 0.9 |
| `rca_preliminary`: a published report with an internal mechanism | 0.1 | 0.6 |
| `rca_final`: the final published report | 0.03 | 0.5 |
| `independent_corroboration`: a party with direct sight and no stake | 0.3 | 0.3 |
| `regulator_finding`: a regulator, inspector general or Congress | 0.02 | 0.05 |
| `official_contradiction`: officials' accounts conflict | 1.5 | 1.2 |
| `attack_claim_unverified` | 2 | 2 |
| `attack_attribution_credible` | 30 | 30 |
| `official_reversal` | 1000 | 1000 |

Two rules stop double counting. The responsible side's own statements form a ladder, from generic denial up to final report, and only the highest rung reached counts. Everything else multiplies, once per speaker.

The second column is the point of the design. A statement from the party that issued the denial barely moves "stays wrong", because a wrong account would say the same thing. Only independent evidence does.

## Time

Silence is evidence. If an attack is behind an honestly premature account, the truth tends to surface within days; the model uses a median of 4 days. If the account stays wrong, it surfaces slowly; the model uses a median of 180 days. Each quiet day multiplies the two attack states by those survival curves and leaves "benign" alone.

## The campaign layer

Under "no campaign", counted events arrive at an unknown rate of λ per week, and each is an attack with its class prior. Under "campaign", attacks add 3 events per week, so an event is a campaign attack with probability 3 / (λ + 3).

- The prior on λ is lognormal with median 2 per week and a wide spread (90% between about 0.5 and 7.5).
- The count that matters is the number of counted events after the ground stop, within a 14-day attention window.
- A fixed-threshold measurement, such as a third party's weekly outage count, enters as a z-score against its own recent weeks and moves the campaign odds by exp(z − ½), capped at a factor of 5 either way.

**Frequency illusion** shows up three ways: the sum of quiet-week visibilities over the logged events (A 0.95, B 0.25, C 0.03); the chance that a primed window of this length holds at least this many events with nothing unusual, averaged over the prior on λ; and the fixed-threshold measurement, which attention cannot inflate.

## Three observers

| Observer | P(campaign) to start | Attack priors |
| --- | --- | --- |
| Calm | 0.1% | one third of the table |
| Middle | 1% | the table |
| Suspicious | 10% | three times the table |

If the three converge, the evidence is doing the work. If they do not, the priors are.

## What comes out

After every row: P(campaign) and P(at least one attack) for each observer, the post-ground-stop count and its tail probability, and the quiet-week-visible count. For each event at the latest row: P(attack) per observer, split into premature and stays wrong, and P(the event happened as reported).

## Rules

1. The log only grows.
2. This file, `model_v1.json` and `scripts/pipeline.py` are frozen by the commit that adds `model/model_v1.sha256`. That commit comes before any row, and the three files never change after it.
3. A change to the model is version 2, with a changelog, and the whole log is rerun through both.
4. Friday's analysis is revised once, when Microsoft's final report and the FAA's findings are published.
5. `scripts/validate.py` checks all of this against git history and reruns the pipeline.

## What freezing does not fix

- The hypotheses, classes, tiers and every number here were chosen after seeing the week's events.
- The answers inherit the priors. The movement per row means more than the level.
- Outages are not Poisson, and attention fades rather than switching off after 14 days.
- "Stays wrong" is close to unfalsifiable from the denying party's own statements. That is deliberate, and it is the residue this model cannot remove.

## Open choices

- Whether the three states are the right ones.
- The two columns of likelihood ratios.
- Whether attack priors should be measured from a reference class before the freeze, not assumed.
- The campaign layer: the extra rate of 3 per week, the prior on λ, the 14-day window.
- Three observers, or one prior.
