import json, collections, subprocess, os
d = json.load(open('/home/a0/carbyn-artifact/splat-house/stops.json'))
for k, a in d['areas'].items():
    print(k, a['name'], a['level'], a['rect'])
c = collections.defaultdict(list)
for i, s in enumerate(d['stops']):
    c[s['area']].append((i, s['id'], s.get('mv'), bool(s.get('splat'))))
for k, v in c.items():
    print(k, v[:5])
print(json.dumps(d['mv']['gen_garage'])[:500])
os.makedirs('/tmp/f', exist_ok=True)
P = '/home/a0/carbyn-artifact/assets/product-ui/'
for v in ['mfg_skid', 'mep_panel', 'assembly_bench', 'construction_walk', 'gasket_sealing', 'continuity_test']:
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '2', '-i', P + f'pov_{v}.mp4', '-frames:v', '1', '-vf', 'scale=-2:360', f'/tmp/f/{v}.jpg'])
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + sum([['-i', f'/tmp/f/{v}.jpg'] for v in ['mfg_skid', 'mep_panel', 'construction_walk', 'assembly_bench', 'gasket_sealing', 'continuity_test']], []) + ['-filter_complex', '[0][1][2][3][4][5]hstack=6', '/tmp/f/all.jpg'])
print(os.listdir('/tmp/f'))
