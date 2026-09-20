import os
import re
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

os.makedirs('references_and_papers', exist_ok=True)

with open('all_references_text.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

title_pattern = re.compile(r'\\emph\{([^}]+)\}')
found_count = 0

for line in lines:
    match = title_pattern.search(line)
    if not match:
        continue
    title = match.group(1).strip()
    # clean up math in title for search
    title_clean = re.sub(r'\$[^$]+\$', '', title)
    title_clean = re.sub(r'[^a-zA-Z0-9 ]', '', title_clean)
    words = title_clean.split()
    if len(words) < 3:
        continue
    
    # search first 6 words to be safe but precise enough
    query_str = " ".join(words[:6])
    query = urllib.parse.quote(f'ti:"{query_str}"')
    
    url = f'http://export.arxiv.org/api/query?search_query={query}&max_results=1'
    
    try:
        response = urllib.request.urlopen(url)
        xml_data = response.read()
        root = ET.fromstring(xml_data)
        
        entry = root.find('{http://www.w3.org/2005/Atom}entry')
        if entry is not None:
            id_url = entry.find('{http://www.w3.org/2005/Atom}id').text
            arxiv_id = id_url.split('/abs/')[-1]
            pdf_url = f"https://export.arxiv.org/pdf/{arxiv_id}.pdf"
            output = f"references_and_papers/{arxiv_id.replace('/', '_')}.pdf"
            
            if not os.path.exists(output):
                print(f"Found on arXiv: {title[:50]}... -> {arxiv_id}")
                urllib.request.urlretrieve(pdf_url, output)
                print(f" -> Saved to {output}")
                found_count += 1
        time.sleep(4)
    except Exception as e:
        print(f"Error searching for {query_str}: {e}")
        if "429" in str(e):
            print("Rate limited! Sleeping for 15 seconds...")
            time.sleep(15)
        else:
            time.sleep(4)

print(f"\nDone! Found and downloaded {found_count} additional papers from arXiv by title search.")
