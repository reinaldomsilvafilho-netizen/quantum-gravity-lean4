# Verificação cega — `dixon_proof.tex` (integral de Dixon contínua)

Verificador independente (regra dos quatro olhos), 2026-09-28. Não escrevi a prova e não editei `dixon_proof.tex`, os scripts dos autores, o cap. 3 nem o WORKPLAN.

**Scripts:**
- meu: `verify/blind_verify.py`, saída em `verify/blind_verify.out.txt`, **TOTAL FAILS: 0**;
- dos autores: `dixon_proof_checks.py`, reexecutado, TOTAL FAILS: 0, com saída idêntica à arquivada.

**Oráculos independentes usados (diferentes dos dos autores):**
- **J₁ e F(ω):** calculados pela transformada de Ramanujan de 1/(Γ(a+t)Γ(b−t)) seguida de convolução tripla. Esse caminho não usa Poisson, nem Dixon, nem quadratura de f.
- **J₃ e J₅ na fronteira:** quadratura direta na reta inteira, com cota explícita de cauda.
- **Cauda:** calculada pela definição com rgamma, não pela forma Beta.
- **Soma bilateral para x real:** comparada com uma *integral* na reta (Cohl–Volkmer, Thm 5.1) e com Euler–Maclaurin na forma de Pochhammer, não com Dougall.
- **Controles negativos:**
  - tipo 2,9π;
  - J₁ sem o fator ½;
  - F(2,9π) e F(2,99π) ≠ 0, detectados;
  - ∫cos(2,8πt)f ≠ 0, detectado e confirmado pela convolução;
  - Dixon sem o sinal (−1)ᵏ;
  - erro ≤ 1/n;
  - constante √3/(4πn) aplicada ao coeficiente inteiro;
  - fator cos(πx).

  Todos são rejeitados.

## Tabela de verificação

