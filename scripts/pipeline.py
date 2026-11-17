#!/usr/bin/env python3
"""Model v1: the frozen rules that turn the log into a dated posterior series.

    python3 scripts/pipeline.py            # writes output/series-v1.csv and
                                           #        output/events-v1.csv

Standard library only. Deterministic: no clock, no randomness. The rules are
described in model/MODEL-v1.md and the numbers live in model/model_v1.json.
Until model/model_v1.sha256 exists this is a draft and may change. The commit
that adds that file is the freeze: from then on this file and that JSON may
not change, and no row of log/log.csv may predate it. A change to the rules
after the freeze is a new version (pipeline_v2.py, model_v2.json) with a
changelog, and the whole log is rerun through it.
"""
import csv
import hashlib
import json
import math
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(ROOT, "model", "model_v1.json")
LOG_PATH = os.path.join(ROOT, "log", "log.csv")
HEADER = ["row_id", "logged_at", "phase", "kind", "event_id", "known_at",
          "occurred_at", "org", "class", "tier", "counted", "value",
          "supersedes", "source", "source_status", "note"]
OBSERVERS = ["calm", "middle", "suspicious"]


def ts(text):
    return datetime.strptime(text, "%Y-%m-%dT%H:%MZ").replace(
        tzinfo=timezone.utc)


def days(later, earlier):
    return (later - earlier).total_seconds() / 86400.0


def fmt(x):
    return format(x, ".6g")


def poisson(n, mean):
    if mean <= 0:
        return 1.0 if n == 0 else 0.0
    return math.exp(-mean + n * math.log(mean) - math.lgamma(n + 1))


def poisson_tail(n, mean):
    """P(N >= n)."""
    return max(0.0, 1.0 - sum(poisson(k, mean) for k in range(n)))


def load_model():
    with open(MODEL_PATH, "rb") as fh:
        raw = fh.read()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def rate_grid(model):
    rp = model["rate_prior"]
    lo, hi, n = math.log(rp["grid_low"]), math.log(rp["grid_high"]), \
        rp["grid_points"]
    mu, sd = math.log(rp["median_per_week"]), rp["sigma_log"]
    lams = [math.exp(lo + (hi - lo) * i / (n - 1)) for i in range(n)]
    w = [math.exp(-0.5 * ((math.log(x) - mu) / sd) ** 2) for x in lams]
    total = sum(w)
    return lams, [x / total for x in w]


class State:
    def __init__(self):
        self.events = {}        # event_id -> dict
        self.evidence = {}      # row_id -> (event_id, kind, org)
        self.row_event = {}     # row_id of an event row -> event_id
        self.instruments = {}   # org -> z
        self.void = set()       # row_ids voided by a correction

    def apply(self, row, model):
        kind, rid = row["kind"], int(row["row_id"])
        if kind == "event":
            self.events[row["event_id"]] = {
                "occurred": ts(row["occurred_at"]), "org": row["org"],
                "class": row["class"], "tier": row["tier"],
                "counted": row["counted"] == "yes",
                "existence": row["value"], "void": False}
            self.row_event[rid] = row["event_id"]
        elif kind == "existence":
            self.events[row["event_id"]]["existence"] = row["value"]
        elif kind == "instrument":
            self.instruments[row["org"]] = float(row["value"])
        elif kind == "correction":
            target = int(row["supersedes"])
            for part in row["value"].split(";"):
                field, _, val = part.partition("=")
                if field == "void":
                    self.void.add(target)
                    if target in self.row_event:
                        self.events[self.row_event[target]]["void"] = True
                elif target in self.row_event:
                    ev = self.events[self.row_event[target]]
                    if field == "occurred_at":
                        ev["occurred"] = ts(val)
                    elif field == "counted":
                        ev["counted"] = val == "yes"
                    elif field in ("class", "tier", "org"):
                        ev[field] = val
                    else:
                        raise ValueError(f"row {rid}: bad field {field}")
                else:
                    raise ValueError(f"row {rid}: only void applies here")
        elif kind in model["kinds"]:
            self.evidence[rid] = (row["event_id"], kind, row["org"])
        elif kind not in model["no_effect_kinds"]:
            raise ValueError(f"row {rid}: unknown kind {kind}")


