import pathlib, re
A = pathlib.Path('/home/a0/carbyn-artifact')
p = A / 'robotics-world-model.html'; s = p.read_text()
s = s.replace('<video src="assets/product-ui/sve-demo.mp4" autoplay muted loop playsinline style="width:100%;height:195px;',
              '<video id="rob-vid" crossorigin="anonymous" autoplay muted loop playsinline style="width:100%;height:195px;')
s = s.replace('Plate Filter Valve Isolation Sequence', 'Gasket Bead Seal &amp; Cover Seat')
s = s.replace('TASK 03 · HVAC / ROTATING MRO', 'TASK 03 · ASSEMBLY SEALING')
s = s.replace('M8 Flange Torque &amp; Gasket Seating', 'Bench Assembly · Driver Fastening')
JS = r'''
  // ---- REAL hand tracking: MediaPipe HandLandmarker (21 keypoints, MANO-compatible topology) on the live POV <video> ----
  const VIDS = ['assembly_bench', 'mep_panel', 'gasket_sealing'];
  const rVid = document.getElementById('rob-vid');
  function loadVid(i) { rVid.innerHTML = `<source src="assets/product-ui/pov_${VIDS[i]}.webm" type="video/webm"><source src="assets/product-ui/pov_${VIDS[i]}.mp4" type="video/mp4">`; rVid.load(); rVid.play().catch(()=>{}); traj.length = 0; }
  let landmarker = null, lmStatus = 'loading MediaPipe HandLandmarker…', lastRes = null, lastTs = -1, traj = [], stepN = 0;
  (async () => {
    try {
      const vision = await import('https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/vision_bundle.mjs');
      const fs = await vision.FilesetResolver.forVisionTasks('https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/wasm');
      const opts = (d) => ({ baseOptions: { modelAssetPath: 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task', delegate: d }, runningMode: 'VIDEO', numHands: 2, minHandDetectionConfidence: 0.35, minTrackingConfidence: 0.35 });
      try { landmarker = await vision.HandLandmarker.createFromOptions(fs, opts('GPU')); } catch (e) { landmarker = await vision.HandLandmarker.createFromOptions(fs, opts('CPU')); }
      lmStatus = 'HandLandmarker live';
    } catch (e) { lmStatus = 'tracker failed to load: ' + e.message; }
  })();
  const BONES = [[0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[5,9],[9,10],[10,11],[11,12],[9,13],[13,14],[14,15],[15,16],[13,17],[17,18],[18,19],[19,20],[0,17]];
  function coverRect(vw, vh, cw, ch) { const k = Math.max(cw / vw, ch / vh); const w = vw * k, h = vh * k; return { x: (cw - w) / 2, y: (ch - h) / 2, w, h }; }
  function drawRobLoop() {
    const W = rCvs.width, H = rCvs.height;
    rCtx.fillStyle = '#07080B'; rCtx.fillRect(0, 0, W, H);
    const ready = rVid.readyState >= 2 && rVid.videoWidth;
    let R = { x: 0, y: 0, w: W, h: H };
    if (ready) {
      R = coverRect(rVid.videoWidth, rVid.videoHeight, W, H);
      rCtx.drawImage(rVid, R.x, R.y, R.w, R.h);
      if (landmarker && rVid.currentTime !== lastTs) {
        lastTs = rVid.currentTime;
        try { lastRes = landmarker.detectForVideo(rVid, performance.now()); } catch (e) { lmStatus = 'detect error: ' + e.message; }
      }
    }
    const hands = (lastRes && lastRes.landmarks) || [];
    const P = (l) => ({ x: R.x + l.x * R.w, y: R.y + l.y * R.h, z: l.z });
    hands.forEach((lm, hi) => {
      const pts = lm.map(P);
      // contact affordance: thumb-index pinch midpoint, radius by aperture
      const a = pts[4], b = pts[8]; const cx = (a.x + b.x) / 2, cy = (a.y + b.y) / 2; const ap = Math.hypot(a.x - b.x, a.y - b.y);
      const rad = Math.max(30, Math.min(110, ap * 1.1));
      const g = rCtx.createRadialGradient(cx, cy, 4, cx, cy, rad); g.addColorStop(0, 'rgba(239,68,68,0.55)'); g.addColorStop(0.6, 'rgba(255,205,17,0.25)'); g.addColorStop(1, 'rgba(255,205,17,0)');
      rCtx.fillStyle = g; rCtx.beginPath(); rCtx.arc(cx, cy, rad, 0, Math.PI * 2); rCtx.fill();
      rCtx.strokeStyle = hi ? '#60A5FA' : '#34D399'; rCtx.lineWidth = 3;
      BONES.forEach(([i, j]) => { rCtx.beginPath(); rCtx.moveTo(pts[i].x, pts[i].y); rCtx.lineTo(pts[j].x, pts[j].y); rCtx.stroke(); });
      pts.forEach((q, k) => { rCtx.fillStyle = [4, 8, 12, 16, 20].includes(k) ? '#FFCD11' : '#FFFFFF'; rCtx.beginPath(); rCtx.arc(q.x, q.y, k ? 4 : 6, 0, Math.PI * 2); rCtx.fill(); });
      // 6-DoF wrist frame from wrist (0), index MCP (5), pinky MCP (17)
      const w = lm[0], i5 = lm[5], p17 = lm[17];
      const ux = [i5.x - w.x, i5.y - w.y, i5.z - w.z], vx = [p17.x - w.x, p17.y - w.y, p17.z - w.z];
      const n = [ux[1]*vx[2]-ux[2]*vx[1], ux[2]*vx[0]-ux[0]*vx[2], ux[0]*vx[1]-ux[1]*vx[0]];
      const yaw = Math.atan2(ux[1], ux[0]), pitch = Math.atan2(n[2], Math.hypot(n[0], n[1])), roll = Math.atan2(vx[1], vx[0]) - yaw;
      const W0 = pts[0];
      rCtx.lineWidth = 3;
      [[Math.cos(yaw), Math.sin(yaw), '#EF4444'], [Math.cos(yaw + Math.PI / 2), Math.sin(yaw + Math.PI / 2), '#34D399']].forEach(([dx, dy, c]) => { rCtx.strokeStyle = c; rCtx.beginPath(); rCtx.moveTo(W0.x, W0.y); rCtx.lineTo(W0.x + dx * 50, W0.y + dy * 50); rCtx.stroke(); });
      if (hi === 0) {
        const prev = traj[traj.length - 1];
        const st = { t: +rVid.currentTime.toFixed(2), wrist: [+w.x.toFixed(3), +w.y.toFixed(3), +w.z.toFixed(3)], rpy: [+roll.toFixed(2), +pitch.toFixed(2), +yaw.toFixed(2)], aperture: +(ap / W).toFixed(3) };
        if (!prev || st.t !== prev.t) { st.a = prev ? [+(st.wrist[0]-prev.wrist[0]).toFixed(3), +(st.wrist[1]-prev.wrist[1]).toFixed(3), +(st.wrist[2]-prev.wrist[2]).toFixed(3)] : [0,0,0]; traj.push(st); if (traj.length > 90) traj.shift(); stepN++; }
      }
      rCtx.fillStyle = 'rgba(11,11,12,0.88)'; rCtx.fillRect(W0.x - 10, W0.y + 12, 250, 22);
      rCtx.fillStyle = '#FFCD11'; rCtx.font = 'bold 12px Inter, sans-serif';
      rCtx.fillText(`${(lastRes.handedness[hi]||[{}])[0].categoryName || 'Hand'} · 21 kp · 6-DoF wrist`, W0.x - 4, W0.y + 27);
    });
    // wrist trajectory trail
    if (traj.length > 1) { rCtx.strokeStyle = 'rgba(255,205,17,0.8)'; rCtx.lineWidth = 2; rCtx.beginPath(); traj.forEach((q, k) => { const x = R.x + q.wrist[0] * R.w, y = R.y + q.wrist[1] * R.h; k ? rCtx.lineTo(x, y) : rCtx.moveTo(x, y); }); rCtx.stroke(); }
    // HUD
    rCtx.fillStyle = 'rgba(11,11,12,0.85)'; rCtx.fillRect(10, 10, 430, 26);
    rCtx.fillStyle = hands.length ? '#34D399' : '#FFCD11'; rCtx.font = 'bold 13px monospace';
    rCtx.fillText(`${lmStatus} · hands=${hands.length} · t=${ready ? rVid.currentTime.toFixed(2) : '-'}s · steps=${stepN}`, 18, 28);
    const el = document.getElementById('rob-stream');
    if (el && traj.length) { const q = traj[traj.length - 1]; el.textContent = JSON.stringify({ step: stepN, s_t: { wrist_xyz: q.wrist, wrist_rpy: q.rpy, pinch_aperture: q.aperture }, a_t: { d_wrist: q.a }, z_t1: 'V-JEPA 2 encoder slot (offline)' }, null, 1); }
    requestAnimationFrame(drawRobLoop);
  }
'''
s = re.sub(r"  function drawRobLoop\(\) \{.*?requestAnimationFrame\(drawRobLoop\);\n  \}\n", lambda m: JS, s, count=1, flags=re.S)
s = s.replace("  function setRobTask(idx) {\n    curRT = idx;", "  function setRobTask(idx) {\n    curRT = idx; loadVid(idx);")
s = s.replace("  renderRobPanel();\n  drawRobLoop();", "  renderRobPanel();\n  loadVid(0);\n  drawRobLoop();")
s = s.replace('<pre style="white-space:pre-wrap;font-family:monospace;font-size:12.5px;background:rgba(0,0,0,0.6);padding:14px;border-radius:12px;border:1px solid rgba(255,205,17,0.35);color:#34D399;line-height:1.4;margin-bottom:14px;">${t.vla}</pre>',
              '<div class="kicker" style="margin:0 0 4px;">LIVE (s_t, a_t, z_{t+1}) STREAM FROM TRACKER</div><pre id="rob-stream" style="white-space:pre-wrap;font-family:monospace;font-size:12px;background:rgba(0,0,0,0.6);padding:12px;border-radius:12px;border:1px solid rgba(52,211,153,0.45);color:#34D399;line-height:1.35;margin-bottom:10px;max-height:230px;overflow:hidden;">waiting for hands…</pre>')
s = s.replace('sve-demo.mp4', 'pov_assembly_bench.mp4')
p.write_text(s)
print('rob sve left:', s.count('sve-demo'), 'mediapipe:', s.count('HandLandmarker'))
