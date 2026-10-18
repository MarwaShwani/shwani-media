"""Post 08: reel «قبل وبعد» الحلقة 1 — أيّ مدرسة تثق بها لطفلك؟ (short, simple version)

Row 3: teal base, milky text. Accents terracotta, dusty pink and sage (no mustard in this row).
1080x1920, ~41s. No prices. The school and its name are invented, and the reel says so on screen.
Marwa, 16 Oct 2026: the long version was not understood by everyone. This one asks a plain question with two
school signs, then reveals it is the same school: only the logo changed. Three changes, a drag to compare,
and a checklist to save. The question is on screen from the first frame.
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from reel import *  # noqa: F401,F403

ROW_BG, ROW_FG = TL, CH
R = Reel(bg=ROW_BG, fg=ROW_FG, acc=TE)
PAPER = "#FBF7EF"
EDGE = "rgba(242,233,216,.28)"
NAVY = "#23395B"            # the invented school's colour
# b-roll made with Veo in Marwa's Gemini (AI-made: tick Instagram's "AI info" label when posting)
BROLL_OPTS = {}
BROLL = broll(HERE, "broll.mp4", 900, 560, **BROLL_OPTS) if os.path.exists(os.path.join(HERE, "broll.mp4")) else None
OFF = 1.0 if BROLL else 0.0      # scene 1 is a second longer with the opening footage
(T1, T2, T3, T4), DUR = timeline([13.5 + OFF, 14.0, 6.8, 7.0])
VO = load_vo(HERE)          # voice-over timing from vo.json (made by vo.py); None = effects only
if VO:
    DUR = VO["dur"]
ICON_SET = ["book", "pencil", "ruler", "star", "cap", "plane", "abc", "bag"]


# ---------------- the school logo in six states ----------------
def lantern(size, stroke=NAVY, flame=TE, base=NAVY, sw=14, glow=False):
    g = (f'<defs><radialGradient id="gl"><stop offset="0" stop-color="#FFF59D"/><stop offset="1" stop-color="#FF9800"/></radialGradient></defs>'
         if glow else "")
    fl = "url(#gl)" if glow else flame
    return (f'<svg viewBox="0 0 200 220" width="{size}" height="{size * 1.1:.0f}" style="display:block;overflow:visible">{g}'
            f'<circle cx="100" cy="24" r="11" fill="none" stroke="{stroke}" stroke-width="{sw * .7:.0f}"/>'
            f'<path d="M62 168 V98 Q62 46 100 46 Q138 46 138 98 V168" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M100 82 C122 108 122 132 100 146 C78 132 78 108 100 82 Z" fill="{fl}"/>'
            f'<path d="M34 172 Q67 156 100 172 Q133 156 166 172 V196 Q133 180 100 198 Q67 180 34 196 Z" fill="{base}"/></svg>')


SHIELD = "M150 20 H270 Q280 20 280 30 V170 Q280 280 150 340 Q20 280 20 170 V30 Q20 20 30 20 Z"


def crest(state):
    """state 0: five icons, seven colours, gradients. 1: one lantern. 2: two colours. 3: shorter name."""
    loud = state < 2
    defs = ('<defs><linearGradient id="sh" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1E88E5"/>'
            '<stop offset="1" stop-color="#8E24AA"/></linearGradient></defs>') if loud else ""
    fill = "url(#sh)" if loud else NAVY
    edge = "#FBC02D" if loud else TE
    leaf_c = "#43A047" if loud else NAVY
    rib = "#E53935" if loud else TE
    leaves = ""
    for a0, a1 in ((105, 205), (75, -25)):        # left branch, right branch (degrees, y down)
        for k in range(8):
            a = math.radians(a0 + (a1 - a0) * k / 7)
            cx, cy = 150 + 168 * math.cos(a), 175 + 168 * math.sin(a)
            rot = math.degrees(a) + 90
            for side in (-1, 1):
                ox, oy = 14 * math.cos(a) * side, 14 * math.sin(a) * side
                leaves += (f'<ellipse cx="{cx + ox:.0f}" cy="{cy + oy:.0f}" rx="9" ry="20" fill="{leaf_c}" '
                           f'transform="rotate({rot + 35 * side:.0f} {cx + ox:.0f} {cy + oy:.0f})"/>')
    stars = "".join(f'<text x="{x}" y="14" font-size="30" fill="{"#FBC02D" if loud else NAVY}" text-anchor="middle">★</text>' for x in (110, 150, 190))
    if state == 0:
        icons = ('<rect x="70" y="70" width="70" height="52" rx="4" fill="#fff"/><rect x="146" y="70" width="70" height="52" rx="4" fill="#fff"/>'
                 '<path d="M215 140 V210" stroke="#8D6E63" stroke-width="12" stroke-linecap="round"/>'
                 '<path d="M215 118 C232 132 230 146 215 150 C200 146 198 132 215 118Z" fill="#FF7043"/>'
                 '<circle cx="95" cy="175" r="34" fill="#29B6F6"/><path d="M78 160 q14 10 8 24 q16 6 26 -6 M95 141 V209 M61 175 H129" stroke="#66BB6A" stroke-width="6" fill="none"/>'
                 '<circle cx="150" cy="250" r="30" fill="#8D6E63"/><circle cx="138" cy="244" r="9" fill="#FFF"/><circle cx="162" cy="244" r="9" fill="#FFF"/>'
                 '<circle cx="138" cy="244" r="4" fill="#212121"/><circle cx="162" cy="244" r="4" fill="#212121"/>'
                 '<path d="M190 280 C220 250 236 220 238 182" stroke="#AB47BC" stroke-width="9" fill="none" stroke-linecap="round"/>')
    else:
        icons = (f'<g transform="translate(78 64) scale(.72)">'
                 f'{lantern(200, "#fff", "#FF9800" if state == 1 else TE, "#fff", glow=(state == 1))[len("<svg "):].split(">", 1)[1].rsplit("</svg>", 1)[0]}</g>')
    ring = ('<path id="rg" d="M10 130 A140 140 0 0 1 290 130" fill="none"/><text font-family="Alexandria" font-size="17" font-weight="300" '
            f'fill="{"#7B1FA2" if loud else NAVY}" letter-spacing="3"><textPath href="#rg" startOffset="50%" text-anchor="middle">'
            'QANDEEL PRIVATE SCHOOLS • EST. 2026</textPath></text>') if state < 3 else ""
    ribbon_text = (f'<text x="150" y="338" font-family="Alexandria" font-size="26" font-weight="200" fill="#fff" text-anchor="middle">مدارس قنديل</text>'
                   if state < 3 else "")
    svg = (f'<svg viewBox="-40 -30 380 400" width="330" height="347" style="display:block;overflow:visible">{defs}'
           f'<g opacity="1">{leaves}</g>{ring}'
           f'<g transform="translate(0 0)">{stars}</g>'
           f'<path d="{SHIELD}" fill="{fill}" stroke="{edge}" stroke-width="8"/>'
           f'<path d="{SHIELD}" fill="none" stroke="#fff" stroke-width="2" transform="translate(15 16) scale(.9)" opacity=".7"/>'
           f'{icons}'
           f'<path d="M30 305 L270 305 L285 330 L270 355 L30 355 L15 330 Z" fill="{rib}"/>{ribbon_text}</svg>')
    if state < 3:
        grad = ("background:linear-gradient(90deg,#E53935,#FB8C00,#43A047,#1E88E5,#8E24AA);-webkit-background-clip:text;background-clip:text;color:transparent"
                if loud else f"color:{NAVY}")
        name = (f'<div style="font-size:30px;font-weight:200;{grad};text-align:center;line-height:1.4;max-width:760px">'
                f'مدارس قنديل الأهلية النموذجية للتعليم الأساسي والثانوي</div>')
    else:
        name = f'<div style="font-size:58px;font-weight:800;color:{NAVY};line-height:1.3">مدارس قنديل الأهلية</div>'
    return (f'<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px">'
            f'{svg}{name}</div>')


def clean(scale=1.0):
    return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:{8 * scale:.0f}px">{lantern(int(190 * scale))}'
            f'<div style="font-size:{int(84 * scale)}px;font-weight:800;color:{NAVY};line-height:1.2">مدارس قنديل</div>'
            f'<div style="display:flex;align-items:center;gap:{14 * scale:.0f}px;color:{NAVY}">'
            f'<span style="font-size:{int(34 * scale)}px;font-weight:600">الأهلية</span>'
            f'<span style="width:6px;height:6px;border-radius:3px;background:{TE}"></span>'
            f'<span class="ltr" style="font-size:{int(24 * scale)}px;font-weight:600;letter-spacing:4px">QANDEEL SCHOOLS</span></div></div>')




def logo(state):
    if state <= 3:
        return crest(state)
    return f'<div style="position:absolute;inset:0;display:grid;place-items:center">{clean()}</div>'


def artboard(html):
    return (f'<div style="position:absolute;inset:0;border-radius:34px;background:{PAPER};overflow:hidden;'
            f'box-shadow:0 30px 70px rgba(0,0,0,.2)">{html}</div>')


def mini_board(state, w=420, h=330):
    """The 900x640 artboard shrunk into a small sign card."""
    k = min(w / 900, h / 640)
    return (f'<div style="position:absolute;inset:0;border-radius:30px;background:{PAPER};overflow:hidden;box-shadow:0 24px 50px rgba(0,0,0,.2)">'
            f'<div style="position:absolute;left:{(w - 900 * k) / 2:.0f}px;top:{(h - 640 * k) / 2:.0f}px;width:900px;height:640px;'
            f'transform:scale({k:.4f});transform-origin:top left">{logo(state)}</div></div>')


# ---------------- scene 1: the question, then the twist ----------------
def scene1():
    # with b-roll: a real school morning plays under the question for the first 2 seconds, then the two signs come in
    cin = 1.7 if BROLL else 0.0          # when the cards come in, minus .3
    tap, twist = 5.4 + OFF, 8.4 + OFF
    film = ""
    if BROLL:
        R.kf.append("@keyframes filmOut{from{opacity:1;transform:none}to{opacity:0;transform:scale(.92)}}")
        film = (f'<div style="position:absolute;left:90px;top:600px;width:900px;height:560px;border-radius:36px;overflow:hidden;'
                f'box-shadow:0 30px 70px rgba(0,0,0,.25);{anims(an("filmOut", 1.75, .4, EASE, "forwards"))}">{R.clip(0, BROLL)}</div>')
        R.cue(1.75, "whoosh")
    ring =f'<div style="position:absolute;inset:-14px;border-radius:40px;border:7px solid {TE};{anims(an("fade", tap, .3))}"></div>'
    ok = (f'<svg viewBox="0 0 64 64" width="76" height="76" style="position:absolute;left:-20px;top:-20px;{anims(an("pop", tap + .05, .45, BOUNCE))}">'
          f'<circle cx="32" cy="32" r="32" fill="{TE}"/><path d="M19 33l9 9 17-19" fill="none" stroke="{DK}" stroke-width="6" '
          f'stroke-linecap="round" stroke-linejoin="round"/></svg>')
    before = R.el(cin + .3, f'<div style="position:absolute;inset:0;{anims(an("dim", tap + .15, .4, "ease", "forwards"), an("undim", twist + .3, .5, "ease", "forwards"))}">{mini_board(0)}</div>',
                  "fromR", cue="pop", style="position:absolute;left:570px;top:640px;width:420px;height:330px")
    after = R.el(cin + .45, R.pressed(tap, mini_board(4) + ring, "position:absolute;inset:0") + ok,
                 "fromL", cue="pop", style="position:absolute;left:90px;top:640px;width:420px;height:330px")
    equal = (f'<div style="width:96px;height:96px;border-radius:48px;background:{CH};color:{TL};display:flex;align-items:center;'
             f'justify-content:center;font-size:70px;font-weight:800;box-shadow:0 12px 26px rgba(0,0,0,.25)">=</div>')
    R.cue(tap + .05, "select")
    body = (
        R.txt(None, "أيّ مدرسة تثق بها", 320, 96, out=twist - .2)
        + R.txt(None, "لطفلك؟", 440, 96, color=TE, out=twist - .2)
        + film + before + after
        + R.think(1.4 + OFF, 3, top=1050, card="rgba(242,233,216,.1)", edge=EDGE, track="rgba(242,233,216,.25)")
        + R.cursor([(4.6 + OFF, 760, 1500, "show"), (tap, 300, 805, "tap"), (tap + .8, 420, 1400, "hide")])
        + R.txt(tap + .6, "اخترتها في ثانية، صحيح؟", 1050, 62, kind="pop", cue="ding", out=twist + .6)
        + R.txt(twist, "المدرسة نفسها!", 380, 100, color=TE, kind="pop", cue="pop", extra="white-space:nowrap")
        + R.el(twist + .4, equal, "pop", d=.5, cue="pop", style="position:absolute;left:492px;top:757px;z-index:5")
        + R.txt(twist + 1.0, "الفرق في الشعار فقط.", 1050, 70, kind="pop")
        + R.txt(twist + 2.2, f'<span style="display:inline-block;padding:14px 34px;border-radius:40px;border:3px solid {EDGE};font-size:36px;font-weight:500">'
                             f'مثال توضيحي: مدرسة من الخيال</span>', 1200, 36, weight=500, kind="fade")
    )
    return R.scene(T1, T2, body, cue=None, leave="sOutUp")


# ---------------- scene 2: three changes ----------------
STEPS = [("رمز واحد", "قنديل واحد بدل خمسة رموز."), ("لونان فقط", "كحلي وبرتقالي بدل سبعة ألوان."), ("اسم واضح", "اسم قصير يُقرأ من بعيد.")]
STATE_SEQ = [0, 1, 2, 4]


def scene2():
    t0 = T2
    taps = [t0 + 1.9, t0 + 5.5, t0 + 9.1]
    states = ""
    for k, s in enumerate(STATE_SEQ):
        t_in = t0 + .4 if k == 0 else taps[k - 1] + .1
        t_out = taps[k] + .1 if k < 3 else None
        a = [an("fade" if k == 0 else "pop", t_in, .45 if k else .4, BOUNCE if k else EASE)]
        if t_out is not None:
            a.append(an("out", t_out, .15, "ease", "forwards"))
        states += f'<div style="position:absolute;inset:0;{anims(*a)}">{logo(s)}</div>'
    tag_b = (f'<span style="position:absolute;right:24px;top:22px;padding:8px 24px;border-radius:24px;background:{RO};color:{DK};font-size:32px;'
             f'font-weight:800;{anims(an("out", taps[0], .25, "ease", "forwards"))}">قبل</span>')
    tag_a = (f'<span style="position:absolute;right:24px;top:22px;padding:8px 24px;border-radius:24px;background:{TE};color:{DK};font-size:32px;'
             f'font-weight:800;{anims(an("pop", taps[2] + .3, .5, BOUNCE))}">بعد</span>')
    board = R.el(t0 + .3, artboard(states + tag_b + tag_a), "up", d=.7, cue="drop",
                 style="position:absolute;left:90px;top:400px;width:900px;height:640px")
    pills = ""
    xs = [840, 540, 240]
    for k, ((name, _), x) in enumerate(zip(STEPS, xs)):
        on = taps[k]
        inner = (f'<div style="position:absolute;inset:0;border-radius:50px;border:3px solid {EDGE};background:rgba(242,233,216,.08)"></div>'
                 f'<div style="position:absolute;inset:0;border-radius:50px;background:{TE};{anims(an("fade", on, .25))}"></div>'
                 f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:12px;font-size:38px;font-weight:700">'
                 f'<span class="ltr" style="opacity:.6">{k + 1}</span>{name}</div>'
                 f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:12px;font-size:38px;font-weight:700;color:{DK};{anims(an("fade", on, .25))}">'
                 f'<span class="ltr" style="opacity:.6">{k + 1}</span>{name}</div>')
        pills += R.el(t0 + .9 + k * .1, R.pressed(on, inner, "position:absolute;inset:0"), "up", d=.55,
                      style=f"position:absolute;left:{x - 140}px;top:1080px;width:280px;height:100px")
        R.cue(on + .12, "pop")
    caps = ""
    for k, (_, cap) in enumerate(STEPS):
        a = [an("up", taps[k] + .2, .5)] + ([an("out", taps[k + 1], .2, "ease", "forwards")] if k < 2 else [])
        caps += (f'<div style="position:absolute;left:90px;width:900px;top:1230px;text-align:center;font-size:50px;font-weight:600;'
                 f'line-height:1.45;{anims(*a)}">{cap}</div>')
    body = (
        R.txt(t0 + .1, "3 تغييرات صنعت الفرق", 285, 68, kind="pop", cue="pop")
        + board + pills + caps
        + R.cursor([(t0 + 1.2, 700, 1580, "show")] + [(t, x, 1130, "tap") for t, x in zip(taps, xs)]
                   + [(taps[2] + .8, 520, 1580, "hide")])
    )
    return R.scene(t0, T3, body, leave="sOutUp")


# ---------------- scene 3: drag to compare ----------------
def scene3():
    t0 = T3
    L, T, Wd, Ht = 90, 420, 900, 760
    d0, d1, d2, d3 = t0 + 1.3, t0 + 2.5, t0 + 3.9, t0 + 4.7
    xs = [(d0, 450), (d1, 70), (d2, 830), (d3, 450)]
    span = d3 + .14 - d0

    def pct(t):
        return (t - d0) / span * 100
    hk = "".join(f"{pct(t):.2f}%{{transform:translateX({x - 450}px);animation-timing-function:cubic-bezier(.45,0,.25,1)}}" for t, x in xs)
    ck = "".join(f"{pct(t):.2f}%{{clip-path:inset(0 0 0 {x}px);animation-timing-function:cubic-bezier(.45,0,.25,1)}}" for t, x in xs)
    R.kf.append(f"@keyframes hnd{{{hk}100%{{transform:none}}}}@keyframes clp{{{ck}100%{{clip-path:inset(0 0 0 450px)}}}}")
    before = f'<div style="position:absolute;inset:0;background:{PAPER}">{logo(0)}</div>'
    after = (f'<div style="position:absolute;inset:0;background:{PAPER};clip-path:inset(0 0 0 450px);'
             f'{anims(an("clp", d0, span, "linear", "forwards"))}"><div style="position:absolute;inset:0;display:grid;place-items:center">{clean()}</div></div>')
    handle = (f'<div style="position:absolute;left:446px;top:0;bottom:0;width:8px;background:{DK};{anims(an("hnd", d0, span, "linear", "forwards"))}">'
              f'<div style="position:absolute;left:-36px;top:340px;width:80px;height:80px;border-radius:40px;background:{DK};display:flex;'
              f'align-items:center;justify-content:center"><svg viewBox="0 0 48 24" width="44" height="22"><path d="M14 4L4 12l10 8M34 4l10 8-10 8" '
              f'fill="none" stroke="{CH}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>')
    labels = (f'<span style="position:absolute;left:24px;top:22px;padding:8px 24px;border-radius:24px;background:{RO};color:{DK};font-size:32px;font-weight:800">قبل</span>'
              f'<span style="position:absolute;right:24px;top:22px;padding:8px 24px;border-radius:24px;background:{TE};color:{DK};font-size:32px;font-weight:800">بعد</span>')
    board = (f'<div style="position:absolute;inset:0;border-radius:34px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.2)">'
             f'{before}{after}{handle}{labels}</div>')
    hy = T + 380
    R.cue(d1 - .5, "swipe"); R.cue(d2 - .7, "swipe")
    body = (
        R.txt(t0 + .1, "اسحب لترى الفرق", 285, 68, kind="pop", cue="pop")
        + R.el(t0 + .3, board, "up", d=.7, style=f"position:absolute;left:{L}px;top:{T}px;width:{Wd}px;height:{Ht}px")
        + R.cursor([(t0 + .8, 760, 1520, "show"), (d0, L + 450, hy, "down"), (d1, L + 70, hy, "move"), (d2, L + 830, hy, "move"),
                    (d3, L + 450, hy, "move"), (d3 + .05, L + 450, hy, "up"), (d3 + .5, 700, 1420, "hide")])
        + R.txt(d3 + .3, "أيّهما أجمل؟ اكتب «قبل» أو «بعد».", 1240, 52, weight=700, cue="ding")
    )
    return R.scene(t0, T4, body, leave="sOutUp")


# ---------------- scene 4: checklist to save, and send ----------------
def scene4():
    t0 = T4
    return R.scene(t0, None,
                   R.endcard(t0, "شعار يثق به الأهل:", ["رمز واحد", "لونان فقط", "اسم واضح يُقرأ من بعيد"], "أرسله لصاحب مدرسة أو مشروع",
                             card_bg=PAPER, card_fg=DK, tick_bg=TE, tick_fg=DK, send_bg=RO, send_fg=DK, logo_color=CH)
                   + R.txt(t0 + 2.2, "احفظه قبل أن تطلب شعارك.", 900, 44, weight=600, kind="fade"))


def cover():
    half_b = f'<div style="position:absolute;inset:0;background:{PAPER}">{logo(0)}</div>'
    half_a = (f'<div style="position:absolute;inset:0;background:{PAPER};clip-path:inset(0 0 0 450px)">'
              f'<div style="position:absolute;inset:0;display:grid;place-items:center">{clean()}</div></div>')
    line = f'<div style="position:absolute;left:446px;top:0;bottom:0;width:8px;background:{DK}"></div>'
    labels = (f'<span style="position:absolute;left:24px;top:22px;padding:8px 24px;border-radius:24px;background:{RO};color:{DK};font-size:32px;font-weight:800">قبل</span>'
              f'<span style="position:absolute;right:24px;top:22px;padding:8px 24px;border-radius:24px;background:{TE};color:{DK};font-size:32px;font-weight:800">بعد</span>')
    board = (f'<div class="ab" style="left:90px;top:420px;width:900px;height:640px;border-radius:34px;overflow:hidden;'
             f'box-shadow:0 30px 70px rgba(0,0,0,.2)">{half_b}{half_a}{line}{labels}</div>')
    chip = (f'<span style="padding:14px 34px;border-radius:44px;border:3px solid {CH};font-size:34px;font-weight:600">'
            f'قبل وبعد · الحلقة 1</span>')
    body = (
        R.touches(ICON_SET, opacity=.1, seed=11)
        + f'<div class="ab" style="right:90px;top:310px">{chip}</div>'
        + board
        + f'<div class="ab" style="right:90px;left:90px;top:1110px;font-size:100px;font-weight:800;line-height:1.22">المدرسة نفسها،<br>والفرق في الشعار</div>'
        + f'<div class="ab" style="right:90px;left:90px;top:1380px;font-size:42px;font-weight:600;line-height:1.6">مثال توضيحي لمدرسة من الخيال</div>'
        + f'<div class="ab" style="left:90px;top:1510px">{lockup_svg(300, CH)}</div>'
    )
    return R.still_page(body)


def build():
    body = (R.touches(ICON_SET, opacity=.12, seed=11) + R.chrome("قبل وبعد · الحلقة 1")
            + scene1() + scene2() + scene3() + scene4())
    return R.page(body, "@keyframes undim{from{opacity:.3}to{opacity:1}}")


if __name__ == "__main__":
    html = build()
    stills = [0.0, 1.0, 4.0, 6.8, 9.6, 12.5, 15.0, 18.5, 22.0, 26.0, 30.5, 40.5]
    if "--stills" in sys.argv:
        stills = [float(s) for s in sys.argv[sys.argv.index("--stills") + 1].split(",")]
    R.render(HERE, html, DUR, cover_html=cover(), stills=[RT(x) for x in stills], voice=VO["voice"] if VO else None)
