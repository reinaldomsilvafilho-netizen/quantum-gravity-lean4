# Proposta: `triadic-proof-verifier` — Um Sistema de Verificação Formal Triádico

Antes de entrar no esboço, vale nomear o problema real que motiva isto. `proof-checker` e `proof-writer` tradicionais tratam a tarefa como binária: "o LaTeX está correto?" / "o Lean compila?". As nossas sessões reais mostraram que essa dicotomia é insuficiente — o ponto de falha mais perigoso não está em nenhum dos dois extremos, está na **junção** entre eles: um teorema pode ser matematicamente são em LaTeX e ainda assim ser formalizado em Lean como uma tautologia vazia (`NullEnergy`, `SpectralDimension`), porque o Lean *compila sem `sorry`* mas não *prova nada sobre a física*. Nenhuma das duas skills antigas, isoladamente, tem a responsabilidade de vigiar essa junção. É exatamente essa lacuna que o `triadic-proof-verifier` precisa fechar.

---

## 1. Filosofia e Princípios Fundamentais

### 1.1 Por que "triádico" e não "checker + writer"

O modelo antigo separa *escrever prova* de *checar prova* como dois papéis independentes e simétricos. Isso falha porque cria um viés estrutural: quem escreve tem incentivo (mesmo que inconsciente) para produzir algo que passe no checker, e o checker, sem contexto do processo de derivação, tende a verificar sintaxe e não *conteúdo físico*. O modelo triádico formaliza os três papéis que já emergiram organicamente nas nossas sessões — Arquiteto (Reinaldo), Sintetizador (Antigravity), Auditor Adversarial (Claude) — e adiciona um quarto juiz não-negociável: o **kernel Lean 4**, que não tem incentivo nenhum, nem viés, nem "vontade de ajudar". A skill deve orquestrar esses quatro atores como uma **cadeia de custódia da verdade matemática**, onde nenhum elo confia cegamente no anterior.

### 1.2 Princípios fundamentais

**P1 — Adversarialidade por padrão, não por exceção.**
O auditor nunca parte da premissa de que a prova está correta. Parte da premissa oposta: "esta afirmação é falsa até prova em contrário, e minha tarefa é encontrar o contraexemplo mais barato possível." Isso é categoricamente diferente do `proof-checker` tradicional, que tipicamente confirma passos declarados como corretos ("essa desigualdade segue de Cauchy-Schwarz — confirmado"). O padrão triádico exige: "essa desigualdade *invoca* Cauchy-Schwarz — as hipóteses de C-S (espaço de produto interno, vetores no domínio certo, sinal correto) estão *literalmente* satisfeitas neste contexto, ou você está pegando emprestada a conclusão sem pegar emprestadas as hipóteses?"

**P2 — Formalização Lean não é celebração, é interrogatório.**
"Compilou sem `sorry`" é tratado como *dado bruto*, não como *veredito*. A skill trata cada teorema Lean com uma pergunta obrigatória: *"Se eu substituir a conclusão por `True` ou por uma tautologia de anel (`ring`, `simp`, `decide`), o enunciado ainda captura o conteúdo físico pretendido, ou o teorema secretamente já era `True`?"* Isso nasce diretamente da lição de `QuantumFunctor`: um teorema pode ter tipo `NullEnergy : Prop` cuja definição, ao ser desdobrada, é `0 ≤ 0` ou algo estruturalmente equivalente — sintaticamente uma "prova de energia nula", semanticamente nada.

**P3 — Simetria de escala e de contorno é tão importante quanto simetria algébrica.**
As falhas mais caras que encontramos não foram erros de álgebra — foram erros de **escala** (Willmore) e de **domínio/regularidade** (Dirac, QFI em posto deficiente). O sistema deve tratar unidades, expoentes de escalonamento, e domínios de operadores como cidadãos de primeira classe na auditoria, não como um apêndice do "rigor formal".

