import sys, glob, numpy as np
from PIL import Image
hits = {}
for f in sorted(glob.glob(sys.argv[1] + '/*.jpg'))[::int(sys.argv[2]) if len(sys.argv) > 2 else 5]:
    a = np.asarray(Image.open(f).convert('L')).astype(float)[:, 60:-60]
    m = a.mean(axis=1)
    # a thin row (1-2 px) that differs from the rows 3 px above and below, which agree with each other
    for w in (1, 2):
        up, dn = m[:-2 * w - 4][2:], m[2 * w + 4:][:-2]
        mid = m[w + 2:-w - 2][2:-2] if False else None
    r = np.arange(4, len(m) - 5)
    c = m[r]; u = m[r - 3]; d = m[r + 3]
    score = np.minimum(np.abs(c - u), np.abs(c - d)) - np.abs(u - d)
    # require the row to be uniform across the width (a straight line, not texture)
    std = a[r].std(axis=1)
    k = np.flatnonzero((score > 12) & (std < 25))
    if len(k): hits[f.split('/')[-1]] = [(int(r[i]), round(float(score[i]), 1)) for i in k[:4]]
for f, v in list(hits.items())[:40]: print(f, v)
print('frames with lines:', len(hits))
