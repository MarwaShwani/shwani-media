"""Marketing print: A5 flyer, A4 tri-fold brochure, 8-page company profile, roll-up, shop sign, outdoor banner.
Large formats are drawn at 1:10 (vector PDF, scale up 10x at the printer).
Run: python3 brand/printwork.py [names...]"""
from kit import *  # noqa: F401,F403

SOFT = "#F9F5EE"   # card on milky
FOLD = "rgba(32,33,38,.18)"


def chip(text, color=CH, size="2.6mm"):
    return (f'<span style="display:inline-block;border:.35mm solid {color};color:{color};border-radius:10mm;'
            f'padding:1.1mm 3.2mm;font-size:{size};font-weight:500;line-height:1.3">{text}</span>')


def kicker(text, color=TE, size="2.7mm"):
    return f'<div style="color:{color};font-size:{size};font-weight:600;margin-bottom:1.4mm">{text}</div>'


# ---------------------------------------------------------------- A5 flyer 148x210

def flyer():
    cards = ""
    order = [1, 0, 3, 2, 5, 4]   # grid is LTR, so the first service sits on the right
    for k in order:
        key, ic, col, title, line, _ = SERVICES[k]
        cards += f'''<div style="direction:rtl;background:{SOFT};border-radius:4.6mm;border-top:1.05mm solid {col};padding:4.2mm 4.3mm 3.6mm;min-height:23.6mm">
  <div style="display:flex;align-items:center;gap:2.6mm;flex-direction:row-reverse;justify-content:flex-end">
    <div style="font-size:3.55mm;font-weight:700;line-height:1.25;text-align:right">{title}</div>{icon(ic, "6.2mm", DK, 1.8)}</div>
  <div style="font-size:2.55mm;line-height:1.6;color:#45464C;margin-top:2.2mm;text-align:right">{line}</div></div>'''
    body = (
        f'<div class="abs" style="right:11.3mm;top:11.4mm">{logo("39.5mm", DK, TE)}</div>'
        + pill("36.8mm", "8.8mm", TE, "left:-3mm;top:20.2mm")
        + dot("5.9mm", MU, "left:36.7mm;top:21.65mm")
        + f'<div class="abs" style="right:11.3mm;top:34.4mm;text-align:right">'
          f'<div style="font-size:9.2mm;font-weight:800;line-height:1.15">فكرتك تستحق<br>هوية تليق بها</div>'
          f'<div style="font-size:3.2mm;color:#55565C;margin-top:3.2mm">تصميم خاص من الصفر، واتفاق مكتوب من البداية.</div></div>'
        + f'<div class="abs" style="left:10.8mm;right:11.2mm;top:75mm;display:grid;grid-template-columns:1fr 1fr;gap:3.1mm;direction:ltr">{cards}</div>'
        + f'''<div class="abs" style="left:-3mm;right:-3mm;top:183.3mm;bottom:-3mm;background:{DK};color:{CH}">
  <div class="abs" style="right:14.3mm;top:8.4mm;text-align:right"><div style="font-size:4.7mm;font-weight:700">راسلنا بنوع خدمتك</div>
    <div style="font-size:2.7mm;color:{CH_DIM};margin-top:1mm">نرسل لك العرض مكتوباً.</div></div>
  <div class="abs" style="left:13.8mm;top:8.6mm">{contact("2.75mm", CH, CH_DIM, TE, "1.6mm", align="flex-end")}</div>
</div>'''
    )
    return Piece("flyer-a5", 148, 210, body, bg=CH, fg=DK)


# ---------------------------------------------------------------- A4 tri-fold 297x210 (panels 99 mm)

def panel(x, bg, inner, w=99, extra=""):
    return f'<div class="abs" style="left:{x}mm;top:-3mm;bottom:-3mm;width:{w}mm;background:{bg};{extra}"><div class="abs" style="left:0;right:0;top:3mm;bottom:3mm">{inner}</div></div>'


