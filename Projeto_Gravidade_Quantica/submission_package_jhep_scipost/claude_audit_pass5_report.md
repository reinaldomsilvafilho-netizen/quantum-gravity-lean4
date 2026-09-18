# Auditoria Adversarial — Rodada 5 (Pass 5 / Final Acceptance Gate)

## 1. Assinatura, Wick e o Problema do Fator Conformal (Remark 1.1)

**Veredito: não resolvido em substância — apenas reformulado.**

A alegação central é:

> "$\|\II_g\|_{\mathrm{op}} \le \ell_P^{-1}$ restringe o gradiente conformal $|\nabla \ln \Omega| \le \ell_P^{-1}$, prevenindo colapso métrico singular e garantindo que $\mathcal{S}_{\mathrm{univ}}$ seja estritamente coercivo."

Isso contém um **erro de categoria não corrigido**, o mesmo apontado na Rodada 4 com um verniz retórico novo:

- $\II_g$ é a segunda forma fundamental de uma **hipersuperfície embutida** (depende de uma folheação escolhida $\Sigma_t \hookrightarrow \mathcal{M}$) — um objeto tensorial extrínseco de codimensão 1.
- $\Omega$ é um **fator de reescala conformal do bulk** $g_{\mu\nu} \to \Omega^2 \bar g_{\mu\nu}$ — um campo escalar intrínseco definido em toda a variedade 4D, independente de qualquer folheação.
- Nenhuma aplicação, mapa ou desigualdade é construída conectando essas duas estruturas. A frase "isso restringe o gradiente conformal" é uma *asserção*, não uma dedução — não há uma única linha de prova entre a Eq. \eqref{eq:minimax_bound_def} e a alegada cota em $\nabla\ln\Omega$.

Mesmo **concedendo** essa conexão não-provada, o mecanismo proposto ainda não resolve o problema GHP genuíno. A instabilidade de Gibbons–Hawking–Perry tem duas fontes:
1. o termo cinético $-(\nabla\Omega)^2$ com sinal errado (mitigável, em princípio, por uma cota de gradiente em domínio compacto de volume finito);
2. o termo de **potencial/acoplamento de curvatura** $\sim -\Omega^2 \bar R$ (ou $\Omega^4\Lambda$), que diverge para $-\infty$ quando $\Omega \to \infty$ **mesmo com gradiente nulo** (rescala conformal rígida/constante de uma métrica com $\bar R>0$). Esta é, historicamente, a formulação *mais elementar* do problema GHP, e uma cota em $|\nabla\ln\Omega|$ não diz absolutamente nada sobre a amplitude de $\Omega$. O texto não menciona este termo em nenhum momento.

Quanto ao "casamento de realidade" no bounce: a demonstração de que $K_{ij}=0$ em $\Sigma_{\mathrm{bounce}}$ é **correta mas trivial** — vale para qualquer bounce homogêneo isotrópico por definição de $H=0$. O problema real levantado na Rodada 4 (rotação de Wick ingênua produzindo curvatura extrínseca *imaginária*) refere-se a **flutuações/perturbações** $\delta K_{ij}(x,t)$ em torno do fundo, que genericamente **não se anulam** em $t=0$ e cuja continuação analítica $t\to it$ segue sendo problemática. O Remark 1.1(b) trata apenas do setor de fundo homogêneo (onde o problema nunca foi difícil) e é silencioso sobre o setor perturbativo (onde o problema de fato reside). Isso não é uma correção — é uma evasão do ponto.

## 2. Setor de Quarks (Proposição 8.2)

**Veredito: melhoria epistêmica real, mas com nova inconsistência numérica interna.**

O ponto positivo: abandonar o produto tensorial fatorado (que era matematicamente falso, como a Rodada 4 provou via o traço $\Tr_{\mathrm{color}}$) e reclassificar o resultado como *relação fenomenológica* em vez de teorema é a atitude epistêmica correta.

Porém, ao verificar numericamente:

- A fórmula $\alpha_s(M_Z)/\sqrt{3}$ não corresponde a nenhuma estrutura conhecida de dimensão anômala de QCD a 1-loop (que tipicamente envolve $C_F = 4/3$, não $\sqrt{3}$). O ajuste $0.1180/\sqrt{3} = 0.06813$ bate com precisão suspeita no valor necessário para produzir exatamente $0.7121$ — isto tem a assinatura de **numerologia reversa** (escolher a combinação que acerta o número-alvo), não de um cálculo perturbativo derivado.
- **Inconsistência interna verificável**: a definição $Q_q \coloneqq \sum m_{q_i} / (\sum \sqrt{m_{q_i}})^2$ não especifica *qual* tripleto de quarks. Usando as próprias massas tabuladas no artigo (Seção 8.2/Tabela 3) para o setor down-type ($m_d=4.67$, $m_s=93.4$ MeV, $m_b=4.18$ GeV):
$$Q_q^{\text{down, calc}} = \frac{4.67\times10^{-3}+0.0934+4.18}{(\sqrt{4.67\times10^{-3}}+\sqrt{0.0934}+\sqrt{4.18})^2} \approx \frac{4.2781}{5.8490} \approx 0.7314,$$
que **não é** $0.7121$ (diferença de $\sim$2.7%, e para o setor up-type dá $\approx 0.849$, totalmente fora da faixa). Ou seja, a própria fórmula definidora de $Q_q$, aplicada às massas que o artigo já tabula, **não reproduz** o valor teórico $0.7121$ que a Proposição 8.2 alega prever. O artigo compara $0.7121$ contra "$Q_q^{\exp}=0.71\pm0.02$" como se fossem calculados de forma consistente, mas nunca exibe o cálculo de $Q_q$ a partir das massas reais — isso deveria ser feito explicitamente e a discrepância, resolvida ou reconhecida.

