# Literatura: coerência supercondutora em redes fractais e a dimensão espectral

Revisão feita em 2026-09-28. Metodologia: WebSearch + WebFetch de resumo/texto; DOI resolvido via
Crossref (`api.crossref.org/works/<DOI>`) quando existe; arXiv ID quando não há DOI de periódico.
"Checado" indica que o resumo (ou, quando indicado, texto completo) foi lido nesta revisão e a
autoria conferida contra essa fonte.

## 1. Mermin–Wagner generalizado em grafos (Cassi; Burioni–Cassi–Vezzani)

1. **D. Cassi**, "Phase transitions and random walks on graphs: A generalization of the
   Mermin–Wagner theorem to disordered lattices, fractals, and other discrete structures",
   *Physical Review Letters* 68, 3631 (1992). DOI: `10.1103/PhysRevLett.68.3631`. Resultado
   central: para modelos clássicos O(n) (e Heisenberg quântico de spin-s ferromagnético) em um
   grafo genérico, **não há magnetização espontânea a T>0 se a caminhada aleatória simples no
   mesmo grafo é recorrente**. Corolário para fractais: simetria contínua só pode quebrar
   espontaneamente se a dimensão espectral d_s > 2. Autoria única (D. Cassi). Checado: DOI via
   Crossref, autor confirmado; resumo lido via busca.

2. **R. Burioni, D. Cassi, A. Vezzani**, "Inverse Mermin–Wagner theorem for classical spin models
   on graphs", *Physical Review E* 60, 1500 (1999). DOI: `10.1103/PhysRevE.60.1500`. Prova a
   **recíproca**: em grafos "transientes na média" (TOA, transient on average), há magnetização
   espontânea a T finita para modelos O(n) — incluindo Ising (n=1). Junto com o item 1, isso dá
   uma dicotomia completa TOA/ROA (recurrent on average) que classifica qualquer grafo/rede quanto
   à possibilidade de quebra espontânea de simetria contínua. Checado: DOI via Crossref, autoria
   (Burioni, Cassi, Vezzani) confirmada.

3. **D. Cassi**, "Local vs average behavior on inhomogeneous structures: recurrence on the average
   and a further extension of the Mermin–Wagner theorem on graphs", *Physical Review Letters* 76,
   2941 (1996). DOI: `10.1103/PhysRevLett.76.2941`. Introduz formalmente a noção de "recorrência
   na média" (definição usada nos itens 1–2), distinguindo-a da recorrência local usual — necessária
   porque grafos com defeitos locais podem ter comportamento local ≠ comportamento médio. Checado:
   DOI via Crossref, autoria confirmada.

**Hipóteses exigidas pelo teorema (conferir antes de aplicar ao modelo XY/arranjos Josephson):**
o resultado de Cassi (1992) é enunciado para grafos com **grau limitado** (coordenação uniformemente
limitada) e simetria contínua O(n) com interação de primeiros vizinhos tipo spin clássico; a
condição decisiva é a recorrência (ou transiência) **na média** da caminhada aleatória simples no
grafo, não apenas a dimensão de Hausdorff. Como o modelo XY tem simetria O(2), ele está diretamente
coberto pelo enunciado — logo, em princípio aplica-se a arranjos Josephson tratados como o modelo XY
clássico (fase da função de onda supercondutora em cada ilha, acoplamento cosseno entre ilhas
vizinhas), desde que a rede subjacente tenha grau limitado, o que vale para as construções usuais de
gaxeta/tapete de Sierpinski. Não encontrei, nesta revisão, um artigo que aplique o teorema de Cassi
**explicitamente** a arranjos Josephson (a ligação XY-clássico ↔ arranjo Josephson é padrão na área,
mas a citação cruzada específica não apareceu nas buscas).

## 2. Experimentos em redes/arranjos Josephson fractais e teoria de dimensão espectral

4. **J. M. Gordon, A. M. Goldman, J. Maps, D. Costello, R. Tiberio, B. Whitehead**,
   "Superconducting-normal phase boundary of a fractal network in a magnetic field", *Physical
   Review Letters* 56, 2280 (1986). DOI: `10.1103/PhysRevLett.56.2280`. Primeira medida da
   fronteira de fase T_c(H) em uma rede de fios de Al na forma de gaxeta de Sierpinski
   (microfabricada); observa invariância dilatacional na curva T_c(H) e extrai a dimensão fracton
   (=espectral) experimentalmente, ≈1,35±0,02, consistente com o valor teórico 1,365 da gaxeta
   plana. Checado: DOI via Crossref, autoria completa confirmada.

