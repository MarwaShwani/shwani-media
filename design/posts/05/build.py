"""Post 05: reel «سيرتك في دقيقة» الحلقة 1 — كم ثانية يقرأ صاحب العمل سيرتك؟ (short, simple version)

Row 2 (milky). 1080x1920, ~42s. One idea, everyday words, no studies or jargon on screen
(the 7.4 s figure comes from the Ladders eye-tracking study, 2018; the source is in the caption).
Marwa, 16 Oct 2026: the long version was not understood by everyone, so this one shows instead of explains:
a crowded CV turns into a clear one in three taps.

Scenes: question with choices -> 7 seconds, then the next CV -> three fixes on one CV -> the bot -> checklist to save.
The question is on screen from the first frame. No prices.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from reel import *  # noqa: F401,F403

R = Reel(bg=CH, fg=DK, acc=SL)
PAPER = "#FBF7EF"
SOFT = "rgba(32,33,38,.14)"
(T1, T2, T3, T4, T5), DUR = timeline([8.5, 7.5, 14.0, 5.5, 6.8])
VO = load_vo(HERE)          # voice-over timing from vo.json (made by vo.py); None = effects only
if VO:
    DUR = VO["dur"]
ICON_SET = ["doc", "clip", "case", "search", "pen", "clock", "check", "mail"]
# b-roll made with Veo in Marwa's Gemini (AI-made: tick Instagram's "AI info" label when posting)
BROLL_OPTS = dict(crop=(330, 0, 900, 720))     # keep the hands and the mug; the 16:9 clip is wider than the card
BROLL = broll(HERE, "broll.mp4", 900, 720, **BROLL_OPTS) if os.path.exists(os.path.join(HERE, "broll.mp4")) and not os.environ.get("NO_BROLL") else None


# ---------------- scene 1: the question ----------------
def option(t, y, label, pick_t=None, dim_t=None):
    check = fill = ""
    if pick_t is not None:
        fill = f'<div style="position:absolute;inset:0;border-radius:64px;background:{MU};{anims(an("fade", pick_t, .3))}"></div>'
        check = (f'<svg viewBox="0 0 48 48" width="52" height="52" style="position:absolute;inset:-2px;{anims(an("pop", pick_t, .5, BOUNCE))}">'
                 f'<circle cx="24" cy="24" r="24" fill="{DK}"/><path d="M14 24.5l6.5 6.5L34 17" fill="none" stroke="{MU}" '
                 f'stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    dim = anims(an("dim", dim_t, .4, "ease", "forwards")) if dim_t else ""
    inner = (f'<div style="position:absolute;inset:0;border-radius:64px;background:{PAPER};border:3px solid {SOFT}"></div>{fill}'
             f'<div style="position:relative;height:100%;display:flex;align-items:center;gap:30px;padding:0 52px">'
             f'<span style="position:relative;width:52px;height:52px;border-radius:26px;border:4px solid rgba(32,33,38,.35);flex-shrink:0">{check}</span>'
             f'<span style="font-size:54px;font-weight:700">{label}</span></div>')
    pressed = R.pressed(pick_t, inner, "position:absolute;inset:0") if pick_t else inner
    wrap = f'<div style="position:absolute;inset:0;{dim}">{pressed}</div>' if dim_t else pressed
    return R.el(t, wrap, "fromR", d=.6, cue="pop", style=f"position:absolute;left:90px;top:{y}px;width:900px;height:136px")


def scene1():
    tap = 5.3
    body = (
        R.txt(None, "كم ثانية يقرأ", 306, 94)
        + R.txt(None, "صاحب العمل", 432, 94)
        + R.txt(None, "سيرتك؟", 552, 94, color=SL)
        + option(.4, 690, "دقيقة كاملة", dim_t=tap + .15)
        + option(.6, 850, "نصف دقيقة", dim_t=tap + .15)
        + option(.8, 1010, "7 ثوانٍ", pick_t=tap)
        + R.think(1.3, 3, top=1200, ring=SL)
        + R.cursor([(4.6, 760, 1560, "show"), (tap, 560, 1078, "tap"), (tap + .9, 640, 1460, "hide")])
        + R.txt(tap + .6, "7 ثوانٍ فقط!", 1195, 84, kind="pop", cue="ding")
        + R.txt(tap + 1.2, "ثم يقرّر: يكمل القراءة، أو ينتقل لغيرك.", 1325, 46, weight=600)
    )
    R.cue(tap + .05, "confirm")
    return R.scene(T1, T2, body, cue=None, leave="sOutUp")


# ---------------- the CV in four states ----------------
def bars(top, right, widths, h=13, gap=11, o=.17):
    out = ""
    for k, w in enumerate(widths):
        out += (f'<div style="position:absolute;top:{top + k * (h + gap)}px;right:{right}px;width:{w}px;height:{h}px;'
                f'border-radius:7px;background:rgba(32,33,38,{o})"></div>')
    return out


def t_(top, text, size, weight=700, right=44, color=DK, extra=""):
    return f'<div style="position:absolute;top:{top}px;right:{right}px;font-size:{size}px;font-weight:{weight};color:{color};white-space:nowrap;{extra}">{text}</div>'


def num_line(top, text):
    return t_(top, text, 25, 600, extra="")


def cv(state, W=640, H=640):
    """0: crowded. 1: + clear name and job title on top. 2: + achievements with numbers. 3: one tidy page."""
    if state < 3:
        if state == 0:
            head = (t_(30, "السيرة الذاتية", 44, 800, right=150)
                    + f'<div style="position:absolute;top:96px;left:44px;width:74px;height:90px;border-radius:8px;background:rgba(32,33,38,.22)"></div>'
                    + t_(104, "الاسم: حسين أحمد", 21, 500) + t_(136, "التولد: 1999 · الحالة: أعزب", 19, 400) + t_(164, "العنوان: بغداد · الهاتف: ٠٧٨٠٠٠٠٠٠٠٠", 19, 400))
            top0 = 212
        else:
            head = (t_(30, "حسين أحمد", 50, 800) + t_(98, "مهندس برمجيات", 32, 700, color=SL)
                    + f'<div style="position:absolute;top:150px;right:44px;left:44px;height:3px;background:{SOFT}"></div>')
            top0 = 176
        if state < 2:
            body = (t_(top0, "الخبرات والأعمال السابقة والمهام", 22, 800)
                    + bars(top0 + 38, 44, [552, 520, 548, 500, 540, 470, 552, 515, 380])
                    + t_(top0 + 260, "الدورات والشهادات واللغات والهوايات", 22, 800)
                    + bars(top0 + 298, 44, [552, 530, 545, 490, 552, 505, 420][: 7 if state == 0 else 5]))
        else:
            body = (t_(top0, "الخبرة", 26, 800, color=TL)
                    + t_(top0 + 44, "مطوّر تطبيقات · شركة نخيل التقنية", 23, 700)
                    + num_line(top0 + 84, f'• جعلتُ التطبيق أسرع بنسبة <b style="color:{TE}">40%</b>')
                    + num_line(top0 + 120, f'• قدتُ فريقاً من <b style="color:{TE}">5</b> مطوّرين')
                    + num_line(top0 + 156, f'• أطلقتُ <b style="color:{TE}">3</b> تطبيقات خلال سنة')
                    + t_(top0 + 210, "الدورات والشهادات واللغات والهوايات", 22, 800)
                    + bars(top0 + 248, 44, [552, 530, 545, 490, 520, 470]))
        return head + body
    # state 3: one tidy page
    sec = lambda top, title: t_(top, title, 26, 800, color=TL)
    return (t_(30, "حسين أحمد", 50, 800) + t_(98, "مهندس برمجيات", 32, 700, color=SL)
            + f'<div style="position:absolute;top:150px;right:44px;left:44px;height:3px;background:{SOFT}"></div>'
            + sec(180, "الخبرة")
            + t_(222, "مطوّر تطبيقات · شركة نخيل التقنية", 23, 700)
            + num_line(262, f'• جعلتُ التطبيق أسرع بنسبة <b style="color:{TE}">40%</b>')
            + num_line(298, f'• قدتُ فريقاً من <b style="color:{TE}">5</b> مطوّرين')
            + sec(358, "التعليم")
            + t_(400, "بكالوريوس هندسة البرمجيات", 23, 700)
            + sec(460, "المهارات")
            + "".join(f'<div style="position:absolute;top:506px;right:{44 + k * 140}px;padding:6px 18px;border-radius:18px;'
                      f'background:rgba(89,113,138,.18);font-size:21px;font-weight:700;direction:ltr">{s}</div>'
                      for k, s in enumerate(["Flutter", "Python", "SQL", "Git"])))


def cv_card(inner, w=640, h=640, extra=""):
    return (f'<div style="position:absolute;inset:0;border-radius:28px;background:{PAPER};'
            f'box-shadow:0 30px 70px rgba(32,33,38,.16),0 0 0 2px {SOFT};overflow:hidden;{extra}">{inner}</div>')


# ---------------- scene 2: seven seconds, then the next CV ----------------
def scene2():
    t0 = T2
    a, b = t0 + .9, t0 + 3.7
    c = 2 * 3.14159 * 54
    for k in range(8):
        R.cue(a + k * (b - a) / 7, "tick")
    watch = (f'<div style="position:relative;width:150px;height:150px;border-radius:75px;background:{DK};color:{CH};'
             f'box-shadow:0 14px 30px rgba(32,33,38,.3)">'
             f'<svg viewBox="0 0 150 150" width="150" height="150" style="position:absolute;inset:0;transform:rotate(-90deg)">'
             f'<circle cx="75" cy="75" r="54" fill="none" stroke="rgba(242,233,216,.2)" stroke-width="12"/>'
             f'<circle cx="75" cy="75" r="54" fill="none" stroke="{MU}" stroke-width="12" stroke-linecap="round" '
             f'stroke-dasharray="{c:.1f} {2 * c:.1f}" stroke-dashoffset="{1.01 * c:.1f}" style="{anims(an("draw", a, b - a, "linear"))}"/></svg>'
             f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:4px">'
             f'<span class="ltr" style="font-size:60px;font-weight:800" data-count="0:7:{RT(a)}:{RT(b)}:0:1">0</span>'
             f'<span style="font-size:28px;font-weight:700;margin-top:14px">ث</span></div></div>')
    swipe = b + .3
    if BROLL:
        # real footage: a hand flipping through a pile of CVs, with the stopwatch on its corner
        film = (f'<div style="position:absolute;inset:0;border-radius:36px;overflow:hidden;background:{PAPER};'
                f'box-shadow:0 30px 70px rgba(32,33,38,.18),0 0 0 2px {SOFT}">{R.clip(t0 + .2, BROLL)}</div>')
        card = R.el(t0 + .2, film, "up", d=.6, cue="drop", style="position:absolute;left:90px;top:430px;width:900px;height:720px")
        watch_at = "position:absolute;left:52px;top:372px;z-index:5"
    else:
        R.kf.append("@keyframes away{0%{transform:none}100%{transform:translate(-1100px,40px) rotate(-14deg)}}")
        R.cue(swipe, "swipe")
        top_card = (f'<div style="position:absolute;inset:0;{anims(an("away", swipe, .7, "cubic-bezier(.5,0,.75,0)", "forwards"))}">'
                    f'{cv_card(cv(0))}</div>')
        back = cv_card(cv(0), extra="transform:rotate(3deg) translate(14px,10px)")
        label = (f'<div style="position:absolute;left:0;right:0;top:-60px;text-align:center;font-size:36px;font-weight:700;opacity:.75;'
                 f'{anims(an("fade", swipe + .4, .4))}">السيرة التالية</div>')
        card = R.el(t0 + .4, f'<div style="position:absolute;inset:0">{back}</div>{label}{top_card}', "up", d=.6, cue="drop",
                    style="position:absolute;left:220px;top:470px;width:640px;height:640px")
        watch_at = "position:absolute;left:150px;top:410px;z-index:5"
    body = (
        R.txt(t0 + .1, "إن لم يجد ما يريده بسرعة...", 300, 66, kind="pop", cue="pop")
        + card
        + R.el(t0 + .7, watch, "pop", d=.5, style=watch_at)
        + R.txt(swipe + .3, "...ينتقل إلى السيرة التالية.", 1250 if BROLL else 1180, 66, kind="pop", cue="ding")
    )
    return R.scene(t0, T3, body, leave="sOutUp")


# ---------------- scene 3: three fixes on one CV ----------------
PILLS = ["اسمك ووظيفتك في الأعلى", "إنجازاتك بالأرقام", "صفحة واحدة مرتبة"]


def scene3():
    t0 = T3
    taps = [t0 + 2.0, t0 + 5.6, t0 + 9.2]
    states = ""
    for s in range(4):
        t_in = t0 + .5 if s == 0 else taps[s - 1] + .1
        t_out = taps[s] + .1 if s < 3 else None
        a = [an("fade" if s == 0 else "pop", t_in, .45 if s else .4, BOUNCE if s else EASE)]
        if t_out is not None:
            a.append(an("out", t_out, .15, "ease", "forwards"))
        states += f'<div style="position:absolute;inset:0;{anims(*a)}">{cv(s)}</div>'
    tag = lambda text, bg, t, out=None: (
        f'<span style="position:absolute;left:22px;top:22px;padding:8px 24px;border-radius:24px;background:{bg};color:{DK};'
        f'font-size:32px;font-weight:800;z-index:3;{anims(an("pop", t, .45, BOUNCE), *([an("out", out, .25, "ease", "forwards")] if out else []))}">{text}</span>')
    board = R.el(t0 + .3, cv_card(states + tag("قبل", RO, t0 + .6, taps[0]) + tag("بعد", MU, taps[2] + .4)), "up", d=.6, cue="drop",
                 style="position:absolute;left:220px;top:440px;width:640px;height:640px")
    pills = ""
    for k, (name, on) in enumerate(zip(PILLS, taps)):
        y = 1110 + k * 118
        inner = (f'<div style="position:absolute;inset:0;border-radius:54px;background:{PAPER};border:3px solid {SOFT}"></div>'
                 f'<div style="position:absolute;inset:0;border-radius:54px;background:{TL};{anims(an("fade", on, .25))}"></div>'
                 f'<div style="position:absolute;inset:0;display:flex;align-items:center;gap:22px;padding:0 34px;font-size:42px;font-weight:700">'
                 f'<span class="ltr" style="width:56px;height:56px;border-radius:28px;background:{DK};color:{CH};display:flex;align-items:center;'
                 f'justify-content:center;font-size:30px">{k + 1}</span>{name}</div>'
                 f'<div style="position:absolute;inset:0;display:flex;align-items:center;gap:22px;padding:0 34px;font-size:42px;font-weight:700;'
                 f'color:{CH};{anims(an("fade", on, .25))}"><span class="ltr" style="width:56px;height:56px;border-radius:28px;background:{CH};'
                 f'color:{TL};display:flex;align-items:center;justify-content:center;font-size:30px">{k + 1}</span>{name}</div>')
        pills += R.el(t0 + .9 + k * .15, R.pressed(on, inner, "position:absolute;inset:0"), "fromR", d=.5,
                      style=f"position:absolute;left:90px;top:{y}px;width:900px;height:104px")
        R.cue(on + .1, "pop")
    body = (
        R.txt(t0 + .1, "3 تعديلات تجعله يكمل القراءة", 300, 54, kind="pop", cue="pop", extra="white-space:nowrap")
        + board + pills
        + R.cursor([(t0 + 1.3, 760, 1600, "show")] + [(t, 540, 1162 + k * 118, "tap") for k, t in enumerate(taps)]
                   + [(taps[2] + .8, 700, 1600, "hide")])
    )
    return R.scene(t0, T4, body, leave="sOutUp")


# ---------------- scene 4: the bot ----------------
def scene4():
    t0 = T4
    ty0, ty1 = t0 + 1.7, t0 + 3.0
    search = (f'<div style="position:absolute;inset:0;border-radius:60px;background:{PAPER};border:3px solid {SOFT}"></div>'
              f'<div style="position:relative;height:100%;display:flex;align-items:center;gap:22px;padding:0 40px;direction:ltr">'
              f'<svg viewBox="0 0 40 40" width="44" height="44"><circle cx="17" cy="17" r="12" fill="none" stroke="{DK}" stroke-width="4"/>'
              f'<path d="M26 26l9 9" stroke="{DK}" stroke-width="4" stroke-linecap="round"/></svg>'
              + R.typing(ty0, ty1, "Sira_Thatiya_CV_bot", "font-size:44px;font-weight:600") + '</div>')
    tap = t0 + 4.0
    result = (f'<div style="position:absolute;inset:0;border-radius:34px;background:{SL}"></div>'
              f'<div style="position:relative;height:100%;display:flex;align-items:center;gap:26px;padding:0 34px;direction:ltr;color:{CH}">'
              f'<span style="width:96px;height:96px;border-radius:48px;background:{CH};display:flex;align-items:center;justify-content:center">'
              f'<svg viewBox="0 0 48 48" width="50" height="50"><rect x="9" y="5" width="30" height="38" rx="5" fill="none" stroke="{SL}" stroke-width="4"/>'
              f'<path d="M16 16h16M16 24h16M16 32h10" stroke="{SL}" stroke-width="4" stroke-linecap="round"/></svg></span>'
              f'<span style="font-size:40px;font-weight:700">Sira_Thatiya_CV_bot</span></div>')
    R.cue(ty1 + .15, "enter")
    body = (
        R.txt(t0 + .1, "لا وقت لتعديلها؟", 320, 84, kind="pop", cue="pop")
        + R.txt(t0 + .6, "نكتب سيرتك خلال 24 ساعة.", 450, 56, weight=600)
        + R.txt(t0 + 1.1, "ابحث في تيليغرام عن:", 640, 44, weight=700, kind="fade")
        + R.el(t0 + 1.3, search, "up", style="position:absolute;left:90px;top:720px;width:900px;height:128px")
        + R.el(t0 + 3.2, R.pressed(tap, result, "position:absolute;inset:0"), "up", cue="pop",
               style="position:absolute;left:90px;top:880px;width:900px;height:150px")
        + R.cursor([(t0 + 3.3, 760, 1300, "show"), (tap, 640, 955, "tap"), (tap + .6, 700, 1250, "hide")])
    )
    return R.scene(t0, T5, body, leave="sOutUp")


# ---------------- scene 5: checklist to save, and send ----------------
def scene5():
    t0 = T5
    body = (R.endcard(t0, "قبل أن ترسل سيرتك:", PILLS, "أرسله لصديق يبحث عن عمل",
                      card_bg=PAPER, card_fg=DK, tick_bg=TL, tick_fg=CH, send_bg=MU, send_fg=DK, logo_color=DK, edge=SOFT)
            + R.txt(t0 + 2.2, "احفظ الفيديو لتعود إليه قبل كل تقديم.", 900, 44, weight=600, kind="fade"))
    return R.scene(t0, None, body)


def cover():
    num = (f'<div style="position:absolute;left:90px;top:420px;width:900px;height:560px">'
           f'<div style="position:absolute;right:60px;top:250px;width:560px;height:190px;border-radius:95px;background:{SL}"></div>'
           f'<div style="position:absolute;right:640px;top:170px;width:110px;height:110px;border-radius:55px;background:{TL}"></div>'
           f'<div style="position:absolute;right:110px;top:40px;display:flex;align-items:baseline;gap:24px;color:{DK}">'
           f'<span class="ltr" style="font-size:400px;font-weight:800;line-height:1">7</span>'
           f'<span style="font-size:120px;font-weight:800">ثوانٍ</span></div></div>')
    chip = (f'<span style="padding:14px 34px;border-radius:44px;border:3px solid {DK};font-size:34px;font-weight:600">'
            f'سيرتك في دقيقة · الحلقة 1</span>')
    body = (
        R.touches(ICON_SET, opacity=.08, seed=5)
        + f'<div class="ab" style="right:90px;top:330px">{chip}</div>'
        + num
        + f'<div class="ab" style="right:90px;left:90px;top:1050px;font-size:104px;font-weight:800;line-height:1.22">هذا كل ما تأخذه<br>سيرتك من وقته</div>'
        + f'<div class="ab" style="right:90px;left:90px;top:1360px;font-size:46px;font-weight:600;line-height:1.6">3 تعديلات تجعله يكمل القراءة</div>'
        + f'<div class="ab" style="left:90px;top:1500px">{lockup_svg(300, DK)}</div>'
    )
    return R.still_page(body)


EXTRA = ""


def build():
    body = (R.touches(ICON_SET, opacity=.1, seed=5) + R.chrome("سيرتك في دقيقة · الحلقة 1")
            + scene1() + scene2() + scene3() + scene4() + scene5())
    return R.page(body, EXTRA)


if __name__ == "__main__":
    html = build()
    stills = [0.0, 3.0, 6.8, 9.5, 12.0, 15.0, 18.0, 21.5, 25.0, 28.5, 33.5, 41.5]
    if "--stills" in sys.argv:
        stills = [float(s) for s in sys.argv[sys.argv.index("--stills") + 1].split(",")]
    R.render(HERE, html, DUR, cover_html=cover(), stills=[RT(x) for x in stills], voice=VO["voice"] if VO else None)
