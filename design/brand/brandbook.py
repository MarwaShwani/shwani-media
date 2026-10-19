"""SHWANI COMPANY brand book (دليل الهوية البصرية), A4 landscape, with the media guide and the publishing plan.
Run after stationery/printwork/merch/logos/mockups:  python3 brand/brandbook.py
Writes out/brandbook/SHWANI-brand-book.pdf and a PNG per page."""
import os, asyncio
from kit import *  # noqa: F401,F403
from rounded import mark_svg

W, H = 297, 210
MOCK = os.path.join(OUT, "mockups")
PNGD = os.path.join(OUT, "png")
BOOK = os.path.join(OUT, "brandbook")
PAGES = []


def img(path, style=""):
    return f'<img src="file://{path}" style="display:block;object-fit:cover;{style}">'


def mock(name, style=""):
    return img(os.path.join(MOCK, name + ".jpg"), style)


def flat(name, style=""):
    return img(os.path.join(PNGD, name + ".png"), style)


def page(n, section, title, body, bg=CH, fg=DK, kicker_color=TE, sub=""):
    dim = GREY if bg in (CH, WHITE) else CH_DIM
    head = (f'<div class="abs" style="right:16mm;top:13mm;left:16mm;display:flex;justify-content:space-between;align-items:flex-start">'
            f'<div style="text-align:right"><div style="color:{kicker_color};font-size:3mm;font-weight:600">{section}</div>'
            f'<div style="font-size:8mm;font-weight:800;line-height:1.25;margin-top:1mm">{title}</div>'
            + (f'<div style="font-size:3.2mm;color:{dim};margin-top:2mm;max-width:150mm;line-height:1.7">{sub}</div>' if sub else "")
            + f'</div><div class="en" style="font-size:3mm;color:{dim};font-weight:500">{n:02d}</div></div>')
    foot = (f'<div class="abs" style="right:16mm;left:16mm;bottom:9mm;display:flex;justify-content:space-between;align-items:center;'
            f'font-size:2.5mm;color:{dim}"><span>دليل الهوية البصرية · <span class="en">SHWANI COMPANY</span></span>'
            f'{sh("4mm", fg if bg in (CH, WHITE) else CH, TE)}</div>')
    PAGES.append(Piece(f"page-{n:02d}", W, H, head + body + foot, bg=bg, fg=fg))


def area(body, top=48, bottom=20, left=16, right=16, style=""):
    return f'<div class="abs" style="top:{top}mm;bottom:{bottom}mm;left:{left}mm;right:{right}mm;{style}">{body}</div>'


def tile(inner, bg, label, fg=DK, h="58mm", note=""):
    return (f'<div style="display:flex;flex-direction:column;gap:2mm"><div style="height:{h};border-radius:4mm;background:{bg};'
            f'display:flex;align-items:center;justify-content:center;border:.3mm solid rgba(32,33,38,.08)">{inner}</div>'
            f'<div style="font-size:3mm;font-weight:600">{label}</div>'
            + (f'<div style="font-size:2.6mm;color:{GREY};line-height:1.6">{note}</div>' if note else "") + '</div>')


def grid(cells, cols, gap="6mm", style=""):
    return f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:{gap};direction:rtl;{style}">{"".join(cells)}</div>'


def p(text, size="3.3mm", color=None, mt="0", lh="1.85"):
    return f'<p style="font-size:{size};line-height:{lh};margin-top:{mt};{f"color:{color};" if color else ""}">{text}</p>'


def bullet_list(items, color=TE, size="3.8mm"):
    return "".join(f'<div style="display:flex;gap:2.6mm;align-items:baseline;font-size:{size};line-height:1.75;margin-bottom:1.4mm">'
                   f'<span style="width:2mm;height:2mm;border-radius:50%;background:{color};flex-shrink:0;transform:translateY(-.4mm)"></span>'
                   f'<span>{t}</span></div>' for t in items)


# ---------------------------------------------------------------- pages

def p01_cover():
    body = (f'<div class="abs" style="inset:-3mm;{pattern(22, CH, TE, CH, MU, .09)}"></div>'
            f'<div class="abs" style="left:28mm;top:62mm">{word("241mm", "#2B2C33", TE)}</div>'
            + dot("12mm", RO, "left:228mm;top:24mm") + pill("44mm", "13mm", MU, "left:256mm;top:23.5mm")
            + f'<div class="abs" style="right:20mm;top:84mm">{logo("96mm", CH, TE)}</div>'
            f'<div class="abs" style="right:20mm;top:140mm;text-align:right;color:{CH}">'
            f'<div style="font-size:9mm;font-weight:800">دليل الهوية البصرية</div>'
            f'<div class="en" style="font-size:3.6mm;color:{CH_DIM};margin-top:2mm;letter-spacing:.6mm">BRAND GUIDELINES · 2026</div>'
            f'<div style="font-size:3.2mm;color:{CH_DIM};margin-top:6mm">الشعار، الألوان، الخط، العناصر، التطبيقات، دليل الميديا وخطة النشر</div></div>')
    PAGES.append(Piece("page-01", W, H, body, bg=DK, fg=CH))


SECTIONS = [
    ("01", "العلامة", "من نحن، قصة الشعار", 3),
    ("02", "الشعار", "الشعار الرئيسي، النسخ، المساحة الآمنة، الاستخدامات الخاطئة", 5),
    ("03", "الألوان", "الألوان الأساسية، ألوان الخدمات، النِّسب والتباين", 9),
    ("04", "الخط", "Alexandria بأوزانه، والتسلسل الهرمي للنص", 12),
    ("05", "العناصر", "الجسور والدوائر، النمط، الأيقونات، أسلوب الصور", 13),
    ("06", "التطبيقات", "القرطاسية، المطبوعات، اللافتات، الهدايا والتغليف، الشاشات", 16),
    ("07", "دليل الميديا", "صوت العلامة، قواعد الكتابة، قوالب المنشورات وصفوف الحساب", 21),
    ("08", "خطة النشر والتطوير", "السلاسل الأسبوعية، المقاييس، خطوات 90 يوماً", 23),
    ("09", "الملفات المسلَّمة", "ما تجده في الباقة، وكيف تستعمله", 25),
]


