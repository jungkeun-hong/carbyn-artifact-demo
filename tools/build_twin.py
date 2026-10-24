"""Build splat-house/twin.html = real Spark 3DGS engine (index.html) + Carbyn spatial work-order / RFI pins + POV video."""
import pathlib, json, sys
sys.exit('DEPRECATED (t_9206624f): this generator mapped industrial WO labels onto residential splats. twin.html is now hand-edited; do not re-run.')
R = pathlib.Path('/home/a0/carbyn-artifact/splat-house')
src = (R / 'index.html').read_text()

def sub(old, new, count=1):
    global src
    assert old in src, old[:80]
    src = src.replace(old, new, count)

# ---------- English UI + honest notice ----------
sub('<html lang="ko">', '<html lang="en">')
sub('<title>Inspection Splat Walk</title>', '<title>Carbyn Spatial Twin · 3DGS Work-Order Walk</title>')
sub('<b>Inspection Splat Walk</b><small id="subtitle">888 Any Street · sample report</small>',
    '<b>Carbyn Spatial Twin</b><small id="subtitle">real 3DGS splats · spatial WO / RFI pins</small>')
sub('<button id="modeOverview" aria-pressed="true">탑뷰 (CCTV)</button>', '<button id="modeOverview" aria-pressed="true">Top-down CCTV</button>')
sub('<button id="modeWalk" aria-pressed="false">1인칭 걷기</button>', '<button id="modeWalk" aria-pressed="false">1st-person walk (WASD)</button>')
sub('<button data-level="all" aria-pressed="true">전체</button>', '<button data-level="all" aria-pressed="true">All</button>')
sub('<button data-level="-1">지하</button>', '<button data-level="-1">B1</button>')
sub('<button data-level="0">1층·외부</button>', '<button data-level="0">L1</button>')
sub('<button data-level="1">2층</button>', '<button data-level="1">L2</button>')
sub('<button data-level="2">다락·지붕</button>', '<button data-level="2">Attic/Roof</button>')
sub('<button class="btn" id="explode" aria-pressed="false">층 분리</button>', '<button class="btn" id="explode" aria-pressed="false">Explode levels</button>')
sub('<button class="btn" id="loadArea" aria-pressed="false">같은 구역 전부 표시</button>', '<button class="btn" id="loadArea" aria-pressed="false" hidden></button>')
sub('<button class="btn" id="tour" aria-pressed="false">▶ 자동 투어</button>', '<button class="btn" id="tour" aria-pressed="false">▶ Auto tour</button>')
sub('<button class="btn" id="enter">이 지점에서 걷기</button>', '<button class="btn" id="enter">Walk from here</button>')
sub("tourOn ? '■ 투어 정지' : '▶ 자동 투어'", "tourOn ? '■ Stop tour' : '▶ Auto tour'")
sub('<span>원본 사진</span>', '<span>source photo</span>')
sub('<span>FLOOR PLAN · 평면 배치</span>', '<span>FLOOR PLAN · PINS</span>')
import re
src = re.sub(r'<div class="notice" style="flex-basis:100%">.*?</div>\n',
    '<div class="notice" style="flex-basis:100%"><b>Real WebGL 3DGS</b> · Spark 2.4 + three.js · SOG splats from a residential walkdown capture. Pins show how plant, jobsite and MEP Cx captures get tagged; pin placement is hand-set, not survey-grade.</div>\n',
    src, count=1, flags=re.S)
sub('<b>Inspection Splat Walk</b><span id="loadMsg">loading scene…</span>', '<b>Carbyn Spatial Twin</b><span id="loadMsg">loading 3DGS scene…</span>')
sub("toast('마커를 클릭하거나 → 키로 촬영 지점을 따라가 보세요 · Enter로 1인칭 전환');",
    "toast('Click a WO / RFI pin · Enter = 1st-person walk · T = top-down CCTV');")
sub("$('subtitle').textContent = `888 Any Street · ${stops.length} stops",
    "$('subtitle').textContent = `${PINS.length} spatial pins · ${stops.length} capture stops")
# status line in English
sub("`AI 확장 3D · 사진 1장 → 생성 영상 ${data.mv[s.mv].frames}프레임 → DA3 → Brush · ${fmt(rec.mesh.numSplats)} gaussians`",
    "`AI-expanded multi-view 3DGS · ${fmt(rec.mesh.numSplats)} gaussians`")
