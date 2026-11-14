"""Post 29 (Sat 21 Nov 21:00): reel «من الفكرة إلى الشعار 3: اسمك بلغتين في شعار واحد». Row 10, terracotta.

Most Iraqi shops need their name in Arabic and English. Shown on the Al-Manar logo (from our work):
one language leads (the Arabic is taller), the other is a base under it (the English is a little wider, so the
name stands on it like a lighthouse on the ground), and both share one spirit (the same gold, thin serifs that
echo the pen). Charcoal text on terracotta, one-colour logo. Voice: Bodi (as reels 6 and 20). AI-made picture.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, DESIGN)
from reelkit import *  # noqa
from kit2 import row, A, fit

K = Kit("terra"); R = K.R
SERIES = "من الفكرة إلى الشعار · الحلقة 3"
LOGO = A("almanar", "01_logo.jpg")
INTRO = load_intro(HERE, 3.0)
(T1, T2, T3, T4, T5), DUR = timeline([INTRO, 9.0, 8.0, 8.5, 8.0])
DUR_DESIGN = DUR
VO_PLAN = [
    (0.0, "اسمُ محلِّك بالعربي والإنجليزي، في شعارٍ واحد: أيُّهما البطل؟", None),
    (T2 + .3, "أولاً: لغةٌ واحدةٌ هي البطل. هنا العربيُّ أكبرُ وأعلى، والإنجليزيُّ أهدأُ تحته.", None),
    (T3 + .3, "ثانياً: الثانيةُ قاعدةٌ تحتها، أعرضُ قليلاً، فيقفُ عليها الاسمُ كما يقفُ المنارُ على الأرض.", None),
    (T4 + .3, "ثالثاً: روحٌ واحدةٌ للخطَّين: نفسُ اللون، وأطرافٌ رفيعةٌ تُشبهُ ريشةَ الخطّ.", None),
    (T5 + .3, "شعارٌ بلغتين: لغةٌ هي البطل، والثانيةُ قاعدةٌ تحتها، وروحٌ واحدةٌ للخطَّين.", None),
    (T5 + 3.6, "احفظْه، وأرسلْه لصاحبِ مشروعٍ جديد.", T5 + 3.5),
]
VO = load_vo(HERE)
if VO:
    DUR = VO["dur"]
ICON_SET = ["abc", "pencil", "circle", "pen", "bezier", "star"]
X0, Y0, W = 140, 470, 800          # the logo picture on screen
P = lambda fx, fy: (X0 + fx * W, Y0 + fy * W)


def pic(t, kind="fade"):
    return R.el(t, K.img(fit(LOGO, 800, 800), 800, 800, radius=40), kind, d=.6, style=f"position:absolute;left:{X0}px;top:{Y0}px")


def hbox(t, fx0, fy0, fx1, fy1, label=None, out=None, below=False, color=DK):
    (x0, y0), (x1, y1) = P(fx0, fy0), P(fx1, fy1)
    return K.box(t, x0, y0, x1 - x0, y1 - y0, label=label, out=out, label_below=below, color=color)


def scene1():
    small = K.img(fit(LOGO, 560, 560), 560, 560, radius=36)
    body = (R.txt(None, "اسمك بالعربي والإنجليزي", 330, 70)
            + R.txt(None, "أيّهما البطل؟", 440, 92, color=CH)
            + f'<div class="ab" style="left:260px;top:600px">{small}</div>'
            + K.think(.2, INTRO - .8, top=1230))
    return R.scene(T1, T2, body, cue=None, leave="sOutUp")


def scene2():
    t = T2
    body = (K.step(t + .1, 1, "لغة واحدة هي البطل") + pic(t + .4, "zoom")
            + hbox(t + 1.6, .27, .15, .73, .61, "البطل", out=None)
            + hbox(t + 3.6, .18, .62, .82, .82, "المساعد", below=True, color=RO)
            + R.txt(t + 5.0, "العربي أكبر وأعلى، والإنجليزي أهدأ تحته.", 1440, 46, weight=700, kind="fade"))
    return R.scene(t, T3, body)


def scene3():
    t = T3
    (ex0, ey), (ex1, _) = P(.19, .75), P(.81, .75)
    (ax0, _), (ax1, _) = P(.30, .1), P(.70, .1)
    line = lambda x0, x1, y, tt, c: R.el(tt, f'<div style="height:10px;border-radius:5px;background:{c};transform-origin:right;'
                                         f'{anims(an("grow", tt, .6))}"></div>', "fade", d=.1, cue="select",
                                         style=f"position:absolute;left:{x0}px;width:{x1 - x0}px;top:{y}px")
    body = (K.step(t + .1, 2, "الثانية قاعدة تحتها") + pic(t + .2, "fade")
            + line(ax0, ax1, Y0 + .64 * W - 6, t + 1.4, RO)
            + line(ex0, ex1, Y0 + .845 * W, t + 2.6, DK)
            + R.txt(t + 3.6, "أعرض قليلاً، فيقف عليها الاسم", 1310, 48, weight=700, kind="fade")
            + R.txt(t + 4.2, "كما يقف المنار على الأرض.", 1385, 48, weight=700, kind="fade", color=CH))
    return R.scene(t, T4, body)


def scene4():
    t = T4
    en, h1 = region(LOGO, (.17, .62, .83, .82), 900)
    ar, h2 = region(LOGO, (.28, .14, .72, .62), 440)
    body = (K.step(t + .1, 3, "روح واحدة للخطّين")
            + R.el(t + .5, ar, "zoom", d=.7, cue="drop", style="position:absolute;left:320px;top:450px")
            + R.el(t + 1.6, en, "fromR", d=.7, cue="drop", style=f"position:absolute;left:90px;top:{450 + h2 + 36:.0f}px")
            + R.txt(t + 3.2, "نفس الذهبي، وأطراف رفيعة", 1290, 48, weight=700, kind="fade")
            + R.txt(t + 3.8, "تشبه ريشة الخط العربي.", 1365, 48, weight=700, kind="fade", color=CH))
    return R.scene(t, T5, body)


def scene_end():
    return R.scene(T5, None, K.end(T5, "شعار بلغتين:", ["لغة واحدة هي البطل", "الثانية قاعدة تحتها", "روح واحدة للخطّين"],
                                   "أرسله لصاحب مشروع جديد", line="احفظه قبل أن تطلب شعارك."))


def cover():
    C = row("terra")
    vis = f'<div class="z" style="display:flex;justify-content:center">{K.img(fit(LOGO, 600, 600), 600, 600, radius=36)}</div>'
    return C.cover(SERIES, "اسمك بلغتين<br>في شعار واحد", vis, "أيّهما البطل: العربي أم الإنجليزي؟", swipe=False)


def build():
    body = R.touches(ICON_SET, opacity=.09, seed=14) + K.chrome(SERIES) + scene1() + scene2() + scene3() + scene4() + scene_end()
    return K.page(body)


if __name__ == "__main__":
    html = build()
    reel_cover(HERE, cover())
    stills = [0.0, T2 + 2.5, T2 + 6.0, T3 + 5.0, T4 + 5.0, T5 + 4.5]
    R.render(HERE, html, DUR, stills=[RT(x) for x in stills], voice=VO["voice"] if VO else None)
