#!/bin/csh

#module purge
module load nco
module load cdo
module load ferret

set echo on

#cd DATA
cd /home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA

set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL)
set i = 1

while ($i <= 5)
set EXP  = $RUN[$i]

ferret <<!
!!------------------------------------------------------------------
!!---Ocean heat uptake OHC
!!------------------------------------------------------------------

use temp_$EXP.nc !1
use dht_$EXP.nc  !2
use area_t_$EXP.nc !3

let rho0   = 1035.0
let Cp     = 3989.0
let volume = area_t[d=3]*dht[l=61:70@ave,d=2]

SET MEMORY/SIZE=888

let heat_dht     = temp[l=61:70@ave,d=1]*dht[l=61:70@ave,d=2]
let OHU          = rho0*Cp*heat_dht[k=@sum]
let OHU_1000     = rho0*Cp*heat_dht[z=0:1000@sum]
let OHU_500      = rho0*Cp*heat_dht[z=0:500@sum]

let heat_volume       = temp[l=61:70@ave,d=1]*volume
let heat_content      = rho0*Cp*heat_volume[i=@sum,k=@sum]
let heat_content_1000 = rho0*Cp*heat_volume[x=@sum,z=0:1000@sum]
let heat_content_500  = rho0*Cp*heat_volume[x=@sum,z=0:500@sum]

save/file=OHU_$EXP.nc/clobber OHU
save/file=heat_content_$EXP.nc/clobber heat_content
save/file=OHU_$EXP.nc/append OHU_1000, OHU_500
save/file=heat_content_$EXP.nc/append heat_content_1000, heat_content_500

exit
!

/bin/rm -f ferret.jnl*
@ i = $i + 1
end
