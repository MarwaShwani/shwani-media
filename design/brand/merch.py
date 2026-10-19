"""Printed gifts and packaging: mug wrap, T-shirt prints, tote print, notebook cover, pen imprint,
sticker sheet, gift box lid, paper bag, company stamp.
Prints for fabric and pens are transparent PNGs (one or two spot colours).
Run: python3 brand/merch.py [names...]"""
import math
from kit import *  # noqa: F401,F403


def mug_wrap():
    # 200 x 85 mm wrap for an 11 oz mug: the H and the line on one side, the logo on the other
    body = (
        f'<div class="abs" style="left:21mm;top:20mm;width:58mm;display:flex;flex-direction:column;align-items:center">'
        f'{bridge("26mm", DK, TE)}<div style="font-size:3.4mm;font-weight:600;margin-top:7mm;white-space:nowrap">{TAG_AR}</div></div>'
        f'<div class="abs" style="left:118mm;top:30mm">{logo("62mm", DK, TE)}</div>'
    )
    return Piece("mug-wrap-200x85", 200, 85, body, bg=WHITE)


def tee_front():
    body = f'<div class="abs" style="inset:0;display:flex;align-items:center;justify-content:center">{logo("96mm", CH, TE)}</div>'
    return Piece("tee-front-chest-100x40", 100, 40, body, bg="transparent")


def tee_back():
    body = (
        f'<div class="abs" style="left:0;right:0;top:20mm;display:flex;justify-content:center">{bridge("150mm", CH, TE)}</div>'
        f'<div class="abs" style="left:0;right:0;top:196mm;text-align:center;color:{CH};font-size:23mm;font-weight:800;line-height:1.25">نبني الجسر<br>بين فكرتك والنتيجة</div>'
        f'<div class="abs" style="left:0;right:0;top:282mm;display:flex;justify-content:center">{logo("70mm", CH, TE)}</div>'
    )
    return Piece("tee-back-300x340", 300, 340, body, bg="transparent")


def tote():
    body = (
        f'<div class="abs" style="left:0;right:0;top:22mm;display:flex;justify-content:center">{bridge("120mm", DK, TE)}</div>'
        f'<div class="abs" style="left:0;right:0;top:165mm;text-align:center;color:{DK};font-size:19mm;font-weight:800;line-height:1.25">نبني الجسر<br>بين فكرتك والنتيجة</div>'
        f'<div class="abs" style="left:0;right:0;top:240mm;display:flex;justify-content:center">{logo("100mm", DK, TE)}</div>'
    )
    return Piece("tote-print-280x330", 280, 330, body, bg="transparent")


def notebook():
    body = (
        f'<div class="abs" style="inset:-3mm;{pattern(15, CH, TE, CH, MU, .09)}"></div>'
        + pill("26mm", "5mm", TE, "left:125mm;top:12mm") + dot("3.6mm", MU, "left:119mm;top:12.7mm")
        + f'<div class="abs" style="left:0;right:0;top:86mm;display:flex;justify-content:center">{sh("27mm", CH, TE)}</div>'
        + f'<div class="abs" style="left:0;right:0;top:186mm;display:flex;justify-content:center">{logo("27mm", CH, TE)}</div>'
    )
    return Piece("notebook-cover-a5", 148, 210, body, bg=DK, fg=CH)


def pen():
    body = f'<div class="abs" style="inset:0;display:flex;align-items:center;justify-content:center">{logo("44mm", CH, TE)}</div>'
    return Piece("pen-imprint-50x20", 50, 20, body, bg="transparent")


def stickers():
    def circ(x, y, d, bg, inner, ring=None):
        rg = f"box-shadow:inset 0 0 0 .9mm {ring};" if ring else ""
        return (f'<div class="abs" style="left:{x}mm;top:{y}mm;width:{d}mm;height:{d}mm;border-radius:50%;background:{bg};{rg}'
                f'display:flex;align-items:center;justify-content:center;outline:.25mm dashed rgba(0,0,0,.25);outline-offset:1.6mm">{inner}</div>')
    body = (
        circ(8, 10, 40, DK, sh("15mm", CH, TE))
        + circ(57, 10, 40, CH, bridge("19mm", DK, TE), DK)
        + f'<div class="abs" style="left:8mm;top:60mm;width:89mm;height:30mm;border-radius:6mm;background:{DK};display:flex;align-items:center;'
          f'justify-content:center;outline:.25mm dashed rgba(0,0,0,.25);outline-offset:1.6mm">{logo("62mm", CH, TE)}</div>'
        + f'<div class="abs" style="left:8mm;top:100mm;width:89mm;height:15mm;border-radius:7.5mm;background:{MU};display:flex;align-items:center;'
          f'justify-content:center;font-size:4.6mm;font-weight:700;color:{DK};outline:.25mm dashed rgba(0,0,0,.25);outline-offset:1.6mm">{TAG_AR}</div>'
        + circ(8, 124, 18, TE, sh("6.5mm", DK, CH)) + circ(31, 124, 18, RO, bridge("8mm", DK, CH))
        + circ(54, 124, 18, TL, sh("6.5mm", CH, TE)) + circ(77, 124, 18, SL, bridge("8mm", CH, TE))
    )
    return Piece("sticker-sheet-a6", 105, 148, body, bg=WHITE)


