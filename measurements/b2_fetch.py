"""Throttled, logged, cached requests to GDELT's DOC 2.0 API (PROTOCOL-2.md).

Every attempt is appended to measurements/b2_requests.csv (URL, UTC time,
HTTP status, SHA-256 of the response body, a label). Each successful body is
kept gzipped in measurements/b2_raw/, named by the SHA-1 of its URL.
One request at a time, at least 6 seconds apart; on a refusal, wait 60
seconds and try once more.
"""
import csv, gzip, hashlib, os, time, urllib.parse, urllib.request, urllib.error
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "b2_raw")
LOG = os.path.join(HERE, "b2_requests.csv")
STAMP = os.path.join(RAW, ".last_request")
ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc"
GAP = 6.5


def url_for(params):
    return ENDPOINT + "?" + urllib.parse.urlencode(params)


def _log(url, status, body, label):
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["time_utc", "label", "http_status", "sha256", "bytes", "url"])
        w.writerow([datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), label,
                    status, hashlib.sha256(body).hexdigest() if body else "", len(body), url])


def _wait():
    try:
        last = os.path.getmtime(STAMP)
    except OSError:
        last = 0
    d = GAP - (time.time() - last)
    if d > 0:
        time.sleep(d)


def _once(url):
    _wait()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "outage-count-script/1.0"})
        with urllib.request.urlopen(req, timeout=90) as r:
            status, body = r.status, r.read()
    except urllib.error.HTTPError as e:
        status, body = e.code, e.read()
    except Exception as e:  # reset, timeout
        status, body = 0, repr(e).encode()
    open(STAMP, "w").close()
    return status, body


def refused(status, body):
    return status != 200 or body.lstrip().startswith(b"Please limit")


def fetch(params, label="", use_cache=True):
    """Return (ok, text). ok is False when both attempts were refused."""
    os.makedirs(RAW, exist_ok=True)
    url = url_for(params)
    path = os.path.join(RAW, hashlib.sha1(url.encode()).hexdigest() + ".gz")
    if use_cache and os.path.exists(path):
        return True, gzip.open(path, "rt", encoding="utf-8", errors="replace").read()
    for attempt in (1, 2):
        status, body = _once(url)
        _log(url, status, body, label)
        if not refused(status, body):
            with gzip.GzipFile(path, "wb", mtime=0) as g:
                g.write(body)
            return True, body.decode("utf-8", "replace")
        if attempt == 1:
            time.sleep(60)
    return False, body.decode("utf-8", "replace")
