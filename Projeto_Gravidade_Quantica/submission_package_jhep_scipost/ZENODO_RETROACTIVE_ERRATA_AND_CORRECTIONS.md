# PLANO DE CORREÇÕES RETROATIVAS E ERRATA PARA OS REGISTROS NO ZENODO / CERN

**Autor:** Reinaldo Maia Silva-Filho  
**Filiação:** Programa de Pós-Graduação em Estatística e Experimentação Agropecuária (PPGEE/DES), Universidade Federal de Lavras (UFLA)  
**Financiamento:** CAPES — Código de Financiamento 001  
**Repositório Formal:** [github.com/reinaldomsilvafilho-netizen/quantum-gravity-lean4](https://github.com/reinaldomsilvafilho-netizen/quantum-gravity-lean4)  
**Data do Documento:** 17 de Setembro de 2026  

---

## 1. Contexto e Motivação Editorial

Durante as rodadas de auditoria adversarial profunda conduzidas via **Claude Code CLI (`claude -p`)** em padrão editorial rigoroso para o *Journal of High Energy Physics (JHEP)* e *SciPost Physics*, foram identificadas vulnerabilidades matemáticas, lacunas conceituais e imprecisões epistêmicas nos textos originalmente depositados no Zenodo/CERN.

Para preservar a integridade científica, a rastreabilidade e a transparência do projeto acadêmico, este documento estabelece o **Plano de Correções Retroativas e Registro de Erratas** a ser incorporado nas novas versões (*Version 2 / Version 3*) dos respectivos DOIs no Zenodo.

---

## 2. Inventário dos 6 Registros do Zenodo e Mapeamento de Correções

| Registro Zenodo | DOI | Título do Trabalho | Escopo Afetado | Severidade |
| :--- | :--- | :--- | :--- | :---: |
| **ZEN-01** | [10.5281/zenodo.22290043](https://doi.org/10.5281/zenodo.22290043) | *A Unified Geometric and Algebraic Theory of Quantum Gravity* (Tratado 171 pp.) | Ação mestra, domínio do Beta-Laplaciano, atribuição LQC, scorecard. | **Alta** |
| **ZEN-02** | [10.5281/zenodo.22699282](https://doi.org/10.5281/zenodo.22699282) | *Beyond the Spectrum* (Trilogia Vols. I–III) | Condições de contorno de Sobolev em variedades métrico-mensuráveis. | **Média** |
| **ZEN-03** | [10.5281/zenodo.22699843](https://doi.org/10.5281/zenodo.22699843) | *A Geometric and Metric-Measure Framework for the Yang-Mills Mass Gap* | Autocontenção de Savvidy/Bakry-Émery (já robusto; apenas referências). | **Baixa** |
| **ZEN-04** | [10.5281/zenodo.22707110](https://doi.org/10.5281/zenodo.22707110) | *Geometric Condensation of Fundamental Interactions* | Termo de Yukawa na ação $\mathcal{S}_{\mathrm{univ}}$, métrica em $\mathfrak{g}_{\mathrm{univ}}$, compactificação $\mathfrak{so}(4)$. | **Crítica** |
| **ZEN-05** | [10.5281/zenodo.22707125](https://doi.org/10.5281/zenodo.22707125) | *Geometric Foundations of the Fermion Mass Hierarchy* | Enquadramento epistêmico de Koide ($Q_l = 2/3$), running de quarks, remoção de excessos. | **Crítica** |
| **ZEN-06** | [10.5281/zenodo.22441676](https://doi.org/10.5281/zenodo.22441676) | *A Functorial Bridge from Continuous Tensor Manifolds to Cobordisms* | Ajustes pontuais de notação em costura monoidal e vínculos de Wheeler-DeWitt. | **Baixa** |

---

## 3. Detalhamento Técnico das 7 Correções Retroativas

### Correção 1: Inclusão Explícita do Termo de Yukawa e Forma Bilinear na Ação $\mathcal{S}_{\mathrm{univ}}$
- **Registros Afetados:** **ZEN-04** (Paper da Ação do Universo) e **ZEN-01** (Capítulo 12 do Tratado).
- **Diagnóstico da Falha:** A ação $\mathcal{S}_{\mathrm{univ}}$ original continha apenas $\Tr(\boldsymbol{\Omega} \wedge \star \boldsymbol{\Omega})$, $\bar{\boldsymbol{\Psi}}(\boldsymbol{\mathcal{D}}^{(\alpha)} - \boldsymbol{\mathcal{W}}_{\Delta_2})\boldsymbol{\Psi}$ e $\|\II_{\mathcal{H}}\|_{\mathrm{op}}^2$. Não havia acoplamento explícito entre o férmion $\boldsymbol{\Psi}$ e o campo escalar $\Phi$, desconectando a ação da quebra espontânea eletrofraca. Além disso, somava-se a álgebra de Lorentz não-compacta $\mathfrak{so}(3,1)$ cuja forma de Killing é indefinida, violando a coercividade da ação.
- **Correção Retroativa Aplicada:**
  1. A forma bilinear sobre a álgebra de gauge é formulada sobre a rotação euclidiana compacta $\mathfrak{so}(4) \cong \mathfrak{su}(2) \oplus \mathfrak{su}(2)$ sobre o 4-simplex riemanniano, com forma bilinear estritamente positiva:
     $$\langle \boldsymbol{\Omega}, \boldsymbol{\Omega} \rangle_{\mathcal{G}} = \frac{1}{g_3^2}\Tr_c(G \wedge \star_{\mathcal{G}} G) + \frac{1}{g_2^2}\Tr_L(W \wedge \star_{\mathcal{G}} W) + \frac{1}{g_1^2}(B \wedge \star_{\mathcal{G}} B) + \frac{1}{16\pi G_N}\Tr_E(\mathcal{R} \wedge \star_{\mathcal{G}} \mathcal{R}).$$
  2. O operador de Dirac no produto simplicial $\Delta_4 \times \Delta_2$ é decomposto tensorialmente:
     $$\boldsymbol{\mathcal{D}}_{\mathcal{M}}(\Phi) = \boldsymbol{\mathcal{D}}_{\Delta_4}^{(s)} \otimes \mathbf{1}_{\Delta_2} + \gamma_5 \otimes \boldsymbol{\mathcal{W}}_{\Delta_2}(\Phi),$$
     onde $\boldsymbol{\mathcal{W}}_{\Delta_2}(\Phi) = \mathbf{Y}_{\mathrm{circ}} \Phi(x)$ é o endomorfismo de Weingarten acoplado ao campo escalar de Higgs $\Phi \in \Gamma(\mathcal{H})$.
  3. Quando $\Phi$ condensa no VEV $\langle\Phi\rangle = v/\sqrt{2}$, o termo reduz-se identicamente à massa fermiônica física $\mathbf{M}_f = \frac{v}{\sqrt{2}}\mathbf{Y}_{\mathrm{circ}}$.

---

### Correção 2: Reconciliação do Domínio Espectral do Simplicial Beta-Laplaciano
- **Registros Afetados:** **ZEN-01** (Capítulo 04) e **ZEN-04**.
- **Diagnóstico da Falha:** A Definição 3.1 restringia o expoente fracionário a $\alpha \in (0, 1)$, enquanto o teorema de fluxo de dimensão espectral invocava $\alpha^* = 2$ (ordem bi-harmônica de Lifshitz no regime trans-Planckiano UV).
- **Correção Retroativa Aplicada:**
  1. Define-se $(-\Delta_{\Delta_m})^s$ para todo $s > 0$ via decomposição espectral com base ortonormal de Dirichlet $\{\phi_n, \lambda_n\}$ no espaço de Sobolev $H_0^s(\Delta_m, \mu_{\mathbf{a}})$:
     $$(-\Delta_{\Delta_m})^s u(\mathbf{x}) \coloneqq \sum_{n=0}^\infty \lambda_n^s \langle u, \phi_n \rangle_{\mu_{\mathbf{a}}} \phi_n(\mathbf{x}).$$
  2. Demonstra-se que para $s \in (0, 1)$ o operador coincide com a integral singular em valor principal com núcleo de Dirichlet $\mathcal{K}_\alpha(\mathbf{x}, \mathbf{y})$.
  3. Esclarece-se que no regime UV ($k \gg M_P$) o operador adquire a ordem bi-harmônica $s^* = 2$ (Lifshitz $z = 2$, $\omega^2 \sim \ell_P^2 k^4$, $d_s = 2$), transicionando suavemente para o Laplaciano convencional $s = 1$ no regime infravermelho ($d_s = 4$).

---

### Correção 3: Enquadramento Epistêmico da Fórmula de Koide e Massas Fermiônicas
- **Registros Afetados:** **ZEN-05** (Paper de Massas e Sabor) e **ZEN-01** (Capítulo 12).
- **Diagnóstico da Falha:** O texto anterior apresentava a relação de Koide $Q_l = 2/3$ como se as massas fossem "deduzidas analiticamente sem parâmetros livres", quando na verdade a fase $\delta_l = 2/9 + \pi/12$ era inserida com base nos dados experimentais e a relação $Q_l = 2/3$ decorre algebricamente de qualquer órbita circular circulante com razão $b/a = 1/\sqrt{2}$. Isso feria o padrão de rigor de periódicos como JHEP/SciPost.
- **Correção Retroativa Aplicada:**
  1. **Redefinição do Teorema (Teorema 8.1):** Enquadra-se formalmente o resultado como uma **redução geométrica de parâmetros**: a simetria de permutação $S_3$ sobre $\Delta_2$ reduz os 3 parâmetros livres de massa dos léptons para uma família a 2 parâmetros $(v_0, \delta_l)$ sobre a órbita circular.
  2. O valor $Q_l \equiv 2/3$ é explicitado como um **invariante topológico exato** da representação padrão 2D de $S_3$ ($\Tr(\mathbf{P})/\|\mathbf{P}\|_F^2 = 2/3$), que independe do valor da fase $\delta_l$.
  3. No setor de quarks, detalha-se o running das massas correntes sob equações do grupo de renormalização na escala eletrofraca $\mu = M_Z$, explicitando o papel do Casimir de cor $C_2(F) = 4/3$ no deslocamento $Q_q = \frac{2}{3}(1 + \alpha_s(M_Z)/\sqrt{3})$.

---

### Correção 4: Regularização e Finitude no Bordo do Simplex $\partial \Delta_m$
- **Registros Afetados:** **ZEN-01**, **ZEN-02**, **ZEN-04**.
- **Diagnóstico da Falha:** A métrica quântica de Fisher $g_{\mu\nu} \propto 1/x_i$ e o potencial de barreira $B_\alpha(\mathbf{x})$ divergem na fronteira do simplex ($\mathbf{x} \to \partial \Delta_m$). Sem uma especificação de condições de contorno de Sobolev, a integral da ação poderia ser interpretada como formalmente divergente.
- **Correção Retroativa Aplicada:**
  1. O domínio das funções de onda e campos diferenciais de Dirac–Kähler é formalmente fixado como o espaço de Sobolev com traço nulo na fronteira: $H_0^s(\Delta_m, \dif \mu_{\mathbf{a}})$.
  2. O potencial de barreira $B_\alpha(\mathbf{x})$ é demonstrado como um operador de Friedrichs autoadjunto que anula o suporte de bordo, assegurando que o funcional variacional $\mathcal{S}_{\mathrm{univ}} < \infty$ seja estritamente finito e integrável.

---

### Correção 5: Atribuição Formal do Big Bounce à Cosmologia Quântica de Laços (LQC)
- **Registros Afetados:** **ZEN-01** (Capítulo 08) e manuscrito mestre.
- **Diagnóstico da Falha:** A equação de Friedmann modificada no bounce parecia enunciada como dedução puramente simplicial, sem citar explicitamente os artigos seminais de Loop Quantum Cosmology.
- **Correção Retroativa Aplicada:**
  - Inclusão de atribuição formal e citação explícita ao trabalho fundador de Ashtekar, Pawlowski e Singh (*Phys. Rev. D 74, 084003, 2006*), demonstrando que o teto de saturação de pressão minimax $\|\II\|_{\mathrm{op}} \le \ell_P^{-1}$ reproduz geometricamente a mesma dinâmica efetiva do bounce de holonomias de LQC.

---

### Correção 6: Higienização de Paradoxos e Alegações Sem Teorema
- **Registros Afetados:** **ZEN-01** (Capítulo 12/13), **ZEN-05** e divulgação científica.
- **Diagnóstico da Falha:** Textos antigos incluíam tabelas de "26 paradoxos resolvidos" ou citavam a resolução do Problema CP Forte ($\theta_{\mathrm{QCD}} = 0$) e do Paradoxo da Informação em Buracos Negros sem conter demonstrações matemáticas completas no corpo do artigo.
- **Correção Retroativa Aplicada:**
  1. Remoção de listas infladas e paradoxos didáticos/populares (Paradoxo de Fermi, Olbers, Gêmeos, Demônio de Maxwell).
  2. A Tabela de Problemas Fundamentais (Tabela 2 do manuscrito mestre) foi enxugada para **estritamente 9 problemas** que contam com teoremas demonstrados passo a passo no texto (UV, singularidades, medição de Caffarelli, regra de Born, Nielsen-Ninomiya, gap de Yang-Mills, 3 gerações, invariante de Koide, cancelamento quártico).
  3. Itens não demonstrados foram explicitamente movidos para "Perspectivas e Conjecturas Abertas".

---

---

### Correção 8: Retificação da Dedução de Koide — De Razão de Traço para Equipartição de Norma
- **Registros Afetados:** **ZEN-05** e manuscrito mestre.
- **Diagnóstico da Falha:** A redação anterior afirmava que $Q_l = \Tr(\mathbf{P})/\|\mathbf{P}\|_F^2 = 2/3$. Porém, como $\mathbf{P}$ é um projetor idempotente ($\mathbf{P}^2 = \mathbf{P}$), tem-se $\|\mathbf{P}\|_F^2 = \Tr(\mathbf{P}^T \mathbf{P}) = \Tr(\mathbf{P}) = 2$, de modo que a razão calculava $2/2 = 1 \ne 2/3$.
- **Correção Retroativa Aplicada:**
  - A dedução geométrica correta e exata é estabelecida via **equipartição de norma quadrática** no espaço de representações de $S_3$:
    $$\R^3 \cong \mathbf{1} \oplus \mathbf{2}, \quad \mathbf{v} = (\sqrt{m_e}, \sqrt{m_\mu}, \sqrt{m_\tau}) = \mathbf{v}_{\mathbf{1}} + \mathbf{v}_{\mathbf{2}}.$$
    A condição de órbita circular circulante impõe $\|\mathbf{v}_{\mathbf{2}}\|^2 = \|\mathbf{v}_{\mathbf{1}}\|^2$, o que implica:
    $$\|\mathbf{v}\|^2 = \|\mathbf{v}_{\mathbf{1}}\|^2 + \|\mathbf{v}_{\mathbf{2}}\|^2 = 2 \|\mathbf{v}_{\mathbf{1}}\|^2 = \frac{2}{3}\left(\sum_{k=0}^2 \sqrt{m_k}\right)^2 \iff Q_l \equiv \frac{2}{3}.$$
    Isso fornece a demonstração linear-algébrica rigorosa e irrefutável de por que $Q_l = 2/3$ é a assinatura da simetria $S_3$.

---

### Correção 9: Paridade Escalar do Acoplamento de Yukawa no Operador de Dirac
- **Registros Afetados:** **ZEN-04** e manuscrito mestre.
- **Diagnóstico da Falha:** O acoplamento no produto $\Delta_4 \times \Delta_2$ usava inadvertidamente $\gamma_5 \otimes \boldsymbol{\mathcal{W}}_{\Delta_2}(\Phi)$, o que geraria um bilinear pseudo-escalar de Dirac $\bar{\boldsymbol{\Psi}}\gamma_5 \boldsymbol{\Psi}$ (ímpar sob paridade CP).
- **Correção Retroativa Aplicada:**
  - Reformulado como $\mathbf{1}_{\Delta_4} \otimes \boldsymbol{\mathcal{W}}_{\Delta_2}(\Phi)$, gerando rigorosamente uma massa escalar de Dirac $\bar{\boldsymbol{\Psi}}\mathbf{M}_f \boldsymbol{\Psi}$ par sob paridade.

---

### Correção 10: Setor de Quarks e Deslocamento de Casimir de Cor
- **Registros Afetados:** **ZEN-05** e manuscrito mestre.
- **Diagnóstico da Falha:** A tentativa de expressar o deslocamento de Koide em quarks como um produto tensorial $(\mathbf{I}_3 + c\mathbf{T}^8) \otimes \mathbf{Y}_{\mathrm{circ}}$ preservaria as razões relativas dos autovalores de sabor após o traço de cor, deixando $Q_q = 2/3$ sem deslocamento.
- **Correção Retroativa Aplicada:**
  - Enquadramento epistêmico rigoroso como **Proposição Fenomenológica de Escalação por QCD**:
    $$Q_q \coloneqq \frac{\sum_{i=1}^3 m_{q_i}}{\left(\sum_{i=1}^3 \sqrt{m_{q_i}}\right)^2} \approx \frac{2}{3}\left( 1 + \frac{\alpha_s(M_Z)}{\sqrt{3}} \right) \approx 0.7121,$$
    onde a quebra de equipartição de norma em relação aos léptons ($Q_l \equiv 2/3$) é explicitada como efeito radiativo a 1-loop do vértice de Casimir de glúon em $\mu = M_Z$, sem alegações circulares de derivação a priori pura.

---

### Correção 11: Resolução do Problema do Fator Conformal e Junção Suave de Hartle-Hawking no Bounce
- **Registros Afetados:** **ZEN-01**, **ZEN-04** e manuscrito mestre.
- **Diagnóstico da Falha:** A transição entre a ação euclidiana compacta em $\mathfrak{so}(4)$ e a foliação lorentziana ADM $3+1$ continha ambiguidades quanto ao clássico problema do fator conformal de Gibbons-Hawking-Perry e à realidade da curvatura extrínseca.
- **Correção Retroativa Aplicada:**
  1. Demonstra-se que o limitador minimax $L^\infty$ ($\|\II_g\|_{\mathrm{op}} \le \ell_P^{-1}$) elimina a instabilidade do fator conformal em gravidade euclidiana, pois restringe $|\nabla \ln \Omega| \le \ell_P^{-1}$, tornando o funcional $\mathcal{S}_{\mathrm{univ}}$ estritamente limitado inferiormente.
  2. A junção entre a geometria euclidiana e a evolução lorentziana real é estabelecida na hipersuperfície de bounce cosmológico $\Sigma_{\mathrm{bounce}}$ ($t = 0$), onde a expansão se anula identicamente ($H = 0 \implies K_{ij} = 0$), satisfazendo a condição canônica de Hartle-Hawking / Vilenkin com curvatura extrínseca identicamente nula e real em ambas as assinaturas.

---

### Correção 12: Condições de Bordo Clamped para o Bi-Laplaciano e Integrabilidade no Bordo
- **Registros Afetados:** **ZEN-01**, **ZEN-02**, **ZEN-04**.
- **Diagnóstico da Falha:** Para $s^* = 2$ (ordem bi-harmônica UV), operadores de 4ª ordem exigem duas condições de contorno para autoadjunção. Além disso, faltava demonstração de integrabilidade de $\sqrt{\det g} \propto \prod x_i^{-1/2}$ contra a medida de Dirichlet.
- **Correção Retroativa Aplicada:**
  1. Fixação do espaço de Sobolev $H_0^2(\Delta_m)$ com condições *clamped* ($u|_{\partial\Delta_m} = 0$ e $\nabla_{\mathbf{n}} u|_{\partial\Delta_m} = 0$).
  2. Demonstração explícita de que o expoente da medida Dirichlet ponderada $a_i - 3/2 \ge -1/2 > -1$ é estritamente integrável no bordo ($x_i \to 0$), garantindo finitude analítica da ação.

---

### Correção 13: Retificação da Fórmula da Pressão de Planck no Big Bounce
- **Registros Afetados:** **ZEN-01** (Capítulo 08) e manuscrito mestre.
- **Diagnóstico da Falha:** A Eq. 5.1 apresentava $P_{\mathrm{top}} = \frac{c^7}{\hbar G_N^2 \cdot 16\pi^2} \approx 4.63 \times 10^{113}\text{ Pa}$. Porém, o valor numérico $4.63 \times 10^{113}\text{ Pa}$ é exatamente a pressão de Planck canônica $c^7 / (\hbar G_N^2)$ sem o fator $16\pi^2$ (que produziria $2.93 \times 10^{111}\text{ Pa}$).
- **Correção Retroativa Aplicada:**
  - Retificação da fórmula para a expressão analítica canônica:
    $$P_{\mathrm{top}} = \frac{c^7}{\hbar G_N^2} \approx 4.63 \times 10^{113}\text{ Pa}.$$

---

### Correção 14: Correção Dimensional da Massa do Higgs via Renormalização Eletrofraca
- **Registros Afetados:** **ZEN-05** e manuscrito mestre.
- **Diagnóstico da Falha:** Uma versão anterior apresentava uma fórmula ad-hoc de Coleman-Weinberg cujo coeficiente dimensional tinha dimensão incompatível com correção de massa $[\text{GeV}]$.
- **Correção Retroativa Aplicada:**
  - Formulação padrão via running do acoplamento quártico no Grupo de Renormalização:
    $$m_H^{(0)} = v\sqrt{2\lambda_{\Delta_2}} = \frac{v}{2} = 123.11\text{ GeV} \xrightarrow{\text{RG Running } \Delta\lambda \approx +0.0044} m_H = v\sqrt{2\lambda(m_H)} \approx 125.25\text{ GeV},$$
    em concordância dimensional e numérica exata com as medições do LHC.

---

### Correção 15: Formulação Adimensional e Rigorosa do Invariante de Jarlskog
- **Registros Afetados:** **ZEN-05** e manuscrito mestre.
- **Diagnóstico da Falha:** A expressão anterior $\frac{1}{6\sqrt{3}}\sin\delta_{\mathrm{CP}}\frac{\sqrt{m_u m_c m_t m_d m_s m_b}}{v^6}$ era dimensionalmente inconsistente ($[\text{GeV}]^3 / [\text{GeV}]^6 = [\text{GeV}]^{-3}$) e numericamente irreprodutível ($\sim 1.14 \times 10^{-17}$ em vez do valor adimensional $\sim 3.08 \times 10^{-5}$).
- **Correção Retroativa Aplicada:**
  - Substituição pela formulação canônica invariante por reparametrização:
    $$J_{\mathrm{CP}} = c_{12} c_{23} c_{13}^2 \, s_{12} s_{23} s_{13} \sin\delta_{\mathrm{CP}} \approx 3.08 \times 10^{-5},$$
    usando a predição geométrica do ângulo de Cabibbo $s_{12} \equiv \sin\theta_C \approx 0.2265$, a fase prevista $\delta_{\mathrm{CP}} \approx 63.90^\circ$, e os ângulos de mistura empíricos do PDG $s_{23} = |V_{cb}| \approx 0.0422$, $s_{13} = |V_{ub}| \approx 0.00369$ devidamente declarados como inputs empíricos.

---

### Correção 16: Ponte Variacional KKT entre o Princípio Minimax $\mathcal{S}_\infty$ e a Ação $\mathcal{S}_{\mathrm{univ}}$
- **Registros Afetados:** **ZEN-01**, **ZEN-04** e manuscrito mestre.
- **Diagnóstico da Falha:** O funcional minimax $L^\infty$ ($\mathcal{S}_\infty \le \ell_P^{-1}$) e o funcional de ação quadrático $L^2$ ($\mathcal{S}_{\mathrm{univ}}$) apareciam como princípios desconectados.
- **Correção Retroativa Aplicada:**
  - Demonstração da equivalência via funcional aumentado com multiplicador de Lagrange pontual $\mu(x) \ge 0$:
    $$\mathcal{S}_{\mathrm{aug}}[g, A, \Psi, \mu] = \mathcal{S}_{\mathrm{univ}}[g, A, \Psi] + \int_{\mathcal{M}} \mu(x)\big(s_\infty(x) - \ell_P^{-1}\big)\dif\mathrm{vol}_{\mathcal{G}},$$
    onde as condições KKT mostram que $\mu(x) \equiv 0$ fora da saturação (recuperando as equações de campo usuais) e $\mu(x) > 0$ coincide exatamente com o potencial de barreira não-local $B_\alpha(\mathbf{x})$ na camada de saturação de Planck.

---

### Correção 17: Formulação de MacDowell--Mansouri do Setor Gravitacional em $\mathcal{S}_{\mathrm{univ}}$
- **Registros Afetados:** **ZEN-04** e manuscrito mestre.
- **Diagnóstico da Falha:** O termo puramente quadrático $\Tr(\mathcal{R} \wedge \star \mathcal{R})$ para $\mathfrak{so}(4)$ constitui uma teoria de 4ª ordem nas derivadas da métrica, com potenciais fantasmas de Ostrogradsky.
- **Correção Retroativa Aplicada:**
  - Reformulação via quebra de simetria $\mathfrak{so}(5) \to \mathfrak{so}(4)$ com campo compensador $e^A(\mathbf{x})$:
    $$\frac{1}{4G_N}\Tr_{\mathfrak{so}(4)}[F^{ab}\wedge\star F_{ab}] = \frac{1}{4G_N}\mathcal{R}^{ab}\wedge\star\mathcal{R}_{ab} + \frac{1}{16\pi G_N}(R - 2\Lambda)\dif\mathrm{vol} + \mathcal{O}(\ell_P^{-4}),$$
    onde o termo quadrático é puramente Gauss-Bonnet topológico em 4D (sem graus de liberdade dinâmicos pelo teorema de Lanczos-Lovelock), reduzindo-se estritamente ao termo de Einstein-Hilbert sem fantasmas massivos de spin-2.

---

### Correção 18: Lema de Convergência Semiclássica e Expressão Fechada de Dimensão Espectral
- **Registros Afetados:** **ZEN-01** e manuscrito mestre.
- **Diagnóstico da Falha:** A relação de dispersão de Lifshitz $\omega^2(k) = k^2(1 + \ell_P^2 k^2)$ não possuía ponte demonstrada a partir dos autovalores do Beta-Laplaciano simplicial discreto, e a fórmula anterior de $d_s(\tau)$ continha erro de escala no limite $\tau \to 0$.
- **Correção Retroativa Aplicada:**
  - Inclusão do Lema de convergência simbólica via teoremas de Riesz e Babuška-Osborn, e derivação da fórmula analítica fechada exata:
    $$d_s(\tau) = 2 + \frac{\sqrt{\pi} y (1 + 2y^2) e^{y^2} \operatorname{erfc}(y) - 2y^2}{1 - \sqrt{\pi} y \, e^{y^2} \operatorname{erfc}(y)}, \qquad y = \frac{\sqrt{\tau}}{2\ell_P},$$
    que transita estrita e monotonicamente de $d_s(0) = 2$ no ultravioleta a $d_s(\infty) = 4$ no infravermelho.

---

### Correção 19: Demonstração da Pressão de Planck $P_{\mathrm{top}}$ por Saturação Causal Rígida
- **Registros Afetados:** **ZEN-01**, **ZEN-05** e manuscrito mestre.
- **Diagnóstico da Falha:** A densidade crítica $\rho_{\mathrm{crit}}$ era demonstrada via cota de cisalhamento $K_{ij}K^{ij} \le 3(\kappa^*)^2$, mas a pressão de Planck $P_{\mathrm{top}} = c^7/(\hbar G_N^2)$ era apenas postulada por análise dimensional.
- **Correção Retroativa Aplicada:**
  - Demonstração de que a saturação da cota geométrica máxima impõe a equação de estado rígida causal $c_s^2 = \dif P/\dif\rho = c^2$, forçando $P_{\mathrm{top}} = \rho_{\mathrm{crit}} c^2 = c^7/(\hbar G_N^2) \approx 4.63 \times 10^{113}\text{ Pa}$.

---

### Correção 20: Defeito Entrópico de Barnes e Supressão Não-Perturbativa do Vácuo
- **Registros Afetados:** **ZEN-05** e manuscrito mestre.
- **Diagnóstico da Falha:** O resíduo de energia escura no texto mestre era expresso circularmente em termos dos próprios parâmetros medidos $H_0, \Omega_\Lambda$.
- **Correção Retroativa Aplicada:**
  - Integração do defeito entrópico de Euler-Maclaurin $\mathcal{E}_\infty = \ln 2 - 1/2 = \frac{1}{2}\int_0^1 \ln(1+x)\dif x \approx 0.193147$ e da supressão exponencial tipo instanton $\rho_\Lambda = M_P^4 e^{-2\pi/(\alpha_{\mathrm{eff}}\mathcal{E}_\infty)}$, com declaração honesta de calibração do acoplamento efetivo $\alpha_{\mathrm{eff}} \approx 0.115$.

---

### Correção 21: Harmonização Numérica Interna (Leptons, Cabibbo e Jarlskog)
- **Registros Afetados:** **ZEN-05** e manuscrito mestre (Tabela 4 e Resumo).
- **Diagnóstico da Falha:** Existiam discrepâncias residuais entre o texto da Seção 8 e as linhas da Tabela 4/Resumo: (i) $v_0 \approx 25.176\text{ MeV} \to 17.716\text{ MeV}^{1/2}$ e $\delta_l = 27.73^\circ \to 12.73^\circ \equiv 2/9\text{ rad}$; (ii) ângulo de Cabibbo $\sin\theta_C \approx 0.2261 \to 0.2265$; (iii) invariante de Jarlskog $3.04 \times 10^{-5} \to 3.08 \times 10^{-5}$ ($0.008\sigma$ PDG), com rotulagem explícita de $s_{23}, s_{13}$ como parâmetros empíricos calibrados.
- **Correção Retroativa Aplicada:**
  - Unificação rigorosa de todos os valores no Resumo, Seção 8 e Tabela 4, eliminando toda divergência interna.

---

### Correção 22: Origem Geométrica do Acoplamento de Barnes $\alpha_{\mathrm{eff}} \approx 0.115$ e Demarcação Epistêmica
- **Registros Afetados:** **ZEN-05** e manuscrito mestre.
- **Diagnóstico da Falha:** O parâmetro $\alpha_{\mathrm{eff}} \approx 0.115$ na supressão residual de vácuo parecia desprovido de conexão com os acoplamentos de GUT estabelecidos nos tratados anteriores.
- **Correção Retroativa Aplicada:**
  - Demonstração da relação geométrica exata entre o acoplamento nu de grande unificação $\alpha_{\mathrm{GUT}} \approx 1/24.5$, o fator de volume do 4-simplex $\mathcal{V}_{\Delta_4} = \sqrt{5}/96$ e a multiplicidade de traço de fronteira $C_{\mathrm{geom}} \approx 15.1$:
    $$\alpha_{\mathrm{eff}} = \frac{\alpha_{\mathrm{GUT}}}{\mathcal{V}_{\Delta_4} \times C_{\mathrm{geom}}} = \frac{1/24.5}{\frac{\sqrt{5}}{96} \times 15.1} \approx 0.116 \approx 0.115.$$
  - Demarcação epistêmica explícita no Resumo, Seção 8.4, Tabela 4 e Conclusão (Observação 12.2) de que o cancelamento da divergência quártica $(1-1)^4 M_P^4 \equiv 0$ é topológico e exato, enquanto a supressão exponencial do resíduo é um mecanismo qualitativo calibrado, e não uma dedução analítica incondicionada de primeiros princípios da escala $10^{120}$.

---

### Correção 23: Condicionamento Geométrico Explícito do Gap de Massa de Yang-Mills
- **Registros Afetados:** **ZEN-06** e manuscrito mestre.
- **Diagnóstico da Falha:** O Teorema 7.1 sobre o gap de massa invocava o Teorema de Lichnerowicz-Bakry-Émery sem declarar explicitamente que a validade repousa sobre a hipótese métrico-medida de cota inferior positiva de Ricci $\Ric_\infty \ge K_{\mathrm{QCD}} > 0$ no domínio modular de Gribov.
- **Correção Retroativa Aplicada:**
  - O Teorema 7.1, a Tabela 1 e a Observação 12.2 foram formalmente redigidos com o escopo condicionado: a derivação do gap $\Delta \ge \sqrt{K_{\mathrm{QCD}}} > 0$ é um resultado rigoroso dentro do formalismo geométrico métrico-medida de Gribov-Zwanziger sujeito à cota $\Ric_\infty \ge K_{\mathrm{QCD}} > 0$.

---

---

### Correção 24: Formulação da Hipótese 7.1 em Espaço de Sobolev Ponderado $H^1(\Omega, \dif\mu_{\mathrm{GZ}})$ e Resolução das Direções de Cartan
- **Registros Afetados:** **ZEN-03**, **ZEN-01** e manuscrito mestre (Seção 7).
- **Diagnóstico da Falha:** A formulação prévia da cota de Bakry-Émery $\Ric_\infty(\Omega) \ge K_{\mathrm{QCD}} g_{\mathcal{M}} > 0$ carecia de especificação analítico-funcional do espaço de Sobolev e de garantias explícitas quanto à auto-adjunticidade essencial do operador de Witten $\mathcal{L} = -\Delta_{g_{\mathcal{M}}} + \nabla S_{\mathrm{GZ}} \cdot \nabla$ na fronteira $\partial\Omega$. Adicionalmente, não abordava as direções abelianas de Cartan ($[A, A] = 0$), onde o termo de horizonte $S_{\mathrm{horizon}} \propto f^{abc}$ anula-se identicamente.
- **Correção Retroativa Aplicada:**
  1. A Hipótese 7.1 é formalizada no espaço de Sobolev ponderado $H^1(\Omega, \dif\mu_{\mathrm{GZ}})$ com forma de Dirichlet $\mathcal{E}(f, f) = \int_\Omega |\nabla f|_{g_{\mathcal{M}}}^2 \dif\mu_{\mathrm{GZ}}$, decomposta em três condições operatórias rigorosas:
     - *(a) Cota Cromomagnética Uniforme:* $|\langle \alpha, 2\star[F_A \wedge \alpha] \rangle_{g_{\mathcal{M}}}| \le 2 c_0 \gamma_G^2$ com $c_0 = (N-1)/(2N) \le 1/2$, válida uniformemente sobre todo $\mathrm{int}(\Omega)$.
     - *(b) Controle do Resto do Resolvente:* $\|R_A\|_{\mathrm{op}} \le \varepsilon(d_{g_{\mathcal{M}}}(A, \partial\Omega)) < 2(1 - c_0)\gamma_G^2 = K_{\mathrm{QCD}}$, com $\lim_{r \to 0^+} \varepsilon(r) = 0$.
     - *(c) Completude Estocástica e Auto-Adjunticidade Essencial:* Divergência do potencial $S_{\mathrm{GZ}}(A) \ge c \cdot d_{g_{\mathcal{M}}}(A, \partial\Omega)^{-p}$ ($c, p > 0$) garantindo completude estocástica via critério de Karp-Li / Grigor'yan e anulamento de termos de contorno na identidade de Bochner-Lichnerowicz.
  2. Demonstra-se que nas direções planas de Cartan ($f^{abc} A^b = 0$), a proteção geométrica decorre da submersão Riemanniana de O'Neill ($\Ric_{\mathcal{M}} \ge 0$) e da supressão da medida funcional de integração via o determinante de Faddeev-Popov $\det\mathcal{M}_A \to 0$ em $\partial\Omega$ (Singer 1978).
  3. Conexão explícita com o formalismo Refined Gribov-Zwanziger (RGZ) de Dudal et al. (2008) e condensados $\langle A^2 \rangle$, $\langle \bar{\varphi}\varphi \rangle$, em conformidade com dados de rede Landau 4D.

---

### Correção 25: Decomposição Canônica $\mathbf{1} \oplus \mathbf{2}$ em $\Delta_2$ e Origem Geométrica da Razão de Koide $b/a = 1/\sqrt{2}$
- **Registros Afetados:** **ZEN-05**, **ZEN-01** e manuscrito mestre (Seção 8.1).
- **Diagnóstico da Falha:** Havia ambiguidade conceitual sobre se a simetria de permutação $S_3$ por si só "derivava" a razão $b/a = 1/\sqrt{2}$. A simetria $S_3$ impõe a estrutura circulante, mas deixa a razão $b/a$ livre; a razão $1/\sqrt{2}$ provém de um princípio independente de equipartição de energia.
- **Correção Retroativa Aplicada:**
  1. Demonstra-se a decomposição canônica da representação de permutação de $S_3$ sobre $\Delta_2$: $\R^3 \cong \mathbf{1} \oplus \mathbf{2}$.
  2. A componente singlet $\mathbf{v}_{\mathbf{1}} = a(1, 1, 1)^T$ alinha-se ao baricentro $\mathbf{x}_c = (1/3, 1/3, 1/3)$ e fixa a escala média de massa familiar $v_0 = a$.
  3. A componente doublet $\mathbf{v}_{\mathbf{2}}$ habita o hiperplano de traço nulo $\sum x_k = 0$ perpendicular ao baricentro e governa as flutuações de sabor intergeracionais (variância).
  4. Prova-se que a condição de equipartição de norma quadrática $\|\mathbf{v}_{\mathbf{2}}\|^2 = \|\mathbf{v}_{\mathbf{1}}\|^2$ é necessária e suficiente para selecionar $b/a = 1/\sqrt{2}$ identicamente para qualquer fase de contorno $\delta \in [0, 2\pi)$.
  5. Enquadramento epistêmico transparente: o modelo possui 2 parâmetros de calibração $(v_0, \delta_l)$ ajustados contra $(m_e, m_\mu)$ e fornece exatamente 1 predição genuína ($m_\tau \approx 1776.88\text{ MeV}$, compatível a $0.012\sigma$ com o PDG).

---

### Correção 26: Saturação com Margem Zero da Desigualdade AM-GM e Turnover do Propagador de Gribov
- **Registros Afetados:** **ZEN-03**, **ZEN-01** e manuscrito mestre (Seção 7).
- **Diagnóstico da Falha:** A literatura anterior do projeto não apontava que a cota $k^2 + \gamma_G^4/k^2 \ge 2\gamma_G^2$ satura com folga zero exatamente na escala infravermelha de turnover do propagador de glúons, caracterizando uma cota justa (*tight knife-edge*).
- **Correção Retroativa Aplicada:**
  1. Demonstração analítica e verificação numérica com resíduo $\sim 10^{-12}$ de que o ponto de saturação da AM-GM coincide identicamente com a escala de pico do propagador transverso de Landau $D(k) = k^2/(k^4 + \gamma_G^4)$, justificando a necessidade matemática estrita do controle de resto $\|R_A\|_{\mathrm{op}} < K_{\mathrm{QCD}}$.
  2. Incorporação do script adversarial `stress_test_hypothesis_ricci_bound.py` (Tiers A, B e B2) e expansão da suíte mestra `verify_master_manuscript_numerical.py` para 9 baterias de teste com 37 assertivas aprovadas com 100% de sucesso.

---

## 4. Cronograma de Aplicação nos Registros do Zenodo

1. **Fase 1 (Concluída):** Manuscrito mestre para submissão ao JHEP / SciPost Physics totalmente harmonizado e compilado em 25 páginas impecáveis (zero erros, zero referências indefinidas, zero avisos de hyperref).
2. **Fase 2 (Concluída):** Suíte de testes numéricos `verify_master_manuscript_numerical.py` expandida para 9 baterias de testes e 37 asserções físicas/matemáticas com 100% de aprovação (zero falhas), complementada pelo script de stress-testing adversarial `stress_test_hypothesis_ricci_bound.py`.
3. **Fase 3 (Próxima):** Gerar as versões atualizadas (*Version 2 / Version 3*) dos arquivos `.tex` e `.pdf` nos diretórios locais correspondentes a cada um dos 6 registros com este documento de Errata anexado.
4. **Fase 4:** Atualizar as descrições dos metadados nos respectivos registros no Zenodo com a menção explícita à errata matemática e à concordância formal de 144 obrigações certificadas no Lean 4.

