"""explainer.py: build a paper-explainer deck, two slides per paper, from one JSON file per paper.

    python3 explainer.py new   <project> --title "T"                     start a project
    python3 explainer.py add   <project> <key> --pdf <path|URL> [--section S]   start one paper
    python3 explainer.py check <project> [key ...] [--no-quotes]         validate, quote-check, render
    python3 explainer.py build <project> [--no-quotes] [--sheet]         assemble, check, export the PDF

A project folder holds explainer.json (the deck: title, label, subtitle, context, sections, glossary,
callout label, optional footer and paper order), papers/<key>.json (one paper each; files starting
with "_" are skipped), figs/ (figure crops, from figcrop.py) and sources/ (page-marked texts and any
local PDFs). Paths inside a paper JSON are relative to the project folder. The schema, limits and
workflow are in references/paper-explainer.md. Output goes to <project>/build (or --out): check/ for
previews, deck/ for the assembled deck, an ordinary deck folder that deck.py can rebuild; edit the
JSON and rebuild rather than editing deck/.

The deck: cover, how to read, contents (linked, as many pages as needed), then per section a divider
and each paper's two slides, built from templates 17 paper-idea and 18 paper-method. Papers follow
the order of explainer.json "papers" when given, else section order, then the year in their venue,
then short name. Every contents row links to its slide; every paper slide links back to the contents.

check, per paper: (1) fields, types, counts and length limits; (2) every $math$ typesets and the
formula fits its panel; (3) the quotes, against the paper (quotecheck.py); (4) both slides rendered in
headless Chrome: a region that overflows (in px, lines and characters to cut), an element over its line
limit, and deck.py's checks (R7 collisions, text past its box, the footer band, type under 24 px, one-word
last lines).
Previews: <out>/check/<key>-1.png and <key>-2.png. Prints CHECK OK <key> or CHECK FAIL <key>.

build: all of check for every paper, then deck.py pdf (images frozen at their screen size, then
pdfcheck.py on the PDF), then a link check on the PDF: every contents row lands on its planned page,
every paper slide links back to the contents and shows its short name. --sheet also renders all slides
and writes <out>/contact-sheet.png. Exits 0 only when every check passes; 1 on failed checks; 2 on
errors that stop the run.
"""
import argparse
import html
import importlib.util
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
import deck as D  # noqa: E402  (sibling scripts: the deck engine, math and quotes)
import mathsvg  # noqa: E402
import quotecheck as Q  # noqa: E402

THEME = "technical-swiss"
TEMPLATES = SCRIPTS.parent / "templates" / THEME / "slides"
IDEA, METHOD = "17-paper-idea.html", "18-paper-method.html"
EQ_PX, FORMULA_MAX_PX = 48, 812      # template 18: --t-eq, and the formula panel's inner width (860 - 2 x 24)
FIG_MAX_PX = 1720                    # figures are stored at most twice their largest display width
CONTENTS_ROWS = 12                   # rows per contents column (two columns a page)

LIMITS = {"short": 24, "title": 110, "venue": 40, "arxiv": 20, "tag": 28, "eyebrow": 80, "problem": 180,
          "idea": 110, "caption": 120, "takeaway": 190, "finding": 55, "method": 110, "reads": 110,
          "measures": 70, "event": 90, "guarantee": 60, "level": 60, "assumes": 70, "result": 110, "limits": 110,
          "for_us": 170, "authors_face": 60}
COUNTS = {"idea": (2, 3), "method": (2, 3), "measures": (1, 2), "results": (2, 3), "limits": (1, 2)}
CONFIG_LIMITS = {"title": 60, "label": 30, "subtitle": 90, "context": 110, "section": 40, "note": 130,
                 "term": 24, "meaning": 90, "callout_label": 16}
PLACEHOLDER = re.compile(r"\[[^\]]*\]")
MATH = re.compile(r"(?<!\\)\$(.+?)(?<!\\)\$")

# Injected with deck.py's checker: per slide, how far each data-fit region's content runs past the
# region, and how many lines each data-lines element takes.
MEASURE = r"""<script>
(function(){
function run(){
  const out=[];
  document.querySelectorAll('.slide > section').forEach((sec,i)=>{
    const rep={index:i+1,id:sec.id,regions:[],lines:[]};
    sec.querySelectorAll('[data-fit]').forEach(r=>{
      const b=r.getBoundingClientRect(); let last=b.top;
      for(const c of r.children){const cr=c.getBoundingClientRect(); if(cr.height>0) last=Math.max(last,cr.bottom);}
      const t=r.querySelector('li,p:not(.kicker)'), cs=t?getComputedStyle(t):null;
      rep.regions.push({name:r.dataset.fit,over:Math.round(last-b.bottom),height:Math.round(b.height),
        line:cs?parseFloat(cs.lineHeight):36,cpl:cs?Math.round(b.width/(0.5*parseFloat(cs.fontSize))):58});
    });
    sec.querySelectorAll('[data-lines]').forEach(e=>{
      const slots=[e,...e.querySelectorAll('[data-slot]')].map(x=>x.dataset.slot).filter(Boolean);
      const lh=parseFloat(getComputedStyle(e).lineHeight);
      rep.lines.push({slots:slots,max:+e.dataset.lines,lines:Math.round(e.getBoundingClientRect().height/lh)});
    });
    out.push(rep);
  });
  const pre=document.createElement('pre'); pre.id='__expl_fit'; pre.textContent=JSON.stringify(out);
  document.body.appendChild(pre);
}
window.addEventListener('load',()=>document.fonts.ready.then(()=>setTimeout(run,60)));
})();
</script>"""


class ExplainerError(Exception):
    """A user-facing error that stops the run."""


# ---------------------------------------------------------------- text

def vis_len(text: str) -> int:
    """Characters as they will show: a $math$ span counts its visible symbols, not its TeX."""
    def m(mt):
        t = re.sub(r"\\[A-Za-z]+", "x", mt[1])
        return "x" * max(1, len(re.sub(r"[{}^_\\\s]", "", t)))
    return len(MATH.sub(m, text))


BIND = re.compile(r" ([=≤≥<>±×≈−]) ")
REF = re.compile(r"\b(Fig|Figs|Eq|Eqs|Prop|Thm|Sec|Tab|Def|Alg|App|Cor|Lem|p|pp|Table|Figure|Theorem|"
                 r"Proposition|Section|Lemma|Corollary|Algorithm|Appendix|Claim)(\.?) (?=[\dA-Z§(])")


