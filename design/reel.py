"""Shared helpers for SHWANI COMPANY reels: 1080x1920, 30 fps.

A reel is one HTML page. Everything that moves is a CSS animation placed on one
global timeline (animation-delay = seconds from the start of the reel). The
renderer pauses every animation and seeks it to each frame time, so the video is
exact and repeatable.

Sound: real recorded effects from design/sfx (mouse clicks, keyboard keys, UI
toggles and chimes; licences in sfx/LICENSES.md), placed from the cue list. No
music. A voice-over version mixes a narration track on top with the effects lowered.

House rules (from Marwa, 15 Oct 2026):
- no prices in any video;
- the background is never empty: small, faint topic icons drift behind the content;
- an unhurried pace, with time to read each line and to take in each movement;
- the SHWANI logo, never the SH mark alone;
- small text no smaller than 34px, body text 44px and up.

Instagram covers its own buttons and caption over the bottom ~420px and the top
~200px of a reel, so key content stays between y=260 and y=1480.
"""
import os, sys, asyncio, subprocess, wave, math, functools, itertools
import numpy as np

DESIGN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DESIGN)
from common import fontlinks, lockup_svg, mark_inline, HANDLE, CH, MU, DK, TE, SL, TL, SG, RO, PL  # noqa: E402,F401

W, H, FPS, SR = 1080, 1920, 30, 44100
EASE = "cubic-bezier(.2,.8,.2,1)"
BOUNCE = "cubic-bezier(.34,1.56,.64,1)"
SFX_DIR = os.path.join(DESIGN, "sfx")


# ---------- voice-over timing ----------
# HOLDS: (design time, extra seconds). Everything placed at or after a hold's design time
# happens that many seconds later, so the visuals wait for the voice. Empty = no voice-over.
HOLDS = []


def RT(t):
    """Design time -> real time."""
    return t + sum(j for h, j in HOLDS if t >= h)


def load_intro(here, default):
    """Length of a reel's opening scene: as long as the voice needs to ask the question naturally
    (vo.py writes it to posts/NN/vo.json as "intro"; Marwa, 28 Oct, 4:12), else `default`."""
    p = os.path.join(here, "vo.json")
    if os.path.exists(p):
        import json
        return json.load(open(p)).get("intro", default)
    return default


def load_vo(here):
    """Read posts/NN/vo.json (written by vo.py) and switch the timeline to it. Returns it or None."""
    p = os.path.join(here, "vo.json")
    if not os.path.exists(p):
        return None
    import json
    vo = json.load(open(p))
    HOLDS[:] = [tuple(h) for h in vo["holds"]]
    vo["voice"] = [(t, os.path.join(here, f)) for t, f in vo["voice"]]
    return vo


def an(name, t, d=.7, ease=EASE, fill="both", raw=False):
    """One CSS animation starting at design time t (real time when raw=True)."""
    return f"{name} {d:.3f}s {ease} {(t if raw else RT(t)):.3f}s 1 normal {fill}"


def anims(*specs):
    return "animation:" + ",".join(specs) + ";"


def timeline(durations):
    """Scene start times from a list of scene lengths: [8, 6.5, ...] -> [0, 8, 14.5, ...] and the total."""
    starts, t = [], 0.0
    for d in durations:
        starts.append(t); t += d
    return starts, t


def broll(here, src, w, h, start=0.0, dur=None, speed=1.0, crop=None, grade=""):
    """Frames of a b-roll video clip for Reel.clip(): posts/NN/<src> -> posts/NN/broll-<name>/f0001.jpg ...

    w, h: the box it fills on screen (frames are cut to that shape, centred).
    crop: optional (x, y, cw, ch) in the source pixels, taken first (e.g. to cut off a watermark corner).
    speed < 1 slows it down. grade: extra ffmpeg filters (e.g. "eq=saturation=.9").
    Cached: the frames are made again only when the settings change. Returns (dir, frame_count).
    """
    import hashlib, glob, shutil
    name = os.path.splitext(os.path.basename(src))[0]
    rel = f"broll-{name}"
    out = os.path.join(here, rel)
    key = hashlib.md5(repr((os.path.getmtime(os.path.join(here, src)), w, h, start, dur, speed, crop, grade)).encode()).hexdigest()
    stamp = os.path.join(out, ".key")
    if not (os.path.exists(stamp) and open(stamp).read() == key):
        shutil.rmtree(out, ignore_errors=True)
        os.makedirs(out)
        vf = []
        if crop:
            vf.append("crop=%d:%d:%d:%d" % (crop[2], crop[3], crop[0], crop[1]))
        vf += [f"setpts=PTS/{speed}", f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos",
               f"crop={w}:{h}", f"fps={FPS}"]
        if grade:
            vf.append(grade)
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", str(start)]
        if dur:
            cmd += ["-t", str(dur * speed)]     # dur = seconds on screen; the input needs dur*speed
        cmd += ["-i", os.path.join(here, src), "-an", "-vf", ",".join(vf), "-q:v", "2", os.path.join(out, "f%04d.jpg")]
        subprocess.run(cmd, check=True)
        open(stamp, "w").write(key)
    return rel, len(glob.glob(os.path.join(out, "f*.jpg")))


