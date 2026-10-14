# Agent protocol: token economy and model routing

Goal: spend the expensive model on hard thinking, the cheap models on mechanics, and never pay twice for the same context. Read this before launching agents.

## 1. Model routing

| Task | Model | Why |
|---|---|---|
| Build PDFs, run scripts, grep, count, copy, list files, git status | none (run it directly) or `haiku` | Mechanical; no judgement |
| Resolve DOIs, check bibliography metadata, update WORKPLAN statuses, lint LaTeX | `haiku` | Deterministic checks |
| House-style sweeps (revision-history wording, `audit/` paths), title/cross-ref consistency | `haiku` → `sonnet` if edits are needed | Pattern work, then small edits |
| Literature search and summaries, prior-art notes | `sonnet` | Reading and summarising |
| Write numerical check scripts (oracle + negative control), regenerate figures | `sonnet` | Standard scientific coding |
| Fix severity-B items (wording, citations, small restatements) | `sonnet` | Local edits with checks |
| Blind referee of a chapter (layer 1), layer-2 re-check of *new proofs* | `opus` | Must find subtle errors |
| Fix severity-A/M items, write new proofs, restate conjectures | `opus` | Mathematical judgement |
| Second-model check of severity-A items | Gemini (outside Claude) with `audit/verify/PROTOCOL.md` | Decorrelates errors |
| Lean batch writer | `opus` or `fable`; the L2 reviewer must be the **other** model | Pilot round 2: Fable writer at the same level as Opus; its one subtle slip (real vs complex projector) was caught by the Opus reviewer |
| Blind L1 of a new proof | **two in parallel, one `opus` and one `fable`**, separate files, no reading of DIARIO while working | Pilot round 3 (S23): identical verdicts, independent certificates |
| Lean L2 fidelity review | `fable` or `opus`, alternating; **both in parallel** for high-risk batches (new proof, book finding) | Pilot 2026-10-10 (`formal_proofs_mathlib/PILOTO_FABLE.md`): same quality and cost, complementary findings; uses the separate Fable quota |

Rule of thumb: if a wrong answer would be caught by the next automatic check (compile, script, Crossref), use the cheap model. If a wrong answer would silently enter the text, use the strong one.

## 2. Spending rules

1. **At most 2 agents in parallel** when the weekly quota is below ~30%; 4 only with plenty of quota. Run `python build_pdfs_safe.py` before any long pause (it never overwrites a good PDF).
2. **Resume, don't restart.** An agent interrupted by a limit keeps its context; resume it with a one-paragraph message. Its work on disk stays valid.
3. **Short hand-backs.** Every agent prompt ends with: "Reply in ≤ 150 words: verdict counts, then one line per PROBLEM/INCERTO. Details go in the file you write." Full reports live in files; the main session reads only the summary.
4. **Scoped reading.** Agents read only the files named in the prompt. Use `grep`/line ranges instead of whole chapters when the task is local. Never paste a chapter into a prompt; give the path.
5. **Batch edits.** Several edits to one file → one script or one Edit sequence, then one compile. Compile each chapter at the end, not after every edit.
6. **No duplicate work.** Before launching, check `audit/verify/` and WORKPLAN §3 for an existing report on the same item.
7. **Cheap verification first.** Run the existing scripts (`audit/verify/scripts/*.py`) before asking a model to re-derive something.
8. **Main session stays light.** The main session plans, launches, consolidates statuses and talks to the author. It does not re-read reports that agents already summarised.

## 3. Compression and hand-off

- **Single entry point.** `CLAUDE.md` (repo root) is the compact state of the project: what it is, where things are, conventions, current status, next steps. Keep it under ~2 pages. Update its "Current status" and "Next steps" at the end of each working day.
- **Registers instead of history.** Status lives in WORKPLAN §3 (one row per finding); details live in `audit/verify/*.md`; the CHANGELOG holds what changed per release. Do not repeat these in chat or in CLAUDE.md; link to them.
- **Context packs for hard tasks.** When a task needs several chapters, first ask a `sonnet` agent to write a compressed pack (definitions, statements, notation, ≤ 1 page per chapter) in `audit/packs/`. Then check it against the source for losslessness on the statements used (skill `high-density-math-compressor`). The `opus` agent then reads the pack plus only the passages it must edit.
- **Stable prompts.** Reuse the prompt templates below instead of writing new ones; they already encode the rules.

## 4. Prompt templates (fill the brackets)

