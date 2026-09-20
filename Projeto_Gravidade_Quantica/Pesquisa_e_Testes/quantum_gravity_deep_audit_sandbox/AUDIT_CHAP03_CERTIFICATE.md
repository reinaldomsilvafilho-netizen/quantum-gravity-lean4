# AUDITORIA MATEMÁTICA RIGOROSA — CAPÍTULO 3
## Continuação Analítica do Simplex de Pascal e Cálculo Fracionário Simplicial

**Auditor**: Chief Adversarial Proof Engineer / Master Mathematical Auditor
**Manuscrito**: `chap03_pascal_simplex_continuous_multinomials.tex`
**Módulo Lean**: `formal_proofs_book/Book/Chap03/PascalSimplex.lean`

---

## Metodologia

Reexecutei a derivação analítica de cada obrigação independentemente (não me apoiei nos vereditos pré-existentes `PROOF_AUDIT_CHAP03_FINAL.md`/`_CERTIFIED.md` já presentes no sandbox), e inspecionei linha a linha o núcleo Lean 4 para verificar se ele de fato formaliza os objetos matemáticos (Γ, ψ, integrais, simplex) ou apenas embrulha hipóteses numéricas.

---

## Avaliação por Obrigação

### OBL-C03-001 (Continuação meromorfa + sistema PDE Digamma) — **CORRETO**
- Recorrência de Stifel verificada por álgebra direta com $\Gamma(z+1)=z\Gamma(z)$: confere exatamente.
- Sistema PDE $\partial_x\ln\binom{x}{y}=\psi(x+1)-\psi(x-y+1)$ e $\partial_y\ln\binom{x}{y}=\psi(x-y+1)-\psi(y+1)$: confirmado por diferenciação direta do logaritmo da razão de Gammas.
- Representação meromorfa via reflexão de Euler: refiz a substituição completa ($\Gamma(y+1)\Gamma(-y)=-\pi/\sin(\pi y)$, etc.) e a fórmula fechada bate exatamente com o texto.

### OBL-C03-002 (Recorrência de defeito de face de Euler–Maclaurin + escala de Fourier) — **REVISAR (rigor)**
- A decomposição pelos $m$ facetas (incluindo a faceta "distante" $\sum y_j=n$) está geometricamente correta: cada faceta, quando restrita, reproduz exatamente o integrando $(m-1)$-partido, dando $I_{m-1}(n)$ por faceta. Correto.
- **Falha de precisão assintótica**: para $m$ fixo e $n\to\infty$, $I_{m-1}(n)\sim(m-1)^n$, que é *exponencialmente* menor que o termo de resto declarado $\mathcal O(m^n/n)$ (decaimento de $(1-1/m)^n$ é exponencial, não polinomial). Logo o termo explícito $-\frac{m}{2}I_{m-1}(n)$ é assintoticamente absorvido pelo próprio resto $\mathcal O(m^n/n)$ nesse regime — a fórmula não erra, mas cria uma falsa impressão de ordem hierárquica de correção. É válida apenas como identidade de Euler–Maclaurin de faceta única em $n$ finito, não como expansão assintótica ordenada. **Correção necessária**: declarar explicitamente o regime (n finito vs. $n\to\infty$ com $m$ fixo) ou reescrever como $I_m(n)=m^n-\mathcal O(m^n/n)$ com o termo $I_{m-1}(n)$ apresentado como aproximação prática, não como correção de ordem líder.
- Na prova de Thm. 3.1 (representação de Fourier multidimensional), a Hessiana $H_{jk}=-\frac1m\delta_{jk}+\frac1{m^2}$ é descrita como "negativo-definida na hiperplano $\sum\theta_j=0$" — mas neste teorema **não há** tal restrição de hiperplano ($\theta_m\equiv0$ é um *gauge fixo*, não um vínculo sobre as $m-1$ variáveis livres). Recalculei os autovalores de $H$ sobre $\mathbb R^{m-1}$ *irrestrito*: todos são $<0$ ($-1/m^2$ no autovetor "todos-uns", $-1/m$ nos demais), de modo que $H$ é negativo-definida em todo o espaço — afirmação mais forte do que a enunciada, mas o enunciado como escrito parece copiado do contexto posterior (Seção 7, onde há de fato um vínculo genuíno $\sum k_j=0$). Não invalida a conclusão, mas é uma imprecisão textual que deve ser corrigida.

