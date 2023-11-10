#!/bin/csh

#module purge
module load nco
module load cdo
module load ferret

set echo on

cd /home/clima-archive2/rfarneti/RENE/DATA

set RUN = ( FAFHEAT )
set i = 1

while ($i <= 1)
set EXP  = $RUN[$i]

ferret <<!
!!---------------------------------------------------
!!---------------Volume-mean temperature
!!---------------------------------------------------

use temp_flux-only.nc !1
use temp_$EXP.nc !2
use added_heat_$EXP.nc !3
use redist_heat_$EXP.nc !4
use dht_$EXP.nc    !5
use area_t_$EXP.nc !6

SET MEMORY/SIZE=888

let added       = added_heat[d=3] - added_heat[l=1,d=3]
let redist      = redist_heat[d=4] - temp[d=1]

let volume      = area_t[d=6]*dht[l=@ave,d=5]
let volume_sum  = volume[i=@sum,j=@sum,k=@sum]

let added_volume  = added*volume
let redist_volume = redist*volume

let added_sum  = added_volume[i=@sum,j=@sum,k=@sum]
let redist_sum = redist_volume[i=@sum,j=@sum,k=@sum]

let temp_volmean = added_sum/volume_sum
save/file=added_volmean_$EXP.nc/clobber temp_volmean

let temp_volmean = redist_sum/volume_sum
save/file=redist_volmean_$EXP.nc/clobber temp_volmean

!!---------------------------------------------------
!!---------------Zonal-mean temperature
!!---------------------------------------------------

let temp_zonalmean  =  added[i=@ave,l=61:70@ave]
save/file=added_zonalmean_$EXP.nc/clobber  temp_zonalmean

let temp_zonalmean =  redist[i=@ave,l=61:70@ave]
save/file=redist_zonalmean_$EXP.nc/clobber temp_zonalmean

exit
!

/bin/rm -f ferret.jnl*
@ i = $i + 1
end
