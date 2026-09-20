import re

text = r'''\contentsline {section}{\tocsection {}{1}{Introduction and Motivation}}{2}{section.1}%
\contentsline {subsection}{\tocsubsection {}{3.1}{Family I: Multilinear, Polynomial, and Spherical Realizations}}{3}{subsection.3.1}%
\contentsline {section}{\tocsection {}{}{References}}{16}{section*.3}%'''

pattern = re.compile(r'\\contentsline\s*\{(?P<type>section|subsection)\}\s*\{\\toc(?:sub)?section\s*\{\}\{(?P<num>.*?)\}\{(?P<title>.*?)\}\}\{(?P<page>\d+)\}')

for match in pattern.finditer(text):
    print(match.groupdict())
