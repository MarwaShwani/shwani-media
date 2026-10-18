"""Size variants used only to dress mockup photos whose paper has a slightly different shape
(e.g. a Letter-size sheet or a 1.66 card in the photo). The print files stay at their true sizes."""
from kit import render
import stationery as st, printwork as pw, merch as mc

def v(piece, w, h, name):
    piece.w, piece.h, piece.name = w, h, name
    return piece

VARIANTS = [
    v(st.letterhead_sample(), 215.9, 279.4, "mock-letterhead-letter"),
    v(st.quotation(), 215.9, 279.4, "mock-quotation-letter"),
    v(st.card_front(), 90, 54.2, "mock-card-front-166"),
    v(st.card_back(), 90, 54.2, "mock-card-back-166"),
    v(pw.brochure_outside(), 297, 234, "mock-brochure-outside-234"),
    v(pw.brochure_inside(), 297, 245, "mock-brochure-inside-245"),
]

if __name__ == "__main__":
    render(VARIANTS, pdf=False)
