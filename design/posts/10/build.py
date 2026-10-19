"""Post 10: carousel «أعمالنا» الحلقة 1 — كيف صمّمنا شعار SHWANI. 7 slides.

Row 4: terracotta base (#E07A47) with charcoal text and the original sizes (Marwa, 20 Oct: white text,
bigger phone sizes and teal background capsules were tried and dropped: the slides got crowded).
No price in any post (Marwa, 19 Oct): the closing slide's price line is gone.
Teal (#2F6F6D) is an identity colour since 20 Oct, so slide 5 shows six colours.
Marwa, 19 Oct 2026:
- the identity is the word SHWANI only: no SH monogram, no lone H, no H pattern. Every slide that
  talks about the link shows the whole word, with the link marked inside it.
- no logo or word is cut at the slide edge; check_marks() below fails the build if one is.
The terracotta link would vanish on a terracotta ground, so the logo always sits on a charcoal or milky card.
"""
import os, sys, re, asyncio
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from common import *  # noqa: F401,F403
from rounded import shwani, lockup  # noqa: E402

ROW_BG = TE
INK = DK                       # text on terracotta
DIM = "rgba(32,33,38,.72)"
CARD_D = DK                    # charcoal card, milky text
CARD_L = CH                    # milky card, charcoal text
N = 7
SERIES = "أعمالنا · الحلقة 1"
WS = shwani(DK, TE).width()    # 4205 units at cap height 700


def pg(body):
    return page(body, bg=ROW_BG, fg=INK)


def word(width, color=CH, bar=TE, sharp=False):
    """The SHWANI word alone, width in px. sharp=True draws the same letters with square ends (for the comparison)."""
    svg = shwani(color, bar).svg()
    if sharp:
        svg = svg.replace('stroke-linecap="round" stroke-linejoin="round"', 'stroke-linecap="butt" stroke-linejoin="miter"')
    return (f'<svg class="wm" aria-label="SHWANI" viewBox="-30 -730 {WS + 60:.0f} 760" '
            f'style="width:{width}px;height:auto;display:block;flex-shrink:0">{svg}</svg>')


def full(width, color=CH, sub=None):
    svg = lockup(color, TE, sub or color)
    return svg.replace('<svg ', f'<svg class="wm" style="width:{width}px;height:auto;display:block;flex-shrink:0" ', 1) \
              .replace(' width="', ' data-w="', 1).replace(' height="1180"', '', 1)


def mono(width, color=DK):
    """One-colour lockup: on terracotta the terracotta link would vanish, so the whole logo takes one ink."""
    svg = lockup(color, color, color)
    return svg.replace('<svg ', f'<svg class="wm" style="width:{width}px;height:auto;display:block;flex-shrink:0" ', 1) \
              .replace(' width="', ' data-w="', 1).replace(' height="1180"', '', 1)


def card(inner, bg=CARD_D, pad="56px 60px", style=""):
    return f'<div class="z" style="background:{bg};border-radius:40px;padding:{pad};{style}">{inner}</div>'


def num(k, size=60, bg=DK, fg=CH):
    return (f'<span class="ltr" style="flex-shrink:0;width:{size}px;height:{size}px;border-radius:{size // 2}px;background:{bg};color:{fg};'
            f'display:flex;align-items:center;justify-content:center;font-size:{int(size * .5)}px;font-weight:800">{k}</span>')


def tip(text, label="الفكرة"):
    return (f'<div class="z" style="border:3px solid {DK};border-radius:32px;padding:26px 34px;display:flex;gap:22px;align-items:center">'
            f'<span style="flex-shrink:0;font-size:30px;font-weight:800;background:{DK};color:{CH};border-radius:24px;padding:6px 20px">{label}</span>'
            f'<span style="flex:1;font-size:32px;font-weight:500;line-height:1.55;text-wrap:balance">{text}</span></div>')


# ---------- slides ----------

