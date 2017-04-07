---
title: Molecular Genetics and Bioinformatics / Genética Molecular e Bioinformática 2704N9 2016-17
---
# My Awesome Course 2016-17

[![Build Status](https://travis-ci.org/BjornFJohansson/TravisSlideProcessor.svg?branch=master)](https://travis-ci.org/BjornFJohansson/TravisSlideProcessor)
[Licenciatura em Biologia Aplicada 2yr](http://www.bio.uminho.pt/Default.aspx?tabid=7&pageid=112&lang=pt-PT)

Location:
  
- Monday  LABI DB Practical class
- Tuesday CP3 305 Theoretical 11:00 - 12:00
- Tuesday CP3 305 TP1 (TP Turno 1) 12:00 - 13:00
- Tuesday Lab informática CPII TP2 (TP Turno 2) 17:00 - 18:00

Teacher: Björn Johansson <bjorn_johansson@bio.uminho.pt>

Delegada: Maria Aluna

Course file dropbox [here](https://www.dropbox.com/sh/a4vwd1ux8h81mg8/AADceqVoh96TOCaNwUZvI976a?dl=0).

Course literature: [GENE CLONING AND DNA ANALYSIS An Introduction T.A. BROWN 7ed](http://bcs.wiley.com/he-bcs/Books?action=index&bcsId=9980&itemId=1119072573)

Calendar:

<iframe src="https://calendar.google.com/calendar/embed?mode=WEEK&amp;height=600&amp;wkst=2&amp;bgcolor=%23FFFFFF&amp;src=e2fuohav3fujq4fu83ea6orbkk%40group.calendar.google.com&amp;color=%2329527A&amp;ctz=Europe%2FLisbon" style="border-width:0" width="800" height="600" frameborder="0" scrolling="no"></iframe>

Extra literature:

* [Molecular Biology of the Cell 4ed (free)](https://www.ncbi.nlm.nih.gov/books/NBK21054/)
* [Bioinformatics for Dummies - 2007](http://eu.wiley.com/WileyCDA/WileyTitle/productCd-0470089857.html)
* [Lehninger Principles of Bichemistry](https://www.amazon.com/Lehninger-Principles-Biochemistry-David-Nelson/dp/1429234148)
* [Stryer Biochemistry (5ed free)](https://www.ncbi.nlm.nih.gov/books/NBK21154/)
* [The Selfish Gene](https://www.amazon.com/Selfish-Gene-Popular-Science/dp/0192860925/ref=cm_cr_arp_d_product_top?ie=UTF8)

## About these files

These files and folders are stored in a repository on [Github](https://github.com).
On push: 

* PDF files are created from Libreoffice Writer and Impress files on [TravisCI](https://travis-ci.com).
* Markdown (.md) files are converted into PDFs using pandoc
* Static html files are made from Jupyter notebook files (.ipynb)

All files are pushed to a dropbox.

1. TravisCI clones the repository.
2. git rev-list HEAD gives a list of all SHA1 sums of all commits.
3. The last commit that was processed by TravisCI is read from the cached (by TravisCI) file cached_sha1_checksum/last.sha1
4. git diff --name-only oldsum, newsum is used to find a list of all files changed since last time travis was run.
5. Files that does not exist or that have a name or folder that begins with a "_" are removed from the list.
6. Files are converted
7. The files in the list (or converted files) are pushed to a shared dropbox.
