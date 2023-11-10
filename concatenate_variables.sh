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

  ncrcat -v tx_trans                  $IDIR/*ocean_diag.nc      tx_trans_${EXP}_v1.nc 
  ncrcat -v ty_trans                  $IDIR/*ocean_diag.nc      ty_trans_${EXP}_v1.nc
  ncrcat -v ty_trans_gm               $IDIR/*ocean_diag.nc      ty_trans_gm_${EXP}_v1.nc
  ncrcat -v ty_trans_rho              $IDIR/*ocean_diag.nc      ty_trans_rho_${EXP}_v1.nc
  ncrcat -v ty_trans_rho_gm           $IDIR/*ocean_diag.nc      ty_trans_rho_gm_${EXP}_v1.nc
  ncrcat -v temp_yflux_gm_int_z       $IDIR/*ocean_diag.nc      temp_yflux_gm_int_z_${EXP}_v1.nc
  ncrcat -v temp_yflux_ndiffuse_int_z $IDIR/*ocean_diag.nc      temp_yflux_ndiffuse_int_z_${EXP}_v1.nc
  ncrcat -v temp_yflux_adv_int_z      $IDIR/*ocean_diag.nc      temp_yflux_adv_int_z_${EXP}_v1.nc
  ncrcat -v temp                      $IDIR/*ocean_diag.nc      temp_${EXP}_v1.nc
  ncrcat -v salt                      $IDIR/*ocean_diag.nc      salt_${EXP}_v1.nc
  ncrcat -v pot_rho_0                 $IDIR/*ocean_diag.nc      pot_rho_0_${EXP}_v1.nc
  ncrcat -v pot_rho_2                 $IDIR/*ocean_diag.nc      pot_rho_2_${EXP}_v1.nc
  ncrcat -v dht                       $IDIR/*ocean_grid.nc      dht_${EXP}_v1.nc
  ncrcat -v dhu                       $IDIR/*ocean_grid.nc      dhu_${EXP}_v1.nc  
  ncrcat -v sea_level                 $IDIR/*eta.nc             sea_level_${EXP}_v1.nc
  ncks   -v area_t                    $IDIR/21881225.ocean_grid.nc  area_t_${EXP}_v1.nc
  ncks   -v area_u                    $IDIR/21881225.ocean_grid.nc  area_u_${EXP}_v1.nc
  ncrcat -v tau_x                     $IDIR/*ocean_fluxes.nc    tau_x_${EXP}_v1.nc
  ncrcat -v tau_y                     $IDIR/*ocean_fluxes.nc    tau_y_${EXP}_v1.nc

  if [ $i == "FAFHEAT" ] || [ $i == "PASSIVEHEAT" ] || [ $i == "PASSIVEHEAT_FAFSTRESS" ]
  then
  ncrcat -v added_heat                $IDIR/*ocean_diag.nc      added_heat_${EXP}_v1.nc
  ncrcat -v redist_heat               $IDIR/*ocean_diag.nc      redist_heat_${EXP}_v1.nc
  fi

##Remapping
  cdo sellonlatbox,-330,30,-90,90 tx_trans_${EXP}_v1.nc                   tx_trans_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 ty_trans_${EXP}_v1.nc                   ty_trans_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 ty_trans_gm_${EXP}_v1.nc                ty_trans_gm_${EXP}.nc 
  cdo sellonlatbox,-330,30,-90,90 ty_trans_rho_${EXP}_v1.nc               ty_trans_rho_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 ty_trans_rho_gm_${EXP}_v1.nc            ty_trans_rho_gm_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 temp_yflux_gm_int_z_${EXP}_v1.nc        temp_yflux_gm_int_z_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 temp_yflux_ndiffuse_int_z_${EXP}_v1.nc  temp_yflux_ndiffuse_int_z_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 temp_yflux_adv_int_z_${EXP}_v1.nc       temp_yflux_adv_int_z_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 temp_${EXP}_v1.nc                       temp_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 salt_${EXP}_v1.nc                       salt_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 pot_rho_0_${EXP}_v1.nc                  pot_rho_0_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 pot_rho_2_${EXP}_v1.nc                  pot_rho_2_${EXP}.nc 
  cdo sellonlatbox,-330,30,-90,90 dht_${EXP}_v1.nc                        dht_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 dhu_${EXP}_v1.nc                        dhu_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 sea_level_${EXP}_v1.nc                  sea_level_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 area_t_${EXP}_v1.nc                     area_t_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 area_u_${EXP}_v1.nc                     area_u_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 tau_x_${EXP}_v1.nc                      tau_x_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 tau_y_${EXP}_v1.nc                      tau_y_${EXP}.nc

  if [ $i == "FAFHEAT" ] || [ $i == "FAFHEAT-plus" ] || [ $i == "PASSIVEHEAT" ] || [ $i == "PASSIVEHEAT_FAFSTRESS" ]  
  then
  cdo sellonlatbox,-330,30,-90,90 added_heat_${EXP}_v1.nc                 added_heat_${EXP}.nc
  cdo sellonlatbox,-330,30,-90,90 redist_heat_${EXP}_v1.nc                redist_heat_${EXP}.nc 
  fi

rm *_v1.nc
done
