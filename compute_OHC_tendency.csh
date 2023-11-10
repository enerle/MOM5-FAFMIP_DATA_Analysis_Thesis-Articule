#!/bin/csh

module load nco
module load cdo
module load ferret

set echo on

cd DATA

set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL FAFHEAT_FAFSTRESS)
set i = 1

while ($i <= 6)
set EXP  = $RUN[$i]

ferret <<!

set region/z=0:5500/y=90S:90N/
set mem/size=9999

use "/home/netapp-clima-users1/rfarneti/ANALYSIS/grids/MOM1/regionmask_v6.nc" !1
let one=tmask[d=1]/tmask[d=1]
let tmask_atl = if (( tmask[d=1] EQ 2 OR tmask[d=1] EQ 4)) then one else one-11
let tmask_ipa = if (( tmask[d=1] EQ 3 OR tmask[d=1] EQ 5)) then one else one-11
let tmask_soc = if (( tmask[d=1] EQ 1 )) then one else one-11
set variable/bad=-10. tmask_atl
set variable/bad=-10. tmask_ipa
set variable/bad=-10. tmask_soc

!!------------------------------------------------------------
!! --- Heat content
!!------------------------------------------------------------

use temp_$EXP.nc !2
use dht_$EXP.nc  !3
use area_t_$EXP.nc !4

let rho0   = 1035.0
let Cp     = 3989.0
!!let volume = area_t[d=4]*dht[d=3] !!OHC in Joules
let volume = dht[d=3] !!OHC in Joules/m2

SET MEMORY/SIZE=888

let heat_volume  = temp[d=2]*volume
let OHC          = rho0*Cp*heat_volume[k=20:50@sum]

let OHC_glb = OHC 
let OHC_atl = OHC*tmask_atl
let OHC_ipa = OHC*tmask_ipa
let OHC_soc = OHC*tmask_soc

save/file=regional_heat_content_$EXP.nc/clobber OHC_glb[i=@sum,j=@sum]
save/file=regional_heat_content_$EXP.nc/append  OHC_atl[i=@sum,j=@sum]
save/file=regional_heat_content_$EXP.nc/append  OHC_ipa[i=@sum,j=@sum]
save/file=regional_heat_content_$EXP.nc/append  OHC_soc[i=@sum,j=@sum]

exit
!
/bin/rm -f ferret.jnl*
@ i = $i + 1

end
