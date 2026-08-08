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
    'one_math_book_1_primary_middle_school_ar.tex',
    'one_math_book_2_high_school.tex',
    'one_math_book_2_high_school_fr.tex',
    'one_math_book_2_high_school_nl.tex',
    'one_math_book_2_high_school_es.tex',
    'one_math_book_2_high_school_pt.tex',
    'one_math_book_2_high_school_hi.tex',
    'one_math_book_2_high_school_ar.tex',
    'one_math_book_3_university_year_1.tex',
    'one_math_book_3_university_year_1_fr.tex',
    'one_math_book_3_university_year_1_nl.tex',
    'one_math_book_3_university_year_1_es.tex',
    'one_math_book_3_university_year_1_pt.tex',
    'one_math_book_3_university_year_1_hi.tex',
    'one_math_book_3_university_year_1_ar.tex',
    'one_math_book_4_university_year_2.tex',
    'one_math_book_4_university_year_2_fr.tex',
    'one_math_book_4_university_year_2_nl.tex',
    'one_math_book_4_university_year_2_es.tex',
    'one_math_book_4_university_year_2_pt.tex',
    'one_math_book_4_university_year_2_hi.tex',
    'one_math_book_4_university_year_2_ar.tex',
    'one_math_book_5_university_year_3.tex',
    'one_math_book_5_university_year_3_fr.tex',
    'one_math_book_5_university_year_3_nl.tex',
    'one_math_book_5_university_year_3_es.tex',
    'one_math_book_5_university_year_3_pt.tex',
    'one_math_book_5_university_year_3_hi.tex',
    'one_math_book_5_university_year_3_ar.tex',
);
# Hindi editions (*_hi.tex) need XeLaTeX for OpenType Devanagari, and Arabic
# editions (*_ar.tex) need LuaLaTeX for babel's Lua bidi engine (bidi=basic);
# every other edition builds with pdfTeX. The choice is made per *source file*,
# inside the command latexmk runs, and deliberately not by setting $pdf_mode:
#
#   * a command-line engine flag beats the rc file, and the release workflow
#     calls `latexmk -pdf <root>` for every book, so any $pdf_mode this file
#     sets is overwritten before the Hindi entry is compiled;
#   * keying off $ARGV[0] only worked for a bare `latexmk file_hi.tex` — with
#     options in front ("-pdf -halt-on-error … file_hi.tex") $ARGV[0] is the
#     first option, so the test silently failed.
#
# Both routes sent the Hindi books through pdflatex, where the guard in
# styles/onemath.sty stops the build ("Hindi editions require XeLaTeX").
# Dispatching on %S is immune to both, because latexmk hands the routine the
# file it is actually compiling.
#
# The books' many TikZ/pgfplots figures also exceed pdfTeX's default main
# memory (5M words), hence the raised runtime limits.
$pdflatex = 'internal om_compile %O %S';
$xelatex  = 'internal om_compile %O %S';
$lualatex = 'internal om_compile %O %S';

sub om_compile {
    my @args = @_;
    my $source = pop @args;
    my @engine = $source =~ /_hi\.tex$/
        ? ('xelatex', '-interaction=nonstopmode', '-halt-on-error')
        : $source =~ /_ar\.tex$/
        ? ('lualatex', '-interaction=nonstopmode', '-halt-on-error')
        : ('pdflatex',
           '-cnf-line=main_memory=12000000',
           '-cnf-line=extra_mem_top=6000000',
           '-cnf-line=extra_mem_bot=6000000',
           '-interaction=nonstopmode', '-halt-on-error');
    # system() hands back the RAW wait status, not an exit code. Returning it
    # verbatim is why a signal death reached latexmk as the meaningless
    # "Command for 'pdflatex' gave return code 0.54296875" -- that is 139/256,
    # and 139 is SIGSEGV+core. LuaTeX segfaulting on an Arabic book in CI was
    # invisible until the number was decoded by hand. Decode it here instead.
    my $status = system(@engine, @args, $source);
    # Return the RAW wait status: latexmk divides what an internal routine
    # returns by 256 to recover the exit code, so handing it a plain exit code
    # makes an ordinary failure print as "return code 0.00390625".
    #
    # A death by SIGNAL is not a multiple of 256, though, and then that same
    # division prints nonsense: LuaTeX segfaulting on an Arabic book in CI
    # surfaced only as "gave return code 0.54296875" (139/256, i.e. SIGSEGV
    # plus core), with no error anywhere in the log. Say so out loud instead.
    if ($status == -1) {
        warn "  !!! $engine[0] could not be run: $!\n";
    }
    elsif (my $signal = $status & 127) {
        warn "  !!! $engine[0] was KILLED BY SIGNAL $signal"
             . (($status & 128) ? " (core dumped)" : "")
             . " while compiling $source -- this is a crash in the engine,\n"
             . "      not a LaTeX error, so the .log will end without a '!' line.\n";
    }
    return $status;
}
$makeindex = 'makeindex %O -o %D %S';
