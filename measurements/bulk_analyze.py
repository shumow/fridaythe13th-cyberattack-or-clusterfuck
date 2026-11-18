#!/usr/bin/env python3
"""Counts and statistics for PROTOCOL-4.md, from the local GDELT table.

    .venv/bin/python measurements/bulk_analyze.py > measurements/bulk_analyze-output.txt

Needs DuckDB (in .venv). Reads bulk_queries.json for every pattern, theme
list and period; nothing about what is counted is decided in this file.
Writes the daily counts to bulk_series.csv and prints the seven statistics.
The chart needs matplotlib and is skipped without it.

    bulk_analyze.py --table GLOB --out DIR

reads another table and writes there: for testing the arithmetic on made-up
rows without touching the real table or this folder's outputs.

How a row is counted. DuckDB pulls every row whose lower-cased title contains
"outage", "ground stop", "cyber" or "hack": a superset of anything the
patterns can match. The patterns themselves are then applied here, in Python,
to the title lower-cased with its whitespace collapsed. Denominators (all rows
with a title, and all distinct titles, per day) are counted by DuckDB over the
whole table.
"""
import csv
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date, timedelta
from statistics import mean, median, stdev

import duckdb

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def opt(flag, default):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


with open(os.path.join(HERE, "bulk_queries.json")) as fh:
    Q = json.load(fh)
TABLE = opt("--table", os.path.join(ROOT, Q["table"]))
OUT = opt("--out", HERE)
PAT = {k: re.compile(v) for k, v in Q["title_patterns"].items()}
THEMES = {k: set(v) for k, v in Q["themes"].items()}
P = Q["periods"]
D = date.fromisoformat
BASE0, BASE1 = D(P["baseline_first_day"]), D(P["baseline_last_day"])
TARGET = tuple(D(x) for x in P["target_week"])
AFTER = tuple(D(x) for x in P["after"])
HEAD = tuple(D(x) for x in P["headline_window"])
EXCLUDED = {D(x) for x in P["excluded"]}
POPS = ("US", "ALL")
MEASURES = ("OUT_T", "OUT_TECH", "OUT_TECH_TH", "ATT_T", "BOTH_T",
            "BOTH_T_STRICT", "BOTH_TH", "BOTH_TH_STRICT")


def norm(title):
    return " ".join(title.lower().split())


def measures(title, themes):
    """The set of measures one row counts in. title is already normalised."""
    out = set()
    att_t = bool(PAT["ATT"].search(title))
    if att_t:
        out.add("ATT_T")
    if not PAT["OUT"].search(title):
        return out
    out.add("OUT_T")
    th = set(themes.split(";")) if themes else set()
    if not (th & THEMES["POWER"]):
        out.add("OUT_TECH_TH")
    if PAT["NOT_TECH"].search(title):
        return out
    out.add("OUT_TECH")
    if att_t:
        out.add("BOTH_T")
    if PAT["ATT_STRICT"].search(title):
        out.add("BOTH_T_STRICT")
    if th & THEMES["ATT"]:
        out.add("BOTH_TH")
    if th & THEMES["ATT_STRICT"]:
        out.add("BOTH_TH_STRICT")
    return out


def count():
    """{(day, pop, measure): [rows, distinct titles]}, 'ALL_ROWS' being the denominator."""
    con = duckdb.connect()
    src = f"read_parquet('{TABLE}', hive_partitioning=true)"
    ntitle = "lower(regexp_replace(trim(title), '\\s+', ' ', 'g'))"
    c = defaultdict(lambda: [0, 0])
    for day, us, rows, distinct in con.sql(f"""
            SELECT day_utc, coalesce(source_country = 'US', false) AS us,
                   count(*), count(DISTINCT {ntitle})
            FROM {src} WHERE title IS NOT NULL GROUP BY 1, 2""").fetchall():
        if us:
            c[(day, "US", "ALL_ROWS")] = [rows, distinct]
        c[(day, "ALL", "ALL_ROWS")][0] += rows
    # Distinct titles over all countries cannot be summed from the two halves.
    for day, distinct in con.sql(f"""
            SELECT day_utc, count(DISTINCT {ntitle}) FROM {src}
            WHERE title IS NOT NULL GROUP BY 1""").fetchall():
        c[(day, "ALL", "ALL_ROWS")][1] = distinct
    seen = defaultdict(set)
    for day, us, title, themes in con.sql(f"""
            SELECT day_utc, coalesce(source_country = 'US', false), title, themes
            FROM {src} WHERE title IS NOT NULL
              AND regexp_matches(lower(title), 'outage|ground\\s+stop|cyber|hack')
            """).fetchall():
        t = norm(title)
        for m in measures(t, themes):
            for pop in (("US", "ALL") if us else ("ALL",)):
                c[(day, pop, m)][0] += 1
                seen[(day, pop, m)].add(t)
    for k, titles in seen.items():
        c[k][1] = len(titles)
    return c


