# Next-Generation-Sequencing-Pipelines
St George's University of London - Genetics Centre Bioinformatics


Scripts for QC, Alignemnt, Variant Calling and Joint Genotyping of Exome Sequence Data. Following the GATK Best Practices guidelines.
=======

##Directory/file structure:

Genetics_Centre_Bioinformatics/Exomes
- ./Aligned
- ./Unaligned
- ./raw_FASTQ
- ./tmp
- ./UBAMs
- ./VCF
- ./FastQC
- ./FastQC_before


##Needs the following resources to run:
For more information check dependencies.py

- FastQC
- MultiQC
- python2.7
- bwa
- human_g1k_v37.fasta
- samtools
- java
- picard-2.815
- gatk-4.0.4.0
- Genome_reference_files/common_all.vcf
- Mills_and_1000G_gold_standard.indels.hg19_modified.vcf
- 1000G_phase1.snps.high_confidence.hg19.sites.vcf
- BroadExACExomeIntervlas.bed (Exome Target, the this case the Broad definition)
