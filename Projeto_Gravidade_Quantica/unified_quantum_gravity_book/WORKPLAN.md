# WORKPLAN — *Geometry, Tensors, and Quantum Gravity* (rumo ao arXiv)

Documento vivo. Toda sessão de trabalho (humana ou de agente) **começa lendo este arquivo e termina atualizando-o** (§8 Protocolo).

| Campo | Valor |
|---|---|
| Versão pública | Zenodo, DOI de conceito `10.5281/zenodo.22290043` (sempre a última versão). Versões: v2.2 `22888334` (2026-09-22); mais recente `22939888` (2026-09-24) |
| Repositório público | `github.com/reinaldomsilvafilho-netizen/quantum-gravity-lean4` (remote `origin`) |
| Linha de base desta revisão | 2026-09-24, fontes em `unified_quantum_gravity_book/` (não rastreadas no git — ver T0.1) |
| Próxima versão-alvo | Zenodo v2.3 → submissão arXiv |
| Registro de achados | §3 deste arquivo (IDs `F-xx`) |
| Evidências reproduzíveis | `audit/scripts/` |

---

## 1. Avaliação (2026-09-24)

### 1.1 Escopo do que foi efetivamente lido
- **Lido por completo:** master volume, cap. 12, cap. 13, `ARXIV_PRE_SUBMISSION_REVIEW.md`, Lean `Chap08`, `Chap12`, `NullEnergy.lean`, `SpectralDimension.lean`, `verify_chap12_numerical.py` (partes).
- **Lido parcialmente:** cap. 8 (§§1–6), cap. 6 (teorema principal), cap. 11 (teorema RT).
- **Executado:** os 13 `verify_chapXX_numerical.py` (todos passam) e `audit/scripts/check_ch12_formulas.py`.
- **Ainda NÃO auditado por mim:** caps. 1–5, 7, 9, 10 e o restante dos caps. 6, 8, 11. O juízo sobre esses capítulos fica pendente (Onda 1).

### 1.2 Veredito resumido
O livro tem núcleos matemáticos aproveitáveis. A fórmula fechada de $d_s(\tau)$ (cap. 12 §8.2 / cap. 13) confere numericamente com quadratura em 5 escalas, e os limites em forma de espaço e a célula de Schwarzschild do cap. 8 estão corretos. Mas, **no estado atual, não está pronto para o arXiv**, por três motivos estruturais:

1. **As camadas de verificação dão uma garantia falsa.** As "144 obrigações Lean" são, sem exceção, estruturas com campos `Bool`/`Float` cujo "teorema" devolve a própria hipótese (`h : x = true ⊢ x = true`). Nenhum arquivo de `Book/` importa Mathlib. Os scripts Python incluem testes circulares (ex.: `delta_S_bulk = delta_H`, seguido de uma checagem de igualdade). O prefácio afirma "certifying … hypothesis discharge". Um revisor que abra o repositório vai perceber em minutos, e isso contamina a credibilidade do livro inteiro.
2. **As partes IV–V trazem afirmações físicas falsas ou sem prova**, e algumas contradizem cálculos do próprio livro (F-03 a F-10). As mais graves são as previsões observacionais, que ficam de 60 a 118 ordens de grandeza abaixo do que o texto afirma ser detectável.
3. **O enquadramento excede os teoremas.** O abstract do cap. 12 diz "proves… non-linear Einstein equations", "UV-finite, anomaly-free", enquanto o próprio teorema é linearizado. As auditorias anteriores (`PROOF_AUDIT_*_FINAL/CERTIFIED`, `CLAUDE_*_VERDICT`, `ARXIV_PRE_SUBMISSION_REVIEW`) marcaram PASSED ou "arXiv-ready" em itens que estão errados. **Elas não devem mais ser tratadas como evidência** (F-23).

### 1.3 Recomendação estratégica (decisão do autor — D1)
- **Opção A (recomendada):** separar o livro em (i) um volume matemático rigoroso (Partes I–III, após a auditoria), submetido em `math.CA`/`math.DG`/`math-ph`, e (ii) as Partes IV–V reescritas como *"Speculative outlook / conjectures"*, com cada afirmação física rotulada como conjectura ou ansatz e os números corrigidos.
- **Opção B:** manter um volume único, mas rebaixar os caps. 12–13 a "programa e conjecturas", remover o Lean de `Book/` das alegações até ele ser real, e submeter em `gr-qc` aceitando o risco de moderação.
- Em ambas as opções: ou o Lean vira formalização real de lemas elementares (Mathlib), ou as alegações sobre ele saem do texto (D2).

---

## 2. Arquitetura do trabalho: 8 frentes paralelas

Cada frente tem entradas, saídas e critério de pronto próprios e **não edita arquivos de outra frente**, o que permite rodar tudo em paralelo (worktrees ou agentes separados). Os conflitos só acontecem na Onda 3 (integração).

| Frente | Escopo | Saída | Skills úteis |
|---|---|---|---|
| **W1 Lean** | `formal_proofs_book/`, `formal_proofs_lean4/` | `audit/lean_inventory.md` + módulos reais em Mathlib | `lean4-vacuity-verifier`, `lean4-proof-engineer` |
| **W2 Python** | `verify_chapXX_numerical.py` | suíte `pytest` sem circularidade + `audit/python_audit.md` | `scientific-computing-python`, `python-testing-patterns` |
| **W3 Matemática** (13 sub-trilhas, 1 por capítulo) | `chapXX*.tex` (leitura) | `audit/chXX_claims.md` (ledger de afirmações) | `adversarial-proof-synthesizer`, `proof-checker`, `triadic-proof-verifier` |
| **W4 Física/ordens de grandeza** | caps. 8, 11–13 | `audit/physics_sanity.md` + scripts | `differential-geometry-symbolic`, `verify-claims` |
| **W5 Literatura/prior art** | bibliografias | `audit/prior_art.md` | `math-physics-references`, `scholarly-metadata-resolver`, `citation-verification` |
| **W6 Enquadramento** | abstracts, intro, conclusões, prefácio | diffs de texto | `materialist-scientific-conception` |
| **W7 Build/LaTeX/arXiv** | preâmbulos, master, pacote | build limpo + `arxiv_bundle/` | — |
| **W8 Release** | Zenodo, GitHub, CHANGELOG | `CHANGELOG.md`, notas de versão | `zenodo-monograph-publisher` |

### Protocolo de W3 (por capítulo, idêntico nos 13)
Para **cada** `theorem/proposition/lemma/corollary` o ledger `audit/chXX_claims.md` registra:

| Campo | Valores |
|---|---|
| ID | `C12-T2.1` (capítulo-tipo-número) |
| Tipo | `clássico-citado` · `novo-provado` · `novo-esboço` · `conjectura` · `heurística/ansatz` · `definição disfarçada` |
| Prova no texto? | completa / esboço / ausente / delega a outro cap. (qual) |
| Hipóteses descarregadas? | sim / não (lista) |
| Checagem independente | à mão · SymPy · numérica (oráculo independente) · Lean real · nenhuma |
| Achados | `F-xx` |
| Ação | manter · reescrever prova · rebaixar a conjectura · citar como clássico · remover |

Regra: **teorema sem prova vira proposição citada (se clássico) ou conjectura (se novo)**. Os achados novos entram no §3 com o próximo ID livre.

