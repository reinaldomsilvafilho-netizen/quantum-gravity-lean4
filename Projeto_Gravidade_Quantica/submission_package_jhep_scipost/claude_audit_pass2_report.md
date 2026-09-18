# Parecer de Auditoria Adversarial — Rodada 2 (Pass 2)
**Revisor:** Física Matemática / JHEP-SciPost
**Manuscrito:** *Simplicial Quantum Gravity on $\Delta_4 \times \Delta_2$...*
**Veredito resumido:** As correções solicitadas na Rodada 1 foram **parcialmente atendidas na forma**, mas **não na substância**. O manuscrito acrescentou aparato formal (representações de $S_3$, matrizes circulantes, Bakry-Émery, referências) sem resolver o problema estrutural de fundo: a ausência de um mecanismo dinâmico independente que gere as massas antes de serem comparadas aos dados. Seções inteiras permanecem não falsificáveis.

---

## 1. Auditoria da Ação $\mathcal{S}_{\mathrm{univ}}$ (Subseção 1.3, Eq. 1.3)

**Problema crítico não resolvido: o termo de Yukawa está ausente.**
A Seção 8 deriva massas fermiônicas a partir de "matrizes de Yukawa circulantes" $\mathbf{Y}_{\mathrm{circ}}(a,b,\delta)$ acopladas ao VEV de Higgs $v$. Porém, a ação mestra (Eq. 1.3) contém apenas três termos: (i) curvatura $\Tr(\Omega\wedge\star\Omega)$, (ii) cinético fermiônico $\bar\Psi(\mathcal{D}^{(\alpha)}-\mathcal{W}_{\Delta_2})\Psi$, e (iii) $\|\II_{\mathcal{H}}\|^2_{\mathrm{op}}$ (puramente bosônico, do setor de Higgs). **Não há termo do tipo $\bar\Psi\,\Phi\,\Psi$** que acople o fermion ao campo escalar. Logo, $S_{\mathrm{univ}}$, como escrita, *não gera* as matrizes de massa usadas na Seção 8 — o operador $\mathcal{W}_{\Delta_2}$ é apresentado como gerando "as matrizes de massa complexas circulantes", mas isso o faz sozinho, sem EWSB, o que contradiz o mecanismo de Higgs alegado alhures. Este é o defeito estrutural mais grave do artigo: a ação e a fenomenologia (§8) não estão conectadas por uma derivação explícita.

**Problema de definição algébrica:** $\Omega \in \Omega^2(\mathcal{M}, \mathfrak{g}_{\mathrm{univ}})$ com $\mathfrak{g}_{\mathrm{univ}} = \mathfrak{su}(3)\oplus\mathfrak{su}(2)\oplus\mathfrak{u}(1)\oplus\mathfrak{so}(3,1)$. O traço $\Tr(\Omega\wedge\star\Omega)$ sobre uma soma direta de álgebras exige uma escolha explícita de forma bilinear invariante (normalização relativa, análoga às constantes $\alpha_1,\alpha_2,\alpha_3$ em GUTs) — isso **não é especificado**. Mais grave: $\mathfrak{so}(3,1)$ é não-compacta com forma de Killing indefinida, enquanto $\mathfrak{su}(N)$ tem forma definida (negativa, na convenção usual). Somar essas contribuições num único termo quadrático sem justificar a assinatura resultante compromete a limitação inferior/coercividade da ação — essencial tanto para o princípio minimax $L^\infty$ quanto para qualquer formulação de integral de caminho euclidiana. Um referee de JHEP pedirá a forma bilinear explícita e uma prova de que o funcional é limitado inferiormente.

**Medida de integração $\dif\mathrm{vol}_{\mathcal{G}}$ indefinida:** dado que a métrica QFI (Eq. 1.5) diverge como $1/x_i$ na fronteira do simplex, a finitude de $\int_{\Delta_4\times\Delta_2}(\cdots)\dif\mathrm{vol}_{\mathcal{G}}$ não é demonstrada. Isso é agravado pelo fato de $B_\alpha(\mathbf{x})$ (potencial de barreira, Def. 3.1) também divergir no bordo — o artigo afirma que isso "garante confinamento" mas nunca prova que a ação total permanece finita.

