#!/bin/csh

module load nco
module load cdo
module load ferret

set echo on

cd DATA

set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL FAFHEAT_FAFSTRESS)
set i = 1

while ($i <= 6)
set EXP  = $RUN[$i]

ferret <<!
!!---------------------------------------------------
!!---------------Zonal-mean salinity
!!---------------------------------------------------

use salt_$EXP.nc            !1
use area_t_$EXP.nc               !2
use dht_$EXP.nc                  !3

SET MEMORY/SIZE=888

let volume               = area_t[d=2]*dht[l=61:70@ave,d=3]

let salt_vol        = salt[l=61:70@ave,d=1]*volume
let salt_zonalmean  = salt_vol[i=@sum]/volume[i=@sum]
save/file=salt_zonalmean_$EXP.nc/clobber salt_zonalmean

exit
!

/bin/rm -f ferret.jnl*

@ i = $i + 1
end
