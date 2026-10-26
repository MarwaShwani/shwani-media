"""Short brand film (1920x1080, ~24 s): the bridge builds itself, the logo appears, then the real-world mockups.
Sounds are the real recordings in design/sfx (soft whoosh, paper). Run: python3 brand/film.py"""
import os, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
SFX = os.path.join(os.path.dirname(HERE), "sfx")
W, H, FPS = 1920, 1080, 30
DK, CH, TE = (32, 33, 38), (242, 233, 216), (224, 122, 71)
FONT = os.path.join(os.path.dirname(HERE), "node_modules", "@fontsource", "alexandria", "files")

# 26 Oct (Marwa): no storefront; portrait photos (roll-up, tote) were cropped to 16:9 and lost their design,
# so every mockup is now shown whole (fitted, never cropped) over a blurred, darkened copy of itself.
MOCKS = ["01-business-cards", "02-stationery", "07-company-profile", "03-flyer", "04-rollup", "13-outdoor-banner",
         "12-tshirts", "11-tote", "14-mugs", "09-packaging", "08-notebook", "16-executive-pen", "10-screens"]
LABELS = {"01-business-cards": "بطاقة العمل", "02-stationery": "الأوراق الرسمية", "03-flyer": "الفلاير",
          "07-company-profile": "الملف التعريفي", "04-rollup": "الرول أب", "12-tshirts": "التيشيرت",
          "14-mugs": "الأكواب", "11-tote": "الحقيبة", "09-packaging": "التغليف",
          "16-executive-pen": "القلم التنفيذي وطقم الهدية", "08-notebook": "الدفتر والقلم التنفيذي",
          "13-outdoor-banner": "البنر الخارجي", "10-screens": "الشاشات"}
BOX_W, BOX_H = 1700, 900      # the whole photo fits inside this box, centred a little above the middle



def ease(t):
    t = min(max(t, 0), 1)
    return 1 - (1 - t) ** 3


def load(name, w):
    im = Image.open(os.path.join(OUT, "logo", "png", name + ".png")).convert("RGBA")
    return im.resize((w, int(im.size[1] * w / im.size[0])), Image.LANCZOS)


def text_img(s, size, color, weight="700"):
    # render Arabic through Chromium-free path: use a pre-rendered PNG from playwright
    return None


def render_text_png(html, path, w, h):
    import asyncio
    from playwright.async_api import async_playwright
    fl = "".join(f'<link rel="stylesheet" href="file://{os.path.dirname(FONT)}/{x}.css">' for x in (400, 600, 700))
    doc = f'<html dir="rtl"><head>{fl}<style>body{{margin:0;background:transparent;font-family:Alexandria}}</style></head><body>{html}</body></html>'

    async def go():
        async with async_playwright() as p:
            b = await p.chromium.launch()
            pg = await b.new_page(viewport={"width": w, "height": h})
            src = path[:-4] + ".html"
            open(src, "w", encoding="utf-8").write(doc)
            await pg.goto("file://" + src)
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=path, omit_background=True)
            await b.close()
    asyncio.run(go())
    return Image.open(path).convert("RGBA")


_MASKS = {}


def rounded_mask(w, h, r):
    key = (w, h, r)
    if key not in _MASKS:
        m = Image.new("L", (w * 2, h * 2), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, w * 2 - 1, h * 2 - 1), r * 2, fill=255)
        _MASKS[key] = m.resize((w, h), Image.LANCZOS)
    return _MASKS[key]


def gallery_layers(src):
    """Background (blurred, darkened cover crop), the fitted photo, and a soft shadow mask."""
    from PIL import ImageFilter
    sw, sh_ = src.size
    kc = max(W / sw, H / sh_)
    cov = src.resize((int(sw * kc) + 2, int(sh_ * kc) + 2), Image.BILINEAR)
    x0, y0 = (cov.size[0] - W) // 2, (cov.size[1] - H) // 2
    cov = cov.crop((x0, y0, x0 + W, y0 + H)).filter(ImageFilter.GaussianBlur(38))
    bg = Image.blend(cov, Image.new("RGB", (W, H), DK), .62)
    kf = min(BOX_W / sw, BOX_H / sh_)
    fg = src.resize((int(sw * kf), int(sh_ * kf)), Image.LANCZOS)
    sm = Image.new("L", (fg.size[0] + 120, fg.size[1] + 120), 0)
    ImageDraw.Draw(sm).rounded_rectangle((60, 60, fg.size[0] + 60, fg.size[1] + 60), 24, fill=150)
    return bg, fg, sm.filter(ImageFilter.GaussianBlur(26))


