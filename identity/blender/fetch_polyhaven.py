import json, urllib.request, os, sys
op = urllib.request.build_opener(); op.addheaders = [("User-Agent", "mustard-bio-brand-render/1.0")]; urllib.request.install_opener(op)
def get(u): return json.load(urllib.request.urlopen(u))
def dl(u, p):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if not os.path.exists(p): urllib.request.urlretrieve(u, p)
H = ['studio_small_09', 'photo_studio_01', 'studio_small_03', 'monochrome_studio_02', 'kloofendal_48d_partly_cloudy_puresky']
for h in H:
    try: f = get(f'https://api.polyhaven.com/files/{h}'); dl(f['hdri']['2k']['hdr']['url'], f'hdri/{h}.hdr'); print('hdri', h)
    except Exception as e: print('fail', h, e)
T = ['cotton_jersey', 'book_pattern', 'oak_veneer_01', 'grey_plaster', 'concrete_floor_02', 'leather_white']
for t in T:
    try:
        f = get(f'https://api.polyhaven.com/files/{t}')
        for m, key in [('Diffuse', 'diff'), ('nor_gl', 'nor'), ('Rough', 'rough'), ('Displacement', 'disp')]:
            if m in f: dl(f[m]['2k']['jpg']['url'] if 'jpg' in f[m]['2k'] else f[m]['2k']['png']['url'], f'tex/{t}/{key}.jpg')
        print('tex', t, os.listdir(f'tex/{t}'))
    except Exception as e: print('fail', t, e)
M = ['modular_factory_facade', 'industrial_microscope', 'chemistry_set', 'potted_plant_02', 'office_notepads', 'stationery_supplies']
for m in M:
    try:
        f = get(f'https://api.polyhaven.com/files/{m}')
        g = f['gltf']['1k']['gltf']; dl(g['url'], f'mod/{m}/{m}.gltf')
        for rel, inc in g.get('include', {}).items(): dl(inc['url'], f'mod/{m}/{rel}')
        print('model', m)
    except Exception as e: print('fail', m, e)