def rich(text: str) -> str:
    """Escape text; $TeX$ becomes <span class="math">, which deck.py typesets. Spaces around = ≤ ≥ < > ± × ≈ −
    become non-breaking, so "n = 400" never breaks at the sign, nor "Prop. 1" or "Table 2" after the word."""
    def bind(t):
        return REF.sub(lambda m: m[1] + m[2] + "\u00a0", BIND.sub("\u00a0\\1\u00a0", t))
    parts = MATH.split(text)
    return "".join(f'<span class="math">{html.escape(p)}</span>' if i % 2 else
                   html.escape(bind(p)).replace("\\$", "$") for i, p in enumerate(parts))


def plain(text: str) -> str:
    """Text without math markup, for alt text and notes."""
    return MATH.sub(lambda m: m[1], text)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "x"


def year(venue: str) -> int:
    m = re.search(r"\b(19|20)\d\d\b", venue)
    return int(m[0]) if m else 9999


# ---------------------------------------------------------------- template slots

VOID = {"img", "br", "hr", "input", "meta", "link"}


def _span(src: str, name: str) -> tuple:
    """(start, inner start, inner end, end) of the element with data-slot="name"."""
    m = re.search(r'<(\w+)\b[^>]*\sdata-slot="%s"[^>]*>' % re.escape(name), src)
    if not m:
        raise ExplainerError(f'template has no element with data-slot="{name}"')
    tag = m[1].lower()
    if tag in VOID:
        return m.start(), m.end(), m.end(), m.end()
    depth = 1
    for t in re.finditer(r"<(/?)%s\b[^>]*?(/?)>" % tag, src[m.end():], re.I):
        depth += -1 if t[1] else (0 if t[2] else 1)
        if depth == 0:
            return m.start(), m.end(), m.end() + t.start(), m.end() + t.end()
    raise ExplainerError(f'template: <{tag} data-slot="{name}"> is not closed')


def fill(src: str, name: str, inner: str) -> str:
    s, i, j, e = _span(src, name)
    return src[:i] + inner + src[j:]


def drop(src: str, name: str) -> str:
    """Remove the element; when it starts its own line, remove that line's indent and newline too."""
    s, _, _, e = _span(src, name)
    line = src.rfind("\n", 0, s) + 1
    if not src[line:s].strip():
        s = line
        e += 1 if src[e:e + 1] == "\n" else 0
    return src[:s] + src[e:]


def set_attr(src: str, name: str, attr: str, value: str) -> str:
    s, i, _, _ = _span(src, name)
    tag = src[s:i]
    new = re.sub(r'\s%s="[^"]*"' % attr, f' {attr}="{html.escape(value, quote=True)}"', tag, count=1)
    if new == tag:
        new = tag[:-1].rstrip("/").rstrip() + f' {attr}="{html.escape(value, quote=True)}">'
    return src[:s] + new + src[i:]


def fill_list(src: str, name: str, items: list) -> str:
    """Repeat the list's first <li> once per item: a str fills the <li>, a dict fills its sub-slots."""
    s, i, j, e = _span(src, name)
    inner = src[i:j]
    m = re.search(r"<li\b", inner)
    if not m:
        raise ExplainerError(f'template list "{name}" has no <li> to repeat')
    k, depth = m.start(), 0
    for t in re.finditer(r"<(/?)li\b[^>]*>", inner[k:]):
        depth += -1 if t[1] else 1
        if depth == 0:
            pattern = inner[k:k + t.end()]
            break
    else:
        raise ExplainerError(f'template list "{name}": its first <li> is not closed')
    indent = re.search(r"\n([ \t]*)<li", inner)
    sep = "\n" + (indent[1] if indent else "")
    out = []
    for it in items:
        if isinstance(it, dict):
            li = pattern
            for slot, val in it.items():
                li = fill(li, slot, val)
        else:
            li = re.sub(r"^(<li\b[^>]*>).*(</li>)$", lambda mm: mm[1] + it + mm[2], pattern, flags=re.S)
        out.append(li)
    end = re.search(r"\n[ \t]*$", inner)
    return src[:i] + sep + sep.join(out) + (end[0] if end else "") + src[j:]


def template(name: str) -> str:
    """A template without its leading comment."""
    src = (TEMPLATES / name).read_text(encoding="utf-8")
    return re.sub(r"^\s*<!--.*?-->\s*", "", src, count=1, flags=re.S)


# ---------------------------------------------------------------- loading and validation

def load_config(project: Path, strict: bool = True) -> dict:
    """explainer.json with defaults filled in; strict also refuses fields still holding a [placeholder]."""
    path = project / "explainer.json"
    if not path.is_file():
        raise ExplainerError(f"{path} not found (start a project with: explainer.py new {project} --title ...)")
    try:
        cfg = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as e:
        raise ExplainerError(f"{path}: {e}")
    cfg.setdefault("label", "Paper explainer")
    cfg.setdefault("callout_label", "For us")
    cfg.setdefault("glossary", [])
    cfg.setdefault("show_authors", False)
    errs = []
    for k in ("title", "sections"):
        if not cfg.get(k):
            errs.append(f"missing {k}")
    for k in ("title", "label", "subtitle", "context", "callout_label"):
        if k in cfg and len(cfg[k]) > CONFIG_LIMITS[k]:
            errs.append(f"{k} is {len(cfg[k])} characters (max {CONFIG_LIMITS[k]})")
    for s in cfg.get("sections", []):
        if not isinstance(s, dict) or "name" not in s:
            errs.append('each section is {"name": ..., "note": ...}')
            continue
        if len(s["name"]) > CONFIG_LIMITS["section"]:
            errs.append(f"section name {s['name']!r} is over {CONFIG_LIMITS['section']} characters")
        if len(s.get("note", "")) > CONFIG_LIMITS["note"]:
            errs.append(f"section {s['name']!r}: note over {CONFIG_LIMITS['note']} characters")
    if strict:
        texts = [cfg.get(k, "") for k in ("title", "label", "subtitle", "context", "callout_label")]
        texts += [x for s in cfg.get("sections", []) if isinstance(s, dict)
                  for x in (s.get("name", ""), s.get("note", ""))]
        errs += [f"{t!r} is still a placeholder" for t in texts
                 if isinstance(t, str) and PLACEHOLDER.fullmatch(t.strip())]
    if len(cfg["glossary"]) > 6:
        errs.append("glossary has more than 6 terms")
    for g in cfg["glossary"]:
        if not (isinstance(g, list) and len(g) == 2):
            errs.append('each glossary entry is ["term", "meaning"]')
        elif len(g[0]) > CONFIG_LIMITS["term"] or vis_len(g[1]) > CONFIG_LIMITS["meaning"]:
            errs.append(f"glossary {g[0]!r}: term over {CONFIG_LIMITS['term']} or meaning over "
                        f"{CONFIG_LIMITS['meaning']} characters")
    if errs:
        raise ExplainerError(f"{path}: " + "; ".join(errs))
    return cfg


