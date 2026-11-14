"""Post 26 (Fri 20 Nov 12:30): carousel «مشروع التخرج 2: كيف تكتب مقترح مشروعك», 7 slides. Row 9, teal.
Keeps the promise of post 7. Limits of academic help (project file): planning, editing, formatting, references
and presentation; we never write the research instead of the student. Example project is invented."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from kit2 import *  # noqa

R = row("teal", 7)
S = "مشروع التخرج · الحلقة 2"
heads = ["العنوان", "المشكلة", "الهدف", "الطريقة والأدوات", "الخطة الزمنية"]
doc = ('<div class="card z" style="padding:40px 46px;display:flex;flex-direction:column;gap:20px">'
       '<div style="font-size:34px;font-weight:800">مقترح مشروع التخرج</div>'
       + "".join(f'<div style="display:flex;align-items:center;gap:20px"><span style="width:14px;height:14px;border-radius:7px;background:{TE};flex-shrink:0"></span>'
                 f'<span style="font-size:32px;font-weight:700;width:270px;flex-shrink:0">{h}</span>'
                 f'<span style="flex-grow:1;height:14px;border-radius:7px;background:rgba(32,33,38,.12)"></span></div>' for h in heads)
       + '</div>')
plan = ('<div class="card z" style="padding:30px 36px;margin-top:40px;display:flex;flex-direction:column;gap:14px;font-size:32px;line-height:1.5">'
        + "".join(f'<div style="display:flex;gap:20px"><b style="width:220px;flex-shrink:0;color:{TE}">{w}</b><span>{t}</span></div>'
                  for w, t in [("الأسبوع 1-2", "القراءة والاستبيان"), ("الأسبوع 3-6", "البناء"), ("الأسبوع 7-8", "التجربة والكتابة")])
        + '</div>')
SLIDES = [
    R.cover(S, "كيف تكتب مقترح<br>مشروعك؟", doc, "صفحة واحدة تقنع المشرف قبل أن تبدأ."),
    R.lesson(2, S, 1, "العنوان", "فكرة واضحة في سطر واحد، كما في الحلقة 1.",
             example="تطبيق لحجز مواعيد عيادة صغيرة", example_label="مثال من الخيال"),
    R.lesson(3, S, 2, "المشكلة", "ما الذي لا يعمل اليوم؟ ومن يتضرّر منه؟ في ثلاثة أسطر.",
             example="المراجع ينتظر ساعة، لأن المواعيد تُكتب على ورق."),
    R.lesson(4, S, 3, "الهدف", "ماذا ستصنع بالضبط في نهاية المشروع؟ شيء يُرى ويُجرَّب.",
             example="تطبيق يحجز الموعد، ويذكّر المراجع قبله بيوم."),
    R.lesson(5, S, 4, "الطريقة والأدوات", "كيف ستعمل، وبأي برامج أو أجهزة، ومن أين تأتي بالمعلومات.",
             example="استبيان لثلاثين مراجعاً، ثم بناء التطبيق وتجربته في العيادة."),
    R.lesson(6, S, 5, "الخطة الزمنية", "قسّم الفصل إلى أسابيع، ولكل أسبوع مهمة واحدة.", visual=plan),
    R.closing("الحلقة القادمة", "مقترحك في صفحة واحدة", "العنوان، ثم المشكلة، ثم الهدف، ثم الطريقة، ثم الخطة.",
              next_ep=("الحلقة 3", "كيف تكتب مراجعك"),
              save="نساعدك في التخطيط والتنسيق والمراجع، ولا نكتب البحث بدلاً منك. احفظه، وأرسله لطالب في سنته الأخيرة."),
]
if __name__ == "__main__":
    build(HERE, SLIDES)
