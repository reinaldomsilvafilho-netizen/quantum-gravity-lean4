import os
import subprocess
import sys
import shutil

def get_target_files(workspace_dir):
    files = [
        "paper_beyond_the_spectrum_3/paper_beyond_the_spectrum_3.tex",
        "paper_yang_mills_mass_gap/paper_yang_mills_mass_gap.tex",
        "research_master_universe_lagrangian/paper_master_universe_lagrangian.tex",
        "paper_standard_model_masses/paper_fermion_mass_hierarchy.tex",
        "paper_functorial_tensor_field_theory/paper_functorial_tensor_field_theory.tex"
    ]
    return [os.path.join(workspace_dir, f) for f in files]

def run_audit(workspace_dir):
    files = get_target_files(workspace_dir)
    print(f"Encontrados {len(files)} arquivos de papers para auditoria.")
    
    claude_cmd = r"C:\Users\monar\AppData\Roaming\npm\claude.cmd"
    
    for idx, filepath in enumerate(files):
        # -----------------------------
        # CRIAÇÃO DE BACKUP ANTES DA EDIÇÃO
        # -----------------------------
        backup_path = filepath + ".bak"
        if not os.path.exists(backup_path):
            shutil.copy2(filepath, backup_path)
            print(f"Backup criado: {os.path.basename(backup_path)}")
        else:
            print(f"Backup já existe: {os.path.basename(backup_path)}")
        
        print(f"\n{'='*60}")
        print(f"[{idx+1}/{len(files)}] Iniciando auditoria para: {os.path.basename(os.path.dirname(filepath))}/{os.path.basename(filepath)}")
        print(f"{'='*60}\n")
        
        prompt = f"""You are the Adversarial Mathematical Auditor.
Perform a critical test and language improvement audit on the following file:
{filepath}

Your goals:
1. Critically review the language, mathematical rigor, and presentation.
2. Improve and update the text where it can be made more concise, clear, and academically robust.
3. Check for any leftover pedagogical fluff, biased language, or unproven physical paradoxes, and rewrite them into rigorous form.
4. USE YOUR TOOLS to edit the file directly and apply the updates.
5. Once finished, output a summary of the improvements made.
"""
        
        proc = subprocess.Popen(
            [claude_cmd, "-p", "--dangerously-skip-permissions"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            bufsize=1
        )
        
        proc.stdin.write(prompt)
        proc.stdin.close()
        
        for line in iter(proc.stdout.readline, ''):
            sys.stdout.write(line.encode('ascii', 'replace').decode('ascii'))
            sys.stdout.flush()
            
        proc.wait()
        
        if proc.returncode != 0:
            print(f"\n[AVISO] Auditoria retornou erro (código {proc.returncode}) para {filepath}")
        else:
            print(f"\n[OK] Auditoria concluída para {filepath}")

if __name__ == "__main__":
    workspace = r"C:\Users\monar\Documents\antigravity\resilient-turing"
    run_audit(workspace)
