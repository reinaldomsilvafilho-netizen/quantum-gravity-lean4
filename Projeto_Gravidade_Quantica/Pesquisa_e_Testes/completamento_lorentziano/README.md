# Completamento lorentziano do operador k² + ℓ²k⁴: levantamento e recomendação

**Status: rascunho (draft) de pesquisa, 2026-09-28.** Ainda não foi verificado de forma independente. Pela regra dos
quatro olhos, nada aqui está "verificado" enquanto não passar pelo parecer cego (camada 1) e pela rechecagem (camada 2).
Não editei nenhum capítulo, artigo, WORKPLAN ou release. O texto sugerido na §6 é só uma **proposta**.

Rótulos:
- **[provado]**: prova completa aqui, ainda sujeita à verificação;
- **[citado: nível]**: vem da literatura; o nível de leitura (texto, resumo ou título) está em `refs.md`;
- **[numérico]**: conferido por script, com oráculo independente e controle negativo;
- **[heurístico]**;
- **[aberto]**.

Ponto de partida: `../consistencia_operador/README.md` e `VERIFICACAO.md`. Lá ficaram estabelecidos:
- o ghost de resíduo −1;
- o núcleo não positivo (Marcinkiewicz);
- a leitura "só euclidiana" (ramo c);
- Hořava z = 3 como realização **local** sem ghost;
- a observação do verificador (A12) de que fatores de forma inteiros também evitam o ghost.

## 0. Resposta curta

1. **O obstáculo é estrutural, não um defeito do livro.**
   - **Lema KL [provado, folclore]:** com invariância de Lorentz, métrica positiva e representação de Källén–Lehmann,
     vale d_s(UV) ≥ 4.
   - Portanto, qualquer completamento com d_s = 2 abandona exatamente uma destas hipóteses:
     - métrica positiva: é o que fazem fakeon, Lee–Wick e PT;
     - a representação espectral: fatores de forma inteiros;
     - Lorentz: Hořava e os modelos multifracionais;
     - a ideia de que d_s vem do propagador do campo: segurança assintótica e CDT.
2. **Recomendação principal: a prescrição fakeon (Anselmi; Anselmi–Piva).**
   - Mantém o símbolo **exato**, a forma fechada erfc de d_s(τ), Lorentz, localidade e renormalizabilidade (Stelle).
   - A teoria lorentziana é *definida* a partir da euclidiana por uma rotação de Wick não analítica. É o encaixe
     mais natural para um livro cuja construção é euclidiana e simplicial.
   - Custos:
     - violação de microcausalidade em escalas ≲ ℓ;
     - unitariedade provada só perturbativamente, e pelos próprios proponentes.
   - Leitura concreta: o símbolo do livro é o operador cinético do setor de spin 2 (termo de Weyl) de R + R² + C².
     - Se ℓ estiver ligado à inflação, a previsão é 4/3 < N²r < 12 (Anselmi–Bianchi–Piva 2020).
     - Com uma **única** escala nos setores de spin 0 e spin 2, a previsão é r = 8/N² ≈ 2,2×10⁻³ (N = 60). Isso está
       ao alcance do LiteBIRD (δr < 10⁻³), mas exige ℓ ≈ 7×10⁻³⁰ m ≈ 4,5×10⁵ ℓ_P, e não ℓ_P.
3. **Segundo lugar: fator de forma inteiro (Tomboulis/Modesto).**
   - Sem ghost e com d_s de 4 a 2.
   - O símbolo **não** é exato: nenhuma função inteira sem zeros é igual a um polinômio com raiz. O perfil de
     d_s(τ) difere do erfc em até 0,38 (τ = 10ℓ²).
   - Custos: não localidade e continuação de Efimov.
4. **Terceiro lugar: d'Alembertianos não locais de conjuntos causais (Sorkin; Benincasa–Dowker).**
   - É a melhor história "discreto e Lorentz": o operador regularizado vai como k² no IR e k⁴ no UV em 4D, e
     d_s → 2 em qualquer dimensão (BBMM 2016).
   - Mas exige aspersão de Poisson (não um complexo simplicial regular), tem peso espectral negativo (Lema KL),
     instabilidade em 4D e uma regularização ad hoc.
