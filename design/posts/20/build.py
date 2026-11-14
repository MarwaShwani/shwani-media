"""Post 20 (Tue 17 Nov 12:30): reel «من الفكرة إلى الشعار 2: من اسم مشروعك إلى رمزه». Row 7, charcoal.

Keeps the second episode named in post 6's draft. One idea, shown not explained: a shop's name -> what it means
(a lighthouse) -> what it sells (a gem) -> both hidden in one letter of the name: the real Al-Manar logo
(from our work, Marwa 14 Nov: no word on whether it was a client). Three questions to save, send it on.
Voice: Bodi (as reel 6). The logo picture is AI-made: «AI info» label on.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, DESIGN)
from reelkit import *  # noqa
from kit2 import row, A, fit

K = Kit("charcoal"); R = K.R
SERIES = "من الفكرة إلى الشعار · الحلقة 2"
LOGO = A("almanar", "01_logo.jpg")
INTRO = load_intro(HERE, 3.0)
(T1, T2, T3, T4, T5), DUR = timeline([INTRO, 7.0, 6.2, 10.5, 8.0])
DUR_DESIGN = DUR
VO_PLAN = [
    (0.0, "كيف يصيرُ اسمُ محلٍّ رمزاً يُرى من بعيد؟", None),
    (T2 + .3, "أولاً: ماذا يعني الاسم؟ المنار: الضوءُ الذي يهدي من بعيد.", None),
    (T3 + .3, "ثانياً: ماذا يبيع؟ مجوهرات، فالجوهرةُ رمزُه الثاني.", None),
    (T4 + .3, "ثالثاً: نجمعُهما في حرفٍ واحدٍ من الاسم.", None),
    (T4 + 4.6, "الألفُ صار مناراً، وفي رأسه جوهرة.", None),
    (T5 + .3, "ثلاثةُ أسئلةٍ قبل رمزك: ماذا يعني اسمك؟ ماذا تبيع؟ وأيُّ حرفٍ يحمل الفكرة؟", None),
    (T5 + 3.6, "احفظه، وأرسله لصاحب مشروعٍ جديد.", T5 + 3.5),
]
VO = load_vo(HERE)
if VO:
    DUR = VO["dur"]
ICON_SET = ["star", "pencil", "circle", "drop", "bezier", "pen"]


def draw(path_d, t, d, color=MU, sw=10, extra=""):
    return (f'<path d="{path_d}" pathLength="1" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" '
            f'stroke-dasharray="1 2" stroke-dashoffset="1.02" style="{anims(an("draw", t, d, "ease-in-out"))};{extra}"/>')


def lighthouse(t):
    R.cue(t, "scribble", d=1.6)
    parts = ["M150 560 L190 230 L250 230 L290 560 Z", "M175 230 L175 180 L265 180 L265 230", "M160 180 L220 120 L280 180 Z",
             "M100 560 L340 560", "M185 330 L255 330 M180 430 L262 430"]
    rays = "".join(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{MU}" stroke-width="8" stroke-linecap="round" '
                   f'style="opacity:0;{anims(an("fade", t + 1.8 + k * .12, .3), an("pulse", t + 2.3, 1.2, "ease-in-out", "none"))}"/>'
                   for k, (x1, y1, x2, y2) in enumerate([(300, 200, 400, 160), (300, 215, 410, 215), (300, 230, 400, 270),
                                                         (140, 200, 40, 160), (140, 215, 30, 215), (140, 230, 40, 270)]))
    svg = "".join(draw(p, t + k * .3, .7) for k, p in enumerate(parts))
    return f'<svg viewBox="0 0 440 600" width="440" height="600" style="display:block">{svg}{rays}</svg>'


def gem(t):
    R.cue(t, "scribble", d=1.4)
    parts = ["M90 140 L150 70 L290 70 L350 140 L220 330 Z", "M90 140 L350 140", "M150 70 L190 140 L220 330 L250 140 L290 70",
             "M190 140 L220 70 L250 140"]
    spark = (f'<path d="M370 40 l10 26 26 10 -26 10 -10 26 -10 -26 -26 -10 26 -10z" fill="{CH}" '
             f'style="transform-origin:370px 76px;{anims(an("pop", t + 1.9, .5, BOUNCE))}"/>')
    R.cue(t + 1.9, "pop")
    svg = "".join(draw(p, t + k * .3, .6, color=RO if k == 0 else MU) for k, p in enumerate(parts))
    return f'<svg viewBox="0 0 440 400" width="440" height="400" style="display:block;overflow:visible">{svg}{spark}</svg>'


def scene1():
    word = K.card('<div style="font-size:150px;font-weight:700;line-height:1.3;text-align:center">المنار</div>'
                  f'<div style="font-size:40px;font-weight:500;text-align:center;opacity:.75">اسم محل مجوهرات</div>', pad=50)
    body = (R.txt(None, "كيف يصير اسمُ محلٍّ", 330, 76)
            + R.txt(None, "رمزاً يُرى من بعيد؟", 435, 76, color=MU)
            + f'<div style="position:absolute;left:190px;width:700px;top:640px">{word}</div>'
            + K.think(.2, INTRO - .8, top=1180))
    return R.scene(T1, T2, body, cue=None, leave="sOutUp")


def scene2():
    t = T2
    body = (K.step(t + .1, 1, "ماذا يعني الاسم؟")
            + R.el(t + .6, lighthouse(t + .8), "fade", d=.3, style="position:absolute;left:320px;top:520px")
            + R.txt(t + 3.4, "المنار: الضوء الذي يهدي من بعيد.", 1180, 52, weight=700, kind="pop", cue="pop"))
    return R.scene(t, T3, body)


def scene3():
    t = T3
    body = (K.step(t + .1, 2, "ماذا يبيع؟")
            + R.el(t + .6, gem(t + .8), "fade", d=.3, style="position:absolute;left:320px;top:600px")
            + R.txt(t + 3.0, "مجوهرات، فالجوهرة رمزه الثاني.", 1120, 52, weight=700, kind="pop", cue="pop"))
    return R.scene(t, T4, body)


def scene4():
    t = T4
    x0, y0, w = 140, 470, 800          # the logo picture, 800 x 800
    P = lambda fx, fy: (x0 + fx * w, y0 + fy * w)
    (ax, ay), (bx, by) = P(.435, .19), P(.555, .585)
    (gx, gy), (hx, hy) = P(.445, .16), P(.545, .25)
    pic = K.img(fit(LOGO, 800, 800), 800, 800, radius=40)
    body = (K.step(t + .1, 3, "اجمعهما في حرف واحد")
            + R.el(t + .7, pic, "zoom", d=.8, cue="drop", style=f"position:absolute;left:{x0}px;top:{y0}px")
            + K.box(t + 3.4, ax, ay + 30, bx - ax, by - ay - 30, color=TE)
            + K.box(t + 5.0, gx, gy, hx - gx, hy - gy, color=RO)
            + R.txt(t + 3.6, "الألف صار مناراً،", 1300, 54, kind="pop")
            + R.txt(t + 5.2, "وفي رأسه جوهرة.", 1380, 54, kind="pop", color=MU)
            + R.cursor([(t + 2.6, 760, 1500, "show"), (t + 3.4, ax + 50, ay + 260, "tap"), (t + 5.0, gx + 40, gy + 30, "tap"),
                        (t + 5.8, 820, 1500, "hide")])
            + R.txt(t + 7.6, "اسمٌ واحد، وفكرةٌ تُرى.", 1480, 46, weight=600, kind="fade"))
    return R.scene(t, T5, body, leave="sOutUp")


def scene5():
    return R.scene(T5, None, K.end(T5, "3 أسئلة قبل رمزك:", ["ماذا يعني اسمك؟", "ماذا تبيع؟", "أيّ حرف يحمل الفكرة؟"],
                                   "أرسله لصاحب مشروع جديد", line="احفظه قبل أن تطلب شعارك."))


def cover():
    C = row("charcoal")
    vis = f'<div class="z" style="display:flex;justify-content:center">{K.img(fit(LOGO, 600, 600), 600, 600, radius=36)}</div>'
    return C.cover(SERIES, "من اسم مشروعك<br>إلى رمزه", vis, "كيف صار اسم «المنار» منارةً وجوهرة؟", size=84, swipe=False)


def build():
    body = R.touches(ICON_SET, opacity=.07, seed=11) + K.chrome(SERIES) + scene1() + scene2() + scene3() + scene4() + scene5()
    return K.page(body)


if __name__ == "__main__":
    html = build()
    reel_cover(HERE, cover())
    stills = [0.0, INTRO + 1.5, INTRO + 5.5, T3 + 4.0, T4 + 2.0, T4 + 6.5, T4 + 9.0, T5 + 4.5]
    R.render(HERE, html, DUR, stills=[RT(x) for x in stills], voice=VO["voice"] if VO else None)
