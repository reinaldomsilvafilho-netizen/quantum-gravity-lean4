"""Lint LaTeX sources for Markdown artifacts and other leftovers (WORKPLAN F-18).

Usage:  python audit/scripts/lint_tex.py          # report
        python audit/scripts/lint_tex.py --fix    # remove '---' rule lines, convert **x** to \\textbf{x}
"""
import glob
import re
import sys

FILES = sorted(glob.glob('chap*.tex')) + ['DICTIONARY_TERMS_AND_SYMBOLS.tex', 'master_book_unified_quantum_gravity.tex']
CHECKS = {
    'markdown rule ---': re.compile(r'^---\s*$', re.M),
    'markdown **bold**': re.compile(r'\*\*([^*\n]+?)\*\*'),
    'placeholder TODO/TBD': re.compile(r'\b(TODO|TBD|FIXME)\b'),
    'unresolved ??': re.compile(r'\?\?'),
}


def main(fix: bool) -> int:
    total = 0
    for f in FILES:
        s = open(f, encoding='utf-8').read()
        for name, rx in CHECKS.items():
            hits = [s[:m.start()].count('\n') + 1 for m in rx.finditer(s)]
            if hits:
                total += len(hits)
                print(f'{f}: {name} at lines {hits}')
        if fix:
            new = re.sub(r'^---\s*\r?\n', '', s, flags=re.M)
            new = re.sub(r'\*\*([^*\n]+?)\*\*', r'\\textbf{\1}', new)
            if new != s:
                open(f, 'w', encoding='utf-8', newline='').write(new)
                print(f'  fixed {f}')
    print(f'{total} issue(s)')
    return 1 if total and not fix else 0


if __name__ == '__main__':
    sys.exit(main('--fix' in sys.argv))
