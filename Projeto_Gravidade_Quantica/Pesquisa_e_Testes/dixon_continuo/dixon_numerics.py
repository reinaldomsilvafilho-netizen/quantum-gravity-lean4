"""Task A: numerics for the continuous Dixon integral.

f_n(t) = binom(2n, n+t)^3 = [Gamma(2n+1) / (Gamma(n+1+t) Gamma(n+1-t))]^3,
I_j(n) = int_{-n}^{n} cos(pi j t) f_n(t) dt,   j odd.

Two independent evaluations are compared:
  (Q) direct Gauss-Legendre/tanh-sinh quadrature on [-n, n];
  (O) oracle from the proof:  I_1 = D_n/2 - 2 T_1,  I_j = -2 T_j (j >= 3),
      with D_n = sum_k (-1)^k binom(2n,n+k)^3 computed in exact integers and
      T_j = int_n^inf cos(pi j t) f_n(t) dt computed from the Beta-function
      representation f_n(n+s) = [B(s,2n+1) sin(pi s)/pi]^3 (different code path).
Then exponential rates are fitted and compared with the saddle/endpoint
predictions, with negative controls.

Run from the project folder:  python Pesquisa_e_Testes/dixon_continuo/dixon_numerics.py
"""
from fractions import Fraction
from math import comb, factorial
import sys

from mpmath import mp, mpf, quad, cos, sin, pi, gamma, rgamma, beta, inf, log, exp, sqrt, tan, mpc, re, harmonic

mp.dps = 70
NS = list(range(2, 21))
JS = [1, 3, 5, 7, 9]
out_lines = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    out_lines.append(s)


def f(n, t):
    return (gamma(2 * n + 1) * rgamma(n + 1 + t) * rgamma(n + 1 - t)) ** 3


def I_direct(n, j):
    # even integrand: 2 * int_0^n, split at quarter-integers
    pts = [mpf(k) / 4 for k in range(0, 4 * n + 1)]
    return 2 * quad(lambda t: cos(pi * j * t) * f(n, t), pts, method="gauss-legendre")


def f_tail(n, s):
    # f_n(n+s) = [B(s,2n+1) sin(pi s)/pi]^3 ; at s=0 the limit is 1
    if s == 0:
        return mpf(1)
    return (beta(s, 2 * n + 1) * sin(pi * s) / pi) ** 3


def tail_cutoff(n, eps=mpf(10) ** -36):
    """L such that int_{n+L}^inf |f| <= eps, using |f(n+s)| <= pi^-3 B(s,m)^3,
    B(s,m) <= (m-1)! s^-m  (integer m), so the remainder is
    <= pi^-3 ((m-1)!)^3 L^(1-3m) / (3m-1)."""
    m = 2 * n + 1
    L = 8
    while (gamma(m) ** 3 / pi ** 3) * mpf(L) ** (1 - 3 * m) / (3 * m - 1) > eps:
        L += 8
    return L


def T_oracle(n, j):
    step = max(4, j)
    L = tail_cutoff(n)
    pts = [mpf(k) / step for k in range(0, 4 * step + 1)] + [mpf(k) / 4 for k in range(17, 33)] + list(range(9, L + 1))
    return quad(lambda s: cos(pi * j * (n + s)) * f_tail(n, s), pts)


def dixon_exact(n):
    return sum((1 - 2 * (k % 2)) * comb(2 * n, n + k) ** 3 for k in range(-n, n + 1))


