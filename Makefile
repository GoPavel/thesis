

.PHONY: all
all: thesis.pdf


thesis.pdf:
	xelatex -synctex=1 -interaction=nonstopmode thesis.tex
	xelatex -synctex=1 -interaction=nonstopmode thesis.tex


.PHONY: clean
clean: 
	rm -f thesis.{aux,log,pdf,toc,bib,bbl,bcf,run.xml,tct,out}
	