### Regras de W2 (testes numéricos)
1. O valor esperado **nunca** é produzido pelo mesmo código que o valor testado. É preciso ter um oráculo independente (quadratura × forma fechada, diferença finita × derivada analítica, literatura × cálculo).
2. Todo teste precisa de um **controle negativo**: uma mutação da fórmula (troca de sinal, fator 2) tem de fazer o teste falhar (mutation testing).
3. `assert x > 0` para uma constante não é teste. Remover.
4. Tolerâncias justificadas (erro de truncamento ou arredondamento estimado).

### Regras de W1 (Lean)
- **Nível 0:** apagar ou isolar as estruturas `Bool`-tautológicas. Elas não podem ser chamadas de "obrigações certificadas" em lugar nenhum.
- **Nível 1:** formalizar em Mathlib os lemas elementares genuínos, por exemplo: limites de $e_2$ em $[-a,a]^3$ e $K_{ij}K^{ij}\le 3a^2$ (C12-T3.1), a equivalência de Koide ⇔ ângulo de 45°, a identidade Gram/Cartan de $A_{m-1}$, os autovalores da Hessiana $\{2,-1,-1\}$ e os limites de $d_s$ para o *ansatz* racional.
- **Nível 2:** afirmações profundas ficam como `def Claim : Prop` **sem prova**, listadas como abertas. Nunca como `theorem` com hipótese igual à tese.
- A tabela de cruzamento `\label` LaTeX ↔ declaração Lean ↔ nível fica em `audit/lean_inventory.md`, e só ela pode ser citada no prefácio.
- Alinhar o toolchain: o prefácio diz v4.29/v4.33, `lean-toolchain` diz `v4.35.0-rc2`.

---

## 3. Registro de achados

Severidade: **C** crítico (bloqueia arXiv) · **A** alto (erro matemático/físico) · **M** médio · **B** baixo.
Status: `aberto` · `em curso` · `corrigido` (commit/hash) · `verificado` (checagem adversarial independente) · `descartado` (com motivo).

