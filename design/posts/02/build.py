"""Post 02: carousel «الخدمات والأسعار» — 6 slides (v2, after Marwa's notes)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from common import *  # noqa: F401,F403

N = 6


def tag(text, bg, fg, extra=""):
    return (f'<span class="z" style="display:inline-block;padding:18px 36px;border-radius:48px;background:{bg};color:{fg};'
            f'font-size:34px;font-weight:600;{extra}">{text}</span>')


def slide1():
    body = (
        top("الخدمات والأسعار", 1, N)
        + deco(f"left:-140px;top:180px;width:340px;height:340px;border-radius:170px;background:{MU}")
        + spacer(150)
        + '<h1 style="font-size:96px;line-height:1.25">أسعار واضحة<br>وباقات مرنة</h1>'
        + spacer(30)
        + '<p style="font-size:32px;line-height:1.7">تصميم خاص بك من الصفر، بلا قوالب جاهزة.<br>احفظ المنشور لترجع إليه حين تحتاجه.</p>'
        + GROW
        + '<div class="z" style="display:flex;flex-direction:column;align-items:flex-start;gap:20px">'
        + tag("للشركات والمؤسسات", TE, DK)
        + tag("للأفراد", RO, DK, "margin-right:90px")
        + tag("للطلاب والباحثين", TL, CH, "margin-right:40px")
        + '</div>'
        + GROW
        + bottom()
    )
    return page(body)


def pkg(name, who, items, price, bg, fg, border=None):
    style = f"background:{bg};color:{fg}" if not border else f"border:3px solid {border};color:{CH}"
    return (
        f'<div class="z" style="{style};border-radius:36px;padding:34px 38px;display:flex;gap:28px;align-items:center">'
        f'<div style="flex:1;display:flex;flex-direction:column;gap:8px">'
        f'<span style="font-size:40px;font-weight:800;line-height:1.3">{name}</span>'
        f'<span style="font-size:24px;font-weight:600;opacity:.85">{who}</span>'
        f'<span style="font-size:25px;font-weight:400;line-height:1.6;margin-top:6px">{items}</span></div>'
        f'<div style="flex-shrink:0;text-align:center;min-width:220px">'
        f'<div style="font-size:22px;font-weight:500">يبدأ من</div>'
        f'<div class="ltr" style="font-size:54px;font-weight:800;line-height:1.25">{price}</div>'
        f'<div style="font-size:24px;font-weight:500">دينار</div></div></div>'
    )


def slide2():
    body = (
        top("الهوية البصرية", 2, N)
        + spacer(56)
        + '<h1 style="font-size:72px">الهوية البصرية</h1>'
        + spacer(12)
        + '<p style="font-size:30px;line-height:1.7">ثلاث باقات، كل تصميم فيها يُرسم لك وحدك</p>'
        + spacer(44)
        + '<div style="display:flex;flex-direction:column;gap:22px">'
        + pkg("هوية بصرية كاملة", "شركات ومؤسسات · 7 إلى 10 أيام",
              "الشعار، الألوان والخطوط، دليل الهوية، تصاميم السوشيال&nbsp;ميديا", "250,000", TE, DK)
        + pkg("هوية شخصية", "أفراد ومستقلون · 3 إلى 5 أيام",
              "شعار شخصي، بطاقة عمل، تصاميم منشورات", "100,000", RO, DK)
        + pkg("شعار فقط", "مشاريع ناشئة · 5 أيام",
              "10&nbsp;مقترحات تختار منها، جولتا تعديل، ملفات بكل الصيغ", "25,000", None, None, border=TE)
        + '</div>'
        + GROW
        + bottom()
    )
    return page(body)


def item(text, dot, sub=None):
    s = f'<span style="font-size:23px;font-weight:400;opacity:.8;line-height:1.5">{sub}</span>' if sub else ""
    return (f'<div style="display:flex;gap:18px;align-items:flex-start;padding:26px 0;border-bottom:2px solid {LINE}">'
            f'<span style="flex-shrink:0;width:18px;height:18px;border-radius:9px;background:{dot};margin-top:14px"></span>'
            f'<span style="display:flex;flex-direction:column;gap:4px">'
            f'<span style="font-size:31px;font-weight:600;line-height:1.45">{text}</span>{s}</span></div>')


def grid(items):
    # RTL grid: the first item of each pair sits in the right column; rows align across columns
    return (f'<div class="z" style="display:grid;grid-template-columns:1fr 1fr;column-gap:40px;border-top:2px solid {LINE}">'
            + "".join(items) + '</div>')


def slide3():
    body = (
        top("للشركات والمؤسسات", 3, N)
        + spacer(56)
        + '<h1 style="font-size:72px">كل ما تحتاجه شركتك</h1>'
        + spacer(12)
        + '<p style="font-size:30px;line-height:1.7">تصاميم مطبوعة ورقمية بهوية واحدة</p>'
        + spacer(40)
        + grid([item("فلايرات وإعلانات", TE), item("مطبوعات وهدايا", RO, "دفاتر، تيشيرتات، أقلام، أكواب"),
                item("بنرات ولافتات", TE), item("الأوراق الرسمية", RO, "ترويسة، أظرف، بطاقات عمل"),
                item("كتيّبات وبروشورات", TE), item("دليل الميديا", RO),
                item("الملف التعريفي للشركة", TE), item("خطة نشر وتطوير الميديا", RO)])
        + GROW
        + f'<div class="z" style="background:{MU};color:{DK};border-radius:36px;padding:34px 40px">'
          '<div style="font-size:40px;font-weight:800;line-height:1.35;margin-bottom:10px">باقات مرنة للشركات</div>'
          '<div style="font-size:27px;font-weight:400;line-height:1.65;text-wrap:balance">تُعدَّل الأسعار بما يناسب متطلبات شركتك، والاتفاق المبرم بيننا، وحجم الخصم.</div></div>'
        + spacer(48)
        + bottom()
    )
    return page(body)


def slide4():
    body = (
        top("للأفراد", 4, N)
        + spacer(56)
        + '<h1 style="font-size:72px">تصاميم تحمل اسمك</h1>'
        + spacer(12)
        + '<p style="font-size:30px;line-height:1.7">لتظهر باحتراف في عملك ومناسباتك</p>'
        + spacer(40)
        + grid([item("شعار وهوية شخصية", RO), item("بطاقات الدعوة", SL, "أعراس، تخرّج، مناسبات"),
                item("بطاقات العمل", RO), item("حسابات التواصل", SL, "صورة الحساب، الهايلايت، المنشورات"),
                item("ملف الأعمال", RO, "بورتفوليو لعرض مشاريعك"), item("هدايا مطبوعة باسمك", SL, "تيشيرتات، أكواب، دفاتر"),
                item("العروض التقديمية", RO), item("السيرة الذاتية", SL, "وخطاب التغطية")])
        + GROW
        + f'<div class="z" style="background:{SL};color:{CH};border-radius:36px;padding:30px 40px;display:flex;flex-direction:column;gap:8px">'
          '<span style="font-size:26px;font-weight:500;line-height:1.6;text-wrap:balance">السيرة الذاتية من بوت تيليغرام مباشرة، بالعربية أو الإنجليزية أو باللغتين، خلال 24 ساعة. ابحث عن:</span>'
          '<span class="ltr" style="font-size:40px;font-weight:800;text-align:right">Sira_Thatiya_CV_bot</span></div>'
        + spacer(48)
        + bottom()
    )
    return page(body)


def check(text, color=SG):
    return (f'<div style="display:flex;align-items:center;gap:22px;font-size:32px;font-weight:500">'
            f'<svg aria-hidden="true" width="40" height="40" viewBox="0 0 40 40" style="flex-shrink:0"><circle cx="20" cy="20" r="20" fill="{color}"/>'
            f'<path d="M12 20.5l5.5 5.5L28.5 14" fill="none" stroke="{DK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            f'<span>{text}</span></div>')


def slide5():
    body = (
        top("للطلاب والباحثين", 5, N)
        + spacer(56)
        + '<h1 style="font-size:72px">البحوث والمشاريع<br>التقنية والأكاديمية</h1>'
        + spacer(40)
        + f'<div class="z" style="background:{TL};color:{CH};border-radius:36px;padding:36px 40px;display:flex;gap:24px;align-items:center">'
          '<div style="flex:1;display:flex;flex-direction:column;gap:12px">'
          '<span style="font-size:30px;font-weight:500;line-height:1.6">السعر يزيد حسب متطلبات المشروع<br>وعدد مرات التعديل</span>'
          f'<span style="align-self:flex-start;background:{SG};color:{DK};border-radius:30px;padding:10px 24px;font-size:26px;font-weight:800">التعديل الأول مجاني</span></div>'
          '<div style="flex-shrink:0;text-align:center;min-width:220px">'
          '<div style="font-size:22px;font-weight:500">يبدأ من</div>'
          '<div class="ltr" style="font-size:60px;font-weight:800;line-height:1.25">10,000</div>'
          '<div style="font-size:24px;font-weight:500">دينار</div></div></div>'
        + spacer(40)
        + '<div class="z" style="display:flex;flex-direction:column;gap:22px;padding-right:8px">'
        + check("خطة منظمة للمشروع")
        + check("تحرير لغوي")
        + check("تنسيق وتوثيق المراجع")
        + check("عرض تقديمي للمناقشة")
        + '</div>'
        + GROW
        + f'<div class="z" style="background:{SG};color:{DK};border-radius:36px;padding:30px 40px">'
          '<div style="font-size:26px;font-weight:800;margin-bottom:8px">حدودنا واضحة</div>'
          '<div style="font-size:27px;font-weight:400;line-height:1.6">نساعدك في التخطيط والتحرير والتنسيق والعرض،<br>ولا نكتب البحث بدلاً منك.</div></div>'
        + spacer(48)
        + bottom()
    )
    return page(body)


def slide6():
    body = (
        top("قبل أن تطلب", 6, N)
        + spacer(56)
        + '<h1 style="font-size:72px">اتفاق واضح من البداية</h1>'
        + spacer(48)
        + '<div class="z" style="display:flex;flex-direction:column;gap:30px;padding-right:8px">'
        + check("عرض مكتوب: ما يشمله العمل، والمدة، والسعر", MU)
        + check("عربون 50% والباقي عند التسليم", MU)
        + check("جولتا تعديل في تصاميم الهوية", MU)
        + check("ملفات جاهزة للطباعة والنشر بدقة عالية", MU)
        + '</div>'
        + deco(f"left:-90px;top:700px;width:380px;height:100px;border-radius:50px;background:{TE}")
        + deco(f"left:325px;top:705px;width:90px;height:90px;border-radius:45px;background:{RO}")
        + GROW
        + f'<div class="z" style="background:{PL};color:{CH};border-radius:36px;padding:36px 40px;position:relative;overflow:hidden">'
          f'<div aria-hidden="true" style="position:absolute;left:-60px;bottom:-80px;width:220px;height:220px;border-radius:110px;background:{MU}"></div>'
          '<div style="position:relative;font-size:26px;font-weight:600">عرض الإطلاق</div>'
          '<div style="position:relative;font-size:48px;font-weight:800;line-height:1.35;margin:6px 0 10px">خصم 30% لأول 10 عملاء</div>'
          '<div style="position:relative;font-size:26px;font-weight:400;line-height:1.6;max-width:720px">على الهوية والمشاريع، مقابل رأيك بعد التسليم.</div></div>'
        + spacer(36)
        + '<p style="font-size:30px;font-weight:600;line-height:1.6">راسلنا على الخاص بنوع خدمتك، ونرسل لك العرض مكتوباً.</p>'
        + spacer(44)
        + bottom(right_html=mark_inline(56))
    )
    return page(body)


if __name__ == "__main__":
    import glob
    for f in glob.glob(os.path.join(HERE, "slide-*")):
        os.remove(f)
    render(HERE, [slide1(), slide2(), slide3(), slide4(), slide5(), slide6()])
