"""Printed gifts and packaging: mug wrap, T-shirt prints, tote print, notebook cover, executive pen and gift set,
sticker sheet, gift box lid, paper bag, company stamp.
Prints for fabric and pens are transparent PNGs (one or two spot colours).
Run: python3 brand/merch.py [names...]"""
import math
from kit import *  # noqa: F401,F403


def mug_wrap():
    # 200 x 85 mm wrap for an 11 oz mug: the SHWANI word and the line on one side, the logo on the other
    # (26 Oct: the word replaces the big H; the logo side is unchanged)
    body = (
        f'<div class="abs" style="left:21mm;top:27mm;width:58mm;display:flex;flex-direction:column;align-items:center">'
        f'{word("52mm", DK, TE)}<div style="font-size:3.6mm;font-weight:600;margin-top:5.5mm;white-space:nowrap">{TAG_AR}</div></div>'
        f'<div class="abs" style="left:118mm;top:30mm">{logo("62mm", DK, TE)}</div>'
    )
    return Piece("mug-wrap-200x85", 200, 85, body, bg=WHITE)


def tee_front():
    body = f'<div class="abs" style="inset:0;display:flex;align-items:center;justify-content:center">{logo("96mm", CH, TE)}</div>'
    return Piece("tee-front-chest-100x40", 100, 40, body, bg="transparent")


def tee_back():
    body = (
        f'<div class="abs" style="left:0;right:0;top:62mm;display:flex;justify-content:center">{word("210mm", CH, TE)}</div>'
        f'<div class="abs" style="left:0;right:0;top:132mm;text-align:center;color:{CH};font-size:23mm;font-weight:800;line-height:1.25">نبني الجسر<br>بين فكرتك والنتيجة</div>'
        f'<div class="abs" style="left:0;right:0;top:250mm;display:flex;justify-content:center">{logo("70mm", CH, TE)}</div>'
    )
    return Piece("tee-back-300x340", 300, 340, body, bg="transparent")


def tote():
    body = (
        f'<div class="abs" style="left:0;right:0;top:50mm;display:flex;justify-content:center">{word("180mm", DK, TE)}</div>'
        f'<div class="abs" style="left:0;right:0;top:112mm;text-align:center;color:{DK};font-size:19mm;font-weight:800;line-height:1.25">نبني الجسر<br>بين فكرتك والنتيجة</div>'
        f'<div class="abs" style="left:0;right:0;top:215mm;display:flex;justify-content:center">{logo("100mm", DK, TE)}</div>'
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


# ---------------------------------------------------------------- executive gifts (Marwa, 26 Oct)
# The plain printed pen is replaced by an executive pen (black lacquer, gold trim) in a gift box, and an
# executive gift set: the pen, a metal business-card holder and a leather key ring with a metal plate.
# Engraving files are one colour on a transparent background, sized to the engraving area; colour-fill
# engraving on the card holder keeps the terracotta link.
GOLD = MU          # gold fill on black lacquer (laser engraving filled with gold, or gold foil)


def _centre(inner):
    return f'<div class="abs" style="inset:0;display:flex;align-items:center;justify-content:center">{inner}</div>'


def pen_engrave():
    """Pen barrel: SHWANI word in gold, 32 mm long, engraving area 40 x 9 mm."""
    return Piece("pen-engrave-40x9", 40, 9, _centre(word("32mm", GOLD, GOLD)), bg="transparent")


def cardholder_engrave():
    """Business-card holder front (95 x 62 mm case): full logo, colour-fill engraving, area 60 x 24 mm."""
    return Piece("cardholder-engrave-60x24", 60, 24, _centre(logo("50mm", DK, TE)), bg="transparent")


def keyring_engrave():
    """Metal plate of the leather key ring: SHWANI word, area 30 x 10 mm."""
    return Piece("keyring-engrave-30x10", 30, 10, _centre(word("24mm", DK, TE)), bg="transparent")


def penbox_lid_inner():
    """Inner side of the pen box lid, printed on cream satin: 180 x 50 mm."""
    body = (f'<div class="abs" style="inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3.2mm">'
            f'{logo("62mm", DK, TE)}<div style="font-size:3.4mm;font-weight:500;color:{DK};opacity:.75">{TAG_AR}</div></div>')
    return Piece("penbox-lid-inner-180x50", 180, 50, body, bg=CH, fg=DK)


def giftset_lid_inner():
    """Inner side of the gift set lid, printed on cream satin: 250 x 170 mm."""
    body = (f'<div class="abs" style="inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7mm">'
            f'{logo("104mm", DK, TE)}<div style="font-size:6mm;font-weight:500;color:{DK};opacity:.75">{TAG_AR}</div></div>')
    return Piece("giftset-lid-inner-250x170", 250, 170, body, bg=CH, fg=DK)


def giftset_lid_outer():
    """Outer lid of the gift set box: soft-touch charcoal with the logo in gold foil, 260 x 180 mm."""
    body = _centre(logo("96mm", GOLD, GOLD))
    return Piece("giftset-lid-outer-260x180", 260, 180, body, bg=DK, fg=CH)


def stickers():
    def circ(x, y, d, bg, inner, ring=None):
        rg = f"box-shadow:inset 0 0 0 .9mm {ring};" if ring else ""
        return (f'<div class="abs" style="left:{x}mm;top:{y}mm;width:{d}mm;height:{d}mm;border-radius:50%;background:{bg};{rg}'
                f'display:flex;align-items:center;justify-content:center;outline:.25mm dashed rgba(0,0,0,.25);outline-offset:1.6mm">{inner}</div>')
    body = (
        circ(8, 10, 40, DK, word("30mm", CH, TE))
        + circ(57, 10, 40, CH, word("30mm", DK, TE), DK)
        + f'<div class="abs" style="left:8mm;top:60mm;width:89mm;height:30mm;border-radius:6mm;background:{DK};display:flex;align-items:center;'
          f'justify-content:center;outline:.25mm dashed rgba(0,0,0,.25);outline-offset:1.6mm">{logo("62mm", CH, TE)}</div>'
        + f'<div class="abs" style="left:8mm;top:100mm;width:89mm;height:15mm;border-radius:7.5mm;background:{MU};display:flex;align-items:center;'
          f'justify-content:center;font-size:4.6mm;font-weight:700;color:{DK};outline:.25mm dashed rgba(0,0,0,.25);outline-offset:1.6mm">{TAG_AR}</div>'
        + circ(8, 124, 18, TE, word("13.5mm", DK, CH)) + circ(31, 124, 18, RO, word("13.5mm", DK, CH))
        + circ(54, 124, 18, TL, word("13.5mm", CH, TE)) + circ(77, 124, 18, SL, word("13.5mm", CH, TE))
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
        f'<div class="abs" style="left:0;right:0;top:92mm;display:flex;justify-content:center">{word("150mm", DK, TE)}</div>'
        f'<div class="abs" style="left:0;right:0;top:142mm;text-align:center;font-size:9mm;font-weight:800;line-height:1.3;color:{DK}">نبني الجسر<br>بين فكرتك والنتيجة</div>'
        f'<div class="abs" style="left:0;right:0;top:255mm;display:flex;justify-content:center">{logo("62mm", DK, TE)}</div>'
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


ALL = lambda: [mug_wrap(), tee_front(), tee_back(), tote(), notebook(), pen_engrave(), cardholder_engrave(), keyring_engrave(),
               penbox_lid_inner(), giftset_lid_inner(), giftset_lid_outer(), stickers(), giftbox_lid(), paper_bag(), stamp()]

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
