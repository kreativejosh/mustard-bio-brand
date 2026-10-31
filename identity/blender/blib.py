"""Shared Blender (Cycles) helpers for Mustard Bio renders: studio sweep, HDRI light, PBR materials, decals."""
import bpy, bmesh, math, os
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
PH = os.path.join(HERE, 'ph')
ART = os.path.join(HERE, '..', 'render', 'art')

def hexc(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]  # sRGB -> linear
    return (*c, a)

C = dict(charcoal='#222F30', deepsea='#445E5F', sage='#C9CBBE', lime='#A7E26E', mint='#CEF79E',
         offwhite='#F7F7F5', stone='#E7E8E1', g1='#EEEEEE', g2='#E4E3E3', white='#FFFFFF')

def reset(w=1600, h=1200, samples=128, exposure=0.0, look='AgX - Medium High Contrast'):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.engine = 'CYCLES'
    s.cycles.device = 'CPU'
    s.cycles.samples = samples
    s.cycles.use_adaptive_sampling = True
    s.cycles.adaptive_threshold = 0.02
    s.cycles.use_denoising = True
    try: s.cycles.denoiser = 'OPENIMAGEDENOISE'
    except Exception: pass
    s.cycles.max_bounces = 16; s.cycles.transmission_bounces = 16; s.cycles.glossy_bounces = 8
    s.cycles.caustics_reflective = True; s.cycles.caustics_refractive = True
    s.cycles.blur_glossy = 0.5
    s.render.resolution_x, s.render.resolution_y, s.render.resolution_percentage = w, h, 100
    s.render.film_transparent = False
    try: s.view_settings.view_transform = 'Khronos PBR Neutral'
    except Exception:
        s.view_settings.view_transform = 'AgX'
        try: s.view_settings.look = look
        except Exception: pass
    s.view_settings.exposure = exposure
    s.render.image_settings.file_format = 'PNG'
    s.render.threads_mode = 'AUTO'
    return s

def world_hdri(name, strength=1.0, rot=0.0, bg=None, bg_strength=1.0):
    """HDRI lights the scene; if bg given, the camera sees a flat colour instead (lighting unaffected)."""
    w = bpy.data.worlds.new('W'); bpy.context.scene.world = w; w.use_nodes = True
    nt = w.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputWorld')
    env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(os.path.join(PH, 'hdri', name + '.hdr'))
    mp = nt.nodes.new('ShaderNodeMapping'); tc = nt.nodes.new('ShaderNodeTexCoord')
    mp.inputs['Rotation'].default_value[2] = rot
    nt.links.new(tc.outputs['Generated'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], env.inputs['Vector'])
    bgn = nt.nodes.new('ShaderNodeBackground'); bgn.inputs['Strength'].default_value = strength
    nt.links.new(env.outputs['Color'], bgn.inputs['Color'])
    if bg is None:
        nt.links.new(bgn.outputs['Background'], out.inputs['Surface'])
    else:
        flat = nt.nodes.new('ShaderNodeBackground'); flat.inputs['Color'].default_value = hexc(bg); flat.inputs['Strength'].default_value = bg_strength
        lp = nt.nodes.new('ShaderNodeLightPath'); mix = nt.nodes.new('ShaderNodeMixShader')
        nt.links.new(lp.outputs['Is Camera Ray'], mix.inputs['Fac'])
        nt.links.new(bgn.outputs['Background'], mix.inputs[1]); nt.links.new(flat.outputs['Background'], mix.inputs[2])
        nt.links.new(mix.outputs['Shader'], out.inputs['Surface'])
    return w

