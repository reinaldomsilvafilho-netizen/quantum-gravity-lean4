"""Step 0: list Zenodo versions of concept 22644743 and their files."""
import json
import urllib.request

URLS = [
    "https://zenodo.org/api/records/22644743",
    "https://zenodo.org/api/records?q=conceptrecid:22644743&all_versions=true",
]


def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def show(rec):
    m = rec["metadata"]
    print(rec["id"], "conceptrecid", rec.get("conceptrecid"), "version", m.get("version"),
          "pubdate", m.get("publication_date"), "created", rec.get("created", "")[:19],
          "updated", rec.get("updated", "")[:19])
    print("   title:", m.get("title"))
    for f in rec.get("files", []):
        print("     file:", f["key"], f["size"], f["links"]["self"])


try:
    r0 = get(URLS[0])
    print("== record 22644743 ==")
    show(r0)
except Exception as e:
    print("record fetch error", e)

d = get(URLS[1])
print("== all versions:", d["hits"]["total"])
for h in d["hits"]["hits"]:
    show(h)
