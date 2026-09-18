# AUDITORIA ADVERSARIAL EMBASADA — Relatório Editorial JHEP/SciPost Physics

**Manuscrito:** *Simplicial Quantum Gravity on $\Delta_4 \times \Delta_2$*
**Método:** Leitura cruzada do manuscrito mestre (Doc. 1) contra o Plano de Errata (Doc. 2), o Ledger Lean 4 (Doc. 3) e os Fundamentos de Hierarquia de Férmions (Doc. 4).

A disponibilização dos documentos de embasamento **não elimina** as fragilidades centrais do manuscrito — ao contrário, em dois pontos críticos (Jarlskog, constante cosmológica) ela **revela** que o conteúdo "derivado" citado no texto mestre na verdade não está contido nele, e que uma fórmula anunciada como corrigida (Correção 15) é numericamente irreprodutível a partir de sua própria expressão analítica. Abaixo seguem os problemas identificados, em ordem decrescente de severidade.

---

## PROB-01 [CRÍTICO] — Fórmula do Invariante de Jarlskog é dimensionalmente inconsistente e não reproduz o valor numérico alegado

**Localização:** Seção 8.2 (Subseção "The Quark Sector"), equação não numerada logo após \eqref{eq:delta_cp_predicted}:
$$J_{\mathrm{CP}} = \frac{1}{6\sqrt{3}}\sin(\delta_{\mathrm{CP}})\frac{\sqrt{m_u m_c m_t m_d m_s m_b}}{v^6} \approx 3.04\times10^{-5}.$$
Também reproduzida em Doc. 4 (Seção 2.6) e anunciada como "corrigida" na Correção 15 do Doc. 2.

**Diagnóstico:** $J_{\mathrm{CP}}$ é uma quantidade **adimensional** (invariante de Jarlskog). Porém, $\sqrt{m_u m_c m_t m_d m_s m_b}$ tem dimensão de $[\text{massa}]^3$, enquanto $v^6$ tem dimensão $[\text{massa}]^6$; a razão tem dimensão $[\text{massa}]^{-3}$, não é adimensional. Substituindo os valores numéricos do próprio artigo (Tabela de massas de quarks, $v=246{,}22$ GeV):
$$\sqrt{m_u m_c m_t m_d m_s m_b} \approx 0{,}0294\ \text{GeV}^3, \qquad v^6 \approx 2{,}228\times10^{14}\ \text{GeV}^6,$$
$$\Rightarrow \frac{1}{6\sqrt3}\sin(63{,}90^\circ)\cdot\frac{0{,}0294}{2{,}228\times10^{14}} \approx 1{,}14\times10^{-17}\ \text{GeV}^{-3} \ne 3{,}04\times10^{-5}\ (\text{adimensional}).$$
Testei também as variantes óbvias de correção de digitação — denominador $v^3$ (resultado $\approx 1{,}7\times10^{-10}$) e numerador sem raiz sobre $v^6$ (resultado $\approx 3{,}4\times10^{-19}$) — **nenhuma reproduz $3{,}04\times10^{-5}$**, nem sequer a ordem de grandeza. O valor $3{,}04\times10^{-5}$ coincide, isso sim, com a fórmula padrão de Wolfenstein $J\approx A^2\lambda^6\eta$, que nada tem a ver com a expressão apresentada. Isto indica que o número foi retro-ajustado ao dado experimental do PDG e uma fórmula "geométrica" foi anexada post-hoc sem verificação dimensional ou numérica — exatamente o tipo de falha que a Correção 15 alegava ter sanado.

**Prescrição:** (i) Refazer a derivação completa de $J_{\mathrm{CP}}$ a partir da matriz de Yukawa circulante $\mathbf{Y}_{\mathrm{circ}}$ efetivamente definida no artigo (Seção 8.1), calculando $\mathrm{Im}\det[M_uM_u^\dagger, M_dM_d^\dagger]$ explicitamente e expressando $J$ em termos consistentes (razões de massa adimensionais, não massas absolutas sobre $v^6$). (ii) Se a fórmula for abandonada, remover a alegação de "avaliação direta... dentro de $0{,}27\sigma$" do abstract, da Seção 8.2 e da Tabela 4 do Doc. 4 — atualmente essa é a alegação de precisão mais citada do projeto e está matematicamente incorreta como escrita. (iii) Não publicar nenhuma versão do artigo com esta equação sem que um terceiro (ou script Python/Sympy) reproduza o número a partir da fórmula literal.

