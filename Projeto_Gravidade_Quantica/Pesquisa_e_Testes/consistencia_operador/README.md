# Consistência do operador cinético de símbolo k² + ℓ*²k⁴ (caps. 12–13 e artigo SQG)

**Status: rascunho (draft) de pesquisa, 2026-09-28.** Ainda não foi verificado de forma independente. Pela convenção
"quatro olhos", nada aqui é "verificado" até passar pelo parecer cego (camada 1) e pela rechecagem (camada 2).
Nenhum capítulo, artigo, WORKPLAN ou release foi editado. As mudanças de texto da §5 são **propostas**.

Rótulos: **[provado]** = prova completa aqui (sujeita à verificação); **[citado]** = resultado da literatura,
com a referência e com o nível de leitura dado em `refs.md`; **[numérico]** = checado por script com oráculo
independente e controle negativo; **[heurístico]**; **[aberto]**.

## 0. Veredito em uma frase

O símbolo k² + ℓ²k⁴ só é consistente como **operador euclidiano cujo traço do núcleo de calor define uma
dimensão espectral**: o ramo (c). Não é consistente como propagador lorentziano (ramo a: ghost), e seu único
parente lorentziano sadio com d_s = 2 é um operador **diferente**, o de Hořava com z = 3 (ramo b). Esse parente
tem folheação preferida, um modo escalar extra e uma escala M* que, pelos vínculos citados, **não pode ser M_P**.
O texto atual já é quase honesto. As falhas remanescentes são quatro:

1. chama de "return probability"/"diffusion" um núcleo que não é positivo, contradizendo a própria observação
   do cap. 12, l.174;
2. identifica ℓ* = ℓ_P na fenomenologia lorentziana;
3. apresenta o ansatz quártico ω² = c²k²(1+ξℓ*²k²) sem dizer que ele exige referencial preferido e, para
   d_s = 2, um termo k⁶ adicional;
4. a tabela do cap. 12, l.603, lista "Planckian UV Renormalizability" sem ressalva.

## 1. O que o texto afirma hoje (passo 1)

| Local | Afirmação |
|---|---|
| cap. 12, l.99 (resumo) | símbolo isotrópico **assumido** k² + ℓ_P²k⁴ em 4D; d_s(τ) em forma fechada de 4 a 2; Hořava obtém os mesmos extremos com operador anisotrópico diferente |
| cap. 12, l.160, 172 | Hořava: d_s = 1 + 3/z, logo d_s = 2 exige z = 3; o elo "d_s = 2 ⇔ renormalizabilidade por contagem de potências" é heurístico e "not established here" |
| cap. 12, l.174, 177 | para símbolo homogêneo \|k\|^{2α} com α > 1, o núcleo tem valores negativos e P é "the diagonal of the kernel rather than a return probability" |
| cap. 12, l.511, 513, 524 | operador isotrópico em 4D **euclidiano**; P(τ) é chamado de "return probability"; a variante anisotrópica ω² + k² + ℓ_P²k⁴ (z = 2) dá 5/2; a forma erfc tem precedente em Sotiriou–Visser–Weinfurtner (SVW), com a redução via I₁ = (τ⁻¹ − I₀)/(2ℓ²); "Whether quantum spacetime diffuses according to this symbol is an assumption" |
| cap. 12, l.562–570 | ansatz ω² = c²k²(1+ξℓ*²k²) "not derived"; a continuação lorentziana isotrópica tem ramo sem massa com ξ = 0 e ghost em p² = −1/ℓ_P²; ξ é tratado como livre (1/2); "diffusion model suggests ℓ* = ℓ_P"; atraso de 10⁻⁶²–10⁻⁶⁰ s |
| cap. 12, l.603 | tabela-dicionário: "Running Spectral Dim d_s(α) → 2" ↔ "Planckian UV Renormalizability" |
| cap. 12, l.624 | "Established: closed-form spectral dimensions for homogeneous and two-scale diffusion symbols" |
| cap. 13, l.49, 56, 65, 88, 94, 126 | as mesmas afirmações da l.562–570, em forma de letter; "For diffusion with the two-scale symbol … we give the return probability"; ℓ* = ℓ_P |
| SQG, l.100 (resumo) | símbolo assumido, isotrópico, euclidiano; "in Lorentzian signature its isotropic k⁴ term carries a ghost" |
| SQG, Prop. l.241–257; Remark l.259–261 | forma fechada; a Remark "Scope of the diffusion model" admite quarta derivada temporal, ghost e 5/2 para z = 2 |
| SQG, l.500, 510, 538 | tabelas: "Lorentzian ghost"; "Short-scale diffusion with d_s = 2" |
| SQG, l.571–576 | o mesmo ansatz de dispersão, com ℓ* = ℓ_P |

