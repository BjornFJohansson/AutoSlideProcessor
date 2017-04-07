#!/usr/bin/env python
# -*- coding: utf-8 -*-
import PyPDF2
import sys
import subprocess
import re
import time

pdf = sys.argv[1]

# this has  to be done for PyPDF2 to work, dont know why?
subprocess.Popen(['pdftk', pdf, 'output', "_"+pdf])

time.sleep(5)

pdf = PyPDF2.PdfFileReader(open("_"+pdf, "rb"))

text = ""

for i in range(0, pdf.getNumPages()):
    print(str(i))
    extractedText = pdf.getPage(i).extractText()
    text +=  extractedText

#Number 65027
#Name Bárbara Filipa Cerqueira Bernardino
#Email A65027@alunos.uminho.pt
#Course Engenharia Biológica
#Enrolled SAUM No

#regex = u"Number(.+?)Name(.+?)Email(.+?)Course(.+?)Enrolled SAUM(Yes|No)"
regex = "Número(.+?)Nome(.+?)Email(.+?)Curso(.+?)Inscrito SAUM(Sim|Não)"

match = re.findall(regex, text)

with open("alunos.txt", "w") as f:
    for m in match:
        f.write("{}   {}\n".format(m[0], m[1]))