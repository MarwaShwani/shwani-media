"""Post 24 (Thu 19 Nov 12:30): reel «قبل وبعد 2: سيرة ذاتية». Row 8, slate.

Keeps the promise of reel 8 («قبل وبعد 2: قبل وبعد لسيرة ذاتية»). Two CV pages for the same invented person
(«حسين أحمد», the name Marwa chose for reel 5), said on screen to be invented. Which one do you read first?
Then a before/after wipe dragged by a finger, and the three changes that make the difference.
The pages are drawn as shapes (no tiny text), so nothing on screen is under 34 px. Voice: Cleo (as reel 8).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, DESIGN)
from reelkit import *  # noqa
from kit2 import row

K = Kit("slate"); R = K.R
SERIES = "قبل وبعد · الحلقة 2"
INTRO = load_intro(HERE, 3.0)
(T1, T2, T3, T4, T5), DUR = timeline([INTRO, 5.2, 7.6, 11.0, 8.0])
DUR_DESIGN = DUR
VO_PLAN = [
    (0.0, "سيرتان لنفس الشخص. أيُّهما يقرؤها صاحبُ العمل أولاً؟", None),
    (T2 + .5, "الثانية، لأنها تُقرأُ في ثوانٍ.", None),
    (T3 + .3, "نفسُ المعلومات، قبل وبعد.", None),
    (T4 + .3, "أولاً: اسمُك ووظيفتُك في أولِ سطر.", None),
    (T4 + 3.8, "ثانياً: عناوينُ واضحة، ونقاطٌ قصيرة.", None),
    (T4 + 7.2, "ثالثاً: صفحةٌ واحدة، وفراغٌ يُريحُ العين.", None),
    (T5 + .3, "سيرةٌ تُقرأُ في ثوانٍ: اسمُك ووظيفتُك أولاً، وعناوينُ ونقاطٌ قصيرة، وصفحةٌ واحدة.", None),
    (T5 + 3.6, "احفظْه، وأرسلْه لمن يكتبُ سيرتَه.", T5 + 3.5),
]
VO = load_vo(HERE)
if VO:
    DUR = VO["dur"]
ICON_SET = ["doc", "search", "pen", "check", "case", "clip"]
GREY = "rgba(32,33,38,.17)"


def bar(w, c=GREY, h=1.0):
    return f'<div style="width:{w}%;height:{h}em;border-radius:.5em;background:{c};flex-shrink:0"></div>'


def cv_before(w):
    """Crowded page: centred title in three colours, a photo, long dense paragraphs, no white space."""
    para = lambda n, c=GREY: "".join(bar(100 if k % 4 else 96, c, .55) for k in range(n))
    inner = (f'<div style="display:flex;align-items:center;gap:.8em"><div style="width:4.2em;height:4.2em;border-radius:50%;background:#B9B2A6;flex-shrink:0"></div>'
             f'<div style="flex-grow:1;display:flex;flex-direction:column;gap:.45em">{bar(70, "#8A2BE2", .9)}{bar(45, "#1E88E5", .6)}</div></div>'
             + para(5) + bar(40, "#2E7D32", .75) + para(6) + bar(35, "#C62828", .75) + para(6) + bar(45, "#F57C00", .75) + para(5))
    return (f'<div style="width:{w}px;height:{w * 1.414:.0f}px;background:#FFFDF7;border-radius:14px;padding:{w * .06:.0f}px;font-size:{w / 26:.1f}px;'
            f'display:flex;flex-direction:column;gap:.42em;border:4px double #555;box-shadow:0 26px 60px rgba(0,0,0,.28);overflow:hidden">{inner}</div>')


def cv_after(w, name=True):
    """Clean page: name and job first, clear headings, short points, white space."""
    sec = lambda n: (bar(34, TE, .8) + "".join(
        f'<div style="display:flex;align-items:center;gap:.6em"><span style="width:.5em;height:.5em;border-radius:50%;background:{SL};flex-shrink:0"></span>{bar(58 - 9 * k)}</div>'
        for k in range(n)))
    head = (f'<div style="font-size:2.9em;font-weight:800;color:{DK};line-height:1.2">حسين أحمد</div>'
            f'<div style="font-size:1.9em;font-weight:600;color:{SL};line-height:1.3">مهندس برمجيات</div>') if name else (bar(55, DK, 2.2) + bar(40, SL, 1.3))
    inner = (head + f'<div style="height:2px;background:{GREY};margin:.6em 0"></div>' + sec(3) + '<div style="height:1.1em"></div>'
             + sec(3) + '<div style="height:1.1em"></div>' + sec(2))
    return (f'<div style="width:{w}px;height:{w * 1.414:.0f}px;background:#FFFFFF;border-radius:14px;padding:{w * .09:.0f}px;font-size:{w / 26:.1f}px;'
            f'display:flex;flex-direction:column;gap:.75em;box-shadow:0 26px 60px rgba(0,0,0,.28);overflow:hidden">{inner}</div>')


def label(t, text, x, y, w):
    return R.el(t, f'<span style="display:inline-block;background:{CH};color:{DK};border-radius:40px;padding:10px 34px;font-size:44px;font-weight:800">{text}</span>',
                "pop", d=.4, style=f"position:absolute;left:{x}px;top:{y}px;width:{w}px;text-align:center")


def scene1():
    pw = 400
    body = (R.txt(None, "سيرتان لنفس الشخص.", 330, 66, weight=700)
            + R.txt(None, "أيّهما تقرأ أولاً؟", 430, 84)
            + f'<div class="ab" style="left:{540 + 20}px;top:600px">{cv_before(pw)}</div>'
            + f'<div class="ab" style="left:{540 - 20 - pw}px;top:600px">{cv_after(pw)}</div>'
            + f'<div class="ab" style="left:{560}px;width:{pw}px;top:1185px;text-align:center;font-size:52px;font-weight:800">أ</div>'
            + f'<div class="ab" style="left:{120}px;width:{pw}px;top:1185px;text-align:center;font-size:52px;font-weight:800">ب</div>'
            + K.think(.2, INTRO - .8, top=1300))
    return R.scene(T1, T2, body, cue=None)


def scene2():
    t, pw = T2, 400
    body = (R.txt(None, "سيرتان لنفس الشخص.", 330, 66, weight=700)
            + R.txt(None, "أيّهما تقرأ أولاً؟", 430, 84)
            + f'<div class="ab" style="left:560px;top:600px;{anims(an("dim", t + .9, .5))}">{cv_before(pw)}</div>'
            + f'<div class="ab" style="left:120px;top:600px;transform-origin:center;{anims(an("pulse", t + .7, .6, "ease-in-out", "none"))}">{cv_after(pw)}</div>'
            + R.cursor([(t + .1, 700, 1500, "show"), (t + .6, 320, 880, "tap"), (t + 1.3, 520, 1500, "hide")])
            + R.txt(t + 1.0, "ب، لأنها تُقرأ في ثوانٍ.", 1215, 58, kind="pop", cue="pop", color=CH)
            + R.txt(t + 1.8, "مثال من الخيال.", 1310, 38, weight=500, kind="fade"))
    return R.scene(t, T3, body, enter="fade", cue=None)


def scene3():
    t, pw = T3, 620
    x0, y0 = 230, 500
    d0, d1 = t + 1.6, t + 4.6
    name = R.uid("wipe")
    R.kf.append(f"@keyframes {name}{{from{{clip-path:inset(0 0 0 100%)}}to{{clip-path:inset(0 0 0 0)}}}}")
    hname = R.uid("hand")
    R.kf.append(f"@keyframes {hname}{{from{{transform:translateX({pw}px)}}to{{transform:translateX(0)}}}}")
    after = f'<div class="ab" style="left:0;top:0;clip-path:inset(0 0 0 100%);{anims(an(name, d0, d1 - d0, "cubic-bezier(.45,0,.25,1)"))}">{cv_after(pw)}</div>'
    handle = (f'<div class="ab" style="left:-4px;top:-20px;width:8px;height:{pw * 1.414 + 40:.0f}px;background:{TE};border-radius:4px;'
              f'transform:translateX({pw}px);{anims(an(hname, d0, d1 - d0, "cubic-bezier(.45,0,.25,1)"))}"></div>')
    R.cue(d0, "swipe")
    stack = f'<div class="ab" style="left:{x0}px;top:{y0}px;width:{pw}px;height:{pw * 1.414:.0f}px">{cv_before(pw)}{after}{handle}</div>'
    hy = y0 + pw * .7
    body = (R.txt(t + .1, "نفس المعلومات، قبل وبعد.", 330, 60, weight=800, kind="fade")
            + R.el(t + .2, stack, "up", d=.6, style="position:absolute;inset:0")
            + label(t + .5, "قبل", x0 + pw - 200, y0 + pw * 1.414 + 18, 200) + label(d1 - .2, "بعد", x0, y0 + pw * 1.414 + 18, 200)
            + R.cursor([(t + 1.0, x0 + pw + 60, hy, "show"), (d0, x0 + pw, hy, "down"), (d1, x0, hy, "move"), (d1 + .05, x0, hy, "up"),
                        (d1 + .6, x0 + 200, hy + 300, "hide")]))
    return R.scene(t, T4, body)


def scene4():
    t, pw = T4, 640
    x0, y0 = 220, 470
    ph = pw * 1.414
    steps = [(t + .4, "1", "اسمك ووظيفتك أولاً", (x0 + 40, y0 + 40, pw - 80, 170)),
             (t + 3.9, "2", "عناوين ونقاط قصيرة", (x0 + 40, y0 + 230, pw - 80, 300)),
             (t + 7.3, "3", "صفحة واحدة، وفراغ مريح", (x0 - 14, y0 - 14, pw + 28, ph + 28))]
    body = R.el(t + .1, f'<div class="ab" style="left:{x0}px;top:{y0}px">{cv_after(pw)}</div>', "fade", d=.4, style="position:absolute;inset:0")
    for k, (ts, n, text, (x, y, w, h)) in enumerate(steps):
        end = steps[k + 1][0] - .1 if k < 2 else None
        body += K.box(ts + .3, x, y, w, h, out=end)
        body += R.txt(ts + .2, f"{n}. {text}", 340, 58, kind="pop", cue="pop", out=end)
    return R.scene(t, T5, body)


def scene_end():
    return R.scene(T5, None, K.end(T5, "سيرة تُقرأ في ثوانٍ:", ["اسمك ووظيفتك أولاً", "عناوين ونقاط قصيرة", "صفحة واحدة"],
                                   "أرسله لمن يكتب سيرته", line="احفظه قبل أن ترسل سيرتك."))


def cover():
    C = row("slate")
    vis = (f'<div class="z" style="position:relative;height:640px">'
           f'<div style="position:absolute;left:560px;top:20px;transform:rotate(4deg);opacity:.9">{cv_before(420)}</div>'
           f'<div style="position:absolute;left:100px;top:20px;transform:rotate(-3deg)">{cv_after(420)}</div></div>')
    return C.cover(SERIES, "سيرة ذاتية:<br>قبل وبعد", vis, "نفس المعلومات، وسيرة تُقرأ في ثوانٍ.", swipe=False)


def build():
    body = (R.touches(ICON_SET, opacity=.08, seed=21) + K.chrome(SERIES) + scene1() + scene2() + scene3() + scene4() + scene_end())
    return K.page(body)


if __name__ == "__main__":
    html = build()
    reel_cover(HERE, cover())
    stills = [0.0, T2 + 2.0, T3 + 1.0, T3 + 3.0, T3 + 6.0, T4 + 1.5, T4 + 5.0, T4 + 9.0, T5 + 4.5]
    R.render(HERE, html, DUR, stills=[RT(x) for x in stills], voice=VO["voice"] if VO else None)
