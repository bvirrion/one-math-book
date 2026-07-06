# latexmk configuration for One Math Book
$pdf_mode = 1;              # pdflatex
$out_dir = 'build';
@default_files = ('main.tex');
# The book's many TikZ/pgfplots figures exceed pdfTeX's default main
# memory (5M words); raise the runtime limits.
$pdflatex = 'pdflatex -cnf-line=main_memory=12000000 -cnf-line=extra_mem_top=6000000 -cnf-line=extra_mem_bot=6000000 -interaction=nonstopmode -halt-on-error %O %S';
$makeindex = 'makeindex %O -o %D %S';