def p02_contents():
    rows = "".join(
        f'<div style="display:flex;align-items:baseline;gap:5mm;padding:3.3mm 0;border-bottom:.3mm solid {RULE}">'
        f'<span class="en" style="font-size:3.4mm;color:{TE};font-weight:700;width:9mm">{num}</span>'
        f'<span style="font-size:4.4mm;font-weight:700;width:58mm">{t}</span>'
        f'<span style="font-size:3.1mm;color:{GREY};flex:1">{d}</span>'
        f'<span class="en" style="font-size:3.2mm;color:{GREY}">{pg:02d}</span></div>' for num, t, d, pg in SECTIONS)
    page(2, "المحتويات", "ماذا في هذا الدليل", area(rows, top=44, right=16, left=60)
         + f'<div class="abs" style="left:16mm;top:52mm;width:34mm">{word("34mm", DK, TE)}</div>'
         + f'<div class="abs" style="left:16mm;top:104mm;width:36mm;font-size:2.9mm;line-height:1.8;color:#55565C;text-align:right">'
           f'هذا الدليل مرجع كل من يصمّم أو يكتب أو يطبع باسم <span class="en">SHWANI COMPANY</span>. اتبعه حتى تبقى العلامة واحدة في كل مكان.</div>')


def p03_about():
    services = [("الهوية البصرية", "للشركات والمؤسسات والأفراد", TE), ("سِيَر ذاتية", "بالعربية والإنجليزية، عبر بوت تيليغرام", SL),
                ("مشاريع تقنية وأكاديمية", "تخطيط وتحرير وتنسيق وعرض", TL), ("خدمات تقنية أخرى", "أخبرنا بما تحتاجه، نراجع إمكانية تنفيذه ونتواصل معك", SG)]
    cells = [f'<div style="border-top:1mm solid {c};padding-top:3mm"><div style="font-size:4mm;font-weight:700">{t}</div>'
             f'<div style="font-size:2.9mm;color:#55565C;line-height:1.7;margin-top:1mm">{d}</div></div>' for t, d, c in services]
    body = area(
        f'<div style="font-size:12mm;font-weight:800;line-height:1.25;color:{DK}">نبني الجسر<br>بين فكرتك والنتيجة</div>'
        + p('<span class="en">SHWANI COMPANY</span> استوديو تصميم وخدمات تقنية في العراق. نصمّم الهوية البصرية للشركات والأفراد، ونكتب السِّيَر الذاتية، '
            'ونساعد في المشاريع التقنية والأكاديمية. كل عمل خاص بصاحبه، من الصفر، بلا قوالب جاهزة.', "3.4mm", "#45464C", "6mm")
        + f'<div style="margin-top:8mm">{grid(cells, 4)}</div>' + mock("13-outdoor-banner", "width:100%;height:52mm;border-radius:4mm;margin-top:7mm"), top=36, left=16, right=16)
    page(3, "01 · العلامة", "من نحن", body)


def p04_story():
    lab = f'font-size:3.4mm;font-weight:600'
    body = (f'<div class="abs" style="left:24mm;top:46mm;width:110mm;height:120mm;background:{DK};border-radius:6mm;display:flex;'
            f'flex-direction:column;align-items:center;justify-content:center;gap:8mm">{word("62mm", CH, TE)}'
            f'<div style="width:62mm;display:flex;justify-content:space-between;color:{CH};{lab}"><span>المشكلة</span>'
            f'<span style="color:{TE}">الحل</span><span>النتيجة</span></div></div>'
            + area(f'<div style="font-size:6.5mm;font-weight:800;line-height:1.35">في قلب اسمنا جسر</div>'
                   + p('حرف <span class="en">H</span> في وسط <span class="en">SHWANI</span> هو قلب الشعار. ركيزته اليمنى هي المشكلة التي يأتينا بها العميل، '
                       'وركيزته اليسرى هي النتيجة التي يريدها، والوصلة بينهما، بلون التيراكوتا، هي الحل الذي نبنيه معه.', "3.4mm", "#45464C", "5mm")
                   + p('الحروف أحادية الخط، بنهايات مستديرة، وسمك واحد في كل الحروف: خط هادئ وواضح يُقرأ من بعيد، ويبقى ودوداً.', "3.4mm", "#45464C", "3mm")
                   + p('ومن الوصلة نفسها خرجت عناصر الهوية كلها: الكبسولات الملوّنة في المطبوعات هي «جسور»، والدوائر نقاط البداية والوصول.', "3.4mm", "#45464C", "3mm"),
                   top=46, left=150, right=16))
    page(4, "01 · العلامة", "قصة الشعار", body)


