#!/bin/csh

#module purge
module load nco
module load cdo
module load ferret

set echo on

cd DATA
set RUN = ( flux-only FAFSTRESS FAFWATER FAFHEAT FAFALL FAFHEAT_FAFSTRESS )
set i = 1

while ($i <= 6)
set EXP  = $RUN[$i]

ferret <<!

set region/z=0:5500/y=90S:90N/
set mem/size=9999

use "/home/netapp-clima-users1/rnavarro/ANALYSIS/regionmask_v6.nc" !1
let one=tmask[d=1]/tmask[d=1]
let tmask_pac  = if (( tmask[d=1] EQ 3 )) then one else one-11
let tmask_atl  = if (( tmask[d=1] EQ 2 OR tmask[d=1] EQ 4)) then one else one-11
set variable/bad=-10. tmask_pac
set variable/bad=-10. tmask_atl

SET MEMORY/SIZE=888

use temp_$EXP.nc !2
use MOC_$EXP.nc  !3

let diff     = temp[d=2,l=61:70@ave] - (temp[d=2,k=1,l=61:70@ave] - 0.5)
let diff_pac = diff*tmask_pac
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