def event_likelihoods(state, model, as_of):
    """For each counted, live event: likelihood of everything logged about it
    under 'attack, account honestly premature' and 'attack, account stays
    wrong', each relative to 'benign' = 1."""
    kinds, ladder = model["kinds"], model["ladder"]
    med = model["survival_median_days"]
    out = {}
    for eid, ev in state.events.items():
        if ev["void"] or not ev["counted"] or ev["occurred"] > as_of:
            continue
        present = {}
        for rid, (e, kind, org) in state.evidence.items():
            if e == eid and rid not in state.void:
                present[(kind, org)] = rid
        rung = max((ladder.index(k) for k, _ in present if k in ladder),
                   default=-1)
        lp = lw = 1.0
        if rung >= 0:
            lp, lw = kinds[ladder[rung]]
        for (kind, _org) in present:
            if kind not in ladder:
                lp *= kinds[kind][0]
                lw *= kinds[kind][1]
        resolved = any(k in model["resolving_kinds"] for k, _ in present)
        quiet = max(0.0, days(as_of, ev["occurred"]))
        if not resolved:
            lp *= 0.5 ** (quiet / med["premature"])
            lw *= 0.5 ** (quiet / med["wrong"])
        cls = model["classes"][ev["class"]]
        w = cls["stays_wrong"]
        lam = w * lw + (1 - w) * lp
        out[eid] = {"lik": lam, "share_wrong": w * lw / lam,
                    "rung": ladder[rung] if rung >= 0 else "none",
                    "quiet_days": quiet, "base": cls["attack_prior"],
                    "real": model["existence"][ev["existence"]]}
    return out


def snapshot(state, model, grid, as_of):
    lams, prior = grid
    lik = event_likelihoods(state, model, as_of)
    mu = model["campaign_extra_rate_per_week"]
    window = model["attention_window_days"]
    primer = state.events.get(model["primer_event"])
    n = 0
    exposure = 0.0
    if primer and not primer["void"] and primer["occurred"] <= as_of:
        exposure = min(window, max(0.0, days(as_of, primer["occurred"])))
        for eid in lik:
            gap = days(state.events[eid]["occurred"], primer["occurred"])
            if 0 < gap <= window:
                n += 1
    weeks = exposure / 7.0
    inst = 1.0
    delta, cap = model["instrument"]["delta"], model["instrument"]["cap"]
    for z in state.instruments.values():
        inst *= min(cap, max(1 / cap, math.exp(delta * z - delta * delta / 2)))
    res = {"n_events": len(lik), "post_primer": n, "exposure_days": exposure,
           "quiet_visible": sum(
               model["tiers_quiet_week_visibility"][state.events[e]["tier"]]
               for e in lik),
           "count_ordinary": sum(p * poisson_tail(n, x * weeks)
                                 for x, p in zip(lams, prior)),
           "obs": {}, "events": {}}
    for name in OBSERVERS:
        ob = model["observers"][name]
        c = ob["campaign_prior"]
        pri = {e: min(model["attack_prior_cap"],
                      v["base"] * ob["attack_prior_mult"])
               for e, v in lik.items()}
        f0 = {e: pri[e] * v["lik"] + 1 - pri[e] for e, v in lik.items()}
        prod0 = math.prod(f0.values())
        num = den = 0.0
        w1 = []
        for x, p in zip(lams, prior):
            a = mu / (x + mu)
            l1 = poisson(n, (x + mu) * weeks) * math.prod(
                a * v["lik"] + (1 - a) * f0[e] for e, v in lik.items())
            l0 = poisson(n, x * weeks) * prod0
            num += p * l1
            den += p * l0
            w1.append(p * l1)
        bf = inst * num / den
        ph1 = c * bf / (c * bf + 1 - c)
        tot1 = sum(w1)
        w1 = [x / tot1 for x in w1]
        p0 = {e: pri[e] * v["lik"] / f0[e] for e, v in lik.items()}
        p1 = {e: 0.0 for e in lik}
        any1 = 0.0
        for x, wj in zip(lams, w1):
            a = mu / (x + mu)
            none = 1.0
            for e, v in lik.items():
                pe = (a * v["lik"] + (1 - a) * pri[e] * v["lik"]) / \
                     (a * v["lik"] + (1 - a) * f0[e])
                p1[e] += wj * pe
                none *= 1 - v["real"] * pe
            any1 += wj * (1 - none)
        any0 = 1 - math.prod(1 - lik[e]["real"] * p0[e] for e in lik)
        res["obs"][name] = {"bf": bf, "campaign": ph1,
                            "any_attack": (1 - ph1) * any0 + ph1 * any1,
                            "any_attack_no_campaign": any0}
        for e in lik:
            res["events"].setdefault(e, {})[name] = {
                "attack": (1 - ph1) * p0[e] + ph1 * p1[e], "attack_h0": p0[e]}
    res["lik"] = lik
    return res


