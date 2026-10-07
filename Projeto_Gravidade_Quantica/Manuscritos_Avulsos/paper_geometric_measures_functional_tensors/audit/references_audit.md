# Reference audit: *Beyond the Spectrum II* (2026-10-07)

- **Scope:** every bibitem of `paper_geometric_measures_functional_tensors.tex`. The bibliography went from 23 to 68 entries: 23 kept, 45 added.
- **Resolver:** `audit/scripts/refs_resolve.py`, output in `refs_resolve.out.txt`.
  - It queries Crossref, falling back to DataCite, the arXiv API and Open Library for the one ISBN-only entry.
  - It compares title, first-author surname and year.
  - Negative controls:
    - a mutated DOI returns 404;
    - a wrong title gives a ratio of 0.24;
    - a mutated ISBN fails the checksum.
  - Result: 66 PASS, 1 CHECK and 0 FAIL, plus one entry with no DOI, which resolves through Open Library. 68 keys are cited, none is missing and none is uncited.
- **Privacy:** no personal data was sent. The scripts use a generic User-Agent, no mailto, and no Unpaywall.
- **Paywalled sources:** marked "not accessible"; the claim was then checked against the open sources named in the note.
- **Backup:** `_arquivo/backup_tex_2026-10-07/.../paper_geometric_measures_functional_tensors_refs.tex`, with a matching line in its `MANIFESTO.tsv`.
- **Build:** pdflatex run 3 times. The result has 0 errors, 0 warnings, 0 overfull boxes, 0 underfull boxes and 0 undefined references, and 21 pages. `\raggedbottom` was added to remove one underfull `\vbox` on the bibliography page.

**Legend:**
- *Resolved*: the identifier returns HTTP 200 from a registry.
- *Cited claim checked?*:
  - **full text**: the statement was read in the source;
  - **abstract**: the claim is at abstract level and the abstract was read;
  - **secondary**: the claim was confirmed only through a named open secondary source;
  - **n/a**: the entry is cited as a general reference.

## 1. Previously unchecked specific-result citations, now re-checked

| Citation | Source read | Finding |
|---|---|---|
| AGS Thm 8.3.1 | An open copy of the 1st edition (2005), Ch. 8, p. 182 ff. The Springer chapter summary of the 2nd edition (2008) confirms the same number. | **Confirmed.** The converse part reads: "if a narrowly continuous curve µt : I → Pp(X) satisfies the continuity equation for some Borel velocity field vt with ‖vt‖_{Lp(µt)} ∈ L¹(I), then µt is absolutely continuous and \|µ′\|(t) ≤ ‖vt‖ for a.e. t". This is exactly how the paper uses it, with L¹ on compact subintervals. |
| Hörmander §8.1–8.2 | The Springer chapter preview of Ch. VIII, pp. 251–252. | **Confirmed at section level.** The preview says "Section 8.1 gives the basic definitions of the wave front set", that WF has "projection in X equal to sing supp u", and that "In Section 8.2 we then reconsider the operations…". The individual numbers, Prop. 8.1.3 and Thm 8.2.4, were not seen; the paper cites sections only. |
| Connes 1988 normalization | The CMP article is not accessible: Project Euclid is behind a bot wall and Springer is paywalled. The open copy of Connes, *Noncommutative Geometry* (1994), from the author's site, was read. | **Confirmed.** Ch. IV §2, Prop. 5 reads: for T ∈ OP^{−n}, Tr_ω(T) = Res(T) = (1/(n(2π)^n)) ∫_{S*M} trace_E(σ_{−n}) ds. The book cites [101] = Connes, CMP 117 (1988), for this. This matches the paper's formula. The Dixmier trace (1/log N)Σ_{n<N} μ_n, extended by linearity, also matches Def. 6.1. The citation now also points to the book's proposition. |

## 2. Table

