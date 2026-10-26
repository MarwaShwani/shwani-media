"""Assemble the identity package (zip) from out/: logos, print PDFs, print PNGs, mockups, digital kit, book and film.
Run after all the other brand scripts:  python3 brand/package.py [dest_dir]"""
import os, sys, shutil, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
NAME = "SHWANI-identity-package"

# working files that are not deliverables
SKIP_PNG = ("mock-", "highlight-", "facebook-cover", "email-signature")


def build(dest):
    root = os.path.join(dest, NAME)
    shutil.rmtree(root, ignore_errors=True)
    parts = {
        "01-logo/svg": [os.path.join(OUT, "logo", "svg", f) for f in sorted(os.listdir(os.path.join(OUT, "logo", "svg")))],
        "01-logo/png": [os.path.join(OUT, "logo", "png", f) for f in sorted(os.listdir(os.path.join(OUT, "logo", "png")))],
        "02-print-PDF": [os.path.join(OUT, "print", f) for f in sorted(os.listdir(os.path.join(OUT, "print")))
                         if not f.startswith(SKIP_PNG)],
        "03-print-PNG": [os.path.join(OUT, "png", f) for f in sorted(os.listdir(os.path.join(OUT, "png")))
                         if not f.startswith(SKIP_PNG)],
        "04-mockups": [os.path.join(OUT, "mockups", f) for f in sorted(os.listdir(os.path.join(OUT, "mockups")))],
        "05-digital": [os.path.join(OUT, "png", f) for f in sorted(os.listdir(os.path.join(OUT, "png")))
                       if f.startswith(("highlight-", "facebook-cover", "email-signature"))]
                      + [os.path.join(OUT, "digital", f) for f in sorted(os.listdir(os.path.join(OUT, "digital")))
                         if f.endswith(".html")],
    }
    for sub, files in parts.items():
        os.makedirs(os.path.join(root, sub), exist_ok=True)
        for f in files:
            shutil.copy2(f, os.path.join(root, sub, os.path.basename(f)))
    shutil.copy2(os.path.join(OUT, "brandbook", "SHWANI-brand-book.pdf"), root)
    shutil.copy2(os.path.join(OUT, "SHWANI-brand-film.mp4"), root)
    z = os.path.join(dest, NAME + ".zip")
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for d, _, fs in os.walk(root):
            for f in sorted(fs):
                p = os.path.join(d, f)
                zf.write(p, os.path.relpath(p, dest))
    return z


if __name__ == "__main__":
    print(build(sys.argv[1] if len(sys.argv) > 1 else OUT))
