import json, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "rec.json"), encoding="utf8"))
m = d["metadata"]
desc = re.sub(r"<[^>]+>", " ", m["description"]).replace("&nbsp;", " ")
desc = re.sub(r"\s+", " ", desc)
s = "\n".join([f"title: {m['title']}", f"date: {m['publication_date']}", f"doi: {m.get('doi')}",
               f"version: {m.get('version')}", "DESCRIPTION: " + desc,
               "related: " + json.dumps(m.get("related_identifiers", []))[:800]])
print(s)
open(os.path.join(HERE, "zenodo_desc.out.txt"), "w", encoding="utf8").write(s)