| key | identifier | resolved? | metadata match | cited claim checked? | status | note |
|---|---|---|---|---|---|---|
| ambrosio2003direct | 10.4171/IFB/72 | yes | yes | abstract | added | The functional ∫\|∇u\|(α+β\|div(∇u/\|∇u\|)\|^p), p ≥ 1. It is placed after the definition of 𝒲 in §4. |
| ambrosio2008gradient | 10.1007/978-3-7643-8722-8 | yes | yes; Crossref stores the short title | full text | kept | Thm 8.3.1 confirmed (§1). |
| atienza2020stability | 10.1016/j.patcog.2020.107509 | yes | yes | full text (arXiv 1803.08304) | added | Thm 3.12 is the stability of persistent entropy. |
| bakry1985diffusions | 10.1007/BFb0075847; ISBN 978-3-540-15230-9 | yes | yes | n/a (classical criterion) | kept | |
| bakry2014analysis | 10.1007/978-3-319-00227-9 | yes | yes | n/a | kept | |
| benamou2000computational | 10.1007/s002110050002 | yes | yes | secondary (AGS Ch. 8 intro; Peyre eq. 6) | kept | |
| bhatia2019bures | 10.1016/j.exmath.2018.01.002 | yes | yes | full text (arXiv 1712.01504) | added | "In the most important special case of Gaussian measures, the distance d_W coincides with the Bures distance". Used in Related work. |
| braunstein1994statistical | 10.1103/PhysRevLett.72.3439 | yes | yes | abstract + secondary (Liu et al. §2.4.2: D_B² = ¼ΣF dx dx) | added | |
| brenier1991polar | 10.1002/cpa.3160440402 | yes | yes | abstract | added | Brenier's theorem in the proof of Thm 2.4(a). |
| buser1982note | 10.24033/asens.1426 | yes | yes | secondary (Ledoux 1994 abstract) | added | Reverse Cheeger inequality under a lower Ricci bound. Cited in a remark and not used. |
| caffarelli2000monotonicity | 10.1007/s002200000257 | yes | yes | not re-read (paywalled) | kept | Still to check: that the contraction theorem covers restriction to a convex set, as in the earlier note. |
| chan2003euler | 10.1137/S0036139901390088 | yes | yes; Crossref year 2003 | abstract | added | Elastica (κ²) inpainting. |
| chazal2009proximity | 10.1145/1542362.1542407 | yes | yes; 5 authors | abstract | added | The original algebraic stability (interleaving) paper. |
| chazal2016structure | 10.1007/978-3-319-42545-0 | yes | yes | n/a | kept | |
| cheeger1970lower | 10.1515/9781400869312-013 | yes | title and author yes; **year CHECK** | n/a | kept | The DOI is De Gruyter's 2015 digitization of the 1970 volume. Expected mismatch; not an error. |
| chen2014entanglement | 10.1088/1742-5468/2014/10/P10011 | yes | yes | n/a (contrast only) | kept | |
| chintakunta2015entropy | 10.1016/j.patcog.2014.06.023 | yes | yes; 5 authors | full text (open repository copy) | added | Def. 3 is persistent entropy, the same formula. Their convention for infinite bars (length to m+1) does not arise here, since all bars are finite. |
| chowdhury2019gromov | 10.1093/imaiai/iaz026 | yes | yes | full text (arXiv 1808.04337) | added | Network GW distance; compares networks with different numbers of nodes (Fig. 5). |
| cohensteiner2007stability | 10.1007/s00454-006-1276-5 | yes | yes (online 2006) | n/a | kept | |
| connes1985noncommutative | 10.1007/BF02698807 | yes | yes, pp. 41–144 | n/a (cited as the origin of cyclic cohomology) | added | Connes 1994's bibliography lists pp. 257–360, but the registry says 41–144; the registry value is used. |
| connes1988action | 10.1007/BF01218391 | yes | yes | secondary: Connes 1994, Ch. IV §2, Prop. 5 (full text) | kept | Normalization confirmed (§1). |
| connes1994noncommutative | ISBN 978-0-12-185860-5 | yes (Open Library) | yes | full text (open copy) | kept | Now cited with locators: Ch. IV §2, Prop. 5 and Thm 8. Thm 8 gives the cocycle λ_n Tr_ω(a⁰[D,a¹]⋯[D,aⁿ]\|D\|^{−n}), "with γa⁰ instead of a⁰ in the even case". This matches τ_d / τ_2^γ up to λ_n. |
| connes1995local | 10.1007/BF01895667 | yes | yes | abstract | added | Local index formula via Dixmier trace and residues. |
| crawley2015decomposition | 10.1142/S0219498815500668 | yes | yes | n/a | kept | |
| edelsbrunner2002topological | 10.1007/s00454-002-2885-2 | yes | yes | full text (open) | added | Introduces persistence. The paper notes that Robins formulated persistence independently. |
| edelsbrunner2010computational | 10.1090/mbk/069; ISBN 978-0-8218-4925-5 | yes | yes (Crossref 2009, printed 2010) | n/a (textbook) | added | |
| evans2015measure | 10.1201/b18333 | yes | yes | n/a | kept | |
| gordon1992one | 10.1090/S0273-0979-1992-00289-6 | yes | yes | abstract | added | Isospectral non-isometric planar domains. |
| grochenig2001foundations | 10.1007/978-1-4612-0003-1; ISBN 978-1-4612-6568-9 | yes | yes | n/a (table of contents: chapter "The Short-Time Fourier Transform") | added | Definition of the STFT. |
| guillemin1985new | 10.1016/0001-8708(85)90018-0 | yes | yes | secondary (Connes 1994 names the "Manin–Wodzicki–Guillemin residue") | added | |
| helstrom1967minimum | 10.1016/0375-9601(67)90366-0 | yes | yes | secondary (standard attribution of the SLD; abstract not available) | added | |
| hormander2003analysis | 10.1007/978-3-642-61497-2; ISBN 978-3-540-00662-6 | yes | yes; Crossref short title | preview pages | kept | §8.1–8.2 confirmed at section level. The origin of WF is Hörmander, ICM Nice 1970 (no DOI); it is not added. |
| jordan1998variational | 10.1137/S0036141096303359 | yes | yes | abstract | added | |
| kac1966can | 10.1080/00029890.1966.11970915 | yes | yes | n/a (cited for the question) | added | |
| kaczynski2004computational | 10.1007/b97315; ISBN 978-0-387-21597-6 | yes | yes | n/a (textbook on cubical homology) | added | |
| kantorovich2006translocation | 10.1007/s10958-006-0049-2 | yes | yes | not accessible | added | English reprint of the 1942 Doklady note; cited for the relaxed formulation. |
| ledoux1994simple | 10.1090/S0002-9939-1994-1186991-X | yes | yes | abstract | added | |
| liu2020quantum | 10.1088/1751-8121/ab5d4d; arXiv 1907.08037 | yes | yes | full text | added | Thm 2.1, eq. (10), is exactly Lemma 7.2. Eq. (77) gives D_B² = ¼F. The theorem number is from the arXiv version. |
| lombardini2019fractional | 10.1515/ans-2018-2016; arXiv 1603.06088 | yes | yes | full text (arXiv) | added | Eq. (1.1)–(1.2) restate Visintin's Props. 11 and 13 (fractal index ≤ Minkowski dimension); there is equality for the von Koch snowflake. |
| lord2013singular | 10.1515/9783110262551; ISBN 978-3-11-026250-6 | yes | yes (Crossref 2012) | abstract | added | General theory of singular traces. |
| lott2009ricci | 10.4007/annals.2009.169.903 | yes | yes | abstract | added | |
| lovasz2012large | 10.1090/coll/060 | yes | yes | n/a | kept | |
| marques2014minmax | 10.4007/annals.2014.179.2.6 | yes | yes | abstract | added | The text says "at least 2π² for every immersed torus", as in the abstract. |
| mccann1997convexity | 10.1006/aima.1997.1634 | yes | yes | not re-read | kept | |
| memoli2011gromov | 10.1007/s10208-011-9093-5 | yes | yes | n/a | kept | Traversal seed. |
| otto2000generalization | 10.1006/jfan.1999.3557 | yes | yes | secondary (Gozlan, arXiv 0804.3089; Peyre §1) | added | LSI ⇒ T₂. Mentioned and not used. |
| petz1996monotone | 10.1016/0024-3795(94)00211-8 | yes | yes | secondary (Liu et al.: "All versions of QFIMs belong to a family of Riemannian monotone metrics established by Petz") | added | The text was weakened to "belongs to Petz's family". It does not say "smallest", because the source was not readable (bot wall). |
| peyre2018comparison | 10.1051/cocv/2017050; arXiv 1104.4631 | yes; the arXiv API timed out, PDF read by hand | yes | full text | added | Thm 1: W₂(µ,ν) ≤ 2‖µ−ν‖_{Ḣ⁻¹(µ)}, plus the formal infinitesimal identity, eq. (5). Placed in the remark after Thm 2.3. |
| provost1980riemannian | 10.1007/BF02193559 | yes | yes | not accessible; standard attribution | added | Pure-state metric. |
| safranek2017discontinuities | 10.1103/PhysRevA.95.052320 | yes | yes | secondary (Liu et al. ref. [87]) | kept | |
| sard1942measure | 10.1090/S0002-9904-1942-07811-6 | yes | yes | n/a (classical) | added | |
| silvafilho2026beyond | 10.5281/zenodo.22644743 | yes (DataCite) | **title differs** | n/a | kept | This is the concept DOI of the series. DataCite's title is "Beyond the Spectrum: The Complete Three-Volume Monograph…", not Volume I alone. Author decision: cite the Volume I version DOI, or reword the entry. |
| silvafilho2026geometry | 10.5281/zenodo.22290043 | yes (DataCite) | yes | DataCite description ("Part I (Ch. 1–2) studies functional realizations…") | added | Book citation, as requested. |
| sturm2006geometryI | 10.1007/s11511-006-0002-8 | yes | yes | abstract | added | Curvature via entropy convexity; 𝔻-distance. |
| sturm2006geometryII | 10.1007/s11511-006-0003-7 | yes | yes | abstract | added | CD(K,N). |
| sturm2023space | 10.1090/memo/1443 | yes | yes | abstract | added | Found by forward traversal of Mémoli 2011. |
| triebel1983theory | 10.1007/978-3-0346-0416-1; ISBN 978-3-0346-0415-4 | yes | yes | n/a (table of contents and zbMATH review quote only) | added | Cited only for the Besov scale. |
| uhlmann1976transition | 10.1016/0034-4877(76)90060-4 | yes | yes | secondary (Liu et al. ref. [80] for fidelity) | added | |
| vandam2003which | 10.1016/S0024-3795(03)00483-X | yes | yes | n/a (survey) | added | |
| verstraete2010continuous | 10.1103/PhysRevLett.104.190405 | yes | yes | n/a | kept | |
| villani2009optimal | 10.1007/978-3-540-71050-9; ISBN 978-3-540-71049-3 | yes | yes | n/a | kept | Ch. 6 = Wasserstein distances. |
| visintin1991generalized | 10.1007/BF03167679 | yes | yes | secondary (Lombardini, full text) | added | Not accessible. |
| von2005transport | 10.1002/cpa.20060 | yes | yes | not re-read | kept | |
| wagner2012efficient | 10.1007/978-3-642-23175-9_7 | yes | yes (online 2011) | abstract | added | |
| white1973global | 10.1090/S0002-9939-1973-0324603-1 | yes | yes | not re-read | kept | |
| wodzicki1987noncommutative | 10.1007/BFb0078372 | yes | yes | secondary (Connes 1994, Ch. IV §2) | added | |
| zanardi2007information | 10.1103/PhysRevLett.99.100603 | yes | yes | abstract | added | |
| zomorodian2005computing | 10.1007/s00454-004-1146-y | yes | yes | full text (open) | added | "persistent homology … is simply the standard homology of a particular graded module". |

