"""Three portfolio reels: the site at phone size + Bodi (Gemini) voice-over.

    python3 site_reels.py A take.wav [--preview]

1. cut the take into its sentences at the longest pauses (design/vo.py), shorten inner pauses,
2. lay the sentences one after another, and place each visual action on its sentence,
3. record the site frame by frame (engine.js), mix voice + soft taps/whooshes, encode 1080x1920.
"""
import json, os, subprocess, sys, wave
import numpy as np
D = '/home/claude/shwani-media/design'
sys.path.insert(0, D)
import reel, vo  # noqa
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import split2

SR = reel.SR
HERE = os.path.dirname(os.path.abspath(__file__))
GAP = .32          # breath between sentences
START = .35        # first word after the headline starts writing
TAIL = 1.6         # the last frame holds a moment after the voice ends
J = 1.15           # a jump between sections

def frac(text, word):
    """Where `word` starts in the sentence, as a share of its length (to time a visual to a word)."""
    i = text.find(word); assert i >= 0, word
    return i / len(text)

# ---- the three reels: sentences (as given to Gemini) and what happens on screen during each
REELS = {
 'A': dict(name='reel-A-ad', sents=[
   'فِكْرَتُكَ عَلى ضِفَّةْ، وَالنَّتِيجَةُ عَلى الأُخْرى.',
   'هذا مَوْقِعُ شْوْاني كومْباني، الجِسْرُ بَيْنَهُما.',
   'نُصَمِّمُ هَوِيَّتَكَ البَصَرِيَّةْ، وَكُلَّ ما يُطْبَعُ بِاسْمِكْ،',
   'وَنَبْني مَوْقِعَكَ الإِلِكْتْرُونِيَّ بِأَكْثَرَ مِنْ لُغَةْ،',
   'وَنُساعِدُكَ في سِيرَتِكَ الذّاتِيَّةِ وَبَحْثِكْ.',
   'افْتَحِ الرّابِطْ، وَاطْلُبْ خِدْمَتَكَ مِنْ هاتِفِكْ.']),
 'B': dict(name='reel-B-tour', sents=[
   'هذا مَوْقِعُ شْوْاني كومْباني، وَفي أَقَلَّ مِنْ دَقِيقَةٍ سَتَرى كُلَّ ما نَصْنَعُهْ.',
   'هَوِيّاتٌ بَصَرِيَّةٌ تُحْفَظْ، وَمَطْبُوعاتٌ تُلْمَسْ، وَمَواقِعُ إِلِكْتْرُونِيَّةْ، وَحُلُولٌ تِقْنِيَّةٌ تَعْمَلْ.',
   'هُنا قِطَعٌ حَقِيقِيَّةٌ مِنْ هَوِيَّتِنا، تَدُورُ مَعَكَ كُلَّما مَرَّرْتْ.',
   'وَهُنا نَعْبُرُ مَعَكَ خَمْسَ خُطُواتْ، مِنْ حِكايَتِكَ إِلى هَوِيَّتِكَ كامِلَةْ.',
   'اضْغَطْ أَيَّ قِطْعَةْ، فَيَظْهَرُ تَصْمِيمُها كامِلاً.',
   'ثُمَّ خِدْماتُنا السَّبْعْ: الهَوِيَّةْ، وَتَصامِيمُ الشَّرِكاتِ وَالأَفْرادْ، وَالمَواقِعْ، وَالسِّيرَةُ الذّاتِيَّةْ، وَالبُحُوثْ، وَالخِدْماتُ التِّقْنِيَّةْ.',
   'وَكُلُّ شَيْءٍ مَكْتُوبٌ بَيْنَنا قَبْلَ أَنْ نَبْدَأْ.',
   'الرّابِطُ في البايو، أَرْسِلْهُ لِصاحِبِ مَشْرُوعٍ جَدِيدْ.']),
 'C': dict(name='reel-C-website', sents=[
   'هذا لَيْسَ تَطْبِيقاً، هذا مَوْقِعُ شْوْاني كومْباني.',
   'نُصَمِّمُ الهَوِيّاتِ وَالمَطْبُوعاتْ، وَنَبْني المَواقِعْ، وَنُساعِدُ في السِّيرَةِ الذّاتِيَّةِ وَالبُحُوثْ.',
   'اسْحَبِ القِطَعْ، وَاخْتَرْ واحِدَةْ.',
   'اضْغَطْها، فَيَنْفَتِحُ تَصْمِيمُها كامِلاً، بِمَلَفّاتِ الطِّباعَةِ الحَقِيقِيَّةْ.',
   'وَالْمِسْ أَيَّ جُزْءٍ مِنْهْ، لِتَرى ما يُمْكِنُ أَنْ نُصَمِّمَهُ لَكْ.',
   'مَوْقِعٌ مِثْلُ هذا نَبْنيهِ لَكَ أَيْضاً: لِلأَفْرادِ وَالمَحَلّاتِ وَالشَّرِكاتْ، بِأَكْثَرَ مِنْ لُغَةْ.',
   'أَرْسِلْهُ لِصاحِبِ مَشْرُوعٍ يَحْتاجُ مَوْقِعاً.']),
}

