cd "$(dirname "$0")"
mkdir -p final
for sc in tees totes bottles mugs bands badge; do
  t0=$(date +%s); python3 merch.py $sc final/merch-$sc.png 1600 1200 160 > log-$sc.txt 2>&1; echo "merch $sc $? $(( $(date +%s)-t0 ))s"
done
for sc in capsule-dark capsule-light mark-dark mark-light flask tubes helix blob tablets pack stationery; do
  t0=$(date +%s); python3 assets.py $sc final/asset-$sc.png 1600 1200 192 > log-$sc.txt 2>&1; echo "asset $sc $? $(( $(date +%s)-t0 ))s"
done
echo ALLDONE
