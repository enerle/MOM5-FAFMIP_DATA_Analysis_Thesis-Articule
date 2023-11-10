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

use pot_rho_2_$EXP.nc !1
use v_$EXP.nc !2
use area_t_$EXP.nc !3
use dht_$EXP.nc !4

set region/z=0:5500/y=90S:90N/
set mem/size=9999

!!----Mask
use "/home/netapp-clima-users/rnavarro/ANALYSIS/regionmask_v6.nc" !5
let one=umask[d=5]/umask[d=5]
let umask_pac  = if (( umask[d=5] EQ 3 )) then one else one-11
let one=tmask[d=5]/tmask[d=5]
let tmask_pac  = if (( tmask[d=5] EQ 3 )) then one else one-11

set variable/bad=-10. umask_pac
set variable/bad=-10. tmask_pac

let rho_lev = 1033.93

let rho    = pot_rho_2[d=1,l=61:70@ave]
let rhopac = rho*tmask_pac
let rho_zlev = rhopac[gz=rho_lev]

let vel    = v[d=2,l=61:70@ave]
let velpac = vel*umask_pac

save/file=PAC_velocities_${EXP}.nc/clobber velpac
save/file=PAC_velocities_${EXP}.nc/append  rhopac
save/file=PAC_velocities_${EXP}.nc/append  rho_zlev

exit
!

/bin/rm -f ferret.jnl*
@ i = $i + 1
end