**Conclusão do item 1:** a formulação de três termos é estruturalmente incompleta (falta o acoplamento de Yukawa) e algebricamente subespecificada (falta a forma bilinear em $\mathfrak{g}_{\mathrm{univ}}$ e prova de integrabilidade). Não está pronta para submissão nesta forma.

---

## 2. Auditoria do Cálculo de Massas (Seção 8, Tabela 3)

Este é o ponto mais vulnerável do manuscrito, e a objeção de "ajuste post-hoc" da Rodada 1 **não foi resolvida** — apenas reformulada com mais formalismo.

**a) O quociente de Koide $Q_l=2/3$ é uma tautologia algébrica, não uma predição física.**
O Teorema 8.1 mostra que $Q_l = \Tr(\mathbf{P})/\|\mathbf{P}\|_F^2 = 2/3$ para o projetor na rep. 2D padrão de $S_3$. Isso é verdade *para qualquer terna de massas parametrizada pela órbita circular* (Eq. 8.1), **para qualquer fase $\delta$** — é uma propriedade da parametrização trigonométrica em si (já conhecida desde Koide 1983 e Foot 1994), não uma consequência de geometria simplicial nova. Rotular isso como "derivação geométrica exata" via $S_3$ em $\Delta_2$ é reembalar um fato matemático conhecido como física nova.

**b) A fase $\delta_l = 2/9+\pi/12$ não é derivada — é ajustada.**
Não há nenhuma justificativa geométrica *a priori* para por que $\delta_l$ toma exatamente esse valor (por que $2/9$? por que $\pi/12$?). Dado que a órbita tem apenas 2 parâmetros livres ($v_0,\delta_l$) para ajustar 3 massas medidas, resta apenas 1 grau de liberdade — precisamente $Q_l=2/3$, que já é garantido pela parametrização (item a). Ou seja: **o modelo tem exatamente parâmetros suficientes para reproduzir os dados, e nenhum grau de liberdade sobra para constituir uma predição real**. Um referee competente exigirá que $\delta_l$ seja derivado independentemente (de um ângulo diedral do simplex, por exemplo) *antes* de comparar com $m_e,m_\mu,m_\tau$ — caso contrário, isso é ajuste de 2 parâmetros para 3 pontos, disfarçado de teorema.

**c) Setor de quarks: inconsistência de escala de renormalização.**
A tabela mistura $m_u,m_d,m_s$ em $\overline{\mathrm{MS}}(2\text{ GeV})$, $m_c,m_b$ em $\overline{\mathrm{MS}}(m_q)$, e $m_t$ como massa de polo — quatro esquemas/escalas distintos combinados numa única razão de Koide "geometricamente derivada" $Q_q$. Isso é tecnicamente inválido: uma quantidade proclamada como invariante geométrico não pode ser calculada a partir de massas definidas em convenções de renormalização incompatíveis sem uma prescrição explícita de "running" comum — ausente no texto.

**d) Valores de quarks "preditos" coincidem exatamente com o PDG — sem fórmula.**
Para léptons, há uma fórmula explícita (Eq. 8.1) computável de $\delta_l, v_0$. Para quarks, a coluna "Geometric Expression" diz apenas "Circulant eigenvalue on $\Delta_2$" — **sem os valores numéricos de $a,b,\delta$ usados**, e os "valores preditos" ($2.16$ MeV, $4.67$ MeV, $93.4$ MeV, $1.27$ GeV, $4.18$ GeV) são **idênticos, dígito a dígito, aos centrais do PDG 2024**. Isso é uma bandeira vermelha inequívoca de injeção direta de dados experimentais disfarçada de predição teórica. Um referee pedirá o cálculo explícito ($a,b,\delta$ para quarks) ou removerá a alegação de "derivação".

