# Auditoria Matemática Rigorosa — CHAP10: Geometria da Informação, Variedades de Stiefel e Barren Plateaus

## Metodologia
Examinei o manuscrito completo (`chap10_information_geometry_minimax_deep_learning.tex`, 238 linhas) e o módulo Lean 4 correspondente (`InformationGeometry.lean`, 148 linhas), obligation por obligation, verificando: (i) descarga de hipóteses, (ii) aciclicidade lógica, (iii) regularidade dimensional/funcional, (iv) correspondência LaTeX↔Lean.

---

## ACHADO CRÍTICO TRANSVERSAL: Vacuidade Semântica no Kernel Lean

Todos os 8 teoremas em `InformationGeometry.lean` seguem um padrão estrutural idêntico e problemático: a conclusão do teorema é literalmente injetada como campo de hipótese na `structure`, e a "prova" consiste em `exact h.campo` — extraindo a hipótese assumida, não derivando-a de primeiros princípios.

Exemplos concretos:
- `terminal_hessian_trace_bound`: `h_bound : expected_trace ≤ dim_D * lambda_max_F * kappa_star` é um **campo assumido** da struct; o teorema apenas devolve `h.h_bound`. Isso não certifica que o *bound* do Hessian decorre da curvatura de Wasserstein — apenas que "se P, então P".
- `pac_bayesian_generalization_bound`, `barren_plateau_isometry_bypass`, `frenet_natural_gradient_scheduling`, `wasserstein_langevin_curvature`: mesmo padrão circular.
- Nenhuma estrutura usa `ℝ` (Real) — todas usam `Float` (ponto flutuante IEEE 754, sem os axiomas de completude/ordem que sustentam análise real), e nenhuma formaliza objetos geométricos reais (métrica de Fisher-Rao como forma bilinear positiva-definida, conexão de Levi-Civita, distância de Wasserstein, medida de Haar, variedade de Stiefel). Não há um único `Manifold`, `InnerProductSpace` ou `MeasureTheory` real sendo usado.

Isso viola diretamente a Regra 2 do protocolo (`CLAUDE.md`): **"Acyclicity in logical dependencies"**. Um teorema cuja hipótese é sintaticamente idêntica à tese não constitui verificação formal — é teatro de formalização. Nenhuma das obrigações matemáticas substantivas do capítulo (curvatura minimax, colapso de Wasserstein, concentração de medida de Lévy, equioscilação de Chebyshev) está de fato formalizada; apenas booleans/flags nomeados por analogia foram encadeados trivialmente.

---

## Avaliação por Obrigação

### OBL-C10-001 (Fisher-Rao + K-FAC)
A Definição 2.1 (linhas 95–101) é bem-posta sintaticamente, mas:
- Não há prova de existência/regularidade do minimizante $\gamma$ (compacidade, semicontinuidade de $\tilde g^{\Fisher}$, argumento de coercividade).
- A restrição sub-Riemanniana à distribuição horizontal (autovetores principais do FIM) **não verifica a condição de Chow–Rashevskii** (bracket-generating). Sem isso, a métrica Carnot-Carathéodory pode ser $+\infty$ entre $\theta_0$ e $\Sigma^*$, invalidando o problema minimax.
- A alegação "$\mathcal{O}(D^3) \to \mathcal{O}(D)$ via K-FAC" é apresentada como fato estabelecido, mas o próprio parágrafo admite que K-FAC é apenas um "geometric preconditioner ... rather than exact Riemannian tensor inversion" — há tensão interna não resolvida entre a alegação de complexidade linear *exata* e a admissão de que é aproximação sob hipótese de independência entre inputs de camada e gradientes de pré-ativação (hipótese nunca descarregada).

**Status: hipóteses não descarregadas (Regra 1).**

### OBL-C10-002/003 (Wasserstein-Langevin + Hessian trace + PAC-Bayes)
Teorema 2.2: a passagem de "SGD é SDE com variação quadrática infinita" para "portanto aplicar $\kappa^*_{info}$ à métrica $\W_2$" é uma afirmação de plausibilidade, não uma derivação. Faltam:
- Definição precisa de curvatura em $(\mathcal{P}_2(\Theta), \W_2)$ (cálculo de Otto), e prova de que $\rho(\theta,t)$ traça uma curva $C^{1,1}$ nesse espaço.
- Cadeia de prova ligando a curvatura macroscópica ao traço do Hessiano terminal (eq. 120) — a desigualdade é **postulada**, não derivada.
- O bound PAC-Bayesiano (eq. 124) assume perda sub-Gaussiana ou limitada em $[0,1]$ "para satisfazer Donsker-Varadhan" — hipótese nunca verificada contra a classe de perdas real (cross-entropy é ilimitada), violando a Regra 1 (descarga de hipóteses).

**Status: teoremas nomeados, mas não provados — apenas enunciados por analogia formal.**

