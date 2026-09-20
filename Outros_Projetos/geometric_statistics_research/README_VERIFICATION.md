# Verificação Numérica e Formal — Geometric Statistics Research

Este guia permite que qualquer pessoa reproduza e confirme os resultados
numéricos das tabelas e as provas formais dos artigos GS-1 e GS-4.

---

## Pré-requisitos

| Ferramenta | Versão mínima | Instalação |
|---|---|---|
| Python | ≥ 3.10 | [python.org](https://www.python.org/downloads/) |
| numpy | ≥ 1.24 | `pip install numpy scipy` |
| scipy | ≥ 1.10 | (incluído acima) |
| Lean 4 + lake | ≥ 4.x | [leanprover.github.io](https://leanprover.github.io/lean4/doc/quickstart.html) |

**Nenhuma GPU é necessária.** Todos os scripts são CPU-only com seeds determinísticos.

---

## GS-1 — Bayesian GLMs & Bakry-Émery

**Artigo:** `papers/paper1_bayesian_glms/paper1_bayesian_glms.pdf`  
**Script Python:** `papers/paper1_bayesian_glms/verify_paper1_numerical.py`  
**Lean 4:** `formal_proofs/GeometricStatistics/BakryEmery.lean`

### Verificação numérica (Python)

```bash
cd papers/paper1_bayesian_glms
python verify_paper1_numerical.py
```

**Saída esperada:**
```
===========================================================================
TRIADIC VERIFICATION HARNESS: PAPER 1 (BAYESIAN GLMS & BAKRY-EMERY)
Author: Reinaldo M. Silva-Filho | PPGEE/DES/UFLA
===========================================================================
[BATTERY 1] Testing Uniform Bakry-Emery Curvature under Separation Sweep...
  ✓ Infimum of minimal eigenvalues: 0.500000 >= lambda_0=0.500000.
  ✓ PASS: Curvature lower bound K* >= lambda_0 holds uniformly under complete separation.

[BATTERY 2] Testing Lichnerowicz-Bakry-Emery Spectral Gap Lower Bound...
  ✓ All Rayleigh quotients satisfy <v, Hess(U) v> >= K* = 0.8000.
  ✓ PASS: Spectral gap lower bound lambda_1 >= K* verified.

[BATTERY 3] Testing 2-Wasserstein Exponential Contraction...
  ✓ PASS: 2-Wasserstein exponential contraction W2(t) <= W2(0) * exp(-K* t) verified.

[BATTERY 4] Running Adversarial Inverse Stress Engine...
  ✓ Global minimal eigenvalue discovered by adversarial optimizer: 0.400002
  ✓ PASS: No adversarial parameter configuration can breach the K* >= lambda_0 curvature floor.

[BATTERY 5] Testing CIG-Langevin Ergodicity and Acceptance Rates...
  ✓ Metropolis-Hastings empirical acceptance rate: 99.67% (Target: >= 30%).
  ✓ PASS: Geometric ergodicity and Metropolis-Hastings filter certified.

===========================================================================
>>> ALL 5 NUMERICAL AND INVERSE VERIFICATION BATTERIES PASSED (0 FAILURES) <<<
===========================================================================
```

### O que cada battery verifica

| Battery | Resultado verificado | Teorema |
|---|---|---|
| 1 | `K* = lambda_0 = 0.5` — curvatura Bakry-Émery uniforme em 30 escalas de separação | Thm 3.1 |
| 2 | Gap espectral de Poincaré `lambda_1 >= K*` — 1.000 direções aleatórias testadas | Thm 3.2 |
| 3 | Contração W2 exponencial `W2(t) <= W2(0) * exp(-K* t)` via acoplamento síncrono de SDE | Thm 3.3 |
| 4 | Inversão adversarial: nenhum otimizador quebra o piso `K* >= lambda_0` | Thm 3.1 |
| 5 | Ergodicidade do CIG-Langevin, taxa de aceitação MH ≥ 30%, covariância a posteriori PD | Thm 4.1 |

---

## GS-4 — Federer Reach & R2-Prox GWAS

**Artigo:** `papers/paper4_federer_reach/paper4_federer_reach.pdf`  
**Script Python:** `papers/paper4_federer_reach/verify_paper4_numerical.py`  
**Lean 4:** `formal_proofs/GeometricStatistics/FedererReach.lean`

### Verificação numérica (Python)

```bash
cd papers/paper4_federer_reach
python verify_paper4_numerical.py
```

**Saída esperada:**
```
==============================================================================
  PAPER 4: TRIADIC NUMERICAL & INVERSE VERIFICATION ENGINE
==============================================================================

BATTERY 1: Federer Reach & Extrinsic Curvature Reciprocal Bound
  mu = 0.10 | Max Extrinsic Curvature kappa*: 10.0000 | Bound 1/mu: 10.0000 | PASS
  mu = 0.25 | Max Extrinsic Curvature kappa*:  4.0000 | Bound 1/mu:  4.0000 | PASS
  mu = 0.50 | Max Extrinsic Curvature kappa*:  2.0000 | Bound 1/mu:  2.0000 | PASS
  mu = 1.00 | Max Extrinsic Curvature kappa*:  1.0000 | Bound 1/mu:  1.0000 | PASS
>>> BATTERY 1 PASSED

BATTERY 5: High-Density Soybean GWAS Benchmark (p=10,000, n=500, LD r^2 > 0.90)
  Method 1: Standard Lasso (L1) -> Selected SNPs: 151 | Discovered QTLs: 13/18 | Block FDR: 0.0%
  Method 2: R2-Prox (Ours)      -> Selected SNPs:  18 | Discovered QTLs: 18/18 | Block FDR: 0.0%
>>> BATTERY 5 PASSED

>>> ALL 5/5 NUMERICAL BATTERIES PASSED WITH ZERO FAILURES. GATE 2 COMPLETE. <<<
```

### O que cada battery verifica

| Battery | Resultado verificado | Teorema |
|---|---|---|
| 1 | `reach(C) >= 1/kappa*` — curvatura recíproca ao reach de Federer em 4 valores de `mu` | Thm 2.1 |
| 2 | Continuidade Lipschitz da projeção dentro do tubo de Steiner; bifurcação detectada fora | Thm 2.2 |
| 3 | Margem de ruído determinística — invariância do suporte em 50 trials (0 saltos) | Thm 3.2 |
| 4 | Convergência linear do R2-Prox; recuperação exata do suporte (15/15 QTLs sintéticos) | Thm 4.1 |
| 5 | Benchmark soja (p=10k, n=500, LD r²>0.90): R2-Prox 18/18 QTLs, FDR=0%; Lasso 13/18 | Table 1 |

---

## Provas Formais Lean 4

```bash
cd formal_proofs
lake build
```

**Saída esperada:** build concluído sem erros, zero `sorry`.

### Módulos Lean e cobertura

| Módulo Lean | Artigo | Obrigações |
|---|---|---|
| `GeometricStatistics/BakryEmery.lean` | GS-1 | OBL-P01-001 a OBL-P01-007 |
| `GeometricStatistics/FedererReach.lean` | GS-4 | OBL-P04-001 a OBL-P04-007 |
| `GeometricStatistics/RiemannianREML.lean` | GS-2/GS-3 | Obrigações REML Riemanniano |
| `GeometricStatistics/SimplicialFractionalGAMM.lean` | GS-5 | Obrigações GAMM Fracionário |
| `GeometricStatistics/TensorTrainDOE.lean` | GS-7 | Obrigações Tensor-Train DOE |

---

## Notas sobre os dados sintéticos

Os scripts **não usam** os dados reais de campo (eucalipto IPEF/UFLA DArTseq ou soja USDA-ARS Axiom 180K),
pois estes são de acesso restrito. Em vez disso, simulam dados sintéticos com as mesmas propriedades
estatísticas (dimensão, estrutura de covariância, sinal-ruído) para confirmar que os algoritmos e garantias
teóricas se sustentam. Os seeds são fixos para reprodutibilidade total.

---

*Autor: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA) — CAPES Finance Code 001*