def folds():
    return "".join(f'<div class="abs" style="left:{x}mm;top:0;bottom:0;border-left:.25mm dashed {FOLD}"></div>' for x in (99, 198))


def brochure_outside():
    cover = (
        f'<div class="abs" style="inset:-3mm;{pattern(20, CH, TE, CH, MU, .10)}"></div>'
        f'<div class="abs" style="right:10mm;top:11.9mm">{chip("خدماتنا")}</div>'
        + pill("41mm", "9.8mm", TE, "left:-3mm;top:44mm") + dot("6.4mm", MU, "left:41.9mm;top:45.7mm")
        + f'<div class="abs" style="right:10mm;top:78.7mm">{logo("67.5mm", CH, TE)}</div>'
        + f'<div class="abs" style="right:10mm;top:115mm;font-size:5.3mm;font-weight:700;line-height:1.35;text-align:right;color:{CH}">نبني الجسر بين فكرتك<br>والنتيجة</div>'
        + f'<div class="abs" style="right:10mm;top:191.5mm;font-size:2.55mm;color:{CH_DIM}">{LINE_AR}</div>'
    )
    back = (
        f'<div class="abs" style="left:0;right:0;top:22.6mm;display:flex;justify-content:center">{sh("14.5mm", DK, TE)}</div>'
        f'<div class="abs" style="left:0;right:0;top:44.5mm;text-align:center"><div style="font-size:5.2mm;font-weight:700">راسلنا</div>'
        f'<div style="font-size:2.9mm;color:{GREY};line-height:1.65;margin-top:1.4mm">بنوع الخدمة، وسطرين عن مشروعك،<br>ومتى تحتاجه.</div></div>'
        f'<div class="abs" style="right:12.7mm;top:77.5mm">{contact("2.85mm", DK, GREY, TE, "3.3mm", place=False)}'
        f'<div style="display:flex;align-items:center;gap:1.8mm;font-size:2.85mm;margin-top:3.3mm;white-space:nowrap">{icon("send", "3.55mm", TE)}'
        f'<span class="en" style="font-weight:600">{CV_BOT}</span><span style="color:{GREY}">السيرة الذاتية · تيليغرام</span></div>'
        f'<div style="display:flex;align-items:center;gap:1.8mm;font-size:2.85mm;margin-top:3.3mm">{icon("pin", "3.55mm", TE)}<span style="color:{GREY}">{PLACE}</span></div></div>'
        f'<div class="abs" style="left:10.3mm;right:10.4mm;top:178.6mm;border:.35mm solid {TE};border-radius:3.6mm;padding:3.3mm 4.3mm;font-size:2.85mm;line-height:1.65;text-align:right">'
        f'<b style="color:{TE}">خدمات تقنية أخرى؟</b> أخبرنا بما تحتاجه، نراجع إمكانية تنفيذه ونتواصل معك.</div>'
    )
    items = "".join(
        f'<div style="display:flex;align-items:center;gap:3mm;padding:2.45mm 0;border-bottom:.25mm solid rgba(242,233,216,.22);font-size:3.05mm">'
        f'<span style="width:2.6mm;height:2.6mm;border-radius:50%;background:{c};flex-shrink:0"></span><span>{t}</span></div>' for t, c in DELIVERABLES)
    flap = (
        f'<div class="abs" style="right:10.1mm;left:10mm;top:17.4mm;text-align:right;color:{CH}">'
        f'{kicker("باقة الهوية الكاملة", TE, "2.6mm")}<div style="font-size:5.5mm;font-weight:700;line-height:1.3">ماذا تستلم<br>في نهاية العمل؟</div>'
        f'<div style="margin-top:6mm">{items}</div>'
        f'<div style="font-size:2.6mm;color:{CH_DIM};line-height:1.6;margin-top:6mm">حقوق الشعار تنتقل إليك بعد الدفعة الأخيرة، وبياناتك لا تُنشر ولا تُشارك.</div></div>'
    )
    body = panel(-3, DK, cover, 102, "color:" + CH) + panel(99, CH, back) + panel(198, TL, flap, 102) + folds()
    return Piece("brochure-trifold-outside", 297, 210, body, bg=CH, fg=DK)


