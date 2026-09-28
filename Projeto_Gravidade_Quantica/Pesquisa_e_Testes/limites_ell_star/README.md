# Limites experimentais sobre a escala livre ℓ* = 1/M* (modelo-brinquedo)

Este diretório reúne, converte e traça em um gráfico de exclusão os limites
experimentais atuais mais relevantes para a escala livre `ℓ* = 1/M*` de um
modelo-brinquedo de gravidade quântica com dois ramos:

- **Ramo I (isotrópico)**: propagador `1/(k² + ℓ*² k⁴)`, dispersão
  `ω² = k²(1 + ℓ*² k²)`, e potencial estático de Yukawa
  `V(r) = −(GMm/r)(1 − e^{−r/ℓ*})` — equivalente a um ghost de spin-2 tipo
  Stelle de massa `1/ℓ*`, com força de Yukawa `α = −1` e alcance `λ = ℓ*`.
- **Ramo II (anisotrópico, Hořava–Lifshitz z=3)**: dispersão
  `ω² = k² + k⁶/M*⁴`, sem desvio estático de Newton em ordem dominante.
- **Ramo III (hipótese opcional de universalidade fotônica)**: se o mesmo
  operador agir sobre fótons, há violação de Lorentz quadrática (n=2,
  atraso `∝ (E/M*)²`) associada ao ramo I e quártica (n=4, atraso
  `∝ (E/M*)⁴`) associada ao ramo II.

Todos os números abaixo foram extraídos dos artigos originais (texto
completo, não apenas resumo) e cada DOI foi verificado programaticamente via
a API do Crossref (`https://api.crossref.org/works/<doi>`); dois DOIs
inicialmente supostos por memória estavam **errados** e foram corrigidos
após a verificação (ver seção "Notas de verificação" abaixo).

## Convenção de unidades

Usa-se `ħ = c = 1` nas fórmulas de física de partículas, de modo que
`ℓ* = 1/M*` diretamente. A conversão explícita para unidades SI usa

```
ħc = 197.3269804 MeV·fm = 1.97327×10⁻⁷ eV·m
```

(consistente com o valor `197.327 MeV·fm` citado na tarefa; usamos o valor
de precisão total do PDG). As fórmulas de conversão são:

```
ℓ*[m] = ħc[eV·m] / M*[eV]         M*[eV] = ħc[eV·m] / ℓ*[m]
```

Para o termo de dispersão `A_4` da parametrização de Mirshekari–Yunes–Will
(`E² = p²c² + A_α p^α c^α`, com `c=1` na tabela da LVK), a correspondência
com o ramo I é `A_4 = ℓ*²` (unidades `eV⁻²`), pois `ω² = k² + ℓ*² k⁴`.

## Tabela de limites

