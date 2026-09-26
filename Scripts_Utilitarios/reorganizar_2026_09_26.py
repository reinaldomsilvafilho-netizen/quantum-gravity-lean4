"""Reorganization of resilient-turing following Projeto_Gravidade_Quantica/ORGANIZACAO_E_VERSOES.md.

Nothing is deleted except regenerable LaTeX/Python build artifacts. Everything else is MOVED, and each
move is written to _arquivo/2026-09-26_reorganizacao/MANIFESTO.tsv (origin -> destination) so it can be undone.
Files tracked by git are never touched (except the release folder, moved with git mv).

Usage:  python Scripts_Utilitarios/reorganizar_2026_09_26.py          (dry run: prints the plan)
        python Scripts_Utilitarios/reorganizar_2026_09_26.py --apply
"""
import fnmatch, os, re, shutil, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
P = 'Projeto_Gravidade_Quantica'
ARQ = f'{P}/_arquivo/2026-09-26_reorganizacao'
APPLY = '--apply' in sys.argv
os.chdir(ROOT)

tracked = set(subprocess.run(['git', 'ls-files'], capture_output=True, text=True).stdout.split('\n'))
def is_tracked_tree(path):
    path = path.replace('\\', '/').rstrip('/')
    return path in tracked or any(t.startswith(path + '/') for t in tracked)

moves = []      # (src, dst)
deletes = []    # regenerable artifacts

def archive(src):
    if os.path.exists(src) and not is_tracked_tree(src):
        moves.append((src, f'{ARQ}/{src}'))

def move(src, dst):
    if os.path.exists(src) and not is_tracked_tree(src):
        moves.append((src, dst))

# 1. repo root: stray scripts and other-project artifacts
for f in ('compare_baks.py', 'organize_zenodo_book.py', 'restore_all_tex_files.py'):
    move(f, f'Scripts_Utilitarios/{f}')
move('geomstat.Rcheck', 'Outros_Projetos/geometric_statistics_research/_build/geomstat.Rcheck')
move('geomstat_0.1.0.tar.gz', 'Outros_Projetos/geometric_statistics_research/_build/geomstat_0.1.0.tar.gz')
archive('gribov_gap.png')

# 2. project root: old audit/certificate reports, backups, old release folders
for f in ('BOOK_QUANTUM_GRAVITY_CLAUDE_AUDIT_REPORT.md', 'CODE_LEAN_PY_CLAUDE_AUDIT_REPORT.md',
          'JHEP_ARXIV_FINAL_VERIFICATION_CERTIFICATE.md', 'JHEP_ARXIV_PEER_REVIEW_REPORT.md',
          'JHEP_ARXIV_PEER_REVIEW_ROUND2_REPORT.md', 'ROADMAP_UNCONDITIONAL_YANG_MILLS_ZENODO_SYNTHESIS.md',
          'codebase_backup_before_refactor.zip', 'backup_unzipped', 'zenodo_final_pdfs'):
    archive(f'{P}/{f}')

# 3. superseded standalone versions of book chapters in Manuscritos_Avulsos
MA = f'{P}/Manuscritos_Avulsos'
old_papers = ('paper_emergent_spacetime_quantum_gravity', 'paper_experimental_quantum_gravity_letters',
              'paper_functional_realizations', 'paper_grand_unification_quantum_gravity',
              'paper_matrix_tensor_pde_flows', 'chap12_grand_unification_quantum_gravity_treatise')
for name in os.listdir(MA):
    base, ext = os.path.splitext(name)
    if base in old_papers and ext in ('.tex', '.pdf'):
        archive(f'{MA}/{name}')
for name in ('fig_experimental_signatures.pdf', 'beyond_the_spectrum_trilogy.pdf'):
    archive(f'{MA}/{name}')
for name in os.listdir(MA):
    if name.startswith('paper_divulgacao_cientifica_quantum_gravity') and os.path.splitext(name)[1] in ('.md', '.pdf', '.tex'):
        move(f'{MA}/{name}', f'{P}/Divulgacao_e_Ensino/{name}')

