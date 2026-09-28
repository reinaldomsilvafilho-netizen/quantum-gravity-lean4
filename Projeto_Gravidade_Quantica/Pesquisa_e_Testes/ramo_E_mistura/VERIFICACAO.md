# Verificação independente: `ramo_E_mistura/` (camada 1, quatro olhos)

Data: 2026-09-28. Verificador: Claude (Opus), sem participação na redação. Não editei o README, os
scripts do rascunho, o artigo nem o WORKPLAN.

## Como verifiquei

- **Scripts próprios** em `verify/`:
  - `v1_b3_exact.py`, 9/9:
    - classificação **exata** (sympy) das 48 permutações com sinal, sem amostragem aleatória;
    - prova analítica do zero;
    - conferência numérica com M_ν invariante aleatória.
  - `v2_tm1_sumrules.py`, 6/6:
    - construção diferente, U = U_TBM·R₂₃(θ,φ);
    - extração na convenção PDG, com cos δ vindo de |U_μ1|² e sen δ vindo de J, e checagem cos² + sen² = 1;
    - controle negativo: matrizes TM2 violam as regras de TM1.
  - `v3_koide_nu.py`, 16/16:
    - parametrização direta √m_k = A(1 + √2 cos(δ + 2πk/3)), com Q = 2/3 por construção;
    - fase fixada pela razão Δm²₂₁/Δm²₃₁ e escala por Δm²₃₁;
    - m_ββ pela regra do triângulo em forma fechada, sem varredura de fases.
  - `v4_resolve_refs.py`: DOIs via Crossref; o controle negativo (DOI mutado) não resolve. A API do arXiv
    respondeu 406 a partir desta máquina, então os IDs do arXiv foram conferidos nas páginas `abs`, via WebFetch.
- **Scripts do rascunho reexecutados** (`verify/rerun_*.out.txt`): as saídas são idênticas às gravadas;
  `signed_scan` difere só por avisos `RuntimeWarning` do numpy.
- **Fontes lidas:**
  - NuFIT 6.0: Tabela 1 (HTML do arXiv 2410.05380);
  - resumo do JUNO (arXiv:2511.14593);
  - resumo do DESI DR2 (arXiv:2503.14738);
  - PDF de Albright–Rodejohann (0812.0436): eq. (25) e tabela 1;
  - PDF de King–Luhn (1107.5332);
  - PDF de Varzielas–Lavoura (1212.3247): eqs. (23)–(32);
  - Brannen: resumo APS NW 2006 e preprint.

## Derivação analítica da afirmação 1

Seja G uma involução real simétrica. Então Gᵀ M G = M ⇔ [M, G] = 0, logo [M†M, G] = 0. Um autovetor v **não
degenerado** de G é, portanto, autovetor de M†M e é uma coluna de U_ν. Os léptons carregados são circulantes,
diagonalizados por U_ω (DFT), então a coluna PMNS é U_ω†v, com as linhas permutadas conforme a atribuição e, μ, τ.

Para a transposição (23), o autovetor não degenerado é v = (0,1,−1)/√2 (autovalor −1). Sua entrada k = 0 é
(1 − 1)/√6 = 0, qualquer que seja a atribuição das linhas. Para (12) e (13) vale o mesmo por conjugação. Logo há
sempre um zero, e a PMNS medida não tem entrada nula (a menor é |U_e3| ≈ 0,148). ∎

## Tabela de veredictos

