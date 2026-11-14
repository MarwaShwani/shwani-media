"""Post 16 (Sun 15 Nov 12:30): single image «4 ملازم مبسطة، مجاناً». Row 6, sage.
Marwa, 14 Nov: the four simplified booklets are free to anyone who asks; the grammar one is the new copy
without the teacher's name. Students write the subject in the comments, Marwa sends the PDF in a message."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from kit2 import *  # noqa

R = row("sage")
covers = [page_img(b, 1) for b in ("comp", "gram", "phys", "math")]
fan = R.sheets(covers, h=500, rot=(-6, -2, 2, 6), gap=-62)
SLIDES = [R.single("مجاناً للطلاب", fan, "4 ملازم مبسطة،<br>مجاناً لك",
                   "للصف الثالث المهني (السادس): الرياضيات، والطبيعيات، وقواعد اللغة العربية، وصيانة الحاسوب.",
                   ask="اكتب اسم المادة في التعليقات، ونرسلها لك في الرسائل.")]
if __name__ == "__main__":
    build(HERE, SLIDES)
