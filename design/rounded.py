import math
CH, MU, DK, TE = "#F2E9D8", "#D4A72C", "#202126", "#E07A47"

def stroke(d, color, w, extra=""):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"{extra}/>'

class Word:
    """Monoline letters with round caps. y down, baseline 0, cap height H, stroke sw."""
    def __init__(self, H, sw, gap):
        self.H, self.sw, self.gap = H, sw, gap
        self.yT, self.yB = -H + sw / 2, -sw / 2
        self.x = 0.0; self.parts = []; self.slots = {}
    def _place(self, width):   # width = centerline width; returns x of centerline left
        x0 = self.x + self.sw / 2
        self.x = x0 + width + self.sw / 2 + self.gap
        return x0
    def S(self, w, color):
        x0 = self._place(w); rx = w / 2; cx = x0 + rx
        ry = (self.yB - self.yT) / 4; ct, cb = self.yT + ry, self.yB - ry
        a1, a2 = math.radians(-22), math.radians(158)
        sx, sy = cx + rx * math.cos(a1), ct + ry * math.sin(a1)
        ex, ey = cx + rx * math.cos(a2), cb + ry * math.sin(a2)
        d = f"M{sx:.1f} {sy:.1f} A{rx:.1f} {ry:.1f} 0 1 0 {cx:.1f} {ct+ry:.1f} A{rx:.1f} {ry:.1f} 0 1 1 {ex:.1f} {ey:.1f}"
        self.parts.append(stroke(d, color, self.sw))
    def H_(self, w, color, bar, bar_w):
        x0 = self._place(w); x1 = x0 + w; ym = (self.yT + self.yB) / 2
        self.parts.append(stroke(f"M{x0:.1f} {self.yT:.1f} V{self.yB:.1f} M{x1:.1f} {self.yT:.1f} V{self.yB:.1f}", color, self.sw))
        self.parts.append(stroke(f"M{x0:.1f} {ym:.1f} H{x1:.1f}", bar, bar_w))
    def W(self, w, color):
        x0 = self._place(w); q = w / 4
        d = f"M{x0:.1f} {self.yT:.1f} L{x0+q:.1f} {self.yB:.1f} L{x0+2*q:.1f} {self.yT+ (self.yB-self.yT)*0.18:.1f} L{x0+3*q:.1f} {self.yB:.1f} L{x0+w:.1f} {self.yT:.1f}"
        self.parts.append(stroke(d, color, self.sw))
    def A(self, w, color, bar_y=0.62):
        x0 = self._place(w); xm = x0 + w / 2
        self.parts.append(stroke(f"M{x0:.1f} {self.yB:.1f} L{xm:.1f} {self.yT:.1f} L{x0+w:.1f} {self.yB:.1f}", color, self.sw))
        yb = self.yT + (self.yB - self.yT) * bar_y; t = (yb - self.yT) / (self.yB - self.yT)
        xl, xr = xm - t * w / 2, xm + t * w / 2
        self.parts.append(stroke(f"M{xl:.1f} {yb:.1f} H{xr:.1f}", color, self.sw))
    def N(self, w, color):
        x0 = self._place(w)
        self.parts.append(stroke(f"M{x0:.1f} {self.yB:.1f} V{self.yT:.1f} L{x0+w:.1f} {self.yB:.1f} V{self.yT:.1f}", color, self.sw))
    def I(self, color):
        x0 = self._place(0)
        self.parts.append(stroke(f"M{x0:.1f} {self.yT:.1f} V{self.yB:.1f}", color, self.sw))
    def C(self, w, color):
        x0 = self._place(w); rx = w / 2; cx = x0 + rx; ry = (self.yB - self.yT) / 2; cy = (self.yT + self.yB) / 2
        a1, a2 = math.radians(-50), math.radians(50)
        d = f"M{cx+rx*math.cos(a1):.1f} {cy+ry*math.sin(a1):.1f} A{rx:.1f} {ry:.1f} 0 1 0 {cx+rx*math.cos(a2):.1f} {cy+ry*math.sin(a2):.1f}"
        self.parts.append(stroke(d, color, self.sw))
    def O(self, w, color):
        x0 = self._place(w); rx = w / 2; ry = (self.yB - self.yT) / 2
        self.parts.append(f'<ellipse cx="{x0+rx:.1f}" cy="{(self.yT+self.yB)/2:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="{color}" stroke-width="{self.sw}"/>')
    def M(self, w, color):
        x0 = self._place(w)
        self.parts.append(stroke(f"M{x0:.1f} {self.yB:.1f} V{self.yT:.1f} L{x0+w/2:.1f} {self.yB - (self.yB-self.yT)*0.25:.1f} L{x0+w:.1f} {self.yT:.1f} V{self.yB:.1f}", color, self.sw))
    def P(self, w, color):
        x0 = self._place(w); ym = self.yT + (self.yB - self.yT) * 0.55; r = (ym - self.yT) / 2
        self.parts.append(stroke(f"M{x0:.1f} {self.yB:.1f} V{self.yT:.1f} H{x0+w-r:.1f} A{r:.1f} {r:.1f} 0 0 1 {x0+w-r:.1f} {ym:.1f} H{x0:.1f}", color, self.sw))
    def Y(self, w, color):
        x0 = self._place(w); ym = self.yT + (self.yB - self.yT) * 0.5
        self.parts.append(stroke(f"M{x0:.1f} {self.yT:.1f} L{x0+w/2:.1f} {ym:.1f} L{x0+w:.1f} {self.yT:.1f} M{x0+w/2:.1f} {ym:.1f} V{self.yB:.1f}", color, self.sw))
    def width(self):
        return self.x - self.gap
    def svg(self):
        return "".join(self.parts)

