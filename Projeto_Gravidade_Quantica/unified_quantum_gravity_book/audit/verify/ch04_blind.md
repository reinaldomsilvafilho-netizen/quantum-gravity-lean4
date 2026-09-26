# Cap. 4 — reauditoria cega (camada 1)

Arquivo auditado: `chap04_simplicial_waves_porous_transport.tex` (365 linhas). Como o capítulo cita o Cap. 3 (Thm 7.2), `chap03_*.tex` também foi lido. Nenhum ledger, WORKPLAN ou relatório de outro agente foi lido.
Script: `audit/verify/scripts/ch04_blind_checks.py`. Caso m=2, α=2, com oráculos independentes: quadratura mpmath do símbolo, jacobiano numérico por diferenças finitas da NLSE e Hessiano numérico de E_β(−Kσt^β) com série de Mittag-Leffler própria. Controles negativos incluídos.

Numeração: Def 2.1, Rem 2.2, Prop 2.3, Rem 2.4, Rem 2.5, Thm 2.6; Thm 3.1, Thm 3.2, Conj 3.3, Rem 3.4; Def 4.1, Thm 4.2, Thm 4.3, Rem 4.4.

| Item | Enunciado | Rótulo honesto? | Veredito | Evidência/observação |
|---|---|---|---|---|
| Intro | Integral de Riesz de (−Δ)^{α/2}, isotropia O(d), caudas algébricas | clássico | CONFIRMA | Fórmula padrão (0<α<2). A motivação física (rochas, metamateriais) é só narrativa, sem afirmação testável. |
| Def 2.1 | Δ^α_{Δm} "self-adjoint acting on u∈H²" | — | PROBLEMA (B) | O operador é limitado em L² (Rem 2.4), então restringir a H² é desnecessário e conflita com a Rem 2.4 ("no domain restrictions"). |
| Rem 2.2 / dimensões | α é ao mesmo tempo ordem (entra em Γ(α+1), adimensional) e raio de suporte (comprimento) | ansatz declarado | PROBLEMA (B) | Checagem dimensional (regra 8): σ tem unidade 1/α². Então ħ²σ/(2M) só é energia se as distâncias forem medidas numa unidade fixa ℓ₀ implícita. A NLSE (eq. 3.1) é dimensionalmente consistente apenas nessa convenção, que o texto não declara. |
| Prop 2.3 | −Δ simétrico e ≥0; forma quadrática (1/(2α²I))∫∫binom\|u(x+y)−u(x)\|² | sim | CONFIRMA, com B | Refeita a conta de translação (fator 2Re confere). "Vanishing iff u is constant" deveria dizer "iff u=0" em L²: invariância por um aberto de translações força u constante, logo nula. |
| Rem 2.4 | Limitado, 0≤−Δ≤2/α² | sim | CONFIRMA | Numérico: sup σ ≈ 0.3214 < 2/α² = 0.5; σ(k)→1/α² = 0.25 quando k cresce (σ(40)=0.2520). |
| Rem 2.5 (a) | Laplaciano fracionário espectral ≠ restrito para s∈(0,1) | clássico, sem citação | CONFIRMA, com B | Resultado conhecido (Servadei–Valdinoci 2014), mas sem referência. |
| Rem 2.5 (b) | Dom((−Δ_D)²) = {u∈H⁴: u=Δu=0 em ∂Ω} (condições de Navier), "for instance a simplex" | parcialmente | PROBLEMA (B/M) | Correto para ∂Ω suave. Num **simplexo** (domínio com cantos/arestas), a regularidade H⁴ falha em geral. O domínio correto é {u∈H²∩H¹₀ : Δu∈H²∩H¹₀}. O exemplo escolhido é justamente o caso em que a afirmação H⁴ não vale. O rótulo interno `thm:biharmonic_boundary` sobre um Remark é resto de versão (cosmético). |
| Thm 2.6 | Símbolo em [0,2/α²], par, real-analítico; σ ≈ k^T M2 k/(2α²), M2 = a Id + b 11^T | citado do Cap. 3, Thm 7.2 | CONFIRMA | A referência "Thm 7.2" do Cap. 3 está certa. O símbolo é na verdade inteiro (FT de suporte compacto). |
| Thm 2.6, parêntese | "fecho 1−R^α cos(αΘ) e limite (1/(2mα))k^T A k pertencem ao multinomial de rede" | não inteiramente | PROBLEMA (B) | O fecho fechado de rede confere. O limite **não**: para o multinomial de rede, σ_lat ≈ S²/(2m²) + (Q−S²/m)/(2mα), com S=Σk, Q=\|k\|². Com m=3, α=7, k=(1e−3, 2e−3): rede 5.476e−7 vs (1/(2mα))kGk = 3.333e−7. Só coincidem com Σk=0: 4.762e−8 = 4.762e−8. (Também coincidem em α=m+1, por acaso.) O Cap. 3, Rem 7.3 diz corretamente "só com vínculo Σk=0"; o Cap. 4 atribui mal. |
| Eq. 3.1 (NLSE) | iħψ_t = −(ħ²/2M)Δψ + Vψ − κ\|ψ\|^{2p}ψ | definição | — | Sem afirmação de boa colocação. Isso é aceitável, porque os teoremas supõem uma solução suave. |
| Thm 3.1 (massa) | N conservada | sim | CONFIRMA | Im(ψ*·eq) reproduzido; ⟨ψ,Δψ⟩ é real porque Δ é simétrico e limitado; V real. |
| Thm 3.1 (energia) | E conservada | sim | CONFIRMA, com B | δE/δψ* = Hψ, e Re((i/ħ)\|Hψ\|²) = 0. Confere, supondo V independente de t. A normalização da transformada de Fourier em ∫σ\|ψ̂\|²dk não é declarada: sem ela aparece um fator (2π)^{−(m−1)}. |
| Estado de fundo | μ₀ = −κρ₀^p | — | CONFIRMA, com B | Exige V≡0 (Δ de constante = 0), o que o Thm 3.2 não declara. |
| Thm 3.2 (dispersão) | ħ²Ω² = ε(ε−2κpρ₀^p), ε = ħ²σ/(2M) | sim | CONFIRMA | Linearização refeita à mão. O jacobiano numérico (κ=0.3, p=1.5, ρ₀=0.8) dá Ω² = −0.0119083, −0.0623279, −0.0626743 em k=0.5, 1.5, 4, igual à fórmula até 1e−11. O mutante sem o fator 2 dá −0.00577, −0.0241 e falha. |
| Thm 3.2 (banda, γ_max) | instável para σ < 4Mκpρ₀^p/ħ²; γ_max = κpρ₀^p/ħ no conjunto σ = 2Mκpρ₀^p/ħ²; "todo vetor de onda" instável se o limiar > sup σ | sim | CONFIRMA, com B | Minimização em ε conferida. Ressalvas: (i) "every wavevector" deveria ser "todo k≠0" (σ(0)=0 dá Ω=0). (ii) O conjunto ressonante é não vazio quando o valor é < sup σ; com igualdade, depende de o sup ser atingido. (iii) O título "on simplicial torus" não corresponde ao domínio ℝ^{m−1} (B). |
| Conj 3.3 (existência) | "ground states of (3.4) exist" (V≡0) | conjectura | PROBLEMA (M) | Com a noção padrão (minimizador de E a massa fixa), **é falso para todo p>0**. O termo cinético é limitado por (ħ²/2M)(2/α²)N, enquanto −κ/(p+1)∫\|ψ\|^{2p+2} → −∞ ao concentrar. Gaussiana de largura w, N=1: E ≤ 0.218, −0.767, −31.9 para w=1, 0.1, 0.01. Logo inf E = −∞ e não existe estado fundamental nesse sentido. A conjectura precisa definir "ground state" (p.ex. solução de energia mínima entre soluções, ou Nehari), senão é falsa ou vazia. |
| Conj 3.3 (simetria) | grupo linear de simetria = S_{m−1}×Z₂, não S_m | enunciado como fato dentro da conjectura | INCERTO | Que S_{m−1}×Z₂ preserva o núcleo simetrizado está verificado. Que não haja outras simetrias lineares não está provado. Consistente com a minha checagem no Cap. 3: a transposição j↔m é afim e não preserva M2. |
| Rem 3.4 | Nem existência nem simetria provadas; decaimento exponencial esperado | honesto | CONFIRMA | Mas ver acima: a existência, na leitura padrão, é refutável. |
| Def 4.1 | Caputo, β∈(0,1] | clássico | CONFIRMA | — |
| Thm 4.2 | û = E_β(−Kσt^β)û₀ | sim | CONFIRMA, com observação | Laplace de Caputo e inversão s^{β−1}/(s^β+a) padrão. Observação: como σ→1/α² quando \|k\|→∞, o propagador tem um **átomo** E_β(−Kt^β/α²)δ(x) que decai lentamente (0.706 em t=3 no teste). A solução para u₀=δ não é uma função. Não é erro, mas deveria ser dito. |
| Thm 4.3 (deriva) | ⟨x⟩=0 | sim | CONFIRMA | σ é par porque o operador é simetrizado, embora o núcleo K̃ tenha média (α/m)1≠0. |
| Thm 4.3 (MSD) | ⟨xxᵀ⟩ = K M2 t^β/(α²Γ(β+1)), exato para todo t | sim | CONFIRMA | O Hessiano numérico de E_β(−Kσt^β) em k=0 (K=0.7, β=0.6, t=3, α=2) dá 0.4834554, e a fórmula 0.4834556. O mutante Γ(β) dá 0.2901 e falha. A exatidão para todo t vem de ∇σ(0)=0. |
| Rem 4.4 | CTRW/Mittag-Leffler padrão; contribuição = núcleo compacto S_{m−1}-simétrico | honesto | CONFIRMA | A atribuição a Metzler–Klafter é adequada. |
| Abstract | conservação; MI "unstable band can cover all wavevectors"; conjectura de simetria; propagador ML; MSD exato | sim | CONFIRMA, com B | Tudo corresponde ao corpo, exceto que "all wavevectors" deve excluir k=0. Não repete o "S_m-invariant" do Cap. 3. |
| Conclusão | Resume os resultados; "simplicial permeability tensor" | sim | CONFIRMA | "Permeability tensor" é só um nome para M2 (segundo momento, não covariância). |
| Citações | Podlubny, Samko, Metzler–Klafter 2000, Laskin 2000, Cap. 3 | — | B | Adequadas. A Rem 2.5 não tem referência. |

