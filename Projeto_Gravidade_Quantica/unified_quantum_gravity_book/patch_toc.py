import os
import re

book_dir = r"C:\Users\monar\Documents\antigravity\resilient-turing\Projeto_Gravidade_Quantica\unified_quantum_gravity_book"
master_tex = os.path.join(book_dir, "master_book_unified_quantum_gravity.tex")

with open(master_tex, "r", encoding="utf-8") as f:
    master_content = f.read()

include_pattern = re.compile(r'\\includepdf\[(.*?)\]\{(.*?\.pdf)\}')

def extract_toc(pdf_name):
    toc_name = pdf_name.replace(".pdf", ".toc")
    toc_path = os.path.join(book_dir, toc_name)
    if not os.path.exists(toc_path):
        return None
    
    with open(toc_path, "r", encoding="utf-8") as f:
        toc_content = f.read()
    
    lines = toc_content.splitlines()
    entries = []
    
    for line in lines:
        if "\\contentsline" not in line: continue
        
        if "{section}" in line:
            level = 1
            type_str = "section"
        elif "{subsection}" in line:
            level = 2
            type_str = "subsection"
        else:
            continue
        
        m_page = re.search(r'\}\{(\d+)\}\{[^}]+\}%\s*$', line)
        if not m_page:
            m_page = re.search(r'\}\{(\d+)\}\{[^}]+\}$', line)
            
        page = m_page.group(1) if m_page else ""
        
        m_toc = re.search(r'\\toc(?:sub)?section\s*\{\}\{(.*?)\}\{(.*?)\}\}\{(?:\d+)\}', line)
        if m_toc:
            num = m_toc.group(1)
            title = m_toc.group(2)
        else:
            m_fallback = re.search(r'\\numberline\s*\{(.*?)\}(.*?)\}\{(?:\d+)\}', line)
            if m_fallback:
                num = m_fallback.group(1)
                title = m_fallback.group(2)
            else:
                num = ""
                title = line
        
        if page and title and num != title:
            # Strip math blocks completely to avoid fragility
            title = re.sub(r'\$.*?\$', '', title)
            # Remove lingering braces
            title = title.replace("{", "").replace("}", "")
            # Remove lingering macros
            title = re.sub(r'\\[a-zA-Z@]+', '', title)
            
            title = title.strip()
            num = num.strip()
            
            # escape commas in title just in case (though we wrap in braces)
            title = title.replace(",", "")
            
            label = f"sec_{page}_{len(entries)}"
            
            if num:
                heading = f"{num} {title}"
            else:
                heading = f"{title}"
                
            entries.append(f"{page},{type_str},{level},{{{heading}}},{label}")
            
    return entries

new_content = master_content

for match in include_pattern.finditer(master_content):
    args = match.group(1)
    pdf_name = match.group(2)
    
    if "DICTIONARY" in pdf_name:
        continue
        
    entries = extract_toc(pdf_name)
    if entries:
        addtotoc_str = "addtotoc={" + ",\n".join(entries) + "}"
        if "addtotoc" in args:
            continue
            
        new_args = f"{args}, {addtotoc_str}"
        old_stmt = match.group(0)
        new_stmt = f"\\includepdf[{new_args}]{{{pdf_name}}}"
        
        new_content = new_content.replace(old_stmt, new_stmt)

with open(master_tex, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Done patching master tex file.")