def mat(name, base='#ffffff', rough=0.5, metal=0.0, coat=0.0, coat_rough=0.1, trans=0.0, ior=1.45, sheen=0.0, sss=0.0, spec=0.5, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = hexc(base) if isinstance(base, str) else base
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    b.inputs['Coat Weight'].default_value = coat; b.inputs['Coat Roughness'].default_value = coat_rough
    b.inputs['Transmission Weight'].default_value = trans; b.inputs['IOR'].default_value = ior
    b.inputs['Sheen Weight'].default_value = sheen
    b.inputs['Subsurface Weight'].default_value = sss
    b.inputs['Subsurface Scale'].default_value = 0.002
    b.inputs['Specular IOR Level'].default_value = spec
    b.inputs['Alpha'].default_value = alpha
    return m

def glass(name='glass', tint='#F2FBF4', rough=0.0, ior=1.5, absorb=None, dens=0.0):
    m = mat(name, tint, rough=rough, trans=1.0, ior=ior)
    if absorb:  # volume absorption for coloured thick glass / liquid
        nt = m.node_tree; va = nt.nodes.new('ShaderNodeVolumeAbsorption')
        va.inputs['Color'].default_value = hexc(absorb); va.inputs['Density'].default_value = dens
        nt.links.new(va.outputs['Volume'], nt.nodes['Material Output'].inputs['Volume'])
    return m

def _img(path, non_color=False):
    im = bpy.data.images.load(path, check_existing=True)
    if non_color: im.colorspace_settings.name = 'Non-Color'
    return im

def tex_mat(name, folder, scale=1.0, tint=None, rough_mul=1.0, bump=0.4, sheen=0.0, disp=0.0, base_override=None):
    """PBR material from a Poly Haven texture folder (diff/nor/rough/disp)."""
    d = os.path.join(PH, 'tex', folder)
    m = mat(name, sheen=sheen); nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (scale, scale, scale)
    nt.links.new(tc.outputs['UV'], mp.inputs['Vector'])
    def node(f, nc):
        n = nt.nodes.new('ShaderNodeTexImage'); n.image = _img(os.path.join(d, f), nc); nt.links.new(mp.outputs['Vector'], n.inputs['Vector']); return n
    if os.path.exists(os.path.join(d, 'diff.jpg')) and base_override is None:
        dn = node('diff.jpg', False)
        if tint:
            mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'; mix.inputs['Factor'].default_value = 1.0
            nt.links.new(dn.outputs['Color'], mix.inputs['A']); mix.inputs['B'].default_value = hexc(tint)
            nt.links.new(mix.outputs['Result'], b.inputs['Base Color'])
        else: nt.links.new(dn.outputs['Color'], b.inputs['Base Color'])
    elif base_override is not None:
        b.inputs['Base Color'].default_value = hexc(base_override)
    if os.path.exists(os.path.join(d, 'rough.jpg')):
        rn = node('rough.jpg', True); mm = nt.nodes.new('ShaderNodeMath'); mm.operation = 'MULTIPLY'; mm.inputs[1].default_value = rough_mul
        nt.links.new(rn.outputs['Color'], mm.inputs[0]); nt.links.new(mm.outputs['Value'], b.inputs['Roughness'])
    if os.path.exists(os.path.join(d, 'nor.jpg')):
        nn = node('nor.jpg', True); nm = nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = bump
        nt.links.new(nn.outputs['Color'], nm.inputs['Color']); nt.links.new(nm.outputs['Normal'], b.inputs['Normal'])
    return m

def decal_mat(name, img_path, base_under=None, rough=0.5, coat=0.0, sheen=0.0, paper_bump=0.0, metal=0.0, emission=0.0):
    """Material whose colour comes from an artwork image mapped by UV (labels, prints, cards)."""
    m = mat(name, rough=rough, coat=coat, sheen=sheen, metal=metal); nt = m.node_tree; b = nt.nodes['Principled BSDF']
    n = nt.nodes.new('ShaderNodeTexImage'); n.image = _img(img_path); n.extension = 'CLIP'; n.interpolation = 'Cubic'
    tc = nt.nodes.new('ShaderNodeTexCoord'); nt.links.new(tc.outputs['UV'], n.inputs['Vector'])
    if base_under:
        mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.inputs['A'].default_value = hexc(base_under)
        nt.links.new(n.outputs['Alpha'], mix.inputs['Factor']); nt.links.new(n.outputs['Color'], mix.inputs['B'])
        nt.links.new(mix.outputs['Result'], b.inputs['Base Color'])
    else: nt.links.new(n.outputs['Color'], b.inputs['Base Color'])
    if emission:
        nt.links.new(n.outputs['Color'], b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value = emission
    if paper_bump:
        nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 900; nz.inputs['Detail'].default_value = 8
        bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = paper_bump; bp.inputs['Distance'].default_value = 0.0005
        nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m, n

def assign(o, m, slot=None):
    if slot is None: o.data.materials.clear(); o.data.materials.append(m)
    else: o.data.materials.append(m)
    return o

def smooth(o, angle=40):
    for p in o.data.polygons: p.use_smooth = True
    try:
        mod = o.modifiers.new('ws', 'WEIGHTED_NORMAL')
    except Exception: pass
    return o

def subsurf(o, lv=2):
    m = o.modifiers.new('sub', 'SUBSURF'); m.levels = lv; m.render_levels = lv; return o

def bevel(o, w=0.002, seg=3):
    m = o.modifiers.new('bev', 'BEVEL'); m.width = w; m.segments = seg; m.limit_method = 'ANGLE'; return o

def cyclorama(color='#E7E8E1', w=40, d=30, h=15, r=6, rough=0.85, mat_override=None):
    """Infinite studio sweep: floor curving up into a back wall."""
    bpy.ops.mesh.primitive_plane_add(size=1)
    o = bpy.context.object; o.name = 'sweep'
    bm = bmesh.new(); prof = []
    for i in range(0, 25): y = -d / 2 + i * ((d - r) / 24); prof.append((y, 0))  # flat floor from front edge to the curve (y = depth axis)
    for i in range(1, 17): a = i / 16 * math.pi / 2; prof.append((d / 2 - r + math.sin(a) * r, r - math.cos(a) * r))
    for i in range(1, 6): prof.append((d / 2, r + i * (h - r) / 5))
    verts = []
    for x in (-w / 2, w / 2):
        verts.append([bm.verts.new((x, y, z)) for (y, z) in prof])
    for i in range(len(prof) - 1):
        bm.faces.new((verts[0][i], verts[1][i], verts[1][i + 1], verts[0][i + 1]))
    bm.to_mesh(o.data); bm.free()
    for p in o.data.polygons: p.use_smooth = True
    assign(o, mat_override or mat('sweep', color, rough=rough))
    return o

def camera(loc, target, lens=50, dof=None, fstop=4.0, sensor=36):
    cam = bpy.data.objects.new('Cam', bpy.data.cameras.new('Cam')); bpy.context.scene.collection.objects.link(cam)
    cam.location = loc; cam.data.lens = lens; cam.data.sensor_width = sensor
    d = Vector(target) - Vector(loc); cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    if dof:
        cam.data.dof.use_dof = True; cam.data.dof.focus_distance = d.length if dof is True else float(dof); cam.data.dof.aperture_fstop = fstop
    bpy.context.scene.camera = cam
    return cam

def ortho_camera(loc, target, scale):
    cam = camera(loc, target); cam.data.type = 'ORTHO'; cam.data.ortho_scale = scale; return cam

def area_light(loc, target, size=4, power=500, color='#ffffff', shape='RECTANGLE', size_y=None):
    l = bpy.data.lights.new('A', 'AREA'); l.energy = power; l.color = hexc(color)[:3]; l.shape = shape; l.size = size
    if size_y: l.size_y = size_y
    o = bpy.data.objects.new('A', l); bpy.context.scene.collection.objects.link(o); o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); return o

def lathe(name, prof, seg=128, close_top=False):
    """Revolve [(r, z), ...] around Z with UVs: u around, v by height."""
    bm = bmesh.new(); rings = []
    zs = [p[1] for p in prof]; z0, z1 = min(zs), max(zs)
    for i in range(seg):
        a = i / seg * 2 * math.pi
        rings.append([bm.verts.new((r * math.cos(a), r * math.sin(a), z)) for r, z in prof])
    uv = bm.loops.layers.uv.new()
    for i in range(seg):
        j = (i + 1) % seg
        for k in range(len(prof) - 1):
            f = bm.faces.new((rings[i][k], rings[j][k], rings[j][k + 1], rings[i][k + 1]))
            u0, u1 = i / seg, (i + 1) / seg
            for loop, (u, kk) in zip(f.loops, [(u0, k), (u1, k), (u1, k + 1), (u0, k + 1)]):
                loop[uv].uv = (u, (prof[kk][1] - z0) / (z1 - z0 + 1e-9))
    bm.normal_update()
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    for p in me.polygons: p.use_smooth = True
    return o

def card(name, w, h, t, front_img=None, back_img=None, edge='#ffffff', rough=0.6, coat=0.0, paper_bump=0.25):
    """Thin box with front/back artwork on UVs; edges in a paper colour."""
    bpy.ops.mesh.primitive_cube_add(size=1); o = bpy.context.object; o.name = name; o.scale = (w, h, t)
    bpy.ops.object.transform_apply(scale=True)
    me = o.data; uvl = me.uv_layers.active
    mats = [mat(name + '_edge', edge, rough=0.85)]
    if front_img: mats.append(decal_mat(name + '_f', front_img, rough=rough, coat=coat, paper_bump=paper_bump)[0])
    if back_img: mats.append(decal_mat(name + '_b', back_img, rough=rough, coat=coat, paper_bump=paper_bump)[0])
    for m in mats: me.materials.append(m)
    for p in me.polygons:
        n = p.normal
        if n.z > 0.9 and front_img: p.material_index = 1; side = 'f'
        elif n.z < -0.9 and back_img: p.material_index = 2 if front_img else 1; side = 'b'
        else: p.material_index = 0; continue
        for li in p.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co
            u = (v.x / w + 0.5); vv = (v.y / h + 0.5)
            if side == 'b': u = 1 - u
            uvl.data[li].uv = (u, vv)
    bevel(o, min(t * 0.3, 0.0004), 2)
    return o

def render(path):
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)

def import_gltf(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    return new
