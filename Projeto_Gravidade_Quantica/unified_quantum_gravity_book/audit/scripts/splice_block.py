"""Replace the block of a .tex file between two marker strings (start inclusive, end exclusive).

Usage: python audit/scripts/splice_block.py FILE START_MARKER END_MARKER REPLACEMENT_FILE
"""
import sys

path, start_marker, end_marker, repl_path = sys.argv[1:5]
s = open(path, encoding='utf-8').read()
i = s.index(start_marker)
i = s.rfind('\n', 0, i) + 1          # start of the line containing the start marker
j = s.index(end_marker, i)
j = s.rfind('\n', 0, j) + 1          # start of the line containing the end marker
s = s[:i] + open(repl_path, encoding='utf-8').read() + s[j:]
open(path, 'w', encoding='utf-8', newline='').write(s)
print(f'replaced {j - i} chars in {path}')
