"""Build the Mustard Bio logo (Calibrated mark + IBM Plex Sans wordmark with capsule o) as SVG.

    python build_logo.py            # writes ../logo/svg/*.svg

Geometry (units: font size 200, IBM Plex Sans cap height = 139.6):
  Mark      11 graduations, pitch 22; tick width 6; centre tick width 12 (the dose).
            Heights: 60,128,116,104,92,80,92,104,116,128,60 -> two straight lines meeting at the centre draw an M.
  Wordmark  "Mustard Bi" IBM Plex Sans Regular, tracking -10/1000.
  Capsule o outer ellipse semi-axes 0.2802 cap x 0.5248 cap, leaning 36.15 deg right,
            stroke 17 (IBM Plex Sans Regular round stroke), left edge 0.143 cap after the i,
            bottom 0.0226 cap below baseline.
  Lockup    mark height = 1.25 x cap height, centred on the cap band; gap = 0.62 x cap.
"""
import os
from kit import *

INK, PAPER = '#1C1B19', '#F2F0EA'

def mark():
    hs = [60, 128, 116, 104, 92, 80, 92, 104, 116, 128, 60]
    p = Path()
    for i, h in enumerate(hs):
        x = i * 22
        p.addPath(rect(x - 6, -h, 12, h) if i == 5 else rect(x - 3, -h, 6, h))
    return clean(p)

def wordmark():
    word, adv, gl = text('Mustard Bi', 'ibm-plex-sans', 400, 200, tracking=-10)
    cap = metrics('ibm-plex-sans', 400, 200)['cap']
    A, B, w, rot = 0.2802 * cap, 0.5248 * cap, 17.0, 36.15
    o = D(ellipse(0, 0, A, B, rot=rot), ellipse(0, 0, A - w, B - w, rot=rot))
    ob = o.bounds; i_right = max(g[1].bounds[2] for g in gl if g[0] == 'i')
    o = move(o, i_right + 0.143 * cap - ob[0], 0.0226 * cap - ob[3])
    return U(word, o), cap

def lockup():
    m = mark(); w, cap = wordmark()
    mb = m.bounds; s = 1.25 * cap / (mb[3] - mb[1])
    m = tf(m, sx=s, tx=-mb[0] * s)
    mb = m.bounds; m = move(m, 0, -cap / 2 - (mb[1] + mb[3]) / 2)
    w = move(w, mb[2] + 0.62 * cap - w.bounds[0], 0)
    return U(m, w)

def svg(p, fill, pad=0.18, title='Mustard Bio'):
    b = p.bounds; wd, ht = b[2] - b[0], b[3] - b[1]; px = ht * pad
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{b[0]-px:.3f} {b[1]-px:.3f} {wd+2*px:.3f} {ht+2*px:.3f}" '
            f'width="{wd+2*px:.0f}" height="{ht+2*px:.0f}"><title>{title}</title><path d="{d_of(p, 3)}" fill="{fill}"/></svg>')

if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logo', 'svg', 'generated')
    os.makedirs(out, exist_ok=True)
    L = lockup(); W, _ = wordmark(); M = mark()
    for name, p in [('primary', L), ('wordmark', W), ('icon', M)]:
        open(f'{out}/mustard-bio-logo-{name}.svg', 'w').write(svg(p, INK))
    open(f'{out}/mustard-bio-logo-white.svg', 'w').write(svg(L, '#FFFFFF'))
    print('written to', out)
