"""Mustard Bio 3D brand assets, packaging and stationery overview in Cycles. Usage: python assets.py <scene> <out.png> [w h spp]"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blib import *
from merch import catmull, flat_shape, ribbon, add_print, floor_paper, powder
from mathutils import Vector

ART = os.path.join(HERE, '..', 'render', 'art')
STAT = os.path.join(HERE, '..', 'render', 'stat')
LOGO = os.path.join(HERE, '..', 'render', 'logo')

def group(name, loc=(0, 0, 0), rot=(0, 0, 0)):
    objs = [o for o in bpy.context.scene.objects if o.parent is None and o.type in ('MESH', 'CURVE', 'META') and not o.get('placed') and o.name not in ('sweep', 'floor')]
    piv = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(piv)
    for o in objs: o.parent = piv; o['placed'] = True
    piv.location = loc; piv.rotation_euler = rot; return piv

def solidify(o, t, offset=-1):
    m = o.modifiers.new('sol', 'SOLIDIFY'); m.thickness = t; m.offset = offset; return o

def capsule_half(r, l, seg=96):
    """Hemispherical cap on a cylinder, open at z=0, pole at z=l+r."""
    prof = [(max(0.0001, r * math.sin(a)), l + r * math.cos(a)) for a in [i / 24 * math.pi / 2 for i in range(25)]] + [(r, 0.0)]
    return lathe('cap', prof, seg)

def lime_frost(name='frost'):
    m = mat(name, '#A7E26E', rough=0.32, trans=0.85, ior=1.45, coat=1.0, coat_rough=0.08, sss=0.0)
    return m

def thin_glass(name='glass', tint='#F4FBF5'):
    return glass(name, tint, rough=0.0, ior=1.5)

def studio_dark(color='#2c3d3e'):
    world_hdri('studio_small_09', 0.12, rot=0.5)
    sw = cyclorama(color, w=14, d=12, h=7, r=2.5, rough=0.6)
    area_light((0, 1.4, 0.6), (0, 6, 2.2), 4.0, 70, color='#cfe3cf')  # wash on the backdrop
    return sw

def studio_light(color='#E7E8E1'):
    world_hdri('studio_small_09', 0.16, rot=0.5)
    sw = cyclorama(color, w=14, d=12, h=7, r=2.5, rough=0.85)
    area_light((0, 1.4, 0.6), (0, 6, 2.2), 4.0, 90)  # lift the backdrop
    return sw

# ---------------- brand assets ----------------
def build_capsule(granules=160):
    r, l = 0.06, 0.07
    top = capsule_half(r, l); solidify(top, 0.0025); assign(top, thin_glass())
    bot = capsule_half(r * 1.015, l); bot.rotation_euler.x = math.pi; assign(bot, lime_frost())
    bpy.ops.mesh.primitive_circle_add(vertices=96, radius=r * 1.01, fill_type='NGON', location=(0, 0, -0.0008)); assign(bpy.context.object, lime_frost('seal'))
    bpy.ops.mesh.primitive_torus_add(major_radius=r * 1.016, minor_radius=0.0007, location=(0, 0, 0)); bpy.ops.object.shade_smooth(); assign(bpy.context.object, mat('band', '#222F30', rough=0.3))
    random.seed(4); cols = ['#FFFFFF', '#CEF79E', '#A7E26E', '#F7F7F5', '#C9CBBE']
    mats = [mat('g' + c, c, rough=0.55, sheen=0.3) for c in cols]
    n = 0; tries = 0; placed = []
    while n < granules and tries < 20000:
        tries += 1
        p = Vector(((random.random() * 2 - 1) * r * 0.85, (random.random() * 2 - 1) * r * 0.85, random.random() * (l + r * 0.7)))
        zz = max(0, p.z - l)
        if p.x ** 2 + p.y ** 2 + zz ** 2 > (r * 0.86) ** 2: continue
        rad = 0.0055 + random.random() * 0.003
        if any((p - q).length < rad + qr for q, qr in placed): continue
        placed.append((p, rad))
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=rad, location=p); g = bpy.context.object
        g.scale = (1, 1, 0.8 + random.random() * 0.3); g.rotation_euler = (random.random() * 3, random.random() * 3, 0); bpy.ops.object.shade_smooth()
        assign(g, mats[n % len(mats)]); n += 1
    return group('capsule', (0, 0, 0.16), (0.35, 0, -math.radians(36.15)))

def scene_capsule(out, w, h, spp, dark=True):
    reset(w, h, spp)
    (studio_dark() if dark else studio_light())
    build_capsule()
    area_light((-0.5, -0.4, 0.6), (0, 0, 0.16), 0.5, 22 if dark else 18)
    area_light((0.6, 0.3, 0.45), (0, 0, 0.16), 0.3, 14 if dark else 8, size_y=0.9)
    area_light((0.0, 0.6, 0.6), (0, 0, 0.1), 0.6, 10 if dark else 6)
    camera((0.0, -1.05, 0.24), (0.0, 0.0, 0.16), 85, dof=True, fstop=8)
    render(out)

def scene_mark(out, w, h, spp, dark=True):
    reset(w, h, spp)
    (studio_dark('#26393a') if dark else studio_light())
    hs = [60, 128, 116, 104, 92, 80, 92, 104, 116, 128, 60]; k = 0.0012
    for i, hh in enumerate(hs):
        wd = (12 if i == 5 else 6) * k * 2.2; H = hh * k; D = 0.05
        bpy.ops.mesh.primitive_cube_add(size=1, location=((i - 5) * 22 * k, 0, H / 2 + 0.008)); o = bpy.context.object; o.scale = (wd, D, H)
        bpy.ops.object.transform_apply(scale=True); bevel(o, min(wd, D) * 0.3, 4); bpy.ops.object.shade_smooth()
        assign(o, lime_frost('dose') if i == 5 else glass('g', '#F2FBF4'))
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.004)); pl = bpy.context.object; pl.scale = (0.34, 0.12, 0.008); bpy.ops.object.transform_apply(scale=True); bevel(pl, 0.002, 4)
    assign(pl, mat('plinth', '#1d2829' if dark else '#FFFFFF', rough=0.45, coat=0.3, coat_rough=0.2))
    group('mark', (0, 0, 0), (0, 0, -0.42))
    area_light((-0.5, -0.3, 0.5), (0, 0, 0.08), 0.5, 20)
    area_light((0.5, 0.4, 0.35), (0, 0, 0.08), 0.15, 12, size_y=0.8)
    area_light((0.0, 0.5, 0.15), (0, 0, 0.08), 0.6, 8)
    camera((0.0, -0.72, 0.2), (0.0, 0.0, 0.07), 70, dof=True, fstop=8)
    render(out)

def scene_flask(out, w, h, spp):
    reset(w, h, spp)
    studio_light('#E9EBE6')
    rb, hb, rn, hn = 0.07, 0.11, 0.018, 0.06
    prof = [(0.0001, 0.0), (rb - 0.008, 0.0), (rb, 0.007)] + [(rb + (rn - rb) * t, 0.007 + (hb - 0.007) * t) for t in [i / 12 for i in range(1, 13)]]
    prof += [(rn, hb + hn), (rn + 0.003, hb + hn + 0.002), (rn + 0.0015, hb + hn + 0.005)]
    f = lathe('flask', prof, 128); solidify(f, 0.0016); assign(f, glass('fg', '#F4FBF5'))
    lev = 0.045; rAt = lambda y: rb + (rn - rb) * ((y - 0.007) / (hb - 0.007))
    lq = [(0.0001, 0.0018), (rb - 0.009, 0.0018), (rb - 0.0016, 0.0075), (rAt(lev) - 0.0016, lev), (0.0001, lev)]
    liq = lathe('liq', lq, 128); assign(liq, glass('liquid', '#E9FCD5', ior=1.34, absorb='#9fd36b', dens=18))
    # printed graduations (white enamel) facing camera
    for i in range(9):
        y = 0.022 + i * 0.0085; r = rAt(y) + 0.0002; slope = math.atan((rb - rn) / (hb - 0.007))
        wd = 0.024 if i == 4 else (0.01 if i % 2 else 0.016); th = 0.0014 if i == 4 else 0.0008
        bpy.ops.mesh.primitive_cube_add(size=1); t = bpy.context.object; t.scale = (wd, 0.0004, th)
        t.location = (-0.012 + wd / 2, -r * math.cos(0) , y); t.rotation_euler.x = slope
        assign(t, mat('enamel', '#A7E26E' if i == 4 else '#FFFFFF', rough=0.35))
    group('flask', (0, 0, 0), (0, 0, 0.2))
    area_light((-0.45, -0.35, 0.45), (0, 0, 0.07), 0.45, 16)
    area_light((0.5, 0.1, 0.3), (0, 0, 0.07), 0.12, 10, size_y=0.6)
    area_light((0.0, 0.5, 0.5), (0, 0, 0.06), 0.6, 10)
    camera((0.0, -0.78, 0.15), (0.0, 0.0, 0.085), 85, dof=True, fstop=8)
    render(out)

def scene_tubes(out, w, h, spp):
    reset(w, h, spp)
    studio_dark('#2f4142')
    fills = [0.42, 0.6, 0.78, 0.6]; cols = ['#CEF79E', '#A7E26E', '#EEF3E2', '#C9CBBE']
    r, H = 0.008, 0.15
    for i, (fl, col) in enumerate(zip(fills, cols)):
        x = (i - 1.5) * 0.028
        prof = [(r * math.sin(a), r - r * math.cos(a)) for a in [k / 12 * math.pi / 2 for k in range(13)]] + [(r, H), (r * 1.1, H + 0.001)]
        t = lathe('tube', prof, 96); solidify(t, 0.0006); assign(t, glass('tg', '#F4FBF5')); t.location.x = x
        lp = [(r * 0.9 * math.sin(a), 0.0007 + r * 0.9 - r * 0.9 * math.cos(a)) for a in [k / 12 * math.pi / 2 for k in range(13)]] + [(r * 0.9, H * fl), (0.0001, H * fl)]
        lq = lathe('liq', lp, 96); assign(lq, glass('lq' + col, '#FFFFFF', ior=1.34, absorb=col, dens=60)); lq.location.x = x
        # liquid also gets a little colour so it reads
        lq.data.materials[0].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = hexc(col)
    rk = mat('rack', '#222F30', rough=0.35, coat=0.6)
    for z, d in [(0.0, 0.04), (0.06, 0.03)]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z + 0.002)); p = bpy.context.object; p.scale = (0.135, d, 0.004); bpy.ops.object.transform_apply(scale=True); bevel(p, 0.001, 3); assign(p, rk)
    for x in (-0.065, 0.065):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 0.032)); s = bpy.context.object; s.scale = (0.004, 0.03, 0.064); bpy.ops.object.transform_apply(scale=True); bevel(s, 0.001, 3); assign(s, rk)
    group('tubes', (0, 0, 0.0), (0, 0, 0.12))
    area_light((0.0, 0.2, 0.55), (0, 0, 0.05), 0.25, 14, shape='DISK')
    area_light((-0.4, -0.3, 0.25), (0, 0, 0.06), 0.3, 6)
    area_light((0.4, -0.2, 0.2), (0, 0, 0.06), 0.15, 5, size_y=0.6)
    camera((0.0, -0.62, 0.14), (0.0, 0.0, 0.08), 85, dof=True, fstop=8)
    render(out)

def scene_helix(out, w, h, spp):
    reset(w, h, spp)
    studio_light('#EEEFEA')
    N, R, pitch, turn = 12, 0.05, 0.022, 0.55
    gm = glass('hg', '#EEF7F1'); cores = ['#445E5F', '#222F30', '#A7E26E', '#445E5F']
    pts = [[], []]
    for i in range(N):
        y = (i - (N - 1) / 2) * pitch; a = i * turn
        for s_ in range(2):
            aa = a + s_ * math.pi; p = Vector((R * math.cos(aa), R * math.sin(aa), y)); pts[s_].append(p)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.012, segments=48, ring_count=24, location=p); bpy.ops.object.shade_smooth(); assign(bpy.context.object, gm)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0055, segments=32, ring_count=16, location=p); bpy.ops.object.shade_smooth()
            assign(bpy.context.object, mat('core' + str((i + s_ * 2) % 4), cores[(i + s_ * 2) % 4], rough=0.15, coat=1.0))
        a0, a1 = pts[0][i], pts[1][i]; d = a1 - a0
        bpy.ops.mesh.primitive_cylinder_add(radius=0.0016, depth=d.length - 0.024, location=(a0 + a1) / 2); c = bpy.context.object
        c.rotation_euler = d.to_track_quat('Z', 'Y').to_euler(); assign(c, gm)
    for P in pts:
        cu = bpy.data.curves.new('s', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.0028; cu.bevel_resolution = 6
        sp = cu.splines.new('NURBS'); sp.points.add(len(P) - 1)
        for i, p in enumerate(P): sp.points[i].co = (*p, 1)
        sp.order_u = 4; sp.use_endpoint_u = True; o = bpy.data.objects.new('strand', cu); bpy.context.scene.collection.objects.link(o); cu.materials.append(gm)
    group('helix', (0, 0, 0.17), (0.12, 0.42, 0.0))
    area_light((-0.5, -0.4, 0.6), (0, 0, 0.17), 0.5, 18)
    area_light((0.5, 0.2, 0.4), (0, 0, 0.17), 0.2, 10, size_y=0.8)
    area_light((0.0, 0.6, 0.5), (0, 0, 0.15), 0.6, 10)
    camera((0.0, -0.95, 0.2), (0.0, 0.0, 0.17), 70, dof=True, fstop=8)
    render(out)

def scene_blob(out, w, h, spp):
    reset(w, h, spp)
    studio_light('#E4EAD9')
    mb = bpy.data.metaballs.new('mb'); mb.resolution = 0.003; mb.render_resolution = 0.0015
    o = bpy.data.objects.new('blob', mb); bpy.context.scene.collection.objects.link(o)
    random.seed(9)
    for p, r in [((0, 0, 0), 0.05), ((0.045, 0.01, 0.025), 0.035), ((-0.04, -0.01, 0.03), 0.03), ((0.02, 0.0, -0.045), 0.032), ((-0.06, 0.01, -0.03), 0.024), ((0.075, 0.0, -0.01), 0.02)]:
        e = mb.elements.new(); e.co = p; e.radius = r; e.stiffness = 2.2
    m = mat('blobm', '#CEF79E', rough=0.08, trans=0.9, ior=1.4, coat=1.0, coat_rough=0.02)
    b = m.node_tree.nodes['Principled BSDF']
    try: b.inputs['Thin Film Thickness'].default_value = 380; b.inputs['Thin Film IOR'].default_value = 1.33
    except Exception: pass
    mb.materials.append(m); o.location = (0, 0, 0.13)
    area_light((-0.5, -0.4, 0.6), (0, 0, 0.13), 0.5, 16)
    area_light((0.5, 0.2, 0.35), (0, 0, 0.13), 0.2, 10, size_y=0.8)
    area_light((0.0, 0.6, 0.4), (0, 0, 0.12), 0.6, 9)
    camera((0.0, -0.7, 0.16), (0.0, 0.0, 0.13), 85, dof=True, fstop=8)
    render(out)

def scene_tablets(out, w, h, spp):
    reset(w, h, spp)
    world_hdri('studio_small_09', 0.12, rot=0.5); floor_paper('#E4E5DE')
    random.seed(3); placed = []
    tp = [(0.0001, -0.0028)] + [(0.0055 - 0.0028 + 0.0028 * math.cos(a), 0.0028 * math.sin(a)) for a in [-math.pi / 2 + k / 12 * math.pi for k in range(13)]] + [(0.0001, 0.0028)]
    caps = [('#222F30', '#F7F7F5'), ('#A7E26E', '#FFFFFF'), ('#445E5F', '#CEF79E'), ('#F7F7F5', '#C9CBBE')]
    for i in range(34):
        isCap = i % 3 != 2; rr = 0.012 if isCap else 0.007
        for _ in range(80):
            x, y = (random.random() - 0.5) * 0.15, (random.random() - 0.5) * 0.11
            if all(math.hypot(x - a, y - b) > rr + c for a, b, c in placed): break
        else: continue
        placed.append((x, y, rr))
        if isCap:
            a, b = caps[i % 4]
            h1 = capsule_half(0.0035, 0.0075, 48); assign(h1, mat('c' + a, a, rough=0.25, coat=1.0, coat_rough=0.08))
            h2 = capsule_half(0.00362, 0.0068, 48); h2.rotation_euler.x = math.pi; assign(h2, mat('c' + b, b, rough=0.25, coat=1.0, coat_rough=0.08))
            group('cap', (x, y, 0.0036), (0, math.pi / 2, random.random() * 6.28))
        else:
            t = lathe('tab', tp, 64); assign(t, mat('tab' + str(i % 2), '#FFFFFF' if i % 2 else '#E3F5C8', rough=0.6, sss=0.05))
            # score line
            bpy.ops.mesh.primitive_cube_add(size=1); sc = bpy.context.object; sc.scale = (0.0105, 0.0006, 0.0006); sc.location = (0, 0, 0.0029); assign(sc, mat('score', '#d8dcd2', rough=0.7))
            group('tab', (x, y, 0.0028), (0, 0, random.random() * 6.28))
    area_light((-0.35, 0.25, 0.4), (0, 0, 0), 0.35, 12)
    area_light((0.35, -0.3, 0.45), (0, 0, 0), 0.5, 3)
    camera((0.0, -0.07, 0.2), (0.0, 0.0, 0.0), 50, dof=True, fstop=32)
    render(out)

# ---------------- packaging ----------------
def carton(W, H, D, front, side, end, top):
    bpy.ops.mesh.primitive_cube_add(size=1); o = bpy.context.object; o.scale = (W, D, H); bpy.ops.object.transform_apply(scale=True)
    me = o.data; uvl = me.uv_layers.active; mats = {}
    def m(key, img, rot=False):
        if key not in mats:
            mm = decal_mat('ct' + key, img, rough=0.38, coat=0.35, paper_bump=0.08)[0]; me.materials.append(mm); mats[key] = (len(me.materials) - 1, rot)
        return mats[key]
    for p in me.polygons:
        n = p.normal
        if n.y < -0.9: key, img, ax = 'front', front, ('x', 'z', W, H, False)
        elif n.y > 0.9: key, img, ax = 'back', front, ('x', 'z', W, H, True)
        elif n.z > 0.9: key, img, ax = 'top', side, ('x', 'y', W, D, False)
        elif n.z < -0.9: key, img, ax = 'bot', top, ('x', 'y', W, D, True)
        else: key, img, ax = 'end', end, ('y', 'z', D, H, n.x < 0)
        idx, _ = m(key, img); p.material_index = idx
        for li in p.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co
            a = getattr(v, ax[0]) / ax[2] + 0.5; b = getattr(v, ax[1]) / ax[3] + 0.5
            if ax[4]: a = 1 - a
            uvl.data[li].uv = (a, b) if ax[0] != 'y' else (b, a)
    bevel(o, 0.0006, 2); return o

def blister(n_rows=2, n_cols=5, foil_img=None, flipped=False):
    W, H = 0.095, 0.046
    bpy.ops.mesh.primitive_cube_add(size=1); pl = bpy.context.object; pl.scale = (W, H, 0.0006); bpy.ops.object.transform_apply(scale=True); bevel(pl, 0.0002, 2)
    if flipped and foil_img:
        assign(pl, mat('alu', '#D6DBD9', rough=0.25, metal=1.0)); me = pl.data
        fm = decal_mat('foilprint', foil_img, rough=0.25, metal=0.6)[0]; me.materials.append(fm); uvl = me.uv_layers.active
        for p in me.polygons:
            if p.normal.z > 0.9:
                p.material_index = 1
                for li in p.loop_indices:
                    v = me.vertices[me.loops[li].vertex_index].co; uvl.data[li].uv = (v.x / W + 0.5, v.y / H + 0.5)
        return pl
    assign(pl, mat('alu', '#B4BAB8', rough=0.32, metal=1.0))
    pvc = glass('pvc', '#FFFFFF', rough=0.05, ior=1.45)
    for r_ in range(n_rows):
        for c in range(n_cols):
            x, y = -W / 2 + W / (n_cols * 2) + c * W / n_cols, -H / 2 + H / (n_rows * 2) + r_ * H / n_rows
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0068, segments=48, ring_count=16, location=(x, y, 0.0003)); b = bpy.context.object
            b.scale.z = 0.55; bpy.ops.object.shade_smooth(); solidify(b, 0.00025)
            bm_ = bmesh.new(); bm_.from_mesh(b.data); bmesh.ops.delete(bm_, geom=[v for v in bm_.verts if v.co.z < -0.0001], context='VERTS'); bm_.to_mesh(b.data); bm_.free()
            assign(b, pvc)
            if not (r_ == 1 and c == n_cols - 1):
                bpy.ops.mesh.primitive_cylinder_add(radius=0.0052, depth=0.0028, location=(x, y, 0.0018)); t = bpy.context.object; bevel(t, 0.0009, 3); bpy.ops.object.shade_smooth()
                assign(t, mat('tabw', '#FFFFFF', rough=0.6))
    return pl

def scene_pack(out, w, h, spp):
    reset(w, h, spp)
    world_hdri('studio_small_09', 0.08, rot=0.5); cyclorama('#C9CBBE', w=14, d=12, h=7, r=2.5)
    W, H, D = 0.1, 0.062, 0.024
    carton(W, H, D, os.path.join(ART, 'carton-front.png'), os.path.join(ART, 'carton-side.png'), os.path.join(ART, 'carton-end.png'), os.path.join(ART, 'carton-top.png'))
    group('box', (-0.03, 0.03, H / 2), (0, 0, 0.18))
    carton(W, H, D, os.path.join(ART, 'carton-front.png'), os.path.join(ART, 'carton-side.png'), os.path.join(ART, 'carton-end.png'), os.path.join(ART, 'carton-top.png'))
    group('box2', (0.085, 0.07, D / 2), (math.pi / 2, 0, -0.35))
    blister(); group('bl', (0.03, -0.045, 0.0003), (0, 0, -0.12))
    blister(foil_img=os.path.join(ART, 'blister-foil.png'), flipped=True); group('bl2', (-0.085, -0.03, 0.0003), (0, 0, 0.22))
    for x, y in [(0.095, -0.07), (0.106, -0.058), (-0.03, -0.088)]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.0052, depth=0.0028, location=(x, y, 0.0014)); t = bpy.context.object; bevel(t, 0.0009, 3); bpy.ops.object.shade_smooth(); assign(t, mat('tabw', '#FFFFFF', rough=0.6))
    area_light((-0.45, -0.35, 0.5), (0, 0, 0.02), 0.5, 7)
    area_light((0.5, 0.0, 0.3), (0, 0, 0.02), 0.2, 2.5, size_y=0.8)
    area_light((0.0, 0.6, 0.5), (0, 0, 0.02), 0.6, 3)
    camera((0.01, -0.5, 0.25), (0.01, 0.01, 0.02), 70, dof=True, fstop=32)
    render(out)

# ---------------- stationery overview: straight top-down, nothing skewed ----------------
def scene_stationery(out, w, h, spp):
    reset(w, h, spp)
    world_hdri('studio_small_09', 0.12, rot=0.5); floor_paper('#DCDDD5')
    S = lambda n: os.path.join(STAT, n + '.png')
    T = 0.0004
    items = [  # (file, w mm, h mm, x mm, y mm, thickness, edge colour)
        ('letterhead', 210, 297, -335, 60, T, '#ffffff'),
        ('continuation-sheet', 210, 297, -105, 60, T, '#ffffff'),
        ('invoice', 210, 297, 125, 60, T, '#ffffff'),
        ('report-cover', 210, 297, 355, 60, 0.0012, '#F7F7F5'),
        ('compliments-slip', 210, 99, -335, -165, T, '#ffffff'),
        ('envelope-dl', 220, 110, -100, -170, 0.0015, '#ffffff'),
        ('notebook-cover', 148, 210, 120 - 22, -185 + 30, 0.012, '#222F30'),
        ('business-card-front', 85, 55, 235, -140, 0.0006, '#222F30'),
        ('business-card-back', 85, 55, 235, -210, 0.0006, '#F7F7F5'),
        ('staff-id-front', 54, 86, 335, -170, 0.0008, '#ffffff'),
        ('visitor-pass', 54, 86, 400, -170, 0.0008, '#A7E26E'),
    ]
    for f, wmm, hmm, x, y, t, edge in items:
        c = card(f, wmm / 1000, hmm / 1000, t, S(f), None, edge=edge, rough=0.75 if t < 0.001 else 0.4, coat=0.0 if t < 0.001 else 0.4, paper_bump=0.15)
        c.location = (x / 1000, y / 1000, t / 2)
    # pen aligned to grid
    bpy.ops.mesh.primitive_cylinder_add(radius=0.0045, depth=0.14, location=(0.0, 0.0, 0.0045), rotation=(0, math.pi / 2, 0)); p = bpy.context.object
    p.location = (0.205, -0.255, 0.0045); bevel(p, 0.001, 3); bpy.ops.object.shade_smooth(); assign(p, mat('pen', '#222F30', rough=0.2, coat=1.0))
    area_light((-0.9, 0.7, 1.1), (0, 0, 0), 1.0, 45)
    area_light((0.9, -0.6, 1.2), (0, 0, 0), 1.4, 8)
    cam = ortho_camera((0.03, -0.05, 1.5), (0.03, -0.05, 0.0), 0.98)
    render(out)

# ---------------- stationery close-ups: top-down, square-on, framed so type is legible ----------------
CLOSE = {  # name: (frame width m, centre x m, centre y m, [(file, w mm, h mm, x mm, y mm, thickness m, edge colour)])
    'cards':   (0.215, 0.0, 0.0, [('business-card-front', 85, 55, -50, 0, 0.0006, '#222F30'), ('business-card-back', 85, 55, 50, 0, 0.0006, '#F7F7F5')]),
    'letter':  (0.5, 0.0, 0.0, [('letterhead', 210, 297, -114, 0, 0.0004, '#ffffff'), ('continuation-sheet', 210, 297, 114, 0, 0.0004, '#ffffff')]),
    'finance': (0.5, 0.0, 0.0, [('invoice', 210, 297, -114, 0, 0.0004, '#ffffff'), ('document-template', 210, 297, 114, 0, 0.0004, '#ffffff')]),
    'report':  (0.62, -0.03, 0.0, [('report-cover', 210, 297, -200, 0, 0.0012, '#F7F7F5'), ('notebook-cover', 148, 210, -10, 0, 0.012, '#222F30'), ('notepad', 148, 210, 160, 0, 0.004, '#ffffff')]),
    'post':    (0.64, 0.01, 0.0, [('compliments-slip', 210, 99, -180, 70, 0.0004, '#ffffff'), ('envelope-dl', 220, 110, -175, -70, 0.0015, '#ffffff'), ('envelope-c4', 324, 229, 135, 0, 0.002, '#222F30')]),
    'id':      (0.3, 0.012, 0.0, [('staff-id-front', 54, 86, -95, 20, 0.0008, '#ffffff'), ('staff-id-back', 54, 86, -35, 20, 0.0008, '#F7F7F5'), ('visitor-pass', 54, 86, 25, 20, 0.0008, '#A7E26E'), ('sticker-sheet', 105, 148, 110, 0, 0.0004, '#F7F7F5')]),
    'folder':  (0.52, 0.0, 0.0, [('presentation-folder', 440, 310, 0, 0, 0.0015, '#222F30')]),
}

def scene_stat_close(out, w, h, spp, name):
    reset(w, h, spp)
    world_hdri('studio_small_09', 0.12, rot=0.5); floor_paper('#DCDDD5')
    fw, cx, cy, items = CLOSE[name]
    S = lambda n: os.path.join(STAT, n + '.png')
    for f, wmm, hmm, x, y, t, edge in items:
        c = card(f, wmm / 1000, hmm / 1000, t, S(f), None, edge=edge, rough=0.75 if t < 0.001 else 0.4, coat=0.0 if t < 0.001 else 0.4, paper_bump=0.12)
        c.location = (x / 1000, y / 1000, t / 2)
    k = fw / 0.98  # keep light falloff consistent with frame size
    area_light((cx - 0.9 * k, cy + 0.7 * k, 1.1 * k), (cx, cy, 0), 1.0 * k, 45 * k * k)
    area_light((cx + 0.9 * k, cy - 0.6 * k, 1.2 * k), (cx, cy, 0), 1.4 * k, 8 * k * k)
    ortho_camera((cx, cy, 1.5), (cx, cy, 0.0), fw)
    render(out)

for _n in CLOSE:
    SCENES_EXTRA = globals().setdefault('SCENES_EXTRA', {})
    SCENES_EXTRA['stat-' + _n] = (lambda n: (lambda o, w, h, s: scene_stat_close(o, w, h, s, n)))(_n)

SCENES = {
    'capsule-dark': lambda o, w, h, s: scene_capsule(o, w, h, s, True),
    'capsule-light': lambda o, w, h, s: scene_capsule(o, w, h, s, False),
    'mark-dark': lambda o, w, h, s: scene_mark(o, w, h, s, True),
    'mark-light': lambda o, w, h, s: scene_mark(o, w, h, s, False),
    'flask': scene_flask, 'tubes': scene_tubes, 'helix': scene_helix, 'blob': scene_blob, 'tablets': scene_tablets,
    'pack': scene_pack, 'stationery': scene_stationery,
}
SCENES.update(SCENES_EXTRA)

if __name__ == '__main__':
    a = sys.argv[1:]
    name, out = a[0], a[1]; w, h, spp = (int(a[2]), int(a[3]), int(a[4])) if len(a) > 4 else (1600, 1200, 192)
    SCENES[name](out, w, h, spp)
