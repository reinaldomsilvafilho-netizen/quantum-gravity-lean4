Confirmado exatamente como suspeitei. Agora tenho evidência suficiente (código-fonte real em disco, artefatos `.olean` mais recentes que os `.lean`, ausência total de `sorry`/`axiom`/`native_decide`) para redigir o parecer adversarial completo.

---

# AUDITORIA ADVERSARIAL INDEPENDENTE — Pacote Lean 4 "QuantumFunctor"

**Nota metodológica**: não consegui executar `lake build` diretamente nesta sessão (a permissão do ambiente bloqueou o comando), mas verifiquei a compilação por evidência indireta forte: todo `.olean` em `.lake/build/lib/lean/` é **posterior** ao `.lean` correspondente (incluindo os editados por último, `SimplicialHodge.lean` e `WheelerDeWitt.lean` às 21:50–21:55, com `.olean` gerado às 21:56), `grep` full-text não encontra `sorry`, `axiom`, `native_decide` ou `unsafe` em nenhum arquivo, e `lake-manifest.json` mostra `"packages": []` (nenhuma dependência externa, nem Mathlib — pacote 100% autocontido). Isso corrobora a alegação de "0 sorry / 0 axioma / compila". O que segue não questiona se o kernel aceitou as provas — quase certamente aceitou —, mas se o **conteúdo matemático/físico** de cada teorema corresponde ao que a prosa (README, `Main.lean`) alega.

## 1. Solidez Lógica & Ausência de Falácias

Aqui está o achado mais sério do pacote, e ele se repete em dois lugares.

### 1.1 `NullEnergy.lean` — circularidade definicional (petitio principii)

```
structure HilbertSchmidtVector (chi : Nat) where
  components : List Float
  norm_sq : Float
  norm_nonneg : norm_sq ≥ 0.0 := by decide   -- linha 11
...
theorem null_energy_condition ... :
    nullStressContraction chi nabla_k_psi ≥ 0.0 := by
  exact nabla_k_psi.norm_nonneg               -- linha 23
```

`norm_sq` é um `Float` **solto**, sem nenhuma equação que o vincule a `components` (não há `norm_sq := components.foldl (·+·^2) 0` ou equivalente a $\mathrm{Tr}(A^\dagger A)$). A não-negatividade é exigida como **campo obrigatório da própria estrutura** que representa "a norma". O "teorema" `null_energy_condition` apenas projeta esse campo de volta. Isso não é uma falácia de vácuo lógico no sentido Curry-Howard clássico (não é `False → P`), mas é uma **petitio principii travestida de física**: o enunciado físico não-trivial — que $\|A\|_{HS}^2 = \mathrm{Tr}(A^\dagger A)\ge 0$ *porque* é soma de módulos ao quadrado — nunca é formalizado. Comparar com o rótulo do `Main.lean` ("Hilbert-Schmidt norm semi-positivity: PROVEN") é uma sobre-alegação: o que está provado é "se você assumir que uma norma é não-negativa, ela é não-negativa". Correção recomendada: definir `norm_sq` como uma função real de `components` (soma de quadrados) e provar `≥0` a partir do `List.foldl` — aí sim seria um teorema genuíno, e trivial de provar via `induction` em `components`.

### 1.2 `SpectralDimension.lean`, Teorema 4.8 — mesma falácia, disfarçada de kernel de calor

```
def ds_num (k : Int) : Int := 4 + 2 * k
def ds_den (k : Int) : Int := 1 + k
...
theorem ir_heat_kernel_quadratic_cancellation (asymp : DiffusionAsymptotics) :
    (1 - asymp.X) + (asymp.X + 3 + asymp.tail_error) = 4 + asymp.tail_error := by omega
```

`ds_num`/`ds_den` **são** a resposta $(4+2k)/(1+k)$ postulada como `def`, não derivada de um cálculo espectral/kernel de calor real (não há operador de difusão, nem série de Seeley-DeWitt, nem traço). Os "Teoremas" 4.1–4.7 são então fatos algébricos triviais sobre essa fração racional já escolhida a dedo — corretos, mas conteúdo-vazios do ponto de vista físico. O pior caso é o 4.8: `(1-X)+(X+3+e) = 4+e` é uma tautologia de anel válida para **quaisquer** inteiros `X`, `e` — não usa absolutamente nada sobre `X` ser "a divergência quadrática de Lifshitz". Chamá-lo de "Exact Quadratic Cancellation in the IR Heat Kernel Limit" é retórica que a prova não sustenta. Isso é o mesmo padrão de 1.1: uma identidade algébrica genérica etiquetada com nome de física.

