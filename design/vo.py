"""Place a recorded voice-over take on a reel, sentence by sentence.

    python3 vo.py NN take.wav [--intro 2.0]

posts/NN/build.py defines VO_PLAN = [(design_time, sentence, hold_at or None), ...] and DUR_DESIGN.
The take is one recording of all the sentences in that order, with a clear pause between them
(in Google AI Studio: <long pause> between sentences). This script

1. cuts the take at its longest pauses into exactly len(VO_PLAN) sentences, trims each one;
   and shortens the pauses inside each sentence (the opening one most);
2. puts each sentence at the moment its line appears on screen (Marwa, 16 Oct);
3. when a sentence runs into the next one, makes the video wait (a hold) instead of talking over it;
4. keeps the opening short (Marwa, 28 Oct: 2 seconds at most): a first sentence longer than the
   opening is sped up a little (up to 1.2x, pitch kept) rather than holding the opening;
5. writes posts/NN/vo/NN.wav and posts/NN/vo.json, which build.py reads through load_vo().

Then: python3 posts/NN/build.py  (reel.mp4 = effects only, reel-vo.mp4 = with the voice).
"""
import importlib.util, json, os, subprocess, sys, wave
import numpy as np

DESIGN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DESIGN)
import reel  # noqa: E402

SR = reel.SR
GAP = .18            # breath between one sentence and the next line
LEAD_IN = .05        # sentence starts this much after its line appears
GAP_OPENING = .05    # the opening question runs straight into the answer: the cut is the breath
MAX_SPEEDUP = 1.2
PAUSE_KEEP = .28     # pauses inside a sentence (at commas) are shortened to this, for a lively pace
PAUSE_KEEP_OPENING = .1


def load(path):
    return reel._load_any(path)


def save(path, x):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def split(x, n, frame=.02, floor_db=-38, min_gap=.25):
    """Cut x into n sentences at its n-1 longest pauses."""
    hop = int(frame * SR)
    rms = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    peak = rms.max() or 1
    loud = 20 * np.log10(rms / peak + 1e-9) > floor_db
    idx = np.flatnonzero(loud)
    first, last = idx[0], idx[-1]
    gaps, k = [], first
    while k <= last:
        if not loud[k]:
            j = k
            while j <= last and not loud[j]:
                j += 1
            if (j - k) * frame >= min_gap:
                gaps.append((j - k, k, j))
            k = j
        else:
            k += 1
    if len(gaps) < n - 1:
        sys.exit(f"found {len(gaps) + 1} sentences in the take, the plan has {n}: check the pauses")
    cuts = sorted(gaps, key=lambda g: -g[0])[:n - 1]
    cuts = sorted((a, b) for _, a, b in cuts)
    bounds, s = [], first
    for a, b in cuts:
        bounds.append((s, a)); s = b
    bounds.append((s, last + 1))
    pad = int(.04 * SR)
    return [x[max(0, a * hop - pad):min(len(x), b * hop + pad)] for a, b in bounds]


def squeeze(x, keep, frame=.02, floor_db=-38):
    """Shorten every pause inside a sentence to `keep` seconds (the voice itself is untouched)."""
    hop = int(frame * SR)
    rms = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    quiet = 20 * np.log10(rms / (rms.max() or 1) + 1e-9) <= floor_db
    out, k, n, kf = [], 0, len(quiet), int(round(keep / frame))
    last = 0
    while k < n:
        if quiet[k]:
            j = k
            while j < n and quiet[j]:
                j += 1
            if 0 < k and j < n and j - k > kf:          # an inner pause, longer than we keep
                a, b = k * hop, j * hop
                mid = a + kf * hop // 2
                out.append(x[last:mid]); last = b - kf * hop // 2
            k = j
        else:
            k += 1
    out.append(x[last:])
    return np.concatenate(out)


def tempo(x, f):
    """Speed x up by f, pitch kept (ffmpeg atempo)."""
    tmp_in, tmp_out = "/tmp/_vo_in.wav", "/tmp/_vo_out.wav"
    save(tmp_in, x)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp_in, "-filter:a", f"atempo={f:.4f}", tmp_out], check=True)
    return load(tmp_out)


def main():
    nn, take = sys.argv[1], sys.argv[2]
    intro = float(sys.argv[sys.argv.index("--intro") + 1]) if "--intro" in sys.argv else 2.0
    here = os.path.join(DESIGN, "posts", nn)
    spec = importlib.util.spec_from_file_location("build", os.path.join(here, "build.py"))
    b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
    plan, dur_d = b.VO_PLAN, b.DUR_DESIGN

    parts = split(load(take), len(plan))
    parts = [squeeze(p, PAUSE_KEEP_OPENING if i == 0 else PAUSE_KEEP) for i, p in enumerate(parts)]
    # the opening: the first sentence must be done before the second line arrives
    room = plan[1][0] - plan[0][0] - GAP_OPENING if len(plan) > 1 else None
    if room and len(parts[0]) / SR > room and plan[1][0] <= intro + 1e-6:
        f = min(MAX_SPEEDUP, len(parts[0]) / SR / room)
        parts[0] = tempo(parts[0], f)
        print(f"opening sentence sped up {f:.2f}x to {len(parts[0]) / SR:.2f}s")

    holds = []
    def rt(t):
        return t + sum(j for h, j in holds if t >= h)

    voice, end = [], 0.0
    for i, ((d, text, hold_at), x) in enumerate(zip(plan, parts)):
        start = rt(d) + (LEAD_IN if i else 0.0)    # the question is on screen from frame one, and so is its voice
        if start < end:                    # the line before is still being said: wait for it
            h = hold_at if hold_at is not None else d - .35
            extra = end - start
            holds.append((round(h, 3), round(extra, 3)))
            start += extra
        f = os.path.join("vo", f"{i + 1:02d}.wav")
        save(os.path.join(here, f), x)
        voice.append((round(start, 3), f))
        end = start + len(x) / SR + (GAP if i else GAP_OPENING)
        print(f"{start:6.2f}s  {len(x) / SR:4.2f}s  {text}")
    dur = max(rt(dur_d), end + 1.2)
    json.dump({"holds": holds, "voice": voice, "dur": round(dur, 2)}, open(os.path.join(here, "vo.json"), "w"), indent=1)
    print("holds", holds, "duration", f"{dur:.1f}s")


if __name__ == "__main__":
    main()
