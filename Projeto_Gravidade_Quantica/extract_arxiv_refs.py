import os
import re
import subprocess

arxiv_pattern = re.compile(r'(?:arXiv:|arxiv/|arxiv\.org/abs/)(\d{4}\.\d{4,5})')
hep_pattern = re.compile(r'(?:hep-th/|gr-qc/|quant-ph/)(\d{7})')
old_arxiv_pattern = re.compile(r'arXiv:([a-z\-]+/\d{7})')

papers = set()

# Also just look for standalone numbers that look like arxiv ids
fallback_pattern = re.compile(r'\b(1[0-9]{3}\.\d{4,5})\b')

for root, dirs, files in os.walk('.'):
    if 'references_and_papers' in root or '.git' in root or '.gemini' in root:
        continue
    for file in files:
        if file.endswith(('.tex', '.tex.bak', '.md', '.bib')):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    papers.update(arxiv_pattern.findall(content))
                    papers.update(hep_pattern.findall(content))
                    papers.update(old_arxiv_pattern.findall(content))
                    papers.update(fallback_pattern.findall(content))
            except Exception as e:
                pass

print(f"Found {len(papers)} unique arXiv papers.")
print(papers)

with open('download_all_papers.bat', 'w') as f:
    f.write('@echo off\n')
    for p in papers:
        f.write(f'uv run C:\\Users\\monar\\.gemini\\config\\skills\\literature-search-arxiv\\scripts\\download_paper.py --id {p} --format pdf --output references_and_papers\\{p}.pdf\n')
print("Generated download_all_papers.bat")
