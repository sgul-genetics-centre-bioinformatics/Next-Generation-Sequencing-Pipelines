#!/usr/bin/env python

#SGUL GENETICS CENTRE EXOME PIPELINE JUNE 2018
#Alan Pittman

#standard pipeline steps:
###############################################################################################

# run BWA command
# run samtools sam to bam conversion command
# run samtools bam sort command 
# run samtools index
# run picard mark PCR Duplicates
# run samtools index again
# run GATK BaseRecalibrator #### need to use big VCF file
# run GATK AnalyzeCovariates ### work in progress need some R libraries installed 
# run GATK ApplyBQSR
	
###############################################################################################

import os
import sys
import subprocess
import csv

#resources:
###############################################################################################
BWAsoftware = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/bwa/bwa"
alignedOUTdir = "/homes/athosnew/Genetics_Centre_Bioinformatics/Exomes/Aligned/"
BWAindex = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/Genome_reference_files/human_g1k_v37.fasta"
samtoolsSoftware = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/samtools-1.8/samtools"
java = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/java/jre1.8.0_171/bin/java"
picard = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/picard-2.815/picard.jar"
gatk = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/gatk-4.0.4.0/gatk-package-4.0.4.0-local.jar"
refknownsitesSNPS = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/Genome_reference_files/common_all.vcf"
refknownsitesINDELS = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/Genome_reference_files/Mills_and_1000G_gold_standard.indels.hg19_modified.vcf"

##################################################################################################

def display(message):
    print(message)

myProject = sys.argv
del myProject[0]

myProject = str(myProject)
myProject = myProject.lstrip('[')
myProject = myProject.lstrip("'")
myProject = myProject.rstrip(']')
myProject = myProject.rstrip("'")    


display("SGUL Genetics Research Centre Alignment Pipeline\n")

print("your project is :")
print(myProject)

print("\n")

dirpath = os.getcwd()
projectDataDir=dirpath + "/" + "Unaligned" + "/" + myProject + "/"
print(os.listdir(projectDataDir))

#generate list of all the samples in the project directory 
mySamples = os.listdir(projectDataDir)

#for each sample in the project folder, identify the fastq files (R1 and R2) an send to BWA alignment
for sample in mySamples:

	sampleDirectory = projectDataDir + sample + "/"

	myinputfiles = os.listdir(sampleDirectory) # assuming we have two fastq files per sample
	
	inputFASTQ1 = myinputfiles[0]
	inputFASTQ2 = myinputfiles[1]
	
	print("your input fastq files are:")
	
	#L1_2.fq.gz # check naming format of fastq files 
	print inputFASTQ1
	print inputFASTQ2
		
	#make analysis output directory
	
	projectFolder = alignedOUTdir + myProject 
	makeDirectoryProject = ['mkdir', projectFolder] 
	subprocess.call(makeDirectoryProject)
	
	sampleFolder = alignedOUTdir + myProject + "/" + sample
	makeDirectory = ['mkdir', sampleFolder] 
	subprocess.call(makeDirectory)
	
	############# SAMPLE VARIABLES ###################################

	outputSAM = sampleFolder + "/" + sample + ".sam" # output samfile
	samHeader = "@RG\\tID:" + sample + "\\tSM:" + sample + "\\tLB:" + sample + "\\tPL:ILLUMINA"
	path_inputFASTQ1 = sampleDirectory + inputFASTQ1
	path_inputFASTQ2 = sampleDirectory + inputFASTQ2
	
	outputBAM = sampleFolder + "/" + sample + ".bam" # output bam file
	
	outputSorstedBAM = sampleFolder + "/" + sample + "_sorted.bam" # output sorted bam file
	
	SorstedUniqueBAM = sampleFolder + "/" + sample + "_sorted_unique" + ".bam" #output sorted unique bam file
	
	picardIbam = "I=" + outputSorstedBAM
	picardObam = "O=" + SorstedUniqueBAM
	picardMfile = "M=" + sampleFolder + "/" + sample + "_marked_dup_metrics.txt"
	
	SorstedUniqueBAMindex = sampleFolder + "/" + sample + "_sorted_unique" + ".bam" + ".bai"
	
	outputSorstedBAMindex = sampleFolder + "/" + sample + "_sorted.bam.bai"	
	
	recal_data_table = sampleFolder + "/" + sample + "_recal_data.table"
	
	AnalyzeCovariates_pdf = sampleFolder + "/" + sample + "_AnalyzeCovariates.pdf"
	
	SorstedUniqueRecalibratedBAM = sampleFolder + "/" + sample + "_sorted_unique_recalibrated" + ".bam"
	
	########## COMMAND LINE ARGUMENTS #################################
	
	BWAcommand = [BWAsoftware, 'mem', BWAindex, path_inputFASTQ1, path_inputFASTQ2,'-t', '8', '-R', samHeader,'-o', outputSAM]
	
	samtoolsViewCommand = [samtoolsSoftware, 'view', '-Sb', 
	outputSAM, '-o', outputBAM]
	
	samtoolsSortCommand = [samtoolsSoftware,'sort', '-m',
	'5000000000', outputBAM, '-o', outputSorstedBAM]
	
	samtoolsINDEXCommand = [samtoolsSoftware, 'index',
	outputSorstedBAM]
	
	picardMARKDUPLICATESCommand = [java, '-jar', picard, 'MarkDuplicates',
	picardIbam, picardObam, picardMfile]
	
	samtoolsINDEXCommand2 = [samtoolsSoftware, 'index', SorstedUniqueBAM]
	
	gatkBaserecalibratorCommand = [java, '-jar', gatk, 'BaseRecalibrator', '-I', SorstedUniqueBAM,
	'-R', BWAindex, '--known-sites', refknownsitesSNPS, '-O', recal_data_table]
	
	gatkAnalyseCovariatesCommand = [java, '-jar', gatk, 'AnalyzeCovariates', '-bqsr', recal_data_table,
	'-plots' , AnalyzeCovariates_pdf]
	
	gatkApplyBQSRCommand = [java, '-jar', gatk, 'ApplyBQSR', '-R', BWAindex, '-I', SorstedUniqueBAM,
	'--bqsr-recal-file', recal_data_table, '-O', SorstedUniqueRecalibratedBAM]
	
	################ RUN COMMANDS #####################################
	
	subprocess.check_call(BWAcommand) # run BWA
	subprocess.check_call(samtoolsViewCommand) # run samtools sam to bam conversion
	
	os.remove(outputSAM) # remove temp sam file
	
	subprocess.check_call(samtoolsSortCommand) # run samtools bam sort	
	subprocess.check_call(samtoolsINDEXCommand) #run samtools index
	
	os.remove(outputBAM)
	
	subprocess.check_call(picardMARKDUPLICATESCommand) ##picard mark PCR Duplicates
	subprocess.check_call(samtoolsINDEXCommand2) # run samtools index again
	
	os.remove(outputSorstedBAM)
	os.remove(outputSorstedBAMindex)
	
	subprocess.check_call(gatkBaserecalibratorCommand) # run GATK BaseRecalibrator
	subprocess.call(gatkAnalyseCovariatesCommand)
	subprocess.check_call(gatkApplyBQSRCommand)
	
	os.remove(SorstedUniqueBAM)
	os.remove(SorstedUniqueBAMindex)
	os.remove(recal_data_table)
		
	
