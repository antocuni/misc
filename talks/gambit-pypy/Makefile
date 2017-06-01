# you can find rst2beamer.py and inkscapeslide.py here:
# http://bitbucket.org/antocuni/env/src/619f486c4fad/bin/rst2beamer.py
# http://bitbucket.org/antocuni/env/src/619f486c4fad/bin/inkscapeslide.py


talk.pdf: talk.rst author.latex title.latex stylesheet.latex diagrams/tracing-phases-p00.pdf diagrams/trace-p00.pdf diagrams/tracetree-p00.pdf diagrams/architecture-p00.pdf diagrams/pypytrace-p00.pdf
	rst2beamer.py --stylesheet=stylesheet.latex --documentoptions=14pt talk.rst talk.latex || exit
	sed 's/\\date{}/\\input{author.latex}/' -i talk.latex || exit
	#sed 's/\\maketitle/\\input{title.latex}/' -i talk.latex || exit
	pdflatex talk.latex  || exit

view: talk.pdf
	evince talk.pdf &

xpdf: talk.pdf
	xpdf talk.pdf &


diagrams/tracing-phases-p00.pdf: diagrams/tracing-phases.svg
	cd diagrams && inkscapeslide.py tracing-phases.svg

diagrams/trace-p00.pdf: diagrams/trace.svg
	cd diagrams && inkscapeslide.py trace.svg

diagrams/tracetree-p00.pdf: diagrams/tracetree.svg
	cd diagrams && inkscapeslide.py tracetree.svg

diagrams/architecture-p00.pdf: diagrams/architecture.svg
	cd diagrams && inkscapeslide.py architecture.svg

diagrams/pypytrace-p00.pdf: diagrams/pypytrace.svg
	cd diagrams && inkscapeslide.py pypytrace.svg
