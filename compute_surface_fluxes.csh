#!/bin/csh

module load nco
module load cdo
module load ferret

set echo on

cd /home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/SFC-fluxes_v2/DATA

ferret <<!

set region/z=0:5500/y=90S:90N/
set mem/size=9999

use "/home/netapp-clima-users1/rfarneti/ANALYSIS/grids/MOM1/regionmask_v6.nc" !1
let one=tmask[d=1]/tmask[d=1]

!!let tmask_glb  = if (( tmask[d=1] EQ 1 OR tmask[d=1] EQ 2 OR tmask[d=1] EQ 3 OR tmask[d=1] EQ 4 OR tmask[d=1] EQ 5)) then one else one-11
let tmask_glb  = if (( tmask[d=1] EQ 1 OR tmask[d=1] EQ 2 OR tmask[d=1] EQ 3 OR tmask[d=1] EQ 4 OR tmask[d=1] EQ 5 OR tmask[d=1] EQ 6 OR tmask[d=1] EQ 7 OR tmask[d=1] EQ 8 OR tmask[d=1] EQ 9 OR tmask[d=1] EQ 10 )) then one else one-11

set variable/bad=-10. tmask_glb

!!!SET MEMORY/SIZE=888

use tau_x_correction.nc !2
use tau_y_correction.nc !3
use salt_sfc_correction.nc !4
use temp_sfc_correction.nc !5

let tau_x_glb     = tau_x[i=1:360,j=1:200,l=@ave,d=2]*tmask_glb[i=1:360,j=1:200]
let tau_y_glb     = tau_y[i=1:360,j=1:200,l=@ave,d=3]*tmask_glb[i=1:360,j=1:200]
let pme_glb       = pme[i=1:360,j=1:200,l=@ave,d=4]*tmask_glb[i=1:360,j=1:200]
let sfc_hflux_glb = sfc_hflux[i=1:360,j=1:200,l=@ave,d=5]*tmask_glb[i=1:360,j=1:200]

let tau_x_v2     = tau_x_glb[x=-250:110,y=-90:90]
let tau_y_v2     = tau_y_glb[x=-250:110,y=-90:90]
let pme_v2       = pme_glb[x=-250:110,y=-90:90]
let sfc_hflux_v2 = sfc_hflux_glb[x=-250:110,y=-90:90]

save/file=tau_x_correction_v2.nc/clobber    tau_x_v2
save/file=tau_y_correction_v2.nc/clobber    tau_y_v2
save/file=salt_sfc_correction_v2.nc/clobber pme_v2
save/file=temp_sfc_correction_v2.nc/clobber sfc_hflux_v2

exit
!
/bin/rm -f ferret.jnl*
