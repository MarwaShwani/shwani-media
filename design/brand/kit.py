"""SHWANI COMPANY brand kit: shared parts for the identity package (print pieces in mm).

Every piece is an HTML page at its trim size in mm. render() writes
  out/print/<name>.pdf  vector PDF with 3 mm bleed (for the printer)
  out/png/<name>.png    trim-size PNG at 300 dpi (for mockups and the brand book)
Elements that touch an edge are drawn 3 mm past it (class .bleed-*), so the PDF bleed is real.
"""
import os, sys, asyncio, base64, math, re

BRAND = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(BRAND)
sys.path.insert(0, DESIGN)
from rounded import Word, lockup, mark, shwani, company, CH, MU, DK, TE  # noqa: E402

FONTS = os.environ.get("ALEXANDRIA_DIR", os.path.join(DESIGN, "node_modules", "@fontsource", "alexandria"))
OUT = os.path.join(BRAND, "out")

# colours
RO, SL, TL, SG, PL = "#C47C8A", "#59718A", "#2F6F6D", "#8FA68F", "#5B3A62"
WHITE = "#FFFFFF"
PAPER = "#FBF7F0"        # light cream panel on white paper
GREY = "#6E6E73"         # secondary text on white
GREY2 = "#9A9AA0"        # tertiary text on white
RULE = "#E4E1DA"         # hairlines on white
CH_DIM = "rgba(242,233,216,.72)"
# the big SHWANI watermark on dark covers: letters a shade lighter than charcoal, the link a dim terracotta,
# so the word reads whole and no bright dash floats on its own (26 Oct)
WM_STEM, WM_BAR = "#2B2C33", "#4A352D"

# contact (no phone number, by Marwa's rule, 18 Oct)
EMAIL = "shwanicompany@gmail.com"
HANDLE = "shwanicompany"
SOCIAL_AR = "انستغرام · فيسبوك"
PLACE = "العراق"
CV_BOT = "Sira_Thatiya_CV_bot"
TAG_AR = "نبني الجسر بين فكرتك والنتيجة"
TAG_EN = "We build the bridge between your idea and the result"
LINE_AR = "هوية بصرية · سِيَر ذاتية · مشاريع تقنية وأكاديمية"
OWNER_AR, OWNER_EN = "مروة شواني", "Marwa Shwani"
ROLE_AR, ROLE_EN = "المؤسِّسة", "Founder"

SERVICES = [  # (key, icon, colour, title, line, details)
    ("identity", "pen", TE, "الهوية البصرية",
     "للشركات والمؤسسات والأفراد: الشعار ونسخه، الألوان والخطوط، ودليل الميديا.",
     ["الشعار ونسخه (أفقي، عمودي، رمز مختصر، أحادي اللون)", "الألوان والخطوط", "العناصر الزخرفية والأنماط", "دليل الهوية ودليل الميديا"]),
    ("corporate", "print", MU, "تصاميم الشركات والمطبوعات",
     "فلايرات، بنرات ولافتات، بروشورات، الملف التعريفي، الأوراق الرسمية، والهدايا المطبوعة.",
     ["فلايرات وبروشورات", "بنرات ولافتات ورول أب", "الملف التعريفي", "الأوراق الرسمية: بطاقة العمل، الورقة الرسمية، الظرف، عرض السعر",
      "هدايا مطبوعة: دفاتر، تيشيرتات، أقلام، أكواب", "خطة نشر وتطوير الميديا"]),
    ("people", "person", RO, "تصاميم الأفراد",
     "شعار وهوية شخصية، بطاقات العمل والدعوة، ملف الأعمال، والعروض التقديمية.",
     ["شعار وهوية شخصية", "بطاقات العمل والدعوة", "ملف الأعمال والعروض التقديمية", "تصميم حسابات التواصل", "هدايا مطبوعة بالاسم"]),
    ("cv", "card", SL, "السيرة الذاتية",
     "بالعربية والإنجليزية، مع خطاب التغطية، عبر بوت تيليغرام خلال 24 ساعة.",
     ["سيرة ذاتية احترافية بالعربية أو الإنجليزية", "خطاب تغطية للوظيفة التي تتقدّم لها", "الطلب من بوت تيليغرام " + CV_BOT, "التسليم خلال 24 ساعة"]),
    ("academic", "cap", TL, "المشاريع التقنية والأكاديمية",
     "تخطيط وتحرير وتنسيق ومراجع وعرض، والبحث يبقى عمل الطالب.",
     ["تخطيط المشروع واختيار العنوان", "التحرير والتنسيق", "المراجع والتوثيق", "العرض التقديمي للمناقشة", "التعديل الأول مجاني"]),
    ("other", "code", SG, "خدمات تقنية أخرى",
     "أخبرنا بما تحتاجه، نراجع إمكانية تنفيذه ونتواصل معك.",
     ["أي خدمة تقنية يطلبها العميل", "نراجع إمكانية تنفيذها من قِبلنا", "ثم نتواصل معك بالجواب والعرض"]),
]
STEPS = [
    ("راسلنا", "بنوع الخدمة، وسطرين عن مشروعك، ومتى تحتاجه.", TE),
    ("العرض المكتوب", "ما يشمله العمل، والمدة، والسعر.", MU),
    ("العربون ونبدأ", "عربون <span class=\"en\">50%</span> عبر زين كاش أو كي كارد.", RO),
    ("التعديلات", "جولتا تعديل في الهوية، والتعديل الأول مجاني في المشاريع.", SL),
    ("التسليم", "الملفات بكل الصيغ، ثم الدفعة الباقية.", SG),
]
DELIVERABLES = [("الشعار بكل نسخه وصيغه", TE), ("الألوان والخطوط", MU), ("القرطاسية الرسمية", RO),
                ("المطبوعات واللافتات", SG), ("الهدايا المطبوعة", SL), ("دليل الميديا", TE), ("خطة النشر", MU)]