def main():
    say("=== A1. Dixon identity, exact integers ===")
    for n in NS:
        D = dixon_exact(n)
        assert D == factorial(3 * n) // factorial(n) ** 3, n
    say("D_n == (3n)!/(n!)^3 for n = 2..20: OK")
    # negative control: mutated closed form must fail
    bad = [n for n in NS if dixon_exact(n) != factorial(3 * n + 1) // (factorial(n) ** 3 * (3 * n + 1)) + 1]
    assert len(bad) == len(NS)
    say("negative control (closed form + 1) rejected for all n: OK")

    say("\n=== A2. I_j by direct quadrature vs oracle ===")
    table = {}
    maxrel = mpf(0)
    for n in NS:
        D = mpf(dixon_exact(n))
        row = []
        for j in JS:
            Iq = I_direct(n, j)
            T = T_oracle(n, j)
            Io = D / 2 - 2 * T if j == 1 else -2 * T
            err = abs(Iq - Io)
            maxrel = max(maxrel, err / max(abs(Io), mpf(1)))
            table[(n, j)] = Iq
            row.append(mp.nstr(Iq, 12))
            assert err < mpf(10) ** -30 * max(abs(Io), 1), (n, j, err)
        say("n=%2d " % n + "  ".join("I_%d=%s" % (j, r) for j, r in zip(JS, row)))
    say("max |Q - O| / max(|O|,1) over all (n,j):", mp.nstr(maxrel, 5), " (required < 1e-30)")

    say("\n=== A3. 30-digit values at n = 20 ===")
    for j in JS:
        say("I_%d(20) = %s" % (j, mp.nstr(table[(20, j)], 32)))
    say("D_20/2  = %s" % mp.nstr(mpf(dixon_exact(20)) / 2, 32))

    say("\n=== A4. Rates ===")
    # least-squares slope of log|I_j| (for j=1 of log(n I_1)) over n = 8..20
    def slope(ys, xs):
        mx = sum(xs) / len(xs)
        my = sum(ys) / len(ys)
        return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)

    xs = [mpf(n) for n in range(8, 21)]
    rates = {}
    for j in JS:
        ys = [log(abs(table[(n, j)]) * (n if j == 1 else 1)) for n in range(8, 21)]
        rates[j] = exp(slope(ys, xs))
        say("j=%d fitted rate exp(slope) = %s" % (j, mp.nstr(rates[j], 10)))

    # saddle-point predictions, principal branch
    def h(tau):
        return 2 * log(2) - (1 + tau) * log(1 + tau) - (1 - tau) * log(1 - tau)

    def saddle_rate(j, tau):
        return exp(re(3 * h(tau) + 1j * pi * j * tau))

    say("\nSaddle tau_j = i tan(pi j/6) (principal branch of log):")
    preds = {}
    for j in JS:
        if j % 6 == 3:
            say("j=%d: tan(pi j/6) infinite, no finite saddle -> endpoint prediction rate 1" % j)
            preds[j] = mpf(1)
            continue
        tau = mpc(0, tan(pi * j / 6))
        preds[j] = saddle_rate(j, tau)
        say("j=%d: tau=%s, predicted rate %s" % (j, mp.nstr(tau, 8), mp.nstr(preds[j], 10)))
    assert abs(preds[1] - 27) < mpf(10) ** -40
    assert abs(rates[1] - 27) < 0.05
    say("j=1: saddle rate == 27 exactly, fit %s: ACCEPTED" % mp.nstr(rates[1], 8))
    for j in [3, 5, 7, 9]:
        verdict_saddle = abs(log(rates[j]) - log(preds[j])) < 0.05
        say("j=%d: fit %s vs saddle/endpoint prediction %s -> %s" % (
            j, mp.nstr(rates[j], 6), mp.nstr(preds[j], 6), "ACCEPTED" if verdict_saddle else "REJECTED"))
        assert abs(log(rates[j])) < 0.05, "j>=3 should be sub-exponential"
    say("Conclusion: for j = 5, 7 the principal-branch saddle predicts exponential growth,"
        " the data show rate 1 (bounded, slowly decaying). The saddle is not on the"
        " integration contour; for j >= 3 the exact full-line integrals vanish (type 3*pi).")

    say("\nNegative control: wrong saddle tau = i tan(pi j/3) for j=1:")
    wrong = saddle_rate(1, mpc(0, tan(pi / 3)))
    ok = abs(log(wrong) - log(rates[1])) > 0.05
    assert ok
    say("  predicted %s vs fit %s -> REJECTED (as it must be)" % (mp.nstr(wrong, 8), mp.nstr(rates[1], 8)))

    say("\n=== A5. Endpoint model for j >= 3 ===")
    say("model: I_j ~ -2 (-1)^n * 3H/(9H^2 + pi^2 j^2),  H = H_{2n}  (from f(n+s) ~ exp(-3 H s))")
    for n in [5, 10, 15, 20]:
        H = harmonic(2 * n)
        parts = []
        for j in [3, 5, 7, 9]:
            model = -2 * (-1) ** n * 3 * H / (9 * H ** 2 + pi ** 2 * j ** 2)
            parts.append("j=%d ratio %s" % (j, mp.nstr(table[(n, j)] / model, 5)))
        say("n=%2d: " % n + "; ".join(parts))

    say("\n=== A6. Finite-interval Poisson identity (fact 1) ===")
    # sum_{j odd >= 3} I_j = 2 T_1 - (-1)^n / 2 ; check with partial sums over j <= J plus 1/j^2 tail fit
    mp.dps = 20
    for n in [4, 7]:
        T1 = T_oracle(n, 1)
        target = 2 * T1 - mpf((-1) ** n) / 2
        partial = mpf(0)
        J = 61
        for j in range(3, J + 1, 2):
            partial += -2 * T_oracle(n, j)
        say("n=%d: sum_{3<=j<=%d} I_j = %s, target %s, diff %s (tail O(1/J))" % (
            n, J, mp.nstr(partial, 10), mp.nstr(target, 10), mp.nstr(partial - target, 3)))
        assert abs(partial - target) < 2.0 / J

    with open(__file__.replace(".py", ".out.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out_lines) + "\n")


if __name__ == "__main__":
    main()
