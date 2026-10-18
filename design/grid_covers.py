"""Reel covers that match the carousel covers of their grid row, and a profile-grid preview.

Marwa, 18 Oct 2026: the reels must look like the posts in the same row, so the profile reads as
three clean bands (row 1 charcoal, row 2 milky, row 3 teal). Each cover is laid out exactly like a
carousel cover (chip, big visual, title, line, handle and the full SHWANI logo), then placed so that
the part Instagram shows in the grid (the centre 3:4 of the 9:16 cover) matches what a 4:5 post shows
in the grid (its centre 3:4). Row colours and accents follow SHWANI-COMPANY-project.md.

    python3 design/grid_covers.py            # covers -> design/posts/NN/cover-grid.png, preview -> design/_grid/
"""
import os, sys, asyncio, importlib.util
DESIGN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DESIGN)
from common import *  # noqa: F401,F403
from PIL import Image

ROOT = os.path.dirname(DESIGN)
OUT = os.path.join(DESIGN, "_grid")


def load(nn):
    spec = importlib.util.spec_from_file_location(f"post{nn}", os.path.join(DESIGN, "posts", nn, "build.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def chip_only(text):
    return f'<div class="top"><span class="chip">{text}</span><span></span></div>'


def cover_page(series, visual, title, line, light=True, bg=None, fg=None, logo=DK):
    body = (
        chip_only(series)
        + spacer(70)
        + f'<div class="z" style="position:relative;height:470px">{visual}</div>'
        + GROW
        + f'<h1 style="font-size:104px;line-height:1.2">{title}</h1>'
        + spacer(28)
        + f'<p style="font-size:34px;line-height:1.7">{line}</p>'
        + spacer(90)
        + bottom(right_html=lockup_svg(250, logo))
    )
    return page(body, light=light, bg=bg, fg=fg)


def shape(style):
    return f'<div aria-hidden="true" style="position:absolute;{style}"></div>'


# ---------- reel 5: سيرتك في دقيقة (row 2, milky; CV accents blue-grey and teal) ----------
def cover05():
    vis = (shape(f"right:40px;top:170px;width:420px;height:150px;border-radius:75px;background:{SL}")
           + shape(f"right:480px;top:130px;width:90px;height:90px;border-radius:45px;background:{TL}")
           + f'<div class="ltr" style="position:absolute;right:110px;top:0;font-weight:800;font-size:420px;line-height:1.1;color:{DK}">7</div>')
    return cover_page("سيرتك في دقيقة · الحلقة 1", vis, "ثوانٍ فقط<br>تُقرأ فيها سيرتك",
                      "و3 تعديلات تجعله يكمل القراءة.")


# ---------- reel 6: من الفكرة إلى الشعار (row 2, milky; identity accents terracotta and dusty pink) ----------
def cover06(m6):
    def card(right, html):
        return (f'<div style="position:absolute;right:{right}px;top:30px;width:380px;height:380px;border-radius:34px;background:{m6.PAPER};'
                f'border:3px solid {m6.SOFT};box-shadow:0 20px 44px rgba(32,33,38,.12);display:flex;align-items:center;justify-content:center">{html}</div>')
    vis = (shape(f"right:-20px;top:300px;width:560px;height:150px;border-radius:75px;background:{TE}")
           + shape(f"right:820px;top:330px;width:90px;height:90px;border-radius:45px;background:{RO}")
           + card(40, f'<div style="filter:blur(6px);opacity:.45">{m6.busy_emblem(290)}</div>')
           + card(460, m6.ring_mark(290)))
    return cover_page("من الفكرة إلى الشعار · الحلقة 1", vis, "أيّ شعار<br>ستتذكّره غداً؟",
                      "واختبر شعارك بـ3 أسئلة.")


# ---------- reel 8: قبل وبعد (row 3, teal with milky text; accents terracotta, dusty pink, sage) ----------
def cover08(m8):
    k = 470 / 640
    w = 900 * k
    half_b = f'<div style="position:absolute;inset:0;background:{m8.PAPER}">{m8.logo(0)}</div>'
    half_a = (f'<div style="position:absolute;inset:0;background:{m8.PAPER};clip-path:inset(0 0 0 450px)">'
              f'<div style="position:absolute;inset:0;display:grid;place-items:center">{m8.clean()}</div></div>')
    line = f'<div style="position:absolute;left:446px;top:0;bottom:0;width:8px;background:{DK}"></div>'
    labels = (f'<span style="position:absolute;left:28px;top:26px;padding:10px 30px;border-radius:30px;background:{RO};color:{DK};font-size:40px;font-weight:800">قبل</span>'
              f'<span style="position:absolute;right:28px;top:26px;padding:10px 30px;border-radius:30px;background:{TE};color:{DK};font-size:40px;font-weight:800">بعد</span>')
    board = (f'<div style="position:absolute;right:40px;top:0;width:{w:.0f}px;height:470px;border-radius:30px;overflow:hidden;'
             f'box-shadow:0 26px 60px rgba(0,0,0,.22)">'
             f'<div style="position:absolute;left:0;top:0;width:900px;height:640px;transform:scale({k:.4f});transform-origin:top left">'
             f'{half_b}{half_a}{line}{labels}</div></div>')
    vis = (shape(f"left:-40px;top:250px;width:300px;height:150px;border-radius:75px;background:{TE}")
           + shape(f"left:150px;top:90px;width:100px;height:100px;border-radius:50px;background:{RO}")
           + shape(f"left:40px;top:40px;width:56px;height:56px;border-radius:28px;background:{SG}")
           + board)
    return cover_page("قبل وبعد · الحلقة 1", vis, "المدرسة نفسها،<br>والفرق في الشعار",
                      "مثال توضيحي لمدرسة من الخيال.", light=False, bg=TL, fg=CH, logo=CH)


async def shoot(items, scale=2):
    """items: [(html, png_path)] rendered at 1080x1350 with device scale `scale`."""
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=scale)
        for html, png in items:
            src = png[:-4] + ".html"
            open(src, "w", encoding="utf-8").write(html)
            await pg.goto("file://" + src)
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(300)
            h = await pg.evaluate("document.querySelector('.s').scrollHeight")
            if h > 1350:
                print(f"WARNING {png} overflows: {h}px")
            await pg.screenshot(path=png, clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
        await b.close()


def to_reel(slide_png, out_png, bg):
    """Centre 3:4 of the 4:5 slide (what the grid shows) -> centre 3:4 of a 9:16 cover."""
    im = Image.open(slide_png).convert("RGB")
    s = im.width / 1080
    crop = im.crop((round(34 * s), 0, round(1046 * s), im.height))          # 1012x1350 at 1x
    zone = crop.resize((1080, 1440), Image.LANCZOS)
    cv = Image.new("RGB", (1080, 1920), bg)
    cv.paste(zone, (0, 240))
    cv.save(out_png)
    return cv


def grid_tile(png, w=360):
    """What Instagram's profile grid shows: the centre 3:4 of the image."""
    im = Image.open(png).convert("RGB")
    W, H = im.size
    if H / W > 4 / 3:          # 9:16 -> centre 3:4
        h = W * 4 / 3
        im = im.crop((0, round((H - h) / 2), W, round((H + h) / 2)))
    else:                      # 4:5 -> centre 3:4
        w3 = H * 3 / 4
        im = im.crop((round((W - w3) / 2), 0, round((W + w3) / 2), H))
    return im.resize((w, round(w * 4 / 3)), Image.LANCZOS)


# ---------- profile preview ----------
ICON = {
    "carousel": '<path d="M7 3h11a3 3 0 0 1 3 3v11" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>'
                '<rect x="3" y="7" width="14" height="14" rx="2.5" fill="#fff"/>',
    "reel": '<rect x="3" y="3" width="18" height="18" rx="4.5" fill="none" stroke="#fff" stroke-width="2.2"/>'
            '<path d="M3 8.5h18M9 3l3 5.5M15 3l3 5.5" stroke="#fff" stroke-width="2"/><path d="M10 12v6l5-3z" fill="#fff"/>',
    "pin": '<path d="M9 3h6l-1 6 3 3v2h-4v6l-1 1-1-1v-6H7v-2l3-3z" fill="#fff"/>',
}


def badge(kind):
    return (f'<svg viewBox="0 0 24 24" width="34" height="34" style="position:absolute;right:12px;top:12px;'
            f'filter:drop-shadow(0 1px 3px rgba(0,0,0,.55))">{ICON[kind]}</svg>')


def tile(png, kinds=(), tag=None):
    marks = "".join(badge(k) for k in kinds[:1])
    if "pin" in kinds and len(kinds) > 1:
        marks = badge("pin")
    label = (f'<span style="position:absolute;left:12px;bottom:12px;background:rgba(32,33,38,.78);color:#fff;'
             f'font-size:26px;font-weight:700;padding:4px 14px;border-radius:14px">{tag}</span>' if tag else "")
    img = f'<img src="file://{png}" style="display:block;width:100%;height:100%;object-fit:cover">' if png else ""
    return f'<div style="position:relative;aspect-ratio:3/4;background:#e9e3d7">{img}{marks}{label}</div>'


def placeholder(text):
    return (f'<div style="aspect-ratio:3/4;background:#f6f6f6;border:4px dashed #b9b2a5;display:flex;align-items:center;'
            f'justify-content:center;text-align:center;font-size:30px;font-weight:600;color:#8a8478;line-height:1.6;padding:20px">{text}</div>')


def profile_html(rows, avatar_svg, caption_rows=None):
    grid = "".join(f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:3px;margin-bottom:3px;direction:ltr">{"".join(r)}</div>'
                   for r in rows)
    tabs = ('<div style="display:flex;justify-content:space-around;border-top:1px solid #dbdbdb;margin-top:30px;direction:ltr">'
            + "".join(f'<div style="padding:22px 0;width:33%;display:flex;justify-content:center;{st}">'
                      f'<svg viewBox="0 0 24 24" width="44" height="44" fill="none" stroke="{c}" stroke-width="2">{p}</svg></div>'
                      for st, c, p in (
                          ("border-top:3px solid #111;margin-top:-2px", "#111", '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 3v18M15 3v18M3 9h18M3 15h18"/>'),
                          ("", "#8e8e8e", '<rect x="3" y="3" width="18" height="18" rx="4.5"/><path d="M3 8.5h18M9 3l3 5.5M15 3l3 5.5"/><path d="M10 12v6l5-3z" fill="#8e8e8e"/>'),
                          ("", "#8e8e8e", '<rect x="3" y="4" width="18" height="16" rx="3"/><circle cx="12" cy="10.5" r="3"/><path d="M6.5 20c1-3 3-4.5 5.5-4.5s4.5 1.5 5.5 4.5"/>')))
            + '</div>')
    return f"""<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">{fontlinks()}
<style>*{{box-sizing:border-box}}body{{margin:0;background:#fff;font-family:'Alexandria',sans-serif;color:#111;width:1080px}}</style></head><body>
<div style="padding:36px 40px 0;display:flex;justify-content:center;align-items:center;gap:14px;font-size:38px;font-weight:700;direction:ltr">shwanicompany</div>
<div style="display:flex;flex-direction:column;align-items:center;padding:34px 40px 0;text-align:center">
  <div style="width:210px;height:210px;border-radius:50%;background:{CH};border:2px solid #dbdbdb;display:flex;align-items:center;justify-content:center">{avatar_svg}</div>
  <div style="font-size:36px;font-weight:700;margin-top:22px;direction:ltr">SHWANI COMPANY</div>
  <div style="font-size:30px;font-weight:400;margin-top:10px;line-height:1.6">نبني الجسر بين فكرتك والنتيجة<br>هوية بصرية • سِيَر ذاتية • مشاريع تقنية وأكاديمية</div>
</div>{tabs}{grid}</body></html>"""


async def shoot_page(html, png, width=1080):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": width, "height": 800}, device_scale_factor=1)
        src = png[:-4] + ".html"
        open(src, "w", encoding="utf-8").write(html)
        await pg.goto("file://" + src)
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(400)
        await pg.screenshot(path=png, full_page=True)
        await b.close()


def preview():
    P = os.path.join(ROOT, "posts")
    D = os.path.join(DESIGN, "posts")
    t = {}
    for key, png in {
        "1": f"{P}/2026-10-15-01-intro/slide-1.png", "2": f"{P}/2026-10-16-02-prices/slide-1.png",
        "3": f"{P}/2026-10-18-03-how-to-order/slide-1.png", "4": f"{P}/2026-10-19-04-before-you-design-1/slide-1.png",
        "5": f"{D}/05/cover-grid.png", "6": f"{D}/06/cover-grid.png",
        "7": f"{P}/2026-10-18-07-graduation-project-1/slide-1.png", "8": f"{D}/08/cover-grid.png",
    }.items():
        out = os.path.join(OUT, f"tile-{key}.jpg")
        grid_tile(png).save(out, quality=92)
        t[key] = out
    avatar = mark_inline(84, DK, TE)
    # Instagram (English UI) puts the newest post on the left, so each row reads right-to-left in order.
    rows = [[tile(t["3"], ("pin",)), tile(t["2"], ("pin",)), tile(t["1"], ("pin",))],
            [tile(t["6"], ("reel",)), tile(t["5"], ("reel",)), tile(t["4"], ("carousel",))]]
    asyncio.run(shoot_page(profile_html(rows, avatar), os.path.join(OUT, "profile-6.png")))
    row3 = [[placeholder("9<br>قبل أن تصمّم 2<br>(قيد التصميم)"), tile(t["8"], ("reel",)), tile(t["7"], ("carousel",))],
            [tile(t["6"], ("reel",)), tile(t["5"], ("reel",)), tile(t["4"], ("carousel",))],
            [tile(t["3"], ("pin",)), tile(t["2"], ("pin",)), tile(t["1"], ("pin",))]]
    # with pinned posts on top the real order is pinned row first; this second image just shows row 3 beside row 2
    asyncio.run(shoot_page(profile_html([row3[2], row3[0], row3[1]], avatar), os.path.join(OUT, "profile-9.png")))
    print("preview done")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    if "--preview-only" not in sys.argv:
        m6, m8 = load("06"), load("08")
        jobs = {"05": (cover05(), CH), "06": (cover06(m6), CH), "08": (cover08(m8), TL)}
        asyncio.run(shoot([(html, os.path.join(OUT, f"slide-cover-{nn}.png")) for nn, (html, _) in jobs.items()]))
        for nn, (_, bg) in jobs.items():
            to_reel(os.path.join(OUT, f"slide-cover-{nn}.png"), os.path.join(DESIGN, "posts", nn, "cover-grid.png"), bg)
            print("cover", nn)
    preview()