**e) $W$, $Z$: fórmulas SM padrão, não geometria nova.**
$m_W=gv/2$, $m_Z = v\sqrt{g^2+g'^2}/2$ são relações de árvore do Modelo Padrão comuns a qualquer livro-texto. O texto afirma que $g,g'$ "são determinados por razões de volume métrico simplicial em $\Delta_4$" mas **nenhuma fórmula ou número é fornecido** — $g,g'$ são efetivamente inseridos a mão a partir dos valores medidos. Não há predição aqui.

**f) Higgs: $\lambda_{\Delta_2}=1/8$ não justificado; correção CW ajustada a posteriori.**
$m_H^{(0)}=v/2$ requer $\lambda_{\Delta_2}=1/8$, atribuído a "curvatura Gaussiana de $\Delta_2$" sem cálculo — o valor $1/8$ parece escolhido para que $v/2 + \Delta m_H \approx 125.09$ GeV funcione. Isso é reversamente derivado da resposta.

**g) Neutrinos: $M_{\GUT}=2\times10^{15}$ GeV é entrada livre, não predição**, e os ângulos PMNS "geométricos" ($1/3$, $1/2$) estão a $2$–$2.5\sigma$ dos dados — inconsistente com a precisão de $<0.01\%$ proclamada no setor de léptons carregados. Essa discrepância de padrão de precisão entre setores (quase exata onde há liberdade de ajuste, imprecisa onde não há) é, por si só, evidência estatística contra a hipótese de que o mecanismo é preditivo.

**Veredito do item 2:** um referee de JHEP/SciPost levantará — corretamente — a objeção de ajuste post-hoc com força total. A "derivação formal dentro das representações de $S_3$ e do fibrado de Higgs" não se sustenta: $Q_l=2/3$ é tautológico; $\delta_l$, $\lambda_{\Delta_2}$, $M_{\GUT}$ são parâmetros livres calibrados contra os próprios dados que deveriam prever; e os valores de quarks parecem copiados do PDG sem cálculo mostrado.

---

## 3. Coerência Geral, Rigor e Notação

- **Contradição de domínio:** a Definição 3.1 define $(-\Delta_{\Delta_m})^\alpha$ para $\alpha\in(0,1)$, mas a Subseção 1.3(iii) invoca um "índice crítico $\alpha^*=2$" — **fora do domínio de definição do próprio operador**. Isso precisa ser resolvido ou explicado (extensão analítica? outro operador?).
- **Integrabilidade do núcleo fracionário não verificada:** $\mathcal{K}_\alpha(\mathbf{x},\mathbf{y})\propto\prod|x_i-y_i|^{1-\alpha}$ — a convergência do valor principal não é demonstrada para $m=4$.
- **Autocitações como base de prova:** seis referências a monografias do próprio autor no Zenodo (não revisadas por pares) são citadas como *passos de demonstração* de resultados centrais (ex.: \cite{silvafilho2026treatise} para prevenção de singularidade conjugada; \cite{silvafilho2026yangmills} para o gap de massa). Referees de JHEP/SciPost normalmente **não aceitam preprints autopublicados não arbitrados como elos de demonstração** — os resultados citados precisam ser reproduzidos no corpo do artigo ou publicados em veículo arbitrado antes da submissão.
- **Alegação de verificação Lean 4 é enganosa por escopo:** "0 sorry" em 141 obrigações provavelmente formaliza identidades algébricas abstratas (traço de projetor de $S_3$, etc.), não as afirmações físicas do artigo (que $\Delta_4\times\Delta_2$ descreve o universo real). Isso deveria ser explicitado com precisão — caso contrário confunde "identidade matemática verificada" com "teoria física verificada".
- **Tabela 4 (scorecard) ainda assimétrica:** embora mais objetiva que a versão anterior, a coluna "Singularity Status" ainda atribui rótulos qualitativamente favoráveis à proposta própria ("Resolved") contra rótulos vagos/desfavoráveis a rivais ("Inconclusive", "Extended volume phases") sem citar criticamente a literatura que disputa isso (ex.: bounce de LQC também é debatido quanto à sua derivação rigorosa desde os graus de liberdade fundamentais).
- **Seção 12 é uma lista de alegações não demonstradas no corpo do texto:** Problema CP forte, informação de buraco negro, problemas de horizonte/planura são "resolvidos" em uma linha de tabela cada, mas **nenhum teorema correspondente aparece no corpo do artigo**. Isso deve ser removido ou movido para "outlook/conjecturas futuras" com linguagem apropriadamente modesta.
- **Dimensão/consistência de $\dif\mu_{\mathbf a}$ vs. medida de Lebesgue:** a Def. 3.1 usa medida de Dirichlet $\mu_{\mathbf a}$ mas o Teorema 3.1 (núcleo do calor) usa integral sobre $\mathbb{R}^4$ com medida de Lebesgue plana — a transição entre as duas geometrias (simplicial vs. plana) não é justificada.

