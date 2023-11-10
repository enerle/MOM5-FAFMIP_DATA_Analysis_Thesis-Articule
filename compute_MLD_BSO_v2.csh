#!/bin/csh

#module purge
module load nco
module load cdo
module load ferret

set echo on

cd /home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA

set RUN = ( flux-only FAFSTRESS FAFWATER FAFHEAT FAFALL )
set i = 1

while ($i <= 5)
set EXP  = $RUN[$i]

ferret <<!

set region/z=0:5500/y=90S:90N/
set mem/size=9999

use "/home/netapp-clima-users/rnavarro/ANALYSIS/regionmask_v6.nc" !1
let one=tmask[d=1]/tmask[d=1]
let tmask_pac  = if (( tmask[d=1] EQ 3 )) then one else one-11
let tmask_atl  = if (( tmask[d=1] EQ 2 OR tmask[d=1] EQ 4)) then one else one-11
set variable/bad=-10. tmask_pac
set variable/bad=-10. tmask_atl

!!---seccion macabra
let tmask_soc   = if (( tmask[d=1] EQ 1 )) then one-11 else one
let tmask_pac   = if (( tmask[d=1] EQ 3 )) then one-11 else one
let ID_soc      = if(x[gx=tmask_soc] GT -215. AND x[gx=tmask_soc] LT -69.) then tmask_soc else one
let ID_pasoc    = tmask_pac*ID_soc
let ID2_pasoc   = if((ID_pasoc EQ 1)) then 0. else ID_pasoc
let tmask_pasoc = ID2_pasoc/ID2_pasoc
set variable/bad=0. tmask_pasoc

SET MEMORY/SIZE=888

use temp_$EXP.nc !2
use MOC_$EXP.nc  !3

let diff     = temp[d=2,l=61:70@ave] - (temp[d=2,k=1,l=61:70@ave] - 0.5)
!!let diff_pac = diff*tmask_pac
let diff_pac = tmask_pasoc*diff
let diff_atl = diff*tmask_atl
let MLD      = diff[i=@ave,z=@loc:0]  
let PMLD     = diff_pac[i=@ave,z=@loc:0] !!!Mixed Layer Depth
let AMLD     = diff_atl[i=@ave,z=@loc:0] 
let PMOC     = moc_pac[d=3]
let MOCATL   = amoc[d=3]

save/file=MLD_BSO_$EXP.nc/clobber PMOC,MOCATL,MLD,PMLD,AMLD
exit
!

/bin/rm -f ferret.jnl*
@ i = $i + 1
end
