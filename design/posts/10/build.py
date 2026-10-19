"""Post 10: carousel «أعمالنا» الحلقة 1 — كيف صمّمنا شعار SHWANI. 7 slides.

Row 4: terracotta base (#E07A47). Marwa's decisions:
- 19 Oct: text on the orange background went white; 20 Oct: back to charcoal (#202126), as in the
  first draft, keeping the phone sizes.
- 19 Oct: no price is mentioned in any post (the closing slide's price line was removed).
- 20 Oct: Alexandria only (common.require_font stops the build if it is missing), text sized for phone
  screens (base rule: headlines >= 84px, body >= 44px, nothing below 36px; check_marks() enforces the
  36px floor). Teal (#2F6F6D) joins the identity colours, so slide 5 shows six. The teal background
  capsules were removed the same night: too crowded.
- the identity is the word SHWANI only: no SH monogram, no lone H, no H pattern.
- no logo or word is cut at the slide edge; check_marks() fails the build if one is.
The terracotta link would vanish on a terracotta ground, so the logo always sits on a charcoal or milky card.
"""
import os, sys, asyncio
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from common import *  # noqa: F401,F403
from rounded import shwani, lockup  # noqa: E402

WH = "#FFFFFF"
ROW_BG = TE
INK = DK                       # text on terracotta: charcoal again (Marwa, 20 Oct)
SUB = DK                       # secondary text on terracotta
CARD_D = DK                    # charcoal card, milky text
CARD_L = CH                    # milky card, charcoal text
N = 7
SERIES = "أعمالنا · الحلقة 1"
WS = shwani(DK, TE).width()    # 4205 units at cap height 700

# phone-readable sizes (Marwa, 20 Oct: base rule for every post)
H1, BODY, SMALL = 88, 44, 36


def caps(*specs):
    """Teal capsules in the background. Each spec: (css position, width, height, degrees)."""
    return "".join(
        f'<div class="deco tl" style="{pos};width:{w}px;height:{h}px;border-radius:{h // 2}px;background:{TL};transform:rotate({r}deg)"></div>'
        for pos, w, h, r in specs)


def pg(body, teal=()):
    return page(caps(*teal) + body, bg=ROW_BG, fg=INK)


def h1(text, size=H1):
    return f'<h1 style="font-size:{size}px;line-height:1.22">{text}</h1>'


def lead(text, size=BODY, weight=500, color=SUB):
    return f'<p style="font-size:{size}px;font-weight:{weight};line-height:1.45;color:{color};text-wrap:balance">{text}</p>'


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


def num(k, size=76, bg=DK, fg=CH):
    return (f'<span class="ltr" style="flex-shrink:0;width:{size}px;height:{size}px;border-radius:{size // 2}px;background:{bg};color:{fg};'
            f'display:flex;align-items:center;justify-content:center;font-size:{int(size * .5)}px;font-weight:800">{k}</span>')


def tip(text, label):
    return (f'<div class="z" style="border:4px solid {DK};border-radius:34px;padding:26px 32px;display:flex;gap:24px;align-items:center">'
            f'<span style="flex-shrink:0;font-size:{SMALL}px;font-weight:800;background:{DK};color:{CH};border-radius:26px;padding:8px 22px">{label}</span>'
            f'<span style="flex:1;font-size:40px;font-weight:600;line-height:1.4;text-wrap:balance">{text}</span></div>')


# ---------- slides ----------

def cover():
    big = card(f'<div style="display:flex;justify-content:center">{full(640, CH)}</div>', CARD_D, "88px 60px 80px",
               "box-shadow:0 26px 60px rgba(32,33,38,.28)")
    body = (
        top(SERIES, 1, N)
        + deco(f"right:-90px;top:130px;width:300px;height:300px;border-radius:150px;background:{RO}")
        + deco(f"left:96px;top:176px;width:96px;height:96px;border-radius:48px;background:{CH}")
        + spacer(250)
        + big
        + GROW
        + h1('كيف صمّمنا<br>شعار <span class="ltr">SHWANI</span>؟', 100)
        + spacer(22)
        + lead("قصة هويتنا، من الفكرة إلى الشعار.")
        + spacer(56) + bottom(arrow=DK)
    )
    return pg(body)


GOALS = [("يُقرأ بسهولة", "من بعيد ومن قريب."),
         ("بسيط", "يكفيه لون واحد."),
         ("له معنى", "يحكي ما نفعله.")]


