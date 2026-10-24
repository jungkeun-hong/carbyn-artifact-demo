import pathlib, re
A = pathlib.Path('/home/a0/carbyn-artifact')
# ---- 3DGS page: real Spark engine iframe replaces fake 2D canvas ----
p = A / '3dgs-digital-twin.html'; s = p.read_text()
s = s.replace('<video src="assets/product-ui/sve-demo.mp4" autoplay muted loop playsinline style="width:100%;height:185px;',
              '<video id="v3-pov" autoplay muted loop playsinline style="width:100%;height:185px;')
s = s.replace('<video id="v3-pov" autoplay muted loop playsinline style="width:100%;height:185px;object-fit:cover;border-radius:12px;border:1px solid rgba(255,205,17,0.45);background:#000;"></video>',
              '<video id="v3-pov" autoplay muted loop playsinline style="width:100%;height:185px;object-fit:cover;border-radius:12px;border:1px solid rgba(255,205,17,0.45);background:#000;"><source src="assets/product-ui/pov_mfg_skid.webm" type="video/webm"><source src="assets/product-ui/pov_mfg_skid.mp4" type="video/mp4"></video>')
s = s.replace('<canvas id="splat-canvas" width="820" height="590" style="width:100%;height:590px;border-radius:14px;background:#07080B;border:1px solid rgba(255,255,255,0.16);cursor:grab;"></canvas>',
              '<iframe id="splat-frame" src="splat-house/twin.html?embed" allow="autoplay; fullscreen" style="width:100%;height:590px;border-radius:14px;background:#07080B;border:1px solid rgba(255,255,255,0.16);"></iframe>')
s = s.replace('LIVE 3D GAUSSIAN SPLATTING SCENE · DRAG TO ORBIT · CLICK PINS', 'REAL WEBGL 3DGS (SPARK + THREE.JS) · WASD WALK · CLICK WO / RFI PINS')
# remove fake 2D splat drawing loop
s = re.sub(r"  const cvs = document.getElementById\('splat-canvas'\);.*?(?=  function set3dVert)", '', s, count=1, flags=re.S)
s = re.sub(r"  function drawSplatLoop\(\) \{.*?requestAnimationFrame\(drawSplatLoop\);\n  \}\n", '', s, count=1, flags=re.S)
s = s.replace('  drawSplatLoop();\n', '')
# vertical switch drives both iframe pins and POV video
s = s.replace('  function set3dVert(idx) {', '''  const VPOV = ['mfg_skid', 'construction_walk', 'mep_panel'];
  const VPIN = [0, 2, 4];
  function syncTwin(idx) {
    const v = document.getElementById('v3-pov');
    v.innerHTML = `<source src="assets/product-ui/pov_${VPOV[idx]}.webm" type="video/webm"><source src="assets/product-ui/pov_${VPOV[idx]}.mp4" type="video/mp4">`; v.load(); v.play().catch(()=>{});
    try { const app = document.getElementById('splat-frame').contentWindow.__app; if (app) app.openPin(app.PINS[VPIN[idx]]); } catch (e) {}
  }
  function set3dVert(idx) {
    syncTwin(idx);''', 1)
s = s.replace('sve-demo.mp4', 'pov_mfg_skid.mp4')
p.write_text(s)
print('3dgs sve left:', s.count('sve-demo'), 'drawSplat left:', s.count('drawSplatLoop'), 'cvs refs:', s.count('cvs'))
