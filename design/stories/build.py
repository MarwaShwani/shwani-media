"""Daily interactive stories for Instagram and Facebook (Marwa, 28 Oct 2026). 1080x1920.

Five stories a day at the peak hours (10:00, 12:30, 15:30, 18:00, 21:05, Baghdad time), kept as highlights.
Every designed story comes in two copies:
  *-ig.png   Instagram. The middle is left empty for the sticker Marwa adds by hand (poll, quiz, slider,
             question, Add Yours). Meta's API cannot publish stickers, so Metricool sends it to her phone
             as a notification at the slot time.
  *-fb.png   Facebook, published automatically by Metricool. The options are printed and the viewer
             replies with a number in Messenger. A quiz gets a second card with the answer (*-fb-answer.png),
             published one minute later, so the next tap shows it.
  *-auto.png An old post from the archive, automatic on both networks.
A new feed post is reshared on Instagram by hand from the post itself (it stays tappable);
Facebook gets an automatic card (*-fb.png of kind "reshare").

Sizes as in the reels: question 76, text 40 to 44, nothing under 34. Content between y=250 and y=1670,
because Instagram covers the top with the profile bar and the bottom with the reply box.
The logo is SHWANI in full, never a monogram, and stays 40 px inside the edges. No price, ever.

Run:  python3 stories/build.py stories/week-01.json
Out:  stories/out/week-01/  (PNGs, previews, manifest.json, contact sheets)
"""
import os, sys, json, asyncio
HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
REPO = os.path.dirname(DESIGN)
sys.path.insert(0, DESIGN)
from common import fontlinks, require_font, FONT_OK_JS, HANDLE, SL, TL, SG, RO  # noqa: E402
from rounded import lockup, CH, MU, DK, TE  # noqa: E402
from PIL import Image  # noqa: E402

W, H = 1080, 1920
TOP, BOT = 250, 1670
SLOTS = ["10:00", "12:30", "15:30", "18:00", "21:05"]
FORBIDDEN = ["دينار", "سعر", "أسعار", "Canva", "قوالب جاهزة", "تابعونا"]

# invented jewellery shop «ياقوت» (post 9 palette)
DEEP, RED, RED_M, GREY, INK = "#0E2931", "#861211", "#B5413D", "#E2E2E0", "#F4F4F2"


def rgba(hex_, a):
    h = hex_.lstrip("#")
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{a})"


def style(bg, fg, acc, b_bg, b_fg, logo, chip, deco):
    return dict(bg=bg, fg=fg, acc=acc, b_bg=b_bg, b_fg=b_fg, logo=logo, chip=chip, deco=deco,
                card=rgba(fg, .07), edge=rgba(fg, .18), dim=rgba(fg, .8))


# text is charcoal on terracotta, rose, sage and mustard; milky on teal, slate and charcoal; no mustard on teal
STY = {
    "poll":    style(DK, CH, TE, TE, DK, (CH, TE, CH), "رأيك يهمّنا", (TE, MU, RO)),
    "tot":     style(CH, DK, TE, TE, DK, (DK, TE, DK), "أيّهما أفضل؟", (TE, MU, TL)),
    "quiz":    style(TL, CH, RO, RO, DK, (CH, TE, CH), "اختبر نفسك", (RO, SG, TE)),
    "future":  style(TE, DK, DK, DK, CH, (DK, DK, DK), "خدمة قادمة؟", (DK, CH, MU)),
    "evening": style(DK, CH, MU, MU, DK, (CH, TE, CH), "سؤال الليلة", (MU, TE, SL)),
    "archive": style(CH, DK, TE, TE, DK, (DK, TE, DK), "من أرشيفنا", (TE, MU, RO)),
    "reshare": style(DK, CH, TE, TE, DK, (CH, TE, CH), "جديد الليلة", (TE, MU, RO)),
}

