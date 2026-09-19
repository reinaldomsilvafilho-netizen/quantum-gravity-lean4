import os
import subprocess
import shutil

# Protocol for compiling and releasing LaTeX documents

# Directory of this script
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ZENODO_DIR = os.path.join(ROOT_DIR, "zenodo_final_pdfs")

TARGETS = [
    {
        "name": "Master Book",
        "work_dir": os.path.join(ROOT_DIR, "unified_quantum_gravity_book"),
        "main_tex": "master_book_unified_quantum_gravity.tex",
        "output_pdf": "master_book_unified_quantum_gravity.pdf"
    },
    {
        "name": "Yang-Mills Trilogy",
        "work_dir": os.path.join(ROOT_DIR, "unconditional_yang_mills_trilogy"),
        "main_tex": "The_Geometric_Yang_Mills_Trilogy.tex",
        "output_pdf": "The_Geometric_Yang_Mills_Trilogy.pdf"
    }
    # We can easily add other specific targets here
]

def compile_latex(work_dir, tex_file):
    print(f"[*] Compiling {tex_file} in {work_dir}...")
    try:
        # Run pdflatex twice for cross-references
        for i in range(2):
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex_file],
                cwd=work_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                print(f"[!] Compilation failed on pass {i+1} for {tex_file}")
                print(result.stdout[-1000:]) # print last 1000 chars of error
                return False
        return True
    except FileNotFoundError:
        print("[!] pdflatex command not found. Ensure MiKTeX/TeX Live is in your PATH.")
        return False

def release_pdf(work_dir, pdf_file):
    source_pdf = os.path.join(work_dir, pdf_file)
    target_pdf = os.path.join(ZENODO_DIR, pdf_file)
    
    if not os.path.exists(source_pdf):
        print(f"[!] Source PDF {source_pdf} not found.")
        return False
        
    os.makedirs(ZENODO_DIR, exist_ok=True)
    print(f"[*] Copying {pdf_file} to Zenodo folder...")
    shutil.copy2(source_pdf, target_pdf)
    return True

def main():
    print("=== LaTeX Build and Zenodo Release Protocol ===")
    
    for target in TARGETS:
        print(f"\n--- Processing: {target['name']} ---")
        
        # Check if directory exists
        if not os.path.exists(target['work_dir']):
            print(f"[-] Directory {target['work_dir']} not found. Skipping.")
            continue
            
        # 1. Compile
        success = compile_latex(target['work_dir'], target['main_tex'])
        if not success:
            print(f"[!] Aborting release for {target['name']} due to compilation errors.")
            continue
            
        # 2. Release
        released = release_pdf(target['work_dir'], target['output_pdf'])
        if released:
            print(f"[+] Successfully compiled and updated {target['name']} in zenodo_final_pdfs!")

if __name__ == "__main__":
    main()
