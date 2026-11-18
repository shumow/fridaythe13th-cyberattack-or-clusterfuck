#!/usr/bin/env python3
"""Numbers and the chart for PROTOCOL-3.md.

    python3 measurements/nw_analyze.py > measurements/nw_analyze-output.txt

Reads a_instrument.csv (the outside counter) and, when it exists,
nw_series.csv (the archive's daily counts, written by nw_fetch.py). Every
number in RESULTS-3.md comes from this script's output. Standard library
only; the chart needs matplotlib and is skipped without it.

    python3 measurements/nw_analyze.py --dir SOMEWHERE

reads nw_series.csv from another folder and writes the chart there. That is
for testing the arithmetic on made-up counts without touching this folder.
"""
import csv
import os
import sys
from datetime import date, timedelta
from statistics import mean, median, stdev

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = sys.argv[sys.argv.index("--dir") + 1] if "--dir" in sys.argv else HERE

# The periods fixed in PROTOCOL-3.md. Days are UTC days.
WEEKS = [date(2026, 8, 17) + timedelta(days=7 * i) for i in range(13)]
BASE, TARGET = WEEKS[:12], WEEKS[12]
AFTER = [date(2026, 11, 13) + timedelta(days=i) for i in range(5)]
FROM_9TH = [date(2026, 11, 9) + timedelta(days=i) for i in range(9)]
assert TARGET == date(2026, 11, 9) and BASE[0].weekday() == 0


def z(x, base):
    sd = stdev(base)
    return (x - mean(base)) / sd if sd else float("nan")


def rank(x, base):
    return 1 + sum(b > x for b in base)


def days(week):
    return [week + timedelta(days=i) for i in range(7)]


def label(week):
    end = week + timedelta(days=6)
    return f"{week.day} {week.strftime('%b')} to {end.day} {end.strftime('%b')}"


# ------------------------------------------------------- the outside counter
print("== Events: the outside counter (ThousandEyes weekly U.S. outage "
      "counts, a_instrument.csv) ==")
with open(os.path.join(HERE, "a_instrument.csv"), newline="") as fh:
    counter = {date.fromisoformat(r["week_start"]): int(r["us_outages"])
               for r in csv.DictReader(fh) if r["us_outages"]}
e_base = [counter[w] for w in BASE]
print(f"baseline, 12 weeks from 17 Aug to 8 Nov 2026: mean {mean(e_base):.1f}; "
      f"sample sd {stdev(e_base):.1f}; range {min(e_base)} to {max(e_base)}")
e_index = None
if TARGET in counter:
    e_t = counter[TARGET]
    e_index = e_t / mean(e_base)
    print(f"week of 9 to 15 Nov: {e_t}; {e_index:.2f} times the baseline mean; "
          f"z = {z(e_t, e_base):+.2f}; rank {rank(e_t, e_base)} of 13")
else:
    print("week of 9 to 15 Nov: not published")

# ------------------------------------------------------------- the coverage
print("\n== Coverage: the news archive (nw_series.csv) ==")
path = os.path.join(WORK, "nw_series.csv")
if not os.path.exists(path):
    print("not measured: nw_series.csv does not exist. The archive has not "
          "answered; see nw_requests.csv.")
    print("\n== The multiplier ==\nnot computed: there is no coverage series.")
    sys.exit(0)

s = {}
with open(path, newline="") as fh:
    for r in csv.DictReader(fh):
        s.setdefault(r["query"], {})[date.fromisoformat(r["day_utc"])] = (
            int(r["articles"]), int(r["norm"]))
span = [WEEKS[0] + timedelta(days=i) for i in range(93)]
for q in sorted(s):
    gaps = [d for d in span if d not in s[q]]
    print(f"{q}: {len(s[q])} days in the file; missing from the 93: {len(gaps)}")


def total(q, ds):
    """(matching articles, all articles) summed over a list of days."""
    got = [s[q][d] for d in ds if d in s[q]]
    return sum(a for a, _ in got), sum(n for _, n in got)


def share(q, ds):
    a, n = total(q, ds)
    return a / n if n else float("nan")


def ratio(num, den, ds):
    a, b = total(num, ds)[0], total(den, ds)[0]
    return a / b if b else float("nan")


base_days = [d for w in BASE for d in days(w)]
c_index = None
for stat, q in ((1, "OUT_IT"), (2, "ATT")):
    if q not in s:
        continue
    print(f"\n-- statistic {stat}: weekly coverage, {q} --")
    shares = [share(q, days(w)) for w in BASE]
    counts = [total(q, days(w))[0] for w in BASE]
    st, ct = share(q, days(TARGET)), total(q, days(TARGET))[0]
    print(f"baseline weeks, matching articles per 10,000 monitored: "
          f"mean {1e4 * mean(shares):.2f}; sd {1e4 * stdev(shares):.2f}; "
          f"range {1e4 * min(shares):.2f} to {1e4 * max(shares):.2f}")
    print(f"week of 9 to 15 Nov: {1e4 * st:.2f}; {st / mean(shares):.2f} times "
          f"the baseline mean; z = {z(st, shares):+.2f}; rank "
          f"{rank(st, shares)} of 13")
    print(f"the same from raw counts: baseline mean {mean(counts):.0f} a week; "
          f"target {ct}; z = {z(ct, counts):+.2f}; rank {rank(ct, counts)} of 13")
    print(f"baseline daily mean: {1e4 * share(q, base_days):.2f}; "
          + "; ".join(f"{d.day} Nov: {1e4 * share(q, [d]):.2f}"
                      for d in (date(2026, 11, 16), date(2026, 11, 17))))
    if q == "OUT_IT":
        c_index = st / mean(shares)
        c_weekly = [x / mean(shares) for x in shares] + [c_index]

