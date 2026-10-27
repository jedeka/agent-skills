"""anatomy.py: render slide templates clean and with an anatomy overlay of grid, margins and regions.

    python3 anatomy.py                          # every template of technical-swiss -> references/templates/
    python3 anatomy.py --only 03,key-number     # a subset, by number or by name
    python3 anatomy.py --deck <deck_dir>        # a deck's slides -> <deck_dir>/build/anatomy/
    python3 anatomy.py --theme <name> --out <dir>

For every slide it writes two PNGs:
    <id>.png          the clean 1920 x 1080 render, made by deck.py png
    <id>-anatomy.png  the same slide under a light veil, with the 12-column grid, the margins, the end
                      of the content area and the footer band drawn on it, every region outlined and
                      numbered, and a legend on the right: the template's "Use:" line, the grid
                      measures, the content height used, and per region its role, capacity, measured
                      size and the grid columns it spans
Template mode also writes gallery.png, all clean renders on one labelled sheet (contact_sheet.py),
unless --only picked a subset.

Regions are the elements marked data-role="<role>", with data-cap="<capacity>" copied from the
template's capacity comment. Regions with the same role and capacity share a number. A slide without
data-role gets its top-level blocks outlined instead, labelled by tag and class. A region whose left
or right edge is more than 2 px off a column edge is listed with its x range instead of its columns.
In template mode every "≤ N" in a data-cap must also appear in the template's comment or in the
region's placeholder text; otherwise a warning names the region and the exit code is 1, so the two
cannot drift apart silently.

Template-mode PNGs are stored with a 256-colour palette: the placeholders are flat, so nothing
visible is lost and the files are under half the size. Deck-mode PNGs keep full colour (photos).
Needs Chrome (as deck.py finds it) and Pillow for the gallery and for compressing the PNGs.
"""
import argparse
import html
import json
import re
import shutil
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import deck as D  # noqa: E402

LEGEND_W = 840

