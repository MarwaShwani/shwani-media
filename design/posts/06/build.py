"""Post 06: reel «من الفكرة إلى الشعار» الحلقة 1 — أيّ شعار تتذكّر؟ (short, simple version)

Row 2 (milky). 1080x1920, ~38.5s. No prices, no studies on screen.
Marwa, 16 Oct 2026: the long version was not understood by everyone. This one is a memory game that
shows the idea instead of explaining it: two logos for three seconds, they flip over, which one do you
remember? The simple one. Then three easy tests for your own logo, and the ending she liked:
«وشعارك أنت؟». The question is on screen from the first frame. Both logos are invented.
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from reel import *  # noqa: F401,F403

R = Reel(bg=CH, fg=DK, acc=TE)
PAPER = "#FBF7EF"
SOFT = "rgba(32,33,38,.14)"
(T1, T2, T3, T4), DUR = timeline([10.5, 15.0, 6.0, 7.0])
VO = load_vo(HERE)          # voice-over timing from vo.json (made by vo.py); None = effects only
if VO:
    DUR = VO["dur"]
ICON_SET = ["pencil", "bezier", "circle", "tri", "square", "drop", "eraser", "pen"]
# b-roll made with Veo in Marwa's Gemini (AI-made: tick Instagram's "AI info" label when posting)
BROLL_OPTS = dict(start=1.0, speed=1.45)     # skip the blank first second; the circle and the leaf are both drawn before the scene ends
BROLL = broll(HERE, "broll.mp4", 900, 600, **BROLL_OPTS) if os.path.exists(os.path.join(HERE, "broll.mp4")) else None


def ring_mark(size, c1=TE, c2=RO, sw=16):
    return (f'<svg viewBox="0 0 220 160" width="{size}" height="{size * 160 / 220:.0f}" style="display:block">'
            f'<circle cx="80" cy="80" r="55" fill="none" stroke="{c1}" stroke-width="{sw}"/>'
            f'<circle cx="140" cy="80" r="55" fill="none" stroke="{c2}" stroke-width="{sw}"/></svg>')


def busy_emblem(size, color=DK):
    rays = "".join(
        f'<line x1="{100+62*math.cos(a):.1f}" y1="{100+62*math.sin(a):.1f}" x2="{100+70*math.cos(a):.1f}" y2="{100+70*math.sin(a):.1f}"/>'
        for a in (k * math.pi / 18 for k in range(36)))
    star = " ".join(f"{100+(34 if k % 2 == 0 else 15)*math.cos(-math.pi/2 + k*math.pi/6):.1f},"
                    f"{100+(34 if k % 2 == 0 else 15)*math.sin(-math.pi/2 + k*math.pi/6):.1f}" for k in range(12))
    leaves = "".join(
        f'<ellipse cx="{100+48*math.cos(a):.1f}" cy="{100+48*math.sin(a):.1f}" rx="7" ry="3" '
        f'transform="rotate({math.degrees(a)+90:.0f} {100+48*math.cos(a):.1f} {100+48*math.sin(a):.1f})"/>'
        for a in (k * math.pi / 8 for k in range(16)))
    return (f'<svg viewBox="0 0 200 200" width="{size}" height="{size}" style="display:block">'
            f'<defs><path id="arc" d="M100,100 m-82,0 a82,82 0 1,1 164,0 a82,82 0 1,1 -164,0"/></defs>'
            f'<g fill="none" stroke="{color}"><circle cx="100" cy="100" r="96" stroke-width="3"/><circle cx="100" cy="100" r="90" stroke-width="1"/>'
            f'<circle cx="100" cy="100" r="74" stroke-width="1"/><circle cx="100" cy="100" r="58" stroke-width="1.5"/>'
            f'<g stroke-width="1">{rays}</g><circle cx="100" cy="100" r="40" stroke-width="1"/></g>'
            f'<g fill="{color}">{leaves}<polygon points="{star}"/></g>'
            f'<text font-family="Alexandria" font-size="10.5" font-weight="500" fill="{color}" letter-spacing="1.5">'
            f'<textPath href="#arc">• QUALITY • SINCE 2026 • BEST SERVICE • TRUSTED BRAND • PREMIUM</textPath></text></svg>')


def face(html, extra=""):
    return (f'<div style="position:absolute;inset:0;border-radius:34px;background:{PAPER};border:3px solid {SOFT};'
            f'box-shadow:0 24px 50px rgba(32,33,38,.12);display:flex;align-items:center;justify-content:center;{extra}">{html}</div>')


# ---------------- scene 1: the memory game ----------------
def flip_card(x, front, back, t_hide, t_show, front_after=None):
    """A card that shows `front`, flips to `back` at t_hide, and flips again at t_show to `front_after`."""
    fa = front_after or front
    q = lambda name, t, k="forwards": an(name, t, .22, "ease-in" if name == "flipOut" else "ease-out", k)
    return (f'<div style="position:absolute;left:{x}px;top:560px;width:400px;height:440px">'
            f'<div style="position:absolute;inset:0;{anims(q("flipOut", t_hide))}">{face(front)}</div>'
            f'<div style="position:absolute;inset:0;transform:scaleX(0);{anims(q("flipIn", t_hide + .22), q("flipOut", t_show))}">'
            f'{face(f"<span style=\'font-size:200px;font-weight:800;color:{TE}\'>؟</span>")}</div>'
            f'<div style="position:absolute;inset:0;transform:scaleX(0);{anims(q("flipIn", t_show + .22))}">{face(fa)}</div></div>')


def scene1():
    hide, show = 3.9, 8.3
    for k in range(3):
        R.cue(.9 + k, "tick")
    count = "".join(
        R.el(.9 + k, f'<span class="ltr" style="font-size:150px;font-weight:800;color:{TE}">{3 - k}</span>', "pop", d=.35, out=1.75 + k, out_d=.15,
             style="position:absolute;left:0;width:1080px;top:1040px;text-align:center")
        for k in range(3))
    R.cue(hide, "swipe"); R.cue(show, "swipe")
    simple = ring_mark(300)
    busy = busy_emblem(320)
    busy_after = f'<div style="filter:blur(9px);opacity:.4">{busy_emblem(320)}</div>'
    cards = (R.el(.3, flip_card(560, busy, "", hide, show, busy_after), "pop", d=.5, cue="pop", style="position:absolute;inset:0")
             + R.el(.45, flip_card(120, simple, "", hide, show), "pop", d=.5, style="position:absolute;inset:0"))
    body = (
        R.txt(None, "لعبة ذاكرة سريعة:", 300, 64, color=TE)
        + R.txt(None, "احفظ الشعارين", 392, 96)
        + cards + count
        + R.txt(hide + .4, "أيّهما تتذكّر شكله؟", 1050, 80, kind="pop", cue="question", out=show + .2)
        + R.think(hide + 1.0, 3, top=1190)
        + R.txt(show + .5, "البسيط يبقى في الذاكرة.", 1080, 74, kind="pop", cue="ding")
        + R.txt(show + 1.0, "والمزدحم يُنسى بسرعة.", 1200, 50, weight=600)
    )
    return R.scene(T1, T2, body, cue=None, leave="sOutUp")


# ---------------- scene 2: three easy tests ----------------
def check_badge(t, x, y):
    return (f'<svg viewBox="0 0 64 64" width="64" height="64" style="position:absolute;left:{x}px;top:{y}px;{anims(an("pop", t, .55, BOUNCE))}">'
            f'<circle cx="32" cy="32" r="32" fill="{TE}"/><path d="M19 33l9 9 17-19" fill="none" stroke="{DK}" stroke-width="6" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>')


TESTS = [("هل ترسمه بإصبعك؟", "في خمس ثوانٍ أو أقل."), ("هل يبقى واضحاً وهو صغير؟", "مثل صورة الحساب."),
         ("هل يبقى جميلاً بلون واحد؟", "على الختم والتطريز.")]


def scene2():
    t0 = T2
    ys = [430, 770, 1110]
    tap1, tap2, tap3 = t0 + 2.0, t0 + 5.7, t0 + 9.3
    cards = ""
    for k, ((title, sub), y) in enumerate(zip(TESTS, ys)):
        on = (tap1, tap2, tap3)[k]
        inner = (f'<div style="position:absolute;inset:0;border-radius:34px;background:{PAPER};border:3px solid {SOFT}"></div>'
                 f'<div style="position:absolute;inset:0;border-radius:34px;border:4px solid {TE};{anims(an("fade", on, .3))}"></div>'
                 f'<div style="position:absolute;right:36px;left:320px;top:50%;transform:translateY(-50%)">'
                 f'<div style="display:flex;align-items:flex-start;gap:16px"><span class="ltr" style="flex-shrink:0;width:56px;height:56px;border-radius:28px;'
                 f'background:{DK};color:{CH};display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:800">{k + 1}</span>'
                 f'<span style="font-size:44px;font-weight:800;line-height:1.3">{title}</span></div>'
                 f'<div style="font-size:38px;font-weight:500;line-height:1.45;margin-top:10px;margin-right:72px;opacity:.85">{sub}</div></div>'
                 f'<div style="position:absolute;left:30px;top:20px;width:260px;height:260px;border-radius:26px;background:#fff;border:3px dashed rgba(32,33,38,.2)"></div>')
        cards += R.el(t0 + .6 + k * .25, R.pressed(on, inner, "position:absolute;inset:0"), "fromR", d=.6, cue="pop",
                      style=f"position:absolute;left:90px;top:{y}px;width:900px;height:300px")
    # test 1: draw the two rings with a finger, a 5-second countdown in the corner
    cx, cy = 250, ys[0] + 150
    c1, c2 = (cx - 30, cy), (cx + 30, cy)
    r = 55
    d0, d1, d2, d3 = tap1 + .3, tap1 + 1.2, tap1 + 1.35, tap1 + 2.25
    demo1 = (f'<svg width="1080" height="1920" style="position:absolute;left:0;top:0;overflow:visible">'
             f'<circle cx="{c1[0]}" cy="{c1[1]}" r="{r}" pathLength="1" fill="none" stroke="{TE}" stroke-width="16" stroke-linecap="round" '
             f'stroke-dasharray="1 2" stroke-dashoffset="1.02" style="{anims(an("draw", d0, d1 - d0, "linear"))}"/>'
             f'<circle cx="{c2[0]}" cy="{c2[1]}" r="{r}" pathLength="1" fill="none" stroke="{RO}" stroke-width="16" stroke-linecap="round" '
             f'stroke-dasharray="1 2" stroke-dashoffset="1.02" style="{anims(an("draw", d2, d3 - d2, "linear"))}"/></svg>')
    timer = (f'<div class="ltr" style="position:absolute;left:136px;top:{ys[0] + 32}px;font-size:36px;font-weight:800;color:{TE};'
             f'{anims(an("fade", tap1 + .2, .3), an("out", d3 + .5, .3, "ease", "forwards"))}"><span data-count="5:2:{RT(d0)}:{RT(d3)}:0:1">5</span> ث</div>')
    R.cue(d0, "scribble", d=d1 - d0); R.cue(d2, "scribble", d=d3 - d2)
    for k in range(4):          # the 5-4-3-2 countdown: one clock tick per number shown
        R.cue(d0 + k * (d3 - d0) / 3, "tick")
    pts = [(t0 + 1.4, 700, 1500, "show"), (tap1, cx, cy, "tap"), (d0, c1[0] + r, c1[1], "down")]
    for k in range(1, 9):
        a = k * math.pi / 4
        pts.append((d0 + (d1 - d0) * k / 8, round(c1[0] + r * math.cos(a)), round(c1[1] + r * math.sin(a)), "move"))
    pts += [(d1 + .05, c1[0] + r, c1[1], "up"), (d2, c2[0] + r, c2[1], "down")]
    for k in range(1, 9):
        a = k * math.pi / 4
        pts.append((d2 + (d3 - d2) * k / 8, round(c2[0] + r * math.cos(a)), round(c2[1] + r * math.sin(a)), "move"))
    pts += [(d3 + .05, c2[0] + r, c2[1], "up")]
    # test 2: the logo shrinks to the size of a profile photo and stays clear
    R.kf.append("@keyframes shrink{from{transform:scale(1)}to{transform:scale(.36)}}")
    small = (f'<div style="position:absolute;left:120px;top:{ys[1] + 20}px;width:260px;height:260px;display:grid;place-items:center">'
             f'<div style="grid-area:1/1;{anims(an("fade", tap2 + .1, .3), an("shrink", tap2 + .6, .8, EASE, "forwards"))}">{ring_mark(210)}</div>'
             f'<div style="grid-area:1/1;width:104px;height:104px;border-radius:52px;border:4px solid {DK};{anims(an("pop", tap2 + 1.4, .4, BOUNCE))}"></div></div>')
    R.cue(tap2 + .6, "min")
    # test 3: two colours -> one colour, still clear
    colour = f'<div style="{anims(an("pop", tap3 + .1, .4, BOUNCE), an("out", tap3 + .9, .6, "ease", "forwards"))}">{ring_mark(200)}</div>'
    mono = f'<div style="{anims(an("fade", tap3 + .9, .6))}">{ring_mark(200, DK, DK)}</div>'
    demo3 = (f'<div style="position:absolute;left:120px;top:{ys[2] + 20}px;width:260px;height:260px;display:grid;place-items:center">'
             f'<div style="grid-area:1/1">{colour}</div><div style="grid-area:1/1">{mono}</div></div>')
    R.cue(tap3 + .9, "min")
    pts += [(tap2, 250, ys[1] + 150, "tap"), (tap3, 250, ys[2] + 150, "tap"), (tap3 + .7, 520, 1500, "hide")]
    ok1, ok2, ok3 = d3 + .4, tap2 + 2.0, tap3 + 1.8
    for t in (ok1, ok2, ok3):
        R.cue(t, "confirm")
    body = (
        R.txt(t0 + .1, "اختبر شعارك بـ3 أسئلة", 290, 66, kind="pop", cue="pop")
        + cards + demo1 + timer + small + demo3
        + check_badge(ok1, 330, ys[0] + 16) + check_badge(ok2, 330, ys[1] + 16) + check_badge(ok3, 330, ys[2] + 16)
        + R.cursor(pts)
    )
    return R.scene(t0, T3, body, leave="sOutUp")


# ---------------- scene 3: your logo (the ending Marwa liked) ----------------
def scene3():
    t0 = T3
    send = t0 + 3.4
    field = (f'<div style="position:absolute;inset:0;border-radius:62px;background:{PAPER};border:3px solid {SOFT}"></div>'
             f'<div style="position:relative;height:100%;display:flex;align-items:center;justify-content:space-between;padding:0 18px 0 44px">'
             f'<span style="font-size:48px;font-weight:700">' + R.typing(t0 + 1.8, t0 + 2.9, "مخبز الورد") + '</span>'
             + R.pressed(send, f'<span style="width:92px;height:92px;border-radius:46px;background:{DK};display:flex;align-items:center;justify-content:center">'
                               f'<svg viewBox="0 0 40 40" width="44" height="44"><path d="M30 20H10M18 11l-9 9 9 9" fill="none" stroke="{CH}" stroke-width="4.5" '
                               f'stroke-linecap="round" stroke-linejoin="round"/></svg></span>') + '</div>')
    heart = (f'<svg viewBox="0 0 48 48" width="64" height="64" style="{anims(an("pop", send + .3, .6, BOUNCE))}">'
             f'<path d="M24 41S6 30 6 17a9 9 0 0 1 18-3 9 9 0 0 1 18 3c0 13-18 24-18 24z" fill="{RO}"/></svg>')
    R.cue(send + .35, "pop")
    film = ""
    if BROLL:   # real footage under the question: a hand sketching a simple logo idea
        film = R.el(t0 + .5, f'<div style="position:absolute;inset:0;border-radius:36px;overflow:hidden;background:{PAPER};'
                             f'box-shadow:0 30px 70px rgba(32,33,38,.16),0 0 0 2px {SOFT}">{R.clip(t0 + .5, BROLL)}</div>',
                    "up", d=.6, style="position:absolute;left:90px;top:860px;width:900px;height:600px")
    body = (
        film
        + R.txt(t0 + .1, "وشعارك أنت؟", 330, 110, kind="pop", cue="pop")
        + R.txt(t0 + .8, "اكتب اسم مشروعك في التعليقات.", 500, 54, weight=600)
        + R.el(t0 + 1.3, field, "up", style="position:absolute;left:90px;top:660px;width:900px;height:130px")
        + R.el(send + .3, heart, "fade", d=.1, style="position:absolute;left:104px;top:566px")
        + R.cursor([(t0 + 2.6, 700, 1160, "show"), (send, 154, 725, "tap"), (send + .7, 320, 1000, "hide")])
    )
    return R.scene(t0, T4, body, leave="sOutUp")


# ---------------- scene 4: checklist to save, and send ----------------
def scene4():
    t0 = T4
    return R.scene(t0, None,
                   R.endcard(t0, "شعار ناجح:", ["ترسمه بإصبعك", "واضح وهو صغير", "جميل بلون واحد"], "أرسله لصاحب مشروع جديد",
                             card_bg=PAPER, card_fg=DK, tick_bg=TE, tick_fg=DK, send_bg=MU, send_fg=DK, logo_color=DK, edge=SOFT)
                   + R.txt(t0 + 2.2, "احفظ الفيديو قبل أن تطلب شعارك.", 900, 44, weight=600, kind="fade"))


def cover():
    card = lambda x, html: (f'<div class="ab" style="left:{x}px;top:430px;width:400px;height:440px;border-radius:34px;background:{PAPER};'
                            f'border:3px solid {SOFT};box-shadow:0 24px 50px rgba(32,33,38,.12);display:flex;align-items:center;justify-content:center">{html}</div>')
    chip = (f'<span style="padding:14px 34px;border-radius:44px;border:3px solid {DK};font-size:34px;font-weight:600">'
            f'من الفكرة إلى الشعار · الحلقة 1</span>')
    body = (
        R.touches(ICON_SET, opacity=.08, seed=8)
        + f'<div class="ab" style="right:90px;top:310px">{chip}</div>'
        + card(560, f'<div style="filter:blur(7px);opacity:.45">{busy_emblem(320)}</div>') + card(120, ring_mark(300))
        + f'<div class="ab" style="right:90px;left:90px;top:930px;font-size:104px;font-weight:800;line-height:1.4">أيّ شعار<br>ستتذكّره غداً؟</div>'
        + f'<div class="ab" style="right:90px;left:90px;top:1270px;font-size:48px;font-weight:600;line-height:1.6">واختبر شعارك بـ3 أسئلة</div>'
        + f'<div class="ab" style="left:90px;top:1420px">{lockup_svg(300, DK)}</div>'
    )
    return R.still_page(body)


EXTRA = ("@keyframes flipOut{from{transform:scaleX(1)}to{transform:scaleX(0)}}"
         "@keyframes flipIn{from{transform:scaleX(0)}to{transform:scaleX(1)}}")


def build():
    body = (R.touches(ICON_SET, opacity=.1, seed=8) + R.chrome("من الفكرة إلى الشعار · الحلقة 1")
            + scene1() + scene2() + scene3() + scene4())
    return R.page(body, EXTRA)


if __name__ == "__main__":
    html = build()
    stills = [0.0, 2.0, 4.0, 6.5, 9.5, 12.5, 15.0, 18.5, 22.0, 25.0, 29.5, 38.0]
    if "--stills" in sys.argv:
        stills = [float(s) for s in sys.argv[sys.argv.index("--stills") + 1].split(",")]
    R.render(HERE, html, DUR, cover_html=cover(), stills=[RT(x) for x in stills], voice=VO["voice"] if VO else None)
