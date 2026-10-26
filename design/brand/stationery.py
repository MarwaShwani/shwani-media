"""Official papers: business card, letterhead, quotation, envelope, folder, ID badge, email signature.
Run: python3 brand/stationery.py  ->  brand/out/print/*.pdf and brand/out/png/*.png"""
from kit import *  # noqa: F401,F403


# ---------------------------------------------------------------- business card 90x50

def card_front():
    body = (
        f'<div class="abs" style="left:0;right:0;top:15.6mm;display:flex;justify-content:center">{logo("49.5mm", CH, TE)}</div>'
        f'<div class="abs" style="left:0;right:0;top:31.6mm;text-align:center;font-size:2.15mm;font-weight:400;color:{CH_DIM}">{LINE_AR}</div>'
        # 26 Oct (Marwa): nothing on the card is cut at the edge; every shape sits inside the trim
        + pill("18mm", "6.2mm", TE, "left:6.6mm;top:37.2mm")
        + dot("4.6mm", MU, "left:27.4mm;top:38mm")
        + dot("7.4mm", SL, "left:76mm;top:6.6mm")
    )
    return Piece("business-card-front", 90, 50, body, bg=DK, fg=CH)


def card_back():
    body = (
        f'<div class="abs" style="left:6.6mm;top:6.6mm">{word("27mm", DK, TE)}</div>'
        + dot("3.4mm", RO, "left:6.6mm;top:40mm")
        + f'''<div class="abs" style="right:6.6mm;top:5.9mm;text-align:right">
  <div style="font-size:4.3mm;font-weight:700;line-height:1.3">{OWNER_AR}</div>
  <div style="font-size:2.6mm;font-weight:500;color:{TE};line-height:1.5">{ROLE_AR}</div>
  <div class="en" style="font-size:2.05mm;font-weight:400;color:{GREY};margin-top:.8mm">{OWNER_EN} · {ROLE_EN}</div>
</div>
<div class="abs" style="right:6.6mm;bottom:5.4mm">{contact("2.25mm", DK, GREY, TE, "1.5mm", align="flex-start")}</div>'''
    )
    return Piece("business-card-back", 90, 50, body, bg=CH, fg=DK)


# ---------------------------------------------------------------- A4 letter pages

def letter_frame(content, note=""):
    """Header (logo, tagline, pill) and dark footer (SH, place, socials, email)."""
    foot_row = "display:flex;align-items:center;gap:1.8mm;font-size:2.75mm;white-space:nowrap"
    return (
        f'<div class="abs" style="right:18.1mm;top:15.2mm">{logo("43.7mm", DK, TE)}</div>'
        f'<div class="abs" style="left:18.1mm;top:16.6mm;text-align:left">'
        f'<div style="font-size:2.85mm;color:{GREY};font-weight:400">{TAG_AR}</div>'
        f'<div class="en" style="font-size:2.3mm;color:{GREY};font-weight:400;margin-top:.9mm">{TAG_EN}</div></div>'
        + pill("27mm", "5.1mm", TE, "left:-3mm;top:35.9mm")
        + dot("4.2mm", MU, "left:26.9mm;top:36.35mm")
        + f'<div class="abs" style="left:39.8mm;right:18.1mm;top:38.5mm;height:.3mm;background:{RULE}"></div>'
        + f'<div class="abs" style="left:18.1mm;right:18.1mm;top:50mm;bottom:22mm">{content}</div>'
        + (f'<div class="abs" style="right:18.1mm;bottom:20.6mm;font-size:2.2mm;color:{GREY2}">{note}</div>' if note else "")
        + f'<div class="abs" style="right:18.1mm;bottom:15mm;width:21.8mm;height:2.2mm;border-radius:1.1mm 1.1mm 0 0;background:{TE}"></div>'
        + f'''<div class="abs" style="left:-3mm;right:-3mm;bottom:-3mm;height:18.1mm;background:{DK};color:{CH}">
  <div class="abs" style="left:21.1mm;right:21.1mm;top:0;height:15.1mm;display:flex;align-items:center;justify-content:space-between">
    <div style="display:flex;align-items:center;gap:9mm">
      <div style="{foot_row}">{icon("mail", "3.3mm", TE)}<span class="en" style="font-weight:500">{EMAIL}</span></div>
      <div style="{foot_row}">{icon("at", "3.3mm", TE)}<span class="en" style="font-weight:600">{HANDLE}</span><span style="color:{CH_DIM};font-weight:400">{SOCIAL_AR}</span></div>
      <div style="{foot_row}">{icon("pin", "3.3mm", TE)}<span style="font-weight:500">{PLACE}</span></div>
    </div>
    {sh("5.4mm", CH, TE)}
  </div>
</div>''')


