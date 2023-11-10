#!/bin/csh

#module purge
module load nco
module load cdo
module load ferret

set echo on

cd /home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA
set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL)
set i = 1

while ($i <= 5)
set EXP  = $RUN[$i]

ferret <<!

use tau_x_$EXP.nc      !1
use tau_y_$EXP.nc      !2
use pot_rho_0_$EXP.nc  !3
use pot_rho_2_$EXP.nc  !4

set region/y=90S:90N/z=0:5000
set mem/size=9999

!!----Mask
use "/home/netapp-clima-users/rnavarro/ANALYSIS/regionmask_v6.nc" !5
let one=umask[d=5]/umask[d=5]
let umask_basin  = if (( umask[d=5] EQ 3 )) then one else one-11 !!PAC
set variable/bad =-10. umask_basin

let one=tmask[d=5]/tmask[d=5]
let tmask_basin  = if (( tmask[d=5] EQ 3 )) then one else one-11 !!PAC
set variable/bad =-10. tmask_basin

!!---seccion macabra
let tmask_soc   = if (( tmask[d=5] EQ 1 )) then one-11 else one
let tmask_pac   = if (( tmask[d=5] EQ 3 )) then one-11 else one
let ID_soc      = if(x[gx=tmask_soc] GT -215. AND x[gx=tmask_soc] LT -69.) then tmask_soc else one
let ID_pasoc    = tmask_pac*ID_soc
let ID2_pasoc   = if((ID_pasoc EQ 1)) then 0. else ID_pasoc
let tmask_pasoc = ID2_pasoc/ID2_pasoc
set variable/bad=0. tmask_pasoc

!!let taux   = tau_x[d=1]*umask_basin
!!let tauy   = tau_y[d=2]*umask_basin
!!let potrho = pot_rho_0[d=3]*umask_basin

let potrho = tmask_pasoc*pot_rho_0[d=3]

let g      = 9.81  !gravity
let rho    = 1035. !sea water density

let freqn2  = (g/rho)*potrho[z=@DDC]

let f500  = freqn2[z=0:500@ave,l=61:70@ave]
let f1000 = freqn2[z=0:1000@ave,l=61:70@ave]
let f2000 = freqn2[z=0:2000@ave,l=61:70@ave]

let gamma  = potrho[x=@ave]
let freqn2  = (g/rho)*gamma[z=@DDC]

save/file=freqn2_${EXP}_PAC.nc/clobber f500
save/file=freqn2_${EXP}_PAC.nc/append  f1000
save/file=freqn2_${EXP}_PAC.nc/append  f2000

save/file=zonalmean_freqn2_${EXP}_PAC.nc/clobber freqn2[l=61:70@ave]

exit
!

/bin/rm -f ferret.jnl*
@ i = $i + 1
end