def p05_primary():
    W_, body_ = mark(DK, TE)
    s = shwani(DK, TE)
    sw = s.width()
    # construction: show the lockup with stroke grid
    cons = (f'<svg viewBox="-60 -760 {sw+120:.0f} 1240" style="width:150mm;height:auto;display:block">'
            f'<rect x="-60" y="-760" width="{sw+120:.0f}" height="1240" fill="none"/>'
            f'<line x1="-40" y1="0" x2="{sw+40:.0f}" y2="0" stroke="{TE}" stroke-width="4" stroke-dasharray="14 10"/>'
            f'<line x1="-40" y1="-700" x2="{sw+40:.0f}" y2="-700" stroke="{TE}" stroke-width="4" stroke-dasharray="14 10"/>'
            f'<line x1="-40" y1="-350" x2="{sw+40:.0f}" y2="-350" stroke="{SL}" stroke-width="3" stroke-dasharray="6 10"/>'
            f'{s.svg()}<g transform="translate(0 420)">{company(DK, sw).svg()}</g></svg>')
    body = (f'<div class="abs" style="left:16mm;top:44mm;width:160mm;height:118mm;background:{WHITE};border-radius:6mm;display:flex;align-items:center;justify-content:center">{cons}</div>'
            + area(bullet_list([
                'الشعار كلمة <span class="en">SHWANI</span> بحروف أحادية الخط مستديرة الأطراف، وتحتها <span class="en">COMPANY</span> بتباعد واسع يملأ عرضها.',
                'سمك الخط ثابت: 160 وحدة من ارتفاع 700، أي نحو 23% من ارتفاع الحرف.',
                'وصلة حرف <span class="en">H</span> وحدها بلون التيراكوتا <span class="en">#E07A47</span>، وأقصر قليلاً من عرض الحرف.',
                'الخطوط المنقّطة: خط القاعدة وخط الرأس ومنتصف الوصلة. لا يُعاد رسم الشعار بخط آخر؛ تُستعمل الملفات الأصلية فقط.',
                'الملفات: <span class="en">SVG</span> للطباعة والويب، و<span class="en">PNG</span> بخلفية شفافة.']), top=48, left=186, right=16))
    page(5, "02 · الشعار", "الشعار الرئيسي وبناؤه", body)


def p06_versions():
    cells = [
        tile(logo("70mm", DK, TE), CH, "الرئيسي على الحليبي", note="الاستعمال الأول في كل مكان"),
        tile(logo("70mm", CH, TE), DK, "المعكوس على الفحمي", note="الخلفيات الداكنة والصور"),
        tile(word("52mm", DK, TE), WHITE, "كلمة SHWANI وحدها", note="المساحات الصغيرة والعريضة، بلا COMPANY"),
        tile(word("52mm", CH, TE), DK, "الكلمة على الفحمي", note="الأختام والأيقونات والمطبوعات الصغيرة"),
        tile(logo("70mm", "#000000", "#000000"), WHITE, "أحادي أسود", note="الفاكس والأختام والحفر"),
        tile(logo("70mm", "#FFFFFF", "#FFFFFF"), "#55565C", "أحادي أبيض", note="الحفر على المعدن والزجاج"),
    ]
    page(6, "02 · الشعار", "نسخ الشعار", area(grid(cells, 3, "7mm"), top=40))


def p07_space():
    s = shwani(DK, TE)
    sw = s.width()
    x = 190  # clear space unit = height of COMPANY letters (190 units)
    box = (f'<svg viewBox="{-x-40} {-700-x-40} {sw+2*x+80:.0f} {700+420+190+2*x+80}" style="width:130mm;height:auto;display:block">'
           f'<rect x="{-x}" y="{-700-x}" width="{sw+2*x:.0f}" height="{700+610+2*x}" fill="none" stroke="{TE}" stroke-width="5" stroke-dasharray="18 12"/>'
           f'<rect x="0" y="-700" width="{sw:.0f}" height="1310" fill="rgba(224,122,71,.06)"/>'
           f'{s.svg()}<g transform="translate(0 420)">{company(DK, sw).svg()}</g>'
           + "".join(f'<rect x="{xx}" y="{yy}" width="{x}" height="{x}" fill="{SL}" opacity=".35"/>'
                     for xx, yy in [(-x, -700 - x), (sw, -700 - x), (-x, 610), (sw, 610)])
           + '</svg>')
    sizes = (f'<div style="display:flex;gap:10mm;align-items:flex-end;margin-top:8mm">'
             f'<div>{logo("25mm", DK, TE)}<div style="font-size:2.8mm;color:{GREY};margin-top:2mm">25 مم في الطباعة<br><span class="en">120 px</span> على الشاشة</div></div>'
             f'<div>{sh("8mm", DK, TE)}<div style="font-size:2.8mm;color:{GREY};margin-top:2mm">الرمز: 8 مم<br><span class="en">32 px</span></div></div></div>')
    body = (f'<div class="abs" style="left:16mm;top:44mm;width:150mm;height:120mm;background:{WHITE};border-radius:6mm;display:flex;align-items:center;justify-content:center">{box}</div>'
            + area(f'<div style="font-size:4.4mm;font-weight:700">المساحة الآمنة</div>'
                   + p('تُترك حول الشعار مساحة فارغة لا تقل عن ارتفاع حروف <span class="en">COMPANY</span> (المربعات الزرقاء)، لا يدخلها نص ولا صورة ولا حافة الورقة.', "3.2mm", "#45464C", "2mm")
                   + f'<div style="font-size:4.4mm;font-weight:700;margin-top:8mm">الحجم الأصغر</div>'
                   + p('أصغر من ذلك تضيع حروف <span class="en">COMPANY</span>؛ عندها تُستعمل كلمة <span class="en">SHWANI</span> وحدها.', "3.2mm", "#45464C", "2mm")
                   + sizes, top=48, left=178, right=16))
    page(7, "02 · الشعار", "المساحة الآمنة والحجم الأصغر", body)


def p08_misuse():
    def bad(inner, label, bg=CH):
        return (f'<div><div style="height:44mm;border-radius:4mm;background:{bg};display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden">{inner}'
                f'<div class="abs" style="left:3mm;top:3mm;width:8mm;height:8mm;border-radius:50%;background:#B3261E;display:flex;align-items:center;justify-content:center">'
                f'<svg viewBox="0 0 24 24" style="width:5mm;height:5mm" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></div></div>'
                f'<div style="font-size:3mm;font-weight:600;margin-top:2mm">{label}</div></div>')
    cells = [
        bad(logo("62mm", DK, TE, style="transform:scaleX(1.35)"), "لا تمطّه ولا تضغطه"),
        bad(logo("62mm", DK, SL), "لا تغيّر لون الوصلة"),
        bad(logo("62mm", DK, TE, style="transform:rotate(-12deg)"), "لا تُدِره"),
        bad(f'<div class="en" style="font-family:Georgia,serif;font-size:9mm;font-weight:700;letter-spacing:.5mm;color:{DK}">SHWANI <span style="color:{TE}">CO.</span></div>',
            "لا تكتبه بخط آخر"),
        bad(logo("62mm", DK, TE, style="filter:drop-shadow(1.5mm 1.5mm 1mm rgba(0,0,0,.45))"), "لا تضف ظلالاً أو مؤثرات"),
        bad(logo("62mm", DK, TE), "لا تضعه على خلفية مزدحمة",
            f"{TE};background-image:repeating-linear-gradient(45deg,{MU} 0 6mm,{RO} 6mm 12mm,{SL} 12mm 18mm)"),
    ]
    page(8, "02 · الشعار", "استخدامات خاطئة", area(grid(cells, 3, "7mm"), top=40))