def cover():
    big = card(f'<div style="display:flex;justify-content:center">{full(640, CH)}</div>', CARD_D, "92px 60px 84px",
               "box-shadow:0 26px 60px rgba(32,33,38,.28)")
    body = (
        top(SERIES, 1, N)
        + deco(f"right:-90px;top:120px;width:300px;height:300px;border-radius:150px;background:{RO}")
        + deco(f"left:70px;top:150px;width:110px;height:110px;border-radius:55px;background:{CH}")
        + deco(f"left:-60px;top:360px;width:250px;height:76px;border-radius:38px;background:{MU}")
        + spacer(250)
        + big
        + GROW
        + '<h1 style="font-size:96px;line-height:1.2">كيف صمّمنا<br>شعار <span class="ltr">SHWANI</span>؟</h1>'
        + spacer(26)
        + '<p style="font-size:34px;line-height:1.7">قصة هويتنا، من الفكرة إلى الشعار.</p>'
        + spacer(70) + bottom(arrow=DK)
    )
    return pg(body)


GOALS = [("يُقرأ بسهولة", "من بعيد على لافتة، ومن قريب على بطاقة صغيرة."),
         ("بسيط", "لون واحد يكفيه، فيُطبع على أي شيء: ورق، قماش، خشب."),
         ("له معنى", "يحكي ما نفعله لعملائنا، لا مجرد حروف جميلة.")]


def s_goals():
    rows = "".join(
        f'<div style="display:flex;align-items:center;gap:28px;padding:30px 0;{"border-top:2px solid rgba(32,33,38,.18);" if k else ""}">'
        f'{num(k + 1, 70)}<div style="flex:1"><div style="font-size:46px;font-weight:800">{a}</div>'
        f'<div style="font-size:33px;font-weight:400;color:{DIM};margin-top:8px;line-height:1.5">{b}</div></div></div>'
        for k, (a, b) in enumerate(GOALS))
    body = (
        top("قبل الرسم", 2, N)
        + spacer(60)
        + '<h1 style="font-size:70px;line-height:1.3">قبل أن نرسم،<br>كتبنا ماذا نريد</h1>'
        + spacer(22)
        + '<p style="font-size:34px;font-weight:400;line-height:1.65">ثلاثة شروط وضعناها لشعارنا، كما نضعها مع كل عميل:</p>'
        + spacer(30)
        + f'<div class="z">{rows}</div>'
        + GROW + tip("نبدأ دائماً بسؤال: ماذا يجب أن يقول الشعار؟ ثم نرسم.", "طريقتنا")
        + spacer(44) + bottom(arrow=DK)
    )
    return pg(body)


def s_idea():
    # the whole word on a milky card; the link inside it is marked with a label above, the two sides below
    W = 820
    k = W / (WS + 60)
    def x(u):   # word units -> px from the svg's left edge
        return (u + 30) * k
    h_left, h_right = 805, 1235           # centre lines of the two strokes beside the link
    link_c = x((h_left + h_right) / 2)
    lab = "font-size:32px;font-weight:700;white-space:nowrap;position:absolute;transform:translateX(-50%)"
    tick = f"position:absolute;width:4px;border-radius:2px;background:{DK};transform:translateX(-50%)"
    hw = 760 * k                          # rendered word height
    yb = 96 + hw                          # bottom of the word inside the box
    art = (f'<div style="position:relative;width:{W}px;margin:0 auto;padding:96px 0 110px">'
           f'<div style="{lab};left:{link_c:.0f}px;top:0;color:{TE}">الحل</div>'
           f'<div style="{tick};left:{link_c:.0f}px;top:52px;height:40px;background:{TE}"></div>'
           f'{word(W, DK, TE)}'
           f'<div style="{tick};left:{x(h_left):.0f}px;top:{yb + 6:.0f}px;height:40px"></div>'
           f'<div style="{tick};left:{x(h_right):.0f}px;top:{yb + 6:.0f}px;height:40px"></div>'
           f'<div style="{lab};left:{x(h_left) - 70:.0f}px;top:{yb + 52:.0f}px;color:{DK}">المشكلة</div>'
           f'<div style="{lab};left:{x(h_right) + 70:.0f}px;top:{yb + 52:.0f}px;color:{DK}">النتيجة</div></div>')
    body = (
        top("الفكرة", 3, N)
        + spacer(60)
        + '<h1 style="font-size:70px;line-height:1.3">الفكرة: جسر<br>داخل الاسم نفسه</h1>'
        + spacer(22)
        + '<p style="font-size:34px;font-weight:400;line-height:1.65;text-wrap:balance">عميلنا يأتي بمشكلة، ويريد نتيجة. عملنا هو ما بينهما.</p>'
        + spacer(44)
        + card(art, CARD_L, "40px 40px")
        + GROW + tip("لون التيراكوتا في الشعار كله لهذه الوصلة وحدها، فتلفت العين إليها.", "التفصيل")
        + spacer(44) + bottom(arrow=DK)
    )
    return pg(body)


