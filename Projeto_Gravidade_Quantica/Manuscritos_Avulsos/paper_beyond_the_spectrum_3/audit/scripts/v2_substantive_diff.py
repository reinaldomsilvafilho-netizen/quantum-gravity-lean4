"""Filter the PDF-vs-tex word diff to blocks that are not explained by
hyphenation, math-macro rendering, headers, or theorem-environment names.
Also checks key formulas in the PDF text."""
import os, re, difflib
HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.normpath(os.path.join(HERE, '..'))
TEX = os.path.normpath(os.path.join(AUD, '..', 'paper_beyond_the_spectrum_3.tex'))
pdf = open(os.path.join(AUD, 'volume_3_pdf_extracted.txt'), encoding='utf-8').read()
pdf = re.sub(r'=== page \d+ ===', ' ', pdf)
tex = open(TEX, encoding='utf-8').read().split('\\begin{document}', 1)[1]
tex = re.sub(r'\\(begin|end|label|ref|eqref|cite|href|bibitem)\{[^}]*\}', ' ', tex)
tex = re.sub(r'\\[A-Za-z]+', ' ', tex)
tex = re.sub(r'%[^\n]*', ' ', tex)


def words(s):
    s = re.sub(r'-\s*\n\s*', '', s)  # de-hyphenate
    return [w.lower() for w in re.findall(r'[A-Za-z]{4,}', s)]


IGN = set('theorem proof lemma proposition definition corollary remark beyond spectrum higher invariants reinaldo silva filho section contents date september symn dgmk'.split())
wp = [w for w in words(pdf) if w not in IGN]
wx = [w for w in words(tex) if w not in IGN]
sm = difflib.SequenceMatcher(None, wp, wx, autojunk=False)
print('filtered similarity %.4f' % sm.ratio())
n = 0
for op, a0, a1, b0, b1 in sm.get_opcodes():
    if op == 'equal':
        continue
    A, B = wp[a0:a1], wx[b0:b1]
    if ''.join(A) == ''.join(B):
        continue
    if len(A) + len(B) <= 2:
        # single-token math artefacts
        continue
    n += 1
    print(op, '| PDF:', ' '.join(A)[:300], '| TEX:', ' '.join(B)[:300])
print('substantive blocks:', n)
for key in ['2 log 3', '1.3652', 'ln(1 +', 'Tr(B)', '21 theoretical', 'machine-checked', 'Mather', 'CAT(']:
    print(repr(key), 'in pdf:', key in pdf)
