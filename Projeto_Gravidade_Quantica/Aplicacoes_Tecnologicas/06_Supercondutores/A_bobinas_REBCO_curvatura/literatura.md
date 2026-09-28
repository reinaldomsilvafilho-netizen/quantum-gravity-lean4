# Literatura: curvatura/torção em bobinas de fita REBCO

Revisão feita em 2026-09-28. Metodologia: busca (WebSearch), leitura de resumo/texto via WebFetch,
DOI resolvido via Crossref (`api.crossref.org/works/<DOI>`); quando não há DOI, uso o arXiv ID.
"Checado" abaixo significa que o resumo (ou, quando indicado, o texto completo) foi lido nesta
revisão e a autoria/afiliação numérica foi conferida contra essa fonte — não apenas contra o
título do resultado de busca.

## 1. Códigos de otimização de bobinas e como tratam curvatura/torção

1. **C. Zhu, S. R. Hudson, Y. Song, Y. Wan**, "New method to design stellarator coils without the
   winding surface", *Nuclear Fusion* 58, 016008 (2018). DOI: `10.1088/1741-4326/aa8e0a`
   (arXiv:1705.02333). Artigo original do código **FOCUS**: cada bobina é uma curva 1D livre no
   espaço (sem superfície de enrolamento), otimizada por penalidades diferenciáveis somadas ao erro
   de campo. Checado: resumo arXiv + DOI via Crossref.

2. **T. G. Kruger, C. Zhu, A. Bader, D. T. Anderson, L. Singh**, "Constrained stellarator coil
   curvature optimization with FOCUS", *Journal of Plasma Physics* 87, 175870201 (2021).
   DOI: `10.1017/S0022377821000106`. Compara penalidade de curvatura média, curvatura média ao
   quadrado (~L²) e penalidade de curvatura **máxima** (aproximação de L∞); mostra que só a
   penalidade de máximo produz de fato um limite superior de curvatura controlado, enquanto as
   métricas em L² permitem picos locais. **Ainda é uma penalidade suave (soft constraint), não uma
   restrição rígida.** Checado: resumo Cambridge Core + autoria confirmada via Crossref
   (`Kruger, Thomas G.`).

3. **M. Landreman**, "An improved current potential method for fast computation of stellarator coil
   shapes", *Nuclear Fusion* 57, 046003 (2017). DOI: `10.1088/1741-4326/aa57d4` (arXiv:1609.04378).
   Artigo original do **REGCOIL**: regularização de Tikhonov (penalidade em L² da densidade de
   corrente) sobre uma superfície de enrolamento fixa; não impõe curvatura da bobina diretamente
   (a bobina discreta é extraída depois do potencial de corrente contínuo). Checado: resumo
   arXiv/IOP.

4. **SIMSOPT** (framework, não um único artigo): oferece `MeanSquaredCurvature` (penalidade L²) e
   `LpCurveCurvature`, que penaliza o excesso de curvatura acima de um limiar em norma Lᵖ — para p
   grande aproxima uma restrição L∞, mas continua sendo penalidade, não restrição rígida. Checado:
   documentação oficial (`simsopt.readthedocs.io`), não é um artigo com DOI.

5. **L. Fu, E. J. Paul, A. A. Kaptanoglu, A. Bhattacharjee**, "Global stellarator coil optimization
   with quadratic constraints and objectives" (QUADCOIL), arXiv:2408.08267 (2024). Formula
   curvatura como restrição **quadrática, podendo ser imposta de forma rígida** (não apenas como
   penalidade) dentro de um problema convexificado; é o código mais próximo, entre os revisados, de
   impor curvatura como restrição dura — mas a restrição é quadrática (≈L²), não minimax/L∞.
   Checado: resumo arXiv.

6. **P. Huslage, E. J. Paul, M. Haque, P. F. Gil, N. Foppiani, J. Smoniewski, E. V. Stenson**,
   "Strain optimisation for ReBCO high-temperature superconducting stellarator coils in SIMSOPT",
   *Journal of Plasma Physics* 91, [issue 2] (2025). DOI: `10.1017/S0022377825000224`
   (arXiv:2409.01925). Implementa penalidade sobre **curvatura binormal** (hard-way) e **torção**
   ao longo da bobina, dentro do SIMSOPT, para manter a deformação da fita REBCO dentro de limites
   toleráveis em três desenhos de estelarator. Confirma explicitamente que o tratamento é por
   penalidade (soft), não por restrição rígida. Checado: resumo arXiv (autoria completa lida ali).

