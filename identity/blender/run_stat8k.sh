#!/bin/bash
# 8K stationery mockups (7680 x 5760), each rendered in 4 strips (strips.py) so an interrupted run resumes where it stopped.
# Before: in ../render, serve the folder on :8123, render the report-cover capsule and flow images at print size
#   (node drive.js with {"s":"capsule","v":"dark","w":4800,"h":3600} and {"s":"flow","w":6000,"h":4500}, saved as final8/*.jpg),
#   then node stat8k.js && python3 pdfprep.py stat8k. Re-run this script until it prints STAT8KDONE.
cd "$(dirname "$0")"; mkdir -p hd8
s(){ local sc=$1 out=$2 n=4; [ -f "$out" ] && return
  for i in $(seq 0 $((n-1))); do python3 strips.py assets.py $sc $out 7680 5760 32 $n $i || exit 1; done
  python3 strips.py assets.py $sc $out 7680 5760 32 $n stitch; }
for n in cards letter finance report post id folder; do s stat-$n hd8/stat-$n.png; done
echo STAT8KDONE
