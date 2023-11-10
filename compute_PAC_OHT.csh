#!/bin/csh

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

use temp_yflux_adv_int_z_$EXP.nc !1
use temp_yflux_gm_int_z_$EXP.nc !2
use temp_yflux_ndiffuse_int_z_$EXP.nc !3

!!----Mask
use "/home/netapp-clima-users/rnavarro/ANALYSIS/regionmask_v6.nc" !3
let one=tmask[d=4]/tmask[d=4]
let tmask_pac     = if (( tmask[d=4] EQ 3 )) then one else one-11
let tmask_pacind  = if (( tmask[d=4] EQ 3 OR tmask[d=4] EQ 5)) then one else one-11

set variable/bad=-10. tmask_pac
set variable/bad=-10. tmask_pacind

!!------------------------------------------------------------
!! --- Heat transport
!!------------------------------------------------------------
let adv   = temp_yflux_adv_int_z[d=1,l=61:70@ave]
let gm    = temp_yflux_gm_int_z[d=2,l=61:70@ave]
let dif   = temp_yflux_ndiffuse_int_z[d=3,l=61:70@ave]
let OHT   = adv + gm + dif

!!let OHT_glb   = OHT*1e-15
!!let OHT_glb_2 = if(OHT_glb GT -.2 AND OHT_glb LT .2) then OHT_glb else 0
!!let OHT_pac   = OHT_glb_2*tmask_pac
!!let PACOHT    = OHT_pac[i=@sum]

let OHTPAC  = (OHT*tmask_pac)*1e-15
let PACOHTZ = OHTPAC[i=@sum]
let PACOHT  = if(y[gy=PACOHTZ] GT -2.6) then PACOHTZ else PACOHTZ-1.2

let OHTPACIND  = (OHT*tmask_pacind)*1e-15
let PACINDOHT = OHTPACIND[i=@sum]

let PACINDOHT_MAX_HN = PACINDOHT[y=10n:30n@max]
let PACINDOHT_MAX_HS = PACINDOHT[y=30s:10s@min]
let PACINDOHT_SUM_HN = PACINDOHT[y=1n:60n@sum]
let PACINDOHT_SUM_HS = PACINDOHT[y=60s:1s@sum]

save/file=OHT_PAC_$EXP.nc/clobber PACOHT, PACINDOHT
save/file=OHT_PAC_$EXP.nc/append  PACINDOHT_MAX_HN, PACINDOHT_MAX_HS, PACINDOHT_SUM_HN, PACINDOHT_SUM_HS

exit
!
/bin/rm -f ferret.jnl*
@ i = $i + 1

end
