# Relatório de Auditoria Adversarial — Fase 1 & Fase 2
## *Beyond the Spectrum III: Higher Invariants, Bipartite Kernels, and Non-Equilibrium Geometry of Functional Realizations*

**Auditor:** Claude CLI (Auditor Adversarial, Protocolo Triadic Proof Verifier)
**Escopo:** OBL-001 a OBL-021, LEDGER.md v.Phase0, TeX completo (9 seções)
**Nota metodológica:** o skill `triadic-proof-verifier` falhou ao carregar (`<error>Execute skill</error>` em duas tentativas); a auditoria abaixo foi executada diretamente contra as instruções do protocolo fornecidas no prompt, sem o pipeline automatizado do skill. Recomendo investigar a falha do skill separadamente.

---

## 0. Legenda de Taxonomia

| Tag | Significado |
|---|---|
| `MATH-HYP` | Hipótese tácita, não descarregada, incompleta ou contraditória |
| `MATH-CIRC` | Circularidade, tautologia ou degenerescência de conteúdo |
| `MATH-BOUND` | Erro/imprecisão em constante, expoente ou desigualdade |
| `GEO-CONN` | Inconsistência de domínio/objeto entre seções ou entre Ledger↔TeX |
| `LEAN-VAC` | Risco de vacuidade na formalização Lean (hipóteses insatisfazíveis) |
| `PROOF-GAP` | Passo do argumento ausente ou insuficientemente justificado |

---

## 1. Sumário Executivo — Achados Críticos (ordenados por severidade)