ICON = {
    "send": '<path d="M21 3L10 14"/><path d="M21 3l-7 18-4-7-7-4z"/>',
    "chat": '<path d="M4 5.5h16v10H9l-5 4z"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "chart": '<path d="M4 20V4"/><path d="M4 20h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>',
    "star": '<path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8-5.2-2.8-5.2 2.8 1-5.8-4.3-4.1 5.9-.8z"/>',
    "pen": '<path d="M14.5 5.5l4 4L9 19H5v-4z"/><path d="M12.5 7.5l4 4"/><path d="M4 21h16"/>',
    "card": '<rect x="5" y="3" width="14" height="18" rx="2.5"/><circle cx="12" cy="10" r="2.6"/><path d="M8.5 17c.6-2 1.9-3 3.5-3s2.9 1 3.5 3"/>',
    "cap": '<path d="M2.5 9.5L12 5l9.5 4.5L12 14z"/><path d="M6.5 11.5V16c1.6 1.6 3.4 2.3 5.5 2.3s3.9-.7 5.5-2.3v-4.5"/><path d="M21.5 9.5v5"/>',
    "question": '<circle cx="12" cy="12" r="9"/><path d="M9.4 9.3a2.7 2.7 0 0 1 5.2 1c0 1.8-2.6 2.3-2.6 4.1"/><path d="M12 17.6h.01"/>',
}


def icon(name, size, color, sw=2.0):
    return (f'<svg aria-hidden="true" viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;display:block">{ICON[name]}</svg>')


def logo(width, colors):
    svg = lockup(*colors)
    return (svg.replace('<svg ', f'<svg class="wm" style="width:{width}px;height:auto;display:block;flex-shrink:0" ', 1)
               .replace(' width="', ' data-w="', 1).replace(' height="1180"', '', 1))


def spacer(h):
    return f'<div style="height:{h}px;flex-shrink:0"></div>'


GROW = '<div style="flex-grow:1"></div>'

CSS = """*{box-sizing:border-box}
html,body{margin:0}
.s{width:1080px;height:1920px;padding:260px 72px 250px;font-family:'Alexandria',sans-serif;position:relative;overflow:hidden;
   display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;align-items:center}
.chip{padding:12px 34px;border-radius:50px;border:3px solid currentColor;font-size:34px;font-weight:600;white-space:nowrap}
h1{margin:0;font-size:76px;font-weight:800;line-height:1.32;text-wrap:balance}
h2{margin:0;font-size:52px;font-weight:800;line-height:1.35;text-wrap:balance}
.sub{margin:0;font-size:40px;font-weight:500;line-height:1.5;text-wrap:pretty}
.z{position:relative;z-index:2}
.deco{position:absolute;z-index:1}
.ltr{direction:ltr;unicode-bidi:isolate}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px}
"""


def page(body, s):
    d1, d2, d3 = s["deco"]
    deco = (f'<div class="deco" style="right:72px;top:168px;width:230px;height:44px;border-radius:22px;background:{d1}"></div>'
            f'<div class="deco" style="right:322px;top:168px;width:44px;height:44px;border-radius:22px;background:{d2}"></div>'
            f'<div class="deco" style="left:72px;bottom:128px;width:300px;height:44px;border-radius:22px;background:{d1};opacity:.9"></div>'
            f'<div class="deco" style="left:392px;bottom:128px;width:44px;height:44px;border-radius:22px;background:{d3}"></div>')
    return (f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">{fontlinks()}<style>{CSS}'
            f'body{{background:{s["bg"]}}}.s{{background:{s["bg"]};color:{s["fg"]}}}</style></head>'
            f'<body><div class="s">{deco}{body}</div></body></html>')


def top(s, chip=None):
    return f'<div class="top z"><span class="chip">{chip or s["chip"]}</span>{logo(230, s["logo"])}</div>'


