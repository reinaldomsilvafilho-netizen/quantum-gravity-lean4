# Capítulo 8: reauditoria cega (camada 1)

Arquivo: `chap08_noneuclidean_minimax_relativity_adm.tex` (660 linhas). O cap. 7 foi consultado só onde o cap. 8 o cita: Conjecturas "Regularity invariance" e "Discrete Γ-convergence", e a Observação "Optimal regularity".
Não li ledgers, WORKPLAN, CHANGELOG, baseline, `audit/scripts/check_*.py` nem relatórios de outros verificadores.

Scripts (todos com controle negativo):
- `audit/verify/scripts/ch08_gr_blind.py`: checagens simbólicas (sympy) de geometria e RG. Resultado: `ALL CHECKS PASSED`.
- `audit/verify/scripts/ch08_uturn_curved.py`: U-turn em H², S² e R², em coordenadas de Fermi. Resultado: `ALL CHECKS PASSED`.

Numeração (amsart, contador por seção): Def 2.1, Teo 2.2 (Gauss–Codazzi–Ricci), Def 2.3 (norma). Teo 3.1, Lema 3.2, Conj 3.3, Obs 3.4. Teo 4.1 (ADM), Cor 4.2, Prop 4.3, Def 4.4, Def 4.5, Prop 4.6, Obs 4.7, Teo 4.8, Obs 4.9, Prop 4.10, Obs 4.11, Prop 4.12, Def 4.13, Prop 4.14, Prop 4.15, Conj 4.16, Obs 4.17–4.23. Tabela 5.1. Conj 6.1, Obs 6.2.

## Tabela de itens

