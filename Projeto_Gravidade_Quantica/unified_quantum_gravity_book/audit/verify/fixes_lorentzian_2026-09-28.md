# Fix log: Lorentzian completion subsection in Chapter 12 (2026-09-28)

Corrector/writer pass (four-eyes: this writer did not author or verify the underlying research note).
Source material used: `Projeto_Gravidade_Quantica/Pesquisa_e_Testes/completamento_lorentziano/README.md`,
`refs.md`, and `VERIFICACAO.md` (31 CONFIRMA, 2 REFUTA, 4 INCERTO). Only CONFIRMA content was asserted;
the two REFUTA items (Lee--Wick "excluded", Pais--Uhlenbeck $\omega_1=0$ premise) were respected, and no
INCERTO item was asserted as fact.

## Change

File: `unified_quantum_gravity_book/chap12_grand_unification_quantum_gravity_treatise.tex`

- Lines 527--566: new `\subsection{Lorentzian Completion}` (`\label{sec:lorentzian_completion}`), inserted
  immediately after the closed-form $d_s(\tau)$ discussion and its Ho\v{r}ava $z=3$ / entire-form-factor /
  `modesto2012` ghost remark (formerly ending at the old line 525), and before the pre-existing
  "Ryu--Takayanagi Hemisphere" subsection (now line 568).
  - Lines 530--539: Källén--Lehmann obstruction, stated as a cited/standard fact with precise hypotheses
    (Stieltjes representation with $\rho \ge 0$ $\Rightarrow$ $d_s(\tau) \ge 4$ for every $\tau$), citing
    Lehmann 1954 and Osterwalder--Schrader 1973 for the representation and BBMM 2016 §IV for the standard
    ("folklore") status of the argument. Corresponds to VERIFICACAO item 1 (CONFIRMA).
  - Lines 541--542: fakeon prescription (Anselmi; Anselmi--Piva) presented as conditional statements, not
    book theorems: unchanged symbol/$d_s(\tau)$, Lorentz invariance, locality, renormalizability of
    $R+R^2+C^2$ (Stelle 1977, ABP 2020), unitarity proved perturbatively to all orders (Anselmi 2021), cost
    = microcausality violation below $\ell$ (Anselmi--Piva 2018). Corresponds to VERIFICACAO items 2, 7, 8,
    10 (all CONFIRMA). Did **not** assert item 9 (independent scrutiny of the fakeon prescription), which is
    INCERTO.
  - Lines 544--551: inflation formula $r = 24 m_\chi^2/[N^2(m_\varphi^2+2m_\chi^2)]$, $m_\chi > m_\varphi/4$,
    $4/3 < N^2 r < 12$, $N=60$ window $[3.7\times10^{-4}, 3.3\times10^{-3}]$; one-scale case $r=8/N^2\approx
    2.2\times10^{-3}$, framed as $\sim2.2\sigma$ from zero at LiteBIRD and $\sim1.1\sigma$ from Starobinsky,
    with an explicit "weak test alone" qualifier. Corresponds to VERIFICACAO items 11, 13, 17 (CONFIRMA /
    CONFIRMA / INCERTO-exagerado, matched by using the corrected, hedged wording of item 17 rather than the
    stronger claim in the original README draft).
  - Lines 550--553: scale $\ell=\hbar c/m_\chi\approx7\times10^{-30}$ m $\approx4.4\times10^5\,\ell_P$ with an
    explicit dimensional check, and the general bound $\ell<2.9\times10^{-29}$ m. Corresponds to
    VERIFICACAO items 14--16 (CONFIRMA).
  - Lines 555--556: Lee--Wick and nonlocal entire form factors mentioned as alternatives, with the corrected
    reading of VERIFICACAO's **R1**: the standard Lee--Wick construction shares the book's tree-level
    symbol exactly, and a complex-conjugate pole pair in the symbol itself (not in a resummed width) needs
    polynomial degree $n\ge3$, hence $d_s\le4/3$, not $2$. No ranking is asserted among fakeon / entire form
    factors / Hořava $z=3$ (the last two already discussed earlier in the chapter), consistent with
    VERIFICACAO's own refusal to assert a ranking beyond the README's un-audited recommendation.
  - Lines 559--566: new `\begin{conjecture}[Spin-2 Identification]` (`\label{conj:spin2_identification}`)
    plus a `\begin{remark}` stating precisely what would need to be shown (identification of $h_{\mu\nu}$ in
    the simplicial/minimax construction, derivation rather than positing of the linearized $R+aR^2+bC^2$
    combination, and control of the $m_\chi/m_\varphi$ ratio) — labelled as a conjecture, not a theorem, per
    house style.
