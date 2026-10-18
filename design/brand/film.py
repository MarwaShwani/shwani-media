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

MOCKS = ["05-storefront", "01-business-cards", "02-stationery", "07-company-profile", "04-rollup", "12-tshirts",
         "14-mugs", "09-packaging", "13-outdoor-banner", "10-screens"]


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


def main():
    tmp = os.path.join(OUT, "film")
    os.makedirs(tmp, exist_ok=True)
    bridge = load("shwani-bridge-symbol-cream", 300)
    logo = load("shwani-logo-cream", 900)
    tag = render_text_png(f'<div style="width:1920px;text-align:center;color:rgb{CH};font-size:54px;font-weight:700">نبني الجسر بين فكرتك والنتيجة</div>',
                          os.path.join(tmp, "tag.png"), 1920, 90)
    contact = render_text_png('<div style="width:1920px;text-align:center;color:rgba(242,233,216,.8);font-size:34px;font-weight:400;line-height:1.8">'
                              '<span dir="ltr">shwanicompany@gmail.com</span><br><span dir="ltr">shwanicompany</span> · انستغرام · فيسبوك</div>',
                              os.path.join(tmp, "contact.png"), 1920, 140)
    caps = {}
    labels = {"05-storefront": "لافتة الواجهة", "01-business-cards": "بطاقة العمل", "02-stationery": "الأوراق الرسمية",
              "07-company-profile": "الملف التعريفي", "04-rollup": "الرول أب", "12-tshirts": "التيشيرت",
              "14-mugs": "الأكواب", "09-packaging": "التغليف", "13-outdoor-banner": "البنر الخارجي", "10-screens": "الشاشات"}
    for m in MOCKS:
        caps[m] = render_text_png(f'<div style="display:inline-block;margin:0 0 0 0;padding:14px 34px;border-radius:40px;background:rgba(32,33,38,.82);'
                                  f'color:rgb{CH};font-size:36px;font-weight:600">{labels[m]}</div>', os.path.join(tmp, f"cap-{m}.png"), 700, 100)
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
    # 2) mockups with slow push-in and cross-fade (2.2 s each)
    seg, fade = 2.2, .35
    t0 = 3.6
    prev = None
    for k, m in enumerate(MOCKS):
        src = Image.open(os.path.join(OUT, "mockups", m + ".jpg")).convert("RGB")
        sw, sh_ = src.size
        k0 = max(W / sw, H / sh_)
        base = src.resize((int(sw * k0 * 1.12), int(sh_ * k0 * 1.12)), Image.LANCZOS)
        cues.append((t0 + k * seg, "paper"))
        nn = int(seg * FPS)
        for i in range(nn):
            p = i / nn
            z = 1.12 - .1 * p
            cw, chh = int(W * z / 1.12 * base.size[0] / (W * 1.0) * (W / base.size[0]) * 1.12), 0
            # crop window that shrinks toward the centre
            ww, hh = int(base.size[0] / z * 1.0), int(base.size[1] / z)
            ww, hh = min(ww, base.size[0]), min(hh, base.size[1])
            x0, y0 = (base.size[0] - ww) // 2, (base.size[1] - hh) // 2
            fr = base.crop((x0, y0, x0 + ww, y0 + hh)).resize((W, H), Image.BILINEAR)
            if prev is not None and i < fade * FPS:
                fr = Image.blend(prev, fr, i / (fade * FPS))
            cap = caps[m]
            fr = fr.convert("RGBA")
            ca = ease((i - 6) / 10)
            c2 = cap.copy()
            c2.putalpha(c2.getchannel("A").point(lambda v: int(v * ca)))
            fr.paste(c2, (W - 700 - 70, H - 160), c2)
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