| # | OBL | Tag | Severidade | Achado em uma linha |
|---|---|---|---|---|
| 1 | **OBL-014** | `LEAN-VAC`/`MATH-HYP` | **CRÍTICA** | Hipótese "$\ker\rho_{\Omega_1}=\{0\}$" é **impossível de satisfazer**: $\rho_{\Omega_1}$ herda posto finito $\le n$ de $K_A$ (soma de $n$ termos), logo em $L^2(\Omega_1)$ (dim. infinita) tem núcleo de codimensão $\le n$ sempre. Teorema vacuamente verdadeiro. Propaga para OBL-015, OBL-016. |
| 2 | **OBL-020** | `MATH-HYP`/`MATH-BOUND` | **ALTA** | Cota $\mathrm{reach}\ge\epsilon_0/M$ captura só a curvatura local; ignora o termo global de auto-colisão que a própria prova menciona e depois esquece. Contraexemplo padrão de "hairpin" quase-tangente derruba a cota. |
| 3 | **OBL-019** | `MATH-BOUND` | **ALTA** | Fórmula $d_s=\log N/\log(N\rho)$ está incorreta por um fator 2 e por inversão $\rho\leftrightarrow1/\rho$; falha no benchmark clássico do tapete de Sierpinski ($N=3,\rho=3/5$: previsto $\approx1.87$, valor correto $d_s=2\log3/\log5\approx1.365$). |
| 4 | **OBL-011** | `MATH-CIRC` | **ALTA** | Como $\Phi(A)$ é sempre normalizado ($\int\Phi(A)=1$), $Z(A)\equiv1$ por definição, logo $\Delta F\equiv0$ é tautológico — a identidade de Jarzynski perde seu conteúdo físico (extração de $\Delta F$ não trivial). |
| 5 | **OBL-010** | `MATH-HYP`/`MATH-BOUND` | **ALTA** | Convexidade só "no infinito" ($\|x\|\ge R_0$) é citada para justificar $CD(\kappa,\infty)$ **global**, que exige convexidade em todo $\Omega$. Taxa de convergência $\kappa$ não é justificada. |
| 6 | **OBL-018** | `PROOF-GAP` | **ALTA** | Prova atribui os polos a $\Gamma(s+\alpha_j+k)^{-1}$ — mas $1/\Gamma$ é **inteira** (tem zeros, não polos); mecanismo dos polos está descrito de forma matematicamente invertida. |
| 7 | **OBL-003** | `GEO-CONN`/`MATH-HYP` | **MÉDIA-ALTA** | Hipótese "$\Phi(A)\in C^\infty_c$" (suporte compacto) é incompatível com a convexidade estrita própria ($\nabla^2\Phi(A)\ge\mu I>0$, $\Phi(A)\to\infty$) assumida no preâmbulo da Seção 2 para o mesmo símbolo $\Phi(A)$. |
| 8 | **OBL-001** | `MATH-BOUND` | **MÉDIA** | Construção da prova (bola inscrita de raio $r^2=2(t-\min\Phi)/\lambda_{\max}$) dá $c_1^{EH}=\pi r^2=2\pi(t-\min\Phi)/\lambda_{\max}$, mas o enunciado tem $\pi(t-\min\Phi)/\lambda_{\max}$ — fator 2 ausente. |
| 9 | **OBL-004** | `PROOF-GAP` | **MÉDIA** | Transversalidade pontual a cada estrato $\mathcal R_r$ não implica Whitney (B) da estratificação puxada-atrás sem invocar o teorema de transversalidade estratificada de Mather (não citado). |
| 10 | **OBL-007** | `MATH-HYP` | **MÉDIA** | Conexidade de $\Omega$ não é hipótese explícita, mas é necessária para a unicidade do autoestado fundamental; contraexemplo trivial com duas bolas desconexas idênticas quebra a unicidade. |
| 11 | **OBL-009** | `MATH-HYP` | **MÉDIA** | Completude de $(\Omega,g_A)$ não é hipótese explícita quando $\Omega=B_1^d(0)$; sem ela, a comparação de Toponogov não garante geodésicas globais nem hiperbolicidade de Gromov uniforme. |
| 12 | **OBL-008** | `PROOF-GAP` | **MÉDIA** | Prova mostra apenas metade (a direção fácil, via coarea) do limite de Cheeger; "convergência monotônica" não é sequer endereçada. |
| 13 | **OBL-013** | `GEO-CONN` | **BAIXA-MÉDIA** | "$K_A(x,x)=\Phi_{\mathrm{scalar}}(A)(x)$" pressupõe $\{\phi_j\}$ escolhidos canonicamente para reproduzir a realização escalar dos Volumes I/II; hipótese apenas diz "família ortonormal" arbitrária. |
| 14 | **OBL-015/016** | `GEO-CONN` | **BAIXA-MÉDIA** | Aresta OBL-014→OBL-015 no DAG não é usada na prova (nunca invoca $K_{\Omega_1}$); OBL-016 importa Dutta–Faulkner sem jamais construir o dual bulk $(M,g_A)$ a partir do kernel finito $K_A$ desta seção. |
| 15 | **OBL-017** | `LEAN-VAC` (risco) | **BAIXA** | Uso de "entire" (inteira) para uma função só provada holomorfa num semiplano é terminologicamente incorreto e cria risco de predicado Lean incompatível (`Entire` vs `AnalyticOn`). |
| 16 | **OBL-002** | `PROOF-GAP` | **BAIXA** | A identidade "$c_{HZ}=\inf|\oint p\,dq|$" é tratada como definição, mas é de fato um teorema não-trivial (Ekeland–Lasry/Hofer–Zehnder) que precisa citação/prova própria. |
| 17 | **OBL-012** | `PROOF-GAP` | **BAIXA** | "Tensor de atrito $\ge$ métrica de Otto $\times\kappa/2$" é a hipótese que faz todo o trabalho do teorema e é apenas afirmada, não provada nem citada com precisão. |

---

## 2. Auditoria Detalhada por Seção

### Seção 2 — Topologia Simplética & Floer (OBL-001–003)

**OBL-001 (EH Capacity).**
- *Hipóteses tácitas:* $\lambda_{\max},\lambda_{\min}$ de $\nabla^2\Phi(A)$ não têm domínio declarado. Como só se assume $\nabla^2\Phi(A)\ge\mu I$ globalmente (sem cota superior global), $\lambda_{\max}(\nabla^2\Phi(A))$ só é finito porque $\overline{K_t(A)}$ é compacto (decorre da propriedade, não é hipótese primitiva declarada) — **`MATH-HYP`**, gap de precisão de notação.
- *Contraexemplo de escala:* $\Phi(A)(x)=\mu|x|^2/2+|x|^4$ satisfaz $\nabla^2\Phi(A)\ge\mu I$ mas tem Hessiana ilimitada em $\mathbb R^{2n}$; sem restringir o sup a $\overline{K_t(A)}$, o RHS da desigualdade é trivialmente $\infty$.
- *Erro de constante (`MATH-BOUND`):* a bola inscrita construída na própria prova tem raio $r=\sqrt{2(t-\min\Phi(A))/\lambda_{\max}}$, logo $c_1^{EH}(E_{\text{in}})=\pi r^2=\dfrac{2\pi(t-\min\Phi(A))}{\lambda_{\max}}$ — o enunciado tem $\dfrac{\pi(t-\min\Phi(A))}{\lambda_{\max}}$, **fator 2 ausente** (e simetricamente no lado superior).
- **Patch mínimo:** (i) definir $\lambda_{\max}:=\sup_{x\in\overline{K_t(A)}}\lambda_{\max}(\nabla^2\Phi(A)(x))$, $\lambda_{\min}:=\inf_{x\in\overline{K_t(A)}}\lambda_{\min}(\nabla^2\Phi(A)(x))$ explicitamente; (ii) corrigir a constante para $2\pi(\cdot)$ em ambos os lados, ou verificar/citar explicitamente a normalização de $c_1^{EH}(B(r))$ usada (se $=\tfrac12\pi r^2$ resolve, declarar essa convenção).