7. **C. Paz-Soldan**, "Non-planar coil winding angle optimization for compatibility with
   non-insulated high-temperature superconducting magnets", *Journal of Plasma Physics* 86,
   815860501 (2020). DOI: `10.1017/S0022377820001208` (arXiv:2003.02154). Otimiza o ângulo de
   enrolamento (orientação da fita em torno do eixo tangente) para minimizar a deformação hard-way e
   a torção, usando splines tensionadas — é um tratamento geométrico do problema de minimizar picos
   de deformação, mas não formaliza isso como um problema minimax com garantia de existência.
   Checado: resumo arXiv.

## 2. Bobinas de estelarator em HTS/REBCO (não-planares)

8. **N. Riva, R. S. Granetz, R. Vieira, A. Hubbard, A. T. Pfeiffer, P. Harris, C. Chamberlain,
   Z. S. Hartwig, A. Watterson, D. Anderson, R. Volberg**, "Development of the first non-planar
   REBCO stellarator coil using VIPER cable", *Superconductor Science and Technology* 36, 105001
   (2023). DOI: `10.1088/1361-6668/aced9d`. Dois protótipos (NOVEL e MINOAN) dobrados a raio de
   curvatura ≈100 mm; degradação de Ic < 15%, dentro da meta de projeto de 20%. Checado: resumo
   IOPscience + DOI via Crossref.

9. **P. Huslage, D. Kulla, J.-F. Lobsien, T. Schuler, E. V. Stenson**, "Winding angle optimization
   and testing of small-scale, non-planar, high-temperature superconducting stellarator coils",
   *Superconductor Science and Technology* 37, 085004 (2024). DOI: `10.1088/1361-6668/ad5382`.
   Modifica o referencial de Frenet para reduzir torção mantendo curvatura binormal aceitável;
   constrói duas bobinas W7-X em escala reduzida (11% e 25%) com fita GdBCO, obtendo raios de
   curvatura ≈2 cm. Checado: resumo IOPscience + autoria e DOI via Crossref.

## 3. Modelos de fita desenvolvível (Sadowsky/Wunderlich, desenvolvíveis retificantes)

10. **M. A. Dias, B. Audoly**, "'Wunderlich, meet Kirchhoff': A general and unified description of
    elastic ribbons and thin rods", *Journal of Elasticity* 119, 49–66 (2015).
    DOI: `10.1007/s10659-014-9487-0` (arXiv:1403.2094, 2014). Unifica o modelo de Sadowsky (fita
    estreita) e o de Wunderlich (fita de largura finita) dentro da teoria de Kirchhoff para hastes,
    usando a direção das geratrizes como variável interna; a fita desenvolvível é construída sobre a
    **desenvolvível retificante** da linha central (plano gerado por tangente e binormal). Checado:
    resumo arXiv + DOI via Crossref.

11. **E. L. Starostin, G. H. M. van der Heijden**, "Forceless Sadowsky strips are spherical",
    *Physical Review E* 97, 023001 (2018). DOI: `10.1103/PhysRevE.97.023001` (arXiv:1802.02472).
    Mostra que minimizadores livres de força do funcional de Sadowsky tendem a formas esféricas;
    relevante como exemplo de que minimizar a energia de uma fita desenvolvível estreita não produz
    automaticamente a forma "menos curva" — a geometria de equilíbrio pode ser não-trivial. Checado:
    resumo arXiv.

Observação de contexto (não uma referência própria, apenas o vínculo notado nesta revisão): a
condição "a fita não pode dobrar hard-way" equivale a exigir curvatura geodésica ≈0 na tira
desenvolvida — ou seja, a curva central deve admitir uma tira de desenvolvível retificante como
modelo geométrico do próprio limite de engenharia. Não encontrei, na busca desta revisão, nenhum
artigo de projeto de bobina de estelarator (itens 1–9) que cite explicitamente Sadowsky, Wunderlich
ou "developable ribbon/strip" — a ligação é feita aqui, não na literatura consultada.

## 4. Minimax/L∞ de curvatura ou teoria de Dubins/Markov (curvatura limitada) em projeto de bobinas

