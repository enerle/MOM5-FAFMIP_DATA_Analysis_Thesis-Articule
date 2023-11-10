#!/bin/csh

#module purge
module load nco
module load cdo
module load ferret

set echo on

cd /home/clima-archive2/rfarneti/RENE/DATA

set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL)
set i = 1

while ($i <= 5)
set EXP  = $RUN[$i]

ferret <<!

set region/z=0:5500/y=90S:90N/
set mem/size=9999

!!----Mask
use "/home/netapp-clima-users/rnavarro/ANALYSIS/regionmask_v6.nc" !1
let one=tmask[d=1]/tmask[d=1]

!!---seccion macabra
let tmask_soc   = if (( tmask[d=1] EQ 1 )) then one-11 else one
let tmask_pac   = if (( tmask[d=1] EQ 3 )) then one-11 else one
let ID_soc      = if(x[gx=tmask_soc] GT -215. AND x[gx=tmask_soc] LT -69.) then tmask_soc else one
let ID_pasoc    = tmask_pac*ID_soc
let ID2_pasoc   = if((ID_pasoc EQ 1)) then 0. else ID_pasoc
let tmask_pasoc = ID2_pasoc/ID2_pasoc
set variable/bad=0. tmask_pasoc

!!---Pacific
use pot_rho_2_$EXP.nc !2
use area_t_$EXP.nc !3
use dht_$EXP.nc !4

!!---potential density (gamma2)
let volume = area_t[d=3]*dht[l=61:70@ave,d=4]
let pot_rho_vol_pasoc = tmask_pasoc*pot_rho_vol
let volume_pasoc = tmask_pasoc*volume
let pot_rho_pasoc = tmask_pasoc*pot_rho_2[d=2]
let pot_rho_vol_pasoc = pot_rho_pasoc*volume_pasoc
let pot_rho_zonalmean_pasoc = pot_rho_vol_pasoc[i=@sum]/volume_pasoc[i=@sum]
let ppotrho2 = pot_rho_zonalmean_pasoc[l=61:79@ave]

let pot_rho_pasoc = tmask_pasoc*pot_rho_2[d=2]
let pot_rho_pasoc_24n = pot_rho_pasoc[y=24n,l=61:79@ave]
let pot_rho_pasoc_24s = pot_rho_pasoc[y=24s,l=61:79@ave]

save/file=zonalsection_rholevels_STC_$EXP.nc/clobber pot_rho_pasoc_24n,pot_rho_pasoc_24s

exit
!
/bin/rm -f ferret.jnl*
@ i = $i + 1

end
