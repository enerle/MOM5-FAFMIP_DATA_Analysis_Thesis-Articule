#!/bin/csh

#module purge
module load nco
module load cdo
module load ferret

set echo on

#cd DATA
cd /home/clima-archive2/rfarneti/RENE/DATA
set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL FAFHEAT_FAFSTRESS)

set i = 1

while ($i <= 6)
set EXP  = $RUN[$i]

ferret <<!

use tau_x_$EXP.nc   !1
use SST_SSS_$EXP.nc !2
use area_u_$EXP.nc  !3
use area_t_$EXP.nc  !4

set region/y=90S:90N/z=0:5000
set mem/size=9999

!!----Mask
use "/home/netapp-clima-users1/rnavarro/ANALYSIS/regionmask_v6.nc" !5
let one=umask[d=5]/umask[d=5]
let umask_pac    = if (( umask[d=5] EQ 3 )) then one else one-11
set variable/bad =-10. umask_pac

let one=tmask[d=5]/tmask[d=5]
let tmask_pac    = if (( tmask[d=5] EQ 3 )) then one else one-11
set variable/bad =-10. tmask_pac

let taux_pac = tau_x[d=1]*umask_pac
let temp_pac = sst[d=2]*tmask_pac

!!--latitudinal correction
let taux = taux_pac*cos(y[gy=taux_pac]*rad)
let temp = temp_pac*cos(y[gy=temp_pac]*rad)

let pi    = 4.0*atan(1.0)
let rad   = pi/180
let omega = 7.292e-5 !(rad/s) Earth angular velocity
let f     = 2*omega*sin(y[gy=taux]*pi/180)
let cp    = 3992.1 !J/kg*C
let R     = 6.371e6 !(m) Earth radius
let Ry    = R*cos(y[gy=taux]*rad)
let dlon  = geolon_t[i=1:360,j=1:200,d=4]
let dlat  = geolat_t[i=1:360,j=1:200,d=4]
let Nrad_lon  = dlon/180
let Nrad_lat  = dlat/180

let tauxminID    = if(taux[x=@ave,y=25n:35n,l=@ave] GT 0.) then 0 else 1
let tauxminIDlat = geolat_t[x=@ave,y=25n:35n,d=4]*tauxminID
let tauxminlat   = tauxminIDlat[y=@max]

let trans         = if ABS(y[gy=taux]) GT 5.0 then (-1)*taux/f !!kg/ms
let trans_dx      = trans[i=@ave,j=1:200]*(Nrad_lon[i=@sum,j=1:200]*pi*Ry) !!trans*dx
let tempgrad      = if(y[gy=temp] GT 0.0) then temp[y=@DDC] else (-1.)*temp[y=@DDC] !!oC/lat
let tempgrad_dlat = tempgrad[i=@ave,j=1:200]*dlat[i=@ave,j=1:200] !!oC

let trans_dx_tempgrad_dlat        = trans_dx[j=1:200]*tempgrad_dlat[j=1:200]
let cumsum_trans_dx_tempgrad_dlat = trans_dx_tempgrad_dlat[y=10:30@rsum] - trans_dx_tempgrad_dlat[y=10:30@sum]
let estc                          = ABS(cp*cumsum_trans_dx_tempgrad_dlat)*1.e-15

!!incluir latitud cero en suma
!!hacer cero todos los valores por encima de dicha latitud

save/file=STC_trans_energy_${EXP}_v21.nc/clobber trans_dx,tempgrad[i=@ave]
save/file=STC_trans_energy_${EXP}_v21.nc/append  taux[i=@ave],temp[i=@ave]
save/file=STC_trans_energy_${EXP}_v21.nc/append  estc
save/file=STC_trans_energy_${EXP}_v21.nc/append  tauxminID,tauxminIDlat,tauxminlat

exit
!

/bin/rm -f ferret.jnl*
@ i = $i + 1
end
