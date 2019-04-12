#!/usr/bin/env python

#SGUL GENETICS CENTRE EXOME PIPELINE APRIL 2019
#Alan Pittman & Dionysios Grigoriadis

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
import csv
##################################################################################################

print BWAsoftware

def display(message):
    print(message)

parser = OptionParser()
parser.add_option("-p", "--Project_name", dest="projectname",
				  help="The name of your project")
parser.add_option("-n", "--nthreads", dest="nthreads",
				  help="How many threads you want to use. Please specify three numbers in comma separated format. "
					   "Each of those three numbers correspond to number of CPUs will be used in some of the jobs in this script.\n"
					   "First Number: CPUs for not very heavy tasks like index and sort (Recommended for Stats 3 is 8).\n"
					   "Second Number: CPUs for intermediate tasks like bwa mem alignment (Recommended for Stats 3 is 4).\n"
					   "Third Number: CPUs for really heavy tasks like mark Duplicates (Recommended for Stats 3 is 2).\n"
					   "Recommended for stats3 input: 8,4,2")

(options, args) = parser.parse_args()

myProject = options.projectname
nthreads = options.nthreads
nthreads = [int(x.strip()) for x in nthreads.split(",")]

def display(message):
    print(message)

myProject = str(myProject)
myProject = myProject.lstrip('[')
myProject = myProject.lstrip("'")
myProject = myProject.rstrip(']')
myProject = myProject.rstrip("'")

#print(myProject)


display("SGUL Genetics Research Centre Alignment Pipeline: Data pre-processing\n")

print("your project is :")
print(myProject)

print("\n")

dirpath = os.getcwd()
projectDataDir=dirpath + "/" + "Unaligned" + "/" + myProject + "/"
alignedOUTdir = dirpath + "/" + "Aligned/"
print(os.listdir(projectDataDir))

#generate list of all the samples in the project directory 
mySamples = os.listdir(projectDataDir)

BWAcommand = []
samtoolsViewCommand = []
samtoolsSortCommand = []
samtoolsINDEXCommand = []
picardMARKDUPLICATESCommand = []
samtoolsINDEXCommand2 = []
gatkBaserecalibratorCommand = []
gatkAnalyseCovariatesCommand = []
gatkApplyBQSRCommand = []
outputSAMs = []
outputBAMs = []
outputSorstedBAMs = []
SorstedUniqueBAMs = []
SorstedUniqueBAMindices = []
outputSorstedBAMindices = []
recal_data_tables = []
f1s = []
f2s = []
samHeaders=[]
SorstedUniqueRecalibratedBAMs = []

nosamples = len(mySamples)

#for each sample in the project folder, identify the bam file, make new fastq and then send to BWA alignment
projectFolder = alignedOUTdir + myProject
makeDirectoryProject = ['mkdir', projectFolder]
subprocess.call(makeDirectoryProject)