def load_papers(project: Path) -> dict:
    out = {}
    for f in sorted((project / "papers").glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            p = json.loads(f.read_text(encoding="utf-8"))
        except ValueError as e:
            raise ExplainerError(f"{f}: {e}")
        if p.get("key") != f.stem:
            raise ExplainerError(f'{f}: "key" must equal the file name ({f.stem!r})')
        out[f.stem] = p
    return out


def validate(p: dict, cfg: dict, project: Path) -> list:
    """Schema, counts, limits, placeholders, sections, the figure file and the math."""
    errs = []
    need = ["key", "short", "title", "venue", "source", "section", "problem", "idea", "takeaway", "finding",
            "method", "measures", "certifies", "results", "limits", "for_us"]
    errs += [f"missing field {k}" for k in need if k not in p]
    if errs:
        return errs
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,39}", p["key"]):
        errs.append("key: letters, digits, - and _ only, at most 40")

    def text(name, val, limit):
        if not isinstance(val, str) or not val.strip():
            errs.append(f"{name} must be a non-empty string")
        elif PLACEHOLDER.fullmatch(val.strip()):
            errs.append(f"{name} is still a placeholder")
        elif vis_len(val) > limit:
            errs.append(f"{name} is {vis_len(val)} characters (max {limit})")

    for k in ("short", "title", "venue", "problem", "takeaway", "finding", "for_us"):
        text(k, p[k], LIMITS[k])
    if p.get("arxiv"):
        text("arxiv", p["arxiv"], LIMITS["arxiv"])
    tags = p.get("tags", [])
    if not isinstance(tags, list) or len(tags) > 2:
        errs.append("tags: a list of at most 2")
    else:
        for i, t in enumerate(tags):
            text(f"tags[{i}]", t, LIMITS["tag"])
    if isinstance(tags, list) and len(eyebrow(p)) > LIMITS["eyebrow"]:
        errs.append(f"section and tags together are {len(eyebrow(p))} characters (max {LIMITS['eyebrow']})")
    for k, (lo, hi) in COUNTS.items():
        xs = p[k]
        if not isinstance(xs, list) or not lo <= len(xs) <= hi:
            errs.append(f"{k}: {lo}-{hi} items")
            continue
        for i, x in enumerate(xs):
            if k == "results":
                if not isinstance(x, dict):
                    errs.append(f"results[{i}] must be {{text, quote, page}}")
                    continue
                text(f"results[{i}].text", x.get("text"), LIMITS["result"])
                if not isinstance(x.get("page"), int) or x["page"] < 1:
                    errs.append(f"results[{i}].page must be a page number (1 = the PDF's first page)")
                if not x.get("quote"):
                    errs.append(f"results[{i}].quote missing")
            else:
                text(f"{k}[{i}]", x, LIMITS[k])
    c = p["certifies"]
    if c is not None and not isinstance(c, dict):
        errs.append("certifies must be {event, guarantee, level, assumes}, or null for no formal guarantee")
    elif c:
        for k in ("event", "guarantee", "level", "assumes"):
            text(f"certifies.{k}", c.get(k), LIMITS[k])
        if c.get("quote") and (not isinstance(c.get("page"), int) or c["page"] < 1):
            errs.append("certifies.page must be a page number when certifies.quote is given")
    if p["section"] not in [s["name"] for s in cfg["sections"]]:
        errs.append(f"section {p['section']!r} is not one of {[s['name'] for s in cfg['sections']]}")
    src = p["source"]
    if not isinstance(src, dict) or not (src.get("pdf") or src.get("text")):
        errs.append('source must be {"pdf": path or URL, "text": path or URL} (at least one)')
    fig = p.get("figure")
    if fig is not None:
        if not isinstance(fig, dict) or not fig.get("file") or not isinstance(fig.get("page"), int) \
                or fig["page"] < 1:
            errs.append("figure must be {file, page, caption} (box optional)")
        else:
            if not (project / fig["file"]).is_file():
                errs.append(f"figure file {fig['file']} not found (crop it with figcrop.py)")
            text("figure.caption", fig.get("caption"), LIMITS["caption"])
    f = p.get("formula")
    if f is not None:
        if not isinstance(f, dict) or not f.get("tex"):
            errs.append('formula must be {tex, reads}; delete "formula" when the paper has none')
        else:
            text("formula.reads", f.get("reads"), LIMITS["reads"])
    if cfg["show_authors"] and len(p.get("authors", "")) > LIMITS["authors_face"]:
        errs.append(f"authors over {LIMITS['authors_face']} characters (show_authors puts them on the slide)")
    if not errs:
        errs += math_errors(p, cfg)
    return errs


def math_errors(p: dict, cfg: dict) -> list:
    fontset = cfg.get("math_fontset", "cm")
    texts = [p["problem"], p["takeaway"], p["finding"], p["for_us"]] + p["idea"] + p["method"] + p["measures"] + \
        p["limits"] + [r["text"] for r in p["results"]] + \
        [v for k, v in (p["certifies"] or {}).items() if k in ("event", "guarantee", "level", "assumes")]
    if p.get("figure"):
        texts.append(p["figure"]["caption"])
    if p.get("formula"):
        texts.append(p["formula"]["reads"])
    errs = []
    for t in texts:
        for tex in MATH.findall(t):
            try:
                mathsvg.tex_to_svg(tex, fontset)
            except mathsvg.MathError as e:
                errs.append(f"math in {plain(t)[:40]!r}...: {e}")
    if p.get("formula"):
        try:
            svg = mathsvg.tex_to_svg(p["formula"]["tex"], fontset)
            width = float(re.search(r"width:([\d.]+)em", svg)[1]) * EQ_PX
            if width > FORMULA_MAX_PX:
                errs.append(f"formula is {width:.0f} px wide at {EQ_PX} px; its panel holds {FORMULA_MAX_PX}: "
                            "shorten it (move a consequence into the reading)")
        except mathsvg.MathError as e:
            errs.append(f"formula: {e}")
    return errs