CORE = [("فحمي", "Charcoal", DK, "32 33 38", "0 0 0 90", CH), ("حليبي", "Milky", CH, "242 233 216", "0 4 11 5", DK),
        ("تيراكوتا", "Terracotta", TE, "224 122 71", "0 55 75 0", DK), ("مسطردي", "Mustard", MU, "212 167 44", "0 21 90 17", DK)]
SERV = [("وردي مغبر", "Dusty rose", RO, "196 124 138", "0 37 30 23", DK, "الهوية البصرية، مع التيراكوتا"),
        ("أزرق رمادي", "Slate", SL, "89 113 138", "36 18 0 46", CH, "السير الذاتية"),
        ("أخضر مزرق", "Teal", TL, "47 111 109", "58 0 2 56", CH, "السير والمشاريع"),
        ("أخضر مريمي", "Sage", SG, "143 166 143", "14 0 14 35", DK, "المشاريع والبحوث"),
        ("بنفسجي", "Plum", PL, "91 58 98", "7 41 0 62", CH, "العروض الخاصة فقط")]


def swatch(ar, en, hx, rgb, cmyk, fg, note="", h="108mm"):
    return (f'<div style="border-radius:5mm;overflow:hidden;border:.3mm solid rgba(32,33,38,.1)">'
            f'<div style="height:{h};background:{hx};color:{fg};padding:5mm;display:flex;flex-direction:column;justify-content:space-between">'
            f'<div><div style="font-size:5mm;font-weight:800">{ar}</div><div class="en" style="font-size:2.9mm;opacity:.8">{en}</div></div>'
            f'<div class="en" style="font-size:2.7mm;line-height:1.7;text-align:left">HEX {hx}<br>RGB {rgb}<br>CMYK {cmyk}</div></div>'
            + (f'<div style="padding:2.6mm 4mm;font-size:2.7mm;background:{WHITE};color:{DK}">{note}</div>' if note else "") + '</div>')


def p09_core():
    cells = [swatch(*c) for c in CORE]
    page(9, "03 · الألوان", "الألوان الأساسية",
         area(grid(cells, 4, "6mm") + p('الفحمي قاعدة العلامة، والحليبي للنص والشعار عليه، والتيراكوتا لون الوصلة والحل، والمسطردي لمسة ذهبية صغيرة. '
                                        'قيم <span class="en">CMYK</span> تقريبية؛ تُطابق مع المطبعة على عيّنة قبل الطباعة الكبيرة.', "3.1mm", GREY, "6mm"), top=40))


def p10_service():
    cells = [swatch(*c[:6], note=c[6], h="98mm") for c in SERV]
    page(10, "03 · الألوان", "ألوان الخدمات",
         area(grid(cells, 5, "5mm") + p('لكل خدمة لون يساعد المتابع على تمييزها من أول نظرة. البنفسجي محجوز للعروض الخاصة فقط.', "3.1mm", GREY, "6mm"), top=40))


def p11_ratio():
    bar = (f'<div style="display:flex;height:34mm;border-radius:4mm;overflow:hidden;direction:ltr">'
           f'<div style="flex:60;background:{DK};color:{CH};display:flex;align-items:center;justify-content:center;font-size:3.4mm" class="en">60%</div>'
           f'<div style="flex:25;background:{CH};display:flex;align-items:center;justify-content:center;font-size:3.4mm;border-top:.3mm solid {RULE};border-bottom:.3mm solid {RULE}" class="en">25%</div>'
           f'<div style="flex:10;background:{TE};display:flex;align-items:center;justify-content:center;font-size:3.2mm" class="en">10%</div>'
           f'<div style="flex:5;background:{MU}"></div></div>')
    pairs = [(TE, DK), (RO, DK), (SG, DK), (MU, DK), (SL, CH), (TL, CH), (PL, CH), (DK, CH)]
    chips = "".join(f'<div style="background:{b};color:{f};border-radius:3mm;padding:9mm 3mm;text-align:center;font-size:4mm;font-weight:700">نص واضح</div>' for b, f in pairs)
    body = area(f'<div style="font-size:4.2mm;font-weight:700;margin-bottom:3mm">النِّسب في التصميم الواحد</div>{bar}'
                f'<div style="font-size:2.9mm;color:{GREY};margin-top:2mm">فحمي 60%، حليبي 25%، تيراكوتا 10%، مسطردي 5% أو أقل.</div>'
                f'<div style="font-size:4.2mm;font-weight:700;margin:9mm 0 3mm">لون النص على كل خلفية</div>'
                f'<div style="display:grid;grid-template-columns:repeat(8,1fr);gap:3mm">{chips}</div>'
                + p('الكتابة فحمية فوق التيراكوتا والوردي والمريمي والمسطردي، وحليبية فوق الأزرق والأخضر المزرق والبنفسجي والفحمي. '
                    'لا مسطردي على الأخضر المزرق، فيبدو باهتاً.', "3.1mm", GREY, "4mm"), top=40)
    page(11, "03 · الألوان", "النِّسب والتباين", body)


