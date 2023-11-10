#!/bin/sh

module purge
module load nco
source /opt-ictp/ESMF/env201906

cd /home/clima-archive2/rfarneti/RENE/DATA #todos los datos brutos deben ir aqui 

DIR1='/home/netapp-clima-users/rnavarro/FMS/archive'
RUN=("flux-only" "FAFSTRESS" "FAFWATER" "FAFHEAT" "FAFALL" "FAFSTRESSx2" "FAFHEATx2")

for i in ${RUN[@]}
do
  EXP=$i
  IDIR=$DIR1/Blaker_${EXP}/history

  echo $IDIR

  ncrcat -v rho_dht      $IDIR/*ocean_grid.nc  rho_dht_${EXP}_v1.nc
  ncrcat -v dst          $IDIR/*ocean_grid.nc  dst_${EXP}_v1.nc

##Remapping
  cdo sellonlatbox,-330,30,-90,90 rho_dht_${EXP}_v1.nc  rho_dht_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 dst_${EXP}_v1.nc      dst_${EXP}.nc

rm *_v1.nc
done