**Task skills (added 2026-10-10).** Every agent prompt starts with "Read and follow `C:\Users\monar\.claude\skills\<skill>\SKILL.md`". The index, with model choice and limits, is `gtqg-orquestrador`. The task skills are:
- `gtqg-tarefa-latex`;
- `gtqg-tarefa-python`;
- `gtqg-tarefa-lean` (role A writer, role B reviewer);
- `gtqg-tarefa-revisao`;
- `gtqg-tarefa-referencias`;
- `gtqg-tarefa-publicacao`.

They hold the step-by-step procedure and every past failure. The templates below only add the task details. Add each new failure mode to the matching skill.

**Blind referee (opus):**
"Independent referee. Read `audit/verify/PROTOCOL.md` (Camada 1). Chapter: [file]. Do not read ledgers, WORKPLAN, CHANGELOG, other reports. Write only in `audit/verify/`. Save scripts as `audit/verify/scripts/[chNN]_*.py` with negative controls. Report: `audit/verify/[chNN]_blind.md`. Reply in ≤ 150 words."

**Corrector (opus for A/M, sonnet for B):**
"You did not write this text. Inputs: [reports]. Edit only [files]. Verify each item before changing; record disagreements. House style: current mathematics only, no revision history, no `audit/` paths. New DOIs via Crossref. Edit LaTeX with Edit or saved scripts; avoid parentheses in shell args (cmd.exe hook). Compile 3×: 0 errors/warnings/overfull/undefined. Log: `audit/verify/fixes_[tag].md`. Reply in ≤ 150 words."

**Layer-2 re-check (opus for new proofs, sonnet for text fixes):**
"You wrote neither the text nor the fixes. Read PROTOCOL.md, the reports [..], the fix log [..], the current files [..]. For each item: resolved? correct? mutation test on every numerical claim; no over-correction; DOIs; house style. Output `audit/verify/L2_[tag].md`; a finding is verified only if all items CONFIRMA. Reply in ≤ 150 words."

**Mechanical (haiku):**
"Run [command] in [dir] and report only: [the exact numbers/lines needed]. Do not edit files."

## 5. Environment notes (Windows)

- A hook routes shell commands through cmd.exe: no parentheses in command-line arguments; put data in files.
- Git Bash heredocs collapse `\\`: never write LaTeX through heredocs.
- A stray `bisect.py` in the session scratchpad can shadow the stdlib: run Python from the project folders.
- `taskkill /IM python.exe` kills every Python process on the machine; do not use it.

## 5b. Publication pipeline (learned 2026-10-06)
1. **Correctness:**
   - blind review (layer 1);
   - correction by another session;
   - layer 2.

   Any new proof written by a corrector gets its own re-check (layer 2b). On 2026-10-06 a second round found a medium-severity (M) gap in about half the papers.
2. **Referee simulation**, separate from correctness. A fresh agent writes a referee report that asks: is it enough for the target journal, what is the closest prior work, and what would strengthen it (ranked). Do this *before* polishing the text. The strengthening results, such as a sparse regime or a sharp rate, then go through step 1.
3. **Text gate.** Title, headings, abstract, tables, the version note and the Zenodo description are checked like theorems. Use the standard declarations block `_staging/DECLARACOES_PADRAO_ARTIGOS.tex`. Never claim formal verification for placeholder Lean.
4. **Release bundle** in `releases/AAAA-MM-DD/<work>/`:
   - the PDF;
   - `VERSION_NOTE.md`;
   - `ZENODO_DESCRIPTION.md`;
   - a top-level `LEIA-ME.md` with the upload steps.

   The author uploads; Claude never does.
5. **Keep the source of every published version.** The .tex of two published versions was lost, and the source had to be rebuilt from the PDF. From now on, copy the exact .tex of each upload into the release bundle and tag it in git when the author commits.
6. **Backups before editing** go to `_arquivo/backup_tex_AAAA-MM-DD/` with a `MANIFESTO.tsv` line. Write the line with Python, not `printf`, because escapes corrupted it twice. Leave no `_backup` copies in working folders.

## 6. Processes and memory (mandatory; added 2026-10-02 after an orphaned 2.7 GB job)
Every agent prompt that runs Python must include these rules:
1. **Every long job has a time limit**: `timeout` on the command or a time limit inside the script, at most ~20 min. Save intermediate results to disk.
2. **Background jobs:**
   - write down the PID when starting;
   - **before the final report, wait for the job to finish or kill it by PID** (`Stop-Process -Id <PID>`);
   - never hand back with a job still running.
