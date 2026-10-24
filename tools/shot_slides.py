"""Screenshot specific slides (by .slide-viewport index) of a deck page. Usage: shot_slides.py <path> <outprefix> <idx,idx,...>"""
import sys
from playwright.sync_api import sync_playwright
path, pre, idxs = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(',')]
with sync_playwright() as p:
    b = p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    pg.goto('http://127.0.0.1:8765/' + path, wait_until='load', timeout=60000)
    pg.wait_for_timeout(4000)
    vps = pg.query_selector_all('.slide-viewport')
    print('slides', len(vps))
    for i in idxs:
        vps[i].scroll_into_view_if_needed(); pg.wait_for_timeout(2500)
        vps[i].screenshot(path=f'{pre}_{i}.png', timeout=60000)
        print('saved', f'{pre}_{i}.png')
    b.close()