### 1.3 Campos `Bool` inertes fingindo ser vínculos físicos

```
qfi_nondegenerate : Bool := true      -- CTensMan.lean:24
adm_on_shell      : Bool := true      -- CTensMan.lean:25
positive_definite : Bool := true      -- Cobordism.lean:16
einstein_satisfied: Bool := true      -- Cobordism.lean:23
```
e em `EmergentFunctor.lean:23-24` / `MonoidalCoherence.lean:59-60`, `stepMap`/`cobordismTranspose` **fixam** `adm_lapse_smooth := true, einstein_satisfied := true` incondicionalmente, independente do `FlowStep` de entrada (que nem tem esses campos). Não há nenhuma equação de Einstein, nenhum vínculo ADM real sendo computado — são *tags* booleanas nunca falsificáveis. Isso não é uma falácia lógica (nenhuma prova depende de premissas contraditórias), mas é **conteúdo físico ausente**: os "teoremas" de preservação (5.2, 5.3) preservam rótulos, não física.

Não encontrei nenhum axioma `axiom`, nenhum `sorry`, nenhum `native_decide`/`unsafe`, nenhuma inconsistência lógica genuína (nada do tipo `h : False` escondido, nenhum uso de decidability espúria). O pacote é **logicamente são** — o problema é de **fidelidade referencial** entre o que é provado e o que a prosa alega, não de corretude formal.

## 2. Qualidade da Formalização

### Categorias de caminhos livres (Tier 2)
A construção `Path`/`pathConcat`/`pathConcat_nil`/`pathConcat_assoc` (`Category.lean`) é a construção padrão e correta de **categoria livre sobre um quiver** — tecnicamente impecável, com identidades estritas por `rfl` (evitando setoides pesados, exatamente como afirmado). Mas é preciso ser honesto sobre o que isso prova: essa construção satisfaz os axiomas de categoria para **qualquer** tipo `Step`, independentemente de física — é um fato genérico de teoria das categorias, não algo específico de `CTensMan`. Mais importante: a Definição 2.1 do artigo fala em morfismos "módulo reparametrização $\mathrm{Diff}^+([0,1],\partial)$" — isto é, um **quociente**. O Lean aqui usa caminhos livres **sem quociente algum**. A parte matematicamente não-trivial da Definição 2.1 (mostrar que a composição é bem definida nas classes de equivalência) está simplesmente ausente. O que é provado é uma afirmação estritamente mais fraca (e mais fácil) do que a anunciada. Isso vale tanto para `CTensMan` quanto para `Cobordism`.

Em contraste, `map_id_preservation`/`map_comp_preservation` em `EmergentFunctor.lean` **são** genuínas — verifiquei manualmente a indução em `mapPath`/`pathConcat`, e o `congr 1; exact ih q` está correto e não é trivial de forma vácua (usa a estrutura indutiva de fato). Esse é o ponto mais forte do Tier 2.

### Operadores adjuntos e nilpotência dual (Tier 3 — `SimplicialHodge.lean`)
Esta é, na minha avaliação, **a parte mais bem executada do pacote**. Verifiquei manualmente, passo a passo, as provas de `up_laplacian_self_adjoint` e `down_laplacian_self_adjoint` (as reescritas via `adj_property`/`inner_symm`) e ambas fecham corretamente — não são `rfl`/`omega` de uma linha, são cadeias de reescrita não-triviais que replicam exatamente o argumento clássico de teoria de Hodge discreta. A axiomatização via `OrderedScalar`/`PreHilbertSpace`/`AdjointPair` é abstrata mas **legítima** (é o mesmo estilo do `InnerProductSpace` de Mathlib: positividade do produto interno é axioma da estrutura, não algo derivado — isso é correto matematicamente, não é uma falha). A cadeia completa (nilpotência do coborde → autoadjunção → decomposição de energia de Dirichlet → semidefinição positiva → ortogonalidade harmônica → coercividade do resolvente) é coerente e reflete corretamente a teoria de Hodge combinatória padrão.//
Ressalva: nenhuma instância concreta de `SimplicialChainSlice` é construída no pacote — nada liga essa álgebra abstrata ao Laplaciano de Kigami do Sierpinski (Cap. 6) ou a um complexo de cadeias real com $\partial$ explícito. É um *esquema de teorema* ("se X satisfaz os axiomas, então Y"), não uma verificação de que os objetos geométricos concretos do tratado satisfazem X.

