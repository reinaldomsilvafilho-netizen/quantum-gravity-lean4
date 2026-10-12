#!/usr/bin/env python3
"""F-19 prototype: check for \\label / \\bibitem key collisions across the
generated chapter bodies (gen/chapNN_body.tex), read-only."""
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
labels = Counter()
bibs = Counter()
for i in range(1, 14):
    txt = (HERE / "gen" / f"chap{i:02d}_body.tex").read_text(encoding="utf-8")
    for m in re.finditer(r"\\label\{([^}]*)\}", txt):
        labels[m.group(1)] += 1
    for m in re.finditer(r"\\bibitem\{([^}]*)\}", txt):
        bibs[m.group(1)] += 1

dup_labels = {k: v for k, v in labels.items() if v > 1}
dup_bibs = {k: v for k, v in bibs.items() if v > 1}
print("total labels:", sum(labels.values()), "unique:", len(labels))
print("total bibitems:", sum(bibs.values()), "unique:", len(bibs))
print("dup labels:", dup_labels)
print("dup bibitems:", dup_bibs)
