"""Safe PDF build: compile each target in a temporary copy of its folder and replace the
published PDF only if the compilation ends with 0 LaTeX errors. Safe to run while other
agents are editing: a half-edited file that fails to compile never overwrites a good PDF.

F-19 (2026-10-07): the book's official master is now assembled single-source by default
-- inventory.py -> extract.py -> gen_master.py -> check_collisions.py -> pdflatex x3 on
master_single_source.tex, which \\input's a fresh read-only copy of every chapNN_*.tex
body (no \\includepdf of 13 separately-compiled chapter PDFs). On success this REPLACES
master_book_unified_quantum_gravity.pdf AND master_book_unified_quantum_gravity.tex (the
.tex is itself now a build artifact; see _single_source_prototype/official_master_structure.tex
for the hand-maintained structural template and ADOCAO_F19.md for the adoption report).
Pass --legacy-master to use the old \\includepdf-of-13-chapter-PDFs assembly instead; the
13 standalone chapter PDFs and the Dictionary PDF are built the same way either way.

Usage: python build_pdfs_safe.py                 (all targets, single-source master)
       python build_pdfs_safe.py --legacy-master  (all targets, old includepdf master)
Log:   build_pdfs_safe.log (appended)
"""
import argparse
import datetime
import os
import re
import shutil
import subprocess
import tempfile
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(ROOT, 'unified_quantum_gravity_book')
PROTO = os.path.join(BOOK, '_single_source_prototype')
SKIP_DIRS = {'audit', '.git', '__pycache__'}
KEEP_EXT = {'.tex', '.bib', '.sty', '.cls', '.bst', '.png', '.jpg', '.jpeg', '.pdf', '.eps', '.bbl'}

CHAPTER_TARGETS = sorted(f for f in os.listdir(BOOK) if re.match(r'chap\d\d_.*\.tex$', f))
DICTIONARY_TARGET = 'DICTIONARY_TERMS_AND_SYMBOLS.tex'
LEGACY_MASTER_TARGET = 'master_book_unified_quantum_gravity.tex'
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


def classify_log(log):
    errors = len(re.findall(r'^! ', log, re.M))
    warns = len(re.findall(r'(LaTeX|Package \w+|Class \w+) Warning', log))
    overfull = log.count('Overfull')
    undefined = len(re.findall(r'undefined on input line|There were undefined (references|citations)', log))
    return errors, warns, overfull, undefined


def compile_in(tmp, tex, passes=3, per_pass_timeout=300):
    for _ in range(passes):
        subprocess.run(['pdflatex', '-interaction=nonstopmode', tex], cwd=tmp,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       timeout=per_pass_timeout)
    log_path = os.path.join(tmp, tex[:-4] + '.log')
    log = open(log_path, encoding='latin-1').read() if os.path.exists(log_path) else ''
    errors, warns, overfull, undefined = classify_log(log)
    return errors, warns, overfull, undefined, log


def build(folder, tex, out):
    """Legacy per-file safe build (chapters, Dictionary, companion papers, and the
    old includepdf master in --legacy-master mode)."""
    with tempfile.TemporaryDirectory() as tmp:
        snapshot(folder, tmp)
        e, w, o, u, _log = compile_in(tmp, tex)
        pdf = os.path.join(tmp, tex[:-4] + '.pdf')
        ok = e == 0 and os.path.exists(pdf)
        if ok:
            shutil.copy2(pdf, os.path.join(folder, tex[:-4] + '.pdf'))
        out.append(f'  {"UPDATED" if ok else "KEPT OLD"}  {tex}  err={e} warn={w} overfull={o} undefined={u}')
        return ok


def run_py(script, cwd, timeout=120):
    return subprocess.run(['python', script], cwd=cwd, capture_output=True, text=True, timeout=timeout)


def count_pages(log_text):
    m = re.search(r'Output written on .*?\((\d+) pages?,', log_text)
    return int(m.group(1)) if m else None


