"""Mustard Bio facility: building exterior and cleanroom corridor, Cycles. Usage: python facility.py <facade|corridor> <out.png> [w h spp]"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blib import *

ART = os.path.join(HERE, '..', 'render', 'art')

def box(name, size, loc, m, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.name = name; o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    if bev: bevel(o, bev, 2)
    assign(o, m); return o

def array(o, count, offset, axis=0):
    a = o.modifiers.new('arr', 'ARRAY'); a.count = count; a.use_relative_offset = False; a.use_constant_offset = True
    v = [0, 0, 0]; v[axis] = offset; a.constant_offset_displace = v; return o

def emissive(name, color='#ffffff', strength=6.0):
    m = mat(name, color, rough=0.5); b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Emission Color'].default_value = hexc(color); b.inputs['Emission Strength'].default_value = strength; return m

def scene_facade(out, w, h, spp):
    reset(w, h, spp)
    world_hdri('kloofendal_48d_partly_cloudy_puresky', 1.0, rot=2.2)
    L, D, H = 46.0, 18.0, 9.5
    sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 3.2; sun.angle = math.radians(1.5)
    so = bpy.data.objects.new('sun', sun); bpy.context.scene.collection.objects.link(so); so.rotation_euler = (math.radians(52), 0, math.radians(-38))
    ground = mat('asphalt', '#55595a', rough=0.85); nt = ground.node_tree; bb = nt.nodes['Principled BSDF']
    tcg = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 60; nz.inputs['Detail'].default_value = 12; nt.links.new(tcg.outputs['Object'], nz.inputs['Vector'])
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = hexc('#4a4e4f'); cr.color_ramp.elements[1].color = hexc('#6a6e6c')
    nt.links.new(nz.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], bb.inputs['Base Color'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.35; nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], bb.inputs['Normal'])
    bpy.ops.mesh.primitive_plane_add(size=400); g = bpy.context.object; assign(g, ground)
    # concrete apron along the building and parking bay lines
    ap = mat('apron', '#cfd1cb', rough=0.8); ant = ap.node_tree; ab = ant.nodes['Principled BSDF']
    atc = ant.nodes.new('ShaderNodeTexCoord'); an = ant.nodes.new('ShaderNodeTexNoise'); an.inputs['Scale'].default_value = 25; an.inputs['Detail'].default_value = 10; ant.links.new(atc.outputs['Object'], an.inputs['Vector'])
    acr = ant.nodes.new('ShaderNodeValToRGB'); acr.color_ramp.elements[0].color = hexc('#c3c5bf'); acr.color_ramp.elements[1].color = hexc('#dadcd5'); ant.links.new(an.outputs['Fac'], acr.inputs['Fac']); ant.links.new(acr.outputs['Color'], ab.inputs['Base Color'])
    box('apron', (L + 6, 7.0, 0.03), (0, -3.5, 0.015), ap)
    for i in range(18):
        box('joint', (0.015, 7.0, 0.002), (-L / 2 - 3 + i * 3.0, -3.5, 0.031), mat('jnt', '#9fa29c', rough=0.9))
    for i in range(10):
        box('bay', (0.12, 5.0, 0.005), (-8 + i * 2.8, -11.0, 0.004), mat('paint', '#E7E8E1', rough=0.7))
    # distant tree line for scale
    import random; random.seed(2)
    for i in range(40):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=2.5 + random.random() * 2, location=(-90 + i * 4.6, 60 + random.random() * 8, 2.5)); t_ = bpy.context.object; t_.scale.z = 1.3
        assign(t_, mat('tree', '#4f5f45', rough=0.9))
    clad = mat('clad', '#222F30', rough=0.42, metal=0.35, coat=0.2)
    wallcore = mat('core', '#1a2425', rough=0.6)
    plinthm = tex_mat('plinth', 'grey_plaster', scale=6, rough_mul=1.0, bump=0.2, tint='#E7E8E1')
    box('shell', (L, D, H), (0, D / 2, H / 2), wallcore)
    # vertical ribbed cladding (trapezoidal profile approximated by thin fins)
    rib = box('rib', (0.07, 0.09, H - 1.2), (-L / 2 + 0.1, -0.045, 1.2 + (H - 1.2) / 2), clad, bev=0.01); array(rib, int(L / 0.25), 0.25)
    # side wall ribs
    rib2 = box('rib2', (0.09, 0.07, H - 1.2), (L / 2 + 0.045, 0.1, 1.2 + (H - 1.2) / 2), clad, bev=0.01); array(rib2, int(D / 0.25), 0.25, axis=1)
    box('plinth', (L + 0.2, 0.25, 1.2), (0, -0.02, 0.6), plinthm)
    box('plinthS', (0.25, D + 0.2, 1.2), (L / 2 + 0.02, D / 2, 0.6), plinthm)
    box('parapet', (L + 0.3, D + 0.3, 0.25), (0, D / 2, H + 0.1), mat('cap', '#C7CBCA', rough=0.3, metal=0.9))
    # glazed entrance block with curtain wall
    gx0, gw, gh = -L / 2 + 3.0, 15.0, 6.2
    box('glzback', (gw, 0.1, gh), (gx0 + gw / 2, -0.25, gh / 2), mat('interior', '#2b3536', rough=0.8))
    glassm = mat('glz', '#BFD3D0', rough=0.02, trans=0.0, metal=0.0, coat=1.0, coat_rough=0.0, spec=1.0)
    gl = box('glz', (gw, 0.03, gh), (gx0 + gw / 2, -1.25, gh / 2), glassm)
    glassm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = hexc('#2f3d3e')
    mull = mat('mull', '#C9CCCB', rough=0.3, metal=0.9)
    mv = box('mullV', (0.08, 0.18, gh), (gx0, -1.3, gh / 2), mull); array(mv, 11, gw / 10)
    mh = box('mullH', (gw, 0.16, 0.08), (gx0 + gw / 2, -1.3, 2.4), mull); array(mh, 3, 1.9, axis=2)
    box('glzSide', (0.03, 1.2, gh), (gx0 + gw, -0.65, gh / 2), glassm)
    box('glzRoof', (gw + 0.3, 1.5, 0.35), (gx0 + gw / 2, -0.7, gh + 0.17), clad)
    # lime soffit band + canopy
    box('soffit', (gw + 0.3, 1.2, 0.06), (gx0 + gw / 2, -0.7, gh - 0.02), emissive('lime', '#A7E26E', 0.6))
    box('canopy', (6.0, 3.2, 0.3), (gx0 + 3.6, -2.6, 3.4), clad, bev=0.02)
    for x in (gx0 + 1.0, gx0 + 6.2):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=3.3, location=(x, -4.0, 1.65)); assign(bpy.context.object, mull)
    # sign: illuminated panel on the cladding
    sign = os.path.join(ART, 'facade-sign.png')
    bpy.ops.mesh.primitive_plane_add(size=1, location=(gx0 + gw + 9.5, -0.2, H - 2.6), rotation=(math.pi / 2, 0, 0)); sp = bpy.context.object
    sp.scale = (13.0, 13.0 * 520 / 2400, 1); m, img = decal_mat('signm', sign, rough=0.4, emission=0.35); assign(sp, m)
    box('signback', (13.3, 0.12, 13.0 * 520 / 2400 + 0.3), (gx0 + gw + 9.5, -0.1, H - 2.6), mat('sb', '#1a2425', rough=0.5))
    # loading dock doors
    dock = mat('dock', '#C9CCCB', rough=0.45, metal=0.6)
    for i in range(3):
        d = box('door', (3.6, 0.08, 4.2), (gx0 + gw + 6 + i * 5.2 + 2.5, -0.15, 2.1), dock)
        bpy.ops.mesh.primitive_cube_add(size=1); s_ = bpy.context.object; s_.scale = (3.6, 0.1, 0.03); s_.location = (d.location.x, -0.2, 0.4); array(s_, 14, 0.27, axis=2); assign(s_, mat('slat', '#AEB3B2', rough=0.5, metal=0.6))
    # kerb, path, planting strip
    box('kerb', (L + 6, 0.2, 0.15), (0, -6.5, 0.075), plinthm)
    box('path', (8, 5.5, 0.02), (gx0 + 3.6, -3.4, 0.01), tex_mat('paving', 'concrete_floor_02', scale=3, tint='#e2e3dc'))
    for i in range(9):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=0.55, location=(gx0 + gw + 1 + i * 1.2, -1.2, 0.3)); b_ = bpy.context.object; b_.scale.z = 0.7
        displace = b_.modifiers.new('d', 'DISPLACE'); t = bpy.data.textures.new('lf', 'CLOUDS'); t.noise_scale = 0.12; displace.texture = t; displace.strength = 0.25
        assign(b_, mat('shrub', '#56684a', rough=0.8, sss=0.1))
    camera((-27.0, -17.5, 1.65), (-4.0, 1.0, 5.0), 30)
    bpy.context.scene.view_settings.exposure = -0.3
    render(out)

def scene_corridor(out, w, h, spp):
    reset(w, h, spp)
    world_hdri('studio_small_09', 0.05)
    W, Lc, Hc = 2.6, 22.0, 3.0
    floor = mat('epoxy', '#C9CBBE', rough=0.18, coat=1.0, coat_rough=0.08)
    box('floor', (W, Lc, 0.05), (0, Lc / 2, -0.025), floor)
    box('guide', (0.08, Lc, 0.002), (-W / 2 + 0.35, Lc / 2, 0.001), mat('gl', '#A7E26E', rough=0.3, coat=0.8))
    wallm = mat('panel', '#F4F5F2', rough=0.35, coat=0.3)
    for side in (-1, 1):
        box('wall', (0.06, Lc, Hc), (side * W / 2, Lc / 2, Hc / 2), wallm)
        j = box('joint', (0.065, 0.006, Hc), (side * (W / 2 - 0.001), 1.2, Hc / 2), mat('jt', '#d5d8d3', rough=0.5)); array(j, 18, 1.2, axis=1)
        box('cove', (0.07, Lc, 0.1), (side * (W / 2 - 0.02), Lc / 2, 0.05), mat('cv', '#E7E8E1', rough=0.3, coat=0.5))
        box('rail', (0.04, Lc, 0.12), (side * (W / 2 - 0.05), Lc / 2, 1.0), mat('rl', '#C9CCCB', rough=0.25, metal=0.9))
    box('ceil', (W, Lc, 0.05), (0, Lc / 2, Hc + 0.025), mat('ceil', '#F7F7F5', rough=0.6))
    for i in range(9):
        box('led', (1.2, 0.6, 0.02), (0, 1.4 + i * 2.4, Hc - 0.005), emissive('led', '#ffffff', 7.0))
    # end wall + double door with vision panels
    box('end', (W, 0.06, Hc), (0, Lc, Hc / 2), wallm)
    doorm = mat('door', '#E7E8E1', rough=0.3, coat=0.6)
    for side in (-1, 1):
        d = box('door', (W * 0.42, 0.06, 2.3), (side * W * 0.215, Lc - 0.05, 1.15), doorm)
        box('vp', (0.35, 0.065, 0.6), (side * W * 0.215, Lc - 0.05, 1.55), mat('vpg', '#5a6866', rough=0.05, coat=1.0))
        box('kick', (W * 0.42, 0.065, 0.25), (side * W * 0.215, Lc - 0.05, 0.13), mat('kick', '#C9CCCB', rough=0.25, metal=1.0))
    box('doorsign', (0.9, 0.065, 0.16), (0, Lc - 0.05, 2.5), mat('ds', '#222F30', rough=0.4))
    # side doors along the corridor
    for y in (6.0, 13.0):
        box('sdoor', (0.07, 1.1, 2.2), (W / 2 - 0.01, y, 1.1), doorm)
        box('svp', (0.075, 0.3, 0.55), (W / 2 - 0.01, y, 1.5), mat('vpg', '#5a6866', rough=0.05, coat=1.0))
        box('zone', (0.075, 0.5, 0.12), (W / 2 - 0.01, y, 2.38), mat('zn', '#222F30', rough=0.4))
    # wayfinding directory on the left wall, facing into the corridor
    bpy.ops.mesh.primitive_plane_add(size=1, location=(-W / 2 + 0.047, 3.6, 1.65), rotation=(math.pi / 2, 0, math.pi / 2)); sg = bpy.context.object
    sg.scale = (0.9, 1.2, 1); m, _ = decal_mat('wf', os.path.join(ART, 'wayfinding.png'), rough=0.3, coat=0.6); assign(sg, m)
    box('wfback', (0.02, 0.92, 1.22), (-W / 2 + 0.03, 3.6, 1.65), mat('wb', '#ffffff', rough=0.4))
    # cleanroom pass box on the right
    box('passbox', (0.08, 0.7, 0.6), (W / 2 - 0.04, 9.6, 1.2), mat('pb', '#C9CCCB', rough=0.25, metal=1.0), bev=0.01)
    camera((0.35, 0.4, 1.58), (-0.25, 8.0, 1.4), 22)
    render(out)

def scene_billboard(out, w, h, spp):
    reset(w, h, spp)
    world_hdri('kloofendal_48d_partly_cloudy_puresky', 1.0, rot=1.6)
    sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 3.0; sun.angle = math.radians(1.5)
    so = bpy.data.objects.new('sun', sun); bpy.context.scene.collection.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-30))
    gm = mat('verge', '#7d8a6a', rough=0.95); nt = gm.node_tree; bb = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3; nz.inputs['Detail'].default_value = 12
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = hexc('#6b7a58'); cr.color_ramp.elements[1].color = hexc('#9aa486')
    nt.links.new(nz.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], bb.inputs['Base Color'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.5; nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], bb.inputs['Normal'])
    bpy.ops.mesh.primitive_plane_add(size=400); assign(bpy.context.object, gm)
    steel = mat('steel', '#5d6766', rough=0.45, metal=0.8)
    frame = mat('frame', '#222F30', rough=0.4, metal=0.3)
    W, Hp, base = 12.0, 4.0, 6.2          # 48-sheet proportions (3:1), panel bottom at 6.2 m
    zc = base + Hp / 2
    # poster face + frame
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -0.16, zc), rotation=(math.pi / 2, 0, 0)); face = bpy.context.object; face.scale = (W, Hp, 1)
    fm, _ = decal_mat('poster', os.path.join(ART, 'billboard.png'), rough=0.55); assign(face, fm)
    box('back', (W + 0.3, 0.3, Hp + 0.3), (0, 0.0, zc), frame, bev=0.03)
    box('trimT', (W + 0.3, 0.12, 0.12), (0, -0.2, base + Hp + 0.09), frame, bev=0.01)
    box('trimB', (W + 0.3, 0.12, 0.12), (0, -0.2, base - 0.09), frame, bev=0.01)
    for sx in (-1, 1): box('trimS', (0.12, 0.12, Hp + 0.3), (sx * (W / 2 + 0.09), -0.2, zc), frame, bev=0.01)
    # structure: two columns, cross beam, catwalk
    for x in (-3.4, 3.4):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.28, depth=base + 0.6, location=(x, 0.45, (base + 0.6) / 2)); assign(bpy.context.object, steel)
        box('footing', (1.0, 1.0, 0.25), (x, 0.45, 0.12), mat('conc', '#b8bab3', rough=0.9))
    box('beam', (W, 0.25, 0.35), (0, 0.4, base - 0.3), steel)
    box('catwalk', (W, 1.0, 0.06), (0, -0.55, base - 1.2), mat('grate', '#7a8382', rough=0.5, metal=0.8))
    rail = box('rail', (W, 0.04, 0.04), (0, -1.03, base - 0.25), steel)  # rail top stays below the poster
    for i in range(13): box('post', (0.04, 0.04, 0.95), (-W / 2 + i * W / 12, -1.03, base - 0.72), steel)
    # four floodlights: plate bolted to the top trim, arm running forward, head angled back at the poster
    for i in range(4):
        x = -W / 2 + W / 8 + i * W / 4
        ztop = base + Hp + 0.15
        box('plate', (0.3, 0.3, 0.04), (x, -0.1, ztop + 0.02), steel)                                   # sits on the frame top
        arm = box('arm', (0.08, 1.15, 0.08), (x, -0.1 - 0.55, ztop + 0.08), steel)                      # starts over the plate
        box('riser', (0.08, 0.08, 0.22), (x, -0.1, ztop + 0.13), steel)                                 # ties arm to plate
        hd = box('head', (0.6, 0.28, 0.16), (x, -1.25, ztop + 0.02), frame, bev=0.02)
        hd.rotation_euler.x = math.radians(-35)                                                          # tipped back toward the face
        bpy.ops.mesh.primitive_plane_add(size=1, location=(x, -1.2, ztop - 0.045), rotation=(math.radians(-35), 0, 0)); lens = bpy.context.object
        lens.scale = (0.5, 0.2, 1); lens.rotation_euler.x = math.radians(180 - 35); assign(lens, emissive('lens', '#fff6e6', 2.0))
    camera((-9.0, -22.0, 1.7), (0.6, 0.0, zc + 0.2), 40)
    bpy.context.scene.view_settings.exposure = -0.2
    render(out)

SCENES = {'facade': scene_facade, 'corridor': scene_corridor, 'billboard': scene_billboard}

if __name__ == '__main__':
    a = sys.argv[1:]
    name, out = a[0], a[1]; w, h, spp = (int(a[2]), int(a[3]), int(a[4])) if len(a) > 4 else (1600, 1200, 160)
    SCENES[name](out, w, h, spp)
