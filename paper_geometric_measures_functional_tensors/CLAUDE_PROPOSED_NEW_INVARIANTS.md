## Panorama e critério de seleção

Antes das propostas, uma observação estrutural: todos os invariantes de Vol. I–II compartilham uma limitação de *codomínio* — $\Phi(A)$ é sempre uma função **escalar** $\Omega \to \mathbb{R}$ (ou uma medida $d\mu_A = \Phi(A)\,dx$). Isso já rendeu uma colheita rica (Sobolev, BV, Wasserstein, Bakry-Émery, TDA, Willmore, microlocal, NCG, QFI), mas **três das seis fronteiras que você propõe exigem, estruturalmente, sair desse codomínio**: gauge de ordem superior precisa que $\Phi$ vire uma *conexão* $\Omega^1(\Omega,\mathfrak g)$; feixes microlocais funcionam melhor quando $\Phi$ é *matriz-valorada* (uma família de matrizes sobre $\Omega$, não um escalar); e holografia/emaranhamento exige que $\Phi$ vire um **núcleo bipartido** $\Omega\times\Omega \to \mathbb{C}$ (i.e. $\Phi(A)(x,y)$ com $\Phi(A)(x,x)$ recuperando o caso escalar). Isso não é um defeito — é o próximo salto categórico natural, e devo sinalizar explicitamente quando uma proposta exige essa mudança de codomínio vs. quando é uma extensão direta do formalismo atual.

Abaixo, uma proposta forte por fronteira (duas nas mais ricas), cada uma com definição exata, ferramentas, ponto cego resolvido, e viabilidade/encaixe.

---

## 1. Topologia Simplética e de Contato

**Nome formal**: *Capacidades de Ekeland–Hofer generalizadas e invariantes espectrais de Floer–Viterbo do sub-nível $K_t(A)$.*

**Definição**: Suponha $\Omega = \mathbb{R}^{2n}$ (ou $T^{2n}$) munido da forma simplética canônica $\omega = \sum dp_i\wedge dq_i$, e seja $\Phi(A)\in C^2(\Omega)$ convexa (caso natural quando $\Phi(A)$ vem de uma forma quadrática associada a $A\in \mathcal S_+^n$, mas também válido para realizações convexas gerais). Para $t$ regular, defina o corpo convexo
$$K_t(A) := \{x\in\Omega : \Phi(A)(x)\le t\}.$$
A *capacidade simplética generalizada* é
$$c_k^{EH}(A,t) := c_k^{EH}(K_t(A)),$$
via o princípio variacional de Ekeland–Hofer (ação dual de Clarke sobre o funcional convexo). Quando $K_t(A)$ não é convexo, use a capacidade de Hofer–Zehnder
$$c_{HZ}(A,t) := \inf\{\text{período de uma característica fechada em }\partial K_t(A)\},$$
que existe para qualquer domínio limitado com fronteira suave (Hofer–Zehnder 1994, sem hipótese de convexidade). O refinamento dinâmico é o **invariante espectral de Viterbo–Schwarz–Oh**: para $a\in H_*(\Omega;\mathbb{Z}_2)\setminus\{0\}$,
$$c(a, \Phi(A)) := \inf\{\lambda \in \mathbb{R} : a \in \mathrm{im}(H_*(F^\lambda) \to H_*(\Omega))\}$$
do complexo de Floer filtrado por ação do fluxo Hamiltoniano de $\Phi(A)$.

**Espaço e ferramentas**: $(\Omega,\omega)$ ou $(T^*\Omega,\omega_{\mathrm{can}})$; teoria de Ekeland–Hofer, Hofer–Zehnder, homologia de Floer Hamiltoniana, geometria de Hofer.

