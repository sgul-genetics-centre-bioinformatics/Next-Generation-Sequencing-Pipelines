#!/bin/bash

#resources:
###############################################################################################

Trimmomatic="/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/Trimmomatic-0.38/trimmomatic-0.38.jar"

##################################################################################################

myPROJECT=$1
masterDIR=`pwd`

echo $masterDIR

mkdir $masterDIR/Unaligned/$myPROJECT

projectDIR=$masterDIR/raw_FASTQ/$myPROJECT
cleanFASTQOUT=$masterDIR/Unaligned/$myPROJECT

mkdir $cleanFASTQOUT

samples=`ls $projectDIR/`

echo $samples

for sample in $samples; do

	mkdir $masterDIR/Unaligned/$myPROJECT/$sample

	echo " "

	fastQs=`ls $projectDIR/$sample`
	
	rm $cleanFASTQOUT/$sample/${sample}_fastQs.txt				
									
	for fastQ in $fastQs; do
			
			
			echo " "
			echo "$projectDIR/$sample/$fastQ" >> $cleanFASTQOUT/$sample/${sample}_fastQs.txt			
						
		done
		
	echo "your sample:"
	echo "$sample"
	echo " "
	echo "your fastq files:"
	echo " "	
	echo `cat $cleanFASTQOUT/$sample/${sample}_fastQs.txt`


	echo " "
	echo "cleaning paired-end reads for sample $sample"
	echo " "
	java -jar $Trimmomatic PE -threads 2 `cat $cleanFASTQOUT/$sample/${sample}_fastQs.txt` -baseout $cleanFASTQOUT/$sample/$sample.gz \
	TRAILING:15 MINLEN:36
	
	echo " " 
	echo "$sample cleaned"
	echo " "

	rm $cleanFASTQOUT/$sample/${sample}_fastQs.txt
	rm $cleanFASTQOUT/$sample/${sample}_1U.gz
	rm $cleanFASTQOUT/$sample/${sample}_2U.gz
	

done

echo " "
echo "fastQs cleaned and ready for alignemnt"


exit
exit
exit