def send_line(st):
    t = st.get("q", "") + st.get("sub", "")
    if "سيرة" in t or "سيرتك" in t or "صاحب العمل" in t:
        who = "أرسلها لمن يبحث عن عمل"
    elif "تخرج" in t or "للطلاب" in t:
        who = "أرسلها لطالب في سنته الأخيرة"
    else:
        who = "أرسلها لصاحب مشروع"
    return who


def foot(s, who="أرسلها لصاحب مشروع"):
    return (f'<div class="foot z"><span style="display:flex;align-items:center;gap:16px;font-weight:600">'
            f'{icon("send", 42, s["acc"] if s["bg"] != TE else DK)}{who}</span>'
            f'<span class="ltr" style="font-weight:500;opacity:.85">{HANDLE}</span></div>')


def head(st, s, q=None):
    return (top(s) + spacer(84) + f'<h1 class="z">{q or st["q"]}</h1>' + spacer(26)
            + f'<p class="sub z" style="color:{s["dim"]}">{st["sub"]}</p>')


def zone(min_h=420):
    """Empty space for the Instagram sticker."""
    return f'<div class="zone" style="flex-grow:1;min-height:{min_h}px"></div>'


def options(opts, s):
    rows = "".join(
        f'<div style="display:flex;align-items:center;gap:26px;background:{s["card"]};border:3px solid {s["edge"]};'
        f'border-radius:34px;padding:20px 30px"><span class="ltr" style="flex-shrink:0;width:72px;height:72px;border-radius:36px;'
        f'background:{s["b_bg"]};color:{s["b_fg"]};display:flex;align-items:center;justify-content:center;font-size:40px;'
        f'font-weight:800">{i}</span><span style="font-size:44px;font-weight:600;line-height:1.35">{o}</span></div>'
        for i, o in enumerate(opts, 1))
    return f'<div class="z" style="display:flex;flex-direction:column;gap:20px">{rows}</div>'


def cta(text, s):
    col = DK if s["bg"] == TE else s["acc"]
    return (f'<div class="z" style="display:flex;align-items:center;gap:20px;font-size:40px;font-weight:700;line-height:1.45">'
            f'{icon("chat", 52, col, 2.2)}<span>{text}</span></div>')


def scale(s):
    dots = "".join(
        f'<span class="ltr" style="width:126px;height:126px;border-radius:63px;background:{s["b_bg"]};color:{s["b_fg"]};'
        f'display:flex;align-items:center;justify-content:center;font-size:50px;font-weight:800;opacity:{.5 + .125 * (i - 1):.2f}">{i}</span>'
        for i in range(1, 6))
    return (f'<div class="z" style="display:flex;flex-direction:column;gap:18px"><div style="display:flex;justify-content:space-between">{dots}</div>'
            f'<div style="display:flex;justify-content:space-between;font-size:36px;font-weight:600;color:{s["dim"]}">'
            f'<span>قليلاً</span><span>كثيراً</span></div></div>')


def question_box(text, s):
    return (f'<div class="z" style="border:3px dashed {s["edge"]};border-radius:40px;padding:44px 40px;display:flex;'
            f'align-items:center;gap:24px;background:{s["card"]}">{icon("chat", 64, s["acc"], 2.2)}'
            f'<span style="font-size:44px;font-weight:700;line-height:1.45">{text}</span></div>')


# ---------------------------------------------------------------- this-or-that visuals
def gem(size, fill=RED, facet=RED_M, line=GREY):
    return (f'<svg aria-hidden="true" viewBox="0 0 120 104" width="{size}" height="{size * 104 / 120:.0f}" style="display:block;flex-shrink:0">'
            f'<path d="M30 4h60l26 30-56 66L4 34z" fill="{fill}"/>'
            f'<path d="M30 4l12 30L60 4l18 30L90 4M4 34h112M42 34l18 66 18-66" fill="none" stroke="{line}" stroke-width="3.2" '
            f'stroke-linejoin="round" opacity=".55"/><path d="M42 34h36l-18 66z" fill="{facet}" opacity=".55"/></svg>')


