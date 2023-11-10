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
let umask_basin  = if (( umask[d=5] EQ 2 OR umask[d=5] EQ 4 )) then one else one-11 !!ATL
set variable/bad =-10. umask_basin

let one=tmask[d=5]/tmask[d=5]
let tmask_basin  = if (( tmask[d=5] EQ 2 OR tmask[d=5] EQ 4 )) then one else one-11 !!ATL
set variable/bad =-10. tmask_basin

let taux = tau_x[d=1]*umask_basin
let temp = sst[d=2]*tmask_basin

let pi    = 4.0*atan(1.0)
let rad   = pi/180.
let omega = 7.292e-5 !(rad/s) Earth angular velocity
let f     = 2.*omega*sin(y[gy=taux]*rad)
let rho   = 1035. !sea water density
let cp    = 3992.1 !J/kg*C
let R     = 6.371e6 !(m) Earth radius
let Ry    = R*cos(y[gy=taux]*rad)

let dlon           = geolon_t[i=1:360,j=1:200,d=4]
let dlon_diff      = dlon[x=@SHF:1] - dlon
let dlon_diff_mask = dlon_diff*tmask_basin
let dx             = dlon_diff_mask*rad*Ry

let dlat           = geolat_t[i=1:360,j=1:200,d=4]
let dlat_diff      = dlat[y=@SHF:1] - dlat
let dlat_diff_mask = dlat_diff*tmask_basin
let dy             = dlat_diff_mask*rad*R

!--find lat for the integral limit
let tauxminID_north    = if(taux[x=@ave,y=25n:32n,l=@ave] GT 0.) then 0 else 1
let tauxminIDlat_north = geolat_t[x=@ave,y=25n:32n,d=4]*tauxminID_north
let tauxminlat_north   = tauxminIDlat_north[y=@max]

let tauxminID_south    = if(taux[x=@ave,y=25s:32s,l=@ave] GT 0.) then 0 else 1
let tauxminIDlat_south = geolat_t[x=@ave,y=25s:32s,d=4]*tauxminID_south
let tauxminlat_south   = tauxminIDlat_south[y=@min]

let trans                = if ABS(y[gy=taux]) GT 5.0 then (-1)*taux/f !!kg/ms
let trans_dx             = trans[i=@ave,j=1:200]*dx[i=@sum,j=1:200]   !!kg/s
let tempgrad             = if(y[gy=temp] GT 0.0) then temp[y=@DDC] else (-1.)*temp[y=@DDC] !!oC/lat
let tempgrad_dy          = tempgrad[i=@ave,j=1:200]*dy[i=@ave,j=1:200] !!oC
let trans_dx_tempgrad_dy = trans_dx[j=1:200]*tempgrad_dy[j=1:200]

let IDD_north                         = if(y[gy=trans_dx_tempgrad_dy] GT tauxminlat_north) then 0 else 1
let trans_dx_tempgrad_dy_IDD_north    = trans_dx_tempgrad_dy[j=1:200]*IDD_north[j=1:200]
let cumsum_trans_dx_tempgrad_dy_north = trans_dx_tempgrad_dy_IDD_north[y=10n:32n@rsum] - trans_dx_tempgrad_dy_IDD_north[y=10n:32n@sum] 
let estc_north                        = ABS(cp*cumsum_trans_dx_tempgrad_dy_north)*1.e-15 !!PW

let IDD_south                         = if(y[gy=trans_dx_tempgrad_dy] LT tauxminlat_south) then 0 else 1
let trans_dx_tempgrad_dy_IDD_south    = trans_dx_tempgrad_dy[j=1:200]*IDD_south[j=1:200]
let cumsum_trans_dx_tempgrad_dy_south = trans_dx_tempgrad_dy_IDD_south[y=10s:32s@rsum]
let estc_south                        = ABS(cp*cumsum_trans_dx_tempgrad_dy_south)*1.e-15 !!

let ekman_trans = (trans_dx/rho)*1.e-6 !m3/s

save/file=STC_trans_energy_${EXP}_ATL.nc/clobber trans_dx,ekman_trans
save/file=STC_trans_energy_${EXP}_ATL.nc/append  dx[i=@sum],dy[i=@ave]
save/file=STC_trans_energy_${EXP}_ATL.nc/append  tempgrad[i=@ave]
save/file=STC_trans_energy_${EXP}_ATL.nc/append  taux[i=@ave],temp[i=@ave]
save/file=STC_trans_energy_${EXP}_ATL.nc/append  estc_north,estc_south
!!save/file=STC_trans_energy_${EXP}_ATL.nc/append  tauxminlat_north,tauxminlat_south

exit
!

/bin/rm -f ferret.jnl*
@ i = $i + 1
end