| # | Afirmação | Veredicto | Evidência |
|---|---|---|---|
| B1 | Com léptons carregados circulantes, qualquer transposição de vértices como Z₂ residual dos neutrinos força um zero na PMNS, e fica excluída | CONFIRMA | Derivação acima; `v1`: (1/2, 1/2, 0) exato para as 6 transposições (±P). Hipótese implícita: o Z₂ residual está em S₃ e M_ν†M_ν tem espectro não degenerado. |
| B2 | As involuções de B₃ fixam exatamente três colunas (TM2, coluna com zero, TM1), 6 geradores cada | CONFIRMA | `v1`: 18 involuções não triviais (19 contando −1), em 3 classes de 6. Só sinais → (1/3,1/3,1/3). ±P → (1/2,1/2,0). Transposição com sinal oposto no par trocado → (2/3,1/6,1/6). A classificação é completa. Nota: o README diz "sign flip at two vertices", mas o flip em **um** vértice dá a mesma coluna (difere por −1). |
| B3 | B₃ ≅ S₄ × Z₂ | CONFIRMA | É o grupo octaédrico completo O_h; as permutações com sinal e det = +1 formam S₄. |
| B4 | TM1: sin²θ₁₂ = 1 − 2/(3cos²θ₁₃) = 0,318, +0,9σ do NuFIT 6.0 | CONFIRMA | `v2`: erro < 4×10⁻¹⁶ em 2000 matrizes TM1; 0,3184, a +0,95σ. |
| B5 | TM1: cos δ = −cot2θ₂₃(1 − 5s₁₃²)/(2√2 s₁₃√(1 − 3s₁₃²)); δ ≈ 74°/286° (s²₂₃ = 0,561) e 98°/262° (s²₂₃ = 0,47) | CONFIRMA | `v2`: erro < 1,3×10⁻¹⁴ na **convenção PDG** (U_μ1 = −s₁₂c₂₃ − c₁₂s₂₃s₁₃e^{iδ}). Derivação manual: igualar \|U_μ1\|² = \|U_τ1\|² = 1/6 dá cos δ = −cot2θ₂₃(s₁₂² − c₁₂²s₁₃²)/(2s₁₂c₁₂s₁₃), e substituir TM1 dá a fórmula. Sobre o sinal: cos δ é invariante sob δ → −δ (U ↔ U*), por isso a ambiguidade de convenção só troca δ por 360° − δ, e o rascunho já lista os dois valores. Valores: 74,3°/285,7° e 97,6°/262,4°. |
| B6 | TM2 desfavorecido, sin²θ₁₂ = 0,341, a +2,8σ | CONFIRMA | 0,3408, a +2,82σ. Com o JUNO 2025, +3,63σ: o veredicto fica mais forte. |
| B7 | Melhores χ²: 17,8 (TM2), 692 (coluna com zero), 1,34 (TM1); controle (1,0,0): 1657 | CONFIRMA | Reexecução idêntica. As colunas fixas coincidem com a classificação exata de `v1`. |
| B8 | Koide ν com Q = 2/3 em NO: exige raiz negativa; m = (0,36; 8,66; 50,13) meV; Σ = 59,2 meV; m_β = 8,9 meV; m_ββ ∈ [1,4; 4,0] meV | CONFIRMA | `v3`, por outro método: m = (0,364; 8,662; 50,131) meV, Σ = 59,16, m_β = 8,87, m_ββ ∈ [1,35; 4,04], com uma raiz negativa. Com todas as raízes positivas, sup Q = 0,585 < 2/3 (controle). |
| B9 | IO: Σ = 102 meV | CONFIRMA | 102,0 meV com Δm²₃₂ = −2,484×10⁻³ (IC24+SK); 102,6 com −2,510×10⁻³ (IC19). |
| B9b | "H1 plus cosmology predicts normal ordering" | INCERTO | É verdade, mas não discrimina H1: **qualquer** IO tem Σ ≥ 98,9 meV > 64 meV. O DESI sozinho já desfavorece IO. Deve ser dito como consistência, não como predição. |
| B10 | H2 (δ_ν = δ_l): Δm²₂₁/Δm²₃₁ = 0,0035 contra 0,0298 (fator 8,4), excluído. Com δ_l + π/12: 0,0308, a +1,3σ | CONFIRMA | `v3`: 0,00354 e 0,03084 (+1,31σ). O dado é 7,49/251,3 = 0,02981. |
| B11 | δ_l = 2/9 com 5 dígitos | CONFIRMA | Com b livre (ajuste em forma fechada): 0,222225, com \|Δ\| = 3×10⁻⁶. Com b/a forçado a 1/√2 sai 0,222239, só 4 dígitos, porque Q_l = 0,666664 ≠ 2/3. |
| B12 | δ_ν(H1) = 0,479 contra δ_l + π/12 = 0,484 | CONFIRMA | 0,4793 (ou 2π/3 − 0,4793, com o mesmo espectro). |
| B13 | Dados "NuFIT 6.0 (2024), NO" usados como um único conjunto | **REFUTA** | Pela Tabela 1 do NuFIT 6.0, s²₁₂ = 0,307, s²₁₃ = 0,02195 e s²₂₃ = 0,561 vêm da análise **IC19 sem SK-atm**, enquanto Δm²₃₁ = 2,513×10⁻³ (NO) e Δm²₃₂ = −2,484×10⁻³ (IO) vêm da **IC24 com SK-atm**. Na IC24+SK: s²₁₃ = 0,02215 e s²₂₃ = 0,470 (octante inferior), e o octante muda a predição de δ. Na IC19: Δm²₃₁ = 2,534×10⁻³ e IO −2,510×10⁻³. O impacto numérico é pequeno (Σ_NO 59,2 → 59,4 meV; TM1 0,3184 → 0,3182), mas os dados precisam vir de uma única análise, citada explicitamente. |
| B13b | Referência NuFIT 6.0 | CONFIRMA | Esteban et al., JHEP 12 (2024) 216, DOI 10.1007/JHEP12(2024)216 (resolve), arXiv:2410.05380. |
| B14 | PDG 2024: m_e = 0,51099895, m_μ = 105,6583755, m_τ = 1776,93 MeV | CONFIRMA | São os valores do PDG 2024 (m_τ = 1776,93 ± 0,09 MeV). Não os rebusquei online; nível "conhecimento". |
| B15 | JUNO, primeiro resultado (pedido) | CONFIRMA (achado) | JUNO Collab., "First measurement of reactor neutrino oscillations at JUNO", arXiv:2511.14593 (18/11/2025), com 59,1 dias: sin²θ₁₂ = 0,3092 ± 0,0087 e Δm²₂₁ = (7,50 ± 0,12)×10⁻⁵ eV² (NO). TM1 fica a +1,05σ e TM2 a +3,63σ. A página `abs` não mostra referência de periódico; confirmar se já saiu publicado antes de citar. |
| B16 | DESI DR2: Σm_ν ≲ 64 meV ("value to be checked") | CONFIRMA | DESI Collab., "DESI DR2 Results II", Phys. Rev. D 112, 083515 (2025), DOI 10.1103/tr6y-kpc6, arXiv:2503.14738: Σm_ν < 0,0642 eV (95%, ΛCDM, DESI BAO + CMB); em w₀w_aCDM, < 0,16 eV. Artigo dedicado: arXiv:2503.14744. H1-NO, com 59,2 meV, fica abaixo do limite, mas a 0,4 meV do mínimo de NO (58,8). |
| B17 | Albright–Rodejohann 2009: TM1/TM2 e regras de soma | CONFIRMA | EPJC 62, 599 (2009), DOI 10.1140/epjc/s10052-009-1074-3 (resolve). O PDF define TM1, TM2 e TM3 (eq. 25; U_TM1 = U_TBM R₂₃) e dá sin²θ₁₂ e a relação s²₂₃–\|U_e3\|–cos δ (tabela 1). |
| B17b | `tm1_delta.py`: a fórmula exata de cos δ é "King & Luhn / Albright–Rodejohann form" | INCERTO | AR 2009 dão a relação θ₂₃–δ só na forma expandida em \|U_e3\|. Não encontrei a forma fechada exata nem em AR 2009 nem em King–Luhn 2011. Ela é correta (B5), mas a atribuição precisa ser conferida, por exemplo em King–Luhn, Rep. Prog. Phys. 2013, ou em Ballett–King–Luhn–Pascoli–Schmidt 2014. |
| B18 | "King and Luhn (2012–2013)" | INCERTO | As datas não batem. King–Luhn, JHEP 09 (2011) 042 (DOI resolve), trata de mistura **TM2** (segunda coluna 1/√3) em A₄/S₄. A revisão é Rep. Prog. Phys. 76 (2013) 056201, DOI 10.1088/0034-4885/76/5/056201 (resolve). Corrigir para "2011; 2013" e não usar o artigo de 2011 como fonte de TM1. |
| B19 | Varzielas–Lavoura 2012: TM1 a partir de S₄ com Z₂ residual | CONFIRMA | J. Phys. G 40 (2013) 085002, DOI 10.1088/0954-3899/40/8/085002 (resolve), arXiv:1212.3247 (dez. 2012). O resumo diz "first column (2,−1,−1)/√6 … the flavour symmetry group adequate for this purpose is S4". **Achado relevante:** no texto, eqs. (23)–(32), eles já usam a matriz **circulante** dos léptons carregados (Z₃ gerado por G₃) e um Z₂ gerado por F₃ na representação 3₁ na mesma base de permutações. É exatamente o arranjo do rascunho. A "leitura geométrica" (B₃ = triângulo com vértices orientados) é, portanto, só uma renomeação dessa base; a parte candidata a nova é ainda menor do que o README sugere. |
| B20 | Brannen 2006: Koide ν com raiz negativa e deslocamento π/12 | CONFIRMA | C. A. Brannen, "Koide's Mass Formula for Neutrinos", APS Northwest Section Meeting 2006 (ADS 2006APS..NWS.B3014B), e o preprint "The Lepton Masses" (brannenworks.com/MASSES2.pdf). Ambos têm −√m_ν1 e δ_ν = δ_l + π/12 (com δ_l = 0,22222204717). Não há DOI nem revisão por pares: citar como resumo de conferência ou preprint. |
| B21 | "O S₃ do triângulo sozinho está excluído" | CONFIRMA | Segue de B1, sob as hipóteses declaradas: léptons carregados circulantes e Z₂ residual dos neutrinos contido em S₃. |
| B22 | TM1: 2 parâmetros livres para 4 observáveis, logo 2 predições (θ₁₂ e δ) | CONFIRMA | Uma coluna fixa deixa um ângulo e uma fase livres. |

## Contagem

CONFIRMA 21 · REFUTA 1 (B13) · INCERTO 3 (B9b, B17b, B18).

A única refutação é de proveniência dos dados: parâmetros de duas análises NuFIT 6.0 misturados. O efeito
numérico é < 0,5%, mas o octante de θ₂₃ muda a predição de δ. Todas as afirmações matemáticas (B1, B2, B4, B5)
estão confirmadas analiticamente.