5. **Excluídos ou rebaixados:**
   - Lee–Wick com par complexo: incompatível com d_s = 2 para símbolos polinomiais (Prop. LW [provado]).
   - PT/Pais–Uhlenbeck: debatido e sem teoria de campos com interação estabelecida.
   - Hořava e multifracional: operador diferente, com violação de Lorentz (LV).
   - Segurança assintótica: dá uma *reinterpretação* elegante (η = −2 reproduz o símbolo **exatamente**), mas não
     define dinâmica.

## 1. Enquadramento: por que d_s = 2 e unitariedade de Lorentz brigam

**Lema KL [provado; argumento de Weinberg, citado como folclore em BBMM 2016 §IV; sem novidade].**
Seja G(z) = w₀/z + ∫ρ(dμ²)/(z+μ²), com z = k² euclidiano, w₀ ≥ 0 e ρ uma medida positiva (não nula).
- Então zG(z) = w₀ + ∫ρ(dμ²) z/(z+μ²) é não decrescente.
- Para z ≥ z₀ vale G ≥ c/z com c = z₀G(z₀), e o símbolo S = 1/G satisfaz S ≤ z/c.
- Em d = 4: P(τ) ∝ ∫ z e^{−τS} dz ≥ ∫_{z₀}^∞ z e^{−τz/c} dz ~ c²/τ². Logo liminf_{τ→0} (−2 ln P/ln τ) ≥ 4. ∎

Consequências:
- O símbolo do livro tem ρ = δ(μ²) − δ(μ² − ℓ⁻²). Ele escapa do lema **só** por causa do peso −1, que é o ghost.
- Uma teoria euclidiana com esse símbolo também **não é reflexão-positiva**. Para campo livre, a positividade de
  Osterwalder–Schrader equivale a ρ ≥ 0. Por isso a reconstrução OS padrão devolve o ghost.

**Numérico [`e1_kl_bound.py`, 6/6]:**
- zG(z) é monótona para 200 densidades positivas aleatórias.
- d_s(10⁻⁶) = 4,00027 ≥ 4. O oráculo compara diferença finita (scipy) com a identidade de momentos (mpmath) e as
  duas concordam a 7×10⁻¹¹.
- Controle negativo 1: o símbolo do livro dá 2,0009 e viola o limite, como deveria.
- Controle negativo 2: trocar o sinal de um peso quebra a monotonicidade.

Rotas de escape:

| Hipótese abandonada | Rotas |
|---|---|
| métrica positiva | fakeon, Lee–Wick, PT, conjuntos causais (ρ < 0, BBMM §IV) |
| representação espectral (propagador não é função de Stieltjes) | fatores de forma inteiros: 1/S_T não é polinomialmente limitado fora do eixo real; `e3`, T3: \|1/S_T(5i)\| ~ 10²⁰⁹²⁷ |
| invariância de Lorentz | Hořava z = 3, multifracional |
| "d_s = d_s do propagador fundamental" | segurança assintótica (propagador vestido e dependente de gauge), CDT (d_s geométrico) |

**Prop. LW [provado, elementar].** Tome um símbolo polinomial S(z) de grau n com S(0) = 0 e S′(0) > 0.
- Ele tem d_s(UV) = 4/n, em d = 4.
- Com n = 2, S = z(α+βz), e a segunda raiz z = −α/β é **real**, com resíduo 1/S′ = −1/α < 0.
- Logo, na classe polinomial:
  - d_s = 2 ⇔ exatamente um ghost real, e o símbolo do livro é essencialmente único;
  - um par complexo conjugado (Lee–Wick) exige n ≥ 3, portanto d_s ≤ 4/3.

Numérico (`e3`): L1, com resíduos aleatórios, dá −1/α; L2, com S = z(1+z+z²), dá d_s → 1,3338.

