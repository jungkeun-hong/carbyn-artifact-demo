"""Upgrade SKT content engine POSTS: real cell landing links, real forms, real POV, de-templated bodies."""
import re, json, sys
F = '/home/a0/carbyn-artifact/skt-content-engine.html'
BASE = 'https://jungkeun-hong.github.io/carbyn-artifact-demo/'
s = open(F).read()
m = re.search(r'const POSTS = (\[.*?\]);\n', s, re.S)
P = json.loads(m.group(1))

# segment -> (cell page, form jpg, POV video, keyword, pain line, sequence)
SEG = {
 'adj':  ('l/adj-tx.html', 'assets/forms/IN01_mha_narrative_p1.jpg', 'pov_construction_walk.mp4', 'ROOF',
          'the 10 PM Xactimate re-entry shift after 6 roofs',
          'elevation + slope, hits per test square, collateral (gutters, screens, soft metals), interior stain + moisture, one cause-of-loss line'),
 'ins':  ('l/ins-dallas.html', 'assets/forms/IN03_citizens_4pt_p1.jpg', 'pov_mep_panel.mp4', '4POINT',
          '2-3 hours writing each report after the inspection',
          'panel brand + amperage + defects, plumbing material + leaks, roof age + covering, HVAC age + condition'),
 'mob':  ('l/mob-tx.html', 'assets/forms/VH01_rvis_sample_p1.jpg', 'pov_assembly_bench.mp4', '3C',
          'washing hands 15 times a day just to type a repair order',
          'concern in the customer words, cause with the part + reading, correction with parts + labor'),
 'roof': ('l/roof-tx.html', 'assets/forms/IN03_citizens_4pt_p2.jpg', 'pov_construction_walk.mp4', 'HAIL',
          'sorting 80 unlabeled roof photos at the kitchen table',
          'facet, covering, layers, hail/wind marks per square, flashing + penetrations'),
 'sew':  ('l/sew-tx.html', 'assets/forms/TR02_ventura_septic_p1.jpg', 'pov_mep_panel.mp4', 'SCOPE',
          'retyping camera footage into a county septic/sewer report',
          'access point, footage, pipe material, defect + distance, recommendation'),
 'rv':   ('l/rv-tx.html', 'assets/forms/VH01_rvis_sample_p2.jpg', 'pov_mfg_skid.mp4', 'RVIS',
          'a 40-page RV inspection report written after dark',
          'system, component, condition code, photo ref, action'),
 'gc':   ('l/index.html', 'assets/forms/CF04_dailyrpt_p1.jpg', 'pov_construction_walk.mp4', 'DAILY',
          'the daily log that gets skipped at 5 PM',
          'crew count by trade, work done by area, deliveries, delays + cause, safety notes'),
 'remo': ('l/index.html', 'assets/forms/CF03_co_nahb_p1.jpg', 'pov_construction_walk.mp4', 'CYA',
          'change orders agreed by text and never paid',
          'scope change, reason, price impact, schedule impact, client OK'),
 'trade':('l/index.html', 'assets/forms/TR01_smartsheet_punch_p1.jpg', 'pov_mep_panel.mp4', 'TICKET',
          'service tickets typed in the truck after the last call',
          'equipment + model, readings, what failed, what you replaced, what you recommend'),
}

def seg_of(p):
    t = (p['ch'] + ' ' + p['title']).lower()
    rules = [('rv', ['rv ', 'nrvia', 'marine']), ('sew', ['septic', 'sewer', 'pumper', 'chimney']),
             ('mob', ['mechanic', 'auto repair', 'repair order', 'dvi', 'tekmetric', '3-c']),
             ('adj', ['adjuster', 'claims', 'xactimate', 'orm/mha', 'cat network']),
             ('ins', ['inspection', 'inspector', '4-point', 'crawlspace', 'spectora']),
             ('roof', ['roof', 'storm restoration']), ('remo', ['change order', 'anti-buildertrend', 'handyman', 'remodel', 'invoice', 'receipt', 'builders']),
             ('gc', ['construction', 'contractor', 'basement', 'daily log']),
             ('trade', ['hvac', 'electric'])]
    for k, kws in rules:
        if any(w in t for w in kws): return k
    return 'trade'

