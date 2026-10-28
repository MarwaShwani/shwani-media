"""Post 11: reel «أعمالنا 2: فيلم هويتنا», ~40 s (Marwa, 28 Oct 2026: the reel is the brand film).

The 16:9 brand film (brand/film.py) re-cut for a phone: 1080x1920, every mockup shown whole and large,
on the row-4 terracotta with charcoal text. Reel rules (SHWANI-COMPANY-project.md):
- the question is on screen from the first frame, the first movement within half a second,
  then a fast «فكّر قليلاً» clock (a tick every 0.2 s): the whole opening is 2 seconds (Marwa, 28 Oct:
  a long wait loses the viewer, so every reel opens in 2 seconds at most), and the answer
  «في كل مكان.» opens the photos;
- the photos come in groups, and each group's line is what the voice-over says at that moment;
- the end card is worth saving (the first three pieces a company needs) and asks to send it on;
- sounds: paper sliding for each photo, a soft whoosh between scenes, no chimes;
- no price, no storefront photo; content between y=260 and y=1480.
On terracotta the terracotta link of the logo would vanish, so the logo is one-colour charcoal (as in post 10),
or full colour on a charcoal card.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, DESIGN)
from reel import *  # noqa: F401,F403
from rounded import lockup  # noqa: E402
from PIL import Image

MOCKS = os.environ.get("MOCKS", os.path.join(DESIGN, "brand", "out", "mockups"))
R = Reel(bg=TE, fg=DK, acc=DK)
SERIES = "أعمالنا · الحلقة 2"
ICON_SET = ["doc", "mail", "pen", "case", "bag", "star", "book", "square"]
PHOTO_D = 2.0                       # seconds per photo

# groups: (line on screen = what the voice says, [(mockup, label)])
GROUPS = [
    ("في المكتب", [("01-business-cards", "بطاقة العمل"), ("02-stationery", "الأوراق الرسمية"),
                   ("07-company-profile", "الملف التعريفي")]),
    ("في المعارض وعلى الطريق", [("03-flyer", "الفلاير"), ("04-rollup", "الرول أب"), ("13-outdoor-banner", "البنر الخارجي")]),
    ("على فريق العمل", [("12-tshirts", "التيشيرت"), ("11-tote", "الحقيبة")]),
    ("في هدايا العملاء", [("14-mugs", "الأكواب"), ("09-packaging", "علبة الهدايا"), ("08-notebook", "الدفتر والقلم"),
                         ("16-executive-pen", "طقم القلم الفاخر")]),
    ("وعلى كل شاشة", [("10-screens", "الشاشات")]),
]
N_PHOTOS = sum(len(g[1]) for g in GROUPS)
INTRO = 2.0                         # the opening, question to first photo (Marwa, 28 Oct: 2 s at most)
(T1, T2, T3), DUR = timeline([INTRO, N_PHOTOS * PHOTO_D + .6, 7.6])
ANSWER_D = 1.0                      # «في كل مكان.» heads the first photo for a second, then the group lines
DUR_DESIGN = DUR


def _group_starts():
    t, out = T2 + .2, []
    for gi, (_, items) in enumerate(GROUPS):
        out.append(T2 + ANSWER_D + .1 if gi == 0 else t)
        t += len(items) * PHOTO_D
    return out


# Voice-over (Bodi, Marwa 28 Oct): each sentence is said the moment its line is on screen, in this order.
# (design time, sentence, hold_at): if the sentence before runs long, the video waits at hold_at
# (default: just before the line, so the photo and the group line on screen wait with it).
# The question must fit the 2-second opening: vo.py speeds it up a little rather than make the opening wait.
_G = _group_starts()
VO_PLAN = [
    (0.0, "بعد الشعار، أين تظهر هويتك؟", None),
    (T2, "في كل مكان.", None),
    (_G[0], "في المكتب،", None),
    (_G[1], "في المعارض وعلى الطريق،", None),
    (_G[2], "على فريق العمل،", None),
    (_G[3], "في هدايا العملاء،", None),
    (_G[4], "وعلى كل شاشة.", None),
    (T3, "أول ثلاث قطع لشركتك: بطاقة العمل، والورق الرسمي والظرف، والملف التعريفي.", None),
    (T3 + 2.2, "احفظه قبل أن تطبع هويتك، وأرسله لصاحب مشروع جديد.", T3 + 2.21),
]
VO = load_vo(HERE)
if VO:
    DUR = VO["dur"]


def mono(width, color=DK):
    svg = lockup(color, color, color)
    return svg.replace('<svg ', f'<svg style="width:{width}px;height:auto;display:block" ', 1) \
              .replace(' width="', ' data-w="', 1).replace(' height="1180"', '', 1)


def small(name, w=1100):
    """A web-sized copy of the mockup next to the reel (the full 2528 px files are slow to paint per frame)."""
    os.makedirs(os.path.join(HERE, "img"), exist_ok=True)
    out = os.path.join(HERE, "img", name + ".jpg")
    if not os.path.exists(out):
        im = Image.open(os.path.join(MOCKS, name + ".jpg")).convert("RGB")
        im.thumbnail((w, w), Image.LANCZOS)
        im.save(out, quality=90)
    with Image.open(out) as im:
        return out, im.size


def chrome():
    chip = (f'<span style="padding:12px 30px;border-radius:40px;border:3px solid {DK};font-size:32px;font-weight:600;color:{DK}">'
            f'{SERIES}</span>')
    return (f'<div style="position:absolute;right:80px;top:212px;z-index:3">{chip}</div>'
            f'<div style="position:absolute;left:80px;top:214px;z-index:3">{mono(250)}</div>')


# ---------------- scene 1: the question, the logo, think ----------------
def scene1():
    card = (f'<div style="background:{DK};border-radius:44px;padding:96px 70px 86px;display:flex;justify-content:center;'
            f'box-shadow:0 30px 70px rgba(32,33,38,.3)">{lockup_svg(600, CH)}</div>')
    body = (
        R.txt(None, "بعد الشعار،<br>أين تظهر هويتك؟", 340, 92)
        + R.el(0, card, "zoom", d=.5, style="position:absolute;left:150px;top:650px;width:780px")
        + R.think(.2, 1.2, top=1180, ring=DK, card="rgba(32,33,38,.08)", edge="rgba(32,33,38,.22)", track="rgba(32,33,38,.2)")
    )
    return R.scene(0, T2, body, leave="sOutUp")


# ---------------- scene 2: the photos, group by group ----------------
def scene2():
    t = T2 + .2
    body = R.txt(T2, "في كل مكان.", 318, 64, kind="pop", d=.5, out=T2 + ANSWER_D - .3)
    box_w, box_h, box_top = 1000, 880, 430
    for gi, (line, items) in enumerate(GROUPS):
        g0, g1 = t, t + len(items) * PHOTO_D
        if gi == 0:
            g0 = T2 + ANSWER_D + .1
        last = gi == len(GROUPS) - 1
        body += R.txt(g0, line, 318, 60, kind="fromR", out=None if last else g1 - .3)
        for name, label in items:
            path, (w, h) = small(name)
            k = min(box_w / w, box_h / h)
            pw, ph = int(w * k), int(h * k)
            x, y = (1080 - pw) // 2, box_top + (box_h - ph) // 2
            kb = f"kb{R.uid()}"
            R.kf.append(f"@keyframes {kb}{{from{{transform:scale(1)}}to{{transform:scale(1.07)}}}}")
            photo = (f'<div style="width:{pw}px;height:{ph}px;border-radius:30px;overflow:hidden;box-shadow:0 30px 70px rgba(32,33,38,.32)">'
                     f'<img src="file://{path}" style="display:block;width:100%;height:100%;object-fit:cover;'
                     f'{anims(an(kb, t, PHOTO_D + .6, "linear", "both"))}"></div>')
            tag = (f'<div style="position:absolute;left:0;right:0;top:{ph + 26}px;display:flex;justify-content:center">'
                   f'<span style="padding:10px 32px;border-radius:36px;background:{DK};color:{CH};font-size:40px;font-weight:700">{label}</span></div>')
            end = t + PHOTO_D
            body += R.el(t, photo + tag, "fromL", d=.5, cue="swipe",
                         out=None if (last and name == items[-1][0]) else end - .05, out_d=.3,
                         style=f"position:absolute;left:{x}px;top:{y}px;width:{pw}px")
            t = end
    return R.scene(T2, T3, body, cue="whoosh")


# ---------------- scene 3: save and send ----------------
def scene3():
    t0 = T3
    html = R.endcard(t0, "أول 3 قطع لشركتك:", ["بطاقة العمل", "الورق الرسمي والظرف", "الملف التعريفي"],
                     "أرسله لصاحب مشروع جديد", card_bg=CH, card_fg=DK, tick_bg=TE, tick_fg=DK, send_bg=DK, send_fg=CH,
                     logo_color=DK)
    html = html.replace(lockup_svg(330, DK), mono(330))        # the terracotta link would vanish on terracotta
    return R.scene(t0, None, html + R.txt(t0 + 2.2, "احفظه قبل أن تطبع هويتك.", 900, 44, weight=600, kind="fade"))


def cover():
    path, (w, h) = small("14-mugs")
    chip = (f'<span style="padding:14px 34px;border-radius:44px;border:3px solid {DK};font-size:34px;font-weight:600">{SERIES}</span>')
    photo = (f'<div class="ab" style="left:90px;top:420px;width:900px;height:640px;border-radius:34px;overflow:hidden;'
             f'box-shadow:0 30px 70px rgba(32,33,38,.3);background:url(\'file://{path}\') center/cover"></div>')
    body = (
        R.touches(ICON_SET, opacity=.1, seed=5)
        + f'<div class="ab" style="right:90px;top:310px">{chip}</div>'
        + photo
        + f'<div class="ab" style="right:90px;left:90px;top:1110px;font-size:100px;font-weight:800;line-height:1.22">فيلم هويتنا</div>'
        + f'<div class="ab" style="right:90px;left:90px;top:1265px;font-size:44px;font-weight:600;line-height:1.6">هكذا تبدو هويتنا مطبوعة.</div>'
        + f'<div class="ab" style="left:90px;top:1510px">{mono(300)}</div>'
    )
    return R.still_page(body)


def build():
    body = R.touches(ICON_SET, opacity=.1, seed=5) + chrome() + scene1() + scene2() + scene3()
    return R.page(body)


if __name__ == "__main__":
    html = build()
    stills = [0.0, .5, 1.0, 1.45, 2.4, 3.4, 8.6, 14.6, 18.6, 22.6, 26.6, 29.6, 32.0, 34.5, DUR - .1]
    R.render(HERE, html, DUR, cover_html=cover(), stills=[RT(x) if x < DUR - .1 else x for x in stills], voice=VO["voice"] if VO else None)
