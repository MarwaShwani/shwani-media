"""Logo files (SVG + transparent PNG) and the social kit (profile picture, Facebook cover, highlight covers).
Run: python3 brand/logos.py"""
import asyncio
from kit import *  # noqa: F401,F403
from rounded import mark_svg, avatar

LOGO = os.path.join(OUT, "logo")


def bridge_svg(color, bar, pad=30):
    W, body = bridge_svg_raw(color, bar)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-700-pad} {W+2*pad:.0f} {700+2*pad}" '
            f'width="{W+2*pad:.0f}" height="{700+2*pad}"><title>SHWANI</title>{body}</svg>')


def word_svg(color, bar, pad=30):
    s = shwani(color, bar); W = s.width()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-700-pad} {W+2*pad:.0f} {700+2*pad}" '
            f'width="{W+2*pad:.0f}" height="{700+2*pad}"><title>SHWANI</title>{s.svg()}</svg>')


def logo_set():
    """name -> svg text"""
    s = {}
    for nm, c, bar, word in [("charcoal", DK, TE, DK), ("cream", CH, TE, CH), ("black", "#000000", "#000000", "#000000"),
                             ("white", "#FFFFFF", "#FFFFFF", "#FFFFFF")]:
        s[f"shwani-logo-{nm}"] = lockup(c, bar, word)
        s[f"shwani-word-{nm}"] = word_svg(c, bar)   # 19 Oct: no SH mark, no lone H
    # 26 Oct (Marwa): SHWANI everywhere, the profile picture too (no SH)
    s["shwani-avatar-cream-1080"] = word_avatar(CH, DK, TE)
    s["shwani-avatar-charcoal-1080"] = word_avatar(DK, CH, TE)
    return s


def word_avatar(bg, color, bar, S=1080, width=800):
    """Profile picture: the SHWANI word centred, well inside the circle Instagram crops."""
    w = shwani(color, bar); W = w.width()
    k = width / W
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">'
            f'<rect width="{S}" height="{S}" fill="{bg}"/>'
            f'<g transform="translate({(S - W*k)/2:.1f} {S/2 + 700*k/2:.1f}) scale({k:.4f})">{w.svg()}</g></svg>')


def tile_svg(size=256):
    w = shwani(CH, TE); W, body = w.width(), w.svg()
    k = size * .76 / W
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">'
            f'<rect width="{size}" height="{size}" rx="{size*.18:.0f}" fill="{DK}"/>'
            f'<g transform="translate({(size - W*k)/2:.1f} {size/2 + 700*k/2:.1f}) scale({k:.4f})">{body}</g></svg>')


def fb_cover():
    # 1640 x 624 px; keep text inside the centre 1640 x 360 band that both phone and desktop show
    body = (
        f'<div class="abs" style="inset:-3mm;{pattern(14, CH, TE, CH, MU, .09)}"></div>'
        f'<div class="abs" style="right:42mm;top:50mm">{logo("118mm", CH, TE)}</div>'
        f'<div class="abs" style="right:178mm;top:50mm;width:.5mm;height:52mm;background:rgba(242,233,216,.3)"></div>'
        f'<div class="abs" style="right:190mm;top:52mm;text-align:right;color:{CH}"><div style="font-size:15mm;font-weight:800;line-height:1.22">نبني الجسر<br>بين فكرتك والنتيجة</div>'
        f'<div style="font-size:6mm;color:{CH_DIM};margin-top:4mm">{LINE_AR}</div></div>'
        + pill("70mm", "12mm", TE, "left:-3mm;top:138mm") + dot("9mm", MU, "left:74mm;top:139.5mm") + dot("26mm", SL, "left:418mm;top:-9mm")
    )
    return Piece("facebook-cover-1640x624", 433.92, 165.1, body, bg=DK, fg=CH)


HIGHLIGHTS = [("الخدمات", "pen", TE), ("الأسعار", "doc", MU), ("اطلب", "chat", RO), ("السيرة", "card", SL),
              ("المشاريع", "cap", TL), ("أعمالنا", "star", SG), ("تواصل", "mail", TE)]


def highlight(name, ic, col):
    # 1080 x 1920 story; Instagram shows the centre circle
    body = (f'<div class="abs" style="left:0;right:0;top:0;bottom:0;display:flex;align-items:center;justify-content:center">'
            f'<div style="width:170mm;height:170mm;border-radius:50%;background:{col};display:flex;align-items:center;justify-content:center">'
            f'{icon(ic, "84mm", DK if col not in (TL, SL) else CH, 1.7)}</div></div>')
    return Piece(f"highlight-{HIGHLIGHTS.index((name, ic, col))+1}", 285.75, 508, body, bg=DK, fg=CH)


async def write_logos():
    from playwright.async_api import async_playwright
    os.makedirs(os.path.join(LOGO, "svg"), exist_ok=True)
    os.makedirs(os.path.join(LOGO, "png"), exist_ok=True)
    items = logo_set()
    items["shwani-tile-256"] = tile_svg(256)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        for nm, svg in items.items():
            open(os.path.join(LOGO, "svg", nm + ".svg"), "w").write(svg)
            import re
            m = re.search(r'viewBox="([-\d. ]+)"', svg)
            vb = [float(x) for x in m.group(1).split()]
            w = 256 if "tile" in nm else (1080 if "avatar" in nm else 3000)
            h = round(w * vb[3] / vb[2])
            html = (f'<html><body style="margin:0;background:transparent">'
                    f'{svg.replace("<svg ", f"<svg style=\"width:{w}px;height:{h}px;display:block\" ", 1)}</body></html>')
            await pg.set_viewport_size({"width": w, "height": h})
            await pg.set_content(html)
            await pg.screenshot(path=os.path.join(LOGO, "png", nm + ".png"), omit_background=True,
                                clip={"x": 0, "y": 0, "width": w, "height": h})
            print("logo", nm, w, h)
        await b.close()


if __name__ == "__main__":
    asyncio.run(write_logos())
    render([fb_cover()], pdf=False, dpi=96)
    render([highlight(*h) for h in HIGHLIGHTS], pdf=False, dpi=96)