| Experimento | Ramo | Limite original | Limite em ℓ* | Limite em M* | Fonte (DOI, tabela/página) |
|---|---|---|---|---|---|
| Eöt-Wash (Lee et al. 2020) | I (Yukawa) | λ < 38.6 μm (95% CL, \|α\|=1) | ℓ* < 3.86×10⁻⁵ m | M* > 5.11×10⁻³ eV = 5.11×10⁻¹² GeV | DOI 10.1103/PhysRevLett.124.101101, PRL 124, 101101 (2020); número no *abstract*, curva α(λ) na Fig. 3 |
| HUST (Tan et al. 2020) | I (Yukawa) | λ = 48 μm (95% CL, \|α\|≤1) | ℓ* < 4.80×10⁻⁵ m | M* > 4.11×10⁻³ eV = 4.11×10⁻¹² GeV | DOI 10.1103/PhysRevLett.124.051301, PRL 124, 051301 (2020); *abstract*, curva na Fig. 4. Não localizamos preprint arXiv indexado. |
| LIGO-Virgo-KAGRA GWTC-3 (dispersão modificada, A₄) | I (dispersão do gráviton) | \|A₄\| < 0.30×10⁴ eV⁻² (90% credível, A>0, 43 eventos) | ℓ* < 1.08×10⁻⁵ m | M* > 1.83×10⁻² eV = 1.83×10⁻¹¹ GeV | DOI 10.1103/PhysRevD.112.084080, "Tests of general relativity with GWTC-3", Tabela VII, p. 24 do PDF do arXiv:2112.06861 |
| GW170817 (velocidade das ondas gravitacionais) | I (cross-check fraco) | \|v_GW/c − 1\| < 3×10⁻¹⁵ (f~100 Hz) | ℓ* < 2.6×10⁻² m | M* > 7.6×10⁻⁶ eV = 7.6×10⁻¹⁵ GeV | DOI 10.3847/2041-8213/aa920c, ApJL 848, L13 (2017), Seção "Constraints" |
| GW170817 (velocidade, proxy fraco) | II (proxy) | idem acima, reinterpretado para `ω²=k²+k⁶/M*⁴` | ℓ* < 94 m | M* > 2.1×10⁻⁹ eV | mesma fonte; **não competitivo**, apenas ordem de grandeza |
| LHAASO GRB 221009A, LIV quadrática (n=2) | I via universalidade | E_QG,2 > 6.9×10¹¹ GeV (95% CL, sub-luminal) | ℓ* < 2.86×10⁻²⁸ m | M* > 6.9×10²⁰ eV = 6.9×10¹¹ GeV | DOI 10.1103/PhysRevLett.133.071501, PRL 133, 071501 (2024), Tabela I, p. 6 do PDF do arXiv:2402.06009 |
| Fermi-LAT GRBs (Vasileiou et al. 2013), LIV quadrática (n=2) | I via universalidade, cross-check | E_QG,2 > 1.3×10¹¹ GeV (95% CL, sub-luminal, GRB 090510) | ℓ* < 1.52×10⁻²⁷ m | M* > 1.3×10¹¹ GeV | DOI 10.1103/PhysRevD.87.122001, PRD 87, 122001 (2013) |
| Crab Nebula (Satunin et al. 2019), LIV quártica (n=4) | II via universalidade, **mecanismo diferente** | E_QG,4-like > 1.4×10¹² GeV (canal sub-luminal) | ℓ* < 1.41×10⁻²⁸ m | M* > 1.4×10¹² GeV | DOI 10.1140/epjc/s10052-019-7520-y, EPJC 79, 1011 (2019) |
| GRB 090510 (Abdo et al. 2009), LIV linear (n=1), referência | — (não usado para ℓ*) | M_QG,1 > 1.22 M_Planck | — | — | DOI 10.1038/nature08574, Nature 462, 331 (2009); citado apenas como referência histórica do método, não convertido (ordem n=1 não corresponde a nenhum dos dois ramos do modelo) |

**Limite não encontrado**: não localizamos, na Tabela VII de GWTC-3 (LVK) ou
em qualquer outro catálogo LVK publicado, um valor tabulado de `A_6`
(a ordem de dispersão correspondente ao ramo II, `ω²=k²+k⁶/M*⁴`); a tabela
para de citar `α=4`. Da mesma forma, não encontramos um limite de tempo de
voo de GRBs dedicado a `n=4` com significância estatística robusta e
mesma metodologia dos limites n=1/n=2 (o único número quártico citado na
literatura recente, de um "fóton de 300 TeV" de GRB 221009A,
arXiv:2508.07153, é apresentado pelos próprios autores como um *indício*
não conclusivo, não uma exclusão — por isso não o registramos na tabela
acima como limite de exclusão).

## Qual ramo é mais restringido, e o tamanho da janela remanescente

**O ramo I é, de longe, o mais restringido**, e por uma grande margem, tanto
em laboratório quanto — se a universalidade fotônica for assumida — por
astrofísica de altas energias:

- Sem qualquer hipótese extra, o limite direto mais forte do ramo I vem da
  dispersão do gráviton em GWTC-3: `ℓ* < 1.08×10⁻⁵ m` (equivalente a
  `M* > 18 meV`), ligeiramente mais forte que os limites de Yukawa em
  laboratório (`ℓ* < 3.86×10⁻⁵`–`4.8×10⁻⁵ m`, Eöt-Wash e HUST).
- **Se** a hipótese de universalidade fotônica for aceita, o limite salta
  para `ℓ* < 2.9×10⁻²⁸ m` (LHAASO GRB 221009A), **~23 ordens de grandeza**
  mais forte que o limite de laboratório, porque uma escala próxima de
  `M*` afeta fótons de altíssima energia (TeV) de forma muito mais
  detectável ao longo de bilhões de anos-luz de propagação.
- O **ramo II não tem nenhum desvio estático de Newton** (por construção) e
  não há bound tabulado de LVK para `α=6`; o único limite direto disponível
  é o cross-check de velocidade de GW170817, extremamente fraco
  (`ℓ* < 94 m`, essencialmente sem poder de exclusão física). Somente com a
  hipótese de universalidade (via o limite quártico, de mecanismo distinto,
  de Crab Nebula) chega-se a um número competitivo, `ℓ* < 1.4×10⁻²⁸ m` —
  mas esse número **não usa exatamente o observável do enunciado** (ver
  ressalvas).

**Janela remanescente entre o limite de laboratório e ℓ_P:**

- Sem universalidade (ramo I, limite mais forte, GWTC-3): a janela permitida
  é `1.6×10⁻³⁵ m ≲ ℓ* ≲ 1.1×10⁻⁵ m`, ou seja, **~30 ordens de grandeza** em
  escala logarítmica ainda não excluídas entre o laboratório e o comprimento
  de Planck.
- Com universalidade fotônica (ramo I, LHAASO): a janela remanescente cai
  para `1.6×10⁻³⁵ m ≲ ℓ* ≲ 2.9×10⁻²⁸ m`, cerca de **~7 ordens de grandeza**
  — muito mais próxima da escala de Planck, mas ainda uma janela aberta não
  trivial.
- Para o ramo II sem universalidade, a janela é essencialmente todo o eixo
  do gráfico (praticamente nenhuma restrição não trivial).

## Ressalvas (caveats)

1. **Força exata do Yukawa `α = −1` vs. divisão de Stelle `4/3` e `1/3`.**
   O modelo do enunciado assume um único grau de liberdade de spin-2 massivo
   com `α = −1` exatamente. Uma teoria completa de gravidade massiva tipo
   Stelle (spin-2 + spin-0) tem, em geral, `α = −4/3` (contribuição de
   spin-2) `+ 1/3` (contribuição de spin-0, com sinal oposto e alcance
   potencialmente diferente), o que altera a normalização do bound de
   Yukawa (Lee/Tan et al. reportam o limite assumindo `α=1` gravitacional
   puro; se o modelo real tiver `|α|=4/3` isolado ou uma combinação com
   cancelamento parcial, o limite efetivo em `ℓ*` muda por um fator
   `O(1)`, não recalculado aqui).
2. **Universalidade fotônica não é garantida.** Os bounds LHAASO/Fermi/Crab
   usados como proxy para os ramos I/II só se aplicam a `ℓ*` **se** o
   mesmo operador de dispersão não-mínimo que afeta o gráviton também
   afeta o setor eletromagnético com o mesmo coeficiente — hipótese
   fortemente dependente de UV completion e não implicada automaticamente
   por gravidade massiva ou por Hořava–Lifshitz puro (poderia haver
   coeficientes de operador distintos para cada setor, ou até ausência
   total de LIV fotônica). Tratamos esses números como um **teto
   condicional**, não como limite incondicional do modelo.
