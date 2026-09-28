# Verificação independente: `consistencia_operador/` (camada 1, quatro olhos)

Data: 2026-09-28. Verificador: Claude (Opus), sem participação na redação do rascunho. Não editei
README, refs, scripts do rascunho, capítulos, artigo nem WORKPLAN.

## Como verifiquei

- **Scripts próprios** em `verify/`, com oráculos diferentes dos do rascunho:
  - `v1_ghost_yukawa.py`, 15/15: resíduos por limite (s−s₀)G(s), sem `apart` nem contorno; potencial por
    transformada seno radial (mpmath `quadosc`); v_g por diferenciação dos ramos exatos.
  - `v2_kernel_sign_ds.py`, 17/17:
    - sinal do núcleo pela **marginal 1D**: se o núcleo 4D fosse ≥ 0, a marginal também seria;
    - conferência cruzada com o núcleo radial 4D via J₁;
    - d_s por derivada numérica da forma erfc do livro;
    - Hořava z = 2, 3;
    - contraexemplo não local (ver A12).
  - `v3_numbers.py`, 11/11: atrasos **recalculados** pela fórmula do livro (não apenas reescalados), janelas
    de M*, limites do GW170817. Controle negativo: reescala linear em ℓ.
- **Controles negativos:**
  - resíduo sadio +1;
  - potencial com 1 + e^{−r/ℓ};
  - marginais gaussiana e de Cauchy ≥ 0;
  - forma erfc sem e^{z²};
  - reescala em ℓ em vez de ℓ².
- **Scripts do rascunho reexecutados** (saídas em `verify/rerun_*.out.txt`): a 14/14, b 16/16, c 18/18, d 10/10.
  As saídas são idênticas às gravadas, exceto por avisos de quadratura do scipy em `c_`.
- **Fontes lidas:**
  - no texto completo (PDF do arXiv, extraído com `pdftotext`): BPS 2011 (arXiv:1007.3503, eqs. 5.16–5.17,
    5.21 e conclusões) e Pospelov–Shang (arXiv:1010.5249, conclusões);
  - só o resumo: CES 2013 (arXiv:1304.7247), Barvinsky et al. 2016 (arXiv:1512.02250) e Collins et al. 2004
    (gr-qc/0403053).
- **Linhas citadas:** conferi uma a uma com `sed -n` nos três `.tex`.

## Tabela de veredictos

