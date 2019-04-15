#!/bin/bash
#Alan Pittman September 2015
#Program to Collect Coverage Metrics

while getopts p: option
do
        case "${option}"
        in
                p) PROJECT=${OPTARG};;


  esac

done

########################################################################################
#/hades/PSP_Genomes_QSBB_Completed/apittman-PSP_Genomes
#get input and output directories

MasterDIR=`pwd`

echo "MASTER DIRECTORY:"

echo " "
echo $MasterDIR
echo " "

inputDIR="$MasterDIR/apittman-PSP_Genomes"
outputDIR="$MasterDIR/apittman-PSP_Genomes"


echo "PROJECT DIRECTORY:"
echo " "
echo $inputDIR
echo " "
echo $outputDIR
echo " "

#get sample ID's

MySampleIDs=`ls $inputDIR`

echo "SAMPLE IDs:"
echo $MySampleIDs
echo " "

echo "PIPELINE!"

sleep 2

#grep BAIT_SET ${iDirectory}/hhoulden-nmencacci-58539/hhoulden-nmencacci-58539.hybridMetrics > /array/Incoming_HiSeq3000/All_Coverage_Metrics_008.txt

echo "Coverage Metrics as requested" > $MasterDIR/All_Coverage_Metrics_${PROJECT}.txt
echo "GENOME_TERRITORY	MEAN_COVERAGE	SD_COVERAGE	MEDIAN_COVERAGE	MAD_COVERAGE	PCT_EXC_MAPQ	PCT_EXC_DUPE	PCT_EXC_UNPAIRED	PCT_EXC_BASEQ	PCT_EXC_OVERLAP	PCT_EXC_CAPPED	PCT_EXC_TOTAL	PCT_1X	PCT_5X	PCT_10X	PCT_15X	PCT_20X	PCT_25X	PCT_30X	PCT_40X	PCT_50X	PCT_60X	PCT_70X	PCT_80X	PCT_90X	PCT_100X	HET_SNP_SENSITIVITY	HET_SNP_Q" >> $MasterDIR/All_Coverage_Metrics_${PROJECT}.txt

for nID in $MySampleIDs; do
echo " grabbing $nID"	
echo " "$nID" `grep 2864785223 ${outputDIR}/$nID/${nID}_wgs_coverage_metrics.txt`" >> $MasterDIR/All_Coverage_Metrics_${PROJECT}.txt

done

echo "Coverage Metrics Collected"

exit