---

## 4. Veredito Editorial Final

| Critério | Nota (0–10) |
|---|---|
| Rigor matemático das seções puramente geométricas (ADM, Caffarelli, Bakry-Émery) | 6 (condicionalmente coerentes, mas com lacunas de integrabilidade/definição) |
| Consistência da ação mestra com a fenomenologia derivada | 1 (falta termo de Yukawa; forma bilinear em $\mathfrak{g}_{\mathrm{univ}}$ indefinida) |
| Rigor do setor de massas de partículas (Seção 8) | 1–2 (tautologias algébricas apresentadas como predições; parâmetros livres calibrados contra os dados-alvo; valores de quarks aparentemente copiados do PDG) |
| Bibliografia e verificabilidade (autocitações, Lean 4) | 3 |
| Adequação editorial para JHEP/SciPost nesta forma | **2/10 — Reject / Major Revision necessária antes de re-submissão** |

**Parecer objetivo:** O manuscrito combina matemática genuína e localmente correta (regularidade $C^{1,1}$ de Caffarelli, cota de cisalhamento ADM, gap Bakry-Émery) com uma seção de fenomenologia de partículas (§8) que não resiste a escrutínio: o quociente de Koide é uma tautologia da parametrização, não uma consequência física nova; a fase $\delta_l$ e a constante $\lambda_{\Delta_2}$ são ajustadas para reproduzir os dados sem derivação independente; e os valores numéricos de quarks parecem ser diretamente os centrais do PDG sem cálculo mostrado. Adicionalmente, a ação mestra (§1.3) carece do próprio termo (acoplamento de Yukawa) necessário para gerar as massas que a Seção 8 afirma derivar dela — uma desconexão estrutural entre a teoria proposta e sua fenomenologia. Até que esses pontos sejam corrigidos com derivações verdadeiramente *a priori* (parâmetros fixados **antes** de qualquer comparação com dados, com predições genuinamente cegas), o artigo será rejeitado por qualquer referee competente de JHEP ou SciPost Physics por conter numerologia disfarçada de rigor formal.

**Recomendações prioritárias para a próxima rodada:**
1. Inserir explicitamente o termo de Yukawa $\bar\Psi\Phi\Psi$ em $S_{\mathrm{univ}}$ e mostrar como $\mathbf{Y}_{\mathrm{circ}}$ emerge dele.
2. Derivar $\delta_l$, $\lambda_{\Delta_2}$, $M_{\GUT}$ de invariantes geométricos puros (ângulos, curvaturas) **sem referência aos valores medidos**, então comparar — não o inverso.
3. Mostrar o cálculo explícito por trás dos valores de quarks (não apenas "circulant eigenvalue on $\Delta_2$").
4. Resolver a contradição $\alpha\in(0,1)$ vs. $\alpha^*=2$.
5. Substituir autocitações Zenodo por demonstrações internas ou referências arbitradas.
6. Retirar ou suavizar as alegações da Tabela 2 (§9) não demonstradas no corpo (CP forte, informação de buraco negro).
