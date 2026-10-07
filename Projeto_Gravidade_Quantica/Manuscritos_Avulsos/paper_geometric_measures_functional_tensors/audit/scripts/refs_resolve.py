"""Reference resolution for Beyond the Spectrum II (2026-10-07).

Resolves every DOI of the bibliography (existing and proposed) through
Crossref, falling back to DataCite; resolves arXiv ids through the arXiv API;
compares title, first-author surname and year with the entry; runs a
negative control (a mutated DOI must not resolve, a wrong title must not
match). Then does a forward/backward citation traversal of three close
papers through OpenAlex.

No personal data is sent: generic User-Agent, no mailto parameter.
Run:  python refs_resolve.py > refs_resolve.out.txt
"""
import difflib
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
UA = "RefAudit/1.0"
TEX = Path(__file__).resolve().parents[2] / "paper_geometric_measures_functional_tensors.tex"
DEADLINE = time.time() + 15 * 60


def get(url, timeout=25):
    if time.time() > DEADLINE:
        raise TimeoutError("global deadline")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def resolve_doi(doi):
    q = urllib.parse.quote(doi, safe="/")
    for url, kind in ((f"https://api.crossref.org/works/{q}", "crossref"),
                      (f"https://api.datacite.org/dois/{q}", "datacite")):
        js = None
        for attempt in range(4):
            try:
                js = json.loads(get(url))
                break
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < 3:
                    time.sleep(5 * (attempt + 1))
                    continue
                if e.code == 404:
                    break
                return kind, None, f"HTTP {e.code}"
            except Exception as e:  # network trouble is not "invalid"
                return kind, None, f"ERR {e}"
        if js is None:
            continue
        if kind == "crossref":
            m = js["message"]
            title = " ".join(m.get("title") or [""])
            authors = [a.get("family", a.get("name", "")) for a in m.get("author", [])] or \
                      [a.get("family", a.get("name", "")) for a in m.get("editor", [])]
            year = None
            for k in ("published-print", "published-online", "issued", "published"):
                if m.get(k, {}).get("date-parts"):
                    year = m[k]["date-parts"][0][0]
                    break
            cont = " ".join(m.get("container-title") or [])
            isbn = m.get("ISBN", [])
            return kind, dict(title=title, authors=authors, year=year, cont=cont, isbn=isbn), "200"
        a = js["data"]["attributes"]
        title = a["titles"][0]["title"] if a.get("titles") else ""
        authors = [c.get("familyName", c.get("name", "")) for c in a.get("creators", [])]
        return kind, dict(title=title, authors=authors, year=a.get("publicationYear"),
                          cont=a.get("publisher", ""), isbn=[]), "200"
    return "none", None, "404"


def resolve_isbn_openlibrary(isbn):
    d = re.sub(r"\D", "", isbn)
    try:
        js = json.loads(get(f"https://openlibrary.org/isbn/{d}.json"))
        return js.get("title", ""), "200"
    except Exception as e:
        return None, f"ERR {e}"


def resolve_arxiv(aid):
    x = None
    for attempt in range(4):
        try:
            time.sleep(3)
            x = get(f"https://export.arxiv.org/api/query?id_list={aid}")
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                time.sleep(10 * (attempt + 1))
                continue
            return None, f"ERR {e}"
        except Exception as e:
            return None, f"ERR {e}"
    ents = re.findall(r"<entry>(.*?)</entry>", x, re.S)
    if not ents:
        return None, "no entry"
    t = re.search(r"<title>(.*?)</title>", ents[0], re.S)
    au = re.findall(r"<name>(.*?)</name>", ents[0])
    return dict(title=" ".join(t.group(1).split()) if t else "", authors=au), "200"


def norm(s):
    s = re.sub(r"\\[a-zA-Z]+|[{}\\'`^\"~]", "", s)
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()


def ratio(a, b):
    return difflib.SequenceMatcher(None, " ".join(norm(a)), " ".join(norm(b))).ratio()


def parse_bib(tex):
    body = tex.split(r"\begin{thebibliography}")[1].split(r"\end{thebibliography}")[0]
    items = re.split(r"\\bibitem\{", body)[1:]
    out = {}
    for it in items:
        key = it.split("}", 1)[0]
        rest = it.split("}", 1)[1]
        title = re.search(r"\\emph\{(.*?)\}\s*,", rest, re.S)
        doi = re.search(r"doi\.org/([^}\s]+)\}", rest)
        arx = re.search(r"arXiv[:~ ]*\\href\{https://arxiv\.org/abs/([^}]+)\}", rest) or \
              re.search(r"arxiv\.org/abs/([^}\s]+)\}", rest)
        isbn = re.search(r"ISBN[:~ ]*([0-9-]{13,17})", rest)
        authors = rest.strip().split("\n", 1)[0]
        year = re.findall(r"\b(1[89]\d\d|20\d\d)\b", rest)
        out[key] = dict(title=" ".join(title.group(1).split()) if title else "",
                        doi=doi.group(1) if doi else None,
                        arxiv=arx.group(1) if arx else None,
                        isbn=isbn.group(1) if isbn else None,
                        authors=authors, years=year)
    return out


def isbn13_ok(s):
    d = re.sub(r"\D", "", s)
    if len(d) != 13:
        return False
    tot = sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(d[:12]))
    return (10 - tot % 10) % 10 == int(d[12])