def v_palettes():
    def sign(bg, g, f, word, line):
        return (f'<div style="width:370px;height:300px;border-radius:28px;background:{bg};display:flex;flex-direction:column;'
                f'align-items:center;justify-content:center;gap:18px">{gem(124, g, f, line)}'
                f'<span style="font-size:64px;font-weight:800;color:{word}">ياقوت</span></div>')

    def sw(cols):
        return ('<div style="display:flex;gap:20px">' + "".join(
            f'<span style="width:78px;height:78px;border-radius:39px;background:{c};border:3px solid rgba(32,33,38,.16)"></span>'
            for c in cols) + '</div>')
    a = sign(DEEP, RED, RED_M, INK, GREY) + sw([DEEP, RED, GREY])
    b = sign("#FF8FC7", "#7FD3FF", "#C9EEFF", "#FFE14D", "#FFFFFF") + sw(["#FF8FC7", "#7FD3FF", "#FFE14D"])
    return a, b


def _star(cx, cy, r, color):
    import math
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * .45
        pts.append(f"{cx + rr * math.cos(ang):.1f},{cy + rr * math.sin(ang):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{color}"/>'


def v_logos():
    import math
    stars = "".join(_star(170 + 151 * math.cos(math.radians(a)), 170 + 151 * math.sin(math.radians(a)), 11, MU)
                    for a in range(0, 360, 30))
    busy = (f'<svg aria-hidden="true" viewBox="0 0 340 340" width="290" height="290" style="display:block">'
            f'<circle cx="170" cy="170" r="164" fill="none" stroke="{RED}" stroke-width="6"/>'
            f'<circle cx="170" cy="170" r="138" fill="none" stroke="{DEEP}" stroke-width="3" stroke-dasharray="7 8"/>'
            f'<circle cx="170" cy="170" r="122" fill="#F3E3C3"/>{stars}'
            f'<path d="M58 222h224l-18 26 18 26H58l18-26z" fill="{RED}"/>'
            f'<g transform="translate(112 86)"><path d="M30 4h60l26 30-56 66L4 34z" transform="scale(.97)" fill="{RED}"/>'
            f'<path d="M30 4l12 30L60 4l18 30L90 4M4 34h112M42 34l18 66 18-66" transform="scale(.97)" fill="none" stroke="{DEEP}" stroke-width="3" opacity=".6"/></g>'
            f'<circle cx="92" cy="120" r="7" fill="{TL}"/><circle cx="248" cy="120" r="7" fill="{TL}"/>'
            f'</svg>')
    a = (busy + f'<div style="text-align:center;color:{RED};line-height:1.2"><div style="font-size:48px;font-weight:800">ياقوت</div>'
         f'<div style="font-size:34px;font-weight:300;color:{DEEP}">للمجوهرات والساعات والهدايا</div></div>')
    b = gem(170) + f'<div style="font-size:84px;font-weight:800;color:{DEEP};line-height:1">ياقوت</div>'
    return a, b


def v_cvs():
    def bars(n, widths, h=9, gap=7, color="rgba(32,33,38,.35)"):
        return "".join(f'<div style="height:{h}px;width:{widths[i % len(widths)]}%;background:{color};border-radius:4px;margin-bottom:{gap}px"></div>'
                       for i in range(n))
    cols = [TE, MU, SL, RO, TL]
    crowded_side = "".join(f'<div style="height:22px;background:{cols[i % 5]};opacity:.75;border-radius:4px;margin-bottom:8px"></div>' for i in range(6))
    a = (f'<div class="vis" style="width:360px;height:470px;background:#fff;border:3px solid rgba(32,33,38,.2);border-radius:14px;padding:16px;'
         f'display:flex;flex-direction:column;gap:10px;overflow:hidden">'
         f'<div style="display:flex;gap:12px;align-items:center"><div style="width:64px;height:64px;background:{SL};border-radius:6px"></div>'
         f'<div style="flex:1"><div style="font-size:34px;font-weight:800;color:{RED};line-height:1.1">حسين أحمد</div></div></div>'
         f'<div style="display:flex;gap:12px;flex:1"><div style="width:110px">{crowded_side}{bars(10, [100, 80, 90], 7, 5)}</div>'
         f'<div style="flex:1">{bars(30, [100, 92, 97, 85, 100, 70], 7, 5)}</div></div></div>')
    sec = "".join(f'<div style="margin-bottom:26px"><div style="height:16px;width:44%;background:{DK};border-radius:6px;margin-bottom:12px"></div>'
                  f'{bars(2, [88, 62], 10, 10)}</div>' for _ in range(4))
    b = (f'<div class="vis" style="width:360px;height:470px;background:#fff;border:3px solid rgba(32,33,38,.2);border-radius:14px;padding:30px 30px;'
         f'display:flex;flex-direction:column">'
         f'<div style="font-size:40px;font-weight:800;color:{DK};line-height:1.1">حسين أحمد</div>'
         f'<div style="height:5px;width:90px;background:{TE};border-radius:3px;margin:16px 0 28px"></div>{sec}</div>')
    return a, b


def v_weights():
    def box(wt):
        return (f'<div style="width:370px;height:420px;border-radius:28px;background:{DEEP};display:flex;flex-direction:column;'
                f'align-items:center;justify-content:center;gap:26px">{gem(96, RED, RED_M, GREY)}'
                f'<span style="font-size:104px;font-weight:{wt};color:{INK};line-height:1">ياقوت</span></div>')
    return box(100), box(800)


VISUALS = {"palettes": v_palettes, "logos": v_logos, "cvs": v_cvs, "weights": v_weights}


def tot_cards(visual, s):
    a, b = VISUALS[visual]()

    def card(label, inner):
        return (f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:22px;background:#FFFDF8;'
                f'border:3px solid {s["edge"]};border-radius:40px;padding:30px 20px 34px;box-shadow:0 14px 34px rgba(32,33,38,.10)">'
                f'<span style="width:80px;height:80px;border-radius:40px;background:{TE};color:{DK};display:flex;align-items:center;'
                f'justify-content:center;font-size:46px;font-weight:800;flex-shrink:0">{label}</span>'
                f'<div style="flex:1;width:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:26px">{inner}</div></div>')
    return f'<div class="z" style="display:flex;gap:36px;height:640px;flex-shrink:0">{card("أ", a)}{card("ب", b)}</div>'


# ---------------------------------------------------------------- story kinds
def designed(st):
    """Returns {variant: html} for the designed kinds."""
    k = st["kind"]
    s = STY[k]
    sticker = st.get("sticker", {"poll": "poll", "tot": "poll", "quiz": "quiz"}.get(k))
    who = send_line(st)
    out = {}
    if k == "tot":
        base = top(s) + spacer(70) + f'<h1 class="z">{st["q"]}</h1>' + spacer(20) + \
               f'<p class="sub z" style="color:{s["dim"]}">{st["sub"]}</p>' + spacer(44) + tot_cards(st["visual"], s)
        out["ig"] = page(base + zone(250) + foot(s, who), s)
        out["fb"] = page(base + spacer(44) + cta("اكتب «أ» أو «ب» في الرسائل.", s) + GROW + foot(s, who), s)
        return out
    out["ig"] = page(head(st, s) + zone() + foot(s, who), s)
    fb_head = head(st, s, st.get("fb_q")) + spacer(56)
    if sticker == "poll":
        fb = options(st.get("fb_options", st["options"]), s) + spacer(40) + cta("اكتب رقم اختيارك في الرسائل.", s)
    elif sticker == "quiz":
        fb = options(st["options"], s) + spacer(40) + cta("اكتب رقم جوابك في الرسائل، ثم اضغط لترى الجواب.", s)
    elif sticker == "slider":
        fb = scale(s) + spacer(48) + cta("اكتب رقماً من 1 إلى 5 في الرسائل.", s)
    elif sticker == "question":
        fb = question_box(st.get("fb_cta", "اكتب سؤالك في الرسائل، ونجيبك في الستوري."), s)
    elif sticker == "addyours":
        fb = question_box(st["fb_cta"], s)
    else:
        raise SystemExit(f"unknown sticker {sticker}")
    out["fb"] = page(fb_head + fb + GROW + foot(s, who), s)
    if sticker == "quiz":
        out["fb-answer"] = answer(st, s, who)
    return out


def answer(st, s, who):
    right = st["options"][st["answer"]]
    badge = (f'<span style="width:120px;height:120px;border-radius:60px;background:{s["b_bg"]};display:flex;align-items:center;'
             f'justify-content:center;flex-shrink:0">{icon("check", 76, s["b_fg"], 2.6)}</span>')
    body = (top(s, "اختبر نفسك · الجواب") + spacer(100) + f'<div class="z">{badge}</div>' + spacer(40)
            + f'<h1 class="z">الجواب: {right}</h1>' + spacer(30)
            + f'<p class="sub z" style="font-size:44px;line-height:1.55">{st["note"]}</p>')
    if st.get("teaser"):
        body += spacer(50) + (f'<div class="z" style="border:3px solid {s["edge"]};background:{s["card"]};border-radius:34px;padding:28px 34px;'
                              f'font-size:40px;font-weight:700;line-height:1.5">{st["teaser"]}</div>')
    body += GROW
    if st.get("source"):
        body += f'<p class="sub z" style="font-size:34px;color:{s["dim"]}">{st["source"]}</p>' + spacer(36)
    return page(body + foot(s, who), s)


def post_card(post, kind, posts):
    s = STY[kind]
    p = posts[post]
    src = os.path.join(REPO, p["img"])
    w, h = Image.open(src).size
    ph = 820
    pw = round(ph * w / h)
    line = ("تجده في صفحتنا. اضغط على اسمنا في الأعلى." if kind == "archive" else "في صفحتنا الآن. شاهده وقل رأيك.")
    body = (top(s) + spacer(56)
            + f'<div class="z" style="align-self:center;width:{pw}px;height:{ph}px;flex-shrink:0;border-radius:30px;'
              f'background:url(\'file://{src}\') center/cover;box-shadow:0 24px 54px rgba(32,33,38,.30)"></div>'
            + spacer(46) + f'<h2 class="z">{p["title"]}</h2>' + spacer(18)
            + f'<p class="sub z" style="color:{s["dim"]}">{line}</p>' + GROW + foot(s))
    return page(body, s)


# ---------------------------------------------------------------- highlight covers
HIGHLIGHTS = [("رأيك", "chart", MU), ("أعمالنا", "star", SG), ("الخدمات", "pen", TE), ("اطلب", "chat", RO),
              ("السيرة", "card", SL), ("المشاريع", "cap", TL), ("أسئلتكم", "question", CH)]


def highlight(ic, col):
    fg = CH if col in (TL, SL) else DK
    body = (f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">'
            f'<div style="width:642px;height:642px;border-radius:50%;background:{col};display:flex;align-items:center;justify-content:center">'
            f'{icon(ic, 318, fg, 1.7)}</div></div>')
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}body{{background:{DK}}}.s{{background:{DK}}}</style></head>'
            f'<body><div class="s">{body}</div></body></html>')


