#!/bin/csh

module load nco
module load cdo
module load ferret

set echo on

cd DATA

set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL)
set i = 1

while ($i <= 6)
set EXP  = $RUN[$i]

ferret <<!
!!---------------------------------------------------
!!---------------Zonal-mean pot-density
!!---------------------------------------------------

use pot_rho_0_$EXP.nc            !1
use pot_rho_2_$EXP.nc            !2
use area_t_$EXP.nc               !3
use dht_$EXP.nc                  !4

use "/home/netapp-clima-users1/rnavarro/ANALYSIS/regionmask_v6.nc" !5
let one=tmask[d=5]/tmask[d=5]
let tmask_pac  = if (( tmask[d=5] EQ 3 )) then one else one-11
let tmask_atl  = if (( tmask[d=5] EQ 2 OR tmask[d=5] EQ 4)) then one else one-11
set variable/bad=-10. tmask_pac
set variable/bad=-10. tmask_atl

!!---seccion macabra
let tmask_soc   = if (( tmask[d=5] EQ 1 )) then one-11 else one
let tmask_pac   = if (( tmask[d=5] EQ 3 )) then one-11 else one
let ID_soc      = if(x[gx=tmask_soc] GT -215. AND x[gx=tmask_soc] LT -69.) then tmask_soc else one
let ID_pasoc    = tmask_pac*ID_soc
let ID2_pasoc   = if((ID_pasoc EQ 1)) then 0. else ID_pasoc
let tmask_pasoc = ID2_pasoc/ID2_pasoc
set variable/bad=0. tmask_pasoc


SET MEMORY/SIZE=888

let volume_glb     = area_t[d=3]*dht[l=61:70@ave,d=4]
let volume_pac     = volume_glb*tmask_pac
let volume_atl     = volume_glb*tmask_atl

let pot_rho_0_glb  = pot_rho_0[l=61:70@ave,d=1]
let pot_rho_0_pac  = pot_rho_0[l=61:70@ave,d=1]*tmask_pac
let pot_rho_0_atl  = pot_rho_0[l=61:70@ave,d=1]*tmask_atl

let pot_rho_0_vol_glb = pot_rho_0_glb*volume_glb
let pot_rho_0_vol_pac = pot_rho_0_pac*volume_pac
let pot_rho_0_vol_atl = pot_rho_0_atl*volume_atl

let pot_rho_0_zonalmean_glb  = pot_rho_0_vol_glb[i=@sum]/volume_glb[i=@sum]
let pot_rho_0_zonalmean_pac  = pot_rho_0_vol_pac[i=@sum]/volume_pac[i=@sum]
let pot_rho_0_zonalmean_atl  = pot_rho_0_vol_atl[i=@sum]/volume_atl[i=@sum]

save/file=pot_rho_0_zonalmean_$EXP.nc/clobber pot_rho_0_zonalmean_glb,pot_rho_0_zonalmean_pac,pot_rho_0_zonalmean_atl

let pot_rho_2_glb  = pot_rho_2[l=61:70@ave,d=2]
let pot_rho_2_pac  = pot_rho_2[l=61:70@ave,d=2]*tmask_pac
let pot_rho_2_atl  = pot_rho_2[l=61:70@ave,d=2]*tmask_atl

let pot_rho_2_vol_glb = pot_rho_2_glb*volume_glb
let pot_rho_2_vol_pac = pot_rho_2_pac*volume_pac
let pot_rho_2_vol_atl = pot_rho_2_atl*volume_atl

let pot_rho_2_zonalmean_glb  = pot_rho_2_vol_glb[i=@sum]/volume_glb[i=@sum]
let pot_rho_2_zonalmean_pac  = pot_rho_2_vol_pac[i=@sum]/volume_pac[i=@sum]
let pot_rho_2_zonalmean_atl  = pot_rho_2_vol_atl[i=@sum]/volume_atl[i=@sum]

save/file=pot_rho_2_zonalmean_$EXP.nc/clobber pot_rho_2_zonalmean_glb,pot_rho_2_zonalmean_pac,pot_rho_2_zonalmean_atl

exit
!

/bin/rm -f ferret.jnl*

@ i = $i + 1
end