### OBL-C10-004 (Barren Plateau via Dynamical Isometry / Stiefel)
Falha lógica substantiva no Teorema 3.1: o argumento é que restringir o caminho a $O(D)$ (Stiefel) "quebra" a concentração de medida de Haar sobre $U(2^n)$. Porém $O(D)$, como grupo de Lie compacto com métrica bi-invariante e curvatura de Ricci limitada inferiormente, **também exibe concentração de medida de Lévy (Gromov–Lévy)** para $D$ grande — a restrição por si só não implica $\lambda_{\min}(\tilde g^{\Fisher}) \ge c > 0$; isso precisaria ser demonstrado especificamente para a constante de Lipschitz da perda restrita a essa subvariedade, o que não é feito.
Além disso, a literatura de dynamical isometry (Pennington et al.) mostra que $J^TJ = I$ tipicamente **não se preserva** após passos de gradiente — o teorema exige manter a isometria ao longo de todo o caminho sem tratar essa deriva conhecida, criando tensão não resolvida entre "seguir estritamente $O(D)$" e "reduzir a perda".
Os limites de complexidade $T \ge \mathcal{O}(2^n)$ e $T \le \mathcal{O}(n^2/\kappa^{*2})$ são afirmados sem derivação (nenhuma desigualdade tipo Polyak-Łojasiewicz ou argumento de taxa de convergência é fornecido).

**Status: mecanismo causal reivindicado não é logicamente sustentado; non sequitur identificado.**

### OBL-C10-005 (Frenet-Serret + Equioscilação de Chebyshev)
O sistema de Frenet-Serret (eq. 154–156) está corretamente formulado como ODE padrão em referencial móvel Riemanniano. Mas a condição $\kappa(s) \equiv \kappa^*_{info}$ é **imposta por definição**, não derivada como condição de otimalidade do problema minimax da Definição 2.1 — ao contrário do teorema de equioscilação de Chebyshev genuíno (necessário e suficiente para melhor aproximação uniforme), aqui não há argumento de cálculo variacional (Euler-Lagrange/Pontryagin) ligando o mínimo de $\kappa^*_{info}$ a esta propriedade de curvatura constante.

**Status: analogia nominal sem prova de correspondência.**

---

## Achado adicional (rastreabilidade)
O `.tex` não contém nenhuma tag/label `OBL-C10-XXX` explícita; a numeração de obrigações no Lean (001–008) não corresponde 1:1 à lista de 5 obrigações fornecida na auditoria. Isso impede verificação cruzada determinística exigida pelo protocolo triádico (`triadic-proof-verifier`).

---

## VERDICT: REVISE

### Pontos exatos a corrigir antes de nova submissão:

1. **Lean (`InformationGeometry.lean`)** — eliminar o padrão "hipótese = tese" em todas as 8 struct/theorem. Reformalizar com objetos reais (`ℝ`, não `Float`; métricas como formas bilineares positivas-definidas via Mathlib `InnerProductSpace`/`Manifold`) e derivar as desigualdades (traço do Hessiano, PAC-Bayes, bypass de barren plateau) a partir de axiomas/definições independentes, não assumi-las diretamente.
2. **Def. 2.1** — provar existência do minimizante $\gamma$ (compacidade/coercividade) e verificar a condição de Chow–Rashevskii para a distribuição horizontal antes de declarar a métrica Carnot-Carathéodory bem-definida.
3. **Teorema 2.2** — fornecer derivação formal (cálculo de Otto) conectando curvatura em $\W_2(\Theta)$ ao traço do Hessiano terminal e ao bound PAC-Bayesiano; descarregar explicitamente a hipótese de sub-Gaussianidade/limitação da perda ou restringir o escopo do teorema a essa classe de perdas.
4. **Teorema 3.1** — resolver a contradição: $O(D)$ também sofre concentração de medida de Lévy (Gromov–Lévy) para $D$ grande; demonstrar por que a restrição de Stiefel evita especificamente essa concentração para a função de perda em questão, e tratar a deriva conhecida da isometria dinâmica durante o treinamento. Derivar (não postular) os limites de complexidade $T \ge \mathcal{O}(2^n)$ / $T \le \mathcal{O}(n^2/\kappa^{*2})$.
5. **Seção 3 (Frenet-Serret)** — derivar a condição de equioscilação $\kappa(s)\equiv\kappa^*_{info}$ como condição de otimalidade do problema da Definição 2.1 via argumento variacional, em vez de impô-la por analogia nominal.
6. **K-FAC** — qualificar precisamente o resultado de complexidade $\mathcal{O}(D)$ com as hipóteses de independência por camada sob as quais ele vale, e reconciliar com a admissão paralela de que K-FAC é apenas um pré-condicionador aproximado.
7. **Rastreabilidade** — inserir `\label{obl:C10-XXX}` no `.tex` correspondentes 1:1 às obrigações formais do Lean, eliminando a divergência de numeração (5 vs. 8 itens).

Enquanto esses pontos não forem corrigidos, o capítulo não atende ao padrão de rigor do framework (Regras 1 e 2), e a certificação Lean atual não constitui verificação formal de nenhuma das obrigações matemáticas substantivas — apenas confirma tautologias sintáticas.