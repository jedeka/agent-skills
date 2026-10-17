#!/usr/bin/env python3
"""Look up a work's references and citing works through the OpenAlex API.

Usage:
    python3 citations.py "<title or DOI>" [--cited-by N] [--refs N] [--json]

Prints the matched work, up to N works it references, and up to N works that
cite it (default 15 each). Optional: when the network is unavailable the script
prints one line saying so and exits 0, so a research run is never blocked by it.
Standard library only. OpenAlex asks for a contact email in the User-Agent;
set OPENALEX_MAILTO to supply one.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.openalex.org"
TIMEOUT = 20


def _get(url):
    mailto = os.environ.get("OPENALEX_MAILTO", "")
    headers = {"User-Agent": f"deepdive-research/1.0 (mailto:{mailto})" if mailto else "deepdive-research/1.0"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.load(resp)


def _brief(work):
    authors = [a.get("author", {}).get("display_name", "") for a in work.get("authorships", [])[:3]]
    loc = (work.get("primary_location") or {}).get("source") or {}
    return {
        "title": work.get("display_name"),
        "year": work.get("publication_year"),
        "authors": authors,
        "venue": loc.get("display_name"),
        "doi": work.get("doi"),
        "cited_by_count": work.get("cited_by_count"),
        "openalex_id": work.get("id"),
        "retracted": work.get("is_retracted", False),
    }


def find_work(query):
    if query.lower().startswith("10.") or "doi.org" in query.lower():
        doi = query.split("doi.org/")[-1]
        return _get(f"{BASE}/works/https://doi.org/{urllib.parse.quote(doi, safe='')}")
    q = urllib.parse.quote(query)
    data = _get(f"{BASE}/works?search={q}&per-page=1")
    results = data.get("results", [])
    return results[0] if results else None


def main(argv):
    as_json = "--json" in argv
    args = [a for a in argv[1:] if a != "--json"]
    n_cited, n_refs = 15, 15
    if "--cited-by" in args:
        i = args.index("--cited-by"); n_cited = int(args[i + 1]); del args[i:i + 2]
    if "--refs" in args:
        i = args.index("--refs"); n_refs = int(args[i + 1]); del args[i:i + 2]
    if len(args) != 1:
        print(__doc__, file=sys.stderr)
        return 2

    try:
        work = find_work(args[0])
        if not work:
            print("no match in OpenAlex")
            return 0
        wid = work["id"].rsplit("/", 1)[-1]
        refs = []
        for rid in work.get("referenced_works", [])[:n_refs]:
            try:
                refs.append(_brief(_get(f"{BASE}/works/{rid.rsplit('/', 1)[-1]}")))
            except (urllib.error.URLError, OSError, ValueError):
                continue
        cited = _get(f"{BASE}/works?filter=cites:{wid}&sort=cited_by_count:desc&per-page={n_cited}")
        citing = [_brief(w) for w in cited.get("results", [])]
    except (urllib.error.URLError, OSError, ValueError) as e:
        print(f"citation lookup unavailable ({e.__class__.__name__}); continue without it")
        return 0

    out = {"work": _brief(work), "references": refs, "cited_by": citing}
    if as_json:
        print(json.dumps(out, indent=1))
        return 0
    w = out["work"]
    print(f"WORK  {w['title']} ({w['year']}) {', '.join(w['authors'])}  cited_by={w['cited_by_count']}"
          f"{'  RETRACTED' if w['retracted'] else ''}\n      {w['doi'] or w['openalex_id']}")
    print(f"\nREFERENCES ({len(refs)} of {len(work.get('referenced_works', []))}):")
    for r in refs:
        print(f"  - {r['title']} ({r['year']})  {r['doi'] or r['openalex_id']}")
    print(f"\nCITED BY (top {len(citing)} by citations):")
    for c in citing:
        print(f"  - {c['title']} ({c['year']})  cited_by={c['cited_by_count']}  {c['doi'] or c['openalex_id']}"
              f"{'  RETRACTED' if c['retracted'] else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