def s_shape():
    def side(label, ok, sharp, note):
        mark = (f'<span style="font-size:28px;font-weight:800;padding:6px 18px;border-radius:20px;'
                f'background:{TE if ok else "rgba(242,233,216,.16)"};color:{DK if ok else CH}">{label}</span>')
        return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:22px">'
                f'<div style="display:flex;gap:18px;align-items:center">{mark}'
                f'<span style="font-size:31px;font-weight:400;color:rgba(242,233,216,.82)">{note}</span></div>'
                f'{word(660, CH, TE, sharp=sharp)}</div>')
    pair = (f'<div style="display:flex;flex-direction:column;gap:34px">'
            f'{side("أطراف حادة", False, True, "رسمية وباردة")}'
            f'<div style="height:2px;background:rgba(242,233,216,.18)"></div>'
            f'{side("أطراف مستديرة", True, False, "ودودة وواضحة")}</div>')
    body = (
        top("الشكل", 4, N)
        + spacer(60)
        + '<h1 style="font-size:70px;line-height:1.3">الحروف نفسها،<br>وإحساس مختلف</h1>'
        + spacer(22)
        + '<p style="font-size:34px;font-weight:400;line-height:1.65;text-wrap:balance">رسمنا كل حرف بخط واحد بسمك ثابت، ثم جرّبنا الأطراف:</p>'
        + spacer(44)
        + card(pair, CARD_D, "38px 44px")
        + GROW + tip("السُّمك الثابت يبقى واضحاً حتى حين يصغر الشعار على قلم أو ختم.", "لماذا")
        + spacer(44) + bottom(arrow=DK)
    )
    return pg(body)


COLORS = [(DK, CH, "فحمي", "القاعدة والكتابة"), (CH, DK, "حليبي", "الورق والمساحات"),
          (TE, DK, "تيراكوتا", "الوصلة، أي الحل"), (MU, DK, "مسطردي", "لمسة دافئة صغيرة"),
          (TL, CH, "أخضر مزرق", "لمسة هادئة تقابل الدفء"), (RO, DK, "وردي مغبر", "الأشكال المساعدة")]


def s_colors():
    rows = "".join(
        f'<div style="display:flex;align-items:center;gap:24px;padding:14px 26px;border-radius:30px;background:{CH}">'
        f'<span style="flex-shrink:0;width:76px;height:76px;border-radius:38px;background:{c};'
        f'{"border:3px solid rgba(32,33,38,.25);" if c in (CH, TE) else ""}"></span>'
        f'<div style="flex:1;display:flex;align-items:baseline;gap:18px;flex-wrap:wrap"><span style="font-size:40px;font-weight:800;color:{DK}">{name}</span>'
        f'<span style="font-size:31px;font-weight:400;color:rgba(32,33,38,.72)">{role}</span></div>'
        f'<span class="ltr" style="font-size:30px;font-weight:500;color:rgba(32,33,38,.6)">{c}</span></div>'
        for c, fg, name, role in COLORS)
    body = (
        top("الألوان", 5, N)
        + spacer(52)
        + '<h1 style="font-size:70px;line-height:1.3">ستة ألوان،<br>ولكل لون عمل</h1>'
        + spacer(36)
        + f'<div class="z" style="display:flex;flex-direction:column;gap:12px">{rows}</div>'
        + GROW
        + '<p style="font-size:32px;font-weight:500;line-height:1.6">ولكل خدمة لون في منشوراتنا: هذا الصف بلون الهوية البصرية.</p>'
        + spacer(44) + bottom(arrow=DK)
    )
    return pg(body)