# ---------------------------------------------------------------- sticker notes for Marwa
def sticker_note(st):
    k, stk = st["kind"], st.get("sticker")
    if k == "archive":
        return "تلقائي على الحسابين، لا شيء عليك."
    if k == "reshare":
        extra = {"slider": f"شريط التقييم بسؤال «{st.get('prompt', '')}» وإيموجي {st.get('emoji', '😍')}",
                 "question": f"ملصق الأسئلة بنص «{st.get('prompt', '')}»"}[stk]
        return f"من المنشور نفسه: زر الإرسال ثم «أضف المنشور إلى قصتك»، وفوقه {extra}."
    if k == "tot":
        return "ملصق الاستطلاع بلا سؤال، والخياران: أ · ب"
    stk = stk or {"poll": "poll", "quiz": "quiz"}[k]
    if stk == "poll":
        return "ملصق الاستطلاع بلا سؤال، والخيارات: " + " · ".join(st["options"])
    if stk == "quiz":
        return ("ملصق الاختبار بلا سؤال، والخيارات: " + " · ".join(st["options"])
                + f"، والصحيح: {st['options'][st['answer']]}")
    if stk == "slider":
        return f"شريط التقييم بلا سؤال، والإيموجي {st.get('emoji', '😍')}"
    if stk == "question":
        return f"ملصق الأسئلة، والنص: {st['prompt']}"
    if stk == "addyours":
        return f"ملصق «أضف صورتك» (Add Yours)، والنص: {st['prompt']}"
    raise SystemExit(f"no note for {st}")


