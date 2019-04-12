#!/usr/bin/env python

#SGUL GENETICS CENTRE EXOME PIPELINE JUNE 2018
#Alan Pittman

#standard pipeline steps:
###############################################################################################

# remake fastq files from bams from any source
# run BWA command
# run samtools sam to bam conversion command
# run samtools bam sort command 
# run samtools index
# run picard mark PCR Duplicates
# run samtools index again
# run GATK BaseRecalibrator #### need to use big VCF file # work in progress
# run GATK AnalyzeCovariates ### work in progress need some R libraries installed 
# run GATK ApplyBQSR
	
###############################################################################################

import os
import sys
import subprocess
import csv
from optparse import OptionParser
from utils import *
from dependencies import *
##################################################################################################

print BWAsoftware

def display(message):
    print(message)

parser = OptionParser()
parser.add_option("-p", "--Project_name", dest="projectname",
				  help="The name of your project")
parser.add_option("-n", "--nthreads", dest="nthreads",
				  help="How many threads you want to use")

(options, args) = parser.parse_args()

myProject = options.projectname
nthreads = options.nthreads

def display(message):
    print(message)

myProject = str(myProject)
myProject = myProject.lstrip('[')
myProject = myProject.lstrip("'")
myProject = myProject.rstrip(']')
myProject = myProject.rstrip("'")

#print(myProject)


display("SGUL Genetics Research Centre Alignment Pipeline\n")

print("your project is :")
print(myProject)

print("\n")

dirpath = os.getcwd()
projectDataDir=dirpath + "/" + "UBAMs" + "/" + myProject + "/"
print(os.listdir(projectDataDir))

#generate list of all the samples in the project directory 
mySamples = os.listdir(projectDataDir)

#for each sample in the project folder, identify the bam file, make new fastq and then send to BWA alignment
for sample in mySamples:

	sampleDirectory = projectDataDir + sample + "/"

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
	
	
	for file in os.listdir(sampleDirectory):
	    if file.endswith(".bam"):

			print(os.path.join(sampleDirectory, file))
			INPUTBAM = (os.path.join(sampleDirectory, file))
	
	INPUTBAM = "I=" + INPUTBAM
	
	External_Unaligned =  DRIVE + "/Exomes/tmp"
	
	FASTQ1out = External_Unaligned + "/" + myProject + "/" + sample + "/" + sample + "_output_R1.fastq"
	FASTQ2out = External_Unaligned + "/" + myProject + "/" + sample + "/" + sample + "_output_R2.fastq"
		
	FASTQ1output = "FASTQ=" + FASTQ1out
	FASTQ2output = "SECOND_END_FASTQ=" + FASTQ2out
	
	BAM_toFASTQ_command = [java, '-jar', picard, 'SamToFastq', 'INCLUDE_NON_PF_READS=true', 'INCLUDE_NON_PRIMARY_ALIGNMENTS=false', 'COMPRESSION_LEVEL=0',
	'VALIDATION_STRINGENCY=SILENT', 'QUIET=true', INPUTBAM, FASTQ1output, FASTQ2output]
	
	External_Unaligned_Project = External_Unaligned + "/"+ myProject
	
	makeDirectory = ['mkdir', External_Unaligned_Project] 
	subprocess.call(makeDirectory)
	
	SampleDir = External_Unaligned + "/" + myProject + "/" + sample
	
	makeDirectory = ['mkdir', SampleDir] 
	subprocess.call(makeDirectory)
		
	BWAcommand = [BWAsoftware, 
	'mem', BWAindex, FASTQ1out, FASTQ2out,'-t', '8', '-R', samHeader,'-o', outputSAM]

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
	
	subprocess.check_call(BAM_toFASTQ_command) # run BAMtoFASTQ
	
	subprocess.check_call(BWAcommand) # run BWA

	#remove fastq as they take up too much space
	os.remove(FASTQ1out)
	os.remove(FASTQ2out)
	
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
		
	