### OBL-C03-003 (Campo potencial Digamma conservativo via Stokes / Estrela de Davi) — **REVISAR (erro de domínio, contradição interna)**
- O Teorema afirma que $\mathbf F=\nabla\ln\binom{x}{y}$ é "um campo gradiente suave no quadrante positivo aberto" $\mathbb R_{>0}^2$, e portanto $\oint_\gamma \nabla\ln\binom{x}{y}\cdot d\mathbf r=0$ para qualquer curva de Jordan fechada nesse quadrante.
- Isso **contradiz diretamente a Proposição 1.4** do mesmo capítulo, que estabelece que $\binom{x}{y}$ possui uma "grade infinita de linhas nodais de zero" fora do intervalo $y\in[0,x]$ — região que está inteiramente contida em $\mathbb R_{>0}^2$ quando $y>x>0$. Nessas linhas nodais, $\binom{x}{y}=0$ ou muda de sinal, logo $\ln\binom{x}{y}$ não é suave (nem real) ali.
- Consequentemente, o Teorema de Stokes não pode ser aplicado a uma curva de Jordan arbitrária em $\mathbb R_{>0}^2$ — apenas em subdomínios onde $\binom{x}{y}>0$ (essencialmente $\{0<y<x\}$, um cone, não simplesmente conexo o suficiente para curvas arbitrárias fechadas fora dele). **Correção necessária**: restringir o domínio do teorema ao cone de positividade $\{(x,y): 0<y<x\}$ (ou a subconjuntos simplesmente conexos dele evitando as linhas nodais), e reformular a condição sobre a curva $\gamma$.

### OBL-C03-004 (Entropia logarítmica de linha via Barnes $G$) — **CORRETO (verificado independentemente)**
- Refiz a dedução completa a partir do Teorema de Alexeiewsky padrão ($\int_0^z\ln\Gamma(t)dt = \frac{z(1-z)}2+\frac z2\ln(2\pi)+z\ln\Gamma(z)-\ln G(z+1)$) combinada com $\int_0^1\ln\Gamma(t)dt=\frac12\ln(2\pi)$ (Raabe) e a equação funcional $G(z+1)=\Gamma(z)G(z)$. O resultado fechado $\mathcal E(x)=x(x+1)-x\ln(2\pi)-x\ln\Gamma(x+1)+2\ln G(x+1)$ bate exatamente com minha derivação independente. Este é o resultado mais solidamente correto do capítulo.

### OBL-C03-005 (Laplaciano fracionário Beta-kernel + métrica de Cartan $A_{m-1}$) — **REVISAR (erro de identificação matemática)**
- A propriedade de semigrupo, o limite identidade e a ação sobre exponenciais estão corretamente derivados via a função geradora multinomial/Chu-Vandermonde contínua.
- **Erro substantivo**: a matriz $\mathbf A_{m-1}$ derivada (diagonal $=2$, todos os fora-da-diagonal $=+1$) **não é** a matriz de Cartan da álgebra de Lie $A_{m-1}$. A matriz de Cartan padrão de $A_{m-1}$ é tridiagonal, com entradas fora-da-diagonal $-1$ (adjacentes) e $0$ (não-adjacentes). Verifiquei numericamente: para $m=4$ ($A_3$, matriz $3\times3$), os autovalores da matriz de Cartan tridiagonal real são $\{2-2\cos(k\pi/4)\}_{k=1}^3\approx\{0.586,\,2,\,3.414\}$, enquanto os autovalores da matriz $I+J$ apresentada no texto são $\{4,1,1\}$ — **conjuntos distintos**, confirmando que não são a mesma forma quadrática sob isometria.
- A matriz $I+J$ derivada é, de fato, corretamente identificada como a matriz de Gram do simplex regular $(m-1)$-dimensional (na parametrização de coordenadas usada) — essa parte do enunciado está certa. Mas a frase "matriz de Cartan da álgebra de Lie $A_{m-1}$" é uma identificação incorreta/imprecisa de terminologia de teoria de Lie. **Correção necessária**: (a) remover a afirmação de que é "a matriz de Cartan" e manter apenas "matriz de Gram do simplex regular / forma quadrática invariante de $A_{m-1}$ na base padrão", OU (b) apresentar explicitamente a mudança de base para a base de raízes simples ($k_j-k_{j+1}$) que produziria a matriz tridiagonal genuína, com prova da congruência.
- Lei de Weyl e relação de dispersão do símbolo espectral: matematicamente consistentes com a estrutura declarada (não encontrei erro adicional), mas dependem da correção acima quanto à nomenclatura "Cartan".

---

## Falha Crítica Transversal: Núcleo Lean 4 é Circular/Vazio

