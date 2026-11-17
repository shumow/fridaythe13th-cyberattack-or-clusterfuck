#!/usr/bin/env python3
"""Validator: checks the repo against its own rules.

    python3 scripts/validate.py

The repo is the source of truth. This script checks that
  1. the log is well formed and every row is sourced;
  2. the frozen model file still has the hash recorded at the freeze;
  3. git history shows the rules were committed before any row, that the
     rules have not changed since, and that the log has only ever grown;
  4. rerunning the pipeline reproduces the committed output byte for byte.
Exit code 0 means every check passed. Needs enough git history to reach the
freeze commit: after a shallow clone, run `git fetch --unshallow` first.
"""
import csv
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import pipeline  # noqa: E402

LOG = "log/log.csv"
FROZEN = ["model/model_v1.json", "model/MODEL-v1.md", "scripts/pipeline.py"]
# The freeze is the commit that adds this file. Before it exists the model is
# a draft and may change; after it, the three files above may not.
FREEZE_MARK = "model/model_v1.sha256"
STATUSES = {"opened", "browser", "relay", "excerpt", "memory", "none"}
PHASES = {"retrospective", "prospective"}
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(("PASS  " if ok else "FAIL  ") + name + (f": {detail}" if detail
                                                    else ""))


def git(*args):
    return subprocess.run(["git", "-C", ROOT] + list(args), check=True,
                          capture_output=True, text=True).stdout


def ts(text):
    return datetime.strptime(text, "%Y-%m-%dT%H:%MZ").replace(
        tzinfo=timezone.utc)


def check_log(model):
    if not os.path.exists(os.path.join(ROOT, LOG)):
        print("DRAFT no log yet: " + LOG)
        return None
    with open(os.path.join(ROOT, LOG), newline="") as fh:
        reader = csv.DictReader(fh)
        header_ok = reader.fieldnames == pipeline.HEADER
        rows = list(reader)
    check("log header matches the frozen schema", header_ok)
    problems = []
    events, seen, prev = set(), set(), None
    allowed = set(model["kinds"]) | set(model["no_effect_kinds"]) | {
        "event", "existence", "instrument", "correction"}
    for i, r in enumerate(rows, start=1):
        rid = r["row_id"]
        if rid != str(i):
            problems.append(f"row {rid}: ids must run 1, 2, 3 ...")
        if r["phase"] not in PHASES:
            problems.append(f"row {rid}: phase")
        if r["kind"] not in allowed:
            problems.append(f"row {rid}: kind {r['kind']}")
        try:
            known, logged = ts(r["known_at"]), ts(r["logged_at"])
            if prev and known < prev:
                problems.append(f"row {rid}: known_at goes backwards")
            if known > logged:
                problems.append(f"row {rid}: known before it was logged")
            if r["phase"] == "prospective" and known != logged:
                problems.append(f"row {rid}: prospective rows are known "
                                "when they are logged")
            prev = known
            if r["occurred_at"]:
                ts(r["occurred_at"])
        except ValueError:
            problems.append(f"row {rid}: timestamp format")
        if r["source_status"] not in STATUSES:
            problems.append(f"row {rid}: source_status")
        if r["kind"] != "checkpoint" and (
                not r["source"] or r["source_status"] == "none"):
            problems.append(f"row {rid}: no source")
        if r["kind"] == "event":
            if r["class"] not in model["classes"] or r["tier"] not in \
                    model["tiers_quiet_week_visibility"] or r["counted"] \
                    not in ("yes", "no") or r["value"] not in \
                    model["existence"] or not r["occurred_at"]:
                problems.append(f"row {rid}: event fields")
            if r["event_id"] in events:
                problems.append(f"row {rid}: duplicate event")
            events.add(r["event_id"])
        elif r["kind"] == "existence":
            if r["value"] not in model["existence"]:
                problems.append(f"row {rid}: existence value")
        elif r["kind"] == "instrument":
            try:
                float(r["value"])
            except ValueError:
                problems.append(f"row {rid}: instrument value")
        elif r["kind"] == "correction":
            if r["supersedes"] not in seen:
                problems.append(f"row {rid}: supersedes an unknown row")
        if r["kind"] in model["kinds"] or r["kind"] == "existence":
            if r["event_id"] not in events:
                problems.append(f"row {rid}: unknown event {r['event_id']}")
        seen.add(rid)
    check("every row is well formed and sourced", not problems,
          "; ".join(problems[:6]))
    return rows


