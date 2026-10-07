"""L2r: spot-check 10 randomly chosen ADDED references (seed 20261007).

Usage: python L2r_refs_sample.py   (run from this scripts folder; the paper folder is ../..)
Added = bibitem keys in the current .tex minus keys in the pre-reference-audit backup.
For each sampled key: resolve DOI (Crossref, fallback DataCite) and/or arXiv id (arXiv API),
print metadata, title similarity with the bibitem, the abstract (Crossref, OpenAlex or
arXiv), and every sentence of the .tex that cites the key, for a human reading.
Generic User-Agent; no e-mail, no name, no mailto.
Negative controls: a fake DOI must not resolve; a wrong title must score low.
Writes L2r_refs_sample.out.txt next to this file. Exit code = resolver failures.
"""
import json
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent.parent
ARQ = PAPER.parent.parent / "_arquivo"
PRE = {
    "paper_functorial_tensor_field_theory": "backup_tex_2026-10-06/Manuscritos_Avulsos/paper_functorial_tensor_field_theory/paper_functorial_tensor_field_theory_refs.tex",
    "paper_functional_realizations": "backup_tex_2026-10-06/Manuscritos_Avulsos/paper_functional_realizations/paper_functional_realizations_refs.tex",
    "paper_geometric_measures_functional_tensors": "backup_tex_2026-10-07/Manuscritos_Avulsos/paper_geometric_measures_functional_tensors/paper_geometric_measures_functional_tensors_refs.tex",
    "paper_beyond_the_spectrum_3": "backup_tex_2026-10-07/Manuscritos_Avulsos/paper_beyond_the_spectrum_3/paper_beyond_the_spectrum_3_refs.tex",
}
UA = {"User-Agent": "reference-check/1.0 (generic)"}
out = []


def log(s=""):
    out.append(s)
    print(s.encode("ascii", "replace").decode())


def get(url, accept=None, tries=3):
    h = dict(UA)
    if accept:
        h["Accept"] = accept
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and k + 1 < tries:
                time.sleep(3 * (k + 1))
                continue
            return e.code, ""
        except Exception as e:  # noqa: BLE001
            if k + 1 < tries:
                time.sleep(2)
                continue
            return -1, str(e)
    return -1, ""


def bibitems(tex):
    body = tex.split("\\begin{thebibliography}")[1].split("\\end{thebibliography}")[0]
    parts = re.split(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", body)
    return {parts[i].strip(): parts[i + 1].strip() for i in range(1, len(parts), 2)}


def words(s):
    s = re.sub(r"\\[a-zA-Z]+|[{}$\\]", " ", s or "")
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) > 2}


def sim(a, b):
    A, B = words(a), words(b)
    return len(A & B) / max(1, len(B))


def strip_tags(s):
    return re.sub(r"<[^>]+>", " ", s or "").strip()


def crossref(doi):
    st, txt = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
    if st == 200:
        m = json.loads(txt)["message"]
        yr = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
        au = "; ".join(f"{a.get('given','')} {a.get('family','')}".strip() for a in m.get("author", [])[:6])
        return {"src": "Crossref", "title": " ".join(m.get("title", [])), "authors": au, "year": yr,
                "venue": " ".join(m.get("container-title", [])), "volume": m.get("volume"),
                "page": m.get("page"), "abstract": strip_tags(m.get("abstract"))}
    st, txt = get("https://api.datacite.org/dois/" + urllib.parse.quote(doi))
    if st == 200:
        a = json.loads(txt)["data"]["attributes"]
        desc = " ".join(d.get("description", "") for d in a.get("descriptions", []))
        return {"src": "DataCite", "title": " ".join(t["title"] for t in a.get("titles", [])),
                "authors": "; ".join(c.get("name", "") for c in a.get("creators", [])[:6]),
                "year": a.get("publicationYear"), "venue": a.get("publisher"), "volume": None,
                "page": None, "abstract": strip_tags(desc)[:1500]}
    return None


