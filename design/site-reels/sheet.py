import sys, glob
from PIL import Image, ImageDraw
src, dst = sys.argv[1], sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 13
fs = sorted(glob.glob(src + '/*.jpg'))
ims = [Image.open(f).convert('RGB') for f in fs]
w, h = ims[0].size; s = 0.42 * 405 / w; tw, th = int(w * s), int(h * s)
rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (cols * (tw + 4), rows * (th + 16)), 'white'); d = ImageDraw.Draw(sheet)
for i, (f, im) in enumerate(zip(fs, ims)):
    x = (i % cols) * (tw + 4); y = (i // cols) * (th + 16); sheet.paste(im.resize((tw, th)), (x, y + 14)); d.text((x + 2, y + 1), '%.1fs' % (int(f[-9:-4]) / 30), fill='black')
sheet.save(dst, quality=78); print(sheet.size)