| Item | Enunciado | Rótulo honesto? | Veredito | Evidência/observação |
|---|---|---|---|---|
| Abstract (1) | Prova de K_M = c + κ² para hipersuperfícies umbílicas | sim | CONFIRMA | Ver Teo 3.1. Há choque de notação: o abstract usa curvatura ±c² e o Teo 3.1 usa c. (B) |
| Abstract (2) | Cota euclidiana 2/w provada. Cotas superiores c·coth(cw/2) e c·cot(cw/2). Otimalidade curva é conjectura | parcialmente | PROBLEMA (M) | A otimalidade curva parece ter prova curta (ver Conj 3.3). As "saturated geometries" listadas não são minimizadores provados (ver Seç. 3.2). |
| Abstract (3) | Os vínculos ADM limitam R; Raychaudhuri com θ≡0 viola a SEC | sim | CONFIRMA | Ver Cor 4.2 e Prop 4.3. |
| Abstract (4) | Horizonte RN em PG; garganta mínima; violação da NEC limitada por K_Gauss | incompleto | PROBLEMA (B) | A cota da NEC exige a hipótese ρ(r0) ≥ 0 (b'(r0) ≥ 0), que o abstract omite. Sem ela, a violação é ilimitada (b' → −∞). |
| Abstract (5) | Aceleração própria = II; problema minimax de worldlines | sim | CONFIRMA | Ver Prop 4.12. |
| Intro §1.1, eq. (1.1) | Definição de κ*(N,g,Ω,Σ,k) como inf sobre A_r(N,g,Ω,Σ,V) | — | PROBLEMA (B) | V aparece sem definição e os argumentos não batem (k à esquerda, V à direita). A Conj 6.1 usa uma terceira assinatura (…,V,r). |
| Intro §1.1 | L¹ (área) e L² (Willmore) "fail to prevent localized curvature singularities" | motivação | PROBLEMA (B) | Afirmação vaga e sem referência. Minimizadores de Willmore são suaves, e obstáculos para área dão C^{1,1}. |
| Intro §1.2 (1) | Curvas temporais não se autointerceptam em espaço-tempo estavelmente causal; κ^{Phys} = κ^{Emb} | sim | CONFIRMA | t é estritamente crescente ao longo de γ. Imersão injetiva de intervalo compacto é mergulho. Os símbolos κ^{*,Phys} e κ^{*,Emb} não estão definidos. (B) |
| Intro §1.2 (2) | Superfícies de Cauchy são mergulhadas | sim | CONFIRMA | Acronalidade implica injetividade. |
| Def 2.1 | Fórmulas de Gauss–Weingarten | sim | CONFIRMA | — |
| Teo 2.2 | Gauss, Codazzi, Ricci com R(X,Y) = ∇X∇Y − ∇Y∇X − ∇[X,Y] | clássico, sim | CONFIRMA | Refiz os sinais à mão. Gauss dá K = κ² para a esfera em R³. Ricci: g(R^⊥ν1,ν2) = g(R̄ν1,ν2) + g([A_{ν1},A_{ν2}]X,Y) está correta nesta convenção. Nota: O'Neill usa a convenção de curvatura oposta, então a citação "Ch. 4" exige ajuste de sinal. (B) |
| Def 2.3 | ‖II_p‖ = sup_{g(v,v)=1} √\|g(II,II)\| = max_{ν∈S(N_pM)} max_i \|κ_i^ν\| | não | PROBLEMA (M) | (a) Em fibrado normal lorentziano (superfície espacial de codim. 2 em espaço-tempo, que é o caso dos horizontes), S(N_pM) não é compacto e o "max" é +∞. Exemplo: esfera t=0, r=R em R^{1,3}, com ν = cosh η e_t + sinh η e_r. Então \|g(II(v,v),ν)\| = sinh η / R → ∞, enquanto √\|g(II,II)\| = 1/R. Script, check 5. (b) Para curvas temporais (Prop 4.12), não existe v com g(v,v) = +1, então o sup é vazio. A definição não cobre o uso feito dela. |
| Teo 3.1 | Hipersuperfície umbílica em N^n(c): K_M = c + κ² | provado | CONFIRMA (com nota B) | Prova correta. Check 1: esfera geodésica em S³ e H³, e o controle c − κ² falha. Notas: (i) para k = 1 (n = 2), K_M não faz sentido e o enunciado deveria exigir n ≥ 3. (ii) A frase "for k = n−1 ≥ 3 Codazzi forces κ constant" é restritiva à toa: o argumento de Codazzi vale para k ≥ 2. |
| Seç. 3.2 (1) | Horosferas: K_M = 0, κ = c | sim | CONFIRMA | Rotular "κ* = c" como valor minimax é abuso: não há problema (Ω,Σ) especificado. (B) |
| Seç. 3.2 (3) | "Equidistant hypersurfaces (κ* = c·tanh(cd)): hyperbolic cylinders at constant distance d from a geodesic" | não | PROBLEMA (A) | Para n ≥ 3, o tubo de raio d em torno de uma **geodésica** em H^n tem curvaturas principais c·coth(cd) (n−2 vezes) e c·tanh(cd). Então ‖II‖_op = c·coth(cd), não c·tanh(cd). O valor tanh vale só para equidistantes de um **hiperplano** totalmente geodésico, ou para n = 2. Script, check 2 (métrica dr² + sinh²r dφ² + cosh²r dt²). |
| Lema 3.2 | U-turn euclidiano em faixa de largura w: k ≥ 2/w, com igualdade para o semicírculo | provado | CONFIRMA | Prova verificada linha a linha: definição de s_a e s_b, θ ∈ (0,π) em (s_a,s_b), fórmula de área para θ Lipschitz, e reflexão y ↦ w − y. A hipótese "direção inicial (1,0)" é essencial: partindo na vertical, basta 1/k. Script C (R²): nenhuma U-turn com 0.97·(2/w). |
| Eq. (3.x) cotas curvas | κ*_{H²} ≤ c·coth(cw/2), κ*_{S²} ≤ c·cot(cw/2); x·coth x > 1 > x·cot x | sim | CONFIRMA | O semicírculo geodésico de raio w/2 centrado em σ é admissível, com tangentes comparadas pelo referencial paralelo das coordenadas de Fermi. Script A reproduz o círculo e o topo em y = ρ. |
| Conj 3.3 | Otimalidade de c·coth(cw/2) e c·cot(cw/2) | rotulada conjectura | PROBLEMA (M): parece ter prova curta | Em coordenadas de Fermi (c = 1), g = dy² + G(y)²dx² com G = cosh y ou cos y, e o ângulo θ é tomado contra o referencial paralelo. Então θ' = κ + (G'/G)(y)·cos θ e y' = sin θ (Liouville; sinal validado no script A, onde o sinal oposto não reproduz círculos). Seja Y(θ) a solução de dY/dθ = sin θ / (k + (G'/G)(Y)·cos θ) com Y(0) = −w/2. Com k = k0, Y é o círculo e Y(π) = w/2. Com k < k0, Y(π) > w/2 (script B). No intervalo (s_a,s_b) do Lema 3.2, Z = y − Y(θ) satisfaz Z' ≥ −C\|Z\|: se θ' ≤ 0, Z' ≥ sin θ ≥ 0; se θ' > 0, usa-se θ' ≤ k + (G'/G)(y)·cos θ e o fato de G'/G ser Lipschitz na faixa. Com Z(s_a) ≥ 0, Gronwall dá Z ≥ 0, logo y(s_b) ≥ Y(π) > w/2 se k < k0, o que é contradição. A "holonomy correction" da Obs 3.4 é justamente o termo absorvido por Gronwall. A busca aleatória (script C: H², w = 1 e 3; S², w = 1 e 2.4) achou 0 U-turns com 0.97·k0 e mais de 200 com 1.03·k0 (controle positivo). Falta conferir, para S² com w ≥ π/2, que o denominador permanece positivo ao longo de Y_k. Recomendação: rebaixar a "conjectura" a proposição com prova, ou justificar por que o argumento acima não serve. |
| Obs 3.4 | O passo faltante é controlar a holonomia | — | PROBLEMA (M) | Ver linha anterior: o controle sai por comparação de EDO mais Gronwall. |
| Seç. 3.4 | Esferas pequenas c·cot(cr) → 1/r; toro de Clifford com K = 0 e κ = 1 | sim | CONFIRMA | Check 3: curvaturas principais ±1. |
| Seç. 4.1 def. K_ij | K_ij := −½ L_n γ_ij = −g(∇̄_{∂i}∂_j, n) | não | PROBLEMA (M) | Com g(n,n) = −1, tem-se −½ L_n γ_ij = +g(∇̄_{∂i}∂_j, n); os dois lados diferem por sinal. Na fatia de Milne em R^{1,3}, −½ L_n γ = −γ/τ, mas −g(∇̄∂∂, n) = +γ/τ. Script, check 4, com controle. Erro de convenção que se propaga para a leitura de θ_l e de Israel. |
| Teo 4.1 | Vínculos hamiltoniano e de momento | clássico, sim | CONFIRMA | Sinais conferem com Gourgoulhon para K = −½ L_n γ. O esboço de prova admite "up to sign". |
| Cor 4.2 | ‖K‖ ≤ κ ⇒ K_ijK^ij ≤ 3κ², σσ ≤ 3κ² − K²/3, −6κ² ≤ R − 16πGρ ≤ 2κ², e as cotas são justas | provado | CONFIRMA (nota B) | e₂ é multiafim, então os extremos estão nos vértices: {3κ², −κ²}. Check 10 usa vértices e 2·10⁵ amostras; o controle "e₂ ≥ 0" falha. Sharpness inferior: hiperboloide de Minkowski (R = −6κ², ρ = 0). A citação "Chapter 12, Theorem 3.1" é desnecessária para um fato elementar e não foi conferida. (B) |
| Prop 4.3 | Congruência geodésica, ω = 0, θ ≡ 0 ⇒ R_{μν}VV = −σσ ≤ 0; a SEC falha onde σ ≠ 0 | provado | CONFIRMA | Raychaudhuri 4D correta. Normais geodésicas exigem só N = N(t); o texto diz "for instance N ≡ 1", o que é correto. |
| Def 4.4 | Slicing minimax sujeito à SEC | — | PROBLEMA (M) | (i) Non sequitur: a Prop 4.3 trata de θ ≡ 0 com N = 1, e minimizar ‖K‖_∞ não força essa configuração. (ii) A restrição "R_{μν}VV ≥ 0 on Ω" é propriedade do espaço-tempo e é vazia se a SEC vale. (iii) Sem condição de contorno, o problema é trivial: em Schwarzschild as fatias t = const (Einstein–Rosen) têm K ≡ 0. |
| Def 4.5 | θ_l := q^{ab} II(e_a,e_b)·l = q^{ab} ∇_a l_b | não | PROBLEMA (M) | Os dois lados têm sinais opostos: II·l = −∇_a l_b, porque g(l, e_b) = 0. Esfera r = R em Minkowski: q^{ab}∇_a l_b = +2/R e q^{ab} II·l = −2/R (check 6). Com a 1ª expressão, as definições de trapped e untrapped se invertem. |
| Prop 4.6 | RN em PG: fatias planas, ‖II_{S+⊂Σ}‖ = 1/r+, θ_l(r+) = 0 | provado | CONFIRMA | Check 7: g_TT = −f; a mudança T = t + ∫β/f dr dá a forma estática, pois f + β² = 1; K^θ_θ = β/r; θ_l = 2(1 − β)/r = 0 em r+ para (M,Q) = (1,0), (1,½), (1,0.9), (2,1), (1,1). Controle com β mutado: θ_l(r+) ≈ −0.47. Também Q²/2M < r+. |
| Obs 4.7 | Na fatia estática √f/r → 0; Kerr–Newman não redondo | sim | CONFIRMA | "Slices degenerate at the horizon" é impreciso: as fatias t = const se encontram na esfera de bifurcação, que é mínima na fatia. (B) |
| Teo 4.8 (Israel) | S_ab = −(1/8πG)([K_ab] − h_ab[K]) | clássico | CONFIRMA (nota B) | É a fórmula de Israel/Poisson com K_ab = ∇_a n_b e n apontando de − para +. Isso é o oposto da convenção K = −½ L_n γ fixada na Seç. 4.1. O capítulo não fixa convenção nem orientação para Σ tipo-tempo. |
| Obs 4.9 | Israel (métrica C^{0,1}) versus cap. 7 (subvariedade C^{1,1}) | — | CONFIRMA (nota B) | Distinção correta. O cap. 7 só *espera* regularidade C^{1,1} ("we have no proof", Obs "Optimal regularity"), e o cap. 8 apresenta isso como fato ("the submanifold is C^{1,1}"). (B) |
| Prop 4.10 | Morris–Thorne: fatia totalmente geodésica, garganta mínima, K_Gauss = 1/r0², ρ + p_r = −(1 − b')/(8πG r0²) e cota por K_Gauss se b' ≥ 0 | provado | CONFIRMA (nota B) | Check 8: tensor de Einstein calculado do zero, 8πGρ = b'/r², p_r confere, 8πG(ρ + p_r)\|_{r0} = (b' − 1)/r0², e o controle com sinal trocado falha. Nota: −½ L_ν(r²dΩ²) tem autovalor −ν(r)/r, não +ν(r)/r. (B) |
| Obs 4.11 | 1/r0 é intrínseco, não extrínseco | sim | CONFIRMA | — |
| Prop 4.12 | II(u,u) = a, a é espacial, ‖II‖ = \|a\| | provado | CONFIRMA (ver Def 2.3) | A prova está correta, mas usa uma norma que a Def 2.3 não define para tangente temporal. |
| Def 4.13 | Problema minimax de worldlines em Ω = exterior | — | CONFIRMA | — |
| Prop 4.14 | R³ menos m bolas é simplesmente conexo; R² menos m discos tem π₁ = F_m | provado | CONFIRMA | Clássico: R³ menos m bolas ≃ ∨S², R² menos m discos ≃ ∨S¹. |
| Prop 4.15 (1) | Curva temporal de p a q ⊂ I⁺(p) ∩ I⁻(q) | provado | PROBLEMA (B) | Os extremos p e q não pertencem a I⁺(p) e I⁻(q) num espaço-tempo cronológico; o correto é o interior da curva ou J⁺ ∩ J⁻. Injetividade: OK. |
| Prop 4.15 (2),(3) | p ∈ B, q ∉ B ⇒ classe vazia; entrar em B não faz κ* divergir | provado | CONFIRMA (nota B) | (2) correto. (3) A finitude de κ* é trivial: basta uma curva C² temporal num compacto. As geodésicas radiais citadas não ligam p a q em geral. Além disso, a Def 4.13 restringe a Ω = exterior, e (2) e (3) saem desse escopo. |
| Conj 4.16 | Minimizador em **cada** classe de winding W ∈ Z; algum W = ±1 bate W = 0 | conjectura | PROBLEMA (A): a 1ª parte é falsa como enunciada | Para curvas temporais no plano equatorial, \|dφ/dt\| < √f/r ≤ 1/(3√3 M), com máximo em r = 3M (check 11). Logo \|Δφ\| < Δt/(3√3 M) e só finitamente muitas classes W são não vazias. Exemplo: Δt = 100M ⇒ \|W\| ≤ 4. Nas demais classes não há minimizador (a classe é vazia). "Fix events p, q … with prescribed coordinate-time separation" é redundante. |
| Obs 4.17 | Rejeita duas afirmações tentadoras; órbitas circulares geodésicas em r > 3M | sim | CONFIRMA | Correto: órbitas circulares temporais geodésicas existem para r > 3M. |
| Obs 4.18 | Minimizadores C^{1,1}; via Conj 6.1, inf em C² = inf em C^{1,1} | heurística | PROBLEMA (M) | A Conj 6.1 do cap. 8 compara C^r com C² (r ≥ 2), não C^{1,1} com C², e é enunciada para N **riemanniana**. Não se aplica a worldlines lorentzianas nem ao par C^{1,1}/C². A versão do cap. 7 compara com A_{1,1}, e a do cap. 8 diverge dela. |
| Seç. 4.9 ¶1 | Fatiamentos maximais "fail to prevent localized runaway of K_ijK^ij" perto de r = 0 | afirmação sem prova | PROBLEMA (M) | Contradiz a própria Tabela 5.1: na fatia limite de Estabrook (maximal), ‖K‖ ≤ 4√3/(9M), logo K_ijK^ij é limitado. O problema conhecido do fatiamento maximal é o *slice stretching* (crescimento de γ_rr), não a explosão de K. |
| Seç. 4.9 item 1 | Σ* = argmin ess sup ‖K‖ ("minimax foliation") | — | PROBLEMA (M) | Sem condições de contorno ou de penetração do horizonte, o ínfimo em Schwarzschild é 0, atingido pela fatia t = const que nem entra no buraco. O objeto é trivial ou mal posto, e a existência do argmin não é discutida. |
| Seç. 4.9 item 2 | Bona–Massó: velocidades α√f reais; limitador preserva hiperbolicidade (conjectura) | conjectura marcada | CONFIRMA | Equação e velocidades de gauge padrão (a rigor α√(f γ^{xx})). (B) |
| Seç. 4.9 item 3 | Barreira μ ≥ d(p, r=0)^{-2} dá folga δ0 (conjectural) | conjectura marcada | PROBLEMA (B) | dist_g(p, singularidade) não está definida: a singularidade não pertence à variedade e g é lorentziana. |
| Seç. 4.10 ¶1 | Plateau de curvatura "admits a direct connection" com a integral de caminho | exagero | PROBLEMA (B) | A Obs 4.19 logo depois admite que é só semelhança estrutural. |
| Obs 4.19 | \|I_GHY\| ≤ (3/8πG) K* Vol₃ | provado (trivial) | CONFIRMA (nota B) | Vale porque \|tr K\| ≤ 3‖K‖. "GHY boundary entropy generation" não tem significado definido. (B) |
| Obs 4.20 | "At the Planck scale where the GHY action truly governs black hole entropy" | física | PROBLEMA (B) | É o contrário: o cálculo euclidiano semiclássico de Gibbons–Hawking vale para buracos grandes (≫ ℓ_P); na escala de Planck ele deixa de valer. |
| Obs 4.21 | Heurística de lensing com minimax de curvatura de geodésicas nulas | heurística marcada | PROBLEMA (M) | A premissa é vazia. Geodésicas nulas afinamente parametrizadas têm ∇_k k = 0, e para curvas nulas a decomposição T ⊕ N não existe (k ∈ k^⊥), então "II" não está definida. A quantidade κ*(λ) da fórmula é nula ou indefinida. "Penrose Affine Parameter" não é termo padrão. (B) |
| Obs 4.22 | K = −3H; cota ‖II‖ ≤ ℓ_P^{-1} ⇒ H² ≲ ℓ_P^{-2}; Friedmann efetiva LQC | analogia marcada | CONFIRMA | K = −3H confere com a convenção K = −½ L_n γ. A equação H² = (8πG/3)ρ(1 − ρ/ρ_c) confere com Ashtekar–Pawłowski–Singh 2006. |
| Eq. P_eff ≤ c⁷/(ħG²) ≈ 4.63·10¹¹³ Pa | Cota de pressão no bounce | afirmada sem derivação | PROBLEMA (M) | Número e dimensão conferem: 4.6329·10¹¹³ Pa, kg·m⁻¹·s⁻² (check 12). Mas a cota não segue do limite ‖K‖ ≤ ℓ_P^{-1}. Em FLRW, p = −(2Ḣ + 3H²)/(8πG) depende de Ḣ, e um limite L^∞ sobre H não controla Ḣ. Só ρ ≤ 3/(8πGℓ_P²) segue. |
| Obs 4.23 | Fator conforme: \|n(ln Ω)\| ≲ ℓ_P^{-1}; bounce com K⁽⁰⁾ = 0 é momento de simetria temporal | parcialmente | CONFIRMA (nota B) | Check 13: κ̃ = κ/Ω + ñ(ln Ω). A cota "ordem ℓ_P^{-1}" vale para a normal unitária de g̃. Com a normal de g, a cota é Ω·ℓ_P^{-1} + \|κ\|. Convém dizer qual n. |
| Tabela linha S^n, curva | Círculo pequeno: c·cot(cR) | sim | CONFIRMA | A coluna rotulada "c" contém a codimensão (n−1), o que colide com c = curvatura. (B) |
| Tabela Clifford | 1 | sim | CONFIRMA | — |
| Tabela H^n, geodesic circle | c·coth(cw/2) | sim | CONFIRMA | — |
| Tabela horosfera | c | sim | CONFIRMA | — |
| Tabela Minkowski | Hiperboloide τ0: ‖K‖ = 1/τ0, "uniform acceleration slice" | valor sim, contexto não | PROBLEMA (B) | O valor confere (check 4: K = −γ/τ0). A fatia t² − \|x\|² = τ0² é a fatia de Milne (tempo próprio constante). "Aceleração uniforme" é o hiperboloide tipo-tempo x² − t² = a^{-2}. |
| Tabela Schwarzschild/Estabrook | \|K^r_r\| = 3√3 M²/(2r³), máximo 4√3/(9M) em r = 3M/2 | sim | CONFIRMA | Check 9: fatia t = h(r) com h' = C/(f√(fr⁴ + C²)); tr K = 0 simbolicamente; \|K^θ_θ\| = C/r³; C² = 27M⁴/16 em r = 3M/2; \|K^r_r\| = 2C/r³. O controle com fator 2 errado falha. Na fatia limite, o valor em r = 3M/2 é atingido no cilindro assintótico. |
| Tabela RN | 1/r+ (dependente do fatiamento) | sim | CONFIRMA | É ‖II‖ em Σ_T, não no espaço-tempo (cf. Def 2.3). |
| Tabela Morris–Thorne | 0, com K_Gauss = r0^{-2} | sim | CONFIRMA | — |
| Tabela FLRW | \|H\| (traço 3H) | sim | CONFIRMA | — |
| Legenda da tabela | "examples and upper bounds, not proven minimizers" | sim | CONFIRMA | Honesta. Contradiz, porém, a Seç. 3.2 ("Saturated Minimax Geometries", "κ* = …"). (B) |
| Título da Seç. 6 | "Fundamental Theorems and Complete Proofs" | não | PROBLEMA (B) | A seção contém só uma conjectura e uma observação. |
| Conj 6.1 | κ*(r) = κ*(2) para r ≥ 2 em N riemanniana | conjectura | PROBLEMA (M) | Diverge da versão do cap. 7 (inf A_r = inf A_{1,1}) e do uso na Obs 4.18. Como enunciada, compara C^r com C² e é mais fraca que a do cap. 7. |
| Obs 6.2 | O molificador ingênuo falha; o caso curvo "reduces to the Euclidean conjecture" | parcialmente | PROBLEMA (M) | As ordens ε^{-4}·ε² e ε^{-2}·ε estão corretas: para h C^{1,1}, \|h − h∗ρ_ε\| = O(ε²). A "redução" ao caso euclidiano não é argumentada: a conjectura euclidiana é igualdade de ínfimos globais em R^n com obstáculo, não um lema local de aproximação transportável por cartas. Termos de Christoffel "de ordem inferior" mudam o valor de κ*. |

