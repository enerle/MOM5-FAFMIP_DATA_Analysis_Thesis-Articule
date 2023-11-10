#!/bin/csh

#module purge
module load nco
module load cdo
module load ferret

set echo on

cd /home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA

set RUN = ( flux-only FAFSTRESS FAFWATER FAFHEAT FAFALL FAFSTRESSx2 FAFHEATx2 )

set i = 1

while ($i <= 7)
set EXP  = $RUN[$i]

ferret <<!

use ty_trans_$EXP.nc !1
use ty_trans_gm_$EXP.nc !2
use ty_trans_rho_$EXP.nc !3
use ty_trans_rho_gm_$EXP.nc !4

set region/z=0:5500/y=90S:90N/
set mem/size=9999

!!----Mask
use "/home/netapp-clima-users/rnavarro/ANALYSIS/regionmask_v6.nc" !5
let one=tmask[d=5]/tmask[d=5]

!!---seccion macabra
let tmask_soc   = if (( tmask[d=5] EQ 1 )) then one-11 else one
let tmask_pac   = if (( tmask[d=5] EQ 3 )) then one-11 else one
let ID_soc      = if(x[gx=tmask_soc] GT -215. AND x[gx=tmask_soc] LT -69.) then tmask_soc else one
let ID_pasoc    = tmask_pac*ID_soc
let ID2_pasoc   = if((ID_pasoc EQ 1)) then 0. else ID_pasoc
let tmask_pasoc = ID2_pasoc/ID2_pasoc
set variable/bad=0. tmask_pasoc

!!let euler      = ty_trans[d=1]*tmask_pasoc
!!let gm         = ty_trans_gm[d=2]*tmask_pasoc
let euler      = tmask_pasoc*ty_trans[d=1]
let gm         = tmask_pasoc*ty_trans_gm[d=2]
let pmoc       = euler[i=@sum,k=@rsum] + gm[i=@sum] - euler[i=@sum,k=@sum]
let pmoc_gm    = gm[i=@sum]
let pmoc_mean  = euler[i=@sum,k=@rsum] - euler[i=@sum,k=@sum]

save/file=MOC_PAC_$EXP.nc/clobber pmoc[l=61:70@ave]
save/file=MOC_PAC_$EXP.nc/append  pmoc_gm[l=61:70@ave]
save/file=MOC_PAC_$EXP.nc/append  pmoc_mean[l=61:70@ave]

exit
!
/bin/rm -f ferret.jnl*
@ i = $i + 1

end