### Kernel de calor e monotonicidade espectral (Tier 4)
Já coberto em 1.2: tecnicamente correto, fisicamente vazio — as definições `ds_num`/`ds_den` são a conclusão travestida de premissa. Os únicos teoremas com conteúdo não-trivial genuíno de álgebra (ainda que elementar) são 4.4 (monotonicidade estrita, que exige expandir o produto cruzado corretamente — verifiquei a álgebra manualmente e está correta) e a própria demonstração via `omega`/`Int.mul_add` está certa.

### Equivalências variacionais WdW e decomposição de cisalhamento (Tier 5)
Verifiquei manualmente `shear_trace_decomposition`, `minimax_shear_maximal_slicing`, `shear_bounded_by_curvature`, `wheeler_dewitt_stationarity` e `shift_stationarity` — todas as identidades algébricas batem exatamente com a GR real ($K_{ij}K^{ij}=\sigma^2+K^2/3$ em 3D, vínculo hamiltoniano ADM, equivalência estacionariedade↔vínculo via `mul_eq_zero` explorando `volume_factor > 0`). Este tier segue o mesmo padrão do Tier 3: axiomas de positividade (`shear_nonneg`, `rho_nonneg`) são **hipóteses de estrutura**, não derivadas de uma métrica concreta — metodologicamente aceitável (é cálculo tensorial abstrato parametrizado), mas value-add real está nas consequências derivadas, que são corretas e não-triviais.

## 3. Prontidão para Publicação — Veredito Final

**Robustez formal**: sólida. Sem `sorry`, sem axiomas, sem trapaças de decidibilidade, sem inconsistência lógica genuína; evidências de compilação real e recente com o toolchain declarado (`v4.33.1`). Como exercício de Lean 4 per se, é competente — em particular o Tier 3 é elegante.

**Problema central para publicação**: existe um descompasso real entre a retórica física do README/`Main.lean` ("Entropic Null Energy Condition PROVEN", "Exact Quadratic Cancellation in IR Heat Kernel PROVEN", "Category laws... zero axioms") e o que de fato foi formalizado em pelo menos três lugares (NullEnergy, o quociente ausente em CTensMan/Cobordism, e os `def`s postulados de SpectralDimension). Um revisor adversarial de Zenodo/arXiv com formação em métodos formais **vai** encontrar exatamente esses três pontos, e a diferença entre "está errado" e "está sobre-alegado" pode não ser óbvia para um leitor não especialista — o que é o risco reputacional real aqui, não um erro matemático.

**Recomendação antes de publicar**:
1. Em `NullEnergy.lean`, redefinir `norm_sq` como função explícita de `components` (soma de quadrados) e provar a não-negatividade por indução — hoje é ~5 linhas para transformar um teorema circular em um teorema real.
2. Em `CTensMan.lean`/`Cobordism.lean`, ou (a) implementar de fato o quociente por reparametrização (mesmo que como `Setoid`/`Quotient` simples), ou (b) adicionar uma nota explícita no README/comentários dizendo que a formalização usa caminhos livres não-quocientados como simplificação de modelagem, deixando claro que a Definição 2.1 completa (com o quociente) não está formalizada.
3. Em `SpectralDimension.lean`, reescrever a documentação para deixar claro que Tier 4 formaliza **consequências algébricas de uma forma fechada postulada**, não uma derivação a partir do núcleo de calor contínuo — ou renomear teoremas como 4.8 para algo que não invoque "heat kernel" quando a prova é uma tautologia de anel.
4. Adicionar uma seção "Escopo e Limitações" ao README distinguindo claramente: (i) o que é derivado de axiomas físicos explícitos (Tiers 3 e 5 — legítimo, estilo axiomático padrão), de (ii) o que é definição travestida de teorema (Tiers 1 e 4, no ponto 4.8).

Com essas correções (a maioria são poucas linhas de Lean + honestidade textual, não um redesenho), o pacote fica genuinamente pronto para GitHub/Zenodo. **Como está agora**, recomendo não publicar sem ao menos o ajuste do README/comentários (item 3-4 acima, baixo custo) e idealmente também o item 1 (NullEnergy), pois é o achado mais fácil de um revisor externo apontar como "prova vazia".
