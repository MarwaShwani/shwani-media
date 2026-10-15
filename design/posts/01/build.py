"""Post 01: carousel «من نحن» — 4 slides, 1080x1350."""
import sys, os, asyncio
HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, DESIGN)
from rounded import Word, lockup, mark, CH, MU, DK, TE  # noqa: E402

FONTS = os.environ.get("ALEXANDRIA_DIR", os.path.join(DESIGN, "node_modules", "@fontsource", "alexandria"))
SL, TL, SG, RO = "#59718A", "#2F6F6D", "#8FA68F", "#C47C8A"
HANDLE = "@shwanicompany"
N = 4

def fontlinks():
    return "".join(f'<link rel="stylesheet" href="file://{FONTS}/{w}.css">' for w in (300, 400, 500, 600, 800))

def page(body, extra_css=""):
    return f"""<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">{fontlinks()}
<style>
*{{box-sizing:border-box}}
html,body{{margin:0;background:{DK}}}
.s{{width:1080px;height:1350px;padding:72px;background:{DK};color:{CH};font-family:'Alexandria',sans-serif;
   position:relative;overflow:hidden;display:flex;flex-direction:column}}
.top{{display:flex;justify-content:space-between;align-items:center;position:relative;z-index:2}}
.chip{{padding:12px 28px;border-radius:40px;border:2px solid {CH};font-size:25px;font-weight:500}}
.count{{font-size:24px;font-weight:400;letter-spacing:2px;direction:ltr;opacity:.85}}
.bot{{display:flex;justify-content:space-between;align-items:center;position:relative;z-index:2}}
.handle{{font-size:24px;font-weight:400;direction:ltr}}
.swipe{{display:flex;align-items:center;gap:16px;font-size:28px;font-weight:600}}
h1{{margin:0;font-weight:800;line-height:1.3;position:relative;z-index:2}}
p{{margin:0;position:relative;z-index:2}}
.deco{{position:absolute;z-index:1}}
{extra_css}
</style></head><body><div class="s">{body}</div></body></html>"""

def top(chip, i):
    return f'<div class="top"><span class="chip">{chip}</span><span class="count">{i}/{N}</span></div>'

def bottom(swipe=True, right_html=None):
    arrow = (f'<svg aria-hidden="true" width="56" height="24" viewBox="0 0 56 24" fill="none" stroke="{MU}" '
             f'stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M54 12H4"/><path d="M14 2L4 12l10 10"/></svg>')
    right = right_html if right_html is not None else (f'<span class="swipe">اسحب{arrow}</span>' if swipe else "")
    return f'<div class="bot"><span class="handle">{HANDLE}</span>{right}</div>'

def lockup_svg(width):
    svg = lockup(CH, TE, CH)
    return svg.replace('width="', f'style="width:{width}px;height:auto;display:block" data-w="', 1)

def mark_inline(height):
    W, body = mark(CH, TE)
    pad = 30
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-700-pad} {W+2*pad:.0f} {700+2*pad}" '
            f'style="height:{height}px;width:auto;display:block">{body}</svg>')

# ---------- slide 1: cover ----------
def slide1():
    body = (
        top("من نحن", 1)
        + f'<div class="deco" style="left:-90px;top:1075px;width:430px;height:120px;border-radius:60px;background:{TE}"></div>'
        + f'<div class="deco" style="left:375px;top:1090px;width:90px;height:90px;border-radius:45px;background:{MU}"></div>'
        + f'<div class="deco" style="right:-60px;top:230px;width:150px;height:150px;border-radius:75px;background:{SL}"></div>'
        + '<div style="flex-grow:1"></div>'
        + f'<div style="position:relative;z-index:2;display:flex;justify-content:center">{lockup_svg(840)}</div>'
        + '<div style="height:96px"></div>'
        + '<h1 style="font-size:72px">نبني الجسر<br>بين فكرتك والنتيجة</h1>'
        + '<div style="height:28px"></div>'
        + f'<p style="font-size:32px;font-weight:400;line-height:1.7">هوية بصرية <span style="color:{MU}">•</span> سِيَر ذاتية <span style="color:{MU}">•</span> مشاريع تقنية وأكاديمية</p>'
        + '<div style="flex-grow:1"></div>'
        + bottom()
    )
    return page(body)

# ---------- slide 2: the bridge ----------
def slide2():
    w = Word(H=700, sw=160, gap=0)
    w.H_(430, CH, TE, 130)
    W = w.width()
    k = 0.62
    gw, gh = W * k, 700 * k
    hsvg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -700 {W:.0f} 700" '
            f'style="width:{gw:.0f}px;height:{gh:.0f}px;display:block">{w.svg()}</svg>')
    lab = "position:absolute;font-size:28px;font-weight:600;white-space:nowrap;transform:translateX(-50%)"
    stem = 160 * k / 2  # centre of each stem from its outer edge
    graphic = (
        f'<div style="position:relative;width:{gw:.0f}px;height:{gh+70:.0f}px;margin:0 auto;z-index:2">{hsvg}'
        f'<span style="{lab};left:{stem:.0f}px;top:{gh+22:.0f}px">النتيجة</span>'
        f'<span style="{lab};left:{gw-stem:.0f}px;top:{gh+22:.0f}px">المشكلة</span>'
        f'<span style="{lab};left:{gw/2:.0f}px;top:{gh/2-92:.0f}px;color:{TE}">الحل</span>'
        '</div>'
    )
    body = (
        top("قصة الشعار", 2)
        + f'<div class="deco" style="left:-210px;top:330px;width:360px;height:360px;border-radius:180px;background:{RO}"></div>'
        + f'<div class="deco" style="right:-40px;top:560px;width:150px;height:56px;border-radius:28px;background:{MU}"></div>'
        + '<div style="flex-grow:1"></div>'
        + graphic
        + '<div style="flex-grow:1"></div>'
        + '<h1 style="font-size:76px">في قلب اسمنا جسر</h1>'
        + '<div style="height:28px"></div>'
        + '<p style="font-size:34px;font-weight:400;line-height:1.75">ركيزتا حرف H هما المشكلة التي تأتينا بها والنتيجة التي تريدها، '
          f'والوصلة <span style="color:{TE};font-weight:600">التيراكوتا</span> بينهما هي الحل الذي نبنيه معك.</p>'
        + '<div style="height:64px"></div>'
        + bottom()
    )
    return page(body)