## 2. Levantamento por abordagem

### 2.1 Fakeon (Anselmi 2018; Anselmi–Piva 2017, 2018; Anselmi 2021)

- **O que é [citado: resumo].** A teoria é uma teoria euclidiana com rotação de Wick não analítica.
  - Os polos de ghost viram "partículas puramente virtuais": saem dos estados assintóticos e das cutting equations.
  - Formulada direto em Minkowski, a mesma teoria de derivadas altas viola unitariedade (Anselmi–Piva PRD 2017,
    resumo).
- **Unitariedade.** Identidades ópticas espectrais "for every (multi)threshold separately" (Anselmi 2021, resumo).
  - Status: perturbativa, todas as ordens, provada pelos proponentes.
  - O escrutínio independente é limitado. Kubo–Kugo 2023 atacam o Lee–Wick de ghost **complexo**, não o fakeon; não
    conferi se há crítica direta ao fakeon [aberto].
- **Renormalizabilidade.** R + R² + C² é renormalizável por contagem de potências (Stelle 1977), e a prescrição é
  compatível com isso (ABP 2020, Introdução, lida no texto).
- **Causalidade.** "violation of causality at energies larger than the fakeon mass" (Anselmi–Piva 2018). Anselmi–Marino
  2020 mostram que o efeito é "short range for all practical purposes": não se propaga ao longo dos cones de luz nem
  por ondas gravitacionais.
- **Relação com o livro [heurístico, com um fato citado].**
  - No setor TT, o operador cinético de Einstein + C² é k²(1 + k²/m₂²) (Stelle 1978, estrutura padrão). É o símbolo
    do livro, com ℓ = 1/m₂.
  - Com R², o setor de spin 0 ganha k²(1 + k²/m₀²), com sinal global de modo conforme.
  - Os dois setores têm d_s → 2 no traço euclidiano.
  - O fakeon age só no lado lorentziano, então P(τ) e a forma erfc **não mudam**. Oráculo: `e3`, B1 (erfc contra
    momentos, 8×10⁻⁷).
  - Ressalva: o traço do modo conforme herda o problema do fator conforme da gravidade euclidiana.
- **Inflação [citado: texto, ABP 2020, eq. 7.3 e §7].**
  - r = 24m_χ²/[N²(m_φ² + 2m_χ²)], n_R − 1 = −2/N e r ≃ −8n_T.
  - A consistência exige m_χ > m_φ/4, e daí 4/3 < N²r < 12. Para N = 60, o texto dá 0,4 ≲ 1000r ≲ 3.
  - Números [`e2_fakeon_r.py`, 11/11]:
    - a janela exata em N = 60 é [0,370; 3,333]×10⁻³;
    - o limite m_χ → ∞ é 12/N². O oráculo independente é o slow-roll de Starobinsky, que dá N²r = 11,98 em N = 10⁴;
    - m_φ = 2,7×10¹³ GeV (A_s de Planck; a forma fechada e o slow-roll concordam a 5%);
    - m_χ,min = 6,8×10¹² GeV, portanto **ℓ < 2,9×10⁻²⁹ m ≈ 1,8×10⁶ ℓ_P**. Checagem dimensional: [ħc/(mc²)] = L.
  - **Escala única** m_χ = m_φ = 1/ℓ: N²r = 8, logo r = 2,22×10⁻³ (N = 60), 2,64×10⁻³ (N = 55) e 1,35×10⁻³
    (N = 77). Aqui ℓ = 7,2×10⁻³⁰ m.
  - Para **ℓ = ℓ_P**, o desvio relativo de r é 2,5×10⁻¹²: inobservável. A inflação seria Starobinsky pura, e o R²
    teria de vir de fora do símbolo.
