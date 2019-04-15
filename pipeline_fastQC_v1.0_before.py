#!/usr/bin/env python

#subprocess.check_call(FASTQCarguments)

import os
import sys
import subprocess
import csv

def display(message):
    print(message)

myProject = sys.argv
del myProject[0]

myProject = str(myProject)
myProject = myProject.lstrip('[')
myProject = myProject.lstrip("'")
myProject = myProject.rstrip(']')
myProject = myProject.rstrip("'")    

softwareargumants = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/FastQC/fastqc"
fastqcOUTdir = "/homes/athosnew/Genetics_Centre_Bioinformatics/Exomes/FastQC_before/"

display("SGUL Genetics Research Centre Exome Analysis Pipeline\n")

print("your project is :")
print(myProject)

print("\n")

dirpath = os.getcwd()
projectDataDir=dirpath + "/" + "raw_FASTQ" + "/" + myProject + "/"
print(os.listdir(projectDataDir))

#generate list of all the samples in the project directory 
mySamples = os.listdir(projectDataDir)

#for each sample in the project folder identify the files for fastqc analysis 
for sample in mySamples:
	print sample
	sampleDirectory = projectDataDir + sample + "/"
	print sampleDirectory
	
	outDir="--outdir=/homes/athosnew/Genetics_Centre_Bioinformatics/Exomes/FastQC_before//"
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
	
	for file in myinputfiles:

		input = sampleDirectory + file
		print input
		
		command = [softwareargumants, input, output]
		subprocess.check_call(command) # run fastqc command 
		
	
