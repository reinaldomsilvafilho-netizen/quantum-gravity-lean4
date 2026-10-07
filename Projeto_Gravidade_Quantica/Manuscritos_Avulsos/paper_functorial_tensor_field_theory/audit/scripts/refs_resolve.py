"""Reference resolver for paper_functorial_tensor_field_theory.tex.

For every bibitem: resolve the DOI via Crossref, falling back to DataCite (Zenodo, arXiv DOIs),
and compare title fragment, first-author surname, year, volume and first page with the values
printed in the .tex.  arXiv identifiers are checked against the arXiv API.  ISBN-13 check digits
are recomputed.  Negative controls: a fake DOI must give 404, and a mutated expected volume and a
mutated ISBN check digit must be detected.

No personal data is sent: generic User-Agent, no mailto parameter.
Exit status = number of failures.  Output also written to refs_resolve.out.txt.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "refs-resolve/1.0 (reference audit script)"}
TEX = os.path.join(HERE, "..", "..", "paper_functorial_tensor_field_theory.tex")

# key: (doi or None, title fragment, first-author surname fragment, year, volume, first page,
#       arXiv id or None, ISBN-13 or None)
BIB = {
    "silvafilho2026book": ("10.5281/zenodo.22290043", "geometry, tensors, and quantum gravity", "silva-filho", 2026, None, None, None, None),
    "atiyah1988topological": ("10.1007/BF02698547", "topological quantum field theor", "atiyah", 1988, "68", "175", None, None),
    "verstraete2010continuous": ("10.1103/PhysRevLett.104.190405", "continuous matrix product states for quantum fields", "verstraete", 2010, "104", "190405", "1002.1824", None),
    "ryu2006holographic": ("10.1103/PhysRevLett.96.181602", "holographic derivation of entanglement entropy", "ryu", 2006, "96", "181602", "hep-th/0603001", None),
    "choquet1952": ("10.1007/BF02392131", "théorème d'existence pour certains systèmes", "bruhat", 1952, "88", "141", None, None),
    "choquetbruhat2009": ("10.1093/acprof:oso/9780199230723.001.0001", "general relativity and the einstein equations", "choquet-bruhat", 2008, None, None, None, "9780199230723"),
    "bousso2016": ("10.1103/PhysRevD.93.024017", "proof of the quantum null energy condition", "bousso", 2016, "93", "024017", "1509.02542", None),
    "godel1949": ("10.1103/RevModPhys.21.447", "an example of a new type of cosmological solutions", "del", 1949, "21", "447", None, None),
    # ---- added ----
    "segal2004": ("10.1017/CBO9780511526398.019", "the definition of cft", "", 2004, None, "432", None, "9780521540490"),
    "baezdolan1995": ("10.1063/1.531236", "higher-dimensional algebra and topological quantum field theory", "baez", 1995, "36", "6073", "q-alg/9503002", None),
    "lurie2009": ("10.4310/CDM.2008.v2008.n1.a3", "on the classification of topological field theories", "lurie", 2008, "2008", "129", "0905.0465", None),
    "selinger2007": ("10.1016/j.entcs.2006.12.018", "dagger compact closed categories and completely positive maps", "selinger", 2007, "170", "139", None, None),
    "baez2006quandaries": (None, "quantum quandaries", "baez", 2004, None, None, "quant-ph/0404040", None),
    "geroch1967": ("10.1063/1.1705276", "topology in general relativity", "geroch", 1967, "8", "782", None, None),
    "gibbonshawking1992": ("10.1007/BF02100864", "selection rules for topology change", "gibbons", 1992, "148", "345", None, None),
    "borde1994": (None, "topology change in classical general relativity", "borde", 1994, None, None, "gr-qc/9406053", None),
    "israel1966": ("10.1007/BF02710419", "singular hypersurfaces and thin shells in general relativity", "israel", 1966, "44", "1", None, None),
    "haegeman2010variational": ("10.1103/PhysRevLett.105.251601", "applying the variational principle to (1+1)-dimensional quantum field theories", "haegeman", 2010, "105", "251601", "1006.2409", None),
    "haegeman2013calculus": ("10.1103/PhysRevB.88.085118", "calculus of continuous matrix product states", "haegeman", 2013, "88", "085118", "1211.3935", None),
    "haegeman2014geometry": ("10.1063/1.4862851", "geometry of matrix product states", "haegeman", 2014, "55", "021902", "1210.7710", None),
    "haegeman2013cmera": ("10.1103/PhysRevLett.110.100402", "entanglement renormalization for quantum fields in real space", "haegeman", 2013, "110", "100402", "1102.5524", None),
    "provost1980": ("10.1007/BF02193559", "riemannian structure on manifolds of quantum states", "provost", 1980, "76", "289", None, None),
    "braunstein1994": ("10.1103/PhysRevLett.72.3439", "statistical distance and the geometry of quantum states", "braunstein", 1994, "72", "3439", None, None),
    "uhlmann1976": ("10.1016/0034-4877(76)90060-4", "transition probability", "uhlmann", 1976, "9", "273", None, None),
    "petz1996": ("10.1016/0024-3795(94)00211-8", "monotone metrics on matrix spaces", "petz", 1996, "244", "81", None, None),
    "liu2020qfi": ("10.1088/1751-8121/ab5d4d", "quantum fisher information matrix and multiparameter estimation", "liu", 2020, "53", "023001", "1907.08037", None),
    "amari2000": ("10.1090/mmono/191", "methods of information geometry", "amari", 2007, None, None, None, "9780821843024"),
    "brown2006": (None, "topology and groupoids", "brown", 2006, None, None, None, "9781419627224"),
    "schreiber2009": (None, "parallel transport and functors", "schreiber", 2007, None, None, "0705.0452", None),
    "adm2008": ("10.1007/s10714-008-0661-1", "republication of: the dynamics of general relativity", "arnowitt", 2008, "40", "1997", "gr-qc/0405109", None),
    "gourgoulhon2012": ("10.1007/978-3-642-24525-1", "3+1 formalism in general relativity", "gourgoulhon", 2012, None, None, None, "9783642245244"),
    "curiel2017": ("10.1007/978-1-4939-3210-8_3", "a primer on energy conditions", "curiel", 2017, None, "43", "1405.0403", None),
    "dewitt1967": ("10.1103/PhysRev.160.1113", "quantum theory of gravity. i. the canonical theory", "dewitt", 1967, "160", "1113", None, None),
    "vanraamsdonk2010": ("10.1007/s10714-010-1034-0", "building up spacetime with quantum entanglement", "van raamsdonk", 2010, "42", "2323", "1005.3035", None),
    "swingle2012": ("10.1103/PhysRevD.86.065007", "entanglement renormalization and holography", "swingle", 2012, "86", "065007", "0905.1317", None),
    "nozaki2012": ("10.1007/JHEP10(2012)193", "holographic geometry of entanglement renormalization in quantum field theories", "nozaki", 2012, "2012", "193", "1208.3469", None),
    "miyaji2015": ("10.1103/PhysRevLett.115.261602", "distance between quantum states and gauge-gravity duality", "miyaji", 2015, "115", "261602", "1507.07555", None),
    "tuybens2022": ("10.1103/PhysRevLett.128.020501", "variational optimization of continuous matrix product states", "tuybens", 2022, "128", "020501", None, None),
    "erdmenger2023": ("10.1103/PhysRevD.108.106020", "from complexity geometry to holographic spacetime", "erdmenger", 2023, "108", "106020", None, None),
    "araujoregado2023": ("10.1007/JHEP03(2023)026", "cauchy slice holography", "araujo-regado", 2023, "2023", "26", None, None),
    "mohr2025codata": ("10.1103/RevModPhys.97.025002", "codata recommended values of the fundamental physical constants: 2022", "mohr", 2025, "97", "025002", None, None),
    "cao2017": ("10.1103/PhysRevD.95.024031", "space from hilbert space", "cao", 2017, "95", "024031", "1606.08444", None),
}


# arXiv preprint titles that differ from the published title (checked by hand: same authors)
ARXIV_TITLE = {
    "adm2008": "the dynamics of general relativity",
    "miyaji2015": "gravity dual of quantum information metric",
}


def get(url, raw=False):
    req = urllib.request.Request(url, headers=UA)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read().decode("utf8")
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 3:
                raise
            time.sleep(5 * (attempt + 1))
    return data if raw else json.loads(data)


def doi_meta(doi):
    q = urllib.parse.quote(doi, safe="/")
    try:
        m = get(f"https://api.crossref.org/works/{q}")["message"]
        dp = (m.get("published-print") or m.get("published-online") or m.get("issued"))["date-parts"][0]
        auth = (m.get("author") or m.get("editor") or [{}])[0]
        page = (m.get("page") or m.get("article-number") or "").split("-")[0]
        return dict(src="crossref", title=(m.get("title") or [""])[0], author=auth.get("family", auth.get("name", "")),
                    year=dp[0], issued=m["issued"]["date-parts"][0][0], volume=m.get("volume"), page=page,
                    container=(m.get("container-title") or [""])[0], isbn=m.get("ISBN"))
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    a = get(f"https://api.datacite.org/dois/{q}")["data"]["attributes"]
    return dict(src="datacite", title=a["titles"][0]["title"], author=a["creators"][0].get("name", ""),
                year=int(a["publicationYear"]), issued=int(a["publicationYear"]), volume=None, page=None,
                container=a.get("publisher"), isbn=None)


def arxiv_meta(aid):
    xml = get(f"http://export.arxiv.org/api/query?id_list={aid}", raw=True)
    ent = xml.split("<entry>")[1] if "<entry>" in xml else ""
    t = re.search(r"<title>(.*?)</title>", ent, re.S)
    a = re.search(r"<name>(.*?)</name>", ent, re.S)
    return (" ".join(t.group(1).split()) if t else None, a.group(1) if a else None)


def isbn13_ok(isbn):
    d = [int(c) for c in isbn if c.isdigit()]
    return len(d) == 13 and sum(x * (1 if i % 2 == 0 else 3) for i, x in enumerate(d)) % 10 == 0


def norm(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", s.lower().replace("–", "-").replace("\u2010", "-"))


def match(m, exp):
    _, tf, au, ye, vo, pg, _, _ = exp
    ok_t = tf in norm(m["title"])
    ok_a = au in norm(m["author"])
    ok_y = ye in (m["year"], m["issued"])
    ok_v = vo is None or m["volume"] == vo
    ok_p = pg is None or m["page"] == pg
    return ok_t and ok_a and ok_y and ok_v and ok_p, (ok_t, ok_a, ok_y, ok_v, ok_p)


def main():
    out, fails = [], 0
    tex = open(TEX, encoding="utf8").read()
    bibkeys = re.findall(r"\\bibitem\{([^}]+)\}", tex)
    cited = set(k.strip() for c in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}", tex) for k in c.split(","))
    out.append(f"bibitems in tex: {len(bibkeys)}; distinct cited keys: {len(cited)}")
    for k in sorted(set(bibkeys) - cited):
        out.append(f"[FAIL] bibitem never cited: {k}"); fails += 1
    for k in sorted(cited - set(bibkeys)):
        out.append(f"[FAIL] cited but no bibitem: {k}"); fails += 1
    for k in bibkeys:
        if k not in BIB:
            out.append(f"[FAIL] bibitem {k} not in resolver table"); fails += 1
    for key, e in BIB.items():
        doi, aid, isbn = e[0], e[6], e[7]
        line = [f"{key}:"]
        ok_all = True
        try:
            if doi:
                m = doi_meta(doi)
                ok, parts = match(m, e)
                ok_all &= ok
                line.append(f"DOI {doi} [{m['src']}] -> '{m['title'][:90]}' / {m['author']} / {m['year']} (issued {m['issued']}) "
                            f"/ vol {m['volume']} / p {m['page']} / {m['container'][:50] if m['container'] else ''} "
                            f"/ isbn {m['isbn']} ; match(t,a,y,v,p)={parts}")
                if doi not in tex and key in bibkeys:
                    line.append("DOI-NOT-IN-TEX"); ok_all = False
            if aid:
                t, a = arxiv_meta(aid)
                frag = ARXIV_TITLE.get(key, e[1])[:20]
                ok = bool(t) and frag in norm(t)
                ok_all &= ok
                line.append(f"arXiv {aid} -> '{(t or '')[:90]}' / {a} ; title-ok={ok}")
            if isbn:
                ok = isbn13_ok(isbn)
                ok_all &= ok
                line.append(f"ISBN {isbn} check-digit-ok={ok}")
        except Exception as ex:  # noqa: BLE001
            line.append(f"ERROR {ex}"); ok_all = False
        out.append(("[PASS] " if ok_all else "[FAIL] ") + " ".join(line))
        fails += 0 if ok_all else 1
        time.sleep(0.3)
    # negative controls
    try:
        doi_meta("10.1103/PhysRevLett.999.999999")
        out.append("[FAIL] control: fake DOI resolved"); fails += 1
    except urllib.error.HTTPError as ex:
        out.append(f"[PASS] control: fake DOI -> {ex}")
    m = doi_meta("10.1007/BF02698547")
    mut = list(BIB["atiyah1988topological"]); mut[4] = "69"
    det = not match(m, tuple(mut))[0]
    out.append(f"[{'PASS' if det else 'FAIL'}] control: mutated volume 69 detected = {det}"); fails += 0 if det else 1
    det = not isbn13_ok("9780199230724")
    out.append(f"[{'PASS' if det else 'FAIL'}] control: mutated ISBN check digit detected = {det}"); fails += 0 if det else 1
    out.append(f"FAILED CHECKS: {fails}")
    txt = "\n".join(out)
    sys.stdout.reconfigure(encoding="utf-8")
    print(txt)
    open(os.path.join(HERE, "refs_resolve.out.txt"), "w", encoding="utf8").write(txt + "\n")
    return fails


if __name__ == "__main__":
    sys.exit(main())
