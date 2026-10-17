#!/usr/bin/env python3
"""Validate claim records in findings.md or proposed.md.

Usage:
    python3 validate_findings.py <findings.md | proposed.md> [--proposed] [--no-paths] [--json]

Checks every `### C<n>:` claim record for the required fields and the
status rules in references/claim-record.md, the four sections of
findings.md, the killed-hypothesis records, and that every project path a
record names exists on disk (relative to the file). Exit 0 when the file
passes, 1 when anything fails, 2 on a usage error. Standard library only.
"""
import json
import re
import sys
from pathlib import Path

STATUSES = ("GROUNDED", "DERIVED", "CONJECTURED", "UNKNOWN")
REQUIRED_FIELDS = ("Status", "Warrant", "Certified by", "Conditions", "Red team", "Would change it", "Hypothesis", "Updated")
SECTIONS = ("## Current best answer", "## Claims", "## Killed hypotheses", "## Open gaps")

RECORD_HEAD = re.compile(r"^###\s+(C\d+):\s*(.*)$", re.M)
KILLED_HEAD = re.compile(r"^###\s+(H\d+):\s*(.*)$", re.M)
FIELD_START = re.compile(r"^-[ \t]*([A-Za-z ]+?):[ \t]*(.*)$")
URL = re.compile(r"https?://\S+")
PATH = re.compile(r"\b((?:literature|experiments|reviews|probes|deepdive|src)/[^\s,;:)]+)")
PERCENT = re.compile(r"\d+(?:\.\d+)?\s*%")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
NOT_YET = re.compile(r"\bNOT YET\b", re.I)
NONE = re.compile(r"^NONE\b", re.I)
RED_TEAM_OK = re.compile(r"\b(survived|wounded)\b", re.I)
ANALYSIS = re.compile(r"experiments/[^\s]+/analysis\.md")
DERIVATION = re.compile(r"derivation above", re.I)
VERIFIED = re.compile(r"\bverified:\s*\S+.*,\s*\S", re.I)


def parse_fields(body):
    """Map field name -> value. A value continues on the lines below it until the next `- Field:` line."""
    fields, current = {}, None
    for line in body.splitlines():
        m = FIELD_START.match(line)
        if m:
            current = m.group(1).strip()
            fields[current] = m.group(2).strip()
        elif current and line.strip():
            fields[current] = (fields[current] + " " + line.strip()).strip()
    return fields


def blocks(text, head_re):
    """Yield (id, title, body) for each heading matched by head_re, body up to the next ### or ## heading."""
    heads = list(head_re.finditer(text))
    for i, m in enumerate(heads):
        start = m.end()
        nxt = re.search(r"^##", text[start:], re.M)
        end = start + nxt.start() if nxt else len(text)
        yield m.group(1), m.group(2).strip(), text[start:end]


