# Verificação cega (camada 1): completamento lorentziano

**Verificador independente, 2026-09-28.** Não escrevi o README nem os scripts `e1`–`e3`. Não editei README, refs,
scripts do autor, capítulos, artigos nem WORKPLAN. Meus scripts estão em `verify/`.

## Resumo

- **Contagem: 31 CONFIRMA, 2 REFUTA, 4 INCERTO (37 itens).**
- **REFUTA:**
  - **R1.** "Lee–Wick excluído: um par complexo força d_s ≤ 4/3". A Prop. LW está correta, mas só na classe
    polinomial. O Lee–Wick padrão (LW 1970; GOW 2008; Donoghue–Menezes) tem **exatamente** o símbolo do livro no nível
    árvore (polo real de resíduo −1), e o par complexo vem da largura. Fora da classe polinomial, u(u²+u+1)/(u+2)
    tem par complexo e d_s = 2 (`v3`, L2).
  - **R2.** "Pais–Uhlenbeck com ω₁ = 0 (graviton sem massa) não conferido". A premissa está errada. Cada modo de
    k²(1+ℓ²k²) é um oscilador PU com ω₁ = |p| e ω₂ = √(p²+ℓ⁻²). Então ω₁ = 0 só vale em p = 0, e ω₂ > ω₁ sempre. O
    caso relevante é o regime de frequências distintas de Bender–Mannheim, não o de ω₁ = 0.
- **Números corrigidos:**
  - janela fakeon: 4/3 < N²r < 12, com r = 24m_χ²/[N²(m_φ²+2m_χ²)] (ABP 2020, eq. 7.3, lida no texto arXiv);
  - N = 60: 3,70×10⁻⁴ < r < 3,33×10⁻³; N = 55: [4,4×10⁻⁴; 4,0×10⁻³]; N = 77: [2,2×10⁻⁴; 2,0×10⁻³];
  - escala única m_χ = m_φ: r = 8/N² = 2,22×10⁻³ (N = 60);
  - ℓ = ħc/m_φ = 6,9–7,2×10⁻³⁰ m ≈ 4,3–4,5×10⁵ ℓ_P, para m_φ = 2,73–2,86×10¹³ GeV (N = 60). Com N = 55,
    ℓ = 6,3×10⁻³⁰ m;
  - limite superior ℓ < 4ħc/m_φ = 2,8–2,9×10⁻²⁹ m.

## Scripts

| Script | Resultado | Oráculo | Controle negativo |
|---|---|---|---|
| rerun `e1`, `e2`, `e3` | 6/6, 11/11, 10/10 (= 27/27, reproduzido) | — | — |
| rerun `resolve_dois.py` | 78/78, mais 2 NEG-PASS | — | — |
| `verify/v1_kl_pointwise.py` | 5/5 | quad em x = ln z (scipy); fórmula de momentos contra diferença finita | símbolo do livro; resíduo invertido |
| `verify/v2_inflation_scale.py` | 8/8 | slow-roll numérico de Starobinsky com M_red (CODATA 2018) contra a forma fechada ABP com M_Pl | M_red na forma fechada (erro de √(8π)); x = 1/2 |
| `verify/v3_symbols.py` | 8/8 | erfc fechado contra momentos; Ein via `special.exp1` | erfc sem e^{x²}; polinômio com par complexo; ramo sem massa |

Observação sobre os controles do autor:
- `e3` NC3 (S = u·u) é trivial;
- `e3` NC2 isenta justamente η = −2.

Os meus controles substituem esses dois.

## Tabela

