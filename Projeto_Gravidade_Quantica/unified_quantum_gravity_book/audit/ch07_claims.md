# Cap. 7: ledger de afirmações (auditoria 2026-09-24)

Checagens: `audit/scripts/check_ch07.py` (8 itens, cada um com controle negativo ou contraexemplo explícito).
Corpo reescrito: `audit/_ch07_body.tex`, aplicado via `splice_block.py`. A versão anterior está em `audit/baseline_v2.2/`.

| ID (antigo) | Enunciado | Tipo | Veredito | Ação |
|---|---|---|---|---|
| Abstract | "3 foundational theorems", "exact synthesis", "master classification" | — | excesso; 2 dos 3 "teoremas" não têm prova | reescrito com lista provado/aberto |
| §1.2 | "L∞ + volume não impede degeneração topológica (Cheeger–Gromov, Langer)" | CL | **ao contrário**: Langer/Breuning dão finitos tipos de difeomorfismo | corrigido |
| §1.3 | Tie-breaker: "área estritamente convexa ⇒ minimizador canônico único" | NE | falso (área não é convexa em espaços de subvariedades) | Remark sem alegação de existência/unicidade |
| T1.1 | Gap topológico emb./imm. | NE | (1) sem prova; (2) vago | substituído por **Prop. provada** (Fáry–Milnor + Fenchel): gap ≥ 2π/L para nós |
| §1.4 | "Axioma": algoritmo exato para n≤4; NP-difícil para n≥5 | HE | sem prova | Remark de escopo (só cotas superiores) |
| §2.2 | reach(ℝⁿ∖Ω)>0 ⇒ ∂Ω ∈ C^{1,1} | CL | **falso** (poliedro convexo tem reach infinito); precisa das duas faces | corrigido |
| §2.3 | PMP ⇒ bang-bang ⇒ saturado/plano para subvariedades | NE | sem objetivo; controle escalar só vale em n=2; não se estende a k≥2 | **Prop. provada** (dualidade de Dubins) + limites explícitos |
| Alg. 3.1 | Pipeline construtivo; "κ*≥2/w_min" para k≥2 | HE | a cota vale só para U-turn planar; em fatia de ℝ³ falha (item 7) | rotulado heurística; cota restrita |
| T4.1 | Partição estrutural; $\mathcal H^k(\mathcal S)>0$ "via Hopf" | NE | partição é definição; positividade sem prova | Definição + **Conjectura** |
| T4.2 | Exclusão por obstáculo: $\|\II_{\partial\Omega}\|\le\kappa^*$ no contato; zonas agudas intocáveis | NE | **falso** para obstáculo convexo (reta tangente a bola, item 6) | **Prop. provada** com sinal correto: $\|\II_M\|\ge\lambda_k(h)$, $h$ medida para Ω |
| T4.3(1) | Piso de fronteira $\kappa^*\ge\sup\|\II_\Sigma\|$ | NE | **desigualdade invertida** (disco plano) | retirado com contraexemplo |
| T4.3(2,3) | Ângulo de giro; U-turn 2/w | CL/NP | corretos; prova antiga do 2/w era só "diâmetro do círculo osculador" | prova completa (a mesma do cap. 8) |
| T4.3(4) | Sagitta $\kappa^*\ge 8d/L^2$ | NE | **falso** (semicírculo: 2/L vs 4/L; item 4) | retirado |
| T4.4 | Homotopia, equioscilação de Chebyshev, "C² toll" estrito, dominância de semiespaço | NE | (1) tautologia; (2) = conjectura; (3) falso como ínfimo (contradiz T5.1); (4) sem prova | Remark |
| T5.1 | Invariância de regularidade | NE | prova sem conteúdo (Azagra–Ferrera, "ajuste conforme"); ignora fronteira/obstáculo/volume | **Conjectura** + Remark do que falta |
| T5.2 | "Caffarelli": falha de C³; penalidade ≥ κ*+O(ε) | NE | vazio/contraditório | Remark (Dubins: C^{1,1}, não C²) |
| T5.3 | Γ-convergência DEC | NE | sem prova | **Conjectura** |
| T5.4 | AMR | HE | não é teorema | Remark |
| T5.5 | Monotonicidade dimensional | NP | correto (trivial) | mantido; legenda da figura dizia "estritamente" → corrigida |
| T5.6 | Lei de escala multi-hélice | NP | hipótese trocada ("raio de giro ≥ R₀" dá curvatura ≤); com a hipótese certa a prova vale; a hélice de fases iguais é um círculo plano | **Prop. condicional** com hipótese explícita |
| T5.7 | Existência $C^{1,1}$ (Langer) para todo k com fronteira | CL | Langer é para superfícies fechadas em ℝ³; sem versão com fronteira | **Prop. provada para k=1** (Arzelà–Ascoli); Remark para k≥2 (Breuning) |
| §6 | Semicírculo, hélice, cilindro, Clifford, hipercilindro | NP | curvaturas corretas (Clifford conferido, item 2); **cilindro não é ótimo** (bojo reduz para 0,73, item 5) | valores mantidos como candidatos/cotas superiores |
| Tab. 7.1 | "Classificação universal n≤12" | NE | linhas multi-hélice com amplitude errada (curvatura 1/R₀, item 3); "SL T³" não é mínimo; linhas G₂/Spin(7)/ℝ¹⁰⁻¹² sem derivação | tabela reduzida a famílias com curvatura exata |
| T7.1 | Calibradas: $\|\II\|_{op}=\|\II\|_F/\sqrt c$, minimizam $\|\II\|_{op}$ | NE | **falso** (curvas complexas: razão 1/2, item 1) | retirado |
| §8 | Fractal, correção de canto, Gauss–Bonnet–Chern com $(2\pi)^m$ | NE | canto: sem sentido ($C^1$ não tem curvatura); GBC: constante não derivada | **Prop. provada** para superfícies (qualquer codimensão); resto em Remark |
| Bib. | Langer 1985 (título/periódico errados, também caps. 8, 9); Wardetzky (DOI de outro trabalho) | — | — | corrigidos; adicionados Milnor 1950, Breuning 2015 (DOI conferido no Crossref: final **-7**), Gilbarg–Trudinger |

Propagação: cap. 8 (F-34): "Non-Euclidean Regularity Invariance" rebaixado; tabela de candidatos corrigida (AdS removida, FLRW $H$ e não $3H$); referências ao "teorema de Γ-convergência" do cap. 7 viraram conjectura.
