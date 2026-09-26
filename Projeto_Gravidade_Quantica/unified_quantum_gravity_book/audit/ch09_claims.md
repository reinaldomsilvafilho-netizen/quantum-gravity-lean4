# Cap. 9: ledger de afirmações (auditoria 2026-09-24)

Checagens: `audit/scripts/check_ch09.py`. Corpo novo em `audit/_ch09_body.tex` (aplicado via `splice_block.py`).

| ID (antigo) | Enunciado | Tipo | Veredito | Ação |
|---|---|---|---|---|
| Abstract | "certified global theory"; "finite topological roadmap"; "true Chebyshev equioscillation" | — | excesso; apoiado em T1.4 e T4.2, ambos falhos | reescrito |
| §1.3 | Em dimensão n, retração por Morse estratificado a 1-esqueleto com π₁ livre | NE | **falso** (ℝ³∖bola ≃ S²; complemento de nó tem grupo de nó) | Remark; capítulo restrito ao plano |
| §1.4 | π₁ ≅ 𝔽_m; "palavra ciclicamente reduzida" | CL | correto com Ω simplesmente conexo e obstáculos conexos; "ciclicamente" errado (isso é para classes de conjugação) | hipóteses explícitas; "reduzida" |
| P1.1 | Classificação por holonomia SU(2) | CL | correto (representação fiel existe), mas sem prova | **Prop. com prova** (conexões planas ↔ representações) |
| P1.2 | Equivariância por MCG: $\mathrm{Hol}(M\gamma)=g\,\mathrm{Hol}(\gamma)g^{-1}$ | NE | **falso**: a trança age por automorfismo não interno (troca geradores em H₁, item 5) | Remark com naturalidade correta |
| T1.3 | "Medial axis holonomy evaluation" | HE | conselho numérico, não teorema | Remark |
| T1.4(1) | Sub-órbita fechada: $\kappa\ge 2/D_\Omega$ | NP | **verdadeiro**, mas a prova assumia raio constante | **Prop. com prova nova** (tangente não cabe em semiplano + lema do U-turn) |
| T1.4(2) | $\int|\kappa|\ge\int|\theta_i'|-\pi$ | NE | sem prova ("except possibly where…") | retirado |
| T1.4(3) | $L\ge2\pi\rho_i|w_i|$ | NP | quase correto: faltava o termo do caminho de referência | corrigido: $|w_i|\le(V/\rho_i+|\Delta\theta_i(\gamma_0)|)/2\pi$ |
| T1.4(4) | Corte finito $K_{\max}$ sem limite de comprimento | NE | **falso**: restringia $L\le\min(L_{\rm base},\pi D)$ sem justificativa; sem limite, o enrolamento é ilimitado com curvatura fixa (item 3); vetores de enrolamento não separam classes (comutadores, item 4) | **Prop. provada**: com comprimento ≤ V há finitas classes (Arzelà–Ascoli + contratibilidade local) |
| T2.1 | Desdobramento de imersões irredutíveis no recobrimento | CL | correto (prova certa) | mantido como Proposição; Remark: minimizadores podem ter laços nulo-homotópicos |
| P4.1 | Paramétrico ≤ gráfico, "estrito se…" | CL | desigualdade trivial; parte estrita vaga | reduzido ao trivial |
| T4.2 | Γ-convergência e "certeza global" | NE | recuperação usa densidade em $W^{2,\infty}$ (falsa); depende de T1.4(4); barreira só de discos; sem equicoercividade; otimizador local não acha mínimos globais | **Conjectura** + Remark com as 4 lacunas |
| T4.3 | "Convexificação de Frenet" | NE | restrição de caixa é convexa, mas extremos/obstáculos não são; parte (2) vazia | Remark |
| P5.1 | Benchmark: gap de 50,6% Jordan vs imersão | NE | **falso**: pelo U-turn, as duas classes têm κ* = 1/H; o caminho "imerso" é mergulhado; 0,80 não vem da geometria (item 1) | **Prop. provada**: não há gap; Remark |
| Conclusão | "rigorous global theory" | — | excesso | reescrita |

Propagação: Dicionário, caixa 3 (Ch. 7–9), reescrito. Bibliografia: removidos itens sem citação (Whitney, Bott–Tu, Langer).