# ---------------------------------------------------------------- arithmetic

def days(a, b):
    return [a + timedelta(i) for i in range((b - a).days + 1)]


BASE_WEEKS = [(BASE0 + timedelta(7 * i), BASE0 + timedelta(7 * i + 6))
              for i in range(((BASE1 - BASE0).days + 1) // 7)]


def total(c, pop, m, a, b, col=0):
    return sum(c.get((d, pop, m), (0, 0))[col] for d in days(a, b))


def ratio(n, d):
    return n / d if d else float("nan")


def z_and_rank(target, base):
    z = (target - mean(base)) / stdev(base) if len(base) > 1 and stdev(base) else float("nan")
    rank = 1 + sum(1 for v in base if v > target)
    return z, rank


def pct(x):
    return "   n/a" if x != x else f"{100 * x:6.3f}%"


def spearman(xs, ys):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r, i = [0.0] * len(v), 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    rx, ry = ranks(xs), ranks(ys)
    mx, my = mean(rx), mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else float("nan")


def coverage(c, pop, m, label):
    """Statistics 1 and 2: weekly coverage of one measure."""
    for col, unit in ((0, "all rows"), (1, "distinct titles")):
        share = [ratio(total(c, pop, m, a, b, col), total(c, pop, "ALL_ROWS", a, b, col))
                 for a, b in BASE_WEEKS]
        raw = [total(c, pop, m, a, b, col) for a, b in BASE_WEEKS]
        t_share = ratio(total(c, pop, m, *TARGET, col), total(c, pop, "ALL_ROWS", *TARGET, col))
        t_raw = total(c, pop, m, *TARGET, col)
        z, r = z_and_rank(t_share, share)
        zr, rr = z_and_rank(t_raw, raw)
        print(f"  {label} [{pop}, {unit}]")
        print(f"    baseline weeks, share: lowest {pct(min(share))}  median {pct(median(share))}"
              f"  highest {pct(max(share))}  mean {pct(mean(share))}")
        print(f"    9 to 15 Nov, share: {pct(t_share)}  z = {z:+.2f}  rank {r} of {len(share) + 1}")
        print(f"    baseline weeks, count: lowest {min(raw)}  median {median(raw):g}"
              f"  highest {max(raw)}  mean {mean(raw):.1f}")
        print(f"    9 to 15 Nov, count: {t_raw}  z = {zr:+.2f}  rank {rr} of {len(raw) + 1}")
        base_days = [ratio(c.get((d, pop, m), (0, 0))[col], c.get((d, pop, "ALL_ROWS"), (0, 0))[col])
                     for d in days(BASE0, BASE1)]
        print(f"    baseline daily mean share {pct(mean(base_days))}; " + "; ".join(
            f"{d:%d %b} {pct(ratio(c.get((d, pop, m), (0, 0))[col], c.get((d, pop, 'ALL_ROWS'), (0, 0))[col]))}"
            for d in days(TARGET[1] + timedelta(1), AFTER[1])))
    return t_share, mean(share)


def framing(c, pop, num, den, label):
    """Statistics 3 and 4: the share of outage headlines that also carry num."""
    def f(a, b, col=0):
        return ratio(total(c, pop, num, a, b, col), total(c, pop, den, a, b, col))
    for col, unit in ((0, "all rows"), (1, "distinct titles")):
        weekly = [f(a, b, col) for a, b in BASE_WEEKS]
        thin = sum(1 for a, b in BASE_WEEKS if total(c, pop, den, a, b, col) < 20)
        ok = [w for w in weekly if w == w]
        z, r = z_and_rank(f(*TARGET, col), ok) if len(ok) > 1 else (float("nan"), 0)
        print(f"  {label} [{pop}, {unit}]")
        print(f"    baseline pooled {pct(f(BASE0, BASE1, col))} "
              f"({total(c, pop, num, BASE0, BASE1, col)} of {total(c, pop, den, BASE0, BASE1, col)});"
              f"  13 to 17 Nov pooled {pct(f(*AFTER, col))} "
              f"({total(c, pop, num, *AFTER, col)} of {total(c, pop, den, *AFTER, col)})")
        if ok:
            print(f"    baseline weeks: lowest {pct(min(ok))}  median {pct(median(ok))}  highest {pct(max(ok))}"
                  + (f"   [{thin} of {len(weekly)} baseline weeks have fewer than 20 {den}]" if thin else ""))
        print(f"    9 to 15 Nov {pct(f(*TARGET, col))}  z = {z:+.2f}  rank {r} of {len(ok) + 1}")
        pre = (HEAD[0], AFTER[0] - timedelta(1))
        print(f"    {pre[0]:%d} to {pre[1]:%d %b} {pct(f(*pre, col))} "
              f"({total(c, pop, num, *pre, col)} of {total(c, pop, den, *pre, col)})"
              f"  against 13 to 17 Nov {pct(f(*AFTER, col))}")
        print("    by day: " + "  ".join(
            f"{d:%d}:{c.get((d, pop, num), (0, 0))[col]}/{c.get((d, pop, den), (0, 0))[col]}"
            for d in days(TARGET[0], AFTER[1])))


def outside_counter():
    rows = {D(r["week_start"]): r["us_outages"]
            for r in csv.DictReader(open(os.path.join(HERE, "a_instrument.csv")))}
    base = [int(rows[a]) for a, _ in BASE_WEEKS if rows.get(a)]
    target = rows.get(TARGET[0])
    return base, (int(target) if target else None)


def api_series():
    path = os.path.join(HERE, "nw_series.csv")
    if not os.path.exists(path):
        return {}
    return {D(r["day_utc"]): (int(r["articles"]), int(r["norm"]))
            for r in csv.DictReader(open(path)) if r["query"] == "OUT_IT"}


def main():
    c = count()
    all_days = sorted({k[0] for k in c})
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "bulk_series.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["day_utc", "population", "measure", "rows", "distinct_titles"])
        for d in all_days:
            for pop in POPS:
                for m in ("ALL_ROWS",) + MEASURES:
                    w.writerow([d, pop, m, *c.get((d, pop, m), (0, 0))])

    print("PROTOCOL-4.md, from", TABLE)
    print(f"days in the table: {len(all_days)} ({all_days[0]} to {all_days[-1]}); "
          f"not used: {', '.join(str(d) for d in sorted(EXCLUDED))}")
    print(f"baseline: {len(BASE_WEEKS)} weeks, {BASE0} to {BASE1}; target week {TARGET[0]} to "
          f"{TARGET[1]}; after {AFTER[0]} to {AFTER[1]}")
    missing = [d for d in days(BASE0, AFTER[1]) if (d, "ALL", "ALL_ROWS") not in c]
    print("days with no rows:", missing or "none")

    cov = {}
    for pop in POPS:
        print(f"\n== 1. Weekly headline coverage, {pop} ==")
        cov[pop] = coverage(c, pop, "OUT_TECH", "OUT_TECH")
        coverage(c, pop, "OUT_TECH_TH", "OUT_TECH_TH (electricity removed by theme)")
        print(f"\n== 2. Attack headlines, {pop} ==")
        coverage(c, pop, "ATT_T", "ATT_T")
        print(f"\n== 3. Headline framing share, {pop} ==")
        framing(c, pop, "BOTH_T", "OUT_TECH", "BOTH_T / OUT_TECH")
        framing(c, pop, "BOTH_T_STRICT", "OUT_TECH", "BOTH_T_STRICT / OUT_TECH")
        print(f"\n== 4. Theme framing share, {pop} ==")
        framing(c, pop, "BOTH_TH", "OUT_TECH", "BOTH_TH / OUT_TECH")
        framing(c, pop, "BOTH_TH_STRICT", "OUT_TECH", "BOTH_TH_STRICT / OUT_TECH")

    print("\n== 5. The multiplier ==")
    base, target = outside_counter()
    if target is None or len(base) != len(BASE_WEEKS):
        print(f"  not computed: outside counter has {len(base)} of {len(BASE_WEEKS)} baseline "
              f"weeks and target {target}")
    else:
        counter = target / mean(base)
        print(f"  outside counter (U.S.): target {target}, baseline mean {mean(base):.1f}, "
              f"ratio {counter:.3f}")
        for pop in POPS:
            t, b = cov[pop]
            print(f"  {pop}: coverage ratio {t / b:.3f}; multiplier {t / b / counter:.3f}")

    print("\n== 6. What the exclusion removes ==")
    for pop in POPS:
        for m in ("OUT_TECH", "OUT_TECH_TH"):
            print(f"  {pop}: {m} / OUT_T  baseline "
                  f"{pct(ratio(total(c, pop, m, BASE0, BASE1), total(c, pop, 'OUT_T', BASE0, BASE1)))}"
                  f"  after {pct(ratio(total(c, pop, m, *AFTER), total(c, pop, 'OUT_T', *AFTER)))}")

    print("\n== 7. Against the search API (descriptive) ==")
    api = api_series()
    if not api:
        print("  nw_series.csv not found")
    else:
        med = median(n for _, n in api.values())
        good = [d for d, (_, n) in sorted(api.items()) if n >= 0.2 * med and (d, "US", "ALL_ROWS") in c]
        xs = [api[d][0] / api[d][1] for d in good]
        ys = [ratio(c.get((d, "US", "OUT_TECH"), (0, 0))[0], c[(d, "US", "ALL_ROWS")][0]) for d in good]
        print(f"  API days returned: {len(api)}; with norm at least 20% of its median ({med:g}): {len(good)}")
        if len(good) > 2:
            print(f"  rank correlation, API OUT_IT share against bulk OUT_TECH share (US): "
                  f"{spearman(xs, ys):+.3f} over {len(good)} days")
        print("  day: API norm / bulk U.S. rows with a title")
        for d, (_, n) in sorted(api.items()):
            print(f"    {d}  {n:>7} / {c.get((d, 'US', 'ALL_ROWS'), (0, 0))[0]:>7}")

    chart(c, base, target)
    return 0


def chart(c, base, target):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n(chart skipped: matplotlib is not installed)")
        return
    weeks = BASE_WEEKS + [TARGET]
    cover = [ratio(total(c, "US", "OUT_TECH", a, b), total(c, "US", "ALL_ROWS", a, b)) for a, b in weeks]
    cover = [v / mean(cover[:-1]) for v in cover]
    labels = [f"{a:%d %b}" for a, _ in weeks]
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    top.plot(labels, cover, marker="o", label="headline coverage (OUT_TECH share)")
    if target is not None and len(base) == len(BASE_WEEKS):
        top.plot(labels, [v / mean(base) for v in base + [target]], marker="s", label="outside counter (U.S.)")
    top.axhline(1, lw=0.5, color="grey")
    top.set_ylabel("index, baseline mean = 1")
    top.legend()
    for num, name in (("BOTH_T", "headline"), ("BOTH_TH", "theme")):
        bottom.plot(labels, [100 * ratio(total(c, "US", num, a, b), total(c, "US", "OUT_TECH", a, b))
                             for a, b in weeks], marker="o", label=f"framing share, {name}")
    bottom.set_ylabel("% of outage headlines")
    bottom.legend()
    plt.xticks(rotation=60)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "bulk-news-wave.png"), dpi=150)
    print("\nchart written: bulk-news-wave.png")


if __name__ == "__main__":
    sys.exit(main())
