#!/usr/bin/perl
###--------------------------------------------inizializzazione comune
#supponiamo che passo il file txt e il nome del latex con percorso
$source=$ARGV[1];
$dest=$ARGV[2];

#apro il txt
open(SF, "<$source");

#genero il latex
open(DF,"+>$dest");

#scansiono il txt
$counter=0;
##variabile globale con lista completa accordi
@totalChordList=();
###var globale che contiene il file in pratica
$file="";
###var che contiene l'intestazione con titolo e autore
$file2="";

if(eof(SF)){warn "ERROR: FILE EMPTY";close(DF);unlink($dest);}
#---------------------------------------------------SCELTA PROGRAMMA DA USARE
$type=$ARGV[0];
if($type eq "sbook")
{
	$flagfirstverse=0;#indica se sono alla prima strofa, mi serve per non far aprire e chiudere strofe sbagliate all'inizio
	
	##ricerca autore e titolo
	$authfound=0;
	$titfound=0;
	$found=0;
	while($found!=1 && !eof(SF)){
		$author=<SF>;
		$title=<SF>;
		if($author=~m/^####AUTHOR:/){
			$authfound=1;
			$author=~s/####AUTHOR://;
		}
		if($title=~m/^####TITLE:/){
			$titfound=1;
			$title=~s/####TITLE://;
		}
		if($authfound==1 && $titfound==1){
			$found=1;
			$author=~s/^ //g;#elimina spazi iniziali
			$title=~s/^ //g;
			$author=~s/[\r\n]*//g;#elimina il terminatore, che non mi serve
			$author=~s/[\n]*//g;#elimina il terminatore, che non mi serve
			$title=~s/[\r\n]*//g;
			$title=~s/[\n]*//g;
			print DF "\\documentclass[a4paper, 10pt]{article}\n\\usepackage[english]{babel}\n\\usepackage[utf8]{inputenc}\n\\usepackage{microtype}\n\\usepackage[chordbk]{songbook}\n";
			print DF "\\begin{document}\n";
			print DF "\\begin{song}{".$title."}{}\n";
			print DF "{".$author."}{}{}{}\n";
		}
	}
	if(eof(SF)){warn "ERROR: NO AUTHOR OR TITLE";close(DF);unlink($dest);}
	
#-------processazione testo
	while(!eof(SF)){
		$lineCh0=<SF>;
		$lineTxt0=<SF>;
	
		$indexCh0=0;
		$indexTxt0=0;
		
		if ($lineCh0 =~ m/^\s*\n/){
		 $lineCh0= "\n";
		}
		
		if ($lineTxt0 =~ m/^\s*\n/){
		 $lineTxt0= "\n";
		}
		
		$lineTxt0 =~ s/'/'/g;
		$lineTxt0 =~ s/à/a'/g;
		$lineTxt0 =~ s/è/e'/g;
		$lineTxt0 =~ s/é/e'/g;
		$lineTxt0 =~ s/ì/i'/g;
		$lineTxt0 =~ s/ò/o'/g;
		$lineTxt0 =~ s/ù/u'/g;
		
		if((length $lineCh0)==1 && (length $lineTxt0)==1 && $flagfirstverse==0)#questo lo fa solo per la prima strofa
		{
			#new strofa
			$flagfirstverse=1;
			$file=$file."\\begin{SBVerse}\n";
		
		}
		elsif((length $lineCh0)==1 && (length $lineTxt0)==1)
		{
			#new strofa
			$file=$file."\\end{SBVerse}\n";
			$file=$file."\\begin{SBVerse}\n";
		
		}
	
	
		elsif(length $lineCh0>length $lineTxt0){ 
			longCh($lineCh0,$lineTxt0);
			$file=$file."\\\\";$file=$file."\n";
			
		}
		elsif(length $lineCh0==length $lineTxt0){
			samelength($lineCh0,$lineTxt0);
			$file=$file."\\\\";$file=$file."\n";
			
		}
		elsif(length $lineCh0<length $lineTxt0){
			longTxt($lineCh0,$lineTxt0);
			$file=$file."\\\\";$file=$file."\n";
			
		}
	
	}
	print DF $file;
	
	print DF "\\end{SBVerse}\n";
	print DF "\\end{song}\n";
	print DF "\\end{document}";
}
####------------------------------------------########
elsif($type eq "gchords"){
	
	$flagfirstverse=0;#indica se sono alla prima strofa, mi serve per non far aprire e chiudere strofe sbagliate all'inizio
	
	##ricerca autore e titolo
	$authfound=0;
	$titfound=0;
	$found=0;
	while($found!=1 && !eof(SF)){
		$author=<SF>;
		$title=<SF>;
		if($author=~m/^####AUTHOR:/){
			$authfound=1;
			$author=~s/####AUTHOR://g;
		}
		if($title=~m/^####TITLE:/){
			$titfound=1;
			$title=~s/####TITLE://g;
		}
		if($authfound==1 && $titfound==1){
			$found=1;
			$author=~s/^ //g;#elimina spazi iniziali
			$title=~s/^ //g;
			$author=~s/[\r\n]*//g;#elimina il terminatore, che non mi serve
			$author=~s/[\n]*//g;#elimina il terminatore, che non mi serve
			$title=~s/[\r\n]*//g;
			$title=~s/[\n]*//g;
			print DF "\\documentclass[a4paper, 10pt]{article}\n";
			print DF "\\usepackage{geometry}\n\\setlength{\\parindent}{0pt}% \\setlength{\\textwidth}{6.5in}\n\\setlength{\\textwidth}{7.2in}";
			print DF "\\usepackage[english]{babel}\n\\usepackage[utf8]{inputenc}\n\\usepackage[T1]{fontenc}\n\\usepackage{microtype}\n\\usepackage{gchords}\n";			
			print DF "\\iftrue\n\\newcommand\\mychords{\n\\def\\chordsize{1.4mm}   % distance between two frets (and two strings)\n\\font\\fingerfont=cmr5  % font used for numbering fingers% \\font\\fingerfont=cmmi5   % font used for numbering fingers\n\\font\\namefont=cmr6    % font used for labeling of the chord\n\\font\\fretposfont=cmr7  % font used for the fret position marker% \\def\\dampsymbol{\$\\scriptstyle\\times\$} %  `damp this string' marker\n\\def\\dampsymbol{{\\tiny\$\\scriptstyle\\times\$}} %  `damp this string' marker\n}\n";
			print DF "\\renewcommand\\yoff{3}\n\\renewcommand\\fingsiz{1.4}\n";	
			$file2=$file2."\\newpage\n\\begin{center}\n\\Large\n";
			$file2=$file2."\\textbf{".$title."} / \\textsl{".$author."}\n";
			$file2=$file2."\\end{center}\n";
		}
	}
	if(eof(SF)){warn "ERROR: NO AUTHOR OR TITLE";close(DF);unlink($dest);}
	

#-------processazione testo
	while(!eof(SF)){
		$lineCh0=<SF>;
		$lineTxt0=<SF>;
	
		$indexCh0=0;
		$indexTxt0=0;
		
		if ($lineCh0 =~ m/^\s*\n/){
		 $lineCh0= "\n";
		}
		
		if ($lineTxt0 =~ m/^\s*\n/){
		 $lineTxt0= "\n";
		}
		
		$lineTxt0 =~ s/'/'/g;
		$lineTxt0 =~ s/à/a'/g;
		$lineTxt0 =~ s/è/e'/g;
		$lineTxt0 =~ s/é/e'/g;
		$lineTxt0 =~ s/ì/i'/g;
		$lineTxt0 =~ s/ò/o'/g;
		$lineTxt0 =~ s/ù/u'/g;
		
		#tutti i prossimi if sono in alternativa
		if((length $lineCh0)==1 && (length $lineTxt0)==1 && $flagfirstverse==0)#questo lo fa solo per la prima strofa
		{
			#new strofa
			$flagfirstverse=1;
			$file=$file."\\begin{verse}\n";
		
		}
		elsif((length $lineCh0)==1 && (length $lineTxt0)==1)
		{
			#new strofa
			$file=$file."\\end{verse}\n";
			$file=$file."\\begin{verse}\n";
		
		}
	
	
		elsif(length $lineCh0>length $lineTxt0){ GlongCh($lineCh0,$lineTxt0);$file=$file."\\\\";$file=$file."\n";}
		elsif(length $lineCh0==length $lineTxt0){
			Gsamelength($lineCh0,$lineTxt0);
			$file=$file."\\\\";$file=$file."\n";
			
		}
		elsif(length $lineCh0<length $lineTxt0){GlongTxt($lineCh0,$lineTxt0);$file=$file."\\\\";$file=$file."\n";}
	
	}
	$file=$file."\\end{verse}\n";
	###############togliamo replicati nella lista globale accordi
	$ind=0;
	@minilist=();
	$flagPresent=0;
	while($indsost<scalar(@totalChordList))
	{
	    $totalChordList[$ind]=~s/[\r\n]*//g;
	    $totalChordList[$ind]=~s/[\n]*//g;
	    $totalChordList[$ind]=~s/[\s]*//g;
	    $indsost++;
	}
	while($ind<scalar(@totalChordList))
	{	
		for($ind2=0;$ind2<scalar(@minilist);$ind2++){
			if($totalChordList[$ind] eq $minilist[$ind2]){$flagPresent=1;last;}
		}
		if($flagPresent==0){
		      push(@minilist,$totalChordList[$ind]);
		}
		$flagPresent=0;
		$ind+=1;
	}
		
	#####NEWCOMMANDS
	$indtest=0;
	while($indtest<scalar(@minilist))
	{
		#warn $minilist[$indtest]."\n";
		
		$chtemp=$minilist[$indtest];
		$chtemp2=$minilist[$indtest];
		#sostituzione dei caratteri non ammessi
		$chtemp=~ s/1/one/g;
		$chtemp=~ s/2/two/g;
		$chtemp=~ s/3/three/g;
		$chtemp=~ s/4/four/g;
		$chtemp=~ s/5/five/g;
		$chtemp=~ s/6/six/g;		
		$chtemp=~ s/7/seven/g;
		$chtemp=~ s/8/eight/g;
		$chtemp=~ s/9/nine/g;
		$chtemp=~ s/10/ten/g;
		$chtemp=~ s/11/eleven/g;
		$chtemp=~ s/\//bsfk/g;
		$chtemp=~ s/#/die/g;
		$chtemp2=~ s/#/\\#/g;
		$chtemp=~ s/[+]/[Maj]/g;
		
		print DF "\\newcommand{\\".$chtemp."}{\\chord{t}{}{".$chtemp2."}}\n";
		$indtest++;
	}
	print DF "\\fi\n";
	print DF "\\begin{document}\n";
	print DF "\\mychords\n";
	print DF "\\pagestyle{empty}\n";
	########risostituzione in modo che vengano visualizzati coi simboli
	$ftemp=$file;
		$ftemp=~ s/1/one/g;
		$ftemp=~ s/2/two/g;
		$ftemp=~ s/3/three/g;
		$ftemp=~ s/4/four/g;
		$ftemp=~ s/5/five/g;
		$ftemp=~ s/6/six/g;		
		$ftemp=~ s/7/seven/g;
		$ftemp=~ s/8/eight/g;
		$ftemp=~ s/9/nine/g;
		$ftemp=~ s/10/ten/g;
		$ftemp=~ s/11/eleven/g;
		$ftemp=~ s/#/die/g;
		$ftemp=~ s/[+]/[Maj]/g;
		$ftemp =~ s/\//bsfk/g;
		$ftemp =~ s/bsfk/\//;
		
		
	####
	print DF $file2;
	print DF $ftemp;
	
	print DF "\\end{document}\n";
}
else{warn "ERROR: type in the package you want to use as the first argument";close(DF);unlink($dest);}


