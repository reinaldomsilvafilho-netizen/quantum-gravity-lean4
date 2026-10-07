# Functorial Tensor Field Theory: pre-release re-check, layer 2 (2026-10-07)

- **Checker:** an independent Claude session (Opus). I wrote neither the paper, the reference audit nor `fixes_prerelease.md`. I did not edit the work.
- **Inputs:**
  - the current `.tex` and PDF;
  - the backups `_arquivo/backup_tex_2026-10-07/.../paper_functorial_tensor_field_theory_prerelease.tex` and `_arquivo/backup_tex_2026-10-06/.../paper_functorial_tensor_field_theory_refs.tex`, both diffed;
  - `audit/references_audit.md` and `audit/fixes_prerelease.md`;
  - `CORRECTIONS_2026-10-06.md` and `ZENODO_DESCRIPTION.md`.
- **Scripts** (in `audit/scripts/`, all exit 0): `L2r_refs_sample.py`, `L2r_declarations_text.py`, `L2r_body_diff.py`, `L2r_build.py`.
- **Processes:** none left; `processos_orfaos.py` finds 0 suspects.

## Verdicts

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 3 | 10 randomly chosen ADDED references (seed 20261007; 34 were added) | **CONFIRMA** (0 mismatches) | **Sample:** gourgoulhon2012, miyaji2015, baezdolan1995, curiel2017, israel1966, selinger2007, uhlmann1976, provost1980, haegeman2014geometry, mohr2025codata.<br>**Identifiers:** all resolve, and the metadata match.<br>**Cited claims:**<br>• Miyaji et al.: "gravity dual approximately the volume of a maximal time slice" matches the abstract.<br>• Haegeman et al. 2014: principal fibre bundle with a Kähler base, as in the abstract.<br>• Baez–Dolan: the extended-TQFT/cobordism programme.<br>• Israel: thin shells characterized by extrinsic curvature (standard; full text not accessible).<br>• Provost–Vallée and Uhlmann: attribution-level claims that match the titles.<br>• CODATA 2022: ℓ_P = 1.616255×10⁻³⁵ m gives ℓ_P² = 2.612×10⁻⁷⁰ m², as stated, and dimensions agree.<br>• Gourgoulhon Ch. 4 (ADM form) and Ch. 5 (constraints): the displayed constraints R + K² − K_ijK^ij − 2Λ = 16πGρ and ∇_j(K^j_i − δ^j_iK) = 8πG j_i agree with the 3+1 equations for Λ = 0, G = 1 (sign conventions K = −∇n).<br>• Curiel §2.1 and Selinger Def. 2.6: I did not re-read these; I rely on the layer-1 full-text check in the reference audit. |
| 4 | Declarations | **CONFIRMA** | The Lean sentence is exact and has no history. The CAPES line, affiliation, competing interests and AI-use block are standard. "For the one book without a DOI, its ISBN record" is true: brown2006 is the only bibitem without a DOI or arXiv id. All 42 bibitems are cited. |
| 5 | Title/abstract/introduction/conclusion | **CONFIRMA** | The title and abstract are unchanged since the reference audit. The Related-work subsection is attribution only, and "Here, in contrast, …" describes the construction without claiming a result. Every new sentence in the open problems (Geroch, Borde, Gibbons–Hawking, Selinger, cobordism hypothesis) is cited context, and none claims anything proved here. |
| 6a | `CORRECTIONS_2026-10-06.md` | **CONFIRMA** (minor) | **Numbering:** every theorem, proposition, remark and open-problem number in the note matches the fresh build: Props. 2.3, 3.1, 3.2, 4.2–4.4, 6.2–6.4, 6.7; Lemmas 2.4, 2.8; Cor. 2.6, 5.5; Thm 5.4; Rem. 2.7, 3.3, 5.6, 6.6, 6.8; Ex. 6.1; Open problems 7.1–7.4.<br>**Counts and fixes:** the counts (8 → 42) and the pre-release fix are recorded correctly.<br>**Cosmetic:**<br>• the 2026-10-07 pre-release bullet sits under "## Scripts";<br>• "Segal removed … no longer cited" is followed later by "Segal is cited again". This is consistent, but a reader may stumble on it.<br>Neither point blocks release. |
| 6b | `ZENODO_DESCRIPTION.md` | **CONFIRMA** | Still accurate. The Lean sentence there ("accompanied the first version") is version history, which is allowed on the landing page. |
| 7 | Build (`audit/L2_final_build/`, pdflatex ×3) | **CONFIRMA** | Exit codes 0/0/0. 0 errors, 0 warnings, 0 overfull, 0 underfull, 0 undefined, 0 rerun. 13 pages, no pdfTeX notices. The text of the shipped PDF is identical to the fresh build. |

**Release-ready: yes.** Optionally, move the 2026-10-07 bullet out of "## Scripts".