OTHER_AR = "تحتاج خدمة تقنية أخرى؟"
OTHER_LINE = "أخبرنا بما تحتاجه، نراجع إمكانية تنفيذه ونتواصل معك."


# ---------------------------------------------------------------- logo

def _unit(v):
    m = re.match(r"^([0-9.]+)([a-z%]*)$", str(v).strip())
    return float(m.group(1)), m.group(2) or "px"


def _word_svg(height, color, bar, style="", pad=0):
    """SHWANI word (no COMPANY) at a given height. class wm: checked to stay inside the trim."""
    s = shwani(color, bar)
    W = s.width()
    return (f'<svg class="wm" xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-700-pad} {W+2*pad:.0f} {700+2*pad}" '
            f'style="height:{height};width:auto;display:block;overflow:visible;{style}">{s.svg()}</svg>')


def logo(width, color=DK, bar=TE, word=None, cls="", style=""):
    """Full SHWANI COMPANY lockup as inline SVG, width in any CSS unit."""
    svg = lockup(color, bar, word or color)
    return svg.replace('<svg ', f'<svg class="wm {cls}" style="width:{width};height:auto;display:block;{style}" ', 1) \
              .replace(' width="', ' data-w="', 1).replace(' height="1180"', '', 1)


def word(width, color=DK, bar=TE, style=""):
    """SHWANI word sized by width (any CSS unit)."""
    v, u = _unit(width)
    return _word_svg(f"{v * 700 / _W_WORD:.3f}{u}", color, bar, style)


def logo_wide(height, color=DK, bar=TE):
    """SHWANI word alone (no COMPANY), for very wide signs."""
    return _word_svg(height, color, bar)


# Marwa, 19 Oct: the identity is the word SHWANI only. No SH monogram, no lone H, no H pattern.
# sh() and bridge() keep their old names and footprint (same width as the old glyph at that height)
# but now draw the SHWANI word, so every piece that used them switches at once.
_W_SH = mark(CH, TE)[0]
_W_H = 430 + 160
_W_WORD = shwani(CH, TE).width()


def sh(height, color=CH, bar=TE, style="", pad=0):
    v, u = _unit(height)
    return _word_svg(f"{v * _W_SH / _W_WORD:.3f}{u}", color, bar, style, pad)


def bridge(height, color=CH, bar=TE, style="", pad=0):
    v, u = _unit(height)
    return _word_svg(f"{v * _W_H / _W_WORD:.3f}{u}", color, bar, style, pad)


# ---------------------------------------------------------------- pattern

def pattern(cell=16, stem=CH, bar=TE, dot=CH, dot2=MU, op=.10, scale=.42):
    """Half-drop grid of small rounded bars (the terracotta link of SHWANI) and dots, as CSS background.
    No letters, so nothing reads as a cut word at the edges. cell is the repeat in mm."""
    L, T = 44 * scale / .42, 13 * scale / .42
    def bar_at(x, y, c):
        return f'<rect x="{x - L/2:.1f}" y="{y - T/2:.1f}" width="{L:.1f}" height="{T:.1f}" rx="{T/2:.1f}" fill="{c}"/>'
    tile = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">'
            f'<g opacity="{op}">{bar_at(50, 50, bar)}{bar_at(150, 150, stem)}'
            f'<circle cx="150" cy="50" r="5" fill="{dot}"/><circle cx="50" cy="150" r="5" fill="{dot2}"/></g></svg>')
    uri = "data:image/svg+xml;base64," + base64.b64encode(tile.encode()).decode()
    return f"background-image:url('{uri}');background-size:{cell}mm {cell}mm;"


# ---------------------------------------------------------------- icons (monoline, round caps)