**Ponto cego resolvido**: Autovalores e traço são invariantes sob **conjugação linear** $A \mapsto U^TAU$. Capacidades simpléticas são invariantes sob todo o grupo (infinito-dimensional) de **simplectomorfismos** de $\Omega$ — um grupo estritamente maior que $O(n)$ ou $U(n)$ — e são estritamente mais finas que volume: dois corpos com o mesmo volume podem ter capacidades diferentes (não-esmagamento de Gromov). Isso captura "forma de fase" de $\Phi(A)$ invisível a qualquer invariante espectral ou até a persistência topológica (que é invariante sob todo homeomorfismo, logo *cega* demais para capturar rigidez simplética).

**Viabilidade e encaixe**: Alta para o caso convexo (fórmula fechada via largura simplética linear de Williamson quando $\Phi(A)$ é quadrática — conecta diretamente a $A$ original). Estabilidade Lipschitz $|c(a,A)-c(a,B)|\le \|\Phi(A)-\Phi(B)\|_{C^0}$ ecoa literalmente o teorema de estabilidade bottleneck que vocês já provaram para $\mathrm{Dgm}_k$ — bom presságio de que o mesmo padrão de prova (comparação de sub-níveis) se transporta. Recomendo como **capítulo de abertura de Beyond the Spectrum III**: é a extensão mais barata tecnicamente e mais estruturalmente análoga ao que já existe.

---

## 2. Topologia Algébrica Superior e Teoria de Calibre de Ordem Superior

**Nome formal**: *Holonomia de Chern–Simons e classe de gerbe de Deligne–Beilinson de tensores de ordem $k\ge 3$.*

**Definição**: Isto exige a mudança de codomínio mencionada acima. Para $A\in T^3(V)$ (tensor de ordem 3), redefina a realização como uma **conexão** em vez de uma função:
$$\mathcal A_A := \Phi(A)_i(x)\,dx^i \in \Omega^1(\Omega,\mathfrak u(N)),$$
onde $\Phi(A)_i(x)$ é a contração da parte antissimétrica de $A_{ijk}$ contra uma base de teste, produzindo uma 1-forma $\mathfrak u(N)$-valorada. A curvatura é $F_A = d\mathcal A_A + \mathcal A_A\wedge\mathcal A_A$, e o **funcional de Chern–Simons**
$$CS(A) := \frac{1}{4\pi}\int_\Omega \mathrm{Tr}\Big(\mathcal A_A\wedge d\mathcal A_A + \tfrac{2}{3}\mathcal A_A\wedge\mathcal A_A\wedge\mathcal A_A\Big) \pmod{\mathbb Z}$$
é um invariante $U(1)$ (fase), bem definido módulo grandes transformações de calibre — exatamente a estrutura de uma classe de Deligne–Beilinson $[\mathcal A_A]\in H^3_D(\Omega,\mathbb Z(2))$. Para $k\ge 4$, a generalização natural é uma **2-conexão de gerbe** $B_A\in\Omega^2(\Omega)$ com holonomia de superfície $\mathrm{Hol}_\Sigma(\mathcal G_A) := \exp\big(2\pi i \int_\Sigma B_A\big)$ para $\Sigma\subset\Omega$ fechada.

**Espaço e ferramentas**: fibrados principais e gerbes com conexão, cohomologia de Deligne–Beilinson, teoria de Chern–Weil, transgressão.

**Ponto cego resolvido**: Toda a Vol. I–II reduz $A$ a um campo **escalar**, descartando integralmente o grau de liberdade "rotacional"/antissimétrico de ordem $\ge 3$ que não tem análogo em matrizes ($k=2$). Chern–Simons e holonomia de gerbe capturam dados de **transporte paralelo global** (ligação, enquadramento, torção topológica) que nenhuma redução escalar pode ver — análogo a como o laço de Wilson detecta linking que nenhuma curvatura local detecta.

**Viabilidade e encaixe**: Média-baixa como extensão imediata — exige repensar $\Phi$ como funtor para conexões, não função, o que é uma mudança de categoria-alvo, não um capítulo adicional. Recomendo **não** para Beyond the Spectrum III (que deveria manter $\Phi:\to F(\Omega)$ ou $F(\Omega\times\Omega)$), mas sim como semente de um **quarto tratado independente** ("Beyond the Spectrum IV: Higher Gauge Invariants of Tensors of Order $\ge 3$"), coordenado com o material de redes tensoriais contínuas do Cap. 11.