3. **Memory:**
   - modest meshes and grids;
   - at most one heavy job at a time;
   - estimate the memory before running (array size × 8 bytes);
   - above ~2 GB, reduce the problem or split it.
4. **Never** `taskkill /IM python.exe` or anything else that kills by name.
6. **Read the sources (author's authorization, 2026-10-07, all projects).** When a text matters for a claim, a proof, a novelty check or a citation, download the open-access PDF (arXiv, the author's page, the publisher's OA copy, a repository) into the project's `biblioteca/` folder and read the relevant theorem or section; an abstract is not a source. Put this permission in every literature, verification or citation prompt.
5. **No personal data to external services** (added 2026-10-06 after an agent sent the author's e-mail to the Unpaywall API): never put the author's e-mail, name or other identifiers in API queries, headers or URLs (Unpaywall, Crossref `mailto`, etc.) unless the author has approved that service. A paywalled source is reported as "not accessible"; the author fetches it through CAPES.

7. **Machine limits** (added 2026-10-07, after the author's 8-core / 8 GB machine froze):
   - at most **2 worker processes per agent**, with no multiprocessing pools;
   - at most **10 minutes per run**;
   - **5 agents is the standing level**, and 6 or more freezes the machine.
   - An agent with no file activity for about 1 h is stuck. Stop it with TaskStop and relaunch it from its partial files. A SendMessage to a stopped agent stays "queued" forever.

## 6b. Editing and tooling pitfalls (learned 2026-10-07)
- **LaTeX edits.** Never edit LaTeX with `sed`: it turns `\t` and `\m` into control characters (`\times` → TAB+"imes"). Use the Edit tool or a Python script, and write MANIFESTO rows with Python, not `printf`, which mangles backslashes. Inline `python -c "…"` with parentheses breaks in the cmd hook; use a heredoc or a script file.
- **Unknown scripts.** `update_workplan_status.py --help` runs the update; scripts may ignore flags. Read a script before running it with flags.
- **Instructions to agents.** Give every instruction at launch. A mid-task SendMessage can be refused as a suspected prompt injection; it happened once, correctly cautious.
- **Build fixes.**
  - `\usepackage{fixcmex}` before microtype removes the pdfTeX font-expansion warnings.
  - `\usepackage{morewrites}` fixes "No room for a new \write" in the single-source book.
- **Concurrency.** Two agents must not edit the same chapter at once. Order the edits, or have the second agent re-read the file before editing (Edit refuses stale state).
- **Declarations.** Declarations follow the Leiden Declaration on AI and Mathematics (arXiv:2609.35334): the "Tool and computational resource disclosure" heading, human-only credit, proactive attribution, risk-proportional verification, and the note that Zenodo is not peer review. Template: `_staging/DECLARACOES_PADRAO_ARTIGOS.tex`.

## 6c. Proof-fidelity techniques (added 2026-10-09; full list in the `prova-rigorosa` skill)
- **Statement freeze and back-translation:** formalise the statement first; another agent back-translates it blindly and compares it with the paper.
- **Non-vacuity witness:** each theorem gets an `example` or a ∃-proof with concrete data satisfying all hypotheses.
- **Mutants:** prove the mutant false (¬statement or an explicit counterexample). Failing to compile is not enough.
- **Counterexample search before proving:** Z3/CVC5, Arb, Plausible.
- **Mechanical verifier loops:** best-of-n or proof repair, accepting only what Lean or Arb checks. Evolutionary search (OpenEvolve with the Claude Code CLI) is an option for constructions and counterexamples.
- **CI:** GitHub Actions on the public repo checks `formal_proofs_mathlib` off the PC (proposal `_staging/lean_ci_proposta.yml`).
- **Lean rounds (2026-10-09):** writer agent → different agent does blind back-translation → wire (LeanReal.lean, verificar.sh, CI, README) → push → CI green. Witnesses must be non-degenerate. Never `lake build` the whole library on the PC (memory kill, orphan lake tree); compile per file with `lake env lean`. Unpublished work goes in `formal_proofs_mathlib/LeanLocal/`, excluded via `.git/info/exclude`.
- **Do not cite** claims about other groups' AI results until the primary source has been read; abstract-level reading has produced extraordinary-sounding errors.

The orchestrator:
- after each agent finishes, runs `python _staging/processos_orfaos.py` (lists Python processes older than 45 min in project folders) and kills orphans by PID with `--matar`;
- the hourly check does the same.
