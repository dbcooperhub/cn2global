import os
folder = r'C:\Users\wangs\.qclaw\workspace\cn2global'
for f in sorted(os.listdir(folder)):
    if f.endswith('.html'):
        path = os.path.join(folder, f)
        size = os.path.getsize(path)
        print(f'{f}: {size//1024}KB ({size} bytes)')
