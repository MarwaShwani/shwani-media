"""Post 03: carousel «كيف تطلب» — 5 slides."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from common import *  # noqa: F401,F403

N = 5


def path_graphic():
    # five numbered stops joined by a terracotta bridge
    stops = "".join(
        f'<span style="width:110px;height:110px;border-radius:55px;background:{MU if i == 5 else CH};color:{DK};'
        f'display:flex;align-items:center;justify-content:center;font-size:46px;font-weight:800;position:relative;z-index:2">{i}</span>'
        for i in range(1, 6))
    return (f'<div class="z" style="position:relative;display:flex;justify-content:space-between;align-items:center">'
            f'<div aria-hidden="true" style="position:absolute;left:40px;right:40px;top:50%;height:26px;margin-top:-13px;'
            f'border-radius:13px;background:{TE}"></div>{stops}</div>')


def slide1():
    body = (
        top("كيف تطلب", 1, N)
        + deco(f"left:-90px;top:500px;width:220px;height:220px;border-radius:110px;background:{SL}")
        + spacer(150)
        + '<h1 style="font-size:92px;line-height:1.25">من أول رسالة<br>إلى الملف النهائي</h1>'
        + spacer(30)
        + '<p style="font-size:32px;line-height:1.7">خمس خطوات واضحة،<br>بلا مفاجآت في السعر أو الموعد.</p>'
        + GROW
        + path_graphic()
        + GROW
        + bottom()
    )
    return page(body)


def step(num, title, text, last=False, color=MU):
    line = "" if last else (f'<div aria-hidden="true" style="position:absolute;right:52px;top:114px;bottom:-30px;width:6px;'
                            f'border-radius:3px;background:rgba(242,233,216,.25)"></div>')
    return (f'<div class="z" style="position:relative;display:flex;gap:34px;align-items:flex-start;padding-bottom:{0 if last else 72}px">'
            f'{line}<span style="flex-shrink:0;width:110px;height:110px;border-radius:55px;background:{color};color:{DK};'
            f'display:flex;align-items:center;justify-content:center;font-size:50px;font-weight:800">{num}</span>'
            f'<div style="display:flex;flex-direction:column;gap:14px;padding-top:12px">'
            f'<span style="font-size:50px;font-weight:800;line-height:1.3">{title}</span>'
            f'<span style="font-size:33px;font-weight:400;line-height:1.65">{text}</span></div></div>')


def slide2():
    body = (
        top("الخطوات 1 إلى 3", 2, N)
        + deco(f"left:-130px;bottom:130px;width:300px;height:300px;border-radius:150px;background:{RO}")
        + spacer(80)
        + step(1, "راسلنا على الخاص", "اكتب نوع الخدمة، وسطرين عن مشروعك،<br>ومتى تحتاجه.")
        + step(2, "نرسل لك العرض مكتوباً", "ما يشمله العمل، والمدة، والسعر،<br>وعدد جولات التعديل.")
        + step(3, "عربون 50% ونبدأ", "الدفع عبر زين كاش أو كي كارد،<br>وترسل لنا صورة الوصل.", last=True)
        + GROW
        + bottom()
    )
    return page(body)


def slide3():
    body = (
        top("الخطوات 4 و5", 3, N)
        + deco(f"left:-110px;top:720px;width:250px;height:250px;border-radius:125px;background:{SL}")
        + deco(f"left:170px;top:800px;width:180px;height:56px;border-radius:28px;background:{MU}")
        + spacer(80)
        + step(4, "ترى العمل وتعدّل", "جولتا تعديل في تصاميم الهوية،<br>والتعديل الأول مجاني في البحوث والمشاريع.")
        + step(5, "التسليم والدفعة الباقية", "ملفات احترافية جاهزة للطباعة والنشر<br>بصيغ <span class=\"ltr\">SVG</span> و<span class=\"ltr\">PNG</span> و<span class=\"ltr\">PDF</span>، مع دليل استخدام الهوية.", last=True)
        + GROW
        + f'<div class="z" style="background:{TE};color:{DK};border-radius:36px;padding:34px 40px">'
          '<div style="font-size:26px;font-weight:600;margin-bottom:8px">بعد التسليم</div>'
          '<div style="font-size:36px;font-weight:800;line-height:1.45">رشّحنا لصديق،<br>وطلبك القادم بخصم 25%.</div></div>'
        + spacer(48)
        + bottom()
    )
    return page(body)


def mini(num, text, bg, fg):
    return (f'<div class="z" style="flex:1;background:{bg};color:{fg};border-radius:32px;padding:36px 28px;display:flex;flex-direction:column;justify-content:space-between;gap:16px;min-height:330px">'
            f'<span class="ltr" style="font-size:64px;font-weight:800;line-height:1;text-align:right">0{num}</span>'
            f'<span style="font-size:31px;font-weight:600;line-height:1.5">{text}</span></div>')


def slide4():
    body = (
        top("السيرة الذاتية", 4, N)
        + spacer(80)
        + '<h1 style="font-size:76px;line-height:1.3">للسيرة الذاتية<br>طريق أقصر</h1>'
        + spacer(20)
        + '<p style="font-size:30px;line-height:1.7">بلا انتظار رد، من بوت تيليغرام مباشرة.</p>'
        + spacer(60)
        + '<div style="display:flex;gap:20px;align-items:stretch">'
        + mini(1, "افتح البوت<br>في تيليغرام", SL, CH)
        + mini(2, "أجب عن الأسئلة<br>وأكمل طلبك", TL, CH)
        + mini(3, "استلم سيرتك<br>خلال 24 ساعة", MU, DK)
        + '</div>'
        + GROW
        + f'<div class="z" style="border:3px solid {SL};border-radius:36px;padding:30px 40px;display:flex;flex-direction:column;gap:8px">'
          '<span style="font-size:25px;font-weight:400">ابحث في تيليغرام عن</span>'
          '<span class="ltr" style="font-size:44px;font-weight:800;text-align:right">Sira_Thatiya_CV_bot</span>'
          '<span style="font-size:24px;font-weight:400;opacity:.85">بصيغتي <span class="ltr">Word</span> و<span class="ltr">PDF</span>، بالعربية أو الإنجليزية أو باللغتين</span></div>'
        + spacer(48)
        + bottom()
    )
    return page(body)


def right_row(text):
    return (f'<div style="display:flex;gap:24px;align-items:flex-start;padding:34px 0;border-bottom:2px solid {LINE}">'
            f'<span style="flex-shrink:0;width:18px;height:18px;border-radius:9px;background:{MU};margin-top:17px"></span>'
            f'<span style="font-size:33px;font-weight:400;line-height:1.6">{text}</span></div>')


def slide5():
    body = (
        top("حقوقك", 5, N)
        + spacer(80)
        + '<h1 style="font-size:76px">حقوقك محفوظة</h1>'
        + spacer(36)
        + f'<div class="z" style="border-top:2px solid {LINE}">'
        + right_row("حقوق الشعار والهوية تنتقل إليك بعد الدفعة الأخيرة.")
        + right_row("نستخدم خطوطاً وصوراً مرخّصة للاستخدام التجاري فقط.")
        + right_row("بيانات سيرتك وبحثك لا تُنشر ولا تُشارك.")
        + right_row("نعرض عملك بإذنك فقط، ونخفي الأسماء والأرقام.")
        + '</div>'
        + deco(f"left:-70px;top:925px;width:160px;height:160px;border-radius:80px;background:{TE}")
        + deco(f"left:115px;top:975px;width:60px;height:60px;border-radius:30px;background:{MU}")
        + GROW
        + '<p style="font-size:44px;font-weight:800;line-height:1.4">ابدأ برسالة على الخاص.</p>'
        + spacer(56)
        + bottom(right_html=mark_inline(56))
    )
    return page(body)


if __name__ == "__main__":
    render(HERE, [slide1(), slide2(), slide3(), slide4(), slide5()])
