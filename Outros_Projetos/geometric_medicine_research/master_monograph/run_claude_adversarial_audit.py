#!/usr/bin/env python3
"""
================================================================================
AUTONOMOUS CLAUDE CODE CLI ADVERSARIAL AUDITOR (MAXIMAL POTENCY MODE)
Target: Geometric Medicine and Quantum Biophysics (Master Monograph - 27 Pillars)
Protocol: Piped Stdin IPC (Zero WinError 206) + Heartbeat + Milestone Monitoring
================================================================================
"""

import os
import sys
import time
import shutil
import subprocess
import threading
from datetime import datetime

# Base Paths
REPO_DIR = r"c:\Users\monar\Documents\antigravity\resilient-turing"
MED_DIR = os.path.join(REPO_DIR, "geometric_medicine_research")
BOOK_DIR = os.path.join(MED_DIR, "master_monograph")
MASTER_TEX = os.path.join(BOOK_DIR, "treatise_geometric_medicine_master_volume.tex")
MASTER_PDF = os.path.join(BOOK_DIR, "treatise_geometric_medicine_master_volume.pdf")
REPORT_MD = os.path.join(BOOK_DIR, "CLAUDE_ADVERSARIAL_AUDIT_REPORT.md")
LOG_FILE = os.path.join(BOOK_DIR, "claude_adversarial_audit.log")

# Skills Directory
SKILLS_DIR = r"C:\Users\monar\.gemini\config\skills"

# Catalog of domain skills to provide to Claude
SKILLS_CATALOG = {
    "Medical & Biomedical Intelligence": [
        ("medical-research", os.path.join(SKILLS_DIR, "medical-research", "SKILL.md"), "PubMed retrieval, disease treatments, and clinical trial evidence synthesis"),
        ("pubmed-database", os.path.join(SKILLS_DIR, "pubmed-database", "SKILL.md"), "NCBI E-utilities, PMC BioC, medical spelling, and compound-gene literature linking"),
        ("bioinformatics-fundamentals", os.path.join(SKILLS_DIR, "bioinformatics-fundamentals", "SKILL.md"), "SAM/BAM, variant filtering, Hi-C/HiFi sequencing, and assembly coordinates"),
        ("genomic-coordinates", os.path.join(SKILLS_DIR, "genomic-coordinates", "SKILL.md"), "Coordinate transforms (0-based vs 1-based), variant normalization, and HGVS formatting"),
        ("jaspar-database", os.path.join(SKILLS_DIR, "jaspar-database", "SKILL.md"), "Transcription factor binding profiles, PWMs, and position frequency matrices"),
        ("encode-ccres-database", os.path.join(SKILLS_DIR, "encode-ccres-database", "SKILL.md"), "SCREEN GraphQL API and ENCODE Registry of cis-Regulatory Elements"),
        ("biomedical-search", os.path.join(SKILLS_DIR, "biomedical-search", "SKILL.md"), "Valyu semantic biomedical search across preprints, trials, and FDA drug labels"),
        ("medical-imaging-review", os.path.join(SKILLS_DIR, "medical-imaging-review", "SKILL.md"), "Medical imaging AI review methods, risk-of-bias appraisal, and evidence synthesis"),
    ],
    "Literature Grounding & Citation Authenticity": [
        ("math-physics-references", os.path.join(SKILLS_DIR, "math-physics-references", "SKILL.md"), "Interdisciplinary vocabulary bridges (arXiv, INSPIRE-HEP, zbMATH, Crossref) and attribution auditing"),
        ("citation-verification", os.path.join(SKILLS_DIR, "citation-verification", "SKILL.md"), "Programmatic citation checking, fake reference detection, and canonical metadata resolution"),
        ("nature-citation", os.path.join(SKILLS_DIR, "nature-citation", "SKILL.md"), "Strict Nature/CNS/Cell reference linking and claim-level verification"),
        ("scholarly-metadata-resolver", os.path.join(SKILLS_DIR, "scholarly-metadata-resolver", "SKILL.md"), "Automated canonical DOI, ISBN, and persistent identifier resolver"),
        ("literature-search-arxiv", os.path.join(SKILLS_DIR, "literature-search-arxiv", "SKILL.md"), "arXiv full-text query, e-print verification, and mathematical preprint analysis"),
    ],
    "Mathematical Rigor, Theoretical Physics & Numerical Proofs": [
        ("claude-adversarial-audit", os.path.join(SKILLS_DIR, "claude-adversarial-audit", "SKILL.md"), "Autonomous Claude CLI adversarial red-teaming and proof obligation verification"),
        ("adversarial-proof-synthesizer", os.path.join(SKILLS_DIR, "adversarial-proof-synthesizer", "SKILL.md"), "Counterexample red-teaming, boundary condition checks, and obligation DAGs"),
        ("triadic-proof-verifier", os.path.join(SKILLS_DIR, "triadic-proof-verifier", "SKILL.md"), "Dual LaTeX/Lean 4 audit, numerical inverse testing, and mutation testing"),
        ("fractional-calculus-pde", os.path.join(SKILLS_DIR, "fractional-calculus-pde", "SKILL.md"), "Non-local fractional Laplacians (-Delta)^alpha, Beta-Laplacians, and Mittag-Leffler propagators"),
        ("tensor-network-computing", os.path.join(SKILLS_DIR, "tensor-network-computing", "SKILL.md"), "Matrix Product States (MPS), DMRG, and tensor variety contractions"),
        ("non-euclidean-optimization", os.path.join(SKILLS_DIR, "non-euclidean-optimization", "SKILL.md"), "Optimization on Riemannian manifolds, Fisher-Rao geometry, and natural gradients"),
        ("scientific-computing-python", os.path.join(SKILLS_DIR, "scientific-computing-python", "SKILL.md"), "Numerical analysis, floating-point error bounds, and inverse process testing"),
        ("zenodo-monograph-publisher", os.path.join(SKILLS_DIR, "zenodo-monograph-publisher", "SKILL.md"), "Open-science treatise compilation, institutional metadata, and Git hygiene"),
    ]
}

