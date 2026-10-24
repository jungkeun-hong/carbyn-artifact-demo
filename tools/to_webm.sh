#!/bin/bash
cd /home/a0/carbyn-artifact/assets/product-ui
for v in mfg_skid mep_panel assembly_bench construction_walk gasket_sealing continuity_test; do
  ffmpeg -v error -y -i pov_$v.mp4 -an -c:v libvpx-vp9 -b:v 900k -deadline realtime -cpu-used 8 -vf "scale='min(720,iw)':-2" pov_$v.webm
  echo done $v
done