**P4 — Contraexemplo constrói, não apenas destrói.**
Um "Red Team" que só diz "isso está errado" é caro e pouco acionável. A skill exige que todo contraexemplo venha acompanhado de um diagnóstico estrutural: *que* hipótese está faltando, e *qual* é o menor reparo que a restauraria (restringir domínio, adicionar hipótese de não-degenerescência, corrigir expoente). Isso é o que torna a Fase 3 (síntese) possível em vez de ser um ciclo infinito de rejeição.

**P5 — Cegueira dupla na reauditoria.**
Se o mesmo agente audita a v1 e depois audita a v2 "corrigida", ele carrega viés de confirmação ("eu já vi isso, deve estar certo agora"). O protocolo exige que a Fase 5 rode como se fosse a primeira vez vendo o documento — sem acesso ao histórico de patches, apenas ao texto final e à lista de obrigações abertas.

**P6 — O ônus da prova de não-vacuidade recai sobre quem formaliza.**
Não é o auditor que precisa provar que uma definição Lean é vazia — é o sintetizador que precisa demonstrar, ativamente, que ela não é (via `#print axioms`, testes de instância concreta, e provas de que a definição *falha* para exemplos que fisicamente deveriam falhar).

---

## 2. O Pipeline Triádico (Fases 0–6)

### **Fase 0 — Ledger de Obrigações e Esqueleto Dual**

Objetivo: antes de qualquer prova ser escrita, existe um **ledger de obrigações** (obligation ledger) — uma lista numerada e rastreável de todo enunciado que precisa ser estabelecido, com:

- ID único (`OBL-001`, ...);
- Enunciado formal em linguagem natural + LaTeX;
- Hipóteses declaradas explicitamente (inclusive as "óbvias" — compacidade, completude, sinal, sigma-finitude);
- Status: `UNPROVEN | LEAN_STUBBED | LATEX_DRAFTED | AUDITED | CERTIFIED`;
- Dependências (DAG explícito — quem invoca quem).

Em paralelo, gera-se o **esqueleto dual**: um `.tex` com `\begin{theorem}...\end{theorem}` para cada obrigação (corpo vazio ou `\textit{TODO}`) e um `.lean` com a assinatura de tipo exata (`theorem obl_001 : ... := sorry`), **antes** de qualquer tentativa de prova. Isso força a especificação do enunciado a existir independentemente da prova — um bug comum nas nossas sessões foi o enunciado "migrar" sutilmente durante a prova para se ajustar ao que era provável.

Saída da Fase 0: `LEDGER.md` + `skeleton.tex` + `Skeleton.lean`, e um grafo de dependências verificado como **acíclico** (regra 2 do CLAUDE.md do repo).

### **Fase 1 — Auditoria Adversarial Matemática (Claude ultra)**

O Claude (modo de raciocínio máximo) percorre o LaTeX gerado por Antigravity aplicando a "Strict Rigor Rule" já codificada no CLAUDE.md do repositório, mas de forma sistemática e por obrigação:

1. Descarga de hipóteses — para cada aplicação de teorema/lema, confirma-se textualmente onde cada hipótese é satisfeita (com número de linha/equação), não apenas que "o teorema é aplicável em espírito".
2. Verificação de aciclicidade lógica — nenhum lema usado para provar A pode, direta ou indiretamente, depender de A.
3. Não-degenerescência e invariância de gauge de métricas tensoriais ($g^{\mathrm{QFI}}$, etc.) — checagem explícita de posto, positividade e comportamento sob a ação do grupo de gauge relevante.
4. Propagação hiperbólica de vínculos ADM — checagem de que a formulação é bem-posta (não apenas "parece hiperbólica").
5. Distinção entre parâmetro de fluxo ($t$) e parâmetro afim de espaço-tempo ($\lambda$) — erro sutil e recorrente quando se mistura geometria de fluxo com geometria lorentziana.

