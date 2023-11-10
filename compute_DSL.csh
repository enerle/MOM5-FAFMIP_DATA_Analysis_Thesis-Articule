#!/bin/csh

#module purge
module load nco
module load cdo
module load ferret

set echo on

cd /home/clima-archive2/rfarneti/RENE/DATA

set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL FAFHEAT_FAFSTRESS)

set i = 1

while ($i <= 6)
set EXP  = $RUN[$i]

ferret <<!
!!------------------------------------------------------------------
!!---Dynamic Sea level
!!------------------------------------------------------------------

use sea_level_$EXP.nc !1
use area_t_$EXP.nc !2

SET MEMORY/SIZE=888

let eta       = sea_level[l=61:70@ave,d=1]
!!!let eta_area  = eta*area_t[i=1:360,j=1:200,d=2]
let eta_area  = eta*area_t[d=2]
let eta_mean  = eta_area[i=@ave,j=@ave]/area_t[i=@ave,j=@ave,d=2]
let DSL       = eta - eta_mean

save/file=DSL_${EXP}.nc/clobber DSL

exit
!

/bin/rm -f ferret.jnl*
@ i = $i + 1
end