---

## PROB-02 [CRÍTICO] — Dois princípios variacionais desconectados: $\mathcal{S}_\infty$ (minimax, Eq. 1.2) nunca se relaciona com $\mathcal{S}_{\mathrm{univ}}$ (quadrática, Eq. 1.10)

**Localização:** Eq. \eqref{eq:minimax_functional_master} (Seção 1) versus Eq. \eqref{eq:simplicial_action_master} (Seção 1.4).

**Diagnóstico:** O artigo introduz **dois** funcionais de ação distintos para o mesmo sistema:
1. $\mathcal{S}_\infty[g,A,\Psi] = \operatorname{ess\,sup}\{\ldots\} \le \ell_P^{-1}$ — um princípio minimax $L^\infty$;
2. $\mathcal{S}_{\mathrm{univ}} = \int(\ldots)\dif\mathrm{vol}_\mathcal{G}$ — uma ação quadrática $L^2$ padrão.

Nenhuma passagem do texto declara a relação lógica entre os dois: não se afirma que (2) é extremizado sujeito ao vínculo (1), nem que (1) é derivado de (2) como um limite/regularização. Na prática, todas as Seções 4–5 (folheações ADM, shear, bounce de Planck) usam **apenas** a restrição minimax (1) e nunca invocam $\mathcal{S}_{\mathrm{univ}}$; e a Seção 8 (massas de férmions, Higgs) usa **apenas** $\mathcal{S}_{\mathrm{univ}}$ e nunca invoca o vínculo minimax. Isto viola diretamente o padrão de acyclicidade/coerência lógica exigido: o leitor não pode verificar que ambos os setores pertencem à mesma teoria de campo, pois nenhuma equação de movimento é derivada de um único princípio de ação unificado — o "framework unificado" é, na estrutura lógica apresentada, dois formalismos justapostos sobre a mesma variedade $\Delta_4\times\Delta_2$.

**Prescrição:** Declarar explicitamente (com um Lema/Proposição) se $\mathcal{S}_\infty \le \ell_P^{-1}$ é: (a) um vínculo de Lagrange imposto sobre extremos de $\mathcal{S}_{\mathrm{univ}}$ (nesse caso, escrever o funcional aumentado $\mathcal{S}_{\mathrm{univ}} + \mu(x)(\mathcal{S}_\infty - \ell_P^{-1})$ e derivar as equações de Euler-Lagrange resultantes); ou (b) uma consequência assintótica de $\mathcal{S}_{\mathrm{univ}}$ no regime UV (nesse caso, prová-la a partir do operador Beta-Laplaciano). Sem essa ponte, o título "unified... framework" não é sustentado pela matemática apresentada.

---

## PROB-03 [ALTO] — Termo de curvatura quadrática $\Tr_E(\mathcal{R}\wedge\star_\mathcal{G}\mathcal{R})/16\pi G_N$ não reproduz Relatividade Geral e reintroduz fantasmas de Ostrogradsky que o artigo alega evitar

**Localização:** Eq. \eqref{eq:gauge_pairing}, quarto termo, e Correção 1/Correção 11 do Doc. 2.

**Diagnóstico:** Ação de Yang-Mills quadrática na curvatura de uma conexão $\mathfrak{so}(4)$ compacta, $\frac{1}{G_N}\Tr(\mathcal{R}\wedge\star\mathcal{R})$, é uma ação de **quarta ordem** nas derivadas da métrica (a curvatura já contém segundas derivadas). Isto **não** é a ação de Einstein-Hilbert (linear em $R$) e, por teoremas conhecidos de gravidade de curvatura quadrática (Stelle 1977), gera um modo de spin-2 massivo do tipo fantasma, a menos que a combinação seja exatamente Gauss-Bonnet (que em 4D é topológica e não contribui à dinâmica) — nesse caso o termo simplesmente não geraria gravitação alguma. Não há, no texto, nenhuma construção do tipo MacDowell-Mansouri (que exigiria a álgebra estendida $\mathfrak{so}(4,1)$ ou $\mathfrak{so}(5)$ quebrada por um campo compensador até $\mathfrak{so}(4)$, produzindo o termo de Einstein-Hilbert mais Gauss-Bonnet mais $\Lambda$) que justificaria a redução a GR usual. Isso contradiz diretamente a Observação da Seção 3 ("Ultraviolet Behavior and Unitarity"), que afirma que o *framework* evita fantasmas de Ostrogradsky — essa afirmação só cobre o setor de matéria (Beta-Laplaciano Lifshitz), não este termo gravitacional separado.

