"""Standing canvas tote in window light, Cycles. Usage: python tote3d.py <natural|ink> <out.png> [w h spp]
Scene frame: Y is up, Z points at the camera (garment-style), floor is the XZ plane at y = FLOOR."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blib import *
from merch import fabric_mat, stitch_x_mat
from tee3d import boundary_loops, seg_dist
import numpy as np
from mathutils import Vector, Matrix

DEC = os.path.join(HERE, '..', 'render', 'decal')
W, H = 0.46, 0.40
FLOOR = -0.215

def box(name, size, loc, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.name = name; o.scale = size
    bpy.ops.object.transform_apply(scale=True); assign(o, m); return o

def strap(name, pts, width, th, m):
    """Flat webbing strap through 3D points, width along local Z (bag depth)."""
    bm = bmesh.new(); rows = []
    for i, p in enumerate(pts):
        a = Vector(pts[max(0, i - 1)]); b = Vector(pts[min(len(pts) - 1, i + 1)]); t = (b - a).normalized()
        side = t.cross(Vector((1, 0, 0))).normalized() * (width / 2)
        if side.length < 1e-6: side = Vector((0, 0, width / 2))
        rows.append((bm.verts.new(Vector(p) + side), bm.verts.new(Vector(p) - side)))
    for i in range(len(rows) - 1): bm.faces.new((rows[i][0], rows[i][1], rows[i + 1][1], rows[i + 1][0]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    s = o.modifiers.new('s', 'SOLIDIFY'); s.thickness = th; s.offset = 0
    sub = o.modifiers.new('sub', 'SUBSURF'); sub.levels = 1; sub.render_levels = 2
    for p in me.polygons: p.use_smooth = True
    assign(o, m); return o

def build_tote(color, decal):
    r = 0.012; ol = []
    for cx, cy, a0 in [(W/2 - r, -H/2 + r, -90), (W/2 - r, H/2 - r, 0), (-W/2 + r, H/2 - r, 90), (-W/2 + r, -H/2 + r, 180)]:
        for k in range(7): a = math.radians(a0 + k * 15); ol.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    full = []
    for i in range(len(ol)):
        p, q = ol[i], ol[(i + 1) % len(ol)]; full.append(p)
        if (i + 1) % 7 == 0:
            for t in [j / 20 for j in range(1, 20)]: full.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
    bm = bmesh.new(); vs = [bm.verts.new((x, y, 0)) for x, y in full]; bm.faces.new(vs)
    me = bpy.data.meshes.new('tote'); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('tote', me); bpy.context.scene.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    s_ = o.modifiers.new('s', 'SOLIDIFY'); s_.thickness = 0.02; s_.offset = 0; bpy.ops.object.modifier_apply(modifier='s')
    rm = o.modifiers.new('r', 'REMESH'); rm.mode = 'VOXEL'; rm.voxel_size = 0.009; bpy.ops.object.modifier_apply(modifier='r')
    # puff to clear the inner form, then open the top
    V = np.array([v.co[:] for v in o.data.vertices]); P = V[:, :2]; O = np.array(full); d = np.full(len(P), 9.0)
    for k in range(len(O)): d = np.minimum(d, seg_dist(P, O[k], O[(k + 1) % len(O)]))
    u = np.clip(d / 0.1, 0, 1); V[:, 2] = np.where(V[:, 2] >= 0, 1, -1) * (0.005 + 0.075 * np.sqrt(1 - (1 - u) ** 2))
    for v, c in zip(o.data.vertices, V): v.co = c
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.calc_center_median().y > H / 2 - 0.014], context='FACES'); bm.to_mesh(o.data); bm.free()
    # soft contents give the bag its belly; canvas settles over them under gravity
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1, location=(0.02, -0.04, 0)); form = bpy.context.object
    form.scale = (0.18, 0.15, 0.06); form.modifiers.new('c', 'COLLISION'); form.collision.thickness_outer = 0.004; form.hide_render = True
    cl = o.modifiers.new('cloth', 'CLOTH'); st = cl.settings
    st.quality = 7; st.mass = 0.35; st.tension_stiffness = 40; st.compression_stiffness = 40; st.shear_stiffness = 20; st.bending_stiffness = 2.0
    vg = o.vertex_groups.new(name='pin'); vg.add([v.index for v in o.data.vertices if v.co.y > H / 2 - 0.03], 1.0, 'REPLACE'); st.vertex_group_mass = 'pin'
    cl.collision_settings.distance_min = 0.003
    sc = bpy.context.scene; sc.gravity = (0, -9.81, 0); sc.frame_start = 1; sc.frame_end = 60; cl.point_cache.frame_end = 60
    for f in range(1, 41): sc.frame_set(f)
    bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier='cloth'); sc.frame_set(1)
    bpy.data.objects.remove(form)
    sub = o.modifiers.new('sub', 'SUBSURF'); sub.levels = 1; bpy.ops.object.modifier_apply(modifier='sub')
    loops = boundary_loops(o); vs = o.data.vertices
    for lp in loops:
        n = len(lp)
        for _ in range(30):
            pos = [vs[i].co.copy() for i in lp]
            for k in range(n): vs[lp[k]].co = pos[k] * 0.5 + (pos[k - 1] + pos[(k + 1) % n]) * 0.25
    rim = [[vs[i].co.copy() for i in lp] for lp in loops]
    th = o.modifiers.new('th', 'SOLIDIFY'); th.thickness = 0.002; th.offset = -1; bpy.ops.object.modifier_apply(modifier='th')
    for p in o.data.polygons: p.use_smooth = True
    m = fabric_mat('tote_' + color, color, tex='book_pattern', scale=11, bump=0.9, sheen=0.3, decal=decal, dc=(0.0, -0.1), dw=0.36, print_rough=0.7)
    assign(o, m)
    hem = fabric_mat('hem_' + color, color, tex='book_pattern', scale=14, bump=1.0, sheen=0.3)
    for lp in rim:
        cu = bpy.data.curves.new('hem', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.006; cu.bevel_resolution = 4
        sp = cu.splines.new('POLY'); sp.points.add(len(lp) - 1)
        for i, p in enumerate(lp): sp.points[i].co = (p.x, p.y - 0.004, p.z, 1)
        sp.use_cyclic_u = True; ho = bpy.data.objects.new('hem', cu); bpy.context.scene.collection.objects.link(ho); ho.scale.y = 1.0; cu.materials.append(hem)
    # handles: front strap and back strap, standing up and falling back slightly
    hm = fabric_mat('strap_' + color, color, tex='book_pattern', scale=20, bump=1.0, sheen=0.35)
    rim_pts = rim[0] if rim else []
    def rim_z(x, front):
        c = [p for p in rim_pts if abs(p.x - x) < 0.02 and ((p.z > 0) == front)]
        return (sum(p.z for p in c) / len(c)) if c else (0.03 if front else -0.03)
    for front, lean, rise in [(True, -0.05, 0.25), (False, -0.12, 0.23)]:
        x0 = 0.085; z0 = rim_z(-x0, front); z1 = rim_z(x0, front); pts = []
        for i in range(41):
            t = i / 40; a = math.pi * t
            x = -x0 * math.cos(a) * (1 + 0.12 * math.sin(a)); y = H / 2 - 0.07 + rise * math.sin(a)
            z = (z0 * (1 - t) + z1 * t) + lean * math.sin(a) ** 1.4 + (0.004 if front else -0.004)
            pts.append((x, y, z))
        strap('handle', pts, 0.03, 0.003, hm)
        for x in (-x0, x0):  # box-X stitched patch where the strap meets the bag
            bpy.ops.mesh.primitive_plane_add(size=1, location=(x, H / 2 - 0.045, rim_z(x, front) + (0.0045 if front else -0.0045)), rotation=(0 if front else math.pi, 0, 0))
            sq = bpy.context.object; sq.scale = (0.03, 0.032, 1); assign(sq, stitch_x_mat(color))
    objs = [ob for ob in bpy.context.scene.objects if ob.type in ('MESH', 'CURVE') and ob.parent is None]
    root = bpy.data.objects.new('root', None); bpy.context.scene.collection.objects.link(root)
    for ob in objs: ob.parent = root
    return root

def scene(colorway, out, w, h, spp):
    reset(w, h, spp)
    world_hdri('studio_small_09', 0.28, rot=1.0, bg='#EFEDE7', bg_strength=1.0)
    ink = colorway == 'ink'
    color = '#262F30' if ink else '#ECE7DA'
    root = build_tote(color, os.path.join(DEC, 'tote-wide-white.png' if ink else 'tote-wide.png'))
    # lean on one corner and turn three-quarters, then sit the lowest point on the floor
    root.rotation_euler = (0, math.radians(-24), math.radians(7)); bpy.context.view_layer.update()
    low = min((ob.matrix_world @ Vector(c)).y for ob in root.children if ob.type == 'MESH' for c in ob.bound_box)
    root.location.y += FLOOR - low + 0.001
    wallm = mat('wall', '#F1EEE7', rough=0.92)
    bpy.ops.mesh.primitive_plane_add(size=6, location=(0, FLOOR, 0), rotation=(math.pi / 2, 0, 0)); assign(bpy.context.object, wallm)  # floor (XZ)
    bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 1.0, -0.42)); assign(bpy.context.object, wallm)                              # back wall (XY)
    # hard window sun from upper left-front, with a window frame casting the shadows
    sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 5.2; sun.angle = math.radians(1.2); sun.color = hexc('#FFF4E2')[:3]
    so = bpy.data.objects.new('sun', sun); bpy.context.scene.collection.objects.link(so)
    sdir = Vector((-0.55, 0.62, 0.56)).normalized()          # direction towards the sun
    so.rotation_euler = (-sdir).to_track_quat('-Z', 'Y').to_euler()
    win = bpy.data.objects.new('window', None); bpy.context.scene.collection.objects.link(win)
    blk = mat('blk', '#000000', rough=1)
    c0 = sdir * 1.6 + Vector((0.05, 0.05, 0))
    q = sdir.to_track_quat('Z', 'Y')
    def wbox(sx, sy, ox, oy):
        o_ = box('wb', (sx, sy, 0.02), (0, 0, 0), blk); o_.matrix_world = Matrix.Translation(c0) @ q.to_matrix().to_4x4() @ Matrix.Translation((ox, oy, 0))
        o_.visible_camera = False; o_.visible_glossy = False
    wo, hgt = 0.62, 0.8                                           # window opening
    wbox(3, 1.5, 0, hgt / 2 + 0.75); wbox(3, 1.5, 0, -hgt / 2 - 0.75); wbox(1.2, hgt, -wo / 2 - 0.6, 0); wbox(1.2, hgt, wo / 2 + 0.6, 0)
    wbox(0.035, hgt, 0, 0); wbox(wo, 0.035, 0, 0.12)                # mullions
    cam = camera((0.34, 0.06, 1.55), (0.0, 0.02, 0.0), 58)
    bpy.context.scene.view_settings.exposure = 0.0
    area_light((0.9, 0.4, 1.6), (0, 0, 0), 2.0, 22)  # soft bounce fill
    # aim with Y as world-up (this scene is Y-up)
    fwd = (Vector((0.0, 0.02, 0.0)) - cam.location).normalized(); z = -fwd; x = Vector((0, 1, 0)).cross(z).normalized(); y = z.cross(x)
    cam.rotation_euler = Matrix((x, y, z)).transposed().to_euler()
    render(out)

if __name__ == '__main__':
    a = sys.argv[1:]
    cw, out = a[0], a[1]; w, h, spp = (int(a[2]), int(a[3]), int(a[4])) if len(a) > 4 else (1280, 1600, 160)
    scene(cw, out, w, h, spp)
