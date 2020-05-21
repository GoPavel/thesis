

.PHONY: all
all: thesis.pdf


thesis.pdf:
	xelatex -synctex=1 -interaction=nonstopmode thesis.tex
	biber thesis
	xelatex -synctex=1 -interaction=nonstopmode thesis.tex
	xelatex -synctex=1 -interaction=nonstopmode thesis.tex


.PHONY: clean
clean:
	rm -f thesis.{aux,log,pdf,toc,bbl,blg,bcf,run.xml,tct,out}
	rm -f texput.log

.PHONY: easy-rebuild
easy-rebuild:
	rm -rf thesis.pdf
	xelatex -syntex=1 -interaction=nonstopmode thesis.tex

.PHNOY: hard-rebuild
hard-rebuild: clean all
