questions.epub: questions.md metadata.txt book_res/* attachments/* Makefile ## Generate epub book
	pandoc --toc --toc-depth=6 -o questions.epub metadata.txt questions.md
