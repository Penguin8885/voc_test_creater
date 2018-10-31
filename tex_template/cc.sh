target=`basename $1 .tex`
platex $target.tex
dvipdfmx $target.dvi
rm $target.tex
rm $target.aux
rm $target.dvi
rm $target.log