def openalex_abstract(doi):
    st, txt = get("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi))
    if st != 200:
        return ""
    inv = json.loads(txt).get("abstract_inverted_index") or {}
    pos = {}
    for w, ps in inv.items():
        for p in ps:
            pos[p] = w
    return " ".join(pos[k] for k in sorted(pos))


def arxiv(aid):
    st, txt = get("http://export.arxiv.org/api/query?id_list=" + aid)
    if st != 200 or "<entry>" not in txt:
        return None
    e = txt.split("<entry>")[1]
    t = re.search(r"<title>(.*?)</title>", e, re.S)
    s = re.search(r"<summary>(.*?)</summary>", e, re.S)
    au = re.findall(r"<name>(.*?)</name>", e)
    pub = re.search(r"<published>(\d{4})", e)
    if not t:
        return None
    return {"src": "arXiv", "title": " ".join(t.group(1).split()), "authors": "; ".join(au[:6]),
            "year": pub.group(1) if pub else None, "venue": "arXiv", "volume": None, "page": None,
            "abstract": " ".join(s.group(1).split()) if s else ""}


def cites(tex, key):
    body = tex.split("\\begin{thebibliography}")[0]
    res = []
    for m in re.finditer(r"\\cite[pt]?(?:\[[^\]]*\])?\{([^}]*)\}", body):
        if key in [k.strip() for k in m.group(1).split(",")]:
            a = max(body.rfind(". ", 0, m.start()), body.rfind("\n\n", 0, m.start()), m.start() - 600)
            b = body.find(". ", m.end())
            b = len(body) if b < 0 else min(b + 1, m.end() + 600)
            res.append(" ".join(body[a:b].split()))
    return res


def main():
    name = PAPER.name
    tex = (PAPER / f"{name}.tex").read_text(encoding="utf-8")
    pre = (ARQ / PRE[name]).read_text(encoding="utf-8")
    cur, old = bibitems(tex), bibitems(pre)
    added = sorted(set(cur) - set(old))
    log(f"paper: {name}; bibitems now {len(cur)}, before {len(old)}, added {len(added)}, removed {sorted(set(old)-set(cur))}")
    sample = random.Random(20261007).sample(added, min(10, len(added)))
    log(f"sample (seed 20261007): {sample}")
    fails = 0
    # negative controls
    if crossref("10.9999/definitely.not.a.doi.20261007") is not None:
        fails += 1
        log("NEG FAIL: fake DOI resolved")
    else:
        log("neg control: fake DOI does not resolve (ok)")
    log(f"neg control: title similarity of a wrong title = {sim('Quantum chromodynamics on the lattice', 'Graph limits and cut distance'):.2f} (must be < 0.5)")
    for key in sample:
        raw = cur[key]
        log("\n" + "=" * 100)
        log(f"KEY {key}\nBIBITEM: {' '.join(raw.split())}")
        doi = re.search(r"10\.\d{4,9}/[^\s}\\,]+", raw)
        aid = re.search(r"(?:arXiv[:\s~]*|abs/)((?:\d{4}\.\d{4,5})|(?:[a-z\-]+(?:\.[A-Z]{2})?/\d{7}))", raw)
        isbn = re.search(r"ISBN[:~\s]*([0-9Xx\-]{10,17})", raw)
        recs = []
        if doi:
            d = doi.group(0).rstrip(".")
            r = crossref(d)
            log(f"DOI {d}: {'resolved via ' + r['src'] if r else 'NOT RESOLVED'}")
            if r:
                if not r["abstract"]:
                    r["abstract"] = openalex_abstract(d)
                recs.append(r)
            elif not aid:
                fails += 1
        if aid:
            r = arxiv(aid.group(1))
            log(f"arXiv {aid.group(1)}: {'resolved' if r else 'NOT RESOLVED'}")
            if r:
                recs.append(r)
            else:
                fails += 1
        if isbn:
            log(f"ISBN {isbn.group(1)} (not resolved here)")
        if not (doi or aid):
            log("no DOI/arXiv id")
        for r in recs:
            log(f"[{r['src']}] title: {r['title']}\n  authors: {r['authors']}\n  year: {r['year']} venue: {r['venue']} vol {r['volume']} p {r['page']}"
                f"\n  title-in-bibitem similarity: {sim(raw, r['title']):.2f}")
            log(f"  abstract: {(r['abstract'] or '(none)')[:1800]}")
        for c in cites(tex, key):
            log(f"  CITED AT: {c}")
        time.sleep(1)
    log(f"\nresolver failures={fails}")
    (HERE / "L2r_refs_sample.out.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    return fails


if __name__ == "__main__":
    sys.exit(main())