# Injected into a one-slide page: draws the overlay and the legend, then reports what it measured
# into <pre id="__anatomy"> (read by --dump-dom in the first pass).
OVERLAY = r"""<script>
(function(){
const M=__META__, LW=__LEGEND_W__;
const MAG='#D0006F', TOL=2;
const px=v=>parseFloat(v)||0, r=Math.round;
function el(tag,css,txt,parent){const e=document.createElement(tag); e.style.cssText=css;
  if(txt!=null) e.textContent=txt; (parent||document.body).appendChild(e); return e;}
function box(e,sr){const b=e.getBoundingClientRect(); return [b.left-sr.left,b.top-sr.top,b.right-sr.left,b.bottom-sr.top];}
function pinned(e,sec){for(let x=e;x&&x!==sec;x=x.parentElement){const p=getComputedStyle(x).position;
  if(p==='absolute'||p==='fixed') return true;} return false;}
function topBlocks(sec){const out=[];
  for(const c of sec.children){if(c.matches('aside.notes,.foot,script,style')) continue;
    if(c.matches('.row,.grid12,.flow')) out.push(...[...c.children].filter(k=>!k.matches('.arrow')));
    else out.push(c);}
  return out;}
function run(){
  const sec=document.querySelector('.slide > section'), sr=sec.getBoundingClientRect(), cs=getComputedStyle(sec);
  const W=sr.width, H=sr.height;
  const pad={l:px(cs.paddingLeft),r:px(cs.paddingRight),t:px(cs.paddingTop),b:px(cs.paddingBottom)};
  const band=px(getComputedStyle(document.documentElement).getPropertyValue('--foot-band'))||80;
  const probe=el('div','position:absolute;visibility:hidden;left:0;top:0;width:'+(W-pad.l-pad.r)+'px',null,sec);
  probe.className='grid12'; const gut=px(getComputedStyle(probe).columnGap); probe.remove();
  const cw=(W-pad.l-pad.r-11*gut)/12, step=cw+gut;
  // regions: data-role elements, else top-level blocks
  let els=[...sec.querySelectorAll('[data-role]')].filter(e=>!e.closest('aside.notes,.foot'));
  const auto=!els.length; if(auto) els=topBlocks(sec);
  const keys=[], regions=[];
  for(const e of els){
    const role=auto?(e.tagName.toLowerCase()+[...e.classList].slice(0,2).map(c=>'.'+c).join('')):e.dataset.role;
    const cap=auto?'':(e.dataset.cap||''), key=role+'|'+cap;
    let n=keys.indexOf(key); if(n<0){keys.push(key); n=keys.length-1;
      regions.push({n:n+1,role,cap,boxes:[],cols:[],text:[]});}
    const b=box(e,sr), g=regions[n];
    const iL=Math.min(11,Math.max(0,Math.round((b[0]-pad.l)/step))), iR=Math.min(11,Math.max(0,Math.round((b[2]-pad.l-cw)/step)));
    const offL=b[0]-(pad.l+iL*step), offR=b[2]-(pad.l+iR*step+cw);
    const on=Math.abs(offL)<=TOL&&Math.abs(offR)<=TOL&&iR>=iL;
    g.boxes.push(b.map(r)); g.text.push((e.textContent||'').replace(/\s+/g,' ').trim().slice(0,300));
    g.cols.push(on?(iL===iR?String(iL+1):(iL+1)+'–'+(iR+1)):null);
  }
  let lowest=0;
  for(const e of sec.querySelectorAll('*')){if(e.closest('aside.notes,.foot,svg')||pinned(e,sec)) continue;
    const b=e.getBoundingClientRect(); if(b.width>0&&b.height>0) lowest=Math.max(lowest,b.bottom-sr.top);}
  // ---- overlay on the slide
  const ov=el('div','position:absolute;left:0;top:0;width:'+W+'px;height:'+H+'px;pointer-events:none;z-index:10;'+
    'font-family:Inter,Arial,sans-serif');
  el('div','position:absolute;inset:0;background:rgba(255,255,255,0.42)',null,ov);
  const hatch=c=>'repeating-linear-gradient(135deg,'+c+' 0 2px,transparent 2px 11px)';
  const marg=hatch('rgba(80,80,80,0.16)');
  for(const [x,y,w,h] of [[0,0,W,pad.t],[0,H-pad.b,W,pad.b],[0,pad.t,pad.l,H-pad.t-pad.b],[W-pad.r,pad.t,pad.r,H-pad.t-pad.b]])
    el('div',`position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;background:${marg}`,null,ov);
  el('div',`position:absolute;left:0;top:${H-band}px;width:${W}px;height:${band}px;background:${hatch('rgba(199,138,0,0.30)')};`+
    'border-top:2px solid rgba(199,138,0,0.9)',null,ov);
  const endFits=H-band-(H-pad.b)>=36;   // room for the end-of-content label above the band
  el('div',`position:absolute;left:${pad.l}px;top:${H-band+10}px;font:600 20px/24px Inter;letter-spacing:1px;color:#8A6000`,
    'FOOTER BAND · '+band+' PX · PAGE NUMBER ONLY'+(endFits?'':' · CONTENT AREA ENDS AT Y '+r(H-pad.b)),ov);
  for(let i=0;i<12;i++){const x=pad.l+i*step;
    el('div',`position:absolute;left:${x}px;top:${pad.t}px;width:${cw}px;height:${H-pad.t-pad.b}px;`+
      'background:rgba(0,150,200,0.09);border-left:1px solid rgba(0,120,170,0.45);border-right:1px solid rgba(0,120,170,0.45)',null,ov);
    el('div',`position:absolute;left:${x}px;top:${Math.max(4,pad.t-70)}px;width:${cw}px;text-align:center;`+
      'font:600 20px/24px Inter;color:#00789F',String(i+1),ov);}
  el('div',`position:absolute;left:${pad.l}px;top:${H-pad.b}px;width:${W-pad.l-pad.r}px;border-top:2px dashed rgba(17,17,17,0.55)`,null,ov);
  if(endFits) el('div',`position:absolute;left:${pad.l}px;top:${H-pad.b+8}px;font:600 20px/24px Inter;letter-spacing:1px;color:#444`,
    'END OF CONTENT AREA · Y '+r(H-pad.b),ov);
  const placed=[];
  const free=(x,y,w,h)=>x>=0&&y>=0&&x+w<=W&&y+h<=H&&!placed.some(p=>x<p[2]+4&&x+w>p[0]-4&&y<p[3]+4&&y+h>p[1]-4);
  for(const g of regions) g.boxes.forEach((b,k)=>{
    el('div',`position:absolute;left:${b[0]-3}px;top:${b[1]-3}px;width:${b[2]-b[0]+6}px;height:${b[3]-b[1]+6}px;`+
      `border:3px solid ${MAG};box-sizing:border-box`,null,ov);
    const h=k===0?30:26;
    const tag=el('div',`position:absolute;left:0;top:0;height:${h}px;padding:0 ${k===0?12:9}px;background:${MAG};color:#fff;`+
      `font:600 ${k===0?20:18}px/${h}px Inter;white-space:nowrap`,k===0?g.n+' '+g.role:String(g.n),ov);
    const w=tag.offsetWidth, x0=b[0]-3, x1=b[2]+3, y0=b[1]-3, y1=b[3]+3;
    const cand=k===0?[[x0,y0-h],[x1-w,y0-h],[x0,y0],[x1-w,y0],[x0,y1],[x0,y1-h],[x1-w,y1-h]]
                    :[[x1-w,y0],[x1-w,y1-h],[x0,y0],[x0,y1-h]];
    const at=cand.find(([x,y])=>free(x,y,w,h))||cand[0];
    tag.style.left=at[0]+'px'; tag.style.top=at[1]+'px'; placed.push([at[0],at[1],at[0]+w,at[1]+h]);
  });
  // ---- legend
  const L=el('div',`position:absolute;left:${W}px;top:0;width:${LW}px;min-height:${H}px;box-sizing:border-box;`+
    'padding:48px 52px 32px 52px;background:#FAFAF8;border-left:1px solid #D9D9D9;font-family:Inter,Arial,sans-serif;color:#111');
  el('p','margin:0;font:600 20px/26px Inter;letter-spacing:2px;color:#666',M.kicker,L);
  el('p','margin:10px 0 0 0;font:700 42px/50px Inter;letter-spacing:-1px',M.name,L);
  if(M.use) el('p','margin:12px 0 0 0;font:400 23px/31px Inter;color:#444',M.use.charAt(0).toUpperCase()+M.use.slice(1),L);
  const facts=[W+' × '+H+' · 12 columns of '+cw.toFixed(1)+' px, gutters '+gut,
    'margins '+pad.l+' sides · '+pad.t+' top · '+pad.b+' bottom · footer band '+band,
    'height used '+r(Math.max(0,lowest-pad.t))+' of '+r(H-pad.t-pad.b)+' px'];
  const F=el('div','margin:22px 0 0 0;padding-top:16px;border-top:2px solid #111;display:flex;flex-direction:column;gap:2px',null,L);
  for(const f of facts) el('p','margin:0;font:400 21px/30px "JetBrains Mono",monospace;color:#444',f,F);
  const R=el('div','margin:18px 0 0 0;display:flex;flex-direction:column',null,L);
  for(const g of regions){
    const row=el('div','display:flex;gap:16px;padding:10px 0;border-top:1px solid #D9D9D9',null,R);
    el('div',`flex:none;width:42px;height:32px;background:${MAG};color:#fff;font:600 21px/32px Inter;text-align:center`,String(g.n),row);
    const t=el('div','display:flex;flex-direction:column;gap:2px;min-width:0',null,row);
    el('p','margin:0;font:600 25px/32px Inter',g.role+(g.boxes.length>1?' ×'+g.boxes.length:''),t);
    // bind each sign to the number after it, so no line ends on "≤" (nbsp; U+2060 after a range dash)
    if(g.cap) el('p','margin:0;font:400 22px/29px Inter;color:#111',g.cap.replace(/([≤≥=×]) /g,'$1\u00a0'),t);
    const b=g.boxes[0], same=g.boxes.every(q=>q[2]-q[0]===b[2]-b[0]&&q[3]-q[1]===b[3]-b[1]);
    const on=[...new Set(g.cols.filter(c=>c))], off=g.boxes.filter((q,i)=>!g.cols[i]).map(q=>q[0]+'–\u2060'+q[2]);
    const where=(on.length?(on.length===1&&!on[0].includes('–')?'col ':'cols ')+on.join(', '):'')+
      (on.length&&off.length?'; ':'')+(off.length?'x '+off.join(', ')+' (off the column edges)':'');
    el('p','margin:0;font:400 20px/28px "JetBrains Mono",monospace;color:#666',
      (same?(b[2]-b[0])+'\u00a0×\u00a0'+(b[3]-b[1])+'\u00a0px · ':'')+where,t);
  }
  if(auto) el('p','margin:16px 0 0 0;font:400 21px/29px Inter;color:#8A6000',
    'No data-role regions in this slide: its top-level blocks are shown.',L);
  const K=el('div',`position:absolute;left:${pad.l}px;top:${H-band+44}px;display:flex;gap:24px;`+
    'font:400 20px/26px Inter;color:#444',null,ov);
  for(const [bg,label] of [['rgba(0,150,200,0.22);border:1px solid rgba(0,120,170,0.6)','grid column'],
                           [hatch('rgba(80,80,80,0.45)')+';border:1px solid #bbb','margin'],
                           [hatch('rgba(199,138,0,0.7)')+';border:1px solid rgba(199,138,0,0.9)','footer band'],
                           ['#fff;border:3px solid '+MAG,'region']]){
    const k=el('div','display:flex;align-items:center;gap:10px',null,K);
    el('span',`display:inline-block;width:34px;height:24px;box-sizing:border-box;background:${bg}`,null,k); el('span','',label,k);}
  // a legend taller than the slide: the strip under the slide is page background, not slide
  if(L.offsetHeight>H) el('div',`position:absolute;left:0;top:${H}px;width:${W}px;height:${L.offsetHeight-H}px;background:#E9E9E7`);
  const rep={regions:regions.map(({n,role,cap,boxes,cols,text})=>({n,role,cap,boxes,cols,text})),
    auto,lowest:r(lowest),limit:r(H-pad.b),top:pad.t,height:Math.ceil(Math.max(H,L.offsetHeight))};
  const pre=el('pre','display:none',JSON.stringify(rep)); pre.id='__anatomy';
}
window.addEventListener('load',()=>document.fonts.ready.then(()=>setTimeout(run,50)));
})();
</script>"""
PAGE_CSS = "body{position:relative;width:%dpx}" % (D.W + LEGEND_W)


