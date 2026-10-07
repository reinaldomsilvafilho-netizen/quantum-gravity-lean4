"""Download latest trilogy and the 2026-09-11 Volume I; report sha256 vs local PDFs."""
import hashlib
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.dirname(HERE)
LOCAL = os.path.join(AUD, "..", "..", "beyond_the_spectrum_files")

DL = {
    "zenodo_latest_trilogy_22866175.pdf":
        "https://zenodo.org/api/records/22866175/files/beyond_the_spectrum_trilogy.pdf/content",
    "zenodo_v22699282_vol1.pdf":
        "https://zenodo.org/api/records/22699282/files/volume_1_functional_realizations.pdf/content",
    "zenodo_v22644744_vol1.pdf":
        "https://zenodo.org/api/records/22644744/files/volume_1_functional_realizations.pdf/content",
}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


for name, url in DL.items():
    out = os.path.join(AUD, name)
    if not os.path.exists(out):
        urllib.request.urlretrieve(url, out)
    print(name, os.path.getsize(out), sha(out))

for name in ["beyond_the_spectrum_trilogy.pdf", "beyond_the_spectrum_trilogy_updated.pdf",
             "volume_1_functional_realizations.pdf"]:
    p = os.path.join(LOCAL, name)
    print("local", name, os.path.getsize(p), sha(p))