def s_sizes():
    sizes = [(520, "لافتة أو غلاف", True), (320, "ورقة رسمية", True), (210, "ختم أو قلم", False)]
    rows = "".join(
        f'<div style="display:flex;align-items:center;justify-content:space-between;gap:30px;padding:24px 0;'
        f'{"border-top:2px solid rgba(242,233,216,.16);" if k else ""}">'
        f'<div style="font-size:32px;font-weight:600;color:{CH};white-space:nowrap">{lab}</div>{full(w, CH) if f else word(w, CH)}</div>'
        for k, (w, lab, f) in enumerate(sizes))
    body = (
        top("الاختبار", 6, N)
        + spacer(56)
        + '<h1 style="font-size:70px;line-height:1.3">اختبرناه كبيراً<br>وصغيراً</h1>'
        + spacer(22)
        + '<p style="font-size:34px;font-weight:400;line-height:1.65;text-wrap:balance">'
          'الخط <span class="ltr">Alexandria</span> للعربية والإنجليزية معاً، وفي المقاس الصغير جداً تكفي كلمة <span class="ltr">SHWANI</span> وحدها:</p>'
        + spacer(36)
        + card(rows, CARD_D, "20px 52px")
        + GROW + tip("الشعار يظهر كاملاً دائماً، لا تقطعه حافة ولا يُختصر إلى حرف.", "القاعدة")
        + spacer(44) + bottom(arrow=DK)
    )
    return pg(body)


def closing():
    body = (
        top("الحلقة القادمة", N, N)
        + deco(f"left:-110px;top:120px;width:270px;height:270px;border-radius:135px;background:{RO}")
        + deco(f"left:170px;top:300px;width:80px;height:80px;border-radius:40px;background:{CH}")
        + spacer(100)
        + '<h1 style="font-size:76px;line-height:1.35">تريد هوية<br>تحكي مشروعك؟</h1>'
        + spacer(24)
        + '<p style="font-size:36px;line-height:1.6">نبدأ معك بالسؤال نفسه: ماذا يجب أن يقول شعارك؟</p>'
        + GROW
        + f'<div class="z" style="background:{DK};color:{CH};border-radius:36px;padding:38px 44px">'
          f'<div style="font-size:30px;font-weight:700;margin-bottom:10px;color:{TE}">الحلقة 2</div>'
          '<div style="font-size:48px;font-weight:800;line-height:1.4">الهوية على أرض الواقع</div></div>'
        + spacer(34)
        + '<p style="font-size:32px;font-weight:600;line-height:1.6">احفظ المنشور، وأرسله لصاحب مشروع جديد.</p>'
        + spacer(44)
        + bottom(right_html=mono(250))
    )
    return pg(body)


SLIDES = [cover(), s_goals(), s_idea(), s_shape(), s_colors(), s_sizes(), closing()]

CHECK_JS = """() => { const S = document.querySelector('.s').getBoundingClientRect(), out = [];
  document.querySelectorAll('svg.wm').forEach((e, i) => { const r = e.getBoundingClientRect();
    const d = [r.left - S.left, S.right - r.right, r.top - S.top, S.bottom - r.bottom];
    if (Math.min(...d) < 40) out.push('logo ' + i + ' margins px (L,R,T,B) ' + d.map(v => v.toFixed(0)).join(', ')); });
  return out; }"""


async def check_marks():
    """Marwa, 19 Oct: no logo cut or crowding the edge. Every SHWANI stays 40 px inside the slide."""
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
    bad = asyncio.run(check_marks())
    if bad:
        print("MEASUREMENT CHECK FAILED:", *bad, sep="\n  ")
        sys.exit(1)
    print("measurement check: every logo inside the slide")
