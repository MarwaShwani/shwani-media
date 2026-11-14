"""Post 19 (Mon 16 Nov 21:00): carousel «من أعمالنا: هوية المنار للمجوهرات», 10 slides. Row 7, charcoal with gold.
Marwa, 14 Nov: shown as our work only, without saying whether it was a client or a concept.
The scenes are AI-made (Instagram «AI info» label on, one line in the caption). Slide 2 is a second cover
(Instagram re-serves carousels from slide 2); the bags, the strongest photo after the logo, sit at the middle."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from kit2 import *  # noqa

R = row("charcoal", 10)
M = lambda n: A("almanar", n + ".jpg")
CH_ = "من أعمالنا"
PIECES = [
    ("02_logo_navy", "منارٌ في حرف الألف", "اسم المحل يعني الضوء الذي يهدي من بعيد، فصار الألف مناراً، وفي رأسه جوهرة.", (0, 0)),
    ("03_storefront", "الواجهة", "الاسم بالذهبي فوق الزجاج، يُقرأ من آخر الممر.", (0, -.75)),
    ("04_wall", "خلف الكاونتر", "الشعار نفسه على الرخام، فيبقى في صورة كل زبون يتصوّر هنا.", (0, -.55)),
    ("05_cards", "بطاقة العمل", "وجه حليبي بالذهب، ووجه كحلي بالمعلومات.", (0, 0)),
    ("06_bags", "الأكياس", "الزبون يحمل اسم المحل في الشارع بعد أن يخرج.", (0, .1)),
    ("07_receipt", "دفتر الفواتير", "حتى الورقة التي يوقّعها الزبون تحمل الهوية.", (0, 0)),
    ("08_stationery", "الأوراق وشهادة الأصالة", "رسالة، وظرف بختم ذهبي، وشهادة تثبت أن القطعة أصلية.", (0, 0)),
    ("09_packaging", "العلبة والكيس المخملي", "أول ما يلمسه الزبون حين يفتح هديته.", (0, 0)),
]
SLIDES = [R.cover(CH_, "هوية «المنار»<br>للمجوهرات", R.band(M("01_logo"), h=660, shift=(0, .05)),
                  "من الشعار إلى العلبة، قطعة قطعة.")]
for i, (img, t, txt, sh) in enumerate(PIECES, 2):
    SLIDES.append(R.visual(i, CH_, R.band(M(img), badge=i, shift=sh), t, txt))
SLIDES.append(R.closing("الحلقة القادمة", "أيّ قطعة تريدها<br>لمحلّك؟", "اكتب رقم شريحتها في التعليقات، ونخبرك كيف نصمّمها لك.",
                        next_ep=("من الفكرة إلى الشعار 2", "كيف صار اسم «المنار» رمزاً؟"),
                        save="احفظ المنشور، وأرسله لصاحب محل جديد.",
                        visual=spacer(36) + R.band(M("10_giftbox"), h=350, inset=True, radius=30)))
assert len(SLIDES) == 10
if __name__ == "__main__":
    build(HERE, SLIDES)
