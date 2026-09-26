# Cap. 2: ledger de afirmações (auditoria 2026-09-24)

Checagens numéricas: `audit/scripts/check_ch02.py`.

| ID | Enunciado | Tipo | Prova | Veredito | Ação |
|---|---|---|---|---|---|
| C02-T2.2 | Cone SPD afim-invariante é Hadamard; geodésica explícita | CL (Bhatia) | esboço + citação | correto | — |
| C02-§2.2 | Métrica de Bures–Wasserstein | CL | — | **fator 2**: com $AS+SA=2U$ a métrica é o dobro da que gera $d_{BW}$ | corrigido ($=U$) |
| C02-P2.3 | Espaço tangente e projeção em $\mathcal M_r$ | CL | — | correto | — |
| C02-T2.4 | Dimensão da variedade TT | CL (Holtz–Rohwedder–Schneider) | esboço + citação | correto (fórmula conferida) | — |
| C02-T2.5 | Projeção tangente TT; fluxo projetado | CL | esboço | correto; citação errada (Absil) | corrigido (Lubich–Oseledets–Vandereycken 2015, DOI verificado) |
| C02-T3.2 | Toda: isoespectral, $Q^TA_0Q$ com QR de $e^{tA_0}$ | CL (Symes, Deift) | completa | (i)–(iii) corretos; **erro**: "tempos inteiros = QR sobre $A_0$". É QR sobre $e^{A_0}$ (verificado: erro 4,4 vs 1e-11) | corrigido (enunciado + linha na prova) |
| C02-T3.3 | Preservação de posto e decaimento da perda | CL | completa | correto | — |
| C02-P4.2 | Energia de Dirichlet do Laplaciano de grafon | CL | — | correto | — |
| C02-T4.3 | Semigrupo do calor em grafons | NP | só esboço antes | correto, e há **solução exata** (verificado vs EDO, erro 1e-13) | melhorado: fórmula fechada + prova |
| C02-T4.4 | Contração da norma de corte; descontinuidades persistem | NP | a prova de (i) **não era válida** (Markov/Riesz–Thorin não controla a norma de corte) | enunciado correto | corrigido: prova nova pela forma fechada (verificado numericamente) |
| C02-T5.1 | "Neckpinch" de Ricci em grafons | NE → condicional | heurística | **métrica $d$ não definida**; com a métrica discreta $\kappa\ge0$; o limite indicado é **falso** (densidades internas crescem como $e^{2c_1t}$) | rebaixado a Proposição condicional + Remark; limite normalizado vira conjectura |
| C02-T5.2 | Dissipação de perímetro sob MCF | CL (formal) | formal | Evans–Spruck exige dado contínuo; $W_A$ é degrau; vale só enquanto os níveis são suaves | rebaixado a Proposição com hipóteses explícitas |
| C02-T6.1 | cMPS: fluxo gradiente dissipativo | CL (Haegeman et al.) | esboço | "converge ao estado fundamental" é **excesso** | corrigido + Remark (pontos estacionários variacionais) |
| C02-T6.2 | Limite contínuo do anel tensorial = holonomia; invariância de gauge | NP (clássico em espírito) | completa | **ordem do traço invertida** ($\Tr(A_1\cdots A_k)$ vs $dU=\mathcal A U$; verificado); constantes do erro são "a menos de constantes" | corrigido ($Z_k=\Tr(A_k\cdots A_1)$ + nota) |
| C02-R6.3 | PEPS → Yang–Mills | CJ | — | já declarado como conjectura | — |
| C02-Tab | Fluxo de covariância $-A(\log A)A$ | — | — | o gradiente AI de $\frac12 d^2$ é $-A\log A$ | corrigido |
| C02-abstract | "rigorously establishing parabolic smoothing"; "converging to the ground state"; "sub-Riemannian" | — | — | contradizia o próprio T4.4 e T6.1 | corrigido |