def comment_meta(src: str, sid: str) -> dict:
    """Name and "Use:" text from the slide's leading HTML comment ("03 main content (design spec §7): ...")."""
    m = re.match(r"\s*<!--(.*?)-->", src, re.S)
    body = m[1] if m else ""
    first = body.strip().splitlines()[0] if body.strip() else ""
    name = re.split(r"\s\(|:\s|\.\s|\.$", first)[0].strip() if first else sid.replace("-", " ", 1)
    use = re.search(r"Use:(.*?)(?:\n\s*[A-Z][a-z]+:|\Z)", body, re.S)
    return {"name": name or sid, "use": re.sub(r"\s+", " ", use[1]).strip() if use else "", "comment": body}


def shot(a, page: Path, out: Path, w: int, h: int, profile: Path) -> None:
    """Screenshot a page at w x h (a later --window-size overrides the one deck.chrome sets)."""
    D.chrome(a, [f"--window-size={w},{h}", f"--screenshot={out.resolve()}", page.resolve().as_uri()],
             profile=profile)
    if not out.is_file():
        raise D.DeckError(f"Chrome wrote no screenshot for {page.name}")


def anatomy(a, deck: dict, slides: list, n: int, tmp: Path, out_png: Path, kicker: str) -> dict:
    """Two passes: measure (dump the report, learn the legend height), then screenshot at that height."""
    sid, src, _ = slides[n - 1]
    meta = comment_meta(src, sid)
    tail = (OVERLAY.replace("__META__", json.dumps({"name": meta["name"], "use": meta["use"], "kicker": kicker}))
            .replace("__LEGEND_W__", str(LEGEND_W)))
    page = tmp / f"anatomy-{n:02d}.html"
    page.write_text(D.page_html(deck, slides, fit=False, extra_css=D.SOLO_CSS + PAGE_CSS, tail=tail,
                                base="../", only=n), encoding="utf-8")
    dom = D.chrome(a, [f"--window-size={D.W + LEGEND_W},{D.H}", "--dump-dom", page.resolve().as_uri()],
                   capture=True, profile=tmp / f"p1-{n}")
    m = re.search(r'<pre id="__anatomy"[^>]*>(.*?)</pre>', dom, re.S)
    if not m:
        raise D.DeckError(f"slide {sid}: the overlay produced no report (try a larger --budget)")
    rep = json.loads(html.unescape(m[1]))
    shot(a, page, out_png, D.W + LEGEND_W, rep["height"], tmp / f"p2-{n}")
    rep.update(id=sid, name=meta["name"], comment=meta["comment"])
    return rep


