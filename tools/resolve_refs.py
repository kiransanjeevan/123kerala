#!/usr/bin/env python3
"""Try to repair broken references in the restored site.

Most of the 1,891 dead references were broken on the original site, but a
chunk of them are near-misses: a typo'd separator, a stale path prefix, a
case difference that an old case-insensitive server forgave. This walks the
missing set and tries a ladder of candidate rewrites against the files we
actually hold, reporting which strategy resolved each one.

Read-only by default; --apply rewrites the HTML.
"""
import os
import re
import sys
import collections
from urllib.parse import urljoin, unquote

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")


def build_index():
    """by_path: lowercase relpath -> real relpath.  by_name: lowercase
    basename -> [real relpaths].  by_tail: last two segments -> [relpaths]."""
    by_path, by_name, by_tail = {}, collections.defaultdict(list), collections.defaultdict(list)
    for dp, dn, fn in os.walk(ROOT):
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, "/")
            by_path[rel.lower()] = rel
            by_name[f.lower()].append(rel)
            segs = rel.split("/")
            if len(segs) >= 2:
                by_tail["/".join(segs[-2:]).lower()].append(rel)
    return by_path, by_name, by_tail


def collect_missing():
    """-> {target: [(page, raw_ref), ...]} for every unresolvable reference."""
    missing = collections.defaultdict(list)
    for dp, dn, fn in os.walk(ROOT):
        for f in fn:
            if not f.lower().endswith((".html", ".htm")):
                continue
            page = os.path.join(dp, f)
            rel = "/" + os.path.relpath(page, ROOT).replace(os.sep, "/")
            d = open(page, "rb").read().decode("latin-1", "ignore")
            for u in re.findall(r'(?:src|background|href)="([^"]+)"', d, re.I):
                if u.lower().startswith(("http", "mailto:", "javascript:", "#", "//")):
                    continue
                if "' +" in u or "%22" in u:
                    continue
                tgt = urljoin(rel, unquote(u.split("#")[0].split("?")[0]))
                if not tgt or tgt.endswith("/"):
                    tgt += "index.html"
                if not os.path.exists(os.path.join(ROOT, tgt.lstrip("/"))):
                    missing[tgt].append((rel, u))
    return missing


def candidates(tgt):
    """Yield (strategy, candidate-relpath) guesses for a dead target."""
    p = tgt.lstrip("/")
    yield "case", p                                    # case-insensitive server
    yield "slashes", re.sub(r"/{2,}", "/", p)          # doubled separators

    # ..foo  ->  ../foo   (a missing slash in the original markup)
    if ".." in p:
        yield "dotdot", re.sub(r"\.\.(?=[A-Za-z])", "../", p)

    # stale deploy prefix from when the site lived in a subdirectory
    for pre in ("123kerala/", "new/"):
        if p.startswith(pre):
            yield "prefix", p[len(pre):]

    # extension variants
    if p.endswith(".htm"):
        yield "ext", p + "l"
    if p.endswith(".html"):
        yield "ext", p[:-1]
    if p.endswith(".jpeg"):
        yield "ext", p[:-4] + "jpg"
    if p.endswith(".jpg"):
        yield "ext", p[:-3] + "jpeg"

    # a root-level path that really lives under /chithram/
    if not p.startswith("chithram/"):
        yield "chithram", "chithram/" + p


GENERIC = {"index", "home", "main", "default", "thumb", "thumbs", "next",
           "prev", "previous", "back", "top", "bottom", "banner", "logo",
           "spacer", "title", "header", "footer", "bg", "button"}


def distinctive(fname):
    """Is this filename specific enough to identify content by name alone?

    Gallery files are numbered per-folder -- /abhirami/11.jpg and
    /illeana/11.jpg are different photographs of different people. Matching
    those by basename silently swaps content, which is worse than leaving
    the reference broken, so only names that carry real meaning qualify.
    """
    stem = os.path.splitext(fname)[0].lower()
    stem = re.sub(r"[_-]?\d+s?$", "", stem)      # trailing index/thumb suffix
    return len(re.findall(r"[a-z]", stem)) >= 4 and stem not in GENERIC


def edit_distance(a, b, cap=2):
    """Levenshtein, short-circuited once it exceeds `cap`."""
    if abs(len(a) - len(b)) > cap:
        return cap + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        if min(cur) > cap:
            return cap + 1
        prev = cur
    return prev[-1]


def fuzzy_dir(tgt, by_path, dirs):
    """Repair a misspelled *directory* against the ones that exist.

    The site has /chithram/meer/ (meant meera) and /chithram/prithvirqj/
    (q for a -- adjacent keys). The filename is fine; the folder is typo'd,
    so filename matching never sees these. Require a close spelling match
    AND that the full path then resolves, which makes a wrong guess
    self-rejecting.
    """
    segs = tgt.lstrip("/").split("/")
    if len(segs) < 2:
        return None
    for i in range(len(segs) - 1):
        parent = "/".join(segs[:i])
        name = segs[i].lower()
        for sib in dirs:
            if os.path.dirname(sib) != parent:
                continue
            cand = os.path.basename(sib)
            # A similarity *ratio* is far too loose for names: amrita_arora
            # and amrita_rao score close on their shared prefix but are two
            # different actresses. Demand a near-identical spelling instead --
            # one slip of the finger, not a different word.
            if abs(len(cand) - len(name)) > 1 or edit_distance(name, cand.lower()) > 1:
                continue
            trial = "/".join(segs[:i] + [cand] + segs[i + 1:])
            hit = by_path.get(trial.lower())
            if hit:
                return hit
    return None


