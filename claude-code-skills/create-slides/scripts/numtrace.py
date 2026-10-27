"""numtrace.py: trace every number on a deck's slide faces and in its speaker notes to source text files.

    python3 numtrace.py <deck_dir> <source> [<source> ...] [--allow 0-20,100] [--faces-only]
                        [--exact] [--verbose] [--chrome PATH] [--budget MS]

The deck's text is read as `deck.py text` prints it (deck.slide_texts: the deck is built and rendered
in Chrome); the sources are UTF-8 text files: CSV, JSON, Markdown, logs, the saved output of the
command that produced the numbers (a derived number's arithmetic included), a paper's page-marked text
(quotecheck.py text writes one from a PDF). NUL bytes in a source are ignored; a PDF or another binary
file is refused with exit 2.

A number is a run of digits with an optional decimal part ("0.83", ".5"; "1,204" is 1204), not glued
to a letter, digit, underscore or dot before it, so ids and versions such as "G13", "v1.2", "p.14" and
"run_3" are not numbers; a unit after it is allowed ("12ms", "4B"). Signs are not read: "-0.4" and
"−0.4" are 0.4, and "21–31%" is 21 and 31. A number followed by "%", or the first number of a range
that ends in "%", is a percentage. Sources are read the same way.

A number on a slide is traced when a source holds:
    exact    the same value (0.40 = 0.4; leading zeros ignored: "03" = 3)
    rounded  a value with more decimals that rounds to it, half up or half to even (0.8349 -> 0.83,
             2.5 -> 2 or 3): rules allow rounding once from the unrounded value
    percent  for a percentage, a fraction 100 times smaller, exact or rounded (0.353 -> 35.3%)
--exact turns the last two off. Traced means the value occurs in a source, not that it is the right
one: the trace finds numbers with no source at all and most copying errors, not a number taken from
the wrong row. Small integers trace almost always; give the ones that need no source (ordinals, slide
and section numbers, counts the slide defines itself) with --allow: values and integer ranges,
"--allow 0-20,100" allows 0, 1, ..., 20 and 100. Text inside images is not read.

Prints each untraced number with its slide, face or notes, and the line it stands in, then a summary;
--verbose also lists every traced number with its source file and line. Exit 0 when every number is
traced or allowed, 1 when any is untraced, 2 on a usage, source or build error.
"""
import argparse
import re
import sys
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import deck as D  # noqa: E402  (the deck engine: build, render, slide_texts)

NUM = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+(?![\d,])|\d+)?(\.\d+)?(?!\d)")
PCT = re.compile(r"\s?%|\s*[-–—]\s*(?:\d{1,3}(?:,\d{3})+|\d+)?(?:\.\d+)?\s?%")


def numbers(text: str):
    """Yield (value, decimals, is_percent, start, end) for every number in text."""
    for m in NUM.finditer(text):
        if not m[1] and not m[2]:
            continue
        lit = (m[1] or "0").replace(",", "") + (m[2] or "")
        pct = bool(PCT.match(text, m.end()))
        yield Decimal(lit), len(m[2]) - 1 if m[2] else 0, pct, m.start(), m.end()


def scale(v: Decimal, dec: int, pct: bool) -> tuple:
    """A source value as a percentage reads it: x100, two fewer decimals."""
    return (v * 100, max(dec - 2, 0)) if pct else (v, dec)


def read_text(p: Path) -> str:
    """A source file as text. NUL bytes are dropped (text extracted from a PDF can hold them: TeX's large
    parentheses have codes 0 and 1). A PDF, or a file of which over 5% does not decode as UTF-8, is refused."""
    data = p.read_bytes()
    text = data.replace(b"\0", b"").decode("utf-8", errors="replace")
    if data[:5] == b"%PDF-" or text.count("\ufffd") * 20 > len(text):
        raise D.DeckError(f"source {p} is not a text file; extract its text first "
                          "(for a PDF: quotecheck.py text <pdf> --out <file.txt>)")
    return text


