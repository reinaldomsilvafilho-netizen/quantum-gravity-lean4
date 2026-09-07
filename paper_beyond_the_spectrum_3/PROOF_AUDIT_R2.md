# AUDITORIA ADVERSARIAL — RODADA 2 (Fase 5: Reauditoria Cega e Verificação de Patches)
## Beyond the Spectrum III — Protocolo Triadic Proof Verifier

**Auditor:** Claude CLI (Adversarial Auditor)
**Status de entrada:** 17 apontamentos da Rodada 1 declarados corrigidos
**Método:** verificação linha-a-linha de cada patch contra o texto LaTeX final, busca de vacuidade residual, contraexemplos e integridade de citação

---

## PARTE A — Verificação Ponto a Ponto dos 17 Patches

| # | Item | Veredito | Observação |
|---|------|----------|------------|
| 1 | OBL-014 (subespaço $\mathcal H_{\mathrm{supp}}$) | ⚠️ **PARCIAL** | O mecanismo espectral (posto finito, regularização de Mercer) está correto isoladamente. Mas ver **Achado Crítico 1** abaixo — a construção herda uma inconsistência estrutural não tratada. |
| 2 | OBL-020 (reach com $d_{\mathrm{sep}}$) | ✅ PASS | Fórmula de Federer com termo de auto-colisão está correta; caso convexo com $d_{\mathrm{sep}}=\infty$ reduz corretamente à cota de curvatura pura. |
| 3 | OBL-019 (Kigami $d_s$) | ✅ PASS | Verificação numérica correta: $N=3,\rho=3/5 \Rightarrow N/\rho=5 \Rightarrow d_s = 2\ln3/\ln5 \approx 1.3652$. Consistente com a literatura padrão do gasket de Sierpinski. |
| 4 | OBL-011 ($\Delta F$ não trivial) | ✅ PASS | $Z(A)=\Tr(A)$ elimina a tautologia; identidade de Jarzynski via Girsanov/Crooks está correta. |
| 5 | OBL-010 (convexidade uniforme) | ⚠️ **MENOR** | Matematicamente correto, mas ver **Achado Menor 2** — erro de atribuição de citação. |
| 6 | OBL-018 (polos de $\Gamma(s+\alpha_j+k)$) | ✅ PASS | Mecanismo de polos corrigido corretamente (numerador, não denominador). |
| 7 | OBL-003 (compacto $K$) | ✅ PASS | Argumento padrão de estimativa de energia em Floer contínuo, válido. |
| 8 | OBL-001 (fator $2\pi$, domínio da Hessiana) | ✅ PASS | Prova via Taylor com resto integral ao longo do segmento $[x_0,x]\subset K_t(A)$ (usa convexidade para manter o segmento dentro do domínio) — correta. Nota cosmética: as regiões $E_{\mathrm{in}}, E_{\mathrm{out}}$ construídas são bolas, não elipsoides gerais, mas isso não invalida o argumento (bolas são elipsoides degenerados). |
| 9 | OBL-004 (Whitney (B) via Mather) | ✅ PASS | Aplicação padrão do teorema de transversalidade estratificada. |
| 10 | OBL-007 (conexidade de $\Omega$) | ✅ PASS | Conexidade + Harnack degenerado garante positividade estrita e unicidade do ground state. |
| 11 | OBL-009 (completude geodésica) | ⚠️ **MENOR** | Conclusão correta, mas ver **Achado Menor 1** — teorema comparativo citado incorretamente. |
| 12 | OBL-008 (Cheeger, dois sentidos) | ❌ **GAP RESIDUAL** | Ver **Achado Médio 1** — a cadeia de desigualdades tem saltos não justificados. |
| 13 | OBL-013 (diagonal de $K_A$) | ⚠️ **PARCIAL** | Ver **Achado Crítico 2** — existência da família ortonormal não é demonstrada, apenas postulada. |
| 14 | OBL-015/016 (holográfico, DAG) | ⚠️ **PARCIAL** | Depende estruturalmente de OBL-014; herda o **Achado Crítico 1**. |
| 15 | OBL-017 (holomorfia) | ✅ PASS | Argumento padrão de convergência dominada + analiticidade sob o sinal de integral. |
| 16 | OBL-002 (citação HZ) | ⚠️ **MENOR** | Ver **Achado Menor 3**. |
| 17 | OBL-012 (Poincaré/atrito) | ✅ PASS | Aritmética final consistente ($\mathcal L^2 \ge \frac\kappa2 W_2^2 \Rightarrow \frac12\mathcal L^2\ge\frac\kappa4 W_2^2$); a cota $g_{\mathrm{fric}}\ge\frac\kappa2 g_{\mathrm{Otto}}$ é citada (Sivak-Crooks/Aurell) e aceitável como resultado importado. |

