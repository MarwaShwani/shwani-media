"""Post 09: carousel «قبل أن تصمّم» الحلقة 2 — كيف تختار ألوان مشروعك. 7 slides.

Row 3: teal base with milky text. Accents terracotta, dusty pink and sage (no mustard in this row).
Four easy steps: start from the feeling, three colours (60/30/10), check that text reads, differ from
the neighbours. The café in the examples is invented, and the slides say so.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from common import *  # noqa: F401,F403

ROW_BG, ROW_FG = TL, CH
N = 7
SERIES = "قبل أن تصمّم · الحلقة 2"
CARD = "rgba(242,233,216,.09)"
EDGE = "rgba(242,233,216,.24)"
DIM = "rgba(242,233,216,.66)"
PAPER = "#FBF7EF"
# the invented café's palette (used on slides 3 to 5)
CREAM, COFFEE, ORANGE = "#F2E9D8", "#5A3E2B", "#E07A47"
CAFE = "مقهى الياسمين"


def pg(body):
    return page(body, bg=ROW_BG, fg=ROW_FG)


def tip(text, label="جرّب", color=TE):
    return (f'<div class="z" style="border:3px solid {color};border-radius:32px;padding:26px 34px;display:flex;gap:22px;align-items:center">'
            f'<span style="flex-shrink:0;font-size:30px;font-weight:800;background:{color};color:{DK};border-radius:24px;padding:6px 20px">{label}</span>'
            f'<span style="flex:1;font-size:32px;font-weight:500;line-height:1.55;text-wrap:balance">{text}</span></div>')


def icon(ok, size=44):
    if ok:
        return (f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 40 40" style="flex-shrink:0"><circle cx="20" cy="20" r="20" fill="{SG}"/>'
                f'<path d="M12 20.5l5.5 5.5L28.5 14" fill="none" stroke="{DK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    return (f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 40 40" style="flex-shrink:0"><circle cx="20" cy="20" r="20" fill="{RO}"/>'
            f'<path d="M14 14l12 12M26 14L14 26" fill="none" stroke="{DK}" stroke-width="4" stroke-linecap="round"/></svg>')


def num(k, color, size=56):
    return (f'<span class="ltr" style="flex-shrink:0;width:{size}px;height:{size}px;border-radius:{size // 2}px;background:{color};color:{DK};'
            f'display:flex;align-items:center;justify-content:center;font-size:{int(size * .52)}px;font-weight:800">{k}</span>')


def swatch(color, size=64, edge=False):
    b = f"border:3px solid {EDGE};" if edge else ""
    return f'<span style="flex-shrink:0;width:{size}px;height:{size}px;border-radius:{size // 2}px;background:{color};{b}display:inline-block"></span>'


def fiction(text="مثال من الخيال"):
    return f'<span style="font-size:30px;font-weight:500;color:{DIM}">({text})</span>'


# ---------- slides ----------
def cover():
    circles = (f'<div aria-hidden="true" style="position:absolute;right:40px;top:30px;width:380px;height:380px;border-radius:190px;background:{TE}"></div>'
               f'<div aria-hidden="true" style="position:absolute;right:360px;top:170px;width:240px;height:240px;border-radius:120px;background:{RO};border:10px solid {TL}"></div>'
               f'<div aria-hidden="true" style="position:absolute;right:560px;top:250px;width:160px;height:160px;border-radius:80px;background:{SG};border:10px solid {TL}"></div>'
               f'<div aria-hidden="true" style="position:absolute;right:740px;top:110px;width:70px;height:70px;border-radius:35px;background:{CH}"></div>')
    body = (
        top(SERIES, 1, N)
        + spacer(70)
        + f'<div class="z" style="position:relative;height:470px">{circles}</div>'
        + GROW
        + '<h1 style="font-size:104px;line-height:1.2">كيف تختار<br>ألوان مشروعك؟</h1>'
        + spacer(28)
        + '<p style="font-size:34px;line-height:1.7">أربع خطوات سهلة قبل أن تطلب شعارك.</p>'
        + spacer(90) + bottom(arrow=TE)
    )
    return pg(body)


FEELINGS = [("مطعم أو مخبز", "دفء وشهية", ["#E07A47", "#C0392B"]),
            ("عيادة أو صيدلية", "هدوء وثقة", ["#3A7CA5", "#6BAA75"]),
            ("عطور أو مجوهرات", "فخامة", ["#1B1B1F", "#C9A227"])]


def s_feeling():
    rows = "".join(
        f'<div style="display:flex;align-items:center;gap:26px;padding:26px 30px;border-radius:30px;background:{CARD};border:2px solid {EDGE}">'
        f'<div style="display:flex;gap:10px">{"".join(swatch(c, 70, True) for c in cols)}</div>'
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
        + GROW + tip("لونك المفضل قد لا يناسب زبونك. اختر لهم، لا لنفسك.", "تذكّر", RO)
        + spacer(44) + bottom(arrow=TE)
    )
    return pg(body)


def cafe_card(w=880, h=400):
    """The invented café's card, painted 60/30/10: cream ground, coffee text, one orange accent."""
    return (f'<div style="width:{w}px;height:{h}px;border-radius:30px;background:{CREAM};position:relative;overflow:hidden;'
            f'box-shadow:0 22px 50px rgba(0,0,0,.22);display:flex;flex-direction:column;justify-content:center;padding:0 60px">'
            f'<div style="position:absolute;left:0;top:0;bottom:0;width:{int(w * .3)}px;background:{COFFEE}"></div>'
            f'<div style="position:absolute;left:{int(w * .3) - 60}px;top:{h // 2 - 60}px;width:120px;height:120px;border-radius:60px;background:{ORANGE}"></div>'
            f'<div style="position:relative;font-size:54px;font-weight:800;white-space:nowrap;color:{COFFEE};padding-left:{int(w * .3) + 40}px">{CAFE}</div>'
            f'<div style="position:relative;font-size:32px;font-weight:500;color:{COFFEE};opacity:.8;margin-top:10px;padding-left:{int(w * .3) + 40}px">قهوة مختصة · بغداد</div></div>')


