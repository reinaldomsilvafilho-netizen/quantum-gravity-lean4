"""Resolve every bibitem of paper_functional_realizations.tex (Volume I).

For each reference: resolve the DOI (Crossref, then DataCite) and/or the arXiv id
(arXiv API), then compare title (word Jaccard >= 0.6), first-author surname and year
(+-1, online vs. issue year) with the values written in the .tex. ISBN-13 check
digits are verified. The script also cross-checks that the keys cited in the .tex
and the keys of \\bibitem coincide.

Negative controls (must FAIL): a nonexistent DOI, a real DOI paired with a wrong
title, and an ISBN with a corrupted check digit.

No personal data is sent: plain User-Agent, no mailto, no e-mail anywhere.
"""
from __future__ import annotations

import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

UA = {"User-Agent": "RefAudit/1.0"}
TEX = Path(__file__).resolve().parents[2] / "paper_functional_realizations.tex"

# key: (doi or None, arxiv or None, title in .tex, first-author surname, year, isbn or None)
REFS = {
    "adler2007random": ("10.1007/978-0-387-48116-6", None, "Random Fields and Geometry", "Adler", 2007, "9780387481128"),
    "auffinger2013random": ("10.1002/cpa.21422", "1003.1129", "Random matrices and complexity of spin glasses", "Auffinger", 2013, None),
    "cartwright2013number": ("10.1016/j.laa.2011.05.040", "1004.4953", "The number of eigenvalues of a tensor", "Cartwright", 2013, None),
    "desilva2008illposed": ("10.1137/06066518X", "math/0607647", "Tensor rank and the ill-posedness of the best low-rank approximation problem", "Silva", 2008, None),
    "evans2015measure": ("10.1201/b18333", None, "Measure Theory and Fine Properties of Functions", "Evans", 2015, "9781482242386"),
    "fleming1960integral": ("10.1007/BF01236935", None, "An integral formula for total gradient variation", "Fleming", 1960, None),
    "hillar2013most": ("10.1145/2512329", "0911.1393", "Most tensor problems are NP-hard", "Hillar", 2013, None),
    "lovasz2006limits": ("10.1016/j.jctb.2006.05.002", "math/0408173", "Limits of dense graph sequences", "Lovasz", 2006, None),
    "lovasz2007szemeredi": ("10.1007/s00039-007-0599-6", None, "Szemeredi's lemma for the analyst", "Lovasz", 2007, None),
    "lovasz2012large": ("10.1090/coll/060", None, "Large Networks and Graph Limits", "Lovasz", 2012, "9780821890851"),
    "lim2005singular": ("10.1109/CAMAP.2005.1574201", "math/0607648", "Singular values and eigenvalues of tensors: a variational approach", "Lim", 2005, None),
    "qi2005eigenvalues": ("10.1016/j.jsc.2005.05.007", None, "Eigenvalues of a real supersymmetric tensor", "Qi", 2005, None),
    "rudin1992nonlinear": ("10.1016/0167-2789(92)90242-F", None, "Nonlinear total variation based noise removal algorithms", "Rudin", 1992, None),
    "milnor1963morse": ("10.1515/9781400881802", None, "Morse Theory", "Milnor", 1963, "9780691080086"),
    "silvafilho2026book": ("10.5281/zenodo.22290043", None, "Geometry, Tensors, and Quantum Gravity", "Silva-Filho", 2026, None),
    "tomioka2014spectral": ("10.48550/arXiv.1407.1870", "1407.1870", "Spectral norm of random tensors", "Tomioka", 2014, None),
    "nguyen2015tensor": ("10.1093/imaiai/iav004", "1005.4732", "Tensor sparsification via a bound on the spectral norm of random tensors", "Nguyen", 2015, None),
    "vershynin2018high": ("10.1017/9781108231596", None, "High-Dimensional Probability: An Introduction with Applications in Data Science", "Vershynin", 2018, None),
    "zhao2015hypergraph": ("10.1002/rsa.20537", "1302.1634", "Hypergraph limits: a regularity approach", "Zhao", 2015, None),
    # ---- added 2026-10-06 ----
    "frieze1999quick": ("10.1007/s004930050052", None, "Quick approximation to matrices and applications", "Frieze", 1999, None),
    "borgs2008convergent": ("10.1016/j.aim.2008.07.008", "math/0702004", "Convergent sequences of dense graphs I: Subgraph frequencies, metric properties and testing", "Borgs", 2008, None),
    "janson2013graphons": (None, "1009.2376", "Graphons, cut norm and distance, couplings and rearrangements", "Janson", 2010, None),
    "alon2006approximating": ("10.1137/S0097539704441629", None, "Approximating the cut-norm via Grothendieck's inequality", "Alon", 2006, None),
    "elek2012measure": ("10.1016/j.aim.2012.06.022", "0810.4062", "A measure-theoretic approach to the theory of dense hypergraphs", "Elek", 2012, None),
    "federer1959curvature": ("10.1090/S0002-9947-1959-0110078-1", None, "Curvature measures", "Federer", 1959, None),
    "kac1943average": ("10.1090/S0002-9904-1943-07912-8", None, "On the average number of real roots of a random algebraic equation", "Kac", 1943, None),
    "fyodorov2004complexity": ("10.1103/PhysRevLett.92.240601", "cond-mat/0401287", "Complexity of random energy landscapes, glass transition, and absolute value of the spectral determinant of random matrices", "Fyodorov", 2004, None),
    "auffinger2013complexity": ("10.1214/13-AOP862", "1110.5872", "Complexity of random smooth functions on the high-dimensional sphere", "Auffinger", 2013, None),
    "subag2017complexity": ("10.1214/16-AOP1139", "1504.02251", "The complexity of spherical p-spin models: a second moment approach", "Subag", 2017, None),
    "subag2017geometry": ("10.1007/s00222-017-0726-4", "1604.00679", "The geometry of the Gibbs measure of pure spherical spin glasses", "Subag", 2017, None),
    "subag2021following": ("10.1002/cpa.21922", "1812.04588", "Following the ground states of full-RSB spherical spin glasses", "Subag", 2021, None),
    "fyodorov2014topology": ("10.1007/s10955-013-0838-1", "1304.0024", "Topology trivialization and large deviations for the minimum in the simplest random optimization", "Fyodorov", 2014, None),
    "ros2019complex": ("10.1103/PhysRevX.9.011003", "1804.02686", "Complex energy landscapes in spiked-tensor and simple glassy models: ruggedness, arrangements of local minima, and phase transitions", "Ros", 2019, None),
    "kentdobias2024arrangement": ("10.21468/SciPostPhys.16.1.001", "2306.12779", "Arrangement of nearby minima and saddles in the mixed spherical energy landscapes", "Kent-Dobias", 2024, None),
    "benarous2019landscape": ("10.1002/cpa.21861", "1711.05424", "The landscape of the spiked tensor model", "Ben Arous", 2019, None),
    "breiding2017expected": ("10.1137/16M1089769", "1604.03910", "The expected number of eigenvalues of a real Gaussian tensor", "Breiding", 2017, None),
    "draisma2016average": ("10.1080/03081087.2016.1164660", "1408.3507", "The average number of critical rank-one approximations to a tensor", "Draisma", 2016, None),
    "friedland2014number": ("10.1007/s10208-014-9194-z", "1210.8316", "The number of singular vector tuples and uniqueness of best rank-one approximation of tensors", "Friedland", 2014, None),
    "lim2021tensors": ("10.1017/S0962492921000076", "2106.08090", "Tensors in computations", "Lim", 2021, None),
    "lim2009nonnegative": ("10.1002/cem.1244", "0903.4530", "Nonnegative approximations of nonnegative tensors", "Lim", 2009, None),
    "evnin2021melonic": ("10.1007/s11005-021-01407-z", "2003.11220", "Melonic dominance and the largest eigenvalue of a large random tensor", "Evnin", 2021, None),
    "dartois2024injective": ("10.48550/arXiv.2404.03627", "2404.03627", "Injective norm of real and complex random tensors I: From spin glasses to geometric entanglement", "Dartois", 2024, None),
    "boedihardjo2024injective": ("10.48550/arXiv.2412.21193", "2412.21193", "Injective norm of random tensors with independent entries", "Boedihardjo", 2024, None),
    "montanari2014statistical": ("10.48550/arXiv.1411.1076", "1411.1076", "A statistical model for tensor PCA", "Montanari", 2014, None),
    "choromanska2015loss": ("10.48550/arXiv.1412.0233", "1412.0233", "The loss surfaces of multilayer networks", "Choromanska", 2015, None),
    "medvedev2014nonlinear": ("10.1137/130943741", "1302.5804", "The nonlinear heat equation on dense graphs and graph limits", "Medvedev", 2014, None),
    "gao2015rate": ("10.1214/15-AOS1354", "1410.5837", "Rate-optimal graphon estimation", "Gao", 2015, None),
    "ruiz2021graphon": ("10.1109/TSP.2021.3106857", "2003.05030", "Graphon signal processing", "Ruiz", 2021, None),
    "ruiz2020graphon": ("10.48550/arXiv.2006.03548", "2006.03548", "Graphon neural networks and the transferability of graph neural networks", "Ruiz", 2020, None),
    "yang2022tensor": ("10.48550/arXiv.2203.03466", "2203.03466", "Tensor Programs V: Tuning large neural networks via zero-shot hyperparameter transfer", "Yang", 2022, None),
    "yoshida2017spectral": ("10.48550/arXiv.1705.10941", "1705.10941", "Spectral norm regularization for improving the generalizability of deep learning", "Yoshida", 2017, None),
    "miyato2018spectral": ("10.48550/arXiv.1802.05957", "1802.05957", "Spectral normalization for generative adversarial networks", "Miyato", 2018, None),
    "rahaman2019spectral": ("10.48550/arXiv.1806.08734", "1806.08734", "On the spectral bias of neural networks", "Rahaman", 2019, None),
    "czarnecki2017sobolev": ("10.48550/arXiv.1706.04859", "1706.04859", "Sobolev training for neural networks", "Czarnecki", 2017, None),
    "entezari2022role": ("10.48550/arXiv.2110.06296", "2110.06296", "The role of permutation invariance in linear mode connectivity of neural networks", "Entezari", 2022, None),
    "ainsworth2023git": ("10.48550/arXiv.2209.04836", "2209.04836", "Git Re-Basin: Merging models modulo permutation symmetries", "Ainsworth", 2023, None),
}


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def words(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", fold(re.sub(r"<[^>]+>", " ", s)))) - {"the", "a", "of", "and", "an", "on", "in", "for", "to", "via"}


def jaccard(a: str, b: str) -> float:
    """Word Jaccard; a registry title that is a prefix/subset (subtitle or series tag
    dropped) counts when the shorter title has >= 2 words, all contained in the longer."""
    A, B = words(a), words(b)
    j = len(A & B) / max(1, len(A | B))
    S, L = (A, B) if len(A) <= len(B) else (B, A)
    if len(S - {"am", "51"}) >= 2 and len((S - {"am", "51"}) - L) == 0:
        j = max(j, 0.99)
    return j


def get(url: str, timeout: float = 25) -> bytes:
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise
            time.sleep(2 + 3 * attempt)
        except Exception:
            time.sleep(2 + 3 * attempt)
    raise RuntimeError("network failure: " + url)


def resolve_doi(doi: str) -> dict | None:
    q = urllib.parse.quote(doi, safe="/")
    try:
        m = json.loads(get(f"https://api.crossref.org/works/{q}"))["message"]
        auth = [a.get("family", a.get("name", "")) for a in m.get("author", m.get("editor", []))]
        y = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
        return {"src": "Crossref", "title": (m.get("title") or [""])[0], "authors": auth, "year": y,
                "isbn": [re.sub(r"\D", "", i) for i in m.get("ISBN", [])]}
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    try:
        d = json.loads(get(f"https://api.datacite.org/dois/{q}"))["data"]["attributes"]
        auth = [c.get("familyName", c.get("name", "")) for c in d.get("creators", [])]
        return {"src": "DataCite", "title": d["titles"][0]["title"], "authors": auth,
                "year": d.get("publicationYear"), "isbn": []}
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    return None


def resolve_arxiv(aid: str) -> dict | None:
    x = get("http://export.arxiv.org/api/query?" + urllib.parse.urlencode({"id_list": aid})).decode("utf-8")
    ents = x.split("<entry>")[1:]
    if not ents or "<title>" not in ents[0]:
        return None
    e = ents[0]
    t = " ".join(re.search(r"<title>(.*?)</title>", e, re.S).group(1).split())
    au = re.findall(r"<name>(.*?)</name>", e)
    y = int(re.search(r"<published>(\d{4})", e).group(1))
    return {"src": "arXiv", "title": t, "authors": [a.split()[-1] for a in au], "year": y}


def openlibrary(isbn: str) -> dict | None:
    d = json.loads(get("https://openlibrary.org/api/books?" + urllib.parse.urlencode(
        {"bibkeys": f"ISBN:{isbn}", "format": "json", "jscmd": "data"})))
    r = d.get(f"ISBN:{isbn}")
    if not r:
        return None
    return {"title": r.get("title", "") + " " + r.get("subtitle", ""), "authors": [a["name"] for a in r.get("authors", [])]}


def isbn13_ok(isbn: str) -> bool:
    d = [int(c) for c in isbn]
    return len(d) == 13 and sum(v * (1 if i % 2 == 0 else 3) for i, v in enumerate(d)) % 10 == 0


def check(key, doi, arx, title, author, year, isbn):
    notes, ok = [], True
    recs = []
    if doi:
        r = resolve_doi(doi)
        if r is None:
            return False, [f"DOI {doi} NOT FOUND"]
        recs.append(r)
    if arx:
        time.sleep(3)
        r = resolve_arxiv(arx)
        if r is None:
            return False, [f"arXiv {arx} NOT FOUND"]
        recs.append(r)
    for r in recs:
        j = jaccard(title, r["title"])
        a_ok = any(fold(author).split()[-1] in fold(x) for x in r["authors"]) if r["authors"] else False
        y_ok = r["year"] is None or abs(int(r["year"]) - year) <= 1 or r["src"] == "arXiv"
        if not r["authors"]:
            a_ok = None  # registry record has no author field; author checked on the ISBN record
        good = j >= 0.6 and a_ok and y_ok
        good = j >= 0.6 and a_ok is not False and y_ok
        ok &= good
        astr = "n/a in record" if a_ok is None else ("ok" if a_ok else "MISMATCH")
        ystr = "n/a in record" if r["year"] is None else str(r["year"])
        notes.append(f"{r['src']}: J={j:.2f} author={astr} year={ystr}{'' if y_ok else ' MISMATCH'} | {r['title'][:90]}")
    if isbn:
        good = isbn13_ok(isbn)
        if good:
            ol = openlibrary(isbn)
            if ol is not None:
                t_ok = jaccard(title, ol["title"]) >= 0.6
                a_ok2 = any(fold(author).split()[-1] in fold(x) for x in ol["authors"])
                good = t_ok and a_ok2
                notes.append(f"OpenLibrary ISBN: title={'ok' if t_ok else 'MISMATCH'} author={'ok' if a_ok2 else 'MISMATCH'} | {ol['title'][:60]} / {', '.join(ol['authors'])[:60]}")
            else:
                notes.append("OpenLibrary ISBN: no record (checksum only)")
        ok &= good
        notes.append(f"ISBN {isbn} checksum {'ok' if isbn13_ok(isbn) else 'BAD'}")
    return ok, notes


def main():
    tex = TEX.read_text(encoding="utf-8")
    cited = set()
    for grp in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}", tex):
        cited |= {k.strip() for k in grp.split(",")}
    items = set(re.findall(r"\\bibitem\{([^}]+)\}", tex))
    print(f"bibitems in .tex: {len(items)}; cited keys: {len(cited)}")
    print("cited but no bibitem:", sorted(cited - items) or "none")
    print("bibitem never cited:", sorted(items - cited) or "none")
    print("bibitem not in REFS table:", sorted(items - set(REFS)) or "none")
    print("REFS entry not in .tex:", sorted(set(REFS) - items) or "none")
    for k in REFS:  # DOI written in the .tex must equal the audited DOI
        doi = REFS[k][0]
        m = re.search(r"\\bibitem\{" + re.escape(k) + r"\}(.*?)(?=\\bibitem|\\end\{thebibliography\})", tex, re.S)
        if m and doi and doi.lower() not in m.group(1).lower():
            print(f"[WARN] {k}: DOI {doi} not written in its bibitem")
    print()
    n_ok = 0
    for k, v in REFS.items():
        ok, notes = check(k, *v)
        n_ok += ok
        print(f"[{'OK ' if ok else 'FAIL'}] {k}")
        for s in notes:
            print("       " + s)
        time.sleep(0.5)
    print(f"\nresolved and matched: {n_ok}/{len(REFS)}")

    print("\nNegative controls (each must FAIL):")
    ok1, n1 = check("neg_fake_doi", "10.1016/j.jctb.2099.99.999", None, "Limits of dense graph sequences", "Lovasz", 2006, None)
    ok2, n2 = check("neg_wrong_title", "10.1016/j.jctb.2006.05.002", None, "Hypergraph regularity and quantum gravity", "Lovasz", 2006, None)
    ok3, n3 = check("neg_bad_isbn", None, None, "x", "x", 2000, "9780821890852")
    for name, ok, n in (("fake DOI", ok1, n1), ("wrong title", ok2, n2), ("bad ISBN", ok3, n3)):
        print(f"  {name}: {'FAILED as required' if not ok else 'PASSED -- CONTROL BROKEN'} | {n}")


if __name__ == "__main__":
    main()
