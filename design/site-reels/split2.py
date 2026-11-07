"""Cut a take into its sentences: among the pauses, pick the set that best matches where each
sentence should end (by its share of letters) while preferring long pauses."""
import itertools, re, sys
import numpy as np
sys.path.insert(0, '/home/claude/shwani-media/design')
import reel
SR = reel.SR

def gaps(x, frame=.02, floor_db=-38, min_gap=.18):
    hop = int(frame * SR)
    rms = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    loud = 20 * np.log10(rms / rms.max() + 1e-9) > floor_db
    idx = np.flatnonzero(loud); first, last = idx[0], idx[-1]; out, k = [], first
    while k <= last:
        if not loud[k]:
            j = k
            while j <= last and not loud[j]: j += 1
            if (j - k) * frame >= min_gap: out.append((k * hop, j * hop))
            k = j
        else: k += 1
    return first * hop, (last + 1) * hop, out

def weight(s):
    return len(re.sub(r'[ً-ْ\s،.:؟]', '', s))   # letters only, no marks

def split(x, sents, w_pos=6.0):
    a0, a1, G = gaps(x); n = len(sents); tot = a1 - a0
    cum = np.cumsum([weight(s) for s in sents]); exp = [a0 + tot * c / cum[-1] for c in cum[:-1]]
    best = None; W = np.array([weight(s) for s in sents], float)
    for comb in itertools.combinations(range(len(G)), n - 1):
        edges = [a0] + [v for gi in comb for v in G[gi]] + [a1]
        durs = np.array([(edges[2 * i + 1] - edges[2 * i]) / SR for i in range(n)])
        lr = np.log(W / np.maximum(durs, .3))                      # speaking rate of each sentence
        cost = 4.0 * np.var(lr) - np.mean([(G[gi][1] - G[gi][0]) / SR for gi in comb])
        if best is None or cost < best[0]: best = (cost, comb)
    cuts = [G[i] for i in best[1]]
    bounds, s = [], a0
    for a, b in cuts: bounds.append((s, a)); s = b
    bounds.append((s, a1)); pad = int(.04 * SR)
    return [x[max(0, a - pad):min(len(x), b + pad)] for a, b in bounds], [(round(a / SR, 2), round((b - a) / SR, 2)) for a, b in cuts]
