"""F-44 check. C = circ with eigenvalues a + 2b cos(delta + 2 pi k/3) (root masses); M = C^2 has
eigenvalues m_k; both circulant. Two circulant (Hermitian) mass matrices -> |V_CKM| is a permutation.
Oracle: numerical diagonalization by eigh (does not use the DFT). Negative control: perturbing the
down-type matrix off the circulant form gives a non-permutation |V|.
Also checks Koide: Q = sum m / (sum sqrt m)^2 = 1/3 + 2b^2/(3a^2).
"""
import numpy as np

rng = np.random.default_rng(5)
w = np.exp(2j * np.pi / 3)
F = np.array([[w ** (j * k) for k in range(3)] for j in range(3)]) / np.sqrt(3)


def circ_from_eigs(lam):
    return F @ np.diag(lam) @ F.conj().T  # Hermitian circulant when lam real


def root_eigs(a, b, d):
    return np.array([a + 2 * b * np.cos(d + 2 * np.pi * k / 3) for k in range(3)])


def is_circulant(M):
    return all(np.allclose(M[(i + 1) % 3, (j + 1) % 3], M[i, j]) for i in range(3) for j in range(3))


def ckm(Mu, Md):
    _, U = np.linalg.eigh(Mu @ Mu.conj().T)
    _, D = np.linalg.eigh(Md @ Md.conj().T)
    return U.conj().T @ D


for trial in range(200):
    a, b, d = rng.uniform(0.5, 2), rng.uniform(0, 0.7), rng.uniform(0, 2 * np.pi)
    lam = root_eigs(a, b, d)
    C = circ_from_eigs(lam)
    M = C @ C
    assert is_circulant(C) and is_circulant(M)
    assert np.allclose(np.sort(np.linalg.eigvalsh(M)), np.sort(lam ** 2))
    Q = np.sum(lam ** 2) / np.sum(lam) ** 2 if np.all(lam >= 0) else None
    if Q is not None:
        assert abs(Q - (1 / 3 + 2 * b ** 2 / (3 * a ** 2))) < 1e-12
    # two independent circulant sectors (generic, nondegenerate)
    Mu = circ_from_eigs(root_eigs(*rng.uniform(0.5, 2, 1), *rng.uniform(0.1, 0.6, 1), *rng.uniform(0, 6, 1)) ** 2)
    Md = circ_from_eigs(root_eigs(*rng.uniform(0.5, 2, 1), *rng.uniform(0.1, 0.6, 1), *rng.uniform(0, 6, 1)) ** 2)
    V = np.abs(ckm(Mu, Md))
    assert np.allclose(np.sort(V, axis=1)[:, :2], 0, atol=1e-8) and np.allclose(V.max(1), 1)
# negative control
Md2 = Md + 0.2 * np.array([[1, 0.3, 0], [0.3, 0, 0], [0, 0, 0]])
assert not is_circulant(Md2)
V2 = np.abs(ckm(Mu, Md2))
print("control |V| row maxima", np.round(V2.max(1), 3))
assert not np.allclose(np.sort(V2, axis=1)[:, :2], 0, atol=1e-3)
print("OK: circulant pairs give permutation |V_CKM|; M = C^2 circulant with eigenvalues m_k; Koide identity")