def check_text(data):
    blob = json.dumps(data, ensure_ascii=False)
    bad = [w for w in FORBIDDEN if w in blob]
    if bad:
        raise SystemExit(f"forbidden words in the stories: {bad}")


CHECK_JS = """() => { const S = document.querySelector('.s').getBoundingClientRect(), out = [];
  document.querySelectorAll('svg.wm').forEach((e, i) => { const r = e.getBoundingClientRect();
    const d = [r.left - S.left, S.right - r.right, r.top - S.top, S.bottom - r.bottom];
    if (Math.min(...d) < 40) out.push('logo margins ' + d.map(v => v.toFixed(0)).join(',')); });
  document.querySelectorAll('.z').forEach(e => { const r = e.getBoundingClientRect();
    if (r.top < %d || r.bottom > %d || r.left < 56 || r.right > 1024)
      out.push('outside safe area: ' + (e.textContent || '').trim().slice(0, 30) + ' y ' + r.top.toFixed(0) + '-' + r.bottom.toFixed(0)); });
  const z = document.querySelector('.zone'); if (z && z.getBoundingClientRect().height < 240) out.push('sticker space ' + z.getBoundingClientRect().height.toFixed(0));
  const w = document.createTreeWalker(document.querySelector('.s'), NodeFilter.SHOW_TEXT);
  while (w.nextNode()) { const n = w.currentNode; if (!n.textContent.trim()) continue; const el = n.parentElement;
    const fs = parseFloat(getComputedStyle(el).fontSize); if (fs < 34 && !el.closest('.vis') && !el.closest('svg')) out.push('text ' + fs + 'px: ' + n.textContent.trim().slice(0, 20)); }
  if (document.querySelector('.s').scrollHeight > 1920) out.push('overflow');
  return out; }""" % (TOP, BOT)


