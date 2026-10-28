"""Single post «أعمالنا 4: هويتنا كاملة في صورة» (Marwa, 28 Oct 2026: the whole identity on one desk, from above).

Row 4: terracotta base with charcoal text, post-10 sizes. The photo is brand/out/mockups/17-desk-flatlay.jpg
(made by brand/flatlay.py on a blank Gemini scene). Every piece carries a number, so the question
«أيّ 3 قطع تطبعها أولاً؟ اكتب أرقامها» can be answered with three digits in the comments.
The numbers sit on a corner of each piece that has no logo under it (flatlay.ITEMS). No price.
"""
import os, sys, asyncio, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, DESIGN)
from common import *  # noqa: F401,F403
from rounded import lockup  # noqa: E402
from PIL import Image

BRAND = os.path.join(DESIGN, "brand")
spec = importlib.util.spec_from_file_location("flatlay", os.path.join(BRAND, "flatlay.py"))
FL = importlib.util.module_from_spec(spec)
sys.path.insert(0, BRAND)
spec.loader.exec_module(FL)

PHOTO = os.path.join(BRAND, "out", "mockups", "17-desk-flatlay.jpg")
CROP = (50, 60, 1807, 2240)          # the empty desk margins trimmed, still 4:5
PH = 956                              # photo height on the slide
PW = round(PH * (CROP[2] - CROP[0]) / (CROP[3] - CROP[1]))
K = PW / (CROP[2] - CROP[0])
DIM = "rgba(32,33,38,.74)"


def mono(width, color=DK):
    svg = lockup(color, color, color)
    return svg.replace('<svg ', f'<svg class="wm" style="width:{width}px;height:auto;display:block;flex-shrink:0" ', 1) \
              .replace(' width="', ' data-w="', 1).replace(' height="1180"', '', 1)


def photo():
    out = os.path.join(HERE, "photo.jpg")
    Image.open(PHOTO).convert("RGB").crop(CROP).resize((PW * 2, PH * 2), Image.LANCZOS).save(out, quality=92)
    stickers = ""
    for k, (_, (x, y)) in enumerate(FL.ITEMS, 1):
        px, py = (x - CROP[0]) * K, (y - CROP[1]) * K
        stickers += (f'<span class="ltr" style="position:absolute;left:{px - 25:.0f}px;top:{py - 25:.0f}px;width:50px;height:50px;'
                     f'border-radius:25px;background:{DK};color:{CH};border:4px solid {TE};display:flex;align-items:center;'
                     f'justify-content:center;font-size:26px;font-weight:800;box-shadow:0 4px 10px rgba(0,0,0,.25)">{k}</span>')
    return (f'<div class="z" style="align-self:center;position:relative;width:{PW}px;height:{PH}px;flex-shrink:0;border-radius:28px;'
            f'background:url(\'file://{out}\') center/cover;box-shadow:0 22px 50px rgba(32,33,38,.3)">{stickers}</div>')


def slide():
    body = (
        f'<div class="top"><span class="chip">أعمالنا · الحلقة 4</span>{mono(190)}</div>'
        + spacer(22)
        + '<h1 style="font-size:70px;line-height:1.25">هويتنا كاملة في صورة</h1>'
        + spacer(24)
        + photo()
        + GROW
        + f'<div class="bot"><span style="font-size:30px;font-weight:700">أيّ 3 قطع تطبعها أولاً؟ اكتب أرقامها.</span>'
          f'<span class="handle">{HANDLE}</span></div>'
    )
    return page(body, bg=TE, fg=DK)


CHECK_JS = """() => { const S = document.querySelector('.s').getBoundingClientRect(), out = [];
  document.querySelectorAll('svg.wm').forEach((e, i) => { const r = e.getBoundingClientRect();
    const d = [r.left - S.left, S.right - r.right, r.top - S.top, S.bottom - r.bottom];
    if (Math.min(...d) < 40) out.push('logo ' + i + ' margins ' + d.map(v => v.toFixed(0)).join(', ')); });
  const s = document.querySelector('.s'); if (s.scrollHeight > 1350) out.push('overflow ' + s.scrollHeight);
  return out; }"""


async def check():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        await pg.goto("file://" + os.path.join(HERE, "slide-1.html"))
        await pg.evaluate("document.fonts.ready")
        bad = await pg.evaluate(CHECK_JS)
        await b.close()
    return bad


if __name__ == "__main__":
    render(HERE, [slide()])
    bad = asyncio.run(check())
    if bad:
        print("CHECK FAILED:", *bad, sep="\n  ")
        sys.exit(1)
    print("check: logo inside the slide, nothing overflows")