LETTER_CSS = """
.body p{font-size:3.55mm;line-height:1.95;font-weight:400;margin-bottom:2.6mm;text-align:justify}
"""


def letterhead():
    return Piece("letterhead-a4", 210, 297, letter_frame(""), bg=WHITE)


def letterhead_sample():
    content = f'''<div class="body">
<div style="display:flex;justify-content:space-between;align-items:baseline;font-size:3.3mm">
  <span style="color:{DK};font-weight:400">إلى: السادة شركة النخيل للتجارة المحترمين</span>
  <span class="en" style="color:{GREY};font-weight:500">2026/10/18</span></div>
<div style="font-size:4.4mm;font-weight:700;margin:9mm 0 6mm">الموضوع: عرض تصميم الهوية البصرية</div>
<p>تحية طيبة،</p>
<p>يسرّنا أن نقدّم لكم عرضنا لتصميم الهوية البصرية الكاملة لشركتكم: الشعار ونسخه، والألوان والخطوط، والقرطاسية الرسمية، والمطبوعات، ودليل الميديا الذي يحفظ هويتكم واضحة في كل مكان تظهر فيه.</p>
<p>نبدأ بجلسة نفهم فيها مشروعكم وجمهوره، ثم نقدّم مقترحات مصممة من الصفر، ونعدّلها معكم حتى تصل إلى النتيجة التي تريدونها، ونسلّم الملفات بكل الصيغ الجاهزة للطباعة والنشر.</p>
<p>تجدون التفاصيل والمدة في عرض السعر المرفق. ويسعدنا الرد على أي سؤال.</p>
<p style="margin-top:7mm;margin-bottom:1.5mm">مع التقدير،</p>
<div style="font-size:3.9mm;font-weight:700;line-height:1.6">{OWNER_AR}</div>
<div style="font-size:3.1mm;font-weight:500;color:{TE}">{ROLE_AR}، <span class="en">SHWANI COMPANY</span></div>
</div>'''
    return Piece("letterhead-a4-sample", 210, 297, letter_frame(content, "(مثال: شركة النخيل للتجارة من الخيال)"),
                 css=LETTER_CSS, bg=WHITE)