---

## PARTE B — Achados Novos (não cobertos pela lista de 17)

### 🔴 Achado Crítico 1 — Inconsistência de domínio na Seção 6 (bipartição espacial vs. produto tensorial)

**Local:** início da Seção 6 vs. `Theorem 6.3` (OBL-014) e `Theorem 6.4` (OBL-015).

O texto declara: *"Let $\Omega = \Omega_1 \sqcup \Omega_2$ be a spatial bipartition"* — **união disjunta**. Isso é fisicamente correto para entropia de emaranhamento de uma região espacial (a la Casini-Huerta): $L^2(\Omega) = L^2(\Omega_1)\oplus L^2(\Omega_2)$ (soma direta).

Porém, a fórmula do traço parcial dada é:
$$\rho_{\Omega_1}(x_1,y_1) \coloneqq \int_{\Omega_2} K_A(x_1,z_2;y_1,z_2)\,dz_2$$

Essa fórmula só é bem tipada se $K_A$ for um núcleo em $(\Omega_1\times\Omega_2)\times(\Omega_1\times\Omega_2)$ — ou seja, exige $\Omega = \Omega_1 \times \Omega_2$ (**produto cartesiano**, estrutura de sistema bipartido/tensorial), não $\Omega_1\sqcup\Omega_2$. Isso é reforçado por `Theorem 6.4`, que exige $\rho_{12}$ em $\mathcal H_{\mathrm{supp}}^{(1)}\otimes\mathcal H_{\mathrm{supp}}^{(2)}$ (produto tensorial explícito) e uma purificação canônica GNS — construção que só faz sentido para um sistema bipartido tensorial, não para subconjuntos disjuntos de um único domínio.

**Consequência:** a hipótese fundacional da Seção 6 ("bipartição espacial", motivando a linguagem de "regiões", "RT surfaces", "entanglement wedge" em OBL-016) contradiz a maquinaria formal usada para de fato definir $\rho_{\Omega_1}$ e $S_R$. Isso não é cosmético — as duas leituras (união disjunta vs. produto) dão objetos matemáticos genuinamente diferentes (soma direta vs. produto tensorial de Hilbert spaces), e a literatura citada (Dutta–Faulkner) sobre entropia refletida holográfica assume precisamente a estrutura de bipartição espacial ($\Omega_1\sqcup\Omega_2$ com álgebras de von Neumann tipo III), que **não** é a que foi formalmente construída aqui via traço parcial ingênuo. Esse ponto **não foi tratado nos 17 patches da Rodada 1** e permanece uma vacuidade estrutural aberta que contamina OBL-014, OBL-015 e OBL-016.

**Verdict:** REJEITADO — requer decisão explícita do autor: (a) redefinir $\Omega$ como $\Omega_1\times\Omega_2$ desde a Proposição 6.2 (perdendo a interpretação de "região espacial" necessária para OBL-016/RT), ou (b) reconstruir $\rho_{\Omega_1}$ via restrição de bloco do operador $T_A$ a $L^2(\Omega_1)\subset L^2(\Omega)$ (consistente com $\Omega_1\sqcup\Omega_2$, mas exigindo reformulação completa de OBL-014/015/016, já que a purificação canônica GNS em produto tensorial não se aplica diretamente).

