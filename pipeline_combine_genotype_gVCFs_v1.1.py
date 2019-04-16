#Dionysios Grigoriadis

#Program to genotype gVCF files in batches to join later for cohort (exome-wide studies etc.)

#Step_by_step:
#1)Combine gVCF files into a joint gVCF file,
#2)Genotype joint gVCF file

#Version 1.1
# - Written in Python instead of bash
# - Log files will be written in the output directories
#################################################################################################################
import os
import sys
import subprocess
import csv
from optparse import OptionParser

#OUR RESOURCES:
from dependencies import *
from utils import *

#USER INPUT
parser = OptionParser()
parser.add_option("-p", "--Project_name", dest="projectname",
				  help="The name of your project/projects of the gVCF files you want to merge. If many projects, the input should be comma separated")
parser.add_option("-l", "--Locations", dest="glocname",
				  help="Instead of project names you can specify the paths of the gVCF files parent directories you want to merge. The directories you specify should have at least 2 gVCF files in them. The input should be comma separated")
parser.add_option("-o", "--output", dest="output",
				  help="suffix of the result files (e.g. comb for ./comb.g.vcf.gz")

(options, args) = parser.parse_args()

pname = options.projectname
gname = options.glocname
output = options.output

##############################################################
#Set-up working and output directories
dirpath = os.getcwd()

temp_dir = dirpath+"D/tmp/"+output+"/"

projectDataDir=dirpath + "/" + "gVCF" + "/"

gvcf_output = temp_dir+output+".g.vcf.gz"
genotyped_output = temp_dir+output+".vcf"


if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

##############################################################
#Appropriate handling of user input
if pname == None and gname == None:
    print("Please provide either project name(s) or gVCF locations")
    raise(ValueError)

elif pname != None and gname != None:
    print("Please specify either project name or gvcf parent directories")
    raise (ValueError)

elif pname != None and gname == None:
    print("Project names were detected")
    inputs = [x.strip() for x in pname.split(",")]
    gvcfparents = [projectDataDir+x+"/" for x in inputs]

elif pname == None and gname != None:
    print("gVCF parent folder names were detected")
    gvcfparents = [x.strip() for x in gname.split(",")]

print("\n")
print("Writing the txt file with the gvcf names")

##############################################################
#Creating a text file with all the names of the detected gVCF files we would like to merge
gvcf_variant=[]
for par in gvcfparents:
    gvcf_variant.extend(["--variant "+par+x+"/"+x+".g.vcf.gz " for x in next(os.walk(par))[1]])

f=open(temp_dir+'temp_vars.txt', 'w+')
for item in gvcf_variant:
    f.write("%s\n" % item)
f.close()

print(temp_dir+'temp_vars.txt')
print("\n")

##############################################################
##RUNNING THE COMMANDS
#Combine GVCFs
print("\n")
print("Combine gVCFs")
comm = java+' -Xmx10g -jar '+gatk+' CombineGVCFs -R '+BWAindex+" `cat "+temp_dir+"temp_vars.txt` -O "+gvcf_output
parallel_command([comm], 1, temp_dir+"/", 'combine.log') #n=2
print(comm)
print("\n")

os.remove(temp_dir+'temp_vars.txt')

#Genotype the combined GVCF file
print("\n")
print("Genotype the joint gVCF")
comm = java+' -Xmx10g -jar '+gatk+' GenotypeGVCFs -R '+BWAindex+" --dbsnp "+refknownsitesSNPS+" --variant "+gvcf_output+" --output "+genotyped_output
parallel_command([comm], 1, temp_dir+"/", 'genotype.log') #n=2

os.remove(gvcf_output)

print("\n")
print(comm)
##############################################################