def brochure_inside():
    steps = "".join(
        f'<div style="display:flex;gap:3.4mm;align-items:flex-start;margin-bottom:5.2mm">'
        f'<span class="en" style="width:8mm;height:8mm;border-radius:50%;background:{c};color:{DK};font-weight:700;font-size:2.9mm;'
        f'display:flex;align-items:center;justify-content:center;flex-shrink:0">{i}</span>'
        f'<div><div style="font-size:3.5mm;font-weight:700;color:{CH}">{t}</div><div style="font-size:2.55mm;color:{CH_DIM};line-height:1.55;margin-top:.6mm">{d}</div></div></div>'
        for i, (t, d, c) in enumerate(STEPS, 1))
    how = (
        f'<div class="abs" style="right:10mm;left:9mm;top:16mm;text-align:right">{kicker("كيف نعمل", TE, "2.6mm")}'
        f'<div style="font-size:5.5mm;font-weight:700;line-height:1.3;color:{CH}">من أول رسالة<br>إلى الملف النهائي</div>'
        f'<div style="margin-top:8mm">{steps}</div></div>'
        + pill("31mm", "6.7mm", TE, "left:-3mm;top:189mm") + dot("4.5mm", MU, "left:31.2mm;top:190.1mm")
    )
    rows = "".join(
        f'<div style="display:flex;gap:3.4mm;align-items:flex-start;padding:2.7mm 0 2.6mm;border-bottom:.25mm solid {RULE}">'
        f'{badge(ic, col, "8.9mm", DK if col not in (TL, SL) else CH)}'
        f'<div style="text-align:right"><div style="font-size:3.45mm;font-weight:700">{title}</div>'
        f'<div style="font-size:2.45mm;color:#55565C;line-height:1.55;margin-top:.5mm">{line}</div></div></div>'
        for key, ic, col, title, line, _ in SERVICES)
    services = (
        f'<div class="abs" style="right:9.3mm;left:8.5mm;top:13.6mm;text-align:right">{kicker("خدماتنا", TE, "2.6mm")}'
        f'<div style="font-size:5.5mm;font-weight:700;line-height:1.3">ستّ خدمات، وطريقة واحدة</div>'
        f'<div style="margin-top:4mm">{rows}</div></div>'
    )
    about = (
        f'<div class="abs" style="right:10.1mm;left:10mm;top:16mm;text-align:right">{kicker("من نحن", TE, "2.6mm")}'
        f'<div style="font-size:5.6mm;font-weight:700;line-height:1.3">في قلب اسمنا جسر</div></div>'
        f'<div class="abs" style="left:0;right:0;top:37.7mm;display:flex;justify-content:center">{bridge("23.8mm", DK, TE)}</div>'
        f'<div class="abs" style="left:15mm;right:15mm;top:66.5mm;display:flex;justify-content:space-between;font-size:2.6mm;color:{GREY}">'
        f'<span>المشكلة</span><span style="color:{TE};font-weight:600">الحل</span><span>النتيجة</span></div>'
        f'<div class="abs" style="right:10.1mm;left:9.5mm;top:76mm;text-align:right;font-size:3mm;line-height:1.85">'
        f'<p>ركيزتا حرف <span class="en">H</span> هما المشكلة التي تأتينا بها والنتيجة التي تريدها، والوصلة بينهما هي الحل الذي نبنيه معك.</p>'
        f'<p style="margin-top:3mm"><span class="en">SHWANI COMPANY</span> استوديو تصميم وخدمات تقنية في العراق. كل تصميم نصنعه خاص بك من الصفر، بلا قوالب جاهزة.</p></div>'
    )
    body = panel(-3, DK, how, 102) + panel(99, SOFT, services) + panel(198, CH, about, 102) + folds()
    return Piece("brochure-trifold-inside", 297, 210, body, bg=CH, fg=DK)


