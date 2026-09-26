"""Order-of-magnitude estimates for the phenomenological signatures of Chapters 12-13.

Produces the numbers quoted in the text and the figure fig_experimental_signatures.pdf.
Run from the book directory:  python audit/scripts/observability_estimates.py

Conventions
-----------
* Dispersion omega^2 = c^2 k^2 (1 + xi l^2 k^2): v_g/c - 1 = (3/2) xi l^2 k_phys^2.
  A graviton observed at frequency f had physical wavenumber k_phys = (2 pi f / c)(1 + z')
  at redshift z', so the accumulated delay is weighted by (1 + z')^2:
      |Delta t| = 6 pi^2 xi l^2 (f2^2 - f1^2) D_2(z) / c^3,
      D_2(z) = (c/H0) int_0^z (1+z')^2 dz' / E(z')
  (Jacob & Piran 2008 with n = 2; Mirshekari, Yunes & Will 2012 with alpha = 4).
* Tensor-tilt running ansatz alpha_t = (d_s - 4)/2 = -x^2/(1+x^2), x = p/M_*, where p is the
  PHYSICAL momentum of the mode when it is generated, i.e. at horizon exit, p = k/a = H_inf.
  H_inf is bounded by the tensor-to-scalar ratio: P_t = 2 H^2/(pi^2 M_red^2) = r A_s.
* M_P = sqrt(hbar c / G) (non-reduced) unless stated; M_red = M_P / sqrt(8 pi).
"""
import numpy as np
from scipy import integrate
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

c = 2.99792458e8          # m/s
hbar = 1.054571817e-34    # J s
G = 6.67430e-11           # m^3 kg^-1 s^-2
ell_P = np.sqrt(hbar * G / c**3)   # m
Mpc = 3.0856775814913673e22        # m
H0 = 70e3 / Mpc                    # s^-1
Om, OL = 0.3, 0.7
GeV_inv_m = 1.973269804e-16        # hbar c in GeV m
M_P_GeV = 1.220890e19              # Planck mass, GeV
M_red_GeV = M_P_GeV / np.sqrt(8 * np.pi)
r_max = 0.036                      # BICEP/Keck 2021, 95% upper limit
A_s = 2.1e-9                       # Planck 2018 scalar amplitude
F1, F2 = 10.0, 1000.0              # Hz, frequency band of the text


def E(z):
    return np.sqrt(Om * (1 + z) ** 3 + OL)


def D2(z):
    """Propagation distance weighted by (1+z')^2 for a quartic (k^4) dispersion correction, m."""
    return c / H0 * integrate.quad(lambda zp: (1 + zp) ** 2 / E(zp), 0, z)[0]


def delta_t(ell, D, f1, f2, xi=0.5):
    """|Delta t| for omega^2 = c^2 k^2 (1 + xi ell^2 k^2)."""
    return 6 * np.pi**2 * xi * ell**2 * D / c**3 * (f2**2 - f1**2)


def ell_required(dt, D, f1, f2, xi=0.5):
    return np.sqrt(dt * c**3 / (6 * np.pi**2 * xi * D * (f2**2 - f1**2)))


def alpha_t(p_GeV, M_GeV=M_P_GeV):
    x = (p_GeV / M_GeV) ** 2
    return -x / (1 + x)


def H_inf_max_GeV(r=r_max, As=A_s):
    return np.pi * M_red_GeV * np.sqrt(r * As / 2)


