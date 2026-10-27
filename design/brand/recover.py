"""Rebuild the blank mockup scenes from the delivered mockups (26 Oct).

The blank Gemini scenes used on 19 Oct were not kept, but every delivered mockup is
    mockup = old_art (warped onto its quad) x surface shading      (mockup.multiply)
so the shading of each printed surface can be read back wherever the old art is light, and filled in
smoothly where it was dark. Outside the quads the photo is the scene itself. The result is written to
scenes/<scene>-blank.jpg at a fixed paper level (W), so mockups.py rebuilds every mockup with the new art.

Fabric prints (T-shirts) are opaque ink: under the old ink the fold shading is read from the ink itself.

Run: python3 brand/recover.py OLD_MOCKUPS_DIR OLD_PNG_DIR [names...]
"""
import os, sys
import cv2
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mockup import H_from_quad, subquad, imread, imread_rgba  # noqa: E402
import mockups as M  # noqa: E402

W_PAPER = 204.0      # blank = shade x W; 204 x 1.25 (the largest shade multiply allows) stays under 255


def warp(img, quad, size, interp=cv2.INTER_LINEAR, border=cv2.BORDER_REPLICATE):
    h, w = img.shape[:2]
    return cv2.warpPerspective(img, H_from_quad(np.float32(quad), w, h), size, flags=interp, borderMode=border)


def quad_mask(quad, size):
    m = np.zeros(size[::-1], np.uint8)
    cv2.fillPoly(m, [np.int32(np.round(quad)).reshape(-1, 1, 2)], 255)
    return m > 0


def _blur(img, s):
    """Gaussian blur; large sigmas are done on a reduced image (same result, many times faster)."""
    if s <= 6:
        return cv2.GaussianBlur(img, (0, 0), s).reshape(img.shape)
    f = s / 3.0
    h, w = img.shape[:2]
    small = cv2.resize(img, (max(1, int(w / f)), max(1, int(h / f))), interpolation=cv2.INTER_AREA)
    small = cv2.GaussianBlur(small, (0, 0), 3.0)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_LINEAR).reshape(img.shape)


def fill_smooth(val, w, scales=(1.5, 5, 16, 50, 160)):
    """Normalized convolution from fine to coarse: keep fine detail where the weight is good, fill the rest."""
    out = None
    for s in reversed(scales):
        num = _blur(val * w[..., None], s)
        den = _blur(w, s)
        den = den[..., None] if den.ndim == 2 else den
        est = num / np.maximum(den, 1e-6)
        if out is None:
            out = est
        else:
            a = np.clip(den / .45, 0, 1)
            out = out * (1 - a) + est * a
    return out


def add_grain(est, shade, wgt, core, offsets=(90, 160, 240, 330, 430)):
    """Where the shading was filled in (under old dark art) the paper grain is missing: borrow the fine grain
    (shade minus its blur) from a nearby spot of the same surface where it was measured."""
    hp = shade - cv2.GaussianBlur(shade, (0, 0), 2.5)
    good = (wgt > .6) & core
    conf = cv2.GaussianBlur(good.astype(np.float32), (0, 0), 2)
    need = core & (conf < .5)
    if not need.any():
        return est
    Hs, Ws = good.shape
    grain = np.zeros_like(est)
    done = ~need
    for d in offsets:
        for dx, dy in ((d, 0), (-d, 0), (0, d), (0, -d), (d, d), (-d, -d), (d, -d), (-d, d)):
            M_ = np.float32([[1, 0, dx], [0, 1, dy]])
            src_ok = cv2.warpAffine(good.astype(np.uint8), M_, (Ws, Hs), flags=cv2.INTER_NEAREST) > 0
            take = ~done & src_ok
            if take.any():
                g = cv2.warpAffine(hp, M_, (Ws, Hs), flags=cv2.INTER_NEAREST)
                grain[take] = g[take]
                done |= take
        if done.all():
            break
    a = np.clip(1 - conf / .5, 0, 1)[..., None]
    return est + grain * a


def layers_of(spec, old_png):
    """(art, quad, opt) for each layer, with the old artwork, prepared exactly as mockups.build does."""
    layers = spec[1]
    out = []
    for a, quad, opt in layers:
        # a layer whose quad was corrected after delivery: recover with what the delivered mockup used
        a, quad = opt.get("old_art", a), opt.get("old_quad", quad)
        if isinstance(a, str) and a.startswith("#"):
            img = M.art(a)
        elif isinstance(a, str) and a.startswith("asset:"):
            img = imread(os.path.join(OLD_ASSETS, a[6:]))
        else:
            img = imread(os.path.join(old_png, a + ".png"))
        if opt.get("crop"):
            fx0, fy0, fx1, fy1 = opt["crop"]
            h, w = img.shape[:2]
            img = img[int(fy0 * h):int(fy1 * h), int(fx0 * w):int(fx1 * w)]
        q = np.float32(quad)
        if opt.get("sub"):
            q = subquad(q, *opt["sub"])
        out.append((a, img, q, opt))
    return out