---

## 3. Teoria de Feixes e Análise Microlocal de Feixes

**Nome formal**: *Ciclo característico $CC(\mathcal F_A)$ da estratificação por posto de uma realização matriz-valorada.*

**Definição**: Suponha agora $\Phi: T^k(V) \to F(\Omega, \mathrm{Mat}_n(\mathbb R))$ — i.e., $\Phi(A)(x)$ é uma **matriz** para cada $x$ (o caso natural para redes tensoriais contínuas, onde $x$ parametriza posição no bulk e $\Phi(A)(x)$ é a matriz de ligação/bond local). Estratifique
$$\Omega = \bigsqcup_r \Sigma_r(A), \qquad \Sigma_r(A) := \{x\in\Omega : \mathrm{rank}\,\Phi(A)(x) = r\}.$$
Seja $\mathcal F_A \in D^b_c(\Omega)$ o complexo constructível associado a essa estratificação (por exemplo, o feixe de ciclos evanescentes de $\det(\Phi(A)(x) - t\cdot\mathrm{Id})$ em $t=0$). O **micro-suporte de Kashiwara–Schapira** $SS(\mathcal F_A)\subset T^*\Omega$ é o menor fechado cônico coisotrópico fora do qual $\mathcal F_A$ é localmente constante na direção covetorial. Quando $\mathcal F_A$ é construtível, $SS(\mathcal F_A)$ é Lagrangiano e seu **ciclo característico**
$$CC(\mathcal F_A) := \sum_\alpha m_\alpha [\overline{T^*_{\Sigma_\alpha}\Omega}] \in Z_{\mathrm{Lagr}}(T^*\Omega)$$
(soma sobre os estratos, com multiplicidades $m_\alpha$ dadas por índices de Milnor locais) satisfaz o **teorema do índice de Kashiwara**: $\chi(\Omega, \mathcal F_A) = CC(\mathcal F_A)\cdot [\text{seção nula}]$.

**Espaço e ferramentas**: categoria derivada $D^b_c(\Omega)$, teoria de Kashiwara–Schapira, classe de Chern–MacPherson de variedades singulares, teoria de Morse estratificada.

**Ponto cego resolvido**: Posto de uma matriz é um único inteiro para UM objeto fixo. Aqui $A$ não é uma matriz — é uma *família contínua de matrizes sobre $\Omega$* — e a álgebra linear clássica simplesmente não tem vocabulário para "como o posto degenera ao longo de uma família", nem para propagação de singularidades associada. Isso é precisamente o problema que motivou Kashiwara–Schapira, e aqui ele é transportado para redes tensoriais contínuas de forma natural — é também um refinamento estrito do $\mathrm{WF}(\Phi(A))$ escalar que vocês já têm: $SS(\mathcal F_A)$ agrega o wavefront de *cada* estrato simultaneamente, não de um único nível.

**Viabilidade e encaixe**: Alta — é a extensão tecnicamente mais natural do material microlocal já existente (Seção de Vol. II), pois basta promover $\Phi(A)$ escalar para matriz-valorada, algo que o programa de "redes tensoriais contínuas" já pressupõe implicitamente. Recomendo como **segundo capítulo âncora de Beyond the Spectrum III**, imediatamente após o simplético.

---

## 4. Geometria Métrica e Hiperbólica não-linear

**Nome formal**: *Família espectral do $p$-Laplaciano ponderado $\{\lambda_1^{(p)}(A)\}_{p\in(1,\infty)}$ e hiperbolicidade de Gromov de $(\Omega, g_A)$.*

