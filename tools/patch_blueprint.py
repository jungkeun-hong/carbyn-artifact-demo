import pathlib
p = pathlib.Path('/home/a0/carbyn-artifact/b2b-product-blueprint.html'); s = p.read_text()
s = s.replace('CONTINUOUS EGOCENTRIC POV STREAM (SVE-DEMO.MP4)', 'REAL 1ST-PERSON POV · PLANT SKID / JOBSITE / 480V PANEL')
s = s.replace('<video src="assets/product-ui/sve-demo.mp4" autoplay muted loop playsinline controls',
              '<video autoplay muted loop playsinline controls')
s = s.replace('background:#000; margin-bottom:14px;"></video>',
              'background:#000; margin-bottom:14px;"><source src="assets/product-ui/pov_mep_panel.webm" type="video/webm"><source src="assets/product-ui/pov_mep_panel.mp4" type="video/mp4"></video>', 1)
# SOP v2 hero: swap static frame for real assembly POV video
s = s.replace('<img id="sop-img" src="assets/product-ui/pov_frame_03.jpg" alt="HUD Preview" style="width:100%; height:100%; object-fit:cover;">',
              '<video id="sop-img" autoplay muted loop playsinline src="assets/product-ui/pov_assembly_bench.mp4" style="width:100%; height:100%; object-fit:cover;"></video>')
for old, new in [('pov_frame_01.jpg",', 'pov_assembly_bench.mp4",'), ('pov_frame_02.jpg",', 'pov_gasket_sealing.mp4",'), ('pov_frame_03.jpg",', 'pov_continuity_test.mp4",'), ('pov_frame_04.jpg",', 'pov_assembly_bench.mp4",')]:
    s = s.replace('img: "assets/product-ui/' + old, 'img: "assets/product-ui/' + new)
s = s.replace("document.getElementById('sop-img').src = d.img;", "{ const v = document.getElementById('sop-img'); if (!v.src.endsWith(d.img)) { v.src = d.img; v.play().catch(()=>{}); } }")
s = s.replace('sve-demo.mp4', 'pov_mfg_skid.mp4')
p.write_text(s)
print('sve left', s.count('sve-demo'), 'pov refs', s.count('pov_'))