BASE_CSS = """
*{box-sizing:border-box}
html,body{margin:0;background:%(bg)s}
.r{width:1080px;height:1920px;background:%(bg)s;color:%(fg)s;font-family:'Alexandria',sans-serif;position:relative;overflow:hidden}
.sc{position:absolute;inset:0;z-index:2}
.bgl{position:absolute;inset:0;z-index:0;pointer-events:none}
.ab{position:absolute}
.ltr{direction:ltr;unicode-bidi:isolate}
.cur{position:absolute;left:0;top:0;width:76px;height:76px;margin:-38px 0 0 -38px;border-radius:50%%;
     background:rgba(32,33,38,.42);border:5px solid #fff;box-shadow:0 10px 28px rgba(32,33,38,.35);z-index:50;opacity:0}
.rip{position:absolute;width:80px;height:80px;margin:-40px 0 0 -40px;border-radius:50%%;border:5px solid %(acc)s;opacity:0;z-index:49}
[data-type]::after{content:"";display:inline-block;width:4px;height:.9em;background:currentColor;margin-inline-start:4px;vertical-align:-.1em;opacity:calc(var(--caret,0) * .7)}
@keyframes sIn{from{opacity:0}to{opacity:1}}
@keyframes sOut{from{opacity:1}to{opacity:0}}
@keyframes sOutUp{from{opacity:1;transform:none}to{opacity:0;transform:translateY(-120px) scale(.96)}}
@keyframes up{from{opacity:0;transform:translateY(60px)}to{opacity:1;transform:none}}
@keyframes down{from{opacity:0;transform:translateY(-60px)}to{opacity:1;transform:none}}
@keyframes pop{0%%{opacity:0;transform:scale(.5)}60%%{opacity:1;transform:scale(1.05)}100%%{opacity:1;transform:scale(1)}}
@keyframes zoom{from{opacity:0;transform:scale(1.4)}to{opacity:1;transform:scale(1)}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes fromR{from{opacity:0;transform:translateX(120px)}to{opacity:1;transform:none}}
@keyframes fromL{from{opacity:0;transform:translateX(-120px)}to{opacity:1;transform:none}}
@keyframes out{from{opacity:1}to{opacity:0}}
@keyframes outUp{from{opacity:1;transform:none}to{opacity:0;transform:translateY(-60px)}}
@keyframes dim{from{opacity:1}to{opacity:.3}}
@keyframes press{0%%,100%%{transform:scale(1)}45%%{transform:scale(.93)}}
@keyframes shake{0%%,100%%{transform:none}20%%{transform:translateX(-14px) rotate(-1deg)}40%%{transform:translateX(12px) rotate(1deg)}60%%{transform:translateX(-8px)}80%%{transform:translateX(5px)}}
@keyframes rip{0%%{opacity:.95;transform:scale(.45)}100%%{opacity:0;transform:scale(2.7)}}
@keyframes draw{to{stroke-dashoffset:0}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes growY{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes spin{from{transform:rotate(0)}to{transform:rotate(360deg)}}
@keyframes drift{0%%,100%%{transform:translate(0,0) rotate(var(--r0))}50%%{transform:translate(var(--dx),var(--dy)) rotate(var(--r1))}}
@keyframes pulse{0%%,100%%{transform:scale(1)}50%%{transform:scale(1.05)}}
"""

SEEK_JS = """
window.__seek = function(ms){
  for (const a of document.getAnimations()) { a.pause(); a.currentTime = ms; }
  const t = ms / 1000;
  document.querySelectorAll('[data-count]').forEach(e => {
    const f = e.dataset.count.split(':').map(Number);
    const [a, b, t0, t1, dec] = f;
    let p = Math.min(1, Math.max(0, (t - t0) / (t1 - t0)));
    if (f[5] === 1) {   // stepped like a clock: one whole number per beat, evenly spaced (each beat has its tick)
      const n = Math.abs(b - a), k = Math.min(n, Math.floor(p * n + 1e-6));
      e.textContent = String(a + Math.sign(b - a) * k);
    } else {
      p = 1 - Math.pow(1 - p, 3);
      e.textContent = (a + (b - a) * p).toFixed(dec);
    }
  });
  document.querySelectorAll('[data-type]').forEach(e => {
    if (e.__full === undefined) e.__full = e.textContent;
    const [t0, t1] = e.dataset.type.split(':').map(Number);
    const p = Math.min(1, Math.max(0, (t - t0) / (t1 - t0)));
    const ch = [...e.__full];
    e.textContent = ch.slice(0, Math.round(p * ch.length)).join('');
    e.style.setProperty('--caret', (p > 0 && p < 1) ? 1 : 0);
  });
  document.querySelectorAll('[data-steps]').forEach(e => {
    const st = e.dataset.steps.split(',').map(s => s.split(':').map(Number));
    let v = st[0][1];
    for (let k = 1; k < st.length; k++) {
      const [tk, vk] = st[k];
      if (t < tk) break;
      let p = Math.min(1, (t - tk) / 0.7); p = 1 - Math.pow(1 - p, 3);
      v = v + (vk - v) * p;
    }
    e.textContent = Math.round(v);
  });
  // b-roll clips: frames extracted to <dir>/f0001.jpg..., shown frame by frame in real time
  const waits = [];
  document.querySelectorAll('[data-clip]').forEach(e => {
    const [t0, fps, n] = e.dataset.clip.split(':').map(Number);
    const i = Math.max(0, Math.min(n - 1, Math.floor((t - t0) * fps + 1e-6)));
    const src = e.dataset.dir + '/f' + String(i + 1).padStart(4, '0') + '.jpg';
    if (e.getAttribute('src') !== src) { e.setAttribute('src', src); waits.push(e.decode().catch(() => {})); }
  });
  return Promise.all(waits);
};
"""