def build_single_source_master(out, time_budget_s=540):
    """F-19: inventory -> extract -> gen_master -> check_collisions -> pdflatex x3,
    entirely READING the live chapNN_*.tex (never modifying them), inside a temp dir
    laid out exactly like _single_source_prototype/ (book-level assets one directory
    above the compile dir, matching the ../ paths extract.py and common_preamble.tex
    already use). Replaces the official master .tex and .pdf only on success."""
    t0 = time.time()

    dict_pdf = os.path.join(BOOK, DICTIONARY_TARGET[:-4] + '.pdf')
    dict_tex = os.path.join(BOOK, DICTIONARY_TARGET)
    if not os.path.exists(dict_pdf) or os.path.getmtime(dict_tex) > os.path.getmtime(dict_pdf):
        build(BOOK, DICTIONARY_TARGET, out)

    for script in ('gen_results_index.py', 'inventory.py', 'extract.py', 'gen_master.py'):
        try:
            r = run_py(script, PROTO)
        except subprocess.TimeoutExpired:
            out.append(f'  ABORTED single-source master: {script} timed out')
            return False
        if r.returncode != 0:
            out.append(f'  ABORTED single-source master: {script} failed:\n{r.stderr[-800:]}')
            return False

    try:
        coll = run_py('check_collisions.py', PROTO)
    except subprocess.TimeoutExpired:
        out.append('  ABORTED single-source master: check_collisions.py timed out')
        return False
    if 'dup labels: {}' not in coll.stdout or 'dup bibitems: {}' not in coll.stdout:
        out.append(f'  ABORTED single-source master: label/bibitem collision detected\n{coll.stdout}')
        return False

    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, 'src')
        os.makedirs(src)
        figures = sorted(f for f in os.listdir(BOOK) if re.match(r'fig_.*\.(pdf|png)$', f))
        for name in ['declarations_chapter.tex', 'DICTIONARY_TERMS_AND_SYMBOLS.pdf',
                     'appendix_results_index.tex'] + figures:
            shutil.copy2(os.path.join(BOOK, name), os.path.join(tmp, name))
        shutil.copy2(os.path.join(PROTO, 'common_preamble.tex'), os.path.join(src, 'common_preamble.tex'))
        shutil.copytree(os.path.join(PROTO, 'gen'), os.path.join(src, 'gen'))
        master_name = 'master_single_source.tex'
        master_staged = os.path.join(PROTO, master_name)
        shutil.copy2(master_staged, os.path.join(src, master_name))

        for i in range(3):
            remaining = time_budget_s - (time.time() - t0)
            if remaining <= 15:
                out.append(f'  ABORTED single-source master: time budget exceeded before pass {i + 1}')
                return False
            subprocess.run(['pdflatex', '-interaction=nonstopmode', master_name], cwd=src,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=max(10, min(remaining, 300)))

        log_path = os.path.join(src, master_name[:-4] + '.log')
        log = open(log_path, encoding='latin-1').read() if os.path.exists(log_path) else ''
        errors, warns, overfull, undefined = classify_log(log)
        pages = count_pages(log)
        pdf = os.path.join(src, master_name[:-4] + '.pdf')
        ok = errors == 0 and undefined == 0 and os.path.exists(pdf)
        if ok:
            shutil.copy2(pdf, os.path.join(BOOK, 'master_book_unified_quantum_gravity.pdf'))
            shutil.copy2(master_staged, os.path.join(BOOK, 'master_book_unified_quantum_gravity.tex'))
        out.append(
            f'  {"UPDATED" if ok else "KEPT OLD"}  master_book_unified_quantum_gravity (single-source)  '
            f'err={errors} warn={warns} overfull={overfull} undefined={undefined} pages={pages}'
        )
        return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--legacy-master', action='store_true',
                    help='assemble the master with the old \\includepdf-of-13-PDFs method '
                         'instead of the single-source default (F-19)')
    args = ap.parse_args()

    out = [f'=== {datetime.datetime.now():%Y-%m-%d %H:%M:%S}' +
           (' (legacy-master)' if args.legacy_master else ' (single-source master)')]

    for tex in CHAPTER_TARGETS:
        build(BOOK, tex, out)
    build(BOOK, DICTIONARY_TARGET, out)

    if args.legacy_master:
        build(BOOK, LEGACY_MASTER_TARGET, out)
    else:
        build_single_source_master(out)

    for rel, tex in OTHER_TARGETS:
        build(os.path.join(ROOT, rel), tex, out)

    text = '\n'.join(out)
    print(text)
    with open(os.path.join(ROOT, 'build_pdfs_safe.log'), 'a', encoding='utf-8') as f:
        f.write(text + '\n')


if __name__ == '__main__':
    main()
