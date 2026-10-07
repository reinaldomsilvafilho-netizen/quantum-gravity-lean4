# BtS II: pre-release re-check, layer 2 (2026-10-07)

- **Checker:** independent Claude session (Opus). I wrote neither the volume, the reference audit nor `fixes_prerelease.md`. The works were not edited.
- **Inputs:**
  - the current `.tex`/PDF;
  - backups `_arquivo/backup_tex_2026-10-07/.../paper_geometric_measures_functional_tensors_prerelease.tex` and `_refs.tex`, both diffed;
  - `audit/references_audit.md` and `audit/fixes_prerelease.md`;
  - `CORRECTIONS_2026-10-06.md` and `ZENODO_DESCRIPTION_VOL2.md`.
- **Scripts** in `audit/scripts/`, all exiting 0:
  - `L2r_refs_sample.py`
  - `L2r_declarations_text.py`
  - `L2r_body_diff.py`
  - `L2r_build.py`
- **Processes:** none left. `processos_orfaos.py` reports 0 suspects.

## Verdicts

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 3 | 10 random ADDED references (seed 20261007; 45 added) | **CONFIRMA** (0 mismatches) | **Sample:** gordon1992one, ledoux1994simple, brenier1991polar, jordan1998variational, uhlmann1976transition, vandam2003which, sturm2023space, chan2003euler, helstrom1967minimum, chintakunta2015entropy. All DOIs resolve and the metadata match.<br>**Brenier:** the cited use (an optimal map pushing $\mu_0$ to $\mu_1$) needs $\mu_0$ absolutely continuous. That holds in Thm 2.6(a), where measures have densities $\rho$ of finite entropy on a bounded convex $\Omega$.<br>**Uhlmann:** "QFI = 4 × Bures metric from Uhlmann's fidelity" is the standard relation and is attributed correctly.<br>**Chan–Kang–Shen, Sturm (L^{2,q}-distortion, Alexandrov curvature ≥ 0), JKO, Ledoux/Buser, Gordon–Webb–Wolpert, van Dam–Haemers, Chintakunta:** abstracts or titles match the sentences.<br>**Helstrom 1967:** the SLD and quantum Fisher information attribution is standard, but the full text was not accessible (Elsevier). |
| 4 | Declarations | **CONFIRMA** | **Lean sentence:** exact, with no history.<br>**Standard text:** the CAPES line, affiliation, competing-interests statement and AI-use block match the standard text.<br>**References:** the "one book without a DOI" claim is true; only connes1994noncommutative lacks a DOI or arXiv id. All 68 bibitems are cited, and no key is undefined.<br>**Volume I citation:** the bibitem now says the Zenodo record holds all three volumes, as DataCite reports. |
| 5 | Title/abstract/introduction/conclusion | **CONFIRMA** | **Unchanged:** the abstract and title are the same as at the reference audit.<br>**Additions:** these are attributions or "not used" remarks:<br>• the introduction paragraph and Related work;<br>• Rem. 4.9 (Buser/Ledoux, "We do not use it");<br>• Peyre's bound;<br>• Visintin/Lombardini;<br>• Marques–Neves.<br>**Connes Thm 8 sentence:** "up to a normalizing constant, τ_d and τ_2^γ are the cochains of Connes Ch. IV §2 Thm 8, with γΦ(A₀) in the even case" is a relational claim. The reference audit checked it in the open full text, and it is consistent with the definitions at l. 654–658.<br>**Pointer:** "Part I of the monograph" agrees with the book, where Ch. 1, *Functional Realizations…*, is in Part I. |
| 6a | `CORRECTIONS_2026-10-06.md` | **PROBLEMA (blocking for the Zenodo note only)** | (i) The header says "**18 pages**". The release has **21**, which item 15 itself states.<br>(ii) "What still needs work" lists **AGS Thm 8.3.1, Hörmander §8.1–8.2 and the Connes trace-theorem normalization** as not checked in full text. Item 15 says they are "now checked in the source text". The bullet contradicts it and must be updated.<br>(iii) That list omits sources the reference audit still marks as not checked in full text: **McCann 1997, von Renesse–Sturm 2005, Visintin 1991 (only via Lombardini), Petz 1996**. Add them, or drop the list.<br>**Numbers:** the theorem numbers quoted in the note match the fresh build: Thm 2.3, 2.6, 3.6, 7.3; Rem. 3.7, 4.3, 5.5, 7.4; Props. 4.4, 4.5, 5.4, 6.2, 6.4; Lemma 7.2. |
| 6b | `ZENODO_DESCRIPTION_VOL2.md` | **CONFIRMA** | Still accurate. The reference expansion added no results. |
| 7 | Build (`audit/L2_final_build/`, pdflatex ×3) | **CONFIRMA** | **Runs:** exit codes 0/0/0. 0 errors, 0 warnings, 0 overfull, 0 underfull, 0 undefined, 0 rerun.<br>**Output:** 21 pages, with no pdfTeX notices. The shipped PDF text is identical to the fresh build. |

**Release-ready:** the PDF is ready. The version note needs the edits in 6a (i)–(iii), made by a separate session.
