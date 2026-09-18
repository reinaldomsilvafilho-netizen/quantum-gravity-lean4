Escrevi a resposta completa ao Pass 8 em `submission_package_jhep_scipost/RESPONSE_TO_REVIEWER_PASS8.md`. Resumo do que o documento contém:

**1. Diagnóstico**: reclassifica todo o manuscrito em três níveis — Tier A (teoremas estritos incondicionais: fluxo espectral, shear ADM, Caffarelli, Nielsen–Ninomiya, cancelamento quártico topológico), Tier B (resultado condicional: Yang–Mills, sujeito a `Ric_∞ ≥ K_QCD` não provado) e Tier C (modelagem fenomenológica: Koide, GST/Cabibbo, Jarlskog, resíduo de Barnes). Propõe novo título removendo "Gauge Condensation".

**2. Substituições LaTeX prontas para colar**, endereçando cada crítica com precisão cirúrgica:
- Novo Abstract sem sobre-reivindicação, com os três tiers explícitos
- Seção 7 reestruturada com `\hypothesis` explícita (`Ric_∞ ≥ K_QCD`) + Teorema condicional + Remark negando explicitamente resolução do Problema do Millennium
- Seção 8.1: Teorema de Koide renomeado "Representation-Theoretic Equivalence", com admissão explícita de 2 parâmetros livres para 3 massas
- Seção 8.2: Cabibbo rotulado "Phenomenological/Semi-Empirical (GST + Color Shift)"; Jarlskog rotulado "Semi-Empirical Evaluation (PDG inputs)"
- Cancelamento de vácuo dividido em Teorema exato + Modelo calibrado separado, com remark explícito "This Is Not a Solution of the Cosmological Constant Problem"
- Tabelas 1 e 4 revisadas com coluna de status honesto e legenda
- Conclusão/Lean 4 rebaixado ao seu papel técnico correto (consistência interna, não validação física)

**3. Plano de atualização do `verify_master_manuscript_numerical.py`** (já lido do disco): nenhum número ou assert muda — só comentários `[EPISTEMIC STATUS]` inseridos em pontos específicos (linhas indicadas) para que os "PASS" não sejam lidos como confirmação de predição quando são, na verdade, confirmação de ajuste calibrado.

Inclui checklist final de fechamento. Nenhuma edição foi aplicada ao `.tex` ou `.py` reais ainda — o documento contém os blocos exatos para você revisar e colar onde indicado.
