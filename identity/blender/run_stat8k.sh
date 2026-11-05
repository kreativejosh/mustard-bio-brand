#!/bin/bash
# 8K stationery mockups (7680 x 5760). Needs ../render/stat8k/ from stat8k.js (serve ../render on :8123).
# Order: scenes without imagery first, then the capsule photo for the report cover, re-export, report scene.
cd "$(dirname "$0")"; mkdir -p hd8
r(){ t0=$(date +%s); "$@" > /dev/null 2>&1; echo "$? $(( $(date +%s)-t0 ))s $*" ; }
for n in finance letter cards post id folder; do r python3 assets.py stat-$n hd8/stat-$n.png 7680 5760 32; done
r python3 assets.py capsule-dark hd8/capsule-dark.png 4800 3600 64
cp hd8/capsule-dark.png ../render/final8/capsule-dark.png
(cd ../render && r node stat8k.js && r python3 pdfprep.py stat8k)
r python3 assets.py stat-report hd8/stat-report.png 7680 5760 32
echo STAT8KDONE