- **Testabilidade.**
  - Hoje: r < 0,036 (BICEP/Keck 2021) e r < 0,032 (Tristram 2022). A janela é compatível.
  - LiteBIRD tem como requisito δr < 0,001 (PTEP 2023). Detecta a borda superior (~3×10⁻³). A borda inferior
    (4×10⁻⁴) fica abaixo do alcance.
  - O CMB-S4 foi descontinuado por DOE/NSF em 9 jul. 2025 (notícias da Science e da SciAm; ver `refs.md`).
  - **Ressalva ACT DR6:** n_s = 0,974 ± 0,003 (P-ACT, resumo). Isso dá N ≈ 77 (69–87) e deixa N = 60 a 2,4σ.
    - A tensão atinge o setor R² (Starobinsky), que o C² não altera.
    - Com N ≈ 77, a janela vira [2,2×10⁻⁴; 2,0×10⁻³] (`e2`, F6).
- **Encaixe discreto [heurístico].**
  - Termos R² e C² aparecem em Regge com derivadas altas (Hamber–Williams 1984, título).
  - A ação espectral Tr f(D²/Λ²) gera Einstein + C² + R² a partir **dos mesmos coeficientes de núcleo de calor** que
    o livro usa (Chamseddine–Connes 1997, título).
  - O fakeon só precisa da teoria euclidiana. É esse o ponto de elegância: o modelo simplicial fornece o objeto
    euclidiano, e a prescrição fornece a dinâmica lorentziana.
- **Prior art e o que o livro acrescentaria.** Tudo que está acima já existe (Anselmi et al.; ABP 2020). O livro só
  acrescentaria:
  - [aberto] derivar os dois símbolos (spin 0 e spin 2), com a razão m_χ/m_φ, do modelo simplicial. Seria uma
    previsão real de r;
  - [heurístico, trivial] notar que d_s do traço euclidiano é invariante sob a prescrição.

### 2.2 Lee–Wick (Lee–Wick 1969/70; Grinstein–O'Connell–Wise 2008; Donoghue–Menezes 2019)

- O ghost ganha largura e vira um par de polos complexos conjugados.
- GOW: "thought to be unitary, but … does not satisfy the usual analyticity conditions" (resumo).
- Estado da questão, **debatido**:
  - Nakanishi 1971: não invariância de Lorentz na prescrição CLOP (título).
  - Kubo–Kugo 2023: "complex ghosts are actually created and unitarity is violated", com teoria unitária só abaixo
    de um limiar (resumo).
  - Liu–Modesto–Calcagni 2023: pares complexos são unitários com a sua prescrição (resumo).
  - Donoghue–Menezes: "arrow of causality" misto, com violação de microcausalidade (resumo).
- **Para o livro:** pela Prop. LW, um símbolo polinomial com par complexo e graviton sem massa tem d_s ≤ 4/3. Ou
  seja, LW *não preserva* d_s = 2, a menos que o par venha só da largura quântica (autoenergia) e não do símbolo.
  Nesse caso ele volta ao 2.1 com outra prescrição. Rebaixado.

### 2.3 Fatores de forma inteiros (Tomboulis 1997; Modesto 2012; BGKM 2012; Modesto–Rachwał 2014)

- **Construção [`e3`, T1–T3].** S_T(k²) = k² exp(½ Ein(e^{−γ}ℓ⁴k⁴)), com Ein(x) = ∫₀ˣ(1−e^{−t})/t dt inteira.
  - S_T é inteira e sem zeros além de 0 (checado em (0, 10⁴]).
  - S_T/(ℓ²k⁴) → 1 no UV (desvio de 3×10⁻²⁶ em k² = 10³) e S_T/k² → 1 no IR.
  - d_s: 4,0000 (IR) → 2,0000 (UV). A diferença finita e a identidade de momentos concordam.
  - Controle negativo NC3: trocar Ein por γ + ln (não inteiro) dá d_s = 2 em todas as escalas, sem recuperação no IR.
  - **Não é o símbolo do livro.** O perfil de d_s difere em até 0,379 (em τ = 10ℓ²). A transição do S_T é mais abrupta
    (d_s(1) = 2,57 contra 2,70).
  - Nenhuma escolha consegue igualar k²+ℓ²k⁴ exatamente, porque essa função tem zero em k² = −ℓ⁻² e e^{H} não tem
    zeros.
