r"""quotecheck.py: check that every quoted span of a paper-explainer JSON occurs in the paper, on the cited page.

    python3 quotecheck.py <paper.json> [...]                     check each paper's quotes
    python3 quotecheck.py --source <pdf|txt|URL> --page N "quote" check one quote against one source
    python3 quotecheck.py text <pdf|URL> --out <file.txt>        write page-marked text from a PDF

What a paper JSON quotes (references/paper-explainer.md): results[i].quote with results[i].page, and
certifies.quote with certifies.page when given. Each check:
  1. Both the quote and the page text are normalised: NFKC (ligatures such as "ﬁ" become "fi"), lower
     case, and every character that is not a letter or digit removed. Line breaks, hyphens at line
     ends, spacing, punctuation and table layout then cannot cause a false miss.
  2. The quote passes when it is a substring of the cited page joined with its neighbours (page - 1,
     page, page + 1), so a sentence that runs across a page break passes. When it lies wholly on a
     neighbour page, the check passes and says which page to cite.
  3. A quote shorter than 12 normalised characters fails: it would match by chance.
  4. Every number in results[i].text must occur in its quote (0.10 = 0.1; 1,000 = 1000; 14% = 14), so a
     result cannot state a number the quoted span does not hold.

Sources come from the JSON's "source": "text" is page-marked text (lines "===== PAGE n =====", or form
feeds between pages as pdftotext writes them); "pdf" is the PDF, read with PyMuPDF. Each is a path
relative to the project folder (the folder that holds papers/; for a JSON outside a papers/ folder, the
JSON's own folder), or an http(s) URL downloaded once into a cache ($CREATE_SLIDES_CACHE, else
$XDG_CACHE_HOME/create-slides or ~/.cache/create-slides, else the temp folder when those are not
writable). Text is preferred when both are given. `text` writes the page-marked form,
with a first line "SOURCE: <pdf or URL>" and without control codes (PyMuPDF keeps the codes 0 and 1 of
TeX's large parentheses), so numtrace.py reads the file as a source.

Prints "QUOTES OK <name>: n checked" or one line per problem and "QUOTES FAIL <name>"; exits 0 when all
pass, 1 on a failed quote, 2 on a missing or unreadable source.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import unicodedata
import urllib.request
from pathlib import Path

PAGE_MARK = re.compile(r"^=+ *PAGE (\d+) *=+ *$", re.M)
NUMBER = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?(?![\w])")
MIN_QUOTE = 12
CONTROL = re.compile(r"[\x00-\x08\x0b\x0e-\x1f]")  # control codes PyMuPDF leaves (TeX's large parentheses are 0, 1)


class SourceError(Exception):
    """A source that cannot be found, downloaded or read."""


def norm(s: str) -> str:
    """Letters and digits only, lower case, after NFKC."""
    return "".join(ch for ch in unicodedata.normalize("NFKC", s).lower() if ch.isalnum())


def numbers(s: str) -> set:
    """The numbers in a text, as floats: '1,000' -> 1000.0, '0.10' -> 0.1, '14%' -> 14.0."""
    return {float(m[1].replace(",", "") + (m[2] or "")) for m in NUMBER.finditer(s)}


def cache_dir() -> Path:
    """Where downloads go: $CREATE_SLIDES_CACHE, else $XDG_CACHE_HOME or ~/.cache, else the temp folder."""
    if os.environ.get("CREATE_SLIDES_CACHE"):
        d = Path(os.environ["CREATE_SLIDES_CACHE"])
        d.mkdir(parents=True, exist_ok=True)
        return d
    first = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "create-slides"
    try:
        first.mkdir(parents=True, exist_ok=True)
        if os.access(first, os.W_OK):
            return first
    except OSError:
        pass
    tmp = Path(tempfile.gettempdir()) / "create-slides-cache"
    try:
        tmp.mkdir(parents=True, exist_ok=True)
    except OSError:
        raise SourceError(f"no writable cache folder ({first}, {tmp}): set CREATE_SLIDES_CACHE to one")
    print(f"note: {first} is not writable; downloads go to {tmp}", file=sys.stderr)
    return tmp


def fetch(ref: str, base: Path = Path(".")) -> Path:
    """A local path for a source: the path itself (relative to base) or a cached download of a URL."""
    if re.match(r"https?://", ref):
        name = re.sub(r"[^A-Za-z0-9._-]+", "_", ref.rstrip("/").rsplit("/", 1)[-1])[:60] or "source"
        out = cache_dir() / f"{hashlib.sha1(ref.encode()).hexdigest()[:12]}-{name}"
        if not out.is_file():
            req = urllib.request.Request(ref, headers={"User-Agent": "create-slides quotecheck"})
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    data = r.read()
            except OSError as e:
                raise SourceError(f"cannot download {ref}: {e}")
            out.write_bytes(data)
        return out
    p = (base / ref) if not Path(ref).is_absolute() else Path(ref)
    if not p.is_file():
        raise SourceError(f"source file not found: {p}")
    return p


def project_of(json_path: Path) -> Path:
    """The folder that paths in a paper JSON are relative to: the parent of papers/, else the JSON's folder."""
    parent = json_path.resolve().parent
    return parent.parent if parent.name == "papers" else parent