for sample in mySamples:

	sampleDirectory = projectDataDir + sample + "/"
	#make analysis output directory
	sampleFolder = alignedOUTdir + myProject + "/" + sample
	makeDirectory = ['mkdir', sampleFolder]
	subprocess.call(makeDirectory)

	############# SAMPLE VARIABLES ###################################
	outputSAM = sampleFolder + "/" + sample + ".sam" # output
	outputSAMs.append(outputSAM)
	samHeader = "'@RG\\tID:" + sample + "\\tSM:" + sample + "\\tLB:" + sample + "\\tPL:ILLUMINA'"

	print(samHeader)

	outputBAM = sampleFolder + "/" + sample + ".bam" # output bam file
	outputBAMs.append(outputBAM)

	outputSorstedBAM = sampleFolder + "/" + sample + "_sorted.bam" # output sorted bam file
	outputSorstedBAMs.append(outputSorstedBAM)

	SorstedUniqueBAM = sampleFolder + "/" + sample + "_sorted_unique" + ".bam" #output sorted unique bam file
	SorstedUniqueBAMs.append(SorstedUniqueBAM)

	picardIbam = "I=" + outputSorstedBAM

	picardObam = "O=" + SorstedUniqueBAM

	picardMfile = "M=" + sampleFolder + "/" + sample + "_marked_dup_metrics.txt"

	SorstedUniqueBAMindex = sampleFolder + "/" + sample + "_sorted_unique" + ".bam" + ".bai"
	SorstedUniqueBAMindices.append(SorstedUniqueBAMindex)

	outputSorstedBAMindex = sampleFolder + "/" + sample + "_sorted.bam.bai"
	outputSorstedBAMindices.append(outputSorstedBAMindex)

	recal_data_table = sampleFolder + "/" + sample + "_recal_data.table"
	recal_data_tables.append(recal_data_table)

	AnalyzeCovariates_pdf = sampleFolder + "/" + sample + "_AnalyzeCovariates.pdf"

	SorstedUniqueRecalibratedBAM = sampleFolder + "/" + sample + "_sorted_unique_recalibrated" + ".bam"
	SorstedUniqueRecalibratedBAMs.append(SorstedUniqueRecalibratedBAM)

	########## COMMAND LINE ARGUMENTS #################################
	FASTQ1in = sampleDirectory + sample + "_1P.gz"
	f1s.append(FASTQ1in)

	FASTQ2in = sampleDirectory + sample + "_2P.gz"
	f2s.append(FASTQ2in)

	BWAcommand.append(BWAsoftware + ' mem ' + BWAindex+' '+FASTQ1in+' '+FASTQ2in+' -t 8 -R '+samHeader+' -o '+outputSAM)

	samtoolsViewCommand.append(samtoolsSoftware+' view '+'-Sb '+outputSAM+' -o '+outputBAM)

	samtoolsSortCommand.append(samtoolsSoftware+' sort '+'-m '+' 5000000000 '+outputBAM+' -o '+outputSorstedBAM)

	samtoolsINDEXCommand.append(samtoolsSoftware+' index '+outputSorstedBAM)

	picardMARKDUPLICATESCommand.append(java+' -jar '+picard+' MarkDuplicates '+picardIbam+' '+picardObam+' '+picardMfile)

	samtoolsINDEXCommand2.append(samtoolsSoftware+' index '+SorstedUniqueBAM)

	gatkBaserecalibratorCommand.append(java+' -jar '+gatk+' BaseRecalibrator -I '+SorstedUniqueBAM+' -R '+BWAindex+' --known-sites '+refknownsitesSNPS+' -O '+recal_data_table)

	gatkAnalyseCovariatesCommand.append(java+' -jar '+gatk+' AnalyzeCovariates -bqsr '+recal_data_table+' -plots '+AnalyzeCovariates_pdf)

	gatkApplyBQSRCommand.append(java+' -jar '+gatk+' ApplyBQSR -R '+BWAindex+' -I '+SorstedUniqueBAM+' --bqsr-recal-file '+recal_data_table+' -O '+SorstedUniqueRecalibratedBAM)

################################################################################
#Generate commands that check number of reads in fastqs and alignment files
chfa1_command = ["echo $(zcat "+x+"|wc -l)/4|bc" for x in f1s]
chfa2_command = ["echo $(zcat "+x+"|wc -l)/4|bc" for x in f1s]
chfa_command = [samtoolsSoftware+' flagstat '+x for x in outputSorstedBAMs]
chfau_command = [samtoolsSoftware+' flagstat '+x for x in SorstedUniqueBAMs]
chfar_command = [samtoolsSoftware+' flagstat '+x for x in SorstedUniqueRecalibratedBAMs]

#EXECUTE THE COMMANDS

################# RUN COMMANDS #####################################

#Alignment
#parallel_command(BWAcommand, nthreads[1], alignedOUTdir, 'BWA-MEM.log') #n=2
#

if len(get_files_with_suffix(dir=alignedOUTdir+"/"+myProject, suffix2=".sam", mindepth=True))!=nosamples:
	print("Problem with alignment outputs. Please check everything is alright first and then move to the next step.")
	raise

print("OK")

for f in f1s:
	try:
		os.remove(f)
	except:
		print("!")


for f in f2s:
	try:
		os.remove(f)
	except:
		print("!")
#