def main():
    tex = TEX.read_text(encoding="utf-8")
    bib = parse_bib(tex)
    cited = set()
    for grp in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}", tex):
        cited.update(k.strip() for k in grp.split(","))
    print(f"bibitems: {len(bib)}   cited keys: {len(cited)}")
    print("cited but missing:", sorted(cited - set(bib)) or "none")
    print("bibitems never cited:", sorted(set(bib) - cited) or "none")
    print()
    n_pass = n_check = n_fail = 0
    for key, e in sorted(bib.items()):
        line = f"{key}"
        if e["doi"]:
            kind, m, st = resolve_doi(e["doi"])
            if m is None:
                print(f"FAIL {line}: DOI {e['doi']} -> {kind} {st}")
                n_fail += 1
                continue
            r = ratio(e["title"], m["title"])
            surname = (m["authors"][0] if m["authors"] else "")
            au_ok = (not surname) or any(t in norm(e["authors"]) for t in norm(surname))
            yr_ok = (m["year"] is None) or str(m["year"]) in e["years"] or \
                any(abs(int(y) - int(m["year"])) <= 1 for y in e["years"])
            ok = (r >= 0.8 or norm(m["title"])[:2] == norm(e["title"])[:2]) and au_ok and yr_ok
            tag = "PASS" if ok else "CHECK"
            n_pass += ok
            n_check += (not ok)
            print(f"{tag} {line}: {e['doi']} [{kind}]")
            print(f"     tex: {e['title'][:110]}")
            print(f"     reg: {m['title'][:110]} | {m['authors'][:3]} | {m['year']} | {m['cont'][:60]}"
                  f" | title ratio {r:.2f} author_ok={au_ok} year_ok={yr_ok}")
            if m.get("isbn"):
                print(f"     registry ISBN: {m['isbn']}")
        else:
            print(f"NODOI {line}")
            if e["isbn"]:
                t, st = resolve_isbn_openlibrary(e["isbn"])
                print(f"     Open Library ISBN {e['isbn']}: {st} | {t} | title ratio "
                      f"{ratio(e['title'], t or ''):.2f}")
        if e["arxiv"]:
            am, st = resolve_arxiv(e["arxiv"])
            if am:
                print(f"     arXiv {e['arxiv']}: {am['title'][:100]} | ratio {ratio(e['title'], am['title']):.2f}")
            else:
                print(f"     arXiv {e['arxiv']}: {st}")
        if e["isbn"]:
            print(f"     ISBN {e['isbn']} checksum {'OK' if isbn13_ok(e['isbn']) else 'BAD'}")
        time.sleep(0.15)
    print(f"\nsummary: PASS {n_pass}  CHECK {n_check}  FAIL {n_fail}")

    # negative controls
    print("\nNEGATIVE CONTROLS")
    kind, m, st = resolve_doi("10.1007/BF01218391x9")
    print("mutated DOI 10.1007/BF01218391x9 ->", st, "(expected 404)")
    print("wrong-title ratio (Connes 1988 vs McCann title):",
          f"{ratio('The action functional in non-commutative geometry', 'A convexity principle for interacting gases'):.2f}",
          "(expected < 0.8)")
    print("ISBN checksum of mutated 978-0-12-185860-6:", isbn13_ok("978-0-12-185860-6"), "(expected False)")

    # traversal
    print("\nCITATION TRAVERSAL (OpenAlex)")
    seeds = {"memoli2011gromov": "10.1007/s10208-011-9093-5",
             "chowdhury2019gromov": "10.1093/imaiai/iaz026",
             "atienza2020stability": "10.1016/j.patcog.2020.107509"}
    for key, doi in seeds.items():
        try:
            w = json.loads(get(f"https://api.openalex.org/works/doi:{doi}"))
        except Exception as ex:
            print(key, "ERR", ex)
            continue
        print(f"\n[{key}] {w['display_name']} | cited_by={w['cited_by_count']} | refs={len(w['referenced_works'])}")
        ids = "|".join(r.split("/")[-1] for r in w["referenced_works"][:50])
        if ids:
            try:
                rs = json.loads(get(f"https://api.openalex.org/works?filter=openalex_id:{ids}&per-page=50"
                                    "&select=display_name,publication_year,cited_by_count,doi"))
                top = sorted(rs["results"], key=lambda r: -r["cited_by_count"])[:8]
                print("  backward (most cited refs):")
                for r in top:
                    print(f"    {r['publication_year']} {r['cited_by_count']:6d} {r['display_name'][:90]} {r['doi']}")
            except Exception as ex:
                print("  backward ERR", ex)
        wid = w["id"].split("/")[-1]
        try:
            fs = json.loads(get(f"https://api.openalex.org/works?filter=cites:{wid},from_publication_date:2023-01-01"
                                "&sort=cited_by_count:desc&per-page=10&select=display_name,publication_year,cited_by_count,doi"))
            print(f"  forward since 2023: {fs['meta']['count']} works; most cited:")
            for r in fs["results"]:
                print(f"    {r['publication_year']} {r['cited_by_count']:5d} {r['display_name'][:90]} {r['doi']}")
        except Exception as ex:
            print("  forward ERR", ex)


if __name__ == "__main__":
    main()
