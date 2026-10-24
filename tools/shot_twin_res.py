"""Shot of twin.html: wait for app ready, optional freeze, report pin screen coords, CDP screenshot.
Usage: shot_twin_res.py <url> <out.png> [w] [h] [settle_ms] [freeze|live]"""
import sys, base64, time
from playwright.sync_api import sync_playwright
url, out = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 else 1280
h = int(sys.argv[4]) if len(sys.argv) > 4 else 720
settle = int(sys.argv[5]) if len(sys.argv) > 5 else 20000
t0 = time.time()
def log(m): print(f'[{time.time()-t0:5.1f}s] {m}', flush=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': w, 'height': h})
    pg.on('pageerror', lambda e: log(f'PAGEERROR: {e}'[:300]))
    pg.goto('http://127.0.0.1:8765/' + url, wait_until='domcontentloaded', timeout=60000)
    log('goto ok')
    pg.wait_for_function('window.__app && document.getElementById("loading").className.includes("done")', timeout=120000, polling=2000)
    log('app ready')
    pg.wait_for_timeout(settle)
    if (sys.argv[6] if len(sys.argv) > 6 else 'freeze') == 'freeze':
        pg.evaluate('window.__app.freeze()')
    log('settled')
    log(pg.evaluate('''(() => { const a = window.__app; const out = []; a.scene.traverse(o => { if (o.userData && o.userData.pin && o.visible) { const v = o.getWorldPosition(new o.position.constructor()).project(a.camera); out.push(o.userData.pin.id + ' ' + Math.round((v.x+1)/2*innerWidth) + ',' + Math.round((1-v.y)/2*innerHeight)); } }); return document.getElementById("status").textContent + ' || ' + out.join(' | '); })()'''))
    cdp = pg.context.new_cdp_session(pg)
    d = cdp.send('Page.captureScreenshot', {'format': 'png'})
    open(out, 'wb').write(base64.b64decode(d['data']))
    log('shot saved')
    b.close()
