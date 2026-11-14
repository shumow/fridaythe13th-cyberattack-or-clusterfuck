#!/usr/bin/env python3
"""Every number in the README, reproduced.

Standard library only. Run:  python3 scripts/show_your_work.py

Inputs marked ASSUMED are guesses, stated so they can be argued with.
Inputs marked REPORTED come from the sources listed in the README.
"""
import math
from datetime import date, datetime
from statistics import NormalDist


def sigma(p):
    """One-sided normal equivalent of a tail probability."""
    return NormalDist().inv_cdf(1 - p)


def section(title):
    print(f"\n== {title} ==")


# --------------------------------------------------------------------------
section("Calendar")
ground_stop = datetime(2026, 11, 13, 15, 54)      # REPORTED, Eastern
exchange_start = datetime(2026, 11, 12, 11, 17)   # REPORTED, Eastern
queues_reduced = datetime(2026, 11, 13, 12, 6)    # REPORTED, Eastern
print("13 Nov 2026 is a", date(2026, 11, 13).strftime("%A"))
tuesdays = [d for d in range(1, 31) if date(2026, 11, d).weekday() == 1]
print("Patch Tuesday (second Tuesday) is 10 Nov:", tuesdays[1] == 10)
print("Exchange incident start -> ground stop:", ground_stop - exchange_start)
print("Mail queues 'significantly reduced' -> ground stop:",
      ground_stop - queues_reduced)

# --------------------------------------------------------------------------
section("Correlation: how surprising is the overlap?")
# Major Microsoft 365 outages as a Poisson process.
# lam: major outages per year (first-pass count: 3 to 4).            ASSUMED
# cover: days of exposure per outage (this one was open 1.2 days
#        at the ground stop; 2 days is the generous window).         ASSUMED
for lam, cover in ((3, 1.2), (3, 2.0), (4, 2.0)):
    p0 = 1 - math.exp(-lam * cover / 365)
    print(f"lambda_M={lam}/yr, exposure={cover} d: "
          f"p0={p0:.2%}  ({sigma(p0):.1f} sigma, one-sided)")

section("Look-elsewhere: nobody picked Microsoft in advance")
# k: other notable incidents that week which would also have felt
#    like a coincidence had they lined up.                           ASSUMED
k = 10
for p0 in (0.0098, 0.0163, 0.0217):
    p_any = 1 - (1 - p0) ** k
    print(f"p0={p0:.2%}, k={k}: P(at least one lines up)={p_any:.1%}  "
          f"({sigma(p_any):.1f} sigma)")

# --------------------------------------------------------------------------
section("The identity: odds(caused : coincidence) = epsilon / (lambda_G * W)")
# lambda_G: nationwide ground stops per year (2 since 2001).         REPORTED
# W: the window in which we would call two events a pair.            ASSUMED
lam_g = 2 / 25
window_years = 2 / 365
threshold = lam_g * window_years
print(f"lambda_G * W = {threshold:.2e}  (even odds at epsilon = 1 in "
      f"{1 / threshold:,.0f})")
for label, eps in (("1 in 50,000", 1 / 50_000), ("1 in 10,000", 1 / 10_000),
                   ("1 in 2,300", threshold), ("1 in 1,000", 1 / 1_000),
                   ("1 in 250", 1 / 250)):
    odds = eps / threshold
    print(f"epsilon = {label:>11}: odds = {odds:5.2f}, "
          f"P(link) = {odds / (1 + odds):.0%}")

section("What history can bound")
# n_prior: major Microsoft 365 outages before this one, none followed
#          by a nationwide ground stop. Rate times ~13 years, not a
#          count.                                                    ASSUMED
n_prior = 45
upper = 3 / n_prior  # rule of three, ~95% upper bound on a zero count
print(f"0 ground stops in ~{n_prior} outages: epsilon < {upper:.1%}")
print(f"That bound is {upper / threshold:.0f}x above the even-odds "
      f"threshold.")

# --------------------------------------------------------------------------
section("Causation: probability of causation, given an update did it")
# d:  P(contractor operations still degraded on Friday afternoon).   ASSUMED
# rr: relative risk of a failed update under degraded operations.    ASSUMED
for d, rr in ((0.2, 1.3), (0.05, 1.1), (0.3, 2.0)):
    p = d * (rr - 1) / rr
    odds_after = p / (1 - p) / 2  # denials treated as a factor of 2. ASSUMED
    print(f"d={d}, RR={rr}: P(Microsoft contributed) = {p:.1%}; "
          f"after halving the odds for the denials: "
          f"{odds_after / (1 + odds_after):.1%}")
print("Taking the denials fully at face value: 0%.")
