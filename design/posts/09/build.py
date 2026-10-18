"""Post 09: carousel «قبل أن تصمّم» الحلقة 2 — كيف تختار ألوان مشروعك. 7 slides.

Row 3: teal base. Marwa, 18 Oct 2026: the first version's brown, milky and slide-1 colours tired the eye.
This post now takes its colours from the palette she sent (#0E2931, #12484C, #2B7574, #861211, #E2E2E0):
white tints for text and light shapes, the deep red and its pale tints for accents, dark teals for cards.
The example is an invented jewellery shop, «ياقوت», with its own logo; the slides say it is invented.
Four easy steps: start from the feeling, three colours (60/30/10), check that text reads, differ from
the neighbours.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from common import *  # noqa: F401,F403

# palette sent by Marwa
DEEP, DARK, TEAL, RED, GREY = "#0E2931", "#12484C", "#2B7574", "#861211", "#E2E2E0"
INK = "#F4F4F2"            # white tint for text
RED_P = "#EBC4C1"          # pale red tint
RED_M = "#B5413D"          # lighter red for gem facets
ROW_BG = TL
N = 7
SERIES = "قبل أن تصمّم · الحلقة 2"
CARD = "rgba(14,41,49,.32)"
EDGE = "rgba(244,244,242,.22)"
DIM = "rgba(244,244,242,.74)"
SHOP = "ياقوت"


def pg(body):
    return page(body, bg=ROW_BG, fg=INK)


def tip(text, label="جرّب"):
    return (f'<div class="z" style="border:3px solid {RED_P};border-radius:32px;padding:26px 34px;display:flex;gap:22px;align-items:center">'
            f'<span style="flex-shrink:0;font-size:30px;font-weight:800;background:{RED};color:{INK};border-radius:24px;padding:6px 20px">{label}</span>'
            f'<span style="flex:1;font-size:32px;font-weight:500;line-height:1.55;text-wrap:balance">{text}</span></div>')


def icon(ok, size=44):
    if ok:
        return (f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 40 40" style="flex-shrink:0"><circle cx="20" cy="20" r="20" fill="{GREY}"/>'
                f'<path d="M12 20.5l5.5 5.5L28.5 14" fill="none" stroke="{DEEP}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    return (f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 40 40" style="flex-shrink:0"><circle cx="20" cy="20" r="20" fill="{RED}"/>'
            f'<path d="M14 14l12 12M26 14L14 26" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/></svg>')


BADGES = [(RED, INK), (GREY, DEEP), (RED_P, DEEP), (DEEP, INK)]


def num(k, size=56):
    bg, fg = BADGES[(k - 1) % len(BADGES)]
    return (f'<span class="ltr" style="flex-shrink:0;width:{size}px;height:{size}px;border-radius:{size // 2}px;background:{bg};color:{fg};'
            f'display:flex;align-items:center;justify-content:center;font-size:{int(size * .52)}px;font-weight:800">{k}</span>')


def swatch(color, size=64, edge=True):
    b = f"border:3px solid {EDGE};" if edge else ""
    return f'<span style="flex-shrink:0;width:{size}px;height:{size}px;border-radius:{size // 2}px;background:{color};{b}display:inline-block"></span>'


def fiction(text="مثال من الخيال"):
    return f'<span style="font-size:30px;font-weight:500;color:{DIM}">({text})</span>'


# ---------- the invented jewellery shop's logo ----------
def gem(size, fill=RED, facet=RED_M, line=GREY):
    return (f'<svg aria-hidden="true" viewBox="0 0 120 104" width="{size}" height="{size * 104 / 120:.0f}" style="display:block;flex-shrink:0">'
            f'<path d="M30 4h60l26 30-56 66L4 34z" fill="{fill}"/>'
            f'<path d="M30 4l12 30L60 4l18 30L90 4M4 34h112M42 34l18 66 18-66" fill="none" stroke="{line}" stroke-width="3.2" stroke-linejoin="round" opacity=".55"/>'
            f'<path d="M42 34h36l-18 66z" fill="{facet}" opacity=".55"/></svg>')


def logo(scale=1.0, word=DEEP, sub=DEEP, fill=RED, facet=RED_M, line=GREY):
    return (f'<div style="display:flex;align-items:center;gap:{int(26 * scale)}px">{gem(int(118 * scale), fill, facet, line)}'
            f'<div><div style="font-size:{int(78 * scale)}px;font-weight:800;line-height:1.05;color:{word};white-space:nowrap">{SHOP}</div>'
            f'<div style="font-size:{int(30 * scale)}px;font-weight:500;color:{sub};opacity:.8;margin-top:{int(8 * scale)}px;white-space:nowrap">مجوهرات · بغداد</div></div></div>')


# ---------- slides ----------
def cover():
    circles = (f'<div aria-hidden="true" style="position:absolute;right:40px;top:30px;width:380px;height:380px;border-radius:190px;background:{GREY}"></div>'
               f'<div aria-hidden="true" style="position:absolute;right:360px;top:170px;width:240px;height:240px;border-radius:120px;background:{RED};border:10px solid {ROW_BG}"></div>'
               f'<div aria-hidden="true" style="position:absolute;right:560px;top:250px;width:160px;height:160px;border-radius:80px;background:{RED_P};border:10px solid {ROW_BG}"></div>'
               f'<div aria-hidden="true" style="position:absolute;right:740px;top:110px;width:70px;height:70px;border-radius:35px;background:{DEEP}"></div>')
    body = (
        top(SERIES, 1, N)
        + spacer(70)
        + f'<div class="z" style="position:relative;height:470px">{circles}</div>'
        + GROW
        + '<h1 style="font-size:104px;line-height:1.2">كيف تختار<br>ألوان مشروعك؟</h1>'
        + spacer(28)
        + '<p style="font-size:34px;line-height:1.7">أربع خطوات سهلة قبل أن تطلب شعارك.</p>'
        + spacer(90) + bottom(arrow=RED_P)
    )
    return pg(body)


FEELINGS = [("مطعم أو مخبز", "دفء وشهية", [RED, "#E9A47C"]),
            ("عيادة أو صيدلية", "هدوء وثقة", [TEAL, "#BCD6D8"]),
            ("مجوهرات أو عطور", "فخامة", [DEEP, GREY])]


def s_feeling():
    rows = "".join(
        f'<div style="display:flex;align-items:center;gap:26px;padding:26px 30px;border-radius:30px;background:{CARD};border:2px solid {EDGE}">'
        f'<div style="display:flex;gap:10px">{"".join(swatch(c, 70) for c in cols)}</div>'
        f'<div style="flex:1"><div style="font-size:42px;font-weight:800">{feel}</div>'
        f'<div style="font-size:31px;font-weight:400;color:{DIM};margin-top:6px">{kind}</div></div></div>'
        for kind, feel, cols in FEELINGS)
    body = (
        top("الخطوة 1", 2, N)
        + spacer(52)
        + '<h1 style="font-size:66px;line-height:1.3">ابدأ بالشعور،<br>لا باللون المفضل</h1>'
        + spacer(18)
        + '<p style="font-size:33px;font-weight:400;line-height:1.65;text-wrap:balance">اسأل: ماذا أريد أن يشعر به الزبون حين يرى مشروعي؟</p>'
        + spacer(40)
        + f'<div class="z" style="display:flex;flex-direction:column;gap:18px">{rows}</div>'
        + spacer(14)
        + f'<p style="font-size:30px;font-weight:500;color:{DIM}">أمثلة شائعة، لا قواعد ثابتة.</p>'
        + GROW + tip("لونك المفضل قد لا يناسب زبونك. اختر لهم، لا لنفسك.", "تذكّر")
        + spacer(44) + bottom(arrow=RED_P)
    )
    return pg(body)


def shop_card(w=860, h=320):
    """The invented shop's card, painted 60/30/10: light grey ground, deep teal band and text, one red gem."""
    band = int(w * .3)
    return (f'<div style="width:{w}px;height:{h}px;border-radius:30px;background:{GREY};position:relative;overflow:hidden;'
            f'box-shadow:0 22px 50px rgba(0,0,0,.25)">'
            f'<div style="position:absolute;left:0;top:0;bottom:0;width:{band}px;background:{DEEP}"></div>'
            f'<div style="position:absolute;left:{band // 2 - 50}px;top:{h // 2 - 44}px;opacity:.35">'
            f'<svg aria-hidden="true" viewBox="0 0 120 104" width="100" height="87" style="display:block">'
            f'<path d="M30 4h60l26 30-56 66L4 34z" fill="none" stroke="{GREY}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M4 34h112M42 34l18 66 18-66" fill="none" stroke="{GREY}" stroke-width="3" stroke-linejoin="round"/></svg></div>'
            f'<div style="position:absolute;left:{band}px;right:0;top:0;bottom:0;display:flex;align-items:center;justify-content:center">{logo(1.0)}</div></div>')


