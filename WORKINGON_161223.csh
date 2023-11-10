#!/bin/csh

module purge
module load cdo
module load ferret

set echo on

cd /home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA
set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL)

set i = 1

while ($i <= 5)
set EXP  = $RUN[$i]

ferret <<!

use u_$EXP.nc !1
use v_$EXP.nc !2
use area_t_$EXP.nc !3
use dht_$EXP.nc !4

set region/z=0:5500/y=90S:90N/
set mem/size=9999

!!----Mask
use "/home/netapp-clima-users/rnavarro/ANALYSIS/regionmask_v6.nc" !5
let one=tmask[d=5]/tmask[d=5]
let tmask_pac  = if (( tmask[d=5] EQ 3 )) then one else one-11

set variable/bad=-10. tmask_pac

let vol = area_t[d=3]*dht[d=4,l=@ave]
let vel = v[d=2,l=61:70@ave]

let volpac = tmask_pac*vol
let velpac = vel*tmask_pac

let velvol = velpac*volpac

let vely   = velvol[i=@sum,z=0:1000@sum]/volpac[i=@sum,z=0:1000@sum]
let velxy  = velvol[z=0:200@sum]/volpac[z=0:1000@sum]

save/file=PAC_velocities_${EXP}.nc/clobber vely
save/file=PAC_velocities_${EXP}.nc/append  velxy

exit
!

/bin/rm -f ferret.jnl*
@ i = $i + 1
end