# ---------------------------------------------------------------- company profile, A4, 8 pages

def pnum(n, color=GREY2):
    return f'<div class="abs en" style="left:14mm;bottom:12mm;font-size:2.5mm;color:{color}">0{n}</div>'


def profile_cover():
    body = (
        f'<div class="abs" style="inset:-3mm;{pattern(26, CH, TE, CH, MU, .09)}"></div>'
        f'<div class="abs" style="left:14mm;top:92mm">{word("182mm", "#2B2C33", TE)}</div>'
        f'<div class="abs" style="right:14mm;top:13.5mm">{chip("الملف التعريفي · <span class=en>2026</span>", CH, "2.5mm")}</div>'
        + dot("10mm", RO, "left:116.5mm;top:24.5mm") + pill("40mm", "12.5mm", MU, "left:171mm;top:23.3mm")
        + f'<div class="abs" style="right:14mm;top:203mm">{logo("68mm", CH, TE)}</div>'
        + f'<div class="abs" style="right:14mm;top:241.5mm;font-size:5.2mm;font-weight:700;color:{CH}">{TAG_AR}</div>'
        + f'<div class="abs" style="right:14mm;top:251.5mm;font-size:2.7mm;color:{CH_DIM}">{LINE_AR}</div>'
        + f'<div class="abs" style="right:14mm;top:268.5mm">{contact("2.4mm", CH, CH_DIM, TE, "1.1mm")}</div>'
    )
    return Piece("profile-01-cover", 210, 297, body, bg=DK, fg=CH)


def profile_about():
    card = (f'<div class="abs" style="left:14mm;right:14mm;top:98mm;height:62mm;border-radius:5mm;background:{DK};color:{CH};overflow:hidden">'
            f'<div class="abs" style="inset:0;{pattern(16, CH, TE, CH, MU, .08)}"></div>'
            f'<div class="abs" style="right:10mm;top:13mm">{bridge("27mm", CH, TE)}</div>'
            f'<div class="abs" style="right:7mm;top:44mm;width:32mm;display:flex;justify-content:space-between;font-size:2.3mm;color:{CH_DIM}">'
            f'<span>المشكلة</span><span style="color:{TE}">الحل</span><span>النتيجة</span></div>'
            f'<div class="abs" style="right:48mm;left:10mm;top:17mm;text-align:right"><div style="font-size:4.8mm;font-weight:700">في قلب اسمنا جسر</div>'
            f'<div style="font-size:2.85mm;line-height:1.85;color:{CH_DIM};margin-top:3mm">ركيزتا حرف <span class="en">H</span> هما المشكلة التي تأتينا بها والنتيجة التي تريدها، '
            f'والوصلة بينهما، بلون التيراكوتا، هي الحل الذي نبنيه معك.</div></div></div>')
    body = (
        f'<div class="abs" style="right:14mm;left:14mm;top:22mm;text-align:right">{kicker("من نحن")}'
        f'<div style="font-size:8.4mm;font-weight:800;line-height:1.25">استوديو تصميم<br>وخدمات تقنية في العراق</div>'
        f'<div style="font-size:3.25mm;line-height:1.95;color:#45464C;margin-top:6mm">نصمّم الهوية البصرية للشركات والمؤسسات والأفراد، ونكتب السِّيَر الذاتية بالعربية والإنجليزية، '
        f'ونساعد في تخطيط المشاريع التقنية والأكاديمية وتحريرها وتنسيقها. كل تصميم نصنعه خاص بصاحبه، من الصفر، بلا قوالب جاهزة.</div></div>'
        + card
        + f'<div class="abs" style="right:14mm;left:14mm;top:236mm;text-align:right;font-size:7mm;font-weight:800;color:{TE};line-height:1.3">«{TAG_AR}»</div>'
        + f'''<div class="abs" style="left:14mm;right:14mm;top:178mm;display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;direction:ltr">
{"".join(f'<div style="direction:rtl;text-align:right;border-top:.9mm solid {c};padding-top:3.5mm"><div style="font-size:3.6mm;font-weight:700">{t}</div><div style="font-size:2.65mm;line-height:1.7;color:#55565C;margin-top:1.3mm">{d}</div></div>'
         for t, d, c in [("رؤيتنا", "أن يجد كل مشروع في العراق هوية واضحة تشبهه، مهما كان حجمه.", SG),
                         ("رسالتنا", "نحوّل فكرتك إلى نتيجة تراها وتستعملها، بخطوات واضحة واتفاق مكتوب.", MU),
                         ("قيمنا", "الوضوح، والعمل من الصفر، واحترام الموعد، وحفظ بيانات العميل.", TE)][::-1])}
</div>'''
        + pill("33mm", "6.5mm", TE, "left:-3mm;top:268mm") + dot("4.6mm", MU, "left:34mm;top:268.95mm")
        + pnum(2)
    )
    return Piece("profile-02-about", 210, 297, body, bg=CH, fg=DK)


