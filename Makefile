questions.epub: questions.md metadata.txt book_res/* attachments/* Makefile ## Generate epub book
	pandoc --toc --toc-depth=6 -o questions.epub metadata.txt questions.md

.PHONY: toc
toc:  ## Generate TOC from questions.md
	python3 generate_toc.py

.PHONY: toc
toc-check:  ## Check that toc is actual
	python3 generate_toc.py --check