def section_text(text, name):
    m = re.search(rf"^{re.escape(name)}\s*$", text, re.M)
    if not m:
        return None
    rest = text[m.end():]
    nxt = re.search(r"^## ", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def check_record(cid, title, body, proposed, base, check_paths):
    problems = []
    fields = parse_fields(body)

    def bad(field, why):
        problems.append({"record": cid, "field": field, "problem": why})

    if not title:
        bad("title", "the heading needs the claim in one sentence")

    for f in REQUIRED_FIELDS:
        if f not in fields:
            bad(f, "missing")
        elif not fields[f]:
            bad(f, "empty")
    if not fields.get("Status"):
        return problems

    status = fields["Status"].strip().upper()
    if status not in STATUSES:
        bad("Status", "must be one of GROUNDED, DERIVED, CONJECTURED, UNKNOWN")
        return problems

    warrant, cert, red = fields.get("Warrant", ""), fields.get("Certified by", ""), fields.get("Red team", "")

    if status == "GROUNDED":
        if not (URL.search(warrant) or URL.search(cert) or "literature/" in cert or "deepdive/" in cert):
            bad("Certified by", "GROUNDED needs the literature note or the source URLs")
        if not (URL.search(warrant) or "\"" in warrant or "“" in warrant):
            bad("Warrant", "GROUNDED needs the quoted span with its URL")
    elif status == "DERIVED":
        if not (ANALYSIS.search(cert) or DERIVATION.search(cert) or VERIFIED.search(cert)):
            bad("Certified by", "DERIVED needs experiments/<slug>/analysis.md with SUPPORTED or KILLED, 'derivation above', or 'verified: <path>, <checker>'")
        if ANALYSIS.search(cert) and not re.search(r"\b(SUPPORTED|KILLED)\b", cert):
            bad("Certified by", "name the decision rule's output: SUPPORTED or KILLED")
    elif status == "CONJECTURED":
        if not PERCENT.search(warrant):
            bad("Warrant", "CONJECTURED needs a prior as a percentage, then the argument")
        if not NONE.match(cert):
            bad("Certified by", "CONJECTURED is certified by NONE, by definition")
    elif status == "UNKNOWN":
        if not NONE.match(cert):
            bad("Certified by", "UNKNOWN is certified by NONE")

    if status in ("GROUNDED", "DERIVED") and not proposed:
        if NOT_YET.search(red):
            bad("Red team", f"{status} cannot enter findings.md before the attack; run red-teaming-research on proposed.md")
        elif not (RED_TEAM_OK.search(red) and PATH.search(red)):
            bad("Red team", "name the review file (reviews/<date>-<label>.md) and the verdict, survived or wounded")
    if RED_TEAM_OK.search(red) and re.search(r"\bwounded\b", red, re.I) and "conced" not in red.lower():
        bad("Red team", "a wounded verdict names what was conceded into Conditions")

    if not DATE.match(fields.get("Updated", "")):
        bad("Updated", "needs YYYY-MM-DD")

    if check_paths:
        for field in ("Certified by", "Red team"):
            for p in PATH.findall(fields.get(field, "")):
                if not (base / p).exists():
                    bad(field, f"path does not exist: {p}")
    return problems


def check_file(path, proposed, check_paths):
    text = path.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)  # template comments are not records
    base = path.parent
    problems = []

    ids = RECORD_HEAD.findall(text)
    seen = set()
    for cid, _ in ids:
        if cid in seen:
            problems.append({"record": cid, "field": "id", "problem": "duplicate record id"})
        seen.add(cid)

    records = list(blocks(text, RECORD_HEAD))
    for cid, title, body in records:
        problems.extend(check_record(cid, title, body, proposed, base, check_paths))

    if not proposed:
        for s in SECTIONS:
            if section_text(text, s) is None:
                problems.append({"record": "file", "field": s, "problem": "section missing"})
        answer = section_text(text, "## Current best answer")
        if answer is not None:
            if not answer.strip():
                problems.append({"record": "file", "field": "Current best answer", "problem": "empty"})
            elif not re.search(r"\bC\d+\b", answer):
                problems.append({"record": "file", "field": "Current best answer", "problem": "must cite the record ids it rests on, as (C7)"})
            else:
                for ref in set(re.findall(r"\bC\d+\b", answer)):
                    if ref not in seen:
                        problems.append({"record": "file", "field": "Current best answer", "problem": f"cites {ref}, which is not a record in this file"})
        killed = section_text(text, "## Killed hypotheses")
        if killed:
            for hid, title, body in blocks(killed, KILLED_HEAD):
                fields = parse_fields(body)
                if not fields.get("Killed by"):
                    problems.append({"record": hid, "field": "Killed by", "problem": "missing: name the analysis.md, probe or review that killed it"})
                elif check_paths:
                    for p in PATH.findall(fields["Killed by"]):
                        if not (base / p).exists():
                            problems.append({"record": hid, "field": "Killed by", "problem": f"path does not exist: {p}"})
                if not fields.get("Date") or not DATE.match(fields["Date"]):
                    problems.append({"record": hid, "field": "Date", "problem": "needs YYYY-MM-DD"})
        if not records:
            problems.append({"record": "file", "field": "Claims", "problem": "no claim records found"})

    return {"file": str(path), "records": len(records), "problems": problems, "passed": not problems}


def main(argv):
    flags = {a for a in argv[1:] if a.startswith("--")}
    args = [a for a in argv[1:] if not a.startswith("--")]
    unknown = flags - {"--proposed", "--no-paths", "--json"}
    if unknown or len(args) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    target = Path(args[0])
    if not target.is_file():
        print(f"not found: {target}", file=sys.stderr)
        return 2
    result = check_file(target, "--proposed" in flags, "--no-paths" not in flags)
    if "--json" in flags:
        print(json.dumps(result, indent=1))
    else:
        mark = "PASS" if result["passed"] else "FAIL"
        print(f"{mark}  {result['file']}  ({result['records']} records)")
        for p in result["problems"]:
            print(f"      {p['record']} | {p['field']}: {p['problem']}")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