sub("`multi-view 3DGS (DA3 → Brush) · ${fmt(rec.mesh.numSplats)} gaussians · ${stops.filter(o => o.mv === s.mv).length}장 공동 학습`",
    "`multi-view 3DGS (DA3 → Brush) · ${fmt(rec.mesh.numSplats)} gaussians`")
sub("${s.focal35 ? '' : ' (EXIF 없음, 30mm 가정)'}", "")
sub("(rec.missing ? 'splat 미생성 · 원본 사진만 표시' : 'splat 로드 실패')", "(rec.missing ? 'no splat · photo only' : 'splat load failed')")
sub(" + (s.gen ? ' · AI 확장' : s.mv ? ' · multi-view' : '')", " + (s.gen ? ' · AI-expanded' : s.mv ? ' · multi-view' : '')")

# ---------- CSS ----------
sub('@media (max-width:720px){', '''
#wo{top:calc(108px + env(safe-area-inset-top,0px));right:max(16px,env(safe-area-inset-right,0px));width:340px;background:var(--panel);border:1px solid var(--line);border-radius:12px;backdrop-filter:blur(10px);padding:10px}
#wo .ttl{font-family:var(--mono);font-size:11px;color:var(--muted);display:flex;justify-content:space-between;margin-bottom:6px}
#wo .tabs{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;margin-bottom:8px}
#wo .tabs button{appearance:none;border:1px solid var(--line);background:#0003;color:var(--muted);font:600 11px var(--mono);padding:6px 4px;border-radius:7px;cursor:pointer}
#wo .tabs button[aria-pressed="true"]{color:#111;border-color:transparent}
#wo .pin{display:flex;gap:8px;align-items:flex-start;padding:7px 8px;border-radius:8px;border:1px solid transparent;cursor:pointer;margin-bottom:4px;background:#ffffff06}
#wo .pin:hover{border-color:#3a4150}
#wo .pin.on{border-color:var(--pc);background:color-mix(in srgb,var(--pc) 14%,transparent)}
#wo .pin i{flex:none;font-style:normal;font:600 10px var(--mono);color:#111;background:var(--pc);border-radius:5px;padding:2px 5px;margin-top:1px}
#wo .pin b{display:block;font-size:12.5px;font-weight:600;line-height:1.3}
#wo .pin small{display:block;font-family:var(--mono);font-size:10.5px;color:var(--muted)}
#pov{left:max(16px,env(safe-area-inset-left,0px));top:calc(108px + env(safe-area-inset-top,0px));width:400px;background:var(--panel);border:1px solid var(--pc,var(--line));border-radius:12px;backdrop-filter:blur(10px);overflow:hidden}
#pov video{display:block;width:100%;height:200px;object-fit:cover;background:#000}
#pov .hd{display:flex;justify-content:space-between;align-items:center;padding:8px 12px 0;font:600 11px var(--mono);color:var(--pc)}
#pov .hd span:last-child{color:var(--muted)}
#pov h4{margin:4px 12px 6px;font-size:15px;font-weight:600;line-height:1.3}
#pov dl{display:grid;grid-template-columns:auto 1fr;gap:3px 10px;margin:0 12px 8px;font-size:12px}
#pov dt{font-family:var(--mono);font-size:10.5px;color:var(--muted)}
#pov dd{margin:0;color:var(--fg)}
#pov .voice{margin:0 12px 10px;padding:7px 9px;border-left:3px solid var(--pc);background:#0006;border-radius:6px;font-size:12px;color:#d4d4ce;font-style:italic}
#pov .x{position:absolute;right:8px;top:8px;width:24px;height:24px;border-radius:6px;border:0;background:#000a;color:#fff;cursor:pointer}
#card{width:min(360px,calc(100vw - 32px))}
#map{width:min(250px,calc(100vw - 32px))}
body.embed #help{display:none}
body.embed #card,body.embed #map,body.embed .notice,body.embed #levels,body.embed #explode,body.embed #tour,body.embed #helpBtn,body.embed .brand small{display:none}
body.embed #wo{top:56px;width:250px;padding:8px}
body.embed #wo .pin small{display:none}
body.embed #pov{top:56px;width:270px}
body.embed #pov video{height:140px}
body.embed #pov dl{display:none}
body.embed #pov h4{font-size:13px}
@media (max-width:720px){''')

