## Auditoria Adversarial — Capítulo 13 (Assinaturas Observacionais)

Revisei diretamente o `.tex` e o `.lean`, refazendo os cálculos-chave (não apenas lendo os certificados pré-existentes no sandbox, que reivindicam PASS). Encontrei três falhas que impedem aprovação.

### OBL-C13-001 — Dispersão de grávitons

**Verificação positiva:** refiz a integral do heat kernel por completamento de quadrado,
$$P(\tau)=\frac{1}{16\pi^2}\int_0^\infty u\,e^{-\tau u-\tau\ell_P^2u^2}\dif u = \frac{1}{32\pi^2\ell_P^2\tau}\big[1-\sqrt\pi\,z\,e^{z^2}\operatorname{erfc}(z)\big],$$
e confirmei que bate exatamente com Eq. (heat_kernel_exact). Também derivei $d_s(\tau)=-2\,d\ln P/d\ln\tau$ de forma independente e obtive
$$d_s(\tau)=1-2z^2+\big[1-\sqrt\pi z e^{z^2}\operatorname{erfc}(z)\big]^{-1},$$
idêntico à Eq. (ds_tau). Os limites $d_s\to2$ ($\tau\to0$) e $d_s\to4$ ($\tau\to\infty$) também se confirmam via as expansões de erfc citadas — o cancelamento "$-2z^2$ contra $2z^2+3+O(z^{-2})$" está correto.

**Falha:** o texto afirma que o símbolo de Lifshitz "herdado" é $\omega^2=k^2+\ell_P^2k^4=k^2(1+\ell_P^2k^2)$, que implica $\xi=1$. Mas a Eq. (dispersion) declara $\xi=1/2$ sem nenhum passo intermediário que explique o fator $1/2$. Não há renormalização, média, ou identificação explícita conectando o símbolo de Lifshitz bruto ao valor $\xi=1/2$ usado em todas as previsões subsequentes (incluindo a fórmula de $\Delta t_{\mathrm{disp}}$, cuja álgebra de $v_g$ e $\Delta t$ confirmei estar correta *dado* $\xi$). Isso é uma lacuna de derivação não descartada — viola a exigência de "hypothesis discharge for every theorem/lemma application" do CLAUDE.md.

### OBL-C13-002 — Running do tilt tensorial CMB

**Falha estrutural mais grave do capítulo.** A Eq. do Padé $d_s(k)=2+\dfrac{2}{1+(k/M_P)}$ é apresentada como aproximação de dois pontos derivada de $d_s(\tau)$ sob $\tau=1/k^2$. Mas os limites por si só (dois pontos) não fixam unicamente uma função — e a escolha feita **não reproduz o comportamento assintótico correto** da fórmula exata:

- Do $d_s(\tau)$ exato (calculado acima), no regime IR relevante para CMB ($k\to0$, $z\to\infty$): $d_s(k)-4 = O(z^{-2}) = O\big((k/M_P)^2\big)$ — **correção quadrática**.
- Do Padé usado no artigo: $d_s(k)-4 = -2(k/M_P)/(1+k/M_P) \approx -2(k/M_P)$ para $k\ll M_P$ — **correção linear**.

Linear ≠ quadrático. Isso não é um detalhe estético: $\alpha_t(k)=\tfrac12(d_s(k)-4)$ alimenta diretamente a forma e a localização da "inflexão ascendente" em $\ell\gg1500$ reivindicada como assinatura observável para LiteBIRD/CMB-S4. Usar uma interpolação com taxa de decaimento errada no regime observacionalmente relevante invalida a previsão quantitativa (posição do multipolo, magnitude de $\sigma(r)$) mesmo que a álgebra de $\alpha_t(k)=-1/(1+(k/M_P)^{-1})$ esteja internamente consistente com o Padé escolhido.

### OBL-C13-003, OBL-C13-004, OBL-C13-005

