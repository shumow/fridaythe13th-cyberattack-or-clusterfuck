#!/usr/bin/env python3
"""Requests for PROTOCOL-3.md, part N1: the coverage series. Standard library only.

    python3 measurements/nw_fetch.py            # the five series requests
    python3 measurements/nw_fetch.py --show     # print the URLs, send nothing
    python3 measurements/nw_fetch.py --backoff 30,60   # waits after each refusal
    python3 measurements/nw_fetch.py --overnight       # keep asking, slowly
    python3 measurements/nw_fetch.py --overnight 8 --every 20

Query strings come from nw_queries.json. Requests go through b2_fetch.py's
throttle, retry and cache, with their own log (nw_requests.csv) and their own
folder of raw answers (nw_raw/). Answered bodies are parsed into
nw_series.csv: one row per query per UTC day.

The first request is the gate. If every attempt at it is refused the script
stops and sends nothing else. PROTOCOL-3.md allows one retry after 60 seconds,
which is the default; --backoff and --overnight are departures from it and
must be recorded in HANDOFF.md when used.

--overnight [HOURS] sends one request, and if it is refused sleeps --every
MINUTES (default 15) and sends it again, for up to HOURS (default 10). It
moves to the next query as soon as one is answered, so the most it can send
is one request per interval. Answered bodies are cached in nw_raw/, so a run
that is stopped or gives up loses nothing: run it again and it resumes. A query the archive rejects as malformed is shortened by
dropping the last term of its last group, as the protocol says, and each
rejected form is printed and logged.
"""
import csv
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timedelta

import b2_fetch as f

HERE = os.path.dirname(os.path.abspath(__file__))
f.RAW = os.path.join(HERE, "nw_raw")
f.LOG = os.path.join(HERE, "nw_requests.csv")
f.STAMP = os.path.join(f.RAW, ".last_request")
SERIES = os.path.join(HERE, "nw_series.csv")
ACCEPTED = os.path.join(HERE, "nw_accepted.json")

with open(os.path.join(HERE, "nw_queries.json")) as fh:
    Q = json.load(fh)


def build(groups):
    """Query text for a list of term lists. One term needs no brackets."""
    parts = []
    for terms in groups:
        parts.append(terms[0] if len(terms) == 1 else "(" + " OR ".join(terms) + ")")
    return " ".join(parts) + Q["suffix"]


def params(query):
    s = Q["series"]
    return {"query": query, "mode": s["mode"], "format": s["format"],
            "startdatetime": s["startdatetime"], "enddatetime": s["enddatetime"]}


def is_json(text):
    return text.lstrip()[:1] in ("{", "[")


def malformed(text):
    """The archive answers a bad query with a sentence about the query."""
    t = text.lower()
    return not is_json(text) and any(w in t for w in (
        "query", "phrase", "keyword", "parenthes", "too short", "too long"))


def parse(text):
    """[(yyyy-mm-dd, matching articles, all articles)] from a TimelineVolRaw answer."""
    out = []
    for series in json.loads(text).get("timeline", []):
        for p in series.get("data", []):
            d = p["date"]
            out.append((f"{d[0:4]}-{d[4:6]}-{d[6:8]}", int(p["value"]), int(p["norm"])))
    return out


def arg(flag, default):
    """The number after a flag, or default if the flag has no number."""
    i = sys.argv.index(flag)
    try:
        return float(sys.argv[i + 1])
    except (IndexError, ValueError):
        return default


def fetch(p, label, deadline, every):
    """f.fetch, or with a deadline: keep asking every `every` seconds until then."""
    while True:
        ok, text = f.fetch(p, label=label)
        if ok or deadline is None:
            return ok, text
        nxt = time.time() + every
        if nxt > deadline:
            f.say(f"{label}: still refused and out of time. Giving up.")
            return ok, text
        f.say(f"{label}: refused. Sleeping {every / 60:g} min; next try at "
              f"{datetime.fromtimestamp(nxt):%H:%M}, giving up at "
              f"{datetime.fromtimestamp(deadline):%H:%M}. Ctrl-C is safe.")
        time.sleep(every)


def main():
    show = "--show" in sys.argv
    deadline, every = None, 15 * 60
    if "--overnight" in sys.argv:
        hours = arg("--overnight", 10)
        if "--every" in sys.argv:
            every = arg("--every", 15) * 60
        deadline = time.time() + hours * 3600
        f.BACKOFF = ()  # one request per interval, no quick retry
        print(f"overnight: one request every {every / 60:g} min while refused, "
              f"until {datetime.now() + timedelta(hours=hours):%a %H:%M} "
              f"(at most {int(hours * 3600 // every) + 5} requests)", flush=True)
    if "--backoff" in sys.argv:
        f.BACKOFF = tuple(float(x) for x in
                          sys.argv[sys.argv.index("--backoff") + 1].split(","))
        print(f"backoff after a refusal: {f.BACKOFF} seconds "
              f"(protocol: (60,))")
    rows, accepted = [], {}
    for i, q in enumerate(Q["queries"]):
        groups = [list(Q["groups"][g]) for g in q["groups"]]
        while True:
            query = build(groups)
            if show:
                print(q["name"], len(query), f.url_for(params(query)), sep="\t")
                break
            ok, text = fetch(params(query), "n1-" + q["name"], deadline, every)
            if not ok:
                print(f"{q['name']}: refused"
                      + (f" {len(f.BACKOFF) + 1} times" if deadline is None
                         else " until the deadline")
                      + ". Stopping; see nw_requests.csv.")
                if i == 0:
                    print("The gate did not pass. Nothing else was sent.")
                return 1
            if malformed(text):
                print(f"{q['name']}: rejected as malformed: {text.strip()[:80]!r}")
                print(f"  form sent: {query}")
                # A cached rejection must not be mistaken for an answer later.
                os.remove(os.path.join(f.RAW, hashlib.sha1(
                    f.url_for(params(query)).encode()).hexdigest() + ".gz"))
                if len(groups[-1]) <= 1:
                    print(f"{q['name']}: nothing left to drop. Stopping.")
                    return 1
                groups[-1].pop()
                continue
            if not is_json(text):
                print(f"{q['name']}: an answer that is neither data nor a "
                      f"complaint about the query: {text.strip()[:120]!r}. Stopping.")
                return 1
            got = parse(text)
            accepted[q["name"]] = query
            rows += [(q["name"], d, v, n) for d, v, n in got]
            print(f"{q['name']}: {len(got)} days, {sum(v for _, v, _ in got)} articles",
                  flush=True)
            break
    if show:
        return 0
    with open(SERIES, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["query", "day_utc", "articles", "norm"])
        w.writerows(rows)
    with open(ACCEPTED, "w") as fh:
        json.dump(accepted, fh, indent=2)
        fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
