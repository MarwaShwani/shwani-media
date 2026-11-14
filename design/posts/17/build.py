"""Post 17 (Sun 15 Nov 21:00): reel «ملازمنا المجانية». Row 6, sage.

The four simplified booklets, flipped page by page (real pages from the PDFs), and the offer: write the subject
in the comments, we send the PDF in a message, free (Marwa, 14 Nov). Paper sounds for every page.
Voice: Sola (Gemini).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, DESIGN)
from reelkit import *  # noqa
from kit2 import row, page_img, fit

K = Kit("sage"); R = K.R
SERIES = "ملازمنا المجانية"
INTRO = load_intro(HERE, 2.8)
BOOKS = [("math", "الرياضيات", "6 فصول، أمثلة محلولة، واختبر نفسك.", [1, 2, 9, 15]),
         ("phys", "الطبيعيات", "من الصفر، مع الوزاري حتى 2025.", [1, 4, 6, 18]),
         ("gram", "قواعد اللغة العربية", "كل قاعدة خطوة خطوة، مع حلول التمارين.", [1, 2, 5, 6]),
         ("comp", "صيانة الحاسوب", "تعاريف وتعاليل ومسائل محلولة.", [1, 2, 3, 6])]
SEG = 4.6
(T1, *TS, TE_), DUR = timeline([INTRO] + [SEG] * 4 + [8.0])
DUR_DESIGN = DUR
VO_PLAN = [
    (0.0, "تُذاكرُ وحدك بلا أستاذ؟ هذه الملازمُ لك، مجاناً.", None),
    (TS[0] + .2, "الرياضيات.", None),
    (TS[1] + .2, "الطبيعيات.", None),
    (TS[2] + .2, "قواعدُ اللغةِ العربية.", None),
    (TS[3] + .2, "وصيانةُ الحاسوب.", None),
    (TE_ + .3, "اكتبِ اسمَ المادةِ في التعليقات، ونرسلُ لك الملزمةَ في الرسائل، مجاناً.", None),
    (TE_ + 3.6, "وأرسلْه لزميلِك في الصف.", TE_ + 3.5),
]
VO = load_vo(HERE)
if VO:
    DUR = VO["dur"]
ICON_SET = ["book", "pencil", "ruler", "cap", "abc", "check"]
PW, PH = 640, 905


def sheet(path, rot):
    return (f'<img src="file://{fit(path, PW, PH)}" style="display:block;width:{PW}px;height:{PH}px;border-radius:14px;'
            f'transform:rotate({rot}deg);box-shadow:0 30px 60px rgba(0,0,0,.28),0 2px 8px rgba(0,0,0,.15)">')


def scene1():
    covers = "".join(f'<div class="ab" style="left:{150 + k * 170}px;top:{640 + (12 if k % 2 else 0)}px;transform:rotate({r}deg)">'
                     f'<img src="file://{fit(page_img(b, 1), 300, 424)}" style="display:block;width:300px;height:424px;border-radius:10px;'
                     f'box-shadow:0 20px 40px rgba(0,0,0,.25)"></div>'
                     for k, (b, r) in enumerate([("comp", -8), ("gram", -3), ("phys", 3), ("math", 8)]))
    body = (R.txt(None, "تذاكر وحدك بلا أستاذ؟", 330, 74)
            + R.txt(None, "هذه الملازم لك، مجاناً.", 440, 62, weight=700, color=CH)
            + covers + K.think(.2, INTRO - .8, top=1180))
    return R.scene(T1, TS[0], body, cue=None, leave="sOutUp")


def segment(k):
    t0 = TS[k]
    t1 = TS[k + 1] if k < 3 else TE_
    book, name, line, pages = BOOKS[k]
    stack = ""
    for j, n in enumerate(pages):
        tj = t0 + .35 + j * .85
        R.cue(tj, "swipe")
        stack += R.el(tj, sheet(page_img(book, n), (-3, 2, -2, 3)[j]), "fromL" if j % 2 else "fromR", d=.45,
                      style=f"position:absolute;left:{(1080 - PW) // 2}px;top:450px;z-index:{j + 1}")
    pill = (f'<span style="display:inline-block;background:{DK};color:{CH};border-radius:50px;padding:16px 44px;font-size:52px;font-weight:800">{name}</span>')
    body = (R.el(t0 + .1, pill, "pop", d=.45, cue="pop", style="position:absolute;left:90px;width:900px;top:320px;text-align:center")
            + stack
            + R.el(t0 + 1.4, f'<span style="display:inline-block;background:{CH};color:{DK};border-radius:30px;padding:16px 34px;font-size:42px;font-weight:700">{line}</span>',
                   "up", d=.5, style="position:absolute;left:60px;width:960px;top:1390px;text-align:center;z-index:9"))
    return R.scene(t0, t1, body)


def scene_end():
    return R.scene(TE_, None, K.end(TE_, "اكتب في التعليقات:", ["رياضيات", "طبيعيات", "قواعد", "صيانة حاسوب"],
                                    "أرسله لزميلك في الصف", line="ونرسل لك الملزمة في الرسائل، مجاناً."))


def cover():
    C = row("sage")
    vis = C.sheets([page_img(b, 1) for b in ("comp", "gram", "phys", "math")], h=560, rot=(-6, -2, 2, 6), gap=-62)
    return C.cover(SERIES, "4 ملازم مبسطة،<br>مجاناً لك", vis, "للثالث المهني: اكتب اسم المادة في التعليقات.", swipe=False)


def build():
    body = R.touches(ICON_SET, opacity=.1, seed=4) + K.chrome(SERIES) + scene1() + "".join(segment(k) for k in range(4)) + scene_end()
    return K.page(body)


if __name__ == "__main__":
    html = build()
    reel_cover(HERE, cover())
    stills = [0.0, TS[0] + 3.5, TS[1] + 3.5, TS[2] + 3.5, TS[3] + 3.5, TE_ + 4.5]
    R.render(HERE, html, DUR, stills=[RT(x) for x in stills], voice=VO["voice"] if VO else None)