5. **J. M. Gordon, A. M. Goldman, B. Whitehead**, "Dimensionality crossover in superconducting
   wire networks", *Physical Review Letters* 59, 2311 (1987). DOI: `10.1103/PhysRevLett.59.2311`.
   Redes com arranjos periódicos de gaxetas de Sierpinski (não uma única gaxeta infinita): mostram
   crossover entre comportamento fractal (escalas curtas) e comportamento 2D homogêneo (escalas
   longas/campos baixos), análogo ao crossover fônon–fracton. Checado: DOI via Crossref, autoria
   confirmada.

   **Nota sobre atribuição:** o PLANO.md desta pasta cita "Gordon, Goldman, Whan e outros". Não
   encontrei nenhum artigo de Whan sobre arranjos Josephson/redes supercondutoras em gaxetas de
   Sierpinski — o coautor real dos experimentos de Gordon–Goldman é **B. Whitehead**, não Whan.
   Existe um C. B. Whan que publicou sobre dinâmica de vórtices e caos em junções Josephson
   individuais (com C. J. Lobb, início dos anos 1990), mas não sobre redes fractais. **Trato
   "Whan" como um provável erro/confusão de nome no PLANO.md** — recomendo corrigir para
   "Whitehead" ou remover a atribuição até confirmar de outra forma.

6. **H. J. Lee, M. G. Forrester, M. Tinkham, C. J. Lobb**, sobre a transição resistiva de arranjos
   de junções Josephson fracas em gaxeta de Sierpinski de 6ª ordem: a dependência R(T) não se
   ajusta às teorias existentes de flutuação para d=1, d=2 nem d=1,585 (a dimensão fractal de
   Hausdorff da gaxeta); o expoente da lei de potência na característica I–V varia suavemente com
   T. Localizado via busca; **não consegui confirmar título exato, periódico e DOI nesta sessão** —
   marco como referência a confirmar antes de citar formalmente.

7. **B. Mitrovic, S. K. Bose**, "Monte Carlo study of the XY-model on Sierpinski gasket",
   *Phase Transitions* 83, 572–580 (2010). DOI: `10.1080/01411594.2010.500804` (arXiv:1006.2138).
   Simulação de Monte Carlo do modelo XY clássico na gaxeta de Sierpinski 2D: **não há transição
   de fase a temperatura finita**, consistente com a previsão teórica (gaxeta tem d_s≈1,365<2).
   Este é o resultado numérico mais direto encontrado para o caso d_s<2 do problema do item B, e
   serve de controle/oráculo natural para a proposta de numérica do PLANO.md. Checado: DOI via
   Crossref, autoria e conclusão confirmadas via resumo.

8. **R. Rammal, G. Toulouse**, "Random walks on fractal structures and percolation clusters",
   *Journal de Physique Lettres* 44, L13–L22 (1983). DOI: `10.1051/jphyslet:0198300440101300`.
   Introduz a dimensão espectral (espectral/fracton) de uma estrutura autossimilar via
   escalonamento da probabilidade de retorno de uma caminhada aleatória; deriva seu valor para a
   família das gaxetas de Sierpinski. Checado: DOI via Crossref.

9. **S. Alexander, R. Orbach**, "Density of states on fractals: 'fractons'", *Journal de Physique
   Lettres* 43, L625–L631 (1982). DOI: `10.1051/jphyslet:019820043017062500`. Introduz a
   distinção entre dimensão euclidiana (de imersão), dimensão de Hausdorff (fractal) e dimensão
   fracton (espectral); densidade de estados de baixa frequência D(ω)~ω^(d_s−1). Base da
   relação de Alexander–Orbach (d_s = 2·d_f/d_w, ligando dimensão espectral, dimensão fractal e
   expoente de difusão anômala) amplamente usada na interpretação dos experimentos dos itens 4–5.
   Checado: DOI via Crossref.

## 3. Dimensão espectral: gaxeta, tapete de Sierpinski, esponja de Menger

- **Gaxeta de Sierpinski (2D):** d_s = 2 ln3/ln5 ≈ 1,365 (forma fechada, via decimação espectral;
  Rammal–Toulouse 1983, item 8). d_s < 2 ⇒ sem quebra de simetria contínua a T>0 pelo teorema de
  Cassi — consistente com a ausência de transição no item 7.
