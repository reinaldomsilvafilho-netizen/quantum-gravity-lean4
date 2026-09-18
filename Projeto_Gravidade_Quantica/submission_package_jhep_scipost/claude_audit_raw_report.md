# Auditoria Adversarial — "Simplicial Quantum Gravity on Δ₄ × Δ₂"

**Crítica meta-metodológica prévia (aplica-se a todo o manuscrito):** a alegação recorrente de "141 teoremas certificados em Lean 4, 0 sorry" é usada ao longo do texto como se fosse evidência de correção *física*. Isso é um erro de categoria. Um assistente de provas verifica apenas que as conclusões seguem logicamente das definições e axiomas *formalizados* — não que essas definições correspondam à física real. Se o axioma "Simplicial Beta-Laplacian" ou o "bound $\|\mathrm{I\!I}\|_{L^\infty}\le \ell_P^{-1}$" já embutem a conclusão desejada (o que ocorre repetidamente abaixo), a verificação mecânica apenas confirma uma tautologia bem formatada. Nenhum árbitro do JHEP/SciPost aceitará "Lean 4 (141/141)" como argumento de rigor físico — isso deve ser removido do corpo científico e relegado, no máximo, a um apêndice de reprodutibilidade.

---

## 1. Auditoria de Rigor por Teorema

**Teor. 2.1 (Evasão de Nielsen–Ninomiya).** A contagem $\dim\Omega^*(\Delta_4)=16=2^4\to 4$ espinores de Dirac é álgebra padrão de Kähler-Dirac (correta). Mas o passo crítico — "as condições de reflexão de fronteira... eliminam três cópias não físicas... restando um único espinor físico por simplexo" — não tem prova; é uma afirmação. Pior: isso contradiz a Seção 1.2, onde $N_g=3$ vem de uma origem *completamente diferente* (irreps de $S_3$ sobre $\Delta_2$). O texto usa "$N_g=3$" duas vezes com duas derivações mutuamente incompatíveis (uma via redução de dobra fermiônica em $\Delta_4$, outra via simetria de sabor em $\Delta_2$) e nunca reconcilia as duas. Isso é uma inconsistência lógica fatal, não um detalhe.
Além disso, a premissa de não-localidade do teorema de Nielsen–Ninomiya original é sobre *operadores locais*; operadores fracionários genuinamente evitam o teorema (isso é conhecido, cf. fermions SLAC/não-locais), mas isso não implica automaticamente ausência de duplicação — é necessário mostrar que o espectro de $(-\Delta_{\Delta_4})^\alpha$ não tem zeros espúrios na zona de Brillouin efetiva. Isso nunca é calculado.

**Teor. 3.2 (fluxo $d_s: 2\to 4$).** A álgebra da integral de calor está correta dado a relação de dispersão de Lifshitz $\omega^2=k^2(1+\ell_P^2k^2)$ (que é *postulada*, não derivada da ação simplicial). O Corolário sobre renormalizabilidade UV ("o propagador escala como $1/k^4$... portanto estritamente renormalizável") é uma non-sequitur: dimensão espectral $d_s\to 2$ no UV é *necessária* mas não *suficiente* para renormalizabilidade (cf. debate Lauscher–Reuter vs. Hořava-Lifshitz sobre unitariedade e ghosts de ordem superior) — o próprio abstract afirma "sem ghosts de Ostrogradsky" sem prova alguma disso no corpo do texto.

**Teor. 4.2 (folheações minimax).** A álgebra de autovalores está correta (é apenas $\sum\lambda_i^2\le 3(\kappa^*)^2$). Mas a conclusão (iii) — "completude geodésica, eliminando singularidades de crushing" — **não segue** da hipótese. Curvatura extrínseca limitada em $L^\infty$ não implica completude geodésica sem hipóteses adicionais (controle do lapso $N$, do shift, e da métrica espacial $\gamma_{ij}$ ao longo do fluxo). A referência de apoio é o próprio "treatise" do autor no Zenodo — citação circular não revisada por pares.