def quotation():
    th = f"background:{DK};color:{CH};font-weight:600;font-size:3.1mm;padding:3.4mm 3mm;text-align:right"
    td = f"padding:4.1mm 3mm;border-bottom:.3mm solid {RULE};font-size:3.05mm;vertical-align:middle"
    rows = [
        ("1", "هوية بصرية كاملة", "الشعار بنسخه، الألوان والخطوط، دليل الميديا", "7 إلى 10 أيام", "250,000"),
        ("2", "القرطاسية الرسمية", "بطاقة العمل، الورقة الرسمية، الظرف، عرض السعر", "3 أيام", "حسب الاتفاق"),
        ("3", "المطبوعات", "فلاير، بروشور، رول أب، لافتة", "5 أيام", "حسب الاتفاق"),
    ]
    trs = "".join(
        f'<tr><td style="{td};width:7mm;color:{GREY}" class="en">{a}</td><td style="{td};font-weight:700;font-size:3.3mm">{b}</td>'
        f'<td style="{td};color:{GREY}">{c}</td><td style="{td}">{d}</td>'
        f'<td style="{td};font-weight:700" class="{"en" if e[0].isdigit() else ""}">{e}</td></tr>' for a, b, c, d, e in rows)
    box = f"flex:1;background:{PAPER};border-radius:3.5mm;padding:5mm 5mm 4.5mm;line-height:1.55"
    sumrow = "display:flex;justify-content:space-between;font-size:3.1mm;padding:1.3mm 0"
    content = f'''
<div style="display:flex;justify-content:space-between;align-items:flex-end">
  <div><div style="font-size:9.5mm;font-weight:800;line-height:1.1">عرض سعر</div>
       <div style="font-size:3.1mm;color:{GREY};margin-top:1.8mm">العرض صالح 30 يوماً من تاريخه</div></div>
  <div style="font-size:3mm;line-height:1.9;color:{GREY}">رقم العرض: <b class="en" style="color:{DK}">Q-2026-014</b><br>التاريخ: <b class="en" style="color:{DK}">2026/10/18</b></div>
</div>
<div style="display:flex;gap:6mm;margin-top:11mm">
  <div style="{box}"><div style="color:{TE};font-size:3mm;font-weight:600">إلى</div>
    <div style="font-size:3.4mm;font-weight:700">شركة النخيل للتجارة</div><div style="font-size:3.1mm;color:{GREY}">بغداد، العراق</div></div>
  <div style="{box}"><div style="color:{TE};font-size:3mm;font-weight:600">من</div>
    <div class="en" style="font-size:3.1mm;font-weight:700;text-align:right">SHWANI COMPANY</div><div class="en" style="font-size:3mm;color:{GREY};text-align:right">{EMAIL}</div></div>
</div>
<table style="width:100%;border-collapse:collapse;margin-top:6mm">
<tr><th style="{th};border-radius:0 0 0 0">#</th><th style="{th}">البند</th><th style="{th}">ما يشمله</th><th style="{th}">المدة</th><th style="{th}">المبلغ (دينار)</th></tr>
{trs}</table>
<div style="display:flex;gap:16mm;margin-top:11mm">
  <div style="flex:1">
    <div style="font-size:3.5mm;font-weight:700;margin-bottom:2.5mm">الشروط</div>
    <div style="font-size:2.95mm;line-height:2.05;color:{DK}">• عربون <span class="en">50%</span> عند البدء، والباقي عند التسليم.<br>• الدفع عبر زين كاش أو كي كارد.<br>• جولتا تعديل في تصاميم الهوية.<br>• حقوق الشعار تنتقل إليكم بعد الدفعة الأخيرة.<br>• بياناتكم لا تُنشر ولا تُشارك.</div>
  </div>
  <div style="flex:1">
    <div style="{sumrow}"><span>البند 1</span><b class="en">250,000</b></div>
    <div style="{sumrow};color:{TE};font-weight:700"><span>خصم الإطلاق <span class="en">30%</span></span><span class="en">-75,000</span></div>
    <div style="{sumrow};border-top:.3mm solid {RULE};margin-top:1mm;padding-top:2mm"><span>الصافي</span><b class="en">175,000</b></div>
    <div style="display:flex;justify-content:space-between;background:{DK};color:{CH};border-radius:2.6mm;padding:3mm 4.5mm;margin-top:2.5mm;font-size:3.2mm;font-weight:700"><span>العربون عند البدء <span class="en">50%</span></span><span class="en">87,500</span></div>
    <div style="font-size:2.5mm;color:{GREY};margin-top:2mm">البندان 2 و3 يُسعَّران حسب الاتفاق.</div>
  </div>
</div>
<div style="margin-top:13mm;border:.35mm solid {TE};border-radius:4mm;padding:4.3mm 6mm;font-size:3.2mm">
  <b style="color:{TE}">{OTHER_AR.replace("تحتاج", "تحتاجون")}</b> أخبرونا بما تحتاجونه، نراجع إمكانية تنفيذه ونتواصل معكم.</div>'''
    return Piece("quotation-a4", 210, 297, letter_frame(content, "(مثال توضيحي: الشركة من الخيال)"), bg=WHITE)