def main():
    print(f"ell_P = {ell_P:.4e} m")
    for z in (1, 3, 8):
        D = D2(z)
        dt = delta_t(ell_P, D, F1, F2)
        print(f"z={z}: D2 = {D/Mpc/1e3:.2f} Gpc, |dt|(10->1000 Hz, xi=1/2, ell_P) = {dt:.2e} s, "
              f"orders below 1e-4 s: {np.log10(1e-4/dt):.1f}")
    D3 = D2(3)
    ellreq = ell_required(1e-4, D3, F1, F2)
    E_req_GeV = GeV_inv_m / ellreq
    print(f"ell_* needed for |dt| = 0.1 ms at z=3: {ellreq:.2e} m  (energy scale {E_req_GeV*1e9:.2f} eV)")
    print(f"ratio ell_*/ell_P = {ellreq/ell_P:.2e}")

    # GW170817 speed bound |v_g - c|/c < ~1e-15 at f ~ 100 Hz: (3/2) xi ell^2 k^2 < 1e-15
    k100 = 2 * np.pi * 100 / c
    print(f"(3/2) xi (ell_req k)^2 at 100 Hz = {1.5 * 0.5 * (ellreq * k100)**2:.1e} (GW170817 bound ~1e-15)")

    # tensor tilt: physical momentum at horizon exit = H_inf
    H = H_inf_max_GeV()
    print(f"H_inf <= {H:.2e} GeV (r < {r_max}, A_s = {A_s})")
    print(f"|alpha_t| at horizon exit: M_*=M_P -> {-alpha_t(H):.1e}; M_*=M_red -> {-alpha_t(H, M_red_GeV):.1e}")
    k_cmb_GeV = 0.05 / Mpc * GeV_inv_m
    print(f"(comoving k_pivot today = {k_cmb_GeV:.1e} GeV is not the physical scale of the mode)")

    # atom interferometry ell_P / lambda_dB for Sr-87
    m_Sr = 87 * 1.66053906660e-27
    for v in (0.01, 1.0, 10.0, 45.0):
        lam = 2 * np.pi * hbar / (m_Sr * v)
        print(f"Sr-87 v={v} m/s: lambda_dB = {lam:.2e} m, ell_P/lambda_dB = {ell_P/lam:.1e}")

    # ---------------- figure ----------------
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
    f = np.logspace(np.log10(F1) + 0.01, 3.5, 200)
    for z, ls in ((1, "-"), (3, "--"), (8, ":")):
        ax[0].loglog(f, delta_t(ell_P, D2(z), F1, f), ls, color="C0", label=f"$\\ell_\\ast=\\ell_P$, z={z}")
    ax[0].loglog(f, delta_t(ellreq, D3, F1, f), "-", color="C3", label=f"$\\ell_\\ast={ellreq:.1e}$ m, z=3")
    ax[0].axhline(1e-4, color="k", lw=0.8, ls="-.")
    ax[0].text(12, 2e-4, "0.1 ms benchmark", fontsize=8)
    ax[0].set_xlabel("frequency $f$ [Hz]")
    ax[0].set_ylabel("$|\\Delta t_{\\rm disp}|$ [s]  (relative to 10 Hz)")
    ax[0].set_title("(a) GW dispersion delay, $\\xi=1/2$", fontsize=10)
    ax[0].legend(fontsize=7, loc="center right")

    xx = np.logspace(-14, 2, 400)          # p / M_* with p the physical momentum
    ax[1].loglog(xx, -alpha_t(xx, 1.0), color="C0")
    x_cmb = H / M_P_GeV
    ax[1].axvspan(xx[0], x_cmb, color="C2", alpha=0.25)
    ax[1].axvline(x_cmb, color="C2", lw=0.8)
    ax[1].text(3e-14, 1e-4, "CMB modes at horizon exit,\n$H_{\\rm inf}\\leq 4.7\\times10^{13}$ GeV\n($r<0.036$, $M_\\ast=M_P$)",
               fontsize=7)
    ax[1].set_xlabel("$p/M_\\ast$  ($p$ = physical momentum at horizon exit)")
    ax[1].set_ylabel("$|\\alpha_t|$")
    ax[1].set_title("(b) tensor-tilt running ansatz", fontsize=10)
    fig.tight_layout()
    fig.savefig("fig_experimental_signatures.pdf")
    print("wrote fig_experimental_signatures.pdf")


if __name__ == "__main__":
    main()
