"""Resolve every DOI in the SQG manuscript bibliography via Crossref/DataCite.

Reuses parse/check from the book's audit/scripts/check_references.py (read-only).
Usage: python check_refs_sqg.py [texfile]
"""
import concurrent.futures as cf
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'unified_quantum_gravity_book', 'audit', 'scripts'))
import check_references as cr  # noqa: E402

tex = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'manuscript_simplicial_quantum_gravity_master.tex')
entries = cr.parse(tex)
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    entries = list(ex.map(cr.check, entries))
for e in entries:
    print(f"{e['status']:18s} {e['key']:32s} {e.get('score', ''):5} {e.get('doi') or e.get('suggested_doi', '')} | {e.get('resolved_title', '')[:80]}")
