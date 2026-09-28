"""TM1 sum rule for delta_CP (closed form, King & Luhn / Albright-Rodejohann form):
cos d = -cot(2 t23) (1 - 5 s13^2) / (2 sqrt2 s13 sqrt(1 - 3 s13^2)).
Cross-checked against the numerical scan in signed_scan.py (delta = 75 deg at s23^2 = 0.558)."""
import numpy as np
s13sq = 0.02195
s13 = np.sqrt(s13sq)
for s23sq in (0.45, 0.47, 0.50, 0.53, 0.558, 0.561, 0.58):
    t23 = np.arcsin(np.sqrt(s23sq))
    c = -(1 / np.tan(2 * t23)) * (1 - 5 * s13sq) / (2 * np.sqrt(2) * s13 * np.sqrt(1 - 3 * s13sq))
    d = np.degrees(np.arccos(np.clip(c, -1, 1)))
    print(f"s23^2={s23sq:.3f}: cos d={c:+.3f}  delta = {d:5.1f} or {360-d:5.1f} deg")