def profile_why():
    why = [("pen", TE, "تصميم من الصفر", "كل عمل خاص بك، بلا قوالب جاهزة ولا نسخ من غيرك."),
           ("doc", MU, "اتفاق مكتوب", "ما يشمله العمل والمدة والسعر، مكتوبة قبل أن نبدأ."),
           ("chat", RO, "جولتا تعديل", "في تصاميم الهوية، والتعديل الأول مجاني في المشاريع."),
           ("box", SL, "ملفات جاهزة", "بكل الصيغ التي تحتاجها للطباعة والنشر."),
           ("star", TL, "الحقوق لك", "حقوق الشعار تنتقل إليك بعد الدفعة الأخيرة."),
           ("check", SG, "بياناتك محفوظة", "لا تُنشر ولا تُشارك مع أحد.")]
    cells = "".join(
        f'<div style="direction:rtl;text-align:right;background:rgba(242,233,216,.06);border:.3mm solid rgba(242,233,216,.12);border-radius:5mm;padding:8mm 7mm 8mm;min-height:52mm">'
        f'{badge(ic, c, "13mm", DK if c not in (TL, SL) else CH)}<div style="font-size:4.8mm;font-weight:700;margin-top:5mm">{t}</div>'
        f'<div style="font-size:3.3mm;line-height:1.75;color:{CH_DIM};margin-top:2mm">{d}</div></div>' for ic, c, t, d in why)
    body = (
        f'<div class="abs" style="inset:-3mm;{pattern(26, CH, TE, CH, MU, .06)}"></div>'
        f'<div class="abs" style="right:14mm;left:14mm;top:22mm;text-align:right">{kicker('لماذا <span class="en">SHWANI</span>؟')}'
        f'<div style="font-size:8.4mm;font-weight:800;line-height:1.25">ستة أشياء<br>تعرفها قبل أن تبدأ</div></div>'
        f'<div class="abs" style="left:14mm;right:14mm;top:76mm;display:grid;grid-template-columns:1fr 1fr;gap:6mm;direction:ltr">{cells}</div>'
        + pnum(3, CH_DIM)
    )
    return Piece("profile-03-why", 210, 297, body, bg=DK, fg=CH)


