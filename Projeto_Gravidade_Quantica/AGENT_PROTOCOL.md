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

The orchestrator:
- after each agent finishes, runs `python _staging/processos_orfaos.py` (lists Python processes older than 45 min in project folders) and kills orphans by PID with `--matar`;
- the hourly check does the same.