## 3. Citation traversal (OpenAlex; details in `refs_resolve.out.txt`)

- **Seeds:**
  - Mémoli 2011: 535 citations; 259 citing works since 2023;
  - Chowdhury–Mémoli 2019: 76 citations; 29 since 2023;
  - Atienza et al. 2020: 99 citations; 63 since 2023.
- **Backward:**
  - the anchors that matter here (Villani, AGS, ELZ, Edelsbrunner–Harer) are now cited;
  - the others belong to shape matching or machine learning and are not relevant.
- **Forward:**
  - Sturm, *The Space of Spaces* (2023), added.
  - Not added, because they are tangential:
    - ultrametric GW (2023);
    - GW between spheres (2024);
    - Monge maps for GW (2024).
  - Recent persistent-entropy citers are applications or vectorization surveys, with no result about isospectral matrices.
- **Prior-art result:** no work was found that computes persistence or persistent entropy of step realizations of isospectral matrix pairs.

## 4. Placement and text changes (no new mathematics)

- **Intro:**
  - spectral non-determination (Kac; Gordon–Webb–Wolpert; van Dam–Haemers);
  - the book (Part I);
  - Sturm, Chowdhury–Mémoli and Sturm 2023 beside GW;
  - a new "Related work" paragraph.
- **§2:**
  - Kantorovich after the W₂ definition;
  - Peyre in the metric-speed remark;
  - Brenier in the proof of Thm 2.4(a);
  - Sturm, Lott–Villani, JKO and Otto–Villani in the remark after Thm 2.4, marked "not used".
