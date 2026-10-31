"""Ghost-mannequin oversized tee (front / back views), Cycles. Usage: python tee3d.py <front|back> <stone|ink> <out.png> [w h spp]"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blib import *
from merch import catmull, fabric_mat
import numpy as np
from mathutils import Vector

DEC = os.path.join(HERE, '..', 'render', 'decal')

# Oversized boxy tee: dropped shoulders, wide short sleeves, straight body. Units metres, y up, x right.
HALF = [(0.0, 0.392), (0.06, 0.39), (0.11, 0.382), (0.2, 0.368), (0.285, 0.345),   # neck to dropped shoulder point
        (0.37, 0.285), (0.45, 0.19), (0.5, 0.115),                                  # sleeve top, longer and dropping
        (0.44, 0.04), (0.355, 0.02),                                                # sleeve hem (opening)
        (0.31, 0.11), (0.3, 0.06), (0.3, -0.15), (0.302, -0.33), (0.304, -0.372),   # underarm, side seam
        (0.2, -0.376), (0.0, -0.377)]

def outline():
    full = HALF + [(-x, y) for x, y in reversed(HALF[1:-1])]
    return catmull(full, 8)

def seg_dist(P, A, B):
    AB = B - A; t = np.clip(((P - A) @ AB) / (AB @ AB + 1e-12), 0, 1)
    Q = A + t[:, None] * AB; return np.linalg.norm(P - Q, axis=1)

def mannequin():
    """Invisible form the garment settles on: torso with sloped shoulders, arms angled out and down."""
    parts = []
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=1, depth=0.66, location=(0, -0.06, 0)); t = bpy.context.object
    t.rotation_euler.x = math.pi / 2; t.scale = (0.255, 0.125, 1); parts.append(t)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1, location=(0, 0.27, 0)); sh = bpy.context.object
    sh.scale = (0.255, 0.1, 0.125); parts.append(sh)
    for sx in (1, -1):
        a, b = Vector((sx * 0.21, 0.27, 0)), Vector((sx * 0.5, 0.02, 0)); d = b - a
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.07, depth=d.length, location=(a + b) / 2); arm = bpy.context.object
        arm.rotation_euler = d.to_track_quat('Z', 'Y').to_euler(); arm.scale = (1, 0.85, 1); parts.append(arm)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.075, location=a); parts.append(bpy.context.object)
    for p in parts:
        p.select_set(True); bpy.context.view_layer.objects.active = p
        c = p.modifiers.new('col', 'COLLISION'); p.collision.thickness_outer = 0.006; p.collision.cloth_friction = 8
        p.hide_render = True
    return parts

def seg_pts_dist(P, a, b):
    a, b = np.array(a), np.array(b); return seg_dist(P, a, b)

def boundary_loops(o):
    bm = bmesh.new(); bm.from_mesh(o.data); bm.edges.ensure_lookup_table()
    edges = [e for e in bm.edges if e.is_boundary]; loops = []; used = set()
    adj = {}
    for e in edges:
        for v in e.verts: adj.setdefault(v.index, []).append(e)
    for e0 in edges:
        if e0.index in used: continue
        loop = [e0.verts[0].index]; cur = e0.verts[0]; e = e0
        while True:
            used.add(e.index); nxt = e.other_vert(cur); loop.append(nxt.index); cur = nxt
            cand = [x for x in adj[cur.index] if x.index not in used]
            if not cand: break
            e = cand[0]
        loops.append(loop[:-1] if loop[0] == loop[-1] else loop)
    bm.free(); return loops

def loop_tube(name, pts, radius, material, flatten=0.6):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = radius; cu.bevel_resolution = 4
    sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
    for i, p in enumerate(pts): sp.points[i].co = (p.x, p.y, p.z, 1)
    sp.use_cyclic_u = True
    o = bpy.data.objects.new(name, cu); bpy.context.scene.collection.objects.link(o); cu.materials.append(material)
    sm = o.modifiers.new('sm', 'SMOOTH') if False else None
    return o

def build_tee(color, print_front, print_back, front_dc, front_dw, back_dc, back_dw):
    ol = outline()
    bm = bmesh.new(); vs = [bm.verts.new((x, y, 0)) for x, y in ol]; bm.faces.new(vs)
    me = bpy.data.meshes.new('tee'); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('tee', me); bpy.context.scene.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    sol = o.modifiers.new('s', 'SOLIDIFY'); sol.thickness = 0.02; sol.offset = 0; bpy.ops.object.modifier_apply(modifier='s')
    rm = o.modifiers.new('r', 'REMESH'); rm.mode = 'VOXEL'; rm.voxel_size = 0.011; bpy.ops.object.modifier_apply(modifier='r')
    # start inflated (clear of the form), then let it settle
    V = np.array([v.co[:] for v in o.data.vertices]); P = V[:, :2]
    O = np.array(ol); d = np.full(len(P), 9.0)
    for k in range(len(O)): d = np.minimum(d, seg_dist(P, O[k], O[(k + 1) % len(O)]))
    u = np.clip(d / 0.12, 0, 1); prof = np.sqrt(1 - (1 - u) ** 2)
    V[:, 2] = np.where(V[:, 2] >= 0, 1.0, -1.0) * (0.006 + 0.15 * prof)
    for v, c in zip(o.data.vertices, V): v.co = c
    # open the hem, sleeve ends and neck
    bm = bmesh.new(); bm.from_mesh(o.data)
    def kill(f):
        c = f.calc_center_median()
        if c.y < -0.362: return True
        for sx in (1, -1):
            if seg_pts_dist(np.array([[c.x, c.y]]), (sx * 0.5, 0.115), (sx * 0.355, 0.02))[0] < 0.016: return True
        nz = (c.x / 0.112) ** 2 + ((c.y - 0.392) / (0.085 if c.z > 0 else 0.032)) ** 2
        return nz < 1.0 and c.y > 0.3
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if kill(f)], context='FACES'); bm.to_mesh(o.data); bm.free()
    body = mannequin()
    cl = o.modifiers.new('cloth', 'CLOTH'); st = cl.settings
    st.quality = 7; st.mass = 0.25; st.tension_stiffness = 15; st.compression_stiffness = 15; st.shear_stiffness = 8; st.bending_stiffness = 0.3
    st.shrink_min = 0.04
    cl.collision_settings.distance_min = 0.004; cl.collision_settings.use_self_collision = False
    sc = bpy.context.scene; sc.frame_start = 1; sc.frame_end = 80; sc.gravity = (0.0, -9.81, 0.0)
    cl.point_cache.frame_start = 1; cl.point_cache.frame_end = 80
    for f in range(1, 56): sc.frame_set(f)
    bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier='cloth'); sc.frame_set(1)
    for p in body: bpy.data.objects.remove(p)
    sub = o.modifiers.new('sub', 'SUBSURF'); sub.levels = 1; bpy.ops.object.modifier_apply(modifier='sub')
    sm = o.modifiers.new('sm', 'CORRECTIVE_SMOOTH') if False else None
    loops = boundary_loops(o)
    vs = o.data.vertices
    for lp in loops:
        n = len(lp)
        if n < 6: continue
        for _ in range(40):
            pos = [vs[i].co.copy() for i in lp]
            for k in range(n):
                vs[lp[k]].co = pos[k] * 0.5 + (pos[k - 1] + pos[(k + 1) % n]) * 0.25
    # ease the ring of faces next to each edge so the smoothed rim blends in
    bm2 = bmesh.new(); bm2.from_mesh(o.data)
    rim = set(i for lp in loops for i in lp)
    near = [v for v in bm2.verts if v.index not in rim and any(e.other_vert(v).index in rim for e in v.link_edges)]
    bmesh.ops.smooth_vert(bm2, verts=near, factor=0.6, use_axis_x=True, use_axis_y=True, use_axis_z=True); bm2.to_mesh(o.data); bm2.free()
    loops = [[vs[i].co.copy() for i in lp] for lp in loops]
    th = o.modifiers.new('th', 'SOLIDIFY'); th.thickness = 0.0025; th.offset = -1; bpy.ops.object.modifier_apply(modifier='th')
    for p in o.data.polygons: p.use_smooth = True
    m = fabric_mat('tee_' + color, color, scale=8, bump=0.6, sheen=0.55, decal=print_front, dc=front_dc, dw=front_dw)
    mb = fabric_mat('teeB_' + color, color, scale=8, bump=0.6, sheen=0.55, decal=print_back, dc=back_dc, dw=back_dw)
    nt = mb.node_tree
    for n in nt.nodes:  # back print: mirror u, print on faces pointing -z
        if n.type == 'MAPPING' and n.vector_type == 'POINT':
            n.inputs['Scale'].default_value[0] *= -1; n.inputs['Location'].default_value[0] = 0.5 + back_dc[0] / back_dw
        if n.type == 'MATH' and n.operation == 'GREATER_THAN': n.operation = 'LESS_THAN'; n.inputs[1].default_value = -0.2
    o.data.materials.append(m); o.data.materials.append(mb)
    for p in o.data.polygons: p.material_index = 0 if p.normal.z >= 0 else 1
    # rib collar, hem band and sleeve bands built on the real opening edges
    rib = fabric_mat('rib_' + color, color, scale=16, bump=0.9, sheen=0.5)
    for lp in loops:
        if len(lp) < 12: continue
        cy = sum(p.y for p in lp) / len(lp)
        r = 0.012 if cy > 0.3 else 0.006
        loop_tube('band', lp, r, rib)
    return o

def scene(view, colorway, out, w, h, spp):
    reset(w, h, spp)
    world_hdri('studio_small_09', 0.12, rot=0.3, bg='#F1F1EE', bg_strength=1.0)
    ink = colorway == 'ink'
    color = '#262F30' if ink else '#E9E6DC'
    front = os.path.join(DEC, 'tee-front-mark-white.png' if ink else 'tee-front-mark.png')
    back = os.path.join(DEC, 'tee-back-white.png' if ink else 'tee-back.png')
    o = build_tee(color, front, back, (0.0, 0.16), 0.125, (0.06, -0.02), 0.22)
    # soft studio key from upper front-left, fill right, rim from behind
    zc = 1 if view == 'front' else -1
    area_light((-1.4, 1.1, 1.8 * zc), (0, 0, 0), 2.0, 70)
    area_light((1.6, 0.2, 1.4 * zc), (0, 0, 0), 2.0, 18)
    area_light((0.0, 0.8, -2.0 * zc), (0, 0, 0), 1.5, 25)
    cam = camera((0, 0.0, 3.2 * zc), (0, 0.0, 0), 50)
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = 1.12
    render(out)

if __name__ == '__main__':
    a = sys.argv[1:]
    view, cw, out = a[0], a[1], a[2]; w, h, spp = (int(a[3]), int(a[4]), int(a[5])) if len(a) > 5 else (1600, 1600, 160)
    scene(view, cw, out, w, h, spp)
