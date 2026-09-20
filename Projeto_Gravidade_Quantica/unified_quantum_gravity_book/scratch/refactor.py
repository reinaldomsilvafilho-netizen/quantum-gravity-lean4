import os
import glob
import re

def main():
    target_dir = r"C:\Users\monar\Documents\antigravity\resilient-turing\Projeto_Gravidade_Quantica\unified_quantum_gravity_book"
    files = glob.glob(os.path.join(target_dir, "verify_chap*.py"))
    
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # 1. Type hints: def test_foo() -> None: or def battery_foo() -> None:
        content = re.sub(r'def (test_[a-zA-Z0-9_]+)\(\):', r'def \1() -> None:', content)
        content = re.sub(r'def (battery[a-zA-Z0-9_]+)\(\):', r'def \1() -> None:', content)
        
        # 2. Add Newton-Raphson safeguard if applicable (we check for any "eps" or "dval" division if it exists)
        if "dval =" in content and "if abs(dval) < 1e-12:" not in content:
            content = re.sub(
                r'(dval\s*=\s*[^\n]+)\n',
                r'\1\n        if abs(dval) < 1e-12:\n            break\n',
                content
            )
            
        # 3. Add Docstrings. We find functions that start with `def ...() -> None:\n    print("...")`
        def add_docstring(match):
            func_def = match.group(1)
            spaces = match.group(2)
            print_stmt = match.group(3)
            str_content = match.group(4)
            
            if '"""' in print_stmt or "'''" in print_stmt:
                return match.group(0) # something weird, skip
                
            docstring = f'{spaces}"""\n{spaces}{str_content}\n{spaces}"""\n'
            return f'{func_def}\n{docstring}{spaces}{print_stmt}'
            
        content = re.sub(
            r'(def (?:test_|battery)[a-zA-Z0-9_]+\(\)(?: -> None)?:\s*\n)(\s*)(print\([f]*["\'](.*?)["\']\))',
            add_docstring,
            content
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {os.path.basename(file_path)}")
        else:
            print(f"Already compliant: {os.path.basename(file_path)}")

if __name__ == "__main__":
    main()
