# BtS III: pre-release re-check, layer 2 (2026-10-07)

- **Checker:** independent Claude session (Opus). I wrote neither the volume, the reference audit nor `fixes_prerelease.md`. The works were not edited.
- **Inputs:**
  - the current `.tex`/PDF;
  - backups `_arquivo/backup_tex_2026-10-07/.../paper_beyond_the_spectrum_3_prerelease.tex` (diffed: OBL-006, OBL-015, declarations) and `_refs.tex` (the state before the reference audit);
  - `audit/references_audit.md`, `audit/fixes_prerelease.md`, `LEDGER.md`, `CORRECTIONS_2026-10-06.md`, `ZENODO_DESCRIPTION_VOL3.md`.
- **Scripts** (`audit/scripts/`, all exit 0):
  - `L2r_obl006_sign.py`;
  - `L2r_refs_sample.py`;
  - `L2r_declarations_text.py`;
  - `L2r_body_diff.py`;
  - `L2r_build.py`.
- **Processes:** none left; `processos_orfaos.py` finds 0 suspects.

## Verdicts

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 2a | OBL-015 (Thm 6.4) title and statement | **CONFIRMA** | I read Hayden–Lemm–Sorce, arXiv:2302.10208v2 (PRA 107, L050401), myself. Thm 1: for every α ∈ (0,2) there is ρ_ABC on C³⊗C³⊗C² with S_R^(α)(A:BC) < S_R^(α)(A:B). The states (2.1) are diagonal, so they are classical, and α = 1 is the reflected entropy.<br>The new title claims canonical purification, symmetry and S_R ≥ I. The body proves these: purity of the GNS vector gives symmetry, and S_R = I(11*:2) ≥ I(1:2) follows by strong subadditivity. The added sentence matches Thm 1 exactly.<br>Related work (l. 104) and `LEDGER.md` agree. No "monoton*" claim remains in the title, abstract or Zenodo description. |
| 2b | OBL-006 (Thm 3.4) sign | **CONFIRMA** | I read Kashiwara, Astérisque 130 (1985) 193–209 (Numdam), myself:<br>• §2.1: T*X is oriented by (dθ)^n;<br>• Thm 4.2: if {x ∈ supp F : φ(x) < t} is compact for every t and Y_φ ∩ SS(F) is compact, then χ(X;F) = (−1)^{n(n+1)/2} SS(F)·Y_φ;<br>• Ex. 8.5(i): c(χ_Y) = [T*_Y X].<br>With φ = 0, Y_φ is the zero section and both hypotheses hold because Ω is compact. The paper writes "≤ t" where the OCR shows "< t"; this is immaterial for compact Ω.<br>**Sign:** `L2r_obl006_sign.py` evaluates (dθ)^m on the base-then-fibre frame by an exact rational Pfaffian expansion, an oracle independent of the parity count. It gives (−1)^{m(m+1)/2} for m = 1..6; the Pfaffian routine is validated on Σdx∧dξ.<br>**Negative controls:** (−1)^{m(m−1)/2} differs at m = 1, 3, 5, and (−1)^m differs at m = 2, 3, 6.<br>**Constant-sheaf sanity case:** with the base-then-fibre self-intersection of the zero section equal to χ(Ω), the right-hand side is (−1)^{m(m+1)/2}·(−1)^{m(m+1)/2}·χ = χ. The unsigned pre-fix formula gives −2 for S² and S⁶ and −1 for RP². For odd m, χ = 0, so the base/fibre order does not matter.<br>Rem. 3.5 uses only multiplicities and is unaffected. KS Ch. IX is now cited only as a book reference, with no sign attributed to it; this is correct. |
| 3 | 10 random ADDED references (seed 20261007, 53 added) | **CONFIRMA** (0 mismatches) | Sample: FloerHofer1994, LiebRuskai1973, BlaberSivak2023, HaydenLemmSorce2023, Seifert2012, Srednicki1993, Viro1988, SchmiedlSeifert2007, Carlson1963, HaimKislevOstrover2026. All DOIs resolve and the metadata match; Annals 203(2) 603–622 is confirmed for Haim-Kislev–Ostrover.<br>**Cited claims:**<br>• HLS: full text (2a).<br>• Lieb–Ruskai: strong subadditivity.<br>• Schmiedl–Seifert: the moving laser trap, optimal protocols.<br>• Haim-Kislev–Ostrover: counterexample to Viterbo's volume–capacity conjecture.<br>• Srednicki: geometric spectrum of two coupled oscillators. This matches the PRL's opening example; I checked the Mehler value q = 1/9 at β = 0.6 by hand.<br>• Carlson 1963: R-function as a Dirichlet average and a symmetric form of F_D.<br>• Viro, Floer–Hofer, Seifert, Blaber–Sivak: the abstracts and titles match the sentences. |
| 4 | Declarations | **CONFIRMA** | Lean sentence exact, with no history. CAPES line, affiliation and competing interests are exact. The AI-use block is the standard one. The reference sentence names three items without a DOI, and the script finds exactly three: DLMF, Kashiwara1985, KawohlFridman2003. All 72 bibitems are cited and all keys are defined. |
| 5 | Title/abstract/introduction | **CONFIRMA** | The abstract and title are unchanged since the reference audit. The new Related-work paragraph contains attributions only. The new body remarks (Federer 4.21, Weyl/Steiner, von Renesse–Sturm, JKO) are cited facts and are marked as not used or as comparison. Cosmetic: l. 562 (proof of Thm 8.3) has "`\cite[Prop.~A.1]{Aamari2019}, (see also …)`", a stray comma before the parenthesis. |
| 6a | `CORRECTIONS_2026-10-06.md` | **PROBLEMA (blocking for the Zenodo note only)** | (i) The header says "**13 pages**"; the release has **16**.<br>(ii) Under "What still needs work", the first bullet says the KS theorem numbers and **Federer 4.8/4.18 were not checked**. The later references bullet says Federer 4.8/4.18 were checked in full text and KS 6.5.4/8.4.1/8.4.2 via secondary sources. The first bullet is now false for Federer and must be updated.<br>(iii) The "Flagged for an independent check: OBL-015 title, OBL-006 sign" sentence can now say "confirmed" (this report).<br>Theorem and remark numbers quoted in the note match the fresh build (Rem. 3.5, 4.5, 5.4, 6.3, 6.5, 7.2, 8.2; Props. 6.2, 7.3). |
| 6b | `ZENODO_DESCRIPTION_VOL3.md` | **CONFIRMA** | Accurate. It claims no monotonicity, and the holographic relation is a proposal. |
| 7 | Build (`audit/L2_final_build/`, pdflatex ×3) | **CONFIRMA** | Exit codes 0/0/0. 0 errors, 0 warnings, 0 overfull, 0 underfull, 0 undefined, 0 rerun. 16 pages. One pre-existing pdfTeX font-expansion notice. The shipped PDF text is identical to the fresh build. |

**Release-ready:** the PDF is ready. The version note needs the 6a (i)–(ii) edits, which a separate session should make.

## Closing
- **Hardest step:** OBL-006, the orientation bookkeeping. The sign depends only on Kashiwara's convention, which is verified in the source. The identity "self-intersection of the zero section = χ" in the base-then-fibre orientation is standard (Euler class), not re-derived numerically.
- **Literature (full text read):**
  - Kashiwara 1985 (Numdam AST_1985__130__193_0);
  - Hayden–Lemm–Sorce 2023 (arXiv:2302.10208, DOI 10.1103/PhysRevA.107.L050401).
