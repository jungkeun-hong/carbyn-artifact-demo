import subprocess
ids = ['IMG_2840', 'IMG_8937', 'IMG_8940', 'IMG_8945', 'IMG_8640', 'IMG_6197', 'IMG_6111', 'IMG_8930', 'IMG_8682', 'IMG_8956', 'IMG_8954', 'IMG_8947']
P = '/home/a0/carbyn-artifact/splat-house/photos/'
args = ['ffmpeg', '-v', 'error', '-y']
for i in ids:
    args += ['-i', P + i + '.jpg']
f = ''.join(f'[{k}]scale=240:320,drawtext=text={ids[k]}:fontcolor=yellow:fontsize=20:x=5:y=5[a{k}];' for k in range(len(ids)))
f += ''.join(f'[a{k}]' for k in range(len(ids))) + f'xstack=inputs={len(ids)}:layout=' + '|'.join(f'{(k%6)*240}_{(k//6)*320}' for k in range(len(ids)))
args += ['-filter_complex', f, '/tmp/f/photos.jpg']
r = subprocess.run(args, capture_output=True, text=True)
print(r.stderr[-500:])
