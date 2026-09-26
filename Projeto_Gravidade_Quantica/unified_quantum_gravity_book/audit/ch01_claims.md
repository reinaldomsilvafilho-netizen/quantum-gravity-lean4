# Cap. 1: ledger de afirmações (auditoria 2026-09-24)

Legenda de tipo: CL = clássico/citado · NP = novo, provado · NE = novo, esboço · CJ = conjectura · HE = heurística/proposta.

| ID | Enunciado | Tipo | Prova | Veredito | Ação |
|---|---|---|---|---|---|
| C01-P3.1 | Extremos/críticos de $x^TAx$ na esfera = autovetores | CL | completa | correto | — |
| C01-C3.x | HS-norm $\|T_A\|_{HS}=\|A\|_F/n$; Parseval da realização harmônica | CL | direta | correto | — |
| C01-T4.1 | Energia de Dirichlet $\sum(k_1^2+k_2^2)|a|^2$; razão $\Theta(n^2)$ sob permutação | NP (elementar) | completa | correto | — |
| C01-Ex4.3 | Tabuleiro "mais rugoso" | HE | — | **enganoso**: $J_n$ tem a mesma energia; a realização harmônica mede índices de frequência | corrigido (texto explica e aponta TV) |
| C01-T4.5 | Fórmula da variação total do degrau | NP (elementar) | completa (sup por campos localizados, esboçado) | correto | — |
| C01-T4.6 | Coárea para $W_A$ | CL (Fleming–Rishel/Federer) | citação | correto | — |
| C01-T4.7 | Índices de Morse $i-1$, $\chi(\Sph^{n-1})$ | CL | completa | correto (Hessiana conferida) | — |
| C01-T4.9 | $\|W\|_\square \le \|T_W\|_{\infty\to1} \le 4\|W\|_\square$ | CL | completa (passo "sup em [0,1] atingido em indicadoras" implícito) | correto; o título cita Grothendieck, que não é usado | aberto (B) |
| C01-T4.10 | Compacidade de $(\widetilde{\mathcal W},\delta_\square)$ | CL (Lovász–Szegedy) | citação | correto | — |
| C01-T5.1 | Existência de $\sigma_{\max}$; equações de Lim–Qi | CL | completa | correto; **excesso**: "sem pesos divergentes" | corrigido + Remark de escopo (posto ≥ 2 continua mal-posto) |
| C01-T5.2 | Dualidade $2^k$ e compacidade de hipergrafons | CL | esboço + citação | correto com a norma de corte por produtos; citação certa é **Zhao 2015** | corrigido (Zhao adicionado, DOI verificado; ressalva do counting lemma) |
| C01-T5.3 | Atenção: $H^2(\Tor^2)\hookrightarrow C^{0,\alpha}$, $\sup|f|\le C\sqrt{\mathcal R}$ | CL (Sobolev) | completa | correto; "uniforme em $N$" só se $\mathcal R$ for limitado; a igualdade com a norma $H^2$ só vale para $\lambda=1$ | aberto (B) |
| C01-T5.4 | Complexidade exponencial (Kac–Rice) | CL (ABČ 2013) | esboço | exponencial correto; a **constante explícita $\Sigma(d)$ não confere** com ABČ | corrigido (constante removida, prova marcada como esboço) |
| C01-T5.5 | Escala $d^{-1/2}$; concentração sub-gaussiana | NP/CL | completa (rede-ε) + esboço (Herbst) | correto | — |
| C01-§6 intro | "três resoluções incondicionais" | HE | — | excesso: são resultados clássicos | corrigido |
| C01-§6.1 | Regularização de Sobolev para DL | HE | — | afirmava "garantia de Lipschitz sem limitar capacidade" sem prova; a penalidade não é invariante por permutação de neurônios | corrigido (duas ressalvas explícitas) |
| C01-§6.2 | RSB ↔ $\beta_0$ | CJ | — | já declarado como conjectura | — |
| C01-§6.4 | "Contorna De Silva–Lim" | HE | — | **falso para posto ≥ 2** | corrigido; também abstract e tabela |
| C01-§6.5 | Imagem médica: "complexidade fractal" | HE | — | excesso | corrigido |

Pendências B: título "Grothendieck" (T4.9), notação $\lambda$ em T5.3, índices da spline ($i=0..m$ com $P\in\R^{m\times n\times3}$), "sub-level" vs super-nível em T4.6.
