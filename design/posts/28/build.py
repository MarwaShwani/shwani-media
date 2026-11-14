"""Post 28 (Sat 21 Nov 12:30): carousel «قبل أن تصمّم 3: كيف تختار خط مشروعك», 7 slides. Row 10, terracotta.
Keeps the promise of post 9. The example is the invented jewellery shop «ياقوت» from post 9 (said on screen).
Example fonts (all SIL Open Font License, from npm @fontsource): Aref Ruqaa, Lalezar, Tajawal; SHWANI's own font stays Alexandria."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from kit2 import *  # noqa
from common import FONTS

FS = os.path.dirname(FONTS)
LINKS = "".join(f'<link rel="stylesheet" href="file://{FS}/{p}/{w}.css">'
                for p, w in [("aref-ruqaa", 700), ("lalezar", 400), ("tajawal", 500), ("tajawal", 800), ("tajawal", 300)])
R = row("terra", 7)
S = "قبل أن تصمّم · الحلقة 3"
FONTS3 = [("Aref Ruqaa", 700, "رشيق وفاخر"), ("Lalezar", 400, "ممتلئ ومرح"), ("Tajawal", 500, "بسيط وعصري")]


def word(fam, wt, size, text="ياقوت", color=DK):
    return f'<span style="font-family:\'{fam}\';font-weight:{wt};font-size:{size}px;line-height:1.25;color:{color}">{text}</span>'


def three(size=110, labels=True):
    cards = "".join(
        f'<div class="card" style="display:flex;align-items:center;justify-content:space-between;padding:18px 40px">'
        f'{word(f, w, size)}' + (f'<span class="ltr" style="font-size:30px;font-weight:700;opacity:.75">{k}</span>' if not labels else
                                f'<span style="font-size:32px;font-weight:700;opacity:.8">{k}. {lab}</span>') + '</div>'
        for k, (f, w, lab) in enumerate(FONTS3, 1))
    return LINKS + f'<div class="z" style="display:flex;flex-direction:column;gap:18px">{cards}</div>'


def avatars():
    av = lambda fam, wt, size: (f'<div style="display:flex;flex-direction:column;align-items:center;gap:14px">'
                                f'<div style="width:150px;height:150px;border-radius:75px;background:{DK};display:flex;align-items:center;justify-content:center">'
                                f'{word(fam, wt, size, color=CH)}</div></div>')
    return (LINKS + f'<div class="card z" style="display:flex;justify-content:space-around;align-items:center;padding:34px">'
            + av("Aref Ruqaa", 700, 30) + av("Tajawal", 800, 34)
            + f'<div style="font-size:32px;font-weight:600;line-height:1.5;max-width:330px">بحجم صورة الحساب: أيّهما تقرؤه أسرع؟</div></div>')


def weights():
    return (LINKS + f'<div class="card z" style="padding:30px 40px;display:flex;flex-direction:column;gap:6px">'
            + word("Tajawal", 800, 76, "ياقوت للمجوهرات")
            + word("Tajawal", 500, 36, "خواتم وقلائد بتصميم خاص، في شارع الكرادة.")
            + word("Tajawal", 300, 30, "خط واحد بثلاثة أوزان: عنوان، ونص، وتفاصيل.") + '</div>')


def bilingual():
    return (f'<div class="card z" style="padding:34px 40px;display:flex;align-items:center;justify-content:space-between">'
            f'<span style="font-size:84px;font-weight:800">ياقوت</span><span style="font-size:54px;font-weight:800;opacity:.85" class="ltr">YAQOOT</span></div>'
            f'<p class="z" style="font-size:30px;font-weight:600;margin-top:14px">بخط واحد له حروف عربية وإنجليزية.</p>')


SLIDES = [
    R.cover(S, "كيف تختار خط<br>مشروعك؟", three(), "الخط يتكلم قبل أن يقرأ الزبون الكلمة. مثال من الخيال: محل «ياقوت»."),
    R.lesson(2, S, 1, "للخط شخصية", "الكلمة نفسها تبدو فاخرة بخط، ومرحة بخط، وجادة بخط آخر. اختر الشخصية قبل الخط.",
             visual=three(84, labels=False)),
    R.lesson(3, S, 2, "يشبه ما تبيعه", "محل مجوهرات: خط رشيق بحواف دقيقة. مطعم شعبي: خط ممتلئ ودافئ. عيادة: خط بسيط واضح.",
             example="«ياقوت» يبيع المجوهرات، فالخط الأول يشبهه أكثر.", example_label="في مثالنا"),
    R.lesson(4, S, 3, "يُقرأ وهو صغير", "جرّب الاسم بحجم صورة الحساب. إن لم يُقرأ، فلا يصلح وحده للاسم.", visual=avatars()),
    R.lesson(5, S, 4, "خطان على الأكثر", "خط للعنوان وخط للنص، أو خط واحد بأوزان مختلفة. أكثر من ذلك يربك العين.", visual=weights()),
    R.lesson(6, S, 5, "عربي وإنجليزي من عائلة واحدة", "اختر خطاً له حروف عربية وإنجليزية متشابهة، فيبدو اسمك باللغتين واحداً.", visual=bilingual()),
    R.closing("الحلقة القادمة", "أيّ خط يشبه<br>مشروعك؟", "اكتب رقمه في التعليقات: 1 الرشيق، 2 الممتلئ، 3 البسيط.",
              next_ep=("الحلقة 4", "أول 5 قطع يحتاجها محلّك الجديد"), visual=spacer(30) + three(60, labels=False)),
]
if __name__ == "__main__":
    build(HERE, SLIDES)