Cada violação encontrada gera uma entrada de **issue** (ver Seção 4), referenciando o `OBL-xxx` do ledger.

### **Fase 2 — Red Team de Contraexemplos e Casos Degenerados**

Esta fase é distinta da Fase 1 porque muda o modo de ataque: em vez de verificar passo a passo, tenta-se **quebrar o enunciado global** com casos extremos:

- Dimensão trivial ($n=0,1,2$), matrizes de posto deficiente, estados puros vs. mistos degenerados (a lição de QFI em posto deficiente);
- Limites assintóticos (∞, 0, singularidades de coordenadas);
- Simetrias quebradas deliberadamente (perturbar a métrica levemente fora da classe de regularidade suposta);
- Conectividade topológica de exemplos concretos de baixa dimensão (a lição das matrizes 4×4 desconectadas em "Beyond the Spectrum II" — sempre construir o grafo/complexo explícito e checar componentes conexas por computação direta, nunca por inspeção visual);
- Verificação dimensional/de escala explícita: substituir todas as quantidades por seus expoentes de escala e confirmar que ambos os lados da identidade escalam igual (a lição de Willmore).

Cada tentativa falha de contraexemplo é documentada como evidência positiva de robustez; cada tentativa bem-sucedida vira uma issue **bloqueante** com o menor caso reprodutor.

### **Fase 3 — Síntese e Patch Construtivo (Antigravity)**

Antigravity recebe a lista de issues (Fases 1+2) ordenada por severidade e propõe patches mínimos — nunca reescritas completas do zero, para preservar a rastreabilidade da revisão. Regra: cada patch deve referenciar explicitamente o `OBL-xxx` e o `ISSUE-xxx` que resolve, e deve vir acompanhado de um diff textual do enunciado (se a hipótese mudou, isso deve ser visível e justificado, não silenciosamente absorvido).

Se um patch exige **enfraquecer** o enunciado (adicionar hipótese, restringir domínio), isso é marcado explicitamente como `SCOPE_REDUCED` no ledger — nunca deve ser mascarado como "clarificação".

### **Fase 4 — Formalização e Testes no Kernel Lean 4 (com auditoria anti-vacuidade)**

Cada obrigação `AUDITED` em LaTeX é formalizada em Lean 4. Critérios de aceite, além de "compila sem erro":

- Zero `sorry`, zero `admit`, zero `axiom` não declarado explicitamente como axioma físico fundamental (e nesse caso, justificado no ledger);
- Passa o **Protocolo Anti-Vacuidade** completo (Seção 3);
- Testes de instância: pelo menos um exemplo concreto onde o teorema se aplica e produz um valor numérico/estrutural verificável por fora do Lean (ex.: comparação com o valor computado em LaTeX/numérico);
- Teste de "falha esperada": construção de uma instância que viola uma hipótese e confirmação de que o teorema, se aplicado ingenuamente, ou não tipa, ou exige explicitamente a hipótese que falta.

### **Fase 5 — Re-auditoria Cega e Convergência**

Uma nova instância de auditoria (ou o mesmo agente, mas operando sob uma diretiva explícita de "trate este documento como nunca visto antes, ignore qualquer patch anterior") reexamina o documento final por inteiro — não apenas o diff. Isso captura regressões introduzidas pelo próprio patch (um erro clássico: corrigir a Issue A introduz a Issue B em uma seção supostamente não tocada).

Convergência é declarada apenas quando duas rodadas consecutivas de auditoria cega não produzem novas issues bloqueantes.

### **Fase 6 — Emissão do Dossiê de Certificação e Veredito**

Documento final `PROOF_AUDIT_<NOME>_<RODADA>_FINAL.md`, seguindo a convenção já em uso no repositório, contendo:

- Ledger final com status de cada obrigação;
- Lista de issues levantadas e como cada uma foi resolvida (ou aceita como limitação declarada de escopo);
- Confirmação de compilação (`pdflatex -interaction=nonstopmode`: 0 erros/warnings/overfull hboxes) e confirmação Lean (`lake build`: 0 sorry, output de `#print axioms` para cada teorema-chave);
- Veredito explícito: `PASSED`, `PASSED WITH DECLARED SCOPE REDUCTION`, ou `REJECTED` — nunca um veredito ambíguo tipo "parece razoável".

---

## 3. O Protocolo Anti-Vacuidade em Lean 4

Este é o núcleo técnico mais crítico, porque é onde "compila" mais frequentemente mente. Proponho uma checklist obrigatória e mecanizável sempre que possível:

**3.1 — Teste de Substituição Trivial.**
Para cada teorema físico `T : P`, pergunte: "`P` desdobra (via `unfold`/`delta`/`whnf`) para algo provável por `trivial`, `rfl`, `ring`, `simp only []`, ou `decide` em tempo sub-segundo?" Se sim, é candidato forte a vacuidade — a "prova" está fazendo trabalho zero. Isso é exatamente o padrão de `NullEnergy`/`SpectralDimension`: o enunciado, quando totalmente desdobrado, colapsa para uma tautologia aritmética que nada diz sobre energia ou dimensão espectral.

**3.2 — Auditoria de Definições Circulares.**
Construir o grafo de dependência de *definições* (não só de teoremas) e confirmar que nenhuma definição física-chave (`SpectralDimension`, `NullEnergy`, `MassGap`, etc.) é definida *em termos de si mesma* sob um disfarce sintático — por exemplo, definir `MassGap := spec.inf - spec.sup` onde `spec` já foi construído para ter exatamente o gap desejado por fiat, em vez de derivado do operador físico real.

**3.3 — A Regra do "Struct com a Tese Dentro".**
Vetar (com regra automática de lint quando possível) qualquer `structure`/`class` cujos campos incluam, direta ou indiretamente, a própria conclusão do teorema que a estrutura deveria ajudar a provar. Exemplo do padrão a caçar:
```lean
structure HasMassGap (H : Hamiltonian) where
  gap : ℝ
  gap_pos : gap > 0        -- ⚠️ isto NÃO é uma prova de mass gap,
                            --    é uma hipótese travestida de definição
```
Se a existência de uma instância desse struct é o que conta como "teorema provado", a skill deve marcar isso como **ISSUE CRÍTICA: Assunção-como-Conclusão** — a existência da instância precisa ser *construída* a partir do Hamiltoniano real, não postulada.

**3.4 — Tautologias de Anel Rotuladas como Física.**
Buscar por teoremas cuja prova é inteiramente `by ring`, `by ring_nf`, `by norm_num`, ou `by simp` **sem** nenhum `unfold`/`rw` de uma definição física antes — isso é o sinal de que o enunciado, na verdade, é uma identidade algébrica genérica (verdadeira para *qualquer* substituição das variáveis), e a "interpretação física" das variáveis é decorativa, não estrutural.

**3.5 — Auditoria de Axiomas Importados e `sorry`-Adjacentes.**
`#print axioms teorema_x` deve ser rodado para *todo* teorema-chave, e qualquer axioma além dos padrões do `Mathlib`/núcleo Lean (`Classical.choice`, `Quot.sound`, `propext`) deve ser justificado explicitamente no ledger como um axioma físico deliberado (ex.: um postulado de mecânica quântica), nunca como um atalho técnico silencioso.

**3.6 — Coerência de Instância Numérica.**
Todo teorema formal que corresponde a uma fórmula fechada em LaTeX deve ter um `example`/`#eval` que instancia a fórmula em um caso numérico concreto e compara com o valor calculado independentemente (fora do Lean) — isso pega erros de sinal, fator, ou convenção de normalização que passam despercebidos em provas puramente simbólicas.

