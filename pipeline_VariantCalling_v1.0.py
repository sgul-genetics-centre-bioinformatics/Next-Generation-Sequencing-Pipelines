#!/usr/bin/env python

#SGUL GENETICS CENTRE EXOME PIPELINE JUNE 2018
#Alan Pittman

#standard pipeline steps:
###############################################################################################

# run GATK haplotype Caller etc.
	
###############################################################################################

import os
import sys
import subprocess
import csv

#resources:
###############################################################################################

ExomeTarget = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/Genome_reference_files/BroadExACExomeIntervlas.bed"

BWAindex = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/Genome_reference_files/human_g1k_v37.fasta"
samtoolsSoftware = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/samtools-1.8/samtools"
java = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/java/jre1.8.0_171/bin/java"
picard = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/picard-2.815/picard.jar"
gatk = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/gatk-4.0.4.0/gatk-package-4.0.4.0-local.jar"
refknownsitesSNPS = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/Genome_reference_files/1000G_phase1.snps.high_confidence.hg19.sites.vcf"
refknownsitesINDELS = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/Genome_reference_files/Mills_and_1000G_gold_standard.indels.hg19.vcf"


#Think about VariantFiltration
##FILTER=<ID=DRAGENHardSNP,Description="Set if true:QD < 2.0 || MQ < 30.0 || FS > 60.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0">
##FILTER=<ID=DRAGENHardINDEL,Description="Set if true:QD < 2.0 || ReadPosRankSum < -20.0 || FS > 200.0">


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


display("SGUL Genetics Research Centre Variant Calling Pipeline\n")


print("your project is :")
print(myProject)

print("\n")

dirpath = os.getcwd()
projectDataDir=dirpath + "/" + "Aligned" + "/" + myProject + "/"
print(os.listdir(projectDataDir))

#generate list of all the samples in the project directory 
mySamples = os.listdir(projectDataDir)

VCFOUTdir = "/homes/athosnew/Genetics_Centre_Bioinformatics/Exomes/VCF/"
gVCFOUTdir = "/homes/athosnew/Genetics_Centre_Bioinformatics/Exomes/gVCF/"

AlignedDir = "/homes/athosnew/Genetics_Centre_Bioinformatics/Exomes/Aligned/"

for sample in mySamples:

	#make analysis output directorys (VCF and GVCF)
	
	projectFolder = VCFOUTdir + myProject 
	makeDirectoryVCFProject = ['mkdir', projectFolder] 
	subprocess.call(makeDirectoryVCFProject)
	
	sampleFolderVCF = VCFOUTdir + myProject + "/" + sample
	makeDirectoryVCFProjectSample = ['mkdir', sampleFolderVCF] 
	subprocess.call(makeDirectoryVCFProjectSample)
	
	
	projectFolder = gVCFOUTdir + myProject 
	makeDirectoryGVCFProject = ['mkdir', projectFolder] 
	subprocess.call(makeDirectoryGVCFProject)
	
	sampleFolderGVCF = gVCFOUTdir + myProject + "/" + sample
	makeDirectoryGVCFProjectSample = ['mkdir', sampleFolderGVCF] 
	subprocess.call(makeDirectoryGVCFProjectSample)
	
	
	############# SAMPLE VARIABLES ###################################

	SorstedUniqueRecalibratedBAM = AlignedDir + "/" + myProject + "/" + sample + "/" + sample + "_sorted_unique_recalibrated" + ".bam"
	
	bamout = AlignedDir + "/" + myProject + "/" + sample + "/" + sample + "bamout" + ".bam"
	
	sampleVCF = sampleFolderVCF + "/" + sample + "_raw.vcf"
	FilteredsampleVCF = sampleFolderVCF + "/" + sample + "_MetricFilters.vcf"
	
	sampleGVCF = sampleFolderGVCF + "/" + sample + ".g.vcf.gz"
	
	########## COMMAND LINE ARGUMENTS #################################
	
	gatkHaplotypeCaller_VCF_Command = [java, '-jar', gatk, 'HaplotypeCaller', '-I', SorstedUniqueRecalibratedBAM,
	'-R', BWAindex, '--intervals', ExomeTarget, '-O', sampleVCF, '-bamout', bamout]
	
	gatkVariantFiltration_VCF_Command = [java, '-jar', gatk, 'VariantFiltration', '-V', sampleVCF, '-O', FilteredsampleVCF,
	'-R', BWAindex, 
	'--genotype-filter-expression', 'GQ < 30.0', '--genotype-filter-name',
	'LowGQ', '--filter-expression', 'QD < 1.5', '--filter-name', 'LowQD', 
	'--filter-expression', 'DP < 6', '--filter-name', 'LowCoverage',
	'--filter-expression', 'SOR > 10.0', '--filter-name', 'StrandBias']
	
	gatkHaplotypeCaller_gVCF_Command = [java, '-jar', gatk, 'HaplotypeCaller', '-I', SorstedUniqueRecalibratedBAM,
	'-R', BWAindex, '--intervals', ExomeTarget, '-O', sampleGVCF, '-ERC', 'GVCF']
	

	################ RUN COMMANDS #####################################
	
	subprocess.check_call(gatkHaplotypeCaller_VCF_Command)
	subprocess.check_call(gatkVariantFiltration_VCF_Command)
	subprocess.check_call(gatkHaplotypeCaller_gVCF_Command)