#!/bin/csh

module purge
module load cdo
module load ferret

set echo on

#cd DATA
cd /home/clima-archive2/rfarneti/RENE/DATA
set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL)
#set RUN = (flux-only FAFHEAT)

set i = 1

while ($i <= 5)
set EXP  = $RUN[$i]

ferret <<!

use ty_trans_$EXP.nc !1
use ty_trans_gm_$EXP.nc !2

set region/z=0:5500/y=90S:90N/
set mem/size=9999

!!----Mask
use "/home/netapp-clima-users/rnavarro/ANALYSIS/regionmask_v6.nc" !5
let one=tmask[d=3]/tmask[d=3]
let tmask_pac  = if (( tmask[d=3] EQ 3 )) then one else one-11

set variable/bad=-10. tmask_pac

!!!!!!!!!!!!!!!!!!!!!!!!
!!!!---Tropical cell
!!!!!!!!!!!!!!!!!!!!!!!!
let trans         = ty_trans[k=@rsum,d=1] + ty_trans_gm[d=2] - ty_trans[k=@sum,d=1]
let trans_pac     = trans*tmask_pac
let pmoc          = trans_pac[i=@sum]

let trans_y        = pmoc[y=0:6@sum]
let ID             = trans_y[z=@max]
let trans_z        = pmoc[gz=ID]
let trans_tc_north = trans_z[y=0:6@max,z=@max]

save/file=STC_max_trans_${EXP}_v2.nc/clobber trans_tc_north

let trans_y        = pmoc[y=6s:1s@sum]
let ID             = trans_y[z=@min]
let trans_z        = pmoc[gz=ID]
let trans_tc_south = ABS(trans_z[y=6s:1s@min,z=@min])

save/file=STC_max_trans_${EXP}_v2.nc/append trans_tc_south

!!!!!!!!!!!!!!!!!!!!!!!!
!!!!---Subtropical cell
!!!!!!!!!!!!!!!!!!!!!!!!

let trans_y         = pmoc[y=10n:15n@sum]
let ID              = trans_y[z=@max]
let trans_z         = pmoc[gz=ID]
let trans_stc_north = trans_z[y=13n,z=@max]

save/file=STC_max_trans_${EXP}_v2.nc/append trans_stc_north

let trans_y         = pmoc[y=15s:10s@sum]
let ID              = trans_y[z=@min]
let trans_z         = pmoc[gz=ID]
let trans_stc_south = ABS(trans_z[y=15s:10s@min,z=@min])

save/file=STC_max_trans_${EXP}_v2.nc/append trans_stc_south

exit
!

/bin/rm -f ferret.jnl*
@ i = $i + 1
end
