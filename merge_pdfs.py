import pypdf
import os

pdf_dir = r'C:\Users\monar\Documents\antigravity\resilient-turing\Projeto_Gravidade_Quantica\zenodo_final_pdfs'
pdfs = [
    'paper_ym_part1_constructive_measure.pdf',
    'paper_ym_part2_entropic_repulsion.pdf',
    'paper_ym_part3_nelson_reconstruction.pdf'
]

merger = pypdf.PdfWriter()

for pdf in pdfs:
    filepath = os.path.join(pdf_dir, pdf)
    if os.path.exists(filepath):
        merger.append(filepath)

output_path = os.path.join(pdf_dir, 'The_Unconditional_Yang_Mills_Trilogy.pdf')
with open(output_path, 'wb') as f:
    merger.write(f)

for pdf in pdfs:
    os.remove(os.path.join(pdf_dir, pdf))

print('Merged successfully into', output_path)
