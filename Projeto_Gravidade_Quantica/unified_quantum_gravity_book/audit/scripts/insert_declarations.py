"""Insert \\input{declarations_chapter} before the bibliography of every chapter (idempotent)."""
import glob

MARK = '\\input{declarations_chapter}'
for f in sorted(glob.glob('chap*.tex')):
    s = open(f, encoding='utf-8').read()
    if MARK in s:
        print(f, 'already has declarations')
        continue
    anchor = '\\begingroup\\raggedright' if '\\begingroup\\raggedright' in s else '\\begin{thebibliography}'
    i = s.index(anchor)
    s = s[:i] + MARK + '\n\n' + s[i:]
    open(f, 'w', encoding='utf-8', newline='').write(s)
    print(f, 'inserted before', anchor)