def p12_type():
    weights = [(300, "خفيف"), (400, "عادي"), (500, "متوسط"), (600, "نصف عريض"), (700, "عريض"), (800, "أعرض")]
    wrow = "".join(f'<div style="display:flex;align-items:baseline;gap:5mm;padding:2mm 0;border-bottom:.25mm solid {RULE}">'
                   f'<span class="en" style="width:12mm;font-size:2.8mm;color:{GREY}">{w}</span>'
                   f'<span style="font-weight:{w};font-size:5.4mm;flex:1">نبني الجسر بين فكرتك والنتيجة</span>'
                   f'<span class="en" style="font-weight:{w};font-size:4.6mm">Bridge 2026</span>'
                   f'<span style="width:20mm;font-size:2.8mm;color:{GREY}">{n}</span></div>' for w, n in weights)
    hier = (f'<div style="font-size:9mm;font-weight:800;line-height:1.25">عنوان رئيسي</div>'
            f'<div style="font-size:2.7mm;color:{GREY}">800 · كبير وقصير</div>'
            f'<div style="font-size:5.4mm;font-weight:700;margin-top:4mm">عنوان فرعي</div><div style="font-size:2.7mm;color:{GREY}">700</div>'
            f'<div style="font-size:3.4mm;font-weight:400;line-height:1.85;margin-top:4mm">نص الفقرة بوزن عادي، وتباعد أسطر واسع يريح العين في العربية.</div>'
            f'<div style="font-size:2.7mm;color:{GREY}">400 · سطر 1.8</div>'
            f'<div style="font-size:3mm;font-weight:600;color:{TE};margin-top:4mm">عنوان صغير ملوّن</div><div style="font-size:2.7mm;color:{GREY}">600</div>')
    body = (area(f'<div style="font-size:12mm;font-weight:700;line-height:1"><span class="en">Alexandria</span></div>'
                 + p('خط واحد للعلامة كلها، بالعربية والإنجليزية. مجاني ومفتوح المصدر (<span class="en">OFL</span>)، ويُنزَّل من '
                     '<span class="en">Google Fonts</span>. لا يُستعمل خط آخر في التصاميم.', "3.1mm", GREY, "3mm")
                 + f'<div style="margin-top:5mm">{wrow}</div>', top=40, left=96, right=16)
            + f'<div class="abs" style="left:16mm;top:44mm;width:70mm;background:{WHITE};border-radius:5mm;padding:6mm">{hier}</div>')
    page(12, "04 · الخط", "الخط", body)


def p13_elements():
    pt = f'<div style="height:100mm;border-radius:4mm;background:{DK};{pattern(14, CH, TE, CH, MU, .16)}"></div>'
    pills = (f'<div style="height:100mm;border-radius:4mm;background:{CH};position:relative;overflow:hidden;border:.3mm solid {RULE}">'
             + pill("60mm", "12mm", TE, "left:-6mm;top:10mm") + dot("9mm", MU, "left:58mm;top:11.5mm")
             + pill("36mm", "9mm", RO, "right:-4mm;top:28mm") + dot("16mm", SL, "right:18mm;top:-4mm")
             + pill("22mm", "6mm", SG, "left:20mm;top:38mm") + '</div>')
    big = (f'<div style="height:100mm;border-radius:4mm;background:{DK};position:relative;overflow:hidden">'
           f'<div class="abs" style="left:6mm;top:12mm">{word("68mm", "#2B2C33", TE)}</div>'
           f'<div class="abs" style="right:6mm;bottom:6mm">{logo("30mm", CH, TE)}</div></div>')
    cells = [f'<div>{pills}<div style="font-size:3.2mm;font-weight:700;margin-top:2.5mm">الجسور والدوائر</div>'
             f'<div style="font-size:2.8mm;color:{GREY};line-height:1.6">كبسولات بأطراف مستديرة تدخل من حافة الصفحة، ودائرة صغيرة بعدها. واحدة أو اثنتان في التصميم.</div></div>',
             f'<div>{pt}<div style="font-size:3.2mm;font-weight:700;margin-top:2.5mm">نمط الكبسولات</div>'
             f'<div style="font-size:2.8mm;color:{GREY};line-height:1.6">كبسولات صغيرة ونقاط، بشفافية 8 إلى 15%، على الفحمي فقط. بلا حروف.</div></div>',
             f'<div>{big}<div style="font-size:3.2mm;font-weight:700;margin-top:2.5mm">الكلمة الكبيرة</div>'
             f'<div style="font-size:2.8mm;color:{GREY};line-height:1.6">كلمة <span class="en">SHWANI</span> كبيرة بلون أفتح قليلاً من الخلفية، كاملة داخل الصفحة لا تقطعها الحافة.</div></div>']
    page(13, "05 · العناصر", "العناصر الجرافيكية", area(grid(cells, 3, "7mm"), top=40))


def p14_icons():
    names = ["pen", "print", "person", "card", "cap", "code", "mail", "at", "pin", "chat", "doc", "calendar", "chart", "camera", "box", "star"]
    cols = [TE, MU, RO, SL, TL, SG] * 3
    cells = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:2mm">{badge(n, c, "24mm", DK if c not in (TL, SL) else CH)}'
                    f'<span class="en" style="font-size:2.4mm;color:{GREY}">{n}</span></div>' for n, c in zip(names, cols))
    body = area(f'<div style="display:grid;grid-template-columns:repeat(8,1fr);gap:14mm 4mm">{cells}</div>'
                + p('أيقونات خطية بسمك واحد ونهايات مستديرة مثل حروف الشعار، داخل دائرة بلون الخدمة. الأيقونة فحمية على الألوان الفاتحة، وحليبية على الأزرق والأخضر المزرق.', "3.1mm", GREY, "9mm"), top=44)
    page(14, "05 · العناصر", "الأيقونات", body)


