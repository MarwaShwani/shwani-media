"""The whole identity on one desk, seen from above (post 12 «أعمالنا 3: هويتنا كاملة في صورة», Marwa, 28 Oct 2026).

Scene: scenes/desk-flatlay-blank.jpg, a blank top-down flat lay made with Gemini in Marwa's account on 28 Oct
(every paper item plain white, a black folded T-shirt, a phone with a black screen). The exact print files from
out/png are laid on each item with mockup.multiply (the paper keeps the photo's light and texture), the chest print
goes on the T-shirt as opaque ink, and the phone shows the Instagram profile.

The badge in the scene is landscape (clip at the top centre), so a landscape version of the ID badge is drawn here
from the same parts as stationery.id_badge (charcoal band with the logo, the name block, terracotta foot).

    python3 brand/flatlay.py        # -> out/mockups/17-desk-flatlay.jpg (+ ITEMS centres for the post's numbers)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mockup import *  # noqa: F401,F403
from kit import Piece, render, logo, word, pattern, DK, CH, TE, MU, GREY, OWNER_AR, ROLE_AR, OWNER_EN, OUT  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SCENE = os.path.join(HERE, "scenes", "desk-flatlay-blank.jpg")
PNG = os.path.join(OUT, "png")
MOCK = os.path.join(OUT, "mockups")


def badge_landscape():
    panel = "#F8F3EA"
    body = (
        f'<div class="abs" style="left:-3mm;right:-3mm;top:-3mm;height:23mm;background:{DK};{pattern(16, CH, TE, CH, MU, .12)}"></div>'
        f'<div class="abs" style="left:5.5mm;top:7.2mm">{logo("25mm", CH, TE)}</div>'
        f'<div class="abs" style="right:5.5mm;top:8.6mm;font-size:3.1mm;font-weight:600;color:{CH}">بطاقة تعريف</div>'
        f'<div class="abs" style="left:-3mm;right:-3mm;top:20mm;bottom:-3mm;background:{panel}"></div>'
        f'<div class="abs" style="left:6mm;top:24.6mm;width:19mm;height:19mm;border-radius:50%;background:{CH};'
        f'display:flex;align-items:center;justify-content:center">{word("14mm", DK, TE)}</div>'
        f'<div class="abs" style="right:6mm;top:24.4mm;text-align:right">'
        f'<div style="font-size:5.3mm;font-weight:700;line-height:1.3">{OWNER_AR}</div>'
        f'<div style="font-size:4mm;font-weight:600;color:{TE};line-height:1.4">{ROLE_AR}</div>'
        f'<div class="en" style="font-size:2.9mm;color:{GREY};margin-top:.6mm">{OWNER_EN}</div></div>'
        f'<div class="abs" style="left:-3mm;right:-3mm;top:48.5mm;bottom:-3mm;background:{TE}"></div>'
    )
    return Piece("id-badge-86x54-landscape", 86, 54, body, bg=DK, fg=DK)


def Q(*pts):
    return np.float32(pts)


# (art, quad TL TR BR BL as the art reads, how) ; quads measured on the 1856x2304 scene, then snapped to the edges
LAYERS = [
    ("letterhead-a4-sample", Q((153, 171), (652, 171), (651, 886), (153, 885)), "paper"),
    ("envelope-dl-back", Q((724, 171), (1295, 171), (1295, 452), (724, 452)), "paper"),
    ("business-card-front", Q((719, 516), (974, 511), (976, 668), (719, 670)), "paper"),
    ("business-card-back", Q((1041, 535), (1293, 535), (1294, 680), (1041, 680)), "paper"),
    ("brochure-trifold-outside", Q((154, 958), (649, 957), (650, 1314), (157, 1314)), "paper"),
    ("notebook-cover-a5", Q((724, 756), (1108, 756), (1108, 1310), (724, 1310)), "paper"),
    ("folder-a4-cover", Q((1187, 745), (1700, 745), (1700, 1402), (1187, 1402)), "paper"),
    ("id-badge-86x54-landscape", Q((154, 1581), (395, 1581), (395, 1740), (154, 1740)), "badge"),
    ("giftbox-lid-200x200", Q((722, 1386), (1063, 1385), (1063, 1724), (722, 1724)), "paper"),
    ("tee-front-chest-100x40", Q((1328, 1690), (1548, 1690), (1548, 1778), (1328, 1778)), "fabric"),
    ("asset:phone-profile.png", None, "screen"),
]

# where the post puts its numbers (scene px): one per piece, on a corner that has no logo under it
ITEMS = [("الورق الرسمي", (153, 171)), ("الظرف", (724, 171)), ("بطاقة العمل", (719, 516)), ("البروشور", (154, 958)),
         ("الدفتر", (724, 756)), ("الملف", (1187, 745)), ("بطاقة الموظف", (154, 1740)), ("علبة الهدايا", (1063, 1386)),
         ("التيشيرت", (1172, 1505)), ("صفحة انستغرام", (728, 1960))]


def art(name):
    if name.startswith("asset:"):
        return imread(os.path.join(HERE, "assets", name[6:]))
    return imread(os.path.join(PNG, name + ".png"))


def screen(scene, img, box=(470, 1780, 670, 2140), dark=48, radius=26):
    """The phone's black glass: found as the dark region inside the phone, then filled with the screenshot.
    The glass reflection of the photo is added back on top so it still reads as glass."""
    x0, y0, x1, y1 = box
    roi = cv2.cvtColor(scene[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY)
    m = (roi < dark).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    x, y, w, h = st[k, :4]
    X0, Y0 = x0 + x + 3, y0 + y + 3
    W, H = w - 6, h - 6
    fit = cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32)
    mask = np.zeros((H, W), np.uint8)
    cv2.rectangle(mask, (radius, 0), (W - radius, H), 255, -1)
    cv2.rectangle(mask, (0, radius), (W, H - radius), 255, -1)
    for cx, cy in ((radius, radius), (W - radius, radius), (radius, H - radius), (W - radius, H - radius)):
        cv2.circle(mask, (cx, cy), radius, 255, -1)
    mask = cv2.GaussianBlur(mask.astype(np.float32) / 255, (0, 0), 1.0)[..., None]
    glass = scene[Y0:Y0 + H, X0:X0 + W].astype(np.float32)
    glare = np.clip(glass - np.percentile(glass, 5), 0, 255) * .55
    out = np.clip(fit * .96 + glare, 0, 255)
    scene = scene.copy()
    scene[Y0:Y0 + H, X0:X0 + W] = np.clip(glass * (1 - mask) + out * mask, 0, 255).astype(np.uint8)
    return scene


def build():
    render([badge_landscape()], pdf=False)
    im = imread(SCENE)
    base = im.copy()
    for name, quad, how in LAYERS:
        img = art(name)
        if how == "screen":
            im = screen(im, img)
            continue
        if how == "fabric":
            im = print_on_fabric(im, imread_rgba(os.path.join(PNG, name + ".png")), quad, opacity=.95, contrast=.7, shade_src=base)
            continue
        quad = refine_quad(base, quad, search=8)
        keep = None
        if how == "badge":     # the metal clip and its slot stay in front of the print
            hsv = cv2.cvtColor(base, cv2.COLOR_BGR2HSV)
            keep = ((hsv[..., 1] < 60) & (hsv[..., 2] > 150)).astype(np.float32)
            keep = cv2.GaussianBlur(cv2.erode(keep, np.ones((3, 3), np.uint8)), (0, 0), 1.0)
        im = multiply(im, img, quad, shade_src=base, keep=keep)
    os.makedirs(MOCK, exist_ok=True)
    out = os.path.join(MOCK, "17-desk-flatlay.jpg")
    cv2.imwrite(out, im, [cv2.IMWRITE_JPEG_QUALITY, 93])
    print("mockup", out)
    return out


if __name__ == "__main__":
    build()
