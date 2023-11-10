#!/bin/csh

module load nco
module load ferret

set exp = FAFHEAT
#set idir = /home/netapp-clima-users1/rnavarro/FMS/archive/Blaker_flux-only/history
set idir = /home/netapp-clima-users1/rnavarro/FMS/archive/Blaker_${exp}/history
set tt = 10 

echo "Starting Ferret"

#/home/netapp-clima-users1/rnavarro/FMS/archive/Blaker_FAFHEAT/history/21881225.ocean_diag.nc
#/home/netapp-clima-users1/rnavarro/FMS/archive/Blaker_FAFHEAT/history/22181225.ocean_diag.nc
#/home/netapp-clima-users1/rnavarro/FMS/archive/Blaker_FAFHEAT/history/22481225.ocean_diag.nc

ferret <<! 

set MEMORY/SIZE=888

!! DYNAMIC SEA LEVEL ZETA
!!========================
use "$idir/22481225.eta.nc" !1
use "$idir/21881225.ocean_grid.nc" !2

let eta_area  = sea_level[d=1]*area_t[d=2]
let eta_mean = eta_area[i=@sum,j=@sum]/area_t[d=2,i=@sum,j=@sum]
let DSL = sea_level[d=1] - eta_mean

save/file=DSL_sealevel_${exp}_3.nc/clobber DSL[l=1]
repeat/l=2:$tt save/file=DSL_sealevel_${exp}_3.nc/append DSL

exit
!

#ncwa -a TIME temp_zonalmean_$exp.nc temp_zonalmean_$exp.nc
#ncwa -a TIME temp_zonalmean_$exp2.nc temp_zonalmean_$exp2.nc

/bin/rm -f ferret.jnl*


