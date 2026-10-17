"""English figure of the notched disc for the book (ch. 7), panels (a)-(d) of
LemaC_ataque/figs/fig_entalhes.py with English labels; same formulas, no new numbers.
O = {r <= r_O(phi)}, r_O = 1 - sum_k w_k^2 psi((phi - phi_k)/w_k), phi_k = 2^-k, w_k = 2^-(k+3).
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

KMAX = 40
OUT = sys.argv[1]


def psi(t):
    t = np.asarray(t, float)
    out = np.zeros_like(t)
    m = np.abs(t) < 1
    out[m] = np.exp(1 - 1 / (1 - t[m] ** 2))
    return out


def r_O(phi):
    phi = np.asarray(phi, float)
    r = np.ones_like(phi)
    for k in range(1, KMAX + 1):
        pk, wk = 2.0 ** (-k), 2.0 ** (-(k + 3))
        r -= wk ** 2 * psi((phi - pk) / wk)
    return r


def hull(pts):
    pts = sorted(set(map(tuple, pts)))

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return np.array(lower[:-1] + upper[:-1])


def bridge_of_notch(k, n=40001):
    pk, wk = 2.0 ** (-k), 2.0 ** (-(k + 3))
    phi = np.linspace(pk - 2.4 * wk, pk + 2.4 * wk, n)
    r = r_O(phi)
    pts = np.c_[r * np.cos(phi), r * np.sin(phi)]
    hv = hull(pts)
    ang = np.sort(np.arctan2(hv[:, 1], hv[:, 0]))
    i = np.searchsorted(ang, pk) - 1
    return ang[i], ang[i + 1]


phim, phip = -0.2, 0.7
pm = np.array([np.cos(phim), np.sin(phim)])
pp = np.array([np.cos(phip), np.sin(phip)])
Tm = np.array([-np.sin(phim), np.cos(phim)])
Tp = np.array([-np.sin(phip), np.cos(phip)])
a1 = pm - 0.1 * Tm
a2 = pp + 0.1 * Tp

fig = plt.figure(figsize=(12, 8.4))
gs = fig.add_gridspec(2, 3, height_ratios=[1.25, 1])
ax = fig.add_subplot(gs[0, :])
ph = np.linspace(-np.pi, np.pi, 4000)
rr = r_O(ph)
ax.fill(rr * np.cos(ph), rr * np.sin(ph), color="#d9d9d9", zorder=1)
ax.plot(rr * np.cos(ph), rr * np.sin(ph), color="#555555", lw=1.0, zorder=2)
ax.add_patch(Circle((0, 0), 3, fill=False, ls="--", lw=0.8, color="#999999"))
arcA = np.linspace(phim, phip, 800)
ax.plot(np.cos(arcA), np.sin(arcA), color="#c0392b", lw=2.5, zorder=3,
        label="$W$ (path along the convex hull of $O$)")
ax.plot([a1[0], pm[0]], [a1[1], pm[1]], color="#c0392b", lw=2.5, zorder=3)
ax.plot([pp[0], a2[0]], [pp[1], a2[1]], color="#c0392b", lw=2.5, zorder=3)
for k in range(1, 6):
    pk = 2.0 ** (-k)
    ax.plot([0.97 * np.cos(pk), 1.03 * np.cos(pk)], [0.97 * np.sin(pk), 1.03 * np.sin(pk)],
            color="#1f5fa8", lw=1.2, zorder=4)
    if k <= 3:
        ax.annotate(r"$\phi_%d$" % k, (1.06 * np.cos(pk), 1.06 * np.sin(pk)), fontsize=10, color="#1f5fa8")
ax.plot(1, 0, "o", color="#1f5fa8", ms=6, zorder=5)
ax.annotate(r"$p_0$: the notches accumulate here", (1.02, -0.06), fontsize=10, color="#1f5fa8")
for P, name, dx, dy in [(a1, r"$a_1$", -0.08, -0.08), (a2, r"$a_2$", 0.05, 0.06),
                        (pm, r"$p_-$", 0.03, -0.09), (pp, r"$p_+$", -0.16, -0.02)]:
    ax.plot(P[0], P[1], "o", color="#c0392b", ms=5, zorder=5)
    ax.annotate(name, (P[0] + dx, P[1] + dy), fontsize=11, color="#c0392b")
ax.annotate(r"$O$ (notched disc)", (-0.45, -0.05), fontsize=11, color="#333333")
ax.annotate(r"$\bar\Omega=\bar D(0,3)\setminus \mathrm{int}\,O$", (-1.75, 1.0), fontsize=11, color="#666666")
ax.set_aspect("equal")
ax.set_xlim(-1.85, 1.85)
ax.set_ylim(-0.45, 1.3)
ax.set_xticks([])
ax.set_yticks([])
ax.set_title(r"(a) notches centred at $\phi_k=2^{-k}$ accumulating at $p_0=(1,0)$; "
             r"at this scale they are invisible (depth $w_k^2\leq 1/256$)", fontsize=10)
ax.legend(loc="upper left", fontsize=9, frameon=False)

for j, k in enumerate([1, 2, 3]):
    axk = fig.add_subplot(gs[1, j])
    pk, wk = 2.0 ** (-k), 2.0 ** (-(k + 3))
    phi = np.linspace(pk - 1.6 * wk, pk + 1.6 * wk, 3000)
    r = r_O(phi)
    s = (phi - pk) / wk
    dev = (r - 1) / wk ** 2
    axk.fill_between(s, dev, -1.6, color="#d9d9d9")
    axk.plot(s, dev, color="#555555", lw=1.2, label=r"$\partial O$")
    ta, tb = bridge_of_notch(k)
    A = np.array([r_O(ta) * np.cos(ta), r_O(ta) * np.sin(ta)])
    B = np.array([r_O(tb) * np.cos(tb), r_O(tb) * np.sin(tb)])
    lam = np.linspace(0, 1, 400)
    Q = A[None, :] * (1 - lam)[:, None] + B[None, :] * lam[:, None]
    qphi = np.arctan2(Q[:, 1], Q[:, 0])
    qr = np.hypot(Q[:, 0], Q[:, 1])
    axk.plot((qphi - pk) / wk, (qr - 1) / wk ** 2, color="#c0392b", lw=2.2, label=r"bridge (part of $W$)")
    for t_ in (ta, tb):
        axk.plot((t_ - pk) / wk, (r_O(t_) - 1) / wk ** 2, "o", color="#1f5fa8", ms=6, zorder=5)
    axk.annotate("contact shoulders", ((ta - pk) / wk, (r_O(ta) - 1) / wk ** 2 + 0.12),
                 fontsize=9, color="#1f5fa8")
    axk.set_xlim(-1.6, 1.6)
    axk.set_ylim(-1.15, 0.35)
    axk.set_xlabel(r"$(\phi-\phi_%d)/w_%d$" % (k, k), fontsize=10)
    axk.set_ylabel(r"$(r-1)/w_%d^2$" % k, fontsize=10)
    axk.set_title("(%s) notch $k=%d$: $w_%d=2^{-%d}$, depth $w_%d^2=2^{-%d}$"
                  % ("bcd"[j], k, k, k + 3, k, 2 * k + 6), fontsize=9.5)
    axk.grid(alpha=0.25)
    if j == 0:
        axk.legend(loc="lower left", fontsize=8, frameon=False)

fig.tight_layout()
fig.savefig(OUT, dpi=150)
print("written", OUT)