async def render_all(jobs, outdir):
    require_font()
    from playwright.async_api import async_playwright
    problems = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for name, html, checked in jobs:
            src = os.path.join(outdir, "html", name + ".html")
            open(src, "w", encoding="utf-8").write(html)
            await pg.goto("file://" + src)
            await pg.evaluate("document.fonts.ready")
            if checked and not await pg.evaluate(FONT_OK_JS):
                raise SystemExit(f"{name}: Alexandria did not load, refusing to export in a fallback font")
            await pg.wait_for_timeout(150)
            if checked:
                for msg in await pg.evaluate(CHECK_JS):
                    problems.append(f"{name}: {msg}")
            await pg.screenshot(path=os.path.join(outdir, name + ".png"), clip={"x": 0, "y": 0, "width": W, "height": H})
        await b.close()
    return problems


def sheet(paths, out, cols=5, w=216):
    h = round(w * H / W)
    rows = (len(paths) + cols - 1) // cols
    im = Image.new("RGB", (cols * w + (cols - 1) * 12, rows * h + (rows - 1) * 12), "#777")
    for i, pth in enumerate(paths):
        if pth:
            r, c = divmod(i, cols)
            im.paste(Image.open(pth).convert("RGB").resize((w, h), Image.LANCZOS), ((cols - 1 - c) * (w + 12), r * (h + 12)))
    im.save(out, quality=88)