# ---------------------------------------------------------------- slides

def eyebrow(p: dict) -> str:
    return " · ".join([p["section"]] + list(p.get("tags", [])))


def figure_size(path: Path, box: str) -> tuple:
    from PIL import Image
    bw, bh = map(int, box.split("x"))
    with Image.open(path) as im:
        w, h = im.size
    s = min(bw / w, bh / h)
    return round(w * s), round(h * s)


def notes_idea(p: dict, cfg: dict) -> str:
    src = p["source"]
    cite = ". ".join(x.rstrip(".") for x in [p.get("authors", ""), p.get("full_title", p["title"]), p["venue"],
                                             f"arXiv {p['arxiv']}" if p.get("arxiv") else ""] if x)
    lines = [f"Source: {cite}.", f"PDF: {src.get('pdf', '-')}; text: {src.get('text', '-')}"]
    if p.get("url"):
        lines.append(f"Page: {p['url']}")
    fig = p.get("figure")
    if fig:
        box = f", box {fig['box']} (PDF points)" if fig.get("box") else ""
        lines.append(f"Figure: p.{fig['page']}{box}, file {fig['file']}.")
    lines.append(f"Built by explainer.py from papers/{p['key']}.json.")
    return "<br>".join(html.escape(x) for x in lines)


def notes_method(p: dict) -> str:
    lines = ["Each result's quoted span, as checked against the paper:"]
    lines += [f"p.{r['page']}: “{r['quote']}”" for r in p["results"]]
    c = p["certifies"] or {}
    if c.get("quote"):
        lines.append(f"What it certifies, p.{c['page']}: “{c['quote']}”")
    if p.get("notes"):
        lines.append(p["notes"])
    return "<br>".join(html.escape(x) for x in lines)


def paper_slides(p: dict, cfg: dict, fig_src: tuple) -> tuple:
    """The two slides of one paper, from templates 17 and 18; fig_src is (src in the deck, file) or ()."""
    a = template(IDEA)
    a = set_attr(a, "section", "id", f"p-{p['key']}")
    a = fill(a, "eyebrow", html.escape(eyebrow(p)))
    a = fill(a, "title", rich(p["title"]))
    if p["short"].casefold() == p["title"].casefold():
        a = drop(drop(a, "short"), "short-sep")
    else:
        a = fill(a, "short", html.escape(p["short"]))
    cite = [p["venue"]] + ([f"arXiv {p['arxiv']}"] if p.get("arxiv") else [])
    if cfg["show_authors"] and p.get("authors"):
        cite.insert(0, p["authors"])
    a = fill(a, "cite", html.escape(" · ".join(cite)))
    a = fill(a, "problem", rich(p["problem"]))
    a = fill_list(a, "idea", [rich(x) for x in p["idea"]])
    fig = p.get("figure")
    if fig and fig_src:
        tag = a[_span(a, "figure-img")[0]:_span(a, "figure-img")[1]]
        box = re.search(r'data-box%s="(\d+x\d+)"' % ("-1" if len(p["title"]) <= 40 else ""), tag) or \
            re.search(r'data-box="(\d+x\d+)"', tag)
        if not box:
            raise ExplainerError("template 17: the figure <img> has no data-box")
        w, h = figure_size(Path(fig_src[1]), box[1])
        a = set_attr(a, "figure-img", "src", fig_src[0])
        a = set_attr(a, "figure-img", "alt", plain(fig["caption"]))
        a = set_attr(a, "figure-img", "style", f"width:{w}px;height:{h}px;flex:none")
        a = fill(a, "caption", rich(fig["caption"]))
        a = fill(a, "figure-page", f"p.{fig['page']}")
    else:
        a = drop(a, "figure")
        a = set_attr(a, "text-col", "class", "c8 stack")
    a = fill(a, "takeaway", rich(p["takeaway"]))
    a = fill(a, "notes", notes_idea(p, cfg))

    b = template(METHOD)
    b = set_attr(b, "section", "id", f"p-{p['key']}-2")
    b = fill(b, "short", html.escape(p["short"]))
    b = fill(b, "finding", rich(p["finding"]))
    b = fill_list(b, "method", [rich(x) for x in p["method"]])
    if p.get("formula"):
        b = fill(b, "tex", html.escape(" ".join(p["formula"]["tex"].split())))
        b = fill(b, "reads", rich(p["formula"]["reads"]))
    else:
        b = drop(b, "formula")
    b = fill_list(b, "measures", [rich(x) for x in p["measures"]])
    if p["certifies"]:
        for k in ("event", "guarantee", "level", "assumes"):
            b = fill(b, k, rich(p["certifies"][k]))
    else:
        b = drop(b, "certifies")
    b = fill_list(b, "results", [{"text": rich(r["text"]), "page": f"p.{r['page']}"} for r in p["results"]])
    b = fill_list(b, "limits", [rich(x) for x in p["limits"]])
    b = fill(b, "callout", html.escape(cfg["callout_label"].rstrip(".") + "."))
    b = fill(b, "for_us", rich(p["for_us"]))
    b = fill(b, "notes", notes_method(p))
    return a.strip() + "\n", b.strip() + "\n"


TOC_LINK = '<a class="meta blue" href="#contents" style="text-decoration:none;flex:none">Contents ↑</a>'


def topline(kicker: str, link: str = TOC_LINK) -> str:
    return (f'<div class="row" style="justify-content:space-between;align-items:baseline">'
            f'<p class="kicker">{kicker}</p>{link}</div>')


