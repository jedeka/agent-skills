"""inline.py: export a built deck to the claude.ai Slides artifact format, and check the result by pixels.

    python3 inline.py <deck_dir> [--out DIR] [--blobs blobs.json] [--no-verify] [--threshold 1.0]
    python3 deck.py inline <deck_dir> [...]                  # the same

The Slides type stores a deck as project/deck.json (an index with "order") plus one file per slide,
project/slides/<id>.html, holding exactly one <section id="<id>"> whose every style is inline, from
a closed subset: no classes, <style>, margin, z-index, em or var(); speaker notes as plain text in
one <aside>, the section's last child; at most 200 elements per slide (counted here with SVG
contents included). This script renders the built deck in Chrome and rewrites each slide in that form:

  styles     each element gets the computed value of every property that differs from what the
             element would get with no stylesheet (inherited ones only where they change); sizes
             only where the theme or the slide declared them (a table cell keeps a declared
             percentage width); a declared line-height ratio stays a ratio; colours as hex
  tags       strong > b, em > i, code > span, h4-h6 > h3, figure > div, ... ; thead/tbody unwrapped
  margins    auto margins in a flex box become a growing wrapper that places the element at its far
             end or centre (main axis), or align-self (cross axis); other margins are reported
  pinned     absolutely positioned elements (the footer, the arrows of the pipeline template, which
             are ::before/::after shapes made real) become pinned children of the section, placed
             in slide coordinates
  attributes src, alt, href, aria-label, colspan and rowspan are kept; ids, classes and data-* go
  notes      <aside class="notes"> becomes <aside> with the plain text
  images     src stays assets/<file> until uploaded: upload each file listed in blobs.json to the
             Slides artifact (Artifact publish with asset: true), write each returned url into
             blobs.json, then rerun with --blobs blobs.json; images must be png, jpg, gif, webp or svg
  faces      deck.json "faces" links each font family the slides use to its Google Fonts css2 URL
             (Inter and JetBrains Mono, the technical-swiss fonts, are both on Google Fonts); a family
             that is not on Google Fonts must be uploaded and given a "src" by hand

Output, in --out (default <deck_dir>/build/inline/):
  project/deck.json, project/slides/<id>.html     the files to publish to the Slides artifact
  blobs.json                                      images to upload, as {"assets/x.png": ""}
  verify/orig-NN.png, verify/inline-NN.png        the renders compared

Verification renders every slide twice, from the build and from the inlined file, and compares the
pixels: the mean absolute difference per channel (0-255) must stay under --threshold (default 1.0).
The inlined file is rendered in a page that holds only the theme's @font-face rules, `section *
{margin:0}` and a positioned 1920 x 1080 section: the Slides runtime forbids margins, so it is
assumed to zero them, and it pins children to the slide. The format rules above are checked on the
written files. The runtime itself is not run here. Needs Chrome and Pillow (for the comparison).
"""
import argparse
import datetime
import html
import json
import re
import shutil
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import deck as D  # noqa: E402

ALLOWED = {"section", "h1", "h2", "h3", "p", "ul", "ol", "li", "br", "b", "i", "u", "a", "span", "div", "img",
           "table", "tr", "th", "td", "svg", "hr", "aside", "x-shape", "x-icon", "x-connector", "x-embed"}
ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")

