#USER modif
#add directories where SPOT products are to be found
inputXML="/mnt/Sen2Agri_DataSets/L2A/Spot4-T5/Ukraine/SPOT4_HRVIR1_XS_20130206_N2A_EUkraineD0000B0000/SPOT4_HRVIR1_XS_20130206_N2A_EUkraineD0000B0000.xml "
inputXML+="/mnt/Sen2Agri_DataSets/L2A/Spot4-T5/Ukraine/SPOT4_HRVIR1_XS_20130226_N2A_EUkraineD0000B0000/SPOT4_HRVIR1_XS_20130226_N2A_EUkraineD0000B0000.xml "
inputXML+="/mnt/Sen2Agri_DataSets/L2A/Spot4-T5/Ukraine/SPOT4_HRVIR1_XS_20130318_N2A_EUkraineD0000B0000/SPOT4_HRVIR1_XS_20130318_N2A_EUkraineD0000B0000.xml "
inputXML+="/mnt/Sen2Agri_DataSets/L2A/Spot4-T5/Ukraine/SPOT4_HRVIR1_XS_20130402_N2A_EUkraineD0000B0000/SPOT4_HRVIR1_XS_20130402_N2A_EUkraineD0000B0000.xml "
inputXML+="/mnt/Sen2Agri_DataSets/L2A/Spot4-T5/Ukraine/SPOT4_HRVIR1_XS_20130412_N2A_EUkraineD0000B0000/SPOT4_HRVIR1_XS_20130412_N2A_EUkraineD0000B0000.xml "
inputXML+="/mnt/Sen2Agri_DataSets/L2A/Spot4-T5/Ukraine/SPOT4_HRVIR1_XS_20130417_N2A_EUkraineD0000B0000/SPOT4_HRVIR1_XS_20130417_N2A_EUkraineD0000B0000.xml "
inputXML+="/mnt/Sen2Agri_DataSets/L2A/Spot4-T5/Ukraine/SPOT4_HRVIR1_XS_20130422_N2A_EUkraineD0000B0000/SPOT4_HRVIR1_XS_20130422_N2A_EUkraineD0000B0000.xml "
inputXML+="/mnt/Sen2Agri_DataSets/L2A/Spot4-T5/Ukraine/SPOT4_HRVIR1_XS_20130427_N2A_EUkraineD0000B0000/SPOT4_HRVIR1_XS_20130427_N2A_EUkraineD0000B0000.xml "
inputXML+="/mnt/Sen2Agri_DataSets/L2A/Spot4-T5/Ukraine/SPOT4_HRVIR1_XS_20130502_N2A_EUkraineD0000B0000/SPOT4_HRVIR1_XS_20130502_N2A_EUkraineD0000B0000.xml "
inputXML+="/mnt/Sen2Agri_DataSets/L2A/Spot4-T5/Ukraine/SPOT4_HRVIR1_XS_20130507_N2A_EUkraineD0000B0000/SPOT4_HRVIR1_XS_20130507_N2A_EUkraineD0000B0000.xml "
inputXML+="/mnt/Sen2Agri_DataSets/L2A/Spot4-T5/Ukraine/SPOT4_HRVIR1_XS_20130512_N2A_EUkraineD0000B0000/SPOT4_HRVIR1_XS_20130512_N2A_EUkraineD0000B0000.xml "
inputXML+="/mnt/Sen2Agri_DataSets/L2A/Spot4-T5/Ukraine/SPOT4_HRVIR1_XS_20130517_N2A_EUkraineD0000B0000/SPOT4_HRVIR1_XS_20130517_N2A_EUkraineD0000B0000.xml "
inputXML+="/mnt/Sen2Agri_DataSets/L2A/Spot4-T5/Ukraine/SPOT4_HRVIR1_XS_20130527_N2A_EUkraineD0000B0000/SPOT4_HRVIR1_XS_20130527_N2A_EUkraineD0000B0000.xml "
inputXML+="/mnt/Sen2Agri_DataSets/L2A/Spot4-T5/Ukraine/SPOT4_HRVIR1_XS_20130601_N2A_EUkraineD0000B0000/SPOT4_HRVIR1_XS_20130601_N2A_EUkraineD0000B0000.xml "
inputXML+="/mnt/Sen2Agri_DataSets/L2A/Spot4-T5/Ukraine/SPOT4_HRVIR1_XS_20130606_N2A_EUkraineD0000B0000/SPOT4_HRVIR1_XS_20130606_N2A_EUkraineD0000B0000.xml "
inputXML+="/mnt/Sen2Agri_DataSets/L2A/Spot4-T5/Ukraine/SPOT4_HRVIR1_XS_20130611_N2A_EUkraineD0000B0000/SPOT4_HRVIR1_XS_20130611_N2A_EUkraineD0000B0000.xml "
inputXML+="/mnt/Sen2Agri_DataSets/L2A/Spot4-T5/Ukraine/SPOT4_HRVIR1_XS_20130616_N2A_EUkraineD0000B0000/SPOT4_HRVIR1_XS_20130616_N2A_EUkraineD0000B0000.xml "
#L3A_DATE="20130617"
L3A_DATE="20130616"
#HALF_SYNTHESIS="50"
HALF_SYNTHESIS="60"
BANDS_MAPPING="bands_mapping_spot.txt"
#end of USER modif 


if [ $# -lt 3 ]
then
  echo "Usage: $0 <otb directory application> <resolution> <out folder name> [scattering coefficient file - S2 case only]"
  echo "The file with input xmls should be given. The resolution for which the computations will be performed should be given. The output directory should be given" 1>&2  
  exit
fi

SCAT_COEF=""
if [ $# == 4 ] ; then    
    ./run_composite_clipping.sh "$1" "$inputXML" "$2" "$3" "$L3A_DATE" "$HALF_SYNTHESIS" "$BANDS_MAPPING" "$4"
else
    ./run_composite_clipping.sh "$1" "$inputXML" "$2" "$3" "$L3A_DATE" "$HALF_SYNTHESIS" "$BANDS_MAPPING"
fi