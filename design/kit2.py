"""Slide kit for the posts from 16 on (plan of 15-28 Nov 2026, Marwa, 14 Nov).

Same rules as common.py (1080x1350, Alexandria only, title 70, text 32-36, bars 24-28, nothing under 24),
plus one colour per grid row. A post module builds its slides with these helpers and calls build():

    from kit2 import *
    R = row("sage")
    slides = [R.cover(...), R.photo(...), ..., R.closing(...)]
    build(HERE, slides)

Every export is checked: logo 40 px inside the edges, no text under the bottom bar, nothing under 24 px,
and no forbidden word (price, dinar, Canva, ready templates, «تابعونا»).
"""
import os, sys, asyncio, hashlib
DESIGN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DESIGN)
from common import *  # noqa: F401,F403
from common import render as _render_slides
from rounded import lockup  # noqa: E402
from PIL import Image, ImageFilter, ImageEnhance

ASSETS = os.path.join(DESIGN, "assets")
CACHE = os.path.join(DESIGN, "_cache")
FORBIDDEN = ["دينار", "سعر", "أسعار", "Canva", "قوالب جاهزة", "تابعونا", "دولار"]


def A(*p):
    return os.path.join(ASSETS, *p)


def page_img(book, n):
    return A("booklets", book, f"p-{n:02d}.jpg")


def rgba(hex_, a):
    h = hex_.lstrip("#")
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{a})"