def p15_photo():
    shots = [("01-business-cards", "ضوء نهار طبيعي من نافذة"), ("13-outdoor-banner", "أماكن عراقية حقيقية"), ("11-tote", "منتجات في الاستعمال اليومي")]
    cells = [f'<div>{mock(n, "width:100%;height:96mm;border-radius:4mm")}<div style="font-size:3mm;font-weight:600;margin-top:2mm">{t}</div></div>' for n, t in shots]
    body = area(grid(cells, 3, "6mm") + f'<div style="margin-top:6mm;display:grid;grid-template-columns:1fr 1fr;gap:8mm">'
                f'<div>{bullet_list(["صور هادئة دافئة، بألوان طبيعية قريبة من ألوان الهوية", "أيدٍ تعمل، أوراق، مكاتب، أماكن من العراق", "مساحة فارغة حول الموضوع لوضع النص"], SG)}</div>'
                f'<div>{bullet_list(["لا وجوه مولّدة تُقدَّم كأنها عملاء", "لا صور مكررة من مواقع الصور المجانية الشائعة", "الصور المولّدة بالذكاء الاصطناعي يُشار إليها عند النشر"], "#B3261E")}</div></div>', top=40)
    page(15, "05 · العناصر", "أسلوب الصور", body)


def gallery(n, section, title, items, cols=2, h="70mm", sub=""):
    cells = [f'<div>{mock(m, f"width:100%;height:{h};border-radius:4mm")}<div style="font-size:3mm;font-weight:600;margin-top:2mm">{t}</div></div>' for m, t in items]
    page(n, section, title, area(grid(cells, cols, "6mm"), top=40 if not sub else 48), sub=sub)


def p16_stationery():
    gallery(16, "06 · التطبيقات", "القرطاسية الرسمية", [("02-stationery", "الورقة الرسمية، عرض السعر، الظرف، بطاقة العمل"),
                                                          ("01-business-cards", "بطاقة العمل: الوجه والظهر (90×50 مم)")], h="128mm")


def p17_print():
    gallery(17, "06 · التطبيقات", "المطبوعات", [("07-company-profile", "الملف التعريفي، 8 صفحات"), ("06-brochure", "البروشور الثلاثي"),
                                                  ("03-flyer", "فلاير A5")], cols=2, h="128mm")


def p18_signage():
    gallery(18, "06 · التطبيقات", "اللافتات", [("13-outdoor-banner", "بنر خارجي (300×100 سم)"),
                                                ("04-rollup", "رول أب (85×200 سم)")], cols=2, h="128mm")


def p19_merch():
    gallery(19, "06 · التطبيقات", "الهدايا والتغليف", [("12-tshirts", "تيشيرت: الوجه والظهر"), ("14-mugs", "أكواب"), ("11-tote", "حقيبة قماش"),
                                                         ("08-notebook", "دفتر وقلم"), ("09-packaging", "علبة هدية، كيس، ملصقات"), ("15-folder-badge", "ملف وبطاقة تعريف")],
            cols=3, h="64mm")


def p20_screens():
    cells = (f'<div>{mock("10-screens", "width:100%;height:128mm;border-radius:4mm")}<div style="font-size:3mm;font-weight:600;margin-top:2mm">الشاشات: الحاسوب والهاتف</div></div>'
             f'<div style="display:flex;flex-direction:column;gap:5mm"><div style="background:{WHITE};border-radius:4mm;padding:5mm">{flat("email-signature", "width:100%;height:auto")}'
             f'<div style="font-size:3mm;font-weight:600;margin-top:2mm">توقيع البريد الإلكتروني</div><div style="font-size:2.7mm;color:{GREY}">ملف <span class="en">HTML</span> جاهز للصق في Gmail</div></div>'
             f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:4mm">{flat("company-stamp-40mm", "width:100%;height:auto;background:#fff;border-radius:4mm;padding:3mm")}'
             f'<div style="font-size:3mm;line-height:1.7"><b>الختم الرسمي</b><br><span style="color:{GREY};font-size:2.7mm">دائري 40 مم بلون حبر واحد، يُطلب من محل الأختام بملف <span class="en">PNG</span> أو <span class="en">PDF</span>.</span></div></div></div>')
    page(20, "06 · التطبيقات", "الرقمي والختم", area(f'<div style="display:grid;grid-template-columns:1.25fr 1fr;gap:7mm;direction:rtl">{cells}</div>', top=40))


def p21_voice():
    left = (f'<div style="font-size:4.4mm;font-weight:700;margin-bottom:3mm">صوت العلامة</div>'
            + bullet_list(["واضح: جملة قصيرة وكلمة يومية، بالفصحى البسيطة", "قريب: نخاطب صاحب المشروع كأنه أمامنا", "صادق: لا مبالغة، وكل رقم بمصدره",
                           "عملي: كل منشور يعطي شيئاً يُحفظ ويُطبَّق"], TE))
    right = (f'<div style="font-size:4.4mm;font-weight:700;margin-bottom:3mm">قواعد الكتابة</div>'
             + bullet_list(["الكلمات المهمة في أول سطر من النص", "5 هاشتاغات على الأكثر", "اسم البوت بلا @ قبله: Sira_Thatiya_CV_bot",
                            "لا عبارة «تابعونا»؛ المتابعة تأتي من القيمة والموعد الثابت", "المثال التخيّلي يُكتب أنه من الخيال",
                            "لا ذكر لقوالب جاهزة؛ كل عمل مصمَّم من الصفر", "لا رقم هاتف في التصاميم: البريد ووسائل التواصل فقط",
                            "لا سعر في الفيديو؛ الأسعار في المنشورات الثابتة فقط"], SL))
    cta = (f'<div style="background:{DK};color:{CH};border-radius:5mm;padding:6mm;margin-top:6mm"><div style="font-size:3mm;color:{TE};font-weight:600">نهاية كل منشور</div>'
           f'<div style="font-size:4.6mm;font-weight:700;margin-top:1.5mm">«احفظ المنشور، وأرسله لصاحب مشروع جديد.»</div>'
           f'<div style="font-size:2.9mm;color:{CH_DIM};margin-top:1.5mm">الإرسال في الرسائل أقوى إشارة لوصول المنشور إلى غير المتابعين.</div></div>')
    page(21, "07 · دليل الميديا", "صوت العلامة وقواعد الكتابة",
         area(f'<div style="display:grid;grid-template-columns:1fr 1.25fr;gap:12mm;direction:rtl"><div>{left}{cta}</div><div>{right}</div></div>', top=40))