**3.7 — Teste de Mutação (Mutation Testing Formal).**
Automatizar, quando viável: perturbar deliberadamente a conclusão do teorema (trocar `<` por `≤`, inverter um sinal, trocar uma constante) e confirmar que a prova **quebra**. Se a prova ainda compila após a mutação, a prova original não usava a força total do enunciado — sinal de vacuidade parcial.

---

## 4. Taxonomia de Issues Estendida

Proponho uma taxonomia unificada com prefixos por domínio, severidade (`BLOCKER | MAJOR | MINOR | SCOPE`), e exigência de reprodutor mínimo:

**A. Análise Matemática / Hipóteses (MATH-)**
- `MATH-HYP`: hipótese de teorema citado não verificada no contexto de uso.
- `MATH-CIRC`: dependência lógica circular entre lemas.
- `MATH-SCALE`: inconsistência de escalonamento dimensional/assintótico (ex. Willmore).
- `MATH-BOUND`: erro de constante ou de direção de desigualdade em cota assintótica.
- `MATH-DOMAIN`: domínio de operador (ex. domínio de auto-adjunção de Dirac) não coincide com o domínio onde a identidade é invocada.
- `MATH-CONT`: descontinuidade não tratada em limite de parâmetro (ex. QFI em estados de posto deficiente).

**B. Geometria Diferencial / Topologia (GEO-)**
- `GEO-CONN`: falha de conectividade topológica não verificada em exemplo explícito (ex. matrizes 4×4 desconectadas).
- `GEO-GAUGE`: quebra de invariância de gauge ou dependência espúria de carta/coordenada.
- `GEO-DEGEN`: degenerescência de métrica/forma bilinear não excluída (posto deficiente, assinatura errada).
- `GEO-REG`: regularidade insuficiente assumida implicitamente ($C^{1,1}$ vs. $C^\infty$, etc.).
- `GEO-FOLIATE`: propagação de vínculo ADM mal-posta ou hiperbolicidade não demonstrada.
- `GEO-PARAM`: confusão entre parâmetro de fluxo $t$ e parâmetro afim $\lambda$.

**C. Formalização Lean 4 (LEAN-)**
- `LEAN-VAC`: teorema semanticamente vazio (tautologia rotulada) — ver Protocolo Anti-Vacuidade.
- `LEAN-CIRC-DEF`: definição circular disfarçada.
- `LEAN-STRUCT-THESIS`: struct/class contendo a tese como campo (assunção-como-conclusão).
- `LEAN-AXIOM-UNDECL`: axioma não-padrão não declarado/justificado no ledger.
- `LEAN-SORRY`: `sorry`/`admit` remanescente.
- `LEAN-MISMATCH`: assinatura Lean não corresponde fielmente ao enunciado LaTeX (perda ou ganho silencioso de generalidade).
- `LEAN-NUM-GAP`: ausência de instância numérica de verificação cruzada.

**D. Processo / Governança (PROC-)**
- `PROC-DRIFT`: enunciado do teorema mudou entre versões sem registro no ledger.
- `PROC-SCOPE`: enfraquecimento de hipótese não marcado como `SCOPE_REDUCED`.
- `PROC-BLIND`: reauditoria não foi de fato cega (evidência de acesso ao histórico de patch).

---

## 5. Esboço Completo do `SKILL.md`