- Lines 725--790: eleven new `\bibitem`s with Crossref-resolved DOIs, verified individually via the Crossref
  API (`https://api.crossref.org/works/<doi>`) against title/author/venue: `Lehmann1954`, `OS1973`,
  `BBMM2016`, `Anselmi2018`, `AnselmiPiva2018`, `Anselmi2021`, `ABP2020`, `Stelle1977`, `Stelle1978`,
  `LeeWick1970`, `GOW2008`.

## Not done / out of scope

- Did not touch any other chapter, `WORKPLAN.md`, or any `audit/` ledger file other than this log.
- Did not assert the REFUTA items from VERIFICACAO (Lee--Wick "excluded"; Pais--Uhlenbeck $\omega_1=0$) and
  did not mention Pais--Uhlenbeck at all, since it was not requested and its premise is refuted.
- Did not cite the Buoninfante 2025 JHEP 02(2025)186 "independent scrutiny" claim used in VERIFICACAO item 9,
  since that item's overall verdict is INCERTO and its DOI is not in the project's resolved `refs.md` table.

## Build verification

Both compiled with `pdflatex -interaction=nonstopmode -halt-on-error`, 3 passes, in temporary directories
(not the tracked working copy):

- **Chapter 12, standalone** (temp copy with `declarations_chapter.tex`): 0 errors, 0 warnings, 0 overfull
  boxes, 0 underfull boxes, 0 undefined references. Output: 20 pages.
- **Master volume** (temp copy of `master_book_unified_quantum_gravity.tex` with all `chapNN_*.pdf` +
  `DICTIONARY_TERMS_AND_SYMBOLS.pdf`, using the freshly rebuilt Chapter 12 PDF): 0 errors, 0 warnings, 0
  overfull boxes, 0 underfull boxes, 0 undefined references. Output: 197 pages (up from 191, consistent with
  the added subsection).

No tracked PDF in the repository was overwritten by this pass; only the `.tex` source of Chapter 12 was
edited. Rebuilding the tracked PDFs is left to `build_pdfs_safe.py`, per the author's normal release process.

## Round 2 (corrector, four-eyes: did not write this subsection, the Round-1 fix log, or the L2 report)

Applied every REFUTA and INCERTO row of `audit/verify/L2_lorentzian_2026-09-28.md` to
`unified_quantum_gravity_book/chap12_grand_unification_quantum_gravity_treatise.tex`,
`sec:lorentzian_completion`. Nothing else in the repository was touched.

