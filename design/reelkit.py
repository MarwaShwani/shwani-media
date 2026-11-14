"""Shared pieces for the reels from 17 on (plan of 15-28 Nov 2026). Built on reel.py.

Each reel keeps the house rules (SHWANI-COMPANY-project.md, «الريلز»): the question on screen from the first
frame, a fast «فكّر قليلاً» clock for as long as the voice needs (load_intro), one idea, everyday words,
a closing card worth saving and «أرسله لـ...», real recorded sounds only, nothing under 34 px, and the
key content between y=260 and y=1480. The background is the colour of the reel's grid row.
The cover is the row's carousel cover (kit2), scaled so the grid's centre 3:4 matches a 4:5 post.
"""
import os, sys, asyncio
DESIGN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DESIGN)
from reel import *  # noqa: F401,F403
from reel import _still  # noqa
from rounded import lockup
from PIL import Image


def rgba(hex_, a):
    h = hex_.lstrip("#")
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{a})"


STY = {
    "sage":     dict(bg=SG, fg=DK, acc=TE, card=CH, cfg=DK, hi=TE, tick=(DK, CH), send=(CH, DK), logo=(DK, TE)),
    "charcoal": dict(bg=DK, fg=CH, acc=MU, card="#2C2D34", cfg=CH, hi=MU, tick=(MU, DK), send=(MU, DK), logo=(CH, TE)),
    "slate":    dict(bg=SL, fg=CH, acc=TE, card=CH, cfg=DK, hi=TE, tick=(TE, DK), send=(CH, DK), logo=(CH, TE)),
    "terra":    dict(bg=TE, fg=DK, acc=DK, card=CH, cfg=DK, hi=DK, tick=(DK, CH), send=(DK, CH), logo=(DK, DK)),
    "teal":     dict(bg=TL, fg=CH, acc=RO, card=CH, cfg=DK, hi=RO, tick=(RO, DK), send=(CH, DK), logo=(CH, TE)),
}


def logo_html(width, word, bar):
    svg = lockup(word, bar, word)
    return svg.replace('<svg ', f'<svg style="width:{width}px;height:auto;display:block" ', 1) \
              .replace(' width="', ' data-w="', 1).replace(' height="1180"', '', 1)


