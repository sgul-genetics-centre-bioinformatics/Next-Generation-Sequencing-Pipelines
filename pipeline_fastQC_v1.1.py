#!/usr/bin/env python

#SGUL GENETICS CENTRE EXOME PIPELINE APRIL 2019
#Alan Pittman & Dionysios Grigoriadis

####Step By Step
#1)FastQC on the trimmed fastq files
#2)MultiQC on the fastqc output

#subprocess.check_call(FASTQCarguments)

import os
import sys
import subprocess
import csv
from optparse import OptionParser
from utils import *
from dependencies import *

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

print(myProject)

fastqcOUTdir = "/homedirs_APittman/sgul/shares/Mimir/Genetics_Centre_Bioinformatics_Mimir/Exomes/FastQC/"

display("SGUL Genetics Research Centre Exome Analysis Pipeline\n")

print("your project is :")
print(myProject)
print("\n")
print("Number of selected threads: "+nthreads)
dirpath = os.getcwd()
projectDataDir=dirpath + "/" + "Unaligned" + "/" + myProject + "/"
print(os.listdir(projectDataDir))

#generate list of all the samples in the project directory 
mySamples = os.listdir(projectDataDir)

#for each sample in the project folder identify the files for fastqc analysis 
for sample in mySamples:
	print sample
	sampleDirectory = projectDataDir + sample + "/"
	print sampleDirectory
	
	outDir="--outdir="+fastqcOUTdir
	output= outDir + myProject + "/" + sample
	print output
	
	myinputfiles = os.listdir(sampleDirectory)
	print myinputfiles
	
	#make analysis output project directory
	
	outputProject = fastqcOUTdir + myProject
	makeDirectoryP = ['mkdir', outputProject] 
	subprocess.call(makeDirectoryP)	
	
	#make anlysis output directory:
	sampleFolder = outputProject + "/" + sample
	makeDirectoryS = ['mkdir', sampleFolder] 
	subprocess.call(makeDirectoryS)		
	command = []
	for file in myinputfiles:

		input = sampleDirectory + file
		print input
		
		command.append(fastqc+' '+input+' '+output)
parallel_command(command, n=nthreads, wordir=fastqcOUTdir+myProject + '/', name='log_fqc.txt')
		
#MultiQC
mqc_command = multiqc+' '+fastqcOUTdir+myProject+' -o '+fastqcOUTdir+myProject
parallel_command([mqc_command], n=nthreads, wordir=fastqcOUTdir+myProject + '/', name='log_mqc.txt')
#print(mqc_command)