EXTRACT = r"""<script>
(function(){
const INH=['color','font-family','font-size','font-weight','font-style','font-variant-numeric',
  'font-feature-settings','line-height','letter-spacing','word-spacing','text-align','text-transform',
  'text-indent','white-space','text-wrap-style','overflow-wrap','word-break','hyphens','list-style-type',
  'list-style-position','border-collapse','border-spacing','visibility'];
const NON=['display','box-sizing','flex-direction','flex-wrap','flex-grow','flex-shrink','flex-basis',
  'align-items','align-self','align-content','justify-content','justify-items','justify-self','row-gap',
  'column-gap','grid-template-columns','grid-template-rows','grid-auto-flow','grid-column-start',
  'grid-column-end','grid-row-start','grid-row-end','order','padding-top','padding-right','padding-bottom',
  'padding-left','border-top-width','border-top-style','border-top-color','border-right-width',
  'border-right-style','border-right-color','border-bottom-width','border-bottom-style','border-bottom-color',
  'border-left-width','border-left-style','border-left-color','border-top-left-radius',
  'border-top-right-radius','border-bottom-right-radius','border-bottom-left-radius','background-color',
  'overflow-x','overflow-y','object-fit','object-position','vertical-align','opacity','text-decoration-line',
  'text-decoration-style','text-decoration-color','outline-width','outline-style','outline-color',
  'outline-offset','table-layout'];
const SIZE=['width','height','min-width','min-height','max-width','max-height'];
const MAP={strong:'b',em:'i',cite:'i',var:'i',dfn:'i',code:'span',kbd:'span',samp:'span',small:'span',
  mark:'span',sub:'span',sup:'span',s:'span',del:'span',ins:'u',abbr:'span',q:'span',label:'span',time:'span',
  h4:'h3',h5:'h3',h6:'h3',figure:'div',figcaption:'p',blockquote:'div',header:'div',footer:'div',main:'div',
  article:'div',nav:'div',section:'div',pre:'p',dl:'div',dt:'p',dd:'p',caption:'p',picture:'span'};
const KEEP=new Set(['h1','h2','h3','p','ul','ol','li','br','b','i','u','a','span','div','img','table','tr','th',
  'td','hr']);
const UNWRAP=new Set(['thead','tbody','tfoot']);
const RULES=[];
function collect(list){for(const r of list){
  if(r instanceof CSSStyleRule) RULES.push(r);
  else if(r instanceof CSSMediaRule&&matchMedia(r.media.mediaText).matches) collect(r.cssRules);}}
for(const sh of document.styleSheets){try{collect(sh.cssRules);}catch(e){}}
function matching(el){return RULES.filter(r=>{try{return el.matches(r.selectorText);}catch(e){return false;}});}
function declared(el){const s=new Map();
  for(const r of matching(el)) for(let i=0;i<r.style.length;i++) s.set(r.style[i],r.style.getPropertyValue(r.style[i]));
  for(let i=0;i<el.style.length;i++) s.set(el.style[i],el.style.getPropertyValue(el.style[i]));
  return s;}
// a stylesheet-free sandbox with the runtime's assumed reset: what each tag looks like unstyled
const fr=document.createElement('iframe');
fr.style.cssText='position:absolute;left:-10000px;top:0;width:1920px;height:1080px;border:0';
document.body.appendChild(fr);
const sd=fr.contentDocument; sd.open();
sd.write('<!doctype html><html><head><style>html,body{margin:0}section *{margin:0}</style></head><body><section></section></body></html>');
sd.close();
const sbox=sd.querySelector('section'), DEF={}, UAINH={};
function probe(tag){
  if(DEF[tag]) return;
  let host=sbox;
  if(tag==='td'||tag==='th'){const t=sd.createElement('table'),r=sd.createElement('tr'); t.appendChild(r); sbox.appendChild(t); host=r;}
  else if(tag==='tr'){host=sd.createElement('table'); sbox.appendChild(host);}
  else if(tag==='li'){host=sd.createElement('ul'); sbox.appendChild(host);}
  const el=sd.createElement(tag); host.appendChild(el);
  const cs=fr.contentWindow.getComputedStyle(el), pcs=fr.contentWindow.getComputedStyle(host);
  DEF[tag]={}; for(const p of NON) DEF[tag][p]=cs.getPropertyValue(p);
  UAINH[tag]=INH.filter(p=>cs.getPropertyValue(p)!==pcs.getPropertyValue(p));
}
function hex(v){return v.replace(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/g,(m,r,g,b,a)=>
  a!==undefined&&parseFloat(a)<1?m:'#'+[r,g,b].map(x=>(+x).toString(16).padStart(2,'0')).join('').toUpperCase());}
function css(list){return list.map(([k,v])=>k+':'+hex(String(v)).replace(/"/g,"'")).join(';');}
function compact(m){
  const out=[], has=k=>m.has(k);
  for(const side of ['top','right','bottom','left']){
    const w=m.get('border-'+side+'-width'), st=m.get('border-'+side+'-style'), c=m.get('border-'+side+'-color');
    ['width','style','color'].forEach(x=>m.delete('border-'+side+'-'+x));
    if(st&&st!=='none'&&parseFloat(w)>0) m.set('border-'+side,w+' '+st+' '+c);
  }
  if(['top','right','bottom','left'].some(s=>has('padding-'+s))){
    const v=['top','right','bottom','left'].map(s=>m.get('padding-'+s)||'0px');
    ['top','right','bottom','left'].forEach(s=>m.delete('padding-'+s)); m.set('padding',v.join(' '));}
  if(m.get('outline-style')==='none'||!m.has('outline-style')){['width','style','color','offset'].forEach(x=>m.delete('outline-'+x));}
  if(m.get('flex-basis')==='0%') m.set('flex-basis','0px');
  if(!m.has('text-decoration-line')||m.get('text-decoration-line')==='none'){m.delete('text-decoration-color'); m.delete('text-decoration-style');}
  for(const [k,v] of m) out.push([k,v]);
  return out;
}
function textOf(n){return n.textContent.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function run(){
  const slides=[];
  document.querySelectorAll('.slide > section').forEach(sec=>{
    const sr=sec.getBoundingClientRect(), pinned=[], warn=[];
    const scs=getComputedStyle(sec);
    function geom(r){return [['position','absolute'],['left',(r.left-sr.left).toFixed(2)+'px'],
      ['top',(r.top-sr.top).toFixed(2)+'px'],['width',r.width.toFixed(2)+'px'],['height',r.height.toFixed(2)+'px']];}
    // the line-height an element inherits: a declared ratio stays a ratio (layout rounds a ratio and
    // its px value differently, which moves text by a pixel); otherwise the computed value
    function nearestLH(el){
      for(let e=el;e;e=e.parentElement){const d=declared(e).get('line-height');
        if(d) return /^[\d.]+$/.test(d.trim())?d.trim():getComputedStyle(el).lineHeight;
        if(e===sec) break;}
      return 'normal';
    }
    function styleFor(el,T,cs,pcs,decl,extra,moved){
      probe(T); const m=new Map();
      for(const p of INH){if(p==='line-height') continue;
        const v=cs.getPropertyValue(p); if(v!==pcs.getPropertyValue(p)||UAINH[T].includes(p)) m.set(p,v);}
      const own=decl&&decl.get('line-height');
      if(own) m.set('line-height',/^[\d.]+$/.test(own.trim())?own.trim():cs.lineHeight);
      else if(moved||UAINH[T].includes('line-height')) m.set('line-height',nearestLH(el));
      for(const p of NON){const v=cs.getPropertyValue(p); if(v!==DEF[T][p]) m.set(p,v);}
      // sizes only where declared; a table cell keeps a percentage (the table algorithm treats percent
      // and px columns differently)
      if(decl) for(const p of SIZE){const d=decl.get(p); const v=cs.getPropertyValue(p);
        if(d&&d!=='auto'&&d!=='none'&&v!=='auto'&&v!=='none') m.set(p,(T==='td'||T==='th')&&/^[\d.]+%$/.test(d.trim())?d.trim():v);}
      for(const [k,v] of (extra||[])) m.set(k,v);
      return css(compact(m));
    }
    function pseudo(el,ps,pcs){
      const cs=getComputedStyle(el,ps), c=cs.content;
      if(!c||c==='none'||c==='normal') return '';
      const txt=/^["'].*["']$/.test(c)?c.slice(1,-1):(warn.push('unsupported '+ps+' content '+c),'');
      const abs=cs.position==='absolute'||cs.position==='fixed';
      let extra=[];
      if(abs){
        const er=el.getBoundingClientRect(), ecs=getComputedStyle(el);
        const left=er.left-sr.left+parseFloat(ecs.borderLeftWidth)+parseFloat(cs.left);
        const top=er.top-sr.top+parseFloat(ecs.borderTopWidth)+parseFloat(cs.top);
        extra=[['position','absolute'],['left',left.toFixed(2)+'px'],['top',top.toFixed(2)+'px'],
               ['width',cs.width],['height',cs.height]];
      }
      const T=cs.display==='inline'?'span':'div';
      const h='<'+T+' style="'+styleFor(el,T,cs,abs?scs:pcs,null,extra,abs)+'">'+textOf({textContent:txt})+'</'+T+'>';
      if(abs){pinned.push(h); return '';}
      return h;
    }
    // children of a box. In a flex box an auto margin on the main axis becomes a wrapper that takes the
    // free space (flex-grow = the child's count of auto margins) and places the child at its far end or
    // centre, which adds no gap; auto margins on the cross axis become align-self.
    function kids(el,cs){
      const flex=cs.display.includes('flex'), row=flex&&cs.flexDirection.startsWith('row');
      const grows=flex&&[...el.children].some(k=>parseFloat(getComputedStyle(k).flexGrow)>0);
      let inner='';
      for(const n of el.childNodes){
        if(n.nodeType===3){inner+=textOf(n); continue;}
        if(n.nodeType!==1) continue;
        let h=conv(n,el);
        if(!h||!flex){inner+=h; continue;}
        const d=declared(n), ncs=getComputedStyle(n), [ms,me,c0,c1]=row?['left','right','top','bottom']:['top','bottom','left','right'];
        const a=d.get('margin-'+c0)==='auto', b=d.get('margin-'+c1)==='auto';
        if(a||b) h=h.replace(/ style="/,' style="'+css([['align-self',a&&b?'center':(a?'flex-end':'flex-start')]])+';');
        const s0=d.get('margin-'+ms)==='auto', s1=d.get('margin-'+me)==='auto';
        if(!grows&&(s0||s1)){
          const w=[['display','flex'],['flex-direction',row?'row':'column'],['flex-grow',String(s0+s1)],
                   ['flex-shrink',ncs.flexShrink],['justify-content',s0&&s1?'center':(s0?'flex-end':'flex-start')],
                   ['align-items',cs.alignItems==='normal'?'stretch':cs.alignItems]];
          if(ncs.alignSelf!=='auto') w.push(['align-self',ncs.alignSelf]);
          h='<div style="'+css(w)+'">'+h+'</div>';
        }
        inner+=h;
      }
      return inner;
    }
    function conv(el,parent){
      const tag=el.tagName.toLowerCase();
      if(el.matches('aside.notes,script,style,template')) return '';
      const cs=getComputedStyle(el);
      if(cs.display==='none') return '';
      if(tag==='svg'){
        const r=el.getBoundingClientRect(), c=el.cloneNode(true);
        c.removeAttribute('class'); c.querySelectorAll('[class]').forEach(x=>x.removeAttribute('class'));
        const st=[['width',r.width.toFixed(2)+'px'],['height',r.height.toFixed(2)+'px']];
        if(cs.display!=='inline') st.unshift(['display',cs.display]);
        if(cs.verticalAlign!=='baseline') st.push(['vertical-align',cs.verticalAlign]);
        c.setAttribute('style',css(st));
        let s=c.outerHTML.replace(/currentColor/g,hex(cs.color));
        if(s.length>52*1024) warn.push('an SVG is '+Math.round(s.length/1024)+' KB; the Slides format allows 52 KB');
        return s;
      }
      if(UNWRAP.has(tag)) return [...el.childNodes].map(n=>n.nodeType===1?conv(n,parent):'').join('');
      const T=KEEP.has(tag)?tag:(MAP[tag]||(cs.display.startsWith('inline')?'span':'div'));
      if(!KEEP.has(tag)&&!MAP[tag]) warn.push('<'+tag+'> written as <'+T+'>');
      const abs=(cs.position==='absolute'||cs.position==='fixed');
      const pcs=abs?scs:getComputedStyle(parent);
      const decl=declared(el);
      for(const side of ['top','right','bottom','left']){const d=decl.get('margin-'+side), v=parseFloat(cs.getPropertyValue('margin-'+side));
        if(d!=='auto'&&v) warn.push('<'+tag+'> margin-'+side+' '+v+'px dropped (the format has no margin)');}
      if(cs.position==='relative'&&['top','left','right','bottom'].some(s=>parseFloat(cs.getPropertyValue(s)))) warn.push('<'+tag+'> relative offset dropped');
      const slot=abs?pinned.push('')-1:-1;
      let extra=abs?geom(el.getBoundingClientRect()):[];
      if(tag==='img') extra=[['width',el.getBoundingClientRect().width.toFixed(2)+'px'],['height',el.getBoundingClientRect().height.toFixed(2)+'px']];
      let attrs='';
      if(tag==='img') attrs=' src="'+el.getAttribute('src')+'" alt="'+(el.getAttribute('alt')||'').replace(/"/g,'&quot;')+'"';
      if(tag==='a'&&el.getAttribute('href')) attrs=' href="'+el.getAttribute('href').replace(/"/g,'&quot;')+'"';
      for(const k of ['colspan','rowspan']) if((tag==='td'||tag==='th')&&el.getAttribute(k)) attrs+=' '+k+'="'+(+el.getAttribute(k))+'"';
      if(el.getAttribute('aria-label')) attrs+=' aria-label="'+el.getAttribute('aria-label').replace(/"/g,'&quot;')+'"';
      const st=styleFor(el,T,cs,pcs,decl,extra,abs);
      let inner='';
      if(tag!=='img'&&tag!=='br'&&tag!=='hr'){
        inner+=pseudo(el,'::before',cs)+kids(el,cs)+pseudo(el,'::after',cs);
      }
      const html=(T==='img'||T==='br'||T==='hr')?'<'+T+attrs+' style="'+st+'">':'<'+T+attrs+' style="'+st+'">'+inner+'</'+T+'>';
      if(abs){pinned[slot]=html; return '';}
      return html;
    }
    probe('section');
    const m=new Map();
    for(const p of INH) m.set(p,scs.getPropertyValue(p));
    for(const p of NON){const v=scs.getPropertyValue(p); if(v!==DEF['section'][p]) m.set(p,v);}
    m.set('background',scs.backgroundColor); m.delete('background-color');
    m.set('width',scs.width); m.set('height',scs.height);
    const inner=kids(sec,scs);
    slides.push({style:css(compact(m)),body:inner+pinned.join(''),warnings:warn});
  });
  const pre=document.createElement('pre'); pre.id='__inline'; pre.textContent=JSON.stringify(slides);
  document.body.appendChild(pre);
}
window.addEventListener('load',()=>document.fonts.ready.then(()=>setTimeout(run,50)));
})();
</script>"""


