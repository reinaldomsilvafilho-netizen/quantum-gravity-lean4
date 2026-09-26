# Cap. 1 — Reauditoria cega (camada 1)

Arquivo auditado: `chap01_functional_realizations_matrices_tensors.tex` (931 linhas). Nenhum outro capítulo é citado.
Script: `audit/verify/scripts/ch01_blind_checks.py`. Resultado: 26/26 PASS. Os testes de "contraexemplo" dão PASS quando o contraexemplo se confirma. Cada teste tem oráculo independente, e há controles negativos T1-neg, T2-neg, T6b-ctrl, T6c-neg e T7-neg.

Data: 2026-09-25. Verificador: subagente Claude com contexto limpo. Não li ledgers, WORKPLAN nem relatórios de outros agentes.

## Tabela

| Item | Enunciado | Rótulo honesto? | Veredito | Evidência/observação |
|---|---|---|---|---|
| Abstract (i)–(iv) | Realizações revelam invariantes "inaccessible to pure matrix algebra"; (iii) inclui "handlebody decompositions" | Não inteiramente | PROBLEMA (B) | Não há decomposição em alças no corpo. A energia de Dirichlet (eq. 4.x) é $\sum(k_1^2+k_2^2)\lvert a\rvert^2$, uma norma de Frobenius ponderada, e o TV é uma soma de diferenças finitas das entradas; a própria Tabela 1 diz "Finite differences $\Delta A$". Ambas são funções algébricas explícitas das entradas, e "inaccessible" é retórica. |
| Abstract (1) | Penalidade de Sobolev "that corrects spectral blindness in deep learning" | Não | PROBLEMA (B) | O §6.1 trata isso como hipótese a testar ("we do not prove any bound"). O abstract promete mais que o corpo. |
| Abstract (2)–(5) | Correspondência spin glass (estrutural), métricas de rede, posto 1 bem-posto, coarea | Sim | CONFIRMA | (4) ressalva corretamente $r\ge 2$. |
| Intro (a)–(c) | Invariância por permutação; posto tensorial NP-difícil sobre $\mathbb R$ e $\mathbb C$; não-fechamento | Sim | CONFIRMA | Hillar–Lim de fato provam NP-dificuldade sobre $\mathbb R$ e $\mathbb C$. |
| Def. 2.1–2.2 | Operador de realização e propriedades | Definição | CONFIRMA | — |
| Constr. quadrática/homogênea | $f_A=x^TAx$, $f_{\mathcal T}(x)$ | Definição | CONFIRMA | — |
| Prop. (Spectral & Critical) | Extremos $\lambda_1,\lambda_n$; os pontos críticos são os autovetores unitários | Provado | CONFIRMA | O Lagrangiano está correto. |
| Constr. step/pixel/poliedral | $W_A$; $f_A\in L^\infty\cap BV$ | Definição/afirmação | CONFIRMA | — |
| Constr. Fourier | $\lVert f_A\rVert_{L^2(d\mu)}=\lVert A\rVert_F$ | Afirmado | CONFIRMA | Parseval com medida normalizada. |
| Constr. splines | $P\in\mathbb R^{m\times n\times 3}$ com somas $i=0..m$, $j=0..n$ | — | PROBLEMA (B) | Os índices não casam: são $(m+1)(n+1)$ pontos. $C^{p-1}$ exige nós simples. |
| Constr. Fredholm | $\lVert T_A\rVert_{HS}=\lVert A\rVert_F/n$ | Afirmado | CONFIRMA | Teste T4. |
| Thm 4.1 (dirichlet_blindness) | $\mathcal E(f_A)=\sum(k_1^2+k_2^2)\lvert a\rvert^2$; razão $n^2$ entre conjugados por permutação | Provado | CONFIRMA | T1: quadratura FFT contra fórmula (erro < 1e-8). A mutação $(k_1+k_2)^2$ falha. A razão é exatamente $n^2$ para n=3, 7, 12. |
| Remark (isotropic) | $cI$, $cJ$ dão razão 1; o máximo $\Theta(n^2)$ | Observação | CONFIRMA | Os pesos ficam em $[2,2n^2]$, então a razão é no máximo $n^2$. |
| Example (checkerboard) | Espectro $\{n,0,\dots\}$; $\mathcal E=2n\sum k^2$; TV$=\Theta(n)$ | Cálculo | CONFIRMA | T1 e T2: TV$=4(n-1)$. O texto admite corretamente que a energia harmônica não mede oscilação espacial. |
| Thm 4.3 (tv_matrix) | Fórmula do TV de $W_A$ | Provado | CONFIRMA | T2: oráculo independente (integral em $t$ do perímetro relativo de $\{W_A>t\}$) igual à fórmula, 19.1667. A mutação sem $1/n$ falha. Obs. (B): $\Gamma^h_{i,j}$ não é definido. |
| Thm 4.4 (coarea_linkage) | TV$=\int\mathcal H^1(\partial^*E_t)\,dt$ | Clássico citado | CONFIRMA, com B | $\{W>t\}$ é chamado de "sub-level set" (é superníveis). A fórmula é de Fleming–Rishel/Federer; "De Giorgi's structure theorem" não é o que dá a coarea. |
| Thm 4.5 (morse_matrix) | $2n$ pontos críticos, índice $i-1$, $P_{-1}=\chi(S^{n-1})=1-(-1)^n$ | Provado | CONFIRMA | T5: Hessiana riemanniana por diferenças finitas na aplicação exponencial dá índices [0..5] para n=6. O caso n=1 também fecha ($\chi(S^0)=2$). |
| Remark Morse–Bott | Autovalor com multiplicidade $m+1$ dá variedade crítica $S^m$ | Observação | CONFIRMA | — |
| Thm 4.7 (cut norm) | $\lVert W\rVert_\square\le\lVert T_W\rVert_{\infty\to1}\le 4\lVert W\rVert_\square$ | Provado | CONFIRMA, com B | T3: 200 kernels-degrau, razão em [1.05, 3.01]. O título cita "Grothendieck Inequality", que não é usada (a prova é elementar). |
| Thm 4.8 (graphon compactness) | $(\bar{\mathcal W}/\bar\Pi,\delta_\square)$ compacto | Clássico citado | CONFIRMA, com B | O quociente correto identifica $\delta_\square=0$ (equivalência fraca), não órbitas de bijeções. A compacidade é de Lovász–Szegedy 2007 (GAFA, "Szemerédi's lemma for the analyst"); o artigo citado (JCTB 2006) prova existência de limites. |
| Example (identity) | $\lVert W_{I_n}\rVert_\square\le 1/n$ | Cálculo | CONFIRMA | $W\ge0$. |
| Thm 5.1 (tensor_weierstrass) | Máximo atingido; equações de Lim; melhor aproximação de posto 1 existe | Provado | CONFIRMA | "Strictly attained" não tem conteúdo. Qi 2005 trata autovalores de tensores simétricos, não valores singulares (B). |
| Remark (Scope) | $r\ge2$ continua mal-posto | Observação | CONFIRMA | Honesto. |
| Def./Thm 5.3 (hypergraphon) (i) | $\lVert W\rVert_{\square,k}\le\lVert T_W\rVert\le 2^k\lVert W\rVert_{\square,k}$ | Provado | CONFIRMA | Mesmo argumento de 4.7. |
| Thm 5.3 (ii) | Compacidade; "every sequence of high-order tensors with bounded entries" converge em subsequência | Citado (Zhao) | PROBLEMA (B) | Hipergrafons são definidos simétricos e com valores em [0,1], mas o enunciado fala de tensores quaisquer com entradas limitadas: faltam simetrização e normalização afim. A nota sobre a falha do counting lemma é correta e honesta. |
| Thm 5.4 (attention_sobolev) | Com penalidade $H^2$, $\sup\lvert f_{\mathcal A}\rvert\le C\sqrt{\mathcal R}$ "uniformly in the sequence length N" | Provado | PROBLEMA (M) | (1) A desigualdade é só a imersão de Sobolev $H^2(\mathbb T^2)\hookrightarrow L^\infty$, sem nada específico de atenção. (2) "Uniformly in N" engana: para **toda** matriz de atenção softmax, com entradas ≥0 e linhas somando 1, vale $f_{\mathcal A}(0,0)=\sum_{ij}\mathcal A_{ij}=N$. Logo $\sup\lvert f\rvert= N$ e $\mathcal R\ge N^2/C^2$ cresce com N, e nenhuma penalidade fica limitada uniformemente (T8: $f(0,0)=N$ exato; $\mathcal R\sim N^{4.3}$). (3) A penalidade usa $dx\,dy$, mas a prova usa $\lVert f\rVert_{L^2}=\lVert\mathcal A\rVert_F$, que vale para a medida normalizada: falta um fator $(2\pi)^2$. (4) $C$ depende de $\lambda$ ($\sim\lambda^{-1/2}$ quando $\lambda\to0$) e o texto o chama de universal. |
| Thm 5.5 (kac_rice_tensors) | Tensor simétrico gaussiano com entradas independentes de variância $n^{-(d-1)}$: $\mathbb E\lvert\mathrm{Crit}\rvert\sim C(d)e^{n\Theta(d)}$ | "Sketch", prova em ABČ | **PROBLEMA (A)** | (a) **Falso para d=2**: é o Thm 4.5 do próprio capítulo. A simétrica gaussiana tem autovalores distintos q.c., então tem exatamente $2n$ pontos críticos, sem crescimento exponencial (T6: 10, 20, 40, 80 para n=5, 10, 20, 40). (b) Mesmo para $d\ge3$ a ordem do expoente está errada: em ABČ a complexidade total é $\tfrac12\log(p-1)$, que é $\Theta(\log d)$, não $\Theta(d)$. (c) Com a hipótese do texto (todas as entradas do tensor simétrico com a mesma variância), o campo **não é isotrópico**: $\operatorname{Var}f(e_1)=1$ e $\operatorname{Var}f((e_1+e_2)/\sqrt2)=1.5$ para d=2, e 1 contra 2.5 para d=3 (T6b; o controle com variância $1/\mathrm{mult}(m)$ é isotrópico). Isso contradiz o "spherical symmetry $K=\frac1d(x\cdot y)^d$" do sketch, e a diferença para ABČ não é "a deterministic factor". (d) A Hessiana condicional correta é $H_0-d\,f(x)I$ (identidade de Euler), não $-(d-1)f(x)I$. T6c: diferenças finitas na esfera, erro 4e-7 com coeficiente $d$ e 2.08 com $d-1$. Para d=2 o coeficiente $d-1$ contradiz a fórmula $2u^TAu-2\lambda_i$ do Thm 4.5. |
| Thm 5.6 (i) (critical_scaling) | $\mathbb E\sup\lvert\hat f\rvert=\Theta(1)$, escala $1/\sqrt d$ única | Provado | CONFIRMA | O argumento de rede com fator $1/(1-k\epsilon)$ e o limite inferior via $\lVert Z\rVert$ estão corretos. T7: $\sup/\sqrt d\approx$ 2.47, 2.64, 2.73, 2.76 para d=8..48 (k=3). "$c_k$" e "$C(k)$" dependem de k (ok). |
| Thm 5.6 (ii) | $P(\lvert\hat f\rvert>\epsilon)\le2e^{-c_kd\epsilon^2}$, "sharp" | Provado | PROBLEMA (M) | O enunciado não diz em que espaço de probabilidade está (só $u$, ou $T$ e $u$). Se for o conjunto, é trivial e exato: dado $u$, $X(u)\sim N(0,1)$, então vale com $c_k=1/2$ para todo k (T7(ii): var 0.981). A prova dada não fecha: o evento $\{\lVert w\rVert^2>2d\}$ entra como termo aditivo $e^{-d/8}$, que não é dominado por $2e^{-c d\epsilon^2}$ para $\epsilon$ grande, e o "Herbst inductively" não é executado. A conclusão está certa, mas a prova está errada. "Sharp" não é justificado. |
| Remark (spin-glass scaling) | $H_k/d=\hat f$ | Cálculo | CONFIRMA | $d^{-(k-1)/2}d^{k/2}=\sqrt d$. |
| §6.1 Deep learning | "By Thm 4.8, dense weight matrices $W_n$ converge in $\delta_\square$ to $\mathcal W_\infty$"; amostrar $\mathcal W_\infty(i/n,j/n)$ | Proposta | PROBLEMA (M) | A compacidade dá apenas **subsequência** convergente, e exige entradas uniformemente limitadas e simetria (pesos não são simétricos). O limite é classe de equivalência definida q.t.p., então a avaliação pontual $\mathcal W_\infty(i/n,j/n)$ não está definida. "Width $n=10^6$ parameters" mistura largura com número de parâmetros. As ressalvas finais são honestas, mas a frase "converge" é falsa como escrita. |
| §6.2 Física | $\lvert\mathrm{Crit}\rvert\sim e^{n\Theta(p)}$; ABČ "governing the location of the static and dynamic phase transitions"; RSB↔$\beta_0$ | Conjectura rotulada | PROBLEMA (B) | Herda o erro $\Theta(p)$ (o correto é $\tfrac12\log(p-1)$). ABČ relacionam a complexidade com a energia do estado fundamental e o limiar $E_\infty$; a leitura "static/dynamic transitions" é frouxa. A conjectura está honestamente rotulada. |
| §6.3 Redes | $\delta_\square$ entre redes de tamanhos diferentes; (i) "rigorous definition of time derivatives $dW/dt$" | Afirmação | PROBLEMA (B) | $(\widetilde{\mathcal W},\delta_\square)$ é espaço métrico sem estrutura linear. Derivada temporal não está definida sem mais estrutura, e não há prova. |
| §6.4 Tensores | Posto 1 bem-posto; CP-ALS "diverge" | Clássico | CONFIRMA, com B | O conteúdo é honesto. "Standard algorithms ... diverge" é exagero: há degeneração e "swamps", não divergência sistemática. Os conjuntos Tucker/TT de posto limitado são fechados (correto). |
| §6.5 Imagem | TV = perímetro integrado (ROF) | Clássico | CONFIRMA | — |
| Tabela 1 | Síntese | — | CONFIRMA, com B | A linha "$f_{\mathcal T}$ ... spin glass Morse complexity" herda o problema do Thm 5.5. |
| Conclusão / problemas abertos | "arise naturally and rigorously"; 4 problemas abertos | — | CONFIRMA, com B | Os problemas abertos estão bem formulados. "Rigorously" não vale para os Thms 5.4 e 5.5. |