# ---------- faint topic icons for the background (64x64, stroked) ----------
ICONS = {
    "doc": '<path d="M16 6h22l12 12v40H16z"/><path d="M38 6v12h12M23 30h20M23 39h20M23 48h13"/>',
    "clip": '<path d="M40 18L22 36a7 7 0 0 0 10 10l20-20a12 12 0 0 0-17-17L14 30a17 17 0 0 0 24 24l14-14"/>',
    "case": '<rect x="8" y="20" width="48" height="34" rx="6"/><path d="M24 20v-7h16v7M8 34h48"/>',
    "search": '<circle cx="27" cy="27" r="16"/><path d="M39 39l15 15"/>',
    "pen": '<path d="M44 8l12 12-32 32H12V40z"/><path d="M38 14l12 12"/>',
    "clock": '<circle cx="32" cy="32" r="24"/><path d="M32 18v15l10 6"/>',
    "check": '<circle cx="32" cy="32" r="24"/><path d="M21 33l8 8 15-17"/>',
    "mail": '<rect x="8" y="14" width="48" height="36" rx="5"/><path d="M8 18l24 18 24-18"/>',
    "pencil": '<path d="M12 52l4-14L42 12l10 10-26 26z"/><path d="M36 18l10 10M12 52l14-4"/>',
    "bezier": '<path d="M10 48C18 18 46 46 54 16"/><rect x="5" y="43" width="10" height="10" rx="2"/><rect x="49" y="11" width="10" height="10" rx="2"/><path d="M10 48l18-26M54 16L36 42"/>',
    "circle": '<circle cx="32" cy="32" r="20"/>',
    "tri": '<path d="M32 12l22 38H10z"/>',
    "square": '<rect x="14" y="14" width="36" height="36" rx="4"/>',
    "drop": '<path d="M32 8C22 24 16 32 16 40a16 16 0 0 0 32 0c0-8-6-16-16-32z"/>',
    "eraser": '<path d="M24 52h28M14 42l22-22 14 14-18 18H24z"/><path d="M26 30l14 14"/>',
    "book": '<path d="M32 16c-6-5-16-6-24-4v38c8-2 18-1 24 4 6-5 16-6 24-4V12c-8-2-18-1-24 4z"/><path d="M32 16v38"/>',
    "ruler": '<rect x="6" y="22" width="52" height="20" rx="3"/><path d="M14 22v8M22 22v5M30 22v8M38 22v5M46 22v8"/>',
    "star": '<path d="M32 8l7 15 16 2-12 11 3 16-14-8-14 8 3-16L9 25l16-2z"/>',
    "cap": '<path d="M4 26l28-12 28 12-28 12z"/><path d="M16 31v12c8 6 24 6 32 0V31M58 27v14"/>',
    "plane": '<path d="M6 30l50-20-14 44-10-16z"/><path d="M32 38l24-28"/>',
    "abc": '<path d="M8 46l8-26 8 26M11 37h10M30 20h8a6 6 0 0 1 0 12h-8zM30 32h9a7 7 0 0 1 0 14h-9zM58 24a10 10 0 1 0 0 18"/>',
    "bag": '<rect x="14" y="20" width="36" height="36" rx="8"/><path d="M24 20v-4a8 8 0 0 1 16 0v4M14 34h36"/>',
}


