#!/bin/sh

module purge
module load nco
source /opt-ictp/ESMF/env201906

cd DATA

RUN=("FAFSTRESS" "FAFALL" "FAFHEAT_FAFSTRESS")

cdo sellonlatbox,-330,30,-90,90 ../SFC-fluxes/tau_x_correction.nc  tau_x_correction_v1.nc
mv tau_x_correction_v1.nc tau_x_correction.nc

for i in ${RUN[@]}
do
  EXP=$i
  for j in `seq 1 70`
  do
    cdo enssum -seltimestep,${j} tau_x_${EXP}.nc -timmean tau_x_correction.nc out_${j}.nc
  done
  cdo mergetime out_*.nc  tau_x_correction_${EXP}.nc
  rm out_*.nc
done
