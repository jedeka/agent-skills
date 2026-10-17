#!/usr/bin/env python3
"""Validate deepdive-research thread notes.

Usage:
    python3 validate_notes.py <notes-dir-or-file> [--json]

Checks every `## Finding:` block for the required fields and every note for
its header fields. Exit code 0 when all notes pass, 1 when any fails,
2 on a usage error. Standard library only.
"""
import json
import re
import sys
from pathlib import Path

HEADER_FIELDS = {
    "Settles when": re.compile(r"^Settles when:\s*\S", re.M),
    "Status": re.compile(r"^Status:\s*(SETTLED|ABSENT|OPEN)\b", re.M),
    "Searched": re.compile(r"^Searched:\s*\S", re.M),
}

# field name -> (regex on the field value, human description of what is wrong)
FINDING_FIELDS = {
    "Claim type": (
        re.compile(r"\b(empirical|theorem|practice|definition|opinion|prediction)\b", re.I),
        "must be one of empirical, theorem, practice, definition, opinion, prediction",
    ),
    "Quote": (re.compile(r"\"[^\"]{8,}\"|“[^”]{8,}”"), "needs a quoted passage of at least 8 characters"),
    "Source": (re.compile(r"https?://\S+"), "needs a URL"),
    "Source type": (
        re.compile(r"\b(primary|secondary|tertiary)\b", re.I),
        "must say primary, secondary or tertiary",
    ),
    "Date true": (re.compile(r"\d{4}|\bundated\b", re.I), "needs a year, a period, or the word undated"),
    "Origin": (
        re.compile(r"this source|these sources|traces to:?\s*\S", re.I),
        "must say 'this source', 'these sources', or 'traces to: <origin>'",
    ),
    "Numbers": (re.compile(r"\S"), "must be present (write 'none' if the finding has no numbers)"),
    "Corroboration": (
        re.compile(r"https?://\S+|NONE YET|DERIVED BY RESEARCHER|two independent sources above|sources above", re.I),
        "needs a second source URL, 'sources above' when the Source field already lists two, NONE YET, or DERIVED BY RESEARCHER",
    ),
    "Bears on": (re.compile(r"\S"), "must say how the finding moves the settling observation"),
}

FIELD_RE = re.compile(r"^-[ \t]*([A-Za-z ]+?):[ \t]*(.*)$", re.M)


def split_findings(text):
    """Return list of (title, body) for each `## Finding:` block."""
    parts = re.split(r"^## Finding:\s*", text, flags=re.M)
    out = []
    for chunk in parts[1:]:
        # body ends at the next level-2 heading
        body = re.split(r"^## ", chunk, maxsplit=1, flags=re.M)[0]
        title = body.splitlines()[0].strip() if body.strip() else "(untitled)"
        out.append((title, body))
    return out


def check_note(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    problems = []

    for name, rx in HEADER_FIELDS.items():
        if not rx.search(text):
            problems.append({"where": "header", "field": name, "problem": "missing or malformed"})

    findings = split_findings(text)
    status = re.search(r"^Status:\s*(\w+)", text, re.M)
    if not findings and status and status.group(1) != "ABSENT":
        problems.append({"where": "note", "field": "Finding", "problem": "no findings and status is not ABSENT"})

    for idx, (title, body) in enumerate(findings, 1):
        fields = {m.group(1).strip(): m.group(2).strip() for m in FIELD_RE.finditer(body)}
        for name, (rx, why) in FINDING_FIELDS.items():
            value = fields.get(name)
            if value is None:
                problems.append({"where": f"finding {idx}: {title[:60]}", "field": name, "problem": "missing"})
            elif not rx.search(value):
                problems.append({"where": f"finding {idx}: {title[:60]}", "field": name, "problem": why})

    if "## Gaps" not in text:
        problems.append({"where": "note", "field": "Gaps", "problem": "section missing (write 'none' if there were no gaps)"})
    if "## Search log" not in text:
        problems.append({"where": "note", "field": "Search log", "problem": "section missing"})

    return {"file": str(path), "findings": len(findings), "problems": problems, "passed": not problems}


def main(argv):
    as_json = "--json" in argv
    args = [a for a in argv[1:] if a != "--json"]
    if len(args) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    target = Path(args[0])
    if target.is_dir():
        files = sorted(p for p in target.glob("*.md") if p.name != "evidence-map.md")
    elif target.is_file():
        files = [target]
    else:
        print(f"not found: {target}", file=sys.stderr)
        return 2
    if not files:
        print(f"no notes found in {target}", file=sys.stderr)
        return 1

    results = [check_note(p) for p in files]
    all_ok = all(r["passed"] for r in results)

    if as_json:
        print(json.dumps({"passed": all_ok, "notes": results}, indent=1))
    else:
        for r in results:
            mark = "PASS" if r["passed"] else "FAIL"
            print(f"{mark}  {r['file']}  ({r['findings']} findings)")
            for p in r["problems"]:
                print(f"      {p['where']} | {p['field']}: {p['problem']}")
        print(f"\n{'all notes pass' if all_ok else 'some notes fail'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