**Definição (peça central)**: com $d\mu_A = \Phi(A)\,dx$ como já definido para Wasserstein/Bakry–Émery, defina o operador não-linear
$$\Delta_p^A u := \mathrm{div}\big(|\nabla u|^{p-2}\nabla u\big) \quad \text{relativo a } \mu_A,$$
e o primeiro autovalor não-linear via princípio variacional (não espectro linear — não há teorema espectral para $p\ne2$):
$$\lambda_1^{(p)}(A) := \inf\left\{ \frac{\int_\Omega |\nabla u|^p \,d\mu_A}{\int_\Omega |u|^p\,d\mu_A} : \int_\Omega |u|^{p-2}u\,d\mu_A = 0 \right\}.$$
Essa família **interpola de forma provável** entre invariantes que vocês já têm: $\lambda_1^{(p)}(A)^{1/p} \to h(A)/2$ quando $p\to\infty$ (Cheeger, já em Vol. II — Kawohl–Fridman), e a formulação $p=1$ relaciona-se à perimetria BV/coárea (já em Vol. I). O **invariante genuinamente novo** é a função $p\mapsto\lambda_1^{(p)}(A)$ inteira — sua log-convexidade em $1/p$, seus pontos de não-diferenciabilidade (transições de fase espectrais análogas a transições de clustering em grafos) — não um único número.

**Segundo invariante (complementar)**: equipe $\Omega$ com a métrica conforme $g_A := \Phi(A)^{2/d}\,\delta$ e defina a constante de $\delta$-hiperbolicidade de Gromov via produto de Gromov na métrica de comprimento induzida $d_{g_A}$:
$$\delta(A) := \sup_{x,y,z,w} \big[(x|y)_w - \min((x|z)_w,(y|z)_w)\big]_{d_{g_A}}.$$

**Espaço e ferramentas**: teoria de Ljusternik–Schnirelmann/gênero de Krasnoselskii (substitui o teorema espectral, inexistente para operadores não-lineares), cálculo das variações, geometria coarse de Gromov.

**Ponto cego resolvido**: "Espectro" pressupõe **linearidade** do operador. Para $p\ne2$, $\Delta_p$ não é linear e não há teoria espectral clássica — os "autovalores" só existem via minimax variacional. Isso não é uma extensão técnica de álgebra linear; é uma categoria de invariante **inacessível em princípio** a ela, porque o próprio conceito de espectro deixa de fazer sentido. Já a hiperbolicidade de Gromov é uma invariante *coarse* (grande escala), ortogonal à curvatura pontual de Bakry–Émery já capturada — mede "tree-likeness" global, não curvatura local.

**Viabilidade e encaixe**: Muito alta, extensão barata e natural do aparato PDE/variacional já dominado no livro (BV, coárea, Cheeger, Bakry–Émery estão todos ali). Bom para **Parte II do livro-mestre** (fluxos geométricos) *e* como capítulo de Beyond the Spectrum III — funciona nos dois lugares.

---

## 5. Gravitação Quântica e Holografia Avançada

**Nome formal**: *Realização bipartida em núcleo $\Phi: T^k(V)\to F(\Omega\times\Omega)$ e a tríade Hamiltoniano modular / entropia refletida / seção transversal de cunha de emaranhamento.*

**Definição**: Este é o salto estrutural mais profundo e, dado o Cap. 11 (RT, holonomias de Wilson) e o QFI de Vol. II já existentes, o mais "on-brand". Em vez de colapsar $A$ em uma densidade diagonal $\Phi(A)(x)$, realize-a como **núcleo integral** $K_A(x,y)$ com $K_A(x,x) = \Phi(A)(x)$ recuperando o caso escalar (pense em $K_A$ como núcleo reprodutor de um RKHS associado a $A$). Isso permite:

