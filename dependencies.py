#!/usr/bin/env python

#SGUL GENETICS CENTRE EXOME PIPELINE APRIL 2019
#Alan Pittman & Dionysios Grigoriadis

#Dependencies for the pipeline

#DRIVE
DRIVE = "/homedirs_APittman/sgul/shares/Mimir/Genetics_Centre_Bioinformatics_Mimir"

#resources: Global
BWAindex = DRIVE + "/resources/Genome_reference_files/human_g1k_v37.fasta"
samtoolsSoftware = DRIVE + "/resources/samtools-1.8/samtools"
java = DRIVE + "/resources/java/jre1.8.0_171/bin/java"
picard = DRIVE + "/resources/picard-2.815/picard.jar"
gatk = DRIVE + "/resources/gatk-4.0.4.0/gatk-package-4.0.4.0-local.jar"
gatk4_1 = DRIVE + "/resources/gatk-4.1.1.0/gatk-package-4.1.1.0-local.jar"
refknownsitesSNPS = DRIVE + "/resources/Genome_reference_files/common_all.vcf"
refknownsitesINDELS = DRIVE + "/resources/Genome_reference_files/Mills_and_1000G_gold_standard.indels.hg19_modified.vcf"

#resources: FastQC and Trimming
fastqc = DRIVE + "/resources/FastQC/fastqc"
multiqc = "~/python2.7_dio/bin/multiqc"
Trimmomatic= DRIVE + "/resources/Trimmomatic-0.38/trimmomatic-0.38.jar"

#resources: Data Pre-processing
###############################################################################################
BWAsoftware = DRIVE + "/resources/bwa/bwa"
externalBAMdir = DRIVE + "/Exomes/UBAMs"

#resources: Variant Calling
###############################################################################################
ExomeTarget = DRIVE + "/resources/Genome_reference_files/BroadExACExomeIntervlas.bed"

#resources: Variant Filtering
hapmap = DRIVE + "/resources/Genome_reference_files/hapmap_3.3.b37.vcf"
omni = DRIVE + "/resources/Genome_reference_files/1000G_omni2.5.b37.vcf"
G1000 = DRIVE + "/resources/Genome_reference_files/1000G_phase1.snps.high_confidence.b37.vcf"
dbsnp = DRIVE + "/resources/Genome_reference_files/dbsnp_138.b37.vcf"
mills = DRIVE + "/resources/Genome_reference_files/Mills_and_1000G_gold_standard.indels.b37.vcf"

