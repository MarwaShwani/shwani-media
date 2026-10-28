"""Carousel «أعمالنا 2: هكذا تبدو هويتنا مطبوعة», 10 slides (Marwa, 28 Oct 2026).

Row 4: terracotta base with charcoal text and the post-10 sizes (title 70, text 32-36, bars 24-28).
One mockup per slide, shown edge to edge in a 1080x760 band so the print reads on a phone.
- slide 1: the result first (business cards) and the question «شعار واحد، كيف صار هوية كاملة؟»
- slide 2: a second, standalone hook (the signing hand), because Instagram re-serves carousels from slide 2
- slide 6: the mugs, the second strongest photo, at the midpoint where swipers drop off
- slide 10: «أيّ قطعة تريدها لمشروعك؟ اكتب رقم شريحتها», save and send, next episode without a day
No price anywhere. No storefront photo (05-storefront is excluded from every design).
Mockups are read from brand/out/mockups (the delivered package, 26-28 Oct; MOCKS env var overrides).
"""
import os, sys, asyncio
HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, DESIGN)
from common import *  # noqa: F401,F403
from rounded import lockup  # noqa: E402
from PIL import Image, ImageFilter, ImageEnhance

MOCKS = os.environ.get("MOCKS", os.path.join(DESIGN, "brand", "out", "mockups"))
ROW_BG, INK = TE, DK
DIM = "rgba(32,33,38,.74)"
N = 10
BW, BH = 1080, 760          # photo band


def mono(width, color=DK):
    svg = lockup(color, color, color)
    return svg.replace('<svg ', f'<svg class="wm" style="width:{width}px;height:auto;display:block;flex-shrink:0" ', 1) \
              .replace(' width="', ' data-w="', 1).replace(' height="1180"', '', 1)


