"""Woven lanyard with breakaway buckle, rivets, threaded through a slotted ID card; visitor pass beside. Cycles.
Usage: python lanyard3d.py <out.png> [w h spp]"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blib import *
from merch import catmull, floor_paper
from mathutils import Vector

DEC = os.path.join(HERE, '..', 'render', 'decal')
STAT = os.path.join(HERE, '..', 'render', 'stat')

def rounded_rect(w, h, r, n=8):
    pts = []
    for cx, cy, a0 in [(w / 2 - r, -h / 2 + r, -90), (w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180)]:
        for k in range(n + 1): a = math.radians(a0 + 90 * k / n); pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

def id_card(name, img, w=0.054, h=0.086, t=0.0008, slot=True, edge='#F7F7F5'):
    """PVC card: rounded corners, punched slot, artwork on the face (planar UV), satin laminate."""
    bm = bmesh.new(); vs = [bm.verts.new((x, y, 0)) for x, y in rounded_rect(w, h, 0.0032)]; f = bm.faces.new(vs)
    bmesh.ops.triangulate(bm, faces=[f])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    so = o.modifiers.new('s', 'SOLIDIFY'); so.thickness = t; so.offset = 1; bpy.ops.object.modifier_apply(modifier='s')
    if slot:
        bm = bmesh.new(); vs = [bm.verts.new((x, y + h / 2 - 0.0065, -0.001)) for x, y in rounded_rect(0.015, 0.0032, 0.0015, 6)]; bm.faces.new(vs)
        cm = bpy.data.meshes.new('slot'); bm.to_mesh(cm); bm.free(); c = bpy.data.objects.new('slot', cm); bpy.context.scene.collection.objects.link(c)
        sc = c.modifiers.new('s', 'SOLIDIFY'); sc.thickness = 0.004; sc.offset = 1
        b = o.modifiers.new('b', 'BOOLEAN'); b.object = c; b.operation = 'DIFFERENCE'; b.solver = 'EXACT'
        bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier='b'); bpy.data.objects.remove(c)
    me = o.data; uvl = me.uv_layers.new(name='UVMap'); me.uv_layers.active = uvl; uvl.active_render = True
    face_m = decal_mat(name + '_f', img, rough=0.32, coat=0.5, paper_bump=0.0)[0]; face_m.node_tree.nodes['Principled BSDF'].inputs['Coat Roughness'].default_value = 0.25
    me.materials.clear()  # the slot boolean leaves an empty slot behind
    me.materials.append(mat(name + '_e', edge, rough=0.35, coat=0.4)); me.materials.append(face_m)
    for p in me.polygons:
        top = abs(p.normal.z) > 0.9 and p.center.z > t * 0.5; p.material_index = 1 if top else 0  # top face by height (solidify may flip normals)
        for li in p.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co; uvl.data[li].uv = (v.x / w + 0.5, v.y / h + 0.5)
    me.update(); me.flip_normals() if any(p.normal.z < -0.9 and p.center.z > t * 0.5 for p in me.polygons) else None
    for p in me.polygons: p.use_smooth = False
    return o

def woven(name, color):
    m = mat(name, color, rough=0.75, sheen=0.6); nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Sheen Roughness'].default_value = 0.4
    # print
    im = nt.nodes.new('ShaderNodeTexImage'); im.image = bpy.data.images.load(os.path.join(DEC, 'lanyard.png'), check_existing=True); im.interpolation = 'Cubic'
    uv = nt.nodes.new('ShaderNodeUVMap'); nt.links.new(uv.outputs['UV'], im.inputs['Vector'])
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.inputs['A'].default_value = hexc(color)
    nt.links.new(im.outputs['Alpha'], mix.inputs['Factor']); nt.links.new(im.outputs['Color'], mix.inputs['B']); nt.links.new(mix.outputs['Result'], b.inputs['Base Color'])
    # fine polyester weave: two crossed wave textures as bump, in UV space
    def wave(rot):
        wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'X' if rot == 0 else 'Y'; wv.inputs['Scale'].default_value = 900
        nt.links.new(uv.outputs['UV'], wv.inputs['Vector']); return wv
    w1, w2 = wave(0), wave(1)
    add = nt.nodes.new('ShaderNodeMath'); add.operation = 'MULTIPLY'; nt.links.new(w1.outputs['Fac'], add.inputs[0]); nt.links.new(w2.outputs['Fac'], add.inputs[1])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.35; bp.inputs['Distance'].default_value = 0.0002
    nt.links.new(add.outputs['Value'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m

def strap(name, pts, width, m, th=0.0011, u_len=0.16):
    """Flat strap along 3D points; UV u runs along the length (one print repeat per u_len metres)."""
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new(); rows = []; acc = [0.0]
    for i in range(1, len(pts)): acc.append(acc[-1] + (Vector(pts[i]) - Vector(pts[i - 1])).length)
    for i, p in enumerate(pts):
        a = Vector(pts[max(0, i - 1)]); b = Vector(pts[min(len(pts) - 1, i + 1)]); t = (b - a).normalized()
        n = Vector((-t.y, t.x, 0)).normalized() * (width / 2)
        rows.append((bm.verts.new(Vector(p) + n), bm.verts.new(Vector(p) - n)))
    for i in range(len(rows) - 1):
        f = bm.faces.new((rows[i][0], rows[i][1], rows[i + 1][1], rows[i + 1][0]))
        for lp, (u, v) in zip(f.loops, [(acc[i], 1), (acc[i], 0), (acc[i + 1], 0), (acc[i + 1], 1)]): lp[uvl].uv = (u / u_len, v)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    s = o.modifiers.new('s', 'SOLIDIFY'); s.thickness = th; s.offset = 1
    assign(o, m); return o

def path(ctrl, n=12, z=0.0):
    pts = catmull(ctrl, n, closed=False); return [(x, y, z) for x, y in pts]

def scene(out, w, h, spp):
    reset(w, h, spp)
    world_hdri('studio_small_09', 0.14, rot=0.7); floor_paper('#E6E5DF')
    card = id_card('staff', os.path.join(STAT, 'staff-id-front.png'))
    card.location = (0.0, -0.07, 0.0); card.rotation_euler.z = math.radians(-6)
    vp = id_card('visitor', os.path.join(STAT, 'visitor-pass.png'), edge='#A7E26E')
    vp.location = (0.095, -0.06, 0.0); vp.rotation_euler.z = math.radians(9)
    sage = woven('lanyard', '#B9BCAC')
    slot_world = card.matrix_world @ Vector((0, 0.086 / 2 - 0.0065, 0.0008))
    # short strap: from the card slot up to the buckle (sits on top of the card face, folded through the slot)
    bx, by = slot_world.x - 0.004, slot_world.y + 0.075
    strap('tab', [(slot_world.x, slot_world.y - 0.004, 0.0009), (slot_world.x + 0.0, slot_world.y + 0.01, 0.0012), (bx, by - 0.016, 0.0016)], 0.02, sage, u_len=0.16)
    # main loop: up from the buckle, round the top, down the right and out of frame
    main = path([(bx, by + 0.016), (bx - 0.006, by + 0.12), (bx + 0.02, by + 0.23), (bx + 0.075, by + 0.27), (bx + 0.12, by + 0.22), (bx + 0.16, by + 0.08), (bx + 0.22, by - 0.08), (bx + 0.29, by - 0.22)], 14, 0.0016)
    strap('loop', main, 0.02, sage)
    # breakaway buckle (black matte plastic) with round release button
    plastic = mat('plastic', '#141819', rough=0.45, coat=0.1)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(bx, by, 0.004)); bk = bpy.context.object; bk.scale = (0.026, 0.03, 0.0075)
    bpy.ops.object.transform_apply(scale=True); bevel(bk, 0.0018, 4); assign(bk, plastic)
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.0085, depth=0.0016, location=(bx, by + 0.002, 0.0083)); bt = bpy.context.object; bevel(bt, 0.0006, 3); bpy.ops.object.shade_smooth(); assign(bt, plastic)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(bx, by - 0.0135, 0.0045)); sl = bpy.context.object; sl.scale = (0.022, 0.0016, 0.006); assign(sl, mat('slotlite', '#c9cfce', rough=0.3, metal=1.0))
    # rivets above and below the buckle
    chrome = mat('chrome', '#d9dddc', rough=0.12, metal=1.0)
    for ry in (by + 0.032, by - 0.034):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.0026, location=(bx, ry, 0.0026)); r = bpy.context.object; r.scale.z = 0.45; bpy.ops.object.shade_smooth(); assign(r, chrome)
    area_light((-0.35, 0.3, 0.45), (0.02, 0.05, 0), 0.4, 9)
    area_light((0.4, -0.3, 0.35), (0.02, 0.05, 0), 0.5, 3)
    cam = camera((0.05, -0.29, 0.40), (0.05, 0.0, 0.0), 45, dof=True, fstop=22)
    render(out)

if __name__ == '__main__':
    a = sys.argv[1:]; out = a[0]; w, h, spp = (int(a[1]), int(a[2]), int(a[3])) if len(a) > 3 else (2400, 1800, 160)
    scene(out, w, h, spp)
