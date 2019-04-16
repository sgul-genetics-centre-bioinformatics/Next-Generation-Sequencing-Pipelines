#!/usr/bin/env python

#SGUL GENETICS CENTRE EXOME PIPELINE APRIL 2019
#Alan Pittman & Dionysios Grigoriadis

#Dependencies for the pipeline

#DRIVE
DRIVE = "/homedirs_APittman/sgul/shares/Mimir/Genetics_Centre_Bioinformatics_Mimir/resources/"

#resources: Global
BWAindex = DRIVE + "Genome_reference_files/human_g1k_v37.fasta"
samtoolsSoftware = DRIVE + "samtools-1.8/samtools"
java = DRIVE + "java/jre1.8.0_171/bin/java"
picard = DRIVE + "picard-2.815/picard.jar"
gatk = DRIVE + "gatk-4.0.4.0/gatk-package-4.0.4.0-local.jar"
gatk4_1 = DRIVE + "gatk-4.1.1.0/gatk-package-4.1.1.0-local.jar"
refknownsitesSNPS = DRIVE + "Genome_reference_files/common_all.vcf"
refknownsitesINDELS = DRIVE + "Genome_reference_files/Mills_and_1000G_gold_standard.indels.hg19_modified.vcf"

#resources: FastQC and Trimming
fastqc = DRIVE + "FastQC/fastqc"
multiqc = DRIVE + "multiqc"
Trimmomatic= DRIVE + "Trimmomatic-0.38/trimmomatic-0.38.jar"

#resources: Data Pre-processing
###############################################################################################
BWAsoftware = DRIVE + "bwa/bwa"
externalBAMdir = DRIVE + "/Exomes/UBAMs"

#resources: Variant Calling
###############################################################################################
ExomeTarget = DRIVE + "Genome_reference_files/BroadExACExomeIntervlas.bed"

#resources: Variant Filtering
hapmap = DRIVE + "Genome_reference_files/hapmap_3.3.b37.vcf"
omni = DRIVE + "Genome_reference_files/1000G_omni2.5.b37.vcf"
G1000 = DRIVE + "Genome_reference_files/1000G_phase1.snps.high_confidence.b37.vcf"
dbsnp = DRIVE + "Genome_reference_files/dbsnp_138.b37.vcf"
mills = DRIVE + "Genome_reference_files/Mills_and_1000G_gold_standard.indels.b37.vcf"

