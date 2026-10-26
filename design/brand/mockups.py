"""Build the photographic mockups: exact artwork from out/png placed on blank Gemini scenes.
Corners are measured once on each blank scene (TL, TR, BR, BL of the artwork as it should read)
and snapped to the paper edges with refine_quad. Run: python3 brand/mockups.py [names...]"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mockup import *  # noqa: F401,F403

HERE = os.path.dirname(os.path.abspath(__file__))
SCN = os.path.join(HERE, "scenes")
PNG = os.path.join(HERE, "out", "png")
MOCK = os.path.join(HERE, "out", "mockups")


def art(name):
    if name.startswith("#"):
        c = name.lstrip("#")
        bgr = [int(c[i:i + 2], 16) for i in (4, 2, 0)]
        return np.full((64, 64, 3), bgr, np.uint8)
    if name.startswith("asset:"):
        return imread(os.path.join(HERE, "assets", name[6:]))
    return imread(os.path.join(PNG, name + ".png"))


def Q(pts, k=1.0):
    return np.float32(pts) * k


# each mockup: scene, list of (artwork, quad, options) painted in order (lowest first)
MOCKUPS = {
    "01-business-cards": ("cards-wood-blank.jpg", [
        ("business-card-front", Q([(396.6, 731.3), (1290.9, 375.8), (1601.5, 635.8), (698.4, 987.5)]), {}),
        ("business-card-back", Q([(1044.1, 872.0), (1903.4, 509.1), (2251.8, 1023.0), (1395.1, 1435.9)]), {}),
    ]),
    "02-stationery": ("stationery-flatlay-blank.jpg", [
        ("mock-quotation-letter", Q([(419.4, 538.0), (1212.1, 317.6), (1499.7, 1367.6), (707.0, 1588.0)]), {}),
        ("mock-letterhead-letter", Q([(913.0, 549.8), (1670.8, 549.8), (1677.7, 1538.8), (916.5, 1544.1)]), {}),
        ("envelope-dl-front", Q([(1176.9, 166.4), (2024.0, 169.4), (2024.0, 576.7), (1178.3, 576.7)]), {}),
        ("mock-card-front-166", Q([(1754.7, 487.8), (2120.2, 485.3), (2123.2, 698.5), (1757.7, 702.3)]), {}),
    ]),
    "03-flyer": ("flyer-marble-blank.jpg", [
        ("flyer-a5", Q([(550.7, 584.5), (1347.1, 391.2), (1997.2, 1231.8), (1018.3, 1559.2)]), {}),
    ]),
    "04-rollup": ("rollup-hall-blank.jpg", [
        ("rollup-85x200cm-scale-1-10", Q([(528.8, 342.4), (1221.7, 323.1), (1204.2, 2012.9), (514.3, 2008.7)]), {}),
    ]),
    # "05-storefront" removed: Marwa, 19 Oct, no outside-office photo in any design
    "06-brochure": ("brochure-blank.jpg", [
        ("mock-brochure-inside-245", Q([(627.7, 225.8), (1138, 245), (1113, 1479), (633.2, 1467.7)]), {"crop": (0, 0, 1/3, 1)}),
        ("mock-brochure-inside-245", Q([(1138, 245), (1645, 257), (1630, 1490), (1113, 1479)]), {"crop": (1/3, 0, 2/3, 1)}),
        ("mock-brochure-inside-245", Q([(1645, 257), (2148, 262.3), (2142.5, 1505.9), (1630, 1490)]), {"crop": (2/3, 0, 1, 1)}),
        ("mock-brochure-outside-234", Q([(174.4, 476.7), (648.7, 338.7), (905.4, 1493.4), (417.4, 1645.3)]), {"crop": (0, 0, 1/3, 1)}),
    ]),
    "07-company-profile": ("profile-desk-blank.jpg", [
        ("profile-01-cover", Q([(187.3, 425.6), (874.4, 414.4), (932.6, 1366.0), (171.8, 1406.9)]), {}),
        ("profile-05-cv-academic-tech", Q([(965.6, 413.0), (1623.0, 385.0), (1753.0, 1342.0), (1024.0, 1385.1)]), {}),
        ("profile-04-design", Q([(1623.0, 385.0), (2238.0, 352.9), (2440.2, 1287.6), (1750.9, 1326.5)]), {}),
    ]),
    # 26 Oct (Marwa): the notebook with the executive pen (black lacquer, gold trim) instead of a plain pen.
    # New Gemini scene: a blank charcoal cover, so the cover art takes the photo's light (on_dark), and SHWANI is
    # engraved in gold on the pen barrel.
    "08-notebook": ("notebook-pen-blank.jpg", [
        ("notebook-cover-a5", Q([(217, 810), (962, 562), (1732, 1110), (905, 1500)]), {"dark": True, "refine": {"search": 14}}),
        ("pen-engrave-40x9", "pen-barrel-nb", {"metal": {"contrast": .55, "lo": .8, "hi": 1.6, "sheen": .15}}),
    ]),
    "09-packaging": ("packaging-b-blank.jpg", [
        ("#F2E9D8", Q([(345, 935), (700, 1112), (705, 1330), (360, 1172)]), {}),
        ("#F2E9D8", Q([(700, 1112), (1180, 940), (1178, 1125), (705, 1330)]), {}),
        ("#202126", Q([(325.2, 850.5), (698.3, 1026.4), (700, 1112), (345, 935)]), {}),
        ("#202126", Q([(698.3, 1026.4), (1185.0, 860.9), (1180, 940), (700, 1112)]), {}),
        ("giftbox-lid-200x200", Q([(325.2, 850.5), (810.1, 686.9), (1185.0, 860.9), (698.3, 1026.4)]), {}),
        ("paper-bag-side-240x320", Q([(1313.7, 397.8), (1909.7, 554.5), (1810.7, 1430.4), (1246.5, 1211.4)]), {}),
        ("sticker-sheet-a6", Q([(1178.3, 1271.2), (1540.3, 1389.0), (1221.6, 1670.7), (850.0, 1533.1)]), {}),
    ]),
    "10-screens": ("laptop-phone-blank.jpg", [
        ("asset:laptop-screen.png", Q([(579.0, 443.9), (1403.4, 364.6), (1500.2, 924.2), (690.0, 1103.2)]), {}),
        ("asset:phone-profile.png", Q([(1592.1, 692.8), (1857.2, 665.9), (1971.5, 1232.2), (1702.4, 1285.3)]), {}),
    ]),
    # the left mug carries the SHWANI word and the line (26 Oct, was the big H); the right mug's logo is unchanged
    "14-mugs": ("mugs-blank.jpg", [
        ("mug-wrap-200x85", None, {"mug": dict(x0=544, x1=1200, y_top=527, y_bot=1302, e_top=40, e_bot=45, a0=-.0075, a1=.508)}),
    ]),
    "13-outdoor-banner": ("billboard-blank.jpg", [
        ("outdoor-banner-300x100cm-scale-1-10", Q([(662.3, 383.8), (1676.5, 545.3), (1685.2, 911.5), (661.7, 827.0)]), {}),
    ]),
    "15-folder-badge": ("folder-badge-blank.jpg", [
        ("folder-a4-cover", Q([(692.3, 401.4), (1744.3, 250.0), (2209.3, 1063.3), (1050.4, 1407.9)]), {}),
        ("id-badge-54x86", Q([(719.9, 985.6), (1068.3, 881.9), (1294.8, 1318.8), (940.7, 1455.4)]), {}),
    ]),
    # 26 Oct (Marwa): the executive pen in a businesswoman's hand, signing on the SHWANI letterhead, with the gift box
    # (pen groove and metal card holder) beside it. Scene: Gemini, blank; the brand mark on the cap finial is painted out.
    "16-executive-pen": ("exec-signing-blank.jpg", [
        ("letterhead-a4-sample", Q([(462.5, 568.6), (1287.1, 614.7), (1124.6, 1398.0), (140.8, 1336.6)]),
         {"keep": {"sat": 16, "vmin": 150, "exclude": [[(1140, 1290), (1460, 1230), (1460, 1520), (1140, 1520)]]}}),
        ("mock-lid-logo-white", Q([(1944, 401), (2156, 513), (2156, 609), (1944, 497)]), {"white": (255, 255, 255)}),
        ("cardholder-engrave-60x24", Q([(1815, 645), (2105, 828), (1935, 928), (1648, 732)]),
         {"metal": {"contrast": .5, "lo": .7, "hi": 1.25, "sheen": .08, "emboss": .35}, "sub": (.185, .19, .815, .58)}),
        ("pen-engrave-40x9", "pen-cap", {"metal": {"contrast": .55, "lo": .8, "hi": 1.6, "sheen": .15}}),
    ], {"paint": [((1710, 1280, 1752, 1318), (1712, 1283))]}),
    "11-tote": ("tote-chair-blank.jpg", [
        ("tote-print-280x330", Q([(519, 1015), (1333, 980), (1400, 1976), (549, 2052)]),
         {"sub": (.12, .08, .88, .9), "white": (255, 255, 255)}),
    ]),
    "12-tshirts": ("tees-hanger-blank.jpg", [
        ("tee-front-chest-100x40", Q([(545, 610), (805, 610), (805, 714), (545, 714)]), {"fabric": True, "contrast": .7, "opacity": .96}),
        ("tee-back-300x340", Q([(1672, 560), (2028, 560), (2028, 963), (1672, 963)]), {"fabric": True, "contrast": .7, "opacity": .96}),
    ]),
}


def along(c, a, length, height):
    """Quad of a strip centred on c, running along unit vector a (text reads along a), in scene pixels."""
    c, a = np.float32(c), np.float32(a) / np.linalg.norm(a)
    n = np.float32([-a[1], a[0]])
    L, h = length / 2, height / 2
    return np.float32([c - L * a - h * n, c + L * a - h * n, c + L * a + h * n, c - L * a + h * n])


NAMED = {
    # SHWANI along the cap of the executive pen, between the highlight and the clip, reading towards the finial
    "pen-cap": along((1617, 1196), (.826, .563), 112, 19),
    # SHWANI on the barrel of the pen beside the notebook, between the two gold rings
    "pen-barrel-nb": along((2022, 1114), (.809, .588), 150, 25),
}


def keep_mask(scene, quad, sat=16, vmin=150, exclude=()):
    """1 where the sheet shows; 0 over the hand, pen, ink and anything in `exclude` (polygons)."""
    hsv = cv2.cvtColor(scene, cv2.COLOR_BGR2HSV)
    k = ((hsv[..., 1] < sat) & (hsv[..., 2] > vmin)).astype(np.uint8)
    for poly in exclude:
        cv2.fillPoly(k, [np.int32(poly).reshape(-1, 1, 2)], 0)
    k = cv2.morphologyEx(k, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    k = cv2.morphologyEx(k, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    return cv2.GaussianBlur(k.astype(np.float32), (0, 0), .8)


def build(name, spec, save=True):
    scene_file, layers = spec[:2]
    extra = spec[2] if len(spec) > 2 else {}
    im = imread(os.path.join(SCN, scene_file))
    for (x0, y0, x1, y1), (sx, sy) in extra.get("paint", []):
        # paint a light mark (e.g. a maker's emblem) in the colour of the surface next to it
        hsv = cv2.cvtColor(im[y0:y1, x0:x1], cv2.COLOR_BGR2HSV)
        m = ((hsv[..., 2] > 122) & (hsv[..., 1] < 100)).astype(np.uint8)
        m = cv2.GaussianBlur(cv2.dilate(m, np.ones((5, 5), np.uint8)).astype(np.float32), (0, 0), 1.0)[..., None]
        col = np.float32(cv2.blur(im, (5, 5))[sy, sx])
        roi = im[y0:y1, x0:x1].astype(np.float32)
        im[y0:y1, x0:x1] = np.clip(roi * (1 - m) + col * m, 0, 255).astype(np.uint8)
    base = im.copy()
    for a, quad, opt in layers:
        if isinstance(quad, str):
            quad = NAMED[quad]
        img = art(a) if isinstance(a, str) else a
        if opt.get("crop"):
            fx0, fy0, fx1, fy1 = opt["crop"]
            h, w = img.shape[:2]
            img = img[int(fy0 * h):int(fy1 * h), int(fx0 * w):int(fx1 * w)]
        if opt.get("refine"):
            quad = refine_quad(im, quad, **opt["refine"])
        if opt.get("sub"):
            quad = subquad(quad, *opt["sub"])
        if opt.get("mug"):
            im = mug(im, img, shade_src=base, **opt["mug"])
            continue
        if opt.get("dark"):
            im = on_dark(im, img, quad, shade_src=base)
            continue
        if opt.get("metal"):
            rgba = imread_rgba(os.path.join(PNG, a + ".png"))
            im = metal_fill(im, rgba, quad, shade_src=base, **opt["metal"])
            continue
        if opt.get("fabric"):
            rgba = imread_rgba(os.path.join(PNG, a + ".png"))
            im = print_on_fabric(im, rgba, quad, opacity=opt.get("opacity", .93),
                                 contrast=opt.get("contrast", 1.25), shade_src=base)
            continue
        keep = keep_mask(base, quad, **opt["keep"]) if opt.get("keep") else None
        im = multiply(im, img, quad, white=opt.get("white"), feather=opt.get("feather", 1.0),
                      gamma=opt.get("gamma", 1.0), shade_src=base, keep=keep)
    if save:
        os.makedirs(MOCK, exist_ok=True)
        cv2.imwrite(os.path.join(MOCK, name + ".jpg"), im, [cv2.IMWRITE_JPEG_QUALITY, 92])
    return im


if __name__ == "__main__":
    only = sys.argv[1:]
    for n, s in MOCKUPS.items():
        if not only or any(n.startswith(o) for o in only):
            build(n, s)
            print("mockup", n)