**Prescrição:** Ou (i) reformular explicitamente o setor gravitacional via construção de MacDowell-Mansouri/Plebanski com a álgebra estendida e o mecanismo de quebra que reduz $\Tr(F\wedge\star F)$ ao termo de Einstein-Hilbert padrão, provando ausência de graus de liberdade fantasmas; ou (ii) admitir que o setor gravitacional de $\mathcal{S}_{\mathrm{univ}}$ é uma teoria de gravidade de ordem superior distinta de GR e analisar seu conteúdo de partículas explicitamente.

---

## PROB-04 [ALTO] — Teorema 3.1 (fluxo da dimensão espectral) usa uma relação de dispersão que nunca é derivada do Beta-Laplaciano simplicial da Definição 3.1

**Localização:** Definição \ref{def:beta_laplacian} versus Teorema \ref{thm:spectral_dimension_flow} e sua demonstração.

**Diagnóstico:** A Definição 3.1 especifica o operador $(-\Delta_{\Delta_m})^s$ via autovalores $\lambda_n$ de um núcleo de Dirichlet singular $\mathcal{K}_\alpha(\mathbf{x},\mathbf{y})$ sobre o simplex $\Delta_m$. A demonstração do Teorema 3.1, no entanto, calcula $P(\tau)$ integrando sobre $\mathbb{R}^4$ plano com a relação de dispersão *ad hoc* $\omega^2(k)=k^2(1+\ell_P^2k^2)$ — um cálculo de teoria de campos em espaço plano completamente desconectado da base de autovetores $\{\phi_n,\lambda_n\}$ definida imediatamente antes. Não há demonstração de que os autovalores do operador simplicial de fato convergem, no limite contínuo, para essa dispersão de Lifshitz. O Teorema, portanto, prova uma afirmação correta sobre um modelo de brinquedo em $\mathbb{R}^4$, não sobre o objeto matemático definido na própria Seção 3.

**Prescrição:** Inserir um lema de ponte explícito mostrando que, no limite de refinamento simplicial (ou no limite semiclássico $m\to\infty$), o espectro $\{\lambda_n\}$ de $(-\Delta_{\Delta_m})^\alpha$ converge à dispersão de Lifshitz assumida, com taxa de convergência controlada. Sem esse lema, o Teorema 3.1 deve ser reclassificado como conjectura ou resultado sobre um modelo contínuo auxiliar, não sobre a geometria simplicial central da tese.

---

## PROB-05 [MÉDIO-ALTO] — Teorema 5.1(i) (pressão de Planck $P_{\mathrm{top}}$) não é demonstrado; a prova fornecida aborda apenas (ii) e (iii)

**Localização:** Teorema \ref{thm:planck_bounce}, item (i), Eq. \eqref{eq:planck_pressure_top}, e o parágrafo de prova subsequente.

**Diagnóstico:** A demonstração apresentada deriva $\rho_{\mathrm{crit}}$ diretamente do vínculo $K_{ij}K^{ij}\le 3(\kappa^*)^2$ (itens ii–iii), mas **nunca menciona** $P_{\mathrm{top}}$ nem deriva por que a pressão satura exatamente em $c^7/(\hbar G_N^2)$. Esse valor é simplesmente a pressão de Planck canônica por análise dimensional — válida em *qualquer* teoria de gravidade quântica com escala de Planck, não uma consequência específica do potencial de barreira simplicial $B_\alpha(\mathbf{x})$ alegado no enunciado do teorema. A Correção 13 do Doc. 2 corrigiu o valor numérico corretamente, mas não resolveu a lacuna estrutural: o item (i) permanece um enunciado sem demonstração.

**Prescrição:** Ou remover o item (i) do enunciado do Teorema 5.1 (reclassificando-o como observação de análise dimensional), ou completar a demonstração conectando $B_\alpha(\mathbf{x})$ explicitamente à pressão efetiva via o tensor de energia-momento induzido pelo potencial de barreira.

---

## PROB-06 [MÉDIO-ALTO] — Teorema 9.1 (cancelamento do vácuo) é circular: o "resíduo" $\Lambda_{\mathrm{residual}}$ é definido em termos dos próprios parâmetros observacionais, e o mecanismo de supressão exponencial do Doc. 4 está ausente do manuscrito mestre

**Localização:** Teorema \ref{thm:vacuum_cancellation}, Seção 8.4, e comparação com Doc. 4 Seção 3.3.

