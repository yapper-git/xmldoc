# See http://tex.stackexchange.com/questions/140845/how-can-i-ignore-latex-error-while-compiling
PDFLATEX = lualatex -interaction nonstopmode -halt-on-error -file-line-error


default: all

all: all-epub all-epub-files all-mobi all-html all-latex all-pdf all-md

all-epub: $(patsubst repositories/%,%.epub,$(wildcard repositories/*))
all-epub-files: $(patsubst repositories/%,%.epub-FILES,$(wildcard repositories/*))
all-mobi: $(patsubst repositories/%,%.mobi,$(wildcard repositories/*))

all-html: $(patsubst repositories/%,%.html,$(wildcard repositories/*))

all-latex: $(patsubst repositories/%,%.tex,$(wildcard repositories/*))
all-pdf: $(patsubst repositories/%,%.pdf,$(wildcard repositories/*))

all-md: $(patsubst repositories/%,%.md,$(wildcard repositories/*))


%.epub: repositories/%
	python ../docexporter.py -f epub $< $@

%.epub-FILES: %.epub
	rm -rf $@
	unzip -o $< -d $@

%.mobi: %.epub
	ebook-convert $< $@


%.html: repositories/%
	python ../docexporter.py -f html $< $@


%.tex: repositories/%
	python ../docexporter.py -f latex $< $@

%.pdf: %.tex
	$(PDFLATEX) $< && $(PDFLATEX) $<
	#grep "Missing character:" $(patsubst %.tex,%.log,$<) | sort | uniq
	#exiftool -all:all $@
	#exiftool -xmp:all= $@
	#exiftool -Title="This is the Title" -Author="Happy Man" -Subject="This is the Subject" -Creator="mysite.com" -Producer="" $@


%.md: repositories/%
	python ../docexporter.py -f markdown $< $@


clean:
	rm -f *.aux *.log *.out *.toc

mrproper: clean
	rm -rf *.epub *.epub-FILES *.mobi
	rm -f *.html
	rm -f *.tex *.pdf
	rm -f *.md

.PHONY: default all all-epub all-epub-files all-mobi all-html all-latex all-pdf all-md clean mrproper

.PRECIOUS: %.tmp
