#!/usr/bin/env python3
"""Fetch archived 123kerala.com pages+images from the Wayback Machine.

Resumable: files already on disk are skipped, so re-running picks up where it
stopped. Uses the `id_` replay modifier to get the original bytes rather than
Wayback's rewritten/toolbar-injected version.
"""
import collections
import json
import os
import sys
import time
import urllib.request
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CDX = os.path.join(ROOT, "cdx", "123kerala-cdx.json")
OUT = os.path.join(ROOT, "sources", "from-wayback")
LOG = os.path.join(ROOT, "tools", "crawl.log")

# snapshot nearest this date wins -- matches the Nov 2010 desktop save
TARGET = 20101113
UA = "Mozilla/5.0 (personal site archival research)"

# Wayback refuses connections outright (not 429) when pushed. 4s held for 700+
# requests, so start there and adapt: ease down while things are clean, back
# off hard on a refusal. Over ~6k requests the pacing matters more than at 900.
DELAY_MIN, DELAY_MAX, DELAY_START = 3.0, 30.0, 4.0

SCOPES = {
    "core": lambda p: not p.startswith("/chithram/"),
    "chithram": lambda p: p.startswith("/chithram/"),
    "all": lambda p: True,
}


def is_throttle(exc):
    """True only for signals that actually mean 'slow down'.

    Wayback throttles by refusing the connection (Errno 61), not with 429s.
    A 404 means the file was never preserved, and a DNS failure (Errno 8)
    means *our* network blipped -- neither says anything about our rate, and
    treating them as throttling ratchets the delay up for no reason.
    """
    s = str(exc)
    return ("Errno 61" in s or "Connection refused" in s
            or "HTTP Error 429" in s or "HTTP Error 503" in s)


def is_junk(p):
    """Malformed URLs the crawler archived from typos in the original markup
    (unescaped quotes, absolute URLs pasted into a relative href), plus the
    modern host's boilerplate. None of it is site content."""
    return ("%22" in p or "http:" in p or "https:" in p
            or p.startswith("/.well-known/") or "site=" in p)


def load_index(scope="core"):
    in_scope = SCOPES[scope]
    rows = json.load(open(CDX))[1:]
    pages, images = collections.defaultdict(list), collections.defaultdict(list)
    for ts, orig, _sc, mt, _dg in rows:
        p = (urlparse(orig).path or "/").lower()
        if not in_scope(p) or is_junk(p):
            continue
        if mt == "text/html":
            pages[p].append(ts)
        elif mt.startswith("image"):
            images[p].append(ts)
    return pages, images


def local_path(p):
    """Map a site path to a file on disk, preserving directory structure.

    Paths with no file extension (/classified, /chithram) were served as
    directory indexes, and the site also has /classified/... beneath them --
    so they must become <path>/index.html or the file collides with the
    directory it needs to contain.
    """
    rel = p.lstrip("/")
    if rel == "" or rel.endswith("/"):
        rel += "index.html"
    elif "." not in os.path.basename(rel):
        rel = os.path.join(rel, "index.html")
    return os.path.join(OUT, rel)


def fetch(url, tries=5):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            return urllib.request.urlopen(req, timeout=90).read()
        except Exception as exc:
            if "HTTP Error 404" in str(exc) or attempt == tries - 1:
                raise
            # A dropped network (laptop asleep, wifi gone) can outlast a short
            # retry window, so wait it out rather than burning every attempt.
            offline = "Errno 8" in str(exc) or "Errno 51" in str(exc)
            time.sleep((60 if offline else 15) * (attempt + 1))
    return None


def main():
    scope = sys.argv[1] if len(sys.argv) > 1 else "core"
    if scope not in SCOPES:
        sys.exit(f"usage: crawl.py [{'|'.join(SCOPES)}]")
    pages, images = load_index(scope)
    targets = [(p, ts, "html") for p, ts in pages.items()]
    targets += [(p, ts, "img") for p, ts in images.items()]
    targets.sort()

    done = skipped = failed = 0
    delay = DELAY_START
    streak = 0
    started = time.time()
    log = open(LOG, "a", buffering=1)
    log.write(f"\n=== crawl started {time.strftime('%Y-%m-%d %H:%M:%S')} "
              f"scope={scope} ({len(targets)} targets) ===\n")

    for i, (path, snaps, kind) in enumerate(targets, 1):
        dest = local_path(path)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            skipped += 1
            continue
        try:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
        except OSError as exc:
            # a file already occupies a directory slot -- log and move on
            # rather than letting one bad path abort the whole run
            failed += 1
            log.write(f"SKIP {path}  {exc}\n")
            continue
        best = min(snaps, key=lambda t: abs(int(t[:8]) - TARGET))
        url = f"http://web.archive.org/web/{best}id_/http://www.123kerala.com{path}"
        try:
            data = fetch(url)
            with open(dest, "wb") as fh:
                fh.write(data)
            done += 1
            streak += 1
            log.write(f"OK   {best[:8]} {len(data):>8}b {path}\n")
            # Recover multiplicatively, mirroring the backoff. Decaying by a
            # fixed 0.25s meant a single spurious backoff to 30s could never
            # unwind inside one run.
            if streak >= 25 and delay > DELAY_MIN:
                delay = max(DELAY_MIN, delay * 0.7)
                streak = 0
                log.write(f"     ...clean streak, delay now {delay:.1f}s\n")
        except Exception as exc:
            failed += 1
            streak = 0
            if is_throttle(exc):
                delay = min(DELAY_MAX, delay * 1.5)
                log.write(f"     ...throttled, delay now {delay:.1f}s\n")
            log.write(f"FAIL {path}  {exc}\n")
        if i % 50 == 0:
            rate = done / max(time.time() - started, 1) * 3600
            left = (len(targets) - i) / max(rate, 1)
            log.write(f"--- progress {i}/{len(targets)}  ok={done} skip={skipped} "
                      f"fail={failed}  delay={delay:.1f}s  eta={left:.1f}h\n")
        time.sleep(delay)

    log.write(f"=== finished: fetched={done} skipped={skipped} failed={failed} ===\n")
    print(f"fetched={done} skipped={skipped} failed={failed}")


if __name__ == "__main__":
    main()
