#!/usr/bin/env python3
"""Chapter 2 (17 Nov 2026): the cluster. Every number in that chapter.

Standard library only. From the repo root:

    python3 scripts/the_week_after.py            # 100,000 runs per rate
    python3 scripts/the_week_after.py 20000      # quicker

Reads data/outages.csv, data/denials.csv, data/optimizely-affected.txt.
Friday's script, show_your_work.py, is left exactly as it was.

ASSUMED = a guess, stated so it can be argued with.
REPORTED = from a source listed in the chapter.
"""
import csv
import math
import os
import random
import sys
from datetime import date, datetime, timezone
from statistics import NormalDist

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
SEED = 20261117
YEARS = 2          # length of the look-back, per the recipe
WINDOW_DAYS = 5    # the scan window, per the recipe


def section(title):
    print(f"\n== {title} ==")


def sigma(p):
    return NormalDist().inv_cdf(1 - p) if 0 < p < 1 else float("nan")


def data(name):
    return os.path.join(ROOT, "data", name)


# --------------------------------------------------------------------------
section("Corrections to Friday, from the accounts now on the record")
ms_end = datetime(2026, 11, 13, 16, 10, tzinfo=timezone.utc)      # REPORTED
ground_stop = datetime(2026, 11, 13, 20, 54, tzinfo=timezone.utc)  # REPORTED
print("Microsoft impact ended before the ground stop by:",
      ground_stop - ms_end)
print("16 Nov 2026 is a", date(2026, 11, 16).strftime("%A"),
      "and 17 Nov a", date(2026, 11, 17).strftime("%A"))

# --------------------------------------------------------------------------
section("The outage list (data/outages.csv)")
rows = list(csv.DictReader(open(data("outages.csv"), newline="")))
for r in rows:
    r["d"] = date.fromisoformat(r["date"])
week_start = date(2026, 11, 12)
before = [r for r in rows if r["d"] < week_start]
week = [r for r in rows if r["d"] >= week_start]
print("rows:", len(rows), "| before this week:", len(before),
      "| this week:", len(week))
by_status = {}
for r in rows:
    by_status[r["source_status"]] = by_status.get(r["source_status"], 0) + 1
print("how each row is sourced:", by_status)

look_back_start = date(2024, 11, 17)
days_all = (week_start - look_back_start).days
# The list is thin after January 2026: my own knowledge stops mid-2026 and
# the searches did not enumerate that stretch. So also fit the rate on the
# stretch that is well covered.                                    ASSUMED
covered_end = date(2026, 1, 31)
days_cov = (covered_end - look_back_start).days
rates = {}
for label, tiers in (("strict (tier A)", "A"), ("loose (A and B)", "AB")):
    n_all = sum(1 for r in before if r["tier"] in tiers)
    n_cov = sum(1 for r in before if r["tier"] in tiers
                and r["d"] <= covered_end)
    lam_all = n_all / days_all * 365
    lam_cov = n_cov / days_cov * 365
    rates[label] = lam_cov
    print(f"{label}: {n_all} events in {days_all} d = {lam_all:.1f}/yr "
          f"(lower bound); {n_cov} in the well-covered {days_cov} d "
          f"= {lam_cov:.1f}/yr")
for tiers, label in (("A", "strict"), ("AB", "loose")):
    names = [r["org"] for r in week if r["tier"] in tiers]
    print(f"this week, {label}: {len(names)} events:", ", ".join(names))

# --------------------------------------------------------------------------
section("Scan statistic: P(at least k events inside some 5-day window, "
        "anywhere in 2 years)")
# Homogeneous Poisson process at rate lam per year. For each simulated
# two-year history, slide a 5-day window along the sorted event times and
# take the largest count. Window placement is free, so the after-the-fact
# choice of window is already paid for. What is NOT paid for: choosing,
# after the fact, which events count. That is the lam axis.


def max_in_window(times, width):
    best = lo = 0
    for hi in range(len(times)):
        while times[hi] - times[lo] > width:
            lo += 1
        best = max(best, hi - lo + 1)
    return best


def scan(lam, runs, rng):
    horizon = 365 * YEARS
    per_day = lam / 365
    tally = [0] * 8  # tally[k] = runs whose best window holds >= k events
    for _ in range(runs):
        t, times = 0.0, []
        while True:
            t += rng.expovariate(per_day)
            if t > horizon:
                break
            times.append(t)
        m = max_in_window(times, WINDOW_DAYS) if times else 0
        for k in range(2, 8):
            if m >= k:
                tally[k] += 1
    return [c / runs for c in tally]