def shwani(color, bar):
    w = Word(H=700, sw=160, gap=95)
    w.S(470, color); w.H_(430, color, bar, 130); w.W(800, color); w.A(620, color, 0.66); w.N(450, color); w.I(color)
    return w

def company(color, target_width):
    # find a gap so the word spans target_width
    def build(gap):
        c = Word(H=190, sw=46, gap=gap)
        c.C(150, color); c.O(170, color); c.M(200, color); c.P(130, color); c.A(190, color, 0.66); c.N(150, color); c.Y(170, color)
        return c
    base = build(0); g = (target_width - base.width()) / 6
    return build(g)

def lockup(color, bar, word_color):
    s = shwani(color, bar); W = s.width()
    c = company(word_color, W)
    body = s.svg() + f'<g transform="translate(0 420)">{c.svg()}</g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-30 -730 {W+60:.0f} 1180" width="{W+60:.0f}" height="1180">'
            f'<title>SHWANI COMPANY</title>{body}</svg>')

def mark(color, bar):   # SH monogram
    w = Word(H=700, sw=160, gap=95)
    w.S(470, color); w.H_(430, color, bar, 130)
    W = w.width()
    return W, w.svg()

def mark_svg(color, bar, pad=30):
    W, body = mark(color, bar)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-700-pad} {W+2*pad:.0f} {700+2*pad}" width="{W+2*pad:.0f}" height="{700+2*pad}">'
            f'<title>SHWANI</title>{body}</svg>')

def avatar(bg, color, bar, ring=None, kind="sh"):
    S = 1080
    if kind == "sh":
        W, body = mark(color, bar)
        k = 560 / W
        g = f'<g transform="translate({(S - W*k)/2:.1f} {S/2 + 700*k/2:.1f}) scale({k:.4f})">{body}</g>'
    else:  # bridge symbol: two stems and the bar
        w = Word(H=700, sw=160, gap=0); w.H_(430, color, bar, 130); W = w.width()
        k = 520 / 700
        g = f'<g transform="translate({(S - W*k)/2:.1f} {S/2 + 700*k/2:.1f}) scale({k:.4f})">{w.svg()}</g>'
    ring_svg = f'<circle cx="540" cy="540" r="470" fill="none" stroke="{ring}" stroke-width="22"/>' if ring else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">'
            f'<rect width="{S}" height="{S}" fill="{bg}"/>{ring_svg}{g}</svg>')

if __name__ == "__main__":
    OUT = "../assets/"
    open(OUT + "shwani-r-lockup-dark.svg", "w").write(lockup(CH, TE, CH))
    open(OUT + "shwani-r-lockup-light.svg", "w").write(lockup(DK, TE, DK))
    open(OUT + "shwani-r-mark-cream.svg", "w").write(mark_svg(CH, TE))
    open(OUT + "shwani-r-mark-charcoal.svg", "w").write(mark_svg(DK, TE))
    open(OUT + "shwani-r-mark-mono-cream.svg", "w").write(mark_svg(CH, CH))
    open(OUT + "shwani-r-mark-mono-charcoal.svg", "w").write(mark_svg(DK, DK))
    open(OUT + "avatar-1.svg", "w").write(avatar(DK, CH, TE))
    open(OUT + "avatar-2.svg", "w").write(avatar(TE, DK, CH))
    open(OUT + "avatar-3.svg", "w").write(avatar(CH, DK, TE))
    open(OUT + "avatar-4.svg", "w").write(avatar(DK, CH, TE, ring=MU, kind="bridge"))
    print("ok")