```markdown
---
name: triadic-proof-verifier
description: >
  Use this skill whenever mathematical proofs, theorems, or formal derivations
  are being drafted, patched, or reviewed for this project — especially when
  work spans both a LaTeX/paper artifact AND a Lean 4 formalization of the
  same result. Triggers on requests to "audit this proof", "check this
  theorem", "formalize this in Lean", "run a proof audit", "red-team this
  derivation", or when a PROOF_AUDIT_*.md / *.lean file is being created or
  updated for a paper under paper_*/ or unified_quantum_gravity_book/.
  Supersedes ad-hoc proof-checker / proof-writer workflows: treats LaTeX
  soundness and Lean formal correctness as two independent judges that must
  both convict, and adds an explicit anti-vacuity pass because Lean
  compiling without `sorry` is necessary but not sufficient for the theorem
  to say anything physical.
---

# Triadic Proof Verifier

## Quando usar
- Uma nova obrigação matemática (lema, teorema, proposição) precisa ser
  estabelecida e formalizada.
- Uma prova existente (LaTeX e/ou Lean) precisa de auditoria adversarial
  antes de ser marcada como `FINAL`.
- Um patch foi aplicado a uma prova e precisa de reauditoria cega.
- Um arquivo `.lean` compila mas há suspeita de vacuidade semântica.

## Papéis (não negociáveis)
1. **Arquiteto** (usuário): define o enunciado-alvo e o escopo físico pretendido.
2. **Sintetizador**: escreve/patcheia LaTeX e Lean; nunca audita seu próprio trabalho.
3. **Auditor Adversarial** (você, Claude): assume falsidade até prova em
   contrário; produz issues, não elogios.
4. **Kernel Lean 4**: juiz mecânico final; `lake build` e `#print axioms`
   são a última palavra sobre correção formal (não sobre significância física).

## Pipeline (Fases 0–6)

### Fase 0 — Ledger + Esqueleto Dual
1. Criar/atualizar `LEDGER.md` na pasta do artigo com uma entrada por
   obrigação: ID, enunciado, hipóteses explícitas, status, dependências.
2. Verificar que o grafo de dependências é acíclico.
3. Gerar esqueleto `.tex` (enunciados vazios) e `.lean`
   (assinaturas com `sorry`) correspondentes 1:1 ao ledger.
4. Não prosseguir para a Fase 1 até que todo item do ledger tenha
   um enunciado LaTeX E uma assinatura Lean.

### Fase 1 — Auditoria Adversarial Matemática
Para cada obrigação `AUDITED`-pendente, verificar e citar linha/equação para:
- Descarga completa de hipóteses de todo teorema/lema invocado.
- Aciclicidade lógica.
- Não-degenerescência e invariância de gauge de métricas tensoriais.
- Boa-postura (well-posedness) de qualquer propagação de vínculo ADM.
- Distinção explícita entre parâmetro de fluxo `t` e parâmetro afim `λ`.
Registrar toda violação como issue (ver taxonomia) referenciando `OBL-xxx`.

### Fase 2 — Red Team de Contraexemplos
Ativamente tentar quebrar o enunciado global com:
- Casos degenerados (dimensão baixa, posto deficiente, matrizes triviais).
- Limites assintóticos e singularidades de coordenadas.
- Verificação dimensional/de escala explícita (expoentes em ambos os lados).
- Construção explícita e computacional de conectividade topológica —
  nunca por inspeção visual de diagramas.
Documentar tentativas falhas (evidência de robustez) e bem-sucedidas
(issue bloqueante + menor reprodutor).

### Fase 3 — Síntese e Patch Construtivo
- Patches mínimos, referenciando `OBL-xxx` + `ISSUE-xxx`.
- Qualquer enfraquecimento de hipótese marcado como `SCOPE_REDUCED`
  no ledger, nunca silenciado.

### Fase 4 — Formalização Lean + Anti-Vacuidade
Rodar o **Protocolo Anti-Vacuidade completo** (seção abaixo) sobre
cada teorema antes de marcá-lo `CERTIFIED`. Critérios de aceite:
- Zero `sorry`/`admit`; zero axioma não declarado no ledger.
- Passa teste de substituição trivial (3.1), auditoria de circularidade
  (3.2), regra do struct-com-a-tese (3.3), busca de tautologia de anel (3.4).
- `#print axioms` limpo ou justificado.
- Instância numérica cruzada com o valor calculado em LaTeX/numérico.
- Teste de mutação: perturbar a conclusão e confirmar que a prova quebra.