def run(log_path=LOG_PATH, out_dir=None):
    model, digest = load_model()
    grid = rate_grid(model)
    with open(log_path, newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != HEADER:
            raise ValueError("log header does not match the frozen schema")
        rows = list(reader)
    state = State()
    series = [["row_id", "as_of", "kind", "event_id", "events_counted",
               "post_primer_count", "exposure_days", "quiet_week_visible",
               "p_count_ordinary"] +
              [f"{k}_{o}" for o in OBSERVERS
               for k in ("bf_campaign", "p_campaign", "p_any_attack")]]
    last = None
    for row in rows:
        state.apply(row, model)
        as_of = ts(row["known_at"])
        last = snapshot(state, model, grid, as_of)
        series.append(
            [row["row_id"], row["known_at"], row["kind"], row["event_id"],
             str(last["n_events"]), str(last["post_primer"]),
             fmt(last["exposure_days"]), fmt(last["quiet_visible"]),
             fmt(last["count_ordinary"])] +
            [fmt(last["obs"][o][k]) for o in OBSERVERS
             for k in ("bf", "campaign", "any_attack")])
    events = [["event_id", "org", "class", "tier", "p_real", "account_rung",
               "quiet_days", "share_stays_wrong_given_attack"] +
              [f"p_attack_{o}" for o in OBSERVERS] +
              ["p_attack_middle_no_campaign", "p_premature_middle",
               "p_stays_wrong_middle"]]
    if last:
        for e, v in last["lik"].items():
            ev = state.events[e]
            mid = last["events"][e]["middle"]["attack"]
            events.append(
                [e, ev["org"], ev["class"], ev["tier"], fmt(v["real"]),
                 v["rung"], fmt(v["quiet_days"]), fmt(v["share_wrong"])] +
                [fmt(last["events"][e][o]["attack"]) for o in OBSERVERS] +
                [fmt(last["events"][e]["middle"]["attack_h0"]),
                 fmt(mid * (1 - v["share_wrong"])),
                 fmt(mid * v["share_wrong"])])
    out_dir = out_dir or os.path.join(ROOT, "output")
    os.makedirs(out_dir, exist_ok=True)
    for name, table in (("series-v1.csv", series), ("events-v1.csv", events)):
        with open(os.path.join(out_dir, name), "w", newline="") as fh:
            fh.write(f"# model v{model['version']} sha256 {digest}\n")
            csv.writer(fh, lineterminator="\n").writerows(table)
    return model, digest, rows, last


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else None
    model, digest, rows, last = run(out_dir=out)
    print(f"model v{model['version']} sha256 {digest}")
    print(f"rows in log: {len(rows)}")
    if last:
        print(f"as of {rows[-1]['known_at']}: {last['n_events']} counted "
              f"events, {last['post_primer']} after the primer in "
              f"{last['exposure_days']:.2f} days")
        print(f"  would have been national news in a quiet week: "
              f"{last['quiet_visible']:.2f} of {last['n_events']}")
        print(f"  P(a primed window this long shows at least this many, "
              f"nothing unusual): {last['count_ordinary']:.3f}")
        for o in OBSERVERS:
            r = last["obs"][o]
            print(f"  {o:<10} Bayes factor for a campaign {r['bf']:.3g}; "
                  f"P(campaign) {r['campaign']:.3g}; "
                  f"P(at least one attack) {r['any_attack']:.3g}")