def svc_block(s, last=False):
    key, ic, col, title, line, det = s
    bullets = "".join(f'<div style="display:flex;gap:2.4mm;align-items:baseline;font-size:3.2mm;line-height:1.9">'
                      f'<span style="width:1.7mm;height:1.7mm;border-radius:50%;background:{col};flex-shrink:0;transform:translateY(-.45mm)"></span>'
                      f'<span>{d}</span></div>' for d in det)
    return (f'<div style="display:flex;gap:5mm;align-items:flex-start;padding:9mm 0 9mm;{"" if last else f"border-bottom:.3mm solid {RULE}"}">'
            f'{badge(ic, col, "15mm", DK if col not in (TL, SL) else CH)}'
            f'<div style="flex:1;text-align:right"><div style="font-size:5.4mm;font-weight:700">{title}</div>'
            f'<div style="font-size:3.2mm;color:#55565C;line-height:1.7;margin:1.4mm 0 3.4mm">{line}</div>{bullets}</div></div>')


def profile_services(n, title, items, name):
    body = (
        f'<div class="abs" style="right:14mm;left:14mm;top:20mm;text-align:right">{kicker("خدماتنا")}'
        f'<div style="font-size:8.4mm;font-weight:800;line-height:1.25">{title}</div>'
        f'<div style="margin-top:4mm">{"".join(svc_block(s, i == len(items) - 1) for i, s in enumerate(items))}</div></div>'
        + pnum(n)
    )
    return Piece(name, 210, 297, body, bg=CH, fg=DK)


def profile_how():
    steps = "".join(
        f'<div style="display:flex;gap:5mm;align-items:flex-start;position:relative;padding-bottom:9mm">'
        f'<span class="en" style="width:12mm;height:12mm;border-radius:50%;background:{c};color:{DK};font-weight:700;font-size:4.2mm;'
        f'display:flex;align-items:center;justify-content:center;flex-shrink:0;position:relative;z-index:1">{i}</span>'
        f'<div style="text-align:right;padding-top:1.4mm"><div style="font-size:4.6mm;font-weight:700">{t}</div>'
        f'<div style="font-size:3.1mm;color:#55565C;line-height:1.7;margin-top:1mm">{d}</div></div></div>'
        for i, (t, d, c) in enumerate(STEPS, 1))
    body = (
        f'<div class="abs" style="right:14mm;left:14mm;top:22mm;text-align:right">{kicker("كيف نعمل")}'
        f'<div style="font-size:8.4mm;font-weight:800;line-height:1.25">من أول رسالة<br>إلى الملف النهائي</div></div>'
        f'<div class="abs" style="right:19.8mm;top:86mm;width:.5mm;height:150mm;background:{RULE}"></div>'
        f'<div class="abs" style="right:14mm;left:14mm;top:80mm">{steps}</div>'
        f'<div class="abs" style="left:14mm;right:14mm;top:238mm;background:{DK};color:{CH};border-radius:5mm;padding:6mm 7mm;display:flex;'
        f'justify-content:space-between;align-items:center"><div style="text-align:right"><div style="font-size:3.9mm;font-weight:700">الدفع</div>'
        f'<div style="font-size:2.9mm;color:{CH_DIM};margin-top:1mm">عربون <span class="en">50%</span> عند البدء والباقي عند التسليم، عبر زين كاش أو كي كارد.</div></div>'
        f'{icon("check", "9mm", TE, 2.2)}</div>'
        + pnum(6)
    )
    return Piece("profile-06-how", 210, 297, body, bg=WHITE, fg=DK)