class Kit:
    def __init__(self, row):
        self.row = row
        self.s = s = STY[row]
        self.R = Reel(bg=s["bg"], fg=s["fg"], acc=s["acc"])

    # ---- frame
    def chrome(self, series):
        s = self.s
        chip = (f'<span style="padding:12px 30px;border-radius:40px;border:3px solid {s["fg"]};font-size:32px;font-weight:600;color:{s["fg"]}">'
                f'{series}</span>')
        return (f'<div style="position:absolute;right:80px;top:212px;z-index:3">{chip}</div>'
                f'<div style="position:absolute;left:80px;top:214px;z-index:3">{logo_html(250, *s["logo"])}</div>')

    def think(self, t, secs, top=1330):
        s = self.s
        dark = s["fg"] == CH
        return self.R.think(t, secs, top=top, ring=s["hi"] if dark else s["hi"],
                            card=rgba(s["fg"], .08), edge=rgba(s["fg"], .24), track=rgba(s["fg"], .2))

    # ---- pieces
    def card(self, html, pad=40, extra=""):
        s = self.s
        return (f'<div style="background:{s["card"]};color:{s["cfg"]};border-radius:40px;padding:{pad}px;'
                f'box-shadow:0 26px 60px rgba(0,0,0,.18);{extra}">{html}</div>')

    def img(self, path, w, h, radius=34, fit="cover", pos="center", extra=""):
        return (f'<div style="width:{w}px;height:{h}px;border-radius:{radius}px;overflow:hidden;'
                f'background:url(\'file://{path}\') {pos}/{fit} no-repeat;box-shadow:0 28px 64px rgba(0,0,0,.28);{extra}"></div>')

    def box(self, t, x, y, w, h, label=None, out=None, color=None, label_below=False, cue="select"):
        """A rounded highlight drawn around part of a picture (absolute, page coordinates), with a label chip."""
        c = color or self.s["hi"]
        lab = ""
        if label:
            ly = f"top:{h + 14}px" if label_below else "bottom:" + f"{h + 14}px"
            fg = DK if c in (MU, TE, RO, CH, SG) else CH
            lab = (f'<span style="position:absolute;{ly};left:50%;transform:translateX(-50%);white-space:nowrap;background:{c};color:{fg};'
                   f'border-radius:30px;padding:10px 26px;font-size:36px;font-weight:800">{label}</span>')
        inner = f'<div style="position:absolute;inset:0;border:6px solid {c};border-radius:26px"></div>{lab}'
        return self.R.el(t, inner, "pop", d=.5, out=out, cue=cue, style=f"position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:6")

    def step(self, t, n, title, top=330, out=None):
        s = self.s
        html = (f'<div style="display:flex;align-items:center;gap:26px;justify-content:center">'
                f'<span class="ltr" style="width:96px;height:96px;border-radius:48px;background:{s["hi"]};color:{DK if s["hi"] != DK else CH};'
                f'display:flex;align-items:center;justify-content:center;font-size:54px;font-weight:800;flex-shrink:0">{n}</span>'
                f'<span style="font-size:66px;font-weight:800;line-height:1.3">{title}</span></div>')
        return self.R.el(t, html, "up", d=.6, out=out, cue="pop", style=f"position:absolute;left:90px;width:900px;top:{top}px")

    def end(self, t0, title, items, send, line=None):
        s, R = self.s, self.R
        tb, tf = s["tick"]
        sb, sf = s["send"]
        body = R.endcard(t0, title, items, send, card_bg=s["card"], card_fg=s["cfg"], tick_bg=tb, tick_fg=tf,
                         send_bg=sb, send_fg=sf, logo_color=s["fg"], edge=rgba(DK, .1))
        if s["logo"][1] == s["logo"][0] or s["bg"] == TE:   # one-colour logo on terracotta
            body = body.replace(lockup_svg(330, s["fg"]), logo_html(330, *s["logo"]))
        if line:
            body += R.txt(t0 + 2.2, line, 960, 44, weight=600, kind="fade")
        return body

    def page(self, body, extra_css=""):
        return self.R.page(body, extra_css)


# ---------------------------------------------------------------- covers
def reel_cover(here, slide_html):
    """slide_html: a 1080x1350 kit2 cover. Rendered, scaled x1.0667 and centred on a 1080x1920 page of the same
    colour, so the grid's centre 3:4 of the reel shows exactly the centre 3:4 of the post-style cover."""
    src = os.path.join(here, "cover-slide.html")
    open(src, "w", encoding="utf-8").write(slide_html)
    png = os.path.join(here, "cover-slide.png")

    async def shot():
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            b = await p.chromium.launch()
            pg = await b.new_page(viewport={"width": 1080, "height": 1350})
            await pg.goto("file://" + src)
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=png, clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
            await b.close()
    asyncio.run(shot())
    im = Image.open(png).convert("RGB")
    bgc = im.getpixel((5, 5))
    k = 1440 / 1350
    sc = im.resize((round(1080 * k), 1440), Image.LANCZOS)
    out = Image.new("RGB", (1080, 1920), bgc)
    out.paste(sc, ((1080 - sc.width) // 2, 240))
    out.save(os.path.join(here, "cover.png"))
    out.convert("RGB").save(os.path.join(here, "cover.jpg"), quality=92)
    return os.path.join(here, "cover.png")


def region(path, box, w, radius=30, extra=""):
    """Show only part of a picture (box = fractions x0,y0,x1,y1), w pixels wide."""
    W_, H_ = Image.open(path).size
    x0, y0, x1, y1 = box
    k = w / ((x1 - x0) * W_)
    h = (y1 - y0) * H_ * k
    return (f'<div style="width:{w}px;height:{h:.0f}px;border-radius:{radius}px;overflow:hidden;box-shadow:0 26px 60px rgba(0,0,0,.25);'
            f'background:url(\'file://{path}\') {-x0 * W_ * k:.1f}px {-y0 * H_ * k:.1f}px/{W_ * k:.1f}px {H_ * k:.1f}px no-repeat;{extra}"></div>'), h