**OBL-002 (HZ Invariance).**
- A igualdade "$c_{HZ}(K_t(A)) = \inf_\gamma|\oint_\gamma p\,dq|$" é apresentada implicitamente como definição, mas é o **teorema de Ekeland–Lasry/Hofer–Zehnder** para corpos estritamente convexos (não trivial, requer regularidade do bordo e a teoria de min-max de Hofer–Zehnder). A prova só estabelece a invariância do espectro de ação sob $\psi$ (trivial), não a identidade em si. **`PROOF-GAP`**.
- **Patch:** citar explicitamente Hofer–Zehnder (1994), Ch. 3–4, ou Ekeland–Lasry (1980), e separar em dois lemas: (a) identidade capacidade↔ação mínima (citação), (b) invariância do espectro de ação (prova atual).

**OBL-003 (Viterbo Lipschitz).**
- **`GEO-CONN` crítico:** hipótese "$\Phi(A),\Phi(B)\in C^\infty_c(\mathbb R^{2n})$" (suporte compacto) é **incompatível** com a suposição de convexidade estrita própria feita no preâmbulo da Seção 2 ($\nabla^2\Phi(A)\ge\mu I>0$ em todo $\mathbb R^{2n}$, $\Phi(A)\to\infty$) para o mesmo símbolo $\Phi(A)$: uma função de suporte compacto não pode ter Hessiana positiva-definida em todo o espaço. Se o LEDGER trata `variables` de Seção 2 como compartilhadas, o conjunto de hipóteses do OBL-003 é **vazio** — risco `LEAN-VAC`.
- A hipótese disjuntiva alternativa "quadratic convex growth at infinity" não é tratada na prova (que só usa mapas de continuação de Floer, técnica-padrão para Hamiltonianos que coincidem fora de compacto — não cobre diretamente o ramo de crescimento quadrático, que tipicamente requer a maquinaria de funções geradoras de Viterbo).
- **Patch:** introduzir um símbolo distinto (e.g. $h_A := \Phi(A) - \Phi(A)|_{x_0}$ regularizado, ou declarar $\Phi(A)$ de Seção 2/OBL-003 como *não* o mesmo objeto do preâmbulo) e provar (ou citar) separadamente o caso de crescimento quadrático via funções geradoras.

---

### Seção 3 — Feixes Microlocais & Ciclos Característicos (OBL-004–006)

**OBL-004 (Whitney Rank Stratification).**
- **`PROOF-GAP`:** transversalidade pontual de $\Phi(A)$ a cada $\mathcal R_r$ dá que $\Sigma_r(A)$ é submersão local (teorema da pré-imagem), mas **não implica automaticamente** a condição de Whitney (B) da estratificação puxada-atrás — isso requer o teorema de transversalidade estratificada de Mather (compatibilidade com os dados de controle da estratificação-alvo, i.e. condição $(a_f)$ de Thom), não citado. Além disso "Thom's transversality theorem" é citado incorretamente — o teorema usado de fato é o teorema da pré-imagem/submersão, não o teorema de genericidade de Thom.
- *Colapso dimensional ($n=1$):* $\mathrm{Sym}_1(\mathbb R)=\mathbb R$; codimensões $\binom{n-r+1}{2}$ dão $0$ (r=1) e $1$ (r=0) — consistente, sem erro aqui, serve como checagem de sanidade positiva.
- **Patch:** citar Mather (*Notes on Topological Stability*) ou Gibson et al. (*Topological Stability of Smooth Mappings*) para a transversalidade estratificada completa; renomear a citação de "Thom's transversality theorem" para "preimage/submersion theorem".

