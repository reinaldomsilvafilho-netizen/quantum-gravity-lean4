"""Relation between SVW (PRD 84 104018, eq. 3.7) and ch12's 4D isotropic closed form.
I0(tau) = int_0^inf exp(-tau(u + l^2 u^2)) du   (SVW 2-space integral up to pi, with l^2 = 1/(4K^2))
I1(tau) = int_0^inf u exp(-tau(u + l^2 u^2)) du (ch12, P = pi^2 I1 / (2 pi)^4)
Identity: I1 = (1/tau - I0) / (2 l^2) (integration by parts). Oracle: scipy quad.
Negative control: mutated identity (factor l^2 instead of 2 l^2) must fail.
"""
import numpy as np
from scipy.integrate import quad
from scipy.special import erfc, erfcx

l = 0.7
for tau in [1e-3, 0.1, 1.0, 10.0, 100.0]:
    I0 = quad(lambda u: np.exp(-tau * (u + l * l * u * u)), 0, np.inf, limit=400)[0]
    I1 = quad(lambda u: u * np.exp(-tau * (u + l * l * u * u)), 0, np.inf, limit=400)[0]
    # SVW eq. 3.7 with K^2 = 1/(4 l^2): pi*I0 = K/2 sqrt(pi/s) exp(sK^2)(1-erf(sqrt(sK^2))) * (2pi?)
    K2 = 1 / (4 * l * l)
    svw = 0.5 * np.sqrt(K2) * np.sqrt(np.pi / tau) * erfcx(np.sqrt(tau * K2))  # = I0 by completing the square
    assert abs(2 * svw / I0 - 1) < 1e-8, (tau, svw, I0)  # SVW measure normalization: constant 2, irrelevant for d_S
    ident = (1 / tau - I0) / (2 * l * l)
    assert abs(ident / I1 - 1) < 1e-8
    mut = (1 / tau - I0) / (l * l)
    assert abs(mut / I1 - 1) > 0.1
    # ch12 closed form: P = 1/(32 pi^2 l^2 tau) [1 - sqrt(pi) z e^{z^2} erfc(z)], z = sqrt(tau)/(2 l)
    z = np.sqrt(tau) / (2 * l)
    P_book = 1 / (32 * np.pi**2 * l * l * tau) * (1 - np.sqrt(np.pi) * z * erfcx(z))
    P_quad = np.pi**2 * I1 / (2 * np.pi) ** 4
    assert abs(P_book / P_quad - 1) < 1e-7, (tau, P_book, P_quad)
    print(f"tau={tau:g}: I0 via SVW ok, identity ok, ch12 P ok ({P_book:.6e})")
print("OK")
