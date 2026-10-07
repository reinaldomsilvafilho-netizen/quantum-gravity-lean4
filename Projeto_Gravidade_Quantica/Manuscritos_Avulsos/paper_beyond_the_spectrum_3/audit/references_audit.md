# Reference audit — Volume III (*Beyond the Spectrum III: Higher Invariants, Bipartite Kernels, and Non-Equilibrium Geometry…*)

Date: 2026-10-07. Auditor: AI session that did not write the volume.
Skills followed: `math-physics-references` (4 passes) and `scholarly-metadata-resolver`.

Resolver: `audit/scripts/refs_resolve.py` → `refs_resolve.out.txt`: **72/72 resolved and matched**, exit 0. It also checks:
- title (Jaccard ≥ 0.6, or one title contained in the other), first author and year (±2, online vs. issue year);
- ISBN-13 checksum, plus the Open Library record (for a chapter, the record of the containing volume);
- that cited keys and bibitems match one to one (72 cited, 72 bibitems, none missing, none uncited);
- that the DOI and ISBN written in each bibitem equal the audited ones.

Three negative controls (fake DOI, wrong title, bad ISBN) all fail as required. No personal data was sent: there is no mailto, Unpaywall was not used, and the User-Agent is `RefAudit/1.0`.
Claim checks were made against open full texts (AMS backfile, arXiv, Numdam, EMS Press, DML-CZ, DLMF), downloaded to the session scratchpad. Paywalled sources are marked "not accessible".

Before/after: **19 → 72** bibitems: 53 added and 19 kept. Two existing entries were fixed. `bibitem` insertion was done by the saved script `audit/scripts/refs_add_bibitems.py`; all text placements used the Edit tool.

Backup before editing: `_arquivo/backup_tex_2026-10-07/Manuscritos_Avulsos/paper_beyond_the_spectrum_3/paper_beyond_the_spectrum_3_refs.tex`, recorded in that folder's `MANIFESTO.tsv`.

## 1. Existing bibitems (task 1)