- **Unitariedade.** Perturbativa, via amplitudes euclidianas continuadas (Pius–Sen 2016; Briscese–Modesto 2019:
  "unitarity … to all perturbative orders"; Koshelev–Tokareva 2021).
  - Briscese–Calcagni–Modesto–Nardelli 2024: densidade espectral positiva e uma KL generalizada para a parte
    time-ordered.
  - Isso não contradiz o Lema KL: o propagador livre completo não é de Stieltjes (T3).
- **Causalidade.** Não localidade na escala ℓ e prescrição de Efimov. O tema é debatido (Tomboulis 2015, título;
  Platania 2022, resumo).
- **Renormalizabilidade.** Super-renormalizável ou finita (Modesto 2012; Modesto–Rachwał 2014, títulos).
- **Origem discreta.** Fraca. Nada no livro gera uma função inteira de □. Na literatura isso vem de teoria de cordas e
  de campos de cordas.
- **Testes.** Não há previsão específica. O potencial estático não tem termo de Yukawa (é regular, do tipo erf), então
  o limite de Eöt-Wash (λ < 38,6 μm para Yukawa com |α| = 1) só se aplica de forma qualitativa [heurístico]. No
  fakeon, o Yukawa com sinal de ghost continua lá, e vale `../limites_ell_star/` (ℓ < 3,9×10⁻⁵ m).

### 2.4 D'Alembertianos de conjuntos causais (Sorkin 2009; Benincasa–Dowker 2010; Aslanbeigi–Saravani–Sorkin 2014)

- **Propriedades [citado: resumo ASS 2014].** O operador é "manifestly Lorentz-invariant, retarded, and non-local".
  - g(p) ∝ p·p para p pequeno e **constante** para p grande (operador não regularizado).
  - Há evidência de que o d'Alembertiano causal original em 4D é **instável**.
- **d_s [citado: texto BBMM 2016].** "universal dimensional reduction to 2 dimensions, in all dimensions".
  - Isso depende de uma **regularização** que remove uma divergência de coincidência. Após ela, g_reg ~ k^d no UV,
    ou seja, **k⁴ em 4D, o mesmo UV do livro**, com IR ~ −k².
  - d_s é **não monótono**: tem máximo acima de d em s ~ ℓ.
  - A rotação de Wick usa um propagador de Feynman que "is not a Green function of the original retarded
    d'Alembertians".
  - Os autores notam o argumento de Weinberg: o UV melhorado implica densidade espectral não positiva.
  - Na versão de Aslanbeigi–Saravani, com ρ ≥ 0, d_s não reduz: começa em 4.
- **Tensão com o livro.**
  - Eichhorn–Mizera 2014 medem, por passeios aleatórios diretamente no conjunto causal, d_s **crescente** no UV
    (resumo).
  - Carlip 2015 obtém redução para 2 em outros estimadores (Myrheim–Meyer, entre outros; resumo).
- **QFT [citado: resumo BBL 2015].** Contínuo de modos massivos. Em 4D o hamiltoniano "is not positive definite".
- **Fenomenologia.** Optomecânica: "spontaneous periodic squeezing" (BBLMMO 2016). O PRD 2017 propõe sensibilidade a
  escalas de não localidade de 10⁻²²–10⁻²⁶ m (resumo, com leitura do separador ÷ a conferir).
- **Encaixe simplicial [heurístico].**
  - A invariância de Lorentz vem da **aspersão de Poisson**. Um complexo regular Δ₄×Δ₂ não a tem.
  - Seria preciso trocar o complexo por um poset aleatório (o poset de faces com aspersão?) [aberto].
- **Veredito.** É a origem discreta mais natural para "d_s = 2 com Lorentz". Mas herda o peso espectral negativo (logo
  precisa de algo como fakeon/Wheeler para o modo instável; BBL 2015 usam o propagador de Wheeler), tem a
  instabilidade em 4D e o d_s não monótono. Terceiro lugar.

