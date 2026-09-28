"""Resolve DOIs (Crossref) and arXiv IDs (arXiv API) for ramo E references.
Negative control: a mutated DOI must not resolve."""
import json
import re
import urllib.request

DOIS = {
    "AlbrightRodejohann2009": "10.1140/epjc/s10052-009-1074-3",
    "KingLuhn2011": "10.1007/JHEP09(2011)042",
    "KingLuhn2013review": "10.1088/0034-4885/76/5/056201",
    "VarzielasLavoura2013": "10.1088/0954-3899/40/8/085002",
    "NuFIT6": "10.1007/JHEP12(2024)216",
    "NEGATIVE_CONTROL": "10.1007/JHEP12(2024)2169",
}
ARXIV = ["0812.0436", "1107.5332", "1301.1340", "1212.3247", "2410.05380", "2511.14593", "2503.14738", "2503.14744"]


def crossref(doi):
    try:
        with urllib.request.urlopen(f"https://api.crossref.org/works/{doi}", timeout=30) as r:
            m = json.load(r)["message"]
        return f"{m.get('title', [''])[0]} | {m.get('container-title', [''])[0]} | {m.get('volume', '')} {m.get('page', m.get('article-number', ''))} | {[a.get('family') for a in m.get('author', [])][:5]}"
    except Exception as e:
        return f"UNRESOLVED ({type(e).__name__})"


for k, d in DOIS.items():
    print(f"{k:24s} {d:40s} {crossref(d)}")
try:
    ids = ",".join(ARXIV)
    req = urllib.request.Request(f"https://export.arxiv.org/api/query?id_list={ids}&max_results=20",
                                 headers={"User-Agent": "ref-verifier/1.0", "Accept": "application/atom+xml"})
    with urllib.request.urlopen(req, timeout=30) as r:
        xml = r.read().decode()
    for e in xml.split("<entry>")[1:]:
        t = re.search(r"<title>(.*?)</title>", e, re.S).group(1).split()
        i = re.search(r"<id>(.*?)</id>", e).group(1)
        j = re.search(r"<arxiv:journal_ref[^>]*>(.*?)</arxiv:journal_ref>", e, re.S)
        dd = re.search(r"<arxiv:doi[^>]*>(.*?)</arxiv:doi>", e)
        print(i.split('/')[-1], "|", " ".join(t), "|", j.group(1).strip() if j else "no journal ref", "|", dd.group(1) if dd else "")
except Exception as exc:
    print("arXiv API unavailable from this machine:", exc, "- arXiv IDs checked via abs pages instead (see VERIFICACAO.md)")