Itens verificados: **66** (linhas da tabela).

## Resumo por gravidade

**A (erro matemático/físico)**
1. Seç. 3.2 (3): tubo em torno de geodésica em H^n (n ≥ 3) tem ‖II‖ = c·coth(cd), não c·tanh(cd). O valor tanh é o de equidistantes de hiperplano. `ch08_gr_blind.py` check 2.
2. Conj 4.16: "minimizador em cada classe W ∈ Z" é falso para dados fixos, pois \|dφ/dt\| < 1/(3√3 M) deixa vazias todas as classes com \|W\| grande. Check 11.

**M (lacuna, rótulo errado ou definição inconsistente)**
3. Def 2.3: norma de operador mal definida em fibrado normal lorentziano (max = ∞) e para tangente temporal (sup vazio). Check 5.
4. Seç. 4.1: K_ij = −½ L_n γ = −g(∇̄∂∂, n) tem o sinal errado no 2º membro. Check 4.
5. Def 4.5: θ_l = q^{ab} II·l = q^{ab}∇_a l_b tem os membros com sinais opostos. Check 6.
6. Conj 3.3 e Obs 3.4: a "conjectura" parece ter prova curta por comparação de EDO mais Gronwall em coordenadas de Fermi. `ch08_uturn_curved.py`: sem contraexemplo com 0.97·k0; o controle positivo funciona.
7. Def 4.4: motivação non sequitur, restrição SEC vazia e problema trivial (K ≡ 0 na fatia de Einstein–Rosen).
8. Seç. 4.9 ¶1 e item 1: "maximal slicing fails to prevent runaway of K_ijK^ij" contradiz a própria linha de Estabrook da tabela; o argmin sem condições de contorno é trivial.
9. Obs 4.18 e Conj 6.1: a conjectura de invariância de regularidade é enunciada de forma incompatível com o cap. 7 e com o uso (C^{1,1} vs C²; riemanniano vs lorentziano).
10. Obs 6.2: a "redução ao caso euclidiano" é afirmada sem argumento.
11. Obs 4.21: a heurística de lensing assenta em "II de geodésica nula", que é zero ou indefinida.
12. P_eff ≤ c⁷/(ħG²): não segue de ‖K‖ ≤ ℓ_P^{-1}, pois Ḣ não é controlado. O número e a dimensão estão corretos.