**OBL-005 (Microsupport Lagrangian).**
- O teorema de involutividade de Kashiwara–Schapira dá $SS(\mathcal F_A)$ Lagrangiano (correto, geral), mas a **igualdade** $SS(\mathcal F_A)=\bigcup\overline{T^*_{\Sigma_r(A)}\Omega}$ (não apenas $\subseteq$) exige que a estratificação $\Sigma_\bullet(A)$ seja exatamente adaptada a $\mathcal F_A$ (sem "saltos" micro-locais dentro de um estrato) — não justificado. **`MATH-HYP`**.
- **Patch:** provar/citar que $\mathcal F_A$ é localmente constante em cada $\Sigma_r(A)$ (constructibilidade fina), ou enfraquecer a conclusão para $\subseteq$.

**OBL-006 (Kashiwara Index).**
- Herda a lacuna de OBL-005 via `GEO-CONN`: a fórmula $CC(\mathcal F_A)=\sum_r m_r[\overline{T^*_{\Sigma_r}\Omega}]$ pressupõe a decomposição exata de OBL-005. Teorema do índice em si (Kashiwara 1973/1985) está corretamente citado.

---

### Seção 4 — Geometria Métrica & Espectral Não-Linear (OBL-007–009)

**OBL-007 ($p$-Laplaciano Minimax).**
- **`GEO-CONN`:** LEDGER exige $\partial\Omega\in C^{1,1}$; TeX (preâmbulo Seção 4) diz apenas "bounded Lipschitz domain" — inconsistência documental.
- **`MATH-HYP` faltante:** conexidade de $\Omega$ não é hipótese, mas é **necessária** para "único a menos de escalar". *Contraexemplo de colapso*: $\Omega=B_r(0)\sqcup B_r(3e_1)$ (duas bolas idênticas desconexas), $\Phi(A)\equiv1$ — dois minimizadores linearmente independentes (um em cada bola, zero na outra) atingem o mesmo $\lambda_1^{(p)}$, violando unicidade.
- **Patch:** adicionar "$\Omega$ conexo" às hipóteses explícitas (Ledger + TeX) e harmonizar regularidade de bordo entre Ledger/TeX.

**OBL-008 (Cheeger $p\to\infty$).**
- **`PROOF-GAP`:** a prova mostrada só estabelece (esboçadamente) $\liminf(\lambda_1^{(p)})^{1/p}\ge h(A)$ via coarea; a direção difícil $\limsup\le h(A)$ (construção de funções teste quase-ótimas a partir do conjunto de Cheeger ótimo) está totalmente ausente, e **"convergência monotônica"** não tem nenhum argumento correspondente.
- **Patch:** adicionar lema de aproximação Lipschitz do conjunto de Cheeger ótimo para a direção $\limsup$, e lema de monotonicidade separado (via desigualdade de Hölder em $p$ para o quociente de Rayleigh).

**OBL-009 (Gromov Hiperbolicidade).**
- **`MATH-HYP` crítico ausente:** completude de $(\Omega,g_A)$ não é hipótese quando $\Omega=B_1^d(0)$ ("or complete simply connected domain" sugere que o primeiro ramo não precisa ser completo). Sem completude, o teorema de Cartan–Hadamard/comparação de Toponogov usado na prova não garante geodésicas minimizantes globais nem hiperbolicidade uniforme.
- *Contraexemplo estrutural:* $\Phi(A)\equiv1$ dá $g_A=\delta_{ij}$ plana (curvatura $0$, não $\le-\kappa_0$) em $B_1^d(0)$ — mostra que atingir a hipótese de curvatura força $\Phi(A)\to\infty$ perto do bordo (modelo tipo disco de Poincaré); se essa explosão não for controlada para dar completude, o conjunto $(\Omega,g_A)$ pode ter geodésicas que "escapam" antes de conectar pontos, invalidando a comparação de triângulos usada.
- **Patch:** adicionar hipótese explícita "$(\Omega,g_A)$ completo e geodésico" (ou provar que $\mathrm{Sec}(g_A)\le-\kappa_0<0$ + $\Phi(A)\to\infty$ em $\partial\Omega$ com taxa suficiente implica completude — lema à parte).

---

### Seção 5 — Termodinâmica Fora do Equilíbrio (OBL-010–012)

