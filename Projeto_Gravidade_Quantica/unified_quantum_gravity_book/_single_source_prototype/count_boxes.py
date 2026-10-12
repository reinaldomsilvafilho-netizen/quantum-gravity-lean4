#!/usr/bin/env python3
import re
import sys

fn = sys.argv[1] if len(sys.argv) > 1 else "buildfull_p3.log"
txt = open(fn, encoding="utf-8", errors="replace").read()
over_h = len(re.findall(r"Overfull \\hbox", txt))
over_v = len(re.findall(r"Overfull \\vbox", txt))
under_h = len(re.findall(r"Underfull \\hbox", txt))
under_v = len(re.findall(r"Underfull \\vbox", txt))
errors = len(re.findall(r"^! ", txt, re.M))
warnings = len(re.findall(r"LaTeX Warning:", txt))
undefined = len(re.findall(r"undefined", txt))
print(f"{fn}: errors={errors} warnings={warnings} overfull_hbox={over_h} "
      f"overfull_vbox={over_v} underfull_hbox={under_h} underfull_vbox={under_v} "
      f"undefined={undefined}")