**Teor. 5.1 (Big Bounce $C^{1,1}$).** A equação de Friedmann modificada $H^2=\frac{8\pi G}{3}\rho(1-\rho/\rho_{\rm crit})$ é **exatamente** a equação efetiva da Cosmologia Quântica de Laços (LQC, Ashtekar–Pawlowski–Singh, *Phys. Rev. Lett.* 96 (2006) 141301) — ela não é derivada de $\Delta_4\times\Delta_2$ em lugar nenhum do texto; é inserida por mão e apresentada como consequência do formalismo minimax. Isso precisa de atribuição explícita ou de uma derivação genuína a partir de \eqref{eq:minimax_bound_def}; caso contrário, um árbitro identificará isso imediatamente como resultado importado sem crédito.

**Teor. 6.1/6.2 (Caffarelli & regra de Born).** Este é o ponto mais frágil do artigo. O "fluxo gradiente de contato dissipativo" nunca é definido (nenhuma equação de movimento, nenhum gerador, nenhuma prova de que preserva a medida de Fubini–Study). A igualdade central $\mathrm{Vol}_\omega(\mathcal B_n)/\sum_k \mathrm{Vol}_\omega(\mathcal B_k) = |c_n|^2$ é **assumida**, não provada — a "prova" apenas redefine $\mathcal B_n$ como a célula de Voronoi $\{|c_n|>|c_k|\}$ e declara a integral igual a $|c_n|^2$ sem cálculo. Isso não é verdade em geral para células de Voronoi em $\mathbb{C}P^N$ com a métrica de Fubini–Study (a medida de uma célula de Voronoi *não* é, em geral, exatamente a norma ao quadrado da coordenada correspondente, exceto em casos triviais de simetria). É a afirmação mais extraordinária do artigo ("resolve o problema da medição") sustentada pela prova mais fraca.

**Teor. 7.1 (gap de massa de Yang–Mills).** A prova textualmente diz "*Veja o tratado especializado do autor*" — ou seja, **não há prova neste artigo**, apenas remissão a outro documento não revisado por pares no Zenodo. Isso é inaceitável como "Teorema" num artigo submetido ao JHEP: o problema do milênio de Clay não pode ser citado como resolvido via referência cruzada a autopublicação. Mesmo no tratado citado, a cadeia lógica (positividade de Bakry–Émery $\Rightarrow$ gap espectral euclidiano $\Rightarrow$ gap físico relativístico via "teorema de reconstrução de Nelson") pula etapas essenciais: positividade de reflexão, existência do limite de continuum, e a reconstrução de Osterwalder–Schrader completa — nenhuma delas é estabelecida.

**Teor. 8.1 (relação de Koide).** Esta é uma tautologia disfarçada de teorema. A parametrização $\mathbf v = v_0(1+\sqrt2\cos(\delta+2\pi k/3))$ **já é** a parametrização original de Koide (1983) que *por construção* satisfaz $Q_l=2/3$ para qualquer $\delta$ — isso é conhecido há décadas e não decorre de teoria de representação de $S_3$ sobre $\Delta_2$; decorre de as três massas caírem sobre uma órbita circular específica, o que é uma hipótese adicional não fisicamente justificada (por que a natureza escolheria essa órbita?). Apresentar isso como "Teorema" derivado do projetor $\mathbf P$ obscurece que $Q_l=2/3$ é uma identidade algébrica de $\mathbf P$, não uma previsão sobre massas físicas — o ajuste fino real está escondido no ângulo $\delta$, que não é derivado, apenas ajustado a posteriori.

**Teor. 8.2 (cancelamento da constante cosmológica).** Aqui há um erro de categoria grave: $\partial\partial=0$ é uma identidade sobre o operador de bordo do complexo de cadeias simpliciais (topologia combinatória); $\rho_{\rm vac}^{(4)}=(1-1)^4M_P^4$ conecta isso a uma integral analítica divergente de energia de ponto zero sem nenhuma ponte matemática real — não há regularização, nem espectro de operador, nem soma de Casimir de fato calculada. A notação "$(1-1)^4$" não é uma dedução, é uma mnemônica. Pior: $\Lambda_{\rm residual}$ é definido **usando os valores observados** $H_0,\Omega_\Lambda$ — logo "coincidir com o valor cosmológico sem ajuste fino" é circular (o resultado foi definido para ser igual à observação), não uma previsão.

---

## 2. O Que Adicionar para Fortalecer

