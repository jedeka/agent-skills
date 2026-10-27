#!/usr/bin/env python3
"""Surface checks for an explanation.

Finds what a script can find: sentences past the length ceiling, acronyms used
before their definition, words that mark a skipped step, analogies with no
stated limit, magnitudes with no number, bare "this", stacked hedges, forward
references, spelling variants of one term, and chat filler. It cannot judge
truth, the order of ideas, or whether an example is correct.

Usage:
    explain_check.py draft.md
    explain_check.py --reader technical --known LRU,TTL < draft.md
    explain_check.py --text draft.md

Exit 0: nothing to fix. Exit 1: one or more `fix` findings. Exit 2: bad input.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict

TARGET_WORDS = 25            # ASD-STE100 rule 6.3
MAX_WORDS = 35
TARGET_SHARE = 0.80
MAX_PARAGRAPH_WORDS = 150    # ASD-STE100 rules 6.3 and 6.6: six sentences of 25 words
LIMIT_WINDOW = 5             # sentences after an analogy in which its limit must appear
MIN_SENTENCES_FOR_SHARE = 5

EVERYDAY = {
    "OK", "US", "USA", "UK", "EU", "UN", "AM", "PM", "AD", "BC", "CE", "BCE", "TV", "PC",
    "ID", "DIY", "FAQ", "PDF", "URL", "GPS", "ATM", "CEO", "DNA", "RNA", "CO2", "H2O",
    "KB", "MB", "GB", "TB",
}
TECHNICAL = {
    "API", "CPU", "GPU", "RAM", "ROM", "SSD", "HDD", "OS", "IO", "IP", "TCP", "UDP", "DNS",
    "HTTP", "HTTPS", "HTML", "CSS", "JS", "JSON", "XML", "YAML", "SQL", "CSV", "UI", "UX",
    "CLI", "GUI", "IDE", "SDK", "SSH", "SSL", "TLS", "VM", "CI", "PR", "AI", "ML", "REST",
    "UTF", "ASCII", "UUID", "AWS", "RPC", "REPL", "TODO", "LLM",
}
CAPITALIZED_WORDS = {
    "NOTE", "TODO", "TIP", "FIXME", "AND", "OR", "NOT", "XOR", "NAND", "NOR", "IF", "THEN",
    "ELSE", "TRUE", "FALSE", "NULL", "NONE", "YES", "NO", "ON", "OFF",
    "II", "III", "IV", "VI", "VII", "VIII", "IX", "XI", "XII", "XIII", "XIV", "XV", "XX",
}
ENGLISH_FUNCTION_WORDS = {
    "the", "and", "is", "are", "of", "to", "in", "that", "it", "for", "with", "on", "this",
    "but", "not", "as", "at", "or", "by", "from", "be", "an", "a", "if", "when", "which",
}

WORD = re.compile(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*")
ACRONYM = re.compile(r"\b[A-Z][A-Z0-9]{1,6}s?\b")
FENCE = re.compile(r"^\s*(```|~~~)")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
PROTECT = re.compile(
    r"\b(?:e\.g|i\.e)\.|\b(?:etc|vs|cf|Fig|Eq|Dr|Mr|Mrs|Ms|Prof|No|approx|al|St)\.(?=\s+[a-z0-9(])"
    r"|\d\.\d|\b[A-Z]\.(?=[A-Z]\.)"
)
BOUNDARY = re.compile(
    r"(?<=[.!?])[\"'”’)\]]*\s+(?=[\"'“‘(\[]?(?:[A-Z0-9]|(?:code|expr|quote|link)\b))")

OPENERS = re.compile(
    r"^(?:(?:great|good|excellent|interesting|fantastic)\s+question"
    r"|(?:sure|certainly|absolutely)[,!.]"
    r"|let(?:'s|’s| us| me)\s+(?:dive|dig|break|unpack|explore|explain|walk)"
    r"|in this (?:explanation|answer|guide|post|article|section),?\s+(?:we|i)\b"
    r"|i(?:'ll|’ll| will)\s+(?:explain|walk|break)"
    r"|here(?:'s|’s| is)\s+(?:an?|the)\s+(?:simple |quick |brief |clear )?(?:explanation|breakdown|overview|rundown))",
    re.I,
)
CLOSERS = re.compile(
    r"\b(?:i hope (?:this|that) helps|hope (?:this|that) helps|let me know if"
    r"|feel free to (?:ask|reach)|happy to (?:explain|elaborate|help|clarify))\b",
    re.I,
)
SKIPPED_STEP = [
    (re.compile(r"\bobviously\b", re.I), "obviously"),
    (re.compile(r"\bof course\b", re.I), "of course"),
    (re.compile(r"\btrivially\b|\btrivial to\b", re.I), "trivially"),
    (re.compile(r"\bstraightforward(?:ly)?\b", re.I), "straightforward"),
    (re.compile(r"\b(?:easy|simple) to (?:see|show|verify|check|prove)\b"
                r"|\beasily (?:seen|shown|verified)\b", re.I), "easy to see"),
    (re.compile(r"\bas (?:is well known|everyone knows|we all know|you know)\b"
                r"|\bneedless to say\b|\bgoes without saying\b", re.I), "as everyone knows"),
    (re.compile(r"(?:^|[.;:,]\s+|\b(?:is|are|it|this|that|which|so|and|then|we)\s+)clearly\b",
                re.I), "clearly"),
    (re.compile(r"\b(?:you|we|can|could|just|then|and|is|are|it)\s+simply\b"
                r"(?!\s+(?:connected|typed|put|stated|laced))"
                r"|\bsimply\s+(?:call|use|add|run|set|take|apply|multiply|divide|replace|plug"
                r"|substitute|follows|means|returns|stores|a|an|the|by)\b", re.I), "simply"),
]
MINIMIZER = re.compile(
    r"\bjust\s+(?:use|add|call|run|set|take|apply|multiply|divide|replace|plug|substitute|do"
    r"|need|have to)\b|\b(?:is|are)\s+just\s+(?:an?|the)\b",
    re.I,
)
ANALOGY = re.compile(
    r"\b(?:think of|imagine|picture an?|(?:is|are|works|acts|behaves)\s+like|similar to how|akin to"
    r"|analogous to|(?:by|this|the|that|a (?:useful|good|common|helpful|rough|loose|simple)) analogy)\b",
    re.I,
)
ANALOGY_LIMIT = re.compile(
    r"\b(?:breaks?|unlike|differs?|difference|not exactly|except|in reality|strictly"
    r"|(?:analogy|picture|comparison|image|metaphor)\s+(?:fails|stops|ends|misleads|goes wrong)"
    r"|where (?:this|the) (?:analogy|picture|comparison|image|metaphor)"
    r"|(?:does not|doesn't|doesn’t|do not|don't|don’t)\s+(?:carry|hold|apply|map))\b",
    re.I,
)
VAGUE_MAGNITUDE = re.compile(
    r"\b(?:significantly|substantially|dramatically|considerably|drastically|vastly|hugely"
    r"|massively|enormously|tremendously)\b"
    r"|\b(?:much|far|way|a lot|lots)\s+(?:faster|slower|larger|smaller|bigger|better|worse"
    r"|more|less|higher|lower|cheaper|quicker)\b",
    re.I,
)
BARE_THIS = re.compile(
    r"^(?:This|That|These|Those)\s+(?:is|are|was|were|means|meant|allows|lets|makes|gives|shows"
    r"|happens|works|causes|leads|results|ensures|implies|can|will|would|should|has|have|helps"
    r"|enables|requires|provides|matters|explains|creates|produces|prevents)\b"
    r"(?!\s+(?:why|because|where|how|what)\b)"
)
HEDGE_PAIR = re.compile(
    r"\b(?:may|might|could|can)\s+(?:possibly|potentially|perhaps|maybe|conceivably)\b"
    r"|\b(?:possibly|perhaps|maybe|probably|likely)\s+(?:may|might|could)\b"
    r"|\b(?:seems?|appears?)\s+to\s+(?:possibly|perhaps|potentially|somewhat)\b"
    r"|\b(?:somewhat|fairly|rather|quite)\s+(?:likely|possibly|probably)\b",
    re.I,
)
HEDGE = re.compile(
    r"\b(?:may|might|could|possibly|perhaps|maybe|probably|potentially|arguably|somewhat"
    r"|seems?|appears?|tends? to|generally|in some cases|to some extent)\b",
    re.I,
)
FORWARD_REFERENCE = re.compile(
    r"\bas we(?:'ll|’ll| will| shall) see\b"
    r"|\bwe(?:'ll|’ll| will) (?:see|cover|discuss|return to|come back to|get to)\b[^.]{0,30}"
    r"\b(?:later|below|shortly|soon|in a moment)\b"
    r"|\bmore on (?:this|that) (?:later|below|shortly)\b"
    r"|\b(?:discussed|explained|covered|described|defined) (?:later|below|further down)\b",
    re.I,
)
PASSIVE_BY = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?"
    r"(\w+(?:ed|en)|built|made|done|sent|kept|held|found|shown|read|run|set|put|drawn)\s+by\s+"
    r"(?!\d|definition\b|default\b|design\b|hand\b|convention\b|construction\b|law\b)",
    re.I,
)
PASSIVE_IDIOMS = {"divided", "multiplied", "followed", "preceded", "given", "denoted", "meant",
                  "indexed", "bounded"}
# Pairs that are two different words rather than two spellings of one term.
NOT_VARIANTS = {"anymore", "everyday", "sometime", "sometimes", "anything", "everything",
                "anyone", "everyone", "someone", "without", "another", "nowhere", "forever"}


def mask(text: str) -> str:
    """Blank out spans the rules do not govern, keeping every line where it was."""
    out, fence, front = [], None, False
    for i, line in enumerate(text.split("\n")):
        if i == 0 and line.strip() == "---":
            front = True
            out.append("")
            continue
        if front:
            front = line.strip() not in ("---", "...")
            out.append("")
            continue
        m = FENCE.match(line)
        if m:
            fence = None if fence == m.group(1) else (fence or m.group(1))
            out.append("")
            continue
        out.append("" if fence else line)
    text = "\n".join(out)
    text = re.sub(r"(?m)^\s*(?:[-*+]|\d+[.)])\s+\[[^\]]+\]\(#[^)]*\)\s*$", "", text)
    text = re.sub(r"\$\$.*?\$\$", lambda m: "\n" * m.group().count("\n"), text, flags=re.S)
    text = re.sub(r"`[^`\n]+`", "code", text)
    text = re.sub(r"\$(?=\S)[^$\n]+?(?<=\S)\$(?!\d)", "expr", text)
    text = re.sub(r"\\\(.*?\\\)", "expr", text)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"https?://\S+", "link", text)
    text = re.sub(r"<[^>\n]+>", "", text)
    text = re.sub(r"[\"“][^\"”\n]{1,80}[\"”]", "quote", text)
    return re.sub(r"(\*\*|__|\*)(?=\S)(.+?)(?<=\S)\1", r"\2", text)


def units(masked: str):
    """Yield (kind, line, text): 'para' and 'item' blocks, and 'skip' lines (headings, tables, quotes)."""
    kind, start, buf = None, 0, []

    def flush():
        nonlocal kind, buf
        if buf:
            yield kind, start, "\n".join(buf)
        kind, buf = None, []

    for n, line in enumerate(masked.split("\n"), 1):
        s = line.strip()
        if not s or re.fullmatch(r"[-*_=]{3,}", s):
            yield from flush()
        elif s.startswith(("#", "|", ">")):
            yield from flush()
            yield "skip", n, s
        elif LIST_ITEM.match(line):
            yield from flush()
            kind, start, buf = "item", n, [LIST_ITEM.sub("", line)]
        else:
            if kind is None:
                kind, start = "para", n
            buf.append(line)
    yield from flush()


def split_sentences(block: str):
    protected = PROTECT.sub(lambda m: m.group().replace(".", "\x00"), block)
    spans, start = [], 0
    for m in BOUNDARY.finditer(protected):
        spans.append((start, m.start()))
        start = m.end()
    spans.append((start, len(block)))
    return [(a, " ".join(block[a:b].split())) for a, b in spans if block[a:b].strip()]


def definition_patterns(stem: str):
    s = re.escape(stem)
    return re.compile(
        rf"\(\s*{s}s?\s*[),;]"
        rf"|\b{s}s?\s*\([^)]{{4,}}\)"
        rf"|\b{s}s?\b[^.()]{{0,30}}\b(?:stands for|is short for|short for|means|named (?:for|after))\b"
        rf"|\b(?:called|named|abbreviated(?:\s+(?:as|to))?|known as|written)\s+(?:an?\s+|the\s+)?{s}\b"
        rf"|^(?:An?\s+|The\s+)?{s}s?\s+(?:is|are)\s+(?:an?|the|any|one)\b"
        rf"|\b{s}\s*[:—–]\s"
    )


def acronym_stems(sentence: str, known: set[str]):
    letters = [c for c in sentence if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.6:
        return
    for m in ACRONYM.finditer(sentence):
        tok = m.group()
        stem = tok[:-1] if tok.endswith("s") else tok
        # "STE100" in "ASD-STE100" is the known "STE" with a version number.
        if sum(c.isupper() for c in stem) >= 2 and not {stem, stem.rstrip("0123456789")} & known:
            yield stem


def check(text: str, reader: str = "general", known: set[str] | None = None) -> dict:
    known_acronyms = EVERYDAY | CAPITALIZED_WORDS | (known or set())
    if reader == "technical":
        known_acronyms |= TECHNICAL

    masked = mask(text)
    tokens = [t.lower() for t in WORD.findall(masked)]
    if len(tokens) >= 30 and sum(t in ENGLISH_FUNCTION_WORDS for t in tokens) / len(tokens) < 0.15:
        return {"verdict": "clean", "non_english": True, "counts": {"fix": 0, "review": 0},
                "metrics": {}, "findings": []}

    findings: list[dict] = []

    def add(check_name, severity, line, excerpt, message):
        findings.append({"check": check_name, "severity": severity, "line": line,
                         "excerpt": excerpt[:100], "message": message})

    sentences = []   # (line, text, paragraph index)
    first_use: dict[str, tuple[int, int, str]] = {}
    defined_at: dict[str, int] = {}
    seq = 0          # position of each sentence or skipped line in reading order
    paragraphs = 0

    def note_definitions(fragment: str):
        for stem in set(re.findall(r"[A-Z][A-Z0-9]{1,6}", fragment)):
            if stem not in defined_at and definition_patterns(stem).search(fragment):
                defined_at[stem] = seq

    for kind, line, block in units(masked):
        if kind == "skip":
            note_definitions(block)
            seq += 1
            continue
        paragraphs += 1
        in_block = split_sentences(block)
        block_words = len(WORD.findall(block))
        if kind == "para" and block_words > MAX_PARAGRAPH_WORDS:
            add("long_paragraph", "review", line, in_block[0][1],
                f"{block_words} words in one paragraph (target: {MAX_PARAGRAPH_WORDS}); "
                "split at the change of topic")
        for offset, sent in in_block:
            sent_line = line + block[:offset].count("\n")
            note_definitions(sent)
            for stem in acronym_stems(sent, known_acronyms):
                first_use.setdefault(stem, (seq, sent_line, sent))
            sentences.append((sent_line, sent, paragraphs))
            seq += 1

    for stem, (pos, line, sent) in first_use.items():
        if stem not in defined_at:
            add("undefined_acronym", "fix", line, sent,
                f"{stem} is never defined; expand it at first use, or pass --known {stem}")
        elif defined_at[stem] > pos + 1:
            add("undefined_acronym", "fix", line, sent, f"{stem} is used before its definition")

    lengths = []
    for i, (line, sent, _) in enumerate(sentences):
        n = len(WORD.findall(sent))
        lengths.append(n)
        if n > MAX_WORDS:
            add("long_sentence", "fix", line, sent, f"{n} words (ceiling: {MAX_WORDS}); split it")
        if i == 0 and OPENERS.search(sent):
            add("chat_filler", "fix", line, sent, "opens with filler; start with the point")
        if CLOSERS.search(sent):
            add("chat_filler", "fix", line, sent, "closing filler; end on content")
        for pattern, label in SKIPPED_STEP:
            if pattern.search(sent):
                add("skipped_step", "fix", line, sent,
                    f'"{label}" marks a step the reader was not shown; write the step or cut the word')
        if MINIMIZER.search(sent):
            add("minimizer", "review", line, sent,
                '"just" hides a step or a difference; say what the step or the difference is')
        if ANALOGY.search(sent):
            window = " ".join(s for _, s, _ in sentences[i:i + 1 + LIMIT_WINDOW])
            if not ANALOGY_LIMIT.search(window):
                add("analogy_without_limit", "review", line, sent,
                    "analogy with no stated limit; say where the comparison stops being true")
        if VAGUE_MAGNITUDE.search(sent) and not re.search(r"\d", sent):
            add("vague_magnitude", "review", line, sent,
                "magnitude with no number; give the quantity and its unit")
        if BARE_THIS.search(sent):
            add("bare_this", "review", line, sent,
                'bare "this/that"; name the thing it points to')
        if HEDGE_PAIR.search(sent) or len(HEDGE.findall(sent)) >= 3:
            add("hedge_stack", "review", line, sent,
                "stacked hedges; state the uncertainty once, at its real strength")
        if FORWARD_REFERENCE.search(sent):
            add("forward_reference", "review", line, sent,
                "points ahead; reorder so the reader has the idea when it is needed")
        m = PASSIVE_BY.search(sent)
        if m and m.group(1).lower() not in PASSIVE_IDIOMS:
            add("passive_with_actor", "review", line, sent,
                "the actor sits after \"by\"; make the actor the subject")

    share = sum(n <= TARGET_WORDS for n in lengths) / len(lengths) if lengths else 1.0
    if len(lengths) >= MIN_SENTENCES_FOR_SHARE and share < TARGET_SHARE:
        add("length_share", "review", sentences[0][0], "",
            f"{share:.0%} of sentences are within {TARGET_WORDS} words (target: {TARGET_SHARE:.0%})")

    surfaces: dict[str, dict[str, int]] = defaultdict(dict)
    singles: dict[str, int] = {}
    for line, sent, _ in sentences:
        low = sent.lower()
        for tok in re.findall(r"[a-z]+(?:-[a-z]+)+", low):
            surfaces[tok.replace("-", "")].setdefault(tok, line)
        for tok in re.findall(r"\b[a-z]{7,}\b", low):
            singles.setdefault(tok, line)
        for m in re.finditer(r"(?=\b([a-z]{3,}) ([a-z]{3,})\b)", low):
            surfaces[m.group(1) + m.group(2)].setdefault(f"{m.group(1)} {m.group(2)}", line)
    for key, forms in surfaces.items():
        if key not in singles or key in NOT_VARIANTS:
            continue
        forms = {**forms, key: singles[key]}
        if len(forms) >= 2:
            ordered = sorted(forms, key=forms.get)
            add("term_variants", "review", forms[ordered[1]], "",
                "one term, several spellings: " + ", ".join(f'"{f}"' for f in ordered) + "; keep one")

    findings.sort(key=lambda f: (f["line"], f["severity"] != "fix"))
    counts = {s: sum(f["severity"] == s for f in findings) for s in ("fix", "review")}
    return {
        "verdict": "fix" if counts["fix"] else "review" if counts["review"] else "clean",
        "counts": counts,
        "metrics": {
            "words": sum(lengths),
            "sentences": len(lengths),
            "paragraphs": paragraphs,
            "mean_sentence_words": round(sum(lengths) / len(lengths), 1) if lengths else 0,
            "max_sentence_words": max(lengths, default=0),
            "share_within_target": round(share, 2),
        },
        "findings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", nargs="?", help="text or Markdown file; stdin if omitted")
    parser.add_argument("--reader", choices=("general", "technical"), default="general",
                        help="technical readers know common computing acronyms")
    parser.add_argument("--known", default="", help="comma-separated acronyms the reader knows")
    parser.add_argument("--text", action="store_true", help="one line per finding instead of JSON")
    args = parser.parse_args(argv)

    try:
        source = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
    except OSError as err:
        print(f"cannot read input: {err}", file=sys.stderr)
        return 2
    if not source.strip():
        print("empty input", file=sys.stderr)
        return 2

    result = check(source, args.reader, {k.strip() for k in args.known.split(",") if k.strip()})
    if args.text:
        for f in result["findings"]:
            print(f'L{f["line"]:<4} {f["severity"]:<6} {f["check"]:<22} {f["message"]}')
        m = result["metrics"]
        if m:
            print(f'{result["verdict"]}: {result["counts"]["fix"]} fix, {result["counts"]["review"]} review; '
                  f'{m["sentences"]} sentences, mean {m["mean_sentence_words"]} words, '
                  f'max {m["max_sentence_words"]}, {m["share_within_target"]:.0%} within {TARGET_WORDS}')
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["counts"]["fix"] else 0


if __name__ == "__main__":
    sys.exit(main())
