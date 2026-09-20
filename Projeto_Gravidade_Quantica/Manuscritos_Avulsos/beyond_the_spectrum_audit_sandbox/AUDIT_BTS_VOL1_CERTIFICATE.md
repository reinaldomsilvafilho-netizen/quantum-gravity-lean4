# CERTIFICADO DE AUDITORIA MATEMÁTICA RIGOROSA — BTS_VOL1

**Obra**: *Beyond the Spectrum, Volume I: Functional Realizations of Matrices and Tensors, Emerging Invariants, and Geometric Measures*
**Manuscrito**: `paper_functional_realizations.tex` (839 linhas, completo, lido integralmente)
**Módulo Lean**: `beyond_the_spectrum_files/formal_proofs_bts/BTS/Volume1_FunctionalRealizations.lean` (lido integralmente)
**Auditor**: Chief Adversarial Proof Engineer (modo máximo)

---

## 1. CONTEÚDO MATEMÁTICO DO MANUSCRITO (LaTeX) — Avaliação por obrigação

| OBL | Enunciado | Verificação matemática |
|---|---|---|
| 001 | Correspondência espectral/crítica (Rayleigh) | ✅ Correto. Multiplicador de Lagrange $\nabla_x\mathcal L=2Ax-2\mu x=0 \Rightarrow Ax=\mu x$; extremos = $\lambda_1,\lambda_n$. Prova autocontida e válida. |
| 002 | Cegueira espectral / energia de Dirichlet | ✅ Correto. Fórmula de Parseval $\mathcal E(f_A)=\sum(k_1^2+k_2^2)|a_{k_1k_2}|^2$ derivada corretamente; exemplo $E_{1,1}$ vs. $E_{n,n}$ dá $\Theta(n^2)$ de forma explícita e verificável. |
| 003 | TV da step-realization | ✅ Correto. Integração por partes célula-a-célula, teorema da divergência, saturação do sinal — fórmula \eqref{eq:tv_formula} está dimensionalmente consistente (fator $1/n$ por aresta de comprimento $1/n$). |
| 004 | Coarea/Hausdorff | ✅ Correto por citação válida (De Giorgi, Evans–Gariepy); hipóteses de BV discutidas no Thm anterior são corretamente herdadas. |
| 005 | Morse/Euler | ✅ Correto. Hessiano riemanniano calculado explicitamente; índice $\gamma(v_i)=i-1$; $1-(-1)^n=\chi(\Sph^{n-1})$ confirmado por cálculo direto de homologia. |
| 006 | Cut-norm ↔ operador $L^\infty\to L^1$ | ✅ Correto. Decomposição $u_\pm,v_\pm$ dá constante $4$ nitidamente correta (resultado clássico Frieze–Kannan/Lovász–Szegedy). |
| 007 | Compacidade do moduli de graphons | ✅ Correto por citação válida e apropriada (Lovász–Szegedy 2006). |
| 008 | Boa-colocação multilinear (De Silva–Lim) | ✅ Correto. Compacidade de Tychonoff + Weierstrass + multiplicadores de Lagrange corretamente aplicados; hipóteses descarregadas. |
| 009 | Dualidade/compacidade de hipergraphons | ✅ Correto, generalização consistente ($2^k$ em vez de $4=2^2$). |
| 010 | Estabilidade Dirichlet em atenção | ✅ Aceitável (mergulho de Sobolev $H^2(\Tor^2)\hookrightarrow C^{0,\alpha}$ é padrão em $d=2$; desigualdade de Morrey/Agmon citada corretamente). |
| 011 | Kac–Rice para tensores | ⚠️ Prova é um *esboço* apoiado inteiramente em citação (Auffinger–Ben Arous–Černý), sem derivação própria — aceitável como restatement, mas deveria ser rotulado "(after ...)". |
| 012 | Concentração sub-Gaussiana | ⚠️ Mesmo padrão de 011. Além disso, a alegação de **unicidade** de $\alpha_k=(k-1)/2$ na parte (i) não é demonstrada — apenas se mostra que essa escala garante $\Theta(1)$; ausência de argumento mostrando falha de outras escalas. Gap genuíno, porém menor. |