**Diagnóstico:** A Eq. \eqref{eq:quartic_cancellation} mostra corretamente que a soma alternada de volumes das faces de $\Delta_4$ pode ser escrita formalmente como $(1-1)^4M_P^4\equiv0$ — mas essa é uma identidade combinatória sobre números binomiais, não uma regularização de campo quântico de fato (a prova invoca "$\partial\circ\partial=0$" sem qualquer cálculo de loop). Mais grave: a fórmula fornecida para o resíduo,
$$\Lambda_{\mathrm{residual}} \sim \frac{3H_0^2\Omega_\Lambda}{c^2}\approx1{,}105\times10^{-52}\text{ m}^{-2},$$
é literalmente a **definição** da constante cosmológica observada em termos de $H_0$ e $\Omega_\Lambda$ — grandezas medidas, não previstas. O mecanismo de supressão não-perturbativo genuinamente proposto no Doc. 4 (Teorema 3.2: $\rho_\Lambda = M_P^4 e^{-2\pi/(\alpha_{\mathrm{GUT}}\mathcal{E}_\infty)}$, com o defeito entrópico de Barnes $\mathcal{E}_\infty=\ln2-1/2$) **não aparece em nenhum lugar do manuscrito mestre**. Isto significa que a alegação do abstract e da Tabela 3 ("solving the $10^{120}$ fine-tuning problem") não é sustentada pelo texto submetido — ela depende inteiramente de conteúdo de um documento de embasamento não incluído no artigo principal.

**Prescrição:** Incluir explicitamente no manuscrito mestre a derivação do Teorema 3.1/3.2 do Doc. 4 (a recorrência de Euler-Maclaurin simplicial com números de Bernoulli e o defeito entrópico de Barnes $\mathcal{E}_\infty$), ou remover a alegação de resolução do problema da constante cosmológica do abstract e do corpo do artigo, substituindo por "mecanismo qualitativo de cancelamento topológico do termo quártico, com supressão residual não derivada neste artigo."

---

## PROB-07 [MÉDIO] — Uso inconsistente e não-derivado do mesmo coeficiente $\alpha_s/\sqrt3$ em contextos físicos distintos (padrão de ajuste numérico, não de derivação unificada)

**Localização:** Eq. \eqref{eq:quark_koide_shift} ($Q_q = \frac23(1+\alpha_s/\sqrt3)$), Eq. \eqref{eq:delta_cp_predicted} ($\delta_{\mathrm{CP}}\approx\pi/3+\alpha_s/\sqrt3$), e Eq. \eqref{eq:cabibbo_angle} ($\sin\theta_C=\sqrt{m_d/m_s}(1+\alpha_s/4\pi)$).

**Diagnóstico:** Três observáveis fisicamente distintos (razão de massa de quarks, fase de violação de CP, ângulo de Cabibbo) recebem correções de "entrelaçamento de cor" com formas funcionais diferentes de $\alpha_s$ ($\alpha_s/\sqrt3$ multiplicativo, $\alpha_s/\sqrt3$ aditivo em radianos, $\alpha_s/4\pi$ multiplicativo), sem que nenhuma seja derivada de um cálculo de loop de QCD explícito (nenhum diagrama, nenhuma integral de Feynman, nenhum operador de Casimir de cor $C_2(F)=4/3$ aparece de fato acoplado nas fórmulas, apesar de a Correção 3 do Doc. 2 alegar que o deslocamento vem do "Casimir de cor $C_2(F)=4/3$" — esse fator $4/3$ não aparece em nenhuma das três fórmulas finais). O padrão sugere ajuste numérico pós-hoc a cada observável individualmente, e não uma correção radiativa unificada de QCD.

**Prescrição:** Fornecer o cálculo de 1-loop explícito (diagrama de troca de glúon, com $C_2(F)$ aparecendo consistentemente) que gera *as três* correções a partir de um único vértice efetivo, ou reclassificar honestamente essas três relações como ajustes fenomenológicos independentes (como já é parcialmente feito para $Q_q$ na Proposição 6.1, rotulada "Phenomenological") — aplicando o mesmo rótulo de honestidade epistêmica às Eqs. \eqref{eq:delta_cp_predicted} e \eqref{eq:cabibbo_angle}, que atualmente aparecem como "Derived Relation"/"Derived Invariant" na Tabela 2, categoria que a Correção 6 do Doc. 2 prometeu reservar a resultados com "teoremas demonstrados passo a passo."

