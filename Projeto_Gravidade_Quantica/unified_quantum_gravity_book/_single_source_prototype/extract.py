#!/usr/bin/env python3
"""F-19 prototype: generate gen/chNN_body.tex from the body of each original
chapter source, WITHOUT modifying the originals. Read-only on chapNN_*.tex.

Strategy per chapter:
  - Take everything between \begin{document} and \end{document}.
  - Drop \maketitle (the master already opens a \chapter{...}).
  - Wrap \begin{abstract}...\end{abstract} content in a manual "Abstract"
    block (book class has no abstract env by default; common preamble
    defines one, see common_preamble.tex).
  - Prefix every \label{...} and every \ref{...}/\eqref{...}/\cref{...}/
    \Cref{...}/\autoref{...} with "chNN:" to avoid cross-chapter collisions.
  - Prefix every \bibitem{key} and \cite{key1,key2,...} (cite/citet/citep/
    nocite too) the same way, so each chapter keeps its own
    thebibliography block with globally unique keys.
"""
import re
from pathlib import Path

BOOK_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent / "gen"
GEN_DIR.mkdir(exist_ok=True)

REF_CMDS = ["ref", "eqref", "cref", "Cref", "autoref", "nameref"]
CITE_CMDS = ["cite", "citet", "citep", "citeauthor", "citeyear", "nocite"]


def prefix_keys(body: str, tag: str) -> str:
    # \label{foo} -> \label{ch01:foo}
    body = re.sub(r"\\label\{([^}]*)\}", lambda m: f"\\label{{{tag}:{m.group(1)}}}", body)
    # \ref{foo}, \eqref{foo}, ... (single key)
    for cmd in REF_CMDS:
        body = re.sub(
            rf"\\{cmd}\{{([^}}]*)\}}",
            lambda m, cmd=cmd: f"\\{cmd}{{{tag}:{m.group(1)}}}",
            body,
        )
    # \bibitem{foo}
    body = re.sub(r"\\bibitem\{([^}]*)\}", lambda m: f"\\bibitem{{{tag}:{m.group(1)}}}", body)
    # \cite{foo,bar} or \cite[pre][post]{foo,bar} (comma list, optional args)
    for cmd in CITE_CMDS:
        def repl(m, cmd=cmd):
            opt = m.group(1) or ""
            keys = [k.strip() for k in m.group(2).split(",")]
            return f"\\{cmd}{opt}{{" + ",".join(f"{tag}:{k}" for k in keys) + "}"
        body = re.sub(rf"\\{cmd}((?:\[[^\]]*\]){{0,2}})\{{([^}}]*)\}}", repl, body)
    return body


def _skip_balanced(text: str, i: int, open_c: str, close_c: str) -> int:
    """text[i] == open_c. Return index just past the matching close_c."""
    depth = 0
    n = len(text)
    while i < n:
        if text[i] == open_c:
            depth += 1
        elif text[i] == close_c:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return n


def remove_titling_command(text: str, cmd: str) -> str:
    """Remove every occurrence of \\cmd[opt]{arg} or \\cmd{arg}, where opt/arg
    may themselves contain balanced {..} (e.g. \\texorpdfstring). Some
    amsart-class chapters place \\title/\\author/\\address/\\email/\\date
    AFTER \\begin{document} (chap07-11) rather than in the preamble
    (chap01-03); book's own \\chapter{} and title page already provide
    this information, so these commands are dropped from every body.
    """
    result = text
    while True:
        m = re.search(rf"\\{cmd}\b", result)
        if not m:
            break
        start = m.start()
        j = m.end()
        # optional [..] argument(s)
        while j < len(result) and result[j] == "[":
            j = _skip_balanced(result, j, "[", "]")
        # mandatory {..} argument
        if j < len(result) and result[j] == "{":
            j = _skip_balanced(result, j, "{", "}")
        result = result[:start] + result[j:]
    return result


