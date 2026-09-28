# Parâmetros de fita REBCO: raio de dobra, torção, deformação crítica

Levantado em 2026-09-28. Fontes primárias (folhas de dados de fabricante) quando disponíveis;
caso contrário, artigos com DOI resolvido via Crossref. Números vêm de amostras/fabricantes
específicos — **não misturar** entre eles sem checar a mesma fita.

## Dobra easy-way (em torno do eixo largo — a mais tolerada)

| Fabricante/fonte | Raio/diâmetro mínimo | Critério | Como checado |
|---|---|---|---|
| SuperPower (folha de especificação oficial) | diâmetro mínimo de dobra 11 mm p/ substrato de 50 µm; 6 mm p/ substrato de 30 µm | 95% de retenção de Ic | WebFetch direto de `superpower-inc.com/specification.aspx`, 2026-09-28 |
| Fujikura (fita c/ substrato 50 µm, citada em literatura secundária) | raio de dobra 5 mm sem degradação | não especificado na fonte secundária | **não confirmado**: veio de resultado de busca agregado, não de leitura direta da folha de dados da Fujikura — tratar como indicativo, não como número de projeto |
| MIT/CFS, cabo VIPER (bobina real, não fita isolada) | raio de curvatura ≈100 mm | degradação de Ic < 15% (meta era <20%) | Riva et al. 2023, *Supercond. Sci. Technol.* 36, 105001, DOI `10.1088/1361-6668/aced9d` — resumo lido |
| IPP, bobinas W7-X em escala reduzida, fita GdBCO | raio de curvatura ≈2 cm alcançado | íntegra supercondutora mantida em N₂ líquido | Huslage et al. 2024, *Supercond. Sci. Technol.* 37, 085004, DOI `10.1088/1361-6668/ad5382` — resumo lido |

Nota: os dois primeiros números (fabricante) são o limite mecânico da **fita nua**; os dois
últimos são resultados de **bobina real montada**, já incluindo cabo/moldura — não comparar
diretamente como se fossem a mesma grandeza.

## Dobra hard-way (no plano da fita — a mais restritiva)

| Fonte | Limite reportado | Como checado |
|---|---|---|
| Shin et al. 2009, *Physica C* 469, 1467–1470, DOI `10.1016/j.physc.2009.05.067` (fita YBCO) | Ic começa a degradar de forma **irreversível** acima de 0,6% de deformação hard-way; não há recuperação ao aliviar a deformação | DOI resolvido via Crossref; resumo/achados lidos via busca (autor confirmado: "Shin" como primeiro autor, consistente com o grupo H.-S. Shin, que publica sistematicamente sobre modos de dobra em REBCO) |

Este é o único número de hard-way com fonte específica encontrado nesta revisão. O PLANO.md
descreve a dobra hard-way como "essencialmente proibida" — o valor de 0,6% (Shin et al.) é
consistente com isso quando comparado à deformação crítica easy-way/axial (~0,5–0,7%, tabela
abaixo): a margem de segurança para hard-way é muito menor em relação ao limite de fabricação
(a deformação de hard-way concentra-se de forma desigual na camada supercondutora).

## Torção

| Fonte | Limite reportado | Como checado |
|---|---|---|
| Takayasu et al. (cabo TSTC de 4 fitas YBCO), *Supercond. Sci. Technol.* 25, 014011 (2012), DOI `10.1088/0953-2048/25/1/014011` | Ic **não degrada** até passo de torção (twist pitch) de 120 mm | Resumo checado via busca; título/journal conferido, mas o texto completo não foi lido nesta revisão — número vem do resumo agregado |
| Ashok, Thomas, Mathai, Nijhuis 2023, *IEEE Trans. Appl. Supercond.* 33(3), DOI `10.1109/TASC.2023.3236010` | Estuda tensão+torção combinadas em fita REBCO | PDF obtido mas **não foi possível extrair números específicos** (conteúdo binário/comprimido na extração); DOI e autoria confirmados via Crossref, mas os valores numéricos de limite de torção **não estão confirmados nesta revisão** |

Números de "passo de torção ~90 mm para 5% de degradação em fita YBCO" e "270° de ângulo de
torção para 5% de degradação (YBCO, 4,3 mm, 60 mm de comprimento)" apareceram em resultados de
busca agregados (não em um único artigo lido diretamente aqui). **Rotulo como não confirmado**:
não consegui rastrear esses números até um artigo específico com DOI verificado nesta sessão.
Não usar em cálculo sem antes ler o artigo original (candidatos prováveis: literatura de cabos
CORC/TSTC de Takayasu ou van der Laan — a confirmar).

## Deformação crítica (tração axial / irreversível)

| Fabricante | Deformação irreversível | Fonte | Como checado |
|---|---|---|---|
| SuperPower | 0,66–0,69% | Barth, Mondonico, Senatore 2015, *Supercond. Sci. Technol.* 28, 045011, DOI `10.1088/0953-2048/28/4/045011` | DOI via Crossref; resumo lido; valor numérico veio de busca agregada sobre o mesmo artigo — **recomenda-se conferir a tabela original (Table 2 ou similar) antes de usar em projeto** |
| SuNAM | 0,66–0,68% | idem | idem |
| Bruker HTS | 0,70–0,72% | idem | idem |
| Fujikura | transição tipo degrau ≈0,47–0,49% | idem | idem |
| SuperPower (folha oficial) | resistência à tração ~550 MPa a 77 K p/ 95% retenção de Ic (não dá diretamente % de deformação) | superpower-inc.com/specification.aspx | WebFetch direto, 2026-09-28 |

O artigo de Barth, Mondonico & Senatore (2015) é a referência mais citada para comparar
fabricantes na mesma base experimental (mesmo protocolo, 77 K campo próprio e 4,2 K/19 T); os
valores acima vieram de um resumo de busca sobre esse artigo, não da tabela lida diretamente no
PDF (a extração do PDF nesta sessão falhou — conteúdo binário). **Ação recomendada antes de
qualquer cálculo numérico do problema de bobina: reabrir o PDF do artigo (ou o HTML do arXiv,
`arxiv.org/html/1502.06713v1`) e copiar a tabela de valores diretamente**, em vez de usar os
números desta tabela como definitivos.

## Resumo para uso no problema-modelo (com ressalvas)

- κ_easy (limite de curvatura easy-way): usar como ponto de partida um raio de dobra de
  referência de fabricante ~5–11 mm (fita nua) vs. ~20–100 mm em bobina real montada — a
  diferença importa e deve ser declarada no problema-modelo.
- κ_hard ≈ 0 (hard-way essencialmente proibida): 0,6% de deformação é o único número com fonte
  específica; tratar como ordem de grandeza, não como constante de projeto validada.
- τ_max (torção): nenhum número robusto e confirmado nesta revisão; usar o resultado de Takayasu
  (sem degradação até passo de 120 mm) apenas como limite inferior grosseiro de segurança, e
  marcar qualquer número mais agressivo como não confirmado até nova checagem.
- ε_crit (deformação axial crítica): ~0,5–0,7%, dependente do fabricante; **confirmar a tabela
  de Barth et al. 2015 diretamente** antes de fixar um valor para os cálculos do passo 3 do
  PLANO.md.
