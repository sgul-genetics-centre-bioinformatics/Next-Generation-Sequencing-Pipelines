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

trimOUTdir = "/homedirs_APittman/sgul/shares/Mimir/Genetics_Centre_Bioinformatics_Mimir/Exomes/Unaligned/"

display("SGUL Genetics Research Centre Exome Analysis Pipeline\n")

print("your project is :")
print(myProject)
print("\n")
print("Number of selected threads: "+nthreads)
dirpath = os.getcwd()
projectDataDir=dirpath + "/" + "raw_FASTQ" + "/" + myProject + "/"
print(os.listdir(projectDataDir))

#generate list of all the samples in the project directory
mySamples = os.listdir(projectDataDir)

#for each sample in the project folder identify the files for trimming
command = []
for sample in mySamples:
    print sample
    sampleDirectory = projectDataDir + sample + "/"
    #print sampleDirectory
    myinputfiles = [sampleDirectory+x for x in os.listdir(sampleDirectory)]
    #print myinputfiles

    command.append(java+' -jar '+Trimmomatic+' PE -threads 2 '+' '.join(myinputfiles)+' -baseout '+trimOUTdir+myProject+'/'+sample+'/'+sample+'.gz')

parallel_command(command, n=nthreads, wordir=trimOUTdir+myProject + '/', name='log_trimming.txt')


