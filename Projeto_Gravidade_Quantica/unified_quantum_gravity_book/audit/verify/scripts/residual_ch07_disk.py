"""Independent check of kappa* >= 1/2 for the ch7 disk-obstacle example.
Oracle: direct integration of curves with |kappa| <= 1/2 (random controls, and the
two extremal constant-curvature arcs). Negative control: |kappa| <= 3.3 can avoid the disk.
"""
import numpy as np

R = 2.0
print("envelope R - sqrt(R^2-u^2) vs disk half-height:")
for x in [-0.5, -0.4, -0.3, -0.25, -0.2, 0.0]:
    u = x + 1
    env = R - np.sqrt(R * R - u * u)
    disk = np.sqrt(max(0.25 - x * x, 0))
    print(f"  x={x:+.2f} env={env:.4f} disk={disk:.4f} inside={env < disk}")


def shoot(kfun, kmax_steps=4000, ds=1e-3):
    x, y, ph = -1.0, 0.0, 0.0
    for i in range(kmax_steps):
        ph += kfun(i) * ds
        x += np.cos(ph) * ds
        y += np.sin(ph) * ds
        if x * x + y * y < 0.25:
            return True, x, y
        if x >= 1.0:
            return False, x, y
    return False, x, y


rng = np.random.default_rng(1)
avoid = 0
for t in range(2000):
    ks = rng.uniform(-0.5, 0.5, 40)
    hit, *_ = shoot(lambda i: ks[min(i // 100, 39)])
    avoid += not hit
for s in (+0.5, -0.5):
    hit, *_ = shoot(lambda i: s)
    avoid += not hit
print("curves with |k|<=1/2 avoiding the disk:", avoid, "(must be 0)")
assert avoid == 0

# negative control: symmetric left-straight-right-straight-left with |k| = 4
def make(k, a, L1):
    s1 = a / k
    seg = [(s1, k), (L1, 0.0), (2 * s1, -k), (L1, 0.0), (s1, k), (10.0, 0.0)]
    bounds = np.cumsum([s for s, _ in seg])
    def f(i):
        s = i * 1e-3
        j = int(np.searchsorted(bounds, s, side="right"))
        return seg[min(j, len(seg) - 1)][1]
    return f
found = False
for a in np.linspace(0.6, 1.4, 17):
    for L1 in np.linspace(0.1, 0.8, 15):
        hit, x, y = shoot(make(4.0, a, L1), kmax_steps=6000)
        if not hit and x >= 1.0 and abs(y) < 0.05:
            found = True
            break
    if found:
        break
print("control |k|<=4 finds a disk-avoiding curve reaching x=1:", found)
assert found
print("OK")
