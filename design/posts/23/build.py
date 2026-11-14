"""Post 23 (Wed 18 Nov 21:00): carousel «سيرتك وخطاب التغطية من هاتفك» (the Telegram CV bot), 6 slides. Row 8, slate.
No price (the bot asks for it itself). Bot name written without @ (Instagram would link it to an Instagram account).
The chat on slide 1 is an illustration, not a screenshot: Marwa checks the steps match the bot."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from kit2 import *  # noqa

R = row("slate", 6)
CH_ = "السيرة الذاتية"
BOT = "Sira_Thatiya_CV_bot"


def bubble(text, me=False):
    side = "flex-end" if me else "flex-start"
    bg, fg = (TL, CH) if me else ("#FFFFFF", DK)
    return (f'<div style="display:flex;justify-content:{side}"><div style="max-width:640px;background:{bg};color:{fg};'
            f'border-radius:28px;padding:18px 28px;font-size:32px;font-weight:500;line-height:1.5">{text}</div></div>')


chat = (f'<div class="z card" style="padding:30px 32px;display:flex;flex-direction:column;gap:16px;background:#E9EEF2">'
        + bubble("أهلاً! ما اسمك الكامل؟") + bubble("حسين أحمد", True)
        + bubble("ما الوظيفة التي تتقدّم لها؟") + bubble("مهندس برمجيات", True)
        + f'<div style="display:flex;justify-content:flex-start"><div style="display:flex;align-items:center;gap:18px;background:#fff;'
          f'border-radius:28px;padding:16px 26px;font-size:30px;font-weight:700;color:{DK}">'
          f'<span style="background:{TE};color:{DK};border-radius:12px;padding:8px 14px;font-size:26px">PDF</span>سيرتك وخطاب التغطية</div></div>'
        + '</div>')
handle = f'<div class="card z ltr" style="padding:30px 36px;font-size:46px;font-weight:800;text-align:center">{BOT}</div>'
SLIDES = [
    R.cover(CH_, "سيرتك وخطاب التغطية<br>من هاتفك", chat, "بوت في تيليغرام يسألك، ويكتب سيرتك.", size=78),
    R.lesson(2, CH_, 1, "ابحث عن البوت", "افتح تيليغرام، واكتب اسمه في البحث:", visual=handle),
    R.lesson(3, CH_, 2, "أجب عن أسئلته", "اسمك، ودراستك، وخبرتك، ومهاراتك، سؤالاً بعد سؤال، بكلماتك.",
             example="لا تحتاج حاسوباً ولا برنامج تصميم: الهاتف يكفي.", example_label="ملاحظة"),
    R.lesson(4, CH_, 3, "استلم ملفك", "يصلك ملف سيرتك، ومعه خطاب التغطية للوظيفة التي تريدها، جاهزين للإرسال."),
    R.points(5, CH_, "جهّز قبل أن تبدأ", [("آخر عملين أو تدريبين", "اسم المكان، والسنة، وماذا فعلت فيه."),
                                         ("شهادتك وسنة تخرجك", "والمعدّل إن كان جيداً."),
                                         ("3 مهارات تعرفها فعلاً", "برامج، أو لغات، أو أجهزة تجيد استعمالها.")]),
    R.closing(CH_, "سيرتك جاهزة اليوم", f'ابحث في تيليغرام عن: <span class="ltr" style="font-weight:800">{BOT}</span>',
              save="احفظ المنشور، وأرسله لمن يبحث عن عمل."),
]
if __name__ == "__main__":
    build(HERE, SLIDES)
