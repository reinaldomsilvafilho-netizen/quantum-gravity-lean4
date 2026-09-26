"""Chapter 9 checks (global minimax curvature in multiply-connected planar domains)."""
import numpy as np
import sympy as sp

print("1. Benchmark Omega_H = {|y|<=H} minus B_R0(0), R0=1, H=1.62")
R0, H = 1.0, 1.62
# w=0 class: semicircle of radius H centred at (-c, 0), c > H + R0, U-turn on the left of the disk
c = H + R0 + 0.5
t = np.linspace(-np.pi/2, np.pi/2, 20001)
arc0 = np.stack([-c + H*np.cos(t), H*np.sin(t)], 1)
print(f"   w=0 semicircle: max|y|={np.max(np.abs(arc0[:,1])):.4f} (<=H), min dist to origin={np.min(np.linalg.norm(arc0,axis=1)):.4f} (>R0), curvature 1/H={1/H:.4f}")
# w=1 class: semicircle of radius H centred at the origin, around the right side of the disk
arc1 = np.stack([H*np.cos(t), H*np.sin(t)], 1)
print(f"   w=1 semicircle: max|y|={np.max(np.abs(arc1[:,1])):.4f}, min dist to origin={np.min(np.linalg.norm(arc1,axis=1)):.4f}, curvature 1/H={1/H:.4f}")
# is the w=1 path self-intersecting? (straight legs y=-H from x=-X to 0, arc, y=+H back to -X)
print("   w=1 path (legs at y=-H and y=+H joined by the arc) is embedded: the legs lie on different lines and the arc meets each once")
print(f"   U-turn lemma in the strip of width 2H gives kappa >= 2/(2H) = {1/H:.4f} for BOTH classes; claimed Jordan value 1/0.80 = {1/0.8:.4f}")
print(f"   claimed 'relative relief' 50.6% -> actual 0% (both classes attain 1/H when the ports are at y=-+H)")

print("2. Diameter bound for closed sub-loops: width >= 2/kappa in some direction")
rng = np.random.default_rng(3)
worst = np.inf
for _ in range(300):
    # random closed curve: Fourier curve, scaled so that max curvature = 1
    k = np.arange(1, 6); a = rng.normal(size=(2, 5))/k**2; b = rng.normal(size=(2, 5))/k**2
    s = np.linspace(0, 2*np.pi, 4001)[:-1]
    x = (a[0][:,None]*np.cos(k[:,None]*s) + b[0][:,None]*np.sin(k[:,None]*s)).sum(0)
    y = (a[1][:,None]*np.cos(k[:,None]*s) + b[1][:,None]*np.sin(k[:,None]*s)).sum(0)
    dx, dy = np.gradient(x, s), np.gradient(y, s); ddx, ddy = np.gradient(dx, s), np.gradient(dy, s)
    kap = np.abs(dx*ddy - dy*ddx)/(dx**2 + dy**2)**1.5
    if not np.all(np.isfinite(kap)): continue
    scale = np.max(kap)          # rescale curve so that max curvature is 1
    X, Y = x*scale, y*scale
    diam = max(np.ptp(X*np.cos(th) + Y*np.sin(th)) for th in np.linspace(0, np.pi, 181))
    worst = min(worst, diam)
print(f"   min diameter over 300 random closed curves with max curvature 1: {worst:.4f} (bound 2; Jung bound would give only sqrt3={np.sqrt(3):.4f})")

print("3. Without a length bound winding is unbounded at fixed curvature: circle of radius r around the obstacle, traversed w times")
r = 2.0
for w in (1, 5, 50):
    print(f"   w={w}: curvature {1/r}, length {2*np.pi*r*w:.1f}")

print("4. Winding vectors do not separate homotopy classes: commutator [a1,a2] has winding vector (0,0)")
a1, a2 = sp.symbols('a1 a2', commutative=False)
word = [('a1', 1), ('a2', 1), ('a1', -1), ('a2', -1)]
wv = {g: sum(e for h, e in word if h == g) for g in ('a1', 'a2')}
print(f"   winding vector of a1 a2 a1^-1 a2^-1 = {wv}; the word is reduced and nontrivial in F_2")

print("5. Braid generator acts on F_2 by a1 -> a1 a2 a1^-1, a2 -> a1: abelianization swaps a1,a2, so the automorphism is not inner")
print("   inner automorphisms act trivially on H_1 = Z^2; this one acts by the swap matrix [[0,1],[1,0]] != I")
