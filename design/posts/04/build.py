"""Post 04: carousel «قبل أن تصمّم» الحلقة 1 — خمسة أخطاء تُضعف شعار مشروعك. 7 slides."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from common import *  # noqa: F401,F403

N = 7
SERIES = "قبل أن تصمّم · الحلقة 1"


# ---------- small building blocks ----------
def verdict(ok, text):
    if ok:
        icon = (f'<svg aria-hidden="true" width="40" height="40" viewBox="0 0 40 40"><circle cx="20" cy="20" r="20" fill="{MU}"/>'
                f'<path d="M12 20.5l5.5 5.5L28.5 14" fill="none" stroke="{DK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>')
        word = "صح"
    else:
        icon = (f'<svg aria-hidden="true" width="40" height="40" viewBox="0 0 40 40"><circle cx="20" cy="20" r="20" fill="{RO}"/>'
                f'<path d="M14 14l12 12M26 14L14 26" fill="none" stroke="{DK}" stroke-width="4" stroke-linecap="round"/></svg>')
        word = "خطأ"
    return (f'<div style="display:flex;align-items:center;gap:14px;margin-top:18px">{icon}'
            f'<span style="font-size:26px;font-weight:800">{word}:</span>'
            f'<span style="font-size:26px;font-weight:400">{text}</span></div>')


def pair(a_html, b_html, a_text, b_text, a_bg=CH, b_bg=CH, h=430):
    def card(html, bg):
        edge = 'border:2px solid rgba(32,33,38,.18);' if bg == CH else ''
        return (f'<div style="height:{h}px;border-radius:32px;background:{bg};{edge}display:flex;align-items:center;'
                f'justify-content:center;overflow:hidden;position:relative">{html}</div>')
    # RTL: first child sits on the right. The mistake goes first (right), the fix second (left).
    return (f'<div class="z" style="display:flex;gap:24px">'
            f'<div style="flex:1;min-width:0">{card(a_html, a_bg)}{verdict(False, a_text)}</div>'
            f'<div style="flex:1;min-width:0">{card(b_html, b_bg)}{verdict(True, b_text)}</div></div>')


def solution(text):
    return (f'<div class="z" style="border:3px solid {TE};border-radius:32px;padding:26px 34px;display:flex;gap:22px;align-items:center">'
            f'<span style="flex-shrink:0;font-size:26px;font-weight:800;background:{TE};color:{DK};border-radius:24px;padding:6px 20px">الحل</span>'
            f'<span style="flex:1;font-size:29px;font-weight:400;line-height:1.6;text-wrap:balance">{text}</span></div>')


def mistake_slide(i, title, text, illus, fix):
    body = (
        top(f"الخطأ {i}", i + 1, N)
        + spacer(52)
        + illus
        + spacer(54)
        + f'<h1 style="font-size:62px">{title}</h1>'
        + spacer(16)
        + f'<p style="font-size:31px;font-weight:400;line-height:1.7;text-wrap:balance">{text}</p>'
        + GROW
        + solution(fix)
        + spacer(44)
        + bottom(arrow=TE)
    )
    return page(body, light=True)


# ---------- illustrations ----------
def busy_emblem(size, color=DK):
    rays = "".join(
        f'<line x1="{100+62*math.cos(a):.1f}" y1="{100+62*math.sin(a):.1f}" x2="{100+70*math.cos(a):.1f}" y2="{100+70*math.sin(a):.1f}"/>'
        for a in (k * math.pi / 18 for k in range(36)))
    star = " ".join(f"{100+(34 if k % 2 == 0 else 15)*math.cos(-math.pi/2 + k*math.pi/6):.1f},"
                    f"{100+(34 if k % 2 == 0 else 15)*math.sin(-math.pi/2 + k*math.pi/6):.1f}" for k in range(12))
    leaves = "".join(
        f'<ellipse cx="{100+48*math.cos(a):.1f}" cy="{100+48*math.sin(a):.1f}" rx="7" ry="3" '
        f'transform="rotate({math.degrees(a)+90:.0f} {100+48*math.cos(a):.1f} {100+48*math.sin(a):.1f})"/>'
        for a in (k * math.pi / 8 for k in range(16)))
    return (f'<svg aria-hidden="true" viewBox="0 0 200 200" width="{size}" height="{size}" style="display:block">'
            f'<defs><path id="arc" d="M100,100 m-82,0 a82,82 0 1,1 164,0 a82,82 0 1,1 -164,0"/></defs>'
            f'<g fill="none" stroke="{color}"><circle cx="100" cy="100" r="96" stroke-width="3"/><circle cx="100" cy="100" r="90" stroke-width="1"/>'
            f'<circle cx="100" cy="100" r="74" stroke-width="1"/><circle cx="100" cy="100" r="58" stroke-width="1.5"/>'
            f'<g stroke-width="1">{rays}</g><circle cx="100" cy="100" r="40" stroke-width="1"/></g>'
            f'<g fill="{color}">{leaves}<polygon points="{star}"/></g>'
            f'<text font-family="Alexandria" font-size="10.5" font-weight="500" fill="{color}" letter-spacing="1.5">'
            f'<textPath href="#arc">• QUALITY • SINCE 2026 • BEST SERVICE • TRUSTED BRAND • PREMIUM</textPath></text></svg>')


def simple_mark(size):
    return mark_inline(size, DK, TE)


def sizes_row(make):
    # the same logo, big and at profile-photo sizes
    return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:26px">{make(150)}'
            f'<div style="display:flex;align-items:center;gap:22px">'
            f'<span style="width:64px;height:64px;border-radius:32px;border:2px solid rgba(32,33,38,.25);display:flex;align-items:center;justify-content:center">{make(40)}</span>'
            f'<span style="width:36px;height:36px;border-radius:18px;border:2px solid rgba(32,33,38,.25);display:flex;align-items:center;justify-content:center">{make(22)}</span>'
            f'</div></div>')


def illus1():
    return pair(sizes_row(busy_emblem), sizes_row(lambda s: simple_mark(s * 0.62)),
                "تختفي حين يصغر", "واضح بأي حجم")


def dots(colors, label):
    d = "".join(f'<span style="width:62px;height:62px;border-radius:31px;background:{c}"></span>' for c in colors)
    return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:26px">'
            f'<div style="display:flex;flex-wrap:wrap;justify-content:center;gap:16px;max-width:330px">{d}</div>'
            f'<span style="font-size:30px;font-weight:800;color:{DK}">{label}</span></div>')


def illus2():
    many = ["#E63946", "#F4A261", "#2A9D8F", "#9B5DE5", "#00BBF9", "#F15BB5", "#FEE440", "#06D6A0"]
    few = [DK, TE, MU]
    return pair(dots(many, "8 ألوان"), dots(few, "3 ألوان"), "تشتّت ويُنسى", "يُتذكّر بسرعة")


def sign(weight, blur):
    return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:22px">'
            f'<div style="background:{DK};border-radius:22px;padding:30px 40px;filter:blur({blur}px)">'
            f'<span style="font-family:Alexandria;font-weight:{weight};font-size:58px;color:{CH};letter-spacing:{4 if weight < 300 else 0}px">مخبز الورد</span></div>'
            f'<span style="font-size:24px;font-weight:500;color:{DK};opacity:.7">لافتة من بعيد</span></div>')


def illus3():
    return pair(sign(100, 2.2), sign(800, 2.2), "يضيع من بعيد", "يُقرأ من بعيد")


def trend_row(label, shape, fades):
    cells = "".join(f'<span style="opacity:{o};display:flex;flex-direction:column;align-items:center;gap:10px">{shape}'
                    f'<span style="font-size:22px;font-weight:600;color:{DK};opacity:1" class="ltr">{y}</span></span>'
                    for y, o in zip(("2026", "2028", "2031"), fades))
    return (f'<div style="display:flex;align-items:center;gap:30px;width:100%">'
            f'<span style="width:150px;font-size:28px;font-weight:800;color:{DK}">{label}</span>'
            f'<div style="flex:1;display:flex;justify-content:space-around;direction:ltr">{cells}</div></div>')


def illus4():
    trendy = ('<span style="width:96px;height:96px;border-radius:48px;display:block;'
              'background:radial-gradient(circle at 30% 28%,#ffffff 0 9%,transparent 10%),linear-gradient(135deg,#9B5DE5,#00BBF9 55%,#F15BB5);'
              'box-shadow:0 10px 24px rgba(155,93,229,.55)"></span>')
    idea = (f'<span style="width:96px;height:96px;border-radius:28px;display:flex;align-items:center;justify-content:center;background:{DK}">'
            f'<span style="width:58px;height:18px;border-radius:9px;background:{TE}"></span></span>')
    card = (f'<div style="height:450px;border-radius:32px;background:{CH};border:2px solid rgba(32,33,38,.18);padding:30px 40px;display:flex;flex-direction:column;justify-content:space-around">'
            + trend_row("موضة العام", trendy, (1, .45, .15))
            + f'<div style="height:2px;background:rgba(32,33,38,.15)"></div>'
            + trend_row("فكرة واضحة", idea, (1, 1, 1))
            + '</div>')
    return (f'<div class="z">{card}<div style="display:flex;gap:36px">'
            f'{verdict(False, "يبهت بعد سنتين")}{verdict(True, "يبقى سنوات")}</div></div>')


def tile(bg, html, border=None):
    b = f"border:2px solid {border};" if border else ""
    return (f'<div style="background:{bg};{b}border-radius:22px;display:flex;align-items:center;justify-content:center">{html}</div>')


def illus5():
    lost = (f'<div style="width:100%;height:100%;background:{DK};display:flex;align-items:center;justify-content:center">'
            f'{mark_inline(150, "#2C2D33", "#34353B")}</div>')
    tiny = (f'<span style="width:64px;height:64px;border-radius:32px;background:{DK};display:flex;align-items:center;justify-content:center">'
            f'{mark_inline(26, CH, TE)}</span>')
    grid = (f'<div style="width:100%;height:100%;padding:22px;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:16px;background:{CH}">'
            + tile(CH, mark_inline(64, DK, TE), border="rgba(32,33,38,.2)")
            + tile(DK, mark_inline(64, CH, TE))
            + tile(TE, mark_inline(64, DK, DK))
            + tile(CH, tiny, border="rgba(32,33,38,.2)")
            + '</div>')
    return pair(lost, grid, "يختفي على الداكن", "نسخة لكل خلفية", a_bg=DK, b_bg=CH)


# ---------- slides ----------
def cover():
    body = (
        top(SERIES, 1, N)
        + spacer(70)
        + '<div class="z" style="position:relative;height:470px;display:flex;align-items:center">'
        + f'<div aria-hidden="true" style="position:absolute;right:40px;top:170px;width:420px;height:150px;border-radius:75px;background:{TE}"></div>'
        + f'<div aria-hidden="true" style="position:absolute;right:480px;top:130px;width:90px;height:90px;border-radius:45px;background:{RO}"></div>'
        + f'<div class="ltr" style="position:relative;font-weight:800;font-size:420px;line-height:1;color:{DK};margin-right:110px">5</div></div>'
        + GROW
        + '<h1 style="font-size:104px;line-height:1.2">أخطاء تُضعف<br>شعار مشروعك</h1>'
        + spacer(28)
        + '<p style="font-size:34px;line-height:1.7">احفظ المنشور قبل أن تطلب شعارك القادم.</p>'
        + spacer(90)
        + bottom(arrow=TE)
    )
    return page(body, light=True)


def closing():
    body = (
        top("الحلقة القادمة", N, N)
        + deco(f"left:-130px;top:330px;width:330px;height:330px;border-radius:165px;background:{RO}")
        + spacer(110)
        + '<h1 style="font-size:76px;line-height:1.35">أيّ خطأ منها<br>رأيته اليوم؟</h1>'
        + spacer(24)
        + '<p style="font-size:34px;line-height:1.7">اكتب رقمه في التعليقات.</p>'
        + GROW
        + f'<div class="z" style="background:{MU};color:{DK};border-radius:36px;padding:38px 44px">'
          '<div style="font-size:27px;font-weight:600;margin-bottom:10px">الحلقة 2</div>'
          '<div style="font-size:46px;font-weight:800;line-height:1.4">كيف تختار ألوان مشروعك</div></div>'
        + spacer(36)
        + '<p style="font-size:30px;font-weight:500;line-height:1.6">احفظ المنشور، وأرسله لصاحب مشروع جديد.</p>'
        + spacer(48)
        + bottom(right_html=lockup_svg(250, DK))     # full SHWANI logo, not SH alone (Marwa, 15 Oct)
    )
    return page(body, light=True)


SLIDES = [
    cover(),
    mistake_slide(1, "تفاصيل كثيرة",
                  "يظهر الشعار صغيراً أكثر مما يظهر كبيراً: في صورة الحساب، وعلى الختم، وفي زاوية الفيديو. هناك تختفي التفاصيل.",
                  illus1(), "جرّب شعارك بحجم صورة الحساب. إن لم يُقرأ صغيراً، فبسّطه."),
    mistake_slide(2, "ألوان كثيرة",
                  "كل لون إضافي يشتّت العين، ويرفع كلفة الطباعة، ويصعّب تذكّر الشعار.",
                  illus2(), "لون أساسي، ولون مساعد، ولون للتمييز. والباقي درجات منها."),
    mistake_slide(3, "خط لا يُقرأ",
                  "الخط الرفيع جداً أو المزخرف يبدو جميلاً على الشاشة، ويضيع على اللافتة وفي الصورة الصغيرة.",
                  illus3(), "اختر خطاً واضحاً، وجرّبه على لافتة من بعيد."),
    mistake_slide(4, "اتّباع الترند",
                  "الشعار الذي يقلّد موضة هذا العام يبدو قديماً بعد سنتين، وتغييره يعني تغيير كل ما طُبع عليه.",
                  illus4(), "اسأل: هل سيمثّل هذا الشعار مشروعي بعد خمس سنوات؟"),
    mistake_slide(5, "شعار بنسخة واحدة",
                  "نسخة واحدة لا تعمل في كل مكان: تختفي على الخلفية الداكنة، ولا تصلح للطباعة بلون واحد على الختم والأكياس.",
                  illus5(), "اطلب نسخة للخلفية الفاتحة، وأخرى للداكنة، وثالثة بلون واحد، ورمزاً مختصراً."),
    closing(),
]

if __name__ == "__main__":
    render(HERE, SLIDES)
