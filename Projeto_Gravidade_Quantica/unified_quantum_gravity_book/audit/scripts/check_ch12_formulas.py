import numpy as np
from scipy import integrate, special
# 1) Jarlskog formula as printed in ch12 (GeV, PDG-ish masses)
mu,mc,mt,md,ms,mb,v=0.00216,1.27,172.7,0.00467,0.0934,4.18,246.22
J=np.sin(np.radians(63.90))/(6*np.sqrt(3))*np.sqrt(mu*mc*mt*md*ms*mb)/v**6
print("J_CP printed formula =",J,"(book claims 3.04e-5; formula has units GeV^-3)")
# 2) closed-form P(tau) and d_s(tau) of ch12 sec 8.2, l_P=1
def P_num(t): return integrate.quad(lambda u: u*np.exp(-t*(u+u*u)),0,np.inf)[0]/(16*np.pi**2)
def P_cf(t):
    z=np.sqrt(t)/2; return (1-np.sqrt(np.pi)*z*special.erfcx(z))/(32*np.pi**2*t)
def ds_book(t):
    z=np.sqrt(t)/2; return 1-t/2+1/(1-np.sqrt(np.pi)*z*special.erfcx(z))
def ds_num(t,h=1e-5):
    return -2*(np.log(P_num(t*np.exp(h)))-np.log(P_num(t*np.exp(-h))))/(2*h)
for t in [1e-3,0.1,1,10,100]:
    print(f"tau={t:g}: P ratio num/cf={P_num(t)/P_cf(t):.6f}  ds_book={ds_book(t):.5f} ds_num={ds_num(t):.5f}")
# 3) alpha_t magnitude at CMB scales
k_over_MP=0.05/ (1.2e19*5.07e15) # k=0.05 Mpc^-1 ~ in GeV? rough: 0.05/Mpc = 0.05/(1.56e38 GeV^-1)
k=0.05/1.56e38; MP=1.22e19
print("alpha_t at k=0.05/Mpc ~", -1/(1+(k/MP)**-2))
# 4) GW dispersion delay, D_L=1 Gpc, f 10->1000 Hz
lp=1.616e-35;c=2.998e8;D=3.086e25
print("Delta t_disp (s) =",6*np.pi**2*0.5*lp**2*D/c**3*(1000**2-10**2))
# 5) hemisphere mean curvature in Poincare half-plane (d=2 slice): curve x=R cos th, z=R sin th, metric (dx^2+dz^2)/z^2
# geodesic curvature in hyperbolic metric: k_h = z*k_e + n_x... use formula k_h = z*k_e - n.grad... numerically: k_h = z*k_E + (unit normal)_z  ; circle centered on boundary
R=1.0; th=0.7; z=R*np.sin(th); kE=1/R; nz=-np.sin(th) # inward normal z-comp
print("hyperbolic geodesic curvature of boundary-centered semicircle =", z*kE+nz)