class FormatCheck(HTMLParser):
    """Collects what the Slides format forbids in one written slide file."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.problems, self.count, self.max_div, self.in_svg, self.stack = [], 0, 0, 0, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.count += 1                      # SVG contents count too
        if self.in_svg:
            self.in_svg += 1
            return
        if tag not in ALLOWED:
            self.problems.append(f"<{tag}> is not in the format")
        if "class" in a:
            self.problems.append(f"<{tag}> has a class")
        st = a.get("style") or ""
        for bad, why in ((r"(^|;)\s*margin", "margin"), (r"z-index", "z-index"), (r"var\(", "var()"),
                         (r"\d(\.\d+)?r?em\b", "em units")):
            if re.search(bad, st):
                self.problems.append(f"<{tag}> style uses {why}")
        if tag == "img" and not re.match(r"^(/_blob/|project/ds/)", a.get("src", "")):
            self.problems.append(f"<img src=\"{a.get('src', '')}\"> is not uploaded yet (blobs.json)")
        if tag == "img" and not re.search(r"\.(png|jpe?g|gif|webp|svg)$", a.get("src", ""), re.I) \
                and not a.get("src", "").startswith("/_blob/"):
            self.problems.append(f"<img src=\"{a.get('src', '')}\"> is not png, jpg, gif, webp or svg")
        if tag == "svg":
            self.in_svg = 1
        elif tag not in ("br", "hr", "img"):
            self.stack.append(tag)
            self.max_div = max(self.max_div, self.stack.count("div"))

    def handle_endtag(self, tag):
        if self.in_svg:
            self.in_svg -= 1
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()


def faces_for(theme_css: str, used: str) -> dict:
    """deck.json "faces": one Google Fonts css2 link per @font-face family that the slides use."""
    weights = {}
    for block in re.findall(r"@font-face\s*\{([^}]*)\}", theme_css):
        fam = re.search(r"font-family\s*:\s*['\"]?([^;'\"]+)", block)
        w = re.search(r"font-weight\s*:\s*(\d+)", block)
        if fam:
            weights.setdefault(fam[1].strip(), set()).add(int(w[1]) if w else 400)
    out = {}
    for fam, ws in weights.items():
        if fam.lower() in used.lower():
            out[re.sub(r"\s+", "-", fam.lower())] = {
                "family": fam,
                "href": "https://fonts.googleapis.com/css2?family=" + fam.replace(" ", "+")
                        + ":wght@" + ";".join(str(w) for w in sorted(ws)) + "&display=swap"}
    return dict(list(out.items())[:4])


def section_titles(src: str) -> str:
    """The title text of a section slide (the h1.section-title that is not just its number)."""
    for t in re.findall(r"""<h1\b[^>]*class=["'][^"']*section-title[^"']*["'][^>]*>(.*?)</h1>""", src, re.S):
        t = html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
        if t and not re.fullmatch(r"[\[\]\d\s.]+", t):
            return t
    return ""


