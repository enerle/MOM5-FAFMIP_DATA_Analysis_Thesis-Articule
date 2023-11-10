#!/bin/csh

#aqui se calcula la anomalia

#module purge
module load nco
module load cdo
module load ferret

set echo on

#cd DATA
cd /home/clima-archive2/rfarneti/RENE/DATA

set RUN = ( FAFHEAT )
set i = 1

while ($i <= 1)
set EXP  = $RUN[$i]

ferret <<!
!!---------------------------------------------------
!!---------------Ocean heat uptake
!!---------------------------------------------------

use temp_flux-only.nc !1
use temp_$EXP.nc             !2
use added_heat_$EXP.nc       !3
use redist_heat_$EXP.nc      !4
use dht_$EXP.nc              !5
use area_t_$EXP.nc           !6

let rho0   = 1035.0
let Cp     = 3989.0
let volume = area_t[d=6]*dht[l=61:70@ave,d=5]

SET MEMORY/SIZE=888

let added_anom  = added_heat[l=61:70@ave,d=3] - added_heat[l=1,d=3]
let heat_dht    = added_anom*dht[l=61:70@ave,d=5]
let OHU         = rho0*Cp*heat_dht[k=@sum]

save/file=OHU_added_$EXP.nc/clobber OHU

let redist_anom  = redist_heat[l=61:70@ave,d=4] - temp[l=61:70@ave,d=1]
let heat_dht     = redist_anom*dht[l=61:70@ave,d=5]
let OHU          = rho0*Cp*heat_dht[k=@sum]

save/file=OHU_redist_$EXP.nc/clobber OHU

!!---------------------------------------------------
!!---------------Ocean heat content
!!---------------and Volume-mean temperature
!!---------------------------------------------------

let heat_volume  = temp[l=61:70@ave,d=1]*volume
let temp_volmean = heat_volume[i=@sum,j=@sum,k=@sum]/volume[i=@sum,j=@sum,k=@sum]
save/file=temp_volmean_$EXP.nc/clobber temp_volmean

let heat_volume  = added_anom*volume
let heat_content = rho0*Cp*heat_volume[i=@sum,k=@sum]
save/file=heat_content_added_$EXP.nc/clobber heat_content

let temp_volmean = heat_volume[i=@sum,j=@sum,k=@sum]/volume[i=@sum,j=@sum,k=@sum]
save/file=temp_volmean_added_$EXP.nc/clobber temp_volmean

let heat_volume  = redist_anom*volume
let heat_content = rho0*Cp*heat_volume[i=@sum,k=@sum]
save/file=heat_content_redist_$EXP.nc/clobber heat_content

let temp_volmean = heat_volume[i=@sum,j=@sum,k=@sum]/volume[i=@sum,j=@sum,k=@sum]
save/file=temp_volmean_redist_$EXP.nc/clobber temp_volmean

exit
!

/bin/rm -f ferret.jnl*
@ i = $i + 1
end