Busquei especificamente por ("Dubins path" + "coil design"/"magnet"), por ("minimax"/"L-infinity
curvature" + "stellarator coil optimization") e por combinações com "bounded curvature path
planning". Resultado: a literatura de Dubins/Markov (curvatura limitada, caminhos ótimos com
raio de curvatura mínimo) é ativa em robótica/planejamento de trajetórias (ver p.ex. Váňa & Faigl,
"Minimal 3D Dubins Path with Bounded Curvature and Pitch Angle", ICRA 2020), mas **nenhum resultado
de busca conectou essa teoria a projeto de bobinas magnéticas ou de fitas HTS**. Do lado dos
códigos de bobina, o mais próximo de uma restrição "dura" é QUADCOIL (item 5), que é quadrática, não
minimax pontual sobre a curva. Não encontrei nenhum artigo que formule o problema de bobina como
minimização em norma L∞ da segunda forma fundamental com prova de existência/regularidade do
minimizador. **Isto não confirma a inexistência do resultado** (a busca não é exaustiva e a
literatura de engenharia mecânica de bobinas HTS é dispersa em atas de conferência não indexadas),
mas dentro do que foi levantado aqui, é uma lacuna real.

## O que é conhecido
- Todos os códigos amplamente citados (FOCUS, REGCOIL, SIMSOPT, QUADCOIL) tratam curvatura e/ou
  torção como termos de penalidade (L² ou Lᵖ) somados ao erro de campo, exceto QUADCOIL, que permite
  impor curvatura como restrição quadrática dura dentro de um programa convexo.
- Kruger et al. (2021) já mostram empiricamente que otimizar a curvatura **máxima** (não a média)
  dá bobinas melhores para fins de engenharia — evidência indireta a favor de uma formulação L∞,
  mas ainda dentro do arcabouço de penalidade suave, não de restrição dura com teoria de existência.
- Para fitas REBCO reais, os grupos que already tentam bobinas não-planares (MIT/VIPER, IPP/Huslage
  et al.) tratam a torção e a curvatura hard-way via otimização numérica do ângulo de enrolamento,
  não via um modelo de fita desenvolvível explícito.
- A teoria de fitas de Sadowsky/Wunderlich está madura na mecânica de elásticas (Dias–Audoly 2014,
  Starostin–van der Heijden 2018), mas desenvolvida para problemas de equilíbrio mecânico de fitas
  livres, não para o problema inverso de projetar uma linha central sob restrição de curvatura para
  um objetivo de campo magnético.

## O que parece aberto
- Uma formulação do problema de bobina como minimização em **L∞ (minimax)** da curvatura normal e
  da torção, com prova de existência de minimizador e alguma estrutura de regularidade (C^{1,1},
  arcos "bang-bang", equioscilação à la Chebyshev) não aparece na literatura levantada.
- A ligação explícita entre "fita não pode dobrar hard-way" ⇔ "a curva central admite uma tira de
  desenvolvível retificante de curvatura geodésica nula" como **restrição de projeto** (em vez de
  apenas o modelo de equilíbrio mecânico da fita já dobrada) não aparece nos artigos de projeto de
  bobina revisados.
- Teoria de curvatura limitada tipo Dubins/Markov (arcos de curvatura constante máxima) aplicada ao
  desenho de bobinas magnéticas não foi encontrada.

## Sugestão de primeiro cálculo
Seguir o passo 3 do PLANO.md: problema-modelo planar/toroidal comparando (i) penalidade L² clássica,
(ii) `LpCurveCurvature` com p grande (aproximação numérica de L∞, já disponível no SIMSOPT) e
(iii) uma restrição rígida de L∞ implementada via otimização com restrições de desigualdade pontuais
(ou via reparametrização por curvatura/torção como em Zhu et al. 2018, item 1). Medir o pico de
curvatura e o erro de campo nos três casos, com oráculo independente (verificação geométrica direta
da curva, não a mesma rotina de otimização) e controle negativo (violar deliberadamente o limite em
um segmento curto e confirmar que o diagnóstico de pico o detecta). Só depois disso rotular alguma
diferença como "vantagem do L∞" — a literatura (item 2, Kruger et al.) já sugere que o ganho
qualitativo existe, mas o tamanho do ganho quantitativo, e se ele justifica a maquinaria de
existência/regularidade, ainda não está medido aqui.