def s_goals():
    rows = "".join(
        f'<div style="display:flex;align-items:center;gap:28px;padding:20px 0;{"border-top:3px solid rgba(32,33,38,.2);" if k else ""}">'
        f'{num(k + 1)}<div style="flex:1"><div style="font-size:52px;font-weight:800;line-height:1.25">{a}</div>'
        f'<div style="font-size:{BODY}px;font-weight:500;color:{SUB};line-height:1.35">{b}</div></div></div>'
        for k, (a, b) in enumerate(GOALS))
    body = (
        top("قبل الرسم", 2, N)
        + spacer(40)
        + h1("قبل أن نرسم،<br>كتبنا ماذا نريد")
        + spacer(14)
        + lead("ثلاثة شروط، كما مع كل عميل:")
        + spacer(14)
        + f'<div class="z">{rows}</div>'
        + GROW + tip("نسأل أولاً: ماذا يقول الشعار؟ ثم نرسم.", "طريقتنا")
        + spacer(34) + bottom(arrow=DK)
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
    lab = f"font-size:40px;font-weight:800;white-space:nowrap;position:absolute;transform:translateX(-50%)"
    tick = f"position:absolute;width:5px;border-radius:3px;background:{DK};transform:translateX(-50%)"
    hw = 760 * k                          # rendered word height
    yb = 104 + hw                         # bottom of the word inside the box
    art = (f'<div style="position:relative;width:{W}px;margin:0 auto;padding:104px 0 118px">'
           f'<div style="{lab};left:{link_c:.0f}px;top:0;color:{TE}">الحل</div>'
           f'<div style="{tick};left:{link_c:.0f}px;top:58px;height:40px;background:{TE}"></div>'
           f'{word(W, DK, TE)}'
           f'<div style="{tick};left:{x(h_left):.0f}px;top:{yb + 6:.0f}px;height:40px"></div>'
           f'<div style="{tick};left:{x(h_right):.0f}px;top:{yb + 6:.0f}px;height:40px"></div>'
           f'<div style="{lab};left:{x(h_left) - 80:.0f}px;top:{yb + 52:.0f}px;color:{DK}">المشكلة</div>'
           f'<div style="{lab};left:{x(h_right) + 80:.0f}px;top:{yb + 52:.0f}px;color:{DK}">النتيجة</div></div>')
    body = (
        top("الفكرة", 3, N)
        + spacer(40)
        + h1("الفكرة: جسر<br>داخل الاسم")
        + spacer(14)
        + lead("العميل يأتي بمشكلة ويريد نتيجة، وعملنا ما بينهما.")
        + spacer(30)
        + card(art, CARD_L, "36px 40px")
        + GROW + tip("التيراكوتا في الشعار للوصلة وحدها، لتلفت العين.", "التفصيل")
        + spacer(34) + bottom(arrow=DK)
    )
    return pg(body)


def s_shape():
    def side(label, ok, sharp, note):
        mark = (f'<span style="font-size:{SMALL}px;font-weight:800;padding:6px 20px;border-radius:24px;'
                f'background:{TE if ok else "rgba(242,233,216,.18)"};color:{DK if ok else CH}">{label}</span>')
        return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:18px">'
                f'<div style="display:flex;gap:18px;align-items:center">{mark}'
                f'<span style="font-size:38px;font-weight:500;color:{CH}">{note}</span></div>'
                f'{word(640, CH, TE, sharp=sharp)}</div>')
    pair = (f'<div style="display:flex;flex-direction:column;gap:28px">'
            f'{side("أطراف حادة", False, True, "رسمية وباردة")}'
            f'<div style="height:3px;background:rgba(242,233,216,.2)"></div>'
            f'{side("أطراف مستديرة", True, False, "ودودة وواضحة")}</div>')
    body = (
        top("الشكل", 4, N)
        + spacer(40)
        + h1("الحروف نفسها،<br>وإحساس مختلف")
        + spacer(14)
        + lead("خط واحد بسُمك ثابت، ثم جرّبنا الأطراف:")
        + spacer(30)
        + card(pair, CARD_D, "34px 44px")
        + GROW + tip("السُّمك الثابت يبقى واضحاً حتى على قلم.", "لماذا")
        + spacer(34) + bottom(arrow=DK)
    )
    return pg(body)


COLORS = [(DK, CH, "فحمي", "القاعدة والكتابة"), (CH, DK, "حليبي", "الورق والمساحات"),
          (TE, DK, "تيراكوتا", "الوصلة، أي الحل"), (TL, CH, "أخضر مزرق", "لمسة هادئة"),
          (MU, DK, "مسطردي", "لمسة دافئة"), (RO, DK, "وردي مغبر", "الأشكال المساعدة")]


def s_colors():
    tiles = "".join(
        f'<div style="background:{CH};border-radius:32px;padding:22px 24px 24px;display:flex;flex-direction:column;gap:8px">'
        f'<div class="ltr" style="height:74px;border-radius:37px;background:{c};color:{fg};display:flex;align-items:center;'
        f'justify-content:center;font-size:{SMALL}px;font-weight:700;letter-spacing:1px;'
        f'{"box-shadow:inset 0 0 0 3px rgba(32,33,38,.25);" if c == CH else ""}">{c}</div>'
        f'<div style="font-size:46px;font-weight:800;color:{DK};line-height:1.25;margin-top:6px">{name}</div>'
        f'<div style="font-size:{SMALL}px;font-weight:500;color:{DK};line-height:1.3">{role}</div></div>'
        for c, fg, name, role in COLORS)
    body = (
        top("الألوان", 5, N)
        + spacer(36)
        + h1("ستة ألوان،<br>ولكل لون عمل", 84)
        + spacer(28)
        + f'<div class="z" style="display:grid;grid-template-columns:1fr 1fr;gap:18px">{tiles}</div>'
        + GROW + bottom(arrow=DK)
    )
    return pg(body)