## 3. Achado adicional não solicitado (erro aritmético verificado)

A fase CP: $\delta_{\mathrm{CP}} = \frac{2\pi}{3} - \frac{\alpha_s}{\sqrt{3}}$. Calculando: $2\pi/3 = 2.0944$ rad, menos $0.0681$ rad $= 2.0263$ rad $= 116.1°$ — **não** $1.161$ rad / $66.5°$ como impresso no texto. Há um erro aritmético/de digitação de fato (fator $\sim1.75\times$), mascarado porque $\sin(116.1°)\approx0.899$ e $\sin(66.5°)\approx0.917$ são numericamente próximos, então $J_{\mathrm{CP}}$ calculado não denuncia o erro. Isto deve ser corrigido antes de submissão — é o tipo de erro que um referee de JHEP encontra em minutos.

## 4. Teorema 8.1 (Equipartição de Norma) — o único ponto solidamente resolvido

Verifiquei algebricamente a identidade central. Para $\sqrt{m_k} = a + 2b\cos(\delta+2\pi k/3)$:
$$\|\mathbf v_1\|^2 = 3a^2, \qquad \|\mathbf v_2\|^2 = 6b^2 \quad\Longrightarrow\quad \|\mathbf v_2\|^2=\|\mathbf v_1\|^2 \iff b/a = 1/\sqrt2,$$
**independente de $\delta_l$** — confirmado por cálculo direto (os termos cruzados e de segunda harmônica somam zero por simetria $\mathbb{Z}_3$). Isto é correto e é de fato um resultado **se-e-somente-se** (o artigo só afirma a suficiência; a necessidade, que eu verifiquei, tornaria o Teorema mais forte e deveria ser incluída).

Dito isso, a moldura retórica ("significado geométrico profundo") ainda exagera o conteúdo físico: $b/a=1/\sqrt2$ não é derivado de $S_3$/$\Delta_2$ — é escolhido precisamente para produzir $Q_l=2/3$. O resultado é uma tautologia algébrica elegante e corretamente rotulada como consequência de um ansatz calibrado, não uma predição independente. Nesse sentido específico, a Rodada 5 finalmente atinge o padrão de honestidade epistêmica exigido — este é o único dos três problemas genuinamente fechado.

## 5. Veredito Editorial Final

**Reject (na forma atual) — requer uma 6ª rodada substantiva antes de submissão ao JHEP/SciPost.**

Justificativa: dois dos três problemas centrais apontados na Rodada 4 permanecem tecnicamente abertos:
- O Remark 1.1(a) contém um salto lógico não demonstrado (erro de categoria entre $\II_g$ extrínseco e $\Omega$ do bulk) e ignora a componente dominante do problema GHP (runaway de amplitude/potencial, não só gradiente).
- A Proposição 8.2, embora agora honestamente rotulada como fenomenológica, contém uma inconsistência numérica verificável entre sua própria definição e as massas tabuladas no mesmo artigo, além de uma fórmula ($\alpha_s/\sqrt3$) sem justificativa de QCD.
- Um erro aritmético concreto foi encontrado na fase CP.

O Teorema 8.1 é a exceção — está agora rigoroso e honestamente enquadrado.

**Nota Editorial (Rodada 5): ≈ 5.6–5.9/10** (progresso modesto sobre o 5.3/10 da Rodada 4 — ganho real em honestidade epistêmica, mas sem avanço matemático líquido no problema mais crítico, e com uma nova inconsistência numérica introduzida). Não tenho acesso aos registros de notas das Rodadas 1–3 nesta conversa para reconstituir a tabela comparativa completa de 5 rodadas com precisão — recomendo puxar os relatórios `PROOF_AUDIT_*` anteriores do repositório se uma tabela numérica completa for necessária para a resposta aos revisores.

### Recomendações para a próxima rodada
1. Ou (a) provar rigorosamente a relação $\II_g \to \nabla\ln\Omega$, ou (b) admitir explicitamente que o problema GHP é apenas *parcialmente mitigado no setor cinético* e permanece aberto no setor de potencial — não afirmar resolução total.
2. Especificar exatamente o tripleto de quarks em $Q_q$, recalcular com as massas tabuladas, e reconciliar o $\sim$2.7% de discrepância ou remover a alegação de "reprodução" do valor experimental.
3. Corrigir a aritmética de $\delta_{\mathrm{CP}}$.
4. Fortalecer o Teorema 8.1 para a versão *se-e-somente-se*.
