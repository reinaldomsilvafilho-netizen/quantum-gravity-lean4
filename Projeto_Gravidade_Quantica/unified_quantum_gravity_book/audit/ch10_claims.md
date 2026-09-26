# Cap. 10: ledger de afirmações (auditoria 2026-09-24)

Checagem: `audit/scripts/check_ch10.py` (contraexemplo + controle negativo). Corpo novo: `audit/_ch10_body.tex`.

| ID (antigo) | Enunciado | Tipo | Veredito | Ação |
|---|---|---|---|---|
| Título/abstract | "Barren plateau avoidance and generalization"; "we prove four foundational theorems" | — | nenhum dos quatro tinha prova; o item (2) (enrolamento em torno de singularidades de Fisher → complexidade polinomial) nem aparecia no corpo | título e abstract reescritos |
| §1.1 | Estrutura sub-Riemanniana de Carnot–Carathéodory nos autovetores principais | HE | a distribuição não tem posto constante nem é bracket-generating em geral | Remark (não usada) |
| §1.1 | K-FAC reduz de O(D³) para O(D) | CL | **falso**: custo O(d_in³+d_out³) + O(d_in d_out(d_in+d_out)) por camada | corrigido |
| D1.1 | κ*_info | def | bem definida | mantida, com classe de caminhos explícita |
| — | (novo) Degenerescência: κ*_info = 0 se uma geodésica atinge Σ* | NP | trivial e decisivo | **Prop. provada** |
| T2.1(2) | $\E\,\mathrm{Tr}\,H\le D\lambda_{\max}\kappa^*$ | NE | **falso** (regressão linear: κ*=0, Tr H≈1) | refutado (Prop.) |
| T2.1(3) | PAC-Bayes com κ* | NE | **falso** (rótulos aleatórios: gap 0,71 > 0,19) | refutado (Prop.); cita Zhang et al. |
| T2.1(1) | Trade-off exploração–explotação | HE | qualitativo | Remark |
| T2.2 | Stiefel + inicialização ortogonal ⇒ tempo polinomial; Euclidiano ⇒ 2^L | NE | sem prova; limite sem sentido para κ*=0; Lévy mal aplicado; prior art (Saxe 2014; Pennington 2017) não citado | **Conjectura** + prior art |
| §3 | Agendamento Frenet com curvatura uniforme | HE | proposta | rotulado proposta |
| Tab. | "Provably terminates at robust, wide minima" | — | falso | tabela reescrita |
| Conclusão | "theoretically established" | — | excesso | reescrita |

Fecha F-15 para o cap. 10 (2 "teoremas" sem prova → 2 proposições provadas + 1 conjectura).
