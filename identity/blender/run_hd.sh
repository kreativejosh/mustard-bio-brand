cd "$(dirname "$0")"; mkdir -p hd
r(){ t0=$(date +%s); "$@" > /dev/null 2>&1; echo "$? $(( $(date +%s)-t0 ))s $*" ; }
for n in cards letter finance report post id folder; do r python3 assets.py stat-$n hd/stat-$n.png 2400 1800 96; done
r python3 lanyard3d.py hd/merch-lanyard.png 2400 1800 128
r python3 merch.py bands hd/merch-bands.png 2400 1800 128
for cw in stone ink; do for v in front back; do r python3 tee3d.py $v $cw hd/tee-$cw-$v.png 2200 2200 112; done; done
r python3 tote3d.py natural hd/tote-natural.png 1920 2400 128
r python3 tote3d.py ink hd/tote-ink.png 1920 2400 128
r python3 assets.py pack hd/asset-pack.png 2400 1800 128
r python3 facility.py billboard hd/billboard.png 2400 1800 128
r python3 merch.py bottles hd/merch-bottles.png 2400 1800 128
r python3 merch.py mugs hd/merch-mugs.png 2400 1800 128
r python3 facility.py facade hd/facility-facade.png 2400 1800 128
r python3 facility.py corridor hd/facility-corridor.png 2400 1800 128
echo HDTEXTDONE
for n in capsule-dark capsule-light mark-dark mark-light flask tubes helix blob tablets; do r python3 assets.py $n hd/asset-$n.png 2400 1800 128; done
echo HDALLDONE
