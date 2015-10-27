#!/bin/bash

./CropMask.py -refp /mnt/Imagery_S2A/In-Situ_TDS/France/LC/SudmipyS2A_LandCoverDecoupe_dissolvedGeometry.shp -ratio 0.75 -input \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130217_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130217_N2A_CSudmipy-ED0000B0000.xml \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130222_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130222_N2A_CSudmipy-ED0000B0000.xml \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130227_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130227_N2A_CSudmipy-ED0000B0000.xml \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130304_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130304_N2A_CSudmipy-ED0000B0000.xml \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130319_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130319_N2A_CSudmipy-ED0000B0000.xml \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130324_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130324_N2A_CSudmipy-ED0000B0000.xml \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130329_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130329_N2A_CSudmipy-ED0000B0000.xml \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130403_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130403_N2A_CSudmipy-ED0000B0000.xml \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130413_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130413_N2A_CSudmipy-ED0000B0000.xml \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130418_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130418_N2A_CSudmipy-ED0000B0000.xml \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130423_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130423_N2A_CSudmipy-ED0000B0000.xml \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130503_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130503_N2A_CSudmipy-ED0000B0000.xml \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130513_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130513_N2A_CSudmipy-ED0000B0000.xml \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130518_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130518_N2A_CSudmipy-ED0000B0000.xml \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130523_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130523_N2A_CSudmipy-ED0000B0000.xml \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130602_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130602_N2A_CSudmipy-ED0000B0000.xml \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130607_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130607_N2A_CSudmipy-ED0000B0000.xml \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130612_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130612_N2A_CSudmipy-ED0000B0000.xml \
/mnt/Satellite_Imagery/S2-QR/CSudmipy-E_LEVEL2A/SPOT4_HRVIR1_XS_20130617_N2A_CSudmipy-ED0000B0000/SPOT4_HRVIR1_XS_20130617_N2A_CSudmipy-ED0000B0000.xml \
-t0 20130217 -tend 20130617 -rate 5 -radius 100 -nbtrsample 4000 -rseed 0 -lmbd 2 -weight 1 -nbcomp 6 -spatialr 10 -ranger 0.65 -minsize 10 -rfnbtrees 100 -rfmax 25 -rfmin 5 -pixsize 20 \
-outdir "/mnt/data/QR_Results/CropMask_CSudmipy_E/"
