Per far partire il programma:
-secondo il formato songbook digitare:
	perl chordsconverter.pl sbook input.txt output.tex
	
-secondo il formato gchords digitare:
	perl chordsconverter.pl gchords input.txt output.tex
	
Il formato del file di ingresso deve essere del tipo:

####AUTHOR: Nomeautore
####TITLE: Titolo


Riga Accordi
Riga testo
...
...


Per una nuova strofa lasciare 2 righe vuote; lasciare 2 righe vuote anche fra il titolo e il resto della canzone.
Non lasciare MAI una sola riga vuota , a meno che non ci sia una riga solo di accordi o solo di testo fatte apposta così.