**Sobre qual campo o operador age:** em nenhum dos três textos o operador age sobre um campo especificado
(métrica, h_ij TT ou escalar). Ele é apenas um símbolo de difusão. O ansatz de dispersão é aplicado "ao gráviton"
sem derivação.

Correção da premissa da tarefa: o operador isotrópico **não** é superluminal. Na continuação lorentziana, os
dois ramos têm v_g ≤ c (check A5). A superluminalidade (v_g > c para ξ > 0) vem do *ansatz* anisotrópico do
cap. 13, que já pressupõe um referencial preferido.

## 2. Classificação dos ramos (passo 2)

### (a) Isotrópico lorentziano: G(p) = 1/[p²(1 + ℓ²p²)], métrica (−,+,+,+)

- **Prop. A1 [provado + numérico]:** G = 1/p² − 1/(p² + ℓ⁻²). O peso espectral é
  ρ(μ²) = δ(μ²) − δ(μ² − ℓ⁻²). O resíduo do polo massivo, m² = 1/ℓ², é **−1**, isto é, um estado de norma
  negativa (ghost). No plano de energia, o resíduo em p⁰ = +ω_m tem sinal oposto ao de um campo massivo sadio.
  Prova: frações parciais. Numericamente, sympy `apart`/`residue` bate com a integral de contorno do mpmath a
  10⁻¹² (`a_ghost_residues.py`, checks A1–A3).
  É a estrutura de Stelle (1977) no setor de spin 2 [citado]. Na formulação com energia positiva, o hamiltoniano
  de Ostrogradsky é ilimitado inferiormente (Woodard 2015) [citado].
- **Prop. A2 [provado + numérico]:** o potencial estático é V(r) = −(GM/r)(1 − e^{−r/ℓ}): Yukawa com α = −1 e
  λ = ℓ, finito em r = 0, com V(0) = −GM/ℓ (check A4, quadratura QAWF vs. forma fechada, erro < 10⁻⁹; o mutante
  com 1 + e^{−r/ℓ} é rejeitado). Em gravidade quadrática completa, o spin 2 contribui com −4/3 e o spin 0 com +1/3
  (Stelle 1978) [citado]. O modelo escalar do livro não fixa essa decomposição.
- **Lee–Wick / fakeon [citado]:**
  - Lee–Wick (1969/70): o ghost adquire largura, forma um par de polos complexos conjugados e sai do espaço de
    estados assintóticos. A unitariedade da matriz S é mantida.
  - Anselmi–Piva (2017) reformulam a teoria como "nonanalytically Wick rotated Euclidean theories". Nas palavras
    deles, "The physical results … are different from those of the previous ones". Tratam também da invariância
    de Lorentz acima dos limiares de LW.
  - Fakeons (Anselmi 2018; Anselmi–Piva 2018): o modo é "puramente virtual". O preço declarado é "violation of
    causality at energies larger than the fakeon mass".
  - Donoghue–Menezes (2019): unitariedade com ghosts instáveis, ao custo de acausalidade microscópica.
  - **O que mudaria para o livro [heurístico]:**
    - d_s(τ) é uma grandeza euclidiana. Nessas prescrições a teoria é definida a partir da euclidiana, logo a
      forma fechada não muda.
    - O potencial estático também não muda, pois não há polo na integral espacial a ω = 0.
    - Muda a interpretação lorentziana: sem partícula massiva assintótica e com acausalidade em escalas ≲ ℓ.
  - **Custo:** abandonar a microcausalidade abaixo de ℓ e adotar uma prescrição não analítica, que teria de ser
    justificada a partir do modelo simplicial. Nada no livro faz isso.
- **Veredito (a):** inconsistente como dinâmica lorentziana unitária e causal, a menos que se adote LW/fakeon,
  que tem custo próprio. Como é o que o texto já diz, não há afirmação errada. Falta só nomear a alternativa.

