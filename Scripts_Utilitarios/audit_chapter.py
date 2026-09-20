import sys, os, subprocess

if len(sys.argv) < 2:
    print("Uso: python audit_chapter.py <numero_capitulo>")
    print("Exemplo: python audit_chapter.py 01")
    sys.exit(1)

chap_num = sys.argv[1].zfill(2)
book_dir = r"c:\Users\monar\Documents\antigravity\resilient-turing\unified_quantum_gravity_book"

# Encontrar arquivo do capitulo
files = [f for f in os.listdir(book_dir) if f.startswith(f"chap{chap_num}_") and f.endswith(".tex")]
if not files:
    print(f"Erro: nenhum arquivo chap{chap_num}_*.tex encontrado em {book_dir}")
    sys.exit(1)

chap_file = os.path.join(book_dir, files[0])
print(f"Auditando capitulo: {files[0]}")

with open(chap_file, "r", encoding="utf-8") as f:
    tex_content = f.read()

prompt = f"""Você é um auditor matemático de elite especializado em geometria diferencial, álgebra multilinear e gravitação quântica.
Realize uma auditoria matemática adversarial minuciosa no Capítulo {chap_num} do livro de Gravitação Quântica.

Analise com extremo rigor:
1. Todas as Definições, Lemas, Proposições e Teoremas do texto.
2. Descarregamento de hipóteses em cada passo de demonstração.
3. Consistência de tipos e espaços funcionais (dimensões, normas Lp, BV, limites assintóticos).
4. Possíveis contraexemplos em casos degenerados ou limites extremos.
5. Lista de pontos que necessitam de correção ou refinamento matemático com a solução sugerida.
6. Veredito formal de consistência matemática (APROVADO, APROVADO COM RESSALVAS ou REJEITADO).

Arquivo: {files[0]}
--- CONTEÚDO DO CAPÍTULO ---
{tex_content}
"""

cmd_path = r"C:\Users\monar\AppData\Roaming\npm\claude.cmd"
print("Invocando Claude Code CLI para auditoria adversarial...")
proc = subprocess.Popen([cmd_path, "-p"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
stdout, stderr = proc.communicate(input=prompt)

out_report = os.path.join(book_dir, f"PROOF_AUDIT_CHAP{chap_num}.md")
with open(out_report, "w", encoding="utf-8") as f:
    f.write(f"# RELATÓRIO DE AUDITORIA ADVERSARIAL - CAPÍTULO {chap_num}\n")
    f.write(f"## Arquivo: `{files[0]}`\n")
    f.write(f"## Auditor: Claude Code (Anthropic)\n\n---\n\n")
    f.write(stdout)

print(f"Relatório de auditoria gerado com sucesso em: {out_report}")
if stderr:
    print("Stderr:", stderr[:300])
