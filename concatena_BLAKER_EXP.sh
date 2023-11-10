#!/bin/sh

module purge
module load nco
module load cdo
module load ferret

#EXP="Blaker_control" 
#EXP="Blaker_flux-only"
#EXP="Blaker_FAFHEAT" 
#EXP="Blaker_FAFHEAT-plus"
#EXP="Blaker_FAFSTRESS"
#EXP="Blaker_FAFWATER"
EXP="Blaker_FAFALL"

NAME=${EXP}.nc
IDIR=/home/netapp-clima-users1/rnavarro/FMS/archive/$EXP/history

ncrcat -v u                         $IDIR/*ocean_diag.nc  u_${NAME}
ncrcat -v v                         $IDIR/*ocean_diag.nc  v_${NAME}
ncrcat -v salt                      $IDIR/*ocean_diag.nc  salt_${NAME}
ncrcat -v temp                      $IDIR/*ocean_diag.nc  temp_${NAME}
ncrcat -v redist_heat               $IDIR/*ocean_diag.nc  redist_heat_${NAME}
ncrcat -v added_heat                $IDIR/*ocean_diag.nc  added_heat_${NAME}
ncrcat -v sea_level                 $IDIR/*eta.nc         sea_level_${NAME}

cdo selvar,area_t                   $IDIR/21881225.ocean_grid.nc  area_t_${NAME}

cdo merge sea_level_${NAME} area_t_${NAME} eta_${NAME}
cdo expr,'dsl = sea_level - (fldmean(sea_level*area_t)/fldmean(area_t))' eta_${NAME} dsl_${NAME}
ncatted -a long_name,dsl,o,c,"Dynamic_Sea_Level" dsl_${NAME}
ncatted -a units,dsl,o,c,"m" dsl_${NAME}
ncatted -a standard_name,dsl,o,c,"Dynamic_Sea_Level" dsl_${NAME}

cdo merge u_${NAME} v_${NAME} salt_${NAME} temp_${NAME} dsl_${NAME} MOM_${NAME}
cdo remapbil,r128x64 -sellonlatbox,0,360,-88.59375,88.59375 MOM_${NAME} regrided_${NAME}
ncap2 -s 'lon=lon+1.40625' regrided_${NAME}                             MOM_regrided_${NAME}

mv MOM_*.nc ../FAFMIP_data