def s_sizes():
    sizes = [(500, "لافتة", True), (320, "ورقة رسمية", True), (230, "ختم أو قلم", False)]
    rows = "".join(
        f'<div style="display:flex;align-items:center;justify-content:space-between;gap:30px;padding:20px 0;'
        f'{"border-top:3px solid rgba(242,233,216,.18);" if k else ""}">'
        f'<div style="font-size:42px;font-weight:700;color:{CH};white-space:nowrap">{lab}</div>{full(w, CH) if f else word(w, CH)}</div>'
        for k, (w, lab, f) in enumerate(sizes))
    body = (
        top("الاختبار", 6, N)
        + spacer(40)
        + h1("اختبرناه كبيراً<br>وصغيراً")
        + spacer(14)
        + lead('وفي المقاس الصغير جداً تكفي كلمة <span class="ltr">SHWANI</span>:')
        + spacer(30)
        + card(rows, CARD_D, "16px 50px")
        + GROW + tip("الشعار يظهر كاملاً دائماً، لا تقطعه حافة.", "القاعدة")
        + spacer(34) + bottom(arrow=DK)
    )
    return pg(body)


def closing():
    body = (
        top("الحلقة القادمة", N, N)
        + deco(f"left:-110px;top:150px;width:270px;height:270px;border-radius:135px;background:{RO}")
        + spacer(110)
        + h1("تريد هوية<br>تحكي مشروعك؟", 92)
        + spacer(22)
        + lead("نبدأ معك بالسؤال نفسه: ماذا يجب أن يقول شعارك؟")
        + GROW
        + f'<div class="z" style="background:{DK};color:{CH};border-radius:36px;padding:34px 44px">'
          f'<div style="font-size:{SMALL}px;font-weight:800;margin-bottom:8px;color:{TE}">الحلقة 2</div>'
          '<div style="font-size:56px;font-weight:800;line-height:1.3">الهوية على أرض الواقع</div></div>'
        + spacer(30)
        + lead("احفظ المنشور، وأرسله لصاحب مشروع جديد.", 42, 700, DK)
        + spacer(36)
        + bottom(right_html=mono(260))
    )
    return pg(body)


SLIDES = [cover(), s_goals(), s_idea(), s_shape(), s_colors(), s_sizes(), closing()]

CHECK_JS = """() => { const S = document.querySelector('.s').getBoundingClientRect(), out = [];
  // 1. no logo cut or crowding the edge
  document.querySelectorAll('svg.wm').forEach((e, i) => { const r = e.getBoundingClientRect();
    const d = [r.left - S.left, S.right - r.right, r.top - S.top, S.bottom - r.bottom];
    if (Math.min(...d) < 40) out.push('logo ' + i + ' margins px (L,R,T,B) ' + d.map(v => v.toFixed(0)).join(', ')); });
  // 2. phone-readable text: nothing under 36 px
  const texts = [], w = document.createTreeWalker(document.querySelector('.s'), NodeFilter.SHOW_TEXT);
  while (w.nextNode()) { const n = w.currentNode; if (!n.textContent.trim() || n.parentElement.closest('svg')) continue;
    const fs = parseFloat(getComputedStyle(n.parentElement).fontSize);
    if (fs < 36) out.push('text under 36px (' + fs + 'px): ' + n.textContent.trim().slice(0, 30));
    const rg = document.createRange(); rg.selectNodeContents(n); for (const r of rg.getClientRects()) texts.push([r, n.textContent.trim().slice(0, 20)]); }
  // 3. teal capsules never behind text, a logo or a card (4 px clearance)
  const blocks = [...document.querySelectorAll('svg.wm, .s > .z, .top > *, .bot > *')].map(e => [e.getBoundingClientRect(), e.tagName + '.' + (e.className.baseVal ?? e.className)]);
  const hit = (a, b) => a.left < b.right + 4 && b.left < a.right + 4 && a.top < b.bottom + 4 && b.top < a.bottom + 4;
  document.querySelectorAll('.deco.tl').forEach((c, i) => { const r = c.getBoundingClientRect();
    for (const [t, s] of texts.concat(blocks)) if (hit(r, t)) { out.push('teal capsule ' + i + ' overlaps ' + s); break; } });
  return out; }"""


async def check_marks():
    """Marwa, 19-20 Oct: no logo cut at the edge, nothing under 36 px, no teal capsule behind content."""
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
        print("CHECK FAILED:", *bad, sep="\n  ")
        sys.exit(1)
    print("checks: logos inside, text >= 36px, teal capsules clear of content")