# ---------- HTML panels ----------
sub('<div id="toast" role="status"></div>', '''<div id="wo" class="hud">
  <div class="ttl"><span>SPATIAL WORK ORDERS · RFIs</span><span id="woCount"></span></div>
  <div class="tabs" id="woTabs">
    <button data-v="mfg" aria-pressed="true">MFG</button>
    <button data-v="con" aria-pressed="false">CONSTR.</button>
    <button data-v="mep" aria-pressed="false">MEP CX</button>
  </div>
  <div id="woList"></div>
</div>
<div id="pov" class="hud" hidden>
  <button class="x" id="povX" aria-label="Close">×</button>
  <video id="povVid" muted loop playsinline autoplay></video>
  <div class="hd"><span id="povSys"></span><span id="povId"></span></div>
  <h4 id="povTitle"></h4>
  <dl id="povFields"></dl>
  <div class="voice" id="povVoice"></div>
</div>
<div id="toast" role="status"></div>''')

# ---------- JS: pins ----------
PINS_JS = r'''
// ---------- Carbyn spatial work-order / RFI pins ----------
const VERT = { mfg: { name: 'Manufacturing', col: 0xffcd11, css: '#FFCD11' }, con: { name: 'Big Construction', col: 0x60a5fa, css: '#60A5FA' }, mep: { name: 'MEP Commissioning', col: 0x34d399, css: '#34D399' } };
const POV = (n) => [`../assets/product-ui/pov_${n}.webm`, `../assets/product-ui/pov_${n}.mp4`];
const PINS = [
  { v: 'mfg', stop: 'IMG_8937', off: [0, 0.6, 2.4], id: 'WO-48213', sys: 'IBM Maximo MAS 9', title: 'AHU-B1 supply duct · insulation torn at elbow', video: 'mfg_skid',
    fields: [['Asset', 'AHU-B1-SUP-04'], ['Failure class', 'ISO 14224 · INL (insulation)'], ['Priority', '2 · energy loss'], ['Labor', '1.5 h · HVAC tech'], ['Status', 'WAPPR → APPR']],
    voice: '"Supply duct on AHU-B1, foil wrap torn at the elbow, about eight inches. Schedule re-wrap this week."' },
  { v: 'mfg', stop: 'IMG_8947', off: [0.4, 0.9, 2.2], id: 'LMB-7731', sys: 'Limble CMMS', title: 'EF-03 exhaust fan · PM vibration route', video: 'mfg_skid',
    fields: [['Asset', 'EF-03 · Basement exhaust'], ['PM template', 'Quarterly vibration + belt'], ['Reading', '0.31 in/s RMS (alert 0.30)'], ['Parts', 'Belt A-42 · staged'], ['Status', 'Open · due Fri']],
    voice: '"EF-03 reading point-three-one inches per second, just over alert. Belt looks glazed, stage an A-42."' },
  { v: 'con', stop: 'IMG_6197', off: [0, 0.4, 2.0], id: 'RFI-0142', sys: 'Procore RFI', title: 'BIM vs as-built · TJI joist bay notched at J-14', video: 'construction_walk',
    fields: [['Drawing', 'S-201 · Grid C/14'], ['Deviation', 'Field notch 2 in. vs no-notch detail'], ['Ball in court', 'Structural EOR'], ['Cost impact', 'TBD'], ['Status', 'Draft → Open']],
    voice: '"Joist bay J-fourteen has a field notch on the bottom flange. Not in S-201. Need EOR direction before close-in."' },
  { v: 'con', stop: 'IMG_6111', off: [0.3, 0.3, 2.2], id: 'ISS-2207', sys: 'Autodesk ACC Build', title: 'Attic insulation depth below R-38 spec', video: 'construction_walk',
    fields: [['Issue type', 'Quality · Deviation'], ['Location', 'L3 Attic · Bay A'], ['Measured', '9 in. blown (spec 13 in.)'], ['Assigned', 'Insulation sub'], ['Status', 'Open · pinned to sheet A-501']],
    voice: '"Attic bay A, blown insulation about nine inches. Spec says R-38, so thirteen. Open an issue to the insulation sub."' },
  { v: 'mep', stop: 'IMG_2840', off: [0, 0.2, 1.6], id: 'CX-L2-031', sys: 'ACC Build · Cx checklist', title: 'Panel LP-1 · L2 functional test + torque check', video: 'mep_panel',
    fields: [['Equipment', 'LP-1 · 208/120V 42-ckt'], ['Checklist', 'L2 pre-functional · 18 items'], ['Torque', 'Lugs verified 250 in-lb'], ['Labeling', 'Ckt 14, 22 unlabeled'], ['Status', '16 / 18 pass · 2 open']],
    voice: '"LP-1 lugs torqued to two-fifty inch-pounds. Circuits fourteen and twenty-two have no labels, open those two items."' },
  { v: 'mep', stop: 'IMG_8954', off: [0.2, 0.5, 2.0], id: 'CX-PNC-118', sys: 'Procore Punch', title: 'Conduit stub-up unlabeled at crawl wall', video: 'mep_panel',
    fields: [['System', 'Branch power · 3/4 in. EMT'], ['Location', 'Crawl · north wall'], ['Spec', 'Div 26 05 53 identification'], ['Assignee', 'Electrical sub'], ['Status', 'Punch · open']],
    voice: '"Three-quarter EMT stub-up on the north crawl wall, no identification. Punch it to the electrical sub."' },
];
const pinGroup = new THREE.Group(); scene.add(pinGroup);
const pinObjs = [];
function pinSprite(text, css) {
  const c = document.createElement('canvas'); c.width = 512; c.height = 112; const g = c.getContext('2d');
  g.fillStyle = 'rgba(11,11,13,.86)'; g.beginPath(); g.roundRect(0, 0, 512, 112, 20); g.fill();
  g.fillStyle = css; g.fillRect(0, 0, 12, 112);
  g.fillStyle = css; g.font = '600 40px IBM Plex Mono, monospace'; g.textBaseline = 'middle'; g.fillText(text, 30, 58);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, depthTest: false, transparent: true })); sp.scale.set(1.6, 0.35, 1); sp.renderOrder = 9; return sp;
}
for (const p of PINS) {
  p.s = stops.find(s => s.id === p.stop); const V = VERT[p.v];
  const g = new THREE.Group(); g.userData.pin = p;
  const head = new THREE.Mesh(new THREE.OctahedronGeometry(0.16), new THREE.MeshBasicMaterial({ color: V.col, depthTest: false, transparent: true }));
  head.renderOrder = 8; g.add(head);
  const halo = new THREE.Mesh(new THREE.RingGeometry(0.22, 0.27, 32), new THREE.MeshBasicMaterial({ color: V.col, transparent: true, opacity: .8, depthTest: false, side: THREE.DoubleSide }));
  halo.renderOrder = 8; g.add(halo); g.userData.halo = halo;
  const lab = pinSprite(p.id, V.css); lab.position.y = 0.42; g.add(lab);
  pinGroup.add(g); pinObjs.push(g);
}
function placePins() {
  for (const g of pinObjs) {
    const p = g.userData.pin, s = p.s, lvl = areas[s.area].level;
    const yaw = THREE.MathUtils.degToRad(s.yaw);
    const fwd = new THREE.Vector3(Math.sin(yaw), 0, Math.cos(yaw)), right = new THREE.Vector3(Math.cos(yaw), 0, -Math.sin(yaw));
    g.position.set(s.pos[0], levelOffset(lvl) + s.pos[1] + p.off[1] - 0.6, s.pos[2]).addScaledVector(fwd, p.off[2]).addScaledVector(right, p.off[0]);
  }
}
let curVert = 'mfg', curPin = null;
function renderWo() {
  const list = PINS.filter(p => p.v === curVert); const V = VERT[curVert];
  $('woList').innerHTML = list.map(p => `<div class="pin ${curPin === p ? 'on' : ''}" style="--pc:${V.css}" data-id="${p.id}"><i>${p.id}</i><div><b>${p.title}</b><small>${p.sys} · ${areas[p.s.area].name}</small></div></div>`).join('');
  [...$('woTabs').children].forEach(b => { const on = b.dataset.v === curVert; b.setAttribute('aria-pressed', on); b.style.background = on ? VERT[b.dataset.v].css : ''; });
  $('woCount').textContent = `${PINS.length} pins · 3 verticals`;
  for (const g of pinObjs) g.visible = g.userData.pin.v === curVert;
}
function openPin(p, opts = {}) {
  curPin = p; curVert = p.v; const V = VERT[p.v];
  const pov = $('pov'); pov.hidden = false; pov.style.setProperty('--pc', V.css);
  const vid = $('povVid'); const want = p.video;
  if (vid.dataset.v !== want) { vid.dataset.v = want; vid.innerHTML = POV(want).map((u, i) => `<source src="${u}" type="video/${i ? 'mp4' : 'webm'}">`).join(''); vid.load(); vid.play().catch(() => {}); }
  $('povSys').textContent = `${V.name.toUpperCase()} · ${p.sys}`; $('povId').textContent = p.id;
  $('povTitle').textContent = p.title;
  $('povFields').innerHTML = p.fields.map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join('');
  $('povVoice').textContent = p.voice;
  renderWo();
  if (!opts.noNav) select(p.s.index);
}
$('woTabs').addEventListener('click', (e) => { const b = e.target.closest('button'); if (!b) return; curVert = b.dataset.v; const first = PINS.find(p => p.v === curVert); openPin(first); });
$('woList').addEventListener('click', (e) => { const r = e.target.closest('.pin'); if (r) openPin(PINS.find(p => p.id === r.dataset.id)); });
$('povX').onclick = () => { $('pov').hidden = true; };
renderer.domElement.addEventListener('click', (e) => {
  const r = renderer.domElement.getBoundingClientRect(); const v = new THREE.Vector2(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
  const rc = new THREE.Raycaster(); rc.setFromCamera(v, camera); rc.params.Sprite = { threshold: .3 };
  const hits = rc.intersectObjects(pinObjs.filter(g => g.visible), true);
  if (hits.length) { let o = hits[0].object; while (o && !o.userData.pin) o = o.parent; if (o) openPin(o.userData.pin); }
});
const _pm = placeMarkers; placeMarkers = function () { _pm(); placePins(); };
renderer.setAnimationLoop(null);
renderer.setAnimationLoop(() => {
  if (tween) tween.step();
  else if (mode === 'overview') orbit.update();
  else { walk.update(camera); if (tourOn) { tourPhase += 0.0035; camera.rotateY(Math.sin(tourPhase) * 0.0012); } }
  const t = performance.now() / 1000;
  for (const g of pinObjs) { g.children[0].rotation.y = t * 1.5; const h = g.userData.halo; h.lookAt(camera.position); const k = (curPin === g.userData.pin) ? 1.25 + 0.2 * Math.sin(t * 5) : 1; h.scale.setScalar(k); }
  renderer.render(scene, camera);
});
// map overlay: pins on the floor plan
const _rm = renderMap; renderMap = function () { _rm(); let h = '';
  for (const p of PINS) { if (p.v !== curVert) continue; const s = p.s; h += `<rect x="${s.pos[0] - .8}" y="${s.pos[2] - .8}" width="1.6" height="1.6" transform="rotate(45 ${s.pos[0]} ${s.pos[2]})" fill="${VERT[p.v].css}" stroke="#111" stroke-width=".25"><title>${p.id} ${p.title}</title></rect>`; }
  svg.insertAdjacentHTML('beforeend', h); };
'''
# placeMarkers / renderMap are function declarations, reassignable in module scope
sub("// ---------- boot ----------", PINS_JS + "\n// ---------- boot ----------")
sub("await select(0);", "if (new URLSearchParams(location.search).has('embed')) document.body.classList.add('embed');\nplacePins(); renderWo();\nawait select(PINS[0].s.index);\nopenPin(PINS[0], { noNav: true });")
sub("setTimeout(cctv, 300);", "setMode('walk');")
sub("const lab = makeLabel(a.name, a.ko, 1);", "const lab = makeLabel(a.name, 'L' + (a.level + 1 > 0 ? a.level + 1 : 'B1'), 1);")
sub("$('areaKo').textContent = a.ko;", "$('areaKo').textContent = '';")
sub("window.__app = { scene, camera, stops, loaded, select, setMode };", "window.__app = { scene, camera, stops, loaded, select, setMode, openPin, PINS, renderer, freeze: () => { renderer.setAnimationLoop(null); renderer.render(scene, camera); } };")
(R / 'twin.html').write_text(src)
print('ok', len(src))