def utm(path, p):
    ch = re.sub(r'[^a-z]+', '-', p['ch'].lower().split('(')[0]).strip('-') or 'social'
    return f"{BASE}{path}?utm_source={ch}&utm_medium=organic&utm_campaign=skt_{p['id'].lower()}"

def body(p, k):
    cell, form, pov, kw, pain, seq = SEG[k]
    ch, arch, title = p['ch'], p['arch'], p['title']
    if ch.startswith('Reddit') or ch.startswith('Forum'):
        if 'Founder' in arch:
            return (f"{title}\n\nBuilding this in public, so being upfront: I'm one of the founders. We kept hearing about {pain}. "
                    f"So we tested one thing: talk through the job once, in this order: {seq}. The app fills the same form you already file. "
                    f"No invented findings, it only writes what you said. Free while we're in beta. Not posting a link per sub rules; it's in my profile. "
                    f"What field would you never trust a tool to fill for you?")
        return (f"{title}\n\nWhat works for us: before you leave the site, say it out loud in one pass: {seq}. "
                f"Then the write-up is copying, not remembering. It kills {pain}. "
                f"If you want, reply with a messy note from today and I'll show what the 5-field version looks like. No link here, mods.")
    if ch.startswith('X'):
        return (f"1/ {title}\n2/ Real problem: {pain}.\n3/ Fix: one spoken pass, {seq}.\n"
                f"4/ Output lands on the form the trade already uses (see image). Filmed POV, not a mockup.\n5/ Try it: {utm(cell, p)}")
    if ch.startswith('Facebook'):
        return (f"Admins OK'd this one. {title}\n\nIf {pain} sounds familiar: comment '{kw}' and send 3 photos + a 15-sec voice note. "
                f"We send back the filled form (like the one pictured) free, within the hour. Order we use: {seq}.")
    return (f"{title}\n[POV clip: {pov}] 0-3s: '{pain.capitalize()}? Watch.' 3-18s: walk the job and talk: {seq}. "
            f"18-30s: show the filled form on the phone. CTA: comment '{kw}' or bio link.")

seen = set()
for i, p in enumerate(P):
    if p['id'] == 'DM_CLOSE_SCRIPT':
        p['seg'] = 'all'; p['cell'] = BASE + 'l/index.html'; p['form'] = 'assets/forms/CF04_dailyrpt_p1.jpg'; p['pov'] = 'pov_mfg_skid.mp4'
        p['cta'] = ("STEP 1 within 15 min of comment: 'Hey [Name], ran your note through Carbyn, here is your filled form [attach]. "
                    "Your trade page: " + BASE + "l/index.html'. STEP 2: 10-min call, ask the magic wand question. "
                    "STEP 3 close: 'Any other questions before I send your link and set up your account?'")
        continue
    k = seg_of(p)
    cell, form, pov, kw, pain, seq = SEG[k]
    p['seg'] = k; p['cell'] = utm(cell, p); p['form'] = form; p['pov'] = pov
    if i >= 10:  # P11+ were template-filled; rewrite
        p['body'] = body(p, k)
    p['cta'] = (f"Public: comment '{kw}'. DM within 15 min: 'Hey [Name], here is your note as a filled form [attach {form.split('/')[-1]}]. "
                f"Run your next 3 free: {p['cell']}'. Close: 'Any other questions before I send your link and set up your account?'")
    assert p['body'] not in seen, p['id']; seen.add(p['body'])

new = 'const POSTS = ' + json.dumps(P, ensure_ascii=False) + ';\n'
s = s[:m.start()] + new + s[m.end():]
json.dump(P, open('/tmp/skt_posts_v3.json', 'w'), ensure_ascii=False, indent=1)
open(F, 'w').write(s)
from collections import Counter
print(len(P), Counter(p['seg'] for p in P))