def giftbox_lid():
    body = (
        f'<div class="abs" style="inset:-3mm;{pattern(18, CH, TE, CH, MU, .09)}"></div>'
        f'<div class="abs" style="left:0;right:0;top:78mm;display:flex;justify-content:center">{logo("108mm", CH, TE)}</div>'
        f'<div class="abs" style="left:0;right:0;top:136mm;text-align:center;font-size:5mm;font-weight:500;color:{CH_DIM}">{TAG_AR}</div>'
        + pill("50mm", "10mm", TE, "left:-3mm;top:20mm") + dot("7mm", MU, "left:52mm;top:21.5mm")
        + dot("16mm", SL, "left:176mm;top:170mm")
    )
    return Piece("giftbox-lid-200x200", 200, 200, body, bg=DK, fg=CH)


def paper_bag():
    body = (
        f'<div class="abs" style="left:0;right:0;top:70mm;display:flex;justify-content:center">{bridge("100mm", DK, TE)}</div>'
        f'<div class="abs" style="left:0;right:0;top:196mm;text-align:center;font-size:9mm;font-weight:800;line-height:1.3;color:{DK}">نبني الجسر<br>بين فكرتك والنتيجة</div>'
        f'<div class="abs" style="left:0;right:0;top:270mm;display:flex;justify-content:center">{logo("62mm", DK, TE)}</div>'
        + dot("14mm", RO, "left:188mm;top:24mm") + pill("44mm", "11mm", MU, "left:-3mm;top:26mm")
    )
    return Piece("paper-bag-side-240x320", 240, 320, body, bg=CH, fg=DK)


def stamp(ink=DK):
    """Round company stamp, 40 mm, one ink."""
    R = 200  # svg units, 1 mm = 10 units
    top = "SHWANI  COMPANY"
    bottom = "استوديو تصميم وخدمات تقنية · العراق"
    sw = shwani(ink, ink); W, body_sh = sw.width(), sw.svg()   # SHWANI word, no SH (19 Oct)
    k = 168 / W
    shg = f'<g transform="translate({200 - W*k/2:.1f} {200 + 700*k/2:.1f}) scale({k:.4f})">{body_sh}</g>'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" style="width:40mm;height:40mm;display:block">
<defs><path id="t" d="M 62 200 A 138 138 0 0 1 338 200"/><path id="b" d="M 44 200 A 156 156 0 0 0 356 200"/></defs>
<circle cx="200" cy="200" r="194" fill="none" stroke="{ink}" stroke-width="9"/>
<circle cx="200" cy="200" r="178" fill="none" stroke="{ink}" stroke-width="3"/>
<circle cx="200" cy="200" r="104" fill="none" stroke="{ink}" stroke-width="3"/>
<text font-family="Alexandria" font-weight="700" font-size="34" letter-spacing="6" fill="{ink}"><textPath href="#t" startOffset="50%" text-anchor="middle">{top}</textPath></text>
<text font-family="Alexandria" font-weight="600" font-size="24" fill="{ink}"><textPath href="#b" startOffset="50%" text-anchor="middle">{bottom}</textPath></text>
<circle cx="74" cy="200" r="7" fill="{ink}"/><circle cx="326" cy="200" r="7" fill="{ink}"/>
{shg}</svg>'''
    return Piece("company-stamp-40mm", 40, 40, f'<div class="abs" style="inset:0">{svg}</div>', bg="transparent")


ALL = lambda: [mug_wrap(), tee_front(), tee_back(), tote(), notebook(), pen(), stickers(), giftbox_lid(), paper_bag(), stamp()]

if __name__ == "__main__":
    import sys as _s
    only = _s.argv[1:]
    ps = [p for p in ALL() if not only or any(p.name.startswith(o) for o in only)]
    big = [p for p in ps if p.w * p.h > 60000]
    small = [p for p in ps if p not in big]
    if small:
        render(small)
    if big:
        render(big, dpi=200)