| # | Afirmação | Veredito | Evidência |
|---|---|---|---|
| 1 | Lema 2.1: forma fechada de f e f(k)=0 para \|k\|>n | CONFIRMA | Γ(n+1±z)=Γ(1±z)∏(k±z) e a fórmula de reflexão; conferido à mão. |
| 2 | Cota (2.1): \|f(z)\| ≤ Kₙe^{3π\|Im z\|}\|z\|^{−6n−3} para \|z\| ≥ 2n | CONFIRMA | \|k²−z²\| ≥ ¾\|z\|² é correto. Numericamente, a razão máxima nos círculos R ∈ {2n,3n,7n,20n} (n=1,2,3,5) vale 0,095 ou menos. No eixo imaginário o tipo é exatamente 3π, e a cota com tipo 2,9π é violada (controle negativo). |
| 3 | Lema 2.2: F(ω)=0 para \|ω\| ≥ 3π, incluindo a fronteira ω=3π | CONFIRMA | O deslocamento de contorno está correto. Nos lados verticais o termo é ≤ 2YKR^{−6n−3} → 0 com Y fixo. Com ω=3π o fator exponencial vale 1, e basta o decaimento polinomial ∫(x²+Y²)^{−(6n+3)/2} ≤ CY^{−6n−2}. A hipótese usada é f ∈ L¹ (decaimento t^{−9} no pior caso, n=1), e não o teorema PW em L². Oráculo por convolução: F(3π)=F(3,1π)=0, enquanto F(2,99π) vale 4,8·10⁻¹⁸ (n=1). Quadratura direta: J₃ ≈ 10⁻²², J₅ ≈ 2·10⁻²¹ para n=1, e ≈ 10⁻²⁴ para n=2, todos dentro da cota de cauda. |
| 4 | Lema 2.3 (Poisson): Dₙ = 2J₁ | CONFIRMA | h=f·e^{iπt} satisfaz \|h\| ≤ C(1+\|t\|)^{−3}, e P é contínua e periódica. Os coeficientes são F(π(1−2ν)); os termos de fronteira ν=−1,2 caem exatamente em ±3π, e é aí que o caso de fronteira do item 3 é necessário. A unicidade vem de Fejér. |
| 5 | Lema 2.4 (Dixon) e J₁ = ½(3n)!/(n!)³ exato | CONFIRMA | Dixon verificado em inteiros exatos para n ≤ 40. A convolução de Ramanujan, independente de Dixon, dá J₁ = 3; 45; 840; 17325; 8576568 para n=1,2,3,4,6, igual a (3n)!/(2(n!)³) em 25 dígitos. O mutante sem ½ dá razão 0,5 e é rejeitado. |
| 6 | Lema 3.1: f(n+s) = [Γ(m)/(Γ(m+s)Γ(1−s))]³ = (B(s,m)sin πs/π)³ | CONFIRMA | Substituição direta. Coincide com a quadratura por rgamma. |
| 7 | Lema 3.2 (1)–(4): A ≤ e^{−sψ(m)}, 0 ≤ R ≤ 1, ∫₁^∞B ≤ 1/(m−1), \|B'\| ≤ BH_m | CONFIRMA | Convexidade de log Γ; Γ ≥ 1 em (0,1]; −log u ≥ 1−u; ψ(s+m)−ψ(s)=Σ1/(s+i) ≤ H_m para s ≥ 1. Tudo conferido à mão. |
| 8 | c_R = 1,17081… < 1,18 | CONFIRMA (ressalva) | Calculado independentemente como máx \|ψ(u)/Γ(u)\|, que dá 1,1708063964 em u* = 0,3021417247. A certificação é numérica, não intervalar. Afeta só o item (3) do teorema, com folga. |
| 9 | Prop. 3.3 e Thm (2): \|I₁ − ½Dₙ\| ≤ 2τₙ, \|I_j\| ≤ 2τₙ | CONFIRMA | A prova é completa e as constantes são explícitas. Numericamente (90 dígitos, n=1..40), a razão máxima \|desvio\|/(2τₙ) é 0,83. O desvio alterna de sinal: 0,294, −0,245, …, −0,126 em n=40. Uma cota mutada do tipo 1/n falha, portanto o erro é de fato ≍ 1/log n. |
| 10 | Thm (3): Σ_{j ímpar≥3}\|I_j\| ≤ κEₙ = O(√log n) | CONFIRMA | A periodização G, a integração por partes (termos de fronteira nulos), Bessel em {sin πjs}, ortonormal em L²(0,2), e Cauchy–Schwarz com Σj⁻² = π²/8−1 estão corretos. As três parcelas de Eₙ foram conferidas, e Eₙ ~ √(3 log n/2). A checagem numérica dos autores foi reexecutada. |
| 11 | Constante: (3n)!/(n!)³ = (√3/(2πn))27ⁿe^{ρₙ} e o colchete de Robbins | CONFIRMA | Algebra conferida. (razão−1)·n → −0,22222 (n=10⁶). O mutante √3/(4πn) dá razão 2 e é rejeitado. |
| 12 | Prop. 6.1: S(x) = Γ(3x+1)/Γ(x+1)³ para x > −1/3, sem fator trigonométrico | CONFIRMA | Refiz a especialização do ₅H₅ de Dougall com e=a/2, a→0: o resultado é o ₃H₃ bem-posto Γ(1−b)Γ(1−c)Γ(1−d)Γ(1−b−c−d)/∏Γ(1−u−v), e a condição 1+3x > 0 está certa. O passo de reflexão também confere. Verifiquei ainda o ₃H₃ com parâmetros distintos (erro 10⁻¹⁷). S(−0,2) e S(0,25) coincidem em 10⁻²⁶ com Euler–Maclaurin. A forma clássica está em Bailey (1935), cap. 6, e Slater. |
| 13 | Thm 6.2: extensão a x real ≥ 1 | CONFIRMA (ressalva) | A estimativa de Stirling uniforme no setor (DLMF 5.11.13) é padrão. Além disso, a lacuna declarada pelos autores está coberta na literatura: o Lema 4.1 de Cohl–Volkmer prova F(t)=0 para \|t\| ≥ mπ sob ΣRe(a_j+b_j+1) > 1. Numericamente, 2J/[Γ(3x+1)/Γ(x+1)³] = 1 com erro de 10⁻¹⁴ ou menos em x = 0,4; 1,3; 2,5; 3,7, pela integral na reta. A cota 2τ(x) vale em x = 1,3; 2,5; 3,7. |
| 14 | Remark 4.x: Σ_{j≥3}I_j = 2T₁ − (−1)ⁿ/2 | CONFIRMA (analítico) | Rederivado: pelo Poisson da f truncada, os saltos em ±n contam a metade, logo Dₙ − (−1)ⁿ = 2Σ_{j ímpar}I_j. Combinado com J₁=Dₙ/2, dá a fórmula. Não é usado na prova. |
| 15 | O teorema provado é a conjectura do cap. 3 (`conj:dixon`) | CONFIRMA | A conjectura pede ∫_{−x}^{x}cos(πt)binom(2x,x+t)³dt ~ ½Γ(3x+1)/Γ(x+1)³ ~ (√3/(4πx))27^x com x → ∞ real. O Thm 1.1 cobre x inteiro, com erro absoluto → 0, e o Thm 6.2 cobre x real ≥ 1. O enunciado provado é mais forte que o conjecturado. |
| 16 | Frase do cap. 3: "ratio = 1 to double precision at x=10" | REFUTA (menor, texto do livro) | Calculei razão−1 = −5,98·10⁻¹⁴ em x=10, cerca de 270 ulp, portanto não é 1 em dupla precisão. Os demais números batem: +5,14·10⁻⁷ em x=5, −5,22·10⁻¹¹ em x=7,5 e −5·10⁻²⁸ em x=20. A frase "We have no proof" fica obsoleta. |
| 17 | Novidade: "the key fact" (J₁ exato via Paley–Wiener + Poisson) | INCERTO → provavelmente **não é novo** | **Arte prévia:** H. S. Cohl, H. Volkmer, *Evaluation of beta integrals of Ramanujan type and integral representations for bilateral hypergeometric series*, Ramanujan J. **67** (2025), DOI 10.1007/s11139-025-01064-z, resolvido via Crossref; arXiv:2411.03574. O Lema 4.1 deles é o suporte em \|t\| ≥ mπ. O Thm 5.1, com a=0 e b_j=x, dá exatamente ∫2cos(πt)/∏Γ(x+1±t)dt = Γ(3x+1)/(Γ(x+1)³Γ(2x+1)³), ou seja, J₁ = ½Γ(3x+1)/Γ(x+1)³ para todo x real > −1/3. Verifiquei numericamente o Thm 5.1 em parâmetros genéricos (a=0,3; b=(0,7; 1,2; 2,1)), com erro de 10⁻²¹. O princípio "soma = integral para funções de banda limitada" está em Baillie–Borwein–Borwein, AMM 115 (2008) 888–901. **O que resta de próprio:** a cota elementar de cauda 2τₙ ~ 2/(3 log n), a cota O(√log n) da soma em j e a leitura "conjectura do livro = corolário". A nota deve citar Cohl–Volkmer e não apresentar J₁ exato como resultado novo. |

## Contagem
- CONFIRMA: 15. Os itens 8, 13 e 14 têm ressalvas: a certificação de c_R não é intervalar; o Stirling uniforme é citado; o item 14 foi rederivado só analiticamente.
- REFUTA: 1. É o item 16, uma frase numérica menor do cap. 3, e não a prova.
- INCERTO: 1. É o item 17, sobre novidade e atribuição; ver a arte prévia acima.

## Recomendações (para o autor/corretor, não aplicadas)
1. Citar Cohl–Volkmer (2025), Lema 4.1 e Thm 5.1, como fonte da identidade exata J₁ = ½Γ(3x+1)/Γ(x+1)³. Isso também fecha a ressalva de Stirling do Thm 6.2.
2. Ao integrar no cap. 3: trocar a conjectura por um teorema e citar os resultados. Remover "1 to double precision at x=10" ou substituir pelo valor 6·10⁻¹⁴.
3. Opcional: certificar c_R < 1,18 por aritmética intervalar (por exemplo, `mpmath.iv`).
4. Resolver os DOIs das referências Dixon, Ekhad, Dougall, Bailey e AAR, conforme a convenção 7.
