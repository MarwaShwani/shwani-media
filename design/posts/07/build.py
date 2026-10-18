"""Post 07: carousel «مشروع التخرج خطوة بخطوة» الحلقة 1 — عنوان مشروعك في 3 أسئلة. 7 slides.

Row 3: teal base with milky text. Accents terracotta, dusty pink and sage (no mustard in this row:
Marwa found two colours pale and asked to drop the yellow, 15 Oct 2026).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from common import *  # noqa: F401,F403

ROW_BG, ROW_FG = TL, CH
N = 7
SERIES = "مشروع التخرج · الحلقة 1"
CARD = "rgba(242,233,216,.09)"
EDGE = "rgba(242,233,216,.24)"
DIM = "rgba(242,233,216,.62)"
Q_COL = [TE, RO, SG]                       # the three questions, same colours on every slide


def pg(body):
    return page(body, bg=ROW_BG, fg=ROW_FG)


def tip(text, label="جرّب", color=TE):
    return (f'<div class="z" style="border:3px solid {color};border-radius:32px;padding:26px 34px;display:flex;gap:22px;align-items:center">'
            f'<span style="flex-shrink:0;font-size:28px;font-weight:800;background:{color};color:{DK};border-radius:24px;padding:6px 20px">{label}</span>'
            f'<span style="flex:1;font-size:32px;font-weight:500;line-height:1.55;text-wrap:balance">{text}</span></div>')


def x_icon(size=40):
    return (f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 40 40" style="flex-shrink:0"><circle cx="20" cy="20" r="20" fill="{RO}"/>'
            f'<path d="M14 14l12 12M26 14L14 26" fill="none" stroke="{DK}" stroke-width="4" stroke-linecap="round"/></svg>')


def ok_icon(size=40, color=TE):
    return (f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 40 40" style="flex-shrink:0"><circle cx="20" cy="20" r="20" fill="{color}"/>'
            f'<path d="M12 20.5l5.5 5.5L28.5 14" fill="none" stroke="{DK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def num(k, color, size=56):
    return (f'<span class="ltr" style="flex-shrink:0;width:{size}px;height:{size}px;border-radius:{size // 2}px;background:{color};color:{DK};'
            f'display:flex;align-items:center;justify-content:center;font-size:{int(size * .52)}px;font-weight:800">{k}</span>')


def mark(text, color):
    return (f'<span style="text-decoration:underline;text-decoration-color:{color};text-decoration-thickness:7px;'
            f'text-underline-offset:14px;text-decoration-skip-ink:none">{text}</span>')


# ---------- slides ----------
def cover():
    big = ('<div class="z" style="position:relative;height:470px;display:flex;align-items:center">'
           f'<div aria-hidden="true" style="position:absolute;right:40px;top:170px;width:440px;height:150px;border-radius:75px;background:{TE}"></div>'
           f'<div aria-hidden="true" style="position:absolute;right:500px;top:120px;width:100px;height:100px;border-radius:50px;background:{RO}"></div>'
           f'<div aria-hidden="true" style="position:absolute;right:640px;top:290px;width:56px;height:56px;border-radius:28px;background:{SG}"></div>'
           f'<div class="ltr" style="position:relative;font-weight:800;font-size:420px;line-height:1;color:{CH};margin-right:120px">3</div></div>')
    body = (
        top(SERIES, 1, N)
        + spacer(70) + big + GROW
        + '<h1 style="font-size:100px;line-height:1.2">أسئلة تصنع<br>عنوان مشروعك</h1>'
        + spacer(28)
        + '<p style="font-size:36px;line-height:1.6">ومثال يُبنى أمامك خطوة بخطوة.</p>'
        + spacer(80) + bottom(arrow=TE)
    )
    return pg(body)


def s_topic():
    chips = "".join(f'<div style="display:flex;align-items:center;gap:18px;padding:22px 30px;border-radius:30px;background:{CARD};border:2px solid {EDGE}">'
                    f'{x_icon(46)}<span style="font-size:40px;font-weight:700">«{t}»</span></div>'
                    for t in ("الذكاء الاصطناعي", "التسويق الإلكتروني", "الطاقة الشمسية"))
    body = (
        top("أولاً", 2, N)
        + spacer(56)
        + f'<div class="z" style="display:flex;flex-direction:column;gap:18px">{chips}</div>'
        + spacer(56)
        + '<h1 style="font-size:66px">هذه مواضيع، لا عناوين</h1>'
        + spacer(18)
        + '<p style="font-size:34px;font-weight:400;line-height:1.65;text-wrap:balance">في كل واحد منها مئات البحوث. العنوان يقول ما ستفعله أنت بالضبط، وأين.</p>'
        + GROW + tip("إن كان عنوانك يصلح اسماً لكتاب، فهو موضوع، لا عنوان.", "قاعدة سهلة")
        + spacer(44) + bottom(arrow=TE)
    )
    return pg(body)


QUESTIONS = [("ماذا ستعمل؟", "تصمّم، تبني، تدرس، تقارن، تحلّل"),
             ("على ماذا؟", "تطبيق، نظام، جهاز، ظاهرة، مادة"),
             ("أين أو لمن؟", "مكان، فئة من الناس، فترة زمنية")]


def s_questions():
    cards = "".join(
        f'<div style="display:flex;align-items:center;gap:28px;padding:30px 34px;border-radius:32px;background:{CARD};border:3px solid {c}">'
        f'{num(k + 1, c, 76)}<div><div style="font-size:50px;font-weight:800">{q}</div>'
        f'<div style="font-size:31px;font-weight:400;color:{DIM};margin-top:8px">{ex}</div></div></div>'
        for k, ((q, ex), c) in enumerate(zip(QUESTIONS, Q_COL)))
    body = (
        top("القاعدة", 3, N)
        + spacer(60)
        + '<h1 style="font-size:70px;line-height:1.3">العنوان الجيد يجيب<br>عن ثلاثة أسئلة</h1>'
        + spacer(50)
        + f'<div class="z" style="display:flex;flex-direction:column;gap:22px">{cards}</div>'
        + GROW
        + '<p style="font-size:34px;font-weight:600;line-height:1.6">ركّب الأجوبة الثلاثة في جملة، وهذا هو عنوانك.</p>'
        + spacer(44) + bottom(arrow=TE)
    )
    return pg(body)


def s_ladder():
    rows = [
        (None, f'<span style="color:{DIM};text-decoration:line-through;text-decoration-thickness:3px">«التطبيقات الذكية»</span>', "الموضوع"),
        (0, f'«{mark("تصميم تطبيق", TE)}»', "ماذا ستعمل؟"),
        (1, f'«تصميم تطبيق {mark("لحجز المواعيد", RO)}»', "على ماذا؟"),
        (2, f'«تصميم تطبيق لحجز {mark("مواعيد عيادات الأسنان", SG)}»', "أين أو لمن؟"),
    ]
    html = ""
    for k, (qi, text, lab) in enumerate(rows):
        badge = (num(qi + 1, Q_COL[qi], 52) if qi is not None else
                 f'<span style="flex-shrink:0;width:52px;height:52px;border-radius:26px;border:3px dashed {EDGE}"></span>')
        last = k == len(rows) - 1
        html += (f'<div style="display:flex;align-items:center;gap:22px;padding:24px 28px;border-radius:28px;'
                 f'background:{"rgba(143,166,143,.22)" if last else CARD};border:{"3px solid " + SG if last else "2px solid " + EDGE}">{badge}'
                 f'<div style="flex:1"><div style="font-size:26px;font-weight:700;color:{DIM};margin-bottom:6px">{lab}</div>'
                 f'<div style="font-size:38px;font-weight:700;line-height:1.7">{text}</div></div>'
                 f'{ok_icon(46, SG) if last else ""}</div>')
        if k < len(rows) - 1:
            html += (f'<svg aria-hidden="true" width="34" height="30" viewBox="0 0 34 30" style="display:block;margin:2px auto">'
                     f'<path d="M17 3v22M7 16l10 10 10-10" fill="none" stroke="{DIM}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    body = (
        top("مثال", 4, N)
        + spacer(44)
        + '<h1 style="font-size:62px">عنوان يُبنى خطوة بخطوة</h1>'
        + spacer(34)
        + f'<div class="z">{html}</div>'
        + GROW
        + '<p style="font-size:34px;font-weight:600;line-height:1.6">كل سؤال يضيّق العنوان خطوة، حتى يصير مشروعاً تعرف أوله وآخره.</p>'
        + spacer(40) + bottom(arrow=TE)
    )
    return pg(body)


EXAMPLES = [("إدارة الأعمال", "التسويق الإلكتروني", "أثر إعلانات انستغرام في قرار الشراء لدى طلبة الجامعة"),
            ("الهندسة الكهربائية", "الطاقة الشمسية", "تصميم منظومة شمسية صغيرة لإنارة ممرات الكلية"),
            ("علوم الحاسوب", "الذكاء الاصطناعي", "نموذج يتعرّف على أصناف التمور من الصور"),
            ("التربية", "التعليم الإلكتروني", "أثر الاختبارات الإلكترونية القصيرة في تحصيل طلبة المتوسطة بالرياضيات")]


def s_majors():
    rows = "".join(
        f'<div style="padding:22px 28px;border-radius:28px;background:{CARD};border:2px solid {EDGE}">'
        f'<div style="display:flex;align-items:center;gap:14px;margin-bottom:10px">'
        f'<span style="font-size:27px;font-weight:800;color:{DK};background:{c};border-radius:20px;padding:4px 18px">{dept}</span>'
        f'<span style="font-size:29px;font-weight:600;color:{DIM};text-decoration:line-through;text-decoration-thickness:2px">«{bad}»</span></div>'
        f'<div style="font-size:34px;font-weight:700;line-height:1.5">«{good}»</div></div>'
        for (dept, bad, good), c in zip(EXAMPLES, (TE, RO, SG, TE)))
    body = (
        top("من تخصصك", 5, N)
        + spacer(44)
        + '<h1 style="font-size:62px">الفكرة نفسها في كل تخصص</h1>'
        + spacer(30)
        + f'<div class="z" style="display:flex;flex-direction:column;gap:16px">{rows}</div>'
        + GROW + spacer(24) + bottom(arrow=TE)
    )
    return pg(body)


def s_check():
    qs = ["هل تستطيع شرحه في جملة واحدة؟", "هل البيانات أو الأدوات متوفرة لك؟", "هل يكفيه الوقت المتاح؟", "هل هو 15 كلمة أو أقل؟"]
    rows = "".join(f'<div style="display:flex;align-items:center;gap:24px;padding:24px 0;{"border-top:2px solid " + EDGE + ";" if k else ""}">'
                   f'{num(k + 1, (TE, RO, SG, TE)[k], 60)}<span style="font-size:40px;font-weight:700;flex:1">{q}</span></div>'
                   for k, q in enumerate(qs))
    body = (
        top("قبل أن تعتمده", 6, N)
        + spacer(60)
        + '<h1 style="font-size:76px">أربعة أسئلة<br>قبل أن تعتمده</h1>'
        + spacer(36)
        + f'<div class="z">{rows}</div>'
        + GROW
        + tip("إن كان جواب أي سؤال «لا»، فعدّل العنوان، ثم اعرضه على مشرفك.", "تذكّر", RO)
        + spacer(44) + bottom(arrow=TE)
    )
    return pg(body)


def closing():
    body = (
        top("الحلقة القادمة", N, N)
        + deco(f"left:-130px;top:300px;width:330px;height:330px;border-radius:165px;background:{RO};opacity:.9")
        + deco(f"left:150px;top:560px;width:90px;height:90px;border-radius:45px;background:{SG}")
        + spacer(100)
        + '<h1 style="font-size:76px;line-height:1.35">ما موضوع<br>مشروعك؟</h1>'
        + spacer(24)
        + '<p style="font-size:36px;line-height:1.6">اكتبه في التعليقات بكلمتين.</p>'
        + spacer(50)
        + '<p style="font-size:32px;font-weight:400;line-height:1.65;text-wrap:balance;max-width:640px">نخطط معك ونحرّر وننسّق المراجع والعرض، والبحث يبقى عملك.</p>'
        + GROW
        + f'<div class="z" style="background:{TE};color:{DK};border-radius:36px;padding:38px 44px">'
          '<div style="font-size:30px;font-weight:600;margin-bottom:10px">الحلقة 2</div>'
          '<div style="font-size:48px;font-weight:800;line-height:1.4">كيف تكتب مقترح مشروعك</div></div>'
        + spacer(34)
        + '<p style="font-size:32px;font-weight:600;line-height:1.6">احفظ المنشور، وأرسله لزميلك في المرحلة الأخيرة.</p>'
        + spacer(44)
        + bottom(right_html=lockup_svg(250, CH))
    )
    return pg(body)


SLIDES = [cover(), s_topic(), s_questions(), s_ladder(), s_majors(), s_check(), closing()]

if __name__ == "__main__":
    render(HERE, SLIDES)