framing_weekly = None
for num in ("BOTH", "BOTH_STRICT"):
    if num not in s or "OUT_IT" not in s:
        continue
    print(f"\n-- statistic 3: the framing share, {num} / OUT_IT --")
    weekly = [ratio(num, "OUT_IT", days(w)) for w in BASE]
    ft = ratio(num, "OUT_IT", days(TARGET))
    print(f"pooled over the baseline: {ratio(num, 'OUT_IT', base_days):.1%}; "
          f"pooled over 13 to 17 Nov: {ratio(num, 'OUT_IT', AFTER):.1%}")
    print(f"twelve baseline weeks: lowest {min(weekly):.1%}, median "
          f"{median(weekly):.1%}, highest {max(weekly):.1%}")
    print(f"week of 9 to 15 Nov: {ft:.1%}; z = {z(ft, weekly):+.2f}; rank "
          f"{rank(ft, weekly)} of 13")
    print("by day: " + "; ".join(f"{d.day} Nov {ratio(num, 'OUT_IT', [d]):.1%}"
                                 for d in FROM_9TH))
    if num == "BOTH":
        framing_weekly = weekly + [ft]

print("\n-- statistic 4: the multiplier --")
if c_index is None or e_index is None:
    print("not computed: it needs both a coverage series and the counter's "
          "value for 9 to 15 Nov.")
else:
    print(f"coverage at {c_index:.2f} times its baseline, the outside counter "
          f"at {e_index:.2f} times its own: multiplier {c_index / e_index:.2f}")
    print("above 1 means coverage rose more than the counter did. The counter "
          "is a weak witness (RESULTS.md, part A).")

if "OUT_PLAIN" in s and "OUT_IT" in s:
    print("\n-- statistic 5: how much of OUT_PLAIN the second group keeps --")
    print(f"baseline: {ratio('OUT_IT', 'OUT_PLAIN', base_days):.1%}; "
          f"13 to 17 Nov: {ratio('OUT_IT', 'OUT_PLAIN', AFTER):.1%}")

# ----------------------------------------------------------------- the chart
if c_index is None:
    sys.exit(0)
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    print("\nchart skipped: matplotlib is not installed")
    sys.exit(0)

INK, MUTED, RULE, SURFACE = "#0b0b0b", "#898781", "#c3c2b7", "#fcfcfb"
BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#52514e"
x = list(range(13))
ticks = [f"{w.day} {w.strftime('%b')}" for w in WEEKS]
e_weekly = [counter[w] / mean(e_base) for w in BASE] + (
    [e_index] if e_index is not None else [])

fig, (top, low) = plt.subplots(
    2, 1, figsize=(8, 6.4), sharex=True, facecolor=SURFACE,
    gridspec_kw={"height_ratios": [3, 2], "hspace": 0.32})
for ax in (top, low):
    ax.set_facecolor(SURFACE)
    ax.axvspan(11.5, 12.5, color=RULE, alpha=0.25, lw=0)
    ax.grid(axis="y", color=RULE, lw=0.6, alpha=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(RULE)
    ax.tick_params(colors=MUTED, length=0, labelsize=9)

top.axhline(1, color=RULE, lw=1)
top.plot(x, c_weekly, color=BLUE, lw=2, marker="o", ms=5,
         label="Stories about outages (news archive)")
top.plot(x[:len(e_weekly)], e_weekly, color=ORANGE, lw=2, marker="o", ms=5,
         label="Outages counted (outside counter)")
top.annotate(f"{c_weekly[-1]:.2f}", (12, c_weekly[-1]), xytext=(8, 0),
             textcoords="offset points", va="center", color=INK, fontsize=9)
if len(e_weekly) == 13:
    top.annotate(f"{e_weekly[-1]:.2f}", (12, e_weekly[-1]), xytext=(8, 0),
                 textcoords="offset points", va="center", color=INK, fontsize=9)
top.set_ylim(bottom=0)
top.legend(loc="lower left", frameon=False, fontsize=9, labelcolor=GREY)
top.set_title("Stories about outages against outages counted, by week",
              loc="left", color=INK, fontsize=12, pad=22)
top.text(0, 1.04, "Each week as a multiple of its own average over the twelve "
         "weeks before 9 November 2026. Shaded: the week of the ground stop.",
         transform=top.transAxes, color=GREY, fontsize=8.5)

if framing_weekly is not None:
    low.plot(x, [100 * v for v in framing_weekly], color=GREY, lw=2,
             marker="o", ms=5)
    low.annotate(f"{100 * framing_weekly[-1]:.0f}%", (12, 100 * framing_weekly[-1]),
                 xytext=(8, 0), textcoords="offset points", va="center",
                 color=INK, fontsize=9)
    low.set_ylim(bottom=0)
low.set_title("Share of outage stories that also use an attack word (%)",
              loc="left", color=INK, fontsize=10.5)
low.set_xticks(x)
low.set_xticklabels(ticks, rotation=45, ha="right")
low.set_xlim(-0.4, 12.9)
low.set_xlabel("Week beginning", color=MUTED, fontsize=9)
out = os.path.join(WORK, "news-wave.png")
fig.savefig(out, dpi=160, bbox_inches="tight", facecolor=SURFACE)
print(f"\nchart written: {os.path.relpath(out, os.path.dirname(HERE))}")
