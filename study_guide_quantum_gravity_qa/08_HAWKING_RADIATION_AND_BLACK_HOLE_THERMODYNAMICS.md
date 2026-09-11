# Module 08: Hawking Radiation & Black Hole Thermodynamics

## 1. What is Hawking Radiation?

In classical General Relativity, nothing (not even light) can escape the event horizon of a black hole.
In 1974, Stephen Hawking combined General Relativity with Quantum Field Theory and proved that **black holes are not black**: they glow with a blackbody thermal spectrum called **Hawking Radiation**.

### Traditional Picture vs. Simplicial Entanglement Picture
* **Traditional Heuristic (Virtual Particle Pairs)**:
  Quantum vacuum fluctuations produce virtual particle-antiparticle pairs near the horizon. One particle with negative energy relative to infinity falls through the horizon, while the other with positive energy escapes to infinity. The escaping particle becomes real radiation, while the inward negative energy flow reduces the black hole's mass ($E = mc^2$).
* **Simplicial Entanglement Derivation (Exact Physics)**:
  The event horizon of a black hole bisects the continuous simplicial tensor network on $\Delta_4$. Tracing out the interior degrees of freedom generates a thermal density matrix $\rho_{\mathrm{horizon}} = \frac{1}{\mathcal{Z}} e^{-\mathcal{H}_{\mathrm{modular}}/k_B T_H}$ via the **Bisognano–Wichmann theorem on continuous simplicial manifolds**.

---

## 2. Fundamental Equations of Black Hole Thermodynamics

### A. The Hawking Temperature ($T_H$)
For a black hole of mass $M$:
$$T_H = \frac{\hbar c^3}{8\pi G M k_B} \approx 6.17 \times 10^{-8}\text{ K} \times \left( \frac{M_\odot}{M} \right)$$
* **Astrophysical Black Hole ($M \sim 10 M_\odot$)**: $T_H \approx 6\text{ nanoKelvin}$ (colder than the CMB).
* **Negative Heat Capacity**: As a black hole loses mass, it gets **hotter and radiates faster**!

### B. The Bekenstein–Hawking Entropy ($S_{\mathrm{BH}}$)
The entropy of a black hole is proportional to the geometric area of its 2D event horizon $A = 4\pi r_s^2 = \frac{16\pi G^2 M^2}{c^4}$, not its 3D volume:
$$S_{\mathrm{BH}} = \frac{k_B c^3 A}{4 G \hbar} = \frac{k_B A}{4 \ell_P^2}$$
**In our model**: The factor of $\frac{1}{4}$ arises as the discrete densitized triad Casimir action of the simplicial face area operator (Chapter 11, Theorem 3.4).

### C. Black Hole Evaporation Lifetime ($\tau_{\mathrm{BH}}$)
By Stefan–Boltzmann radiation ($P = \sigma A T_H^4 = \frac{\hbar c^6}{15360 \pi G^2 M^2}$):
$$\frac{dM}{dt} = -\frac{P}{c^2} \implies \tau_{\mathrm{BH}} = \frac{5120 \pi G^2 M^3}{\hbar c^4} \approx 2.1 \times 10^{67} \left( \frac{M}{M_\odot} \right)^3\text{ years}$$

---

## 3. How this Model Resolves the Black Hole Information Paradox

### The Classic Paradox (Hawking, 1976)
If you throw an encyclopedia into a black hole, and the black hole evaporates into completely random, thermal Hawking radiation, the information is permanently lost. This violates the fundamental **unitarity of Quantum Mechanics** ($\operatorname{Tr}(\rho^2) = 1$).

### The Geometric Resolution in Simplicial Quantum Gravity (Chapter 11 & 12)
1. **Continuous Ryu–Takayanagi Minimal Surfaces via Mean Curvature Flow (MCF)**:
   In the holographic dual tensor network, the entanglement entropy of the Hawking radiation follows the **exact Page Curve**:
   - For $t < t_{\mathrm{Page}}$: Entanglement entropy grows linearly as radiation escapes.
   - For $t > t_{\mathrm{Page}}$: Quantum extremal surfaces shift to the interior "island" boundary, and the entanglement entropy **monotonically decreases back to zero**.
2. **Unitary Information Return**:
   Information is not destroyed; it is encoded in subtle multi-qubit quantum entanglement correlations between early-time and late-time Hawking radiation.
3. **The Kac–Rice Horizon Complexity Bound**:
   The number of microstates saturates the Maldacena–Shenker–Stanford (MSS) quantum chaos bound $\lambda_L = 2\pi k_B T / \hbar$, ensuring that the quantum state vector remains purely unitary throughout evaporation.

---

## 4. The Final Planckian State: No Infinite Singularity

What happens at the end of evaporation when $M \to M_P$?

In standard classical GR, the evaporation ends in an unphysical singular explosion.
In this framework:
* The **Federer Reach Condition** and **Minimax Curvature Ceiling** ($\kappa^* \le 1/\ell_P$) prevent the curvature from diverging.
* When the black hole reaches the Planck mass ($M \sim M_P \approx 2.18 \times 10^{-8}\text{ kg}$), the horizon area hits the minimum single-simplex boundary $A_{\mathrm{min}} \sim \ell_P^2$.
* The remaining energy dissolves smoothly into a finite burst of gravitons and photons through **topological unwinding**, leaving behind pure, flat spacetime with **zero remnant singularity**.

---

## 5. Hawking Radiation $\longleftrightarrow$ Unruh Radiation Equivalence

By Einstein's Equivalence Principle:
* A stationary observer hovering at radius $r$ outside a black hole horizon experiences a proper acceleration $a(r) = \frac{GM}{r^2 \sqrt{1 - 2GM/rc^2}}$.
* The local thermometer measures the **Unruh temperature**:
  $$T_{\mathrm{Unruh}}(r) = \frac{\hbar a(r)}{2\pi c k_B} = \frac{\hbar GM}{2\pi c k_B r^2 \sqrt{1 - 2GM/rc^2}}$$
* When this thermal radiation propagates to an observer at spatial infinity ($r \to \infty$), it undergoes gravitational redshift ($\times \sqrt{1 - 2GM/rc^2}$):
  $$T_\infty = T_{\mathrm{Unruh}}(r) \cdot \sqrt{1 - \frac{2GM}{rc^2}} \equiv \frac{\hbar c^3}{8\pi G M k_B} = T_{\mathrm{Hawking}}$$

$$\textbf{Hawking Radiation is the exact gravitational redshift of Unruh Radiation measured at spatial infinity.}$$
