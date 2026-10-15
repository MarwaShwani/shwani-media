"""Shared helpers for SHWANI COMPANY Instagram slides (1080x1350)."""
import sys, os, asyncio
DESIGN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DESIGN)
from rounded import Word, lockup, mark, CH, MU, DK, TE  # noqa: E402,F401

FONTS = os.environ.get("ALEXANDRIA_DIR", os.path.join(DESIGN, "node_modules", "@fontsource", "alexandria"))
SL, TL, SG, RO, PL = "#59718A", "#2F6F6D", "#8FA68F", "#C47C8A", "#5B3A62"
HANDLE = "@shwanicompany"
LINE = "rgba(242,233,216,.16)"
LINE_L = "rgba(32,33,38,.16)"


def fontlinks():
    return "".join(f'<link rel="stylesheet" href="file://{FONTS}/{w}.css">' for w in (100, 300, 400, 500, 600, 700, 800))


def page(body, extra_css="", light=False):
    bg, fg = (CH, DK) if light else (DK, CH)
    return f"""<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">{fontlinks()}
<style>
*{{box-sizing:border-box}}
html,body{{margin:0;background:{bg}}}
.s{{width:1080px;height:1350px;padding:72px;background:{bg};color:{fg};font-family:'Alexandria',sans-serif;
   position:relative;overflow:hidden;display:flex;flex-direction:column}}
.top{{display:flex;justify-content:space-between;align-items:center;position:relative;z-index:2}}
.chip{{padding:12px 28px;border-radius:40px;border:2px solid currentColor;font-size:25px;font-weight:500}}
.count{{font-size:24px;font-weight:400;letter-spacing:2px;direction:ltr;opacity:.85}}
.bot{{display:flex;justify-content:space-between;align-items:center;position:relative;z-index:2}}
.handle{{font-size:24px;font-weight:400;direction:ltr}}
.swipe{{display:flex;align-items:center;gap:16px;font-size:28px;font-weight:600}}
h1{{margin:0;font-weight:800;line-height:1.3;position:relative;z-index:2}}
p{{margin:0;position:relative;z-index:2}}
.deco{{position:absolute;z-index:1}}
.z{{position:relative;z-index:2}}
.ltr{{direction:ltr;unicode-bidi:isolate}}
{extra_css}
</style></head><body><div class="s">{body}</div></body></html>"""


def top(chip, i, n):
    return f'<div class="top"><span class="chip">{chip}</span><span class="count">{i}/{n}</span></div>'


ARROW = (f'<svg aria-hidden="true" width="56" height="24" viewBox="0 0 56 24" fill="none" stroke="{MU}" '
         f'stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M54 12H4"/><path d="M14 2L4 12l10 10"/></svg>')


def bottom(swipe=True, right_html=None, arrow=MU):
    a = ARROW.replace(f'stroke="{MU}"', f'stroke="{arrow}"')
    right = right_html if right_html is not None else (f'<span class="swipe">اسحب{a}</span>' if swipe else "")
    return f'<div class="bot"><span class="handle">{HANDLE}</span>{right}</div>'


def lockup_svg(width, color=CH, word=None):
    svg = lockup(color, TE, word or color)
    return svg.replace('width="', f'style="width:{width}px;height:auto;display:block" data-w="', 1)


def mark_inline(height, color=CH, bar=TE):
    W, body = mark(color, bar)
    pad = 30
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-700-pad} {W+2*pad:.0f} {700+2*pad}" '
            f'style="height:{height}px;width:auto;display:block">{body}</svg>')


def spacer(h):
    return f'<div style="height:{h}px;flex-shrink:0"></div>'


GROW = '<div style="flex-grow:1"></div>'


def deco(style):
    return f'<div class="deco" style="{style}"></div>'


async def _render(outdir, htmls):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for i, html in enumerate(htmls, 1):
            src = os.path.join(outdir, f"slide-{i}.html")
            open(src, "w", encoding="utf-8").write(html)
            await pg.goto("file://" + src)
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(250)
            # overflow check: the slide must not grow past 1350
            h = await pg.evaluate("document.querySelector('.s').scrollHeight")
            if h > 1350:
                print(f"WARNING slide {i} overflows: {h}px")
            await pg.screenshot(path=os.path.join(outdir, f"slide-{i}.png"),
                                clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
        await b.close()


def render(outdir, htmls):
    asyncio.run(_render(outdir, htmls))
    from PIL import Image
    ims = [Image.open(os.path.join(outdir, f"slide-{i}.png")).convert("RGB") for i in range(1, len(htmls) + 1)]
    cols = min(4, len(ims))
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 450 + (cols - 1) * 20, rows * 562 + (rows - 1) * 20), "#888")
    for k, im in enumerate(ims):
        r, c = divmod(k, cols)
        sheet.paste(im.resize((450, 562)), (c * 470, r * 582))
    sheet.save(os.path.join(outdir, "contact.png"))
    print("rendered", len(ims))
