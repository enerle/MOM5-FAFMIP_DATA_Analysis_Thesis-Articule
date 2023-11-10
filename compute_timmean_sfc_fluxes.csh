#!/bin/csh

module purge
module load nco
module load cdo
module load ferret

#source /opt-ictp/ESMF/env201906

set echo on

set dir1 = /home/netapp-clima-users1/rnavarro/MOM5_FAFMIP/FAFMIP/data/NYF/IC
set dir2 = /home/netapp-clima-users1/rnavarro/FMS/archive
set dir3 = /home/netapp-clima-users1/rfarneti/FMS/archive
cd SFC-fluxes

##--FAFMIP anomalous fluxes
cp ${dir1}/*_correction.nc .

cdo sellonlatbox,-250,110,-90,90 -timmean temp_sfc_correction.nc temp_sfc_correction_timmean.nc
cdo sellonlatbox,-250,110,-90,90 -timmean salt_sfc_correction.nc salt_sfc_correction_timmean.nc

ncrename -v xu_ocean,xt_ocean -v yu_ocean,yt_ocean -O tau_x_correction.nc
ncrename -v xu_ocean,xt_ocean -v yu_ocean,yt_ocean -O tau_y_correction.nc
ncrename -d xu_ocean,xt_ocean -d yu_ocean,yt_ocean -O tau_x_correction.nc
ncrename -d xu_ocean,xt_ocean -d yu_ocean,yt_ocean -O tau_y_correction.nc
cdo chname,tau_x,tau_xy -sqrt -add -sqr -selname,tau_x tau_x_correction.nc -sqr -selname,tau_y tau_y_correction.nc tau_correction.nc

cdo sellonlatbox,-250,110,-90,90 -timmean tau_x_correction.nc  tau_x_correction_timmean.nc
cdo sellonlatbox,-250,110,-90,90 -timmean tau_y_correction.nc  tau_y_correction_timmean.nc
cdo sellonlatbox,-250,110,-90,90 -timmean tau_correction.nc    tau_correction_timmean.nc

##--Surface fluxes from each Blaker-experiment
set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL FAFHEAT_FAFSTRESS)
set i = 1

while ($i <= 6)
set EXP  = $RUN[$i]

cdo sellonlatbox,-250,110,-90,90 -timmean -mergetime ${dir2}/${EXP}/history/*.ocean_fluxes.nc  ${EXP}_ocean_fluxes_timmean.nc

@ i = $i + 1
end

##--Surface fluxes from each CORE-experiment

#ncrcat /home/netapp-clima-users1/rfarneti/FMS/archive/MOM_FAFMIP_CTL/history/*.ocean_surf.nc test1.nc ##pues no funciono con cdo
cdo sellonlatbox,-250,110,-90,90 -timmean test1.nc CORE_MOM_FAFMIP_CTL_ocean_fluxes_timmean.nc


set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL FAFHEAT_FAFSTRESS)
set j = 1

while ($i <= 6)
set EXP  = $RUN[$j]

cdo sellonlatbox,-250,110,-90,90 -timmean -mergetime ${dir3}/${EXP}/history/*.ocean_surf.nc  CORE_${EXP}_ocean_fluxes_timmean.nc

@ j = $j + 1
end