**Afiliação institucional**: conforme exatamente ao padrão obrigatório (DES/PPGEE/UFLA). ✅

**Aciclicidade do DAG de dependências internas**: verificada — grafo é um DAG simples (Thm 4.5 depende de Thm 4.4; Thm 5.3 generaliza o método de prova de Thm 4.9; Seção 6 só referencia retroativamente). Nenhum ciclo. ✅

---

## 2. ACHADO CRÍTICO (BLOQUEANTE): Vacuidade semântica e desconexão de build no Lean 4

Isto é o achado dominante desta auditoria.

**2.1 — Todas as 12 "provas" formais são logicamente vazias (petitio principii).**
Cada teorema Lean segue o mesmo padrão: define-se uma `structure` cujo campo de hipótese **já é** a conclusão do teorema, e a "prova" é um `exact` trivial nesse campo:

```lean
structure PermutedRealization where
  ...
  h_amp : dirichlet_perm ≥ dirichlet_orig      -- hipótese = conclusão

theorem spectral_blindness_dirichlet (P : PermutedRealization) :
    P.dirichlet_perm ≥ P.dirichlet_orig := by
  exact P.h_amp                                 -- vacuidade
```

Nenhum objeto matemático substantivo do enunciado real está presente: não há $\mathbb{R}$, integrais, $L^p$/$H^s$/BV, medidas de Hausdorff, esferas, hessianos, autovetores, ou desigualdades de concentração. Tudo é `Nat`/`Int`/`Bool` opaco. Casos mais graves:

- **OBL-BTS1-003 e OBL-BTS1-004** (`step_realization_total_variation` e `coarea_hausdorff_level_curves`) usam a **mesma** `structure`, a **mesma** hipótese e o **mesmo** termo de prova — apesar de formalizarem dois teoremas matematicamente distintos (fórmula explícita de TV vs. identidade de Coarea/Hausdorff).
- **OBL-BTS1-005** (`morse_spectrum_euler_characteristic`) reduz-se a `rfl` sobre uma definição igual a si mesma — não codifica pontos críticos, pares antipodais, nem índice de Morse algum.

**2.2 — O arquivo não está no grafo de build do próprio pacote.**
`lakefile.lean` declara `lean_lib «BTS3»` **sem** `globs`/`roots`, e não existe nenhum arquivo `BTS3.lean` em lugar algum da árvore — apenas o diretório `BTS/` (namespace diferente). `Main.lean` contém somente `import BTS3`. Pelas regras padrão de resolução de módulos do Lake, isso significa que:
- `import BTS3` não resolve para nenhum arquivo em disco;
- os arquivos em `BTS/` (incluindo `Volume1_FunctionalRealizations.lean`) não são alcançáveis pelo alvo de build declarado do pacote.

Tentei confirmar isso empiricamente via `lake build` (toolchain Lean/Lake está instalado — `elan`, `lake`, `lean` presentes), mas o comando exigiu aprovação interativa que não foi concedida nesta sessão. A evidência estática por si só já é suficiente para concluir que o pipeline de build **como configurado** não exercita este arquivo — recomendo que o autor rode `lake build` diretamente para obter o traço de erro definitivo.

**2.3 — Padrão sistêmico.** O mesmo anti-padrão (hipótese = conclusão) foi encontrado em `BTS/FedererReach.lean` (OBL-020/021), indicando que isto não é um defeito isolado do Volume I, mas um padrão de autoria em toda a suíte `formal_proofs_bts`.

**Consequência**: a alegação do manuscrito (§"Formal Verification and Code Availability", linha 789) de que o framework foi "formally verified in Lean 4 ... with zero sorry statements" **não é sustentada** pelo artefato em disco — nem no sentido de correção lógica (as provas não verificam conteúdo, apenas ecoam hipóteses), nem no sentido de compilação efetiva (arquivo fora do grafo de build declarado).

---