# ---------- slide 3: services ----------
def card(num, title, text, bg, fg):
    return (f'<div style="position:relative;z-index:2;background:{bg};color:{fg};border-radius:36px;padding:34px 40px;'
            f'display:flex;gap:32px;align-items:flex-start">'
            f'<span style="font-size:56px;font-weight:800;line-height:1;direction:ltr;opacity:.9">{num}</span>'
            f'<span style="display:flex;flex-direction:column;gap:10px">'
            f'<span style="font-size:42px;font-weight:800;line-height:1.3">{title}</span>'
            f'<span style="font-size:28px;font-weight:400;line-height:1.6">{text}</span></span></div>')

def slide3():
    body = (
        top("ماذا نقدّم", 3)
        + '<div style="height:72px"></div>'
        + '<h1 style="font-size:76px">ثلاث خدمات تكمّل بعضها</h1>'
        + '<div style="height:20px"></div>'
        + '<p style="font-size:30px;font-weight:400;line-height:1.7;max-width:860px">من يبني هوية مشروعه يحتاج غالباً سيرة أو عرضاً بالمظهر نفسه.</p>'
        + '<div style="height:52px"></div>'
        + '<div style="display:flex;flex-direction:column;gap:24px">'
        + card("01", "الهوية البصرية", "شعار وألوان وخطوط وتصاميم مطبوعة ورقمية، للشركات والمؤسسات والأفراد.", TE, DK)
        + card("02", "السيرة الذاتية", "بالعربية أو الإنجليزية، مع خطاب تغطية عند الطلب.", SL, CH)
        + card("03", "المشاريع التقنية والأكاديمية", "تخطيط وتحرير وتنسيق وتوثيق مراجع وعرض تقديمي.", TL, CH)
        + '</div>'
        + '<div style="flex-grow:1"></div>'
        + bottom()
    )
    return page(body)

# ---------- slide 4: weekly schedule ----------
def row(day, series, fmt, dot):
    return (f'<div style="display:flex;align-items:center;gap:26px;padding:27px 0;border-bottom:2px solid rgba(242,233,216,.16)">'
            f'<span style="width:22px;height:22px;border-radius:11px;background:{dot};flex-shrink:0"></span>'
            f'<span style="width:170px;font-size:32px;font-weight:600;flex-shrink:0">{day}</span>'
            f'<span style="flex-grow:1;font-size:32px;font-weight:400">{series}</span>'
            f'<span style="font-size:24px;font-weight:400;opacity:.75">{fmt}</span></div>')

def slide4():
    body = (
        top("موعدنا", 4)
        + '<div style="height:72px"></div>'
        + '<h1 style="font-size:76px">كل أسبوع هنا</h1>'
        + '<div style="height:20px"></div>'
        + '<p style="font-size:30px;font-weight:400;line-height:1.7">خمس سلاسل بمواعيد ثابتة، كل حلقة منها مفيدة وحدها.</p>'
        + '<div style="height:44px"></div>'
        + '<div style="position:relative;z-index:2;border-top:2px solid rgba(242,233,216,.16)">'
        + row("السبت", "«قبل وبعد»", "ريل", TE)
        + row("الاثنين", "«قبل أن تصمّم»", "كاروسيل", RO)
        + row("الثلاثاء", "«سيرتك في دقيقة»", "ريل", SL)
        + row("الخميس", "«من الفكرة إلى الشعار»", "ريل", MU)
        + row("الجمعة", "«مشروع التخرج خطوة بخطوة»", "كاروسيل", TL)
        + '</div>'
        + '<div style="flex-grow:1"></div>'
        + f'<div style="position:relative;z-index:2;background:{MU};color:{DK};border-radius:36px;padding:36px 44px">'
          '<div style="font-size:26px;font-weight:600;margin-bottom:10px">الحلقة الأولى، الاثنين</div>'
          '<div style="font-size:40px;font-weight:800;line-height:1.4">خمسة أخطاء تُضعف شعار مشروعك</div></div>'
        + '<div style="height:56px"></div>'
        + bottom(right_html=mark_inline(56))
    )
    return page(body)

async def render(htmls):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for i, html in enumerate(htmls, 1):
            src = os.path.join(HERE, f"slide-{i}.html")
            open(src, "w", encoding="utf-8").write(html)
            await pg.goto("file://" + src)
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(250)
            await pg.screenshot(path=os.path.join(HERE, f"slide-{i}.png"), clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
        await b.close()

if __name__ == "__main__":
    asyncio.run(render([slide1(), slide2(), slide3(), slide4()]))
    print("ok")
