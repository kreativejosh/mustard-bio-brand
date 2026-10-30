"""Vector toolkit: font outlines (HarfBuzz shaping), geometry, curve-preserving booleans (Skia PathOps)."""
import math, os, functools
import pathops
from pathops import Path, PathOp, op
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
K = 0.5522847498

def font_path(family, weight):
    return f'{FS}/{family}-latin-{weight}-normal.woff'

@functools.lru_cache(None)
def load(family, weight):
    p = font_path(family, weight)
    tt = TTFont(p)
    import io
    buf = io.BytesIO(); tt.flavor = None; tt.save(buf); data = buf.getvalue()
    face = hb.Face(data); f = hb.Font(face)
    return tt, f, tt['head'].unitsPerEm

def text(s, family, weight, size, x=0, y=0, tracking=0, features=None):
    """Return (Path, advance) for text; y is baseline, SVG coords (y down). tracking in em/1000."""
    tt, f, upem = load(family, weight)
    if not s: return Path(), 0, []
    buf = hb.Buffer(); buf.add_str(s); buf.guess_segment_properties()
    hb.shape(f, buf, features or {"kern": True, "liga": True})
    gs = tt.getGlyphSet(); order = tt.getGlyphOrder()
    sc = size / upem; out = Path(); pen_x = 0
    glyphs = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        gx = x + (pen_x + pos.x_offset) * sc; gy = y - pos.y_offset * sc
        p = Path(); tp = TransformPen(p.getPen(glyphSet=gs), (sc, 0, 0, -sc, gx, gy))
        gs[name].draw(tp)
        glyphs.append((name, p, gx, (pos.x_advance) * sc))
        out.addPath(p)
        pen_x += pos.x_advance + tracking / 1000 * upem
    adv = (pen_x - tracking / 1000 * upem) * sc
    return clean(out), adv, glyphs

def metrics(family, weight, size):
    tt, f, upem = load(family, weight)
    os2 = tt['OS/2']; sc = size / upem
    return dict(xh=os2.sxHeight * sc, cap=os2.sCapHeight * sc, asc=tt['hhea'].ascent * sc, desc=-tt['hhea'].descent * sc)

def clean(p):
    q = Path(p); q.simplify(); return q

def U(*ps):
    out = Path()
    for p in ps:
        out = op(out, p, PathOp.UNION)
    return out

def D(a, b):
    return op(a, b, PathOp.DIFFERENCE)

def I(a, b):
    return op(a, b, PathOp.INTERSECTION)

def X(a, b):
    return op(a, b, PathOp.XOR)

def circle(cx, cy, r):
    p = Path(); k = K * r
    p.moveTo(cx + r, cy)
    p.cubicTo(cx + r, cy + k, cx + k, cy + r, cx, cy + r)
    p.cubicTo(cx - k, cy + r, cx - r, cy + k, cx - r, cy)
    p.cubicTo(cx - r, cy - k, cx - k, cy - r, cx, cy - r)
    p.cubicTo(cx + k, cy - r, cx + r, cy - k, cx + r, cy)
    p.close(); return p

def ellipse(cx, cy, rx, ry, rot=0):
    p = circle(0, 0, 1); return tf(p, sx=rx, sy=ry, rot=rot, tx=cx, ty=cy)

def rect(x, y, w, h, r=0):
    p = Path()
    if r <= 0:
        p.moveTo(x, y); p.lineTo(x + w, y); p.lineTo(x + w, y + h); p.lineTo(x, y + h); p.close(); return p
    k = K * r
    p.moveTo(x + r, y); p.lineTo(x + w - r, y); p.cubicTo(x + w - r + k, y, x + w, y + r - k, x + w, y + r)
    p.lineTo(x + w, y + h - r); p.cubicTo(x + w, y + h - r + k, x + w - r + k, y + h, x + w - r, y + h)
    p.lineTo(x + r, y + h); p.cubicTo(x + r - k, y + h, x, y + h - r + k, x, y + h - r)
    p.lineTo(x, y + r); p.cubicTo(x, y + r - k, x + r - k, y, x + r, y); p.close(); return p

def poly(pts):
    p = Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close(); return p

def arc_pts(cx, cy, r, a0, a1, n=None):
    """angles in degrees, SVG coords (y down), counter-clockwise visually means negative y."""
    n = n or max(8, int(abs(a1 - a0) / 3))
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy - r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

def arc_to(p, cx, cy, r, a0, a1, move=False):
    """Append true cubic arc (y-down svg, angles ccw visual). splits into <=90deg pieces."""
    segs = max(1, int(math.ceil(abs(a1 - a0) / 90 - 1e-9)))
    da = (a1 - a0) / segs
    def P(a): return (cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a)))
    if move: p.moveTo(*P(a0))
    for i in range(segs):
        s, e = a0 + i * da, a0 + (i + 1) * da
        k = 4 / 3 * math.tan(math.radians(e - s) / 4) * r
        x0, y0 = P(s); x3, y3 = P(e)
        # tangent directions (y-down): derivative of (cos, -sin) = (-sin, -cos)
        t0 = (-math.sin(math.radians(s)), -math.cos(math.radians(s)))
        t1 = (-math.sin(math.radians(e)), -math.cos(math.radians(e)))
        p.cubicTo(x0 + k * t0[0], y0 + k * t0[1], x3 - k * t1[0], y3 - k * t1[1], x3, y3)
    return p

def stroke(p, w, cap='round', join='round'):
    q = Path(p)
    caps = {'butt': pathops.LineCap.BUTT_CAP, 'round': pathops.LineCap.ROUND_CAP, 'square': pathops.LineCap.SQUARE_CAP}
    joins = {'miter': pathops.LineJoin.MITER_JOIN, 'round': pathops.LineJoin.ROUND_JOIN, 'bevel': pathops.LineJoin.BEVEL_JOIN}
    q.stroke(w, caps[cap], joins[join], 4)
    q.convertConicsToQuads(0.05)
    q.simplify(); return q

def open_path(pts):
    p = Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    return p

def tf(p, sx=1, sy=None, rot=0, tx=0, ty=0, ox=0, oy=0):
    sy = sx if sy is None else sy
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    # translate(-o) -> scale -> rotate -> translate(o + t)
    a, b, cc, d = sx * c, sx * s, -sy * s, sy * c
    e = -ox * a - oy * cc + ox + tx; f = -ox * b - oy * d + oy + ty
    q = Path(); p.draw(TransformPen(q.getPen(), (a, b, cc, d, e, f))); return q

def move(p, dx, dy):
    return tf(p, tx=dx, ty=dy)

def bounds(p):
    return p.bounds  # (xmin, ymin, xmax, ymax)

def d_of(p, prec=2):
    pen = SVGPathPen(None, ntos=lambda v: f'{v:.{prec}f}'.rstrip('0').rstrip('.'))
    p.draw(pen); return pen.getCommands()

def svg_path(p, fill='#1C1B19', extra=''):
    return f'<path d="{d_of(p)}" fill="{fill}" fill-rule="nonzero" {extra}/>'
