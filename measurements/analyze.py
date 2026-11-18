#!/usr/bin/env python3
"""Summaries for the frequency-illusion measurements. Standard library only.

    python3 measurements/analyze.py > measurements/analyze-output.txt

Reads the CSV files in this folder and data/outages.csv. Every number in
measurements/RESULTS.md comes from this script's output.
"""
import csv
import math
import os
import random
from datetime import date, timedelta
from statistics import mean, median, stdev
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
# The national outlets' own domains, as fixed in PROTOCOL.md.
NATIONAL = ["apnews.com", "reuters.com", "bloomberg.com", "nytimes.com",
            "wsj.com", "washingtonpost.com", "cnn.com", "nbcnews.com",
            "abcnews.go.com", "abcnews.com", "cbsnews.com", "foxnews.com",
            "npr.org", "cnbc.com", "usatoday.com", "axios.com", "time.com"]
TARGET_START = date(2026, 11, 9)
SEED = 20261117


def rows(name, folder=HERE):
    with open(os.path.join(folder, name), newline="") as fh:
        return list(csv.DictReader(fh))


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def monday(d):
    return d - timedelta(days=d.weekday())


def is_national(url):
    host = urlparse(url).netloc.lower()
    host = host[4:] if host.startswith("www.") else host
    return any(host == d or host.endswith("." + d) for d in NATIONAL)


# ---------------------------------------------------------------- A
print("== A. Fixed-threshold instrument: ThousandEyes weekly U.S. outage "
      "counts ==")
a = rows("a_instrument.csv")
series = sorted((date.fromisoformat(r["week_start"]), int(r["us_outages"]))
                for r in a if r["us_outages"])
base = [int(r["us_outages"]) for r in a if r["role"] == "baseline"]
m, s = mean(base), stdev(base)
print(f"protocol baseline, 8 weeks from 14 Sep to 8 Nov 2026: mean {m:.1f}; "
      f"sample sd {s:.1f}; range {min(base)} to {max(base)}")
print(f"a target week reads 'mildly high' above {m + s:.0f} and 'elevated' "
      f"above {m + 2 * s:.0f}")
y2026 = [x for d, x in series if d >= date(2025, 12, 29)]
for r in a:
    if r["role"] != "target":
        continue
    if r["us_outages"]:
        x = int(r["us_outages"])
        rank = 1 + sum(v > x for v in y2026)
        print(f"target week of {r['week_start']}: {x}; z = {(x - m) / s:.2f}; "
              f"rank {rank} of {len(y2026) + 1} weeks of 2026")
    else:
        print(f"target week of {r['week_start']}: not yet published")
print(f"weeks of 2026 published: {len(y2026)}; lowest {min(y2026)}, median "
      f"{median(y2026):.0f}, highest {max(y2026)}")
print(f"of those, above the 'mildly high' line: "
      f"{sum(v > m + s for v in y2026)}; above the 'elevated' line: "
      f"{sum(v > m + 2 * s for v in y2026)}")
print(f"whole series: {len(series)} weeks, {series[0][0]} to {series[-1][0]}; "
      f"not on the page: "
      f"{', '.join(r['week_start'] for r in a if r['role'] == 'missing')}")
