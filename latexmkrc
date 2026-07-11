# latexmk configuration for the One Math Book series
$pdf_mode = 1;              # pdflatex
$out_dir = 'build';
# One entry file per book; each PDF is named after its entry file
# (build/one_math_book_<slug>.pdf).
@default_files = (
    'one_math_book_primary_middle_school.tex',
    'one_math_book_high_school.tex',
    'one_math_book_university_year_1.tex',
    'one_math_book_university_year_2.tex',
);
# The books' many TikZ/pgfplots figures exceed pdfTeX's default main
# memory (5M words); raise the runtime limits.
$pdflatex = 'pdflatex -cnf-line=main_memory=12000000 -cnf-line=extra_mem_top=6000000 -cnf-line=extra_mem_bot=6000000 -interaction=nonstopmode -halt-on-error %O %S';
$makeindex = 'makeindex %O -o %D %S';
