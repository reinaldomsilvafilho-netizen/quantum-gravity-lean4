"""Step 0: query Zenodo for all versions of concept 22644743 and list files."""
import json, urllib.request, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)
out = []
c = get("https://zenodo.org/api/records/22644743")
out.append("concept/record 22644743 -> id %s title %s" % (c.get("id"), c.get("metadata", {}).get("title")))
d = get("https://zenodo.org/api/records?q=conceptrecid:22644743&all_versions=true&size=25")
for h in d["hits"]["hits"]:
    m = h["metadata"]
    out.append("%s | v=%s | pub=%s | created=%s | %s" % (h["id"], m.get("version"), m.get("publication_date"), h.get("created"), m["title"]))
    for f in h.get("files", []):
        out.append("    %s %s %s" % (f["key"], f["size"], f["links"]["self"]))
latest = max(d["hits"]["hits"], key=lambda h: h["created"])
out.append("LATEST id %s" % latest["id"])
json.dump(latest, open(os.path.join(HERE, "zenodo_latest.json"), "w", encoding="utf8"), indent=1)
open(os.path.join(HERE, "zenodo_latest_description.html"), "w", encoding="utf8").write(latest["metadata"].get("description", ""))
txt = "\n".join(out)
print(txt)
open(os.path.join(HERE, "zenodo_check.out.txt"), "w", encoding="utf8").write(txt)