- **Tapete de Sierpinski (Sierpinski carpet):** não tem forma fechada conhecida para d_s; valores
  numéricos citados na literatura secundária ficam em torno de d_s ≈ 1,8–1,86 (dimensão de
  Hausdorff do tapete é ln8/ln3 ≈ 1,893, um limite superior natural para d_s). **Não confirmei
  esses números numéricos (1,8 / 1,86) contra um artigo específico nesta sessão** — vieram de
  resultados de busca agregados; tratar como indicativo. Ainda assim, o consenso qualitativo (d_s
  do tapete plano < 2) é consistente com o resultado independente do item 10 abaixo (condensação de
  Bose só ocorre para variantes do tapete com d_s>2).
- **Esponja de Menger (generalização 3D):** dimensão espectral **depende da família específica**
  (nível de "ramificação"/parâmetros da construção MS(n,k)). Um resultado de busca (não confirmado
  contra artigo específico nesta sessão) reporta intervalos como 2,21<d_s<2,60 para MS(3,1),
  2,00<d_s<2,26 para MS(4,2), decrescendo para versões mais "esparsas" da esponja — ou seja,
  **existem construções de esponja de Menger com d_s>2 e outras com d_s<2**, dependendo dos
  parâmetros. Isto é relevante diretamente para a pergunta do PLANO.md sobre "quais famílias com
  d_s>2 são realizáveis": esponjas de Menger (ou variantes 3D de tapetes) são candidatos naturais,
  mas o valor exato de d_s precisa ser recalculado (ou a fonte, reconfirmada) antes de qualquer
  afirmação numérica no texto final.

10. **J. P. Chen**, "Statistical mechanics of a Bose gas in Sierpinski carpets" (submetido a
    *Communications in Mathematical Physics* no momento do preprint), arXiv:1202.1274 (2012).
    Prova rigorosa (via funções zeta espectrais e núcleo do calor) de que **condensação de
    Bose–Einstein ocorre se e somente se d_s>2**, para bósons livres em tapetes de Sierpinski
    generalizados (família ajustável para atingir d_s>2, ao contrário do tapete usual). Este é o
    análogo bosônico mais próximo, na literatura encontrada, de um "critério de d_s" quantitativo —
    mas é para gás de Bose livre, não para o modelo XY/Josephson interagente do problema B. Checado:
    resumo arXiv, autoria e resultado central confirmados.

## 4. Bandas planas, peso superfluido/métrica quântica, e fractais

11. **S. Peotta, P. Törmä**, "Superfluidity in topologically nontrivial flat bands",
    *Nature Communications* 6, 8944 (2015). DOI: `10.1038/ncomms9944`. Mostra que o peso
    superfluido de uma banda plana isolada é não-nulo apenas em sistemas multibanda e é
    proporcional à **métrica quântica** integrada sobre a banda — é o resultado fundador da linha
    "geometria quântica ⇒ supercondutividade de banda plana". Checado: DOI via Crossref, autoria
    confirmada.

12. **S. N. Kempkes, M. R. Slot, S. E. Freeney, S. J. M. Zevenhuizen, D. Vanmaekelbergh, I. Swart,
    C. Morais Smith**, "Design and characterization of electrons in a fractal geometry",
    *Nature Physics* 15, 127–131 (2019). DOI: `10.1038/s41567-018-0328-0`. Realização eletrônica
    (STM, moléculas de CO sobre Cu(111)) de fractais de Sierpiński artificiais; funções de onda
    eletrônicas medidas herdam dimensão não-inteira. Não trata de supercondutividade, mas é a
    referência-chave para "realização eletrônica de rede fractal" pedida no PLANO.md. Checado: DOI
    via Crossref, autoria confirmada.

13. **A. A. Iliasov, R. Canyellas, M. I. Katsnelson, A. A. Bagrov**, "Strong enhancement of
    superconductivity on finitely ramified fractal lattices", arXiv:2310.11497 (2023, v3 2024).
    Modelo de Hubbard atrativo em campo médio (BCS) em gaxeta de Sierpinski vs. tapete de
    Sierpinski: **forte aumento de T_c na gaxeta** (comparada à rede triangular regular),
    atribuído à ramificação finita da gaxeta, mas **aumento desprezível no tapete** (comparado à
    rede quadrada). É o resultado mais próximo, na literatura encontrada, de uma "previsão de T_c
    em rede fractal" — mas é numérico/campo médio para uma família específica de fractais em cada
    geração, não uma lei de escala fechada em função contínua de d_s. Checado: resumo arXiv,
    autoria confirmada. Sem DOI de periódico até o momento desta revisão.

