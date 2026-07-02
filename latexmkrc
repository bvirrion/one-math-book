# latexmk configuration for One Math Book
$pdf_mode = 1;              # pdflatex
$out_dir = 'build';
@default_files = ('main.tex');
$pdflatex = 'pdflatex -interaction=nonstopmode -halt-on-error %O %S';
$makeindex = 'makeindex %O -o %D %S';
