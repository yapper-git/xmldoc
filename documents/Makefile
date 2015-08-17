# See http://tex.stackexchange.com/questions/140845/how-can-i-ignore-latex-error-while-compiling
PDFLATEX = lualatex -interaction nonstopmode -halt-on-error -file-line-error

MARKDOWN_FILES := $(patsubst %.xml,%.md,$(wildcard *.xml))
PDF_FILES      := $(patsubst %.xml,%.pdf,$(wildcard *.xml))
XHTML_FILES    := $(patsubst %.xml,%.xhtml,$(wildcard *.xml))

default: $(MARKDOWN_FILES) $(PDF_FILES) $(XHTML_FILES)

%.tmp: %.xml
	python ../extract_minifier.py -f $< $@

%.xhtml: %.tmp
	python ../extract_to_xhtml.py -f $< $@

%.md: %.tmp
	python ../extract_to_text.py -f $< $@

%.tex: %.tmp
	python ../extract_to_latex.py $< $@

%.pdf: %.tex
	$(PDFLATEX) $< && $(PDFLATEX) $<
	grep "Missing character:" $(patsubst %.tex,%.log,$<) | sort | uniq
	exiftool -all:all $@
	#exiftool -xmp:all= $@
	#exiftool -Title="This is the Title" -Author="Happy Man" -Subject="This is the Subject" -Creator="mysite.com" -Producer="" $@

%.mobi: %.epub
	epub-convert $< $@

clean:
	rm -f *.tmp
	rm -f *.aux *.log *.out *.toc

mrproper: clean
	rm -f *.md *.xhtml *.tex *.pdf

.PHONY: default clean mrproper

.PRECIOUS: %.tmp