def sc(at, to, dur, ease='io', jump=False):
    return dict(at=round(at, 3), type='scroll', to=to, dur=round(dur, 3), ease=ease, jump=jump)

def actions(key, S, end):
    """S = [(start, length)] per sentence; end = when the voice stops. Returns the action list."""
    s = [a for a, _ in S]; d = [b for _, b in S]; T = REELS[key]['sents']; A = []
    if key == 'A':      # opens on the crossing: an idea on one bank, the result on the other
        A += [sc(s[0] + .6, ['#hw', 'p', 1], s[1] + d[1] - s[0] - .4, 'sio'),
              sc(s[2] - .45, ['#services', 'serv', 0], J, jump=True),
              sc(s[2] + d[2] * frac(T[2], 'وَكُلَّ') - .3, ['#services', 'serv', 1], .8),
              sc(s[3] - .3, ['#services', 'serv', 3], 1.0),
              sc(s[4] - .1, ['#services', 'serv', 4], .8),
              sc(s[4] + d[4] * frac(T[4], 'وَبَحْثِكْ') - .25, ['#services', 'serv', 5], .8),
              sc(s[5] - .45, ['#closing', 'top', 0], 1.3, jump=True),
              sc(s[5] + 1.2, ['#footer', 'max', 0], max(1.2, end - s[5] - .6), 'sio')]
    if key == 'B':      # the tour: the front page only while the name is said, then straight in
        k = T[5]; tin = s[0] + d[0] * frac(T[0], 'وَفي') - .35
        e2 = s[1] + d[1]
        A += [sc(tin, ['#benefits', 'top', 0], J, jump=True),
              sc(tin + J, ['#benefits', 'p', 1], e2 - 1.8 - tin - J, 'lin'),
              sc(e2 - 1.8, ['#approach', 'top', -40], 2.1, 'sio'),
              sc(s[2] - .45, ['#pieces', 'top', 0], J, jump=True),
              dict(at=round(s[2] + .45, 3), type='drag', el='#shelf', **{'from': [.8, .55], 'to': [.25, .55]}, dur=.6),
              dict(at=round(s[2] + d[2] * frac(T[2], 'تَدُورُ'), 3), type='drag', el='#shelf', **{'from': [.8, .55], 'to': [.25, .55]}, dur=.6),
              sc(s[3] - .45, ['#hw', 'p', 0], J, jump=True),
              sc(s[3] - .45 + J, ['#hw', 'p', 1], d[3] + .45 - J + .15, 'sio'),
              sc(s[4] - .45, ['#pieces', 'top', 0], J, jump=True),
              dict(at=round(s[4] + d[4] * frac(T[4], 'فَيَظْهَرُ') - .2, 3), type='tap', el='center-piece'),
              dict(at=round(s[5] + .1, 3), type='tap', el='#pvX'),
              sc(s[5] + .6, ['#services', 'serv', 0], J, jump=True)]
        for i, w in enumerate(['وَتَصامِيمُ', 'وَالأَفْرادْ', 'وَالمَواقِعْ', 'وَالسِّيرَةُ', 'وَالبُحُوثْ', 'وَالخِدْماتُ'], 1):
            A.append(sc(s[5] + d[5] * frac(k, w) - .3, ['#services', 'serv', i], .6))
        A += [sc(s[6] - .45, ['#facts', 'top', -10], J, jump=True),
              sc(s[7] - .45, ['#closing', 'top', 0], 1.3, jump=True),
              sc(s[7] + 1.0, ['#footer', 'max', 0], max(1.2, end - s[7] - .4), 'sio')]
    if key == 'C':      # opens on the dark scene, then the site answers every touch
        A += [sc(.2, ['#approach', 'top', 60], s[0] + d[0] * frac(T[0], 'هذا مَوْقِعُ') - .4, 'sio'),
              dict(at=round(s[0] + d[0] * frac(T[0], 'هذا مَوْقِعُ') - .15, 3), type='tap', el='.menuBtn'),
              dict(at=round(s[1] + .35, 3), type='tap', el='#mClose'),
              sc(s[1] + .9, ['#services', 'serv', 0], J, jump=True),
              sc(s[1] + d[1] * frac(T[1], 'وَالمَطْبُوعاتْ') - .2, ['#services', 'serv', 1], .6),
              sc(s[1] + d[1] * frac(T[1], 'وَنَبْني') - .2, ['#services', 'serv', 3], .7),
              sc(s[1] + d[1] * frac(T[1], 'السِّيرَةِ') - .3, ['#services', 'serv', 4], .6),
              sc(s[1] + d[1] * frac(T[1], 'وَالبُحُوثْ') - .2, ['#services', 'serv', 5], .6),
              sc(s[2] - .6, ['#pieces', 'top', 0], J, jump=True),
              dict(at=round(s[2] + .35, 3), type='drag', el='#shelf', **{'from': [.2, .55], 'to': [.75, .55]}, dur=.6),
              dict(at=round(s[2] + d[2] * frac(T[2], 'وَاخْتَرْ') + .05, 3), type='drag', el='#shelf', **{'from': [.2, .55], 'to': [.75, .55]}, dur=.6),
              dict(at=round(s[3] + .25, 3), type='tap', el='center-piece'),
              dict(at=round(s[3] + d[3] * frac(T[3], 'بِمَلَفّاتِ'), 3), type='pvscroll', by=210, dur=1.6),
              dict(at=round(s[4] - .35, 3), type='pvscroll', by=-210, dur=.5),
              dict(at=round(s[4] + d[4] * frac(T[4], 'جُزْءٍ'), 3), type='tap', el='nth-hs:0'),
              dict(at=round(s[5] - .75, 3), type='tap', el='#pvX'),
              sc(s[5] - .2, ['#statement', 'top', -30], J, jump=True),
              sc(s[5] + J, ['#statement', 'top', 20], d[5] - J, 'sio'),
              dict(at=round(s[6] + .05, 3), type='tap', el='#statement button[data-serv="3"]')]
    return A

