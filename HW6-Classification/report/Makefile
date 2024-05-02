# Variables
TEX=pdflatex
TEXFLAGS=-output-directory=debug
SOURCE=main.tex
BUILDDIR=.
DEBUGDIR=debug

# Default target
.PHONY: all clean

all: clean pdf

pdf:
	@mkdir -p $(BUILDDIR)
	@mkdir -p $(DEBUGDIR)
	$(TEX) $(TEXFLAGS) $(SOURCE)
	@mv debug/*.pdf $(BUILDDIR)

clean:
	@rm -rf $(BUILDDIR)/*.pdf $(DEBUGDIR)
