"""Mustard Bio merch, rendered in Cycles. Usage: python merch.py <scene> <out.png> [w h samples]"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blib import *
from mathutils import Vector

DEC = os.path.join(HERE, '..', 'render', 'decal')
ARTD = os.path.join(HERE, '..', 'render', 'art')
STAT = os.path.join(HERE, '..', 'render', 'stat')

def catmull(pts, n=8, closed=True):
    out = []; P = pts; L = len(P)
    rng = range(L) if closed else range(L - 1)
    for i in rng:
        p0, p1, p2, p3 = P[(i - 1) % L], P[i], P[(i + 1) % L], P[(i + 2) % L]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in range(2)))
    return out

def flat_shape(name, outline, thick=0.012, voxel=0.0035, smooth_iter=12):
    """2D outline -> soft fabric slab with rounded rolled edges (voxel remesh + smooth)."""
    bm = bmesh.new(); vs = [bm.verts.new((x, y, 0)) for x, y in outline]; f = bm.faces.new(vs)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    sol = o.modifiers.new('sol', 'SOLIDIFY'); sol.thickness = thick; sol.offset = 0
    bpy.ops.object.modifier_apply(modifier='sol')
    rm = o.modifiers.new('rm', 'REMESH'); rm.mode = 'VOXEL'; rm.voxel_size = voxel
    bpy.ops.object.modifier_apply(modifier='rm')
    sm = o.modifiers.new('sm', 'SMOOTH'); sm.factor = 0.8; sm.iterations = smooth_iter
    bpy.ops.object.modifier_apply(modifier='sm')
    for p in o.data.polygons: p.use_smooth = True
    o.select_set(False)
    return o

def displace(o, tex_type='CLOUDS', size=0.25, strength=0.006, depth=2, basis='BLENDER_ORIGINAL', coords='OBJECT', direction='Z', mid=0.5, **kw):
    t = bpy.data.textures.new('d' + tex_type, tex_type)
    if hasattr(t, 'noise_scale'): t.noise_scale = size
    if hasattr(t, 'noise_depth'): t.noise_depth = depth
    if hasattr(t, 'noise_basis'): t.noise_basis = basis
    for k, v in kw.items(): setattr(t, k, v)
    m = o.modifiers.new('disp', 'DISPLACE'); m.texture = t; m.strength = strength; m.texture_coords = coords; m.direction = direction; m.mid_level = mid
    return m

def fabric_mat(name, color, tex='cotton_jersey', scale=7.0, bump=0.7, sheen=0.7, decal=None, dc=(0, 0), dw=0.2, print_rough=0.55, print_bump=0.25):
    """Knit fabric (scanned normal/rough) tinted to colour; optional screen print mapped from object XY."""
    d = os.path.join(PH, 'tex', tex)
    m = mat(name, color, rough=0.95, sheen=sheen); nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Sheen Roughness'].default_value = 0.45
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (scale, scale, scale)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    # knit relief from the scanned height map (bump needs no UV tangents; remeshed cloth has no UVs)
    nn = nt.nodes.new('ShaderNodeTexImage'); nn.image = bpy.data.images.load(os.path.join(d, 'disp.jpg'), check_existing=True); nn.image.colorspace_settings.name = 'Non-Color'
    nn.projection = 'BOX'; nn.projection_blend = 0.3
    nt.links.new(mp.outputs['Vector'], nn.inputs['Vector'])
    nm = nt.nodes.new('ShaderNodeBump'); nm.inputs['Strength'].default_value = min(1.0, bump); nm.inputs['Distance'].default_value = 0.0006
    nt.links.new(nn.outputs['Color'], nm.inputs['Height'])
    # subtle colour variation from the scan's diffuse (melange)
    dn = nt.nodes.new('ShaderNodeTexImage'); dpath = os.path.join(d, 'diff.jpg'); dpath = dpath if os.path.exists(dpath) else os.path.join(PH, 'tex', 'cotton_jersey', 'diff.jpg'); dn.image = bpy.data.images.load(dpath, check_existing=True); dn.projection = 'BOX'
    nt.links.new(mp.outputs['Vector'], dn.inputs['Vector'])
    bw = nt.nodes.new('ShaderNodeRGBToBW'); nt.links.new(dn.outputs['Color'], bw.inputs['Color'])
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 0.86; mr.inputs['To Max'].default_value = 1.06
    nt.links.new(bw.outputs['Val'], mr.inputs['Value'])
    tint = nt.nodes.new('ShaderNodeMix'); tint.data_type = 'RGBA'; tint.blend_type = 'MULTIPLY'; tint.inputs['Factor'].default_value = 1
    tint.inputs['A'].default_value = hexc(color); nt.links.new(mr.outputs['Result'], tint.inputs['B'])
    col_out = tint.outputs['Result']; normal_out = nm.outputs['Normal']; rough_val = None
    if decal:
        im = nt.nodes.new('ShaderNodeTexImage'); im.image = bpy.data.images.load(decal, check_existing=True); im.extension = 'CLIP'; im.interpolation = 'Cubic'
        aspect = im.image.size[1] / im.image.size[0]
        mp2 = nt.nodes.new('ShaderNodeMapping'); mp2.vector_type = 'POINT'
        mp2.inputs['Location'].default_value = (0.5 - dc[0] / dw, 0.5 - dc[1] / (dw * aspect), 0)
        mp2.inputs['Scale'].default_value = (1 / dw, 1 / (dw * aspect), 1)
        nt.links.new(tc.outputs['Object'], mp2.inputs['Vector']); nt.links.new(mp2.outputs['Vector'], im.inputs['Vector'])
        # print only on the upward-facing side
        geo = nt.nodes.new('ShaderNodeNewGeometry'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(geo.outputs['Normal'], sep.inputs['Vector'])
        up = nt.nodes.new('ShaderNodeMath'); up.operation = 'GREATER_THAN'; up.inputs[1].default_value = 0.2; nt.links.new(sep.outputs['Z'], up.inputs[0])
        a = nt.nodes.new('ShaderNodeMath'); a.operation = 'MULTIPLY'; nt.links.new(im.outputs['Alpha'], a.inputs[0]); nt.links.new(up.outputs['Value'], a.inputs[1])
        # ink sits on the knit: knit texture breaks it up slightly
        brk = nt.nodes.new('ShaderNodeMath'); brk.operation = 'MULTIPLY'; nt.links.new(a.outputs['Value'], brk.inputs[0])
        mr2 = nt.nodes.new('ShaderNodeMapRange'); mr2.inputs['From Min'].default_value = 0.2; mr2.inputs['From Max'].default_value = 0.6; mr2.inputs['To Min'].default_value = 0.8; mr2.inputs['To Max'].default_value = 1.0
        nt.links.new(bw.outputs['Val'], mr2.inputs['Value']); nt.links.new(mr2.outputs['Result'], brk.inputs[1])
        mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
        nt.links.new(brk.outputs['Value'], mix.inputs['Factor']); nt.links.new(col_out, mix.inputs['A']); nt.links.new(im.outputs['Color'], mix.inputs['B'])
        col_out = mix.outputs['Result']
        rmix = nt.nodes.new('ShaderNodeMix'); rmix.data_type = 'FLOAT'; rmix.inputs['A'].default_value = 0.95; rmix.inputs['B'].default_value = print_rough
        nt.links.new(brk.outputs['Value'], rmix.inputs['Factor']); nt.links.new(rmix.outputs['Result'], b.inputs['Roughness'])
        sh = nt.nodes.new('ShaderNodeMix'); sh.data_type = 'FLOAT'; sh.inputs['A'].default_value = sheen; sh.inputs['B'].default_value = 0.05
        nt.links.new(brk.outputs['Value'], sh.inputs['Factor']); nt.links.new(sh.outputs['Result'], b.inputs['Sheen Weight'])
        bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = print_bump; bp.inputs['Distance'].default_value = 0.0004
        nt.links.new(brk.outputs['Value'], bp.inputs['Height']); nt.links.new(nm.outputs['Normal'], bp.inputs['Normal'])
        normal_out = bp.outputs['Normal']
    nt.links.new(col_out, b.inputs['Base Color']); nt.links.new(normal_out, b.inputs['Normal'])
    return m

def tube_along(name, pts, radius, material, z=0.0, flatten=1.0, closed=False):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = radius; cu.bevel_resolution = 4; cu.use_fill_caps = True
    sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
    for i, (x, y) in enumerate(pts): sp.points[i].co = (x, y, z, 1)
    sp.use_cyclic_u = closed
    o = bpy.data.objects.new(name, cu); bpy.context.scene.collection.objects.link(o); o.scale.z = flatten
    o.data.materials.append(material); return o

def tee_outline():
    half = [(0.0, 0.372), (0.06, 0.368), (0.098, 0.358), (0.16, 0.345), (0.232, 0.322), (0.30, 0.268), (0.372, 0.205), (0.405, 0.172),
            (0.368, 0.118), (0.33, 0.082), (0.268, 0.122), (0.262, 0.05), (0.264, -0.12), (0.268, -0.30), (0.272, -0.372), (0.14, -0.376), (0.0, -0.377)]
    full = half + [(-x, y) for x, y in reversed(half[1:-1])]
    return catmull(full, 6)

def build_tee(color, decal, dc, dw, x0, rot=0.0, seed=1, label_dark=False):
    o = flat_shape('tee', tee_outline(), thick=0.014)
    # drape: soft undulation + directional wrinkles at underarms and hem
    displace(o, 'CLOUDS', size=0.3, strength=0.014, depth=1)
    w = displace(o, 'WOOD', size=0.11, strength=0.0045, wood_type='BANDNOISE', noise_basis_2='SIN', turbulence=4.0)
    displace(o, 'CLOUDS', size=0.09, strength=0.0018, depth=0)
    m = fabric_mat('tee_' + color, color, decal=decal, dc=dc, dw=dw)
    assign(o, m)
    darker = '#e9e9e6' if not label_dark else '#1b2526'
    rib = fabric_mat('rib_' + color, color, scale=14, bump=1.0)
    # front collar rib (U) sitting on top surface
    neck = catmull([(-0.098, 0.358), (-0.07, 0.31), (0.0, 0.287), (0.07, 0.31), (0.098, 0.358)], 6, closed=False)
    tube_along('collar', neck, 0.0085, rib, z=0.008, flatten=0.55)
    # back neck seam + inside back panel (visible through neck opening), woven label
    backn = catmull([(-0.098, 0.358), (-0.05, 0.366), (0.0, 0.368), (0.05, 0.366), (0.098, 0.358)], 6, closed=False)
    tube_along('backneck', backn, 0.006, rib, z=0.008, flatten=0.5)
    if False: inside = flat_shape('inside', [(x, y - 0.003) for x, y in neck] + list(reversed([(x, y - 0.006) for x, y in backn])), thick=0.002, voxel=0.002, smooth_iter=2)
    if False: inside.location.z = 0.0062; assign(inside, fabric_mat('in_' + color, darker if not label_dark else '#1a2223', bump=0.4))
    bpy.ops.mesh.primitive_plane_add(size=1); lab = bpy.context.object; lab.scale = (0.05, 0.016, 1); lab.location = (0, 0.343, 0.0075)
    lm = mat('label', '#222F30' if not label_dark else '#F7F7F5', rough=0.6, sheen=0.4); assign(lab, lm)
    # twin-needle stitching at hem and sleeves
    st = mat('stitch_' + color, color, rough=0.9, sheen=0.6)
    for dy in (0.018, 0.024):
        tube_along('hem', [(-0.26, -0.372 + dy), (0.26, -0.372 + dy)], 0.0009, st, z=0.0075)
    for s in (1, -1):
        for dd in (0.017, 0.023):
            a, bb = Vector((0.405 * s, 0.172)), Vector((0.33 * s, 0.082)); d = (bb - a).normalized(); n = Vector((-d.y, d.x)) * (1 if s > 0 else -1)
            p0, p1 = a + d * 0.01 - n * dd, bb - d * 0.01 - n * dd
            tube_along('sl', [(p0.x, p0.y), (p1.x, p1.y)], 0.0009, st, z=0.0075)
        # shoulder / sleeve seam
        seam = catmull([(0.232 * s, 0.322), (0.245 * s, 0.25), (0.268 * s, 0.122)], 6, closed=False)
        tube_along('seam', seam, 0.0016, st, z=0.0072, flatten=0.5)
    grp = [ob for ob in bpy.context.scene.objects if ob.parent is None and ob.type in ('MESH', 'CURVE') and ob.name != 'sweep' and not ob.get('placed')]
    piv = bpy.data.objects.new('teeRoot', None); bpy.context.scene.collection.objects.link(piv)
    for ob in grp: ob.parent = piv; ob['placed'] = True
    piv.location = (x0, 0, 0.0075); piv.rotation_euler.z = rot
    return piv

def floor_paper(color='#E7E8E1'):
    bpy.ops.mesh.primitive_plane_add(size=8); f = bpy.context.object
    m = mat('paper', color, rough=0.9); nt = m.node_tree; b = nt.nodes['Principled BSDF']
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 400; nz.inputs['Detail'].default_value = 6
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.08
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    assign(f, m); f['placed'] = True; f.name = 'floor'; return f

def scene_tees(out, w, h, spp):
    reset(w, h, spp)
    world_hdri('studio_small_09', 0.12, rot=1.2)
    floor_paper('#DADBD3')
    build_tee('#F3F3F0', os.path.join(DEC, 'tee-chest.png'), (0.112, 0.2), 0.11, -0.47, rot=0.03)
    build_tee('#262F30', os.path.join(DEC, 'tee-big.png'), (0.0, 0.07), 0.28, 0.47, rot=-0.03, label_dark=True)
    area_light((-2.4, 0.9, 1.25), (0, 0, 0), 1.6, 140)
    area_light((2.2, -1.0, 2.2), (0, 0, 0), 2.5, 22)
    camera((0, -0.16, 2.45), (0, 0.0, 0), 50, dof=True, fstop=11)
    render(out)


def studio(sweep='#E7E8E1', hdri='studio_small_09', hs=0.15, rot=0.0):
    world_hdri(hdri, hs, rot=rot); return cyclorama(sweep, w=12, d=10, h=6, r=2.0, rough=0.9)

def ring_xy(r, n=96):
    return [(r * math.cos(i / n * 2 * math.pi), r * math.sin(i / n * 2 * math.pi)) for i in range(n)]

def band_outline(curve_pts, width):
    """Closed outline of a flat band of given width following an open polyline."""
    L, R = [], []
    for i, p in enumerate(curve_pts):
        a = Vector(curve_pts[max(0, i - 1)]); b = Vector(curve_pts[min(len(curve_pts) - 1, i + 1)])
        d = (b - a).normalized(); n = Vector((-d.y, d.x)) * width / 2
        L.append((p[0] + n.x, p[1] + n.y)); R.append((p[0] - n.x, p[1] - n.y))
    return L + list(reversed(R))

def stitch_x_mat(color):
    """Box-X stitch patch: transparent except thread lines."""
    m = mat('stx', color, rough=0.9, sheen=0.5); nt = m.node_tree; b = nt.nodes['Principled BSDF']
    m.blend_method = 'HASHED' if hasattr(m, 'blend_method') else None
    uv = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(uv.outputs['UV'], sep.inputs['Vector'])
    f = nt.nodes.new('ShaderNodeScript') if False else None
    # lines: border + two diagonals, width ~0.035 in UV
    def absdiff(a, bb):
        n = nt.nodes.new('ShaderNodeMath'); n.operation = 'SUBTRACT'; nt.links.new(a, n.inputs[0]); nt.links.new(bb, n.inputs[1])
        ab = nt.nodes.new('ShaderNodeMath'); ab.operation = 'ABSOLUTE'; nt.links.new(n.outputs['Value'], ab.inputs[0]); return ab.outputs['Value']
    inv = nt.nodes.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1; nt.links.new(sep.outputs['Y'], inv.inputs[1])
    d1 = absdiff(sep.outputs['X'], sep.outputs['Y']); d2 = absdiff(sep.outputs['X'], inv.outputs['Value'])
    mn = nt.nodes.new('ShaderNodeMath'); mn.operation = 'MINIMUM'; nt.links.new(d1, mn.inputs[0]); nt.links.new(d2, mn.inputs[1])
    # border distance
    bx = nt.nodes.new('ShaderNodeMath'); bx.operation = 'PINGPONG'; bx.inputs[1].default_value = 0.5; nt.links.new(sep.outputs['X'], bx.inputs[0])
    by = nt.nodes.new('ShaderNodeMath'); by.operation = 'PINGPONG'; by.inputs[1].default_value = 0.5; nt.links.new(sep.outputs['Y'], by.inputs[0])
    mb = nt.nodes.new('ShaderNodeMath'); mb.operation = 'MINIMUM'; nt.links.new(bx.outputs['Value'], mb.inputs[0]); nt.links.new(by.outputs['Value'], mb.inputs[1])
    mm = nt.nodes.new('ShaderNodeMath'); mm.operation = 'MINIMUM'; nt.links.new(mn.outputs['Value'], mm.inputs[0]); nt.links.new(mb.outputs['Value'], mm.inputs[1])
    lt = nt.nodes.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = 0.03; nt.links.new(mm.outputs['Value'], lt.inputs[0])
    nt.links.new(lt.outputs['Value'], b.inputs['Alpha'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.6; nt.links.new(lt.outputs['Value'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m

def build_tote(color, decal, x0, rot, handle_col=None):
    W, H = 0.38, 0.42
    rr = 0.008; outline = []
    for cx, cy, a0 in [(W/2 - rr, -H/2 + rr, -90), (W/2 - rr, H/2 - rr, 0), (-W/2 + rr, H/2 - rr, 90), (-W/2 + rr, -H/2 + rr, 180)]:
        for k in range(7):
            a = math.radians(a0 + k * 15); outline.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        # straight edge with slight sag
        nx, ny = {-90: (1, 0), 0: (0, 1), 90: (-1, 0), 180: (0, -1)}[a0]
    full = []
    for i in range(len(outline)):
        p, q = outline[i], outline[(i + 1) % len(outline)]; full.append(p)
        if (i + 1) % 7 == 0:
            for t in [j / 12 for j in range(1, 12)]: full.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
    outline = full
    o = flat_shape('tote', outline, thick=0.0045, voxel=0.0018, smooth_iter=3)
    displace(o, 'CLOUDS', size=0.3, strength=0.005, depth=1)
    displace(o, 'WOOD', size=0.09, strength=0.003, wood_type='BANDNOISE', noise_basis_2='SIN', turbulence=3.0)
    assign(o, fabric_mat('tote_' + color, color, tex='book_pattern', scale=9, bump=0.9, sheen=0.35, decal=decal, dc=(0, -0.02), dw=0.22, print_rough=0.6))
    hm = fabric_mat('handle_' + color, handle_col or color, tex='book_pattern', scale=16, bump=1.0, sheen=0.3)
    for k, (sx, ang) in enumerate([(1, 0.12), (-1, -0.2)]):
        arc = [(sx * 0.0 + 0.085 * math.cos(t) * 1.0 + 0.0, H / 2 - 0.02 + 0.30 * math.sin(t) * 0.9) for t in [math.pi * i / 24 for i in range(25)]]
        arc = [(x * (1 + 0.15 * k), y - k * 0.01) for x, y in arc]
        ho = flat_shape('handle', band_outline(arc, 0.025), thick=0.0022, voxel=0.0011, smooth_iter=2)
        ho.location.z = 0.0035 + 0.0024 * k; ho.rotation_euler.z = ang * 0.3
        for sx2 in (-1, 1):
            px, py = arc[0 if sx2 < 0 else -1]
            bpy.ops.mesh.primitive_plane_add(size=1, location=((px) * (1 if True else 1), H / 2 - 0.035 - k * 0.01, 0.0026 + 0.0024 * k)); sq = bpy.context.object; sq.scale = (0.024, 0.03, 1)
            sq.rotation_euler.z = ang * 0.3; assign(sq, stitch_x_mat(handle_col or color))
        displace(ho, 'CLOUDS', size=0.1, strength=0.003, depth=0)
        assign(ho, hm)
    grp = [ob for ob in bpy.context.scene.objects if ob.parent is None and ob.type in ('MESH', 'CURVE') and ob.name != 'sweep' and not ob.get('placed')]
    piv = bpy.data.objects.new('toteRoot', None); bpy.context.scene.collection.objects.link(piv)
    for ob in grp: ob.parent = piv; ob['placed'] = True
    piv.location = (x0, -0.08, 0.006); piv.rotation_euler.z = rot
    return piv

def scene_totes(out, w, h, spp):
    reset(w, h, spp)
    world_hdri('studio_small_09', 0.12, rot=1.2)
    floor_paper('#D9DAD2')
    build_tote('#E8E2D2', os.path.join(DEC, 'tote-print.png'), -0.3, 0.06)
    build_tote('#262F30', os.path.join(DEC, 'tote-print-white.png'), 0.3, -0.05)
    # charcoal tote takes a white print: swap decal by re-tinting below
    area_light((-2.4, 0.9, 1.25), (0, 0, 0), 1.6, 120)
    area_light((2.2, -1.0, 2.2), (0, 0, 0), 2.5, 20)
    camera((0, -0.1, 1.85), (0, 0.04, 0), 50, dof=True, fstop=11)
    render(out)

def powder(name, color, rough=0.5):
    m = mat(name, color, rough=rough, coat=0.25, coat_rough=0.35); nt = m.node_tree; b = nt.nodes['Principled BSDF']
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 2500; nz.inputs['Detail'].default_value = 4
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.12; bp.inputs['Distance'].default_value = 0.0002
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m

def add_print(m, img, ink_rough=0.35):
    """Layer a UV-mapped print (alpha) onto an existing principled material."""
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    im = nt.nodes.new('ShaderNodeTexImage'); im.image = bpy.data.images.load(img, check_existing=True); im.interpolation = 'Cubic'
    uv = nt.nodes.new('ShaderNodeUVMap'); nt.links.new(uv.outputs['UV'], im.inputs['Vector'])
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    mix.inputs['A'].default_value = b.inputs['Base Color'].default_value[:]
    nt.links.new(im.outputs['Alpha'], mix.inputs['Factor']); nt.links.new(im.outputs['Color'], mix.inputs['B']); nt.links.new(mix.outputs['Result'], b.inputs['Base Color'])
    rm = nt.nodes.new('ShaderNodeMix'); rm.data_type = 'FLOAT'; rm.inputs['A'].default_value = b.inputs['Roughness'].default_value; rm.inputs['B'].default_value = ink_rough
    nt.links.new(im.outputs['Alpha'], rm.inputs['Factor']); nt.links.new(rm.outputs['Result'], b.inputs['Roughness'])
    return m

def build_bottle(body_col, cap_col, decal, loc, rz):
    r, h = 0.037, 0.205
    body = [(0.0, 0.0), (r - 0.006, 0.0), (r - 0.0015, 0.0012), (r, 0.006)]
    body += [(r, z) for z in [0.02 + i * (h - 0.02) / 10 for i in range(11)]]
    for i in range(1, 11):
        a = i / 10 * math.pi / 2; body.append((0.027 + (r - 0.027) * math.cos(a), h + 0.03 * math.sin(a)))
    body.append((0.027, h + 0.034))
    b = lathe('bottle', body, 128); m = powder('pc_' + body_col, body_col); add_print(m, decal); assign(b, m)
    ring = lathe('ring', [(0.0262, h + 0.034), (0.0272, h + 0.035), (0.0272, h + 0.044), (0.0262, h + 0.045)], 96)
    assign(ring, mat('steel', '#C9CCCB', rough=0.22, metal=1.0))
    cp = [(0.0, h + 0.075), (0.026, h + 0.075), (0.0285, h + 0.073), (0.0295, h + 0.069)] + [(0.0295, h + 0.045 + i * 0.0024) for i in range(10, -1, -1)] + [(0.028, h + 0.044), (0.0, h + 0.044)]
    cap = lathe('cap', cp, 128); cm = mat('cap_' + cap_col, cap_col, rough=0.55, coat=0.1); assign(cap, cm)
    # knurl grip ribs
    for i in range(48):
        a = i / 48 * 2 * math.pi
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0.0297 * math.cos(a), 0.0297 * math.sin(a), h + 0.058)); rb = bpy.context.object
        rb.scale = (0.0012, 0.0012, 0.018); rb.rotation_euler.z = a; assign(rb, cm)
    # carry loop
    bpy.ops.mesh.primitive_torus_add(major_radius=0.016, minor_radius=0.0042, location=(0, 0, h + 0.079), rotation=(math.pi / 2, 0, math.pi / 2)); lp = bpy.context.object
    bpy.ops.object.shade_smooth(); assign(lp, cm)
    grp = [ob for ob in bpy.context.scene.objects if ob.parent is None and ob.type == 'MESH' and ob.name != 'sweep' and not ob.get('placed')]
    piv = bpy.data.objects.new('bRoot', None); bpy.context.scene.collection.objects.link(piv)
    for ob in grp: ob.parent = piv; ob['placed'] = True
    piv.location = loc; piv.rotation_euler.z = rz
    return piv

def scene_bottles(out, w, h, spp):
    reset(w, h, spp)
    studio('#E4E5DE', hs=0.15, rot=0.6)
    # print faces camera at u=0.5 (lathe angle pi) -> rotate so -X faces -Y camera
    build_bottle('#222F30', '#A7E26E', os.path.join(DEC, 'bottle-white.png'), (-0.048, 0.0, 0), math.pi / 2 + 0.08)
    build_bottle('#F2F2EE', '#222F30', os.path.join(DEC, 'bottle-ink.png'), (0.05, 0.05, 0), math.pi / 2 - 0.1)
    area_light((-0.9, -0.5, 0.9), (0, 0, 0.12), 0.9, 45)
    area_light((0.9, -0.2, 0.5), (0, 0, 0.12), 0.6, 14, size_y=1.4)
    area_light((0.0, 0.8, 0.9), (0, 0, 0.15), 0.6, 18)
    camera((0, -1.2, 0.3), (0, 0.02, 0.145), 85, dof=True, fstop=18)
    render(out)

def build_mug(body_col, inside_col, decal, loc, rz, glossy=True):
    R, H, t = 0.041, 0.095, 0.0035
    prof = [(0.0, 0.004), (R - 0.008, 0.004), (R - 0.006, 0.0), (R - 0.003, 0.0), (R, 0.004)] + [(R, 0.01 + i * (H - 0.014) / 8) for i in range(9)]
    prof += [(R - 0.0006, H - 0.0008), (R - t / 2, H), (R - t + 0.0006, H - 0.0008)] + [(R - t, H - 0.006 - i * (H - 0.02) / 6) for i in range(7)] + [(R - t - 0.006, 0.0085), (0.0, 0.008)]
    b = lathe('mug', prof, 128)
    m = mat('glaze_' + body_col, body_col, rough=0.06 if glossy else 0.45, coat=1.0 if glossy else 0.2, coat_rough=0.03)
    add_print(m, decal, ink_rough=0.08 if glossy else 0.3)
    # inside colour by height on inner wall: use geometry normal facing inward -> simpler: second material on inner faces
    inm = mat('in_' + inside_col, inside_col, rough=0.06, coat=1.0)
    b.data.materials.append(m); b.data.materials.append(inm)
    for p in b.data.polygons:
        c = p.center
        p.material_index = 1 if (math.hypot(c.x, c.y) < R - t * 0.6 and c.z > 0.0085) else 0
    for poly in b.data.polygons: pass
    # handle: D shape
    hp = [(R - 0.002, 0.0, 0.078), (R + 0.022, 0.0, 0.08), (R + 0.034, 0.0, 0.062), (R + 0.034, 0.0, 0.038), (R + 0.022, 0.0, 0.02), (R - 0.002, 0.0, 0.022)]
    cu = bpy.data.curves.new('h', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.0062; cu.bevel_resolution = 6; sp = cu.splines.new('NURBS'); sp.points.add(len(hp) - 1)
    for i, p in enumerate(hp): sp.points[i].co = (*p, 1)
    sp.order_u = 4; sp.use_endpoint_u = True
    ho = bpy.data.objects.new('handle', cu); bpy.context.scene.collection.objects.link(ho); ho.scale.y = 0.75
    cu.materials.append(mat('glaze_plain_' + body_col, body_col, rough=0.06 if glossy else 0.45, coat=1.0 if glossy else 0.2, coat_rough=0.03))
    grp = [ob for ob in bpy.context.scene.objects if ob.parent is None and ob.type in ('MESH', 'CURVE') and ob.name != 'sweep' and not ob.get('placed')]
    piv = bpy.data.objects.new('mRoot', None); bpy.context.scene.collection.objects.link(piv)
    for ob in grp: ob.parent = piv; ob['placed'] = True
    piv.location = loc; piv.rotation_euler.z = rz
    return piv

def scene_mugs(out, w, h, spp):
    reset(w, h, spp)
    studio('#E4E5DE', hs=0.15, rot=0.6)
    build_mug('#FBFBF9', '#222F30', os.path.join(DEC, 'mug-wrap.png'), (-0.055, 0.0, 0), -0.25)
    build_mug('#222F30', '#A7E26E', os.path.join(DEC, 'mug-wrap-white.png'), (0.068, 0.075, 0), 0.35, glossy=False)
    area_light((-0.8, -0.5, 0.8), (0, 0, 0.05), 0.8, 38)
    area_light((0.9, -0.1, 0.4), (0, 0, 0.05), 0.5, 10, size_y=1.2)
    area_light((0.0, 0.8, 0.8), (0, 0, 0.05), 0.6, 15)
    camera((0.0, -0.72, 0.22), (0.005, 0.03, 0.05), 85, dof=True, fstop=26)
    render(out)

def silicone(name, color):
    m = mat(name, color, rough=0.42, sss=0.12, sheen=0.25, spec=0.4)
    m.node_tree.nodes['Principled BSDF'].inputs['Subsurface Scale'].default_value = 0.0004  # 2 mm wall: keep scatter shallow
    return m

def build_band(color, fill, decal, loc, rot):
    """Silicone band; lettering engraved 0.4 mm into the outer face (micro-displacement), optionally ink-filled."""
    R, wd, th = 0.0322, 0.013, 0.0024
    prof = [(R, -wd / 2 + 0.0008), (R + 0.0004, -wd / 2), (R + th - 0.0004, -wd / 2), (R + th, -wd / 2 + 0.0006)]
    prof += [(R + th, -wd / 2 + 0.0006 + (wd - 0.0012) * t / 16) for t in range(1, 16)]
    prof += [(R + th, wd / 2 - 0.0006), (R + th - 0.0004, wd / 2), (R + 0.0004, wd / 2), (R, wd / 2 - 0.0008)]
    o = lathe('band', prof + [prof[0]], 360)
    sub = o.modifiers.new('sub', 'SUBSURF'); sub.subdivision_type = 'SIMPLE'; sub.levels = 0; sub.render_levels = 1
    sub.use_adaptive_subdivision = True; sub.adaptive_space = 'PIXEL'; sub.adaptive_pixel_size = 1.0
    m = silicone('sil_' + color + (fill or ''), color); nt = m.node_tree; b = nt.nodes['Principled BSDF']
    m.displacement_method = 'DISPLACEMENT'
    uv = nt.nodes.new('ShaderNodeUVMap'); mp = nt.nodes.new('ShaderNodeMapping')
    # outer face spans v from ~0.15 to ~0.85 of the profile height: map the decal onto it
    mp.inputs['Location'].default_value = (0, -0.06, 0); mp.inputs['Scale'].default_value = (1, 1.12, 1)
    nt.links.new(uv.outputs['UV'], mp.inputs['Vector'])
    hm = nt.nodes.new('ShaderNodeTexImage'); hm.image = bpy.data.images.load(os.path.join(DEC, 'band-height.png'), check_existing=True); hm.image.colorspace_settings.name = 'Non-Color'
    hm.interpolation = 'Cubic'; hm.extension = 'CLIP'; nt.links.new(mp.outputs['Vector'], hm.inputs['Vector'])
    tco = nt.nodes.new('ShaderNodeTexCoord'); sx = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tco.outputs['Object'], sx.inputs['Vector'])
    cxy = nt.nodes.new('ShaderNodeCombineXYZ'); nt.links.new(sx.outputs['X'], cxy.inputs['X']); nt.links.new(sx.outputs['Y'], cxy.inputs['Y'])
    vl = nt.nodes.new('ShaderNodeVectorMath'); vl.operation = 'LENGTH'; nt.links.new(cxy.outputs['Vector'], vl.inputs['Vector'])
    gt = nt.nodes.new('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = R + th - 0.0003; nt.links.new(vl.outputs['Value'], gt.inputs[0])
    a = nt.nodes.new('ShaderNodeMath'); a.operation = 'MULTIPLY'; nt.links.new(hm.outputs['Color'], a.inputs[0]); nt.links.new(gt.outputs['Value'], a.inputs[1])
    disp = nt.nodes.new('ShaderNodeDisplacement'); disp.inputs['Midlevel'].default_value = 0.0; disp.inputs['Scale'].default_value = -0.0004
    nt.links.new(a.outputs['Value'], disp.inputs['Height']); nt.links.new(disp.outputs['Displacement'], nt.nodes['Material Output'].inputs['Displacement'])
    if fill:
        mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.inputs['A'].default_value = hexc(color); mix.inputs['B'].default_value = hexc(fill)
        nt.links.new(a.outputs['Value'], mix.inputs['Factor']); nt.links.new(mix.outputs['Result'], b.inputs['Base Color'])
    assign(o, m); o.location = loc; o.rotation_mode = 'ZYX'; o.rotation_euler = rot; return o

def scene_bands(out, w, h, spp):
    reset(w, h, spp)
    bpy.context.scene.cycles.dicing_rate = 1.0
    studio('#E7E8E1', hs=0.15, rot=0.4)
    dec = os.path.join(DEC, 'band-text.png')
    # two bands standing, lettering to camera; two lying behind
    build_band('#A7E26E', '#222F30', dec, (-0.04, 0.0, 0.0346), (0.25, math.pi / 2, 0.6))
    build_band('#222F30', None, dec, (0.04, 0.012, 0.0346), (-0.2, math.pi / 2, 2.6))
    build_band('#F7F7F5', '#222F30', dec, (-0.03, 0.075, 0.0065), (0, 0, 2.0))
    build_band('#CEF79E', '#445E5F', dec, (0.045, 0.085, 0.0065), (0, 0, 0.7))
    area_light((-0.5, -0.35, 0.45), (0, 0, 0.03), 0.4, 6)
    area_light((0.45, -0.1, 0.25), (0, 0, 0.03), 0.25, 2)
    area_light((0.0, 0.5, 0.35), (0, 0, 0.03), 0.4, 2)
    camera((0.0, -0.36, 0.13), (0.0, 0.02, 0.03), 85, dof=True, fstop=64)
    render(out)

def ribbon(name, pts, width, th, material, z=0.0, u_rep=1.0):
    """Flat ribbon mesh with UVs along length, solidified."""
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new(); rows = []
    total = 0; lens = [0]
    for i in range(1, len(pts)): total += (Vector(pts[i]) - Vector(pts[i - 1])).length; lens.append(total)
    for i, p in enumerate(pts):
        a = Vector(pts[max(0, i - 1)]); b = Vector(pts[min(len(pts) - 1, i + 1)]); d = (b - a).normalized(); n = Vector((-d.y, d.x, 0)) * width / 2
        P = Vector((p[0], p[1], p[2] if len(p) > 2 else z))
        rows.append((bm.verts.new(P + n), bm.verts.new(P - n)))
    for i in range(len(rows) - 1):
        f = bm.faces.new((rows[i][0], rows[i][1], rows[i + 1][1], rows[i + 1][0]))
        for lp, (u, v) in zip(f.loops, [(lens[i], 1), (lens[i], 0), (lens[i + 1], 0), (lens[i + 1], 1)]): lp[uvl].uv = (u / (width * 16) * u_rep, v)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    s = o.modifiers.new('s', 'SOLIDIFY'); s.thickness = th
    for p in me.polygons: p.use_smooth = False
    assign(o, material); return o

def scene_badge(out, w, h, spp):
    reset(w, h, spp)
    world_hdri('studio_small_09', 0.12, rot=0.8)
    floor_paper('#E1E2DA')
    W, H = 0.054, 0.086
    cf = card('id', W, H, 0.0008, os.path.join(STAT, 'staff-id-front.png'), None, edge='#F7F7F5', rough=0.18, coat=0.8, paper_bump=0)
    cf.location = (0.02, -0.01, 0.0005); cf.rotation_euler.z = -0.12
    vp = card('vp', W, H, 0.0008, os.path.join(STAT, 'visitor-pass.png'), None, edge='#A7E26E', rough=0.18, coat=0.8, paper_bump=0)
    vp.location = (0.095, 0.035, 0.0005); vp.rotation_euler.z = 0.2
    # lanyard: lime woven ribbon with charcoal print, loop on the table
    lm = mat('lan', '#A7E26E', rough=0.7, sheen=0.6); add_print(lm, os.path.join(DEC, 'lanyard.png'), ink_rough=0.7)
    nt = lm.node_tree; nn = nt.nodes.new('ShaderNodeTexImage'); nn.image = bpy.data.images.load(os.path.join(PH, 'tex', 'book_pattern', 'nor.jpg')); nn.image.colorspace_settings.name = 'Non-Color'
    tc = nt.nodes.new('ShaderNodeTexCoord'); mpp = nt.nodes.new('ShaderNodeMapping'); mpp.inputs['Scale'].default_value = (60, 60, 60); nt.links.new(tc.outputs['Object'], mpp.inputs['Vector']); nt.links.new(mpp.outputs['Vector'], nn.inputs['Vector'])
    nmp = nt.nodes.new('ShaderNodeNormalMap'); nmp.inputs['Strength'].default_value = 0.8; nt.links.new(nn.outputs['Color'], nmp.inputs['Color']); nt.links.new(nmp.outputs['Normal'], nt.nodes['Principled BSDF'].inputs['Normal'])
    ctrl = [(0.016, 0.046), (0.03, 0.09), (0.0, 0.16), (-0.08, 0.19), (-0.17, 0.15), (-0.2, 0.05), (-0.17, -0.04), (-0.11, -0.03), (-0.06, 0.04), (-0.02, 0.075), (0.008, 0.058), (0.012, 0.047)]
    pts = catmull(ctrl, 10, closed=False); pts3 = [(x, y, 0.0012 + 0.0004 * math.sin(i)) for i, (x, y) in enumerate(pts)]
    ribbon('lanyard', pts3, 0.02, 0.0009, lm, u_rep=1.0)
    # clip: steel swivel hook + split ring at top of card
    st = mat('steel', '#C4C8C7', rough=0.2, metal=1)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.0065, minor_radius=0.0011, location=(0.014, 0.034, 0.0015)); bpy.ops.object.shade_smooth(); assign(bpy.context.object, st)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.013, 0.043, 0.002)); cl = bpy.context.object; cl.scale = (0.008, 0.016, 0.003); bevel(cl, 0.0012, 3); assign(cl, st)
    area_light((-0.5, 0.3, 0.6), (0, 0, 0), 0.6, 20)
    area_light((0.5, -0.4, 0.5), (0, 0, 0), 0.6, 5)
    camera((-0.02, -0.11, 0.36), (-0.03, 0.03, 0.0), 50, dof=True, fstop=22)
    render(out)

SCENES = {'tees': scene_tees, 'totes': scene_totes, 'bottles': scene_bottles, 'mugs': scene_mugs, 'bands': scene_bands, 'badge': scene_badge}

if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    name, out = a[0], a[1]; w, h, spp = (int(a[2]), int(a[3]), int(a[4])) if len(a) > 4 else (1600, 1200, 160)
    SCENES[name](out, w, h, spp)