def run(a) -> int:
    deck_dir = Path(a.deck_dir)
    out = Path(a.out) if getattr(a, "out", "") else deck_dir / "build" / "inline"
    deck, slides = D.cmd_build(a, quiet=True)
    build = deck_dir / "build"
    probe = build / "_inline.html"
    probe.write_text(D.page_html(deck, slides, fit=False, tail=EXTRACT), encoding="utf-8")
    try:
        dom = D.chrome(a, ["--dump-dom", probe.resolve().as_uri()], capture=True)
    finally:
        probe.unlink(missing_ok=True)
    m = re.search(r'<pre id="__inline">(.*?)</pre>', dom, re.S)
    if not m:
        raise D.DeckError("the inliner produced no output (try a larger --budget)")
    got = json.loads(html.unescape(m[1]))
    blobs = json.loads(Path(a.blobs).read_text(encoding="utf-8")) if getattr(a, "blobs", "") else {}

    shutil.rmtree(out / "project" / "slides", ignore_errors=True)
    (out / "project" / "slides").mkdir(parents=True)
    ids, local, sections, cover, used, problems = [], [], {}, None, "", 0
    for (sid, src, notes), g in zip(slides, got):
        if not ID_RE.match(sid):
            raise D.DeckError(f"slide id '{sid}' is not [A-Za-z0-9_-]{{1,64}}; rename the slide file")
        if len(notes) > 4000:
            g["warnings"].append(f"speaker notes are {len(notes)} characters; the format keeps 4,000")
        aside = f"<aside>{html.escape(notes[:4000], quote=False)}</aside>" if notes else ""
        section = f'<section id="{sid}" style="{g["style"]}">\n{g["body"]}\n{aside}</section>\n'
        local.append(section)
        for ref, url in blobs.items():
            if url:
                section = section.replace(f'src="{ref}"', f'src="{url}"')
        (out / "project" / "slides" / f"{sid}.html").write_text(section, encoding="utf-8")
        ids.append(sid)
        used += g["style"] + g["body"]
        classes = (re.search(r"""<section\b[^>]*class=["']([^"']*)""", src) or [None, ""])[1].split()
        if cover is None and "cover" in classes:
            cover = sid
        if "section" in classes:
            sections[f"s{len(sections) + 1}"] = {"description": section_titles(src) or sid, "start": sid}
        fc = FormatCheck()
        fc.feed(section)
        if fc.count > 200:
            fc.problems.append(f"{fc.count} elements; the format allows 200")
        if fc.max_div > 15:
            fc.problems.append(f"divs nest {fc.max_div} deep; the format allows 15")
        for p in dict.fromkeys(fc.problems):
            if "not uploaded" not in p:
                problems += 1
            print(f"  {sid}: {p}")
        for w in dict.fromkeys(g["warnings"]):
            print(f"  {sid}: warning: {w}")
    if ids[0] not in [s["start"] for s in sections.values()]:
        sections = {"s0": {"description": deck["title"], "start": ids[0]}, **sections}
    sections = {f"s{i}": v for i, v in enumerate(sections.values(), 1)}
    index = {"v": 4, "createdOnFiles": {"v": 1, "at": datetime.datetime.now(datetime.timezone.utc)
                                        .strftime("%Y-%m-%dT%H:%M:%SZ")},
             "lists": "css", "title": deck["title"], "order": ids, "sections": sections,
             "cover": cover or ids[0],
             "faces": faces_for((D.theme_dir(deck["theme"]) / "theme.css").read_text(encoding="utf-8"), used),
             "designSystems": []}
    (out / "project" / "deck.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n",
                                               encoding="utf-8")
    refs = sorted(set(re.findall(r'src="(assets/[^"]+)"', "".join(local))))
    (out / "blobs.json").write_text(json.dumps({r: blobs.get(r, "") for r in refs}, indent=2) + "\n",
                                    encoding="utf-8")
    pending = [r for r in refs if not blobs.get(r)]
    print(f"wrote {out / 'project'} ({len(ids)} slides, deck.json with {len(index['faces'])} face(s))")
    if pending:
        print(f"{len(pending)} image(s) to upload before publishing; listed in {out / 'blobs.json'}")
    rc = 1 if problems else 0
    if not getattr(a, "no_verify", False):
        rc |= verify(a, deck, slides, local, out)
    return rc


