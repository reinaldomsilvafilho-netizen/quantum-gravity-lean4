## Auditoria Matemática Rigorosa — CHAP04: Ondas Simpliciais Não-Lineares e Transporte Poroso Anômalo

Analisei o manuscrito LaTeX (`chap04_simplicial_waves_porous_transport.tex`) e o módulo formal Lean 4 (`Book/Chap04/SimplicialWaves.lean`), com verificação cruzada em `verify_chap04_numerical.py`. Resultado: **há falhas materiais que impedem certificação**, algumas propagando-se através de múltiplas obrigações.

---

### OBL-C04-001 — Auto-adjunção e semi-positividade de $\Delta_{\Delta_m}^\alpha$

A prova da Proposição (linhas 110–121) está estruturalmente correta: a simetrização via $\int u^*(x)u(x-y)dx = \int u(x)u^*(x+y)dx$ é válida, e o passo final que reduz $2|u(x)|^2 - u^*(x)u(x+y) - u(x)u^*(x+y)$ a $|u(x+y)-u(x)|^2$ depende implicitamente de $\int|u(x+y)|^2dx = \int|u(x)|^2dx$ (invariância translacional da medida de Lebesgue) — passo correto, mas **omitido**, o que viola o padrão de rigor exigido (discharge explícito de hipóteses).

**Falha mais séria de consistência de domínio**: a Definição (eq. 5) declara o operador para $u \in H^2(\mathbb{R}^{m-1})$, mas como $\binom{\alpha}{\mathbf y}$ tem suporte compacto em $\Delta_{m-1}(\alpha)$ (domínio limitado), o símbolo $\sigma_{\Delta_m}^\alpha(\mathbf k) \in [0, 2/\alpha^2]$ é **uniformemente limitado** — logo o operador é **limitado em todo $L^2(\mathbb{R}^{m-1})$**, não requer $H^2$. A própria Proposição já opera em $L^2$ geral. Isso é uma inconsistência de domínio entre Definição e Proposição — a analogia com o Laplaciano fracionário clássico (não-limitado) é enganosa aqui.

### OBL-C04-002 — Símbolo de dispersão fechado

**Falha crítica de dependência não auditada**: a fórmula fechada $\sigma_{\Delta_m}^\alpha(\mathbf k) = \frac{1}{\alpha^2}[1-R(\mathbf k)^\alpha\cos(\alpha\Theta(\mathbf k))]$ depende da identidade $\int_\Delta \binom{\alpha}{\mathbf y}e^{-i\mathbf k\cdot\mathbf y}d\mathbf y / I_m(\alpha) = \left(\frac1m\sum_j e^{-ik_j}\right)^\alpha$ (continuação analítica da função característica multinomial), estabelecida no Capítulo 3 (`silvafilho2026simplex`). Segundo o mapa do repositório, o Capítulo 3 **não** está listado como "AUDIT PASSED" (apenas chap01/chap02 do livro unificado têm essa marca). O Teorema~\ref{thm:dispersion} — pilar de todo o capítulo — **não tem prova no manuscrito** (o texto salta diretamente da declaração do teorema para a Seção 3). Isso é uma violação direta da Regra de Rigor #2 (aciclicidade de dependências lógicas): um teorema central é herdado sem prova de uma fonte não certificada.

**Falha crítica independente — nomenclatura da "matriz de Cartan"**: a matriz $\mathbf A_{m-1}$ definida (2 na diagonal, **1** fora da diagonal, densa) **não é** a matriz de Cartan do tipo $A_{m-1}$. A matriz de Cartan padrão de $\mathfrak{sl}(m)$ é tridiagonal: $C_{ij} = 2\delta_{ij} - \delta_{|i-j|,1}$ (2 na diagonal, **−1** apenas nos vizinhos adjacentes, 0 caso contrário) — ver Humphreys, *Introduction to Lie Algebras*. A matriz obtida corretamente do cálculo de $\sum_{j=1}^m k_j^2$ com $k_m=-\sum k_j$ (verifiquei a álgebra — está correta: dá $k^T(I+J)k$ na base de $k_1,\dots,k_{m-1}$) é de fato $2I + (J-I)$, mas isso é o **Gram/quadratic-form da rede de pesos** (ou proporcional ao inverso da métrica de Killing em certa base), não a matriz de Cartan. Esse erro terminológico **não é cosmético**: propaga-se para o resultado central do abstract ("conexão geométrica rigorosa entre sistemas de raízes de álgebras de Lie... e difusão anômala anisotrópica") e para OBL-C04-005 (tensor de permeabilidade). O script numérico (`verify_chap04_numerical.py`, linha 27, 208) **reforça o erro** hard-codando `A2 = [[2,1],[1,2]]` em vez de testar contra a matriz de Cartan real `[[2,-1],[-1,2]]`, e nunca valida a fórmula fechada contra a integral original — apenas confere autoconsistência entre duas formas já assumidas equivalentes (circular).

### OBL-C04-003 — Conservação de massa e energia

Prova estruturalmente sólida e padrão para NLSE não-local (linhas 174–196), condicionada à auto-adjunção (OBL-001, com a ressalva de domínio acima). Sem objeções adicionais de correção lógica aqui.

### OBL-C04-004 — Simetria $S_m$ do soliton fundamental