def layout(parts):
    S, t = [], START
    for x in parts:
        S.append((round(t, 3), len(x) / SR)); t += len(x) / SR + GAP
    return S, t - GAP

def mix(S, parts, acts, dur, out):
    n = int(dur * SR) + SR; bed = np.zeros(n); vox = np.zeros(n)
    rng = np.random.default_rng(7)
    for (t, _), x in zip(S, parts):
        x = x / (np.max(np.abs(x)) or 1) * 10 ** (vo.VO_PEAK_DB / 20); i = int(t * SR); vox[i:i + len(x)] += x
    for a in acts:
        if a['type'] == 'tap':
            c = reel._click(rng) * .55; i = int((a['at'] + .12 - reel.CLICK_LEAD) * SR); bed[i:i + len(c)] += c[:n - i]
        if a['type'] == 'drag':
            c = reel._paper(rng, 'slide', reel.G_SLIDE * .7); i = int(a['at'] * SR); bed[i:i + len(c)] += c[:n - i]
        if a['type'] == 'scroll' and a.get('jump'):
            w = reel._whoosh(rng) * .7; i = int(a['at'] * SR); bed[i:i + len(w)] += w[:n - i]
    y = reel._limit(vox + bed, reel.VO_CEIL)[:int(dur * SR)]
    with wave.open(out, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())

def main():
    key, take = sys.argv[1], sys.argv[2]; preview = '--preview' in sys.argv
    R = REELS[key]; out = os.path.join(HERE, 'out', R['name']); os.makedirs(out, exist_ok=True)
    parts, cuts = split2.split(reel._load_any(take), R['sents']); print('cuts', cuts)
    parts = [p if i == 0 else vo.squeeze(p, vo.PAUSE_KEEP) for i, p in enumerate(parts)]
    S, end = layout(parts); dur = round(end + TAIL, 2)
    acts = actions(key, S, end)
    for (t, l), txt in zip(S, R['sents']): print(f'{t:6.2f}s {l:4.2f}s  {txt}')
    print('duration', dur)
    start = {'A': ['#hw', 'p', 0], 'C': ['#approach', 'top', 0]}.get(key)
    json.dump({'dur': dur, 'actions': acts, 'voice': S, **({'start': start} if start else {})}, open(os.path.join(out, 'plan.json'), 'w'), ensure_ascii=False, indent=1)
    mix(S, parts, acts, dur, os.path.join(out, 'audio.wav'))
    fr = os.path.join(out, 'frames-preview' if preview else 'frames')
    subprocess.run(['rm', '-rf', fr]); subprocess.run(['node', os.path.join(HERE, 'engine.js'), os.path.join(out, 'plan.json'), fr] + (['--preview'] if preview else []), check=True)
    if preview: return
    mp4 = os.path.join(out, R['name'] + '.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', '30', '-i', os.path.join(fr, 'f%05d.jpg'), '-i', os.path.join(out, 'audio.wav'),
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '30', '-movflags', '+faststart',
                    '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest', mp4], check=True)
    print('wrote', mp4)

if __name__ == '__main__':
    main()