**OBL-010 (Langevin Ergodicidade).**
- **`MATH-HYP`/`MATH-BOUND`:** hipótese é convexidade **apenas no infinito** ($\nabla^2V_A\ge\kappa I$ para $\|x\|\ge R_0$), mas a prova invoca $CD(\kappa,\infty)$ de Bakry–Émery, que exige a cota **globalmente**, e conclui convergência exponencial em $\mathcal W_2$ via Otto–Villani (que precisa do log-Sobolev global correspondente). Isso é um salto teórico não-trivial — para hipóteses "convexo no infinito" a ferramenta correta é acoplamento por reflexão (Eberle 2016) ou o critério de Lyapunov de Bakry–Émery–Wang, que dão uma taxa de convergência **diferente** de $\kappa$ (dependente também do comportamento em $\{\|x\|<R_0\}$).
- **Patch:** substituir a citação por Eberle (*Reflection couplings and contraction rates for diffusions*, 2016) ou Cattiaux–Guillin (critério de Lyapunov), e reescrever a taxa de convergência em termos dos parâmetros corretos (não apenas $\kappa$).

**OBL-011 (Jarzynski).**
- **`MATH-CIRC` crítico:** como $\Phi(A)$ é sempre normalizado por hipótese estrutural da Seção 5 ($\int_\Omega\Phi(A)=1$), $Z(A)=Z(B)=1$ **por definição**, tornando $\Delta F\equiv0$ tautológico — sem qualquer uso da dinâmica. Isso esvazia o propósito físico do teorema de Jarzynski (extrair $\Delta F$ não-trivial de flutuações fora do equilíbrio). Em Lean, isso é um risco `LEAN-VAC` real: a parte "$e^{-\Delta F}=Z(B)/Z(A)=1$" é demonstrável por álgebra pura da hipótese de normalização, sem tocar o SDE/Girsanov — um formalizador poderia (erroneamente) provar o enunciado inteiro ignorando a dinâmica, mascarando a ausência de uma prova genuína de $\mathbb E_{\mu_A}[e^{-W}]=1$.
- **Patch:** reformular com $\Phi(A)$ **não-normalizado**: $\tilde\Phi(A)(x)=e^{-\tilde V_A(x)}$ com $\tilde V_A$ livre de constante aditiva, definir $Z(A)=\int e^{-\tilde V_A}\,dx$ genuinamente não-trivial, e provar $\Delta F(A,B)=-\log(Z(B)/Z(A))\ne0$ em geral — restaurando o conteúdo do teorema.

**OBL-012 (Comprimento Termodinâmico vs $\mathcal W_2$).**
- Consistência interna checada: $\frac12\mathcal L^2\ge\frac\kappa4\mathcal W_2^2 \iff \mathcal L^2\ge\frac\kappa2\mathcal W_2^2$, que bate com a prova (sem erro de constante aqui, ao contrário de OBL-001).
- **`PROOF-GAP` central:** a afirmação-chave "o tensor de atrito é limitado inferiormente pela métrica de Otto–Wasserstein vezes $\kappa/2$" é o único passo que faz o teorema funcionar e é **apenas afirmada**, sem prova nem citação de um teorema nomeado (ao contrário de Bakry–Émery ou Otto–Villani, citados noutros lugares). É tema de pesquisa em aberto/heurística física (Sivak–Crooks), não teorema rigoroso estabelecido.
- Herda `GEO-CONN` de OBL-010 (o $\kappa$ usado aqui é o mesmo $\kappa$ cuja justificativa em OBL-010 é falha).
- **Patch:** ou (a) rebaixar para "conjectura"/hipótese explícita rotulada, ou (b) provar a desigualdade de dominação do tensor de atrito via uma desigualdade de Poincaré explícita relacionando $g_{jk}$ ao gerador $L_A$, citando literatura rigorosa (e.g. resultados de Chen–Sheu ou similares sobre comprimento termodinâmico e transporte).

---

### Seção 6 — Kernel Bipartido & Holografia (OBL-013–016)

**OBL-013 (Kernel PSD).**
- Prova algébrica está correta e completa para o kernel de posto finito $n$.
- **`GEO-CONN`:** "$K_A(x,x)=\Phi_{\mathrm{scalar}}(A)(x)$" pressupõe $\{\phi_j\}$ escolhidos canonicamente para casar com a realização escalar de Vol. I/II — mas a hipótese diz apenas "família ortonormal" **arbitrária**. Para $\{\phi_j\}$ genérico, a diagonal $\sum\lambda_j|\phi_j(x)|^2$ não coincide com um alvo pré-especificado sem uma construção inversa explícita (problema espectral inverso não trivial, nem sempre solúvel).
- **Patch:** ou definir $\Phi_{\mathrm{scalar}}(A)$ **como** essa diagonal (invertendo a direção lógica do enunciado), ou provar um lema de existência de $\{\phi_j\}$ ortonormais reproduzindo um alvo positivo dado com $\int=\mathrm{Tr}(A)$.

