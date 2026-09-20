import os
import re

pattern = re.compile(r'\\bibitem\{[^}]+\}\s*(.*?)(?=\\bibitem|\\end\{thebibliography\})', re.DOTALL)
refs = set()

for root, _, files in os.walk('unified_quantum_gravity_book'):
    for file in files:
        if file.endswith('.tex') or file.endswith('.tex.bak'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for match in pattern.finditer(content):
                        ref = match.group(1).strip().replace('\n', ' ')
                        ref = re.sub(r'\s+', ' ', ref)
                        if len(ref) > 10:
                            refs.add(ref)
            except Exception as e:
                pass

with open('all_references_text.txt', 'w', encoding='utf-8') as f:
    for i, r in enumerate(refs):
        f.write(f'{i+1}. {r}\n')

print(f'Found {len(refs)} references in chapters.')
