#!/usr/bin/env bash
#dgrigori@stats3.sgul.ac.uk:!/bin/bash
#September 2017
#Program to query vcf file and annotation
##############################################################

#our resources:
RESOURCES="/homedirs_APittman/sgul/shares/Mimir/Genetics_Centre_Bioinformatics_Mimir/resources/"
JAVA="${RESOURCES}java/jre1.8.0_171/bin/java"
GATK="${RESOURCES}gatk-4.0.4.0/gatk-package-4.0.4.0-local.jar"
GENOMEREF="${RESOURCES}Genome_reference_files/human_g1k_v37.fasta"
ANNOVARconvert="${RESOURCES}resources/annovar/convert2annovar.pl"
ANNOVARtable="${RESOURCES}annovar/table_annovar.pl"
ANNOdbs="refGene,ensGene,cytoBand,genomicSuperDups,1000g2015aug_all,esp6500siv2_ea,esp6500siv2_aa,esp6500siv2_all,exac03,kaviar_20150923,gnomad_exome,gnomad_genome,hrcr1,gme,avsnp150,dbnsfp33a,dbnsfp31a_interpro,spidex,revel,mcap,clinvar_20170905"
ANNOv="${RESOURCES}annovar/humandb"
ANNOprotocol="g,g,r,r,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f"

#############################################################
#Define our directories:
##############################################################

while getopts v: option
do
        case "${option}"
        in
				v) inVCF=${OPTARG};;
                o) outDIR=${OPTARG};;

  esac

done

#mkdir $outDIR

##annotation

$ANNOVARtable -vcfinput $inVCF $ANNOv -buildver hg19 --thread 8 -protocol $ANNOdbs -remove -otherinfo \
 -operation $ANNOprotocol -genericdbfile hg19_spidex.txt \
 -argument '-hgvs,-hgvs,,,,,,,,,,,,,,,,,,,' -arg '-splicing 5,-splicing 5,,,,,,,,,,,,,,,,,,,' \
 -polish -nastring .

#python vcf_melt.py $outDIR$(basename $bFile).vcf.hg19_multianno.vcf > $outDIR/query_$(basename $bFile).txt

##housekeeping
sleep 3

#rm $OUT/query_${bFile}.vcf
#rm $OUT/query_${bFile}.vcf.idx
#rm $OUT/query_${bFile}.vcf.hg19_multianno.vcf


exit
exit