def p22_social():
    rows = [(DK, CH, "الصف 1", "من نحن، الخدمات والأسعار، كيف تطلب (مثبّتة)"), (CH, DK, "الصف 2", "قبل أن تصمّم، سيرتك في دقيقة، من الفكرة إلى الشعار"),
            (TL, CH, "الصف 3", "مشروع التخرج، قبل وبعد، قبل أن تصمّم 2"), (RO, DK, "الصف 4", "أعمالنا: هوية SHWANI ومشاريع العملاء")]
    rr = "".join(f'<div style="display:flex;gap:2mm;align-items:center;margin-bottom:2.5mm">'
                 + "".join(f'<div style="width:18mm;height:22mm;border-radius:1.5mm;background:{b}"></div>' for _ in range(3))
                 + f'<div style="margin-right:3mm"><div style="font-size:3mm;font-weight:700">{t}</div><div style="font-size:2.6mm;color:{GREY}">{d}</div></div></div>'
                 for b, f, t, d in rows)
    specs = bullet_list(["المنشور والكاروسيل: 1080×1350", "الريل والستوري: 1080×1920، والمحتوى المهم بين 260 و1480 بكسل من الأعلى",
                         "غلاف الريل بتصميم غلاف الكاروسيل في صفّه", "شعار SHWANI الكامل في كل منشور، ولا رمز SH ولا حرف H وحده",
                         "الخط في الشرائح 30 بكسل فأكثر، وفي الريلز 34 فأكثر"], MU)
    hl = "".join(flat(f"highlight-{i}", "width:16mm;height:16mm;border-radius:50%;object-fit:cover;object-position:center") for i in range(1, 8))
    body = area(f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12mm;direction:rtl">'
                f'<div><div style="font-size:4.4mm;font-weight:700;margin-bottom:3mm">صفوف الحساب: ثلاثة منشورات بلون واحد</div>{rr}'
                f'<div style="font-size:4.4mm;font-weight:700;margin:6mm 0 3mm">أغلفة الهايلايت</div><div style="display:flex;gap:2.5mm">{hl}</div></div>'
                f'<div><div style="font-size:4.4mm;font-weight:700;margin-bottom:3mm">المقاسات والقواعد</div>{specs}'
                f'<div style="margin-top:5mm">{flat("facebook-cover-1640x624", "width:100%;height:auto;border-radius:3mm")}'
                f'<div style="font-size:2.8mm;color:{GREY};margin-top:1.5mm">غلاف صفحة فيسبوك (1640×624)</div></div></div></div>', top=40)
    page(22, "07 · دليل الميديا", "قوالب المنشورات وصفوف الحساب", body)


