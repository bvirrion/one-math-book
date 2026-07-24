# latexmk configuration for the One Math Book series
$pdf_mode = 1;              # pdflatex by default
$out_dir = 'build';
# One entry file per book; each PDF is named after its entry file
# (build/one_math_book_<N>_<slug>.pdf).
@default_files = (
    'one_math_book_1_primary_middle_school.tex',
    'one_math_book_1_primary_middle_school_fr.tex',
    'one_math_book_1_primary_middle_school_nl.tex',
    'one_math_book_1_primary_middle_school_es.tex',
    'one_math_book_1_primary_middle_school_pt.tex',
    'one_math_book_1_primary_middle_school_hi.tex',
    'one_math_book_2_high_school.tex',
    'one_math_book_2_high_school_fr.tex',
    'one_math_book_2_high_school_nl.tex',
    'one_math_book_2_high_school_es.tex',
    'one_math_book_2_high_school_pt.tex',
    'one_math_book_2_high_school_hi.tex',
    'one_math_book_3_university_year_1.tex',
    'one_math_book_3_university_year_1_fr.tex',
    'one_math_book_3_university_year_1_nl.tex',
    'one_math_book_3_university_year_1_es.tex',
    'one_math_book_3_university_year_1_pt.tex',
    'one_math_book_3_university_year_1_hi.tex',
    'one_math_book_4_university_year_2.tex',
    'one_math_book_4_university_year_2_fr.tex',
    'one_math_book_4_university_year_2_nl.tex',
    'one_math_book_4_university_year_2_es.tex',
    'one_math_book_4_university_year_2_pt.tex',
    'one_math_book_4_university_year_2_hi.tex',
    'one_math_book_5_university_year_3.tex',
    'one_math_book_5_university_year_3_fr.tex',
    'one_math_book_5_university_year_3_nl.tex',
    'one_math_book_5_university_year_3_es.tex',
    'one_math_book_5_university_year_3_pt.tex',
    'one_math_book_5_university_year_3_hi.tex',
);
# The books' many TikZ/pgfplots figures exceed pdfTeX's default main
# memory (5M words); raise the runtime limits.
$pdflatex = 'pdflatex -cnf-line=main_memory=12000000 -cnf-line=extra_mem_top=6000000 -cnf-line=extra_mem_bot=6000000 -interaction=nonstopmode -halt-on-error %O %S';
# Hindi editions (*_hi.tex) need XeLaTeX for OpenType Devanagari. Entry files
# carry "% !TEX program = xelatex"; also force the engine when the jobname
# ends in _hi so a bare `latexmk file_hi.tex` works without relying on the
# magic-comment scan order.
$xelatex = 'xelatex -interaction=nonstopmode -halt-on-error %O %S';
if ($ARGV[0] && $ARGV[0] =~ /_hi(\.tex)?$/) {
    $pdf_mode = 5;  # xelatex
}
$makeindex = 'makeindex %O -o %D %S';
