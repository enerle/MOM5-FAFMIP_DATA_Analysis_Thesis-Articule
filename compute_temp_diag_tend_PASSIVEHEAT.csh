#!/bin/csh

module load nco
module load cdo
module load ferret

set echo on

cd /home/clima-archive2/rfarneti/RENE/DATA
set RUN = (PASSIVEHEAT PASSIVEHEAT_FAFSTRESS FAFHEAT)

set i = 1

while ($i <= 3)
set EXP  = $RUN[$i]

ferret <<!

set region/z=0:5500/y=90S:90N/
set mem/size=9999

use "/home/netapp-clima-users1/rfarneti/ANALYSIS/grids/MOM1/regionmask_v6.nc" !1
let one=tmask[d=1]/tmask[d=1]
let tmask_glb  = if (( tmask[d=1] EQ 1 OR tmask[d=1] EQ 2 OR tmask[d=1] EQ 3 OR tmask[d=1] EQ 4 OR tmask[d=1] EQ 5)) then one else one-11
let tmask_atl = if (( tmask[d=1] EQ 2 OR tmask[d=1] EQ 4)) then one else one-11
let tmask_ipa = if (( tmask[d=1] EQ 3 OR tmask[d=1] EQ 5)) then one else one-11
let tmask_soc = if (( tmask[d=1] EQ 1 )) then one else one-11
let tmask_pac = if (( tmask[d=1] EQ 3 )) then one else one-11
let tmask_ind = if (( tmask[d=1] EQ 5 )) then one else one-11

set variable/bad=-10. tmask_glb
set variable/bad=-10. tmask_atl
set variable/bad=-10. tmask_ipa
set variable/bad=-10. tmask_soc
set variable/bad=-10. tmask_pac
set variable/bad=-10. tmask_ind

SET MEMORY/SIZE=888

use area_t_$EXP.nc !2
use dht_$EXP.nc    !3
use added_heat_$EXP.nc !4
use redist_heat_$EXP.nc !5
use temp_$EXP.nc !6

let rho    = 1035.0
let cp     = 3989.0
let volume = area_t[d=2]*dht[d=3]

let added_heat_vol  = added_heat[d=4]*volume
let redist_heat_vol = redist_heat[d=5]*volume
let total_heat_vol  = temp[d=6]*volume

let added_heat_glb  = rho*cp*added_heat_vol[k=27:50@sum]
let redist_heat_glb = rho*cp*redist_heat_vol[k=27:50@sum]
let total_heat_glb  = rho*cp*total_heat_vol[k=27:50@sum]

!!!GLB
let heat_added  = added_heat_glb*tmask_glb
let heat_redist = redist_heat_glb*tmask_glb
let heat_total  = total_heat_glb*tmask_glb

save/file=heat_budget_${EXP}_GLB.nc/clobber heat_added[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_GLB.nc/append  heat_redist[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_GLB.nc/append  heat_total[i=@sum,j=@sum] 

!!!SOC
let heat_added  = added_heat_glb*tmask_soc
let heat_redist = redist_heat_glb*tmask_soc
let heat_total  = total_heat_glb*tmask_soc

save/file=heat_budget_${EXP}_SOC.nc/clobber heat_added[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_SOC.nc/append  heat_redist[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_SOC.nc/append  heat_total[i=@sum,j=@sum]

!!!ATL
let heat_added  = added_heat_glb*tmask_atl
let heat_redist = redist_heat_glb*tmask_atl
let heat_total  = total_heat_glb*tmask_atl

save/file=heat_budget_${EXP}_ATL.nc/clobber heat_added[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_ATL.nc/append  heat_redist[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_ATL.nc/append  heat_total[i=@sum,j=@sum]

!!!IPA
let heat_added  = added_heat_glb*tmask_ipa
let heat_redist = redist_heat_glb*tmask_ipa
let heat_total  = total_heat_glb*tmask_ipa

save/file=heat_budget_${EXP}_IPA.nc/clobber heat_added[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_IPA.nc/append  heat_redist[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_IPA.nc/append  heat_total[i=@sum,j=@sum]

!!!PAC
let heat_added  = added_heat_glb*tmask_pac
let heat_redist = redist_heat_glb*tmask_pac
let heat_total  = total_heat_glb*tmask_pac

save/file=heat_budget_${EXP}_PAC.nc/clobber heat_added[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_PAC.nc/append  heat_redist[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_PAC.nc/append  heat_total[i=@sum,j=@sum]

!!!IND
let heat_added  = added_heat_glb*tmask_ind
let heat_redist = redist_heat_glb*tmask_ind
let heat_total  = total_heat_glb*tmask_ind

save/file=heat_budget_${EXP}_IND.nc/clobber heat_added[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_IND.nc/append  heat_redist[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_IND.nc/append  heat_total[i=@sum,j=@sum]

exit

!
/bin/rm -f ferret.jnl*
@ i = $i + 1

end