---

## PROB-08 [MÉDIO] — Discrepância numérica entre o próprio manuscrito e o Ledger Lean 4 quanto ao número de obrigações certificadas (141 vs. 144)

**Localização:** Manuscrito, Seção 10 ("Formal Verification..."): *"Verification Coverage: 141 formal proof obligations across 13 modules"*; Remark \ref{rem:lean_status}: *"over 144 certified theorems"*; versus Doc. 3, tabela final: *"TOTAL VERIFIED OBLIGATIONS ... 144/144 ... 100% CERTIFIED"*.

**Diagnóstico:** O próprio corpo do manuscrito é internamente inconsistente (141 na Seção 10 vs. "over 144" na Conclusão), e ambos diferem do total exato reivindicado no ledger externo (144). Para um artigo cuja credibilidade central se apoia na alegação de certificação formal exaustiva "0 sorry," essa falta de reconciliação exata é um sinal de descuido documental que mina a confiabilidade do próprio processo de auditoria declarado (contradiz a Fase 3 do cronograma do Doc. 2, que promete "menção explícita... à concordância formal de 144 obrigações certificadas").

**Prescrição:** Reconciliar o número exato de obrigações certificadas entre o manuscrito, o Doc. 3 e o repositório Lean público antes de qualquer submissão, citando o commit hash exato do repositório verificado.

---

## PROB-09 [MÉDIO] — Teorema 4.1 assume, sem provar, a existência de hipersuperfícies minimax-ótimas e não trata propagação hiperbólica dos vínculos (violação direta do Padrão de Rigor #1 e #4 do próprio protocolo do projeto)

**Localização:** Teorema \ref{thm:minimax_shear}, enunciado ("Let $\Sigma^*\subset\mathcal{M}$ be a spacelike Cauchy hypersurface achieving...").

**Diagnóstico:** O teorema começa por *postular* a existência de $\Sigma^*$ que atinge o limitante minimax $\|\II_{\Sigma^*}\|_{L^\infty}\le\kappa^*$; a demonstração é pura álgebra linear condicionada a essa hipótese, mas não há teorema de existência (Choquet-Bruhat ou variacional) garantindo que tal folheação exista para dados iniciais genéricos satisfazendo os vínculos Hamiltoniano/momento \eqref{eq:wdw_constraint}–\eqref{eq:momentum_constraint}. Tampouco há qualquer demonstração de que os vínculos, uma vez satisfeitos na fatia inicial, permanecem satisfeitos sob a evolução (propagação hiperbólica dos vínculos) — exatamente o item 4 do protocolo de rigor do próprio CLAUDE.md do projeto.

**Prescrição:** Adicionar um Lema de existência (via método variacional direto ou teoria de Choquet-Bruhat com dados iniciais compatíveis) demonstrando que hipersuperfícies minimax-ótimas existem genericamente, e um Lema de propagação de vínculos compatível com a evolução ADM sob o limitante $\kappa^*$.

---

## Nota Editorial e Veredito

O manuscrito contém núcleos matemáticos genuinamente sólidos quando isolados (a demonstração corrigida do Teorema de Koide via equipartição de norma — PROB-08 do errata anterior, agora correta; os limites de shear extrínseco; a estrutura combinatória do fluxo de dimensão espectral, modulo PROB-04). Contudo, a auditoria embasada nos documentos de apoio **piora**, não melhora, o veredito: ela expõe que (a) o resultado de precisão mais anunciado do projeto (Jarlskog, PROB-01) é dimensionalmente incorreto e numericamente irreprodutível a partir de sua própria fórmula; (b) a "unificação" alegada no título é estruturalmente duas teorias desconectadas (PROB-02); (c) o setor gravitacional da ação mestra provavelmente não reduz a Relatividade Geral (PROB-03); e (d) a alegação central sobre a constante cosmológica (abstract, Tabela 3) depende de conteúdo ausente do próprio artigo e é circular como apresentada (PROB-06).

**Nota Editorial: 3/10**

**Veredito Editorial: MAJOR REVISIONS** (não Reject, pois partes isoláveis do arcabouço — Koide, ADM shear bound, spectral dimension formalism sujeito a PROB-04 — são estruturalmente recuperáveis; mas o artigo não pode ser aceito, nem em revisão menor, enquanto PROB-01, PROB-02, PROB-03 e PROB-06 permanecerem sem resolução, dado que atingem diretamente as alegações centrais do abstract.)