### 2.5 PT-simétrico / Pais–Uhlenbeck (Bender–Mannheim 2008)

- **A favor:** "no states of negative norm … energy spectrum bounded below … time-evolution operator is unitary", com
  hamiltoniano não Dirac-hermitiano (resumo).
- **Críticas [resumo]:**
  - Smilga 2009: na realização de Bender–Mannheim, as funções de onda crescem exponencialmente; a unitariedade quebra
    no limite de frequências iguais; "generically, the inclusion of interaction terms breaks unitarity".
  - Salvio–Strumia 2016: energia positiva, mas com "negative-norm configuration space" e uma interpretação
    probabilística modificada.
- **Para o livro:** mantém o símbolo e d_s formalmente. Mas o caso ω₁ = 0 (graviton sem massa) não foi conferido nas
  fontes [aberto], e não há QFT gravitacional interagente estabelecida. **Debatido; rebaixado.**

### 2.6 Segurança assintótica

- **d_s [citado: resumo Lauscher–Reuter 2005].** O resumo diz "effective dimensionality of 2". O mecanismo vem de
  conhecimento padrão, a conferir no texto: no ponto fixo, η_N = −2, o propagador vai como 1/p⁴ e d_s = 2.
  Reuter–Saueressig 2011 acrescentam um regime intermediário com 4/3 (título).
- **Resultado [numérico, `e3` A1].** A família S = k²(1+ℓ²k²)^{−η/2} tem d_s(UV) = 2d/(2−η): 4; 2,6667; 2,0001; 1,6006
  para η = 0, −1, −2, −3.
  - **η = −2 é exatamente o símbolo do livro.** O livro pode ser lido como a interpolação mais simples entre η = 0 e
    η = −2.
  - Controle negativo: 2d/(2+η) falha.
- **Ghosts.**
  - Platania–Wetterich 2020: polos de ghost em truncações podem ser "fictitious": o resíduo some quando todos os
    operadores entram (resumo).
  - Bonanno et al. 2022: a função espectral do graviton **dinâmico** é positiva; a do de fundo tem partes negativas
    (resumo).
  - Fehre et al. 2023: função espectral positiva, com pico sem massa e contínuo de multigravitons (resumo).
  - Draper et al. 2020: amplitudes finitas e unitárias a partir de fatores de forma (resumo).
- **Tensão.** Se a função espectral é positiva, o Lema KL impede 1/p⁴ nesse propagador. O d_s = 2 de SA então se
  refere a outro objeto: o propagador de fundo ou dependente do regulador, ou o escalamento de k. Isso precisa ser
  conferido no texto [aberto].
- **Veredito.** É uma boa *reinterpretação* (o símbolo como propagador efetivo interpolante, com o polo real sendo
  artefato de truncação). Mas não fornece dinâmica lorentziana por si só. Combina com a leitura 2.1 (Holdom–Ren 2016:
  ghost confinado, conjectura).

### 2.7 Hořava z = 3 e multifracional (resumido; detalhes em `../consistencia_operador/`)

- **Hořava:** sem ghost e d_s = 1 + 3/z = 2. Custos: operador diferente, folheação, khronon, M* ≲ 10¹⁵–10¹⁶ GeV (BPS
  2011) e percolação de LV.
- **Multifracional (Calcagni 2017, 2021; títulos):** medidas multiescala dão d_s → 2 no UV. As versões com derivadas
  ponderadas ou q-derivadas deformam Lorentz. Não preserva o símbolo.

### 2.8 Outros

- **Ação espectral (Chamseddine–Connes 1997; CCM 2007).** Gera C² com coeficiente fixado pelos momentos de f.
  - Vínculo: β ≳ 10⁴ m⁻¹ de balanças de torção (Lambiase–Sakellariadou–Stabile 2013, resumo), isto é,
    ℓ ≲ 10⁻⁴ m.
  - A ação é euclidiana; a versão lorentziana de triplas espectrais é problema aberto.
  - É a **origem** mais elegante para o termo k⁴ num livro baseado em núcleo de calor. Combina com 2.1.