### (b) Anisotrópico z = 3: −∂_t² + F(−∇²), com F(k²) = c²k² + a k⁴/M*² + k⁶/M*⁴

- **Prop. B1 [provado + numérico]:** com D dimensões espaciais,
  P(τ) = (4πτ)^{−1/2} (2π)^{−D} ∫ e^{−τF}, e d_s(UV) = 1 + D/z, d_s(IR) = 1 + D.
  - Prova: no UV, a substituição k = τ^{−1/(2z)}x mostra que ∫ e^{−τF} ~ τ^{−D/(2z)}, e os termos de ordem menor
    são dominados, por convergência dominada. No IR vale a mesma conta com k = τ^{−1/2}x.
  - Para D = 3 e z = 3: d_s de 2 a 4, monótona, com aproximação d_s − 2 ∝ τ^{2/3}.
  - Um termo quártico a k⁴ com a > −2 não altera os limites.
  - Checks B1–B7: diferença finita de ln P (scipy) vs. identidade de momentos d_s = 1 + 2τ⟨F⟩ (mpmath, 30
    dígitos) concordam a 10⁻⁷.
  - Controle negativo: z = 2 dá 2,5000, reproduzindo o 5/2 do livro, e falha o teste "→ 2".
  - Também z = 4 → 7/4 e z = 6 → 3/2.
- **Sem ghost [citado: Hořava 2009]:** as equações são de segunda ordem no tempo, logo não há polo extra de
  resíduo negativo. A dispersão do spin 2 é ω² = c²k² + … + k⁶/M*⁴. O preço é uma **folheação preferida**:
  Lorentz só é recuperado no IR.
- **Problemas conhecidos [citado]:**
  - O modo escalar extra (khronon) é fortemente acoplado ou instável na versão original (Charmousis–Niz–Padilla–
    Saffin 2009; Blas–Pujolàs–Sibiryakov 2009; Papazoglou–Sotiriou 2010).
  - A extensão sadia não projetável (BPS 2010) é, segundo BPS 2011, "the only model which is free from
    instabilities and strong coupling".
  - Acoplamento fraco exige M* < M_SC ~ √α M_P. Com os limites PPN, **M* ≲ 10¹⁵–10¹⁶ GeV** (BPS 2011, eq. 5.17,
    lido no texto).
  - GW170817 impõe |c_g/c − 1| ≲ 10⁻¹⁵, o que força β ≈ 0 no setor IR; α e λ ficam limitados por PPN e outros
    vínculos (Gümrükçüoğlu–Saravani–Sotiriou 2018).
  - Renormalizabilidade: provada para a versão **projetável** (Barvinsky et al. 2016), que tem liberdade
    assintótica em 2+1 (2017) e em 3+1 (BKS 2023). Mas a versão projetável é a "bad" de BPS 2011, e a versão sadia
    (não projetável) não tem prova de renormalizabilidade. Esse conteúdo foi conferido só pelo título, e a
    afirmação precisa de conferência na camada 2.
- **Percolação de violação de Lorentz (LV) para a matéria [citado]:**
  - Collins et al. (2004): LV no UV induz, via laços, LV de dimensão 4 não suprimida no IR, salvo ajuste fino.
  - Pospelov–Shang (2012): a proteção vem de separação de escalas, com supressão Λ_HL²/M_P². Com os limites de
    LV de dimensão 4 (< 10⁻²⁰), isso exige **Λ_HL ≲ 10¹⁰ GeV** (lido no texto, conclusões).
  - Alternativa: supersimetria (Groot Nibbelink–Pospelov 2005).
  - Pelo lado de baixo: se M*(matéria) ~ M*, os atrasos de fótons de AGN e GRB dão M* ≳ 10¹⁰–10¹¹ GeV (BPS 2011,
    eq. 5.21, com ressalva dos autores).
