#!/usr/bin/env python

#SGUL GENETICS CENTRE EXOME PIPELINE APRIL 2019
#Alan Pittman & Dionysios Grigoriadis

#standard pipeline steps:
###############################################################################################

# run GATK haplotype Caller etc.
	
###############################################################################################

import os
import sys
import subprocess
import csv
from optparse import OptionParser
from utils import *
from dependencies import *
import csv

#Think about VariantFiltration
##FILTER=<ID=DRAGENHardSNP,Description="Set if true:QD < 2.0 || MQ < 30.0 || FS > 60.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0">
##FILTER=<ID=DRAGENHardINDEL,Description="Set if true:QD < 2.0 || ReadPosRankSum < -20.0 || FS > 200.0">

##################################################################################################

def display(message):
    print(message)

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
nthreads = int(options.nthreads)

myProject = str(myProject)
myProject = myProject.lstrip('[')
myProject = myProject.lstrip("'")
myProject = myProject.rstrip(']')
myProject = myProject.rstrip("'")    


display("SGUL Genetics Research Centre Variant Calling Pipeline: Variant Calling\n")


print("your project is :")
print(myProject)

print("\n")

dirpath = os.getcwd()
projectDataDir=dirpath + "/" + "Aligned" + "/" + myProject + "/"
VCFOUTdir = dirpath + "/" + "VCF/"
gVCFOUTdir = dirpath + "/" + "gVCF/"
AlignedDir = dirpath + "/" + "Aligned/"

print(os.listdir(projectDataDir))

#generate list of all the samples in the project directory 
mySamples = os.listdir(projectDataDir)
mySamples = [x for x in mySamples if not x.endswith('.csv')]
mySamples = [x for x in mySamples if not x.endswith('.log')]

#VCFOUTdir = "/homedirs_APittman/sgul/shares/Mimir/Genetics_Centre_Bioinformatics_Mimir/Exomes/VCF/"
#gVCFOUTdir = "/homedirs_APittman/sgul/shares/Mimir/Genetics_Centre_Bioinformatics_Mimir/Exomes/gVCF/"

#AlignedDir = "/homedirs_APittman/sgul/shares/Mimir/Genetics_Centre_Bioinformatics_Mimir/Exomes/Aligned/"

gatkHaplotypeCaller_VCF_Command=[]
gatkVariantFiltration_VCF_Command=[]
gatkHaplotypeCaller_gVCF_Command=[]

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
	gatkHaplotypeCaller_VCF_Command.append(java + ' -jar ' + gatk + ' HaplotypeCaller -I ' + SorstedUniqueRecalibratedBAM + \
	' -R ' + BWAindex + ' --intervals ' + ExomeTarget + ' -O ' + sampleVCF + ' -bamout ' + bamout)

	gatkVariantFiltration_VCF_Command.append(java + ' -jar ' + gatk + ' VariantFiltration -V ' + sampleVCF + ' -O ' + FilteredsampleVCF + \
	' -R ' + BWAindex + \
	' --genotype-filter-expression "GQ < 30.0" --genotype-filter-name LowGQ --filter-expression "QD < 1.5" --filter-name LowQD' + \
	' --filter-expression "DP < 6" --filter-name LowCoverage --filter-expression "SOR > 10.0" --filter-name "StrandBias"')

	gatkHaplotypeCaller_gVCF_Command.append(java + ' -jar ' + gatk + ' HaplotypeCaller -I ' + SorstedUniqueRecalibratedBAM + \
	' -R ' + BWAindex + ' --intervals ' + ExomeTarget + ' -O ' + sampleGVCF + ' -ERC' + ' GVCF ')


################ RUN COMMANDS #####################################
parallel_command(gatkHaplotypeCaller_VCF_Command, nthreads, VCFOUTdir + myProject + "/", 'HaplotypeCaller.log')
parallel_command(gatkVariantFiltration_VCF_Command, nthreads, VCFOUTdir + myProject + "/", 'VariantFiltration.log')
parallel_command(gatkHaplotypeCaller_gVCF_Command, nthreads, gVCFOUTdir + myProject + "/", 'HaplotypeCaller_GVCF.log')