# ---------------------------------------------------------------- DL envelope 220x110

def envelope_front(sample=True):
    to = (f'<div class="abs" style="right:108mm;top:42mm;text-align:right">'
          f'<div style="font-size:3.6mm;font-weight:700">إلى: شركة النخيل للتجارة</div>'
          f'<div style="font-size:3.3mm;color:{GREY};margin-top:1.6mm">بغداد، العراق</div></div>') if sample else ""
    body = (
        f'<div class="abs" style="right:12mm;top:11mm">{logo("35.5mm", DK, TE)}</div>'
        f'<div class="abs" style="right:12mm;top:32mm">{contact("2.45mm", DK, GREY, TE, "1.4mm")}</div>'
        + to
        + pill("37mm", "6.9mm", TE, "left:-3mm;top:90.8mm")
        + dot("4.7mm", MU, "left:37.8mm;top:91.9mm")
    )
    return Piece("envelope-dl-front" + ("" if sample else "-blank"), 220, 110, body, bg=WHITE)


def envelope_back():
    body = (
        f'<div class="abs" style="inset:-3mm;{pattern(22, CH, TE, CH, MU, .13)}"></div>'
        f'<div class="abs" style="left:0;right:0;top:46mm;display:flex;justify-content:center">{sh("18.5mm", CH, TE)}</div>'
        f'<div class="abs" style="left:0;right:0;top:99.5mm;text-align:center;font-size:2.8mm;color:{CH_DIM}">{TAG_AR}</div>'
    )
    return Piece("envelope-dl-back", 220, 110, body, bg=DK, fg=CH)


# ---------------------------------------------------------------- presentation folder 230x310

def folder():
    stem = "#2B2C33"
    body = (
        f'<div class="abs" style="inset:-3mm;{pattern(30, CH, TE, CH, MU, .09)}"></div>'
        f'<div class="abs" style="left:22.5mm;right:22.5mm;top:96mm">{word("185mm", WM_STEM, WM_BAR)}</div>'
        + dot("12.9mm", RO, "left:159mm;top:41.4mm")
        + pill("56mm", "15.8mm", MU, "left:180.1mm;top:40mm")
        + f'<div class="abs" style="right:22.5mm;top:230mm">{logo("77mm", CH, TE)}</div>'
        + f'<div class="abs" style="right:22.5mm;top:263.5mm;font-size:4.3mm;font-weight:500;color:{CH}">{TAG_AR}</div>'
        + f'<div class="abs" style="right:22.5mm;top:280.5mm">{contact("2.7mm", CH, CH_DIM, TE, "1.2mm")}</div>'
    )
    return Piece("folder-a4-cover", 230, 310, body, bg=DK, fg=CH)


# ---------------------------------------------------------------- ID badge 54x86

def id_badge():
    panel = "#F8F3EA"
    body = (
        f'<div class="abs" style="left:-3mm;right:-3mm;top:-3mm;height:46.8mm;background:{DK};{pattern(16, CH, TE, CH, MU, .12)}"></div>'
        f'<div class="abs" style="left:21mm;top:3mm;width:12mm;height:2.6mm;border-radius:1.3mm;background:#E9E6E0"></div>'
        f'<div class="abs" style="left:10.2mm;right:10.2mm;top:16.6mm">{logo("33.6mm", CH, TE)}</div>'
        f'<div class="abs" style="left:-3mm;right:-3mm;top:43.8mm;bottom:-3mm;background:{panel}"></div>'
        f'<div class="abs" style="left:17.5mm;top:39.4mm;width:19mm;height:19mm;border-radius:50%;background:{panel}"></div>'
        f'<div class="abs" style="left:18.55mm;top:40.45mm;width:16.9mm;height:16.9mm;border-radius:50%;background:{CH};display:flex;align-items:center;justify-content:center">{sh("7.2mm", DK, TE)}</div>'
        f'<div class="abs" style="left:0;right:0;top:60.2mm;text-align:center">'
        f'<div style="font-size:5.3mm;font-weight:700;line-height:1.3">{OWNER_AR}</div>'
        f'<div style="font-size:4mm;font-weight:600;color:{TE};line-height:1.4">{ROLE_AR}</div>'
        f'<div class="en" style="font-size:2.9mm;color:{GREY};margin-top:.6mm">{OWNER_EN}</div></div>'
        f'<div class="abs" style="left:-3mm;right:-3mm;top:82mm;bottom:-3mm;background:{TE}"></div>'
    )
    return Piece("id-badge-54x86", 54, 86, body, bg=DK, fg=DK)