def s_rule():
    parts = [(60, CREAM, "أساسي", "الخلفيات والمساحات الكبيرة"), (30, COFFEE, "مساعد", "الكتابة والأشكال"), (10, ORANGE, "لمسة", "ما تريده أن يُرى أولاً")]
    bar = "".join(f'<div style="flex:{p};background:{c};display:flex;align-items:center;justify-content:center;'
                  f'color:{DK if c != COFFEE else CH};font-size:34px;font-weight:800" class="ltr">{p}%</div>' for p, c, _, _ in parts)
    legend = "".join(f'<div style="display:flex;align-items:center;gap:20px">{swatch(c, 50, True)}'
                     f'<span style="font-size:36px;font-weight:800">{name} <span class="ltr">{p}%</span></span>'
                     f'<span style="font-size:31px;font-weight:400;color:{DIM}">{use}</span></div>' for p, c, name, use in parts)
    body = (
        top("الخطوة 2", 3, N)
        + spacer(52)
        + '<h1 style="font-size:66px;line-height:1.3">ثلاثة ألوان تكفي</h1>'
        + spacer(36)
        + f'<div class="z" style="display:flex;height:96px;border-radius:26px;overflow:hidden;border:3px solid {EDGE}">{bar}</div>'
        + spacer(34)
        + f'<div class="z" style="display:flex;flex-direction:column;gap:20px">{legend}</div>'
        + spacer(40)
        + f'<div class="z" style="display:flex;justify-content:center">{cafe_card(860, 300)}</div>'
        + spacer(14)
        + f'<div class="z" style="text-align:center">{fiction("مقهى من الخيال")}</div>'
        + GROW + spacer(30) + bottom(arrow=TE)
    )
    return pg(body)


def sign(fg, bg, label, ok):
    return (f'<div style="flex:1;min-width:0">'
            f'<div style="height:380px;border-radius:30px;background:{bg};display:flex;align-items:center;justify-content:center;'
            f'box-shadow:0 18px 40px rgba(0,0,0,.2)">'
            f'<span style="font-size:48px;font-weight:800;white-space:nowrap;color:{fg}">{CAFE}</span></div>'
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
        + f'<div class="z" style="display:flex;gap:26px">{sign("#E9C9A6", CREAM, "باهت لا يُقرأ", False)}{sign(COFFEE, CREAM, "واضح من بعيد", True)}</div>'
        + GROW + tip("صغّر التصميم واقرأه من مسافة متر. إن تعبت عينك، فزِد الفرق بين اللونين.")
        + spacer(44) + bottom(arrow=TE)
    )
    return pg(body)


def mini_shop(bg, fg, name, mine=False):
    ring = f"outline:6px solid {CH};outline-offset:8px;" if mine else ""
    tag = (f'<div style="position:absolute;top:-62px;left:50%;transform:translateX(-50%);white-space:nowrap;font-size:30px;font-weight:800;'
           f'background:{CH};color:{DK};border-radius:20px;padding:4px 18px">أنت</div>' if mine else "")
    return (f'<div style="position:relative;flex:1;height:300px;border-radius:24px;background:{bg};{ring}display:flex;flex-direction:column;'
            f'align-items:center;justify-content:center;gap:12px;box-shadow:0 14px 30px rgba(0,0,0,.2)">{tag}'
            f'<svg aria-hidden="true" width="64" height="64" viewBox="0 0 64 64" fill="none" stroke="{fg}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M12 26h34v14a14 14 0 0 1-14 14h-6a14 14 0 0 1-14-14z"/><path d="M46 30h4a6 6 0 0 1 0 12h-5M22 8c-3 4 3 6 0 10M32 8c-3 4 3 6 0 10"/></svg>'
            f'<span style="font-size:30px;font-weight:800;color:{fg}">{name}</span></div>')


