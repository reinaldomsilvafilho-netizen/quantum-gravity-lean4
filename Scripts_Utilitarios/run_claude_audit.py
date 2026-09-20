import subprocess, sys

with open('paper_functorial_tensor_field_theory/paper_functorial_tensor_field_theory.tex', 'r', encoding='utf-8') as f:
    tex_content = f.read()

prompt = f"""Realize uma auditoria matematica adversarial e independente rigorosa do seguinte paper em LaTeX (incluido na integra abaixo).

Verifique com extremo rigor matematico:
1. Definição 2.1 (espaço de objetos CTens, vínculo on-shell, classe de equivalência de morfismos);
2. Lema 5.1 (equivalência ADM-Einstein e propagação hiperbólica de vínculos de Choquet-Bruhat);
3. Teorema 5.2 (funtorialidade, preservação de identidades e composição via classes de reparametrização);
4. Teorema 5.3 (coerência monoidal simétrica com dagger e desacoplamento de campos de matéria);
5. Teorema 5.4 (costura de cobordismos e correspondência semiclássica com vínculos de Wheeler-DeWitt);
6. Teorema 5.6 (fidelidade do funtor F sob todos os dados do cobordismo e prova da Condição de Energia Nula / NEC via QNEC).

Forneça seu parecer formal detalhado, destacando a solidez das provas, eventuais sutilezas e o veredito final.

--- CODIGO FONTE DO PAPER ---
{tex_content}
"""

cmd_path = r"C:\Users\monar\AppData\Roaming\npm\claude.cmd"
proc = subprocess.Popen([cmd_path, '-p'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
stdout, stderr = proc.communicate(input=prompt)

print("=== RETORNO DO CLAUDE (PRO) ===")
print(stdout)
if stderr:
    print("=== STDERR ===", stderr)