- **CDT (Ambjørn–Jurkiewicz–Loll 2005; Coumbe–Jurkiewicz 2015; Loll 2019).** Triangulações **lorentzianas** com
  folheação causal dão d_s curto ≈ 1,5–2 (valores de memória, a conferir). A ligação com Hořava vem de AGJJL 2010.
  - É o precedente simplicial mais próximo, mas dá d_s geométrico, não o símbolo.
  - Construir um "CDT de Δ₄×Δ₂" é um programa de pesquisa, não uma correção de texto.

## 3. Tabela comparativa

| Rota | Símbolo exato? | d_s = 2? | Lorentz | Unitariedade (status) | Custo causal | Origem discreta natural | Previsão testável / escala | Prior art (o que o livro somaria) |
|---|---|---|---|---|---|---|---|---|
| **Fakeon** (R+R²+C²) | **sim** (spin 2; spin 0 também com R²) | **sim, forma erfc inalterada** | sim | perturbativa, todas as ordens (proponentes); escrutínio independente limitado | microcausalidade violada em ≲ ℓ; na prática curto alcance | **boa**: só precisa da teoria euclidiana; Regge R²/C², ação espectral | 4/3 < N²r < 12; escala única: r = 8/N² ≈ 2,2×10⁻³ (LiteBIRD); ℓ < 2,9×10⁻²⁹ m | ABP 2020 completo; o livro somaria a derivação simplicial de m_χ/m_φ [aberto] |
| Fator de forma inteiro | não (só assintótico; Δd_s ≤ 0,38) | sim | sim | perturbativa (Efimov/Pius–Sen/BM 2019) | não localidade ~ℓ; Efimov | fraca | nenhuma específica; Newton regular | Tomboulis/Modesto; nada novo |
| Conjunto causal | não (UV ~k⁴, IR ~k², não polinomial) | sim (BBMM), não monótono | sim, retardado | problemática: ρ < 0, H não positivo, 4D instável | retardado por construção; modos instáveis | **ótima** para posets com aspersão; ruim para complexo regular | optomecânica (escalas de não localidade) | BBMM 2016; o livro somaria uma ponte simplicial→poset [aberto] |
| Lee–Wick (par complexo) | não | **não** (≤ 4/3, Prop. LW) | debatido (Nakanishi) | debatida (Kubo–Kugo × LMC 2023) | acausal ~1/M | nenhuma | — | excluído |
| PT / Pais–Uhlenbeck | sim (formal) | sim (formal) | sim | debatida; interação quebra (Smilga) | — | nenhuma | — | rebaixado |
| Segurança assintótica | sim, como η: 0 → −2 | sim | sim | aberta (espectral positiva para o graviton dinâmico) | — | CDT/SA (evidência) | — | reinterpretação; tensão com o Lema KL [aberto] |
| Hořava z = 3 | não (k⁶, anisotrópico) | sim | só no IR | sem ghost; projetável renormalizável | folheação | CDT (AGJJL 2010) | M* ≲ 10¹⁵–10¹⁶ GeV | ver consistencia_operador |
| Multifracional | não | sim | deformado | — | — | — | limites de LV | rebaixado |
| Só euclidiano (atual) | sim | sim | n/a | n/a | n/a | é o que o livro prova | nenhuma | já adotado |

## 4. Ranking (mais elegante, com o menor enfraquecimento)

1. **Fakeon, com o símbolo lido como o setor de Weyl de R + R² + C².**
   - Preserva tudo o que o livro prova: símbolo, erfc, d_s.
   - Acrescenta Lorentz, localidade, renormalizabilidade e uma previsão (janela de r).
   - O único custo novo é a microcausalidade em ≲ ℓ.
   - É honesto dizer que tudo isso é prior art, e que o elo simplicial (a origem do C² e o valor de m_χ/m_φ) é
     problema aberto.
