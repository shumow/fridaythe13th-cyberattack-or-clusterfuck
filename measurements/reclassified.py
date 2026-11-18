#!/usr/bin/env python3
"""Counts for the reclassified-outages search (PROTOCOL-3.md).

    python3 measurements/reclassified.py

Standard library only. Reads r1_raw_results.csv, r1_events.csv and
r_pages_opened.csv. Every number in RESULTS-3.md comes from this output.
"""
import csv, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
def rows(n):
    with open(os.path.join(HERE, n), newline="") as f:
        return list(csv.DictReader(f))
raw, ev, pages = rows("r1_raw_results.csv"), rows("r1_events.csv"), rows("r_pages_opened.csv")
print(f"R1 searches run: {len({r['query_no'] for r in raw})}; results saved: {len(raw)}")
c = Counter(r["about"] for r in raw)
for k, v in c.most_common():
    print(f"  {k}: {v} ({100*v/len(raw):.0f}%)")
print("  by query, share about this week's outages:")
for q in sorted({r['query_no'] for r in raw}):
    sub = [r for r in raw if r['query_no'] == q]
    w = sum(r['about'] == "this week's outages" for r in sub)
    print(f"    query {q}: {w} of {len(sub)}")
print(f"Pages attempted: {len(pages)}; opened: {sum(not r['result'].startswith('not opened') for r in pages)}")
print(f"Candidate past cases: {len(ev)}")
s = Counter(r["status"].split(":")[0] for r in ev)
for k, v in s.items():
    print(f"  {k}: {v}")
fixed = [r for r in ev if r["delay_days"].isdigit() and r["status"].startswith("reclassified")]
print(f"Reclassified events with both dates fixed: {len(fixed)}")