def band_image(name, shift=0.0, BH=BH):
    """Crop the mockup to the band ratio (centre crop, shift moves it -1..1) and save it next to the slides.
    A portrait photo is shown whole over a blurred, darkened copy of itself (as in the brand film)."""
    src = Image.open(os.path.join(MOCKS, name + ".jpg")).convert("RGB")
    w, h = src.size
    out = os.path.join(HERE, f"band-{name}-{BH}.jpg")
    if h > w:
        bg = src.resize((BW, int(h * BW / w)), Image.LANCZOS)
        top = (bg.height - BH) // 2
        bg = bg.crop((0, top, BW, top + BH)).filter(ImageFilter.GaussianBlur(28))
        bg = ImageEnhance.Brightness(bg).enhance(0.72)
        fg = src.resize((int(w * BH / h), BH), Image.LANCZOS)
        bg.paste(fg, ((BW - fg.width) // 2, 0))
        bg.save(out, quality=92)
        return out
    r = BW / BH
    if w / h > r:                       # too wide: trim the sides
        cw = int(h * r)
        x0 = int((w - cw) / 2 * (1 + shift))
        box = (x0, 0, x0 + cw, h)
    else:                               # too tall: trim top and bottom
        ch = int(w / r)
        y0 = int((h - ch) / 2 * (1 + shift))
        box = (0, y0, w, y0 + ch)
    src.crop(box).resize((BW, BH), Image.LANCZOS).save(out, quality=92)
    return out


def band(name, shift=0.0, BH=BH, badge=None):
    """badge: the slide number as a charcoal sticker inside the photo's lower right corner (for «اكتب رقم شريحتها»)."""
    path = band_image(name, shift, BH)
    sticker = (f'<span class="ltr" style="position:absolute;right:72px;bottom:30px;width:92px;height:92px;border-radius:46px;'
               f'background:{DK};color:{CH};border:6px solid {TE};display:flex;align-items:center;justify-content:center;'
               f'font-size:44px;font-weight:800">{badge}</span>') if badge else ""
    return (f'<div class="z" style="margin:0 -72px;width:{BW}px;height:{BH}px;flex-shrink:0;position:relative;'
            f'background:url(\'file://{path}\') center/cover;box-shadow:0 18px 40px rgba(32,33,38,.22)">{sticker}</div>')


def num(k, size=64):
    return (f'<span class="ltr" style="flex-shrink:0;width:{size}px;height:{size}px;border-radius:{size // 2}px;background:{DK};color:{CH};'
            f'display:flex;align-items:center;justify-content:center;font-size:{int(size * .5)}px;font-weight:800">{k}</span>')


def pg(body):
    return page(body, bg=ROW_BG, fg=INK)


def piece(i, chip, photo, title, text, shift=0.0):
    body = (
        top(chip, i, N)
        + spacer(34)
        + band(photo, shift, badge=i)
        + spacer(40)
        + f'<h1 style="font-size:70px;line-height:1.25">{title}</h1>'
        + f'<p style="font-size:34px;font-weight:400;line-height:1.6;margin-top:18px;color:{DIM};text-wrap:pretty">{text}</p>'
        + GROW + bottom(arrow=DK)
    )
    return pg(body)


def cover():
    body = (
        top("أعمالنا · الحلقة 2", 1, N)
        + spacer(40)
        + '<h1 style="font-size:84px;line-height:1.22">شعار واحد،<br>كيف صار هوية كاملة؟</h1>'
        + spacer(40)
        + band("01-business-cards", BH=680)
        + spacer(36)
        + '<p style="font-size:36px;font-weight:600;line-height:1.6">هكذا تبدو هويتنا مطبوعة، قطعة قطعة.</p>'
        + GROW + bottom(arrow=DK)
    )
    return pg(body)


PIECES = [
    ("التفاصيل", "16-executive-pen", "حتى قلمك يحمل اسمك",
     'ورقة رسمية، وقلم فاخر محفور عليه <span class="ltr">SHWANI</span>، وطقم هدية لعميل مهم.'),
    ("الأوراق الرسمية", "02-stationery", "كل ورقة تخرج من مكتبك",
     "رسالة، وعرض سعر، وظرف، وبطاقة: كلها بهوية واحدة، فيعرفك الزبون من أول ورقة."),
    ("داخل الشركة", "15-folder-badge", "الملف وبطاقة الموظف",
     "الموظف يحمل اسم الشركة على صدره، والملف يجمع أوراق العميل بترتيب."),
    ("التسويق", "06-brochure", "البروشور",
     "خدماتك وطريقة العمل في ورقة تُطوى، ويأخذها الزبون معه."),
    ("الهدايا", "14-mugs", "كوب على مكتب زبونك",
     "هدية صغيرة يراها كل صباح، واسمك عليها."),
    ("التعريف بالشركة", "07-company-profile", "الملف التعريفي",
     "ثماني صفحات تعرّف بشركتك قبل أن تتكلم: من نحن، ولماذا نحن، وكيف نعمل."),
    ("المعارض", "04-rollup", "الرول أب",
     "في المعرض يُقرأ من بعيد: الاسم أولاً، ثم الجملة، ثم الخدمات."),
    ("الهدايا الفاخرة", "08-notebook", "الدفتر والقلم الفاخر",
     "هدية تبقى مع عميلك في كل اجتماع."),
]


def closing():
    body = (
        top("الحلقة القادمة", N, N)
        + deco(f"left:-110px;top:120px;width:270px;height:270px;border-radius:135px;background:{RO}")
        + deco(f"left:170px;top:300px;width:80px;height:80px;border-radius:40px;background:{CH}")
        + spacer(110)
        + '<h1 style="font-size:76px;line-height:1.35">أيّ قطعة تريدها<br>لمشروعك؟</h1>'
        + spacer(24)
        + '<p style="font-size:36px;line-height:1.6">اكتب رقم شريحتها في التعليقات، ونخبرك كيف نصمّمها لك.</p>'
        + GROW
        + f'<div class="z" style="background:{DK};color:{CH};border-radius:36px;padding:38px 44px">'
          f'<div style="font-size:30px;font-weight:700;margin-bottom:10px;color:{TE}">الحلقة 3</div>'
          '<div style="font-size:48px;font-weight:800;line-height:1.4">فيلم هويتنا</div></div>'
        + spacer(34)
        + '<p style="font-size:32px;font-weight:600;line-height:1.6">احفظ المنشور، وأرسله لصاحب مشروع جديد.</p>'
        + spacer(44)
        + bottom(right_html=mono(250))
    )
    return pg(body)


SLIDES = [cover()] + [piece(i, *p) for i, p in enumerate(PIECES, 2)] + [closing()]
assert len(SLIDES) == N

CHECK_JS = """() => { const S = document.querySelector('.s').getBoundingClientRect(), out = [];
  document.querySelectorAll('svg.wm').forEach((e, i) => { const r = e.getBoundingClientRect();
    const d = [r.left - S.left, S.right - r.right, r.top - S.top, S.bottom - r.bottom];
    if (Math.min(...d) < 40) out.push('logo ' + i + ' margins px ' + d.map(v => v.toFixed(0)).join(', ')); });
  const bot = document.querySelector('.bot').getBoundingClientRect();
  document.querySelectorAll('h1, p').forEach(e => { const r = e.getBoundingClientRect();
    if (r.bottom > bot.top - 8) out.push('text runs into the bottom bar: ' + e.textContent.slice(0, 30)); });
  return out; }"""


async def check():
    from playwright.async_api import async_playwright
    bad = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pgw = await b.new_page(viewport={"width": 1080, "height": 1350})
        for i in range(1, N + 1):
            await pgw.goto("file://" + os.path.join(HERE, f"slide-{i}.html"))
            await pgw.evaluate("document.fonts.ready")
            bad += [f"slide {i}: {r}" for r in await pgw.evaluate(CHECK_JS)]
        await b.close()
    return bad


if __name__ == "__main__":
    render(HERE, SLIDES)
    bad = asyncio.run(check())
    if bad:
        print("CHECK FAILED:", *bad, sep="\n  ")
        sys.exit(1)
    print("check: logos inside the slide, no text under the bottom bar")
