#!/bin/sh

module purge
module load nco
source /opt-ictp/ESMF/env201906

cd TEMP-tendency

DIR1='/home/netapp-clima-users1/rnavarro/FMS/archive'
RUN=("flux-only" "FAFSTRESS" "FAFWATER" "FAFHEAT") 

#notar que fafall, fafheat-fafstress no incluyen los diagnopsticos tendency

for i in ${RUN[@]}
do
  EXP=$i
  IDIR=$DIR1/Blaker_${EXP}/history
  
  echo $IDIR

  ncrcat -v temp_tendency             $IDIR/*ocean_tendency.nc  temp_tendency_${EXP}_v1.nc
  ncrcat -v temp_advection            $IDIR/*ocean_tendency.nc  temp_advection_${EXP}_v1.nc
  ncrcat -v temp_submeso              $IDIR/*ocean_tendency.nc  temp_submeso_${EXP}_v1.nc
  ncrcat -v neutral_diffusion_temp    $IDIR/*ocean_tendency.nc  neutral_diffusion_temp_${EXP}_v1.nc
  ncrcat -v neutral_gm_temp           $IDIR/*ocean_tendency.nc  neutral_gm_temp_${EXP}_v1.nc
  ncrcat -v temp_vdiffuse_diff_cbt    $IDIR/*ocean_tendency.nc  temp_vdiffuse_diff_cbt_${EXP}_v1.nc
  ncrcat -v sw_heat                   $IDIR/*ocean_tendency.nc  sw_heat_${EXP}_v1.nc
  ncrcat -v swflx                     $IDIR/*ocean_tendency.nc  swflx_${EXP}_v1.nc

##Remapping
  cdo sellonlatbox,-330,30,-90,90 temp_tendency_${EXP}_v1.nc              temp_tendency_${EXP}.nc  
  cdo sellonlatbox,-330,30,-90,90 temp_advection_${EXP}_v1.nc             temp_advection_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 temp_submeso_${EXP}_v1.nc               temp_submeso_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 neutral_diffusion_temp_${EXP}_v1.nc     neutral_diffusion_temp_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 neutral_gm_temp_${EXP}_v1.nc            neutral_gm_temp_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 temp_vdiffuse_diff_cbt_${EXP}_v1.nc     temp_vdiffuse_diff_cbt_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 sw_heat_${EXP}_v1.nc                    sw_heat_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 swflx_${EXP}_v1.nc                      swflx_${EXP}.nc

##Merging all togheter
  cdo merge temp_tendency_${EXP}.nc temp_advection_${EXP}.nc temp_submeso_${EXP}.nc neutral_diffusion_temp_${EXP}.nc neutral_gm_temp_${EXP}.nc temp_vdiffuse_diff_cbt_${EXP}.nc sw_heat_${EXP}.nc swflx_${EXP}.nc  temp_diag_tend-${EXP}.nc

rm *_v1.nc
done