## 3. ACHADO MODERADO: Numeração das obrigações não corresponde à numeração automática real do LaTeX

O preâmbulo compartilha o contador entre Theorem/Lemma/Proposition/Corollary **e também** Definition/Example/Remark/Construction (via `\newtheorem{definition}[theorem]{Definition}` etc.), resetado por seção. Contando manualmente cada ambiente na ordem do documento:

| Obrigação (rótulo alegado) | Numeração real no PDF compilado |
|---|---|
| OBL-BTS1-001 "Prop 2.2" | **Proposition 3.3** |
| OBL-BTS1-002 "Thm 3.1" | **Theorem 4.1** |
| OBL-BTS1-003 "Thm 3.2" | **Theorem 4.4** |
| OBL-BTS1-004 "Thm 3.3" | **Theorem 4.5** |
| OBL-BTS1-005 "Thm 3.4" | **Theorem 4.6** |
| OBL-BTS1-006 "Thm 4.1" | **Theorem 4.9** |
| OBL-BTS1-007 "Thm 4.2" | **Theorem 4.10** |
| OBL-BTS1-008 "Thm 4.3" | **Theorem 5.1** |
| OBL-BTS1-009 "Thm 4.4" | **Theorem 5.3** |
| OBL-BTS1-010 "Thm 5.1" | **Theorem 5.4** |
| OBL-BTS1-011 "Thm 5.2" | **Theorem 5.5** |
| OBL-BTS1-012 "Thm 5.3" | **Theorem 5.6** |

Todas as 12 obrigações estão deslocadas. Isso quebra a rastreabilidade exigida pelo protocolo ("verificar hipótese descarregada para cada teorema correspondente às obrigações listadas") — o próprio arquivo Lean repete esses rótulos incorretos em seus comentários de cabeçalho.

**Correção proposta**: atribuir `\label{}` explícito a cada ambiente teorema-símile e fazer o ledger de obrigações referenciar a chave do `\label` (já existem várias, ex. `thm:dirichlet_blindness`, `thm:tv_matrix`) em vez de números contados à mão, que ficam obsoletos a cada edição.

---

## 4. SÍNTESE

- O **conteúdo matemático puro** do Volume I (Seções 2–4, obrigações 1–9) é rigoroso, dimensionalmente consistente e corretamente fundamentado na literatura citada.
- Duas obrigações (011, 012) contêm gaps menores de rigor (prova por citação sem derivação própria; alegação de unicidade não demonstrada).
- A **camada de verificação formal Lean 4** é semanticamente vazia para as 12 obrigações e, pela configuração do Lake, não está sequer no grafo de compilação do pacote — isso é bloqueante frente ao requisito estrito de "compilar com 0 erros e 0 sorry" como evidência de verificação formal genuína.
- A **numeração de referência** das obrigações não corresponde à numeração automática real do documento.

---

VERDICT: REVISE

**Pontos que exigem correção antes de nova submissão:**
1. Reescrever as 12 provas em `Volume1_FunctionalRealizations.lean` para formalizar o conteúdo matemático real (tipos em `ℝ`/`EuclideanSpace`/medida, não `Nat`/`Bool` com hipótese-igual-a-conclusão), ou re-rotular explicitamente o arquivo como "protocolo/esqueleto de obrigações" (não como "verificação formal").
2. Corrigir `lakefile.lean` (adicionar `globs := #[.submodules \`BTS]` ou equivalente) e `Main.lean` (`import BTS.Volume1_FunctionalRealizations`) para que o arquivo entre de fato no alvo de build padrão; confirmar com `lake build` retornando 0 erros/0 sorry.
3. Eliminar a duplicação idêntica entre OBL-BTS1-003 e OBL-BTS1-004.
4. Sincronizar o ledger de obrigações com os `\label`s reais do LaTeX (tabela da Seção 3 acima).
5. (Menor) Adicionar qualificador "(after Auffinger–Ben Arous–Černý)" / "(after Lévy–Gromov)" aos Thms 5.5–5.6, e fechar o gap de unicidade no Thm 5.6(i).