**OBL-014 (Hamiltoniano Modular).**  ⚠️ **Achado central da auditoria**
- **`LEAN-VAC` / `MATH-HYP` — hipótese insatisfazível.** $K_A$ é construído em OBL-013 como soma de **$n$** termos ($n=\dim A$), logo $\mathrm{rank}(K_A)\le n$; o traço parcial $\rho_{\Omega_1}$ só pode **diminuir ou manter** o posto: $\mathrm{rank}(\rho_{\Omega_1})\le n$. Mas $L^2(\Omega_1)$ é de dimensão infinita, então qualquer operador de posto $\le n$ tem núcleo de **codimensão $\le n$** — em particular $\ker(\rho_{\Omega_1})\ne\{0\}$ **sempre**. A Hipótese 4 do OBL-014 ("$\ker(\rho_{\Omega_1})=\{0\}$") é, portanto, **impossível de satisfazer** dado o restante da construção. O teorema é vacuamente verdadeiro — exatamente o padrão de anti-vacuidade que a Fase 1 deve capturar.
- Consequência adicional: mesmo relaxando a hipótese, $K_{\Omega_1}=-\log\rho_{\Omega_1}$ não está bem definido no núcleo ($-\log 0=+\infty$), então "espectro discreto" está mal-formulado — o operador teria, no melhor caso, um subespaço próprio de autovalor $+\infty$ (não discreto no sentido usual).
- **Impacto no DAG:** compromete diretamente OBL-015 e OBL-016 (dependentes declarados).
- **Patch construtivo:** (i) generalizar $K_A$ para um núcleo de posto genuinamente infinito (soma infinita/operador trace-class de espectro cheio) na definição de OBL-013, **ou** (ii) reformular OBL-014 restringindo $K_{\Omega_1}$ ao complemento ortogonal de $\ker\rho_{\Omega_1}$ (subespaço de dimensão $\le n$) e trocando "espectro discreto acumulando em $+\infty$" por "espectro discreto de no máximo $n$ autovalores finitos, mais um subespaço de dimensão infinita formalmente associado a $+\infty$ (grau de liberdade "congelado")".

**OBL-015 (Entropia Refletida).**
- Não afetada estruturalmente pela lacuna de posto finito (entropia de estado de posto finito está bem definida).
- **`GEO-CONN`:** a prova nunca invoca $K_{\Omega_1}$ apesar da dependência declarada OBL-014→OBL-015 no DAG — aresta possivelmente espúria, ou prova incompleta (deveria conectar $\sigma_{11^*}$ à teoria modular via $K_{\Omega_1}$ e não o faz).
- **Patch:** remover a aresta do DAG se de fato desnecessária, ou completar a prova conectando purificação canônica à teoria modular.

**OBL-016 (Desigualdade Holográfica EW).**
- **`GEO-CONN` severo:** o "bulk" $(M,g_A)$ satisfazendo RT/NEC é **postulado** nas hipóteses, mas nada nas Seções 5–6 **constrói** esse dual a partir do kernel finito $K_A$ desta seção. O teorema, como está, apenas reimporta o resultado de Dutta–Faulkner sob um novo rótulo ($S_R$ desta seção), sem provar que o $S_R$ definido em OBL-015 (via GNS/traço parcial do kernel finito) coincide com a entropia refletida de uma CFT de bordo dual a $(M,g_A)$.
- **Patch:** ou (a) explicitar que OBL-016 é condicional/axiomático ("assumindo a existência de um dual holográfico clássico satisfazendo RT..."), rotulando-o como corolário físico-motivado e não teorema matemático pleno, ou (b) construir explicitamente o mapa $A\mapsto(M,g_A)$ e provar as propriedades necessárias.

---

### Seção 7 — Pascal Simplex & Resíduos de Barnes–Kigami (OBL-017–019)

**OBL-017 (Mellin Simplicial).**
- Prova de holomorfia correta em conteúdo, mas **terminologia incorreta**: "entire" (inteira) é usado para uma função só estabelecida holomorfa num semiplano $\mathrm{Re}(s)>-\min\alpha_i$ — termos contraditórios (uma função inteira não tem polos em lugar nenhum de $\mathbb C$; OBL-018, na sequência imediata, prova que $\mathcal Z_A$ **tem** polos). Numericamente os polos ficam fora do semiplano aberto declarado (consistente), mas a palavra "entire" é objetivamente errada e cria risco `LEAN-VAC` se portada literalmente (predicado `Entire`/`AnalyticOnNhd Set.univ` do Mathlib seria **falso**, forçando ou um `sorry` disfarçado ou uma reformulação silenciosa que diverge do TeX).
- **Patch:** trocar "entire holomorphic function... in the right half-plane" por "holomorphic on $\{\mathrm{Re}(s)>-\min_i\alpha_i\}$".