# ------------------------------------------------------------------ images
def fit(path, w, h, shift=(0.0, 0.0), whole=False):
    """Crop (or, whole=True, letterbox over a blurred copy) an image to w x h; returns a cached file path."""
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.md5(f"{path}{w}{h}{shift}{whole}{os.path.getmtime(path)}".encode()).hexdigest()[:12]
    out = os.path.join(CACHE, f"{key}.jpg")
    if os.path.exists(out):
        return out
    src = Image.open(path).convert("RGB")
    sw, sh = src.size
    if whole:
        bg = src.resize((w, int(sh * w / sw)) if sw / sh < w / h else (int(sw * h / sh), h), Image.LANCZOS)
        bg = bg.crop(((bg.width - w) // 2, (bg.height - h) // 2, (bg.width - w) // 2 + w, (bg.height - h) // 2 + h))
        bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(30))).enhance(.7)
        k = min(w / sw, h / sh)
        fg = src.resize((int(sw * k), int(sh * k)), Image.LANCZOS)
        bg.paste(fg, ((w - fg.width) // 2, (h - fg.height) // 2))
        bg.save(out, quality=92)
        return out
    r = w / h
    if sw / sh > r:
        cw = int(sh * r); x0 = int((sw - cw) / 2 * (1 + shift[0])); box = (x0, 0, x0 + cw, sh)
    else:
        ch = int(sw / r); y0 = int((sh - ch) / 2 * (1 + shift[1])); box = (0, y0, sw, y0 + ch)
    src.crop(box).resize((w, h), Image.LANCZOS).save(out, quality=92)
    return out


def url(p):
    return f"url('file://{p}')"


# ------------------------------------------------------------------ rows
ROWS = {
    # name: bg, fg, dim text, card bg, card fg, number badge bg/fg, accent, logo (word, bar), decorations
    "sage":     dict(bg=SG, fg=DK, dim=rgba(DK, .76), card=CH, card_fg=DK, nb=DK, nf=CH, acc=DK, logo=(DK, TE), deco=(CH, TE, TL)),
    "charcoal": dict(bg=DK, fg=CH, dim=rgba(CH, .76), card=rgba(CH, .07), card_fg=CH, nb=MU, nf=DK, acc=MU, logo=(CH, TE), deco=(MU, TE, RO)),
    "slate":    dict(bg=SL, fg=CH, dim=rgba(CH, .82), card=CH, card_fg=DK, nb=DK, nf=CH, acc=CH, logo=(CH, TE), deco=(TE, RO, CH)),
    "teal":     dict(bg=TL, fg=CH, dim=rgba(CH, .82), card=CH, card_fg=DK, nb=RO, nf=DK, acc=RO, logo=(CH, TE), deco=(RO, SG, TE)),
    "terra":    dict(bg=TE, fg=DK, dim=rgba(DK, .74), card=CH, card_fg=DK, nb=DK, nf=CH, acc=DK, logo=(DK, DK), deco=(RO, CH, DK)),
    "milky":    dict(bg=CH, fg=DK, dim=rgba(DK, .74), card="#FBF7EF", card_fg=DK, nb=TE, nf=DK, acc=TE, logo=(DK, TE), deco=(TE, MU, TL)),
}


def logo_svg(width, word, bar):
    svg = lockup(word, bar, word)
    return svg.replace('<svg ', f'<svg class="wm" style="width:{width}px;height:auto;display:block;flex-shrink:0" ', 1) \
              .replace(' width="', ' data-w="', 1).replace(' height="1180"', '', 1)


class row:
    def __init__(self, name, n=None):
        self.name, self.s, self.n = name, ROWS[name], n

    # ---- wrappers
    def pg(self, body, css=""):
        s = self.s
        extra = (f".card{{background:{s['card']};color:{s['card_fg']};border-radius:34px}}"
                 f".dim{{color:{s['dim']}}}" + css)
        return page(body, extra, bg=s["bg"], fg=s["fg"])

    def logo(self, w=250):
        return logo_svg(w, *self.s["logo"])

    def num(self, k, size=64):
        s = self.s
        return (f'<span class="ltr" style="flex-shrink:0;width:{size}px;height:{size}px;border-radius:{size // 2}px;background:{s["nb"]};'
                f'color:{s["nf"]};display:flex;align-items:center;justify-content:center;font-size:{int(size * .5)}px;font-weight:800">{k}</span>')

    def bot(self, last=False, single=False):
        if last or single:
            return bottom(right_html=self.logo(250))
        return bottom(arrow=self.s["acc"] if self.s["bg"] != DK else MU)

    def head(self, chip, i):
        if self.n is None:      # single image post: chip only
            return f'<div class="top"><span class="chip">{chip}</span><span></span></div>'
        return top(chip, i, self.n)

    # ---- visuals
    def band(self, path, h=760, badge=None, shift=(0, 0), whole=False, radius=0, inset=False):
        """A photo the full width of the slide (or inset with rounded corners)."""
        w = 936 if inset else 1080
        p = fit(path, w, h, shift, whole)
        s = self.s
        sticker = (f'<span class="ltr" style="position:absolute;right:{36 if inset else 72}px;bottom:28px;width:88px;height:88px;border-radius:44px;'
                   f'background:{s["nb"]};color:{s["nf"]};border:6px solid {s["bg"]};display:flex;align-items:center;justify-content:center;'
                   f'font-size:42px;font-weight:800">{badge}</span>') if badge else ""
        margin = "0" if inset else "0 -72px"
        return (f'<div class="z" style="margin:{margin};width:{w}px;height:{h}px;flex-shrink:0;position:relative;border-radius:{radius}px;'
                f'background:{url(p)} center/cover;box-shadow:0 18px 40px rgba(0,0,0,.22)">{sticker}</div>')

    def sheets(self, paths, h=760, rot=(-4, 3), gap=-60, badge=None, shadow=.32):
        """Booklet pages as paper sheets on the row colour (one, two or three, overlapping)."""
        k = len(paths)
        ph = h - 70
        pw = int(ph * 827 / 1170)
        if k == 1:
            items = [(0, rot[0] if isinstance(rot, tuple) else rot)]
        else:
            items = [((j - (k - 1) / 2) * (pw + gap), r) for j, r in zip(range(k), (rot * 3)[:k])]
        html = ""
        for (dx, r), path in zip(items, paths):
            p = fit(path, pw * 2 // 2, ph, whole=False)
            html += (f'<img src="file://{p}" style="position:absolute;left:{540 - pw / 2 + dx:.0f}px;top:35px;width:{pw}px;height:{ph}px;'
                     f'border-radius:10px;transform:rotate({r}deg);box-shadow:0 26px 50px rgba(0,0,0,{shadow}),0 2px 6px rgba(0,0,0,.18)">')
        s = self.s
        sticker = (f'<span class="ltr" style="position:absolute;right:72px;bottom:10px;width:88px;height:88px;border-radius:44px;z-index:3;'
                   f'background:{s["nb"]};color:{s["nf"]};border:6px solid {s["bg"]};display:flex;align-items:center;justify-content:center;'
                   f'font-size:42px;font-weight:800">{badge}</span>') if badge else ""
        return f'<div class="z" style="margin:0 -72px;width:1080px;height:{h}px;flex-shrink:0;position:relative">{html}{sticker}</div>'

    def crop_sheet(self, path, box, w=936, h=None, badge=None):
        """A close-up of part of a page (box = fractions x0,y0,x1,y1), as a card with a shadow."""
        im = Image.open(path).convert("RGB")
        W_, H_ = im.size
        x0, y0, x1, y1 = box
        os.makedirs(CACHE, exist_ok=True)
        key = hashlib.md5(f"{path}{box}{w}{h}".encode()).hexdigest()[:12]
        out = os.path.join(CACHE, f"z{key}.jpg")
        if not os.path.exists(out):
            c = im.crop((int(x0 * W_), int(y0 * H_), int(x1 * W_), int(y1 * H_)))
            c = c.resize((w * 2, int(c.height * w * 2 / c.width)), Image.LANCZOS)
            c.save(out, quality=92)
        if h is None:
            cw, chh = (x1 - x0) * W_, (y1 - y0) * H_
            h = int(w * chh / cw)
        s = self.s
        sticker = (f'<span class="ltr" style="position:absolute;right:24px;bottom:24px;width:80px;height:80px;border-radius:40px;'
                   f'background:{s["nb"]};color:{s["nf"]};display:flex;align-items:center;justify-content:center;font-size:38px;font-weight:800">{badge}</span>'
                   if badge else "")
        return (f'<div class="z" style="width:{w}px;height:{h}px;flex-shrink:0;position:relative;border-radius:26px;overflow:hidden;'
                f'background:#fff {url(out)} top center/100% auto no-repeat;box-shadow:0 22px 46px rgba(0,0,0,.25)">{sticker}</div>')

    # ---- slides
    def cover(self, chip, title, visual, line, size=84, swipe=True):
        body = (self.head(chip, 1) + spacer(40)
                + f'<h1 style="font-size:{size}px;line-height:1.22">{title}</h1>' + spacer(36)
                + visual + spacer(34)
                + f'<p style="font-size:36px;font-weight:600;line-height:1.55">{line}</p>'
                + GROW + self.bot(last=not swipe))
        return self.pg(body)

    def visual(self, i, chip, visual, title, text, gap=40):
        """Any visual (band, sheets, crop) with a one-line title and a line of 'why'."""
        body = (self.head(chip, i) + spacer(34) + visual + spacer(gap)
                + f'<h1 style="font-size:70px;line-height:1.25">{title}</h1>'
                + (f'<p class="dim" style="font-size:34px;font-weight:400;line-height:1.6;margin-top:16px;text-wrap:pretty">{text}</p>' if text else "")
                + GROW + self.bot(single=self.n is None))
        return self.pg(body)

    def points(self, i, chip, title, items, intro=None, big=None, last=False):
        """Numbered cards: items = [(title, sub), ...]."""
        cards = ""
        for k, (t, sub) in enumerate(items, 1):
            cards += (f'<div class="card z" style="display:flex;gap:26px;align-items:flex-start;padding:30px 34px">'
                      f'{self.num(k, 60)}<div><div style="font-size:38px;font-weight:800;line-height:1.35">{t}</div>'
                      + (f'<div style="font-size:32px;font-weight:400;line-height:1.55;margin-top:8px;opacity:.82">{sub}</div>' if sub else "")
                      + '</div></div>')
        body = (self.head(chip, i) + spacer(56)
                + (big or "")
                + f'<h1 style="font-size:70px;line-height:1.25">{title}</h1>'
                + (f'<p class="dim" style="font-size:34px;line-height:1.6;margin-top:16px">{intro}</p>' if intro else "")
                + spacer(40) + f'<div style="display:flex;flex-direction:column;gap:20px">{cards}</div>'
                + GROW + self.bot(last=last))
        return self.pg(body)

    def lesson(self, i, chip, k, title, text, example=None, example_label="مثال", visual=None):
        """One step of a lesson: big step number, title, explanation, and an example card (or any visual)."""
        s = self.s
        ex = ""
        if example:
            ex = (f'<div class="card z" style="padding:34px 38px;margin-top:40px">'
                  f'<div style="font-size:28px;font-weight:700;color:{TE if s["card"] != TE else DK};margin-bottom:10px">{example_label}</div>'
                  f'<div style="font-size:36px;font-weight:600;line-height:1.6">{example}</div></div>')
        body = (self.head(chip, i) + GROW
                + f'<div class="z ltr" style="font-size:150px;font-weight:800;line-height:1;color:{s["acc"] if s["bg"] != DK else MU};opacity:.9;text-align:right">{k}</div>'
                + spacer(26) + f'<h1 style="font-size:70px;line-height:1.25">{title}</h1>'
                + f'<p class="dim" style="font-size:36px;line-height:1.6;margin-top:20px;text-wrap:pretty">{text}</p>'
                + ex + (spacer(36) + visual if visual else "")
                + GROW + self.bot())
        return self.pg(body)

    def closing(self, chip, title, text, next_ep=None, save="احفظ المنشور، وأرسله لصاحب مشروع جديد.", visual="", title_size=76):
        s = self.s
        d1, d2, _ = s["deco"]
        nxt = ""
        if next_ep:
            label, name = next_ep
            nb, nf = (DK, CH) if s["bg"] != DK else (CH, DK)
            nxt = (f'<div class="z" style="background:{nb};color:{nf};border-radius:36px;padding:36px 44px">'
                   f'<div style="font-size:30px;font-weight:700;margin-bottom:10px;color:{TE if nb == DK else TE}">{label}</div>'
                   f'<div style="font-size:46px;font-weight:800;line-height:1.4">{name}</div></div>' + spacer(34))
        body = (self.head(chip, self.n or 1)
                + deco(f"left:-110px;top:120px;width:270px;height:270px;border-radius:135px;background:{d1};opacity:.9")
                + deco(f"left:170px;top:300px;width:80px;height:80px;border-radius:40px;background:{d2}")
                + spacer(50 if visual else 110)
                + f'<h1 style="font-size:{title_size}px;line-height:1.35">{title}</h1>' + spacer(24)
                + f'<p style="font-size:36px;line-height:1.6">{text}</p>'
                + visual + GROW + nxt
                + (f'<p style="font-size:32px;font-weight:600;line-height:1.6">{save}</p>' + spacer(44) if save else "")
                + bottom(right_html=self.logo(250)))
        return self.pg(body)

    def single(self, chip, visual, title, text, ask=None, gap=36, title_size=76):
        """A one-image post: chip, the picture, a title, a line, and a question for the comments."""
        a = ""
        if ask:
            a = (f'<div class="z" style="display:flex;align-items:center;gap:18px;margin-top:22px;font-size:34px;font-weight:700;line-height:1.5">'
                 f'<span style="flex-shrink:0;width:16px;height:16px;border-radius:8px;background:{self.s["acc"] if self.s["bg"] != DK else MU}"></span>{ask}</div>')
        body = (self.head(chip, 1) + spacer(34) + visual + spacer(gap)
                + f'<h1 style="font-size:{title_size}px;line-height:1.22">{title}</h1>'
                + (f'<p class="dim" style="font-size:34px;line-height:1.6;margin-top:14px;text-wrap:pretty">{text}</p>' if text else "")
                + a + GROW + bottom(right_html=self.logo(250)))
        return self.pg(body)


# ------------------------------------------------------------------ build + checks
CHECK_JS = """() => { const S = document.querySelector('.s').getBoundingClientRect(), out = [];
  document.querySelectorAll('svg.wm').forEach((e, i) => { const r = e.getBoundingClientRect();
    const d = [r.left - S.left, S.right - r.right, r.top - S.top, S.bottom - r.bottom];
    if (Math.min(...d) < 40) out.push('logo ' + i + ' margins px ' + d.map(v => v.toFixed(0)).join(', ')); });
  const bot = document.querySelector('.bot').getBoundingClientRect();
  document.querySelectorAll('h1, p, .card').forEach(e => { const r = e.getBoundingClientRect();
    if (r.bottom > bot.top - 8) out.push('runs into the bottom bar: ' + e.textContent.trim().slice(0, 30)); });
  const w = document.createTreeWalker(document.querySelector('.s'), NodeFilter.SHOW_TEXT);
  while (w.nextNode()) { const n = w.currentNode; if (!n.textContent.trim()) continue; const el = n.parentElement;
    if (el.closest('svg')) continue; const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs < 24) out.push('text ' + fs + 'px: ' + n.textContent.trim().slice(0, 20)); }
  return out; }"""


async def _check(here, n):
    from playwright.async_api import async_playwright
    bad = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for i in range(1, n + 1):
            await pg.goto("file://" + os.path.join(here, f"slide-{i}.html"))
            await pg.evaluate("document.fonts.ready")
            bad += [f"slide {i}: {r}" for r in await pg.evaluate(CHECK_JS)]
        await b.close()
    return bad


def build(here, slides, caption=None):
    blob = " ".join(slides) + (caption or "")
    bad = [w for w in FORBIDDEN if w in blob]
    if bad:
        raise SystemExit(f"forbidden words: {bad}")
    _render_slides(here, slides)
    bad = asyncio.run(_check(here, len(slides)))
    if bad:
        print("CHECK FAILED:", *bad, sep="\n  ")
        sys.exit(1)
    print("check ok:", len(slides), "slides")