| # | Afirmação do rascunho | Veredicto | Evidência |
|---|---|---|---|
| A1 | 1/(k²+ℓ²k⁴) lorentziano: polo em p² = −1/ℓ² com resíduo −1 (ghost) | CONFIRMA | `v1`: resíduo −1,00000000001 para ℓ = 0,4, 1 e 3; o controle sadio dá +1. No plano da energia, o resíduo tem sinal oposto ao do campo massivo sadio (±0,40962). |
| A2 | Potencial estático V = −(GM/r)(1 − e^{−r/ℓ}), Yukawa α = −1, V(0) = −GM/ℓ | CONFIRMA | `v1`: erro relativo < 4×10⁻³⁰ contra a forma fechada; o mutante 1 + e^{−r/ℓ} erra de 4% a 3900%. |
| A3 | O operador isotrópico **não** é superluminal | CONFIRMA | Os ramos são E² = k² e E² = k² + ℓ⁻², com v_g ≤ 1 (`v1` A5). A superluminalidade vem só do *ansatz* ω² = c²k²(1+ξℓ²k²) com ξ > 0. |
| A4 | Stelle 1978: spin 2 contribui −4/3, spin 0 +1/3 | CONFIRMA | É o resultado padrão, V = −(GM/r)(1 + e^{−m₀r}/3 − 4e^{−m₂r}/3). Não reli o artigo; nível "conhecimento padrão". |
| A5 | BPS 2011: M* ≲ 10¹⁵–10¹⁶ GeV (eq. 5.17); M*(mat) ≳ 10¹⁰–10¹¹ GeV (eq. 5.21), com ressalva | CONFIRMA | Texto, eq. (5.17): "constrains M_α to be lower than 10¹⁵ ÷ 10¹⁶ GeV … M* ≲ 10¹⁵ ÷ 10¹⁶ GeV". Eq. (5.21), com "this lower bound must be taken cautiously". O resumo diz, literalmente, "the only model which is free from instabilities and strong coupling is the non-projectable one". |
| A6 | Pospelov–Shang: Λ_HL ≲ 10¹⁰ GeV | CONFIRMA | Conclusões: "constraints on dimension 4 LV operators are more stringent than 10⁻²⁰, one would need to have Λ_HL < 10¹⁰ GeV". Os autores acrescentam que uma afirmação "much more definitive" exige estender o cálculo aos férmions do Modelo Padrão, e o texto do livro deve manter o "suggests". Nota: o título publicado é "Lorentz violation in Hořava-Lifshitz-type theories"; no arXiv é "On Lorentz violation…". |
| A7 | Prop. C1: o núcleo de e^{−τ(k²+ℓ²k⁴)} assume valores negativos para **todo** τ > 0 (Marcinkiewicz) | CONFIRMA | A lógica é válida. A marginal numa reta tem função característica exp(−τ(t²+ℓ²t⁴)), e pelo teorema de Marcinkiewicz (grau ≤ 2) ela não pode ser uma densidade. O DOI 10.1007/BF01210677 resolve; o enunciado é o clássico (Lukacs, *Characteristic Functions*). Numericamente (`v2`), a marginal 1D é negativa em τ = 0,01, 1 e 10, e também para k²+k⁶. A razão 4D K(1,937)/K(0) = −0,018934 reproduz o −1,893×10⁻² do rascunho. |
| A8 | CES 2013 registram que as difusões "quantum-improved", inclusive a de Hořava–Lifshitz, não são positivas | CONFIRMA | Resumo: "a crucial property, namely positivity of their solutions, is not preserved automatically … applicable to … Horava-Lifshitz gravity". Confirmei o trecho literal da Sec. II só pelo resumo. |
| A9 | Prop. C2: nenhuma difusão de Lévy invariante por translação em ℝ⁴ dá d_s = 2 no UV | INCERTO | A conclusão está certa para processos **simétricos** (ψ real). A prova escreve P(τ) ≥ ∫e^{−τ Re ψ}, mas para ψ complexo vale p_τ(0) = (2π)^{−m}∫e^{−τ Re ψ}cos(τ Im ψ), e a cota inferior não segue como está escrita. Correção: restringir a semigrupos simétricos (autoadjuntos), o caso do traço do núcleo de calor, ou tratar o drift à parte. A referência de livro (Berg–Forst/Jacob) continua sem ISBN resolvido. |
| A10 | d_s: símbolo do livro 4 → 2, aproximação no IR 4 − 12ℓ²/τ; Hořava 1 + 3/z (z = 3 → 2, z = 2 → 5/2) | CONFIRMA | `v2`: erfc = quadratura a 4×10⁻²²; d_s(10⁻⁸) = 2,00009 e d_s(10⁸) = 4,0000000; d_s(10⁴) = 3,9988017, contra 3,9988 previsto. Hořava: 2,50001 e 2,0000. |
| A11 | Prop. B2: o ansatz com ξ ≠ 0 só dá d_s = 2 com um termo k⁶ adicional | CONFIRMA | Dentro da família −∂_t² + F(k²) com F polinomial, d_s(UV) = 1 + 3/z, com 2z = grau de F. O k⁴ sozinho dá 5/2. A condição a > −2 é exatamente a positividade de 1 + au + u². |
| A12 | "É o único ramo lorentziano sem ghost que dá d_s = 2" (§2 veredito b); "The ghost-free Lorentzian operator with ultraviolet value d_s = 2 is the anisotropic z = 3 operator" (item 3); "ghost-free only in an anisotropic z = 3 realization" (item 13) | **REFUTA** | Contraexemplo invariante de Lorentz, não local, do tipo Tomboulis (1997) / Modesto (2012; o rascunho lista Modesto em `refs.md` mas não o usa): S(p²) = p²·exp(½Ein(ℓ⁴p⁴)), com Ein(x) = γ + ln x + E₁(x) inteira. O fator de forma é inteiro e sem zeros, logo o propagador só tem o polo sem massa (sem ghost). No eixo euclidiano S ~ e^{γ/2}ℓ²k⁴, e `v2` X1 dá d_s(10⁻⁷) = 2,0 e d_s(10⁷) = 4,0. O custo é a não localidade, com unitariedade e causalidade em loops dependentes de prescrição. A frase deve dizer "a **local** ghost-free realization" ou citar também os fatores de forma inteiros. |
| A13 | ℓ* ≈ 2×10⁻³² a 2×10⁻²⁶ m, 10³ a 10⁹ ℓ_P; (ℓ*/ℓ_P)² ≈ 1,5×10¹⁸; atrasos ~10⁻⁴³–2×10⁻⁴² s; "10⁵⁶ → ~10³⁸" | CONFIRMA | `v3`, recalculando pela fórmula do livro: 9,6×10⁻⁴⁴ a 1,7×10⁻⁴² s, ou seja, 37,8 a 39,0 ordens abaixo de 10⁻⁴ s ("38–39" é mais exato que "38–40"). 56 − 18,17 = 37,8. Com M* = 10¹⁶ GeV, o fator é 1,49×10⁶ e ficam 49,8–51,0 ordens. Dimensão: [ℓ²/c³ · m · s⁻²] = s. Os atrasos 6×10⁻⁶², 3×10⁻⁶¹ e 1,2×10⁻⁶⁰ s do livro são reproduzidos (6,4; 2,9; 11,6). |
| A14 | GW170817: ℓ* < 2×10⁻² m (quártico, ξ = 1) e < 89 m (z = 3) | CONFIRMA | `v3`: 2,13×10⁻² m e 88,8 m; o coeficiente (5/2)x⁴ também foi verificado. |
| A15 | Renormalizabilidade provada para a versão projetável (Barvinsky et al. 2016); sem prova para a não projetável | CONFIRMA | Resumo: "We prove perturbative renormalizability of projectable Horava gravity … We also comment on the difficulties of this approach when addressing the renormalizability of the non-projectable model." |
| A15b | "A versão projetável é a 'bad' de BPS 2011" | INCERTO | O texto de BPS 2011 não usa "good"/"bad" fora do título; a atribuição é inferência. O conteúdo (a projetável tem instabilidade/acoplamento forte) está confirmado pelo resumo. Sugiro não pôr o rótulo entre aspas. |
| A16 | Collins et al. 2004: LV no UV induz LV de dimensão 4 não suprimida no IR, salvo ajuste fino | CONFIRMA | Resumo: um referencial preferido na escala de Planck dá "Lorentz violation at the percent level … unless … fine-tuning". São 5 autores (Collins, Perez, Sudarsky, Urrutia, Vucetich); `refs.md` está certo. |
| A17 | Tabela §1: citações de linhas nos caps. 12 e 13 e no SQG | CONFIRMA, com exceção | As linhas 99, 160, 172, 174, 177, 511, 513, 524, 566, 570, 603 e 624 (cap. 12), 49, 56, 65, 88, 94 e 126 (cap. 13) e 100, 241–261, 500, 510, 538 e 571–576 (SQG) contêm o que é descrito. Exceção: ver A18. |
| A18 | Tabela §1, linha "cap. 12, l.562–570: … 'diffusion model suggests ℓ* = ℓ_P'" | **REFUTA** | `grep` mostra que o cap. 12 **não contém** "suggest" nesse trecho. A frase está no cap. 13, l.88, e no SQG, l.571. O cap. 12 só **usa** ℓ* = ℓ_P na l.570. |
| A19 | Item 1 (cap. 12, l.99) | CONFIRMA | O texto citado existe; a mudança é correta e coerente com A7. |
| A20 | Item 2 (cap. 12, l.511 e l.524) | CONFIRMA | "the return probability" está na l.511; "this particular diffusion model" e "Whether quantum spacetime…" estão na l.524. É coerente com a l.174 do próprio capítulo. |
| A21 | Item 3 (cap. 12, l.511) | **REFUTA** | A inserção afirma unicidade ("The ghost-free … is the … z = 3 operator"), o que é falso por A12. Basta trocar por "A local ghost-free …". |
| A22 | Item 4 (cap. 12, l.566) | **REFUTA** | Há dois problemas. (i) Manda substituir "suggests ℓ* = ℓ_P", que **não existe** no cap. 12 (A18). (ii) "any ξ ≠ 0 presupposes a preferred frame, and v_g > c" está errado: v_g > c só para ξ > 0; para ξ < 0, v_g < c (`v1` A5b: 1,066 contra 0,931). Os números de M* estão certos (A5, A6). |
| A23 | Item 5 (cap. 12, l.570) | CONFIRMA | O fator 1,5×10¹⁸ e o intervalo ~10⁻⁴³–10⁻⁴² s estão certos. "some 38 orders" também (37,8–39,0). |
| A24 | Item 6 (cap. 12, l.603) | CONFIRMA | A célula "Planckian UV Renormalizability" está na l.603, e o próprio cap. 12, l.172, diz "not established". |
| A25 | Item 7 (cap. 12, l.624) | CONFIRMA | O texto está na l.624. |
| A26 | Item 8 (cap. 13, l.49) | CONFIRMA, com ressalva | "For diffusion with the two-scale symbol … the return probability" está na l.49. "Na mesma linha, 'the diffusion model suggests'" é falso: essa frase está na l.88. A mudança em si é correta. |
| A27 | Item 9 (cap. 13, l.65, 56 e 126) | CONFIRMA | As três expressões existem nas linhas citadas. |
| A28 | Item 10 (cap. 13, l.88 e 94) | INCERTO | As linhas estão certas ("suggests" na l.88; números na l.94), mas o item herda o erro de sinal de ξ do item 4 (A22). Fica correto se usar "v_g > c for ξ > 0". |
| A29 | Item 11 (SQG, l.100) | CONFIRMA | O texto está presente e a mudança é coerente com A7. |
| A30 | Item 12 (Remark do SQG, l.259–261) | CONFIRMA | A Remark já menciona ghost e Hořava; o acréscimo é correto. Deve evitar a unicidade (A12). |
| A31 | Item 13 (SQG, l.510 e 500) | **REFUTA** (parte l.500) | A mudança na l.510 está correta. Na l.500, "ghost-free only in an anisotropic z = 3 realization" é falso por A12. |
| A32 | Item 14 (SQG, l.571–576) | INCERTO | As linhas estão certas ("suggests ℓ* = ℓ_P" está na l.571), mas o item herda o erro de ξ do item 4. |
| A33 | Recomendação "adotar o ramo (c)" | CONFIRMA | O ramo (c) é exatamente o que a Prop. do livro prova (traço do núcleo de calor / lei de Weyl), e é consistente com A7 e A10. |

## Contagem

CONFIRMA 25 · REFUTA 5 (A12, A18, A21, A22, A31) · INCERTO 4 (A9, A15b, A28, A32).

As refutações vêm de duas causas.
1. **Unicidade da realização z = 3** (A12, A21, A31): basta qualificar como "local" e citar os fatores de forma
   inteiros (Tomboulis 1997; Modesto 2012), já presentes em `refs.md`.
2. **Localização e sinal** (A18, A22): a frase "suggests ℓ* = ℓ_P" não está no cap. 12. Além disso,
   v_g > c vale só para ξ > 0.

Nenhuma afirmação física central do rascunho foi derrubada: ghost, α = −1, não positividade, janelas de M* e
reescala dos atrasos estão todos corretos.
