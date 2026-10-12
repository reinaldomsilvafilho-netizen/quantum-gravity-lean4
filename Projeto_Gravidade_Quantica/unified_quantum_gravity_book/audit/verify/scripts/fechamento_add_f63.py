from pathlib import Path
P = Path(r"C:\Users\monar\Documents\antigravity\resilient-turing\Projeto_Gravidade_Quantica\unified_quantum_gravity_book\WORKPLAN.md")
lines = P.read_text(encoding="utf-8").split("\n")
ids = [l.split("|")[1].strip() for l in lines if l.startswith("| F-")]
if "F-63" in ids:
    raise SystemExit("F-63 already present")
last = max(i for i, l in enumerate(lines) if l.startswith("| F-"))
row = ("| F-63 | B | cap. 2, thm:continuous_path_integral (ii), exemplo de nitidez (l. 642) | "
       "O exemplo de que o fator e^{M/k} não pode ser omitido usa ℛ_j ≡ M sem exigir M > 0; o enquadramento admite M = 0, "
       "onde o erro é 0 = M/k e \"exceeds\" falha (achado pelo Lean do lote A-B5, `mutant_M_zero_false`). | "
       "`audit/verify/L2_FIDELIDADE_LIVRO_A_B5.md` (seção de adjudicação); `audit/verify/scripts/l1_ch2_pathint.py` | "
       "Frase mínima: \"ℛ_j ≡ M\" → \"ℛ_j ≡ M > 0\" | "
       "**corrigido** 2026-10-10 (`audit/verify/fixes_fechamento_livro_2026-10-10.md`); camada 2 pendente |")
lines.insert(last + 1, row)
P.write_text("\n".join(lines), encoding="utf-8")
print("inserted after line", last + 1)