def main(spec_path):
    data = json.load(open(spec_path, encoding="utf-8"))
    check_text(data)
    tag = os.path.splitext(os.path.basename(spec_path))[0]
    outdir = os.path.join(HERE, "out", tag)
    os.makedirs(os.path.join(outdir, "html"), exist_ok=True)
    os.makedirs(os.path.join(outdir, "preview"), exist_ok=True)
    posts = data["posts"]
    jobs, manifest = [], []
    for day in data["days"]:
        times = [st["time"] for st in day["stories"]]
        if times != SLOTS:
            raise SystemExit(f"day {day['day']}: slots {times} != {SLOTS}")
        for st in day["stories"]:
            base = f"d{day['day']}-{st['time'].replace(':', '')}"
            files = {}
            if st["kind"] == "archive":
                jobs.append((base + "-auto", post_card(st["post"], "archive", posts), True))
                files = {"ig": base + "-auto.png", "fb": base + "-auto.png"}
                ig_mode, fb_mode = "auto", "auto"
            elif st["kind"] == "reshare":
                jobs.append((base + "-fb", post_card(st["post"], "reshare", posts), True))
                files = {"fb": base + "-fb.png"}
                ig_mode, fb_mode = "native", "auto"
            else:
                for variant, html in designed(st).items():
                    jobs.append((f"{base}-{variant}", html, True))
                    files[variant] = f"{base}-{variant}.png"
                ig_mode, fb_mode = "manual", "auto"
            manifest.append({"day": day["day"], "date": day["date"], "label": day["label"], "time": st["time"],
                             "kind": st["kind"], "title": st.get("q") or posts[st["post"]]["title"], "post": st.get("post"),
                             "files": files, "ig": ig_mode, "fb": fb_mode, "sticker": sticker_note(st),
                             "highlight": st["highlight"]})
    for i, (name, ic, col) in enumerate(HIGHLIGHTS, 1):
        jobs.append((f"highlight-{i}", highlight(ic, col), False))
    problems = asyncio.run(render_all(jobs, outdir))
    for name, _, _ in jobs:
        Image.open(os.path.join(outdir, name + ".png")).convert("RGB").resize((540, 960), Image.LANCZOS) \
            .save(os.path.join(outdir, "preview", name + ".jpg"), quality=82)
    json.dump({"week": data["week"], "start": data["start"], "slots": SLOTS, "stories": manifest,
               "highlights": [{"name": n, "file": f"highlight-{i}.png"} for i, (n, _, _) in enumerate(HIGHLIGHTS, 1)]},
              open(os.path.join(outdir, "manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ig = [os.path.join(outdir, m["files"]["ig"]) if "ig" in m["files"] else os.path.join(outdir, m["files"]["fb"]) for m in manifest]
    fb = [os.path.join(outdir, m["files"]["fb"]) for m in manifest]
    sheet(ig, os.path.join(outdir, "contact-ig.jpg"))
    sheet(fb, os.path.join(outdir, "contact-fb.jpg"))
    extra = [os.path.join(outdir, n + ".png") for n, _, _ in jobs if n.endswith("-answer") or n.startswith("highlight-")]
    sheet(extra, os.path.join(outdir, "contact-extra.jpg"), cols=6)
    print(f"rendered {len(jobs)} images into {outdir}")
    if problems:
        print("CHECK FAILED:", *problems, sep="\n  ")
        sys.exit(1)
    print("check: logos inside the edges, content in the safe area, nothing under 34 px, no forbidden words")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "week-01.json"))
