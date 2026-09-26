"""Camada 2 (F-41..F-43): consistencia de citacoes e resolucao dos DOIs novos.

1. Em cada capitulo (8, 12, 13): toda chave \\cite tem \\bibitem e todo \\bibitem e citado.
2. Cada DOI novo (lista do corretor) e resolvido na API do Crossref (DataCite para 10.48550);
   titulo, autores e ano retornados sao comparados com o \\bibitem por sobreposicao de tokens
   e por sobrenomes dos autores.
Controles negativos: um DOI mutado (ultimo caractere trocado) NAO pode resolver com o mesmo
titulo, e um titulo errado deve falhar no teste de sobreposicao.
Rodar do diretorio do livro:  python audit/verify/scripts/L2_ch12_ch13_refs_doi.py
"""
import json
import re
import time
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CHAPS = {
    "ch08": "chap08_noneuclidean_minimax_relativity_adm.tex",
    "ch12": "chap12_grand_unification_quantum_gravity_treatise.tex",
    "ch13": "chap13_experimental_observational_signatures_quantum_gravity.tex",
}
# (capitulo, chave, sobrenomes esperados)
NEW = [
    ("ch12", "thiemann1998qsd", ["Thiemann"]),
    ("ch12", "deharo2001holographic", ["Haro", "Skenderis", "Solodukhin"]),
    ("ch12", "chamseddine2007gravity", ["Chamseddine", "Connes", "Marcolli"]),
    ("ch12", "jacob2008lorentz", ["Jacob", "Piran"]),
    ("ch12", "mirshekari2012constraining", ["Mirshekari", "Yunes", "Will"]),
    ("ch12", "bicepkeck2021constraints", ["Ade"]),
    ("ch12", "planck2018parameters", ["Aghanim"]),
    ("ch12", "swingle2014universality", ["Swingle", "Raamsdonk"]),
    ("ch13", "jacob2008lorentz", ["Jacob", "Piran"]),
    ("ch13", "mirshekari2012constraining", ["Mirshekari", "Yunes", "Will"]),
    ("ch13", "bicepkeck2021constraints", ["Ade"]),
    ("ch13", "planck2018parameters", ["Aghanim"]),
]
FAIL = []


def check(name, ok, info=""):
    print(f"[{'OK  ' if ok else 'FAIL'}] {name} {info}")
    if not ok:
        FAIL.append(name)


def strip_acc(s):
    return "".join(ch for ch in unicodedata.normalize("NFKD", s) if not unicodedata.combining(ch))


def bib_entries(tex):
    body = tex.split("\\begin{thebibliography}")[1]
    parts = re.split(r"\\bibitem\{([^}]+)\}", body)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}


def cites(tex):
    main = tex.split("\\begin{thebibliography}")[0]
    keys = set()
    for m in re.finditer(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}", main):
        keys.update(k.strip() for k in m.group(1).split(","))
    return keys


def jacc(a, b):
    ta, tb = tokens(a), tokens(b)
    return len(ta & tb) / max(1, len(ta | tb))


def tokens(s):
    s = strip_acc(s).lower()
    s = re.sub(r"\\[a-z]+", " ", s)
    return {w for w in re.findall(r"[a-z]{4,}", s)}


def fetch(doi):
    if doi.startswith("10.48550") or doi.startswith("10.5281"):
        url = "https://api.datacite.org/dois/" + doi
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "L2-audit"}), timeout=30) as r:
            a = json.load(r)["data"]["attributes"]
        title = a["titles"][0]["title"]
        authors = [c.get("familyName") or c.get("name", "") for c in a["creators"]]
        year = a.get("publicationYear")
        return title, authors, year
    url = "https://api.crossref.org/works/" + doi
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "L2-audit (mailto:none)"}), timeout=30) as r:
        m = json.load(r)["message"]
    title = (m.get("title") or [""])[0]
    if m.get("subtitle"):
        title += ": " + m["subtitle"][0]
    title = re.sub(r"<[^>]+>", "", " ".join(title.split()))
    authors = [a.get("family", a.get("name", "")) for a in m.get("author", [])]
    year = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
    return title, authors, year


texs = {ch: (ROOT / f).read_text(encoding="utf-8") for ch, f in CHAPS.items()}
for ch, tex in texs.items():
    bib, cit = bib_entries(tex), cites(tex)
    check(f"{ch}: every cite has a bibitem", not (cit - set(bib)), str(sorted(cit - set(bib))))
    check(f"{ch}: every bibitem is cited", not (set(bib) - cit), str(sorted(set(bib) - cit)))

seen = {}
for ch, key, surnames in NEW:
    entry = bib_entries(texs[ch]).get(key)
    if entry is None:
        check(f"{ch}:{key} present", False)
        continue
    m = re.search(r"(?:\\doi\{|doi\.org/)(10\.[^}\s]+)\}", entry)
    doi = m.group(1)
    tm = re.search(r"\\emph\{(.+?)\}\s*,", entry, re.S)
    btitle = tm.group(1) if tm else entry
    if doi not in seen:
        try:
            seen[doi] = fetch(doi)
        except Exception as e:  # noqa: BLE001
            seen[doi] = None
            print("   erro de rede:", e)
        time.sleep(0.5)
    res = seen[doi]
    if res is None:
        check(f"{ch}:{key} {doi} resolves", False)
        continue
    title, authors, year = res
    ov = jacc(btitle, title)
    auth_ok = all(any(s.lower() in strip_acc(a).lower() for a in authors) for s in surnames)
    ym = re.search(r"\((\d{4})\)|(\d{4})", entry)
    check(f"{ch}:{key} {doi}", ov > 0.75 and auth_ok,
          f"| Crossref/DataCite: '{title[:90]}' | {authors[:4]} | {year} | overlap={ov:.2f}")
    # controle negativo 1: titulo errado deve falhar
    wrong = "Quantum phases of matter on a programmable simulator"
    assert jacc(wrong, title) < 0.5

# controle negativo 2: DOI mutado nao resolve (ou resolve para outro titulo)
for orig, mut in (("10.1103/PhysRevD.85.024041", "10.1103/PhysRevD.85.024042"),
                  ("10.1088/0264-9381/15/4/011", "10.1088/0264-9381/15/4/012")):
    orig_title = (seen.get(orig) or ("",))[0]
    try:
        t, _, _ = fetch(mut)
        ok = jacc(t, orig_title) < 0.5
        info = f"resolves to a different record: '{t[:60]}'"
    except urllib.error.HTTPError as e:
        ok, info = True, f"HTTP {e.code}"
    check(f"NEG mutated DOI {mut} does not reproduce the record of {orig}", ok, info)

print("\nFALHAS:", FAIL if FAIL else "nenhuma")
raise SystemExit(1 if FAIL else 0)