#-----------------------------------------------------------fine main
#----------------------------------------FUNZIONI SONGBOOK
sub samelength{
	$indexCh=0;
	$indexTxt=0;
	$lineCh=$_[0];
	$lineTxt=$_[1];
	@arrayChords=();#inserisco la posizione e la stringa dell'accordo: per estrarli vedo posiz pari e dispari dell'array
	$indexArray=0;
	$flagInChord=0;#se 1 sono in mezzo a un accordo
	$tempString="";
	
	while($indexCh<length $lineCh){
		$tempChar=substr($lineCh,$indexCh,1);
		if($tempChar ne " " && $tempChar ne "\t" && $tempChar ne "\n" && $flagInChord==0) {#inizio accordo
			push(@arrayChords,$indexCh);
			$flagInChord=1;
			$tempString=$tempString.$tempChar;
		}
		elsif(($tempChar eq " " || $tempChar eq "\t" || $indexCh==(length $lineCh)-1) && $flagInChord==1){#fine accordo
			$flagInChord=0;
			$tempString=~s/[\r\n]*//g;
			$tempString=~s/[\n]*//g;
			push(@arrayChords,$tempString);
			$tempString="";
		}
		elsif($tempChar ne " " && $tempChar ne "\t" && $flagInChord==1){#in mezzo all'accordo
			$tempString=$tempString.$tempChar;
		}
		$indexCh++;
	}#warn "fine ciclo lettura uguali";
	#qui faccio un whiole per copiare il txt e gli accordi su DF
	while($indexArray<scalar(@arrayChords)){#ciclo sugli elem dell'array
		$writePosition=0;#indica da dove devo riprendere a copiare il testo#inutile perche indextxt non viene riazzerato
		while($indexTxt<$arrayChords[$indexArray]){#ciclo sul testo
			$file=$file.substr($lineTxt,$indexTxt,1);
			#warn substr($lineTxt,$indexTxt,1);
			$indexTxt++;
		}
		$file=$file."\\Ch{".$arrayChords[$indexArray+1]."}{";
		####e qui andare avanti nel testo di quanto era lungo l'accordo
		$templ=length $arrayChords[$indexArray+1];
		for($ind=0;$ind<$templ;$ind++){
			$file=$file.substr($lineTxt,$indexTxt,1);
			$indexTxt++;
		}
		$file=$file."}";
		$indexArray+=2;
	}
	if($indexTxt!=length $lineTxt){# � il caso in cui "testo{\La7},", cio� c'� testo dopo l'ultimo accordo ma la linetxt finisce insieme a linech!
		while($indexTxt<length $lineTxt){
			$file=$file.substr($lineTxt,$indexTxt,1);
			$indexTxt++;
		}
	}
}
#---------------------------------------------------------------
sub longTxt{
	$indexCh=0;
	$indexTxt=0;
	$lineCh=$_[0];
	$lineTxt=$_[1];
	@arrayChords=();#inserisco la posizione e la stringa dell'accordo: per estrarli vedo posiz pari e dispari dell'array
	$indexArray=0;
	$flagInChord=0;#se 1 sono in mezzo a un accordo
	$tempString="";
	
	while($indexCh<length $lineCh){
		$tempChar=substr($lineCh,$indexCh,1);
		if($tempChar ne " " && $tempChar ne "\t" && $tempChar ne "\n" && $flagInChord==0) {#inizio accordo
			push(@arrayChords,$indexCh);
			$flagInChord=1;
			$tempString=$tempString.$tempChar;
		}
		elsif(($tempChar eq " " || $tempChar eq "\t" || $indexCh==(length $lineCh)-1) && $flagInChord==1){#fine accordo
			$flagInChord=0;
			$tempString=~s/[\r\n]*//g;
			$tempString=~s/[\n]*//g;
			push(@arrayChords,$tempString);
			$tempString="";
		}
		elsif($tempChar ne " " && $tempChar ne "\t" && $flagInChord==1){#in mezzo all'accordo
			$tempString=$tempString.$tempChar;
		}
		$indexCh++;
	}#warn "fine ciclo lettura long text";
	
	
	##############################################################TEST
	#$indextmp=0;
	#warn "Stampa accordi long txt";
	#while($indextmp<scalar(@arrayChords)){
	#	warn $arrayChords[$indextmp]."\n"; 
	#	$indextmp++;
	#}
	##############fine test
	
	#qui faccio un whiole per copiare il txt e gli accordi su DF
	while($indexArray<scalar(@arrayChords)){#ciclo sugli elem dell'array
		$writePosition=0;#indica da dove devo riprendere a copiare il testo#inutile perche indextxt non viene riazzerato
		while($indexTxt<$arrayChords[$indexArray]){#ciclo sul testo
			$file=$file.substr($lineTxt,$indexTxt,1);
			#warn substr($lineTxt,$indexTxt,1);
			$indexTxt++;
		}
		$file=$file."\\Ch{".$arrayChords[$indexArray+1]."}{";
		####e qui andare avanti nel testo di quanto era lungo l'accordo
		$templ=length $arrayChords[$indexArray+1];
		for($ind=0;$ind<$templ;$ind++){
			$file=$file.substr($lineTxt,$indexTxt,1);
			$indexTxt++;
		}
		$file=$file."}";
		$indexArray+=2;
	}
	while($indexTxt<length $lineTxt){#finisce la riga testo
		$file=$file.substr($lineTxt,$indexTxt,1);
		$indexTxt++;
	}
	

}
#---------------------------------------------------------------
sub longCh{
	$indexCh=0;
	$indexTxt=0;
	$lineCh=$_[0];
	$lineTxt=$_[1];
	@arrayChords=();#inserisco la posizione e la stringa dell'accordo: per estrarli vedo posiz pari e dispari dell'array
	$indexArray=0;
	$flagInChord=0;#se 1 sono in mezzo a un accordo
	$tempString="";
	
	while($indexCh<length $lineCh){
		$tempChar=substr($lineCh,$indexCh,1);
		if($tempChar ne " " && $tempChar ne "\t" && $tempChar ne "\n" && $flagInChord==0) {#inizio accordo
			push(@arrayChords,$indexCh);
			$flagInChord=1;
			$tempString=$tempString.$tempChar;
		}
		elsif(($tempChar eq " " || $tempChar eq "\t" || $indexCh==(length $lineCh)-1) && $flagInChord==1){#fine accordo
			$flagInChord=0;
			$tempString=~s/[\r\n]*//g;
			$tempString=~s/[\n]*//g;
			push(@arrayChords,$tempString);
			$tempString="";
		}
		elsif($tempChar ne " " && $tempChar ne "\t" && $flagInChord==1){#in mezzo all'accordo
			$tempString=$tempString.$tempChar;
		}
		$indexCh++;
	}#warn "fine ciclo lettura long chords";
	##############################################################TEST
	#$indextmp=0;
	#warn "Stampa accordi";
	#while($indextmp<scalar(@arrayChords)){
	#	warn $arrayChords[$indextmp]."\n"; 
	#	$indextmp++;
	#}
	##############fine test
	
	#qui faccio un whiole per copiare il txt e gli accordi su DF
	while($indexArray<scalar(@arrayChords)){#ciclo sugli elem dell'array
		$writePosition=0;#indica da dove devo riprendere a copiare il testo#inutile perche indextxt non viene riazzerato
		while($indexTxt<$arrayChords[$indexArray] && $indexTxt<length $lineTxt){#ciclo sul testo 
			if(substr($lineTxt,$indexTxt,1) ne "\n") {$file=$file.substr($lineTxt,$indexTxt,1);}############PUNTO CHIAVE PER L'ERRORE
			#warn substr($lineTxt,$indexTxt,1);
			$indexTxt++;
		}
		if($indexTxt==length $lineTxt){
			#warn "fine riga".$indexTxt;
			#warn "length=".(length $lineTxt);
			
		}
		$file=$file."\\Ch{".$arrayChords[$indexArray+1]."}{";
		####e qui andare avanti nel testo di quanto era lungo l'accordo
		$templ=length $arrayChords[$indexArray+1];
		for($ind=0;$ind<$templ;$ind++){
			if(substr($lineTxt,$indexTxt,1) ne "\n"){$file=$file.substr($lineTxt,$indexTxt,1);}
			$indexTxt++;
		}
		$file=$file."}";
		$indexArray+=2;
		
	}
	if($indexTxt!=length $lineTxt){# � il caso in cui "testo{\La7},", cio� c'� testo dopo l'ultimo accordo ma la linetxt finisce prima di linech!
		while($indexTxt<length $lineTxt){
			if(substr($lineTxt,$indexTxt,1) ne "\n"){$file=$file.substr($lineTxt,$indexTxt,1);}
			$indexTxt++;
		}
	}
	#se gli accordi sono finiti ma devo vedere se c'erano ulteriori spazi:
	if((length $lineCh)>$arrayChords[$indexArray-2]+(length $arrayChords[$indexArray-1])){
		$spaces=(length $lineCh)-($arrayChords[$indexArray-2]+(length $arrayChords[$indexArray-1]));
		for($i=0;$i<$spaces;$i++){
			$file=$file." ";
		}
	}
	
	$file=$file."\n";
}