1. **Hamiltoniano modular genuíno**: para uma bipartição $\Omega=\Omega_1\sqcup\Omega_2$, a matriz densidade reduzida $\rho_{\Omega_1} := \mathrm{Tr}_{\Omega_2} K_A$ (traço parcial via integração em $\Omega_2$) dá $K_{\Omega_1} := -\log\rho_{\Omega_1}$ — note que isso generaliza estritamente o $V_A=-\log\Phi(A)$ que vocês já usam para Bakry–Émery, que é o caso degenerado sem bipartição.
2. **Entropia refletida**: $S_R(\Omega_1{:}\Omega_2) := -\mathrm{Tr}(\sigma_{\Omega_1\Omega_1^*}\log\sigma_{\Omega_1\Omega_1^*})$ onde $\sigma$ vem da purificação canônica $|\sqrt{\rho_A}\rangle$.
3. **Seção transversal de cunha de emaranhamento**: $EW(A;\Omega_1,\Omega_2) := \min_\gamma \mathrm{Area}_{g_A}(\gamma)$ sobre superfícies $\gamma$ que bissectam a cunha holográfica construída a partir da métrica induzida por $K_A$ — recuperando e refinando rigorosamente o contorno de emaranhamento $S_{\mathrm{cont}}(x)$ que já é invariante de Vol. II, mas agora derivado como propriedade genuína de uma matriz densidade reduzida, não postulado.
4. **Complexidade = Volume**: $C_V(A) := \mathrm{Vol}_{g_A}(\Sigma_{\max})/(G_N\ell)$, com $g_A$ a métrica de Fisher/Bures induzida por $K_A$ — distância geodésica no *espaço de realizações*, não invariante de um único $A$.

**Espaço e ferramentas**: teoria de Tomita–Takesaki (teoria modular de álgebras de von Neumann), replica trick contínuo, geometria de Nielsen de complexidade de circuitos, geometria de informação de Fisher–Bures.

**Ponto cego resolvido**: Álgebra linear clássica não tem noção de **emaranhamento** porque nunca decompõe $A$ como estado bipartido — isso exige reinterpretar o objeto categoricamente, não apenas aplicar mais análise. "Complexidade = Volume" é ainda mais radical: não é invariante de $A$, é uma **métrica no espaço dos tensores**, medindo dificuldade de alcançar $A$ a partir de uma referência — uma questão dinâmica/informacional estranha à pergunta estática "quais são os invariantes de $A$" que organiza toda a Vol. I–II.

**Viabilidade e encaixe**: Ambicioso e tecnicamente pesado (exige provar que $K_A\mapsto \rho_{\Omega_1}$ está bem posto, positividade, etc.), mas é exatamente o tipo de salto que justifica um volume próprio. **Recomendo como espinha dorsal de Beyond the Spectrum III** — não um capítulo entre outros, mas o motivo de existir do volume, com os itens 1–3 acima como núcleo demonstrável e o item 4 (complexidade) como capítulo mais especulativo/programático ao final.

---

## 6. Termodinâmica Fora do Equilíbrio e Geometria Estocástica

**Nome formal**: *Comprimento termodinâmico $\mathcal L(A,B)$ via igualdade de Jarzynski.*

**Definição**: Considere um caminho $A_s$, $s\in[0,1]$, de $A_0=A$ a $A_1=B$, e a dinâmica de Langevin sob o potencial deformante $V_{A_s}=-\log\Phi(A_s)$:
$$dX_t = -\nabla V_{A_{s(t)}}(X_t)\,dt + \sqrt2\,dW_t.$$
O trabalho estocástico é $W[X_\cdot] := \int_0^\tau \partial_s V_{A_{s(t)}}(X_t)\,\dot s(t)\,dt$, e a igualdade de Jarzynski dá o invariante de **energia livre relativa**, independente do protocolo:
$$\Delta F(A,B) := -\log\langle e^{-W}\rangle = -\log(Z_B/Z_A).$$
No limite de condução lenta, a dissipação mínima esperada sobre todos os protocolos que ligam $\mu_A$ a $\mu_B$ é dada pelo **comprimento termodinâmico**
$$\mathcal L(A,B)^2 \propto \lim_{\tau\to\infty} \tau\cdot\langle W\rangle_{\min} = \tfrac12 \mathcal W_2(\mu_A,\mu_B)^2$$
(resultado de Sivak–Crooks / Aurell et al.) — ou seja, **o transporte ótimo $W_2$ que vocês já formalizaram em Vol. II é exatamente o limite quase-estático desta nova família termodinâmica**, e $\mathcal L$ generaliza $W_2$ para protocolos a velocidade finita, com a dissipação $\langle W\rangle - \Delta F \ge 0$ (segunda lei) medindo quão longe um caminho está de ser geodésico.