- **Consequência para o livro [citado + numérico, `d_dimensional.py`]:** no ramo (b), **ℓ* = ℓ_P está fora da
  janela**, pois M_P = 1,22×10¹⁹ GeV está acima do teto de acoplamento fraco (check O2).
  - A janela citada é 10¹⁰ ≲ M* ≲ 10¹⁵–10¹⁶ GeV. Com Pospelov–Shang, M* ~ 10¹⁰ GeV.
  - Em comprimento: ℓ* ≈ 2×10⁻³² a 2×10⁻²⁶ m, ou seja, 10³ a 10⁹ ℓ_P.
  - Mesmo assim, os efeitos seguem muito fora de alcance:
    - só com z = 3: Δv/c = (5/2)(ℓ*k)⁴ ≈ 7×10⁻¹²⁶ a 100 Hz, para M* = 10¹⁰ GeV;
    - com a admixtura quártica do cap. 13: o atraso escala por (ℓ*/ℓ_P)² ≈ 1,5×10¹⁸, logo 10⁻⁶²–10⁻⁶⁰ s viram
      ~10⁻⁴³–2×10⁻⁴² s, ainda **~38–40 ordens** abaixo de 10⁻⁴ s. O fato-chave "10⁵⁶ vezes abaixo do alcance" do
      CLAUDE.md vale só para ℓ* = ℓ_P.
  - GW170817 sozinho dá apenas ℓ* < 89 m para z = 3 e ℓ* < 2×10⁻² m para o ansatz quártico com ξ = 1. Bate, a
    fatores O(1), com `limites_ell_star/`.
- **Prop. B2 [provado]: o ansatz do cap. 13 com d_s = 2.** O ansatz ω² = c²k²(1+ξℓ*²k²) com ξ ≠ 0 só é
  compatível com d_s(UV) = 2 dentro do ramo (b) se houver também um termo k⁶. Nesse caso ξ é um acoplamento
  independente, não fixado por d_s (check B6). Sem o termo k⁶, a teoria tem z = 2 e d_s → 5/2 (NC1b).
- **Veredito (b):** é o único ramo lorentziano sem ghost que dá d_s = 2 com a mesma interpolação 4 → 2. Mas não é
  o operador do livro, não é derivado do modelo simplicial, tem custos conhecidos (folheação, modo escalar,
  acoplamento forte, percolação de LV) e **não admite ℓ* = ℓ_P**.

### (c) Só euclidiano: o operador A = −Δ + ℓ²Δ² em ℝ⁴ define apenas o traço do núcleo de calor

- **Prop. C1 [provado + numérico]: o núcleo de e^{−τA} assume valores negativos para todo τ > 0.** Logo não
  existe processo de difusão (Markov) subjacente, e P(τ) = e^{−τA}(x,x) **não é uma probabilidade de retorno**.
  - Prova: K_τ é real, contínuo e tem ∫K_τ = 1. Se fosse K_τ ≥ 0, seria uma densidade de probabilidade, e a
    marginal numa reta teria função característica exp(−τ(t² + ℓ²t⁴)). Pelo teorema de Marcinkiewicz (1939), se
    e^{P(t)} com P polinomial é função característica, então grau P ≤ 2. Contradição. ∎
  - O mesmo argumento vale para a parte espacial do ramo (b), e^{−τ(k² + k⁶)}.
  - Numérico (`c_kernel_positivity.py`, 18/18): transformada de Hankel em 4D por dois métodos (scipy e mpmath).
    - Para τ = 0,01ℓ²: min K / max K = −1,9×10⁻²; "massa negativa" ∫max(−K,0) = 0,55, com ∫K = 1,00000.
    - Para z = 3 em 3D: −5,3×10⁻².
    - O controle negativo (gaussiano, símbolo k²) bate com a forma exata a 10⁻¹⁵ e não tem valores negativos.
  - A literatura já registra isso: Calcagni–Eichhorn–Saueressig (2013) mostram que as equações de difusão
    "quantum-improved", inclusive a de Hořava–Lifshitz, "do not give rise to a well-defined diffusion process"
    [citado, lido no texto]. Nenhuma novidade é reivindicada.