- **R1 (#5), `chap12...tex:532-542`.** The K\"all\'en--Lehmann step only bounds the UV limit. Restated
  eq. `kl_bound` (line 539-540) as `\lim_{\tau\to0} d_s(\tau) \ge 4` and added one sentence (line 542)
  noting the stronger pointwise claim needs a further Chebyshev-type moment bound not carried out here,
  instead of asserting `d_s(\tau)\ge4` "for every $\tau$" from the sketched argument alone.
- **R2 (#6), `chap12...tex:542`.** Added a direct citation to Weinberg's argument, `\cite{Weinberg1995}
  (\S 10.7, p. 460)`, new `\bibitem{Weinberg1995}` at `chap12...tex:741-745` (Cambridge Univ. Press,
  DOI `10.1017/CBO9781139644167`, Crossref-checked: title "The Quantum Theory of Fields", ISBN
  9780521550017 = Vol. I *Foundations*). Changed "\S IV ... (folklore)" to "\S V", dropping "folklore",
  for `\cite{BBMM2016}`.
- **R3 (#9), `chap12...tex:542`.** "gives up Lorentz invariance below $M_\ast$" to "above $M_\ast$".
- **R4 (#10), `chap12...tex:542,557`.** Line 542: removed the unsupported "asymptotic positivity of the
  spectral density" claim for entire form factors; now says only that they keep Lorentz invariance and
  give up locality, with positivity of their spectral density left unestablished, and the family is
  explicitly marked "a different family from Modesto's ghost-free construction \cite{modesto2012}". Line
  557: same clarification where `modesto2012` is cited as one of "the other two routes".
- **R5 (#17), `chap12...tex:544`.** "distances $\lesssim\ell$ (Compton wavelength)" replaced by
  "centre-of-mass energies above $m_\chi$, at distances or time intervals below $1/|\Gamma_\chi|$", with
  $\Gamma_\chi<0$ the fakeon width and $\Gamma_\chi\propto m_\chi^3/M_P^2 \ll m_\chi$ stated explicitly.
- **R6 (#26), `chap12...tex:555`.** Rewrote the end of the fakeon-scale paragraph to keep $\ell=1/m_\chi$
  (fakeon Compton wavelength) and $\ell_\ast$ of eq. `graviton_dispersion` (the Lorentz-violating
  $\xi$-term, discussed at line ~608) explicit and separate: the Lorentz-invariant fakeon completion
  predicts $\xi=0$ (no dispersion signal) and does not fix $\ell_\ast$; if it applied here it would fix
  $\ell=1/m_\chi$ instead.
- **R7 (#29), `chap12...tex:557`.** Added the missing hypothesis "together with the massless (graviton)
  pole" to the $n\ge3\Rightarrow d_s\le4/3$ statement, with a parenthetical noting that a bare
  complex-conjugate pair alone already has $n=2$, $d_s=2$.
- **R8 (#30), `chap12...tex:557`.** "each gives up a different one of locality, Lorentz invariance and
  positivity" replaced by an explicit statement that Lee--Wick and the fakeon both give up positivity
  (same tree-level symbol and residue, differing only in the pole prescription), while entire form
  factors give up locality and Ho\v{r}ava--Lifshitz gives up Lorentz invariance.
- **R9 (#32), `chap12...tex:559-570`.** Reworded the Conjecture (lines 559-562) to identify only the
  *symbol*, under the formal substitution $\ell_P\to\ell:=1/m_2$, leaving $m_2$ free subject to
  $m_\chi>m_\varphi/4$; it no longer sets $m_2=1/\ell_P$. Updated the accompanying Remark (564-566) to say
  item (b) would fix $m_\chi/m_\varphi$ (since $A_s$ already fixes $m_\varphi$), not leave it undetermined.
  Added a second Remark (568-570) stating explicitly that $\ell=\ell_P$ (giving $N^2r=12(1-2.5\times
  10^{-12})$, i.e. Starobinsky) and the one-scale choice $m_\chi=m_\varphi$ ($r=8/N^2$) are independent,
  mutually exclusive specializations within $4/(3N^2)<r<12/N^2$, not consequences of the Conjecture.
- **#3 (INCERTO), `chap12...tex:532,537`.** Added "scalar field, or ... a positive-metric component" and
  "$P(\tau)<\infty$" to the Källén--Lehmann hypotheses (line 532), and a sentence (line 537) noting
  covariant-gauge graviton propagators (indefinite metric before gauge-fixing) are not directly covered.
- **#34 (INCERTO), `chap12...tex:561`.** Added "(a limit not constructed here)" after "continuum limit of
  the simplicial construction of this book" in the Conjecture statement, to flag explicitly that the
  limit is not a defined object in this chapter, consistent with the pre-existing Remark's "None of
  (a)--(c) is attempted here".

### Build verification

`pdflatex -interaction=nonstopmode`, 3 passes, temp copies (via `build_pdfs_safe.build`, not the tracked
working directory):

- **Chapter 12, standalone:** err=0, warn=0, overfull=0.
- **Master volume** (with the freshly rebuilt Chapter 12 PDF): err=0, warn=0, overfull=0.

No undefined-reference warnings were reported for either target (`LaTeX Warning` count is included in
`warn`, which is 0). No tracked `.tex` file other than `chap12_grand_unification_quantum_gravity_treatise.tex`
was edited; the rebuilt `.pdf` outputs are git-ignored (`*.pdf` in `.gitignore`) and were not committed.
