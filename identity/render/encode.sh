set -e
cd "$(dirname "$0")"
NODE_PATH=$(npm root -g) node drive.js jv.json 2>&1 | grep -v Deprec
# crossfade loops for non-periodic clips (last 48 frames blend into first 48)
python3 - <<'PY'
from PIL import Image; import glob, os
for name in ['blob','flow','tubes']:
    fs=sorted(glob.glob(f'frames/{name}/f*.png')); n=len(fs); k=48
    out=f'frames/{name}-loop'; os.makedirs(out,exist_ok=True)
    for i in range(n-k):
        im=Image.open(fs[i+k]) if False else None
    # output frames: for j in 0..n-k-1 : frame j+k? use: loop = frames[k..n-1], with last k frames blended toward frames[0..k-1]
    idx=0
    for j in range(k, n):
        a=Image.open(fs[j]).convert('RGB')
        if j >= n-k:
            t=(j-(n-k))/k; b=Image.open(fs[j-(n-k)]).convert('RGB'); a=Image.blend(a,b,t)
        a.save(f'{out}/f{idx:04d}.png'); idx+=1
PY
for n in capsule helix markbuild; do ffmpeg -y -loglevel error -framerate 24 -i frames/$n/f%04d.png -c:v libx264 -pix_fmt yuv420p -crf 22 -movflags +faststart vid/$n.mp4; done
for n in blob flow tubes; do ffmpeg -y -loglevel error -framerate 24 -i frames/$n-loop/f%04d.png -c:v libx264 -pix_fmt yuv420p -crf 22 -movflags +faststart vid/$n.mp4; done
ls -la vid
