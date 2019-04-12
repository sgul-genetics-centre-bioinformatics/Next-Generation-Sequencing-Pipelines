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
				  help="The suffix of the joint vcf you want to filter")
#parser.add_option("-o", "--output", dest="output",
#				  help="suffix of the result files (e.g. comb for ./comb.g.vcf.gz")

(options, args) = parser.parse_args()

pname = options.projectname
#gname = options.glocname
#output = options.output


#pname='postergaard_athos_and_25032019'
pname = pname.strip()

##############################################################
#Set-up working and output directories
dirpath = os.getcwd()
temp_dir = dirpath+"/tmp/"+pname+"/"
cohort_dir = dirpath+"/Filtered_Joint_called_VCFs/"
out_dir = cohort_dir + pname + "/"
vfilt_output = temp_dir+pname+"_HF.vcf"
vrecal1_output = temp_dir+pname+"_SNP.recal"
vsqr_output = temp_dir+pname+"_HF_SNP.recal.snps.vcf"
vrecal2_output = temp_dir+pname+"_INDEL.recal"
vsqr_final_output = out_dir+pname+"_HF4_SNP.recal.snps.indel.vcf"
vsqr_final_annotated_output = out_dir+pname+"_HF4_SNP.recal.snps.indel.dbSNP.vcf"


if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)


if not os.path.exists(cohort_dir):
    os.makedirs(cohort_dir)



if not os.path.exists(out_dir):
    os.makedirs(out_dir)

##############################################################
##############################################################
##RUNNING THE COMMANDS
#Variant Filtration
print("\n")
print("VariantFiltration")
comm = java+' -Xmx10g -jar '+gatk+' VariantFiltration -R '+BWAindex+" -V "+temp_dir+pname+".vcf "+'--genotype-filter-expression "DP < 6" ' \
        '--genotype-filter-name "LowDepth" --genotype-filter-expression "GQ < 20.0 && GQ > 0.0" --genotype-filter-name "LowGQ" -O '+vfilt_output
parallel_command([comm], 1, temp_dir+"/", 'VariantFiltration.log') #n=2
print(comm)
print("\n")

#os.remove(temp_dir+'temp_vars.txt')

#VariantRecalibrator
print("\n")
print("VariantRecalibrator")
comm = java+' -Xmx10g -jar '+gatk+' VariantRecalibrator -R '+BWAindex+" -V "+vfilt_output+" -tranche 100.0 -tranche 99.9 -tranche 99.5 " \
       "-tranche 99.0 -tranche 90.0 -mode SNP --tranches-file "+temp_dir+pname+"_SNP.tranches --rscript-file "+temp_dir+pname+".plots.R " \
       "--resource hapmap,known=false,training=true,truth=true,prior=15.0:"+hapmap+" --resource omni,known=false,training=true,truth=true," \
       "prior=12.0:"+omni+" --resource 1000G,known=false,training=true,truth=false,prior=10.0:"+G1000+" --resource dbsnp,known=true,training=" \
       "false,truth=false,prior=2.0:"+dbsnp+" -an QD -an MQ -an MQRankSum -an ReadPosRankSum -an FS -an SOR --output "+vrecal1_output
parallel_command([comm], 1, temp_dir+"/", 'VariantRecalibrator.log') #n=2

#os.remove(gvcf_output)
print(comm)
print("\n")

#ApplyVQSR
print("\n")
print("ApplyVQSR")
comm = java+' -Xmx10g -jar '+gatk+' ApplyVQSR -R '+BWAindex+" -mode SNP --truth-sensitivity-filter-level 99.5 -V "+vfilt_output+" " \
       "--tranches-file "+temp_dir+pname+"_SNP.tranches --recal-file "+vrecal1_output+" -O "+vsqr_output
parallel_command([comm], 1, temp_dir+"/", 'ApplyVQSR.log') #n=2

#os.remove(gvcf_output)
print(comm)
print("\n")

#VariantRecalibrator INDELS
print("\n")
print("VariantRecalibrator INDELS")
comm = java+' -Xmx10g -jar '+gatk+' VariantRecalibrator -R '+BWAindex+" -V "+vfilt_output+" -tranche 100.0 -tranche 99.9 -tranche 99.5 " \
       "-tranche 99.0 -tranche 90.0 -mode INDEL --tranches-file "+temp_dir+pname+"_INDEL.tranches --rscript-file "+temp_dir+pname+"_INDEL.plots.R " \
       "--resource mills,known=false,training=true,truth=true,prior=12.0:"+mills+" --resource dbsnp,known=true,training=" \
       "false,truth=false,prior=2.0:"+dbsnp+" -an QD -an MQ -an MQRankSum -an ReadPosRankSum -an FS -an SOR --output "+vrecal2_output
parallel_command([comm], 1, temp_dir+"/", 'VariantRecalibrator_INDEL.log') #n=2

#os.remove(gvcf_output)
print(comm)
print("\n")

#ApplyVQSR INDELS
print("\n")
print("ApplyVQSR INDELS")
comm = java+' -Xmx10g -jar '+gatk+' ApplyVQSR -R '+BWAindex+" -mode INDEL --truth-sensitivity-filter-level 98.0 -V "+vsqr_output+" " \
       "--tranches-file "+temp_dir+pname+"_INDEL.tranches --recal-file "+vrecal2_output+" -O "+vsqr_final_output
parallel_command([comm], 1, temp_dir+"/", 'ApplyVQSR_INDEL.log') #n=2

print(comm)
print("\n")

#VariantAnnotator
print("\n")
print("Variant Annotator")
comm = java+' -Xmx10g -jar '+gatk+' VariantAnnotator -R '+BWAindex+" -V "+vsqr_final_output+" " \
       "--dbsnp "+refknownsitesSNPS+" -O "+vsqr_final_annotated_output
parallel_command([comm], 1, temp_dir+"/", 'variantannotator.log') #n=2

print(comm)
print("\n")