def profile_deliver():
    items = "".join(
        f'<div style="display:flex;align-items:center;gap:4mm;padding:5.6mm 0;border-bottom:.3mm solid rgba(242,233,216,.2);font-size:4.6mm">'
        f'<span style="width:3.6mm;height:3.6mm;border-radius:50%;background:{c};flex-shrink:0"></span><span>{t}</span></div>' for t, c in DELIVERABLES)
    body = (
        f'<div class="abs" style="right:14mm;left:14mm;top:22mm;text-align:right">{kicker("باقة الهوية الكاملة")}'
        f'<div style="font-size:8.4mm;font-weight:800;line-height:1.25">ماذا تستلم<br>في نهاية العمل؟</div>'
        f'<div style="margin-top:10mm">{items}</div>'
        f'<div style="font-size:3.1mm;color:{CH_DIM};line-height:1.8;margin-top:9mm">حقوق الشعار تنتقل إليك بعد الدفعة الأخيرة، وبياناتك لا تُنشر ولا تُشارك.<br>'
        f'المدة من 7 إلى 10 أيام للهوية الكاملة، ويُكتب كل شيء في العرض قبل البدء.</div></div>'
        + pill("42mm", "11mm", MU, "left:171mm;top:262mm") + dot("7mm", RO, "left:158mm;top:264mm")
        + pnum(7, CH_DIM)
    )
    return Piece("profile-07-deliver", 210, 297, body, bg=TL, fg=CH)


def profile_back():
    body = (
        f'<div class="abs" style="inset:-3mm;{pattern(26, CH, TE, CH, MU, .09)}"></div>'
        f'<div class="abs" style="left:0;right:0;top:78mm;display:flex;justify-content:center">{logo("92mm", CH, TE)}</div>'
        f'<div class="abs" style="left:0;right:0;top:136mm;text-align:center;font-size:5mm;font-weight:700;color:{CH}">{TAG_AR}</div>'
        f'<div class="abs" style="left:0;right:0;top:160mm;display:flex;justify-content:center">{contact("3.4mm", CH, CH_DIM, TE, "2mm", align="flex-start")}</div>'
        f'<div class="abs" style="left:35mm;right:35mm;top:205mm;border:.4mm solid {TE};border-radius:5mm;padding:5mm 6mm;text-align:center;font-size:3.2mm;line-height:1.7">'
        f'<b style="color:{TE}">{OTHER_AR}</b><br>{OTHER_LINE}</div>'
        + pill("60mm", "12mm", TE, "left:-3mm;top:262mm") + dot("8mm", MU, "left:62mm;top:264mm")
    )
    return Piece("profile-08-back", 210, 297, body, bg=DK, fg=CH)


def profile_pages():
    return [profile_cover(), profile_about(), profile_why(),
            profile_services(4, "التصميم", SERVICES[:3], "profile-04-design"),
            profile_services(5, "السيرة والمشاريع والتقنية", SERVICES[3:], "profile-05-cv-academic-tech"),
            profile_how(), profile_deliver(), profile_back()]


# ---------------------------------------------------------------- roll-up 85x200 cm (1:10)

def rollup():
    rows = "".join(
        f'<div style="display:flex;align-items:center;gap:3.2mm;padding:2.1mm 0;border-bottom:.2mm solid rgba(242,233,216,.16)">'
        f'{badge(ic, col, "7.6mm", DK if col not in (TL, SL) else CH)}<span style="font-size:3.6mm;font-weight:600">{title}</span></div>'
        for key, ic, col, title, line, _ in SERVICES)
    body = (
        f'<div class="abs" style="inset:-3mm;{pattern(16, CH, TE, CH, MU, .08)}"></div>'
        f'<div class="abs" style="left:0;right:0;top:14mm;display:flex;justify-content:center">{logo("52mm", CH, TE)}</div>'
        + pill("33mm", "4.6mm", TE, "left:-3mm;top:47mm") + dot("3.6mm", MU, "left:32.6mm;top:47.5mm")
        + f'<div class="abs" style="right:9mm;top:53.5mm;text-align:right;font-size:8.6mm;font-weight:800;line-height:1.22;color:{CH}">نبني الجسر<br>بين فكرتك<br>والنتيجة</div>'
        + f'<div class="abs" style="right:9mm;left:9mm;top:90mm">{rows}</div>'
        + f'''<div class="abs" style="left:-3mm;right:-3mm;top:166mm;bottom:-3mm;background:{TE};color:{DK}">
  <div class="abs" style="right:12mm;left:12mm;top:6.5mm;text-align:right"><div style="font-size:5.3mm;font-weight:800">راسلنا بنوع خدمتك</div>
  <div style="margin-top:3mm">{contact("2.9mm", DK, "rgba(32,33,38,.7)", DK, "1.6mm")}</div></div></div>'''
    )
    return Piece("rollup-85x200cm-scale-1-10", 85, 200, body, bg=DK, fg=CH)


