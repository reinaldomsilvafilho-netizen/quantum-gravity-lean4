"""Set the Status column of WORKPLAN.md register rows.

Edit STATUS below (one entry per finding, current status only) and run from the book folder.
The script refuses to run if a finding ID appears twice, so a stale entry cannot silently
override a newer one.
"""
import ast
import re
import sys

STATUS = {
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
    'F-15': 'caps. 7–13: todo teorema tem prova, citação clássica ou virou conjectura/remark (verificado nas camadas 1–2); caps. 1–6 aguardam camada 2 de F-45–F-50',
    'F-45': '**verificado** 2026-09-26 (camada 2 `audit/verify/L2_F45-F50.md`; I_m ~ m^x provado e conferido)',
    'F-49': '**verificado** 2026-09-26 (camada 2 `L2_F45-F50.md`; nova fórmula de inversão e γ = 1 conferidos)',
    'F-46': 'corrigido; camada 2 confirmou as provas; o item B residual (Navier/H⁴) foi corrigido em `fixes_final_integration_2026-09-26.md` — aguarda camada 2 curta',
    'F-47': 'corrigido; camada 2 confirmou Kac–Rice; o item B residual (§6.4, Lim) foi corrigido em `fixes_final_integration_2026-09-26.md` — aguarda camada 2 curta',
    'F-48': 'corrigido; camada 2 confirmou a cota de Dyson; título do cap. 1 unificado em `fixes_final_integration_2026-09-26.md` — aguarda camada 2 curta',
    'F-50': 'corrigido; Problema 2.3 reformulado sobre K×K (não é trivialmente falso nem verdadeiro; checagem no log) em `fixes_final_integration_2026-09-26.md` — aguarda camada 2 curta',
    'F-51': 'corrigido 2026-09-26 (títulos unificados; cap. 12 atualizado; 30 referências cruzadas conferidas) — aguarda camada 2 curta',
    'F-20': 'corrigido no livro 2026-09-26 (caps. 12, 13 e Dicionário com uma única forma de d_s e α_t); `formal_proofs_lean4/SpectralDimension.lean` continua inconsistente (pendente com F-24)',
    # --- older corrections (first sessions); superseded where a blind audit covered the chapter ---
    'F-04': 'corrigido 2026-09-24 (fórmula retirada); cap. 12 reauditado às cegas (F-42 verificado)',
    'F-05': 'corrigido 2026-09-24; cap. 12 reauditado às cegas (F-42 verificado)',
    'F-06': 'corrigido 2026-09-24 (Prop. 4.1 + Conj. 4.3); Conj. 4.3 reespecificada em F-42 (verificado)',
    'F-08': 'corrigido (cap. 12 via F-42, verificado; cap. 2 via F-48, aguarda camada 2)',
    'F-09': 'corrigido 2026-09-24; abstracts dos caps. 12–13 reauditados (F-41, F-42 verificados)',
    'F-10': 'corrigido; prior art ampliado em F-41/F-42 (verificados)',
    'F-11': '**verificado** 2026-09-26 via F-42 (cap. 12) e F-45 (cap. 3)',
    'F-12': 'corrigido 2026-09-24; cotas ADM confirmadas nas auditorias cegas dos caps. 8 e 12',
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
    'F-02': 'caps. 12–13 reescritos (oráculos independentes + controles negativos); caps. 1–11 pendentes',
    'F-19': 'em curso: master recompila limpo, mas ainda via \\includepdf',
    'F-21': 'corrigido 2026-09-24 (prefácio, Tabela 1 removida, declarações em todos os caps.) — **autor deve confirmar o texto sobre uso de IA e a ausência de conflitos**',
    'F-23': 'corrigido 2026-09-24 (auditorias antigas em audit/archive/; CLAUDE.md e README resetados); README do GitHub reescrito 2026-09-25',
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
