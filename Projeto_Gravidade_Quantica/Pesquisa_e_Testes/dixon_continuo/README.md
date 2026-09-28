# Integral de Dixon contínua — status: **PROVADO** (x inteiro); x real ≥ 1 provado módulo uma estimativa de Stirling padrão

Conjectura (livro, cap. 3): com f(t) = binom(2x, x+t)^3,
I_1(x) = ∫_{−x}^{x} cos(πt) f(t) dt ~ ½ Γ(3x+1)/Γ(x+1)^3 ~ (√3/(4πx)) 27^x.

## Resultado principal (dixon_proof.tex / .pdf)

Ideia central: f(z) = Γ(2n+1)^3 sin^3(πz) / (π^3 z^3 ∏(k²−z²)^3) é **inteira de tipo exponencial 3π**
e decai como |t|^(−6n−3) na reta. Logo (Paley–Wiener, provado por deslocamento de contorno):

* J_j := ∫_ℝ cos(πjt) f(t) dt = 0 **exatamente** para todo j ímpar ≥ 3 (inclusive o caso de fronteira j = 3);
* Poisson na reta inteira + identidade de Dixon: **J_1 = ½ (3n)!/(n!)^3 exatamente**.

Então I_j = J_j − 2T_j, com T_j = ∫_n^∞ cos(πjt) f(t) dt, e a cauda satisfaz
f(n+s) = [Γ(m)/(Γ(m+s)Γ(1−s))]^3, m = 2n+1, o que dá, para todo inteiro n ≥ 1:

    |I_1 − ½(3n)!/(n!)^3| ≤ 2τ_n,   |I_j| ≤ 2τ_n (j ímpar ≥ 3),
    τ_n = 1/(3ψ(2n+1)) + 1/(π³ m² (m−1)) = 1/(3(H_{2n} − γ)) + ...  → 0 como 1/(3 log n).

Ou seja, o erro não é só o(27^n/n): ele **tende a zero**. Além disso
Σ_{j ímpar ≥ 3} |I_j| ≤ κ E_n = O(√log n) (Bessel + Cauchy–Schwarz, κ = (2/π)√(π²/8 − 1)).

Constante: por Robbins, (3n)!/(n!)^3 = (√3/(2πn)) 27^n e^{ρ_n}, ρ_n = −2/(9n) + O(n^−2), com colchete explícito.
O fator ½ vem de Poisson: a soma alternada capta as duas frequências ±π, cada uma com J_1.

| n | ∫_n^∞ abs(f) | τ_n | abs(I_1 − D_n/2) | 2τ_n |
|---|---|---|---|---|
| 1 | 0.1776 | 0.3630 | 0.2940 | 0.7260 |
| 10 | 0.0886 | 0.1104 | 0.1658 | 0.2207 |
| 30 | 0.0694 | 0.0812 | 0.1329 | 0.1625 |

| n | Σ_{j ímpar ≥ 3} abs(I_j) (numérico) | cota κE_n |
|---|---|---|
| 1 | 0.213 | 0.962 |
| 12 | 0.359 | 0.931 |

## x não inteiro (tarefa C)

A soma bilateral S(x) = Σ_{k∈ℤ} (−1)^k binom(2x, x+k)^3 é **exatamente Γ(3x+1)/Γ(x+1)^3, sem fator trigonométrico**
(para x > −1/3). Dedução: ₅H₅ de Dougall com e = a/2 (cancela o fator muito-bem-posto), a → 0, b = c = d = −x.
Numericamente: S(x)·Γ(x+1)^3/Γ(3x+1) − 1 < 10^−39 em x = 2.5, 3.7, 1.3, 6.25; um fator cos(πx) é rejeitado.
Com isso, |I_1(x) − ½Γ(3x+1)/Γ(x+1)^3| ≤ 2τ(x) para x real ≥ 1 (ex.: x = 3.7: desvio 0.181 ≤ 0.323).
Ressalva: a cota de crescimento de f_x no semiplano (Stirling uniforme em setor) está enunciada sem constantes explícitas.

## Heurística de ponto de sela (tarefa A)

* j = 1: sela τ = i/√3 dá exatamente a taxa 27 — confirmada.
* j ≡ 3 (mod 6): sem sela; I_j é efeito de extremidade (canto em t = ±n), de tamanho ≍ 1/log n.
* j ≡ 5 (mod 6): a sela conjugada (ramo principal) prevê taxa 27·e^{6π/√3} ≈ 1,44·10^6 — **falsa**; os dados dão taxa 1,00.
* j = 7: o ramo principal prevê taxa ≈ 5,1·10^−4 — também rejeitada (dados: 1,01). Taxas ajustadas (n = 8..20): j=1: 27,04; j=3,5,7,9: 0,995; 1,005; 1,011; 1,014.
* Sela errada τ = i·tan(π/3) para j=1 prevê 230,8 — rejeitada (controle negativo).
  A fase de Stirling não é a continuação analítica de log f (perde o fator sin³); o tipo 3π anula J_5 exatamente.
* Modelo de extremidade I_j ≈ −2(−1)^n · 3H_{2n}/(9H_{2n}² + π²j²) concorda com os dados em 1–4 % (5 ≤ n ≤ 20, 3 ≤ j ≤ 9).
* Valores a n = 20: I_1 = 2,88915607239·10^26 (D_20/2 = 288915607239237911915932950), I_3 = −0,10208, I_5 = −0,06352, I_7 = −0,04023, I_9 = −0,02695. Quadratura direta vs. oráculo concordam a < 10^−30 relativo.

## Arquivos

* `dixon_numerics.py` (+ `.out.txt`): I_j para j = 1,3,5,7,9, n = 2..20, 90 dígitos, quadratura direta vs. oráculo
  independente (D_n inteiro exato + cauda via função Beta); ajuste de taxas; controles negativos (sela errada, fórmula de Dixon mutada).
* `dixon_proof_checks.py` (+ `.out.txt`): verifica cada desigualdade/constante da prova para n = 1..30, com controles negativos
  (τ_n/2 falha; ψ(m+1) no lugar de ψ(m) falha; c_R ≤ 1.13 falha; binom^4, de tipo 4π, tem J_3 ≠ 0; fator cos(πx) falha). TOTAL FAILS: 0.
* `dixon_proof.tex` / `.pdf`: prova completa (amsart), compila com 0 erros, 0 avisos, 0 overfull.

## Ressalvas honestas

* c_R = max |(1/Γ)'| em [0,1] = 1.17081… (u* ≈ 0.3021) é certificado numericamente (não por intervalo); afeta só a cota da soma em j.
  Um primeiro palpite (c_R < 1.13) estava errado e foi pego pelo script de checagem.
* As identidades de Dixon e de Dougall são citadas (e checadas numericamente); os dados bibliográficos não foram resolvidos por DOI.
* O "Fato 1" (Poisson em intervalo finito) não é usado na prova; a consequência Σ_{j ímpar ≥ 3} I_j = 2T_1 − (−1)^n/2 é checada numericamente.
