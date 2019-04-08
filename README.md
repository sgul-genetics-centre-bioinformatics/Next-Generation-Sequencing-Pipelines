# Next-Generation-Sequencing-Pipelines


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

- FastQC
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

##Individual scripts:

- pipeline_alignment_v1.0.py
- pipeline_Annotate_v1.0.py
- pipeline_calculate_coverage_metrics.sh
- pipeline_fastq_clean_Adapter_removal_v1.0.sh
- pipeline_fastq_clean_Quality_clip_v1.0.sh
- pipeline_fastQC_v1.0_before.py
- pipeline_fastQC_v1.0.py
- pipeline_realignment_external_BAMs_v1.0.py
- pipeline_VariantCalling_v1.0.py