print("median U.S. count by calendar quarter (the level drifts):")
quarters = {}
for d, x in series:
    quarters.setdefault((d.year, (d.month - 1) // 3 + 1), []).append(x)
print("  " + "; ".join(f"{y} Q{q}: {median(v):.0f}"
                       for (y, q), v in sorted(quarters.items())))
steps = [abs(series[i][1] - series[i - 1][1]) for i in range(1, len(series))]
print(f"median change from one published week to the next: "
      f"{median(steps):.0f}; largest: {max(steps)}")

print("\n-- the protocol's statistic applied to every past week --")
print("z = (week - mean of the 8 published weeks before it) / their sample sd")
zs = {}
for i in range(8, len(series)):
    prev = [x for _, x in series[i - 8:i]]
    zs[series[i][0]] = (series[i][1] - mean(prev)) / stdev(prev)
n = len(zs)
hi1 = sum(z >= 1 for z in zs.values())
hi2 = sum(z >= 2 for z in zs.values())
lo1 = sum(z <= -1 for z in zs.values())
lo2 = sum(z <= -2 for z in zs.values())
print(f"weeks with a z: {n}")
print(f"read 'mildly high' or more (z >= 1): {hi1} ({hi1 / n:.0%}); "
      f"'elevated' (z >= 2): {hi2} ({hi2 / n:.0%})")
print(f"read z <= -1: {lo1} ({lo1 / n:.0%}); z <= -2: {lo2} ({lo2 / n:.0%})")
rng = random.Random(SEED)
sims = 200_000
c1 = c2 = 0
for _ in range(sims):
    draw = [rng.gauss(0, 1) for _ in range(9)]
    z = (draw[8] - mean(draw[:8])) / stdev(draw[:8])
    c1 += z >= 1
    c2 += z >= 2
print(f"for comparison, independent noise with no drift ({sims:,} simulated "
      f"weeks, seed {SEED}): z >= 1 in {c1 / sims:.0%}, z >= 2 in "
      f"{c2 / sims:.1%}")

print("\n-- does it move in weeks with a known major outage? --")
print("tier-A rows of data/outages.csv before 9 Nov 2026 (* = from memory)")
known = []
for r in rows("outages.csv", os.path.join(ROOT, "data")):
    d = date.fromisoformat(r["date"])
    if r["tier"] != "A" or d >= TARGET_START or monday(d) not in zs:
        continue
    w = monday(d)
    star = "*" if r["source_status"] == "memory" else " "
    count = dict(series)[w]
    known.append((w, zs[w], r["source_status"]))
    print(f"  {r['date']}{star} {r['org'][:24]:<24} week count {count:>3}  "
          f"z = {zs[w]:+.2f}")
weeks_known = {}
for w, z, status in known:
    weeks_known.setdefault(w, []).append(status)
zk = [zs[w] for w in weeks_known]
k1 = sum(z >= 1 for z in zk)
print(f"distinct weeks: {len(zk)}; reading z >= 1: {k1} "
      f"({k1 / len(zk):.0%}); z <= -1: {sum(z <= -1 for z in zk)}; "
      f"median z {median(zk):+.2f}")
sourced = [zs[w] for w, st in weeks_known.items()
           if any(x != "memory" for x in st)]
print(f"leaving out weeks known only from memory: {len(sourced)} weeks; "
      f"z >= 1: {sum(z >= 1 for z in sourced)}; z <= -1: "
      f"{sum(z <= -1 for z in sourced)}; median z {median(sourced):+.2f}")
others = [z for w, z in zs.items() if w not in weeks_known]
o1 = sum(z >= 1 for z in others)
print(f"all other weeks: {len(others)}; reading z >= 1: {o1} "
      f"({o1 / len(others):.0%}); median z {median(others):+.2f}")

# ---------------------------------------------------------------- B
print("\n== B. The inclusion rule applied backwards: pilot ==")
raw = rows("b_raw_results.csv")
events = rows("b_backwards.csv")
pages = rows("b_pages_opened.csv")
weeks = sorted({(r["week_start"], r["role"]) for r in raw},
               key=lambda t: (t[1] != "baseline", t[0]))
print(f"searches kept: {len({(r['week_start'], r['sector']) for r in raw})}; "
      f"results returned: {len(raw)}")
tot_in = 0
for ws, role in weeks:
    rr = [r for r in raw if r["week_start"] == ws]
    inside = sum(r["inside_requested_week"] == "yes" for r in rr)
    outside = sum(r["inside_requested_week"] == "no" for r in rr)
    unknown = len(rr) - inside - outside
    tot_in += inside
    ev = [e for e in events if e["week_start"] == ws]
    found = [e for e in ev if e["found_by_search"] == "yes"]
    by_rule = [e for e in found
               if e["status"].startswith(("confirmed", "candidate"))]
    standing = [e for e in by_rule if "contradicted" not in e["status"]]
    unresolved = [e for e in found if e["status"] == "unresolved"]
    kn = [e for e in ev if e["in_outages_csv"].startswith("yes")]
    kn_found = [e for e in kn if e["found_by_search"] == "yes"]
    opened = sum(p["week_charged"] == ws and p["in_page_budget"] == "yes"
                 for p in pages)
    print(f"week of {ws} ({role}): {len(rr)} results; about an event inside "
          f"the week {inside}, outside it {outside}, cannot be placed "
          f"{unknown}")
    print(f"    events by the rule: {len(by_rule)} "
          f"({sum(e['status'] == 'confirmed' for e in by_rule)} confirmed); "
          f"still standing after extra reading: {len(standing)}; unresolved: "
          f"{len(unresolved)}; pages opened within the budget: {opened}")
    if kn:
        print(f"    events already in data/outages.csv for this week: "
              f"{len(kn)}; returned by the search: {len(kn_found)}")
    else:
        print("    no event in data/outages.csv for this week, so no check "
              "on what the search missed")
print(f"share of all results about an event inside the week asked for: "
      f"{tot_in}/{len(raw)} ({tot_in / len(raw):.0%})")
base_rows = [r for r in raw if r["role"] == "baseline"]
print(f"the same share for the two baseline weeks: "
      f"{sum(r['inside_requested_week'] == 'yes' for r in base_rows)}/"
      f"{len(base_rows)}")
for ws, role in weeks:
    if role != "baseline":
        continue
    air = [r for r in raw if r["week_start"] == ws
           and r["sector"] == "airlines and rail"]
    tally = {}
    for r in air:
        key = (r["subject"], r["subject_date"])
        tally[key] = tally.get(key, 0) + 1
    on_13_nov = sum(r["subject_date"] == "2026-11-13" for r in air)
    (subj, when), top = max(tally.items(), key=lambda kv: kv[1])
    print(f"airline query, week of {ws}: {len(air)} results; most common: "
          f"{subj}, {when} ({top}); about 13 Nov 2026: {on_13_nov}")
nat = [r for r in raw if is_national(r["url"])]
print(f"results on a national outlet's own domain: {len(nat)}/{len(raw)}"
      + "".join(f" ({urlparse(r['url']).netloc}: {r['subject']}, "
                f"{r['subject_date']})" for r in nat))
titles = sum(r["subject"].startswith("unknown") for r in raw)
print(f"results whose title is only a site name or page number: {titles}")
extra = sum(p["in_page_budget"] == "no" and p["read"] == "yes" for p in pages)
print(f"pages read outside the budget, for leads only: {extra}")

# ---------------------------------------------------------------- C
print("\n== C. Like for like: short system-wide groundings at panel "
      "airlines ==")
c = rows("c_like_for_like.csv")
strict = [r for r in c if r["qualifies"] == "yes"]
for label, group in (("qualifying (3 hours or less confirmed)", strict),
                     ("all six found", c)):
    n = len(group)
    k_list = sum(int(r["national_list_domains_in_results"]) > 0 for r in group)
    k_any = sum(int(r["national_list_domains_in_results"]) > 0 or
                int(r["national_wire_or_network_copies_in_results"]) > 0
                for r in group)
    lo, hi = wilson(k_any, n)
    print(f"{label}: n={n}; a national outlet's own domain in the results: "
          f"{k_list}; a national wire or network story visible, own domain "
          f"or copy: {k_any} ({k_any / n:.0%}, 95% interval {lo:.0%} to "
          f"{hi:.0%})")
dates = sorted(r["event_date"] for r in c)
years = 2.0
print(f"events found in the two-year window: {len(c)} "
      f"(first {dates[0]}, last {dates[-1]}): at least {len(c) / years:.1f} "
      f"a year, a lower bound from three searches")
rate = len(c) / years
print(f"chance of at least one such grounding in any given 5 days at that "
      f"rate: {1 - math.exp(-rate * 5 / 365):.1%}")

# ---------------------------------------------------------------- by-catch
print("\n== By-catch: dated events the pilot turned up while looking for "
      "other weeks ==")
y = rows("bycatch.csv")
win = [r for r in y if r["in_two_year_window"] == "yes"]
new = [r for r in win if r["in_outages_csv"] == "no"]
fed = [r for r in new if r["class"] == "federal"]
sec = [r for r in fed if r["security_incident"].startswith("yes")]
print(f"dated events at panel organisations: {len(y)}; inside the two-year "
      f"window: {len(win)}; of those, absent from data/outages.csv: "
      f"{len(new)}")
print(f"absent ones by class: federal {len(fed)}, other "
      f"{len(new) - len(fed)}")
lo, hi = wilson(len(sec), len(fed))
print(f"federal ones described as a security incident: {len(sec)} of "
      f"{len(fed)} (95% interval {lo:.0%} to {hi:.0%}; an accidental sample, "
      f"not an estimate)")
for r in sec:
    print(f"    {r['event_date']} {r['org']}: {r['what']}")
table = {(r["date"], r["org"]) for r in
         rows("outages.csv", os.path.join(ROOT, "data"))}
c_absent = [r for r in c if not any(d == r["event_date"] and
                                    r["airline"] in org for d, org in table)]
both = {(r["event_date"], r["airline"]) for r in c_absent} | {
    (r["event_date"], r["org"].split()[0]) for r in new}
print(f"measurement C's groundings absent from data/outages.csv: "
      f"{len(c_absent)} of {len(c)}")
print(f"absent events from both sources, counted once: {len(both)}")
