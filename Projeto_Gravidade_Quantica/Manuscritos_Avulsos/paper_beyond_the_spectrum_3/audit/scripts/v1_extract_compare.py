"""Extract Vol. III text from the Zenodo trilogy PDF (record 22866175) and from
volume_3_higher_invariants.pdf, and compare with the local .tex (theorem-level
and word-level)."""
import os, re, difflib
import fitz  # PyMuPDF

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.normpath(os.path.join(HERE, '..'))
FILES = os.path.normpath(os.path.join(AUD, '..', '..', 'beyond_the_spectrum_files'))
TEX = os.path.normpath(os.path.join(AUD, '..', 'paper_beyond_the_spectrum_3.tex'))


def pdf_text(p):
    d = fitz.open(p)
    return [pg.get_text() for pg in d]


tri = pdf_text(os.path.join(FILES, 'beyond_the_spectrum_trilogy_updated.pdf'))
v3 = pdf_text(os.path.join(FILES, 'volume_3_higher_invariants.pdf'))
print('trilogy pages', len(tri), 'vol3 pages', len(v3))
# locate Vol III start in trilogy: page containing the Vol III title
starts = [i for i, t in enumerate(tri) if 'Beyond the Spectrum III' in t or 'BEYOND THE SPECTRUM III' in t.upper()]
print('pages mentioning Vol III title:', starts[:10])
start = None
for i in starts:
    if 'Higher Invariants' in tri[i] or 'HIGHER INVARIANTS' in tri[i].upper():
        start = i
        break
tri3 = tri[start:]
open(os.path.join(AUD, 'zenodo_22866175_vol3_extracted.txt'), 'w', encoding='utf-8').write(
    '\n'.join('=== trilogy page %d ===\n%s' % (start + 1 + k, t) for k, t in enumerate(tri3)))
open(os.path.join(AUD, 'volume_3_pdf_extracted.txt'), 'w', encoding='utf-8').write(
    '\n'.join('=== page %d ===\n%s' % (k + 1, t) for k, t in enumerate(v3)))


def words(s):
    s = re.sub(r'\s+', ' ', s)
    return re.findall(r'[A-Za-z]{3,}', s)


def strip_running(pages):
    return ' '.join(pages)


wt = words(strip_running(tri3))
wv = words(strip_running(v3))
# tex: drop commands, keep words
tex = open(TEX, encoding='utf-8').read()
tex_body = tex.split('\\begin{document}', 1)[1]
tex_body = re.sub(r'\\(begin|end|label|ref|eqref|cite|href|bibitem)\{[^}]*\}', ' ', tex_body)
tex_body = re.sub(r'\\[A-Za-z]+', ' ', tex_body)
wx = words(tex_body)
print('word counts: trilogy-vol3 %d, vol3.pdf %d, tex %d' % (len(wt), len(wv), len(wx)))


def ratio(a, b):
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


print('similarity trilogy-vol3 vs vol3.pdf: %.4f' % ratio(wt, wv))
print('similarity vol3.pdf vs tex: %.4f' % ratio(wv, wx))
print('similarity trilogy-vol3 vs tex: %.4f' % ratio(wt, wx))
# negative control: vol3.pdf vs Vol I pdf should be low
v1 = words(' '.join(pdf_text(os.path.join(FILES, 'volume_1_functional_realizations.pdf'))))
print('NEG CONTROL vol3.pdf vs vol1.pdf: %.4f' % ratio(wv, v1[:len(wv)]))

# OBL tags present
for name, w in [('trilogy', ' '.join(tri3)), ('vol3pdf', ' '.join(v3)), ('tex', tex)]:
    tags = sorted(set(re.findall(r'OBL-\d{3}', w)))
    print(name, 'OBL tags:', len(tags), tags[0] if tags else None, tags[-1] if tags else None)

# list differing word blocks vol3.pdf vs tex
sm = difflib.SequenceMatcher(None, wv, wx, autojunk=False)
print('--- diff blocks vol3.pdf -> tex (non-equal, first 80) ---')
n = 0
for op, a0, a1, b0, b1 in sm.get_opcodes():
    if op != 'equal':
        n += 1
        if n <= 80:
            print(op, ' '.join(wv[a0:a1])[:160], ' ==> ', ' '.join(wx[b0:b1])[:160])
print('total non-equal blocks', n)
sm2 = difflib.SequenceMatcher(None, wt, wv, autojunk=False)
print('--- diff blocks trilogy-vol3 -> vol3.pdf ---')
n = 0
for op, a0, a1, b0, b1 in sm2.get_opcodes():
    if op != 'equal':
        n += 1
        if n <= 40:
            print(op, ' '.join(wt[a0:a1])[:160], ' ==> ', ' '.join(wv[b0:b1])[:160])
print('total non-equal blocks', n)