**OBL-018 (Continuação Meromórfica / Polos de Barnes).**
- **`PROOF-GAP` sério:** a prova afirma que "as contribuições singulares se reduzem a polos de gama $\Gamma(s+\alpha_j+k)^{-1}$" — mas $1/\Gamma(z)$ é **função inteira** (zeros em $z=0,-1,-2,\dots$, sem polos!). O mecanismo correto de polos numa transformada de Mellin–Barnes vem de $\Gamma(s+\alpha_j+k)$ **sem** o inverso (que tem polos simples em $s+\alpha_j+k=0,-1,-2,\dots$), tipicamente via a função Beta multivariada $B(s+\alpha_j,\ldots)$. Como escrito, o argumento está matematicamente invertido.
- **Patch:** reescrever a prova citando a expansão em série de Taylor de $\Phi(A)$ nos vértices combinada com a fórmula integral de Barnes para a função Beta $B(\cdot,\cdot)$ (cujo numerador $\Gamma$ produz os polos corretos), não $1/\Gamma$.

**OBL-019 (Dimensão Espectral de Kigami).**
- **`MATH-BOUND` — checagem numérica falha.** Fórmula proposta: $d_s=\dfrac{\log N}{\log(N\rho)}$. Fórmula clássica de Kigami (verificável no tapete de Sierpinski, $N=3$, fator de escala de resistência $r=5/3$, i.e. $\rho:=1/r=3/5\in(0,1)$ como na hipótese do Ledger): $d_s=\dfrac{2\log N}{\log(N/\rho)}$, dando $d_s=2\log3/\log5\approx1.365$ (valor bem estabelecido na literatura). A fórmula do manuscrito dá $\log3/\log(3\times0.6)=\log3/\log1.8\approx1.869$ — **discrepância dupla**: falta o fator $2$ no numerador **e** $\rho$ aparece multiplicando $N$ em vez de dividindo.
- **Patch:** corrigir para $s_0=-\dfrac{d_s}2=-\dfrac{\log N}{\log(N/\rho)}$ (equivalente a $d_s=2\log N/\log(N/\rho)$), e adicionar uma verificação explícita com o exemplo do tapete de Sierpinski como teste de regressão no Lean/numérico.

---

### Seção 8 — Alcance de Federer & Eixo Medial (OBL-020–021)

**OBL-020 (Cota do Reach via Hessiana).**
- **`MATH-HYP`/`MATH-BOUND` crítico.** A própria prova reconhece que $\mathrm{reach}=\min(1/\kappa_{\max}, \tfrac12\cdot\text{dist. de auto-colisão global})$, mas só estima o termo de curvatura local ($1/\kappa_{\max}\le M/\epsilon_0$) e **nunca** controla o termo global — apesar de mencioná-lo explicitamente na frase anterior à conclusão.
- **Contraexemplo padrão ("hairpin" quase-tangente):** em $\mathbb R^2$, tome $\Sigma_t$ como uma curva em forma de U muito alongada e fina, com curvatura uniformemente pequena e fixa ao longo de todo o comprimento (logo $M/\epsilon_0$ pequeno, dando cota inferior grande via a fórmula do teorema), mas cujos dois "braços" paralelos se aproximam a uma distância euclidiana $w\to0$ arbitrariamente pequena enquanto o comprimento de arco entre pontos correspondentes permanece grande. O reach real é $\approx w/2\to0$, **violando** a cota $\mathrm{reach}\ge\epsilon_0/M$ para $w$ suficientemente pequeno com $\epsilon_0/M$ fixo.
- **Patch:** adicionar hipótese global explícita — e.g. $\Sigma_t=\partial\Omega'$ com $\Omega'$ estritamente convexo (excluindo hairpins), ou uma cota adicional do tipo "distância de dupla-normal" $\ge d_0$, ou simplesmente renomear a conclusão para "raio de curvatura" em vez de "reach de Federer" se a intenção era apenas o resultado local.