def extract_body(text: str) -> str:
    m = re.search(r"\\begin\{document\}(.*)\\end\{document\}", text, re.S)
    if not m:
        raise ValueError("no \\begin{document}...\\end{document} found")
    body = m.group(1)
    # drop \maketitle (book \chapter already provides the heading)
    body = re.sub(r"\\maketitle\s*", "", body)
    # some chapters (chap07-11) place \title/\author/\address/\email/\date
    # AFTER \begin{document} rather than in the preamble; strip them from
    # the body too (book's \chapter{} + title page already cover this).
    # 2026-10-11: \thanks (CAPES funding footnote) is dropped too: chap08
    # places it AFTER \begin{document} (chap11/12 place it in the preamble,
    # outside the extracted body, so they were never affected). Left alone,
    # \thanks{...} survives \maketitle's removal and typesets as an orphan
    # footnote mark "1" at the top of the chapter in the master (the mark
    # has no \maketitle/title to attach to). The book already carries the
    # funding statement once, via declarations_chapter.tex's single
    # "Funding." paragraph, so dropping the per-chapter \thanks loses no
    # information from the master.
    for cmd in ("title", "author", "address", "email", "date", "pacs", "affiliation", "thanks"):
        body = remove_titling_command(body, cmd)
    # turn \begin{abstract}...\end{abstract} into a manual block
    body = re.sub(
        r"\\begin\{abstract\}(.*?)\\end\{abstract\}",
        lambda m: "\\begin{chapterabstract}" + m.group(1) + "\\end{chapterabstract}",
        body,
        flags=re.S,
    )
    # drop \keywords{...} and \subjclass[...]{...} (amsart-only, no book equivalent needed for prototype)
    body = re.sub(r"\\keywords\{[^}]*\}", "", body)
    body = re.sub(r"\\subjclass(\[[^\]]*\])?\{[^}]*\}", "", body)
    # 2026-10-10: drop each standalone chapter's own \tableofcontents (and
    # \listoffigures/\listoftables), together with the \newpage/\clearpage
    # that only follows it. In the book they printed an empty "Contents" page
    # after every chapter opening and set the running head to "CONTENTS".
    # The master's own \tableofcontents lives in official_master_structure.tex
    # and is not touched here.
    body = re.sub(
        r"\\(?:tableofcontents|listoffigures|listoftables)\b[ \t]*\n?"
        r"(?:\s*\\(?:newpage|clearpage)\b[ \t]*\n?)?",
        "",
        body,
    )
    # 2026-10-10: the book carries ONE Declarations section, \input once from
    # declarations_chapter.tex in the front matter of
    # official_master_structure.tex. Drop the per-chapter copy from every body
    # (the standalone chapter PDFs keep theirs; chapNN_*.tex is untouched).
    body = re.sub(r"[ \t]*\\input\{(?:\.\./)?declarations_chapter(?:\.tex)?\}[ \t]*\n?", "", body)
    # revtex4-2's \ruledtabular (chap13 only) has no book-class equivalent.
    # Textually rewrite \begin{ruledtabular}\begin{tabular}{spec} ... \end
    # {tabular}\end{ruledtabular} into a plain centered booktabs table
    # (\toprule/\bottomrule around the SAME rows; the chapter's own
    # \midrule between header and body is untouched). Purely textual, at
    # extraction time, so no fragile macro-patching is needed at runtime.
    body = re.sub(
        r"\\begin\{ruledtabular\}\s*\\begin\{tabular\}(\{[^}]*\})",
        r"\\begin{center}\n\\begin{tabular}\1\n\\toprule",
        body,
    )
    body = re.sub(
        r"\\end\{tabular\}\s*\\end\{ruledtabular\}",
        r"\\bottomrule\n\\end{tabular}\n\\end{center}",
        body,
    )
    return body


MACRO_DEF_RE = re.compile(
    r"\\(providecommand|newcommand|renewcommand)\{(\\[A-Za-z]+)\}(\[[0-9]\])?\{(.*?)\}\s*(?=\n|\\[a-zA-Z])",
    re.S,
)
DECLARE_OP_RE = re.compile(r"\\DeclareMathOperator\*?\{(\\[A-Za-z]+)\}\{([^}]*)\}")


def harvest_macros(chap_files):
    """Scan every chapter's PREAMBLE (before \\begin{document}) for macro
    definitions and write ONE deduplicated gen/common_macros.tex, so the
    prototype's shared preamble does not need to be hand-maintained.
    First definition of a given name wins; every emitted definition uses
    \\providecommand so loading order never raises 'already defined'.
    """
    seen = {}
    order = []
    for f in chap_files:
        text = f.read_text(encoding="utf-8")
        pre = text.split("\\begin{document}", 1)[0]
        for kind, name, arity, body in MACRO_DEF_RE.findall(pre):
            if name not in seen:
                seen[name] = (arity, body.strip())
                order.append(name)
        for name, body in DECLARE_OP_RE.findall(pre):
            key = name + "@op"
            if key not in seen:
                seen[key] = ("@op", body.strip())
                order.append(key)
    lines = [
        "% AUTO-GENERATED by extract.py from the union of chapter preambles.",
        "% Do not edit chapNN_*.tex; re-run extract.py to refresh this file.",
    ]
    for name in order:
        arity, body = seen[name]
        if arity == "@op":
            real_name = name[: -len("@op")]
            lines.append(f"\\providecommand{real_name}{{}}")
            lines.append(f"\\renewcommand{real_name}{{\\operatorname{{{body}}}}}")
        else:
            arity_s = arity or ""
            lines.append(f"\\providecommand{{{name}}}{arity_s}{{{body}}}")
    out = GEN_DIR / "common_macros.tex"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out, len(order)


def main():
    chap_files = sorted(BOOK_DIR.glob("chap[01][0-9]_*.tex"))
    macro_file, n_macros = harvest_macros(chap_files)
    print(f"{macro_file.name}: {n_macros} unique macros harvested from preambles")
    report = []
    for f in chap_files:
        tag = f.name.split("_")[0]  # chNN
        text = f.read_text(encoding="utf-8")
        try:
            body = extract_body(text)
        except ValueError as e:
            report.append(f"{f.name}: SKIP ({e})")
            continue
        body = prefix_keys(body, tag)
        out = GEN_DIR / f"{tag}_body.tex"
        out.write_text(body, encoding="utf-8")
        report.append(f"{f.name}: OK -> {out.name} ({len(body)} bytes)")
    print("\n".join(report))


if __name__ == "__main__":
    main()
