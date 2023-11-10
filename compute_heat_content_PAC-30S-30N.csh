#!/bin/csh

module load nco
module load cdo
module load ferret

set echo on

cd DATA/
set RUN =(flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL FAFHEAT_FAFSTRESS)
set i = 1

while ($i <= 6)
set EXP  = $RUN[$i]

ferret <<!

set region/z=0:5500/y=90S:90N/
set mem/size=9999

use "/home/netapp-clima-users1/rfarneti/ANALYSIS/grids/MOM1/regionmask_v6.nc" !1
let one=tmask[d=1]/tmask[d=1]

let tmask_pac  = if (( tmask[d=1] EQ 3 )) then one else one-11

set variable/bad=-10. tmask_pac

SET MEMORY/SIZE=888

use temp_$EXP.nc   !2
use dht_$EXP.nc    !3
use area_t_$EXP.nc !4

let rho0   = 1035.0
let Cp     = 3989.0
let volume = area_t[d=4]*dht[d=3]

SET MEMORY/SIZE=888

let heat_volume        = temp[d=2]*volume
let heat_content       = rho0*Cp*heat_volume*tmask_pac
let heat_content_k0005 = heat_content
let heat_content_k0610 = heat_content
let heat_content_k0010 = heat_content
let heat_content_k0020 = heat_content
let heat_content_k1150 = heat_content
let heat_content_k2150 = heat_content
 
save/file=heat_content_PAC-30S-30N_$EXP.nc/clobber heat_content[x=@sum,y=-30s:30n@sum,k=@sum]            !!
save/file=heat_content_PAC-30S-30N_$EXP.nc/append  heat_content_k0005[x=@sum,y=-30s:30n@sum,k=1:5@sum]   !!
save/file=heat_content_PAC-30S-30N_$EXP.nc/append  heat_content_k0610[x=@sum,y=-30s:30n@sum,k=6:10@sum]  !!
save/file=heat_content_PAC-30S-30N_$EXP.nc/append  heat_content_k0010[x=@sum,y=-30s:30n@sum,k=1:10@sum]
save/file=heat_content_PAC-30S-30N_$EXP.nc/append  heat_content_k0020[x=@sum,y=-30s:30n@sum,k=1:20@sum]
save/file=heat_content_PAC-30S-30N_$EXP.nc/append  heat_content_k1150[x=@sum,y=-30s:30n@sum,k=11:50@sum] !!
save/file=heat_content_PAC-30S-30N_$EXP.nc/append  heat_content_k2150[x=@sum,y=-30s:30n@sum,k=21:50@sum]

exit
!

/bin/rm -f ferret.jnl*
@ i = $i + 1
end