class Reel:
    def __init__(self, bg=CH, fg=DK, acc=TE):
        self.bg, self.fg, self.acc = bg, fg, acc
        self.cues = []      # (seconds, kind, params)
        self.kf = []        # generated @keyframes
        self.n = 0

    # ---------- timeline helpers ----------
    def uid(self, p="k"):
        self.n += 1
        return f"{p}{self.n}"

    def cue(self, t, kind, raw=False, **params):
        self.cues.append((t if raw else RT(t), kind, params))

    def el(self, t, html, kind="up", d=.7, style="", out=None, out_kind="out", out_d=.4, cue=None, ease=None, cls="", tag="div"):
        """An element that enters at t (and optionally leaves at `out`)."""
        e = ease or (BOUNCE if kind == "pop" else EASE)
        a = [an(kind, t, d, e)]
        if out is not None:
            a.append(an(out_kind, out, out_d, "ease-in", "forwards"))
        if cue:
            self.cue(t, cue)
        return f'<{tag} class="{cls}" style="{style};{anims(*a)}">{html}</{tag}>'

    def scene(self, t0, t1, html, style="", enter="sIn", leave="sOut", d=.45, cue="whoosh"):
        a = [an(enter, t0, d)] if t0 > 0 else []      # the first scene is on screen from frame one
        if t1 is not None:   # fully gone by t1, so the next scene starts on a clean screen
            a.append(an(leave, RT(t1) - .5, .5, "cubic-bezier(.5,0,.75,0)", "forwards", raw=True))
        if cue and t0 > 0:
            self.cue(max(0, t0 - .1), cue)
        return f'<div class="sc" style="{style};{anims(*a) if a else ""}">{html}</div>'

    def clip(self, t, frames, style=""):
        """A b-roll clip (made by broll()) that starts playing at t, muted, cropped to fill its box."""
        d, n = frames
        return (f'<img data-dir="{d}" data-clip="{RT(t):.3f}:{FPS}:{n}" src="{d}/f0001.jpg" '
                f'style="display:block;width:100%;height:100%;object-fit:cover;{style}">')

    def typing(self, t0, t1, text, style="", cls=""):
        """Text typed out between t0 and t1, with keyboard sounds."""
        self.cue(t0, "type", n=len(text), d=RT(t1) - RT(t0))
        return f'<span class="{cls}" style="{style}" data-type="{RT(t0):.2f}:{RT(t1):.2f}">{text}</span>'

    def ripple(self, t, x, y, color=None):
        """t is real time (called from cursor())."""
        c = f"border-color:{color};" if color else ""
        return f'<div class="rip" style="left:{x}px;top:{y}px;{c}{anims(an("rip", t, .7, "ease-out", "none", raw=True))}"></div>'

    def pressed(self, t, html, style=""):
        """Wrap something that gets pressed (scales down a little) at t."""
        return f'<div style="{style};{anims(an("press", RT(t) - .05, .35, "ease-out", "none", raw=True))}">{html}</div>'

    def cursor(self, pts, sound="click"):
        """A touch indicator that glides between points and taps.

        pts: list of (t, x, y, act) with act in 'show', 'move', 'tap', 'down', 'up', 'hide'.
        For 'tap' the finger arrives at (x, y) shortly before t and presses at t.
        """
        frames = []          # (t, x, y, opacity, scale), real time
        ripples = ""
        held = 1
        for t0, x, y, act in pts:
            t = RT(t0)
            if act == "show":
                frames += [(t, x, y, 0, 1.25), (t + .3, x, y, 1, 1)]
            elif act == "move":
                frames.append((t, x, y, 1, held))
            elif act == "down":
                frames += [(t, x, y, 1, 1), (t + .14, x, y, 1, .78)]
                ripples += self.ripple(t, x, y)
                self.cue(t, "click", raw=True)
                held = .78
            elif act == "up":
                frames += [(t, x, y, 1, .78), (t + .14, x, y, 1, 1)]
                held = 1
            elif act == "tap":
                frames += [(t - .2, x, y, 1, 1), (t, x, y, 1, .78), (t + .2, x, y, 1, 1)]
                ripples += self.ripple(t, x, y)
                if sound:
                    self.cue(t, sound, raw=True)
            elif act == "hide":
                frames += [(t, x, y, 1, 1), (t + .35, x, y, 0, .8)]
        frames.sort(key=lambda f: f[0])
        t_start, t_end = frames[0][0], frames[-1][0]
        span = max(.01, t_end - t_start)
        name = self.uid("cur")
        steps = []
        for t, x, y, o, s in frames:
            p = (t - t_start) / span * 100
            steps.append(f"{p:.3f}%{{transform:translate({x}px,{y}px) scale({s});opacity:{o};"
                         f"animation-timing-function:cubic-bezier(.45,0,.25,1)}}")
        self.kf.append(f"@keyframes {name}{{{''.join(steps)}}}")
        return ripples + f'<div class="cur" style="{anims(an(name, t_start, span, "linear", raw=True))}"></div>'

    def touches(self, names, color=None, opacity=.11, seed=3, count=16, size=(70, 120)):
        """Faint topic icons drifting slowly behind everything, kept mostly to the edges."""
        rng = np.random.default_rng(seed)
        color = color or self.fg
        # slots around the edges and in the low band that Instagram's caption covers
        slots = [(70, 300), (980, 360), (60, 640), (1000, 760), (90, 1000), (990, 1120), (70, 1380), (1000, 1480),
                 (200, 1640), (520, 1720), (860, 1660), (330, 180), (760, 150), (60, 1820), (1010, 1860), (540, 1540)]
        out = ""
        for k in range(min(count, len(slots))):
            x, y = slots[k]
            x += int(rng.integers(-25, 26)); y += int(rng.integers(-30, 31))
            s = int(rng.integers(size[0], size[1]))
            ic = ICONS[names[k % len(names)]]
            r0 = int(rng.integers(-18, 19)); r1 = r0 + int(rng.integers(-10, 11))
            dx, dy = int(rng.integers(-16, 17)), int(rng.integers(-22, 23))
            dur = float(rng.uniform(7, 11)); ph = float(rng.uniform(0, dur))
            out += (f'<svg viewBox="0 0 64 64" width="{s}" height="{s}" style="position:absolute;left:{x - s / 2:.0f}px;top:{y - s / 2:.0f}px;'
                    f'opacity:{opacity};--r0:{r0}deg;--r1:{r1}deg;--dx:{dx}px;--dy:{dy}px;'
                    f'animation:drift {dur:.2f}s ease-in-out {-ph:.2f}s infinite" fill="none" stroke="{color}" stroke-width="4.5" '
                    f'stroke-linecap="round" stroke-linejoin="round">{ic}</svg>')
        return f'<div class="bgl">{out}</div>'

    def chrome(self, series, color=None, chip_border=None):
        """Series chip (top right) and the SHWANI logo (top left), on screen the whole reel."""
        color = color or self.fg
        chip = (f'<span style="padding:12px 30px;border-radius:40px;border:3px solid {chip_border or color};font-size:32px;font-weight:600;color:{color}">'
                f'{series}</span>')
        # static: visible from the very first frame, which is also what a viewer sees while scrolling
        return (f'<div style="position:absolute;right:80px;top:212px;z-index:3">{chip}</div>'
                f'<div style="position:absolute;left:80px;top:214px;z-index:3">{lockup_svg(250, color)}</div>')

    # ---------- building blocks shared by the reels ----------
    def txt(self, t, text, top, size, weight=800, kind="up", left=90, width=900, align="center", color=None,
            extra="", cue=None, d=.7, out=None):
        """A centred text block that enters at t. t=None: static, already on screen in the first frame."""
        style = (f"position:absolute;left:{left}px;top:{top}px;width:{width}px;text-align:{align};"
                 f"font-size:{size}px;font-weight:{weight};line-height:1.35;color:{color or self.fg};{extra}")
        if t is None:
            if out is not None:
                style += anims(an("out", out, .4, "ease-in", "forwards"))
            return f'<div style="{style}">{text}</div>'
        return self.el(t, text, kind, d=d, cue=cue, out=out, style=style)

    def think(self, t, secs=1.2, top=1330, ring=TE, card="rgba(32,33,38,.05)", edge="rgba(32,33,38,.14)", track="rgba(32,33,38,.15)",
              beat=.2):
        """'Think a little...' chip with a clock ring: at each beat one segment goes out and one clock tick plays,
        so the ticks you hear are exactly the beats you see (Marwa, 17 Oct).
        Fast by default (Marwa, 28 Oct): a beat every 0.2 s, the same wall-clock sound, just quicker.
        The opening lasts as long as the voice needs to ask the question at ease (load_intro), so a reel
        gives the clock that length: secs = opening - 0.8. The old 3-second clock was think(t, 3, beat=.5)."""
        c = 2 * math.pi * 30
        n = max(3, round(secs / beat))
        seg, gap = c / n, 3.2
        segs = ""
        for k in range(n):
            tk = t + .2 + k * beat
            self.cue(tk, "tick")
            segs += (f'<circle cx="36" cy="36" r="30" fill="none" stroke="{ring}" stroke-width="8" '
                     f'stroke-dasharray="{seg - gap:.2f} {c:.1f}" stroke-dashoffset="{-k * seg:.2f}" '
                     f'style="{anims(an("out", tk, .12, "ease", "forwards"))}"/>')
        svg = (f'<svg viewBox="0 0 72 72" width="64" height="64" style="transform:rotate(-90deg)">'
               f'<circle cx="36" cy="36" r="30" fill="none" stroke="{track}" stroke-width="8"/>{segs}</svg>')
        body = (f'<div style="display:inline-flex;align-items:center;gap:20px;padding:14px 36px 14px 20px;border-radius:50px;'
                f'background:{card};border:3px solid {edge}">{svg}<span style="font-size:42px;font-weight:700">فكّر قليلاً...</span></div>')
        return self.el(t, body, "pop", d=.6, out=t + secs + .25, cue="question",
                       style=f"position:absolute;left:90px;width:900px;top:{top}px;text-align:center")

    def endcard(self, t0, title, items, send, card_bg, card_fg, tick_bg, tick_fg, send_bg, send_fg, logo_color, edge=None):
        """The closing screen: a short checklist worth saving, a 'send it to...' prompt, and the logo."""
        rows = ""
        for k, item in enumerate(items):
            tk = t0 + 1.0 + k * .6
            self.cue(tk + .1, "select")
            tick = (f'<svg viewBox="0 0 48 48" width="56" height="56" style="flex-shrink:0;{anims(an("pop", tk, .5, BOUNCE))}">'
                    f'<circle cx="24" cy="24" r="24" fill="{tick_bg}"/><path d="M14 24.5l6.5 6.5L34 17" fill="none" stroke="{tick_fg}" '
                    f'stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
            rows += (f'<div style="display:flex;align-items:center;gap:24px;padding:20px 0;'
                     f'{"border-top:2px solid " + (edge or "rgba(0,0,0,.08)") + ";" if k else ""}{anims(an("fromR", tk - .1, .5))}">'
                     f'{tick}<span style="font-size:44px;font-weight:700;line-height:1.35">{item}</span></div>')
        card = (f'<div style="border-radius:40px;background:{card_bg};color:{card_fg};padding:40px 48px;'
                f'{"border:3px solid " + edge + ";" if edge else ""}box-shadow:0 26px 60px rgba(0,0,0,.12)">'
                f'<div style="font-size:52px;font-weight:800;margin-bottom:10px">{title}</div>{rows}</div>')
        plane = (f'<svg viewBox="0 0 64 64" width="58" height="58" fill="none" stroke="{send_fg}" stroke-width="5" stroke-linecap="round" '
                 f'stroke-linejoin="round" style="flex-shrink:0;{anims(an("fly", t0 + 3.2, 1.2, "ease-in-out", "none"))}">{ICONS["plane"]}</svg>')
        self.kf.append("@keyframes fly{0%{transform:none}40%{transform:translate(-18px,-14px) rotate(-8deg)}100%{transform:none}}")
        pill = (f'<div style="display:inline-flex;align-items:center;gap:22px;padding:22px 42px;border-radius:60px;'
                f'background:{send_bg};color:{send_fg};font-size:46px;font-weight:800">{plane}{send}</div>')
        self.cue(t0 + 2.6, "pop")
        return (self.el(t0 + .2, card, "up", d=.7, cue="drop", style="position:absolute;left:90px;top:330px;width:900px")
                + self.el(t0 + 2.6, pill, "pop", d=.6, style="position:absolute;left:90px;width:900px;top:1110px;text-align:center")
                + self.el(t0 + 3.4, lockup_svg(330, logo_color), "fade", d=.8,
                          style="position:absolute;left:0;width:1080px;top:1300px;display:flex;justify-content:center"))

    # ---------- pages ----------
    def page(self, body, extra_css=""):
        css = BASE_CSS % {"bg": self.bg, "fg": self.fg, "acc": self.acc}
        return (f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">{fontlinks()}'
                f'<style>{css}{"".join(self.kf)}{extra_css}</style></head>'
                f'<body><div class="r">{body}</div><script>{SEEK_JS}</script></body></html>')

    def still_page(self, body, extra_css=""):
        css = BASE_CSS % {"bg": self.bg, "fg": self.fg, "acc": self.acc}
        return (f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">{fontlinks()}'
                f'<style>{css}{extra_css}</style></head><body><div class="r">{body}</div></body></html>')

    # ---------- sound ----------
    def audio(self, path, seconds, voice=None, sfx_gain=1.0):
        n = int(seconds * SR) + SR
        mix = np.zeros(n)
        rng = np.random.default_rng(7)
        global _ticks
        _ticks = itertools.count()
        last = {}
        for t, kind, params in sorted(self.cues, key=lambda c: c[0]):
            g = "click" if kind in LEAD else kind
            if g in last and t - last[g] < (.25 if g == "click" else .12):   # one tap = one click, not two
                continue
            s = SFX[kind](rng, **params)
            if s is None:
                continue
            last[g] = t
            i = max(0, int((t - LEAD.get(kind, 0)) * SR))
            if i >= n:
                continue
            j = min(n, i + len(s))
            # clock ticks stay audible under the voice: every beat on screen must be heard (Marwa, 17 Oct)
            mix[i:j] += s[:j - i] * (max(sfx_gain, .75) if kind == "tick" else sfx_gain)
        if voice:
            for t, vpath in voice:
                v = _load_any(vpath)
                i = int(t * SR); j = min(n, i + len(v))
                mix[i:j] += v[:j - i]
        if voice:                # a clock tick landing on a loud syllable must not poke above the calm level
            mix = _limit(mix, VO_CEIL)
        peak = np.max(np.abs(mix)) or 1
        if peak > .9:            # only ever turned down, never boosted
            mix = mix / peak * .9
        data = (np.clip(mix[:int(seconds * SR)], -1, 1) * 32767).astype(np.int16)
        with wave.open(path, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes(data.tobytes())

    # ---------- render ----------
    def render(self, outdir, html, seconds, cover_html=None, name="reel", stills=None, voice=None):
        """Renders the frames once to <name>-silent.mp4, then mixes the sound onto it:
        <name>.mp4 with the effects only, and, when `voice` is given ([(seconds, wav), ...]),
        <name>-vo.mp4 with the narration on top and the effects lowered.
        REMIX_ONLY=1 skips the frames and remixes the sound onto the existing silent video.
        """
        os.makedirs(outdir, exist_ok=True)
        src = os.path.join(outdir, f"{name}.html")
        open(src, "w", encoding="utf-8").write(html)
        if os.environ.get("STILLS_ONLY"):
            asyncio.run(_stills(src, stills or [0], os.path.join(outdir, "contact.png")))
            return
        silent = os.path.join(outdir, f"{name}-silent.mp4")
        if not (os.environ.get("REMIX_ONLY") and os.path.exists(silent)):
            asyncio.run(_video(src, seconds, silent, stills, os.path.join(outdir, "contact.png")))
        versions = [(name, None, 1.0)] + ([(f"{name}-vo", voice, .4)] if voice else [])
        for out, vo, gain in versions:
            wav = os.path.join(outdir, f"{out}.wav")
            self.audio(wav, seconds, vo, gain)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-c:v", "copy",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                            os.path.join(outdir, f"{out}.mp4")], check=True)
            os.remove(wav)
        if cover_html:
            csrc = os.path.join(outdir, "cover.html")
            open(csrc, "w", encoding="utf-8").write(cover_html)
            asyncio.run(_still(csrc, os.path.join(outdir, "cover.png")))
        print("rendered", name, f"{seconds:.1f}s", "+ voice-over" if voice else "")


async def _open(p):
    b = await p.chromium.launch()
    pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    return b, pg


async def _still(src, out):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b, pg = await _open(p)
        await pg.goto("file://" + src)
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=out, clip={"x": 0, "y": 0, "width": W, "height": H})
        await b.close()


def _sheet(shots, contact):
    from PIL import Image
    cols = min(6, len(shots)); rows = (len(shots) + cols - 1) // cols
    tw, th = 360, 640
    sheet = Image.new("RGB", (cols * tw + (cols - 1) * 16, rows * th + (rows - 1) * 16), "#888")
    for k, (t, im) in enumerate(shots):
        r, c = divmod(k, cols)
        sheet.paste(im.resize((tw, th)), (c * (tw + 16), r * (th + 16)))
    sheet.save(contact)


async def _stills(src, times, contact):
    from playwright.async_api import async_playwright
    from PIL import Image
    import io
    shots = []
    async with async_playwright() as p:
        b, pg = await _open(p)
        await pg.goto("file://" + src)
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(400)
        for t in times:
            await pg.evaluate(f"window.__seek({t * 1000:.3f})")
            buf = await pg.screenshot(type="png", clip={"x": 0, "y": 0, "width": W, "height": H})
            shots.append((t, Image.open(io.BytesIO(buf)).convert("RGB")))
        await b.close()
    _sheet(shots, contact)


async def _video(src, seconds, mp4, stills, contact):
    from playwright.async_api import async_playwright
    from PIL import Image
    import io
    n = int(round(seconds * FPS))
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
         "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), mp4],
        stdin=subprocess.PIPE)
    want = sorted(stills or [])
    shots = []
    async with async_playwright() as p:
        b, pg = await _open(p)
        await pg.goto("file://" + src)
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(400)
        for i in range(n):
            t = i / FPS
            await pg.evaluate(f"window.__seek({t * 1000:.3f})")
            buf = await pg.screenshot(type="jpeg", quality=94, clip={"x": 0, "y": 0, "width": W, "height": H})
            ff.stdin.write(buf)
            while want and want[0] <= t + 1e-6:
                shots.append((want.pop(0), Image.open(io.BytesIO(buf)).convert("RGB")))
        await b.close()
    ff.stdin.close()
    ff.wait()
    if shots:
        _sheet(shots, contact)


