# See http://tex.stackexchange.com/questions/140845/how-can-i-ignore-latex-error-while-compiling
PDFLATEX = lualatex -interaction nonstopmode -halt-on-error -file-line-error


default: all

all: all-latex all-pdf all-epub all-epub-files all-mobi all-html

all-latex: $(patsubst repositories/%,%.tex,$(wildcard repositories/*))

all-pdf: $(patsubst repositories/%,%.pdf,$(wildcard repositories/*))

all-epub: $(patsubst repositories/%,%.epub,$(wildcard repositories/*))

all-epub-files: $(patsubst repositories/%,%.epub-FILES,$(wildcard repositories/*))

all-mobi: $(patsubst repositories/%,%.mobi,$(wildcard repositories/*))

all-html: $(patsubst repositories/%,%.html,$(wildcard repositories/*))

%.tex: repositories/%
	python ../doc2latex.py $< $@

%.pdf: %.tex
	$(PDFLATEX) $< && $(PDFLATEX) $<
	#grep "Missing character:" $(patsubst %.tex,%.log,$<) | sort | uniq
	#exiftool -all:all $@
	#exiftool -xmp:all= $@
	#exiftool -Title="This is the Title" -Author="Happy Man" -Subject="This is the Subject" -Creator="mysite.com" -Producer="" $@

%.epub: repositories/%
	python ../doc2epub.py $< $@

%.epub-FILES: %.epub
	rm -rf $@
	unzip -o $< -d $@

%.mobi: %.epub
	ebook-convert $< $@

%.html: repositories/%
	python ../doc2html.py $< $@

clean:
	rm -f *.aux *.log *.out *.toc

mrproper: clean
	rm -f *.tex *.pdf
	rm -rf *.epub *.epub-FILES *.mobi
	rm -f *.html

.PHONY: default all all-latex all-pdf all-epub all-epub-files all-mobi all-html clean mrproper

.PRECIOUS: %.tmp