Itens verificados: 34.

## Resumo dos PROBLEMAS por gravidade

**A (erro matemático)**
1. **Thm 5.5 (kac_rice_tensors).** É falso para d=2 (exatamente 2n pontos críticos, pelo Thm 4.5 do próprio capítulo). A ordem $e^{n\Theta(d)}$ está errada: ABČ dão $\tfrac12\log(d-1)$. A hipótese de "entradas independentes de mesma variância" produz campo não isotrópico, então não é o modelo de ABČ, e não é só questão de fator de escala. O coeficiente da Hessiana condicional é $d$, não $d-1$. Evidência: T6, T6b, T6c e a mutação T6c-neg.

**M (lacuna ou rótulo errado)**
2. **Thm 5.4 (attention_sobolev).** "Uniformly in N" é enganoso: $\sup\lvert f_{\mathcal A}\rvert=N$ para toda atenção softmax, então $\mathcal R_{\rm Attn}\ge N^2/C^2$. O resultado é só a imersão de Sobolev, com inconsistência de medida ($(2\pi)^2$) e constante que depende de $\lambda$. Evidência: T8.
3. **Thm 5.6 (ii).** O espaço de probabilidade não é especificado. A prova tem um termo aditivo $e^{-d/8}$ que não é absorvido. O enunciado vale de forma trivial com $c_k=1/2$ (Gaussianidade exata de $X(u)$), e a prova deve ser trocada por isso. Evidência: T7(ii).
4. **§6.1.** "Dense weight matrices converge" em $\delta_\square$: só há subsequência, com hipóteses de simetria e limitação, e a avaliação pontual do grafon limite não está definida.

**B (redação/citação)**
5. Abstract: "handlebody decompositions" sem conteúdo no corpo; "corrects spectral blindness" contradiz o §6.1; "inaccessible to pure matrix algebra" é retórico.
6. Thm 4.7: o título cita Grothendieck, que não é usado. Thm 4.8: o quociente correto é por $\delta_\square=0$, e a compacidade deve ser citada de Lovász–Szegedy 2007 (GAFA).
7. Thm 4.4: "sub-level" deveria ser "super-level"; a coarea é atribuída a De Giorgi em vez de Fleming–Rishel/Federer.
8. Thm 5.3 (ii): faltam simetrização e normalização para "tensores com entradas limitadas".
9. Construção de splines: índices inconsistentes.
10. §6.2: herda $\Theta(p)$, e a atribuição a ABČ ("phase transitions") é frouxa. §6.3 (i): derivada temporal no espaço quociente sem estrutura. §6.4: "CP-ALS diverge" é exagero.
11. Qi 2005 citado para valores singulares (o artigo trata autovalores de tensores simétricos).
