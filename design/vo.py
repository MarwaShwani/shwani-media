"""Place a recorded voice-over take on a reel, sentence by sentence.

    python3 vo.py NN take.wav

posts/NN/build.py defines VO_PLAN = [(design_time, sentence, hold_at or None), ...] and DUR_DESIGN.
The take is one recording of all the sentences in that order, with a clear pause between them
(in Google AI Studio: <long pause> between sentences). This script

1. cuts the take at its longest pauses into exactly len(VO_PLAN) sentences, trims each one,
   and shortens long pauses inside the later sentences (the opening question is left as spoken);
2. sizes the opening to the question (Marwa, 28 Oct, 4:12: the opening lasts as long as the voice
   needs to say it naturally and at ease; the earlier 2-second rule is dropped): vo.json gets
   "intro" = the question + a breath, and build.py builds its opening scene that long (load_intro);
3. puts each sentence at the moment its line appears on screen (Marwa, 16 Oct);
4. when a sentence runs into the next one, makes the video wait (a hold) instead of talking over it;
5. writes posts/NN/vo/NN.wav and posts/NN/vo.json, which build.py reads through load_vo().

Then: python3 posts/NN/build.py  (reel.mp4 = effects only, reel-vo.mp4 = with the voice).
"""
import importlib.util, json, os, sys, wave
import numpy as np

DESIGN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DESIGN)
import reel  # noqa: E402

SR = reel.SR
GAP = .18            # breath between one sentence and the next line
LEAD_IN = .05        # sentence starts this much after its line appears
GAP_OPENING = .3     # a relaxed breath after the opening question, before the answer
MIN_INTRO = 1.6      # the opening is never shorter than this, even for a very short question
PAUSE_KEEP = .28     # pauses inside the later sentences (at commas) are shortened to this
VO_PEAK_DB = -10     # every sentence peaks here: a calm, even level (Marwa, 16 Oct: peaks about -10 dBFS)


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


def _import_build(here):
    spec = importlib.util.spec_from_file_location("build", os.path.join(here, "build.py"))
    b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
    return b


def _plan_len(here):
    return len(_import_build(here).VO_PLAN)


def main():
    nn, take = sys.argv[1], sys.argv[2]
    here = os.path.join(DESIGN, "posts", nn)
    vo_json = os.path.join(here, "vo.json")

    parts = split(load(take), _plan_len(here))
    parts = [p if i == 0 else squeeze(p, PAUSE_KEEP) for i, p in enumerate(parts)]
    intro = round(max(MIN_INTRO, len(parts[0]) / SR + GAP_OPENING), 2)
    # the opening scene is built as long as the question needs: build.py reads "intro" before its timeline
    json.dump({"intro": intro, "holds": [], "voice": [], "dur": 0}, open(vo_json, "w"))
    b = _import_build(here)
    plan, dur_d = b.VO_PLAN, b.DUR_DESIGN
    print(f"opening {intro:.2f}s (question {len(parts[0]) / SR:.2f}s, as spoken)")

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
        save(os.path.join(here, f), x / (np.max(np.abs(x)) or 1) * 10 ** (VO_PEAK_DB / 20))
        voice.append((round(start, 3), f))
        end = start + len(x) / SR + (GAP if i else GAP_OPENING)
        print(f"{start:6.2f}s  {len(x) / SR:4.2f}s  {text}")
    dur = max(rt(dur_d), end + 1.2)
    json.dump({"intro": intro, "holds": holds, "voice": voice, "dur": round(dur, 2)}, open(vo_json, "w"), indent=1)
    print("holds", holds, "duration", f"{dur:.1f}s")


if __name__ == "__main__":
    main()
