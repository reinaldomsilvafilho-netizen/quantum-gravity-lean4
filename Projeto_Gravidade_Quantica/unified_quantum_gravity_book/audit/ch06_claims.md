# Cap. 6: ledger de afirmações (auditoria 2026-09-24)

Checagens: `audit/scripts/check_ch06.py`, `check_ch06_b.py`.

| ID | Enunciado | Tipo | Veredito | Ação |
|---|---|---|---|---|
| C06-§1 | Pirâmide de Pascal mod 2 → $m$-simplexo de Sierpiński, $d_H=\ln(m+1)/\ln 2$ | CL | correto (contagem $4^k$ conferida para $m=3$) | — |
| C06-A2.2 | Fator de renormalização $m+3$ | CL (Kigami) | correto; declarado como hipótese importada | — |
| C06-D2.1 | Operador decimado | def | **mal definido** ($\Delta_{\Delta_m}^\alpha$ age em $\R^m$, não em $K$) | marcado como formal + referência ao Remark |
| C06-T2.3 | "Convergência forte de resolventes a $\Delta_{\rm Kigami}$" | NE → CJ | falso como enunciado (formas nulas: $K$ tem medida de Lebesgue zero) | já rebaixado a Conjectura + Remark; **faltava `\newtheorem{conjecture}`** (o cap. não compilava) → corrigido |
| C06-T2.4 | Lei de Weyl $N\sim C\lambda^{d_s/2}$ | CL (Kigami–Lapidus) | **"∼" errado**: no gasket $N/\lambda^{d_s/2}$ oscila (log-periódico) | enunciado com cotas $c_1\lambda^{d_s/2}\le N\le c_2\lambda^{d_s/2}$ |
| C06-P3.1 | Assintótica de $\mathcal E(x)$ via Barnes $G$ | NP | correto; resto real é $-\frac16\ln x+2\zeta'(-1)-\frac1{12}+O(x^{-1})$ (verificado até $10^4$, controle negativo com $\frac1{12}$ falha) | enunciado refinado; prova inclui o termo $\frac1{12x}$ de Stirling |
| C06-R3.2 | Espectro multifractal parabólico, $\sigma_0^2=\frac12$ | HE | circular (a "confirmação" usa o mesmo $\int H=\frac12$) | já é Remark heurístico; texto introdutório não o chama mais de derivação; citação de Halsey et al. 1986 adicionada (antes atribuída a Falconer) |
| C06-T4.1 | Dimensão box de Pascal mod 2 | CL | correto, mas a prova misturava a fórmula de reflexão (irrelevante) e contagem sem definir o limite | reescrito como Proposição clássica com prova por IFS/Hutchinson + condição do conjunto aberto; afirmação sobre índice superior negativo precisada ($\binom{-a}{j}=(-1)^j\binom{a+j-1}{j}$, contagem $3^k$ conferida até $k=8$) |
| C06-intro/concl. | "rigorous analytical bridge"; "we proved strong resolvent convergence… derived the multifractal spectrum" | — | falso (contradizia a Conjectura do próprio cap.) | reescritos |

Propagação: Dicionário, linha de $\tau(q)$, marcada como heurística.