def is_pdf(path: Path) -> bool:
    with open(path, "rb") as f:
        return f.read(5) == b"%PDF-"


def pdf_pages(path: Path) -> dict:
    try:
        import pymupdf
    except ImportError:
        raise SourceError("reading a PDF needs PyMuPDF (pip install pymupdf, or run scripts/setup.sh)")
    try:
        return {i: pg.get_text() for i, pg in enumerate(pymupdf.open(path), 1)}
    except Exception as e:  # PyMuPDF raises its own error types for damaged files
        raise SourceError(f"cannot read PDF {path}: {e}")


def text_pages(path: Path) -> dict:
    t = CONTROL.sub("", path.read_text(encoding="utf-8", errors="replace"))
    parts = PAGE_MARK.split(t)
    if len(parts) > 1:
        return {int(parts[i]): parts[i + 1] for i in range(1, len(parts) - 1, 2)}
    if "\f" in t:
        return {i: p for i, p in enumerate(t.split("\f"), 1) if p.strip() or i == 1}
    raise SourceError(f"{path} has no page marks ('===== PAGE n =====' lines or form feeds); "
                      "write it with: quotecheck.py text <pdf> --out <file>")


def load_pages(ref: str, base: Path = Path(".")) -> dict:
    """page number -> raw text, from a page-marked text file or a PDF (path or URL)."""
    path = fetch(ref, base)
    return pdf_pages(path) if is_pdf(path) else text_pages(path)


def paper_pages(paper: dict, base: Path) -> tuple:
    """(page -> normalised text, the source used) for a paper JSON's "source"."""
    src = paper.get("source") or {}
    refs = [src[k] for k in ("text", "pdf") if src.get(k)]
    if not refs:
        raise SourceError('no "source" with "text" or "pdf" to check quotes against')
    errors = []
    for ref in refs:
        try:
            return {k: norm(v) for k, v in load_pages(ref, base).items()}, ref
        except SourceError as e:
            errors.append(str(e))
    raise SourceError("; ".join(errors))


def find_quote(quote: str, page: int, pages: dict) -> tuple:
    """(passes, message or ''): the quote on page +- 1, as described in the module docstring."""
    q = norm(quote)
    if len(q) < MIN_QUOTE:
        return False, f"quote too short to check ({len(q)} letters and digits; at least {MIN_QUOTE})"
    here, before, after = pages.get(page, ""), pages.get(page - 1, ""), pages.get(page + 1, "")
    if q in here:
        return True, ""
    for k, text in ((page - 1, before), (page + 1, after)):
        if q in text:
            return True, f"found on p.{k}, cited p.{page}: cite p.{k}"
    if q in here + after or q in before + here:
        return True, ""                 # runs across the page break
    where = sorted(k for k, v in pages.items() if q in v)
    return False, (f"not on p.{page} or its neighbours" +
                   (f"; it is on p.{', p.'.join(map(str, where))}" if where else "; not found in the source"))