### 🔴 Achado Crítico 2 — Existência não demonstrada da família ortonormal em OBL-013

**Local:** `Proposition 6.2` (OBL-013).

A proposição assume como hipótese: *"Let $\{\phi_j\}_{j=1}^n$ be an orthonormal family in $L^2(\Omega)$ chosen such that... $\sum_j \lambda_j|\phi_j(x)|^2 = \Phi_{\mathrm{scalar}}(A)(x)$."* Trata-se de uma condição pontual (infinitas restrições) impondo compatibilidade com apenas $n$ graus de liberdade funcionais sujeitos a $n(n+1)/2$ restrições adicionais de ortonormalidade. Não há demonstração de que tal família exista para um $\Phi_{\mathrm{scalar}}(A)$ arbitrário herdado dos Volumes I/II — o enunciado apenas presume sua existência ("chosen such that"). Se essa família não existir genericamente, toda a Seção 6 (OBL-013 a OBL-016) é **vazia por hipótese não-realizável**, exatamente o tipo de vacuidade que motivou a rejeição original de OBL-014 na Rodada 1.

**Verdict:** este ponto era exatamente o problema já apontado em OBL-014/R1 — o patch resolveu a vacuidade *dado* $\{\phi_j\}$, mas não resolveu a vacuidade *da existência* de $\{\phi_j\}$. Requer uma construção explícita (e.g., via decomposição espectral de $\Phi_{\mathrm{scalar}}(A)$ como um kernel de Mercer $K_A^{\mathrm{diag}}(x,x)$ herdado consistentemente da definição original em Volumes I/II) ou uma referência cruzada que garanta a propriedade por construção.

### 🟡 Achado Médio 1 — Gap na prova do limite de Cheeger (OBL-008)

**Local:** `Theorem 4.3`, prova.

Dois saltos não justificados:
1. **Monotonicidade:** afirma-se que $p\mapsto(\lambda_1^{(p)})^{1/p}$ é não-decrescente "por Hölder na medida normalizada por probabilidade" — mas Hölder aplicado a uma função fixa $u$ não implica monotonicidade do **ínfimo** $\lambda_1^{(p)}$, pois o minimizante $u_p$ varia com $p$ e o espaço admissível $W_0^{1,p}$ também muda. O argumento como escrito não fecha.
2. **Limite inferior:** a desigualdade de coárea é feita para $p=1$ (variação total ponderada), mas a passagem "Taking the $L^p$ norm as $p\to\infty$" para concluir $\liminf(\lambda_1^{(p)})^{1/p}\ge h(A)$ pula a etapa técnica real (relacionar $\int\|\nabla u_p\|\Phi(A)$, que é uma norma $L^1$, à quantidade $L^p$ $\lambda_1^{(p)}$ via Hölder reverso) — tentativa direta de fechar esse passo (verificado manualmente pelo auditor) produz a desigualdade na direção **errada** (Hölder dá $\int|u_p|\Phi(A) \le \mu_A(\Omega)^{1-1/p}$, uma cota superior, não inferior, quando se precisa de uma cota inferior).

O teorema final é verdadeiro e bem estabelecido (Kawohl–Fridman 2003, citado corretamente para a direção do limsup), mas a prova como apresentada não demonstra de fato a direção do liminf nem a monotonicidade — apenas as assume por analogia com o resultado citado.

**Verdict:** manter `AUDITED_PATCHED` apenas se a prova citar Kawohl–Fridman/Juutinen–Lindqvist–Manfredi para **ambas** as direções (em vez de apresentar uma prova própria incompleta); caso contrário, rebaixar para `NEEDS_REVISION`.

### 🟡 Achado Médio 2 — Teorema comparativo incorreto citado em OBL-009

**Local:** `Theorem 4.4`, prova.