2. **Fator de forma inteiro.** Troca o símbolo exato por "assintoticamente o mesmo", para ganhar a ausência de ghost.
   O custo em causalidade é parecido, e a origem discreta é pior.
3. **Conjunto causal.** É a narrativa discreta mais bonita, mas tem mais problemas abertos (regularização, instabilidade,
   ρ < 0) e exige aleatoriedade de Poisson.

Complementos que combinam com 1:
- a ação espectral, como origem do C²;
- a segurança assintótica, como reinterpretação do polo (Platania–Wetterich) e de η = −2.

## 5. Scripts

Rodar a partir **desta pasta** (o `bisect.py` do scratchpad sombreia a stdlib), com `PYTHONIOENCODING=utf-8`. As saídas
estão em `*.out.txt`.

| Script | Verifica | Oráculo | Controle negativo | Resultado |
|---|---|---|---|---|
| `e1_kl_bound.py` | Lema KL: zG monótona, d_s(UV) ≥ 4 | diferença finita (scipy) vs. momentos (mpmath) | símbolo do livro (ρ < 0) viola; peso invertido quebra a monotonicidade | 6/6 |
| `e2_fakeon_r.py` | janela de r do ABP 2020, m_φ, ℓ máx., escala única, ACT n_s | slow-roll numérico de Starobinsky (N²r → 12; m_φ) | fórmula com m_φ↔m_χ trocados; limite m_φ/2 | 11/11 |
| `e3_ds_candidates.py` | d_s: livro (erfc), Tomboulis, família η, Prop. LW | erfc fechado vs. momentos; diferença finita vs. momentos | erfc sem e^{x²}; lei 2d/(2+η); Ein→ln | 10/10 |
| `resolve_dois.py` | 78 DOIs (Crossref; DataCite para arXiv) | título vs. palavra-chave | DOI errado; palavra-chave errada | 78/78 + 2 NEG |

## 6. Proposta de texto (não aplicada)

Remark no cap. 12, perto da l.511, e na Remark "Scope" do SQG, em house style e sem histórico:

> *Lorentzian completion.* The symbol $k^2+\ell^2k^4$ is the transverse-traceless kinetic operator of Einstein
> gravity with a Weyl-squared term, with $\ell=1/m_2$ \cite{Stelle1978}. By the Källén–Lehmann representation, no
> positive-metric Lorentz-invariant propagator has an ultraviolet heat-kernel dimension below 4, so the
> massive pole of residue $-1$ cannot be an ordinary particle. Under the fakeon prescription \cite{Anselmi2018,
> AnselmiPiva2018} it is purely virtual: the theory is defined from its Euclidean version by a nonanalytic Wick
> rotation, so the heat-kernel trace and $d_s(\tau)$ above are unchanged, while microcausality fails at scales
> $\lesssim\ell$. If the same construction drives inflation, $4/3<N^2r<12$ \cite{ABP2020}. No simplicial
> derivation of this prescription or of $m_2$ is given here.

## 7. Incertezas e pendências para a camada 2

- **Fakeon.** A unitariedade em todas as ordens é afirmação dos proponentes. Não localizei nem li uma crítica
  independente específica ao fakeon.
- **Tensão do Lema KL com SA.** Não li em texto qual propagador tem η = −2 em Lauscher–Reuter.
- **Afirmações só pelo resumo:** BBLMMO 2017 (escala 10⁻²²–10⁻²⁶ m; o separador "÷" veio corrompido) e CDT
  d_s ≈ 1,5–2 (de memória).
- **Casos não conferidos:** Pais–Uhlenbeck com ω₁ = 0; a data de lançamento do LiteBIRD.
- **Identificação do símbolo escalar do livro com o setor TT/spin 0:** é modelagem [heurístico], não derivação. O
  livro não especifica o campo (ver consistencia_operador §1).
- **Checagem dimensional:** feita só em `e2` (ℓ = ħc/(mc²)). As demais grandezas estão em unidades ℓ = 1.