Este é o achado mais grave e afeta **todas as 16 obrigações simultaneamente**. Inspecionando `PascalSimplex.lean`:

```lean
structure StifelRecurrence where
  stifelError : Float
  stifel_exact : stifelError ≤ 1e-10
  ...
theorem stifel_recurrence_digamma_pde (S : StifelRecurrence) :
    S.stifelError ≤ 1e-10 ∧ ... := by
  exact ⟨S.stifel_exact, ...⟩
```

Cada uma das 16 "estruturas certificadas" define um campo `Float` livre e um campo de prova (`..._exact`, `..._valid`) que **assume por hipótese** exatamente a desigualdade que o "teorema" subsequente afirma provar. O "teorema" é uma tautologia lógica — `exact S.stifel_exact` simplesmente reextrai a hipótese do registro. Nenhuma definição real de $\Gamma$, $\psi$, integral simplicial, função de Barnes $G$, ou Laplaciano fracionário aparece em nenhum lugar do arquivo. Na função `verifyChap03`, os valores numéricos (`stifelError := 0.0`, `pdeXError := 2.64e-10`, etc.) são **literais digitados manualmente** pelo autor, não computados a partir de nenhuma avaliação Lean das funções especiais reais — o kernel apenas confirma via `by decide` que esses literais escolhidos à mão satisfazem os limiares também escolhidos à mão.

Isso viola diretamente a Regra de Rigor Estrito do `CLAUDE.md` (item 2: "Acyclicity in logical dependencies"): não há dependência lógica genuína entre o conteúdo matemático do capítulo e as "provas" Lean — a estrutura é circular por construção (hipótese = tese). Portanto, a alegação de "Formalização Engine: Lean 4" e "Certified Obligations" no cabeçalho do arquivo é **enganosa**: não existe verificação formal independente de nenhuma das 16 obrigações; existe apenas confirmação de que números escolhidos pelo autor obedecem cotas escolhidas pelo autor.

**Correção necessária**: o módulo Lean precisa ser reconstruído para (i) formalizar de fato $\Gamma$/$\psi$ via Mathlib (`Mathlib.Analysis.SpecialFunctions.Gamma`, `Polygamma`), (ii) derivar as igualdades/PDEs simbolicamente ou (iii), se a intenção é apenas certificação numérica (ponte número→teorema), então isso deve ser reclassificado explicitamente como "numerical certification bridge" e não como "prova formal Lean 4", evitando a linguagem de "CERTIFIED" que sugere verificação dedutiva completa.

---

## VERDICT: REVISE

### Pontos exatos a corrigir, em ordem de severidade:

1. **[CRÍTICO — todas as obrigações]** Reconstruir `PascalSimplex.lean` para eliminar a circularidade estrutura-hipótese≡tese, ou reclassificar honestamente a certificação como ponte numérica (não "formal proof").
2. **[OBL-C03-003]** Corrigir o domínio do Teorema de Stokes/Estrela-de-Davi: restringir a curva de Jordan $\gamma$ ao cone de positividade $\{0<y<x\}$, eliminando a contradição com a Proposição 1.4 (linhas nodais de $\binom{x}{y}$ fora de $[0,x]$).
3. **[OBL-C03-005]** Corrigir a identificação da matriz $\mathbf A_{m-1}=I+J$ como "matriz de Cartan de $A_{m-1}$" — os autovalores não coincidem com os da matriz de Cartan tridiagonal padrão (verificado para $m=4$: $\{4,1,1\}$ vs. $\{3.414,2,0.586\}$). Renomear para "matriz de Gram do simplex regular" ou fornecer a mudança de base explícita para a forma tridiagonal.
4. **[OBL-C03-002]** Esclarecer o regime assintótico da fórmula de defeito de face: o termo $-\frac m2 I_{m-1}(n)$ é exponencialmente subdominante ao resto declarado $\mathcal O(m^n/n)$ quando $n\to\infty$ com $m$ fixo; declarar o regime de validade pretendido (n finito ou joint asymptotics).
5. **[OBL-C03-002, menor]** Corrigir a descrição da Hessiana na prova do Teorema de representação de Fourier multidimensional — não há vínculo de hiperplano $\sum\theta_j=0$ nesse teorema (apenas gauge $\theta_m\equiv0$); a negativo-definição vale no espaço irrestrito $\mathbb R^{m-1}$ inteiro, mais forte do que o texto declara.

Pontos 3 e 4 (OBL-C03-004) e a maior parte de OBL-C03-001 foram **verificados independentemente como corretos** e não exigem revisão.