| ID | Sev | Local | Achado | Evidência | Ação proposta | Status |
|---|---|---|---|---|---|---|
| F-01 | C | `formal_proofs_book/Book/**` | As 144 "obrigações" são projeções de campos `Bool`/`Float` (`h : x = true ⊢ x = true`). Nenhum `import Mathlib`. Só `BookReal/Chap01` tem conteúdo real (2 lemas triviais). | `Chap12/GrandUnification.lean:15-23`, `Chap08/NonEuclideanADM.lean:32-44`; perfil: 0 imports em todos os `Book/*.lean` | W1 níveis 0–2; reescrever prefácio e Tabela 1 (F-21) | aberto |
| F-02 | C | `verify_chap12_numerical.py:100,167` | Testes circulares: `delta_S_bulk = delta_H` e depois checa igualdade; "MSS" testa `2π > 0`. Os outros 12 scripts ainda não foram auditados. | leitura do código | W2 em todos os 13 scripts | caps. 12–13 reescritos (oráculos independentes + controles negativos); caps. 1–11 pendentes |
| F-03 | C | cap. 13 (eq. Δt, α_t, tabela, Fig. 1); cap. 12 §9 | Com a própria fórmula: Δt_disp ≈ **9·10⁻⁶³ s** (1 Gpc, 10–1000 Hz), não "~ms". α_t(k=0,05 Mpc⁻¹) ≈ **−7·10⁻¹¹⁸**, invisível em ℓ~1500–4000. ℓ_P/λ_dB ~ 10⁻²⁴, não 10⁻¹⁹. A Fig. 1(a)(b) é incompatível com as fórmulas. | `audit/scripts/check_ch12_formulas.py` | Refazer a seção com números corretos. Declarar que não é observável ou mudar o modelo (ex.: escala de energia livre $M_\ast \ll M_P$ como parâmetro). Regenerar a figura a partir de script versionado. | **verificado** 2026-09-25 via F-41 (cap. 13 reauditado às cegas, corrigido e reverificado) |
| F-04 | A | cap. 12 §7 (J_CP) | A fórmula $\sin\delta\,\sqrt{\prod m_q}/(6\sqrt3\,v^6)$ tem dimensão GeV⁻³ e dá **1,1·10⁻¹⁷**, não 3,04·10⁻⁵. | script acima | Corrigir ou remover. Declarar a contagem de parâmetros livres. | corrigido 2026-09-24 (fórmula retirada); cap. 12 reauditado às cegas (F-42 verificado) |
| F-05 | A | cap. 12 §8.3 | Semiesferas ortogonais à fronteira são **totalmente geodésicas** no semiespaço de Poincaré (H=0, verificado). São estacionárias sob MCF, então R(t)=R₀e^{−t/L} e dS/dt≠0 são falsos. O próprio `verify_chap12` (bateria 6) trata a semiesfera como mínima. | script acima (curvatura geodésica = 0) | Remover ou refazer com uma superfície de teste não mínima | corrigido 2026-09-24; cap. 12 reauditado às cegas (F-42 verificado) |
| F-06 | A | cap. 12 Thm 4.1; cap. 8 §1.2; cap. 13 | (i) vale para curvas **tipo-tempo**, mas os laços de LQG em Σ são **tipo-espaço**, então (ii) não decorre de (i). (iii) o fechamento da álgebra quântica de vínculos é problema aberto e é "provado" em 3 linhas. A identidade de Mandelstam para SU(2) é $W_\alpha W_\beta = W_{\alpha\beta}+W_{\alpha\beta^{-1}}$, não $W_{\alpha\circ\beta}=W_\alpha W_\beta$. Usa uma *conjectura* (Hawking) como hipótese. | leitura | Rebaixar (ii)–(iii) a conjectura. Corrigir Mandelstam. Remover o teste de interferometria atômica (F-03). | corrigido 2026-09-24 (Prop. 4.1 + Conj. 4.3); Conj. 4.3 reespecificada em F-42 (verificado) |
| F-07 | A | cap. 12 Thm 7.1; cap. 11 | A complexidade de Kac–Rice do p-spin esférico ≠ entropia do SYK ≠ Bekenstein–Hawking. O SYK só satura λ_L=2π/β no limite βJ→∞. Enunciado sem prova. | literatura (Maldacena–Stanford 2016) | Rebaixar a analogia/conjectura com hipóteses explícitas | **verificado** 2026-09-25 via F-40/F-42 (caps. 11 e 12) |
| F-08 | A | cap. 12 Thm 5.1, §8.4; cap. 2 | A curvatura de Ollivier é limitada inferiormente (κ ≥ −2 com métrica de grafo), logo κ ≤ −c/ε com ε→0 é impossível. Convergência em norma de corte **não** produz variedade 4D nem métrica de Einstein. | definição de Ollivier | Reformular como modelo de brinquedo explícito ou remover "condensação em variedade de Einstein" | corrigido (cap. 12 via F-42, verificado; cap. 2 via F-48, aguarda camada 2) |
| F-09 | A | abstract e conclusão do cap. 12; cap. 13 | O abstract afirma que prova Einstein **não linear**; o Thm 4.1 é linearizado. A conclusão fala em "UV-finite, anomaly-free"; o cap. 13 diz "exact non-perturbative unification". | leitura | W6: o abstract só pode afirmar o que os teoremas provam | corrigido 2026-09-24; abstracts dos caps. 12–13 reauditados (F-41, F-42 verificados) |
| F-10 | A | cap. 12 Thm 2.1, §8.2; cap. 13 | α é definido em (0,1) e depois usado em α=2. $d_s=m/\alpha$ é constante (não "corre"). A redução 4→2 com $k^2+\ell^2k^4$ é conhecida (Hořava 2009; Sotiriou–Visser–Weinfurtner 2011; Calcagni) e não é citada. §8.2 usa coeficiente 1, §9/cap. 13 usam ξ=½ "derivado" dele. **Crédito:** a forma fechada de $d_s(\tau)$ está correta (confere com quadratura). | script acima | Corrigir o domínio de α, citar o prior art, unificar ξ, remover "we now prove" | corrigido; prior art ampliado em F-41/F-42 (verificados) |
| F-11 | M | cap. 12 Thm 2.2 (e cap. 3 correspondente) | $\sum v_i^2 = c^\top A_{m-1}c$ em coordenadas de raízes, então o fator $m/4x$ deveria ser $m/2x$. Mistura vetor de dimensão $m$ com matriz $(m-1)\times(m-1)$. Qualquer forma $S_m$-invariante no hiperplano soma-zero tem essa estrutura, então "gauge symmetries emerge" não se sustenta. | álgebra | Corrigir o fator, explicitar as coordenadas, retirar a leitura física | **verificado** 2026-09-26 via F-42 (cap. 12) e F-45 (cap. 3) |
| F-12 | M | cap. 12 Thm 3.1 | (i)–(ii) corretos, mas elementares. Omite o termo de matéria 16πρ. (iii) "evita singularidades" pressupõe κ*<∞ (circular). A existência do minimizador não é tratada. Chama o vínculo clássico de "Wheeler–DeWitt". | leitura | Rotular como lema elementar e remover (iii) ou dar hipóteses | corrigido 2026-09-24; cotas ADM confirmadas nas auditorias cegas dos caps. 8 e 12 |
| F-13 | A | cap. 8 Thm "Minimax Throat" e "Apparent Horizon"; tabela §5 | Em fatias t=const de espaços estáticos, K_ij=0. A esfera da garganta é superfície **mínima** na fatia (curvatura ∝ √(1−b/r)/r = 0 em r₀), então $K^\theta_\theta=1/r_0$ está errado. O horizonte de Kerr não é redondo, então um valor único $1/r_+$ está errado. | geometria padrão | Refazer com definições corretas | **verificado** 2026-09-25 via auditoria cega do cap. 8 + F-43 |
| F-14 | A | cap. 8 §4 (slingshot) | O complemento de bolas em ℝ³ é **simplesmente conexo** (π₁ trivial), não $\mathbb F_m$: não há classes de enrolamento W=±1 em 3D. $V_{\rm eff}$ é finito em r=3M, então a divergência afirmada não tem base. | topologia padrão | Restringir ao caso planar (equatorial) ou remover | **verificado** 2026-09-25 via auditoria cega do cap. 8 + F-43 |
| F-15 | M | caps. 8, 10, 12 | Cap. 8: 14 ambientes de teorema e **1** prova. Cap. 10: 2 teoremas, 0 provas. Cap. 12: RT–MCF e Kac–Rice sem prova. Resultados clássicos (Gauss–Codazzi, ADM, Israel) rotulados como "Theorem" sem indicar que são clássicos. | `grep` | Protocolo W3 | caps. 7–13: todo teorema tem prova, citação clássica ou virou conjectura/remark (verificado nas camadas 1–2); caps. 1–6 aguardam camada 2 de F-45–F-50 |
| F-16 | B | cap. 8 tabela, linha Schwarzschild | $3\sqrt3M^2/(2r^3)$ está **correto** (fatia-limite de Estabrook et al. 1973, $|K^r_r|$). O alerta do review anterior era falso. Falta citação e falta dizer que o sup é atingido em r=3M/2. | cálculo | Citar e esclarecer | **verificado** 2026-09-25 (Estabrook conferido na auditoria cega do cap. 8) |
| F-17 | M | cap. 11 Thm RT–MCF | A prova só dá a cota superior S ≤ (#cortes)·log χ. A igualdade, a unicidade e a convergência da MCF são afirmadas sem prova (a MCF pode singularizar; há transições de fase entre superfícies RT). | leitura | Rebaixar/refazer | **verificado** 2026-09-25 via F-40 |
| F-18 | B | cap. 8 (linhas 126,164,200,231,…,206) | Artefatos de Markdown no LaTeX: linhas `---` (viram travessões) e `**…**`. | `grep` | W7: lint automático em todos os capítulos | corrigido 2026-09-24 em todos os caps. (`audit/scripts/lint_tex.py --fix`) |
| F-19 | M | `master_book_…tex` | O master monta o livro via `\includepdf` de PDFs compilados à parte. O arXiv exige fonte; numeração, hyperlinks e bibliografias ficam fragmentados; há preâmbulos diferentes (amsart/revtex). | leitura | W7: build único a partir de fonte (`\input`, preâmbulo e bibliografia únicos) | em curso: master recompila limpo, mas ainda via \includepdf |
| F-20 | M | Lean `SpectralDimension.lean` × cap. 13 × cap. 12 | Três formas incompatíveis: Lean $d_s=(4+2k)/(1+k)$, $\alpha_t=-k/(1+k)$; cap. 13 $d_s=2+2/(1+(k/M_P)^2)$; cap. 12 $\alpha_t=-1/(1+(k/M_P)^{-2})$. | leitura | Uma única fonte de verdade | corrigido no livro 2026-09-26 (caps. 12, 13 e Dicionário com uma única forma de d_s e α_t); `formal_proofs_lean4/SpectralDimension.lean` continua inconsistente (pendente com F-24) |
| F-21 | C | prefácio, Tabela 1, README | "144 obligations… zero axioms… certifying hypothesis discharge", "tripartite epistemic architecture". Falso enquanto F-01/F-02 estiverem abertos. A declaração de IA ("strictly for language editing… LaTeX") precisa refletir fielmente o uso real de IA no projeto (auditorias, geração de provas e código). Decisão do autor. | leitura | Reescrever após W1/W2 | corrigido 2026-09-24 (prefácio, Tabela 1 removida, declarações em todos os caps.) — **autor deve confirmar o texto sobre uso de IA e a ausência de conflitos** |
| F-22 | M | cap. 12 §7 (Higgs, Koide, $Q_q$) | $m_H^{(0)}=v/2$ mais Δλ=+0,0044 ajustado ⇒ ajuste, não previsão. Koide é reformulação conhecida (ângulo de 45°). | aritmética | Contar parâmetros × observáveis; mover para apêndice fenomenológico | corrigido; cap. 12 §7 reauditado (F-42, F-44 verificados) |
| F-23 | C | `PROOF_AUDIT_*`, `CLAUDE_*VERDICT*`, `ARXIV_PRE_SUBMISSION_REVIEW.md`, CLAUDE.md §1–2 | Auditorias anteriores marcaram PASSED/"arXiv-ready" em itens errados (ex.: cap. 13, F-03; Lean, F-01). O CLAUDE.md propaga esses status. | este registro | Mover para `audit/archive/`, resetar os status no CLAUDE.md para "em reauditoria" | corrigido 2026-09-24 (auditorias antigas em audit/archive/; CLAUDE.md e README resetados); README do GitHub reescrito 2026-09-25 |
| F-24 | M | `formal_proofs_lean4/` (paper do functor, "PASSED FINAL") | Também sem Mathlib. A "NEC" é soma de quadrados de uma `List Int`. Mesmo padrão de F-01, em outro projeto já publicado. | `NullEnergy.lean` | Incluir no escopo do W1 | aberto |

| F-25 | M | cap. 3, teorema "Continuum Limit and Emergence of the $A_{m-1}$ Cartan Metric" | A matriz exibida (2 na diagonal, **+1** fora) não é a matriz de Cartan (tridiagonal 2, −1). É a matriz de Gram das raízes $e_i-e_m$, integralmente congruente à de Cartan. | leitura, linha ~561 | Renomear e explicitar a mudança de base | **verificado** 2026-09-26 via F-45 (cap. 3) |
| F-27 | A | cap. 12 §6, eq. do fluxo de Ricci de graphons | Sinal invertido ($-2\kappa W$) em relação ao cap. 2 ($+2\kappa W$). Com ele, gargalos de curvatura negativa **cresceriam**. Detectado pelo novo teste independente (bateria 4). | `verify_chap12_numerical.py` | Sinal corrigido e explicado no texto | corrigido 2026-09-24; sinal confirmado na auditoria cega do cap. 12 (F-42 verificado) |
| F-28 | A | bibliografias, caps. 3, 6, 7, 8, 11, 12, 13 | DOIs errados ou títulos divergentes: Koide (DOI de outro artigo), LiteBIRD (dígito final), Willmore 1965 (DOI de capítulo de 2021), Hirani (DOI SSRN de outro trabalho), Azagra–Ferrera (título/periódico não batiam), Samko (DOI inexistente), Falconer (DOI da 2ª ed.), títulos de Ambjørn et al. e Ryu–Takayanagi | `audit/scripts/check_references.py`, `audit/references_report.md` | Corrigidos por `fix_references_2026_09_24.py`; restam 12 obras antigas/livros sem DOI (aceitável) | corrigido 2026-09-24 |
| F-29 | M | todos os caps. e master | Faltavam declarações de financiamento (em 6 caps.), de uso de IA, de conflito de interesses e de disponibilidade. A licença do Dicionário ("All Rights Reserved") contradizia o CC BY 4.0 do Zenodo. | leitura; API Zenodo | `declarations_chapter.tex` incluído em todos os caps.; seção Declarations no master; licença corrigida | corrigido 2026-09-24 — **confirmar com o autor** |
| F-30 | B | caps. 2, 3, 5, 8 | Overfull boxes pré-existentes (≤ 2 pt, na maioria `vbox`) | logs | Ajuste de layout | corrigido (todos os caps. compilam 0/0/0; build seguro `../build_pdfs_safe.py`) |
| F-31 | M | Dicionário | Repetia as afirmações retiradas (144 obrigações "Mathlib verified", slingshot, pinch-off em tempo finito, sinais observáveis, UV-finite) | leitura | Reescrito com status provado/conjectura/ansatz | corrigido 2026-09-24 |
| F-32 | M | cap. 11 (linhas ~121, ~481) | "the spacetime metric manifold rigorously emerges"; "GR and QFT can be mathematically reconciled": o mesmo excesso de enquadramento de F-09 | leitura | W6 | **verificado** 2026-09-25 via F-40 (cap. 11 reauditado às cegas, corrigido e reverificado) |
| F-26 | B | cap. 8, página do sumário | `Overfull \vbox (1.6pt)`, já presente na linha de base v2.2 | log | Ajuste fino de layout | corrigido 2026-09-24 (abstract do cap. 8 encurtado; 0/0/0) |
| F-33 | A | cap. 7 (quase todo) | Cinco enunciados **falsos**: piso de curvatura de fronteira (desigualdade invertida; disco plano), princípio de exclusão por obstáculo (falha para obstáculo convexo), cota da sagitta, isotropia de subvariedades calibradas (curvas complexas: razão 1/2), curvaturas das multi-hélices na tabela (amplitude errada). Invariância de regularidade, Γ-convergência DEC e positividade do conjunto saturado sem prova. Cilindro apresentado como ótimo não é. Tabela "n≤12" com linhas sem derivação. | `audit/scripts/check_ch07.py`; `audit/ch07_claims.md` | Reescrever: provar o que é elementar, rebaixar o resto | corrigido; ver F-37 (verificado) |
| F-34 | A | cap. 8 §6–7 | "Non-Euclidean Regularity Invariance" com prova inválida (mollifier com corte em escala ε² faz os termos em χ'' divergirem) e apoiada no teorema do cap. 7 agora rebaixado. Tabela de "minimax κ*" que mostra só candidatos; linha AdS₅×S⁵ inconsistente (k=5, "4-brane"); FLRW com 3H (traço) em vez de H. Usava o "teorema de Γ-convergência" do cap. 7. | leitura | Rebaixar a conjectura; corrigir a tabela | corrigido; ver F-43 (verificado) |
| F-35 | A | cap. 9 (T1.4, P1.2, §1.3, T4.2, P5.1) | Corte finito de enrolamento apoiado numa restrição de comprimento arbitrária (sem limite de comprimento, o enrolamento é ilimitado com curvatura fixa), e vetores de enrolamento não separam classes (comutadores). Equivariância por MCG falsa (automorfismo não interno). Retração n-dim → 1-esqueleto livre falsa. Γ-convergência "certificada" sem prova. **Benchmark de 50,6% falso**: pelo lema do U-turn, as duas classes têm κ* = 1/H. | `audit/scripts/check_ch09.py`; `audit/ch09_claims.md` | Reescrever com enunciados provados | corrigido; ver F-38 (verificado) |
| F-36 | A | cap. 10 (T2.1, T2.2, abstract) | Limites de Hessiana e de PAC-Bayes em termos de κ*_info **falsos**: o funcional vale 0 sempre que uma geodésica de Fisher atinge Σ*, logo não vê o ponto final. Na regressão linear com rótulos aleatórios, κ*=0, Tr H≈1 e gap 0,71 contra o limite 0,19. O "teorema" de Stiefel/tempo polinomial não tem prova. K-FAC não é O(D). | `audit/scripts/check_ch10.py`; `audit/ch10_claims.md` | Reescrever como proposta com limites explícitos | corrigido; ver F-39 (verificado) |
| F-37 | M | cap. 7 (abstract, título, pipeline, princípio de contato) | Verificação cega: pipeline com grau r−2 não dá $C^r$ (mínimo 2r−3); abstract generaliza o princípio de contato além do ponto de contato (um disco entre p e q eleva κ*); princípio de contato provado para $C^2$ e aplicado a $C^{1,1}$; título "up to Dimension 12" sem suporte; + 8 itens B. | `audit/verify/ch07_blind.md` | Corrigir em sessão distinta da autora da reescrita | **verificado** 2026-09-25 (camadas 1, 2 e 2-residual: `audit/verify/L2_residual_2026-09-25.md`) |
| F-38 | M | cap. 9 (Obs. 1.1, 1.3, 2.3(c), 3.3; §1.3–1.4; Alg. 4.1) | Verificação cega: "não age por conjugação" falso para ρ específica; hipóteses de π₁≅F_m insuficientes; ∫|κ|≥∫|θ'|−π é verdadeira (texto diz "não sabemos"); teardrop afirmado sem prova; CAD não decide homotopia em n≥5; grade não garante cota superior; + 7 itens B. | `audit/verify/ch09_blind.md` | Corrigir em sessão distinta | **verificado** 2026-09-26 (`L2_residual_2026-09-25.md`, Rodada 2); obs. B: citar Fricke–Vogt/Goldman para (trA, trB, trAB) |
| F-39 | M | cap. 10 (Def. 1.2, Conj. 3.1, §4, conclusão) | Verificação cega: sem limite de comprimento κ*_info=0 mesmo com obstáculo bloqueando geodésicas (conclusão falsa); Conj. 3.1 trivial/ não falsificável e Stiefel pode tornar Σ* inalcançável; §4 atribui ao cap. 7 resultado só provado sem obstáculo; + 8 itens B. Contraexemplo da Prop. 2.2 confirmado (gap ≥ 1/2 analiticamente). | `audit/verify/ch10_blind.md` | Corrigir em sessão distinta | **verificado** 2026-09-26 (`L2_residual_2026-09-25.md`, Rodada 2); obs. B: "at least about 48, 72, 96" e "loss at least ε" |
| F-40 | M | cap. 11 (Conj. cMERA, Conj. RT–MCF); cap. 12 Conj. 5.2 | Verificação cega: métrica cMERA escrita é de $H^d$, não AdS$_{d+1}$ ($c_2=L^2/z_0^2$); "todo corte converge a minimizador" falso (geodésicas não minimizantes estacionárias, dois intervalos); atribuições a corrigir (Miyaji et al. 2015; Immirzi; restrições de Faulkner et al. 2017); + 10 itens B. | `audit/verify/ch11_blind.md` | Corrigir em sessão distinta | **verificado** 2026-09-25 (caps. 11 e 12; `L2_residual_2026-09-25.md`) |
| F-41 | A | cap. 13 (Eq. 5, D₂(z), §tilt, abstract, tabela, Fig. 1); cap. 12 §10.1 | Verificação cega: atraso de dispersão com fator (1+z) em vez de (1+z)² (Δt corretos 6,4e-62/2,9e-61/1,2e-60 s; ℓ* ≈ 3e-7 m); running do tilt comparado com k comóvel atual (sem sentido físico; escala correta H_inf ⇒ α_t ≲ 1e-11); "símbolo ↔ ξ=1" falso (Lorentziano dá fantasma, sem dispersão; anisotrópico com ξ=1 tem d_s=2,5); Hořava z=2 dá d_s=2,5, não 2; faixa CMB da Fig. 1(b) errada. Conclusão de inobservabilidade se mantém. Reabre parte de F-03/F-10. | `audit/verify/ch13_blind.md`, `audit/verify/scripts/ch13_*.py` | Corrigir em sessão distinta; regenerar figura | **verificado** 2026-09-25 (camada 1 `ch13_blind.md`; correção `fixes_F41-F43.md`; camada 2 `L2_F41-F43.md`) |
| F-42 | A | cap. 12 (Conj. 5.2, §9.5 Fefferman–Graham, Obs. 6.2, Conj. 4.3, §8.1–8.2, §9.2) | Verificação cega: Conj. RT/MCF falsa como enunciada (geodésicas desconexas estacionárias, AdS₃, dois intervalos); "g_(2) = C₂/L²" falso (fronteira plana ⇒ g_(2)=0) e conteúdo conjectural apresentado como solução exata; cota κ≥−2 não vale com a métrica arbitrária do cap. 2 (κ=−372 com métrica euclidiana); Conj. 4.3 mal especificada (invariância trivial sob Ĥ de Thiemann); §8.1 sem γ₅ não há gap; Q_q sem derivação e dependente de esquema; atribuição a Sotiriou–Visser–Weinfurtner errada (CDT 2+1, 3→2); + 6 itens B. Confirmados: d_s=m/α, forma fechada de d_s(τ) (erro 2e-10), cotas ADM, Hessiano/A_{m−1}. | `audit/verify/ch12_blind.md` | Corrigir em sessão distinta (junto com a parte do cap. 12 de F-40 e F-41) | **verificado** 2026-09-25 (inclui prior art Sotiriou–Visser–Weinfurtner PRD 84 (2011) 104018 conferido no fonte arXiv; redução 4D numérica 1e-14) |
| F-43 | A | cap. 8 (Seç. 3.2, Conj. 4.16, Def. 2.3, Seç. 4.1, Def. 4.4–4.5, Seç. 4.9–4.10, Obs. 4.18/4.21, Conj. 6.1) | Verificação cega: tubo em torno de geodésica em Hⁿ tem ‖II‖ = c·coth(cd), não c·tanh(cd); Conj. 4.16 falsa para |W| grande (curvas temporais têm |dφ/dt| < 1/(3√3M): classes vazias); norma de operador mal definida no fibrado normal lorentziano; sinais trocados em K_ij e θ_l; Def. 4.4 trivial (Einstein–Rosen K≡0); Seç. 4.9 contradiz a tabela (Estabrook); invariância de regularidade incompatível com o cap. 7; Conj. 3.3 parece ter prova curta (comparação de EDO); cota P_eff não segue; + 12 itens B. Confirmados: Gauss–Codazzi, K_M=c+κ², U-turn 2/w, cotas ADM, Raychaudhuri, horizonte RN/PG, garganta MT, topologia, Estabrook. | `audit/verify/ch08_blind.md` | Corrigir em sessão distinta | **verificado** 2026-09-25 (camada 1 `ch08_blind.md`; correção `fixes_F41-F43.md`; camada 2 `L2_F41-F43.md`; Teorema 3.3 novo conferido) |
| F-44 | M | cap. 12 §7 | Encontrado pelo corretor do artigo de férmions: o texto escreve M_f = (v/√2) Y_circ mas aplica a forma circulante às raízes quadradas das massas; é preciso dizer qual (o artigo usa M = C²). Além disso, se ambos os setores de quarks são circulantes, a mesma matriz de Fourier diagonaliza os dois e a CKM é trivial (sem Cabibbo). | `Manuscritos_Avulsos/paper_standard_model_masses/CORRECTIONS_2026-09-25.md` | Corrigir em sessão distinta | **verificado** (camada 2) 2026-09-25; sem camada 1 cega específica do trecho |
| F-45 | A | cap. 3 (Thm 3.2, 2.1, 5.3–5.5, 5.9, 5.10, Rem 5.2, 7.3, Tab. 1–2, abstract) | Verificação cega: representação do multinomial contínuo como integral no toro **falsa para m≥3** (binom(2;½,½,1)=8/π≈2,5465 vs 76/(3π²)≈2,5668), logo I_m = m^x J_m falsa e I_m ~ m^x sem prova válida; provas de Thm 2.1 e 5.10 insuficientes; forma quadrática de longo comprimento de onda **não** é S_m-invariante (contradiz cap. 4 Conj. 3.3); leitura "Stokes discreto" da Estrela de Davi não se sustenta; teoremas sem prova (5.4, 5.5); tabela m=4 errada; atribuição Gould→Hoggatt–Hansell; abstract promete Chu–Vandermonde inexistente. | `audit/verify/ch03_blind.md` | Corrigir em sessão distinta | **verificado** 2026-09-26 (camada 2 `audit/verify/L2_F45-F50.md`; I_m ~ m^x provado e conferido) |
| F-46 | M | cap. 4 (Conj. 3.3, Rem 2.5(b), Thm 2.6, Def 2.1, Prop 2.3, Thm 3.1–3.2, 4.2) | Verificação cega: "ground states exist" falso (termo cinético limitado ⇒ energia a massa fixa ilimitada inferiormente para todo p>0); regularidade H⁴ com Navier falha num simplexo; limite (1/2mα)kᵀAk não vale sem Σk=0; iff u=0 (não constante); consistência dimensional de α; + itens B. Dispersão MI, MSD exato, Mittag-Leffler e conservações confirmados. | `audit/verify/ch04_blind.md` | Corrigir em sessão distinta | corrigido; camada 2 confirmou as provas; o item B residual (Navier/H⁴) foi corrigido em `fixes_final_integration_2026-09-26.md` — aguarda camada 2 curta |
| F-47 | A | cap. 1 (Thm 5.5, 5.4, 5.6, §6, abstract) | Verificação cega: Kac–Rice (Thm 5.5) **falso para d=2** (2n pontos críticos, pelo próprio Thm 4.5), expoente deve ser ½log(d−1) (ABČ), campo com entradas i.i.d. não é isotrópico (não é o modelo ABČ) e coeficiente da Hessiana condicional é −d f I, não −(d−1) f I; atenção/Sobolev "uniforme em N" enganoso (sup|f|=N); Thm 5.6(ii) espaço de probabilidade não especificado; convergência de grafons só por subsequência; + itens B (Grothendieck, super-level, coarea Fleming–Rishel/Federer, Qi 2005). | `audit/verify/ch01_blind.md` | Corrigir em sessão distinta | corrigido; camada 2 confirmou Kac–Rice; o item B residual (§6.4, Lim) foi corrigido em `fixes_final_integration_2026-09-26.md` — aguarda camada 2 curta |
| F-48 | A | cap. 2 (Thm 6.2(ii), Prop 4.2, Tab. 2, Thm 6.1, 3.3(iii)) | Verificação cega: cota explícita do erro de Dyson (Thm 6.2(ii)) **falsa** (A≡0, R_j=M: (1+M/k²)^k−1 > M/k; Grönwall com soma de Riemann e fator e^{M/k} omitido; taxa O(1/k) continua válida); Laplaciano de grafon "limitado e PSD" exige 0≤W∈L^∞ (contraexemplos W=−1 e W ilimitado); massa fora da diagonal do Toda não é monótona (147/200 casos aumentam); cMPS: métrica degenerada por gauge, Q omitido, McLachlan ≠ Dirac–Frenkel, rotular como esboço formal; + itens B (Takatsu não citado, script citado numa prova). | `audit/verify/ch02_blind.md` | Corrigir em sessão distinta | corrigido; camada 2 confirmou a cota de Dyson; título do cap. 1 unificado em `fixes_final_integration_2026-09-26.md` — aguarda camada 2 curta |
| F-49 | A | cap. 5 (Prop 5.1, Thm 4.2, Def 6.1, abstract/título, §7) | Verificação cega: fórmula de inversão da Prop 5.1 **falsa** mesmo formalmente (dados são restrições a planos pela origem, não transformadas de n-planos; razão reconstrução/h = 11,28; 10,01; −0,90; 14,73); conservação de massa do Thm 4.2 exige Γ+Δ₃(α)⊂Ω não declarado e é cálculo formal; "sharp Wasserstein distortion bounds" não provados; generalização a Gr(n,m) prometida no título/abstract não existe; ganho γ=1 do núcleo Beta é provável por partes e não foi escrito; + itens B. Confirmados: representação de Fourier, traço, extensão dual, contração baricêntrica, Siegel–Wishart. | `audit/verify/ch05_blind.md` | Corrigir em sessão distinta | **verificado** 2026-09-26 (camada 2 `L2_F45-F50.md`; nova fórmula de inversão e γ = 1 conferidos) |
| F-50 | M | cap. 6 (Conj 2.3, Rem 2.4, Def 2.1, Assumption 2.2, Thm 2.5, Rem 3.2) | Verificação cega: Conj 2.3 vazia como enunciada (satisfeita pelas aproximações de Kigami); linhas nodais da fórmula de reflexão erradas (zeros só nos inteiros negativos); dimensões ℝ^{m−1} vs ℝ^m; r_m=m+3 é fato provável (não "assumption"); citar Kigami–Lapidus 1993; referência a script interno no texto. Confirmados: Prop 3.1 (resto é −1/(180x²)), reflexão, Pascal mod 2, fator m+3. | `audit/verify/ch06_blind.md` | Corrigir em sessão distinta | corrigido; Problema 2.3 reformulado sobre K×K (não é trivialmente falso nem verdadeiro; checagem no log) em `fixes_final_integration_2026-09-26.md` — aguarda camada 2 curta |
| F-51 | B | cap. 12 (Kac–Rice exp(Nθ(k)), linha I_m = m^x J_m, "imported decimation constant"); master (títulos dos caps. divergem dos arquivos); bibliografias dos caps. 2, 11–13 (título do cap. 1 = título Zenodo de *Beyond the Spectrum*) | Consistência entre capítulos após F-45–F-50: cap. 12 deve usar θ = ½log(k−1), não sugerir representação oscilatória de J_m, e citar que r_m = m+3 agora é provado no cap. 6; títulos no master e título canônico do cap. 1 precisam ser unificados (decisão do autor). | `audit/verify/fixes_F45-F50.md` (itens abertos) | Onda 3 (integração) | corrigido 2026-09-26 (títulos unificados; cap. 12 atualizado; 30 referências cruzadas conferidas) — aguarda camada 2 curta |

### 3.1 Cap. 8: balanço dos enunciados sem prova (2026-09-24)

| Enunciado original | Veredito | Destino |
|---|---|---|
| Gauss–Codazzi–Ricci | clássico | Teorema com citação (O'Neill; Gourgoulhon) |
| Acoplamento seccional–extrínseco $K_M=c+\kappa^2$ | verdadeiro | **provado** (Gauss) |
| Corolário "amplificação hiperbólica" | Euclidiano verdadeiro; caso curvo em aberto | **Lema 2/w provado**; cotas superiores por círculos geodésicos; **Conjectura** para a otimalidade |
| Restrições ADM | clássico | Teorema citado + esboço; **novo corolário provado** (cotas pontuais) |
| Raychaudhuri/SEC | verdadeiro com hipóteses (geodésica, ω=0) | **Proposição provada** + Definição do problema restrito |
| Horizonte aparente $1/r_+$ (Kerr–Newman) | falso em geral (dependente da fatiação; Kerr não é redondo) | **Proposição provada** para RN/Schwarzschild em Painlevé–Gullstrand + remark |
| Israel | clássico | citado (Israel 1966; Mars–Senovilla 1993) |
| Corolário "C^{1,1} fundamenta Israel" | confunde dois objetos | rebaixado a Remark explicativo |
| Garganta $K=1/r_0$ | falso (garganta é superfície mínima) | **Proposição provada** (mínima + cota NEC via curvatura de Gauss intrínseca) |
| Aceleração própria = II | verdadeiro | **Proposição provada** + Definição |
| Slingshot (π₁ ≅ 𝔽ₘ, divergência em 3M, estimativa de κ*) | falso em 3D; divergência não sustentada | **Props. provadas** (topologia; restrições causais) + **Conjectura planar** + remarks |
| Bona–Massó "certified clearance" | não provado | marcado como conjectura |
| Lente/anel de sombra | heurístico, depende da normalização afim | Remark heurístico |
| Fator conforme | não é teorema | Remark; correção do fator 3 na cota GHY |

Verificação simbólica: `audit/scripts/check_ch08_gr.py`. Continuam em aberto no cap. 8: Conj. "Curvature Amplification and Relief" e Conj. "Planar Relativistic Slingshot".

---

## 4. Ondas de execução (DAG)

```
Onda 0 (serial, 1 sessão) ──► Onda 1 (≈20 trilhas paralelas) ──► Onda 2 (correções paralelas por capítulo)
                                                                        │
                                              Onda 4 (release) ◄── Onda 3 (integração, serial)
```

**Onda 0 — linha de base** (bloqueia o resto)
- T0.1 Rastrear no git as fontes `.tex`/`.py` do livro (hoje `??`) e criar a tag `book-v2.2-baseline`. Artefatos (`.aux/.log/.pdf/.bak`) vão para `.gitignore`.
- T0.2 Criar `audit/` (feito), `audit/archive/` e o modelo de ledger `audit/_claims_template.md`.
- T0.3 Decisões do autor: **D1** (opção A/B, §1.3) e **D2** (destino do Lean).

**Onda 1 — diagnóstico (tudo em paralelo, somente leitura nos fontes)**
- W3 × 13: ledgers `audit/ch01_claims.md` … `ch13_claims.md`.
- W1: `audit/lean_inventory.md` (classificar cada declaração: tautológica / trivial-real / substantiva).
- W2: `audit/python_audit.md` (circularidade, oráculos, controles negativos) para os 13 scripts.
- W4: `audit/physics_sanity.md` (análise dimensional e ordens de grandeza de toda fórmula com número).
- W5: `audit/prior_art.md` (para cada resultado "novo", o prior art mais próximo, com DOI verificado).
- W7: script de lint (`audit/scripts/lint_tex.py`: `---`, `**`, `TODO`, `??`, palavras em PT, rótulos duplicados) + relatório de warnings/overfull.

**Onda 2 — correções** (paralelizável por capítulo; cada correção fecha um `F-xx`)
- Regra dos quatro olhos: quem corrige não verifica. O status `verificado` exige uma checagem adversarial feita por agente/sessão diferente, com contexto limpo.
- W1 níveis 0–1 e W2 (reescrita dos testes) rodam em paralelo com W3.

**Onda 3 — integração (serial)**
- Consistência entre capítulos (notação, F-20), abstracts/prefácio (W6, F-09, F-21), build unificado (F-19), CLAUDE.md atualizado (F-23).

**Onda 4 — release**
- `CHANGELOG.md`, Zenodo v2.3 (nova versão do mesmo conceito DOI), pacote arXiv testado localmente (`arxiv_bundle/` compila sozinho com `pdflatex` + `bibtex`).

---

## 5. Critério de pronto para o arXiv (gates)

- [ ] G1 Nenhum achado **C** ou **A** com status diferente de `verificado`/`descartado`.
- [ ] G2 Todo `theorem` tem prova no texto, citação a resultado clássico, ou foi rebaixado a `conjecture`/`remark`.
- [ ] G3 O abstract e a introdução de cada capítulo só afirmam o que os teoremas do capítulo provam (checagem W6 linha a linha).
- [ ] G4 Toda alegação sobre Lean corresponde a uma entrada de nível ≥1 em `audit/lean_inventory.md`, e `lake build` passa sem `sorry` e sem `axiom` (`#print axioms` em cada teorema citado).
- [ ] G5 `pytest` passa, e cada teste tem oráculo independente e controle negativo que falha sob mutação.
- [ ] G6 Todo número físico tem análise dimensional e ordem de grandeza registrada em `physics_sanity.md`.
- [ ] G7 Build a partir de fonte: 0 erros, 0 warnings, 0 overfull (regra do CLAUDE.md); lint limpo; pacote arXiv compila isolado.
- [ ] G8 Bibliografia: todos os DOIs resolvem (HTTP 200) e o prior art de F-10/F-07/F-17 está citado.
- [ ] G9 Declaração de uso de IA e prefácio revisados pelo autor (F-21).

---

## 6. Paralelização prática

- **Unidade de paralelismo:** uma frente × um capítulo. Cada trilha escreve só em `audit/<seu-arquivo>` (Onda 1) ou só no seu `chapXX` (Onda 2), então não há conflito de merge.
- **Isolamento:** na Onda 2, cada trilha usa um git worktree próprio (`isolation: worktree`) e produz um commit por achado (`fix(ch12): F-05 …`).
- **Custo:** a Onda 1 é a que mais se beneficia de agentes em paralelo (leitura independente). A Onda 3 deve ser serial, feita por uma única sessão.
- **Coordenação com a outra sessão Claude (skills):** as skills citadas no §2 estão sendo atualizadas em paralelo. Antes de cada onda, confirmar com ela quais versões usar, em especial `lean4-vacuity-verifier`, `adversarial-proof-synthesizer` e `proof-checker`. Um ponto a levar a ela: essas skills precisam **reprovar** o padrão `structure … (h : x = true)` e testes com expected = computed, que passaram nas rodadas anteriores.

---

## 7. Sincronização com o que é público

- Antes de cada release, conferir o Zenodo (`zenodo.org/api/records?q=creators.name:"Silva-Filho"`) e o GitHub (`origin`).
- Estado em 2026-09-24: Zenodo tem *Geometry, Tensors, and Quantum Gravity* v2.2 (22888334), *Beyond the Spectrum* v2 (22866175), *Geometric Condensation…* v2.0 (22837872) e *Fermion Mass Hierarchy…* v2.0 (22837696).
- F-04/F-22 (fenomenologia de massas) provavelmente afetam também os registros 22837872/22837696. Verificar na Onda 1 (W4).

---

## 8. Protocolo de atualização deste arquivo

1. **Início de sessão:** ler §3 e §4, escolher os itens e marcá-los `em curso` com a data.
2. **Novo achado:** acrescentar uma linha no §3 com o próximo ID, severidade, local exato (`arquivo:linha`) e evidência **reproduzível** (script em `audit/scripts/` ou citação).
3. **Correção:** status `corrigido (hash)`. Só vira `verificado` depois da checagem independente.
4. **Fim de sessão:** registrar uma linha no Diário (§9).
5. Nunca apagar achados. Usar `descartado` com o motivo.

## 9. Diário

| Data | Sessão | O que mudou |
|---|---|---|
| 2026-09-24 | Claude (avaliação inicial) | Criado o WORKPLAN. Achados F-01…F-24. Script `audit/scripts/check_ch12_formulas.py`. Os 13 verificadores Python rodados (todos "passam", o que não significa correção, ver F-02). |
| 2026-09-24 | Claude (correções urgentes) | Baseline copiada em `audit/baseline_v2.2/`. Cap. 12 reescrito (proposições vs conjecturas, J_CP retirado, §8.3 e §9 corrigidos, prior art citado). Cap. 13 reescrito como avaliação de ordens de grandeza, com figura gerada por `observability_estimates.py`. Cap. 8: todos os enunciados sem prova resolvidos (§3.1). Lint de Markdown em todos os caps. Caps. 8, 12, 13 compilam com 0 erros/0 warnings (resta F-26). Pendentes para fechar a v2.3: prefácio/Tabela 1 (F-21), Python caps. 12–13 (F-02), rebuild do master, CLAUDE.md (F-23), checagem independente. Lição: no Git Bash, heredocs colapsam `\\`, então usar scripts em arquivo. |
| 2026-09-24 | Claude (fechamento v2.3) | Prefácio e Tabela 1 do master reescritos (sem alegações falsas sobre Lean). Seção Declarations no master e `declarations_chapter.tex` em todos os caps. (F-21, F-29). Dicionário corrigido (F-31). Auditoria de 171 referências: 10 correções (F-28). Testes dos caps. 12–13 reescritos com oráculos independentes e controles negativos; pegaram o sinal invertido do fluxo de graphons (F-27) e um bound mal arredondado. Auditorias antigas arquivadas; CLAUDE.md e README resetados (F-23). Todos os caps. + master compilam com 0 erros (master: 0 warnings, 0 overfull). `CHANGELOG.md` criado. |
| 2026-09-24 | Claude (Onda 1–2, caps. 1–6) | Ledgers `audit/ch01…ch06_claims.md` (W3). Principais erros corrigidos: cap. 2 (Toda = QR sobre $e^{A_0}$; fator 2 em Bures–Wasserstein; prova da contração da norma de corte refeita; neckpinch rebaixado); cap. 3 (assintótica de $\mathcal J$ falsa; "defeito de fronteira" vazio; símbolo fechado, semigrupo e limite "Cartan" falsos, retirados); cap. 4 (Laplaciano espectral ≠ integral; Navier ≠ clamped; coeficiente do MSD); cap. 5 (dimensão do núcleo, ganho de traço falso para α>1, sinal da extensão dual, inversão mal-posta); cap. 6 (faltava `\newtheorem{conjecture}` — não compilava; Weyl "∼" → cotas; resto de $\mathcal E(x)$ refinado; Pascal mod 2 com prova por IFS; intro/conclusão). Scripts `check_ch02/03/03_b/03_kernel/06/06_b.py`. Caps. 1–6 compilam 0/0/0. Próximo: caps. 7, 9, 10, 11 (F-07, F-15, F-17, F-32). |
| 2026-09-24 | Claude (Onda 1–2, caps. 6–11) | Cap. 6 concluído (não compilava: faltava `\newtheorem{conjecture}`). Caps. 7, 9, 10, 11 reescritos a partir de ledgers (`audit/ch07…ch11_claims.md`) e scripts com contraexemplos (`check_ch07/09/10/11.py`). Novos achados: F-33 (cap. 7), F-34 (cap. 8: regularidade não euclidiana e tabela), F-35 (cap. 9: corte de enrolamento e benchmark de 50,6% falsos), F-36 (cap. 10: limites de generalização falsos). Fechados F-07, F-15, F-17, F-26, F-30, F-32. Langer 1985 corrigido (caps. 7–9); DOI de Breuning conferido (final -7). Caps. 1–13 e Dicionário compilam com 0 erros/0 warnings/0 overfull. Pendentes: verificação independente (regra dos quatro olhos) de todos os "corrigido"; W1 Lean; W2 Python caps. 1–11; F-19 (build a partir de fonte); F-20; F-24; D1/D2. |
| 2026-09-24 | Claude (limpeza de histórico) | A pedido do autor, o texto dos capítulos deixou de narrar a própria revisão ("an earlier version…"): ~70 passagens reescritas em tom neutro por `audit/scripts/remove_version_history.py`, mantendo os contraexemplos como remarks matemáticos. O histórico fica em `CHANGELOG.md` (agora com caps. 1–11 listados) e nos ledgers `audit/chXX_claims.md`. Todos os caps., Dicionário e master (169 pp.) compilam 0/0/0. |
| 2026-09-24 | Claude (verificação, camada 1) | Protocolo `audit/verify/PROTOCOL.md`. Quatro verificadores cegos de contexto limpo (caps. 7, 9, 10, 11): nenhum erro A; provas das proposições confirmadas; problemas M em conjecturas, abstracts e hipóteses → F-37…F-40 (consolidação em `audit/verify/SUMMARY.md`). Nenhum status passou a "verificado" (falta camada 2). As correções de F-37…F-40 devem ser feitas por outra sessão. |
| 2026-09-24 | Claude (verificação, rodada 2) | Camada 1 dos caps. 8, 12, 13 (novos F-41 A, F-42 A, F-43 A; os erros A concentram-se nos caps. corrigidos na primeira sessão: redshift (1+z)² e escala do running em ch13; RT/MCF e Fefferman–Graham em ch12; tanh→coth e classes vazias em ch8). Corretor independente fechou F-37…F-40 nos caps. 7, 9, 10, 11 (61 itens, 0 contestados; log `audit/verify/fixes_F37-F40.md`); compilação 0/0/0 conferida pelo consolidador. Próximo: corretor independente para caps. 8, 12, 13; camada 2 para F-37…F-40. |
| 2026-09-25 | Claude (verificação, camada 2 caps. 8/12/13; artigos) | Camada 2: F-41 e F-43 **verificados** (primeiros achados a fechar o ciclo completo); F-03, F-13, F-14, F-16 verificados por tabela; F-42 com 1 B + 1 INCERTO. Três artigos avulsos (SQG, Yang–Mills, férmions) corrigidos contra o livro por corretores independentes, notas `CORRECTIONS_2026-09-25.md` em cada pasta; nenhuma afirmação de gap de massa sobrevive. Novo F-44 (cap. 12 §7, circulante vs raízes de massa; CKM trivial). Build seguro `../build_pdfs_safe.py` a cada 20 min. Pendentes: mini-corretor caps. 7/9/10/11 + cap. 12 (F-42 B, F-44) e observações N1–N3; camada 1 dos caps. 1–6; segunda verificação dos artigos; paper do lagrangiano em Pesquisa_e_Testes. |
| 2026-09-26 | Claude (camada 2 caps. 1–6; integração final) | Camada 2 dos caps. 1–6: F-45 e F-49 **verificados**; resíduos de F-46/47/48/50 corrigidos junto com a integração final (F-51: títulos unificados, cap. 1 com título próprio, 24 entradas silvafilho2026* padronizadas, cap. 12 atualizado; F-20: forma única de d_s e α_t). F-38, F-39 verificados (rodada 2). Script de status reescrito (recusa chaves duplicadas; havia status antigos sobrescrevendo novos). Documento "Árvore de Conjecturas" criado para o autor. Build 0/0/0 em tudo. Pendentes: camada 2 curta da integração; Lean (F-01, F-24); Python caps. 1–11 (F-02); build a partir de fonte (F-19); declaração de IA (F-21, F-29). |