# ---------- sound effects from recorded samples ----------
@functools.lru_cache(maxsize=None)
def _load(name):
    with wave.open(os.path.join(SFX_DIR, name + ".wav"), "rb") as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
    return x


def _load_any(path):
    """Any audio file -> mono float array at SR (through ffmpeg)."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32768


def _pitch(x, f):
    """Resample to shift pitch (and length) by factor f."""
    if abs(f - 1) < 1e-3:
        return x
    idx = np.arange(0, len(x) - 1, f)
    return np.interp(idx, np.arange(len(x)), x)


def _pick(rng, base, k, gain, spread=.04):
    name = f"{base}_{int(rng.integers(1, k + 1)):03d}"
    if not os.path.exists(os.path.join(SFX_DIR, name + ".wav")):
        name = f"{base}_001"
    return _pitch(_load(name), float(rng.uniform(1 - spread, 1 + spread))) * gain


def _cat(*parts):
    """parts: (offset_seconds, array) -> one array."""
    end = max(int(o * SR) + len(a) for o, a in parts)
    out = np.zeros(end)
    for o, a in parts:
        i = int(o * SR); out[i:i + len(a)] += a
    return out


VO_CEIL = 10 ** (-10 / 20)      # voice-over versions peak at about -10 dBFS (Marwa, 16 Oct)


def _limit(x, ceil, block=.001, look=.005, release=.08):
    """Gentle peak limiter: turns down only the few milliseconds that would pass `ceil`."""
    b = max(1, int(block * SR))
    n = (len(x) + b - 1) // b
    pk = np.abs(np.pad(x, (0, n * b - len(x)))).reshape(n, b).max(axis=1)
    g = np.minimum(1.0, ceil / np.maximum(pk, 1e-9))
    k = int(look / block)
    g = np.min(np.stack([np.roll(g, s) for s in range(-k, k + 1)]), axis=0)   # attack ahead of each peak
    a = np.exp(-block / release)
    for i in range(1, n):                                                     # slow release afterwards
        g[i] = min(g[i], a * g[i - 1] + (1 - a))
    return x * np.repeat(g, b)[:len(x)]


@functools.lru_cache(maxsize=None)
def _norm(name):
    """A sample scaled so its loudest point is 1.0: the gains below are then real peak levels."""
    x = _load(name)
    return x / (np.max(np.abs(x)) or 1)


# Marwa, 16 Oct: only familiar, gentle sounds, all real recordings.
# A real mouse click for every tap, a wall clock for every timer, real keyboard keys for typing,
# paper on a table for cards, a soft whoosh between scenes. Text appearing on screen makes no sound.
CLICK_LEAD = .095        # mouse_click.wav = press, then the louder release ~95 ms later: it lands on the tap
G_CLICK, G_CLOCK, G_KEY, G_PAPER, G_SLIDE, G_WHOOSH, G_PENCIL = .34, .30, .17, .16, .13, .12, .10


def _click(rng, gain=G_CLICK, **_):
    return _pitch(_norm("mouse_click"), float(rng.uniform(.985, 1.015))) * gain


_ticks = itertools.count()


def _clock(rng, **_):
    """Wall-clock tick: the four recorded ticks in turn, so it sounds like tick, tock, tick, tock."""
    return _norm(f"clock_{next(_ticks) % 4 + 1}") * G_CLOCK


def _key(rng, gain=G_KEY):
    k = f"key{int(rng.integers(1, 6))}"
    return _cat((0, _pitch(_norm(k), float(rng.uniform(.97, 1.03))) * gain),
                (float(rng.uniform(.05, .08)), _norm("key_up") * gain * .4))


def _type(rng, n=8, d=1.0, **_):
    n = max(2, int(n))
    parts, t = [], 0.0
    step = d / n
    for k in range(n):
        if rng.random() < .1:
            parts.append((t, _norm("key_space") * G_KEY * .8))
        else:
            parts.append((t, _key(rng)))
        t += step * float(rng.uniform(.75, 1.25))
    return _cat(*parts)


def _paper(rng, kind="place", gain=G_PAPER, **_):
    n = int(rng.integers(1, 5))
    return _norm(f"paper_{kind}_{n}") * gain


def _whoosh(rng, gain=G_WHOOSH, **_):
    return _pitch(_norm("whoosh_soft"), float(rng.uniform(.97, 1.03))) * gain


def _scribble(rng, d=1.0, **_):
    """Pencil on paper for d seconds: overlapping scratch samples, quiet."""
    parts, t = [], 0.0
    while t < d:
        parts.append((t, _pitch(_norm(f"scratch_{int(rng.integers(1, 6)):03d}"), float(rng.uniform(.95, 1.05))) * G_PENCIL))
        t += float(rng.uniform(.12, .2))
    return _cat(*parts)


def _silent(rng, **_):
    return None


SFX = {
    # taps and choices: a real mouse click
    "click": _click, "tap": _click, "select": _click, "toggle": _click,
    # typing: real keyboard keys
    "type": _type,
    "key": lambda rng, **_: _key(rng),
    "enter": lambda rng, **_: _norm("key_enter") * G_KEY * 1.2,
    # timers and the «فكّر قليلاً» pause: a wall clock
    "tick": _clock,
    # cards and pages: paper on a table
    "drop": _paper,
    "swipe": lambda rng, **_: _paper(rng, "slide", G_SLIDE),
    "min": lambda rng, **_: _paper(rng, "slide", G_SLIDE * .8),
    "max": lambda rng, **_: _paper(rng, "slide", G_SLIDE * .8),
    # between scenes
    "whoosh": _whoosh,
    # finger drawing
    "scribble": _scribble,
    # no sound for text appearing, chimes or bells
    "pop": _silent, "ding": _silent, "confirm": _silent, "question": _silent,
    "open": _silent, "close": _silent, "error": _silent, "bong": _silent,
}
LEAD = {"click": CLICK_LEAD, "tap": CLICK_LEAD, "select": CLICK_LEAD, "toggle": CLICK_LEAD}
