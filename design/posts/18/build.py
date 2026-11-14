"""Post 18 (Mon 16 Nov 12:30): carousel «ملزمة الرياضيات المبسطة», 7 slides. Row 6, sage.
Pages from the booklet itself (assets/booklets/math, rendered from the PDF at 100 dpi). Free on request."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from kit2 import *  # noqa

R = row("sage", 7)
B = lambda n: page_img("math", n)
CH_ = "ملازمنا المجانية"
SLIDES = [
    R.cover(CH_, "ملزمة الرياضيات<br>المبسطة", R.sheets([B(1)], h=640, rot=(-3,)),
            "للثالث المهني، الفرع الصناعي: حاسوب وتقنية المعلومات. مجاناً."),
    R.visual(2, CH_, R.sheets([B(2), B(9)], h=700, rot=(-4, 4), gap=-120),
             "6 فصول في 35 صفحة", "القوانين الأساسية فقط، مع أمثلة محلولة، ومصمّمة لتدرس وحدك بلا أستاذ."),
    R.visual(3, CH_, R.crop_sheet(B(2), (.03, .02, .97, .40)),
             "كل قانون في مربع", "القانون أولاً، ثم معنى كل رمز بلون، ثم مثال محلول تحته."),
    R.visual(4, CH_, R.sheets([B(11)], h=700, rot=(3,)),
             "الرسم يشرح قبل الكلام", "القطوع المخروطية بالرسم: ترى الشكل، ثم تفهم المعادلة."),
    R.visual(5, CH_, R.sheets([B(8)], h=700, rot=(-3,)),
             "اختبر نفسك بعد كل فصل", "أسئلة قصيرة تتأكد بها أنك فهمت، قبل أن تنتقل إلى ما بعده."),
    R.visual(6, CH_, R.sheets([B(15), B(20), B(26)], h=700, rot=(-6, 0, 6), gap=-170),
             "من المشتقة إلى الاحتمالات", "الأعداد المركبة، والقطوع، والمشتقة، والتكامل، والهندسة الفراغية، والاحتمالات."),
    R.closing(CH_, "اكتب «رياضيات»<br>في التعليقات", "ونرسل لك الملزمة كاملة في الرسائل، ملف PDF مجاناً.",
              next_ep=("وعندنا أيضاً", "الطبيعيات · القواعد · صيانة الحاسوب"),
              visual=spacer(30) + R.sheets([page_img(b, 1) for b in ("comp", "gram", "phys")], h=330, rot=(-6, 0, 6), gap=-40),
              save="احفظ المنشور، وأرسله لزميلك في الصف."),
]
if __name__ == "__main__":
    build(HERE, SLIDES)