def s_rule():
    parts = [(60, GREY, DEEP, "أساسي", "الخلفيات والمساحات الكبيرة"), (30, DEEP, INK, "مساعد", "الكتابة والأشكال"),
             (10, RED, INK, "لمسة", "ما تريده أن يُرى أولاً")]
    bar = "".join(f'<div style="flex:{p};background:{c};display:flex;align-items:center;justify-content:center;'
                  f'color:{t};font-size:34px;font-weight:800" class="ltr">{p}%</div>' for p, c, t, _, _ in parts)
    legend = "".join(f'<div style="display:flex;align-items:center;gap:20px">{swatch(c, 50)}'
                     f'<span style="font-size:36px;font-weight:800">{name} <span class="ltr">{p}%</span></span>'
                     f'<span style="font-size:31px;font-weight:400;color:{DIM}">{use}</span></div>' for p, c, _, name, use in parts)
    body = (
        top("الخطوة 2", 3, N)
        + spacer(52)
        + '<h1 style="font-size:66px;line-height:1.3">ثلاثة ألوان تكفي</h1>'
        + spacer(36)
        + f'<div class="z" style="display:flex;height:96px;border-radius:26px;overflow:hidden;border:3px solid {EDGE}">{bar}</div>'
        + spacer(34)
        + f'<div class="z" style="display:flex;flex-direction:column;gap:20px">{legend}</div>'
        + spacer(40)
        + f'<div class="z" style="display:flex;justify-content:center">{shop_card(860, 300)}</div>'
        + spacer(14)
        + f'<div class="z" style="text-align:center">{fiction("محل مجوهرات من الخيال")}</div>'
        + GROW + spacer(30) + bottom(arrow=RED_P)
    )
    return pg(body)


