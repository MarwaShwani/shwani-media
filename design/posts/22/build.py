"""Post 22 (Wed 18 Nov 12:30): reel «سيرتك في دقيقة 2: كلمات تُضعف سيرتك». Row 8, slate.

Keeps the second episode named in post 5's draft. A game in three rounds: a weak line from a CV, a tap on ✗,
it is struck out, and a stronger line slides in with ✓ and a one-line rule. Everyday words, no studies.
The example lines are invented. Voice: Sola (Gemini), as decided for the latest reels.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, DESIGN)
from reelkit import *  # noqa
from kit2 import row

K = Kit("slate"); R = K.R
SERIES = "سيرتك في دقيقة · الحلقة 2"
INTRO = load_intro(HERE, 3.2)
(T1, T2, T3, T4, T5), DUR = timeline([INTRO, 8.4, 8.4, 8.0, 8.0])
DUR_DESIGN = DUR
ROUNDS = [
    ("الأولى", "مجتهد وأحب العمل", "صفة يكتبها الجميع، ولا تُثبت شيئاً.", "نظّمتُ مخزن المحل في أسبوع واحد", "اكتب ما فعلته، لا صفتك."),
    ("الثانية", "كنتُ مسؤولاً عن المبيعات", "تقول مكانك، لا ما أنجزته.", "بعتُ 120 جهازاً في شهر واحد", "ابدأ بفعل، وأضف رقماً."),
    ("الثالثة", "أجيد استخدام الحاسوب", "كلمة عامة لا يمكن اختبارها.", '<span class="ltr">Word · Excel · PowerPoint</span>', "سمِّ البرامج بأسمائها."),
]
VO_PLAN = [
    (0.0, "ثلاثُ جُمَلٍ في سيرتك يتجاوزُها صاحبُ العمل. هل عندك واحدةٌ منها؟", None),
    (T2 + .3, "الأولى: مجتهدٌ وأحبُّ العمل.", None),
    (T2 + 3.0, "صفةٌ يكتبُها الجميع. اكتبْ ما فعلتَه: نظّمتُ مخزنَ المحلِّ في أسبوعٍ واحد.", None),
    (T3 + .3, "الثانية: كنتُ مسؤولاً عن المبيعات.", None),
    (T3 + 3.0, "تقولُ مكانَك، لا إنجازَك. ابدأْ بفعلٍ ورقم: بعتُ مئةً وعشرين جهازاً في شهر.", None),
    (T4 + .3, "الثالثة: أُجيدُ استخدامَ الحاسوب.", None),
    (T4 + 3.0, "كلمةٌ عامّة. سمِّ البرامجَ بأسمائها.", None),
    (T5 + .3, "سيرةٌ لا تُتجاوَز: ما فعلتَه لا صفاتُك، وفعلٌ ورقم، وأسماءُ البرامج.", None),
    (T5 + 3.6, "احفظْه، وأرسلْه لمن يكتبُ سيرتَه.", T5 + 3.5),
]
VO = load_vo(HERE)
if VO:
    DUR = VO["dur"]
ICON_SET = ["doc", "case", "pen", "check", "search", "clip"]


def mini_cv():
    bar = lambda w, c="rgba(32,33,38,.16)", h=16: f'<div style="width:{w}%;height:{h}px;border-radius:8px;background:{c}"></div>'
    rows = (bar(55, DK, 26) + bar(35) + '<div style="height:16px"></div>' + bar(90) + bar(80)
            + f'<div style="border:5px solid {TE};border-radius:16px;padding:12px 14px;display:flex;flex-direction:column;gap:12px">{bar(70, TE)}</div>'
            + bar(85) + bar(60))
    return K.card(f'<div style="display:flex;flex-direction:column;gap:16px">{rows}</div>', pad=44)


def scene1():
    body = (R.txt(None, "3 جمل في سيرتك", 330, 84)
            + R.txt(None, "يتجاوزها صاحب العمل.", 450, 66, weight=700)
            + R.txt(None, "هل عندك واحدة منها؟", 560, 52, weight=600, color=CH)
            + f'<div style="position:absolute;left:230px;width:620px;top:690px">{mini_cv()}</div>'
            + K.think(.2, INTRO - .8, top=1180))
    return R.scene(T1, T2, body, cue=None, leave="sOutUp")


def xbtn():
    return (f'<span style="width:84px;height:84px;border-radius:42px;background:{DK};display:flex;align-items:center;justify-content:center;flex-shrink:0">'
            f'<svg viewBox="0 0 40 40" width="40" height="40"><path d="M11 11l18 18M29 11L11 29" stroke="{CH}" stroke-width="5" stroke-linecap="round"/></svg></span>')


def vbtn(t):
    return (f'<svg viewBox="0 0 48 48" width="84" height="84" style="flex-shrink:0;{anims(an("pop", t, .5, BOUNCE))}">'
            f'<circle cx="24" cy="24" r="24" fill="{TE}"/><path d="M14 24.5l6.5 6.5L34 17" fill="none" stroke="{DK}" stroke-width="5" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def round_(t0, t1, k):
    which, weak, why, strong, rule = ROUNDS[k]
    tap = t0 + 1.9
    strike = (f'<div style="position:absolute;right:40px;left:150px;top:50%;height:8px;margin-top:-4px;border-radius:4px;background:{TE};'
              f'transform-origin:right;transform:scaleX(0);{anims(an("grow", tap + .15, .45))}"></div>')
    R.cue(tap + .15, "scribble", d=.45)
    weak_card = K.card(f'<div style="display:flex;align-items:center;gap:30px;position:relative">'
                       f'<span style="flex-grow:1;font-size:56px;font-weight:800;line-height:1.35">{weak}</span>'
                       + R.pressed(tap, xbtn()) + f'</div>{strike}', pad=46, extra="position:relative")
    weak_el = (f'<div style="{anims(an("shake", RT(tap) + .1, .5, "ease", "none", raw=True), an("dim", tap + .7, .5))}">{weak_card}</div>')
    strong_card = K.card(f'<div style="display:flex;align-items:center;gap:30px;position:relative">'
                         f'<span style="flex-grow:1;font-size:{48 if "ltr" in strong else 56}px;font-weight:800;line-height:1.35;white-space:{"nowrap" if "ltr" in strong else "normal"}">{strong}</span>'
                         + vbtn(t0 + 4.7) + '</div>', pad=46, extra=f"border:6px solid {TE}")
    body = (R.txt(t0 + .1, f"الجملة {which}", 330, 54, weight=700, kind="fade")
            + R.txt(t0 + .3, "قبل", 410, 36, weight=700, kind="fade", align="right")
            + R.txt(t0 + 4.2, "بعد", 840, 36, weight=700, kind="fade", align="right")
            + R.el(t0 + .3, weak_el, "fromR", d=.6, cue="drop", style="position:absolute;left:90px;width:900px;top:470px")
            + R.cursor([(t0 + 1.2, 700, 1400, "show"), (tap, 192, 575, "tap"), (tap + .8, 400, 1300, "hide")])
            + R.txt(t0 + 2.9, why, 760, 46, weight=600, kind="fade")
            + R.el(t0 + 4.2, strong_card, "fromR", d=.6, cue="drop", style="position:absolute;left:90px;width:900px;top:900px")
            + R.el(t0 + 5.6, f'<span style="display:inline-block;background:{CH};color:{DK};border-radius:44px;padding:18px 40px;font-size:46px;font-weight:800">{rule}</span>',
                   "pop", d=.5, cue="pop", style="position:absolute;left:90px;width:900px;top:1230px;text-align:center"))
    return R.scene(t0, t1, body)


def scene_end():
    return R.scene(T5, None, K.end(T5, "سيرة لا تُتجاوز:", ["ما فعلته، لا صفاتك", "فعل ورقم", "أسماء البرامج"],
                                   "أرسله لمن يكتب سيرته", line="احفظه قبل أن ترسل سيرتك."))


def cover():
    C = row("slate")
    vis = (f'<div class="z" style="display:flex;flex-direction:column;gap:22px">'
           f'<div class="card" style="padding:30px 40px;font-size:50px;font-weight:800;position:relative;opacity:.8">مجتهد وأحب العمل'
           f'<div style="position:absolute;right:40px;left:40px;top:50%;height:8px;background:{TE};border-radius:4px"></div></div>'
           f'<div class="card" style="padding:30px 40px;font-size:50px;font-weight:800;border:6px solid {TE}">نظّمتُ مخزن المحل في أسبوع</div></div>')
    return C.cover(SERIES, "كلمات تُضعف<br>سيرتك", vis, "3 جمل يتجاوزها صاحب العمل، وما تكتبه بدلاً منها.", swipe=False)


def build():
    body = (R.touches(ICON_SET, opacity=.08, seed=5) + K.chrome(SERIES) + scene1()
            + round_(T2, T3, 0) + round_(T3, T4, 1) + round_(T4, T5, 2) + scene_end())
    return K.page(body)


if __name__ == "__main__":
    html = build()
    reel_cover(HERE, cover())
    stills = [0.0, T2 + 1.5, T2 + 3.5, T2 + 6.5, T3 + 6.5, T4 + 6.5, T5 + 4.5]
    R.render(HERE, html, DUR, stills=[RT(x) for x in stills], voice=VO["voice"] if VO else None)