def sane_jump(tgt, cand):
    """Reject name matches that would land somewhere semantically wrong.

    Two real cases from this site: /missuniverse2002/india.jpg matching
    /miss2001/india.jpg (different pageant, different person), and a gallery
    photo matching a same-named file under /cgi-script/ (an ad banner, not
    content). Same filename is not the same picture.
    """
    if "cgi-script/" in cand.lower():
        return False
    yr = lambda s: set(re.findall(r"(?:19|20)\d{2}", s))
    a, b = yr(os.path.dirname(tgt)), yr(os.path.dirname(cand))
    return not (a and b and a != b)


def resolve(tgt, by_path, by_name, by_tail, dirs=()):
    for strat, cand in candidates(tgt):
        cand = os.path.normpath(cand).replace(os.sep, "/").lstrip("./")
        hit = by_path.get(cand.lower())
        if hit:
            return strat, hit

    # Last resort: match on the final two path segments, then on the bare
    # filename -- but only for names distinctive enough to mean one thing,
    # and only when exactly one file could be intended.
    segs = tgt.lstrip("/").split("/")
    if len(segs) >= 2:
        t = by_tail.get("/".join(segs[-2:]).lower(), [])
        if len(t) == 1:
            return "tail", t[0]
    # NOTE: fuzzy directory matching is deliberately NOT used. It looks
    # attractive -- /chithram/meer/ really is a typo for meera -- but the
    # site is full of real names one character apart: meera/meena,
    # divya/diya, bhumila/bhumika are different actresses with different
    # galleries. No edit-distance threshold separates "typo" from "someone
    # else", so a correction here silently swaps one person's photos for
    # another's. 22 recoverable references are not worth that. fuzzy_dir()
    # is kept below for reference but intentionally uncalled.
    if not distinctive(segs[-1]):
        return "unsafe", None
    n = [c for c in by_name.get(segs[-1].lower(), []) if sane_jump(tgt, c)]
    if len(n) == 1:
        return "basename", n[0]
    if len(n) > 1:
        return "ambiguous", None
    return None, None


def main():
    apply = "--apply" in sys.argv
    by_path, by_name, by_tail = build_index()
    dirs = set()
    for dp, dn, fn in os.walk(ROOT):
        for d in dn:
            dirs.add(os.path.relpath(os.path.join(dp, d), ROOT).replace(os.sep, "/"))
    missing = collect_missing()
    print(f"indexed {len(by_path)} files; {len(missing)} distinct dead references\n")

    resolved, ambiguous, unsafe, dead = {}, [], [], []
    by_strat = collections.Counter()
    for tgt in sorted(missing):
        strat, hit = resolve(tgt, by_path, by_name, by_tail, dirs)
        if strat == "ambiguous":
            ambiguous.append(tgt)
        elif strat == "unsafe":
            unsafe.append(tgt)
        elif hit:
            resolved[tgt] = (strat, hit)
            by_strat[strat] += 1
        else:
            dead.append(tgt)

    refs = lambda keys: sum(len(missing[k]) for k in keys)
    print(f"RESOLVED  {len(resolved):>5} targets  ({refs(resolved)} references)")
    for s, c in by_strat.most_common():
        print(f"    {s:<10} {c}")
    print(f"AMBIGUOUS {len(ambiguous):>5} targets  ({refs(ambiguous)} references)")
    print(f"UNSAFE    {len(unsafe):>5} targets  ({refs(unsafe)} references)"
          f"  -- generic filenames, name match would swap content")
    print(f"DEAD      {len(dead):>5} targets  ({refs(dead)} references)")

    print("\nsample resolutions:")
    for tgt, (s, hit) in list(resolved.items())[:15]:
        print(f"   [{s}] {tgt}\n        -> /{hit}")

    if not apply:
        print("\n(dry run -- pass --apply to rewrite the HTML)")
        return

    # rewrite each page's raw refs to a root-relative path that resolves
    edits = collections.defaultdict(list)
    for tgt, (s, hit) in resolved.items():
        for page, raw in missing[tgt]:
            edits[page].append((raw, "/" + hit))
    changed = 0
    for page, pairs in edits.items():
        fp = os.path.join(ROOT, page.lstrip("/"))
        d = open(fp, "rb").read().decode("latin-1", "ignore")
        orig = d
        for raw, new in set(pairs):
            d = d.replace(f'"{raw}"', f'"{new}"')
        if d != orig:
            open(fp, "w", encoding="latin-1", errors="ignore").write(d)
            changed += 1
    print(f"\nrewrote {changed} pages")


if __name__ == "__main__":
    main()
