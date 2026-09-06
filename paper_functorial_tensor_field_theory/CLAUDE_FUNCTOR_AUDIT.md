# Revisão: "A Functorial Bridge from Continuous Tensor Manifolds to 4-Dimensional Spacetime Cobordisms"

## 1. Veredito de Publicabilidade

**Não está pronto para submissão imediata**, apesar das 7 rodadas de auditoria interna. O documento tem uma arquitetura categórica elegante e consistente na maior parte, mas contém **pelo menos um erro definicional real**, **duas lacunas analíticas não triviais**, e **uma seção (Teorema 5.4) que não é uma prova no sentido que CMP/JMP exigiriam** — é uma correspondência descritiva/física travestida de teorema categórico. Nenhum desses problemas é fatal para o programa de pesquisa, mas todos são do tipo que um referee de revista séria vai apontar na primeira rodada, gerando "major revision" na melhor hipótese.

Estimativa: mais 1–2 rodadas de revisão focadas (não apenas "auditoria adversarial" interna, mas correção estrutural) antes de estar em condições de submissão a uma revista Tier 1 de física-matemática.

---

## 2. Avaliação Técnica

### Definição 2.1 — Objetos e morfismos de $\CTens$

**Erro definicional concreto**: a condição on-shell em 2.1(a) referencia $(\rho_{\mathrm{matt}}, j_i)$ como "induzidos por $\psi_\Sigma$" — mas $\psi_\Sigma$ **não é parte do dado de objeto** $(\mathcal{M}, \mathcal{T}, \rho)$. Ele só é definido na Seção 4.1(3), como parte da *imagem* de $\mathcal{F}$ na categoria alvo. Isso é uma referência para frente inválida: você não pode impor uma condição on-shell em $\CTens$ que depende de uma estrutura que só existe depois de aplicar o funtor. Isso precisa ser corrigido explicitamente — ou $\psi_\Sigma$ (ou um análogo intrínseco a $\mathcal{T}$) entra na tripla de dados do objeto, ou a condição on-shell precisa ser reescrita em termos puramente de $(\mathcal{M},\mathcal{T},\rho)$.

**Lacuna técnica**: a "spatial immersion condition" (posto pleno de $d\mathcal{T}$) é usada na Seção 4.1(2) para concluir que o núcleo da métrica QFI $g^{\QFI}_{ij}$ é trivial. Mas posto pleno de $d\mathcal{T}(x): T_x\mathcal{M}\to T_{\mathcal{T}(x)}\mathcal{M}^{\mathrm{TT}}$ garante apenas que as derivadas $\partial_i\mathcal{T}$ são linearmente independentes *no espaço ambiente* — não que permaneçam independentes **depois de projetadas** por $(I - |\mathcal{T}\rangle\langle\mathcal{T}|)$. Se alguma combinação de $\partial_i\mathcal{T}$ for paralela a $|\mathcal{T}\rangle$, a projeção mata essa componente e a métrica QFI degenera, mesmo com imersão de posto pleno. O texto afirma a implicação sem prová-la; isso é exatamente o tipo de "gap" que os revisores anteriores (nas rodadas 1–6) aparentemente não pegaram porque é sutil. Precisa de uma hipótese adicional explícita (e.g., transversalidade da imersão em relação à direção de fase $|\mathcal{T}\rangle$) ou uma prova de que ela é automática dado o cMPS/cTT ansatz.

Também vale notar: $\rho$ é definido "através de qualquer bipartição" — mas a métrica QFI (Eq. 3.1) não depende de $\rho$, só de $\mathcal{T}$ puro. O papel de $\rho$ na estrutura de objeto fica subespecificado exceto no functor dagger ($\rho^T$). Isso não é um erro fatal, mas é uma inconsistência estética que sinaliza escrita apressada.

### Lema 5.1 (Equivalência ADM-Einstein / propagação hiperbólica)

A lógica de Choquet-Bruhat está correta em espírito: vínculos satisfeitos na fatia inicial + evolução via equações simétrico-hiperbólicas ⟹ vínculos propagados. Mas a "Hessian condition" (Eq. 5.1) que amarra a ação de entrelaçamento $\mathcal{S}$ à curvatura extrínseca é **postulada, não derivada** — o lema assume por hipótese exatamente a condição que faria o resto funcionar ("Suppose the entanglement action $\mathcal{S}(\mathcal{T})$ is chosen such that..."). Isso é logicamente válido (é um lema condicional), mas do ponto de vista físico é uma hipótese de existência não trivial: não há garantia, em geral, de que uma ação de entrelaçamento com esse Hessiano exista para um cMPS arbitrário satisfazendo a spatial immersion condition. Um referee vai perguntar: "para qual classe de $\mathcal{S}$ isso vale, e ela é não vazia?" Sem isso, o Lema 5.1 é uma tautologia disfarçada de teorema físico.

