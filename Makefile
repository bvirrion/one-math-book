.PHONY: all clean distclean

all:
	latexmk

clean:
	latexmk -c

distclean:
	latexmk -C
	rm -rf build
