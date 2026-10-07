# Reference audit: paper_functorial_tensor_field_theory.tex (2026-10-06)

Resolver: `audit/scripts/refs_resolve.py` and its output `refs_resolve.out.txt`.
- It resolves every DOI with Crossref, falling back to DataCite. It checks each arXiv id with the arXiv API and recomputes ISBN-13 check digits.
- It compares title, first author, year, volume and first page with the bibliography.
- Negative controls: a fake DOI returns 404, and a mutated volume and a mutated ISBN check digit are both detected.
- Result: 0 failures across 42 bibitems, all of them cited.
- No personal data was sent: the User-Agent is generic and no mailto parameter was used.

Other sources used:
- abstracts from OpenAlex, INSPIRE and arXiv;
- full texts from arXiv PDFs, numdam (Atiyah), the author's site (Selinger) and groupoids.org.uk (Brown);
- Open Library for ISBNs.

Not accessible (behind a paywall or blocked to bots): Springer full texts (Provost–Vallée, Gibbons–Hawking, Israel), Elsevier (Petz, Uhlmann), Cambridge Core (Segal), Project Euclid, and the OUP book (Choquet-Bruhat). Each of these is cited only at the level its abstract or metadata supports.

Before: 8 references. After: 42 references (34 added, 8 kept, 1 of them fixed).