def s_neighbours():
    brown, beige = "#6B4A33", "#E8D9C4"
    shops = (mini_shop(brown, beige, "مقهى 1") + mini_shop(brown, beige, "مقهى 2")
             + mini_shop(SG, DK, "الياسمين", mine=True) + mini_shop(brown, beige, "مقهى 3"))
    body = (
        top("الخطوة 4", 5, N)
        + spacer(52)
        + '<h1 style="font-size:66px;line-height:1.3">لا تشبه جيرانك</h1>'
        + spacer(18)
        + '<p style="font-size:33px;font-weight:400;line-height:1.65;text-wrap:balance">إن كانت كل المقاهي في شارعك بنّية، فلون مختلف يجعلك تُرى أولاً، ويتذكّرك الزبون.</p>'
        + spacer(110)
        + f'<div class="z" style="display:flex;gap:22px">{shops}</div>'
        + spacer(22)
        + f'<div class="z" style="text-align:center">{fiction("شارع ومقاهٍ من الخيال")}</div>'
        + GROW + tip("صوّر لافتات منافسيك، وضعها جنباً إلى جنب قبل أن تختار.")
        + spacer(44) + bottom(arrow=TE)
    )
    return pg(body)


STEPS = [("ابدأ بالشعور", "ماذا تريد أن يشعر به زبونك؟"),
         ("ثلاثة ألوان تكفي", 'أساسي <span class="ltr">60%</span>، ومساعد <span class="ltr">30%</span>، ولمسة <span class="ltr">10%</span>'),
         ("اختبر القراءة", "هل يُقرأ الاسم على لونك من بعيد؟"),
         ("اختلف عن جيرانك", "لون مختلف يجعلك تُرى أولاً")]


def s_summary():
    rows = "".join(f'<div style="display:flex;align-items:center;gap:26px;padding:26px 0;{"border-top:2px solid " + EDGE + ";" if k else ""}">'
                   f'{num(k + 1, (TE, RO, SG, TE)[k], 66)}<div style="flex:1"><div style="font-size:44px;font-weight:800">{a}</div>'
                   f'<div style="font-size:32px;font-weight:400;color:{DIM};margin-top:6px">{b}</div></div></div>'
                   for k, (a, b) in enumerate(STEPS))
    body = (
        top("الخلاصة", 6, N)
        + spacer(60)
        + '<h1 style="font-size:76px;line-height:1.3">ألوان مشروعك<br>في أربع خطوات</h1>'
        + spacer(30)
        + f'<div class="z">{rows}</div>'
        + GROW + tip("احفظ المنشور، وارجع إليه قبل أن تطلب شعارك.", "احفظه", RO)
        + spacer(44) + bottom(arrow=TE)
    )
    return pg(body)


def closing():
    body = (
        top("الحلقة القادمة", N, N)
        + deco(f"left:-130px;top:300px;width:330px;height:330px;border-radius:165px;background:{RO};opacity:.9")
        + deco(f"left:150px;top:560px;width:90px;height:90px;border-radius:45px;background:{SG}")
        + spacer(100)
        + '<h1 style="font-size:76px;line-height:1.35">ما الشعور الذي<br>تريده لمشروعك؟</h1>'
        + spacer(24)
        + '<p style="font-size:36px;line-height:1.6">اكتبه في التعليقات بكلمة واحدة.</p>'
        + GROW
        + f'<div class="z" style="background:{TE};color:{DK};border-radius:36px;padding:38px 44px">'
          '<div style="font-size:30px;font-weight:600;margin-bottom:10px">الحلقة 3</div>'
          '<div style="font-size:48px;font-weight:800;line-height:1.4">كيف تختار خط مشروعك</div></div>'
        + spacer(34)
        + '<p style="font-size:32px;font-weight:600;line-height:1.6">احفظ المنشور، وأرسله لصاحب مشروع جديد.</p>'
        + spacer(44)
        + bottom(right_html=lockup_svg(250, CH))
    )
    return pg(body)


SLIDES = [cover(), s_feeling(), s_rule(), s_contrast(), s_neighbours(), s_summary(), closing()]

if __name__ == "__main__":
    render(HERE, SLIDES)
