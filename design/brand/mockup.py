"""Put the exact print artwork onto photographic mockup scenes.

The scenes are photographs generated with Gemini (Nano Banana) from an earlier version of the art, so the
lettering on them can drift (wrong letters, missing dots). This tool lays the exact artwork over each printed
surface and keeps the scene's light:
  1. find the surface: SIFT match between the reference art (what the scene shows) and the scene, inside a
     region of interest, then a RANSAC homography; or four corners given by hand;
  2. light map = smooth(scene) / smooth(reference art warped), per channel, measured only inside the surface;
  3. result = new art warped x light map, with a soft edge, a touch of blur and grain to match the photo.
"""
import cv2
import numpy as np

SIFT = cv2.SIFT_create(nfeatures=40000, contrastThreshold=0.02)


def imread(p):
    im = cv2.imread(p, cv2.IMREAD_UNCHANGED)
    if im is None:
        raise FileNotFoundError(p)
    if im.ndim == 3 and im.shape[2] == 4:
        a = im[:, :, 3:4].astype(np.float32) / 255
        im = (im[:, :, :3].astype(np.float32) * a + 255 * (1 - a)).astype(np.uint8)
    return im


def register(scene, ref, roi=None, ratio=.78, reproj=4.0, max_side=1400):
    """Homography mapping ref pixels -> scene pixels. roi = (x0, y0, x1, y1) in scene pixels."""
    k = min(1.0, max_side / max(ref.shape[:2]))
    ref_s = cv2.resize(ref, None, fx=k, fy=k, interpolation=cv2.INTER_AREA) if k < 1 else ref
    gs = cv2.cvtColor(scene, cv2.COLOR_BGR2GRAY)
    mask = None
    if roi:
        mask = np.zeros(gs.shape, np.uint8)
        x0, y0, x1, y1 = roi
        mask[max(0, y0):y1, max(0, x0):x1] = 255
    ks, ds = SIFT.detectAndCompute(gs, mask)
    kr, dr = SIFT.detectAndCompute(cv2.cvtColor(ref_s, cv2.COLOR_BGR2GRAY), None)
    m = cv2.BFMatcher().knnMatch(dr, ds, k=2)
    good = [a for a, b in m if a.distance < ratio * b.distance]
    if len(good) < 10:
        return None, 0
    src = np.float32([kr[g.queryIdx].pt for g in good]) / k
    dst = np.float32([ks[g.trainIdx].pt for g in good])
    H, inl = cv2.findHomography(src, dst, cv2.RANSAC, reproj, maxIters=20000, confidence=.999)
    return H, int(inl.sum()) if inl is not None else 0


def corners(H, w, h):
    c = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)
    return cv2.perspectiveTransform(c, H).reshape(-1, 2)


def H_from_quad(quad, w, h):
    return cv2.getPerspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]]), np.float32(quad))


def _smooth(img, mask, sigma):
    num = cv2.GaussianBlur(img * mask[..., None], (0, 0), sigma)
    den = cv2.GaussianBlur(mask, (0, 0), sigma)[..., None]
    return num / np.maximum(den, 1e-4)