| key | identifier | resolved? | metadata match | cited claim checked? | added/kept/fixed | note |
|---|---|---|---|---|---|---|
| silvafilho2026book | 10.5281/zenodo.22290043 | yes (DataCite) | yes | n/a (programme) | kept | |
| atiyah1988topological | 10.1007/BF02698547 | yes | yes, except title | yes, full text (numdam): §2 axioms; gluing = axiom (3b), Z(M)=⟨Z(M1),Z(M2)⟩ | fixed | Crossref/numdam metadata give the singular "Topological quantum field theory"; the article heading reads "TOPOLOGICAL QUANTUM FIELD THEORIES". Restored to the printed plural. §1 confirms that Atiyah follows Segal's approach to CFT. |
| verstraete2010continuous | 10.1103/PhysRevLett.104.190405; arXiv:1002.1824 | yes | yes | yes, full text: definition, gauge invariance, block-entropy bound "2 log₂(D)" (bits; the same as 2 ln χ in nats, matching the paper's natural log) | kept | |
| ryu2006holographic | 10.1103/PhysRevLett.96.181602; hep-th/0603001 | yes | yes | yes (abstract, area/4G formula) | kept | |
| choquet1952 | 10.1007/BF02392131 | yes | yes | prior L2 audit (vacuum local existence) | kept | |
| choquetbruhat2009 | 10.1093/acprof:oso/9780199230723.001.0001; ISBN 978-0-19-923072-3 | yes | yes (Crossref "issued" 2008 = online date; print year 2009) | chapter level only (Ch. VI chapter abstract); book not accessible | kept | theorem number still open |
| bousso2016 | 10.1103/PhysRevD.93.024017; arXiv:1509.02542 | yes | yes | yes (abstract: free and superrenormalizable bosonic QFTs) | kept | |
| godel1949 | 10.1103/RevModPhys.21.447 | yes | yes | prior audit | kept | |
| haegeman2013calculus | 10.1103/PhysRevB.88.085118; arXiv:1211.3935 | yes | yes | yes, full text: Sec. VI, Eq. (55), position-dependent gauge transformation | added | intro; Lemma 2.4 proof; related work |
| adm2008 | 10.1007/s10714-008-0661-1; arXiv:gr-qc/0405109 | yes | yes (republication; arXiv title "The Dynamics of General Relativity") | yes, full text: Sec. 3, Eqs. (3.9)–(3.12), lapse N and shift Nⁱ | added | the original is Ch. 7 of L. Witten (ed.), Wiley 1962, pp. 227–265, per the arXiv journal-ref; section numbering is preserved |
| gourgoulhon2012 | 10.1007/978-3-642-24525-1; ISBN 978-3-642-24524-4 | yes | yes (LNP 846 via Open Library) | yes, via the arXiv precursor gr-qc/0703035: Hamiltonian constraint Eq. (4.19), momentum constraint Eq. (4.22) with p = −T(n,γ·), E = T(n,n) | added | Book chapters per Crossref: Ch. 4 "Geometry of Foliations", Ch. 5 "3+1 Decomposition of Einstein Equation". The book text itself was not accessible, so it is cited at chapter level. The text says Λ=0 and G_N=1 there. |
| provost1980 | 10.1007/BF02193559 | yes | yes | abstract only (INSPIRE): metric tensor defined from the Hilbert-space structure on submanifolds of states | added | full text not accessible; cited for attribution only |
| liu2020qfi | 10.1088/1751-8121/ab5d4d; arXiv:1907.08037 | yes | yes | yes, full text (arXiv v3): Thm 2.5 Eq. (25) pure-state QFIM; §2.4.1 Eq. (74) Fubini–Study = QFIM/4; Eq. (29) F_φφ = sin²2θ; §2.1 QFIMs ⊂ Petz monotone metrics | added | Equation numbers are from arXiv v3, the accepted version. They are used in Def. 2.2, Example 6.1 and Related work. |
| braunstein1994 | 10.1103/PhysRevLett.72.3439 | yes | yes | abstract | added | related work |
| uhlmann1976 | 10.1016/0034-4877(76)90060-4 | yes | yes | abstract (INSPIRE) | added | related work; full text not accessible |
| petz1996 | 10.1016/0024-3795(94)00211-8 | yes | yes | abstract (INSPIRE) | added | related work; full text not accessible |
| amari2000 | 10.1090/mmono/191; ISBN 978-0-8218-4302-4 | yes | yes (Crossref online year 2007; AMS print year 2000) | publisher description (includes a chapter on quantum systems) | added | survey; see-also only |
| haegeman2014geometry | 10.1063/1.4862851; arXiv:1210.7710 | yes | yes | abstract: principal fibre bundle, Kähler base | added | related work; a seed of the citation graph |
| haegeman2010variational | 10.1103/PhysRevLett.105.251601; arXiv:1006.2409 | yes | yes (Crossref title has MathML) | abstract | added | related work |
| tuybens2022 | 10.1103/PhysRevLett.128.020501 | yes | yes | abstract | added | found by forward citation of Verstraete–Cirac and Haegeman et al. 2013 (OpenAlex) |
| vanraamsdonk2010 | 10.1007/s10714-010-1034-0; arXiv:1005.3035 | yes | yes | abstract | added | related work |
| swingle2012 | 10.1103/PhysRevD.86.065007; arXiv:0905.1317 | yes | yes | abstract | added | related work |
| haegeman2013cmera | 10.1103/PhysRevLett.110.100402; arXiv:1102.5524 | yes | yes | abstract | added | related work |
| nozaki2012 | 10.1007/JHEP10(2012)193; arXiv:1208.3469 | yes | yes | abstract: metric in the holographic direction for cMERA | added | related work; a seed of the citation graph |
| miyaji2015 | 10.1103/PhysRevLett.115.261602; arXiv:1507.07555 | yes | yes (arXiv title "Gravity Dual of Quantum Information Metric") | abstract: dual ≈ volume of maximal time slice | added | related work |
| erdmenger2023 | 10.1103/PhysRevD.108.106020 | yes | yes | abstract: Fubini–Study complexity geometry | added | found by forward citation of Nozaki et al. (OpenAlex) |
| cao2017 | 10.1103/PhysRevD.95.024031; arXiv:1606.08444 | yes | yes | abstract | added | related work; a seed of the citation graph |
| segal2004 | 10.1017/CBO9780511526398.019; ISBN 978-0-521-54049-0 | yes | Crossref: DOI .019 = "The definition of CFT", pp. 432–575, with no author field. Segal's whole contribution spans pp. 421–577 (foreword .018, references .020). | attribution only, via Atiyah §1 (verified) | added | Cambridge Core not accessible (429) |
| baezdolan1995 | 10.1063/1.531236; q-alg/9503002 | yes | yes | abstract | added | Related work; Open problem 7.2 |
| lurie2009 | 10.4310/CDM.2008.v2008.n1.a3; arXiv:0905.0465 | yes | yes | abstract (proof sketch of the Baez–Dolan cobordism hypothesis) | added | Related work; Open problem 7.2 |
| baez2006quandaries | arXiv:quant-ph/0404040 | yes | yes (book chapter, OUP 2006, pp. 240–265, per the arXiv journal-ref) | abstract: nCob and Hilb are *-categories with non-cartesian monoidal structure | added | Related work; Open problem 7.4 |
| schreiber2009 | arXiv:0705.0452 (J. Homotopy Relat. Struct. 4 (2009) 187–244) | yes | yes | yes, full text: Def. 2.1, sitting instant | added | Def. 5.1; Related work |
| brown2006 | ISBN 978-1-4196-2722-4 (no DOI) | yes (Open Library) | yes | yes, full text (author's PDF): §3.4 p. 77 "path of length r"; §6.1 Ex. 1 p. 203: category PX with zero paths as identities | added | Def. 5.1; Related work |
| curiel2017 | 10.1007/978-1-4939-3210-8_3; arXiv:1405.0403 | yes | yes | yes, full text: §2.1 table, NEC in geometric (R_kk ≥ 0) and physical (T_kk ≥ 0) forms | added | Remark 3.3(a) |
| israel1966 | 10.1007/BF02710419 | yes | yes | abstract (INSPIRE): junctions characterized by extrinsic curvatures; thin shells | added | after Prop. 6.7; full text not accessible |
| dewitt1967 | 10.1103/PhysRev.160.1113 | yes | yes | abstract: canonical theory, constraints on the state vector | added | §6.6 heuristic |
| araujoregado2023 | 10.1007/JHEP03(2023)026 | yes | yes | abstract | added | found by forward citation of Nozaki et al.; §6.6 |
| mohr2025codata | 10.1103/RevModPhys.97.025002 | yes | yes | ℓ_P = 1.616255e-35 m (NIST CODATA 2022 page), so ℓ_P² = 2.612e-70 m² and A/(8ℓ_P²) = 4.785e68 for 1 m² | added | §6.6 |
| selinger2007 | 10.1016/j.entcs.2006.12.018 | yes | yes | yes, full text (author's preprint): Def. 2.6, dagger compact closed category | added | Open problem 7.3; numbering taken from the preprint |
| geroch1967 | 10.1063/1.1705276 | yes | yes | abstract: under certain conditions, topology change iff acausal | added | Open problem 7.3; full text not accessible |
| borde1994 | arXiv:gr-qc/9406053 | yes | yes | abstract | added | Open problem 7.3; unpublished. Crossref has no record; PRD 50, 3692 is a different Borde paper. |
| gibbonshawking1992 | 10.1007/BF02100864 | yes | yes | abstract (INSPIRE): Z₂ invariant = mod 2 Kervaire semi-characteristic; spinor structure | added | Open problem 7.3; full text not accessible |

## Considered and not added
- **Bhatia, *Matrix Analysis* (Weyl's inequality):** the text was not accessible, so the theorem number could not be checked. Weyl's inequality stays uncited, as a named classical result.
- **Helstrom (1976):** not accessible; the pure-state QFI is cited from Liu et al.
- **Hawking–Ellis; Wald:** not accessible; NEC definitions are taken from Curiel, and the Hilbert stress tensor is derived in the text.
- **Abramsky–Coecke 2004:** Selinger's Def. 2.6 already credits it.
- **CODATA 2018 (Tiesinga et al. 2021):** superseded by CODATA 2022.

## Citation graph (OpenAlex, citing works since 2022)
- **Seeds:**
  - Haegeman et al. 2014 (84 citing works)
  - Nozaki–Ryu–Takayanagi 2012 (192)
  - Cao–Carroll–Michalakis 2017 (212)
  - Verstraete–Cirac 2010 (271)
  - Haegeman et al. 2013 (87)
- **Added from the graph:** Tuybens et al. 2022, Erdmenger et al. 2023, Araujo-Regado–Khan–Wall 2023.
- **Screened and not added, because they are off-topic for this paper:**
  - Qi et al. 2025, gerbes over MPS families;
  - Vardian 2023, cMERA of cMPS;
  - relativistic cMPS follow-ups;
  - higher Berry curvature of MPS.

## Build
- pdflatex was run 3 times: 0 errors, 0 warnings, 0 overfull boxes, 0 undefined references. The PDF has 13 pages, up from 11.
- The .aux, .out, .toc and .log files were deleted.
- Backup: `_arquivo/backup_tex_2026-10-06/Manuscritos_Avulsos/paper_functorial_tensor_field_theory/paper_functorial_tensor_field_theory_refs.tex`, logged in `MANIFESTO.tsv`.

## Text changes (no new mathematical claims)
- **New "Related work" subsection in §1.**
- **Citations placed where each claim is made:**
  - ADM form, in the introduction;
  - QFI equals 4 × Fubini–Study (Def. 2.2);
  - gauge invariance along the line (Lemma 2.4);
  - constraint equations (§3), "cf." with Λ=0 and G_N=1;
  - NEC and null convergence (Remark 3.3);
  - Moore paths and sitting instants (Def. 5.1);
  - the qubit QFI sin²2θ (Example 6.1);
  - Israel junctions (after Prop. 6.7);
  - Wheeler–DeWitt and CODATA 2022 (§6.6);
  - cobordism hypothesis, dagger-compact categories and topology-change results (Open problems 7.2–7.4).
- **Declarations:** "resolved through Crossref, DataCite, arXiv or, for the one book without a DOI, its ISBN record."
- **Not touched, flagged for the author:** the Verification-status paragraph still says "files that accompanied earlier versions". This conflicts with house rule 6 if that rule covers the declarations.