rng = random.Random(SEED)
grid = [5, 8, 12, 16, 20, 30, 40, 60]
print(f"runs per rate: {RUNS:,}; seed {SEED}; window {WINDOW_DAYS} d; "
      f"look-back {YEARS} yr")
print("lam/yr   " + "".join(f"k>={k:<7}" for k in range(2, 7)))
for lam in grid:
    p = scan(lam, RUNS, rng)
    print(f"{lam:>6}   " + "".join(f"{p[k]:<9.3f}" for k in range(2, 7)))
for label, lam in rates.items():
    p = scan(lam, RUNS, rng)
    print(f"fitted {label}, lam={lam:.1f}/yr: "
          + ", ".join(f"P(>={k})={p[k]:.3f}" for k in (3, 4, 6))
          + f"  [k>=4 is {sigma(p[4]):.1f} sigma]")

section("Sanity check on the simulation (first-order approximation)")
# Expected number of k-clusters ~ N * P(Poisson(mu) >= k-1), mu = lam*w/365.
for lam in (12, 30):
    mu = lam * WINDOW_DAYS / 365
    n = lam * YEARS
    tail3 = 1 - math.exp(-mu) * (1 + mu + mu * mu / 2)
    print(f"lam={lam}: P(>=4) is roughly 1-exp(-N*tail) = "
          f"{1 - math.exp(-n * tail3):.3f}")

# --------------------------------------------------------------------------
section("Denials as evidence (data/denials.csv)")
# lr = P(statement | it was an attack) / P(statement | it was not).  ASSUMED
den = list(csv.DictReader(open(data("denials.csv"), newline="")))
for r in den:
    print(f"  {r['event']:<16} lr={float(r['lr']):<5} {r['statement'][:58]}")
day_one = {"Microsoft 365": 0.9, "FAA": 0.9, "JPMorgan Chase": 0.7,
           "NSA Net": 0.9}
best = {}
for r in den:
    if r["event"] in day_one:
        best[r["event"]] = min(best.get(r["event"], 1.0), float(r["lr"]))
prod_day_one = math.prod(day_one.values())
prod_best = math.prod(best.values())
print(f"product, day-one denials only: {prod_day_one:.2f}")
print(f"product, strongest statement per event: {prod_best:.3f}  {best}")
for prior in (1e-2, 1e-3, 1e-4):  # prior P(all four were attacks)  ASSUMED
    def post(lr, p=prior):
        o = p / (1 - p) * lr
        return o / (1 + o)
    print(f"prior {prior:g}: after day-one denials {post(prod_day_one):.2g}; "
          f"after the specific accounts {post(prod_best):.2g}")

# --------------------------------------------------------------------------
section("The Optimizely overlap")
names = [ln.strip() for ln in open(data("optimizely-affected.txt"))
         if ln.strip() and not ln.startswith("#")]
news = [n.replace(" [news]", "") for n in names if n.endswith("[news]")]
print("organisations on the list:", len(names), "| news and media:",
      len(news))
print("snippets infected in Report URI's sweep: 186 of 1,611 =",
      f"{186 / 1611:.1%}")                                        # REPORTED
# Reference set of large U.S. news sites.                          ASSUMED
top_us = ["CNN", "Fox News", "The New York Times", "NBC News", "CBS News",
          "ABC News", "The Washington Post", "USA Today", "NPR",
          "The Wall Street Journal"]
hit = [o for o in top_us if o in news]
print(f"of {len(top_us)} large U.S. news sites, on the list: {len(hit)} "
      f"({', '.join(hit)}) = {len(hit) / len(top_us):.0%}")
clean = datetime(2026, 11, 16, 23, 11, tzinfo=timezone.utc)       # REPORTED
first = datetime(2026, 11, 16, 4, 21, tzinfo=timezone.utc)        # REPORTED
nsa_copy = datetime(2026, 11, 17, 16, 41, tzinfo=timezone.utc)    # REPORTED
chase_start = datetime(2026, 11, 16, 14, 0, tzinfo=timezone.utc)  # REPORTED
print("malicious code live for at most:", clean - first)
print("NSA story (WRAL copy) published after the all-clean by:",
      nsa_copy - clean)
print("Chase outage began inside the compromise window:",
      first < chase_start < clean)
