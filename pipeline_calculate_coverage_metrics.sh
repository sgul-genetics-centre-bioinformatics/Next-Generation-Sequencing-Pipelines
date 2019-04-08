#!/bin/bash

#resources:
###############################################################################################

java=/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/java/jre1.8.0_171/bin/java
picard=/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/picard-2.815/picard.jar
BWAindex=/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/Genome_reference_files/human_g1k_v37.fasta
INTERVALS=/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/Genome_reference_files/Nextera_focussed_ExomeTarget_hg19_0bp.tab.intList

##################################################################################################

myPROJECT=$1
masterDIR=`pwd`

echo $masterDIR

mkdir $masterDIR/CoverageMetrics/$myPROJECT

projectDIR=$masterDIR/Aligned/$myPROJECT
MetricsOUT=$masterDIR/CoverageMetrics/$myPROJECT

mkdir $cleanFASTQOUT

samples=`ls $projectDIR/`

echo $samples

for sample in $samples; do

	mkdir $MetricsOUT/$sample

	$java -jar $picard CollectWgsMetrics \
	INPUT=$projectDIR/$sample/${sample}_sorted_unique_recalibrated.bam \
	OUTPUT=$MetricsOUT/$sample/$sample.exonic.metrics \
	MINIMUM_MAPPING_QUALITY=15 \
	INTERVALS=$INTERVALS \
	REFERENCE_SEQUENCE=$BWAindex

done

exit
exit
exit


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