#Sam to BAMs
parallel_command(samtoolsViewCommand, nthreads[2], projectFolder+'/', 'sam2bam.log') #n=8 can be 12
#
if len(get_files_with_suffix(dir=alignedOUTdir+"/"+myProject, suffix2=".bam", mindepth=True))!=nosamples:
	print("Problem with conversion outputs. Please check everything is alright first and then move to the next step.")
	raise

for f in outputSAMs:
	try:
		os.remove(f)
	except:
		print("!")
#
#Sort and Index BAMs
parallel_command(samtoolsSortCommand, nthreads[2], projectFolder+'/', 'bamsort.log') #n-
parallel_command(samtoolsINDEXCommand, nthreads[2], projectFolder+'/', 'bamindex.log')

if len(get_files_with_suffix(dir=alignedOUTdir+"/"+myProject, suffix2="_sorted.bam", mindepth=True))!=nosamples:
	print("Problem with sorting/indexing outputs. Please check everything is alright first and then move to the next step.")
	raise


for f in outputBAMs:
	try:
		os.remove(f)
	except:
		print("!")

#Mark Duplicates
parallel_command(picardMARKDUPLICATESCommand, nthreads[0], projectFolder+'/', 'markdups.log')
parallel_command(samtoolsINDEXCommand2, nthreads[2], projectFolder+'/', 'bamindex2.log')

if len(get_files_with_suffix(dir=alignedOUTdir+"/"+myProject, suffix2="_unique.bam", mindepth=True))!=nosamples:
	print("Problem with mark_duplicates outputs. Please check everything is alright first and then move to the next step.")
	raise

for f in outputSorstedBAMs:
	try:
		os.remove(f)
	except:
		print("!")

for f in outputSorstedBAMindices:
	try:
		os.remove(f)
	except:
		print("!")

#Base recalibration / BQSR
parallel_command(gatkBaserecalibratorCommand, nthreads[0], projectFolder+'/', 'base_recal.log')
parallel_command(gatkAnalyseCovariatesCommand, nthreads[0], projectFolder+'/', 'analyse_covar.log')
parallel_command(gatkApplyBQSRCommand, nthreads[0], projectFolder+'/', 'applyBQSR.log')

if len(get_files_with_suffix(dir=alignedOUTdir+"/"+myProject, suffix2="_recalibrated.bam", mindepth=True))!=nosamples:
	print("Problem with recalibration outputs. Please check everything is alright first and then move to the next step.")
	raise

for f in SorstedUniqueBAMs:
	try:
		os.remove(f)
	except:
		print("!")

for f in SorstedUniqueBAMindices:
	try:
		os.remove(f)
	except:
		print("!")


for f in recal_data_tables:
	try:
		os.remove(f)
	except:
		print("!")


qc_dir = {}
######QC STEP######
# Check how many reads in fastq files and how many aligned ones
# for i in range(0,len(chfa1_command)):
# 	#print(i)
# 	p1 = subprocess.Popen(chfa1_command[i], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# 	output1, error1 = p1.communicate()
# 	p2 = subprocess.Popen(chfa2_command[i], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# 	output2, error2 = p2.communicate()
# 	p3 = subprocess.Popen(chfa_command[i], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# 	output3, error3 = p3.communicate()
# 	p4 = subprocess.Popen(chfau_command[i], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# 	output4, error4 = p4.communicate()
# 	p5 = subprocess.Popen(chfar_command[i], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# 	output5, error5 = p5.communicate()
# 	qc_dir[mySamples[i]]=[int(output1.strip()), int(output2.strip()), int(output3.split('+')[0].strip()), int(output4.split('+')[0].strip()),int(output4.split('+')[0].strip())]
#
# #and write a csv_file
# with open(projectFolder+'/raw_to_alignment_qc.csv', 'w') as f:
# 	f.write(','.join(['Sample','1P_raw_reads','2P_raw_reads','aligned_reads','aligned_dedup_reads','aligned_recalib_reads\n']))
# 	for key in qc_dir.keys():
# 		f.write("%s,%s\n"%(key,','.join([str(x) for x in qc_dir[key]])))


