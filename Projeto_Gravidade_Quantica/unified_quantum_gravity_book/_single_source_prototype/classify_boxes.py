#!/usr/bin/env python3
import re
import sys

fn = sys.argv[1] if len(sys.argv) > 1 else "buildfull_p3.log"
txt = open(fn, encoding="utf-8", errors="replace").read()
header_over = len(re.findall(r"Overfull \\hbox[^\n]*while \\output is active", txt))
para_over = len(re.findall(r"Overfull \\hbox[^\n]*in paragraph", txt))
detected_over = len(re.findall(r"Overfull \\hbox[^\n]*detected at line", txt))
header_under = len(re.findall(r"Underfull \\hbox[^\n]*while \\output is active", txt))
para_under = len(re.findall(r"Underfull \\hbox[^\n]*in paragraph", txt))
detected_under = len(re.findall(r"Underfull \\hbox[^\n]*detected at line", txt))
print("overfull header:", header_over, "paragraph:", para_over, "detected:", detected_over)
print("underfull header:", header_under, "paragraph:", para_under, "detected:", detected_under)