# 4. old audit/certificate/verdict reports and old release notes anywhere in paper folders
report_pat = re.compile(r'(PROOF_AUDIT|CERTIFICATE|VERDICT|CLAUDE_.*AUDIT|AUDIT_REPORT|REFEREE_REPORT|RELEASE_NOTES|'
                        r'claude_audit|claude_final|claude_grounded|claude_deep|claude_autonomous|claude_pass|'
                        r'RESPONSE_TO_REVIEWER|ZENODO_RETROACTIVE|ZENODO_LEAN4_CONCORDANCE|LEDGER_YANG_MILLS|proof_audit_report)',
                        re.I)
for top in (MA, f'{P}/submission_package_jhep_scipost'):
    for dirpath, dirnames, filenames in os.walk(top):
        dirnames[:] = [d for d in dirnames if d not in ('.lake', '.git', '__pycache__')]
        for fn in filenames:
            path = f'{dirpath}/{fn}'.replace('\\', '/')
            if report_pat.search(fn) and not fn.startswith('CORRECTIONS_'):
                archive(path)

# 5. backup copies anywhere in the project (except the intentional audit baseline and the archive itself)
bak_pat = re.compile(r'(\.bak$|\.bak\.|_backup|backup_|\(1\)|_copy\b|^formal_proofs_.*\.zip$)', re.I)
for dirpath, dirnames, filenames in os.walk(P):
    d = dirpath.replace('\\', '/')
    if '/_arquivo' in d or '/audit/baseline_v2.2' in d or '/.lake' in d:
        dirnames[:] = []
        continue
    for fn in filenames:
        if bak_pat.search(fn):
            archive(f'{d}/{fn}')

# 6. submission package: outdated cover letters, manifest and old test scripts
SP = f'{P}/submission_package_jhep_scipost'
for fn in ('COVER_LETTER_JHEP.md', 'COVER_LETTER_SCIPOST.md', 'ARXIV_METADATA_MANIFEST.md',
           'stress_test_hypothesis_ricci_bound.py', 'verify_master_manuscript_numerical.py'):
    archive(f'{SP}/{fn}')

# 7. regenerable artifacts (deleted)
art_ext = ('.aux', '.out', '.toc', '.synctex.gz', '.fls', '.fdb_latexmk')
for dirpath, dirnames, filenames in os.walk(P):
    d = dirpath.replace('\\', '/')
    if '/.lake' in d or '/_arquivo' in d:
        dirnames[:] = []
        continue
    for dn in list(dirnames):
        if dn == '__pycache__':
            deletes.append(f'{d}/{dn}')
            dirnames.remove(dn)
    for fn in filenames:
        path = f'{d}/{fn}'
        if (fn.endswith(art_ext) or (fn.endswith('.log') and fn != 'build_pdfs_safe.log')) and path not in tracked:
            deletes.append(path)

# de-duplicate (a path may match several rules; keep the first)
seen, plan = set(), []
for s, t in moves:
    if s not in seen and not any(s.startswith(x + '/') for x in seen):
        seen.add(s); plan.append((s, t))

print(f'moves: {len(plan)}   artifact deletions: {len(deletes)}')
for s, t in plan:
    print(f'  MOVE {s}  ->  {t}')
print(f'  (+ {len(deletes)} build artifacts / __pycache__ to delete)')

if APPLY:
    os.makedirs(ARQ, exist_ok=True)
    with open(f'{ARQ}/MANIFESTO.tsv', 'a', encoding='utf-8') as man:
        for s, t in plan:
            os.makedirs(os.path.dirname(t), exist_ok=True)
            shutil.move(s, t)
            man.write(f'{s}\t{t}\n')
    for p in deletes:
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
        elif os.path.exists(p):
            os.remove(p)
    # release bundle: zenodo_upload_* -> releases/<date>/ (tracked note moved with git mv)
    for name in os.listdir(P):
        if name.startswith('zenodo_upload_'):
            src, dst = f'{P}/{name}', f'{P}/releases/{name.replace("zenodo_upload_", "")}'
            os.makedirs(dst, exist_ok=True)
            for fn in os.listdir(src):
                s, t = f'{src}/{fn}', f'{dst}/{fn}'
                if s in tracked:
                    subprocess.run(['git', 'mv', s, t], check=True)
                else:
                    shutil.move(s, t)
            os.rmdir(src)
            print('release folder ->', dst)
    print('done; manifest:', f'{ARQ}/MANIFESTO.tsv')