def find_claude_executable():
    """Locate the Claude CLI executable on Windows."""
    candidates = [
        r"C:\Users\monar\AppData\Roaming\npm\claude.cmd",
        r"C:\Users\monar\AppData\Local\Programs\claude\claude.exe",
        shutil.which("claude.cmd"),
        shutil.which("claude"),
        shutil.which("claude.exe"),
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    return "claude"

def build_skills_reference_text():
    """Format the skills inventory for Claude's audit prompt."""
    lines = []
    lines.append("## SYSTEM SPECIALIZED SKILLS DIRECTORY & TOOLING REFERENCE")
    lines.append("You have access to specialized skills and reference databases on this machine. You MUST consult and cross-reference these skills during your audit:\n")
    for category, skills in SKILLS_CATALOG.items():
        lines.append(f"### {category}")
        for name, path, desc in skills:
            exists_mark = "[AVAILABLE]" if os.path.exists(path) else "[PATH SPECIFIED]"
            lines.append(f"- **{name}** {exists_mark}: `{path}`\n  *Focus:* {desc}")
        lines.append("")
    return "\n".join(lines)

def build_adversarial_prompt():
    """Assemble the exhaustive, maximal-potency adversarial audit prompt."""
    skills_text = build_skills_reference_text()
    
    prompt = """You are the Lead Adversarial Auditor, Senior Theoretical Biophysicist, and Differential Geometer conducting a MAXIMAL POTENCY, UNCOMPROMISING ADVERSARIAL AUDIT of the completed master volume:

================================================================================
MONOGRAPH TITLE: GEOMETRIC MEDICINE AND QUANTUM BIOPHYSICS
Author: Reinaldo Maia Silva-Filho (Universidade Federal de Lavras - UFLA)
Master LaTeX File: `<<MASTER_TEX>>`
Master Compiled PDF: `<<MASTER_PDF>>`
Total Pages: 121 pages across 6 Parts and 27 Pillars
Computational Engine: 135/135 passing test batteries (0 failures)
Parent Theoretical Physics Treatise: DOI 10.5281/zenodo.22290043
Hardcover Mathematics Monograph: ISBN 978-65-87456-12-8
================================================================================

<<SKILLS_TEXT>>

## CONTEXT OF RECENT REVISION & SYSTEMATIC REMEDIATION:
A rigorous remediation pass was conducted following the preliminary audit:
1. Chapter 24 (Prion Eyring Kinetic Barrier): Corrected the uncatalyzed activation barrier to $\Delta G_0^\ddagger = 40.15$ kcal/mol, which accurately yields $k_{\text{uncat}} \approx 3.3 \times 10^{-16}\text{ s}^{-1} \approx 1.04 \times 10^{-8}\text{ year}^{-1}$. An explicit 80-year human lifetime test (`incubation_days = 365.25 * 80`) was added to `verify_numerical.py`, confirming spontaneous conversion is $\approx 8.3 \times 10^{-7}$ (matching the real $\sim 1\text{--}2$ per million annual sCJD incidence).
2. Chapter 18 (TRD Manifold): Replaced the misnomer "scalar curvature" for $\frac{1}{N^2}\operatorname{Tr}(\mathbf{\Sigma}^{-2})$ with "Fisher-Rao Information Spectral Sensitivity Index" and added foundational citations to Skovgaard (1984) and Amari \& Nagaoka (2000).
3. Chapter 19 (Refractory Epilepsy ECoG): Replaced the artificial $0.0$ mm localization artifact with realistic $0.48$ mm empirical resolution ($\mathrm{AUC} = 0.991$).
4. Foundational Attributions Added: Cites Sarkar (2011) for Chapter 11 (hyperbolic tree embeddings); Barachant et al. (2013) and Congedo et al. (2017) for Chapter 20 (Riemannian BCI); Zarate et al. (2006) for Chapter 18 (ketamine). Consolidated duplicate treatise bibkeys.
5. Epistemological Humility & Sober A1 Journal Framing: All 27 benchmark cohorts are explicitly and transparently designated as controlled \emph{in silico} simulation benchmarks. All hyperbolic and triumphalist prose ("unprecedented", "definitive", "completely eliminates", "holy grail", etc.) has been purged. The Preface and Synthesis include a formal section on Epistemological Humility, Modeling Assumptions, Known Limitations, and a 4-Phase Translational Roadmap.

## YOUR AUDIT MISSION & OPERATING DIRECTIVE:
You are operating in MAXIMUM REASONING MODE with EXTREME ADVERSARIAL DEPTH. Do NOT produce polite pleasantries or surface-level summaries. Your explicit mission is to vigorously stress-test, scrutinize, red-team, and attack every single mathematical equation, proof step, biophysical model, clinical dosage, unit conversion, and citation claim across all 27 chapters of this book. Verify whether the recent remediations successfully resolve prior critical objections, and provide a definitive, rigorous evaluation of the monograph's scientific integrity, mathematical rigor, and A1 journal readiness.

### THE 27 PILLARS TO SCRUTINIZE ACROSS ALL 6 PARTS:
1. Part I: Global Health Challenges & Chronic Complex Diseases (Chapters 1-7)
   - Ch 01: Multi-Ancestry Geometric Polygenic Risk Scores (Moreau-Yosida envelopes, linkage disequilibrium)
   - Ch 02: Curvature-Informed Geometric Langevin Diffusion for ctDNA Liquid Biopsy (Ricci drift, Cramér-Rao)
   - Ch 03: Affine-Invariant Riemannian Connectomics on Cartan-Hadamard Manifolds (Alzheimer's, d_AI geodesics)
   - Ch 04: Non-Local Fractional Porous Diffusion on Complex Networks for AMR (Mittag-Leffler, biofilm percolation)
   - Ch 05: Fisher-Rao Information Geometry on DNA Methylation Manifolds (Horvath epigenetic aging clock)
   - Ch 06: Fractal Alveolar Resolvents and Non-Local Gas Diffusion in Pulmonary Fibrosis (Kigami Dirichlet form)
   - Ch 07: Multi-Locus HLA Information Geometry and Geodesic Cox Survival Modeling (Kidney transplantation)

2. Part II: Tropical Diseases, Global Virology & Rational Vaccinology (Chapters 8-13)
   - Ch 08: Non-Local Fractional Vector-Host Dynamics & Antibody-Dependent Enhancement (Dengue, fractional SEIR)
   - Ch 09: Fractal Microvascular Resolvents & Antigenic Variation Dynamics in Malaria (PfEMP1 var switching)
   - Ch 10: Riemannian Manifolds of Myocardial Strain Tensors & Vectorcardiography (Chagas, Leishmaniasis)
   - Ch 11: Hyperbolic Antigenic Cartography on Poincaré Space Forms (Flaviviruses, HIV-1, Influenza)
   - Ch 12: Minimax Extrinsic Curvature on Glycoprotein Submanifolds & Rational Vaccine Design (Glycan shield)
   - Ch 13: Non-Local Fractional Metapopulation Diffusion & Ollivier-Ricci Curvature (Epidemic early warning)

3. Part III: Maternal, Neonatal & Pediatric Global Health (Chapters 14-17)
   - Ch 14: Minimax Extrinsic Curvature on Alveolar Surfactant Interfaces in Prematurity (Laplace-Young, reach)
   - Ch 15: Riemannian Manifolds of Uterine Spiral Artery Impedance & Ricci Remodeling in Preeclampsia
   - Ch 16: Continuous Simplicial Fractional Laplacians & Dirichlet-Barnes Deconvolution for Neonatal IEMs
   - Ch 17: Simplicial Fractional Diffusion & Ecological Basin Bifurcations in Childhood Stunting (Gut-brain axis)

4. Part IV: Computational Neuroscience, Mental Health & Neurotechnology (Chapters 18-20)
   - Ch 18: Fisher-Rao Information Geometry of DMN Attractors in Treatment-Resistant Depression
   - Ch 19: Optimal Transport Divergence & Gauge Holonomies on ECoG Manifolds in Refractory Epilepsy
   - Ch 20: Affine-Invariant Riemannian Geodesics on Covariance Manifolds for Stroke BCI Rehabilitation

5. Part V: Quantum Pharmacology & Molecular Therapeutics (Chapters 21-23)
   - Ch 21: Minimax Extrinsic Curvature on Constrained Submanifolds & Moreau-Yosida PPI Barriers (KRAS, MYC)
   - Ch 22: Tensor Network Matrix Product States & Variational DMRG for Quantum Ligand Affinity
   - Ch 23: Population Pharmacogenomics, CYP450 Multi-Ethnic Manifolds & Bakry-Émery Ricci Floors

6. Part VI: Prion Diseases, TSEs & Creutzfeldt-Jakob Disease (Chapters 24-27)
   - Ch 24: Variational Landau-Ginzburg Free Energy Landscapes & Catalytic Barrier Collapse in PrP Conversion
   - Ch 25: Non-Linear Nucleated Polymerization Kinetics & Curvature-Induced Fibril Fragmentation (sCJD)
   - Ch 26: Anomalous Fractional Diffusion on the Human Brain Connectome, Cortical Ribboning & RT-QuIC
   - Ch 27: Minimax Extrinsic Curvature End-Capping Peptidomimetics & Pharmacological Chaperones for sCJD

---

### ADVERSARIAL DEFECT TAXONOMY (SCRUTINIZE EACH CHAPTER AGAINST ALL 7 CLASSES):
1. [INV-01] CRITICAL: False mathematical claim, unproven step, sign error, invalid dimensional factor, or mathematical counterexample.
2. [GAP-02] MAJOR: Logical non-sequitur, unjustified asymptotic limit (e.g. t -> infty, n -> infty), missing inferential bounds, or unproved regularity transfer.
3. [UNC-03] MAJOR: Undefined function space (e.g. H^s vs W^{{k,p}}), missing boundary conditions, lack of domain compactness, or unverified operator domain self-adjointness.
4. [VAC-04] CRITICAL: Vacuous antecedent implication (False => P), trivialization where bounds hold trivially by 0 <= 0, or parameter regime devoid of physical meaning.
5. [CIRC-05] CRITICAL: Circular reasoning, defining quantities in terms of the results they purport to prove, or unphysical parameter tuning to match benchmarks.
6. [TYPO-06] MINOR: LaTeX syntax inconsistencies, floating table placement issues, unescaped macros, or punctuation glitches.
7. [NOT-07] MINOR: Notation collision (e.g. using lambda for both eigenvalue and regularization parameter in the same chapter without disambiguation).

---

### DOMAIN-SPECIFIC CLINICAL & BIOPHYSICAL VERIFICATION:
- **Biochemical & Thermodynamic Realism:**
  * Free energy barriers Delta G^ddagger (are they compatible with physiological timescales: 15-30 kcal/mol for spontaneous folding vs sub-second catalysis?).
  * Binding affinities K_d (are the picomolar and nanomolar claims realistic for macrocycles and peptidomimetics?).
  * Dissociation and fragmentation constants (are k_n, k_p, k_- consistent with Knowles-Griffith experimental ranges for amyloid and prion fibrils?).
- **Clinical Relevance:**
  * Diagnostic latency (does RT-QuIC kinetics reflect 24-48h CSF assays?).
  * EEG and ECoG sampling frequencies and matrix dimensions in Riemannian BCI (do they match standard 64-128 channel arrays?).
  * Pharmacokinetic concentrations and enzyme kinetics (CYP2D6, CYP2C19 clearance profiles in admixed cohorts).
- **Physical Constants & Dimensions:**
  * Verify consistency of physical constants: hbar, k_B, c, G_N.
  * Check every equation for dimensional homogeneity (energy, time^-1, length^-1, curvature units m^-1).

---

### DELIVERABLE REQUIREMENTS:
1. Examine `<<MASTER_TEX>>` thoroughly.
2. Generate an exhaustive, publication-grade markdown audit report and save it to:
   `<<REPORT_MD>>`
3. The report must contain:
   - **Executive Verdict:** [PASS / MINOR REVISION / MAJOR REVISION] with clear, definitive rationale.
   - **Obligation Disposition Table:** Comprehensive table listing each Chapter (1-27), the core theorems/models scrutinized, the defects identified (or confirmed absent), and remediation notes.
   - **Detailed Chapter-by-Chapter Scrutiny:** Specific section-by-section breakdown of findings, strengths, vulnerabilities, and exact mathematical/clinical recommendations.
   - **Literature & Reference Audit:** Cross-referencing against the canonical tools outlined in `math-physics-references`, `citation-verification`, and `pubmed-database`.
   - **Formal Anti-Vacuity & Computational Soundness Assessment:** Evaluation of the 135 numerical test batteries and theoretical physics integration.

Proceed with the exhaustive audit now.
"""
    prompt = prompt.replace("<<MASTER_TEX>>", MASTER_TEX)
    prompt = prompt.replace("<<MASTER_PDF>>", MASTER_PDF)
    prompt = prompt.replace("<<SKILLS_TEXT>>", skills_text)
    prompt = prompt.replace("<<REPORT_MD>>", REPORT_MD)
    return prompt

def run_claude_audit():
    print("=" * 80)
    print("STARTING AUTONOMOUS CLAUDE ADVERSARIAL AUDITOR (MAXIMAL POTENCY)")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target Master Monograph: {MASTER_TEX}")
    print(f"Target Compiled PDF: {MASTER_PDF}")
    print(f"Skills Directory: {SKILLS_DIR}")
    print("=" * 80)

    # 1. Verify target existence
    if not os.path.exists(MASTER_TEX):
        print(f"[ERROR] Master TeX file does not exist: {MASTER_TEX}")
        sys.exit(1)
    if not os.path.exists(MASTER_PDF):
        print(f"[WARNING] Master PDF does not exist yet at {MASTER_PDF}. Compilation should be verified.")

    # 2. Locate Claude CLI
    claude_bin = find_claude_executable()
    print(f"[STATUS] Claude CLI binary resolved: {claude_bin}")

    # 3. Build prompt
    print("[STATUS] Assembling maximal potency prompt with skills inventory...")
    prompt_text = build_adversarial_prompt()
    print(f"[STATUS] Prompt prepared ({len(prompt_text)} characters, {len(prompt_text.splitlines())} lines).")

    # 4. Open log file
    log_f = open(LOG_FILE, "w", encoding="utf-8")
    log_f.write(f"=== CLAUDE ADVERSARIAL AUDIT EXECUTION LOG ===\nStarted: {datetime.now()}\n\n")
    log_f.flush()

    # 5. Spawn Claude subprocess with piped stdin IPC
    cmd = [claude_bin, "-p", "--dangerously-skip-permissions"]
    print(f"[STATUS] Spawning subprocess: {' '.join(cmd)} (Piped stdin IPC)")

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            cwd=BOOK_DIR,
            env=env
        )
    except Exception as e:
        print(f"[CRITICAL ERROR] Failed to spawn Claude CLI: {e}")
        log_f.write(f"Failed to spawn Claude CLI: {e}\n")
        log_f.close()
        sys.exit(1)

    # 6. Stream prompt to stdin and close to signal EOF
    print("[STATUS] Writing prompt payload to stdin pipe...")
    try:
        proc.stdin.write(prompt_text)
        proc.stdin.close()
        print("[STATUS] stdin pipe closed. Prompt successfully transmitted.")
    except Exception as e:
        print(f"[ERROR] Failed writing to stdin pipe: {e}")
        log_f.write(f"Failed writing to stdin: {e}\n")
        proc.kill()
        sys.exit(1)

    # 7. Asynchronous output streamer thread
    stdout_buffer = []
    stderr_buffer = []

    def stream_reader(pipe, buf, prefix, log_handle):
        for line in iter(pipe.readline, ""):
            buf.append(line)
            try:
                log_handle.write(f"[{prefix}] {line}")
                log_handle.flush()
            except Exception:
                pass
            try:
                safe_line = line.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(sys.stdout.encoding or "utf-8", errors="replace")
                sys.stdout.write(f"[{prefix}] {safe_line}")
                sys.stdout.flush()
            except Exception:
                pass
        pipe.close()

    t_out = threading.Thread(target=stream_reader, args=(proc.stdout, stdout_buffer, "CLAUDE", log_f))
    t_err = threading.Thread(target=stream_reader, args=(proc.stderr, stderr_buffer, "STDERR", log_f))
    t_out.daemon = True
    t_err.daemon = True
    t_out.start()
    t_err.start()

    # 8. 30-second Initial Heartbeat Check
    print("\n[MONITOR] Entering initial 30-second health check window...")
    start_time = time.time()
    time.sleep(30)

    ret = proc.poll()
    if ret is not None and ret != 0:
        print(f"[FAILURE] Claude CLI exited prematurely within 30s with returncode: {ret}")
        print("Stderr tail:")
        print("".join(stderr_buffer[-20:]))
        log_f.close()
        sys.exit(ret)
    else:
        print(f"[HEARTBEAT PASS] Subprocess alive at T=30s. Output buffer has {len(stdout_buffer)} lines.")

    # 9. Milestone Polling Loop (every 60s, up to 1800s timeout)
    timeout_sec = 1800
    poll_interval = 60
    while True:
        elapsed = int(time.time() - start_time)
        ret = proc.poll()
        if ret is not None:
            print(f"\n[COMPLETE] Claude auditor terminated with exit code {ret} after {elapsed}s.")
            break
        if elapsed > timeout_sec:
            print(f"\n[TIMEOUT] Reached max timeout of {timeout_sec}s. Terminating process.")
            proc.kill()
            break
        print(f"[POLL T={elapsed}s] Process active | Output lines: {len(stdout_buffer)} | Active thread alive.")
        time.sleep(poll_interval)

    t_out.join(timeout=5)
    t_err.join(timeout=5)
    log_f.write(f"\nExecution finished at: {datetime.now()}\n")
    log_f.close()

    # 10. Post-Execution Harvest
    full_output = "".join(stdout_buffer)
    if os.path.exists(REPORT_MD):
        rep_size = os.path.getsize(REPORT_MD) / 1024
        print("\n" + "=" * 80)
        print(f"SUCCESS! Claude Adversarial Audit Report generated at:")
        print(f"  {REPORT_MD} ({rep_size:.1f} KB)")
        print("=" * 80)
    else:
        if len(full_output.strip()) > 500:
            with open(REPORT_MD, "w", encoding="utf-8") as f:
                f.write(full_output)
            print("\n" + "=" * 80)
            print(f"Harvested Claude stdout into Report at:")
            print(f"  {REPORT_MD} ({len(full_output)/1024:.1f} KB)")
            print("=" * 80)
        else:
            print(f"[WARNING] No report file detected and stdout buffer too short ({len(full_output)} chars).")
            print("Check log file:", LOG_FILE)

if __name__ == "__main__":
    run_claude_audit()
