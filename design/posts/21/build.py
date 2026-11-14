"""Post 21 (Tue 17 Nov 21:00): single image «حتى الخاتم يحمل الشعار». Row 7, charcoal with gold. AI-made scene."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from kit2 import *  # noqa

R = row("charcoal")
SLIDES = [R.single("من أعمالنا", R.band(A("almanar", "11_ring.jpg"), h=600, shift=(0, .1)),
                   "حتى الخاتم<br>يحمل الشعار", "شعار «المنار» محفوراً على خاتم، بالتفاصيل نفسها: المنار، والجوهرة، والحروف.",
                   ask="أين ترى شعارك أولاً؟ الواجهة، أم الكيس، أم القطعة نفسها؟")]
if __name__ == "__main__":
    build(HERE, SLIDES)