# ---------------------------------------------------------------- shop sign 300x90 cm (1:10)

def shop_sign():
    body = (
        f'<div class="abs" style="inset:-3mm;{pattern(13, CH, TE, CH, MU, .08)}"></div>'
        f'<div class="abs" style="right:22mm;top:20mm">{logo("94mm", CH, TE)}</div>'
        f'<div class="abs" style="right:131mm;top:15mm;bottom:15mm;width:.6mm;background:rgba(242,233,216,.35)"></div>'
        f'<div class="abs" style="right:143mm;top:21mm;text-align:right;color:{CH}">'
        f'<div style="font-size:11mm;font-weight:800;line-height:1.22">نبني الجسر بين فكرتك<br>والنتيجة</div>'
        f'<div style="font-size:4.4mm;color:{CH_DIM};margin-top:4mm">{LINE_AR}</div></div>'
        + pill("40mm", "6mm", TE, "left:-3mm;top:73mm") + dot("4.6mm", MU, "left:41mm;top:73.7mm")
    )
    return Piece("shop-sign-300x90cm-scale-1-10", 300, 90, body, bg=DK, fg=CH)


# ---------------------------------------------------------------- outdoor banner 300x100 cm (1:10)

def outdoor_banner():
    svc = "".join(f'<span style="display:inline-flex;align-items:center;gap:2.4mm">'
                  f'<span style="width:3mm;height:3mm;border-radius:50%;background:{col}"></span>{title}</span>'
                  for key, ic, col, title, line, _ in SERVICES)
    body = (
        f'<div class="abs" style="left:-3mm;top:-3mm;bottom:-3mm;width:104mm;background:{DK};{pattern(14, CH, TE, CH, MU, .09)}"></div>'
        f'<div class="abs" style="left:-3mm;top:-3mm;bottom:-3mm;width:104mm;display:flex;align-items:center;justify-content:center">{logo("72mm", CH, TE)}</div>'
        f'<div class="abs" style="right:16mm;top:11mm;text-align:right">'
        f'<div style="font-size:12.5mm;font-weight:800;line-height:1.18">فكرتك تستحق<br>هوية تليق بها</div>'
        f'<div style="font-size:4.6mm;color:#45464C;margin-top:3.5mm">تصميم خاص من الصفر، واتفاق مكتوب من البداية.</div></div>'
        f'<div class="abs" style="left:118mm;top:14mm;width:66mm;font-size:4mm;font-weight:600;line-height:1;display:flex;flex-direction:column;gap:3.6mm;align-items:flex-start">{svc}</div>'
        f'<div class="abs" style="right:16mm;bottom:10mm">{contact("4.4mm", DK, GREY, TE, "1.8mm")}</div>'
        + pill("40mm", "7mm", TE, "left:101mm;top:84mm") + dot("5.4mm", MU, "left:144mm;top:84.8mm")
    )
    return Piece("outdoor-banner-300x100cm-scale-1-10", 300, 100, body, bg=CH, fg=DK)


ALL = lambda: [flyer(), brochure_outside(), brochure_inside(), *profile_pages(), rollup(), shop_sign(), outdoor_banner()]

if __name__ == "__main__":
    import sys as _s
    only = _s.argv[1:]
    ps = [p for p in ALL() if not only or any(p.name.startswith(o) for o in only)]
    big = [p for p in ps if "scale-1-10" in p.name]
    small = [p for p in ps if p not in big]
    if small:
        render(small)
    if big:
        render(big, dpi=600)
