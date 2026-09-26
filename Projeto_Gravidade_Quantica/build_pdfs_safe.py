"""Safe PDF build: compile each target in a temporary copy of its folder and replace the
published PDF only if the compilation ends with 0 LaTeX errors. Safe to run while other
agents are editing: a half-edited file that fails to compile never overwrites a good PDF.

Usage: python build_pdfs_safe.py            (all targets)
Log:   build_pdfs_safe.log (appended)
"""
import datetime
import os
import re
import shutil
import subprocess
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(ROOT, 'unified_quantum_gravity_book')
SKIP_DIRS = {'audit', '.git', '__pycache__'}
KEEP_EXT = {'.tex', '.bib', '.sty', '.cls', '.bst', '.png', '.jpg', '.jpeg', '.pdf', '.eps', '.bbl'}

BOOK_TARGETS = sorted(f for f in os.listdir(BOOK) if re.match(r'chap\d\d_.*\.tex$', f)) + [
    'DICTIONARY_TERMS_AND_SYMBOLS.tex', 'master_book_unified_quantum_gravity.tex']
OTHER_TARGETS = [
    ('submission_package_jhep_scipost', 'manuscript_simplicial_quantum_gravity_master.tex'),
    ('Manuscritos_Avulsos/paper_yang_mills_mass_gap', 'paper_yang_mills_mass_gap.tex'),
    ('Manuscritos_Avulsos/paper_standard_model_masses', 'paper_fermion_mass_hierarchy.tex'),
]


def snapshot(src, dst):
    for name in os.listdir(src):
        p = os.path.join(src, name)
        if os.path.isdir(p):
            if name not in SKIP_DIRS and name in ('figures', 'figs', 'img', 'images'):
                shutil.copytree(p, os.path.join(dst, name))
        elif os.path.splitext(name)[1].lower() in KEEP_EXT:
            shutil.copy2(p, os.path.join(dst, name))


def compile_in(tmp, tex):
    for _ in range(3):
        subprocess.run(['pdflatex', '-interaction=nonstopmode', tex], cwd=tmp,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=900)
    log = open(os.path.join(tmp, tex[:-4] + '.log'), encoding='latin-1').read()
    errors = len(re.findall(r'^! ', log, re.M))
    warns = len(re.findall(r'(LaTeX|Package \w+|Class \w+) Warning', log))
    overfull = log.count('Overfull')
    return errors, warns, overfull


def build(folder, tex, out):
    with tempfile.TemporaryDirectory() as tmp:
        snapshot(folder, tmp)
        e, w, o = compile_in(tmp, tex)
        pdf = os.path.join(tmp, tex[:-4] + '.pdf')
        ok = e == 0 and os.path.exists(pdf)
        if ok:
            shutil.copy2(pdf, os.path.join(folder, tex[:-4] + '.pdf'))
        out.append(f'  {"UPDATED" if ok else "KEPT OLD"}  {tex}  err={e} warn={w} overfull={o}')
        return ok


def main():
    out = [f'=== {datetime.datetime.now():%Y-%m-%d %H:%M:%S}']
    # book chapters first (the master includes their PDFs), then the master
    for tex in BOOK_TARGETS:
        build(BOOK, tex, out)
    for rel, tex in OTHER_TARGETS:
        build(os.path.join(ROOT, rel), tex, out)
    text = '\n'.join(out)
    print(text)
    with open(os.path.join(ROOT, 'build_pdfs_safe.log'), 'a', encoding='utf-8') as f:
        f.write(text + '\n')


if __name__ == '__main__':
    main()
