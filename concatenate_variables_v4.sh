#!/bin/sh

module purge
module load nco
source /opt-ictp/ESMF/env201906

#cd DATA
cd /home/clima-archive2/rfarneti/RENE/DATA/

DIR1='/home/netapp-clima-users1/rnavarro/FMS/archive'
RUN=("flux-only" "FAFSTRESS" "FAFWATER" "FAFHEAT" "FAFALL" "FAFHEAT_FAFSTRESS" "PASSIVEHEAT" "PASSIVEHEAT_FAFSTRESS")

for i in ${RUN[@]}
do
  EXP=$i
  IDIR=$DIR1/Blaker_${EXP}/history
  
  echo $IDIR

  ncrcat -v dht                       $IDIR/*ocean_grid.nc      dht_${EXP}_v1.nc
  ncrcat -v dhu                       $IDIR/*ocean_grid.nc      dhu_${EXP}_v1.nc  
  ncks   -v area_t                    $IDIR/21881225.ocean_grid.nc  area_t_${EXP}_v1.nc
  ncks   -v area_u                    $IDIR/21881225.ocean_grid.nc  area_u_${EXP}_v1.nc

  cdo sellonlatbox,-330,30,-90,90 dht_${EXP}_v1.nc                        dht_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 dhu_${EXP}_v1.nc                        dhu_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 area_t_${EXP}_v1.nc                     area_t_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 area_u_${EXP}_v1.nc                     area_u_${EXP}.nc

rm *_v1.nc
done
