import os
import urllib.request
import time

papers = {'1501.02155', '1203.3591', '1702.00786', 'cond-mat/0407066', '1999.3557', '1703.11008', '1023.4546', '2111.14522', '1202.1491', '1407.1870', '1994.1097', '0905.1317', '1503.05671', '1023.0000', 'hep-th/0505016', '1005.3035', '0705.0016', '1609.04836', 'hep-ph/9402242', '1907.04833', 'hep-th/0105267', '0105267', '0505016', '1610.02743'}

os.makedirs('references_and_papers', exist_ok=True)

for p in papers:
    # clean up id
    clean_id = p.replace('/', '_')
    url = f"https://arxiv.org/pdf/{p}.pdf"
    output = f"references_and_papers/{clean_id}.pdf"
    
    print(f"Downloading {p}...")
    try:
        urllib.request.urlretrieve(url, output)
        print(f" -> Saved to {output}")
        time.sleep(3) # Be nice to arxiv
    except Exception as e:
        print(f" -> Failed to download {p}: {e}")

print("Done!")
