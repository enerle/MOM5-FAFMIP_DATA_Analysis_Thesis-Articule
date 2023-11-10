#!/bin/csh

#module purge
module load nco
module load cdo
module load ferret

set echo on

cd /home/clima-archive2/rfarneti/RENE/DATA

set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL FAFHEAT_FAFSTRESS)
set i = 1

while ($i <= 6)
set EXP  = $RUN[$i]

ferret <<!
!!---------------------------------------------------
!!---------------Volume-mean temperature
!!---------------------------------------------------

use temp_$EXP.nc   !1
use dht_$EXP.nc    !2
use area_t_$EXP.nc !3

SET MEMORY/SIZE=888

let volume       = area_t[d=3]*dht[l=@ave,d=2]
let volume_sum   = volume[i=@sum,j=@sum,k=@sum]

let temp_volume  = temp[d=1]*volume
let temp_sum     = temp_volume[i=@sum,j=@sum,k=@sum]
let temp_volmean = temp_sum/volume_sum

save/file=temp_volmean_$EXP.nc/clobber temp_volmean

!!---------------------------------------------------
!!---------------Zonal-mean temperature
!!---------------------------------------------------

let temp_zonalmean   =  temp[i=@ave,l=61:70@ave,d=1]

save/file=temp_zonalmean_$EXP.nc/clobber temp_zonalmean

exit
!

/bin/rm -f ferret.jnl*
@ i = $i + 1
end