class Sources:
    """Every number of the source files, indexed for exact and rounded lookup."""

    def __init__(self, paths: list):
        self.nums = []                         # (value, decimals, where)
        self.exact = {}
        for path in paths:
            p = Path(path)
            if not p.is_file():
                raise D.DeckError(f"source {path} is not a file")
            text = read_text(p)
            for ln, line in enumerate(text.splitlines(), 1):
                for v, dec, _, _, _ in numbers(line):
                    self.nums.append((v, dec, f"{p.name}:{ln}"))
                    for pct in (False, True):
                        self.exact.setdefault((pct, scale(v, dec, pct)[0]), f"{p.name}:{ln}")
        self.rounded = {}                      # (pct, decimals) -> {rounded value: where}

    def rounding(self, pct: bool, d: int) -> dict:
        key = (pct, d)
        if key not in self.rounded:
            q, table = Decimal(1).scaleb(-d), {}
            for v, dec, where in self.nums:
                v, dec = scale(v, dec, pct)
                if dec > d:
                    for mode in (ROUND_HALF_UP, ROUND_HALF_EVEN):
                        try:
                            table.setdefault(v.quantize(q, rounding=mode), where)
                        except InvalidOperation:       # more digits than Decimal's precision: no match
                            pass
            self.rounded[key] = table
        return self.rounded[key]

    def trace(self, v: Decimal, dec: int, pct: bool, exact_only: bool):
        """(how, where) for a number on a slide, or None."""
        if (False, v) in self.exact:
            return "exact", self.exact[(False, v)]
        if pct and (True, v) in self.exact:
            return "percent", self.exact[(True, v)]
        if exact_only:
            return None
        for p in (False, True) if pct else (False,):
            where = self.rounding(p, dec).get(v)
            if where:
                return ("percent, rounded" if p else "rounded"), where
        return None


def parse_allow(spec: str) -> set:
    allowed = set()
    for part in filter(None, (s.strip() for s in spec.split(","))):
        lo, sep, hi = part.partition("-")
        try:
            if sep:
                allowed |= {Decimal(i) for i in range(int(lo), int(hi) + 1)}
            else:
                allowed.add(Decimal(part))
        except (ValueError, InvalidOperation):
            raise D.DeckError(f"--allow: '{part}' is neither a number nor an integer range such as 0-20")
    return allowed


def context(line: str, start: int, end: int, width: int = 80) -> str:
    a = max(0, start - (width - (end - start)) // 2)
    b = min(len(line), a + width)
    return ("..." if a else "") + line[a:b] + ("..." if b < len(line) else "")


def main(argv=None) -> int:
    sys.stdout.reconfigure(line_buffering=True)
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("deck_dir", help="deck folder holding deck.json, slides/ and assets/")
    p.add_argument("sources", nargs="+", help="source text files the numbers come from")
    p.add_argument("--allow", default="",
                   help="numbers that need no source: values and integer ranges, e.g. 0-20,100")
    p.add_argument("--faces-only", action="store_true", help="skip the speaker notes")
    p.add_argument("--exact", action="store_true",
                   help="accept exact values only (no rounding, no percent scaling)")
    p.add_argument("--verbose", action="store_true",
                   help="also list every traced number and where it was found")
    p.add_argument("--chrome", default="", help="path to Chrome/Chromium (else CHROME_PATH, PATH)")
    p.add_argument("--budget", type=int, default=8000, help="Chrome virtual-time budget in ms")
    a = p.parse_args(argv)
    try:
        allowed = parse_allow(a.allow)
        src = Sources(a.sources)
        texts = D.slide_texts(a)
    except D.DeckError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    counts, untraced = {"exact": 0, "rounded": 0, "allowed": 0}, []
    for t in texts:
        for part in ("face",) if a.faces_only else ("face", "notes"):
            for line in t[part].splitlines():
                for v, dec, pct, s, e in numbers(line):
                    lit = line[s:e] + ("%" if pct and line[e:e + 1] == "%" else "")
                    where = f"slide {t['n']:02d} {part:<5}"
                    if v in allowed:
                        counts["allowed"] += 1
                        continue
                    hit = src.trace(v, dec, pct, a.exact)
                    if hit:
                        counts["exact" if hit[0] in ("exact", "percent") else "rounded"] += 1
                        if a.verbose:
                            print(f"traced    {where}  {lit:<10} {hit[0]:<17} {hit[1]}")
                    else:
                        untraced.append(f"untraced  {where}  {lit:<10} {context(line, s, e)}")
    for u in untraced:
        print(u)
    total = sum(counts.values()) + len(untraced)
    print(f"numtrace: {total} number(s) on the {'faces' if a.faces_only else 'faces and in the notes'} of "
          f"{len(texts)} slide(s), against {len(a.sources)} source file(s): {counts['exact']} exact, "
          f"{counts['rounded']} rounded, {counts['allowed']} allowed, {len(untraced)} untraced")
    return 1 if untraced else 0


if __name__ == "__main__":
    sys.exit(main())
