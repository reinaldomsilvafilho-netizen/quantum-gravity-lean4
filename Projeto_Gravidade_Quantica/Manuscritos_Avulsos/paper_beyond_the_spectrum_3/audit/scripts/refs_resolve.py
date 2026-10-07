"""Resolve every bibitem of paper_beyond_the_spectrum_3.tex (Volume III).

For each reference: resolve the DOI (Crossref, then DataCite) and compare the title
(word Jaccard >= 0.6, or the shorter title contained in the longer), the first-author
surname and the year (+-2: online vs. issue year) with the values written here.
arXiv-only items are resolved through their DataCite DOI 10.48550/arXiv.<id>.
Items without a DOI are checked on their landing page (HTTP 200 + title words).
ISBN-13 check digits are verified, and books are looked up on Open Library.
The script also checks that cited keys and \\bibitem keys coincide, and that the
DOI written in each bibitem equals the audited DOI.

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
TEX = Path(__file__).resolve().parents[2] / "paper_beyond_the_spectrum_3.tex"

# key: (doi or None, landing URL or None, title, first-author surname, year, isbn or None)
REFS = {
    # ---- kept (19) ----
    "Aamari2019": ("10.1214/19-EJS1551", None, "Estimating the reach of a manifold", "Aamari", 2019, None),
    "Aurell2011": ("10.1103/PhysRevLett.106.250601", None, "Optimal protocols and optimal transport in stochastic thermodynamics", "Aurell", 2011, None),
    "BakryEmery1985": ("10.1007/BFb0075847", None, "Diffusions hypercontractives", "Bakry", 1985, "9783540152309"),
    "Crooks1999": ("10.1103/PhysRevE.60.2721", None, "Entropy production fluctuation theorem and the nonequilibrium work relation for free energy differences", "Crooks", 1999, None),
    "DuttaFaulkner2019": ("10.1007/JHEP03(2021)178", None, "A canonical purification for the entanglement wedge cross-section", "Dutta", 2021, None),
    "EkelandHofer1989": ("10.1007/BF01215653", None, "Symplectic topology and Hamiltonian dynamics", "Ekeland", 1989, None),
    "Federer1959": ("10.1090/S0002-9947-1959-0110078-1", None, "Curvature measures", "Federer", 1959, None),
    "GibsonEtAl1976": ("10.1007/BFb0095244", None, "Topological Stability of Smooth Mappings", "Gibson", 1976, None),
    "Gromov1987": ("10.1007/978-1-4613-9586-7_3", None, "Hyperbolic groups", "Gromov", 1987, "9780387966182"),
    "HoferZehnder1994": ("10.1007/978-3-0348-8540-9", None, "Symplectic Invariants and Hamiltonian Dynamics", "Hofer", 1994, None),
    "Jarzynski1997": ("10.1103/PhysRevLett.78.2690", None, "Nonequilibrium equality for free energy differences", "Jarzynski", 1997, None),
    "KashiwaraSchapira1990": ("10.1007/978-3-662-02661-8", None, "Sheaves on Manifolds", "Kashiwara", 1990, "9783540518617"),
    "BridsonHaefliger1999": ("10.1007/978-3-662-12494-9", None, "Metric Spaces of Non-Positive Curvature", "Bridson", 1999, "9783540643241"),
    "JuutinenLindqvistManfredi1999": ("10.1007/s002050050157", None, "The infinity-eigenvalue problem", "Juutinen", 1999, None),
    "OttoVillani2000": ("10.1006/jfan.1999.3557", None, "Generalization of an inequality by Talagrand and links with the logarithmic Sobolev inequality", "Otto", 2000, None),
    "KawohlFridman2003": (None, "https://dml.cz/handle/10338.dmlcz/119420", "Isoperimetric estimates for the first eigenvalue of the p-Laplace operator and the Cheeger constant", "Kawohl", 2003, None),
    "Lindqvist1990": ("10.1090/S0002-9939-1990-1007505-7", None, "On the equation div(|grad u|^(p-2) grad u) + lambda |u|^(p-2) u = 0", "Lindqvist", 1990, None),
    "SilvaFilhoBTS": ("10.5281/zenodo.22644743", None, "Beyond the Spectrum", "Silva-Filho", 2026, None),
    "SivakCrooks2012": ("10.1103/PhysRevLett.108.190602", None, "Thermodynamic metrics and optimal paths", "Sivak", 2012, None),
    # ---- added 2026-10-07 ----
    "ArtsteinAvidanKarasevOstrover2014": ("10.1215/00127094-2794999", None, "From symplectic measurements to the Mahler conjecture", "Artstein-Avidan", 2014, None),
    "ArtsteinAvidanOstrover2008": ("10.1093/imrn/rnn044", None, "A Brunn-Minkowski inequality for symplectic capacities of convex domains", "Artstein-Avidan", 2008, None),
    "AkersRath2020": ("10.1007/JHEP04(2020)208", None, "Entanglement wedge cross sections require tripartite entanglement", "Akers", 2020, None),
    "BelloniKawohlJuutinen2006": ("10.4171/JEMS/40", None, "The p-Laplace eigenvalue problem as p goes to infinity in a Finsler metric", "Belloni", 2006, None),
    "BlaberSivak2023": ("10.1088/2399-6528/acbf04", None, "Optimal control in stochastic thermodynamics", "Blaber", 2023, None),
    "BoissonnatLieutierWintraecken2019": ("10.1007/s41468-019-00029-8", None, "The reach, metric distortion, geodesic convexity and the variation of tangent spaces", "Boissonnat", 2019, None),
    "Carlson1963": ("10.1016/0022-247X(63)90067-2", None, "Lauricella's hypergeometric function FD", "Carlson", 1963, None),
    "ChampionDePascaleJimenez2008": ("10.48550/arXiv.0811.1934", None, "The infinity eigenvalue problem and a problem of optimal transportation", "Champion", 2008, None),
    "Cheeger1970": ("10.1515/9781400869312-013", None, "A lower bound for the smallest eigenvalue of the Laplacian", "Cheeger", 1970, None),
    "Chow2022": ("10.48550/arXiv.2201.11013", None, "Schlomilch integrals and probability distributions on the simplex", "Chow", 2022, None),
    "CieliebakHoferLatschevSchlenk2005": ("10.48550/arXiv.math/0506191", None, "Quantitative symplectic geometry", "Cieliebak", 2005, None),
    "Crooks2007": ("10.1103/PhysRevLett.99.100602", None, "Measuring thermodynamic length", "Crooks", 2007, None),
    "DLMF": (None, "https://dlmf.nist.gov/5.12", "NIST Handbook of Mathematical Functions", "Olver", 2010, "9780521192255"),
    "EkelandHofer1990": ("10.1007/BF02570756", None, "Symplectic topology and Hamiltonian dynamics II", "Ekeland", 1990, None),
    "FloerHofer1994": ("10.1007/BF02571699", None, "Symplectic homology I: Open sets in C^n", "Floer", 1994, None),
    "FukagaiItoNarukawa1999": ("10.57262/die/1367265629", None, "Limit as p to infinity of p-Laplace eigenvalue problems and L-infinity inequality of the Poincare type", "Fukagai", 1999, None),
    "Gromov1985": ("10.1007/BF01388806", None, "Pseudo holomorphic curves in symplectic manifolds", "Gromov", 1985, None),
    "HaimKislevOstrover2026": ("10.4007/annals.2026.203.2.5", None, "A counterexample to Viterbo's conjecture", "Haim-Kislev", 2026, None),
    "HaydenLemmSorce2023": ("10.1103/PhysRevA.107.L050401", None, "Reflected entropy is not a correlation measure", "Hayden", 2023, None),
    "HaydenParrikarSorce2021": ("10.1007/JHEP10(2021)047", None, "The Markov gap for geometric reflected entropy", "Hayden", 2021, None),
    "JordanKinderlehrerOtto1998": ("10.1137/S0036141096303359", None, "The variational formulation of the Fokker-Planck equation", "Jordan", 1998, None),
    "Kashiwara1985": (None, "http://www.numdam.org/item?id=AST_1985__130__193_0", "Index theorem for constructible sheaves", "Kashiwara", 1985, None),
    "LiebRuskai1973": ("10.1063/1.1666274", None, "Proof of the strong subadditivity of quantum-mechanical entropy", "Lieb", 1973, None),
    "Lindqvist2008": ("10.1142/9789812811066_0005", None, "A nonlinear eigenvalue problem", "Lindqvist", 2008, "9789812811059"),
    "MacPherson1974": ("10.2307/1971080", None, "Chern classes for singular algebraic varieties", "MacPherson", 1974, None),
    "Mather2012": ("10.1090/S0273-0979-2012-01383-6", None, "Notes on topological stability", "Mather", 2012, None),
    "Mercer1909": ("10.1098/rsta.1909.0016", None, "Functions of positive and negative type, and their connection with the theory of integral equations", "Mercer", 1909, None),
    "NakazatoIto2021": ("10.1103/PhysRevResearch.3.043093", None, "Geometrical aspects of entropy production in stochastic thermodynamics based on Wasserstein distance", "Nakazato", 2021, None),
    "NguyenEtAl2018": ("10.1007/JHEP01(2018)098", None, "Entanglement of purification: from spin chains to holography", "Nguyen", 2018, None),
    "NiyogiSmaleWeinberger2008": ("10.1007/s00454-008-9053-2", None, "Finding the homology of submanifolds with high confidence from random samples", "Niyogi", 2008, None),
    "OrroTrotman2010": ("10.1017/CBO9780511731983.022", None, "Regularity of the transverse intersection of two regular stratifications", "Orro", 2010, "9780521169691"),
    "RatajZahle2019": ("10.1007/978-3-030-18183-3", None, "Curvature Measures of Singular Sets", "Rataj", 2019, "9783030181826"),
    "SalamonBerry1983": ("10.1103/PhysRevLett.51.1127", None, "Thermodynamic length and dissipated availability", "Salamon", 1983, None),
    "Schapira1991": ("10.1016/0022-4049(91)90131-K", None, "Operations on constructible functions", "Schapira", 1991, None),
    "Schapira2017": ("10.48550/arXiv.1701.08955", None, "Microlocal analysis and beyond", "Schapira", 2017, None),
    "SchmiedlSeifert2007": ("10.1103/PhysRevLett.98.108301", None, "Optimal finite-time processes in stochastic thermodynamics", "Schmiedl", 2007, None),
    "Schmidt1907": ("10.1007/BF01449770", None, "Zur Theorie der linearen und nichtlinearen Integralgleichungen", "Schmidt", 1907, None),
    "Schwarz2000": ("10.2140/pjm.2000.193.419", None, "On the action spectrum for closed symplectically aspherical manifolds", "Schwarz", 2000, None),
    "Seifert2012": ("10.1088/0034-4885/75/12/126001", None, "Stochastic thermodynamics, fluctuation theorems and molecular machines", "Seifert", 2012, None),
    "silvafilho2026book": ("10.5281/zenodo.22290043", None, "Geometry, Tensors, and Quantum Gravity", "Silva-Filho", 2026, None),
    "Srednicki1993": ("10.1103/PhysRevLett.71.666", None, "Entropy and area", "Srednicki", 1993, None),
    "Talagrand1996": ("10.1007/BF02249265", None, "Transportation cost for Gaussian and other product measures", "Talagrand", 1996, None),
    "Trotman2020": ("10.1007/978-3-030-53061-7_4", None, "Stratification theory", "Trotman", 2020, "9783030530600"),
    "UmemotoTakayanagi2018": ("10.1038/s41567-018-0075-2", None, "Entanglement of purification through holographic duality", "Umemoto", 2018, None),
    "VanVuSaito2023": ("10.1103/PhysRevX.13.011013", None, "Thermodynamic unification of optimal transport: thermodynamic uncertainty relation, minimum dissipation, and thermodynamic speed limits", "Van Vu", 2023, None),
    "Villani2009": ("10.1007/978-3-540-71050-9", None, "Optimal Transport: Old and New", "Villani", 2009, "9783540710493"),
    "Viro1988": ("10.1007/BFb0082775", None, "Some integral calculus based on Euler characteristic", "Viro", 1988, "9783540502371"),
    "Viterbo1992": ("10.1007/BF01444643", None, "Symplectic topology as the geometry of generating functions", "Viterbo", 1992, None),
    "Viterbo2000": ("10.1090/S0894-0347-00-00328-3", None, "Metric and isoperimetric problems in symplectic geometry", "Viterbo", 2000, None),
    "vonRenesseSturm2005": ("10.1002/cpa.20060", None, "Transport inequalities, gradient estimates, entropy and Ricci curvature", "Renesse", 2005, None),
    "Weyl1939": ("10.2307/2371513", None, "On the volume of tubes", "Weyl", 1939, None),
    "Whitney1965": ("10.2307/1970400", None, "Tangents to an analytic variety", "Whitney", 1965, None),
    "ZhongDeWeese2024": ("10.1103/PhysRevLett.133.057102", None, "Beyond linear response: equivalence between thermodynamic geometry and optimal transport", "Zhong", 2024, None),
}

# For a chapter in an edited volume the ISBN belongs to the volume: compare the
# Open Library record with the volume title and accept any author (editors differ).
CONTAINER = {
    "BakryEmery1985": "Seminaire de Probabilites XIX 1983/84",
    "Gromov1987": "Essays in Group Theory",
    "Lindqvist2008": "Topics in Mathematical Analysis",
    "OrroTrotman2010": "Real and Complex Singularities",
    "Trotman2020": "Handbook of Geometry and Topology of Singularities I",
    "Viro1988": "Topology and Geometry - Rohlin Seminar",
    "DLMF": "NIST Handbook of Mathematical Functions",  # edited volume: Olver et al. (eds.)
}

STOP = {"the", "a", "of", "and", "an", "on", "in", "for", "to", "via", "der", "und", "zur", "with", "its", "their"}


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def words(s: str) -> set[str]:
    s = re.sub(r"<[^>]+>|\$[^$]*\$", " ", s)
    return set(re.findall(r"[a-z0-9]+", fold(s))) - STOP


def jaccard(a: str, b: str) -> float:
    """Word Jaccard; a title contained in the other (subtitle or series tag dropped)
    counts when the shorter one has >= 2 words."""
    A, B = words(a), words(b)
    j = len(A & B) / max(1, len(A | B))
    S, L = (A, B) if len(A) <= len(B) else (B, A)
    if len(S) >= 2 and len(S - L) == 0:
        j = max(j, 0.99)
    return j


def get(url: str, timeout: float = 30) -> bytes:
    last = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise
            last = e
        except Exception as e:  # network hiccup: retry
            last = e
        time.sleep(3 + 4 * attempt)
    raise RuntimeError(f"network failure: {url}: {last}")


def resolve_doi(doi: str) -> dict | None:
    q = urllib.parse.quote(doi, safe="/")
    if not doi.startswith(("10.48550/", "10.5281/")):
        try:
            m = json.loads(get(f"https://api.crossref.org/works/{q}"))["message"]
            auth = [a.get("family", a.get("name", "")) for a in m.get("author", m.get("editor", []))]
            y = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
            return {"src": "Crossref", "title": (m.get("title") or [""])[0], "authors": auth, "year": y}
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise
    try:
        d = json.loads(get(f"https://api.datacite.org/dois/{q}"))["data"]["attributes"]
        auth = [c.get("familyName") or c.get("name", "") for c in d.get("creators", [])]
        return {"src": "DataCite", "title": d["titles"][0]["title"], "authors": auth, "year": d.get("publicationYear")}
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    return None


def landing(url: str) -> dict | None:
    try:
        html = get(url).decode("utf-8", "replace")
    except urllib.error.HTTPError:
        return None
    t = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", html)
    return {"src": "landing", "title": " ".join((t.group(1) if t else "").split()), "body": text}


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


def surname_in(author: str, names: list[str]) -> bool:
    a = fold(author).replace("-", " ").split()[-1]
    return any(a in fold(x).replace("-", " ") for x in names)


def check(key, doi, url, title, author, year, isbn):
    notes, ok = [], True
    if doi:
        r = resolve_doi(doi)
        if r is None:
            return False, [f"DOI {doi} NOT FOUND"]
        j = jaccard(title, r["title"])
        a_ok = surname_in(author, r["authors"]) if r["authors"] else None
        y_ok = r["year"] is None or abs(int(r["year"]) - year) <= 2
        # Cheeger 1970: DOI is the 2015 digital reissue of the 1970 volume
        if key == "Cheeger1970" and r["year"] == 2015:
            y_ok = True
        good = j >= 0.6 and a_ok is not False and y_ok
        ok &= good
        astr = "n/a in record" if a_ok is None else ("ok" if a_ok else "MISMATCH")
        notes.append(f"{r['src']}: J={j:.2f} author={astr} year={r['year']}{'' if y_ok else ' MISMATCH'} | {r['title'][:90]}")
    if url:
        r = landing(url)
        if r is None:
            return False, [f"URL {url} NOT FOUND"]
        body = fold(r["title"] + " " + r["body"][:20000])
        hits = [w for w in words(title) if w in body]
        good = len(hits) >= max(2, int(0.6 * len(words(title))))
        if key == "DLMF":  # the DLMF page carries the DLMF name, not the print title
            good = "dlmf" in body and "beta" in body
        ok &= good
        notes.append(f"landing {url}: HTTP 200, title words found {len(hits)}/{len(words(title))} | {r['title'][:80]}")
    if isbn:
        cs = isbn13_ok(isbn)
        good = cs
        if cs:
            ol = openlibrary(isbn)
            if ol is not None:
                t_ok = jaccard(CONTAINER.get(key, title), ol["title"]) >= 0.6
                a_ok2 = surname_in(author, ol["authors"]) if ol["authors"] else None
                if key in CONTAINER:
                    a_ok2 = None  # volume editors, not the chapter author
                good = t_ok and a_ok2 is not False
                notes.append(f"OpenLibrary ISBN: title={'ok' if t_ok else 'MISMATCH'} author={'n/a' if a_ok2 is None else ('ok' if a_ok2 else 'MISMATCH')} | {ol['title'][:60]} / {', '.join(ol['authors'])[:60]}")
            else:
                notes.append("OpenLibrary ISBN: no record (checksum only)")
        ok &= good
        notes.append(f"ISBN {isbn} checksum {'ok' if cs else 'BAD'}")
    return ok, notes


def main():
    tex = TEX.read_text(encoding="utf-8")
    cited = set()
    for grp in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}", tex):
        cited |= {k.strip() for k in grp.split(",")}
    items = re.findall(r"\\bibitem\{([^}]+)\}", tex)
    print(f"bibitems in .tex: {len(items)} (distinct {len(set(items))}); cited keys: {len(cited)}")
    print("cited but no bibitem:", sorted(cited - set(items)) or "none")
    print("bibitem never cited:", sorted(set(items) - cited) or "none")
    print("bibitem not in REFS table:", sorted(set(items) - set(REFS)) or "none")
    print("REFS entry not in .tex:", sorted(set(REFS) - set(items)) or "none")
    for k, v in REFS.items():  # DOI written in the .tex must equal the audited DOI
        doi = v[0]
        m = re.search(r"\\bibitem\{" + re.escape(k) + r"\}(.*?)(?=\\bibitem|\\end\{thebibliography\})", tex, re.S)
        if m and doi and doi.lower() not in m.group(1).lower():
            print(f"[WARN] {k}: DOI {doi} not written in its bibitem")
        if m and v[5]:
            digits = re.sub(r"\D", "", " ".join(re.findall(r"ISBN:\s*([0-9-]+)", m.group(1))))
            if digits and digits != v[5]:
                print(f"[WARN] {k}: ISBN in .tex {digits} differs from audited {v[5]}")
    print()
    n_ok = 0
    for k, v in REFS.items():
        try:
            ok, notes = check(k, *v)
        except Exception as e:  # could not check is not the same as invalid
            ok, notes = False, [f"COULD NOT CHECK: {e}"]
        n_ok += ok
        print(f"[{'OK ' if ok else 'FAIL'}] {k}")
        for s in notes:
            print("       " + s)
        time.sleep(0.7)
    print(f"\nresolved and matched: {n_ok}/{len(REFS)}")

    print("\nNegative controls (each must FAIL):")
    ok1, n1 = check("neg_fake_doi", "10.1090/S0002-9947-2099-9999999-9", None, "Curvature measures", "Federer", 1959, None)
    ok2, n2 = check("neg_wrong_title", "10.1090/S0002-9947-1959-0110078-1", None, "Reflected entropy of tensor networks on graphons", "Federer", 1959, None)
    ok3, n3 = check("neg_bad_isbn", None, None, "x", "x", 2000, "9783540518618")
    for name, ok, n in (("fake DOI", ok1, n1), ("wrong title", ok2, n2), ("bad ISBN", ok3, n3)):
        print(f"  {name}: {'FAILED as required' if not ok else 'PASSED -- CONTROL BROKEN'} | {n}")
    sys.exit(0 if n_ok == len(REFS) and not (ok1 or ok2 or ok3) else 1)


if __name__ == "__main__":
    main()