def cover_slide(cfg: dict, n_papers: int, n_sections: int, command: str) -> str:
    context = cfg.get("context") or (f"{n_papers} papers in {n_sections} section{'s' if n_sections > 1 else ''}, "
                                     "two slides each. Every result is quoted from its paper, with the page.")
    sub = (f'\n      <p class="lead" style="text-wrap:balance">{rich(cfg["subtitle"])}</p>'
           if cfg.get("subtitle") else "")
    return f"""<section class="cover" id="cover" data-nofooter>
  <p class="kicker">{html.escape(cfg['label'])}</p>
  <div class="row fill" style="align-items:flex-end">
    <div class="c9 stack">
      <h1 style="text-wrap:balance">{html.escape(cfg['title'])}</h1>{sub}
    </div>
  </div>
  <div class="row rule" style="justify-content:space-between;align-items:baseline">
    <p class="meta">{rich(context)}</p>
    <a class="meta blue" href="#contents" style="text-decoration:none;flex:none">Contents →</a>
  </div>
  <aside class="notes">Built with: {html.escape(command)}</aside>
</section>
"""


def howto_slide(cfg: dict) -> str:
    one = ["Problem: what goes wrong without the paper.", "Idea: the mechanism, in two or three steps.",
           "Figure: the paper's own, with its page.", "Takeaway: the sentence to remember."]
    two = ["Method, with its formula when it has one.",
           "What it certifies: the event the theorem bounds, the guarantee, its level and assumptions.",
           "Measures and results; each result carries its page.", "Limits, on the amber rule.",
           f"{cfg['callout_label'].rstrip('.')}: what the paper means for the reader's work."]

    def li(xs):
        return "".join(f"<li>{html.escape(x)}</li>" for x in xs)
    if cfg["glossary"]:
        terms = "".join(f'<li><strong>{html.escape(t)}:</strong> {rich(m)}</li>' for t, m in cfg["glossary"])
        third = (f'\n    <div class="c4 head rule2"><p class="kicker">Terms</p>'
                 f'<ul class="plain" style="gap:16px">{terms}</ul></div>')
        width = "c4"
    else:
        third, width = "", "c6"
    down = TOC_LINK.replace("\u2191", "\u2193")
    key = ("Blue text is a link. The amber rule marks limits. p.N is the page in the paper; the quote behind "
           "each result is in the speaker notes.")
    return f"""<section id="howto" style="--t-body:var(--t-cap)">
  <div class="head">
    {topline("How to read", down)}
    <h2>Two slides per paper: the idea, then how it works</h2>
  </div>
  <div class="row">
    <div class="{width} head rule2"><p class="kicker">Slide 1 · The idea</p>
      <ul class="dash">{li(one)}</ul></div>
    <div class="{width} head rule2"><p class="kicker">Slide 2 · How it works</p>
      <ul class="dash">{li(two)}</ul></div>{third}
  </div>
  <p class="meta rule" style="margin-top:auto">{html.escape(key)}</p>
  <aside class="notes">The eyebrow above each paper's title names its section and tags. Every result's quote is in the
  notes of the paper's second slide, checked against the paper by quotecheck.py.</aside>
</section>
"""


def paginate(entries: list) -> list:
    """Split contents rows into pages of two CONTENTS_ROWS columns. A section row never ends a page, and a
    page that starts inside a section repeats the section's row, marked continued."""
    per, pages, cur, last = 2 * CONTENTS_ROWS, [], [], None
    for e in entries:
        if cur and (len(cur) == per or (e[0] == "sec" and len(cur) == per - 1)):
            pages.append(cur)
            cur = [] if e[0] == "sec" else [("sec", last[1] + " (continued)", "", last[3], last[4])]
        last = e if e[0] == "sec" else last
        cur.append(e)
    return pages + [cur] if cur else pages


def contents_slides(chunks: list, n_papers: int, n_sections: int) -> list:
    """chunks: pages from paginate(), rows (kind, label, detail, page, anchor)."""
    out = []
    for n, chunk in enumerate(chunks, 1):
        cols = []
        for col in (chunk[:CONTENTS_ROWS], chunk[CONTENTS_ROWS:]):
            rows = []
            for kind, label, detail, page, anchor in col:
                if kind == "sec":
                    rows.append(f'<a class="row rule2" href="#{anchor}" style="color:inherit;text-decoration:none;'
                                f'padding:16px 0 8px;justify-content:space-between;align-items:baseline">'
                                f'<p class="kicker">{html.escape(label)}</p><p class="meta">{page:02d}</p></a>')
                else:
                    rows.append(f'<a class="row rule" href="#{anchor}" style="color:inherit;text-decoration:none;'
                                f'padding:8px 0;justify-content:space-between;align-items:baseline">'
                                f'<p><strong class="blue">{html.escape(label)}</strong>'
                                f' <span class="sec">· {html.escape(detail)}</span></p>'
                                f'<p class="meta">{page:02d}</p></a>')
            cols.append(f'<div class="c6 stack" style="gap:0">{"".join(rows)}</div>' if rows else "")
        sid = ' id="contents"' if n == 1 else ""
        part = f" · {n} of {len(chunks)}" if len(chunks) > 1 else ""
        link = ('<a class="meta blue" href="#howto" style="text-decoration:none;flex:none">How to read ↑</a>')
        title = (f"{n_papers} paper{'s' if n_papers != 1 else ''} in "
                 f"{n_sections} section{'s' if n_sections != 1 else ''}")
        out.append(f"""<section{sid} style="--t-body:var(--t-cap)">
  <div class="head">
    {topline("Contents" + part, link)}
    <h2>{title}</h2>
  </div>
  <div class="row">{"".join(cols)}</div>
</section>
""")
    return out


def divider_slide(cfg: dict, idx: int, sec: dict, papers: list, pages: dict) -> str:
    names = " · ".join(p["short"] for p in papers)
    if len(names) <= 100:
        links = " · ".join(f'<a class="blue" href="#p-{p["key"]}" style="text-decoration:none">'
                           f'{html.escape(p["short"])}</a>' for p in papers)
        line = f"{len(papers)} paper{'s' if len(papers) != 1 else ''}: {links}"
    else:
        first, last = pages[papers[0]["key"]], pages[papers[-1]["key"]] + 1
        line = f"{len(papers)} papers, pages {first:02d}–{last:02d}"
    note = f'\n      <p class="lead" style="text-wrap:balance">{rich(sec["note"])}</p>' if sec.get("note") else ""
    return f"""<section class="section" id="sec-{idx:02d}-{slug(sec['name'])}" data-nofooter>
  {topline(html.escape(cfg['label']))}
  <div class="row rule2" style="margin-top:auto">
    <h1 class="section-title c2 ter">{idx:02d}</h1>
    <div class="c10 stack">
      <h1 class="section-title">{html.escape(sec['name'])}</h1>{note}
    </div>
  </div>
  <p class="meta" style="margin-top:auto">{line}</p>
</section>
"""