14. Realizações de bandas planas em redes tipo fractal fora do caso eletrônico "puro": redes
    fotônicas do tipo Sierpinski/kagome decorado mostram bandas planas duplamente degeneradas com
    estados localizados compactos (ver p.ex. Hanafi et al., *Adv. Optical Materials* 2022,
    "Localized states emerging from singular and nonsingular flat bands in a frustrated
    fractal-like photonic lattice", arXiv:2111.03507 — resumo checado, DOI de periódico não
    verificado nesta sessão); circuitos topolétricos também já realizam redes com múltiplas
    bandas planas simultâneas (arXiv:2508.13571, "Realization and characterization of an
    all-bands-flat electrical lattice" — resumo checado via título/arXiv, texto completo não lido).
    Nenhuma dessas realizações (fotônica, circuito) trata de supercondutividade — são plataformas
    de banda plana clássicas/de partícula única, não sistemas com pareamento.

## O que é conhecido
- A dicotomia de Cassi/Burioni–Cassi–Vezzani (itens 1–3) é um teorema rigoroso, com hipóteses
  claras (grau limitado, simetria O(n), recorrência **na média**), e dá exatamente o critério
  qualitativo d_s>2 usado no PLANO.md para fractais regulares.
- Experimentalmente (itens 4–7), gaxetas de Sierpinski (d_s<2) não sustentam ordem de longo
  alcance/T_c homogêneo — tanto em redes de fios metálicos (anos 1980) quanto numericamente no
  modelo XY clássico (Mitrovic–Bose 2010).
- O análogo bosônico rigoroso (Chen 2012, item 10) confirma "condensação sse d_s>2" para uma
  família ajustável de tapetes de Sierpinski generalizados — evidência forte de que o critério de
  Cassi tem um paralelo quantitativo do lado bosônico.
- Bandas planas com geometria quântica não-trivial (Peotta–Törmä 2015) e redes fractais com bandas
  planas (item 14, mais o caso eletrônico do item 12) existem como linhas de pesquisa separadas;
  Iliasov et al. (2023/24, item 13) já unem fractal + supercondutividade em campo médio e encontram
  reforço de T_c em gaxetas.

## O que parece aberto
- Uma **lei de escala fechada** para a rigidez de fase (ou T_c) em função de d_s, especificamente
  no regime d_s → 2⁺ (o PLANO.md pergunta isso explicitamente), não aparece em nenhum dos itens
  acima. O teorema de Cassi é uma dicotomia (existe ordem / não existe), não uma lei de expoente
  perto do limiar.
- Uma previsão de T_c para redes fractais **combinando explicitamente** o mecanismo de banda plana
  de Peotta–Törmä (peso superfluido ∝ métrica quântica) com a dimensão espectral fractal não foi
  encontrada — as realizações de banda plana em fractais (item 14) são plataformas sem pareamento, e
  o trabalho de campo médio (item 13) não usa a linguagem de métrica quântica/geometria de banda.
- Não encontrei um artigo que aplique o teorema de Cassi **nominalmente** a arranjos Josephson (a
  ponte XY↔Josephson é padrão, mas a citação cruzada explícita não apareceu).

## Sugestão de primeiro cálculo
Seguir o passo 2 do PLANO.md: modelo XY clássico (spin-wave harmônico ou Monte Carlo completo) na
gaxeta de Sierpinski (oráculo: decimação espectral, valor fechado d_s=2ln3/ln5, e o resultado
independente de Mitrovic–Bose 2010 — ausência de transição — como verificação cruzada) e no tapete
de Sierpinski (onde d_s não tem forma fechada — calcular numericamente via decimação/contagem de
autovalores do laplaciano de Kigami do livro, cap. 6). Controle negativo: rede quadrada (d_s=2 exato,
transição BKT conhecida) tratada pelo mesmo código, para garantir que o código reproduz o caso de
controle antes de confiar no caso fractal. Só depois disso vale tentar variar a família de fractal
(parâmetros da esponja de Menger ou de tapetes generalizados) para obter pontos com d_s
continuamente acima de 2 e testar se a rigidez/T_c extrapolada aproxima alguma lei simples perto do
limiar — isso é exatamente o que a literatura revisada aqui não fornece ainda.