- **Prop. C2 [provado; provavelmente folclore, sem novidade reivindicada]: nenhum semigrupo de Markov invariante
  por translação em ℝᵐ reduz a dimensão no UV.**
  - Se ψ é o expoente de Lévy–Khintchine de um processo de Lévy em ℝᵐ, então Re ψ(k) ≤ C(1 + |k|²). Isso vem da
    subaditividade de √|ψ| para funções negativas definidas contínuas.
  - Logo P(τ) ≥ (2π)^{−m} ∫ e^{−τC(1+k²)} dk = e^{−Cτ}(4πCτ)^{−m/2}.
  - Portanto, quando existe, d_s(UV) := lim_{τ→0} 2 ln P / (−ln τ) ≥ m.
  - Consequência: **nenhuma difusão genuína invariante por translação em ℝ⁴ dá d_s = 2 no UV.** A redução
    dimensional exige núcleo não positivo, tempo de difusão não linear (a construção de CES 2013) ou abandono da
    invariância por translação (fractais: o valor de Sierpiński do cap. 6 vem de um processo genuíno, sem essa
    invariância).
- **O que o livro pode afirmar honestamente no ramo (c) [provado]:**
  - A Prop. (forma fechada de P e de d_s) é um teorema sobre o **traço do núcleo de calor** (por volume) do
    operador elíptico positivo A = −Δ + ℓ²Δ² em ℝ⁴.
  - Equivalentemente, é uma afirmação sobre a lei de Weyl de A: N(λ) ~ λ² no IR e ~ λ no UV. P(τ) > 0, e d_s está
    bem definido.
  - O livro **não** pode afirmar, a partir disso:
    - um processo de difusão;
    - um propagador;
    - um potencial estático, com α = −1 (portanto os limites de Yukawa de `limites_ell_star/` não se aplicam ao
      ramo c);
    - uma relação de dispersão (ξ fica indeterminado, como o texto já diz);
    - um vínculo sobre ℓ*;
    - renormalizabilidade.

## 3. Scripts e resultados (passo 3)

| Script | Verifica | Oráculo independente | Controle negativo | Resultado |
|---|---|---|---|---|
| `a_ghost_residues.py` | resíduos, peso espectral, sinal do resíduo em p⁰, potencial de Yukawa, v_g | sympy `apart`/`residue` vs. contorno mpmath; QAWF vs. forma fechada | mutante sadio 1/s + 1/(s+1) (sem ghost); mutante 1/(s(1−ℓ²s)) (táquion, polo ≠ −1/ℓ²); potencial com 1 + e^{−r/ℓ} | 14/14 |
| `b_ds_lifshitz.py` | d_s(τ) para z = 3, limites 2 e 4, taxa τ^{2/3}, admixtura k⁴, 1 + 3/z para z = 1…6; reprodução da forma erfc do livro | diferença finita (scipy) vs. momento (mpmath) | z = 2 deve falhar "→ 2" (dá 2,5); forma erfc sem o fator u deve falhar | 16/16 |
| `c_kernel_positivity.py` | sinal do núcleo em 4D (isotrópico) e em 3D (z = 3), massa negativa, normalização | scipy vs. mpmath no mínimo; gaussiano vs. forma exata | o gaussiano não pode ter valores negativos | 18/18 |
| `d_dimensional.py` | dimensões de ℓ* = ħ/(M*c), ω² = c²k² + c²ℓ*⁴k⁶, k² + ℓ²k⁴; ℓ_P por duas rotas (CODATA via `scipy.constants`); ordens de grandeza | vetores de dimensão (L, T, M); forma SI vs. unidades naturais | ħ/(M*c²) e ℓ⁴k⁴ devem falhar | 10/10 |
| `resolve_dois.py` | 36 DOIs via Crossref | título retornado vs. palavra-chave | DOI errado não resolve | 36/36 |

As saídas estão nos arquivos `*.out.txt`. Rodar a partir **desta pasta**: o `bisect.py` do scratchpad da sessão
sombreia a stdlib. Use `PYTHONIOENCODING=utf-8` no Windows.

## 4. Recomendação (passo 4)

**Adotar o ramo (c) como a afirmação do livro, citar o ramo (b) como a única realização lorentziana conhecida sem
ghost e rebaixar o ramo (a) a uma observação.** Justificativa:

- (c) é exatamente o que está provado.
- (b) exige um operador diferente, uma folheação preferida e ℓ* ≫ ℓ_P, e nada disso é derivado.
- (a) tem ghost.

A fenomenologia dos caps. 12–13 continua como "ansatz postulado". Ela deve dizer que ξ ≠ 0 pressupõe um
referencial preferido (ramo b com termo k⁶) e que, nesse ramo, ℓ* não é ℓ_P. A conclusão "inobservável" continua
válida e fica mais robusta, mas o número "56 ordens" passa a valer só para ℓ* = ℓ_P.