def p23_plan():
    series = [("السبت", "قبل وبعد", "ريل", TE), ("الاثنين", "قبل أن تصمّم", "كاروسيل", RO), ("الثلاثاء", "سيرتك في دقيقة", "ريل", SL),
              ("الخميس", "من الفكرة إلى الشعار", "ريل", MU), ("الجمعة", "مشروع التخرج خطوة بخطوة", "كاروسيل", TL)]
    rows = "".join(f'<div style="display:flex;align-items:center;gap:4mm;padding:4.2mm 0;border-bottom:.25mm solid {RULE}">'
                   f'<span style="width:3mm;height:3mm;border-radius:50%;background:{c}"></span><span style="width:20mm;font-size:3.1mm;color:{GREY}">{d}</span>'
                   f'<span style="flex:1;font-size:3.4mm;font-weight:700">{s}</span><span style="font-size:3mm;color:{GREY}">{f}</span></div>' for d, s, f, c in series)
    kpis = [("الوصول", "كم شخصاً رأى المنشور، ومنهم غير المتابعين"), ("الحفظ", "هل المحتوى مفيد بما يكفي ليُرجع إليه"),
            ("الإرسال", "أقوى إشارة للانتشار"), ("الرسائل", "كم شخصاً سأل عن خدمة")]
    kk = "".join(f'<div style="background:{WHITE};border-radius:4mm;padding:7mm 5mm"><div style="font-size:4.2mm;font-weight:700">{k}</div>'
                 f'<div style="font-size:2.7mm;color:{GREY};line-height:1.6;margin-top:1mm">{v}</div></div>' for k, v in kpis)
    body = area(f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12mm;direction:rtl">'
                f'<div><div style="font-size:4.4mm;font-weight:700;margin-bottom:2mm">خمس سلاسل ثابتة</div>{rows}'
                f'<div style="font-size:2.9mm;color:{GREY};margin-top:3mm;line-height:1.7">منشور كل يوم الساعة 9 مساءً بتوقيت بغداد، على انستغرام وفيسبوك معاً. '
                f'تُجرَّب الساعة 6 مساءً أسبوعين ثم يُختار الأفضل من إحصاءات الحساب.</div></div>'
                f'<div><div style="font-size:4.4mm;font-weight:700;margin-bottom:3mm">ما نقيسه كل أسبوع</div>'
                f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:3mm">{kk}</div></div></div>', top=40)
    page(23, "08 · خطة النشر والتطوير", "النشر الأسبوعي", body)


def p24_growth():
    phases = [("الأيام 1 إلى 30", "البناء", ["نشر يومي بالسلاسل الخمس", "تثبيت من نحن والخدمات وكيف تطلب", "الرد على كل رسالة وتعليق خلال يوم", "ربط انستغرام بصفحة فيسبوك"], TE),
              ("الأيام 31 إلى 60", "الثقة", ["منشورات «أعمالنا» بإذن أصحابها", "آراء العملاء الأوائل مكتوبة", "ريل «قبل وبعد» لكل عمل جديد", "رد آلي على الكلمات الشائعة في التعليقات"], MU),
              ("الأيام 61 إلى 90", "النمو", ["إعلان ممول صغير لأفضل ريل", "تعاون مع صفحات طلابية ومشاريع صغيرة", "مراجعة المقاييس وتعديل المواعيد", "دليل مجاني يُرسل لمن يراسلنا"], TL)]
    cells = [f'<div style="background:{WHITE};border-radius:5mm;padding:6mm;border-top:1.4mm solid {c}"><div style="font-size:2.9mm;color:{GREY}">{t}</div>'
             f'<div style="font-size:6mm;font-weight:800;margin:1mm 0 4mm">{n}</div>{bullet_list(items, c, "3.9mm")}</div>' for t, n, items, c in phases]
    page(24, "08 · خطة النشر والتطوير", "خطة التطوير: 90 يوماً", area(grid(cells, 3, "7mm"), top=40))


def p25_files():
    groups = [("الشعار", ["SVG وPNG شفاف: الرئيسي، المعكوس، كلمة SHWANI وحدها، أسود، أبيض", "صورة الحساب 1080×1080"]),
              ("ملفات الطباعة PDF (بنزف 3 مم)", ["بطاقة العمل، الورقة الرسمية، عرض السعر، الظرف، الملف، بطاقة التعريف",
                                                 "الفلاير، البروشور، الملف التعريفي 8 صفحات", "الرول أب واللافتة والبنر بمقياس 1:10",
                                                 "الدفتر، الكوب، التيشيرت، الحقيبة، القلم، الملصقات، العلبة، الكيس، الختم"]),
              ("الرقمي", ["توقيع البريد HTML وصورة", "غلاف فيسبوك وأغلفة الهايلايت", "صور واقعية (موكاب) لكل القطع"]),
              ("المصدر", ["كل قطعة تُعاد بسكربت في مستودع shwani-media، فيتغيّر البريد أو أي نص بسطر واحد"])]
    cells = [f'<div><div style="font-size:4mm;font-weight:700;margin-bottom:2.5mm">{t}</div>{bullet_list(items, TE, "3.7mm")}</div>' for t, items in groups]
    page(25, "09 · الملفات المسلَّمة", "ماذا تجد في الباقة", area(grid(cells, 2, "10mm 14mm"), top=40))


def p26_back():
    body = (f'<div class="abs" style="inset:-3mm;{pattern(22, CH, TE, CH, MU, .09)}"></div>'
            f'<div class="abs" style="left:0;right:0;top:56mm;display:flex;justify-content:center">{logo("110mm", CH, TE)}</div>'
            f'<div class="abs" style="left:0;right:0;top:122mm;text-align:center;font-size:6mm;font-weight:700;color:{CH}">{TAG_AR}</div>'
            f'<div class="abs" style="left:0;right:0;top:140mm;display:flex;justify-content:center">{contact("3.6mm", CH, CH_DIM, TE, "2mm")}</div>'
            f'<div class="abs" style="left:0;right:0;top:170mm;text-align:center;font-size:3.2mm;color:{CH}"><b style="color:{TE}">{OTHER_AR}</b> {OTHER_LINE}</div>'
            + pill("60mm", "12mm", TE, "left:-3mm;top:186mm") + dot("8mm", MU, "left:62mm;top:188mm"))
    PAGES.append(Piece("page-26", W, H, body, bg=DK, fg=CH))


BUILD = [p01_cover, p02_contents, p03_about, p04_story, p05_primary, p06_versions, p07_space, p08_misuse, p09_core, p10_service,
         p11_ratio, p12_type, p13_elements, p14_icons, p15_photo, p16_stationery, p17_print, p18_signage, p19_merch, p20_screens,
         p21_voice, p22_social, p23_plan, p24_growth, p25_files, p26_back]


async def merge_pdf(pieces, path):
    """One PDF from all pages (no bleed; the book is read on screen or printed at home)."""
    from playwright.async_api import async_playwright
    html = "".join(f'<div class="pg">{pc.html(0).split("<body")[1].split(">", 1)[1].rsplit("</body>", 1)[0]}</div>' for pc in pieces)
    css = pieces[0].html(0).split("<style>")[1].split("</style>")[0]
    doc = (f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">{fontlinks()}<style>{css}'
           f'.pg{{width:{W}mm;height:{H}mm;position:relative;overflow:hidden;page-break-after:always}}'
           f'.pg .sheet{{position:relative}}</style></head><body>{html}</body></html>')
    # each page keeps its own background colour through its .sheet; re-inject per-page backgrounds
    for pc in pieces:
        pass
    src = os.path.join(BOOK, "book.html")
    open(src, "w", encoding="utf-8").write(doc)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        await pg.goto("file://" + src)
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(1500)
        await pg.pdf(path=path, width=f"{W}mm", height=f"{H}mm", print_background=True,
                     margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        await b.close()


if __name__ == "__main__":
    for f in BUILD:
        f()
    os.makedirs(BOOK, exist_ok=True)
    render(PAGES, pdf=False, dpi=150, outdir=BOOK)
    # per-page PDFs keep each page's own background; merge them with pypdf
    render(PAGES, png=False, outdir=BOOK)
    from pypdf import PdfWriter, PdfReader
    w = PdfWriter()
    for pc in PAGES:
        r = PdfReader(os.path.join(BOOK, "print", pc.name + ".pdf"))
        pg = r.pages[0]
        # crop the 3 mm bleed away
        mm = 72 / 25.4
        pg.mediabox.lower_left = (3 * mm, 3 * mm)
        pg.mediabox.upper_right = ((W + 3) * mm, (H + 3) * mm)
        w.add_page(pg)
    out = os.path.join(BOOK, "SHWANI-brand-book.pdf")
    with open(out, "wb") as fh:
        w.write(fh)
    print("book", out, len(PAGES))