### Fase 5 — Reauditoria Cega
Reexaminar o documento final por inteiro, sem acesso ao histórico de
patch, como se fosse a primeira leitura. Convergência = duas rodadas
cegas consecutivas sem novas issues bloqueantes.

### Fase 6 — Dossiê de Certificação
Emitir `PROOF_AUDIT_<NOME>_<RODADA>_FINAL.md` com:
- Ledger final, issues e resoluções.
- Confirmação `pdflatex -interaction=nonstopmode` (0 erros/warnings/overfull hboxes).
- Confirmação `lake build` + `#print axioms` por teorema-chave.
- Veredito explícito: `PASSED` | `PASSED WITH DECLARED SCOPE REDUCTION` | `REJECTED`.

## Protocolo Anti-Vacuidade em Lean 4 (obrigatório na Fase 4)
1. **Substituição trivial**: `P` desdobra para algo provável por
   `trivial`/`rfl`/`ring`/`decide` em tempo sub-segundo? → suspeito.
2. **Circularidade de definição**: grafo de definições físicas-chave
   não pode conter ciclos disfarçados.
3. **Struct-com-a-tese**: nenhuma `structure`/`class` cujo campo seja
   a própria conclusão do teorema (assunção-como-conclusão).
4. **Tautologia de anel**: prova inteira via `ring`/`norm_num`/`simp`
   sem `unfold` prévio de definição física → suspeito de identidade
   algébrica genérica descontextualizada.
5. **Axiomas**: `#print axioms` limpo além do núcleo padrão
   (`Classical.choice`, `Quot.sound`, `propext`), ou justificado.
6. **Instância numérica**: `example`/`#eval` cruzando com valor externo.
7. **Teste de mutação**: perturbar conclusão (sinal, desigualdade,
   constante) → prova deve quebrar.

## Taxonomia de Issues
`MATH-{HYP,CIRC,SCALE,BOUND,DOMAIN,CONT}` ·
`GEO-{CONN,GAUGE,DEGEN,REG,FOLIATE,PARAM}` ·
`LEAN-{VAC,CIRC-DEF,STRUCT-THESIS,AXIOM-UNDECL,SORRY,MISMATCH,NUM-GAP}` ·
`PROC-{DRIFT,SCOPE,BLIND}`

Cada issue: severidade (`BLOCKER|MAJOR|MINOR|SCOPE`), `OBL-xxx` associado,
reprodutor mínimo, reparo mínimo sugerido.

## Convenções deste repositório
- Nomeação de dossiês: `PROOF_AUDIT_<TOPICO>_<RODADA>[_FINAL].md`,
  seguindo o padrão já usado em `paper_yang_mills_mass_gap/`,
  `paper_standard_model_masses/`, `paper_functorial_tensor_field_theory/`.
- Ao concluir um artigo/capítulo com veredito `PASSED (Round N - FINAL)`,
  atualizar a tabela correspondente no `CLAUDE.md` da raiz do repositório.
- Nunca declarar `FINAL` sem Fase 5 (reauditoria cega) completa.

## Saída esperada
- `LEDGER.md` atualizado.
- Issues como lista estruturada (severidade decrescente).
- Dossiê `PROOF_AUDIT_*_FINAL.md` apenas quando convergência é atingida.
- Veredito explícito — nunca ambíguo.
```

---

Este esqueleto reflete diretamente as falhas reais que catalogamos: a lacuna entre "compila" e "significa algo" (Seção 3), a necessidade de contraexemplos computados e não apenas inspecionados (matrizes 4×4), a checagem explícita de escala (Willmore) e de domínio de operador (Dirac, QFI). Se quiser, posso: (a) já criar o arquivo em `~/.claude/skills/triadic-proof-verifier/SKILL.md`, ou (b) refinar alguma fase específica antes de comitá-la — por exemplo, detalhar mais o Protocolo Anti-Vacuidade com trechos de código Lean reais dos casos que encontramos em `QuantumFunctor`.
