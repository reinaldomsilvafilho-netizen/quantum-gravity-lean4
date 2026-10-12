"""Per chapter: macros defined in the preamble and used in the body, and symbols that occur in
display math (Greek letters, \\mathcal/\\mathbb/\\mathbf/\\mathfrak/\\operatorname tokens, sub-
scripted Latin symbols). Compare with what the Dictionary mentions. Print, per chapter, the most
frequent display symbols ABSENT from the Dictionary, and every chapter macro absent from it.
Usage: python symbol_scan.py > symbol_scan_report.txt"""
import re
from collections import Counter
from pathlib import Path

BOOK = Path(r"C:\Users\monar\Documents\antigravity\resilient-turing\Projeto_Gravidade_Quantica\unified_quantum_gravity_book")
DICT = (BOOK / "DICTIONARY_TERMS_AND_SYMBOLS.tex").read_text(encoding="utf-8")

DISPLAY = re.compile(r"\\begin\{(equation|align|gather|multline|eqnarray)\*?\}(.*?)\\end\{\1\*?\}|\\\[(.*?)\\\]|\$\$(.*?)\$\$", re.S)
INLINE = re.compile(r"(?<!\\)\$(?!\$)(.+?)(?<!\\)\$", re.S)
TOK = re.compile(r"\\(?:mathcal|mathbb|mathbf|mathfrak|mathscr|boldsymbol|operatorname)\{[^{}]+\}"
                 r"|\\(?:alpha|beta|gamma|delta|epsilon|varepsilon|zeta|eta|theta|vartheta|iota|kappa|lambda|mu|nu|xi|pi|rho|sigma|tau|upsilon|phi|varphi|chi|psi|omega|Gamma|Delta|Theta|Lambda|Xi|Pi|Sigma|Phi|Psi|Omega)(?:_\{[^{}]+\}|_[A-Za-z0-9])?(?:\^\{?\*\}?)?"
                 r"|(?<![\\A-Za-z])[A-Za-z](?:_\{[^{}]+\}|_[A-Za-z])")
NEWCMD = re.compile(r"\\(?:newcommand|providecommand|renewcommand|DeclareMathOperator)\*?\{?\\([A-Za-z]+)\}?")
SKIP = {"left", "right", "frac", "mathrm", "text", "label", "quad", "qquad", "cdot", "sum", "int", "end", "begin"}


def norm(tok):
    return re.sub(r"\s+", "", tok)


def in_dict(tok):
    t = norm(tok)
    d = norm(DICT)
    if t in d:
        return True
    base = re.sub(r"_.*", "", t)  # e.g. \kappa_W -> \kappa
    return False if base == t else (base + "_") in d or (base + "^") in d and False


def main():
    for f in sorted(BOOK.glob("chap[01][0-9]_*.tex")):
        ch = int(f.name[4:6])
        if ch > 13:
            continue
        text = f.read_text(encoding="utf-8")
        text = re.sub(r"(?<!\\)%.*", "", text)
        pre, _, body = text.partition("\\begin{document}")
        macros = set(NEWCMD.findall(pre))
        used = Counter(m for m in re.findall(r"\\([A-Za-z]+)", body) if m in macros)
        disp = Counter()
        for m in DISPLAY.finditer(body):
            seg = next(g for g in m.groups()[1:] if g)
            disp.update(norm(t) for t in TOK.findall(seg))
        inl = Counter()
        for m in INLINE.finditer(body):
            inl.update(norm(t) for t in TOK.findall(m.group(1)))
        tot = disp + inl
        missing = [(t, c) for t, c in tot.most_common() if not in_dict(t) and c >= 3]
        print(f"=== ch{ch:02d} {f.name}")
        print("  macros used and absent from Dictionary:",
              ", ".join(f"\\{k}({v})" for k, v in used.most_common() if ("\\" + k) not in DICT and k not in SKIP))
        print("  frequent symbols absent (display+inline count >= 3, top 30):")
        print("   ", "  ".join(f"{t}({c})" for t, c in missing[:30]))


if __name__ == "__main__":
    main()