def place(scene, art, quad, ref=None, ref_quad=None, sigma_frac=.05, feather=1.2, inset=0.0, blur=.6,
          grain=1.6, light=None, clamp=(.35, 1.45), seed=0):
    """Return scene with `art` placed on the four-corner `quad` (TL, TR, BR, BL in scene pixels).
    ref: the artwork the scene currently shows on that surface (for the light map); ref_quad defaults to quad.
    light: optional fixed (b, g, r) multiplier instead of a measured light map."""
    Hs, Ws = scene.shape[:2]
    quad = np.float32(quad)
    if inset:
        cx = quad.mean(0)
        quad = cx + (quad - cx) * (1 - inset)
    h, w = art.shape[:2]
    Ha = H_from_quad(quad, w, h)
    warped = cv2.warpPerspective(art, Ha, (Ws, Hs), flags=cv2.INTER_AREA if w > 2000 else cv2.INTER_LINEAR,
                                 borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
    m = cv2.warpPerspective(np.full((h, w), 255, np.uint8), Ha, (Ws, Hs), flags=cv2.INTER_LINEAR).astype(np.float32) / 255
    side = min(np.linalg.norm(quad[1] - quad[0]), np.linalg.norm(quad[3] - quad[0]))
    sig = max(3.0, side * sigma_frac)
    sc = scene.astype(np.float32)
    if light is not None:
        L = np.ones_like(sc) * np.float32(light)
    elif ref is not None:
        rq = np.float32(ref_quad) if ref_quad is not None else quad
        hr, wr = ref.shape[:2]
        rw = cv2.warpPerspective(ref, H_from_quad(rq, wr, hr), (Ws, Hs), flags=cv2.INTER_AREA,
                                 borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
        core = cv2.erode((m > .99).astype(np.float32), np.ones((5, 5), np.uint8))
        L = _smooth(sc, core, sig) / np.maximum(_smooth(rw, core, sig), 8)
        L = np.clip(L, *clamp)
    else:
        raise ValueError("need ref or light")
    out = warped * L
    if blur:
        out = cv2.GaussianBlur(out, (0, 0), blur)
    if grain:
        rng = np.random.default_rng(seed)
        n = rng.normal(0, grain, out.shape[:2]).astype(np.float32)[..., None]
        out = out + n
    if feather:
        m = cv2.GaussianBlur(m, (0, 0), feather)
    m = m[..., None]
    res = sc * (1 - m) + out * m
    return np.clip(res, 0, 255).astype(np.uint8)


def draw_quads(scene, quads, color=(0, 0, 255)):
    im = scene.copy()
    for q in quads:
        cv2.polylines(im, [np.int32(q).reshape(-1, 1, 2)], True, color, 3)
    return im


def _line(p, q):
    d = (q - p) / np.linalg.norm(q - p)
    n = np.array([-d[1], d[0]])
    return p, d, n


def _intersect(l1, l2):
    p1, d1, _ = l1
    p2, d2, _ = l2
    A = np.array([d1, -d2]).T
    t = np.linalg.solve(A, p2 - p1)
    return p1 + t[0] * d1


def refine_quad(scene, quad, search=10.0, step=.5, angles=1.2, astep=.2, span=(.12, .88), edges=(0, 1, 2, 3)):
    """Snap each edge of a rough quad (TL, TR, BR, BL) to the strongest straight edge nearby."""
    g = cv2.GaussianBlur(cv2.cvtColor(scene, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 1.0)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)
    H, W = g.shape
    q = np.float64(quad)
    lines = []
    for i in range(4):
        p, r = q[i], q[(i + 1) % 4]
        if i not in edges:
            lines.append(_line(p, r))
            continue
        c = (p + r) / 2
        L = np.linalg.norm(r - p)
        best = (-1, None)
        for a in np.arange(-angles, angles + 1e-9, astep):
            th = np.radians(a)
            d0 = (r - p) / L
            d = np.array([d0[0] * np.cos(th) - d0[1] * np.sin(th), d0[0] * np.sin(th) + d0[1] * np.cos(th)])
            n = np.array([-d[1], d[0]])
            ts = np.linspace((span[0] - .5) * L, (span[1] - .5) * L, 160)
            for off in np.arange(-search, search + 1e-9, step):
                pts = c + n * off + ts[:, None] * d
                x, y = pts[:, 0], pts[:, 1]
                ok = (x >= 0) & (x < W - 1) & (y >= 0) & (y < H - 1)
                if ok.sum() < 40:
                    continue
                xi, yi = x[ok].astype(int), y[ok].astype(int)
                s = np.abs(gx[yi, xi] * n[0] + gy[yi, xi] * n[1])
                sc = np.median(s) * .6 + s.mean() * .4
                if sc > best[0]:
                    best = (sc, (c + n * off, d, n))
        lines.append(best[1])
    out = []
    for i in range(4):
        out.append(_intersect(lines[(i - 1) % 4], lines[i]))
    return np.float32(out)


def multiply(scene, art, quad, white=None, feather=1.0, inset=0.0, gamma=1.0, strength=1.0, shade_src=None):
    """Mockup on a BLANK white surface: result = art x (surface shading). white = paper colour under neutral light,
    measured automatically as the 97th percentile of the surface if None."""
    Hs, Ws = scene.shape[:2]
    quad = np.float32(quad)
    if inset:
        cx = quad.mean(0)
        quad = cx + (quad - cx) * (1 - inset)
    h, w = art.shape[:2]
    Ha = H_from_quad(quad, w, h)
    warped = cv2.warpPerspective(art, Ha, (Ws, Hs), flags=cv2.INTER_AREA if max(w, h) > 1.5 * max(Ws, Hs) else cv2.INTER_LINEAR,
                                 borderMode=cv2.BORDER_REPLICATE).astype(np.float32) / 255
    m = cv2.warpPerspective(np.full((h, w), 255, np.uint8), Ha, (Ws, Hs), flags=cv2.INTER_LINEAR).astype(np.float32) / 255
    sc = scene.astype(np.float32)
    src = sc if shade_src is None else shade_src.astype(np.float32)
    inside = m > .99
    if white is None:
        white = np.percentile(src[inside], 97, axis=0)
    shade = np.clip(src / np.float32(white), 0, 1.25) ** gamma
    out = warped * shade * 255
    if strength < 1:
        out = sc * (1 - strength) + out * strength
    if feather:
        m = cv2.GaussianBlur(m, (0, 0), feather)
    m = m[..., None]
    return np.clip(sc * (1 - m) + out * m, 0, 255).astype(np.uint8)


def subquad(quad, u0, v0, u1, v1):
    """Quad of the sub-rectangle [u0,u1]x[v0,v1] (fractions) of a quad, through its homography."""
    H = H_from_quad(np.float32(quad), 1, 1)
    pts = np.float32([[u0, v0], [u1, v0], [u1, v1], [u0, v1]]).reshape(-1, 1, 2)
    return cv2.perspectiveTransform(pts, H).reshape(-1, 2)


def print_on_fabric(scene, art_rgba, quad, opacity=.93, contrast=1.25, shade_src=None, feather=.8):
    """Opaque ink (e.g. cream on a dark T-shirt): ink colour modulated by the fabric's folds."""
    Hs, Ws = scene.shape[:2]
    h, w = art_rgba.shape[:2]
    Ha = H_from_quad(np.float32(quad), w, h)
    col = cv2.warpPerspective(art_rgba[:, :, :3], Ha, (Ws, Hs), flags=cv2.INTER_AREA).astype(np.float32)
    a = cv2.warpPerspective(art_rgba[:, :, 3], Ha, (Ws, Hs), flags=cv2.INTER_AREA).astype(np.float32) / 255
    src = (scene if shade_src is None else shade_src).astype(np.float32)
    lum = cv2.cvtColor(src.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
    region = a > .5
    ref = np.median(lum[region]) if region.any() else lum.mean()
    shade = np.clip((lum / max(ref, 1)) ** contrast, .45, 1.6)[..., None]
    ink = col * shade
    if feather:
        a = cv2.GaussianBlur(a, (0, 0), feather)
    a = (a * opacity)[..., None]
    out = scene.astype(np.float32) * (1 - a) + ink * a
    return np.clip(out, 0, 255).astype(np.uint8)


def imread_rgba(p):
    im = cv2.imread(p, cv2.IMREAD_UNCHANGED)
    if im.shape[2] == 3:
        im = np.dstack([im, np.full(im.shape[:2], 255, np.uint8)])
    return im


def mug(scene, art, x0, x1, y_top, y_bot, e_top, e_bot, a0, a1, v0=.06, v1=.94, theta=1.35, white=None, shade_src=None):
    """Wrap a band of `art` (columns a0..a1 as fractions = the visible half of the mug) around a vertical cylinder.
    x0..x1: body silhouette; y_top/y_bot: band edge at the silhouette; e_top/e_bot: how far the ellipses sag at the centre."""
    Hs, Ws = scene.shape[:2]
    src = (scene if shade_src is None else shade_src).astype(np.float32)
    cx, r = (x0 + x1) / 2, (x1 - x0) / 2
    yy, xx = np.mgrid[0:Hs, int(x0):int(x1) + 1].astype(np.float32)
    u = np.clip((xx - cx) / r, -1, 1)
    c = np.sqrt(1 - u ** 2)
    yt = y_top + e_top * c
    yb = y_bot + e_bot * c
    v = (yy - yt) / (yb - yt)
    th = np.arcsin(u)
    s = (th / np.pi + .5)  # 0..1 over the visible half
    h, w = art.shape[:2]
    mx = (a0 + s * (a1 - a0)) * (w - 1)
    vv = (v - v0) / (v1 - v0)
    my = vv * (h - 1)
    warped = cv2.remap(art, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255)).astype(np.float32) / 255
    m = ((v >= 0) & (v <= 1) & (np.abs(th) <= theta)).astype(np.float32)
    m = cv2.GaussianBlur(m, (0, 0), 1.2)
    sub = src[:, int(x0):int(x1) + 1]
    if white is None:
        white = np.percentile(sub[m > .9], 96, axis=0)
    shade = np.clip(sub / np.float32(white), 0, 1.2)
    out = warped * shade * 255
    res = scene.astype(np.float32).copy()
    region = res[:, int(x0):int(x1) + 1]
    res[:, int(x0):int(x1) + 1] = region * (1 - m[..., None]) + out * m[..., None]
    return np.clip(res, 0, 255).astype(np.uint8)