def sign(washed, label, ok):
    lg = (logo(.82, word="#CDCDCA", sub="#C4C4C1", fill="#E7CFCD", facet="#EADAD8", line=GREY) if washed
          else logo(.82))
    return (f'<div style="flex:1;min-width:0">'
            f'<div style="height:380px;border-radius:30px;background:{GREY};display:flex;align-items:center;justify-content:center;'
            f'box-shadow:0 18px 40px rgba(0,0,0,.22)">{lg}</div>'
            f'<div style="display:flex;align-items:center;gap:14px;margin-top:22px">{icon(ok)}'
            f'<span style="font-size:32px;font-weight:700">{label}</span></div></div>')


def s_contrast():
    body = (
        top("الخطوة 3", 4, N)
        + spacer(52)
        + '<h1 style="font-size:66px;line-height:1.3">هل يُقرأ النص<br>على لونك؟</h1>'
        + spacer(18)
        + '<p style="font-size:33px;font-weight:400;line-height:1.65;text-wrap:balance">لونان جميلان معاً قد يضيع بينهما الاسم. الفرق بين الفاتح والغامق هو ما يجعله يُقرأ.</p>'
        + spacer(48)
        + f'<div class="z" style="display:flex;gap:26px">{sign(True, "باهت لا يُقرأ", False)}{sign(False, "واضح من بعيد", True)}</div>'
        + GROW + tip("صغّر التصميم واقرأه من مسافة متر. إن تعبت عينك، فزِد الفرق بين اللونين.")
        + spacer(44) + bottom(arrow=RED_P)
    )
    return pg(body)


def mini_shop(name, mine=False):
    if mine:
        bg, fg, ring = GREY, DEEP, f"outline:6px solid {INK};outline-offset:8px;"
        mark = gem(84)
        tag = (f'<div style="position:absolute;top:-62px;left:50%;transform:translateX(-50%);white-space:nowrap;font-size:30px;font-weight:800;'
               f'background:{INK};color:{DEEP};border-radius:20px;padding:4px 18px">أنت</div>')
    else:
        bg, fg, ring, tag = "#1D1D21", "#B89B5E", "", ""
        mark = (f'<svg aria-hidden="true" viewBox="0 0 120 104" width="84" height="73" style="display:block">'
                f'<path d="M30 4h60l26 30-56 66L4 34z" fill="none" stroke="{fg}" stroke-width="5" stroke-linejoin="round"/>'
                f'<path d="M4 34h112M42 34l18 66 18-66" fill="none" stroke="{fg}" stroke-width="3" stroke-linejoin="round"/></svg>')
    return (f'<div style="position:relative;flex:1;height:300px;border-radius:24px;background:{bg};{ring}display:flex;flex-direction:column;'
            f'align-items:center;justify-content:center;gap:18px;box-shadow:0 14px 30px rgba(0,0,0,.22)">{tag}{mark}'
            f'<span style="font-size:32px;font-weight:800;color:{fg}">{name}</span></div>')


