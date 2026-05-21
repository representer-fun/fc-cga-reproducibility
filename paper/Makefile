# Makefile for CIKM 2026 paper: Flow-Constrained Counterfactual Graph Augmentation
# Usage:
#   make named     -- build named (author-identified) version
#   make anon      -- build anonymous version
#   make all       -- build both
#   make clean     -- remove generated files

PDFLATEX = pdflatex -interaction=nonstopmode -halt-on-error
BIBTEX   = bibtex

NAMED_SRC  = paper_named.tex
ANON_SRC   = paper_anonymous.tex

NAMED_PDF  = paper_named.pdf
ANON_PDF   = paper_anonymous.pdf

.PHONY: all named anon clean figures

all: named anon

figures:
	python3 make_paper_figures.py

named: $(NAMED_PDF)

anon: $(ANON_PDF)

FIGURES = figures/fig_07_layering_10seed_delta_ci.pdf \
          figures/fig_08_effect_scope_map.pdf \
          figures/fig_09_amount_alignment.pdf

$(NAMED_PDF): $(NAMED_SRC) references.bib $(FIGURES)
	$(PDFLATEX) paper_named
	$(BIBTEX)   paper_named
	$(PDFLATEX) paper_named
	$(PDFLATEX) paper_named

$(ANON_PDF): $(ANON_SRC) references.bib $(FIGURES)
	$(PDFLATEX) paper_anonymous
	$(BIBTEX)   paper_anonymous
	$(PDFLATEX) paper_anonymous
	$(PDFLATEX) paper_anonymous

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.fls *.fdb_latexmk \
	      paper_named.pdf paper_anonymous.pdf

# Convenience targets for single-pass quick view (no bibliography)
quick-named:
	$(PDFLATEX) paper_named

quick-anon:
	$(PDFLATEX) paper_anonymous
