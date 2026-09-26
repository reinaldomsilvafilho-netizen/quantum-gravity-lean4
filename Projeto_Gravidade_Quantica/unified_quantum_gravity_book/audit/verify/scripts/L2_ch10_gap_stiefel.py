"""Camada 2, F-39 (ch. 10). Independent checks of the corrector's new content.

[1] Analytic gap >= 1/2: min_f E_y min((y-f)^2,1) with y uniform on {+-1} is 1/2 (grid over f).
    Mutation/negative control: biased labels P(y=1)=0.9 give a minimum < 1/2 (hypothesis needed).
[2] Threshold N >= 8 for sqrt(ln(2/delta)/2N) < 1/2 at delta=0.05; value 0.192 at N=50.
    Mutation: /N instead of /2N moves the threshold (to N >= 15).
[3] Remark rem:length_bound: O_sing annulus radii from cond(g~)=1+|grad psi|^2/(1+lambda0);
    covariant acceleration 1/(sqrt(1+lambda0) R_h); major arcs stay at distance >= 2 from c.
    Mutation: forgetting sqrt(1+lambda0).
[4] ||2I-Q||_F^2 = 5d - 4 tr Q >= d for Q in O(d). Mutation 4d-4trQ fails the identity.
[5] Reformulated Stiefel conjecture: connected-component obstruction. For a tanh network
    f(x) = W2 tanh(W1 x), d=2, with W_i in O(2): prod det(W_i) is constant along any continuous
    trajectory (in particular Riemannian GD with the exponential retraction), and the function
    classes {prod det = +1} and {prod det = -1} differ. Teacher with W1 = reflection, W2 = I:
    Sigma* (small eps) meets O(2)^2 but not the component SO(2)^2 of an orthogonal
    initialization in SO(2)^2. Control: a teacher in SO(2)^2 is fitted exactly.
"""
import numpy as np

rng = np.random.default_rng(3)
res = []


def rep(name, ok, extra=""):
    res.append(ok)
    print(("[PASS] " if ok else "[FAIL] ") + name, extra)


# [1]
f = np.linspace(-4, 4, 800001)
cl = lambda y: np.minimum((y - f) ** 2, 1)
m = (0.5 * cl(1) + 0.5 * cl(-1)).min()
rep("[1] min_f E_y clipped loss = 1/2 (uniform labels)", abs(m - 0.5) < 1e-9, f"({m:.6f})")
mb = (0.9 * cl(1) + 0.1 * cl(-1)).min()
rep("[1] NEG biased labels (0.9): minimum < 1/2, so the uniform-label hypothesis is used", mb < 0.5, f"({mb:.3f})")

# [2]
b = lambda N, d=0.05: np.sqrt(np.log(2 / d) / (2 * N))
rep("[2] bound(50)=0.192, bound(7)>1/2, bound(8)<1/2",
    abs(b(50) - 0.1921) < 5e-4 and b(7) > 0.5 and b(8) < 0.5, f"({b(50):.4f}, {b(7):.3f}, {b(8):.3f})")
bm = lambda N, d=0.05: np.sqrt(np.log(2 / d) / N)
rep("[2] NEG mutation /N: threshold not at N=8", bm(8) > 0.5 and bm(15) < 0.5)

# [3]
lam0, Lmax = 0.1, 1.5
r = np.linspace(0, 1, 2_000_001)
grad = 60 * r * (1 - r ** 2) ** 2
cond = 1 + grad ** 2 / (1 + lam0)
inO = r[cond > Lmax]
rep("[3] O_sing = annulus r in [%.4f, %.4f] (referee: [0.013, 0.941])" % (inO.min(), inO.max()),
    abs(inO.min() - 0.0124) < 1e-3 and abs(inO.max() - 0.941) < 1e-3)
for h in (2.0, 20.0):
    Rh = np.hypot(2, h)
    t = np.linspace(0, 2 * np.pi, 400001)
    P = np.stack([2 + Rh * np.cos(t), h + Rh * np.sin(t)], 1)
    major = P[P[:, 1] >= 0]
    dmin = np.linalg.norm(major - [2, 0], axis=1).min()
    # covariant acceleration in constant metric a I, g-unit speed: |D gamma'/ds|_g = sqrt(a) * |x''|_euc / a
    a = 1 + lam0
    acc = np.sqrt(a) * (1 / Rh) / a
    rep(f"[3] h={h}: major arc dist to c = {dmin:.4f} >= 2; g-acceleration {acc:.4f} = 1/(sqrt(1.1) R_h)",
        dmin >= 2 - 1e-9 and abs(acc - 1 / (np.sqrt(a) * Rh)) < 1e-12)