def plan(cfg: dict, papers: dict) -> tuple:
    """The deck's order: [(section, [papers])], sections without papers left out."""
    if cfg.get("papers"):
        missing = [k for k in cfg["papers"] if k not in papers]
        if missing:
            raise ExplainerError(f'explainer.json "papers" lists {missing}, which have no papers/<key>.json')
        chosen = [papers[k] for k in cfg["papers"]]
    else:
        chosen = sorted(papers.values(), key=lambda p: (year(p["venue"]), p["short"].lower()))
    groups = []
    for sec in cfg["sections"]:
        ps = [p for p in chosen if p["section"] == sec["name"]]
        if ps:
            groups.append((sec, ps))
    return groups


def assemble(project: Path, cfg: dict, groups: list, out: Path, command: str) -> tuple:
    """Write the deck folder; return (deck dir, slide ids, planned pages)."""
    deck_dir = out / "deck"
    if deck_dir.exists():
        shutil.rmtree(deck_dir)
    (deck_dir / "slides").mkdir(parents=True)
    n_papers = sum(len(ps) for _, ps in groups)
    shape = []
    for _, ps in groups:                       # the rows' kinds alone fix the number of contents pages
        shape += [("sec", "", "", 0, "")] + [("paper", "", "", 0, "")] * len(ps)
    n_toc = len(paginate(shape))
    page = 3 + n_toc
    sec_page, paper_page = {}, {}
    for sec, ps in groups:
        sec_page[sec["name"]] = page
        page += 1
        for p in ps:
            paper_page[p["key"]] = page
            page += 2
    entries = []
    for i, (sec, ps) in enumerate(groups, 1):
        entries.append(("sec", f"{i:02d} · {sec['name']}", "", sec_page[sec["name"]],
                        f"sec-{i:02d}-{slug(sec['name'])}"))
        entries += [("paper", p["short"], p["venue"], paper_page[p["key"]], f"p-{p['key']}") for p in ps]
    slides = [("cover", cover_slide(cfg, n_papers, len(groups), command)), ("how-to-read", howto_slide(cfg))]
    toc = contents_slides(paginate(entries), n_papers, len(groups))
    assert len(toc) == n_toc
    slides += [(f"contents-{n}", s) for n, s in enumerate(toc, 1)]
    for i, (sec, ps) in enumerate(groups, 1):
        slides.append((f"section-{slug(sec['name'])}", divider_slide(cfg, i, sec, ps, paper_page)))
        for p in ps:
            pair = paper_slides(p, cfg, stage_figure(project, p, deck_dir))
            slides += zip((f"{p['key']}-1", f"{p['key']}-2"), pair)
    width = max(2, len(str(len(slides))))
    ids = []
    for n, (name, src) in enumerate(slides, 1):
        ids.append(f"{n:0{width}d}-{name}")
        (deck_dir / "slides" / f"{ids[-1]}.html").write_text(src, encoding="utf-8")
    deck = {"title": cfg["title"], "theme": THEME, "slides": ids}
    for k in ("footer", "math_fontset"):
        if cfg.get(k):
            deck[k] = cfg[k]
    (deck_dir / "deck.json").write_text(json.dumps(deck, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return deck_dir, ids, {"sections": sec_page, "papers": paper_page, "contents": list(range(3, 3 + n_toc)),
                           "entries": entries}


def stage_figure(project: Path, p: dict, deck_dir: Path) -> tuple:
    """Copy the figure into the deck's assets, at most FIG_MAX_PX wide; return (src in the deck, path)."""
    fig = p.get("figure")
    if not fig:
        return ()
    from PIL import Image
    src = project / fig["file"]
    ext = ".png" if src.suffix.lower() == ".png" else ".jpg"
    dst = deck_dir / "assets" / "figs" / f"{p['key']}{ext}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        if im.width > FIG_MAX_PX:
            im = im.resize((FIG_MAX_PX, round(im.height * FIG_MAX_PX / im.width)), Image.LANCZOS)
        if ext == ".png":
            im.save(dst, optimize=True)
        else:
            im.convert("RGB").save(dst, quality=88)
    return f"assets/figs/{dst.name}", str(dst)


# ---------------------------------------------------------------- rendering and checks

def chrome_args(a) -> argparse.Namespace:
    return argparse.Namespace(chrome=a.chrome, budget=a.budget)


def measure(deck_dir: Path, a) -> tuple:
    """Render the deck once with deck.py's checker and MEASURE; return (checker report, fit report)."""
    ns = argparse.Namespace(deck_dir=str(deck_dir), **vars(chrome_args(a)))
    try:
        deck, slides = D.cmd_build(ns, quiet=True)
        probe = deck_dir / "build" / "_measure.html"
        probe.write_text(D.page_html(deck, slides, fit=False, tail=D.CHECKER + MEASURE), encoding="utf-8")
        try:
            dom = D.chrome(ns, ["--dump-dom", probe.resolve().as_uri()], capture=True)
        finally:
            probe.unlink(missing_ok=True)
    except D.DeckError as e:
        raise ExplainerError(str(e))
    rep = re.search(r'<pre id="__ppt_report">(.*?)</pre>', dom, re.S)
    fit = re.search(r'<pre id="__expl_fit">(.*?)</pre>', dom, re.S)
    if not (rep and fit):
        raise ExplainerError("the render produced no report (Chrome did not finish; try a larger --budget)")
    return json.loads(html.unescape(rep[1])), json.loads(html.unescape(fit[1]))


def slide_problems(rep_slide: dict, fit_slide: dict) -> list:
    out = []
    for r in fit_slide["regions"]:
        if r["over"] > 2:
            lines = math.ceil(r["over"] / r["line"])
            out.append(f"{r['name']}: {r['over']} px too tall, about {lines} line{'s' if lines > 1 else ''} "
                       f"(~{lines * r['cpl']} characters) to cut or move to the notes")
    for ln in fit_slide["lines"]:
        if ln["lines"] > ln["max"]:
            name = " and ".join(x for x in ln["slots"] if x not in ("callout", "figure-page")) or "an element"
            out.append(f"{name} takes {ln['lines']} lines (at most {ln['max']})")
    for pr in rep_slide["problems"]:
        out.append(f"[{pr['kind']}] {pr['el']}: {pr['msg']}")
    return out


def run_deck(*args) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPTS / "deck.py"), *args], capture_output=True, text=True)


