#!/usr/bin/env python3
"""The baseline weeks for measurement B, drawn once and in a fixed order.

    python3 measurements/sample_weeks.py

Population: the 104 Monday-starting weeks from 11 Nov 2024 to 2 Nov 2026,
the two years before the week of the ground stop. The seed is the date the
protocol was written. A pilot takes the first few weeks of the list and a
full run keeps going down it, so the pilot is a prefix of the full sample.
"""
import random
from datetime import date, timedelta

SEED = 20261117
first = date(2024, 11, 11)
weeks = [first + timedelta(days=7 * i) for i in range(104)]
assert weeks[-1] == date(2026, 11, 2) and all(w.weekday() == 0 for w in weeks)
order = random.Random(SEED).sample(weeks, 26)
if __name__ == "__main__":
    for i, w in enumerate(order, start=1):
        print(f"{i:2d}  week of {w.strftime('%B')} {w.day}, {w.year}")
