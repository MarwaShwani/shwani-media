"""Post 27 (Fri 20 Nov 21:00): carousel «تذاكر وحدك؟ 5 خطوات تجعل الملزمة تكفيك», 7 slides. Row 9, teal.
Study habits for students on their own (spaced review, testing yourself), told in everyday words, no figures."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from kit2 import *  # noqa

R = row("teal", 7)
S = "للطلاب"
steps = ('<div class="z" style="display:flex;gap:18px;align-items:center">' + f'<span style="flex-grow:1;height:6px;background:{RO};border-radius:3px"></span>'.join(
    f'<span class="card" style="padding:22px 30px;font-size:34px;font-weight:800;white-space:nowrap">{w}</span>' for w in ("اليوم", "بعد يوم", "بعد أسبوع")) + '</div>')
SLIDES = [
    R.cover(S, "تذاكر وحدك<br>بلا أستاذ؟", R.sheets([page_img("phys", 6), page_img("math", 2)], h=620, rot=(-5, 4), gap=-110),
            "5 خطوات تجعل الملزمة تكفيك."),
    R.lesson(2, S, 1, "الفكرة قبل القانون", "اقرأ سطر «الفكرة باختصار» أولاً، فتعرف لماذا تحفظ القانون قبل أن تحفظه.",
             visual=R.crop_sheet(page_img("gram", 4), (.03, .03, .97, .245))),
    R.lesson(3, S, 2, "غطِّ الحل، وحلّ وحدك", "حلّ المثال على ورقة، ثم قارن حلّك بالحل المكتوب خطوة خطوة.",
             visual=R.crop_sheet(page_img("math", 3), (.05, .18, .97, .62))),
    R.lesson(4, S, 3, "اختبر نفسك في آخر الدرس", "إن أخطأت في سؤال، ارجع إلى فقرته فقط، لا إلى الدرس كله.",
             visual=R.crop_sheet(page_img("math", 8), (.04, .04, .96, .56))),
    R.lesson(5, S, 4, "الوزاري المتكرر أولاً", "السؤال الذي تكرّر كثيراً في الامتحانات السابقة يستحق وقتك قبل غيره.",
             visual=R.crop_sheet(page_img("phys", 17), (.03, .03, .97, .42))),
    R.lesson(6, S, 5, "راجع بعد يوم، ثم بعد أسبوع", "مراجعات قصيرة متباعدة تثبّت المعلومة أكثر من قراءة واحدة طويلة.",
             visual=steps),
    R.closing(S, "أيّ ملزمة تريد؟", "اكتب اسم المادة في التعليقات: رياضيات، طبيعيات، قواعد، صيانة حاسوب. ونرسلها لك مجاناً.",
              save="احفظ المنشور، وأرسله لزميلك في الصف."),
]
if __name__ == "__main__":
    build(HERE, SLIDES)