def render_pngs(deck_dir: Path, a) -> None:
    r = run_deck("png", str(deck_dir), *chrome_flags(a))
    if r.returncode:
        raise ExplainerError(f"deck.py png failed: {(r.stderr or r.stdout).strip()[-500:]}")


def chrome_flags(a) -> list:
    return (["--chrome", a.chrome] if a.chrome else []) + ["--budget", str(a.budget)]


def check_link_pdf(pdf: Path, ids: list, pages: dict, papers: dict) -> list:
    import pymupdf
    doc = pymupdf.open(pdf)
    errs = []
    if len(doc) != len(ids):
        errs.append(f"the PDF has {len(doc)} pages, the deck {len(ids)} slides")
        return errs
    targets = {}
    for i, pg in enumerate(doc, 1):
        targets[i] = [ln.get("page", -1) + 1 for ln in pg.get_links()
                      if ln.get("kind") in (pymupdf.LINK_GOTO, pymupdf.LINK_NAMED)]
    toc = pages["contents"]
    found = {t for n in toc for t in targets[n]}
    for kind, label, _, page, _ in pages["entries"]:
        if page not in found:
            errs.append(f"contents: no link lands on p.{page} ({label})")
    for key, page in pages["papers"].items():
        for n in (page, page + 1):
            if toc[0] not in targets[n]:
                errs.append(f"p.{n} ({key}): no link back to the contents")
            short = papers[key]["short"]
            if short.lower() not in doc[n - 1].get_text().lower():
                errs.append(f"p.{n}: short name {short!r} not on the page planned for {key}")
    if toc[0] not in targets[1]:
        errs.append("cover: no link to the contents")
    return errs


# ---------------------------------------------------------------- commands

def need(*modules) -> None:
    """Stop with one clear message when a library the command needs is missing."""
    names = {"matplotlib": "matplotlib", "PIL": "Pillow", "pymupdf": "PyMuPDF"}
    missing = [names[m] for m in modules if importlib.util.find_spec(m) is None]
    if missing:
        raise ExplainerError(f"this needs {', '.join(missing)}: pip install {' '.join(missing).lower()}, "
                             "or run scripts/setup.sh")


def out_dir(a, project: Path) -> Path:
    return Path(a.out) if a.out else project / "build"


def gather(a, project: Path, cfg: dict, papers: dict, keys: list) -> tuple:
    """Validate and quote-check the given papers: (key -> problems, keys whose fields are valid)."""
    res, valid = {}, []
    for k in keys:
        errs = validate(papers[k], cfg, project)
        if not errs:
            valid.append(k)
            if not a.no_quotes:
                qerr, notes, _ = Q.check_paper(papers[k], project)
                errs += qerr
                for n in notes:
                    print(f"  {k}: note: {n}")
        res[k] = errs
    return res, valid


