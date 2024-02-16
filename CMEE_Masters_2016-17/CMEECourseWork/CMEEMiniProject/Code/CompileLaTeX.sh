#!/bin/bash
   
rm $1.pdf # remove existing pdf

pdflatex $1.tex
# pdflatex $1.tex
bibtex $1
pdflatex $1.tex
pdflatex $1.tex

#Now open pdf if file exists and is non-empty
if [ -s $1.pdf ] 
then
	evince $1.pdf &
else
	echo "$1.pdf is empty."
fi

## Cleanup
rm -f *~
rm -f *.aux
rm -f *.blg
rm -f *.log
rm -f *.nav
rm -f *.out
rm -f *.snm
rm -f *.toc
rm -f *.vrb
rm -f *.bbl
rm -f *.dvi
rm -f *.lot
rm -f *.lof