3. **Problema do ghost no ramo I.** O termo extra `1/(k²+ℓ*²k⁴)` no
   propagador equivale, via frações parciais, a `1/k² − 1/(k²+ℓ*⁻²)`, ou
   seja, a um segundo polo com **resíduo de sinal oposto** — um ghost
   massivo de Stelle, com massa `1/ℓ*`. Isso é uma instabilidade
   perturbativa conhecida (ghost de Ostrogradski/Stelle) e levanta a
   questão de unitariedade/estabilidade do vácuo em qualquer escala de
   energia acima de `M*`; os limites experimentais aqui reportados
   restringem apenas a fenomenologia de baixa energia (desvio de Newton e
   dispersão), não resolvem nem invocam nenhum mecanismo de supressão do
   ghost (self-interações, ressoma não-perturbativa, etc.).
4. **Mecanismo do limite quártico (Crab Nebula) é diferente do assumido.**
   O único número quártico (n=4) que localizamos na literatura vem de
   limiares de produção de pares/*photon splitting* em QED com violação de
   Lorentz, não do atraso de tempo de voo `∝(E/M*)⁴` assumido no
   enunciado para o ramo II. É citado apenas como ordem de grandeza
   ilustrativa, com essa ressalva explícita na tabela.
5. **Ausência de bound direto LVK para `α=6`.** A Tabela VII de GWTC-3 vai
   até `α=4`; não há, até onde verificamos, nenhum catálogo publicado de
   LVK com `α=6`, de modo que o ramo II carece de um teste direto de
   dispersão gravitacional análogo ao do ramo I.

## Reprodutibilidade

Execute a partir **desta pasta** (há um `bisect.py` de scratchpad de sessão
em outro diretório que sombreia o módulo padrão da biblioteca — rodar fora
desta pasta pode quebrar o `import` de `random`/`urllib`):

```
python3 bounds_ell_star.py
```

O script:

1. roda dois **controles negativos** (fórmula com potência errada de `A_4`,
   e fórmula sem o fator `2π` na conversão frequência→número de onda) e
   verifica explicitamente que essas mutações produzem um resultado
   detectavelmente diferente do resultado correto (`assert` de divergência
   relativa `> 50%`);
2. roda dois **cross-checks** de conversão por rota independente (ida-e-volta
   comprimento↔massa, e duas ordens de operação distintas para `A_4→ℓ*`),
   verificando concordância numérica a `< 10⁻⁹` de diferença relativa;
3. converte todos os limites da tabela acima e imprime o resumo;
4. gera `fig_bounds_ell_star.pdf`, o gráfico de exclusão com eixo `ℓ*` em
   escala log de `1.6×10⁻³⁵ m` (extremo do eixo) a `10⁻³ m`, mostrando a
   região excluída por experimento/ramo e marcando o comprimento de Planck
   `ℓ_P = 1.616255×10⁻³⁵ m` (valor CODATA) com uma linha vertical tracejada.

## Notas de verificação de DOI

Todo DOI da tabela foi consultado via
`https://api.crossref.org/works/<doi>` e o título/periódico/volume/página
retornados foram conferidos contra a citação pretendida. Dois DOIs que
haviam sido inicialmente presumidos de memória estavam **incorretos** e
foram corrigidos após a consulta:

- `10.1038/nphys2667` (suposto para Vasileiou et al. 2013) na verdade
  resolve para um artigo completamente diferente ("Capturing photons with
  transformation optics", Nature Physics 9, 518). O DOI correto,
  confirmado via Crossref, é `10.1103/PhysRevD.87.122001` (Phys. Rev. D 87,
  122001, 2013).
- `10.1103/PhysRevD.106.082004` (suposto para "Tests of General Relativity
  with GWTC-3") na verdade resolve para um artigo não relacionado sobre
  "Thunderstorm ground enhancements". O DOI correto, confirmado via
  Crossref, é `10.1103/PhysRevD.112.084080` (Phys. Rev. D 112, 084080,
  2025).

Este é exatamente o tipo de erro que a verificação por Crossref, exigida
pelo protocolo do projeto, existe para capturar — nenhum número final da
tabela depende de um DOI não verificado.