def cap_drift(rep: dict) -> list:
    """Every '≤ N' in a data-cap must occur in the template comment or the region's placeholder text."""
    found = set(re.findall(r"≤\s*(\d+)", rep["comment"]))
    warn = []
    for g in rep["regions"]:
        own = set(re.findall(r"≤\s*(\d+)", " ".join(g["text"])))
        for num in re.findall(r"≤\s*(\d+)", g["cap"]):
            if num not in found | own:
                warn.append(f"{rep['id']}: region '{g['role']}' says ≤ {num}, which neither the capacity "
                            "comment nor its placeholder text states")
    return warn


def compress(png: Path, palette: bool) -> None:
    """Re-save smaller; palette=True stores 256 colours (lossless to the eye on flat placeholders)."""
    try:
        from PIL import Image
    except ImportError:
        return
    im = Image.open(png).convert("RGB")
    if palette:
        im = im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    im.save(png, optimize=True)


def template_deck(theme: str, work: Path, only: str) -> Path:
    """A throwaway deck holding the theme's templates (all, or those --only names)."""
    tdir = D.theme_dir(theme)
    files = sorted((tdir / "slides").glob("*.html"))
    if only:
        want = [w.strip() for w in only.split(",") if w.strip()]
        files = [f for f in files if any(f.stem == w or f.stem.split("-", 1)[0] == w or
                                         f.stem.split("-", 1)[-1] == w for w in want)]
        if not files:
            raise D.DeckError(f"--only {only} matches no template in {tdir / 'slides'}")
    (work / "slides").mkdir(parents=True)
    for f in files:
        shutil.copy2(f, work / "slides" / f.name)
    if (tdir / "assets").is_dir():
        shutil.copytree(tdir / "assets", work / "assets")
    (work / "deck.json").write_text(json.dumps({"title": f"{theme} templates", "theme": theme,
                                                "slides": [f.stem for f in files]}, indent=2))
    return work


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--theme", default="technical-swiss")
    p.add_argument("--deck", default="", help="render this deck's slides instead of the theme's templates")
    p.add_argument("--out", default="", help="output folder (default: references/templates, or "
                                             "<deck_dir>/build/anatomy with --deck)")
    p.add_argument("--only", default="", help="templates to render, by number or name: 03,key-number")
    p.add_argument("--chrome", default="", help="path to Chrome/Chromium (else CHROME_PATH, PATH)")
    p.add_argument("--budget", type=int, default=8000, help="Chrome virtual-time budget in ms")
    a = p.parse_args(argv)
    sys.stdout.reconfigure(line_buffering=True)      # keep stdout and stderr lines in order
    work = None
    try:
        if a.deck:
            if a.only:
                raise D.DeckError("--only selects templates; with --deck every slide is drawn")
            deck_dir = Path(a.deck)
            out = Path(a.out) if a.out else deck_dir / "build" / "anatomy"
        else:
            out = Path(a.out) if a.out else D.SKILL / "references" / "templates"
            work = Path(tempfile.mkdtemp(prefix="anatomy-"))
            deck_dir = template_deck(a.theme, work / "deck", a.only)
        out.mkdir(parents=True, exist_ok=True)
        a.deck_dir, a.slides = str(deck_dir), ""
        pngs, slides = D.cmd_png(a, quiet=True)
        deck = D.load_deck(deck_dir)
        tmp = Path(tempfile.mkdtemp(prefix="_anatomy-", dir=deck_dir / "build"))
        kicker = "SLIDE ANATOMY" if a.deck else "TEMPLATE ANATOMY"

        def draw(n: int) -> dict:
            return anatomy(a, deck, slides, n, tmp, out / f"{slides[n - 1][0]}-anatomy.png", kicker)

        try:
            with ThreadPoolExecutor(max_workers=4) as pool:
                reps = list(pool.map(draw, range(1, len(slides) + 1)))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        for png, (sid, _, _) in zip(pngs, slides):
            shutil.copy2(png, out / f"{sid}.png")
        warnings = []
        for rep in reps:
            auto = " (top-level blocks: no data-role)" if rep["auto"] else ""
            print(f"{rep['id']}: {len(rep['regions'])} region(s){auto}; content ends at y {rep['lowest']} of {rep['limit']}")
            for g in rep["regions"]:
                count = f" x{len(g['boxes'])}" if len(g["boxes"]) > 1 else ""
                b = g["boxes"][0]
                where = dict.fromkeys(f"cols {c}" if c else f"x {q[0]}-{q[2]} (off the column edges)"
                                      for c, q in zip(g["cols"], g["boxes"]))
                print(f"  {g['n']:>2} {g['role'] + count:<26} {b[2] - b[0]:>4} x {b[3] - b[1]:<4} {' · '.join(where)}")
            if not a.deck:
                warnings += cap_drift(rep)
        if not a.deck and not a.only:    # a partial run keeps the full gallery
            try:
                import contact_sheet
            except ImportError:
                raise D.DeckError("gallery.png needs Pillow (pip install pillow, or run scripts/setup.sh)")
            contact_sheet.sheet(deck_dir, out / "gallery.png")
        for f in [out / f"{sid}{x}.png" for sid, _, _ in slides for x in ("", "-anatomy")] + [out / "gallery.png"]:
            if f.is_file():
                compress(f, palette=not a.deck)
        for w in warnings:
            print(f"warning: {w}", file=sys.stderr)
        print(f"wrote {2 * len(slides)} PNG(s){' and gallery.png' if not (a.deck or a.only) else ''} to {out}")
        return 1 if warnings else 0
    except D.DeckError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    finally:
        if work:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
