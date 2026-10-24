"""Usage: shot.py <path> <out.png> [wait_ms] [js_before_shot] [w] [h]"""
import sys
from playwright.sync_api import sync_playwright
path, out = sys.argv[1], sys.argv[2]
wait = int(sys.argv[3]) if len(sys.argv) > 3 else 8000
js = sys.argv[4] if len(sys.argv) > 4 else ''
PRESETS = {'freeze': 'window.__app && window.__app.freeze()', 'none': '',
           'walk': 'window.__app.setMode("walk")',
           'mep': 'window.__app.openPin(window.__app.PINS[4])',
           'con': 'window.__app.openPin(window.__app.PINS[2])'}
js = PRESETS.get(js, js)
w = int(sys.argv[5]) if len(sys.argv) > 5 else 1920
h = int(sys.argv[6]) if len(sys.argv) > 6 else 1080
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required'])
    pg = b.new_page(viewport={'width': w, 'height': h})
    logs = []
    pg.on('console', lambda m: logs.append(f'{m.type}: {m.text}'[:200]))
    pg.on('pageerror', lambda e: logs.append(f'PAGEERROR: {e}'[:300]))
    pg.goto('http://127.0.0.1:8765/' + path, wait_until='domcontentloaded', timeout=60000)
    pg.wait_for_timeout(wait)
    if js:
        try:
            pg.evaluate(js)
        except Exception as e:
            logs.append('EVALERR ' + str(e)[:200])
        pg.wait_for_timeout(3000)
    pg.screenshot(path=out, timeout=120000)
    for l in logs[-15:]:
        print(l)
    b.close()