**OBL-021 (Volume do Tubo).**
- Autocontido em relação a OBL-020 (toma $R_t>0$ diretamente como hipótese, não re-deriva de OBL-020) — não propaga o erro acima automaticamente, mas a dependência declarada no DAG (OBL-020→OBL-021) fica **enfraquecida na prática**: se OBL-020 não estabelece $R_t>0$ de forma confiável, OBL-021 precisa assumir $R_t>0$ como hipótese primitiva independente (o que já faz), tornando a aresta do DAG mais fraca do que sugere ("usa a *conclusão* de OBL-020" vs. "assume a *mesma hipótese de conclusão*" diretamente).
- Fórmula de Weyl–Federer em si: correta e bem citada, sem erro encontrado.
- **Patch:** anotar no DAG que a dependência OBL-020→OBL-021 é condicional à correção de OBL-020, e no meio tempo declarar $R_t>0$ como hipótese independente e verificável separadamente (já é o caso na prática — apenas tornar isso explícito no texto).

---

## 3. Tabela de Impacto no DAG (propagação de falhas)

| Nó com defeito | Nós afetados a jusante | Severidade da propagação |
|---|---|---|
| OBL-014 (vacuidade) | OBL-015, OBL-016 | Alta — 3/21 obrigações (14%) comprometidas |
| OBL-005 (igualdade não provada) | OBL-006 | Média |
| OBL-010 ($CD(\kappa,\infty)$ mal-justificado) | OBL-012 | Alta — constante $\kappa$ usada indevidamente |
| OBL-020 (cota local apenas) | OBL-021 (aresta enfraquecida, não quebrada) | Baixa |
| OBL-011 (tautologia) | — (terminal na prática, mas mina a narrativa de Seção 5) | Média |

---

## 4. Resumo de Risco `LEAN-VAC` (anti-vacuidade)

| OBL | Assinatura Lean | Risco | Motivo |
|---|---|---|---|
| `OBL-014` | `modular_hamiltonian_density` | **Alto** | Hipótese `ker ρ = ⊥` insatisfazível com `K_A` de posto finito ⇒ provável por `exact absurd` a partir das hipóteses, sem conteúdo. |
| `OBL-003` | `viterbo_spectral_lipschitz` | **Médio** | Se as `variables` de Seção 2 forem compartilhadas, hipóteses de convexidade própria + suporte compacto podem ser conjuntamente vazias. |
| `OBL-011` | `jarzynski_free_energy_id` | **Médio** | Metade do enunciado (`Z(B)/Z(A)=1`) é demonstrável só por álgebra da normalização, sem tocar o SDE — risco de "prova" que não exercita a dinâmica alegada. |
| `OBL-017` | `simplicial_mellin_transform` | **Baixo** | Divergência de predicado (`Entire` vs. holomorfia local) pode forçar enunciado Lean mais fraco (ou falso) silenciosamente. |

---

## 5. Recomendações para Fase 3 (ordem de prioridade sugerida)

1. **OBL-014** — redesenhar a construção do kernel (posto infinito) ou reformular a hipótese/conclusão do Hamiltoniano modular. Bloqueador para OBL-015/016.
2. **OBL-019** — corrigir a fórmula da dimensão espectral com verificação contra o benchmark de Sierpinski.
3. **OBL-020** — adicionar hipótese global de não-auto-aproximação ou renomear a conclusão.
4. **OBL-011** — dessnormalizar $\Phi(A)$ para restaurar conteúdo físico não-trivial.
5. **OBL-010/012** — trocar Otto–Villani por Eberle/Bakry–Émery–Wang com Lyapunov; revisar constante $\kappa$ propagada a OBL-012.
6. **OBL-018** — corrigir o mecanismo de polos ($\Gamma$ vs. $1/\Gamma$).
7. **OBL-001** — corrigir fator 2 e domínio de $\lambda_{\max},\lambda_{\min}$.
8. **OBL-003** — resolver a contradição de hipóteses (suporte compacto vs. convexidade própria).
9. **OBL-004, OBL-005, OBL-007, OBL-009** — fechar lacunas de hipóteses (Mather transversality, igualdade de micro-suporte, conexidade de $\Omega$, completude de $(\Omega,g_A)$).
10. **OBL-013, OBL-015, OBL-016, OBL-002, OBL-008, OBL-017, OBL-021** — patches menores de precisão/terminologia/citação listados acima.

---

*Fim do relatório Fase 1 + Fase 2. Pronto para orientar os patches cirúrgicos da Fase 3 do protocolo Triadic Proof Verifier.*