### Teorema 5.2 (Funtorialidade)

Estruturalmente é a parte mais sólida do artigo. A prova de preservação de composição usa colagem de cobordismos via junção Darmois-Israel com salto de curvatura extrínseca nulo — correto em princípio. Um ponto de rigor: a suavidade $C^\infty$ na junção depende do "mollifier de junção que anula a todas as ordens no ponto de transição" mencionado na Definição 2.1(c), mas essa maquinaria **não é reinvocada explicitamente na prova do Teorema 5.2** — o leitor precisa reconstruir por que a métrica composta é de fato suave (não só contínua) na fatia de colagem. Recomendo tornar isso explícito na prova, não deixar implícito na definição.

### Teorema 5.3 (Coerência monoidal e dagger)

Tecnicamente é a seção mais segura: como o produto monoidal em ambas as categorias é literalmente união disjunta estrita, associador e unitores são identidades triviais, e a prova é essencialmente combinatória. Sem objeções sérias aqui.

### Teorema 5.4 (Costura de cobordismos / Wheeler-DeWitt)

**Este é o ponto mais fraco do artigo e o principal obstáculo à publicação em uma revista rigorosa.** A "prova" não prova a correspondência anunciada — ela a *descreve*. Frases como "the categorical content is the following: ... This is an exact functorial statement" e "the constraint content ... parallels the Wheeler-DeWitt constraint system" são afirmações de analogia física, não deduções matemáticas. Especificamente:

- Não há derivação de que $\int_\Sigma \mathcal{D}\psi\, \mathcal{Z}(M_1)\mathcal{Z}(M_2) = \Tr_\chi(\mathcal{T}_1\mathcal{T}_2)$ além de invocar o "master duality dictionary" de uma referência não publicada do próprio autor (\cite{silvafilho2026flows}, um preprint).
- A afirmação de que "gauge invariance ... guarantees that variations with respect to $N^i$ vanish identically" não é demonstrada — é uma asserção de plausibilidade.
- $\hat{\mathcal{H}}|\Psi_{WDW}\rangle=0$ não é derivado a partir de nada definido no artigo; é citado por analogia com quantização canônica padrão.

Um referee de CMP/JMP vai rebaixar isso para "conjectural correspondence" ou exigir prova completa. Como está, é insustentável como "Theorem".

### Corolário 5.5 (funtor $\mathcal{Z}_{\mathrm{eff}} = \mathcal{Z}\circ\mathcal{F}$)

Problema estrutural sério: o corolário assume a existência de "$\mathcal{Z}: \Cob \to \Hilb$, o funtor TQFT axiomático de Atiyah" aplicado a $\Cob_{3+1}^{\mathbf{Fields}}$ — uma categoria de cobordismos **Lorentzianos, dinâmicos, sujeitos às equações de Einstein não lineares com matéria**. O funtor original de Atiyah-Segal é definido para cobordismos topológicos/compactos sem dinâmica de campo não linear. Construir rigorosamente tal $\mathcal{Z}$ para $\Cob_{3+1}^{\mathbf{Fields}}$ **é essencialmente equivalente ao problema em aberto de quantização não perturbativa da gravidade**. Apresentar isso como hipótese ("Let $\mathcal{Z}$ be Atiyah's TQFT functor") sem reconhecer que sua existência não está estabelecida é uma sobrecarga (overreach) que um referee vai identificar imediatamente. Isso deveria ser reformulado como corolário condicional explícito ("assuming such $\mathcal{Z}$ exists...") em vez de deixar implícito.

### Teorema 5.6 (Fidelidade e NEC)

O argumento de fidelidade (dados ADM completos determinam os geradores $(Q,R)$ até gauge $SU(\chi)$) é razoável e a parte mais convincente desta seção. Mas a prova da NEC assume uma forma canônica específica para $T_{\mu\nu}[\Psi]$ (tipo escalar livre cinético) **sem derivá-la** da definição real de $\psi_\Sigma = \Tr_\chi(\mathcal{T}\gamma^a A_a)$ dada na Seção 4.1(3). Não há lagrangiana especificada para $\Psi$; a forma de $T_{\mu\nu}$ é importada de fora. Além disso, a "correspondência semiclássica com QNEC" invoca o resultado de Bousso et al. \cite{bousso2016}, que foi provado em QFT sobre fundo fixo sob hipóteses específicas — aplicá-lo aqui por analogia, sem verificar as hipóteses, é outro salto não justificado.

