"""Lint do estilo da casa (CLAUDE.md, convenções 2 e 6) para os .tex publicáveis.

Barra, em texto que vai para o leitor:
  H1  histórico de versões ("earlier version", "withdrawn", "we correct", ...);
  H2  caminhos internos do projeto (audit/, _staging, Pesquisa_e_Testes, FILA.md, WORKPLAN, ...);
  H3  ênfase decorativa ("rigorously", "definitively", "rigorous proof");
  R1  ambiente theorem sem prova logo depois e sem citação no argumento opcional (aviso;
      vira erro com --estrito).

Comentários LaTeX (%) são ignorados. Para aceitar uma linha de propósito, termine-a com
`% lint-ok: <motivo>`.

Uso:
  python checagens/lint_estilo.py                       # capítulos, dicionário, declarações e master do livro
  python checagens/lint_estilo.py arquivo.tex [...]     # arquivos escolhidos
  python checagens/lint_estilo.py --estrito ...         # R1 também reprova
Saída 0 = limpo; 1 = achados que reprovam. Testes: python checagens/testes/test_checagens.py
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOK = ROOT / "unified_quantum_gravity_book"

H1 = re.compile(
    r"\b(earlier|previous|prior|first|old|older|original) (version|draft|release|edition)s?\b"
    r"|\bwithdrawn\b|\bretracted\b|\berratum\b"
    r"|\bwe (now )?correct(ed)?\b|\bcorrected (version|statement|proof|claim)\b"
    r"|\b(in|since) (version|v)\s?\d"
    r"|\bthis (claim|statement|result) (was|has been) (false|wrong|incorrect)\b",
    re.I)
H2 = re.compile(r"(?<![\w-])(audit/|_staging|Pesquisa_e_Testes|FILA\.md|WORKPLAN|CHANGELOG\.md|DIARIO\.md|BIFURCACOES)")
H3 = re.compile(r"\b(rigorously|definitively|rigorous proof)\b", re.I)
THM_ENVS = r"(theorem|thm)"
NEXT_BLOCK = re.compile(r"\\begin\{(theorem|thm|lemma|proposition|corollary|conjecture|definition)\}|\\(sub)*section\*?\{")

REGRAS = {
    "H1": "histórico de versões no texto: reescreva como matemática atual; o histórico vai para CHANGELOG/notas do Zenodo",
    "H2": "caminho interno do projeto: tire do texto publicável",
    "H3": "ênfase decorativa: o rótulo (Theorem/Conjecture/...) já diz o status",
    "R1": "Theorem sem \\begin{proof} logo depois e sem \\cite no argumento opcional: prove, cite ou troque o rótulo",
}


def sem_comentarios(linha):
    return re.sub(r"(?<!\\)%.*", "", linha)


def checar(caminho, estrito=False):
    texto = caminho.read_text(encoding="utf-8", errors="replace")
    linhas = texto.splitlines()
    achados = []
    na_bib = False
    for i, bruta in enumerate(linhas, 1):
        if re.search(r"%\s*lint-ok:", bruta):
            continue
        linha = sem_comentarios(bruta)
        if "\\begin{thebibliography}" in linha:
            na_bib = True
        if "\\end{thebibliography}" in linha:
            na_bib = False
        # na bibliografia, "Erratum" e "First Edition" são metadados de obras citadas
        regras = (("H2", H2),) if na_bib else (("H1", H1), ("H2", H2), ("H3", H3))
        for cod, rx in regras:
            m = rx.search(linha)
            if m:
                achados.append((cod, i, m.group(0), True))
    limpo = "\n".join(sem_comentarios(l) for l in linhas)
    for m in re.finditer(r"\\begin\{" + THM_ENVS + r"\}(\[[^\]]*\])?", limpo):
        opc = m.group(2) or ""
        if "\\cite" in opc:
            continue
        fim = limpo.find("\\end{" + m.group(1) + "}", m.end())
        if fim < 0:
            continue
        resto = limpo[fim:]
        prox = NEXT_BLOCK.search(resto)
        trecho = resto[: prox.start()] if prox else resto
        if "\\begin{proof}" not in trecho:
            n = limpo.count("\n", 0, m.start()) + 1
            if not re.search(r"%\s*lint-ok:", linhas[n - 1]):
                achados.append(("R1", n, m.group(0)[:60], estrito))
    return achados


def alvos_padrao():
    fs = sorted(BOOK.glob("chap[0-9][0-9]_*.tex"))
    fs = [f for f in fs if not f.name.startswith("chap14")]  # cap. 14 fora do master (F-52)
    for nome in ("DICTIONARY_TERMS_AND_SYMBOLS.tex", "declarations_chapter.tex", "appendix_results_index.tex",
                 "_single_source_prototype/official_master_structure.tex"):
        if (BOOK / nome).exists():
            fs.append(BOOK / nome)
    return fs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arquivos", nargs="*")
    ap.add_argument("--estrito", action="store_true")
    a = ap.parse_args()
    fs = [pathlib.Path(f) for f in a.arquivos] or alvos_padrao()
    reprova = 0
    avisos = 0
    for f in fs:
        for cod, n, trecho, bloqueia in checar(f, a.estrito):
            tipo = "ERRO " if bloqueia else "aviso"
            print(f"{tipo} {cod} {f.name}:{n}: «{trecho}» -> {REGRAS[cod]}")
            reprova += bloqueia
            avisos += not bloqueia
    print(f"lint_estilo: {len(fs)} arquivo(s), {reprova} erro(s), {avisos} aviso(s)")
    sys.exit(1 if reprova else 0)


if __name__ == "__main__":
    main()