- **Seção de vínculos hamiltonianos completa**: os vínculos de momento $\mathcal H_i=0$ nunca aparecem — só $\mathcal H=0$. Sem o vínculo de difeomorfismo espacial e sem discutir a álgebra de vínculos $\{\mathcal H,\mathcal H\}$, $\{\mathcal H,\mathcal H_i\}$ (Dirac–Teitelboim), a alegação de "propagação hiperbólica de vínculos ADM" do CLAUDE.md do projeto não é sustentada no texto.
- **Definição explícita e prova de boa-definição de $(-\Delta_{\Delta_m})^\alpha$**: domínio de definição, espaço de Sobolev fracionário apropriado ($H^\alpha(\Delta_m,\mu_{\mathbf a})$), auto-adjunção, espectro discreto vs. contínuo.
- **Derivação explícita da ação $\mathcal S_\infty$ a partir de primeiros princípios** (por que minimax $L^\infty$ ao invés de $L^2$? Qual princípio variacional gera as equações de movimento reportadas? Não há cálculo de variação de $\mathcal S_\infty$ em lugar nenhum).
- **Prova completa e independente** (não citação circular) do gap de massa de Yang–Mills, incluindo positividade de reflexão e existência de limite de continuum — ou reformular a afirmação como conjectura.
- **Cálculo explícito** da medida de Voronoi em $\mathbb{C}P^N$ sob Fubini–Study, com prova rigorosa de $\mathrm{Vol}(\mathcal B_n)=|c_n|^2\mathrm{Vol}(\mathbb{C}P^N)$, ou abandonar a alegação de "derivação determinística da regra de Born".
- **Seção de calibre**: nenhuma discussão de invariância de calibre residual, fantasmas de Faddeev–Popov explícitos, ou o papel do parâmetro $\gamma_G$ (massa de Gribov) como função do acoplamento renormalizado.
- **Distinção explícita $t$ vs. $\lambda$** (fluxo vs. parâmetro afim) exigida pelo protocolo interno do projeto — ausente em todo o artigo; o fluxo de Ricci de grafton e o tempo cosmológico são misturados sem aviso.
- **Análise de erros/incertezas** nas previsões numéricas (Cabibbo, $v=246.22$ GeV, $P_{\rm top}$) — nenhuma propagação de incerteza é mostrada.
- **Seção de limitações e testes de falseabilidade mais duros**: o artigo deveria declarar explicitamente que resultado experimental *refutaria* o framework (atualmente as previsões em 13 são vagas: "$\delta\Phi\le10^{-19}$ rad" sem cronograma de sensibilidade real dos detectores citados).

---

## 3. Expansão Bibliográfica (as ~20 referências atuais são insuficientes para um artigo de síntese)

> Nota: dou aqui referências de landmark papers pelo melhor do meu conhecimento; o autor **deve verificar DOI/ano exatos** antes de submissão — não devo inventar identificadores que não tenho certeza.

**Triangulações Dinâmicas / QG discreta:**
- T. Regge, *General Relativity without coordinates*, Nuovo Cimento 19 (1961) 558.
- J. Ambjørn, J. Jurkiewicz, R. Loll, *Dynamically Triangulating Lorentzian Quantum Gravity*, Nucl. Phys. B610 (2001) 347, arXiv:hep-th/0105267.
- J. Ambjørn, A. Görlich, J. Jurkiewicz, R. Loll, *Nonperturbative Quantum Gravity*, Phys. Rept. 519 (2012) 127, arXiv:1203.3591.
- H. W. Hamber, *Quantum Gravitation: The Feynman Path Integral Approach*, Springer, 2009.
- D. Oriti (ed.), *Approaches to Quantum Gravity*, Cambridge University Press, 2009.
- L. Freidel, *Group Field Theory: An Overview*, Int. J. Theor. Phys. 44 (2005) 1769, arXiv:hep-th/0505016.

**Obstáculo / Regularidade de Caffarelli:**
- D. Kinderlehrer, G. Stampacchia, *An Introduction to Variational Inequalities and Their Applications*, Academic Press, 1980.
- L. C. Evans, *Partial Differential Equations*, AMS Grad. Studies in Math., 1998.
- H. Federer, *Curvature measures*, Trans. AMS 93 (1959) 418.
- L. A. Caffarelli, S. Salsa, *A Geometric Approach to Free Boundary Problems*, AMS, 2005.