---

## 3. Recomendações Estratégicas

**Antes de qualquer submissão:**
1. Corrigir a referência circular $\psi_\Sigma$ em Definição 2.1 — isso sozinho, se pego por um referee, mina a confiança em todo o resto do documento por parecer descuido.
2. Reclassificar o Teorema 5.4 como conjectura/correspondência heurística, ou fornecer prova completa (isso é trabalho substancial, possivelmente um artigo à parte).
3. Tornar o Corolário 5.5 explicitamente condicional à existência do funtor $\mathcal{Z}$.
4. Fechar a lacuna imersão→não-degenerescência da métrica QFI (Seção 4.1(2)) com hipótese explícita de transversalidade, ou prova.
5. Resolver a suavidade da função lapso $N(x,t)=\sqrt{|\partial_t S_{\mathrm{vN}}|+\sigma_0}$: $|\cdot|$ composta com raiz não é suave nos zeros de $\partial_tS_{\mathrm{vN}}$, mesmo com $\sigma_0>0$ deslocando o argumento — a não-suavidade de $|f|$ no zero de $f$ não é removida por somar uma constante depois. Isso ameaça a suavidade $C^\infty$ da métrica Lorentziana $g_{\mu\nu}$ reivindicada implicitamente ao longo do artigo. Ou restrinja a fluxos com produção de entropia de sinal definido (removendo o valor absoluto), ou trate isso explicitamente.

**Onde submeter (arXiv):** `math-ph` como primário, cross-list em `gr-qc` e possivelmente `hep-th`. Não `quant-ph` como primário — o conteúdo é geometria/categoria, não informação quântica per se.

**Periódicos:**
- **J. Math. Phys.** é provavelmente o encaixe mais realista *depois* das correções acima — tem histórico de aceitar construções categóricas rigorosas em física matemática, mas exige provas completas, não correspondências narrativas.
- **CQG** aceitaria o conteúdo ADM/GR mais facilmente, mas seus referees de relatividade geral vão cravar duro exatamente no Teorema 5.4/Corolário 5.5 por soarem como especulação sobre quantização da gravidade.
- **Ann. Henri Poincaré** e **Adv. Theor. Math. Phys.** são mais tolerantes a construções formais/categóricas especulativas, mas ainda exigiriam que "Theorem" signifique prova, não analogia.
- **Communications in Mathematical Physics** — eu não submeteria ainda. O padrão de rigor do CMP é o mais alto desta lista; o Teorema 5.4 seria motivo de rejeição rápida.

**Ponto de cautela mais importante, e o mais delicado**: pelo histórico visível no repositório, este artigo faz parte de um portfólio que inclui alegações de resolução do **gap de massa de Yang-Mills** e da **regularidade global de Navier-Stokes** — ambos problemas do Prêmio Millennium do Clay Institute. Editores e referees de revistas sérias tratam pacotes de múltiplas "resoluções" de problemas em aberto célebres, autoetiquetadas com "PASSED (Round N — FINAL)" via auditoria interna (inclusive assistida por IA), como um forte sinal de alerta — independentemente do mérito técnico individual de cada peça. Isso não significa que o trabalho seja inválido, mas significa que:
- Cada submissão será examinada com ceticismo redobrado por associação;
- Vale considerar submeter este artigo (o funtorial, que é o mais autocontido e modesto em escopo) **isoladamente**, sem referenciar os outros preprints como já estabelecidos (as citações \cite{silvafilho2026book} e \cite{silvafilho2026flows} são autocitações a preprints não publicados/não revisados por pares — isso enfraquece a base lógica de resultados que dependem delas, como o "master duality dictionary" usado no Teorema 5.4);
- Recomendo fortemente obter uma revisão externa por um especialista humano em geometria categórica/TQFT ou relatividade numérica *antes* de submeter, independentemente da revista escolhida — 7 rodadas de auditoria adversarial interna (possivelmente pelo mesmo sistema de IA) não substituem um par humano independente, especialmente dado o padrão acima.

**Resumo direto**: o esqueleto categórico (Definição 2.1, Teoremas 5.2–5.3) é sólido o suficiente para ser levado a sério. As Seções 5.4–5.6 precisam de mais trabalho real antes de irem a um editor. Eu não apertaria o botão ainda.