#----------------------------------------FINE FUNZIONI SONGBOOK

#------------------------------------------FUNZIONI GCHORDS
sub Gsamelength{
	$indexCh=0;
	$indexTxt=0;
	$lineCh=$_[0];
	$lineTxt=$_[1];
	@arrayChords=();#inserisco la posizione e la stringa dell'accordo: per estrarli vedo posiz pari e dispari dell'array
	$indexArray=0;
	$flagInChord=0;#se 1 sono in mezzo a un accordo
	$tempString="";
	
	while($indexCh<length $lineCh){
		$tempChar=substr($lineCh,$indexCh,1);
		if($tempChar ne " " && $tempChar ne "\t" && $tempChar ne "\n" && $flagInChord==0) {#inizio accordo
			push(@arrayChords,$indexCh);
			$flagInChord=1;
			$tempString=$tempString.$tempChar;
		}
		elsif(($tempChar eq " " || $tempChar eq "\t" || $indexCh==(length $lineCh)-1) && $flagInChord==1){#fine accordo
			$flagInChord=0;
			$tempString=~s/[\r\n]*//g;
			$tempString=~s/[\n]*//g;
			push(@arrayChords,$tempString);
			$tempString="";
		}
		elsif($tempChar ne " " && $tempChar ne "\t" && $flagInChord==1){#in mezzo all'accordo
			$tempString=$tempString.$tempChar;
		}
		$indexCh++;
	}#warn "fine ciclo lettura uguali";
	#qui faccio un whiole per copiare il txt e gli accordi su DF
	while($indexArray<scalar(@arrayChords)){#ciclo sugli elem dell'array
		##copio solo gli accordi nella lista globale
		push(@totalChordList,$arrayChords[$indexArray+1]);
		$writePosition=0;
		while($indexTxt<$arrayChords[$indexArray]){#ciclo sul testo
			$file=$file.substr($lineTxt,$indexTxt,1);
			#warn substr($lineTxt,$indexTxt,1);
			$indexTxt++;
		}
		$file=$file."\\upchord{\\".$arrayChords[$indexArray+1]."}{";
		####e qui andare avanti nel testo di quanto era lungo l'accordo
		$templ=length $arrayChords[$indexArray+1];
		for($ind=0;$ind<$templ;$ind++){
			$file=$file.substr($lineTxt,$indexTxt,1);
			$indexTxt++;
		}
		$file=$file."}";
		$indexArray+=2;
	}
	if($indexTxt!=length $lineTxt){# � il caso in cui "testo{\La7},", cio� c'� testo dopo l'ultimo accordo ma la linetxt finisce insieme a linech!
		while($indexTxt<length $lineTxt){
			$file=$file.substr($lineTxt,$indexTxt,1);
			$indexTxt++;
		}
	}
}
#---------------------------------------------------------------
sub GlongTxt{
	$indexCh=0;
	$indexTxt=0;
	$lineCh=$_[0];
	$lineTxt=$_[1];
	@arrayChords=();#inserisco la posizione e la stringa dell'accordo: per estrarli vedo posiz pari e dispari dell'array
	$indexArray=0;
	$flagInChord=0;#se 1 sono in mezzo a un accordo
	$tempString="";
	
	while($indexCh<length $lineCh){
		$tempChar=substr($lineCh,$indexCh,1);
		if($tempChar ne " " && $tempChar ne "\t" && $tempChar ne "\n" && $flagInChord==0) {#inizio accordo
			push(@arrayChords,$indexCh);
			$flagInChord=1;
			$tempString=$tempString.$tempChar;
		}
		elsif(($tempChar eq " "  || $tempChar eq "\t" || $indexCh==(length $lineCh)-1) && $flagInChord==1){#fine accordo
			$flagInChord=0;
			$tempString=~s/[\r\n]*//g;
			$tempString=~s/[\n]*//g;
			push(@arrayChords,$tempString);
			$tempString="";
		}
		elsif($tempChar ne " "  && $tempChar ne "\t" && $flagInChord==1){#in mezzo all'accordo
			$tempString=$tempString.$tempChar;
		}
		$indexCh++;
	}#warn "fine ciclo lettura long text";
	
	
	##############################################################TEST
	#$indextmp=0;
	#warn "Stampa accordi long txt";
	#while($indextmp<scalar(@arrayChords)){
	#	warn $arrayChords[$indextmp]."\n"; 
	#	$indextmp++;
	#}
	##############fine test
	
	#qui faccio un whiole per copiare il txt e gli accordi su DF
	while($indexArray<scalar(@arrayChords)){#ciclo sugli elem dell'array
		##copio solo gli accordi nella lista globale
		push(@totalChordList,$arrayChords[$indexArray+1]);
		$writePosition=0;
		while($indexTxt<$arrayChords[$indexArray]){#ciclo sul testo
			$file=$file.substr($lineTxt,$indexTxt,1);
			#warn substr($lineTxt,$indexTxt,1);
			$indexTxt++;
		}
		$file=$file."\\upchord{\\".$arrayChords[$indexArray+1]."}{";
		####e qui andare avanti nel testo di quanto era lungo l'accordo
		$templ=length $arrayChords[$indexArray+1];
		for($ind=0;$ind<$templ;$ind++){
			$file=$file.substr($lineTxt,$indexTxt,1);
			$indexTxt++;
		}
		$file=$file."}";
		$indexArray+=2;
	}
	while($indexTxt<length $lineTxt){#finisce la riga testo
		$file=$file.substr($lineTxt,$indexTxt,1);
		$indexTxt++;
	}

}
#---------------------------------------------------------------
sub GlongCh{
	$indexCh=0;
	$indexTxt=0;
	$lineCh=$_[0];
	$lineTxt=$_[1];
	@arrayChords=();#inserisco la posizione e la stringa dell'accordo: per estrarli vedo posiz pari e dispari dell'array
	$indexArray=0;
	$flagInChord=0;#se 1 sono in mezzo a un accordo
	$tempString="";
	
	while($indexCh<length $lineCh){
		$tempChar=substr($lineCh,$indexCh,1);
		if($tempChar ne " " && $tempChar ne "\t" && $tempChar ne "\n" && $flagInChord==0) {#inizio accordo
			push(@arrayChords,$indexCh);
			$flagInChord=1;
			$tempString=$tempString.$tempChar;
		}
		elsif(($tempChar eq " " || $tempChar eq "\t" || $indexCh==(length $lineCh)-1) && $flagInChord==1){#fine accordo
			$flagInChord=0;
			$tempString=~s/[\r\n]*//g;
			$tempString=~s/[\n]*//g;
			push(@arrayChords,$tempString);
			$tempString="";
		}
		elsif($tempChar ne " " && $tempChar ne "\t" && $flagInChord==1){#in mezzo all'accordo
			$tempString=$tempString.$tempChar;
		}
		$indexCh++;
	}#warn "fine ciclo lettura long chords";
	##############################################################TEST
	#$indextmp=0;
	#warn "Stampa accordi";
	#while($indextmp<scalar(@arrayChords)){
	#	warn $arrayChords[$indextmp]."\n"; 
	#	$indextmp++;
	#}
	##############fine test
	
	#qui faccio un whiole per copiare il txt e gli accordi su DF
	while($indexArray<scalar(@arrayChords)){#ciclo sugli elem dell'array
		##copio solo gli accordi nella lista globale
		push(@totalChordList,$arrayChords[$indexArray+1]);
		$writePosition=0;
		while($indexTxt<$arrayChords[$indexArray] && $indexTxt<length $lineTxt){#ciclo sul testo 
			if(substr($lineTxt,$indexTxt,1) ne "\n") {$file=$file.substr($lineTxt,$indexTxt,1);}
			#warn substr($lineTxt,$indexTxt,1);
			$indexTxt++;
		}
		if($indexTxt==length $lineTxt){
			#warn "fine riga".$indexTxt;
			#warn "length=".(length $lineTxt);
		}
		$file=$file."\\upchord{\\".$arrayChords[$indexArray+1]."}{";
		####e qui andare avanti nel testo di quanto era lungo l'accordo
		$templ=length $arrayChords[$indexArray+1];
		for($ind=0;$ind<$templ;$ind++){
			if(substr($lineTxt,$indexTxt,1) ne "\n"){$file=$file.substr($lineTxt,$indexTxt,1);}
			$indexTxt++;
		}
		$file=$file."}";
		$indexArray+=2;
		
	}
	if($indexTxt!=length $lineTxt){# � il caso in cui "testo{\La7},", cio� c'� testo dopo l'ultimo accordo ma la linetxt finisce prima di linech!
		while($indexTxt<length $lineTxt){
			if(substr($lineTxt,$indexTxt,1) ne "\n"){$file=$file.substr($lineTxt,$indexTxt,1);}
			$indexTxt++;
		}
	}
	#se gli accordi sono finiti ma devo vedere se c'erano ulteriori spazi:
	if((length $lineCh)>$arrayChords[$indexArray-2]+(length $arrayChords[$indexArray-1])){
		$spaces=(length $lineCh)-($arrayChords[$indexArray-2]+(length $arrayChords[$indexArray-1]));
		for($i=0;$i<$spaces;$i++){
			$file=$file." ";
		}
	}
	
	$file=$file."\n"; 
}

#------------------------------------------FINE FUNZIONI GCHORDS

###---------------------------------------------parte finale comune

close(SF);
if(-e $dest){close(DF);}