**B (redação/citação)**
13. O abstract (4) omite a hipótese ρ(r0) ≥ 0 da cota da NEC.
14. Notação de κ* e de A_r inconsistente (k, V, r); coluna "c" da tabela = codimensão; choque c versus c².
15. Seç. 3.2 chama exemplos de "saturated minimax geometries" com "κ* = …", o que contradiz a legenda da tabela.
16. Teo 3.1: faltam n ≥ 3; a restrição k ≥ 3 é desnecessária (basta k ≥ 2).
17. Prop 4.15 (1): extremos fora de I^±; (2) e (3) fora do escopo Ω da Def 4.13.
18. Israel: convenção de sinal de K oposta à da Seç. 4.1, sem aviso.
19. Tabela: hiperboloide de Minkowski rotulado "uniform acceleration" (é Milne).
20. Obs 4.20: física invertida (GHY e entropia na escala de Planck).
21. Seç. 4.10 ¶1: "direct connection" exagerado; "GHY entropy generation" sem sentido.
22. Obs 4.9: C^{1,1} do cap. 7 apresentado como fato, quando lá é expectativa.
23. Seç. 4.9 item 3: dist até a singularidade indefinida.
24. Título da Seç. 6 enganoso; citação de O'Neill com convenção de curvatura oposta; "Penrose affine parameter"; citação desnecessária ao cap. 12 na Cor 4.2; sinal de ν(r)/r na prova da Prop 4.10; "is foliate".

**Confirmados sem ressalva substancial:** Teo 2.2, Teo 3.1, Lema 3.2, cotas superiores curvas, Teo 4.1, Cor 4.2, Prop 4.3, Prop 4.6 (horizonte RN em PG), Prop 4.10 (garganta de Morris–Thorne), Prop 4.12, Prop 4.14, valores da tabela (Estabrook 3√3M²/(2r³) e 4√3/(9M), Clifford, horosfera, FLRW), número da pressão de Planck.
