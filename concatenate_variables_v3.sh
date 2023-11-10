#!/bin/sh

module purge
module load nco
source /opt-ictp/ESMF/env201906

cd DATA

DIR1='/home/netapp-clima-users1/rnavarro/FMS/archive'
RUN=("flux-only" "FAFSTRESS" "FAFWATER" "FAFHEAT" "FAFALL" "FAFHEAT_FAFSTRESS" "PASSIVEHEAT" "PASSIVEHEAT_FAFSTRESS")

for i in ${RUN[@]}
do
  EXP=$i
  IDIR=$DIR1/Blaker_${EXP}/history
  
  echo $IDIR

  ncrcat -v tau_x             $IDIR/*ocean_fluxes.nc   tau_x_${EXP}_v1.nc

  cdo sellonlatbox,-330,30,-90,90 tau_x_${EXP}_v1.nc   tau_x_${EXP}.nc

rm *_v1.nc
done