def verify(a, deck, slides, local, out) -> int:
    try:
        from PIL import Image, ImageChops, ImageStat
    except ImportError:
        raise D.DeckError("the pixel comparison needs Pillow (pip install pillow, or run scripts/setup.sh); "
                          "pass --no-verify to skip it")
    deck_dir = Path(a.deck_dir)
    build = deck_dir / "build"
    vdir = out / "verify"
    shutil.rmtree(vdir, ignore_errors=True)
    vdir.mkdir(parents=True)
    faces = "\n".join(re.findall(r"@font-face\s*\{[^}]*\}",
                                 (D.theme_dir(deck["theme"]) / "theme.css").read_text(encoding="utf-8")))
    base = build.resolve().as_uri() + "/"
    head = (f'<!doctype html><html><head><meta charset="utf-8"><base href="{base}"><style>\n{faces}\n'
            "html,body{margin:0;background:#FFFFFF}\nsection{position:relative;overflow:hidden;width:1920px;"
            "height:1080px;box-sizing:border-box}\nsection *{margin:0}\naside{display:none}\n</style></head><body>\n")
    tmp = Path(tempfile.mkdtemp(prefix="_inline-", dir=build))

    def pair(n: int) -> tuple:
        orig, mine = vdir / f"orig-{n:02d}.png", vdir / f"inline-{n:02d}.png"
        p1 = tmp / f"orig-{n:02d}.html"
        p1.write_text(D.page_html(deck, slides, fit=False, extra_css=D.SOLO_CSS, base=base, only=n),
                      encoding="utf-8")
        p2 = tmp / f"inline-{n:02d}.html"
        p2.write_text(head + local[n - 1] + "</body></html>\n", encoding="utf-8")
        for page, png in ((p1, orig), (p2, mine)):
            D.chrome(a, [f"--screenshot={png.resolve()}", page.resolve().as_uri()], profile=tmp / f"prof-{png.stem}")
        i1, i2 = Image.open(orig).convert("RGB"), Image.open(mine).convert("RGB")
        diff = ImageChops.difference(i1, i2)
        mean = sum(ImageStat.Stat(diff).mean) / 3
        changed = sum(1 for px in diff.convert("L").getdata() if px > 32) / (i1.width * i1.height)
        return n, mean, changed

    try:
        with ThreadPoolExecutor(max_workers=4) as pool:
            res = list(pool.map(pair, range(1, len(slides) + 1)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    bad = 0
    print(f"\npixel comparison, build vs inlined (threshold: mean abs diff < {a.threshold:g} of 255)")
    for (n, mean, changed), (sid, _, _) in zip(res, slides):
        ok = mean < a.threshold
        bad += not ok
        print(f"  {n:02d} {sid:<32} mean {mean:6.3f}  pixels off by > 32: {100 * changed:5.2f}%  {'ok' if ok else 'DIFFERS'}")
    print(f"{'all ' + str(len(res)) + ' slides match' if not bad else str(bad) + ' slide(s) differ'}; "
          f"renders in {vdir}")
    return 1 if bad else 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("deck_dir")
    p.add_argument("--out", default="", help="output folder (default <deck_dir>/build/inline)")
    p.add_argument("--blobs", default="", help='JSON {"assets/x.png": "/_blob/<id>"} of uploaded images')
    p.add_argument("--no-verify", action="store_true", help="skip the pixel comparison")
    p.add_argument("--threshold", type=float, default=1.0,
                   help="largest mean absolute pixel difference allowed per slide (0-255, default 1.0)")
    p.add_argument("--chrome", default="", help="path to Chrome/Chromium (else CHROME_PATH, PATH)")
    p.add_argument("--budget", type=int, default=8000, help="Chrome virtual-time budget in ms")
    a = p.parse_args(argv)
    try:
        return run(a)
    except D.DeckError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