**Extensão conjectural (menor confiança)**: *Expoentes de rugosidade tipo KPZ/Tracy–Widom* das flutuações da fronteira $\partial X_t(A)$ sob perturbação $A\to A+\epsilon\xi$ ($\xi$ no ensemble GOE/GUE, já latente no Kac–Rice de Vol. I). Sinalizo isso explicitamente como **conjectural/em aberto** — universalidade KPZ nesse contexto exigiria um teorema novo de convergência de escala, não uma aplicação direta de maquinaria existente.

**Espaço e ferramentas**: mecânica estatística de não-equilíbrio (Jarzynski, Crooks), geometria de informação (comprimento termodinâmico de Ruppeiner/Crooks), para o item conjectural: classe de universalidade KPZ e teoria de matrizes aleatórias.

**Ponto cego resolvido**: Álgebra linear é estática — $A$ é um objeto fixo. Toda essa fronteira trata de **invariantes de transições/protocolos entre tensores**, um eixo ortogonal à pergunta "quais são os invariantes de um único $A$" que organiza Vol. I–II inteiro.

**Viabilidade e encaixe**: O comprimento termodinâmico é **altamente viável e demonstrável hoje** — teoremas já estabelecidos na literatura, conexão direta e elegante com $W_2$/LSI/Bakry–Émery já existentes, praticamente escreve-se como corolário do material de Vol. II. Recomendo como **terceiro capítulo âncora de Beyond the Spectrum III**. Já o expoente KPZ deve ir para um apêndice de "problemas em aberto", não para um teorema.

---

## Recomendação de priorização

| Prioridade | Invariante | Mudança de codomínio necessária? | Confiança de prova |
|---|---|---|---|
| **1 (âncora)** | Núcleo bipartido → modular/refletida/EW (Frente 5) | Sim ($F(\Omega)\to F(\Omega\times\Omega)$) | Média-alta, trabalho real mas doutrinado |
| **2** | $CC(\mathcal F_A)$, feixes de posto (Frente 3) | Sim (escalar → matriz-valorada) | Alta |
| **3** | Capacidades EH/HZ + espectro de Floer (Frente 1) | Não | Alta (caso convexo) |
| **4** | $\lambda_1^{(p)}(A)$ e $\delta$-hiperbolicidade (Frente 4) | Não | Muito alta |
| **5** | Comprimento termodinâmico $\mathcal L(A,B)$ (Frente 6) | Não | Muito alta |
| **6 (volume separado)** | Chern–Simons/gerbes para $k\ge3$ (Frente 2) | Sim (função → conexão) | Média, mas categoricamente distinto |
| **Apêndice em aberto** | Expoentes KPZ/Tracy–Widom (Frente 6) | — | Baixa/conjectural |

Sugestão concreta: **Beyond the Spectrum III** organiza-se em torno de 3–4 capítulos demonstráveis (5, 3, 1, 4 e/ou 6-termodinâmico), com a mudança de codomínio para núcleos bipartidos $K_A(x,y)$ como inovação estrutural central do volume — ela sozinha desbloqueia items 5.1–5.3 e torna o contorno de emaranhamento de Vol. II um corolário em vez de um postulado. A teoria de calibre de ordem superior (Frente 2) fica melhor como um **quarto tratado separado**, dedicado especificamente a $T^k(V)$ com $k\ge3$, coordenado com o Cap. 11 do livro-mestre.
