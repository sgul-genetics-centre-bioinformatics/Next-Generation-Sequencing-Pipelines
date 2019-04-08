#!/usr/bin/env python

#SGUL GENETICS CENTRE EXOME PIPELINE JUNE 2018
#Alan Pittman

# run annovar annotation 
	
###############################################################################################

import os
import sys
import subprocess
import csv

#resources:
###############################################################################################

convert2annovar = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/annovar/convert2annovar.pl"
tableAnnovar = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/annovar/table_annovar.pl"
humandb = "/homes/athosnew/Genetics_Centre_Bioinformatics/resourses/annovar/humandb"

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


display("SGUL Genetics Research Centre Annotation Pipeline\n")


print("your project is :")
print(myProject)

print("\n")

dirpath = os.getcwd()
projectDataDir=dirpath + "/" + "VCF" + "/" + myProject + "/"
print(os.listdir(projectDataDir))

#generate list of all the samples in the project directory 
mySamples = os.listdir(projectDataDir)

Annodir = "/homes/athosnew/Genetics_Centre_Bioinformatics/Exomes/Annotated/"
VCFOUTdir = "/homes/athosnew/Genetics_Centre_Bioinformatics/Exomes/VCF/"


for sample in mySamples:
		
	############# SAMPLE VARIABLES ###################################
	

	sampleFolderVCF = VCFOUTdir + myProject + "/" + sample

	FilteredsampleVCF = sampleFolderVCF + "/" + sample + "_MetricFilters.vcf"
	
	#make analysis output directorys (Annotated)
	
	projectFolder = Annodir + myProject 
	makeDirectoryAnnoProject = ['mkdir', projectFolder] 
	subprocess.call(makeDirectoryAnnoProject)
	
	sampleFolderAnno = Annodir + myProject + "/" + sample
	makeDirectoryAnnoProjectSample = ['mkdir', sampleFolderAnno] 
	subprocess.call(makeDirectoryAnnoProjectSample)
	
	AVinput = sampleFolderAnno + "/" + sample + ".avinput"
	
	Annovaroutput = sampleFolderAnno + "/" +sample + ".annovar"
	
	########## COMMAND LINE ARGUMENTS #################################
	
	convert2annovarCommand = [convert2annovar, '-format', 'vcf4', FilteredsampleVCF, '-allsample', '-withfreq', '-includeinfo', '-outfile', AVinput]
	
	print convert2annovarCommand
	
	annovarCommand = [tableAnnovar, AVinput, humandb, '-buildver', 'hg19', '-out', Annovaroutput, '-remove',
	'-protocol', 'refGene,ensGene,cytoBand,genomicSuperDups,1000g2015aug_all,esp6500siv2_ea,esp6500siv2_aa,esp6500siv2_all,exac03,kaviar_20150923,gnomad_exome,gnomad_genome,hrcr1,gme,avsnp150,dbnsfp33a,dbnsfp31a_interpro,spidex,revel,mcap,clinvar_20170905',
	'-operation', 'g,g,r,r,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f',
	'-genericdbfile', 'hg19_spidex.txt',
	'-argument', '-hgvs,-hgvs,,,,,,,,,,,,,,,,,,,',
	'-arg', '-splicing 5,-splicing 5,,,,,,,,,,,,,,,,,,,',
	'-nastring', '"NA"', '-polish', '-otherinfo']

	################ RUN COMMANDS #####################################
	
	subprocess.check_call(convert2annovarCommand)
	
	print annovarCommand
	
	subprocess.check_call(annovarCommand)	