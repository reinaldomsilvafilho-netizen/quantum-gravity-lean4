# Cap. 3: ledger de afirmações (auditoria 2026-09-24)

Checagens: `audit/scripts/check_ch03.py`, `check_ch03_b.py`, `check_ch03_kernel.py`.

| ID | Enunciado | Tipo | Veredito | Ação |
|---|---|---|---|---|
| C03-P1.2 | Stifel contínuo | CL | correto (prova completa) | — |
| C03-P1.3 | EDP do digama | CL | correto | — |
| C03-P1.4 | Extensão meromorfa, zeros | CL | correto | — |
| C03-T2.1 | $I(x)=2^x\mathcal J(x)$, forma trigonométrica | NP | **representação exata correta** (verificada até 1e-8) | — |
| C03-T2.1b | $\mathcal J=1-\frac{1}{2x}+O(x^{-2})$ | NE | **falso**: $2^x-I\in(0{,}44;\,0{,}83)$; a aproximação é mais rápida que qualquer potência | corrigido (prova nova via $\operatorname{erf}$) |
| C03-T3.1 | $I_m(x)\sim m^x$ (fase estacionária) | NE | correto numericamente (m=3 até n=14); prova é esboço | — (esboço; B) |
| C03-T4.1 | "Relação exata de defeito de fronteira" $I_m=m^n-\frac m2 I_{m-1}-O(m^n/n)$ | NE | **falso/vazio**: o erro domina a correção; o coeficiente real é ≈0,9 e cai, não 1,5; o termo de E–M em codim. 1 foi omitido | rebaixado a Remark heurístico com números |
| C03-T5.1 | Estrela de Davi contínua | NP | correto (erro 1e-15) | overfull corrigido |
| C03-T5.2 | Diagonal de Fibonacci $\sim\phi^{x+1}/\sqrt5$ | NP | correto (razão 1,000000 em x=40) | — |
| C03-T5.3 | Normas $L^p$ | NE | correto (Laplace/gaussiana conferida à mão) | sem prova no texto (B) |
| C03-T5.4 | Dixon contínuo $\sim\frac12\binom{3x}{x,x,x}$ | NE | correto numericamente (1,000000 em x≥8) | sem prova (B) |
| C03-T5.5 | Integral alternada | NP | parte "x ímpar ⇒ 0" correta; o resto do enunciado tinha **"…"** | corrigido (prova + remark numérico) |
| C03-T5.6 | Hockey-stick contínuo | NE | trivial/assintótico; o termo $-1/\Gamma(r+2)$ fica dentro do erro | B |
| C03-T5.7 | Momentos e covariância | NE | numericamente consistente (Var→x/4, m=2); prova tem passo $O(x)$ não controlado | B (esboço) |
| C03-T5.8 | Entropia de linha via Barnes G | NP | **exata** (verificada com mpmath) | — |
| C03-P6.3(3) | Ação em exponenciais = $((1+\sum e^{-\lambda})/m)^\alpha$ | NE | **falso** para o núcleo contínuo (erros até 30%) | corrigido: vale $\mathcal G_\alpha(\lambda)$ (transformada de Laplace) |
| C03-P6.3(4) | Semigrupo $\mathcal D^\alpha\mathcal D^\beta=\mathcal D^{\alpha+\beta}$ | NE | **falso** (0,128 vs 0,206) | retirado; Remark explica que vale só na rede (Grünwald–Letnikov) |
| C03-T7.1 | Símbolo fechado $R^\alpha\cos(\alpha\Theta)$ | NE | **falso** para o contínuo | substituído por fórmula integral exata + expansão quadrática |
| C03-T7.2 | Limite "Cartan" $\frac{1}{2m\alpha}k^TAk$ | NE | **falso** (já em m=2); a prova impunha $\sum k=0$ artificialmente; a matriz nem é a de Cartan (F-25) | retirado; sobra a forma $S_m$-invariante $a\,I+b\,\mathbf{1}\mathbf{1}^T$ |
| C03-T7.3 | Lei de Weyl com $\lambda_n\to\infty$ | NE | **impossível**: o operador é limitado ($\le 2/\alpha^2$) | retirado; heurística semiclássica para o espectro baixo |
| C03-Tab | Tabela numérica | — | números conferem com os meus | legenda corrigida |

**Propagação:** ch12 Prop. 2.1 (ponte com o símbolo $|k|^{2\alpha}$) corrigida; Dicionário caixa 1 corrigida; **caps. 4, 5 e 6 usam o símbolo fechado e precisam de revisão** (próximas trilhas).
