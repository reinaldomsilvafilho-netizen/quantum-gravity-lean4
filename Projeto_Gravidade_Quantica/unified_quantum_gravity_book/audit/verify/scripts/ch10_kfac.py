"""Camada 1 (cega), cap. 10: custo K-FAC por camada.

Oraculo independente: (A kron G)^{-1} vec(V) (inversao densa D x D, D = din*dout) comparado com
G^{-1} V A^{-1} (vec coluna-major). Contagem de flops do caminho fatorado:
inversoes ~ din^3 + dout^3, aplicacao ~ dout^2 din + dout din^2 = din dout (din + dout).
Controle negativo: ordem trocada (A^{-1} no lado errado / kron invertido) deve falhar.
"""
import numpy as np

rng = np.random.default_rng(42)
ok = True
for din, dout in [(3, 5), (7, 4), (10, 10)]:
    Ma = rng.standard_normal((din, din)); A = Ma @ Ma.T + din * np.eye(din)
    Mg = rng.standard_normal((dout, dout)); G = Mg @ Mg.T + dout * np.eye(dout)
    V = rng.standard_normal((dout, din))                  # gradient of W (dout x din)
    vecV = V.reshape(-1, order="F")
    dense = np.linalg.solve(np.kron(A, G), vecV)          # D^3 oracle
    fact = (np.linalg.solve(G, V) @ np.linalg.inv(A)).reshape(-1, order="F")
    wrong = np.linalg.solve(np.kron(G, A), vecV)          # mutated ordering
    e, ew = np.abs(dense - fact).max(), np.abs(wrong - fact).max()
    D = din * dout
    flops_fact = din**3 + dout**3 + din*dout*(din+dout)
    print(f"din={din} dout={dout}: err fatorado {e:.1e}; err mutado {ew:.1e}; "
          f"custo fatorado ~{flops_fact} vs D^3={D**3}")
    ok &= e < 1e-10 and ew > 1e-3
print("ALL CHECKS OK" if ok else "SOME CHECK FAILED")