- **§3:**
  - ELZ and Zomorodian–Carlsson after the filtration definition;
  - cubical complexes after Def. 3.2;
  - Chazal et al. 2009 in the stability proof;
  - Chintakunta et al. and Atienza et al. after the definition of persistent entropy.
- **§4:**
  - Sard;
  - Marques–Neves;
  - an elastica/inpainting sentence after the definition of 𝒲;
  - a new remark on Buser–Ledoux, marked "not used".
- **§5:**
  - Gröchenig at the Gabor transform;
  - Triebel at the Besov seminorm;
  - Visintin and Lombardini in the Minkowski remark.
- **§6:**
  - Connes 1994 locators;
  - Lord–Sukochev–Zanin;
  - Wodzicki and Guillemin in the trace theorem;
  - a paragraph tying τ_d to Connes' Thm IV.2.8, with Connes 1985 and Connes–Moscovici.
- **§7:**
  - an SLD/QFI history paragraph (Helstrom, Braunstein–Caves, Uhlmann, Petz, Provost–Vallee, Zanardi et al.);
  - Lemma 7.2 is now labelled "classical, see Liu et al., Thm 2.1".

## 5. Flags for the author (not fixed here)

1. **House style.** The Declarations still say "The Lean 4 files that accompanied earlier versions…". This is version history in the body, against convention 6.
2. **Volume I citation.** The DOI 22644743 is the series concept record, and its current title is the complete trilogy. Decide whether "Volume I" should cite a version DOI.
3. **Declarations.** The text says "Every reference was resolved through Crossref, DataCite or arXiv". Connes 1994 has no DOI and was resolved through its ISBN at Open Library. Consider "…or by ISBN".
4. **Still unchecked in full text:**
   - Caffarelli 2000 (convex restriction);
   - White 1973;
   - McCann 1997;
   - von Renesse–Sturm 2005;
   - Visintin 1991 (checked only through Lombardini);
   - Petz 1996.
5. **Mathematics.** No mathematical problem was found in the passages read for placement. The Connes normalization, AGS 8.3.1 and the QFI eigenbasis formula agree with their sources.