Estas obrigações são majoritariamente qualitativas/fenomenológicas e dependem de "Teorema 7.1" e "Teorema 4.1" de `silvafilho2026grand`, um tratado companion **não incluído nesta auditoria**. Não há circularidade lógica interna visível nem inconsistência dimensional nas fórmulas apresentadas ($g^{\mathrm{FS}}_{ij}$, $F(t)$, $\Delta\Phi$), mas a prova não é autocontida — repousa em teoremas externos não verificados neste escopo. Isso é aceitável para uma "Letter" de física, mas não para um selo de auditoria formal completa.

### Módulo Lean 4 — falha crítica de integridade formal

Este é o ponto mais sério. **Todos os seis teoremas em `ExperimentalSignatures.lean` são vacuamente triviais**: cada `structure` inclui como campo de hipótese exatamente a conclusão que o teorema declara provar, e a prova é `exact` da própria hipótese (ex.: `h_xi : xi_parameter = 0.5` é assumido, e o teorema "prova" `xi_parameter = 0.5`). Isso é a tautologia $A\Rightarrow A$, repetida seis vezes. Nenhuma das fórmulas matemáticas reais do capítulo — a integral do heat kernel, a assíntota de erfc, $d_s(\tau)$, o Padé, $\Delta t_{\mathrm{disp}}$ — está codificada ou verificada em Lean. O rótulo "Zero Sorry, Zero Axiom Cheating" é tecnicamente verdadeiro mas enganoso: não há `sorry` porque não há nada não-trivial a provar. Isso não constitui verificação formal do conteúdo matemático do capítulo, apenas checagem de tipos de booleanos/floats desacoplados da física.

Observo que certificados pré-existentes no sandbox (`PROOF_AUDIT_CHAP13_FINAL.md`, `AUDIT_CHAP13_CERTIFICATE.md`) reivindicam PASS — minha auditoria independente diverge desse resultado por razões concretas e reproduzíveis acima.

---

**VERDICT: REVISE**

Pontos exatos a corrigir antes de nova submissão:

1. **OBL-C13-001**: Derivar explicitamente $\xi=1/2$ a partir do símbolo de Lifshitz $\omega^2=k^2(1+\ell_P^2k^2)$ (que dá $\xi=1$ nu), ou corrigir o símbolo/a equação de dispersão para que sejam mutuamente consistentes. Não deixar o fator $1/2$ sem origem rastreável.
2. **OBL-C13-002**: Substituir o Padé $d_s(k)=2+2/(1+k/M_P)$ por uma interpolação cuja expansão IR reproduza a taxa quadrática $O((k/M_P)^2)$ derivada rigorosamente de $d_s(\tau)$ sob $\tau=1/k^2$ — ou, alternativamente, apresentar $\alpha_t(k)$ diretamente da substituição exata em $d_s(\tau)$ sem introduzir uma aproximação com assíntota incorreta. Refazer a previsão numérica de $\ell$ e $\sigma(r)$ com a forma corrigida.
3. **Lean 4**: Reescrever `ExperimentalSignatures.lean` para formalizar de fato as obrigações matemáticas centrais (ao menos a identidade fechada da integral do heat kernel Eq. (heat_kernel_exact) e os limites assintóticos de $d_s(\tau)$ em Eq. (ds_limits), que são as únicas partes deste capítulo genuinamente demonstráveis em Lean com `Real`/`Mathlib.Analysis.SpecialFunctions.Gaussian` e `erfc`). Estruturas com hipótese = conclusão devem ser eliminadas; se uma obrigação é puramente fenomenológica/empírica (OBL-C13-003/004/005) e não demonstrável formalmente, isso deve ser declarado explicitamente como tal em vez de embrulhado em um "theorem" vazio.
4. Anexar explicitamente a dependência de OBL-C13-003–005 em teoremas do tratado companion como hipóteses externas não verificadas neste módulo, para não implicar prova autocontida.