## Resumo por gravidade

**A (erro matemático)**
- Nenhum encontrado no corpo. O capítulo herda do Cap. 3 apenas o Thm 7.2, que confere.

**M (lacuna ou rótulo errado)**
- Conj 3.3: "ground states exist" é falso na acepção padrão. A energia a massa fixa é ilimitada inferiormente para todo p>0, porque o termo cinético é limitado (script, bloco "Energy unbounded"). É preciso definir a noção de estado fundamental ou reformular.
- Rem 2.5(b): o domínio H⁴ com condições de Navier é apresentado para "um simplexo", onde a regularidade H⁴ falha.

**B (redação/citação)**
- Thm 2.6, parêntese: o limite (1/(2mα))kᵀAk não pertence ao multinomial de rede sem o vínculo Σk=0. Evidência numérica no script, e isso contradiz a formulação correta do Cap. 3, Rem 7.3.
- Def 2.1 "u∈H²" conflita com a limitação em L².
- Prop 2.3: "iff u constant" deveria ser "iff u=0".
- Checagem dimensional: α é adimensional (ordem) e comprimento (raio) ao mesmo tempo, então a NLSE só é consistente com uma unidade ℓ₀ implícita.
- Thm 3.2: hipótese V≡0 não declarada; "every wavevector" deveria ser k≠0; título "torus" num problema em ℝ^{m−1}.
- Thm 3.1: normalização de Fourier não declarada.
- Thm 4.2: não menciona o átomo em δ(x) do propagador.

Itens verificados: 25 linhas da tabela.
