"""Apply literal replacements to a LaTeX file.

Usage: python _apply.py target.tex edits.txt
edits.txt holds blocks separated by lines '@@OLD', '@@NEW', '@@END'.
Each OLD must occur exactly once.
"""
import io
import sys

target, edits = sys.argv[1], sys.argv[2]
s = io.open(target, encoding="utf-8").read()
blocks = io.open(edits, encoding="utf-8").read().split("@@OLD\n")[1:]
for blk in blocks:
    old, rest = blk.split("@@NEW\n", 1)
    new = rest.split("@@END", 1)[0]
    old = old[:-1] if old.endswith("\n") else old
    new = new[:-1] if new.endswith("\n") else new
    n = s.count(old)
    if n != 1:
        sys.exit("count=%d for: %s" % (n, old[:80]))
    s = s.replace(old, new)
io.open(target, "w", encoding="utf-8").write(s)
print("applied", len(blocks), "edits to", target)