**Gribov–Zwanziger / Confinamento:**
- L. D. Faddeev, V. N. Popov, *Feynman diagrams for the Yang-Mills field*, Phys. Lett. B25 (1967) 29.
- G. K. Savvidy, *Infrared Instability of the Vacuum State of Gauge Theories*, Phys. Lett. B71 (1977) 133.
- G. 't Hooft, *On the Phase Transition Towards Permanent Quark Confinement*, Nucl. Phys. B138 (1978) 1.
- K. G. Wilson, *Confinement of Quarks*, Phys. Rev. D10 (1974) 2445.
- A. M. Polyakov, *Compact Gauge Fields and the Infrared Catastrophe*, Phys. Lett. B59 (1975) 82.
- N. Vandersickel, D. Zwanziger, *The Gribov problem and QCD dynamics*, Phys. Rept. 520 (2012) 175, arXiv:1202.1491.

**Dirac–Kähler / Fermions em retículo:**
- E. Kähler, *Der innere Differentialkalkül*, Rend. Mat. 21 (1962) 425.
- T. Becher, H. Joos, *The Dirac-Kähler Equation and Fermions on the Lattice*, Z. Phys. C15 (1982) 343.
- J. M. Rabin, *Homology Theory of Lattice Fermion Doubling*, Nucl. Phys. B201 (1982) 315.
- T. Banks, Y. Dothan, D. Horn, *Geometric Fermions*, Phys. Lett. B117 (1982) 413.

**Koide / Física de Sabor:**
- R. Foot, *A note on Koide's lepton mass relation*, arXiv:hep-ph/9402242.
- H. Harari, H. Haut, J. Weyers, *Charge patterns and mass relations for quarks and leptons*, Phys. Lett. B78 (1978) 459.
(Confirme separadamente as referências específicas de Rodejohann e Xing sobre relações de Koide — não tenho certeza suficiente de título/ano para citá-las sem verificação.)

**Holografia / Redes de Tensores:**
- V. E. Hubeny, M. Rangamani, T. Takayanagi, *A Covariant Holographic Entanglement Entropy Proposal*, JHEP 0707 (2007) 062, arXiv:0705.0016.
- M. Van Raamsdonk, *Building up spacetime with quantum entanglement*, Gen. Rel. Grav. 42 (2010) 2323, arXiv:1005.3035.
- B. Swingle, *Entanglement Renormalization and Holography*, Phys. Rev. D86 (2012) 065007, arXiv:0905.1317.
- F. Verstraete, J. I. Cirac, *Renormalization algorithms for Quantum-Many Body Systems*, arXiv:cond-mat/0407066.

**Provas Formais/Verificação Mecânica:**
- J. Avigad, *The mechanization of mathematics*, Notices AMS 65 (2018).
- T. Hales et al., *A formal proof of the Kepler conjecture*, Forum of Mathematics, Pi (2017), arXiv:1501.02155.
- G. Gonthier, *Formal Proof—The Four-Color Theorem*, Notices AMS 55 (2008) 1382.

---

## 4. Veredito Editorial

Nenhuma das duas opções apresentadas ("Aprovado com refinamentos" / "Revisão menor") reflete honestamente o estado do manuscrito. Meu parecer como revisor adversarial:

**REJEIÇÃO / NECESSITA REFORMULAÇÃO SUBSTANCIAL (Major Revision, na fronteira de Reject-and-Resubmit).**

Razões que impedem "revisão menor":
1. Duas derivações incompatíveis de $N_g=3$ nunca reconciliadas (erro lógico, não estético).
2. O "Teorema" central de Yang–Mills não contém prova — apenas remissão a autopublicação não revisada por pares.
3. A "derivação determinística da regra de Born" carece de prova matemática real onde mais precisa (a igualdade-chave é postulada).
4. O cancelamento da constante cosmológica confunde topologia combinatória com regularização analítica (erro de categoria) e é circular na comparação numérica.
5. Uso retórico de "141 teoremas Lean 4, 0 sorry" como se fosse evidência de correção física, ao longo de todo o texto — isso será identificado por qualquer árbitro de física teórica como propaganda metodológica, não rigor.
6. Tabelas 9–10 têm tom promocional incompatível com o padrão de um artigo científico (comparações auto-favoráveis com String Theory, LQG etc. usando métricas informais como "Testabilidade: Inalcançável" vs. "2026–2035" para o próprio trabalho).

Antes de resubmissão, cada teorema listado na Seção 1 precisa de prova completa e autocontida (não citações cruzadas a Zenodo), e as alegações de "resolver" 12 problemas fundamentais da física devem ser substancialmente moderadas ou removidas.