def main():
    tmp = os.path.join(OUT, "film")
    os.makedirs(tmp, exist_ok=True)
    bridge = load("shwani-word-cream", 640)
    logo = load("shwani-logo-cream", 900)
    tag = render_text_png(f'<div style="width:1920px;text-align:center;color:rgb{CH};font-size:54px;font-weight:700">نبني الجسر بين فكرتك والنتيجة</div>',
                          os.path.join(tmp, "tag.png"), 1920, 90)
    contact = render_text_png('<div style="width:1920px;text-align:center;color:rgba(242,233,216,.8);font-size:34px;font-weight:400;line-height:1.8">'
                              '<span dir="ltr">shwanicompany@gmail.com</span><br><span dir="ltr">shwanicompany</span> · انستغرام · فيسبوك</div>',
                              os.path.join(tmp, "contact.png"), 1920, 140)
    caps = {}
    for m in MOCKS:
        c = render_text_png(f'<div style="display:inline-block;padding:14px 34px;border-radius:40px;background:rgba(32,33,38,.86);'
                            f'color:rgb{CH};font-size:36px;font-weight:600;white-space:nowrap">{LABELS[m]}</div>',
                            os.path.join(tmp, f"cap-{m}.png"), 900, 100)
        caps[m] = c.crop(c.getbbox())
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", os.path.join(tmp, "video.mp4")], stdin=subprocess.PIPE)
    cues = []

    def emit(im):
        ff.stdin.write(np.asarray(im.convert("RGB")).tobytes())

    # 1) intro: the bridge, then the logo (3.6 s)
    n = int(3.6 * FPS)
    cues.append((0.25, "whoosh"))
    cues.append((1.55, "whoosh"))
    for i in range(n):
        t = i / FPS
        f = Image.new("RGB", (W, H), DK)
        a1 = ease((t - .2) / .5) * (1 - ease((t - 1.4) / .4))
        if a1 > 0:
            s = .7 + .3 * ease((t - .2) / .6)
            b = bridge.resize((int(bridge.size[0] * s), int(bridge.size[1] * s)))
            b.putalpha(b.getchannel("A").point(lambda v: int(v * a1)))
            f.paste(b, ((W - b.size[0]) // 2, (H - b.size[1]) // 2 - 40), b)
        a2 = ease((t - 1.5) / .6)
        if a2 > 0:
            lg = logo.copy()
            lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a2)))
            f.paste(lg, ((W - lg.size[0]) // 2, 330 + int(30 * (1 - a2))), lg)
            tg = tag.copy()
            a3 = ease((t - 2.2) / .6)
            tg.putalpha(tg.getchannel("A").point(lambda v: int(v * a3)))
            f.paste(tg, (0, 760), tg)
        emit(f)
    # 2) mockups, each shown whole: blurred copy behind, the photo fitted on top with a slow push-in (2.4 s each)
    seg, fade = 2.4, .4
    t0 = 3.6
    prev = None
    for k, m in enumerate(MOCKS):
        src = Image.open(os.path.join(OUT, "mockups", m + ".jpg")).convert("RGB")
        bg, fg, shadow = gallery_layers(src)
        cues.append((t0 + k * seg, "paper"))
        nn = int(seg * FPS)
        cap = caps[m]
        for i in range(nn):
            p = i / (nn - 1)
            z = 1.0 + .035 * p                       # gentle push-in, the photo stays whole
            fw, fh = int(fg.size[0] * z), int(fg.size[1] * z)
            x, y = (W - fw) // 2, (H - fh) // 2 - 30
            fr = bg.copy()
            sh_ = shadow.resize((fw + 120, fh + 120), Image.BILINEAR)
            fr.paste((0, 0, 0), (x - 60, y - 40), sh_)
            fr.paste(fg.resize((fw, fh), Image.BILINEAR), (x, y), rounded_mask(fw, fh, 18))
            if prev is not None and i < fade * FPS:
                fr = Image.blend(prev, fr, ease(i / (fade * FPS)))
            fr = fr.convert("RGBA")
            ca = ease((i - 6) / 10)
            c2 = cap.copy()
            c2.putalpha(c2.getchannel("A").point(lambda v: int(v * ca)))
            fr.paste(c2, (x + fw - cap.size[0] - 28, y + fh - cap.size[1] // 2), c2)
            fr = fr.convert("RGB")
            emit(fr)
        prev = fr
    # 3) end card (3.4 s)
    t_end = t0 + len(MOCKS) * seg
    cues.append((t_end + .1, "whoosh"))
    n = int(3.4 * FPS)
    for i in range(n):
        t = i / FPS
        f = Image.new("RGB", (W, H), DK)
        a = ease(t / .5)
        lg = logo.copy()
        lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
        f.paste(lg, ((W - lg.size[0]) // 2, 250), lg)
        ct = contact.copy()
        a2 = ease((t - .5) / .6)
        ct.putalpha(ct.getchannel("A").point(lambda v: int(v * a2)))
        f.paste(ct, (0, 720), ct)
        if prev is not None and i < 10:
            f = Image.blend(prev, f, i / 10)
        emit(f)
    ff.stdin.close()
    ff.wait()
    total = t_end + 3.4
    # sound: soft whoosh and paper, quiet (peak about -10 dBFS)
    files = {"whoosh": os.path.join(SFX, "whoosh_soft.wav"), "paper": os.path.join(SFX, "paper_slide.wav")}
    inputs, filt = [], []
    for j, (t, kind) in enumerate(cues):
        inputs += ["-i", files[kind] if kind == "whoosh" else os.path.join(SFX, f"paper_slide_{j % 4 + 1}.wav")]
        filt.append(f"[{j}:a]adelay={int(t * 1000)}|{int(t * 1000)},volume={.5 if kind == 'whoosh' else .35}[a{j}]")
    mix = "".join(f"[a{j}]" for j in range(len(cues))) + f"amix=inputs={len(cues)}:normalize=0,apad,atrim=0:{total:.2f},alimiter=limit=0.32[aout]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt) + ";" + mix, "-map", "[aout]",
                    os.path.join(tmp, "audio.wav")], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(tmp, "video.mp4"), "-i", os.path.join(tmp, "audio.wav"),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", os.path.join(OUT, "SHWANI-brand-film.mp4")], check=True)
    print("film", total)


if __name__ == "__main__":
    main()
