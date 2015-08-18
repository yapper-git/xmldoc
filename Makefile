# See http://tex.stackexchange.com/questions/140845/how-can-i-ignore-latex-error-while-compiling
PDFLATEX = lualatex -interaction nonstopmode -halt-on-error -file-line-error

EPUB_FILES := 
MOBI_FILES := 

default: all-latex all-epub

all: all-latex all-pdf all-epub all-epub-files all-mobi

all-latex: $(patsubst repositories/%,latex/%/text.tex,$(wildcard repositories/*))

all-pdf: $(patsubst repositories/%,latex/%/text.pdf,$(wildcard repositories/*))

all-epub: $(patsubst repositories/%,ebook/%.epub,$(wildcard repositories/*))

all-epub-files: $(patsubst repositories/%,ebook/%.epub-FILES,$(wildcard repositories/*))

all-mobi: $(patsubst repositories/%,ebook/%.mobi,$(wildcard repositories/*))

latex/%/text.tex: repositories/%
	rm -rf $(dir $@)
	mkdir -p $(dir $@)
	../doc2latex.py $< $@

latex/%/text.pdf: latex/%/text.tex
	cd $(dir $<) && $(PDFLATEX) $(notdir $<) && $(PDFLATEX) $(notdir $<)
	#grep "Missing character:" $(patsubst %.tex,%.log,$<) | sort | uniq
	#exiftool -all:all $@
	#exiftool -xmp:all= $@
	#exiftool -Title="This is the Title" -Author="Happy Man" -Subject="This is the Subject" -Creator="mysite.com" -Producer="" $@

ebook/%.epub: repositories/%
	../doc2epub.py $< $@

ebook/%.epub-FILES: ebook/%.epub
	rm -rf $@
	unzip -o $< -d $@

ebook/%.mobi: ebook/%.epub
	ebook-convert $< $@

clean:
	rm -f latex/*/text.aux latex/*/text.log latex/*/text.out latex/*/text.toc

mrproper: clean
	rm -f latex/*/text.pdf
	rm -rf ebook

.PHONY: default all all-latex all-pdf all-epub all-epub-files all-mobi clean mrproper

.PRECIOUS: %.tmp