A prova invoca "Toponogov's comparison theorem" para justificar que triângulos geodésicos são mais finos que triângulos de comparação em curvatura constante $-\kappa_0$. O teorema de Toponogov é o teorema clássico de comparação para **cotas inferiores** de curvatura seccional ($\mathrm{Sec}\ge\kappa$), produzindo triângulos "mais gordos". Para **cotas superiores** ($\mathrm{Sec}\le-\kappa_0$, o caso aqui), a ferramenta correta é a comparação de Rauch/Alexandrov (espaços CAT($-\kappa_0$)), não Toponogov. A conclusão numérica ($\delta \le \kappa_0^{-1/2}\ln(1+\sqrt2)$) é plausível e consistente com a literatura de espaços CAT($\kappa$), mas o teorema citado é o errado.

### 🟢 Achado Menor 1 — Citação incorreta em OBL-010

**Local:** `Proposition 5.2`, prova: *"By the Otto–Villani theorem \cite{BakryEmery1985}..."* — o teorema de Otto–Villani (2000, conectando LSI a Talagrand $W_2$) é atribuído à referência de Bakry–Émery (1985, que estabelece o próprio critério $\Gamma_2\ge\kappa\Gamma$ ⟹ LSI). Não existe entrada bibliográfica para Otto–Villani na lista de referências — citação ausente.

### 🟢 Achado Menor 2 — Atribuição imprecisa em OBL-002

**Local:** `Proposition 2.2`, prova: atribui a identidade $c_{\mathrm{HZ}}=\inf\mathcal A_{\mathrm{act}}$ a "Ekeland–Lasry and Hofer–Zehnder". O artigo de Ekeland–Lasry (1980) trata da existência de múltiplas características fechadas sob condição de "pinching" — um resultado diferente. A identidade em si é teoria padrão de capacidade de Hofer–Zehnder.

---

## PARTE C — Verificação de Integridade do DAG e Contagem

- DAG de dependências (`mermaid`): **acíclico confirmado** — todas as arestas seguem ordem crescente de índice, sem ciclos.
- Contagem de obrigações: 21/21 consistente entre ledger, abstract e corpo do texto.
- Seções 2–5, 7–8 (OBL-001 a 012, 017–021): estruturalmente sólidas modulo os achados médios/menores acima.
- Seção 6 (OBL-013 a 016): **estruturalmente comprometida** pelo Achado Crítico 1.

---

## VEREDITO FORMAL DA RODADA 2

> **STATUS: REJEITADO — RODADA 3 REQUERIDA**

Dos 17 patches declarados, **11 PASSAM** integralmente (OBL-001, 003, 004, 007, 011, 012, 015-parcial-estrutura-interna, 017, 018, 019, 020), **4 requerem apenas correção de citação/atribuição** (OBL-002, 009, 010 — menores, não bloqueantes para publicação mas obrigatórios para rigor acadêmico), e **2 apresentam gaps substantivos não resolvidos**:

1. **OBL-008** — prova incompleta (gap técnico real, não apenas cosmético).
2. **OBL-013/014/015/016** — vacuidade estrutural não tratada (Achados Críticos 1 e 2), que é **mais grave** que os problemas originais da Rodada 1 nesta mesma região do texto, pois atinge a própria definibilidade dos objetos (não apenas a positividade do Hamiltoniano modular).

**Ações obrigatórias para Rodada 3:**
1. Resolver a contradição $\Omega_1\sqcup\Omega_2$ vs. $\Omega_1\times\Omega_2$ na Seção 6, com reconstrução completa de OBL-014/015/016 sob a escolha consistente.
2. Fornecer construção explícita (ou hipótese adicional citável) garantindo a existência da família ortonormal $\{\phi_j\}$ em OBL-013.
3. Reescrever a prova de OBL-008 citando corretamente a literatura para ambas as direções do limite, ou fechar rigorosamente os dois saltos identificados.
4. Corrigir as três atribuições de citação incorretas (OBL-002, OBL-009, OBL-010) e adicionar entrada bibliográfica para Otto–Villani (2000) se mantida a menção.

Nenhum contraexemplo numérico foi encontrado (OBL-019 confere numericamente); os problemas remanescentes são de **rigor de prova e consistência estrutural de definições**, não de falsidade dos enunciados finais.