ICONS = {
    "mail": '<rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="M4 7.5l8 6 8-6"/>',
    "at": '<circle cx="12" cy="12" r="3.6"/><path d="M15.6 12v1.4a2.6 2.6 0 0 0 5.2 0V12a8.8 8.8 0 1 0-3.4 6.9"/>',
    "pin": '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
    "pen": '<path d="M14.5 5.5l4 4L9 19H5v-4z"/><path d="M12.5 7.5l4 4"/><path d="M4 21h16"/>',
    "print": '<path d="M7 9V4h10v5"/><rect x="3.5" y="9" width="17" height="7.5" rx="2"/><path d="M7 14h10v6H7z"/>',
    "person": '<circle cx="12" cy="8.5" r="3.8"/><path d="M4.5 20c.9-3.8 3.8-5.8 7.5-5.8s6.6 2 7.5 5.8"/>',
    "card": '<rect x="5" y="3" width="14" height="18" rx="2.5"/><circle cx="12" cy="10" r="2.6"/><path d="M8.5 17c.6-2 1.9-3 3.5-3s2.9 1 3.5 3"/>',
    "cap": '<path d="M2.5 9.5L12 5l9.5 4.5L12 14z"/><path d="M6.5 11.5V16c1.6 1.6 3.4 2.3 5.5 2.3s3.9-.7 5.5-2.3v-4.5"/><path d="M21.5 9.5v5"/>',
    "code": '<rect x="2.5" y="4" width="19" height="13" rx="2.2"/><path d="M8 20h8"/><path d="M9.5 8.5L7 10.5l2.5 2"/><path d="M14.5 8.5l2.5 2-2.5 2"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "send": '<path d="M21 3L10 14"/><path d="M21 3l-7 18-4-7-7-4z"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.5 2.6 3.7 5.6 3.7 9s-1.2 6.4-3.7 9c-2.5-2.6-3.7-5.6-3.7-9S9.5 5.6 12 3z"/>',
    "chat": '<path d="M4 5.5h16v10H9l-5 4z"/>',
    "doc": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/><path d="M9 12h6M9 16h6"/>',
    "star": '<path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8-5.2-2.8-5.2 2.8 1-5.8-4.3-4.1 5.9-.8z"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "chart": '<path d="M4 20V4"/><path d="M4 20h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>',
    "camera": '<rect x="3" y="6.5" width="18" height="13" rx="3"/><circle cx="12" cy="13" r="3.6"/><path d="M8.5 6.5l1.5-2.5h4l1.5 2.5"/>',
    "box": '<path d="M3.5 8L12 3.5 20.5 8v8L12 20.5 3.5 16z"/><path d="M3.5 8L12 12.5 20.5 8M12 12.5v8"/>',
}


def icon(name, size="5mm", color=TE, sw=1.9, style=""):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round" style="width:{size};height:{size};flex-shrink:0;display:block;{style}" '
            f'aria-hidden="true">{ICONS[name]}</svg>')


def badge(name, bg, size="10mm", fg=DK, k=.56):
    return (f'<span style="width:{size};height:{size};border-radius:50%;background:{bg};display:inline-flex;'
            f'align-items:center;justify-content:center;flex-shrink:0">{icon(name, f"calc({size}*{k})", fg)}</span>')


def contact(size="3mm", color=DK, dim=GREY, accent=TE, gap="1.6mm", place=False, align="flex-start", email=True):
    """Email line and social line (no phone)."""
    row = (f'display:flex;align-items:center;gap:1.8mm;justify-content:{align};font-size:{size};'
           f'line-height:1.25;white-space:nowrap')
    isz = f"calc({size}*1.25)"
    out = ""
    if email:
        out += (f'<div style="{row}">{icon("mail", isz, accent)}'
                f'<span class="en" style="color:{color};font-weight:500">{EMAIL}</span></div>')
    out += (f'<div style="{row};margin-top:{gap}">{icon("at", isz, accent)}'
            f'<span class="en" style="color:{color};font-weight:600">{HANDLE}</span>'
            f'<span style="color:{dim};font-weight:400">{SOCIAL_AR}</span></div>')
    if place:
        out += (f'<div style="{row};margin-top:{gap}">{icon("pin", isz, accent)}'
                f'<span style="color:{color};font-weight:500">{PLACE}</span></div>')
    return f'<div style="display:flex;flex-direction:column;align-items:{align}">{out}</div>'


def pill(w, h, color=TE, style=""):
    return f'<div class="deco" style="position:absolute;width:{w};height:{h};border-radius:{h};background:{color};{style}"></div>'


def dot(d, color=MU, style=""):
    return f'<div class="deco" style="position:absolute;width:{d};height:{d};border-radius:50%;background:{color};{style}"></div>'


# ---------------------------------------------------------------- page + render