def check_hash():
    mark = os.path.join(ROOT, FREEZE_MARK)
    if not os.path.exists(mark):
        print("DRAFT the model is not frozen: no " + FREEZE_MARK)
        return False
    with open(os.path.join(ROOT, "model/model_v1.json"), "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    with open(mark) as fh:
        recorded = fh.read().split()[0]
    check("model file matches the hash recorded at the freeze",
          digest == recorded, digest[:16])
    return True


def check_history(rows):
    try:
        freeze = git("log", "--diff-filter=A", "--format=%H", "--",
                     FREEZE_MARK).split()
    except (subprocess.CalledProcessError, FileNotFoundError):
        check("git history available", False, "not a git checkout")
        return
    if not freeze:
        check("git history reaches the freeze commit", False,
              "freeze record not committed, or history too shallow")
        return
    freeze = freeze[-1]
    when = git("show", "-s", "--format=%cI", freeze).strip()
    check("freeze commit found", True, f"{freeze[:10]} at {when}")
    for path in FROZEN:
        later = git("log", "--format=%H", f"{freeze}..HEAD", "--",
                    path).split()
        same = subprocess.run(["git", "-C", ROOT, "diff", "--quiet", freeze,
                               "--", path]).returncode == 0
        check(f"unchanged since the freeze: {path}", not later and same,
              f"{len(later)} later commit(s) touch it")
    if rows is None:
        return
    commits = git("log", "--reverse", "--format=%H", "--", LOG).split()
    grown, first_data, prev = True, None, None
    for c in commits:
        text = git("show", f"{c}:{LOG}")
        if prev is not None and not text.startswith(prev):
            grown = False
        if first_data is None and len(text.strip().splitlines()) > 1:
            first_data = c
        prev = text
    with open(os.path.join(ROOT, LOG), newline="") as fh:
        working = fh.read()
    if prev is not None and not working.startswith(prev):
        grown = False
    check("the log has only ever grown", grown,
          f"{len(commits)} commit(s) touch it")
    if first_data:
        after = first_data != freeze and subprocess.run(
            ["git", "-C", ROOT, "merge-base", "--is-ancestor", freeze,
             first_data]).returncode == 0
        check("the rules were committed before the first row", after,
              f"first row in {first_data[:10]}")
    else:
        check("the rules were committed before the first row", True,
              "no rows committed yet")


def check_reproduces():
    names = ["series-v1.csv", "events-v1.csv"]
    with tempfile.TemporaryDirectory() as tmp:
        pipeline.run(out_dir=tmp)
        same = True
        for name in names:
            committed = os.path.join(ROOT, "output", name)
            if not os.path.exists(committed):
                same = False
                continue
            with open(committed, "rb") as a, open(os.path.join(tmp, name),
                                                  "rb") as b:
                same = same and a.read() == b.read()
    check("rerunning the pipeline reproduces the committed output", same)


if __name__ == "__main__":
    with open(os.path.join(ROOT, "model/model_v1.json")) as fh:
        model = json.load(fh)
    rows = check_log(model)
    frozen = check_hash()
    if frozen:
        check_history(rows)
    if rows is not None:
        check_reproduces()
    if not frozen:
        print("DRAFT state: freeze and history checks skipped")
    print(f"{sum(results)} of {len(results)} checks passed")
    sys.exit(0 if all(results) else 1)