def check_paper(paper: dict, base: Path) -> tuple:
    """(errors, notes, number of quotes checked) for one paper JSON."""
    try:
        pages, _ = paper_pages(paper, base)
    except SourceError as e:
        return [str(e)], [], 0
    errors, notes, n = [], [], 0
    items = [(f"results[{i}]", r) for i, r in enumerate(paper.get("results") or [])]
    cert = paper.get("certifies") or {}
    if cert.get("quote"):
        items.append(("certifies", cert))
    for name, item in items:
        quote, page = item.get("quote", ""), item.get("page")
        if not isinstance(page, int):
            errors.append(f"{name}.page missing or not a whole number")
            continue
        n += 1
        ok, msg = find_quote(quote, page, pages)
        if not ok:
            errors.append(f"{name}.quote {msg}")
        elif msg:
            notes.append(f"{name}.quote {msg}")
        if name.startswith("results"):
            missing = sorted(numbers(item.get("text", "")) - numbers(quote))
            if missing:
                errors.append(f"{name}.text states {', '.join(f'{x:g}' for x in missing)}, which its quote "
                              "does not hold: quote the span with the number, or move a derived number to the notes")
    return errors, notes, n


def cmd_text(a) -> int:
    path = fetch(a.pdf)
    if not is_pdf(path):
        raise SourceError(f"{a.pdf} is not a PDF")
    pages = pdf_pages(path)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"SOURCE: {a.pdf}\n")
        for k, t in pages.items():
            f.write(f"\n===== PAGE {k} =====\n{CONTROL.sub('', t).rstrip()}\n")
    print(f"wrote {out} ({len(pages)} pages)")
    return 0


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    try:
        if argv and argv[0] == "text":
            p = argparse.ArgumentParser(prog="quotecheck.py text")
            p.add_argument("pdf", help="PDF path or URL")
            p.add_argument("--out", required=True, help="page-marked text file to write")
            return cmd_text(p.parse_args(argv[1:]))
        p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
        p.add_argument("papers", nargs="*", help="paper JSON files")
        p.add_argument("--source", help="check one quote: a PDF or page-marked text (path or URL)")
        p.add_argument("--page", type=int, help="the page the quote is cited on (with --source)")
        p.add_argument("quote", nargs="?", default=None, help=argparse.SUPPRESS)
        a = p.parse_args(argv)
        if a.source:
            quote = a.quote or (a.papers[0] if a.papers else "")
            if not quote or a.page is None:
                p.error('--source needs --page N and the quote: --source X --page N "quote"')
            pages = {k: norm(v) for k, v in load_pages(a.source).items()}
            ok, msg = find_quote(quote, a.page, pages)
            print(("QUOTE OK" if ok else "QUOTE FAIL") + (f": {msg}" if msg else ""))
            return 0 if ok else 1
        if not a.papers:
            p.error("give paper JSON files, or --source")
        rc = 0
        for f in a.papers:
            path = Path(f)
            try:
                paper = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as e:
                print(f"QUOTES FAIL {path.name}: cannot read the JSON: {e}")
                rc = max(rc, 2)
                continue
            errors, notes, n = check_paper(paper, project_of(path))
            for m in notes:
                print(f"  note: {m}")
            for m in errors:
                print(f"  {m}")
            print(f"QUOTES OK {path.name}: {n} checked" if not errors else f"QUOTES FAIL {path.name}")
            rc = max(rc, 1 if errors else 0)
        return rc
    except SourceError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