**Observação [heurístico, aberto]:** a folheação L^∞-minimax da Parte III poderia fornecer a folheação preferida
do ramo (b). Isso é apenas uma sugestão, sem derivação. Precedente: a folheação causal de CDT já foi relacionada a
Hořava–Lifshitz (Ambjørn–Görlich–Jordan–Jurkiewicz–Loll 2010). Não há novidade a reivindicar sem uma construção
explícita.

## 5. Mudanças de texto propostas (apenas propostas; 14 itens)

Nenhuma usa linguagem de histórico ("earlier version", "corrected"), conforme a regra 6 do CLAUDE.md.

**Cap. 12** (`chap12_grand_unification_quantum_gravity_treatise.tex`)

1. **l.99:** "for the assumed isotropic two-scale symbol $k^2+\ell_P^2k^4$ in four dimensions" → "…in four
   Euclidean dimensions … closed-form expression for the spectral dimension of its heat-kernel trace $d_s(\tau)$".
   Acrescentar: "the kernel is not positive, so no diffusion process is implied".
2. **l.511 e l.524:** "the return probability" → "the heat-kernel diagonal $P(\tau)$". Justificativa: coerência
   com a própria l.174, porque o termo k⁴ torna o núcleo não positivo para todo τ (Prop. C1). Na l.524, "this
   particular diffusion model" → "this particular heat-kernel model", e acrescentar uma frase com a citação de
   CES 2013: "As for Hořava–Lifshitz and other modified diffusion equations, the kernel is not positive and
   admits no probabilistic interpretation".
3. **l.511 (parêntese):** acrescentar "The ghost-free Lorentzian operator with ultraviolet value $d_s=2$ is the
   anisotropic $z=3$ operator $\omega^2 + c^2k^2 + k^6/M_\ast^4$ with a preferred foliation \cite{horava2009}; it
   is a different operator and is not derived here."
4. **l.566:** depois de "…rather than 2", acrescentar:
   - "A quartic term with $\xi\neq0$ is compatible with $d_s\to2$ only inside a $z=3$ theory with an additional
     $k^6$ term, where $\xi$ is an independent coupling; any $\xi\neq0$ presupposes a preferred frame, and
     $v_g>c$."
   - Substituir "suggests $\ell_\ast=\ell_P$" por "sets no Lorentzian scale; in the healthy extension of
     Hořava–Lifshitz gravity weak coupling requires $M_\ast\lesssim10^{15}$–$10^{16}$ GeV \cite{BPS2011}, and
     protection of matter from Lorentz violation suggests $M_\ast\lesssim10^{10}$ GeV \cite{PospelovShang2012},
     i.e. $\ell_\ast\gtrsim10^{3}$–$10^{9}\,\ell_P$".
5. **l.570:** depois dos números para ℓ* = ℓ_P, acrescentar "For $\ell_\ast=\hbar c/(10^{10}\,\mathrm{GeV})$ the
   delays scale by $(\ell_\ast/\ell_P)^2\approx1.5\times10^{18}$, to $\sim10^{-43}$–$10^{-42}$ s, still some 38
   orders of magnitude below the benchmark."
6. **l.603 (tabela):** "Planckian UV Renormalizability" → "Power-counting heuristic (Hořava $z=3$; not
   established)", ou remover a célula.
7. **l.624:** "two-scale diffusion symbols" → "two-scale symbols (Euclidean heat-kernel traces)".

**Cap. 13** (`chap13_experimental_observational_signatures_quantum_gravity.tex`)

8. **l.49 (resumo):** "For diffusion with the two-scale symbol … we give the return probability" → "For the
   Euclidean heat kernel of the two-scale symbol … we give its diagonal". Na mesma linha, "the diffusion model
   suggests" → ver o item 10.
9. **l.65:** "The diffusion kernel with the isotropic symbol" → "The heat kernel of the isotropic symbol (not a
   positive kernel, hence not a diffusion in the probabilistic sense)"; "the return probability is" → "its
   diagonal is". **l.56 e l.126:** "a diffusion" / "a two-scale diffusion" → "a heat kernel" / "a two-scale heat
   kernel".