def fontlinks():
    return "".join(f'<link rel="stylesheet" href="file://{FONTS}/{w}.css">' for w in (300, 400, 500, 600, 700, 800))


BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:transparent}
body{font-family:'Alexandria',sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{position:relative;overflow:hidden}
.bleedmode .page{overflow:visible}
.abs{position:absolute}
.en{direction:ltr;unicode-bidi:isolate}
.ltr{direction:ltr}
"""


class Piece:
    def __init__(self, name, w, h, body, css="", bg=WHITE, fg=DK, lang="ar"):
        self.name, self.w, self.h, self.body, self.css, self.bg, self.fg, self.lang = name, w, h, body, css, bg, fg, lang

    def html(self, bleed=0.0):
        W, H = self.w + 2 * bleed, self.h + 2 * bleed
        return f"""<!doctype html><html lang="{self.lang}" dir="rtl"><head><meta charset="utf-8">{fontlinks()}
<style>{BASE_CSS}
@page{{size:{W}mm {H}mm;margin:0}}
.sheet{{width:{W}mm;height:{H}mm;position:relative;overflow:hidden;background:{self.bg}}}
.page{{position:absolute;left:{bleed}mm;top:{bleed}mm;width:{self.w}mm;height:{self.h}mm;background:{self.bg};color:{self.fg}}}
{self.css}</style></head>
<body class="{'bleedmode' if bleed else ''}"><div class="sheet"><div class="page">{self.body}</div></div></body></html>"""


SAFE_MM = 1.5   # every logo stays at least this far inside the trim
PROBLEMS = []
CHECK_JS = """(m) => { const P = document.querySelector('.page').getBoundingClientRect(); const out = [];
  document.querySelectorAll('svg.wm').forEach((e, i) => { const r = e.getBoundingClientRect();
    if (r.width < 1) return;
    const d = [r.left - P.left, P.right - r.right, r.top - P.top, P.bottom - r.bottom].map(v => v / 3.7795);
    if (Math.min(...d) < m / 3.7795) out.push('logo ' + i + ' inside margins mm (L,R,T,B) = ' + d.map(v => v.toFixed(1)).join(', '));
  });
  const W = [...document.querySelectorAll('svg.wm')].map(e => e.getBoundingClientRect()).filter(r => r.width > 1);
  document.querySelectorAll('.deco').forEach((e, i) => { const r = e.getBoundingClientRect();
    W.forEach((w, j) => { if (r.left < w.right && r.right > w.left && r.top < w.bottom && r.bottom > w.top)
      out.push('shape ' + i + ' overlaps logo ' + j); }); });
  return out; }"""


async def _render(pieces, pdf=True, png=True, dpi=300, outdir=None):
    from playwright.async_api import async_playwright
    outdir = outdir or OUT
    os.makedirs(os.path.join(outdir, "print"), exist_ok=True)
    os.makedirs(os.path.join(outdir, "png"), exist_ok=True)
    os.makedirs(os.path.join(outdir, "html"), exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for pc in pieces:
            pxw, pxh = pc.w * 96 / 25.4, pc.h * 96 / 25.4
            if png:
                pg = await b.new_page(viewport={"width": math.ceil(pxw), "height": math.ceil(pxh)},
                                      device_scale_factor=dpi / 96)
                src = os.path.join(outdir, "html", pc.name + ".html")
                open(src, "w", encoding="utf-8").write(pc.html(0))
                await pg.goto("file://" + src)
                await pg.evaluate("document.fonts.ready")
                await pg.wait_for_timeout(200)
                bad = await pg.evaluate(CHECK_JS, SAFE_MM * 96 / 25.4)
                for r in bad:
                    PROBLEMS.append(f"{pc.name}: {r}")
                await pg.screenshot(path=os.path.join(outdir, "png", pc.name + ".png"),
                                    clip={"x": 0, "y": 0, "width": pxw, "height": pxh},
                                    omit_background=(pc.bg == "transparent"))
                await pg.close()
            if pdf:
                pg = await b.new_page()
                src = os.path.join(outdir, "html", pc.name + "-bleed.html")
                open(src, "w", encoding="utf-8").write(pc.html(3))
                await pg.goto("file://" + src)
                await pg.evaluate("document.fonts.ready")
                await pg.wait_for_timeout(200)
                await pg.pdf(path=os.path.join(outdir, "print", pc.name + ".pdf"),
                             width=f"{pc.w + 6}mm", height=f"{pc.h + 6}mm", print_background=True,
                             margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
                await pg.close()
            print("ok", pc.name)
        await b.close()


def render(pieces, **kw):
    asyncio.run(_render(pieces, **kw))
    if PROBLEMS:
        print("\nMEASUREMENT CHECK FAILED (logo cut or too close to the edge):")
        for p in PROBLEMS:
            print("  ", p)
        sys.exit(1)
    print("measurement check: all logos inside the trim")