| # | Afirmação | Veredito | Evidência |
|---|---|---|---|
| 1 | Lema KL: com G = w₀/z + ∫ρ/(z+μ²) e ρ ≥ 0, vale d_s(UV) ≥ 4 | **CONFIRMA** (e vale mais forte) | A prova do README dá liminf da razão de logs ≥ 4, o que está correto. Prova independente: zG não decrescente ⇒ S/z não crescente ⇒ q = h²/2 = s²m(s) com m crescente; pela desigualdade de Chebyshev sob a densidade Gama(3), **d_s(τ) ≥ 4 para todo τ**, pontualmente, e não só no UV. Numérico: `v1` K1–K3 (mínimo 4,000000 em 40 medidas × 25 τ, inclusive o caso com gap). **Hipóteses precisas:** d_s é o do traço do núcleo de calor do símbolo euclidiano S = 1/G; G é de Stieltjes (campo escalar, ou componente com métrica positiva); P(τ) < ∞. Propagadores dependentes de gauge em gauges de métrica indefinida não são cobertos. "Lorentz" só entra para garantir a forma KL. |
| 2 | Símbolo do livro: ρ = δ(μ²) − δ(μ²−ℓ⁻²); escapa só pelo peso −1 | CONFIRMA | 1/(z(1+z)) = 1/z − 1/(z+1); `v1` NC1 dá d_s mínimo 2,0009. |
| 3 | Campo livre: positividade OS ⇔ ρ ≥ 0 | CONFIRMA | Resultado clássico (Glimm–Jaffe; OS 1973). Não relido no texto. |
| 4 | Tabela de rotas de escape (§1) | CONFIRMA, com ressalva | Correta. O LW com ghost real no nível árvore cai na mesma linha do fakeon (ver R1). |
| 5 | Prop. LW (matemática): d_s = 4/n; n = 2 ⇒ segunda raiz real com resíduo −1/α; par complexo e polo sem massa ⇒ n ≥ 3 ⇒ d_s ≤ 4/3 | CONFIRMA | Prova elementar correta; `v3` L1 dá 2,0000 e 1,3335. |
| 6 | "Lee–Wick incompatível com d_s = 2; excluído/rebaixado" (§0.5, §2.2, tabela) | **REFUTA** | Ver R1. O Lee–Wick canônico tem o símbolo k²(1+k²/M²) no nível árvore. A ressalva da §2.2 ("a menos que o par venha da largura") descreve o caso **padrão**, não uma exceção. A exclusão só vale para um par complexo *no símbolo polinomial*. `v3` L2 dá um contraexemplo racional. |
| 7 | O fakeon mantém o símbolo exato, e com ele P(τ), a forma erfc e d_s | CONFIRMA (trivial) | A teoria é definida pela rotação de Wick não analítica da teoria euclidiana (Anselmi–Piva 2017, resumo), e d_s é calculado no símbolo euclidiano. Ressalva: d_s é propriedade do objeto euclidiano, não um observável lorentziano da teoria com fakeon. |
| 8 | Unitariedade: perturbativa, em todas as ordens, provada pelos proponentes | CONFIRMA | Anselmi 2018 (arXiv:1801.00915), resumo: "perturbatively unitary to all orders". Não há prova não perturbativa. |
| 9 | "Escrutínio independente limitado; não conferi crítica direta ao fakeon" | INCERTO (a completar) | Há escrutínio independente: Buoninfante, JHEP 02 (2025) 186, §2.1: "It is still unclear whether anti-Feynman and fakeon ghosts can be consistently described within the operator formalism". Kubo–Kugo 2023 (PTEP 123B02) tratam do ghost complexo e não citam o fakeon no resumo. Há literatura que estende a objeção das sutilezas com deltas às regras de Feynman usuais (não conferi no texto). Donoghue–Menezes 2019 propõem uma alternativa (modos "Merlin"). Nenhuma refutação publicada foi encontrada. |
| 10 | Renormalizabilidade de R+R²+C² com fakeon | CONFIRMA | Stelle 1977 (contagem de potências). Anselmi 2018, resumo: "If standard power counting constraints are fulfilled, the models are also renormalizable". ABP 2020, §2: "manifestly renormalizable". |
| 11 | ABP 2020: r = 24m_χ²/[N²(m_φ²+2m_χ²)], m_χ > m_φ/4, 4/3 < N²r < 12, 0,4 ≲ 1000r ≲ 3 (N = 60), r ≃ −8n_T, A_R e n_R iguais aos de Starobinsky | CONFIRMA | Lido no texto arXiv 2005.10293, §7, eqs. 7.3–7.5 e fig. 1; `v2` I2. |
| 12 | Starobinsky como limite m_χ → ∞: N²r = 12 | CONFIRMA | `v2` I2. |
| 13 | Escala única m_χ = m_φ ⇒ r = 8/N² = 2,22×10⁻³ (N = 60), 2,64×10⁻³ (N = 55), 1,35×10⁻³ (N = 77) | CONFIRMA (aritmética); identificação [heurística] | `v2`. Usar m_χ = m_φ para "a mesma ℓ nos setores de spin 0 e spin 2" é hipótese de modelagem. |
| 14 | ℓ ≈ 7,2×10⁻³⁰ m ≈ 4,5×10⁵ ℓ_P | CONFIRMA | CODATA 2018: ħc = 1,97327×10⁻¹⁶ GeV·m. m_φ = √(3πA_s)·M_Pl/N, com A_s = e^{3,044}×10⁻¹⁰. Forma fechada: 2,86×10¹³ GeV, logo ℓ = 6,9×10⁻³⁰ m. Slow-roll: 2,73×10¹³ GeV, logo ℓ = 7,2×10⁻³⁰ m. Dimensão: [GeV·m]/[GeV] = m. Ordem de grandeza: m_φ ~ 10⁻⁵ M_Pl ⇒ ℓ ~ 10⁵ ℓ_P, consistente. |
| 15 | ℓ < 2,9×10⁻²⁹ m ≈ 1,8×10⁶ ℓ_P; m_χ,min = 6,8×10¹² GeV | CONFIRMA | `v2`: 2,76–2,89×10⁻²⁹ m, conforme o m_φ usado. |
| 16 | ℓ = ℓ_P ⇒ desvio relativo de r de 2,5×10⁻¹² | CONFIRMA | m_φ²/(2M_Pl²) = 2,5×10⁻¹². |
| 17 | "r = 8/N² está ao alcance do LiteBIRD (δr < 10⁻³)"; "detecta a borda superior" | INCERTO (exagerado) | Com σ_r = 10⁻³: r = 2,22×10⁻³ fica em 2,2σ (1,35σ para N = 77), e a borda superior em 3,3σ. Isso é indício, não detecção. Pior: 8/N² e o 12/N² de Starobinsky diferem por 1,1σ em N = 60, e a incerteza em N (55–77) é degenerada com m_χ/m_φ. O LiteBIRD não distingue a previsão de escala única da inflação de Starobinsky pura (`v2` I4, I5). |
| 18 | ACT DR6: n_s = 0,974 ± 0,003 ⇒ N ≈ 77 (69–87); N = 60 a 2,4σ | CONFIRMA (aritmética) | `v2` I6. O valor de n_s vem do resumo e não foi relido. |
| 19 | r < 0,036 (BK 2021) e r < 0,032 (Tristram 2022) | CONFIRMA | Valores publicados, padrão. |
| 20 | CMB-S4 descontinuado por DOE/NSF em 9 jul. 2025 | INCERTO | Não conferi. |
| 21 | Fator de forma inteiro S_T: inteiro, sem zeros além de 0, S_T → k² (IR) e → ℓ²k⁴ (UV), d_s 4 → 2 | CONFIRMA | Ein(x) ~ γ + ln x ⇒ S_T → u². `v3` T1 dá UV 2,0000 e IR 4,0000. |
| 22 | Desvio máximo de d_s em relação ao erfc de 0,379 em τ = 10; d_s(1) = 2,57 contra 2,70 | CONFIRMA | `v3` T2: 0,3794 em τ = 10 (grade de 49 pontos). d_s(1): 2,5694 contra 2,7009. |
| 23 | Nenhuma função inteira sem zeros iguala k²+ℓ²k⁴ | CONFIRMA | S_B/u = 1+u tem zero em u = −1, e e^{H} não tem zeros. |
| 24 | \|1/S_T(5i)\| ~ 10²⁰⁹²⁷ ⇒ não é Stieltjes (não contradiz o Lema KL) | CONFIRMA | Rerun de `e3` T3. Ein(−y) cresce como e^{y}/y. |
| 25 | Unitariedade perturbativa não local (Pius–Sen; Briscese–Modesto 2019, "all perturbative orders"; BCMN 2024) | INCERTO | Só pelo resumo, como declarado; não relido (limite de sessão). |
| 26 | Conjuntos causais (ASS 2014): g ∝ p·p no IR, constante no UV; o d'Alembertiano 4D original é instável | CONFIRMA | Resumo de arXiv:1403.1622: "for large p it becomes constant"; "the original 4D causal set d'Alembertian is unstable, while its 2D counterpart is stable". |
| 27 | BBMM 2016: d_s → 2 em toda dimensão, dependente da regularização; g_reg ~ k^d (k⁴ em 4D), IR ~ −k²; máximo acima de d; o propagador de Feynman não é função de Green; argumento de Weinberg (§10.7); Aslanbeigi–Saravani com ρ ≥ 0 dá d_s começando em 4 | CONFIRMA | Texto (pdftotext). Detalhes: o máximo fica em s ~ 10ℓ para d = 3 e 4 (s ~ ℓ só em 2D); "evidence suggests" ρ não positiva para d > 2, o que o Lema KL torna um teorema, dada a forma de Stieltjes. Falta em `refs.md` a referência Saravani–Aslanbeigi 2015 (arXiv:1502.01655). |
| 28 | BBL 2015: contínuo de modos massivos; propagador de Wheeler para os modos instáveis; H não positivo em 4D | CONFIRMA | Resumo de arXiv:1411.6513: contínuo de modos massivos "in any dimension", "Wheeler propagator", "In 2 dimensions the Hamiltonian is positive definite". |
| 29 | Optomecânica: escalas de não localidade de 10⁻²²–10⁻²⁶ m (BBLMMO 2017) | CONFIRMA | Resumo de arXiv:1611.07959: "10^−22 ÷10^−26 m". O "÷" é a notação original de intervalo, não um separador corrompido. |
| 30 | Eichhorn–Mizera 2014: d_s crescente no UV | CONFIRMA | Corroborado pelo texto de BBMM §I. |
| 31 | SA: a família S = k²(1+ℓ²k²)^{−η/2} tem d_s(UV) = 2d/(2−η); η = −2 dá exatamente o símbolo | CONFIRMA | Rerun de `e3` A1. Reforço: com G(p) = G₀/(1+ωG₀p²) (melhoria RG padrão), p²/G(p) ∝ p² + ωG₀p⁴, que é exatamente o símbolo. |
| 32 | Lauscher–Reuter: η_N = −2 ⇒ propagador 1/p⁴ ⇒ d_s = 2 | CONFIRMA (padrão) | O resumo de hep-th/0508202 atribui o resultado "to the anomalous dimension of Newton's constant". O valor η = −2 é o conhecido do ponto fixo; não relido no texto. |
| 33 | Tensão entre SA e o Lema KL: com espectral positiva, o d_s = 2 de SA não vem desse propagador | CONFIRMA (como aberto) | Consequência direta do item 1: se o propagador do graviton dinâmico for de Stieltjes, d_s ≥ 4 pontualmente. |
| 34 | CDT: d_s curto ≈ 1,5–2 | CONFIRMA | AJL 2005 ("two-dimensional"; 1,80 ± 0,25 no texto, de memória do verificador). Coumbe–Jurkiewicz 2015, resumo: "approximately 3/2". |
| 35 | Pais–Uhlenbeck: "ω₁ = 0 (graviton sem massa) não conferido" | **REFUTA** (premissa) | Ver R2; `v3` PU1 e NC3. A objeção de Smilga no limite de frequências iguais não se aplica (ω₂² − ω₁² = ℓ⁻² > 0). A crítica "interação quebra a unitariedade" continua válida. |
| 36 | Stelle: operador TT de Einstein + C² = k²(1+k²/m₂²), ℓ = 1/m₂ | CONFIRMA | O propagador de spin 2 é 1/k² − 1/(k²+m₂²). |
| 37 | Scripts (27 checks) e DOIs (78/78) | CONFIRMA | Rerun idêntico. Controles do autor fracos em `e3` NC2/NC3, cobertos por `v1`–`v3`. |

## Recomendações para o autor (sem editar)

1. **Reclassificar o Lee–Wick.** No nível árvore ele coincide com o fakeon no símbolo. O que muda é a prescrição, e
   Kubo–Kugo contra LMC é o debate relevante. A Prop. LW deve dizer "símbolo polinomial com par complexo
   **explícito**".
2. **Ajustar a frase do LiteBIRD.** "Indício em ~2σ; não distingue de Starobinsky puro."
3. **Reformular o item PU.** A questão aberta é a QFT interagente, não ω₁ = 0.
4. **Lema KL.** Enunciar a versão pontual (d_s(τ) ≥ d para todo τ), com as hipóteses do item 1, e acrescentar
   Saravani–Aslanbeigi 2015 a `refs.md`.
5. **Escrutínio do fakeon (§7).** Citar Buoninfante 2025 (JHEP 02 (2025) 186) como escrutínio independente
   (formalismo de operadores em aberto).