def recover_mug(mock, img, params):
    """Wrapped print on a white mug: mask what the old wrap printed (rendered with the same cylinder) and fill it
    from the glaze around it."""
    from mockup import mug
    white = np.full(mock.shape, 255, np.uint8)
    r = mug(white, img, white=np.float32([255, 255, 255]), **params)
    ink = (r.astype(np.float32).min(2) < 246).astype(np.uint8)
    ink = cv2.dilate(ink, np.ones((21, 21), np.uint8)) > 0
    ok = (~ink).astype(np.float32)
    x0, x1 = int(params["x0"]) + 6, int(params["x1"]) - 6
    ok[:, :x0] = 0
    ok[:, x1:] = 0                     # only glaze of this mug feeds the fill
    est = fill_smooth(mock, ok, scales=(3, 8, 20, 50))
    out = mock.copy()
    out[ink] = est[ink]
    return out


def recover(name, old_mock_dir, old_png):
    spec = M.MOCKUPS[name]
    mock = cv2.imread(os.path.join(old_mock_dir, name + ".jpg")).astype(np.float32)
    Hs, Ws = mock.shape[:2]
    size = (Ws, Hs)
    if any(o.get("mug") for _, _, o in spec[1]):
        out = mock
        for a, quad, opt in spec[1]:
            img = imread(os.path.join(old_png, a + ".png"))
            out = recover_mug(out, img, opt["mug"])
        return np.clip(out, 0, 255).astype(np.uint8)
    L = layers_of(spec, old_png)
    masks = [quad_mask(q, size) for _, _, q, _ in L]
    blank = mock.copy()
    # feathered coverage of each layer, as multiply() draws it
    cover = []
    for a, img, q, opt in L:
        mh = warp(np.full(img.shape[:2], 255, np.uint8), q, size, border=cv2.BORDER_CONSTANT).astype(np.float32) / 255
        f = opt.get("feather", 1.0)
        cover.append(cv2.GaussianBlur(mh, (0, 0), f) if f else mh)
    for i, (a, img, q, opt) in enumerate(L):
        later = np.zeros((Hs, Ws), np.float32)
        for c in cover[i + 1:]:
            later = np.maximum(later, c)
        mf = cover[i]
        free = later < .02
        core = (mf >= .85) & free
        band = (mf >= .02) & (mf < .85) & free
        if not core.any():
            continue
        if opt.get("fabric"):
            rgba = imread_rgba(os.path.join(old_png, a + ".png"))
            blank = _fabric(blank, mock, rgba, q, core | band, opt)
            continue
        wa = warp(img, q, size, cv2.INTER_AREA if max(img.shape[:2]) > 1.5 * max(Ws, Hs) else cv2.INTER_LINEAR).astype(np.float32) / 255
        inner = cv2.erode(core.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
        lum = cv2.erode(wa.mean(2), np.ones((5, 5), np.uint8))          # stay away from the edges of the artwork
        wgt = np.where(inner, np.clip((lum - .18) / .5, 0, 1) ** 2, 0).astype(np.float32)
        shade = np.clip(mock / np.maximum(wa * 255, 1), 0, 1.3)
        est_l = fill_smooth(shade, wgt)
        # under large dark areas (a charcoal cover) the light estimate has nothing near: read the shading through the
        # dark ink itself, averaged over a wider window to beat the noise
        lum_d = cv2.erode(wa.mean(2), np.ones((3, 3), np.uint8))
        wd = np.where(inner, (lum_d > .035).astype(np.float32), 0).astype(np.float32)
        est_d = fill_smooth(shade, wd, scales=(5, 14, 40, 120))
        # prefer the light estimate wherever light paper is within reach (it has no ink bias); the dark one only
        # fills wide dark areas
        conf = _blur(wgt, 25)
        a_ = np.clip(conf / .12, 0, 1)[..., None]
        est = est_l * a_ + est_d * (1 - a_)
        est = add_grain(est, shade, wgt, core)
        Wc = 255.0 if opt.get("white") else W_PAPER
        blank[core] = np.clip(est[core] * Wc, 0, 255)
        # the feathered edge: undo the blend with the old art to get the scene that was under it
        out_old = wa * est * 255
        m3 = mf[..., None]
        solved = (mock - out_old * m3) / np.maximum(1 - m3, .15)
        blank[band] = np.clip(solved[band], 0, 255)
    # corrected quads: the surface around the old quad is real paper; bring the rebuilt part to the same level
    for (a, img, q, opt), raw in zip(L, spec[1]):
        if "old_quad" in opt:
            blank = match_paper(blank, mock, q, np.float32(raw[1]), level=opt.get("paper_min", 225))
    return np.clip(blank, 0, 255).astype(np.uint8)


def match_paper(blank, mock, old_q, new_q, ring=25, level=225):
    Hs, Ws = blank.shape[:2]
    old_m = quad_mask(old_q, (Ws, Hs))
    new_m = quad_mask(new_q, (Ws, Hs))
    near_out = (cv2.dilate(old_m.astype(np.uint8), np.ones((2 * ring + 1,) * 2, np.uint8)) > 0) & ~old_m & new_m
    paper = near_out & (mock.mean(2) > level)
    near_in = old_m & (cv2.dilate(paper.astype(np.uint8), np.ones((2 * ring + 1,) * 2, np.uint8)) > 0)
    near_in &= cv2.erode(old_m.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
    if paper.sum() < 200 or near_in.sum() < 200:
        return blank
    k = np.median(mock[paper], axis=0) / np.maximum(np.median(blank[near_in], axis=0), 1)
    region = cv2.erode(old_m.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    out = blank.copy()
    out[region] = np.clip(blank[region] * k, 0, 255)
    # the old quad's edge (a few pixels where old art and photo were blended) leaves a faint line: fill it from both sides
    edge = np.zeros((Hs, Ws), np.uint8)
    cv2.polylines(edge, [np.int32(np.round(old_q)).reshape(-1, 1, 2)], True, 1, 1)
    edge = (cv2.dilate(edge, np.ones((9, 9), np.uint8)) > 0) & new_m
    w = (new_m & ~edge).astype(np.float32)          # only the surface itself feeds the fill
    fill = fill_smooth(out.astype(np.float32), w, scales=(2, 5, 12))
    out[edge] = np.clip(fill[edge], 0, 255)
    print("  paper level matched, x", np.round(k, 3))
    return out


def _fabric(blank, mock, rgba, quad, grow, opt):
    """Under an opaque print: shade = ink pixel / ink colour, lum = ref x shade^(1/contrast); fabric colour from around it."""
    Hs, Ws = mock.shape[:2]
    h, w = rgba.shape[:2]
    Ha = H_from_quad(np.float32(quad), w, h)
    col = cv2.warpPerspective(rgba[:, :, :3], Ha, (Ws, Hs), flags=cv2.INTER_AREA).astype(np.float32)
    a = cv2.warpPerspective(rgba[:, :, 3], Ha, (Ws, Hs), flags=cv2.INTER_AREA).astype(np.float32) / 255
    a = cv2.GaussianBlur(a, (0, 0), .8)
    op, k = opt.get("opacity", .93), opt.get("contrast", 1.25)
    lum_m = cv2.cvtColor(mock.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
    ring = (cv2.dilate((a > .02).astype(np.uint8), np.ones((41, 41), np.uint8)) > 0) & (a < .01)
    ref = np.median(lum_m[ring])
    fab = np.median(mock[ring], axis=0)                       # fabric colour (BGR) at the reference level
    solid = a > .9
    col_l = cv2.cvtColor(np.clip(col, 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
    sh = np.where(solid, (lum_m - (1 - op) * ref) / np.maximum(op * col_l, 1), 0)
    lum_ink = ref * np.clip(sh, .45, 1.6) ** (1 / k)
    # fabric lum: measured from the ink where the print is solid, from the photo where there is no print
    val = np.where(solid, lum_ink, lum_m)[..., None]
    wgt = (solid | (a < .01)).astype(np.float32)
    est = fill_smooth(val, wgt, scales=(1.2, 4, 12, 40))[..., 0]
    region = cv2.dilate((a > .01).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    rebuilt = fab[None, None, :] * (est / max(ref, 1))[..., None]
    out = blank.copy()
    out[region] = rebuilt[region]
    return out


OLD_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

if __name__ == "__main__":
    old_mock, old_png = sys.argv[1], sys.argv[2]
    if len(sys.argv) > 3 and sys.argv[3].startswith("--assets="):
        OLD_ASSETS = sys.argv[3].split("=", 1)[1]
        only = sys.argv[4:]
    else:
        only = sys.argv[3:]
    os.makedirs(M.SCN, exist_ok=True)
    for n, spec in M.MOCKUPS.items():
        if only and not any(n.startswith(o) for o in only):
            continue
        if not os.path.exists(os.path.join(old_mock, n + ".jpg")):
            print("skip (no delivered mockup)", n)
            continue
        im = recover(n, old_mock, old_png)
        cv2.imwrite(os.path.join(M.SCN, spec[0]), im, [cv2.IMWRITE_JPEG_QUALITY, 95])
        print("scene", spec[0], "from", n)