# ---------------------------------------------------------------- email signature (screen, 600x170 px)

def email_signature_html():
    """Gmail-safe HTML signature (tables, inline styles, hosted SH image)."""
    return f'''<table cellpadding="0" cellspacing="0" style="font-family:Alexandria,Tahoma,Arial,sans-serif;direction:rtl">
<tr><td style="padding-left:16px"><img src="https://raw.githubusercontent.com/MarwaShwani/shwani-media/main/brand/logo/png/shwani-sh-tile-256.png" width="72" height="72" alt="SHWANI COMPANY" style="display:block;border-radius:14px"></td>
<td style="border-right:3px solid {TE};padding-right:14px">
<div style="font-size:17px;font-weight:700;color:{DK}">{OWNER_AR}</div>
<div style="font-size:13px;font-weight:600;color:{TE}">{ROLE_AR}، SHWANI COMPANY</div>
<div style="font-size:13px;color:{DK};margin-top:6px;direction:ltr;text-align:right">{EMAIL}</div>
<div style="font-size:13px;color:{GREY}"><b style="color:{DK}">{HANDLE}</b> · {SOCIAL_AR}</div>
</td></tr></table>'''


def email_signature():
    # 160 x 45.3 mm at 190 dpi gives 1200 x 340 px
    body = (
        f'<div class="abs" style="left:6.9mm;top:6.9mm;width:1.9mm;height:31.1mm;border-radius:1mm;'
        f'background:linear-gradient({TE},{MU},{RO},{SG})"></div>'
        f'<div class="abs" style="right:51.2mm;top:8.6mm;text-align:right">'
        f'<div style="font-size:5.5mm;font-weight:700;line-height:1.25">{OWNER_AR}</div>'
        f'<div style="font-size:3.6mm;font-weight:600;color:{TE};margin-top:.6mm">{ROLE_AR}، <span class="en">SHWANI COMPANY</span></div></div>'
        f'<div class="abs" style="left:15.5mm;right:51.2mm;top:23.2mm;height:.25mm;background:{RULE}"></div>'
        f'<div class="abs" style="right:51.2mm;top:26.4mm">{contact("3.35mm", DK, GREY, TE, "1.4mm")}</div>'
        f'<div class="abs" style="right:7.7mm;top:4.5mm;width:36.3mm;height:36.3mm;border-radius:6mm;background:{DK};'
        f'display:flex;align-items:center;justify-content:center">{sh("13.5mm", CH, TE)}</div>'
    )
    return Piece("email-signature", 160, 45.3, body, bg=WHITE)


PIECES = [card_front, card_back, letterhead, letterhead_sample, quotation,
          lambda: envelope_front(True), lambda: envelope_front(False), envelope_back, folder, id_badge]

if __name__ == "__main__":
    import sys as _s
    only = _s.argv[1:]
    ps = [f() for f in PIECES]
    ps = [p for p in ps if not only or p.name in only]
    render(ps)
    sig = email_signature()
    if not only or sig.name in only:
        render([sig], pdf=False, dpi=190)
        os.makedirs(os.path.join(OUT, "digital"), exist_ok=True)
        open(os.path.join(OUT, "digital", "email-signature.html"), "w", encoding="utf-8").write(email_signature_html())