| key | identifier | resolved? | metadata match | cited claim checked? | status | note |
|---|---|---|---|---|---|---|
| Aamari2019 | 10.1214/19-EJS1551; arXiv:1705.04565 | yes | yes | yes: Thm 2.2 (= Federer 4.18), Thm 3.4 (global/local dichotomy), Prop. A.1(i) ‖II‖ ≤ 1/τ (arXiv full text, EJS layout) | kept | page range not in Crossref, so not added |
| Aurell2011 | 10.1103/PhysRevLett.106.250601; arXiv:1012.2037 | yes | yes | yes: eq. (23), minimal dissipated work = quadratic transport cost /(t_f − t_o), i.e. 𝒲₂²/τ in the units of §5 | kept | |
| BakryEmery1985 | 10.1007/BFb0075847; ISBN 978-3-540-15230-9 | yes | yes (ISBN = volume *Séminaire de Probabilités XIX*) | not accessible | kept | |
| Crooks1999 | 10.1103/PhysRevE.60.2721 | yes | yes | not accessible (abstract level) | kept | |
| DuttaFaulkner2019 | 10.1007/JHEP03(2021)178; arXiv:1905.00577 | yes | yes | yes: eqs. (2.12)–(2.14), S_R ≥ I from strong subadditivity / monotonicity of relative entropy | kept | key says 2019 (arXiv year); journal year 2021 is printed |
| EkelandHofer1989 | 10.1007/BF01215653 | yes | yes | not accessible; c₁^EH(B(r)) = πr² and monotonicity/invariance confirmed in Cieliebak–Hofer–Latschev–Schlenk §2.3.1 | kept | |
| Federer1959 | 10.1090/S0002-9947-1959-0110078-1 | yes | yes | **yes, read in full (AMS open PDF)**: Def. 4.1 (reach, Unp); Thm 4.8 (6), (8), (12) (projection Lipschitz with constant q/(q−r); ξ(a+v)=a for normal v, \|v\| < reach); Thm 4.18 (reach formula); Remark 4.21; Thm 5.6 (Steiner formula for sets of positive reach) | kept | the earlier note "4.8/4.18 not checked" is closed |
| GibsonEtAl1976 | 10.1007/BFb0095244 | yes | yes | **not accessible.** Chapter list confirmed from Crossref chapter DOIs: Ch. I Gibson, *Construction of canonical stratifications* (pp. 8–34); Ch. II Wirthmüller, *Stratifications and flows*; Ch. III du Plessis; Ch. IV Looijenga. Secondary: Orro–Trotman 2010 abstract (via search) says the transverse intersection of two Whitney regular stratified sets was first published by Gibson in these notes | kept | still cited without chapter number; I did not add one I could not confirm |
| Gromov1987 | 10.1007/978-1-4613-9586-7_3; ISBN 978-0-387-96618-2 | yes | yes | not accessible | **fixed** | the ISBN 978-1-4612-9173-2 in v3 belongs to *Analytic Number Theory and Diophantine Problems* (Open Library); replaced by the 1987 Springer ISBN of *Essays in Group Theory* |
| HoferZehnder1994 | 10.1007/978-3-0348-8540-9 | yes | yes | not accessible; the convex-body result (c_HZ = c₁^EH = minimal action) confirmed in Artstein-Avidan–Ostrover, Thm 1.3, which attributes it to [EH89] and [HZ94], and in CHLS eq. (12) | kept | |
| Jarzynski1997 | 10.1103/PhysRevLett.78.2690 | yes | yes | abstract level | kept | |
| KashiwaraSchapira1990 | 10.1007/978-3-662-02661-8; ISBN 978-3-540-51861-7 | yes | yes | **book not accessible; numbers now confirmed secondarily.** Thm 6.5.4 = involutivity (Schapira 2017, Thm 3.5; Kuo arXiv:2102.06791, §2); Prop. 8.4.1 = SS ⊂ conormals of a Whitney stratification ⇔ constructible w.r.t. it (Kuo, Prop. 2.51); Thm 8.4.2 = weakly ℝ-constructible ⇔ SS in a closed conic subanalytic Lagrangian, which is then itself Lagrangian (Schapira 2017, Thm 3.7). Chapter titles from Crossref chapter DOIs: V *Micro-support of sheaves*, VI *Micro-support and microlocalization*, VIII *Constructible sheaves*, IX *Characteristic cycles* | kept | citations changed from Ch. VI / Ch. VIII to Thm 6.5.4 / Prop. 8.4.1 (+ Thm 8.4.2); the index theorem stays at Ch. IX, with Kashiwara 1985 added as primary source |
| BridsonHaefliger1999 | 10.1007/978-3-662-12494-9; ISBN 978-3-540-64324-1 | yes | yes | not accessible | **fixed** | the ISBN 978-3-540-64306-7 in v3 belongs to an IAU colloquium volume (Open Library); replaced by the 1999 hardcover ISBN |
| JuutinenLindqvistManfredi1999 | 10.1007/s002050050157 | yes | yes | **not accessible** (Springer login; Semantic Scholar abstract elided by publisher; zbMATH behind a Cloudflare check). Attribution confirmed by four secondary sources: Lindqvist 2008 §4 item VI and Lemma 11; Champion–De Pascale–Jimenez §2 ("already proved in [24]"); Belloni–Kawohl–Juutinen §1 ("see [18, 13]" = JLM and Fukagai–Ito–Narukawa); Kawohl–Fridman Remark 5 | kept | |
| OttoVillani2000 | 10.1006/jfan.1999.3557 | yes | yes | not accessible (title level: LSI ⇒ Talagrand) | kept | |
| KawohlFridman2003 | EuDML 249339; DML-CZ 119420 | yes (DML-CZ HTTP 200; EuDML answers 403 to scripts) | yes | **yes, read in full (DML-CZ PDF)**: abstract, λ_p → h as p → 1; Remark 5, h(B_R) = n/R and λ_p^{1/p} → 1/R as p → ∞ | kept (link added) | DML-CZ link added |
| Lindqvist1990 | 10.1090/S0002-9939-1990-1007505-7 | yes | yes | confirmed in Lindqvist 2008 (ref. [33], "uniqueness … first proved in [33]") | kept | an Addendum exists (PAMS 116); not added |
| SilvaFilhoBTS | 10.5281/zenodo.22644743 | yes (DataCite) | yes | n/a (author's trilogy record) | kept | |
| SivakCrooks2012 | 10.1103/PhysRevLett.108.190602; arXiv:1201.4166 | yes | yes | yes: friction tensor (12a–b); W_ex ≥ ℒ²/t, equality only at constant excess power (Cauchy–Schwarz) | kept | |

## 2. Added bibitems (task 2)

"Read" states the level at which the source was read; "secondary" means the attribution was confirmed in another source that was read.

| key | identifier | resolved? | read at level cited? | placed at |
|---|---|---|---|---|
| ArtsteinAvidanKarasevOstrover2014 | 10.1215/00127094-2794999; arXiv:1303.4197 | yes | abstract | Related work |
| ArtsteinAvidanOstrover2008 | 10.1093/imrn/rnn044; arXiv:0712.2631 | yes (Crossref issue year 2010, online 2008) | full text: Thm 1.3 (c_EH = c_HZ = min action on convex domains) | Related work |
| AkersRath2020 | 10.1007/JHEP04(2020)208; arXiv:1911.07852 | yes | abstract | Related work; Rem. OBL-016 |
| BelloniKawohlJuutinen2006 | 10.4171/JEMS/40 | yes | full text (EMS open PDF): §1 | Related work |
| BlaberSivak2023 | 10.1088/2399-6528/acbf04; arXiv:2212.00706 | yes | abstract | Related work |
| BoissonnatLieutierWintraecken2019 | 10.1007/s41468-019-00029-8 | yes | abstract | Related work |
| Carlson1963 | 10.1016/0022-247X(63)90067-2 | yes | not accessible (ScienceDirect blocks scripts); definition of the R-function confirmed in Chow 2022, §3.3.1, eq. (3.25), ref. [49] | after Prop. OBL-017 |
| ChampionDePascaleJimenez2008 | arXiv:0811.1934 (DOI 10.48550/…) | yes | full text: §§1–2 | Related work |
| Cheeger1970 | 10.1515/9781400869312-013 | yes (DOI is the 2015 digital reissue of the 1970 volume) | not accessible; attribution in Kawohl–Fridman | Related work; Rem. after OBL-008 |
| Chow2022 | arXiv:2201.11013 | yes | full text: §3.3.1 | after Prop. OBL-017 |
| CieliebakHoferLatschevSchlenk2005 | arXiv:math/0506191 | yes | full text: §2.3.1–2.3.2, eq. (12) | Related work |
| Crooks2007 | 10.1103/PhysRevLett.99.100602; arXiv:0706.0559 | yes | abstract | Related work; Rem. OBL-012 |
| DLMF | ISBN 978-0-521-19225-5; dlmf.nist.gov | yes (Open Library; site HTTP 200) | §5.2(i), eq. 5.12.1, eq. 18.18.28 (Mehler) read online | Prop. 7.3 proof; Rem. after OBL-014 |
| EkelandHofer1990 | 10.1007/BF02570756 | yes | not accessible; role (sequence c_k) confirmed in CHLS §2.3.1 | Thm OBL-001; Related work |
| FloerHofer1994 | 10.1007/BF02571699 | yes | not accessible (title level) | Rem. OBL-003 |
| FukagaiItoNarukawa1999 | 10.57262/die/1367265629 | yes | not accessible (Project Euclid blocks scripts); attribution confirmed in Belloni–Kawohl–Juutinen ref. [13] | proof of OBL-008; Related work |
| Gromov1985 | 10.1007/BF01388806 | yes | not accessible; non-squeezing attribution in Artstein-Avidan–Ostrover §1 | Related work |
| HaimKislevOstrover2026 | 10.4007/annals.2026.203.2.5; arXiv:2405.16513 | yes | abstract | Related work |
| HaydenLemmSorce2023 | 10.1103/PhysRevA.107.L050401; arXiv:2302.10208 | yes | abstract | Related work |
| HaydenParrikarSorce2021 | 10.1007/JHEP10(2021)047; arXiv:2107.00009 | yes | abstract | Related work; Rem. OBL-016 |
| JordanKinderlehrerOtto1998 | 10.1137/S0036141096303359 | yes | not accessible (title level) | after Prop. OBL-010; Related work |
| Kashiwara1985 | Astérisque 130, 193–209 (Numdam) | yes (HTTP 200, title) | full text: §0.2, index theorem for constructible sheaves | proof of OBL-006; Related work |
| LiebRuskai1973 | 10.1063/1.1666274 | yes | not accessible; Dutta–Faulkner eq. (2.13) uses strong subadditivity | proof of OBL-015 |
| Lindqvist2008 | 10.1142/9789812811066_0005; ISBN 978-981-281-105-9 | yes | full text (author's copy, pp. 175–203): §4 III, VI; Thm 6; Lemma 11 | Rem. after OBL-007; proof of OBL-008 |
| MacPherson1974 | 10.2307/1971080 | yes | not accessible (title level: local Euler obstruction) | Rem. `rem:chi_counterexample` |
| Mather2012 | 10.1090/S0273-0979-2012-01383-6 | yes | full text: §§1–2 (conditions a, b due to Whitney [5]) | Prop. OBL-004; Related work |
| Mercer1909 | 10.1098/rsta.1909.0016 | yes | not accessible (title level: Mercer's theorem) | proof of OBL-014(4) |
| NakazatoIto2021 | 10.1103/PhysRevResearch.3.043093; arXiv:2103.00503 | yes | abstract | Rem. OBL-012; Related work |
| NguyenEtAl2018 | 10.1007/JHEP01(2018)098; arXiv:1709.07424 | yes | abstract | Rem. OBL-016; Related work |
| NiyogiSmaleWeinberger2008 | 10.1007/s00454-008-9053-2 | yes | full text: Prop. 6.1 (‖II‖ ≤ 1/τ) | proofs of OBL-020 and OBL-021 |
| OrroTrotman2010 | 10.1017/CBO9780511731983.022; ISBN 978-0-521-16969-1 | yes | abstract only, read through a search snippet (Cambridge page blocks scripts) | proof of OBL-004 |
| RatajZahle2019 | 10.1007/978-3-030-18183-3; ISBN 978-3-030-18182-6 | yes | table of contents (Ch. 4 *Sets with positive reach*) | Related work |
| SalamonBerry1983 | 10.1103/PhysRevLett.51.1127 | yes | not accessible (title level) | Rem. OBL-012; Related work |
| Schapira1991 | 10.1016/0022-4049(91)90131-K | yes | not accessible (title level) | proof of OBL-006; Related work |
| Schapira2017 | arXiv:1701.08955 | yes | full text: Thms 3.5, 3.7 | Lemma OBL-005 proof; Related work |
| SchmiedlSeifert2007 | 10.1103/PhysRevLett.98.108301; arXiv:cond-mat/0701554 | yes | full text: case study I, moving laser trap; jumps in optimal protocols | Rem. OBL-012; Related work |
| Schmidt1907 | 10.1007/BF01449770 | yes | not accessible (title level: Schmidt expansion) | Prop. OBL-014(2) |
| Schwarz2000 | 10.2140/pjm.2000.193.419 | yes | abstract | Rem. OBL-003 |
| Seifert2012 | 10.1088/0034-4885/75/12/126001; arXiv:1205.4176 | yes | abstract | Related work |
| silvafilho2026book | 10.5281/zenodo.22290043 | yes (DataCite) | the monograph: Ch. 1 is *Functional Realizations…*; Ch. 7 (`chap07`, l. 185) uses Federer's reach for obstacles | Related work; Rem. 8.2(c) |
| Srednicki1993 | 10.1103/PhysRevLett.71.666; arXiv:hep-th/9303048 | yes | full text: two coupled oscillators, thermal reduced state with geometric eigenvalues | Rem. after OBL-014 |
| Talagrand1996 | 10.1007/BF02249265 | yes | not accessible; Villani Ch. 22 read (CD(K,∞) ⇒ T₂(K)) | Rem. after OBL-010 |
| Trotman2020 | 10.1007/978-3-030-53061-7_4; ISBN 978-3-030-53060-0 | yes | abstract (RePEc) | Related work |
| UmemotoTakayanagi2018 | 10.1038/s41567-018-0075-2; arXiv:1708.09393 | yes | abstract | Rem. OBL-016; Related work |
| VanVuSaito2023 | 10.1103/PhysRevX.13.011013; arXiv:2206.02684 | yes | abstract | Rem. OBL-012; Related work |
| Villani2009 | 10.1007/978-3-540-71050-9; ISBN 978-3-540-71049-3 | yes | preprint version: TOC; Ch. 22 (Talagrand under CD(K,∞)); chapter numbering matches the book (Crossref chapter DOIs) | Rem. after OBL-010; Related work |
| Viro1988 | 10.1007/BFb0082775; ISBN 978-3-540-50237-1 | yes | not accessible (title level) | proof of OBL-006; Related work |
| Viterbo1992 | 10.1007/BF01444643 | yes | not accessible (title level: generating-function spectral invariants) | Rem. OBL-003 |
| Viterbo2000 | 10.1090/S0894-0347-00-00328-3 | yes | full text (AMS): introduction, "widespread belief" that the ball maximizes capacity at fixed volume, plausibly among convex sets | Related work |
| vonRenesseSturm2005 | 10.1002/cpa.20060 | yes | abstract | after Prop. OBL-010; Related work |
| Weyl1939 | 10.2307/2371513 | yes | not accessible; attribution in Federer 1959 §1 ([W]) | after Thm OBL-021; Related work |
| Whitney1965 | 10.2307/1970400 | yes | not accessible; Mather 2012 §1 attributes conditions a and b to it (ref. [5], pp. 496–549) | Prop. OBL-004 and its proof; Related work |
| ZhongDeWeese2024 | 10.1103/PhysRevLett.133.057102; arXiv:2404.01286 | yes | abstract | Rem. OBL-012; Related work |

## 3. Pass summaries

- **Pass 1 (foundational anchors):** Gromov 1985; Ekeland–Hofer I–II; Whitney 1965; Kashiwara 1985; Cheeger 1970; Salamon–Berry 1983; Jordan–Kinderlehrer–Otto 1998; Schmidt 1907; Mercer 1909; Lieb–Ruskai 1973; Weyl 1939.
- **Pass 2 (prior art across vocabularies):**
  - Carlson's R-function (special functions) is exactly 𝒵_A(s) for an affine realization. This is now stated after Prop. OBL-017.
  - The geometric Schmidt spectrum of Remark 6.3(a) is Srednicki's coupled-oscillator computation (hep-th), and also Mehler's formula (DLMF 18.18.28).
  - Fukagai–Ito–Narukawa (1999) is a second source for the limit in OBL-008.
  - Federer's Remark 4.21 is an older lower bound for the reach of a preimage. It is now noted in Rem. 8.2(c).
  - Thermodynamic length versus 𝒲₂ is treated by Zhong–DeWeese, Nakazato–Ito and Van Vu–Saito.
- **Pass 3 (citation traversal, OpenAlex, citing works 2023–):** the three closest papers are Aurell 2011, Sivak–Crooks 2012 and Dutta–Faulkner 2021.
  - **Forward:** Van Vu–Saito, Blaber–Sivak and Zhong–DeWeese were adopted, as was Hayden–Lemm–Sorce (a citing work of Dutta–Faulkner). Chennakesavalu–Rotskoff (PRL 130, 107101) was read at abstract level and not added, because it overlaps Zhong–DeWeese.
  - **Backward:** Umemoto–Takayanagi and Nguyen et al. came from Dutta–Faulkner. Fukagai–Ito–Narukawa came from Belloni–Kawohl–Juutinen. Carlson came from Chow.
- **Pass 4 (claim level):** see the tables. No bibitem was generated from memory: every one was resolved by the script.

## 4. Findings for the author (not edited: four-eyes rule, no new mathematics)

1. **OBL-015 title.** The title says "Canonical Purification and Reflected Entropy **Monotonicity**", but the statement proves only non-negativity, symmetry and S_R ≥ I. Hayden–Lemm–Sorce (PRA 107, L050401, 2023) show that the reflected entropy is *not* monotone under partial trace. Suggested fix: drop "Monotonicity" from the title. This needs a separate corrector.
2. **Sign convention in OBL-006.** Kashiwara's 1985 index formula carries a factor (−1)^{n(n+1)/2} and intersects with the graph of dφ. The paper writes χ = CC(F)·[T*_ΩΩ] with no sign and cites KS Ch. IX, whose theorem number and normalization I could not read. A checker should confirm that the orientation convention of CC used in the paper absorbs this sign.
3. **Kawohl–Fridman hypotheses.** Their paper assumes a bounded, *simply connected* domain (with a regularity condition). Remark 4.5 cites the p → 1 limit without these hypotheses. The disk example is unaffected; this is a wording point only.
4. **Gibson et al.** are still cited without chapter or theorem numbers for (i) Whitney genericity and (ii) transverse pull-back of Whitney stratifications. The book was not accessible.
5. **Build:** 3 pdflatex runs give 0 errors, 0 LaTeX/package warnings, 0 overfull/underfull boxes and 0 undefined references; 16 pages (13 before). The pdfTeX "font expansion" notice remains, as in v3 (documented in `CORRECTIONS_2026-10-06.md`). `.aux/.out/.toc` were deleted.