def s_neighbours():
    shops = mini_shop("محل 1") + mini_shop("محل 2") + mini_shop(SHOP, mine=True) + mini_shop("محل 3")
    body = (
        top("الخطوة 4", 5, N)
        + spacer(52)
        + '<h1 style="font-size:66px;line-height:1.3">لا تشبه جيرانك</h1>'
        + spacer(18)
        + '<p style="font-size:33px;font-weight:400;line-height:1.65;text-wrap:balance">إن كانت كل محلات المجوهرات في شارعك بالأسود والذهبي، فلون مختلف يجعلك تُرى أولاً، ويتذكّرك الزبون.</p>'
        + spacer(110)
        + f'<div class="z" style="display:flex;gap:22px">{shops}</div>'
        + spacer(22)
        + f'<div class="z" style="text-align:center">{fiction("شارع ومحلات من الخيال")}</div>'
        + GROW + tip("صوّر لافتات منافسيك، وضعها جنباً إلى جنب قبل أن تختار.")
        + spacer(44) + bottom(arrow=RED_P)
    )
    return pg(body)


STEPS = [("ابدأ بالشعور", "ماذا تريد أن يشعر به زبونك؟"),
         ("ثلاثة ألوان تكفي", 'أساسي <span class="ltr">60%</span>، ومساعد <span class="ltr">30%</span>، ولمسة <span class="ltr">10%</span>'),
         ("اختبر القراءة", "هل يُقرأ الاسم على لونك من بعيد؟"),
         ("اختلف عن جيرانك", "لون مختلف يجعلك تُرى أولاً")]


def s_summary():
    rows = "".join(f'<div style="display:flex;align-items:center;gap:26px;padding:26px 0;{"border-top:2px solid " + EDGE + ";" if k else ""}">'
                   f'{num(k + 1, 66)}<div style="flex:1"><div style="font-size:44px;font-weight:800">{a}</div>'
                   f'<div style="font-size:32px;font-weight:400;color:{DIM};margin-top:6px">{b}</div></div></div>'
                   for k, (a, b) in enumerate(STEPS))
    body = (
        top("الخلاصة", 6, N)
        + spacer(60)
        + '<h1 style="font-size:76px;line-height:1.3">ألوان مشروعك<br>في أربع خطوات</h1>'
        + spacer(30)
        + f'<div class="z">{rows}</div>'
        + GROW + tip("احفظ المنشور، وارجع إليه قبل أن تطلب شعارك.", "احفظه")
        + spacer(44) + bottom(arrow=RED_P)
    )
    return pg(body)


def closing():
    body = (
        top("الحلقة القادمة", N, N)
        + deco(f"left:-130px;top:300px;width:330px;height:330px;border-radius:165px;background:{RED_P}")
        + deco(f"left:150px;top:560px;width:90px;height:90px;border-radius:45px;background:{RED}")
        + spacer(100)
        + '<h1 style="font-size:76px;line-height:1.35">ما الشعور الذي<br>تريده لمشروعك؟</h1>'
        + spacer(24)
        + '<p style="font-size:36px;line-height:1.6">اكتبه في التعليقات بكلمة واحدة.</p>'
        + GROW
        + f'<div class="z" style="background:{GREY};color:{DEEP};border-radius:36px;padding:38px 44px">'
          f'<div style="font-size:30px;font-weight:700;margin-bottom:10px;color:{RED}">الحلقة 3</div>'
          '<div style="font-size:48px;font-weight:800;line-height:1.4">كيف تختار خط مشروعك</div></div>'
        + spacer(34)
        + '<p style="font-size:32px;font-weight:600;line-height:1.6">احفظ المنشور، وأرسله لصاحب مشروع جديد.</p>'
        + spacer(44)
        + bottom(right_html=lockup_svg(250, INK))
    )
    return pg(body)


SLIDES = [cover(), s_feeling(), s_rule(), s_contrast(), s_neighbours(), s_summary(), closing()]

if __name__ == "__main__":
    render(HERE, SLIDES)
