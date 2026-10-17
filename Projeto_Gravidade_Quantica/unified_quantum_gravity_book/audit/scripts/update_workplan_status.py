"""Set the Status column of WORKPLAN.md register rows.

Edit STATUS below (one entry per finding, current status only) and run from the book folder.
The script refuses to run if a finding ID appears twice, so a stale entry cannot silently
override a newer one.
"""
import ast
import re
import sys

STATUS = {
    'F-66': '**verificado** 2026-10-17 (cap. 10: sementes 1000–1005, professor e normalização declarados; faixa corrigida para 1,57–1,75; laço F-02)',
    'F-65': '**verificado** 2026-10-17 (cap. 2: passeio preguiçoso simples declarado; pesos só pela distância; "analogue" de Ni et al.; laço F-02)',
    'F-64': '**verificado** 2026-10-16 (laço iterativo: r1 `audit/verify/F64_critique_r1.md` 0/1/9, r2 `fixes_F64_r2_2026-10-16.md`, r3 `F64_critique_r3.md` 0/0/3, r4 `F64_critique_r4.md` 0/0/0 CONVERGIU)',
    'F-29': '**verificado** 2026-10-17 (L2 técnico 2026-10-16; texto confirmado pelo autor em 2026-10-17)',
    'F-28': '**verificado** 2026-10-16 (L2: audit/verify/L2_status_2026-10-16.md); DOIs de Koide, LiteBIRD, Hirani, Ryu-Takayanagi e Ambjorn resolvidos (200) e conferidos',
    # --- verified (full cycle: blind referee, independent correction, targeted re-check) ---
    'F-03': '**verificado** 2026-09-25 via F-41 (cap. 13 reauditado às cegas, corrigido e reverificado)',
    'F-07': '**verificado** 2026-09-25 via F-40/F-42 (caps. 11 e 12)',
    'F-13': '**verificado** 2026-09-25 via auditoria cega do cap. 8 + F-43',
    'F-14': '**verificado** 2026-09-25 via auditoria cega do cap. 8 + F-43',
    'F-16': '**verificado** 2026-09-25 (Estabrook conferido na auditoria cega do cap. 8)',
    'F-17': '**verificado** 2026-09-25 via F-40',
    'F-32': '**verificado** 2026-09-25 via F-40 (cap. 11 reauditado às cegas, corrigido e reverificado)',
    'F-37': '**verificado** 2026-09-25 (camadas 1, 2 e 2-residual: `audit/verify/L2_residual_2026-09-25.md`)',
    'F-38': '**verificado** 2026-09-26 (`L2_residual_2026-09-25.md`, Rodada 2); obs. B: citar Fricke–Vogt/Goldman para (trA, trB, trAB)',
    'F-39': '**verificado** 2026-09-26 (`L2_residual_2026-09-25.md`, Rodada 2); obs. B: "at least about 48, 72, 96" e "loss at least ε"',
    'F-40': '**verificado** 2026-09-25 (caps. 11 e 12; `L2_residual_2026-09-25.md`)',
    'F-41': '**verificado** 2026-09-25 (camada 1 `ch13_blind.md`; correção `fixes_F41-F43.md`; camada 2 `L2_F41-F43.md`)',
    'F-42': '**verificado** 2026-09-25 (inclui prior art Sotiriou–Visser–Weinfurtner PRD 84 (2011) 104018 conferido no fonte arXiv; redução 4D numérica 1e-14)',
    'F-43': '**verificado** 2026-09-25 (camada 1 `ch08_blind.md`; correção `fixes_F41-F43.md`; camada 2 `L2_F41-F43.md`; Teorema 3.3 novo conferido)',
    'F-44': '**verificado** (camada 2) 2026-09-25; sem camada 1 cega específica do trecho',
    # --- corrected, awaiting layer 2 ---
    'F-15': '**verificado** 2026-10-07: caps. 1–13, todo teorema tem prova, citação clássica ou virou conjectura/remark (camadas 1–2; caps. 1–6 fechados por `L2_F45-F50.md` + `L2_final_integration.md`)',
    'F-45': '**verificado** 2026-09-26 (camada 2 `audit/verify/L2_F45-F50.md`; I_m ~ m^x provado e conferido)',
    'F-49': '**verificado** 2026-09-26 (camada 2 `L2_F45-F50.md`; nova fórmula de inversão e γ = 1 conferidos)',
    'F-46': '**verificado** 2026-10-07 (camada 2 curta `audit/verify/L2_final_integration.md`; Navier/H⁴ conferido)',
    'F-47': '**verificado** 2026-10-07 (camada 2 curta `audit/verify/L2_final_integration.md`; §6.4 conferido)',
    'F-48': '**verificado** 2026-10-07 (camada 2 curta `audit/verify/L2_final_integration.md`; títulos conferidos)',
    'F-50': '**verificado** 2026-10-07 (camada 2 curta `audit/verify/L2_final_integration.md`; Problema 2.3 sobre K×K não trivial nos dois sentidos, script independente; obs. B: E_k(h_j) cresce devagar, log diz limitada)',
    'F-51': '**verificado** 2026-10-07 (camada 2 curta `audit/verify/L2_final_integration.md`; 13 títulos, 24 bibliografias, 21 refs cruzadas; obs. B: pdftitle do cap. 11, 1 vs 1,2e-60 s caps. 12/13)',
    'F-58': '**verificado** 2026-10-07: o prefácio (l. 97) e o Dicionário (l. 175) foram reescritos, sem caminho BookReal e sem afirmação sobre o cap. 12 (`audit/verify/fixes_F58.md`, por um corretor); a conferência do texto e do grep foi feita pelo orquestrador; build 0/0/0',
    'F-24': '**verificado** 2026-10-16 (L2: audit/verify/L2_status_2026-10-16.md); README_SKELETON.md em formal_proofs_lean4 e nas pastas Lean dos papers; SpectralDimension.lean continua inconsistente (esqueleto, registrado no README); alterações Lean não commitadas pendentes de decisão (ver L2)',
    'F-01': '**verificado** 2026-10-16 (L2: audit/verify/L2_status_2026-10-16.md); esqueletos com README_SKELETON.md, nenhuma afirmação de verificação fora de formal_proofs_mathlib; obs. B: alinhar a seção Scope do README de formal_proofs_mathlib e a lista de capítulos do README raiz',
    'F-52': '**verificado** 2026-10-07: os 3 passos do resgate do cap. 14 estão integrados e verificados. (1) Gota (CCC teardrop, r*(a) = profundidade clássica do Ω-turn, não nova; contribuição: minimalidade em F_a e o cenário de corredor) → cap. 9, sec:mouth_uturn (`audit/verify/L2_F52_gota.md`). (2) Chattering (Robbins 1980 creditado; Lema wall_structure provado; Conj. W) → cap. 7, l. 246–434 (`audit/verify/L2_F52_chattering.md`). (3) Nash–Kuiper (Prop. ball_bound) → cap. 7 (`audit/verify/L2_F52_nash_kuiper.md`). O cap. 14 em si continua fora do master. Obs.: no cap. 7 surgiram 2 underfull vbox novos por reflow (fora do gate).',
    'F-20': 'livro **verificado** 2026-10-07 (camada 2 curta `audit/verify/L2_final_integration.md`; forma única de d_s e α_t, quadratura 2e-10, mutações falham); `formal_proofs_lean4/SpectralDimension.lean` continua inconsistente (pendente com F-24)',
    'F-63': '**verificado** 2026-10-11 (correção do fechamento; camada 2 `audit/verify/L2_FECHAMENTO_LIVRO_2026-10-11.md`)',
    # --- older corrections (first sessions); superseded where a blind audit covered the chapter ---
    'F-04': 'corrigido 2026-09-24 (fórmula retirada); cap. 12 reauditado às cegas (F-42 verificado)',
    'F-05': 'corrigido 2026-09-24; cap. 12 reauditado às cegas (F-42 verificado)',
    'F-06': 'corrigido 2026-09-24 (Prop. 4.1 + Conj. 4.3); Conj. 4.3 reespecificada em F-42 (verificado)',
    'F-08': 'corrigido (cap. 12 via F-42, verificado; cap. 2 via F-48, aguarda camada 2)',
    'F-09': 'corrigido 2026-09-24; abstracts dos caps. 12–13 reauditados (F-41, F-42 verificados)',
    'F-10': 'corrigido; prior art ampliado em F-41/F-42 (verificados)',
    'F-11': '**verificado** 2026-09-26 via F-42 (cap. 12) e F-45 (cap. 3)',
    'F-12': '**verificado** 2026-10-16 (L2: audit/verify/L2_status_2026-10-16.md); Thm. 3.1 inclui 16πG_Nρ, hipótese κ*<∞ explícita, (iii) removido',
    'F-22': 'corrigido; cap. 12 §7 reauditado (F-42, F-44 verificados)',
    'F-25': '**verificado** 2026-09-26 via F-45 (cap. 3)',
    'F-27': 'corrigido 2026-09-24; sinal confirmado na auditoria cega do cap. 12 (F-42 verificado)',
    'F-33': 'corrigido; ver F-37 (verificado)',
    'F-34': 'corrigido; ver F-43 (verificado)',
    'F-35': 'corrigido; ver F-38 (verificado)',
    'F-36': 'corrigido; ver F-39 (verificado)',
    'F-18': 'corrigido 2026-09-24 em todos os caps. (`audit/scripts/lint_tex.py --fix`)',
    'F-26': 'corrigido 2026-09-24 (abstract do cap. 8 encurtado; 0/0/0)',
    'F-30': 'corrigido (todos os caps. compilam 0/0/0; build seguro `../build_pdfs_safe.py`)',
    # --- structural / author decisions ---
    'F-02': '**verificado** 2026-10-17: caps. 1–13 com oráculo independente e controle negativo; caps. 2, 4, 5, 8, 10, 11 pelo laço (r1 0/10/24, r3 0/0/7, r5 0/1/5, r6 CONVERGIU; `audit/verify/F02_*`, `fixes_F02_r6_2026-10-17.md`): 71 afirmações verificadas, 0 falhas, 27 não verificáveis',
    'F-19': '**verificado** 2026-10-07: build oficial por fonte única (`build_pdfs_safe.py`, padrão; `--legacy-master` disponível), aprovado pelo autor; master com 0 erros, 0 warnings, 0 overfull, 0 undefined e 268 pp (`_single_source_prototype/ADOCAO_F19.md`, `audit/verify/fixes_overfull_master.md`). O Dicionário segue via includepdf (conflito de macros).',
    'F-21': '**verificado** 2026-10-17 (L2 técnico 2026-10-16; texto confirmado pelo autor em 2026-10-17)',
    'F-23': '**verificado** 2026-10-16 (`audit/verify/L2_status_2026-10-16.md`; o último resíduo, o LEDGER "PASSED" do BtS III, foi arquivado em `Manuscritos_Avulsos/paper_beyond_the_spectrum_3/audit/archive/` com nota, commit a875574)',
}


def check_no_duplicates():
    """Parse this file and refuse duplicated keys in the STATUS literal."""
    tree = ast.parse(open(__file__, encoding='utf-8').read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(getattr(t, 'id', '') == 'STATUS' for t in node.targets):
            keys = [k.value for k in node.value.keys]
            dup = sorted({k for k in keys if keys.count(k) > 1})
            if dup:
                sys.exit(f'duplicate keys in STATUS: {dup}')


check_no_duplicates()
p = 'WORKPLAN.md'
lines = open(p, encoding='utf-8').read().split('\n')
n = 0
for i, line in enumerate(lines):
    m = re.match(r'^\| (F-\d\d) \|', line)
    if m and m.group(1) in STATUS:
        cells = line.split(' | ')
        cells[-1] = STATUS[m.group(1)] + ' |'
        lines[i] = ' | '.join(cells)
        n += 1
open(p, 'w', encoding='utf-8').write('\n'.join(lines))
print('updated', n)
