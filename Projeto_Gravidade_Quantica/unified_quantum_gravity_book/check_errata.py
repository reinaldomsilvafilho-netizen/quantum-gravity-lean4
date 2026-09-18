import os

book_dir = r'c:\Users\monar\Documents\antigravity\resilient-turing\unified_quantum_gravity_book'
chapters = [f for f in os.listdir(book_dir) if f.startswith('chap') and f.endswith('.tex')]

def check_chapter(chap_name):
    with open(os.path.join(book_dir, chap_name), 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    if 'S_{\\mathrm{univ}}' in content and '\\mathcal{W}_{\\Delta_2}' not in content:
        issues.append('Cor 1 (Yukawa / S_univ)')
    if 'Q_l' in content and 'equipartition' not in content.lower() and 'equipartição' not in content.lower():
        issues.append('Cor 3/8 (Koide framing / equipartition)')
    if 'bounce' in content.lower() and 'Ashtekar' not in content:
        issues.append('Cor 5 (Big Bounce LQC citation)')
    if '10^{113}' in content and '16\pi^2' in content:
        issues.append('Cor 13 (Planck pressure 16pi^2 error)')
    if 'Coleman-Weinberg' in content and 'Higgs' in content:
        issues.append('Cor 14 (Higgs Coleman-Weinberg)')
    if '1.14' in content and '10^{-17}' in content:
        issues.append('Cor 15 (Jarlskog dimensional error)')
        
    return issues

for chap in sorted(chapters):
    res = check_chapter(chap)
    if res:
        print(f'{chap}: {res}')
    else:
        print(f'{chap}: OK')
