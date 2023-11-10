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

let umask_pac  = if (( umask[d=1] EQ 3 )) then one else one-11
set variable/bad=-10. umask_pac

!!---Pacific
use pot_rho_2_$EXP.nc !2
use area_t_$EXP.nc !3
use dht_$EXP.nc !4
use v_$EXP.nc !5
use ty_trans_$EXP.nc !6
use ty_trans_gm_$EXP.nc !7
use ty_trans_rho_$EXP.nc !8
use ty_trans_rho_gm_$EXP.nc !9

!!---potential density (gamma2)
let volume = area_t[d=3]*dht[l=61:70@ave,d=4]
let pot_rho_vol_pasoc = tmask_pasoc*pot_rho_vol
let volume_pasoc = tmask_pasoc*volume
let pot_rho_pasoc = tmask_pasoc*pot_rho_2[d=2]
let pot_rho_vol_pasoc = pot_rho_pasoc*volume_pasoc
let pot_rho_zonalmean_pasoc = pot_rho_vol_pasoc[i=@sum]/volume_pasoc[i=@sum]
let ppotrho2 = pot_rho_zonalmean_pasoc[l=61:79@ave]

let pot_rho_pasoc = tmask_pasoc*pot_rho_2[d=2]
!!!let pot_rho_pasoc     = pot_rho_2[d=2]*tmask_pac
let pot_rho_pasoc_24n = pot_rho_pasoc[y=24n,l=61:79@ave]
let pot_rho_pasoc_24s = pot_rho_pasoc[y=24s,l=61:79@ave]

save/file=zonalsection_rholevels_STC_$EXP.nc/clobber pot_rho_pasoc_24n,pot_rho_pasoc_24s

let vel       = v[d=5]
let vel_pac   = vel*umask_pac
let vel_pac_24n = vel_pac[y=24n,l=61:79@ave] 
let vel_pac_24s = vel_pac[y=24s,l=61:79@ave]

save/file=zonalsection_velocity_STC_$EXP.nc/clobber vel_pac_24n,vel_pac_24s

let euler = ty_trans[d=6]*tmask_pasoc
let gm    = ty_trans_gm[d=7]*tmask_pasoc
let trans = euler + gm
let trans_pac_24n = trans[y=24n,l=61:79@ave]
let trans_pac_24s = trans[y=24s,l=61:79@ave]

save/file=zonalsection_trans_STC_$EXP.nc/clobber trans_pac_24n, trans_pac_24s

let euler_rho = ty_trans_rho[d=8]*tmask_pasoc
let gm_rho    = ty_trans_rho_gm[d=9]*tmask_pasoc
let trans_rho = euler_rho + gm_rho
let trans_rho_pac_24n = trans_rho[y=24n,l=61:79@ave]
let trans_rho_pac_24s = trans_rho[y=24s,l=61:79@ave]

save/file=zonalsection_trans_rho_STC_$EXP.nc/clobber trans_rho_pac_24n, trans_rho_pac_24s


exit
!
/bin/rm -f ferret.jnl*
@ i = $i + 1

end