10. **l.88 e l.94:** as mesmas inserções dos itens 4 e 5 (ξ ≠ 0 ⇒ referencial preferido e termo k⁶ para
    d_s = 2; ℓ* ≫ ℓ_P no ramo de Hořava; atraso reescalado).

**Artigo SQG** (`manuscript_simplicial_quantum_gravity_master.tex`)

11. **l.100 (resumo):** "two-scale diffusion symbol" → "two-scale symbol"; acrescentar "the associated heat kernel
    is not positive, so $d_s$ is a property of the heat-kernel trace, not of a diffusion process".
12. **Remark l.259–261** ("Scope of the diffusion model" → "Scope of the heat-kernel model"): acrescentar a
    Prop. C1 (Marcinkiewicz; CES 2013), a realização z = 3 sem ghost com seus custos (folheação, modo escalar,
    acoplamento forte; BPS 2010/2011) e a janela de M*.
13. **l.510 (tabela):** "Short-scale diffusion with $d_s=2$" → "Short-scale heat-kernel scaling $d_s=2$".
    **l.500:** acrescentar "ghost-free only in an anisotropic $z=3$ realization (not derived)".
14. **l.571–576:** as mesmas inserções dos itens 4 e 5.

## 6. Novas conjecturas e problemas abertos

- **[aberto] O1 — derivação.** Algum operador simplicial do livro (o Beta-Laplaciano ou o operador em
  Δ₄×Δ₂ com folheação minimax) induz, num limite contínuo, um símbolo anisotrópico com z = 3? Uma resposta
  positiva transformaria o ramo (b) de citação em resultado. Hoje o texto diz (SQG, Remark) que o símbolo "is not
  induced by the kernel".
- **[aberto] O2 — janela de M*.** Com os vínculos citados, 10¹⁰ ≲ M* ≲ 10¹⁵–10¹⁶ GeV, e Pospelov–Shang empurram
  para ~10¹⁰ GeV. Se o livro quiser um ramo lorentziano, precisa aceitar M* ≠ M_P e dizer de onde vem a
  hierarquia M*/M_P ~ 10⁻⁹.
- **[aberto] O3 — proteção de LV na matéria.** Que mecanismo protegeria o setor de matéria do livro (o setor de
  férmions com ansatz circulante)? Candidatos: separação de escalas (Pospelov–Shang, que exige termos de dimensão
  de Lifshitz mais alta para matar divergências quadráticas) ou supersimetria (Groot Nibbelink–Pospelov). Não há
  resposta no livro.
- **[aberto] O4 — escala de acoplamento forte.** Se O1 der um z = 3 com khronon, é preciso calcular M_SC ~ √α M_P
  e verificar M* < M_SC.
- **[aberto, provavelmente difícil] O5 — versão positiva.** Existe um processo genuíno, não invariante por
  translação ou com tempo não linear à la CES 2013, cujo d_s(τ) coincide com a forma erfc do livro? Pela Prop. C2,
  a invariância por translação precisa ser abandonada ou o tempo reparametrizado. CES 2013 já fazem isso para
  outros perfis, então é preciso checar o precedente antes de qualquer reivindicação.
- **[heurístico] O6 — LW/fakeon.** Uma formulação fakeon do ramo (a) preservaria a forma fechada euclidiana e o
  potencial α = −1, mas com acausalidade em escalas ≲ ℓ. É um caminho possível, com custo físico declarado, não
  uma solução.

## 7. Incertezas

- As afirmações sobre renormalizabilidade da versão projetável e não projetável, Collins et al., Stelle 4/3–1/3,
  Groot Nibbelink–Pospelov e o limite de GW170817 foram conferidas só por título ou resumo (ver `refs.md`). A
  camada 2 deve ler os textos.
- A Prop. C2 usa a cota Re ψ ≤ C(1+|k|²) para expoentes de Lévy. Ela é clássica (Berg–Forst; Jacob), mas a
  referência de livro com ISBN ainda não foi resolvida.
- Os números de 38–40 ordens assumem ξ ~ 1/2 e M* = 10¹⁰ GeV. Com M* = 10¹⁶ GeV, o fator é (ℓ*/ℓ_P)² ≈ 1,5×10⁶,
  e a distância ao alcance fica em ~50 ordens.