def cmd_new(a) -> int:
    project = Path(a.project)
    if (project / "explainer.json").exists() and not a.force:
        raise ExplainerError(f"{project}/explainer.json exists; pass --force to overwrite")
    for d in ("papers", "figs", "sources"):
        (project / d).mkdir(parents=True, exist_ok=True)
    cfg = {"title": a.title, "label": "Paper explainer", "subtitle": "[One sentence: what the papers have in common]",
           "sections": [{"name": "[Section name]", "note": "[What this group of papers answers, <= 130 characters]"}],
           "glossary": [], "callout_label": "For us"}
    (project / "explainer.json").write_text(json.dumps(cfg, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {project}/explainer.json and papers/, figs/, sources/. Fill in explainer.json, then: "
          f"explainer.py add {project} <key> --pdf <path or URL>")
    return 0


PAPER_SKELETON = {
    "short": "[Short name]", "title": "[The paper's title, verbatim]", "authors": "[Authors as cited]",
    "venue": "[Venue year]", "arxiv": "", "section": "", "tags": [],
    "problem": "[What goes wrong without the paper]", "idea": ["[Step]", "[Step]"],
    "figure": {"file": "figs/KEY.jpg", "page": 0, "box": [], "caption": "[What to look at]"},
    "takeaway": "[The sentence to remember]", "finding": "[What the paper shows]",
    "method": ["[Step]", "[Step]"], "formula": {"tex": "", "reads": "[The formula in words]"},
    "measures": ["[Measure: definition]"],
    "certifies": {"event": "[Event the theorem bounds]", "guarantee": "[Type]", "level": "[Level, n]",
                  "assumes": "[What the guarantee needs]",
                  "quote": "", "page": 0},
    "results": [{"text": "[Result]", "quote": "[Verbatim span]", "page": 0},
                {"text": "[Result]", "quote": "[Verbatim span]", "page": 0}],
    "limits": ["[Limit]"], "for_us": "[What it means for the reader's work]", "notes": ""}


def cmd_add(a) -> int:
    project = Path(a.project)
    cfg = load_config(project, strict=False)
    path = project / "papers" / f"{a.key}.json"
    if path.exists() and not a.force:
        raise ExplainerError(f"{path} exists; pass --force to overwrite")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,39}", a.key):
        raise ExplainerError("key: letters, digits, - and _ only, at most 40 (e.g. ren23knowno)")
    txt = project / "sources" / f"{a.key}.txt"
    r = subprocess.run([sys.executable, str(SCRIPTS / "quotecheck.py"), "text", a.pdf, "--out", str(txt)],
                       capture_output=True, text=True)
    if r.returncode:
        raise ExplainerError(f"cannot read the PDF: {(r.stderr or r.stdout).strip()}")
    print(r.stdout.strip())
    paper = {"key": a.key, **PAPER_SKELETON}
    paper["source"] = {"pdf": a.pdf, "text": f"sources/{a.key}.txt"}
    paper["section"] = a.section or cfg["sections"][0]["name"]
    paper["figure"] = dict(paper["figure"], file=f"figs/{a.key}.jpg")
    path.write_text(json.dumps(paper, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {path}: fill every field from {txt} (references/paper-explainer.md), crop the figure with "
          f"figcrop.py, then: explainer.py check {project} {a.key}")
    return 0


def cmd_check(a) -> int:
    need("matplotlib", "PIL")
    project = Path(a.project)
    cfg = load_config(project)
    papers = load_papers(project)
    keys = a.keys or list(papers)
    unknown = [k for k in keys if k not in papers]
    if unknown:
        raise ExplainerError(f"no papers/<key>.json for {unknown}")
    if not keys:
        raise ExplainerError(f"no papers in {project / 'papers'}")
    res, good = gather(a, project, cfg, papers, keys)    # render every paper whose fields are valid
    out = out_dir(a, project) / "check"
    if good:
        cdir = out / "deck"
        if cdir.exists():
            shutil.rmtree(cdir)
        (cdir / "slides").mkdir(parents=True)
        ids = []
        for k in good:
            for n, src in enumerate(paper_slides(papers[k], cfg, stage_figure(project, papers[k], cdir)), 1):
                ids.append(f"{len(ids) + 1:03d}-{k}-{n}")
                (cdir / "slides" / f"{ids[-1]}.html").write_text(src, encoding="utf-8")
        deck = {"title": "explainer check", "theme": THEME, "slides": ids}
        if cfg.get("math_fontset"):
            deck["math_fontset"] = cfg["math_fontset"]
        (cdir / "deck.json").write_text(json.dumps(deck, indent=2), encoding="utf-8")
        rep, fit = measure(cdir, a)
        render_pngs(cdir, a)
        for i, sid in enumerate(ids):
            k, n = sid[4:].rsplit("-", 1)
            res[k] += [f"slide {n}: {m}" for m in slide_problems(rep["slides"][i], fit[i])]
            shutil.copy2(cdir / "build" / "png" / f"slide-{i + 1:02d}.png", out / f"{k}-{n}.png")
    for k in keys:
        print(f"CHECK OK {k}" if not res[k] else f"CHECK FAIL {k}:\n    " + "\n    ".join(res[k]))
    if good:
        print(f"previews: {out}/<key>-1.png and <key>-2.png; look at each")
    return 0 if all(not v for v in res.values()) else 1


def cmd_build(a) -> int:
    need("matplotlib", "PIL", "pymupdf")
    project = Path(a.project)
    cfg = load_config(project)
    papers = load_papers(project)
    groups = plan(cfg, papers)
    keys = [p["key"] for _, ps in groups for p in ps]
    if not keys:
        raise ExplainerError("no papers belong to the sections in explainer.json")
    skipped = sorted(set(papers) - set(keys))
    if skipped:
        print(f"note: not in the deck (section not listed, or not in \"papers\"): {', '.join(skipped)}")
    res, _ = gather(a, project, cfg, papers, keys)
    bad = {k: v for k, v in res.items() if v}
    if bad:
        for k, v in bad.items():
            print(f"CHECK FAIL {k}:\n    " + "\n    ".join(v))
        print("fix these (explainer.py check shows the slides), then build again")
        return 1
    out = out_dir(a, project)
    command = f"explainer.py build {project.resolve().name}"
    deck_dir, ids, pages = assemble(project, cfg, groups, out, command)
    print(f"assembled {deck_dir}: {len(ids)} slides ({len(keys)} papers, {len(groups)} sections)")
    rep, fit = measure(deck_dir, a)
    problems = []
    for i, sid in enumerate(ids):
        problems += [f"slide {i + 1:02d} {sid}: {m}" for m in slide_problems(rep["slides"][i], fit[i])]
    for f in rep["fonts_failed"]:
        problems.append(f"font failed to load: {f}")
    print("\n".join(problems) if problems else f"layout OK: {len(ids)} slides fit; no collisions")
    r = run_deck("pdf", str(deck_dir), *chrome_flags(a))
    print(r.stdout.rstrip())
    if r.returncode not in (0, 1):
        raise ExplainerError(f"deck.py pdf failed: {(r.stderr or r.stdout).strip()[-600:]}")
    pdf = deck_dir / "build" / f"{D.slug(cfg['title'])}.pdf"
    links = check_link_pdf(pdf, ids, pages, papers)
    print("\n".join(f"links: {e}" for e in links) if links else
          f"links OK: {len(pages['entries'])} contents rows land on their pages; every paper slide links back")
    final = out / pdf.name
    shutil.copy2(pdf, final)
    if a.sheet:
        render_pngs(deck_dir, a)
        s = subprocess.run([sys.executable, str(SCRIPTS / "contact_sheet.py"), str(deck_dir),
                            str(out / "contact-sheet.png")], capture_output=True, text=True)
        print(s.stdout.strip() or s.stderr.strip())
    ok = not problems and r.returncode == 0 and not links
    print(f"\n{'explainer OK' if ok else 'explainer FAILED'}: {final}")
    return 0 if ok else 1


def main(argv=None) -> int:
    sys.stdout.reconfigure(line_buffering=True)
    chromeopts = argparse.ArgumentParser(add_help=False)
    chromeopts.add_argument("--chrome", default="", help="path to Chrome/Chromium (else CHROME_PATH, PATH)")
    chromeopts.add_argument("--budget", type=int, default=8000, help="Chrome virtual-time budget in ms")
    chromeopts.add_argument("--out", default="", help="output folder (default <project>/build)")
    chromeopts.add_argument("--no-quotes", action="store_true", help="skip the quote check")
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new", help="start a project: explainer.json, papers/, figs/, sources/")
    n.add_argument("project")
    n.add_argument("--title", required=True)
    n.add_argument("--force", action="store_true")
    d = sub.add_parser("add", help="start one paper: page-marked text and a JSON skeleton")
    d.add_argument("project")
    d.add_argument("key", help="file name and anchor, e.g. ren23knowno (never shown on a slide)")
    d.add_argument("--pdf", required=True, help="the paper's PDF: path or URL")
    d.add_argument("--section", default="", help="its section (default: the first in explainer.json)")
    d.add_argument("--force", action="store_true")
    c = sub.add_parser("check", parents=[chromeopts], help="validate, quote-check and render papers")
    c.add_argument("project")
    c.add_argument("keys", nargs="*", help="paper keys (default: all)")
    b = sub.add_parser("build", parents=[chromeopts], help="assemble the deck, check it, export the PDF")
    b.add_argument("project")
    b.add_argument("--sheet", action="store_true", help="also render every slide and write contact-sheet.png")
    a = p.parse_args(argv)
    try:
        return {"new": cmd_new, "add": cmd_add, "check": cmd_check, "build": cmd_build}[a.cmd](a)
    except (ExplainerError, Q.SourceError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