**Falha crítica**: o "Teorema (Symmetry of Simplicial Solitons)" (linhas 225–227) é **enunciado sem qualquer prova** — nenhum argumento variacional, de unicidade de estado fundamental, ou de simetrização (rearrangement) é oferecido. Da mesma forma, o "Teorema (Simplicial Modulational Instability)" (linhas 205–215), que fundamenta a fórmula de $\Omega^2(\mathbf k)$, **também não tem prova** no manuscrito. Dois de seis teoremas centrais do capítulo são afirmações nuas.

### OBL-C04-005 — Propagador Mittag-Leffler e covariância MSD

As provas (linhas 259–269, 285–305) são metodologicamente corretas (transformada de Laplace–Fourier, expansão em série de $E_\beta$), modulo o mesmo erro de nomenclatura da matriz de Cartan herdado de OBL-002. Adicionalmente, a interpretação de $\langle \mathbf x\mathbf x^T\rangle(t)$ como covariância pressupõe que $u(\mathbf x,t)$ seja uma densidade não-negativa (interpretação probabilística de MSD); como o operador $-\Delta_{\Delta_m}^\alpha$ é limitado (não é um gerador de Lévy padrão), a positividade do propagador de Mittag-Leffler correspondente **não é demonstrada** nem é óbvia por analogia com a literatura clássica de difusão fracionária (que assume geradores não-limitados tipo Feller). Isso é uma lacuna secundária, mas relevante para a interpretação física reivindicada.

---

### Formalização Lean 4 — Falha estrutural de vacuidade

O módulo `SimplicialWaves.lean` **não formaliza nenhum conteúdo matemático real** do capítulo. Cada `structure` embute o próprio enunciado como campo de hipótese (ex.: `SimplicialLaplacian.sym_exact : symmetryError ≤ 1e-12`), e cada `theorem` é provado por `exact` direto do campo da hipótese — isto é, **hipótese e conclusão são sintaticamente idênticas**. Não há definição de $L^2$, transformada de Fourier, operador $\Delta_{\Delta_m}^\alpha$, NLSE, função de Mittag-Leffler, ou matriz de Cartan em `Mathlib`; os valores numéricos inseridos em `verifyChap04` (ex. `symmetryError := 0.0`, `energyRelativeDrift := 3.27e-8`) são **escolhidos a dedo** para satisfazer trivialmente os limiares, refletindo (não verificando independentemente) os resultados do script Python. Isso viola a Regra de Rigor #2 (aciclicidade) da forma mais direta possível: o "kernel formal" é circular por construção e não fornece nenhuma garantia independente de correção. Isto não constitui verificação formal no sentido do Kernel Lean 4 declarado nas diretrizes de auditoria — é teatro de obrigação de prova.

---

## VERDICT: REVISE

### Pontos exatos a corrigir antes de nova submissão:

1. **Provar os Teoremas 2.3 (Dispersion Symbol), 3.2 (Modulational Instability) e 3.4 (Symmetry of Simplicial Solitons)**, atualmente enunciados sem demonstração. Em particular, o Teorema de dispersão deve incluir (ou re-derivar internamente, sem depender de uma importação não certificada) a prova da identidade da função característica multinomial usada para obter a forma fechada de $\sigma_{\Delta_m}^\alpha(\mathbf k)$.
2. **Corrigir a identificação da matriz $\mathbf A_{m-1}$**: renomear explicitamente como a matriz de Gram/forma quadrática associada (não "matriz de Cartan" de $A_{m-1}$), ou demonstrar rigorosamente sob qual convenção não-padrão ela mereceria esse nome — e propagar a correção a todo enunciado que a referencia (símbolo de dispersão, abstract, tensor MSD, script numérico `verify_chap04_numerical.py`).
3. **Resolver a inconsistência de domínio** entre a Definição ($u \in H^2$) e a Proposição/prova (válida em $L^2$ geral), aproveitando para declarar explicitamente que $-\Delta_{\Delta_m}^\alpha$ é um operador limitado em $L^2(\mathbb{R}^{m-1})$ (dado $\sigma \le 2/\alpha^2$), o que também deveria ser mencionado como distinção física/matemática frente ao Laplaciano fracionário de Riesz clássico (não-limitado) citado na introdução.
4. **Tornar explícito** o passo de invariância translacional $\int|u(x+y)|^2dx=\int|u(x)|^2dx$ na prova de auto-adjunção.
5. **Endereçar a positividade do propagador** de Mittag-Leffler anisotrópico antes de reivindicar a interpretação probabilística de MSD, ou reformular o resultado como momento formal no espaço de Fourier sem apelo a densidade de probabilidade.
6. **Reformular o módulo Lean 4** para formalizar objetos matemáticos reais (ou, no mínimo, documentar explicitamente que `SimplicialWaves.lean` é um *placeholder* de certificação numérica de limiares — não uma prova formal do conteúdo analítico — evitando o rótulo "CERTIFIED" nos comentários de cabeçalho, que induz a uma leitura de verificação formal completa que não ocorre).
7. **Reforçar `verify_chap04_numerical.py`** para validar a fórmula fechada do símbolo de dispersão contra a integral original (eq. 3, quadratura numérica direta do núcleo Beta multinomial), em vez de comparar apenas duas formas fechadas já assumidas equivalentes — eliminando a circularidade da Bateria 1.

Nenhum destes pontos invalida a estrutura geral do programa (operador não-local via núcleo Beta, NLSE, difusão fracionária); são falhas de rigor discharge-level e de rotulagem, corrigíveis, mas que impedem certificação FINAL no estado atual.