rep("[3] NEG mutation 1/R_h differs from the metric value", abs(1 / np.hypot(2, 2) - 1 / (np.sqrt(1.1) * np.hypot(2, 2))) > 1e-3)

# [4]
ok = True; okneg = False; mins = []
for d in (2, 3, 5, 8):
    for _ in range(200):
        Q, _r = np.linalg.qr(rng.normal(size=(d, d)))
        lhs = np.linalg.norm(2 * np.eye(d) - Q) ** 2
        ok &= abs(lhs - (5 * d - 4 * np.trace(Q))) < 1e-9 and lhs >= d - 1e-9
        okneg |= abs(lhs - (4 * d - 4 * np.trace(Q))) > 1e-6
rep("[4] ||2I-Q||^2 = 5d-4trQ >= d (equality at Q=I)", ok and abs(np.linalg.norm(np.eye(3)) ** 2 - 3) < 1e-12)
rep("[4] NEG mutation 4d-4trQ fails", okneg)

# [5]
d, N = 2, 40
X = rng.normal(size=(N, d)) * 1.5
Rot = lambda a: np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
Ref = np.diag([1.0, -1.0])
net = lambda W1, W2: np.tanh(X @ W1.T) @ W2.T
loss = lambda W1, W2, Y: np.mean(np.sum((net(W1, W2) - Y) ** 2, 1))
Y_bad = net(Rot(0.7) @ Ref, np.eye(2))           # teacher with prod det = -1
Y_good = net(Rot(0.7), Rot(-0.4))                 # teacher in SO(2)^2
ang = np.linspace(0, 2 * np.pi, 721)
best_bad = min(loss(Rot(a1), Rot(a2), Y_bad) for a1 in ang for a2 in ang)
best_good = min(loss(Rot(a1), Rot(a2), Y_good) for a1 in ang for a2 in ang)
# also the other prod-det=+1 component (det,det)=(-1,-1)
best_bad2 = min(loss(Rot(a1) @ Ref, Rot(a2) @ Ref, Y_bad) for a1 in ang[::4] for a2 in ang[::4])
rep("[5] teacher with prod det=-1 is exactly representable in O(2)^2 (loss 0)",
    loss(Rot(0.7) @ Ref, np.eye(2), Y_bad) < 1e-30)
rep("[5] ...but min over SO(2)^2 and over (det,det)=(-1,-1) stays >> 0",
    best_bad > 0.05 and best_bad2 > 0.05, f"(min SO(2)^2 {best_bad:.3f}, min (-,-) {best_bad2:.3f})")
rep("[5] control: teacher in SO(2)^2 is fitted on the grid (min ~ 0)", best_good < 1e-3, f"({best_good:.2e})")
# Riemannian GD with exponential retraction on SO(2)^2 keeps det = +1 (trivial but explicit)
W1, W2 = Rot(0.1), Rot(0.2)
for it in range(300):
    eps = 1e-6
    g1 = (loss(Rot(eps) @ W1, W2, Y_bad) - loss(Rot(-eps) @ W1, W2, Y_bad)) / (2 * eps)
    g2 = (loss(W1, Rot(eps) @ W2, Y_bad) - loss(W1, Rot(-eps) @ W2, Y_bad)) / (2 * eps)
    W1, W2 = Rot(-0.2 * g1) @ W1, Rot(-0.2 * g2) @ W2
rep("[5] Riemannian GD (exp retraction) from SO(2)^2: dets stay +1, loss stays >= min",
    np.linalg.det(W1) > 0 and np.linalg.det(W2) > 0 and loss(W1, W2, Y_bad) >= best_bad - 1e-3,
    f"(final loss {loss(W1, W2, Y_bad):.3f})")

print("\nSUMMARY: %d / %d ok" % (sum(res), len(res)))
