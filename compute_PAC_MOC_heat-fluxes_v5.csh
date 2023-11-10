#!/bin/csh

#module purge
module load nco
module load cdo
module load ferret

set echo on

cd /home/clima-archive2/rfarneti/RENE/DATA

#set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL)
set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL FAFSTRESSx2 FAFHEATx2)
set i = 1

#while ($i <= 5)
while ($i <= 7)
set EXP  = $RUN[$i]

ferret <<!

use ty_trans_$EXP.nc !1
use ty_trans_gm_$EXP.nc !2
use ty_trans_rho_$EXP.nc !3
use ty_trans_rho_gm_$EXP.nc !4

set region/z=0:5500/y=90S:90N/
set mem/size=9999

!!----Mask
use "/home/netapp-clima-users/rnavarro/ANALYSIS/regionmask_v6.nc" !5
let one=tmask[d=5]/tmask[d=5]

!!---seccion macabra
let tmask_soc   = if (( tmask[d=5] EQ 1 )) then one-11 else one
let tmask_pac   = if (( tmask[d=5] EQ 3 )) then one-11 else one
let ID_soc      = if(x[gx=tmask_soc] GT -215. AND x[gx=tmask_soc] LT -69.) then tmask_soc else one
let ID_pasoc    = tmask_pac*ID_soc
let ID2_pasoc   = if((ID_pasoc EQ 1)) then 0. else ID_pasoc
let tmask_pasoc = ID2_pasoc/ID2_pasoc
set variable/bad=0. tmask_pasoc

!!---Pacific
use pot_rho_2_$EXP.nc !6
use area_t_$EXP.nc !7
!!use dht_$EXP.nc !8
use rho_dht_$EXP.nc !8
use temp_$EXP.nc !9

let rho     = 1035. !sea water density
let cp      = 3992.1 !J/kg*C
let vol     = area_t[d=7]*rho_dht[l=61:70@ave,d=8]

let pi    = 4.0*atan(1.0)
let rad   = pi/180.
let omega = 7.292e-5 !(rad/s) Earth angular velocity
let R     = 6.371e6 !(m) Earth radius
let Ry    = R*cos(y[gy=temptemp]*rad)

let dlon           = geolon_t[i=1:360,j=1:200,d=7]
let dlon_diff      = dlon[x=@SHF:1] - dlon
let dlon_diff_mask = dlon_diff*tmask_pasoc
let dx             = dlon_diff_mask*rad*Ry
let dxdht          = dx[i=1:360,j=1:200]*rho_dht[i=1:360,j=1:200,d=8]

!!-----meridional sverdrup transport, density space
let temptemp  = temp[d=9]*tmask_pasoc
let euler_rho = ty_trans_rho[d=3]*tmask_pasoc
let gm_rho    = ty_trans_rho_gm[d=4]*tmask_pasoc

!!!heat transport for each water mass
let trans_mass  = euler_rho+gm_rho !!(kg/s)
let tempdxdht   = temptemp*dxdht

!!(J/kgoC)(kg/s)(oC)dxdz: (Jm2/s) ?

let trans_rho_tot       = cp*trans_mass[x=@sum]*tempdxdht[x=@ave]
let trans_rho_int_north = cp*trans_mass[x=145e:69w@sum]*tempdxdht[x=145e:69w@ave]
let trans_rho_wbc_north = cp*trans_mass[x=95e:145e@sum]*tempdxdht[x=95e:145e@ave]
let trans_rho_int_south = cp*trans_mass[x=165e:69w@sum]*tempdxdht[x=165e:69w@ave]
let trans_rho_wbc_south = cp*trans_mass[x=95e:165e@sum]*tempdxdht[x=95e:165e@ave]

let trans_rho_tot_24N_t = trans_rho_tot[y=24n]
let trans_rho_int_24N_t = trans_rho_int_north[y=24n]
let trans_rho_wbc_24N_t = trans_rho_wbc_north[y=24n]
let trans_rho_tot_24S_t = trans_rho_tot[y=24s]
let trans_rho_int_24S_t = trans_rho_int_south[y=24s]
let trans_rho_wbc_24S_t = trans_rho_wbc_south[y=24s]

let trans_rho_tot_24N = trans_rho_tot_24N_t[l=61:70@ave]
let trans_rho_int_24N = trans_rho_int_24N_t[l=61:70@ave]
let trans_rho_wbc_24N = trans_rho_wbc_24N_t[l=61:70@ave]
let trans_rho_tot_24S = trans_rho_tot_24S_t[l=61:70@ave]
let trans_rho_int_24S = trans_rho_int_24S_t[l=61:70@ave]
let trans_rho_wbc_24S = trans_rho_wbc_24S_t[l=61:70@ave]

save/file=MOC_RHO_PAC_hflux_$EXP.nc/clobber trans_rho_tot_24N,trans_rho_int_24N,trans_rho_wbc_24N
save/file=MOC_RHO_PAC_hflux_$EXP.nc/append  trans_rho_tot_24S,trans_rho_int_24S,trans_rho_wbc_24S

!!----mass transport across 24N
!!--total transport=wbc+int
let trans00_tot_north_t = trans_rho_tot_24N_t[z=1028:1031.8668@sum] !!potrho24N
let trans01_tot_north_t = trans_rho_tot_24N_t[z=1028:1032.7973@sum] !!potrho30N
let trans02_tot_north_t = trans_rho_tot_24N_t[z=1028:1033.8931@sum] !!potrho40N
let trans03_tot_north_t = trans_rho_tot_24N_t[z=1028:1034.6656@sum] !!potrho45N
let trans04_tot_north_t = trans_rho_tot_24N_t[z=1028:1035.0366@sum] !!potrho60N
let trans05_tot_north_t = trans_rho_tot_24N_t[z=1028:1035.3538@sum] !!potrho64N
let trans06_tot_north_t = trans_rho_tot_24N_t[z=1028:1036.20@sum]  !!non-ventilated within NH but in SH
let trans07_tot_north_t = trans_rho_tot_24N_t[z=1028:1036.80@sum]  !!last-ventilated isopycnal in SH
let trans08_tot_north_t = trans_rho_tot_24N_t[z=1028:1036.90@sum]  !!un-ventilated recirculating bottom water SOC
let trans09_tot_north_t = trans_rho_tot_24N_t[z=@sum]

let trans0000_tot_north_t = trans00_tot_north_t                   !!upper-24n
let trans0100_tot_north_t = trans01_tot_north_t-trans00_tot_north_t !!upper-30n
let trans0201_tot_north_t = trans02_tot_north_t-trans01_tot_north_t !!upper-40n
let trans0302_tot_north_t = trans03_tot_north_t-trans02_tot_north_t !!intermediate-45n
let trans0403_tot_north_t = trans04_tot_north_t-trans03_tot_north_t !!intermediate-60n 
let trans0504_tot_north_t = trans05_tot_north_t-trans04_tot_north_t !!intermediate-64n
let trans0605_tot_north_t = trans06_tot_north_t-trans05_tot_north_t !!deep1-SH-ventilated
let trans0706_tot_north_t = trans07_tot_north_t-trans06_tot_north_t !!deep2-SH-ventilated
let trans0807_tot_north_t = trans08_tot_north_t-trans07_tot_north_t !!deep3-SH-ventilated
let trans0908_tot_north_t = trans09_tot_north_t-trans08_tot_north_t !!bottom
let trans0009_tot_north_t =                     trans09_tot_north_t !!total-volumelet trans0000_tot_north_t = 

let trans0000_tot_north = trans0000_tot_north_t[l=61:70@ave]
let trans0100_tot_north = trans0100_tot_north_t[l=61:70@ave]
let trans0201_tot_north = trans0201_tot_north_t[l=61:70@ave] 
let trans0302_tot_north = trans0302_tot_north_t[l=61:70@ave]
let trans0403_tot_north = trans0403_tot_north_t[l=61:70@ave]
let trans0504_tot_north = trans0504_tot_north_t[l=61:70@ave]
let trans0605_tot_north = trans0605_tot_north_t[l=61:70@ave]
let trans0706_tot_north = trans0706_tot_north_t[l=61:70@ave]
let trans0807_tot_north = trans0807_tot_north_t[l=61:70@ave] 
let trans0908_tot_north = trans0908_tot_north_t[l=61:70@ave]
let trans0009_tot_north = trans0009_tot_north_t[l=61:70@ave] 

save/file=MOC_RHO_PAC_hflux_$EXP.nc/append trans0000_tot_north,trans0100_tot_north,trans0201_tot_north,trans0302_tot_north,trans0403_tot_north,trans0504_tot_north,trans0605_tot_north,trans0706_tot_north,trans0807_tot_north,trans0908_tot_north,trans0009_tot_north

!!-- interior
let trans00_int_north_t = trans_rho_int_24N_t[z=1028:1031.8668@sum] !!potrho24N
let trans01_int_north_t = trans_rho_int_24N_t[z=1028:1032.7973@sum] !!potrho30N
let trans02_int_north_t = trans_rho_int_24N_t[z=1028:1033.8931@sum] !!potrho40N
let trans03_int_north_t = trans_rho_int_24N_t[z=1028:1034.6656@sum] !!potrho45N
let trans04_int_north_t = trans_rho_int_24N_t[z=1028:1035.0366@sum] !!potrho60N
let trans05_int_north_t = trans_rho_int_24N_t[z=1028:1035.3538@sum] !!potrho64N
let trans06_int_north_t = trans_rho_int_24N_t[z=1028:1036.20@sum]  !!non-ventilated within NH but in SH
let trans07_int_north_t = trans_rho_int_24N_t[z=1028:1036.80@sum]  !!last-ventilated isopycnal in SH
let trans08_int_north_t = trans_rho_int_24N_t[z=1028:1036.90@sum]  !!un-ventilated recirculating bottom water SOC
let trans09_int_north_t = trans_rho_int_24N_t[z=@sum]

let trans0000_int_north_t = trans00_int_north_t                   !!upper-24n
let trans0100_int_north_t = trans01_int_north_t-trans00_int_north_t !!upper-30n
let trans0201_int_north_t = trans02_int_north_t-trans01_int_north_t !!upper-40n
let trans0302_int_north_t = trans03_int_north_t-trans02_int_north_t !!intermediate-45n
let trans0403_int_north_t = trans04_int_north_t-trans03_int_north_t !!intermediate-60n
let trans0504_int_north_t = trans05_int_north_t-trans04_int_north_t !!intermediate-64n
let trans0605_int_north_t = trans06_int_north_t-trans05_int_north_t !!deep1-SH-ventilated
let trans0706_int_north_t = trans07_int_north_t-trans06_int_north_t !!deep2-SH-ventilated
let trans0807_int_north_t = trans08_int_north_t-trans07_int_north_t !!deep3-SH-ventilated
let trans0908_int_north_t = trans09_int_north_t-trans08_int_north_t !!bottom
let trans0009_int_north_t =                     trans09_int_north_t !!intal-volumelet trans0000_int_north_t =

let trans0000_int_north = trans0000_int_north_t[l=61:70@ave]
let trans0100_int_north = trans0100_int_north_t[l=61:70@ave]
let trans0201_int_north = trans0201_int_north_t[l=61:70@ave]
let trans0302_int_north = trans0302_int_north_t[l=61:70@ave]
let trans0403_int_north = trans0403_int_north_t[l=61:70@ave]
let trans0504_int_north = trans0504_int_north_t[l=61:70@ave]
let trans0605_int_north = trans0605_int_north_t[l=61:70@ave]
let trans0706_int_north = trans0706_int_north_t[l=61:70@ave]
let trans0807_int_north = trans0807_int_north_t[l=61:70@ave]
let trans0908_int_north = trans0908_int_north_t[l=61:70@ave]
let trans0009_int_north = trans0009_int_north_t[l=61:70@ave]

save/file=MOC_RHO_PAC_hflux_$EXP.nc/append trans0000_int_north,trans0100_int_north,trans0201_int_north,trans0302_int_north,trans0403_int_north,trans0504_int_north,trans0605_int_north,trans0706_int_north,trans0807_int_north,trans0908_int_north,trans0009_int_north

!!-- western boundary-
let trans00_wbc_north_t = trans_rho_wbc_24N_t[z=1028:1031.8668@sum] !!potrho24N
let trans01_wbc_north_t = trans_rho_wbc_24N_t[z=1028:1032.7973@sum] !!potrho30N
let trans02_wbc_north_t = trans_rho_wbc_24N_t[z=1028:1033.8931@sum] !!potrho40N
let trans03_wbc_north_t = trans_rho_wbc_24N_t[z=1028:1034.6656@sum] !!potrho45N
let trans04_wbc_north_t = trans_rho_wbc_24N_t[z=1028:1035.0366@sum] !!potrho60N
let trans05_wbc_north_t = trans_rho_wbc_24N_t[z=1028:1035.3538@sum] !!potrho64N
let trans06_wbc_north_t = trans_rho_wbc_24N_t[z=1028:1036.20@sum]  !!non-ventilated within NH but in SH
let trans07_wbc_north_t = trans_rho_wbc_24N_t[z=1028:1036.80@sum]  !!last-ventilated isopycnal in SH
let trans08_wbc_north_t = trans_rho_wbc_24N_t[z=1028:1036.90@sum]  !!un-ventilated recirculating bottom water SOC
let trans09_wbc_north_t = trans_rho_wbc_24N_t[z=@sum]

let trans0000_wbc_north_t = trans00_wbc_north_t                   !!upper-24n
let trans0100_wbc_north_t = trans01_wbc_north_t-trans00_wbc_north_t !!upper-30n
let trans0201_wbc_north_t = trans02_wbc_north_t-trans01_wbc_north_t !!upper-40n
let trans0302_wbc_north_t = trans03_wbc_north_t-trans02_wbc_north_t !!intermediate-45n
let trans0403_wbc_north_t = trans04_wbc_north_t-trans03_wbc_north_t !!intermediate-60n
let trans0504_wbc_north_t = trans05_wbc_north_t-trans04_wbc_north_t !!intermediate-64n
let trans0605_wbc_north_t = trans06_wbc_north_t-trans05_wbc_north_t !!deep1-SH-ventilated
let trans0706_wbc_north_t = trans07_wbc_north_t-trans06_wbc_north_t !!deep2-SH-ventilated
let trans0807_wbc_north_t = trans08_wbc_north_t-trans07_wbc_north_t !!deep3-SH-ventilated
let trans0908_wbc_north_t = trans09_wbc_north_t-trans08_wbc_north_t !!bottom
let trans0009_wbc_north_t =                     trans09_wbc_north_t !!wbcal-volumelet trans0000_wbc_north_t =

let trans0000_wbc_north = trans0000_wbc_north_t[l=61:70@ave]
let trans0100_wbc_north = trans0100_wbc_north_t[l=61:70@ave]
let trans0201_wbc_north = trans0201_wbc_north_t[l=61:70@ave]
let trans0302_wbc_north = trans0302_wbc_north_t[l=61:70@ave]
let trans0403_wbc_north = trans0403_wbc_north_t[l=61:70@ave]
let trans0504_wbc_north = trans0504_wbc_north_t[l=61:70@ave]
let trans0605_wbc_north = trans0605_wbc_north_t[l=61:70@ave]
let trans0706_wbc_north = trans0706_wbc_north_t[l=61:70@ave]
let trans0807_wbc_north = trans0807_wbc_north_t[l=61:70@ave]
let trans0908_wbc_north = trans0908_wbc_north_t[l=61:70@ave]
let trans0009_wbc_north = trans0009_wbc_north_t[l=61:70@ave]

save/file=MOC_RHO_PAC_hflux_$EXP.nc/append trans0000_wbc_north,trans0100_wbc_north,trans0201_wbc_north,trans0302_wbc_north,trans0403_wbc_north,trans0504_wbc_north,trans0605_wbc_north,trans0706_wbc_north,trans0807_wbc_north,trans0908_wbc_north,trans0009_wbc_north

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!----Southern hemisphere
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!--total

let trans00_tot_south_t = trans_rho_tot_24S_t[z=1028:1032.1096@sum] !!potrho24S
let trans01_tot_south_t = trans_rho_tot_24S_t[z=1028:1032.7334@sum] !!potrho30S
let trans02_tot_south_t = trans_rho_tot_24S_t[z=1028:1033.9313@sum] !!potrho40S
let trans03_tot_south_t = trans_rho_tot_24S_t[z=1028:1034.6682@sum] !!potrho45S
let trans04_tot_south_t = trans_rho_tot_24S_t[z=1028:1036.2835@sum] !!potrho60S
let trans05_tot_south_t = trans_rho_tot_24S_t[z=1028:1036.5690@sum] !!potrho64S
let trans06_tot_south_t = trans_rho_tot_24S_t[z=1028:1036.7336@sum] !!potrho70S
let trans07_tot_south_t = trans_rho_tot_24S_t[z=1028:1036.85@sum]
let trans08_tot_south_t = trans_rho_tot_24S_t[z=1028:1036.90@sum]
let trans09_tot_south_t = trans_rho_tot_24S_t[z=@sum]

let trans0000_tot_south_t = trans00_tot_south_t                     !!upper-24s
let trans0100_tot_south_t = trans01_tot_south_t-trans00_tot_south_t !!upper-30s
let trans0201_tot_south_t = trans02_tot_south_t-trans01_tot_south_t !!upper-40s
let trans0302_tot_south_t = trans03_tot_south_t-trans02_tot_south_t !!intermediate-45s
let trans0403_tot_south_t = trans04_tot_south_t-trans03_tot_south_t !!intermediate-60s
let trans0504_tot_south_t = trans05_tot_south_t-trans04_tot_south_t !!intermediate-64s
let trans0605_tot_south_t = trans06_tot_south_t-trans05_tot_south_t !!deep1-70s
let trans0706_tot_south_t = trans07_tot_south_t-trans06_tot_south_t !!deep2-unventilated
let trans0807_tot_south_t = trans08_tot_south_t-trans07_tot_south_t !!deep3-unventilated
let trans0908_tot_south_t = trans09_tot_south_t-trans08_tot_south_t !!bottom-unventilated
let trans0009_tot_south_t =                     trans09_tot_south_t !!total-volume

let trans0000_tot_south = trans0000_tot_south_t[l=61:70@ave]
let trans0100_tot_south = trans0100_tot_south_t[l=61:70@ave]
let trans0201_tot_south = trans0201_tot_south_t[l=61:70@ave]
let trans0302_tot_south = trans0302_tot_south_t[l=61:70@ave]
let trans0403_tot_south = trans0403_tot_south_t[l=61:70@ave]
let trans0504_tot_south = trans0504_tot_south_t[l=61:70@ave]
let trans0605_tot_south = trans0605_tot_south_t[l=61:70@ave]
let trans0706_tot_south = trans0706_tot_south_t[l=61:70@ave]
let trans0807_tot_south = trans0807_tot_south_t[l=61:70@ave]
let trans0908_tot_south = trans0908_tot_south_t[l=61:70@ave]
let trans0009_tot_south = trans0009_tot_south_t[l=61:70@ave]

save/file=MOC_RHO_PAC_hflux_$EXP.nc/append trans0000_tot_south,trans0100_tot_south,trans0201_tot_south,trans0302_tot_south,trans0403_tot_south,trans0504_tot_south,trans0605_tot_south,trans0706_tot_south,trans0807_tot_south,trans0908_tot_south,trans0009_tot_south

!!!--interior

let trans00_int_south_t = trans_rho_int_24S_t[z=1028:1032.1096@sum] !!potrho24S
let trans01_int_south_t = trans_rho_int_24S_t[z=1028:1032.7334@sum] !!potrho30S
let trans02_int_south_t = trans_rho_int_24S_t[z=1028:1033.9313@sum] !!potrho40S
let trans03_int_south_t = trans_rho_int_24S_t[z=1028:1034.6682@sum] !!potrho45S
let trans04_int_south_t = trans_rho_int_24S_t[z=1028:1036.2835@sum] !!potrho60S
let trans05_int_south_t = trans_rho_int_24S_t[z=1028:1036.5690@sum] !!potrho64S
let trans06_int_south_t = trans_rho_int_24S_t[z=1028:1036.7336@sum] !!potrho70S
let trans07_int_south_t = trans_rho_int_24S_t[z=1028:1036.85@sum]
let trans08_int_south_t = trans_rho_int_24S_t[z=1028:1036.90@sum]
let trans09_int_south_t = trans_rho_int_24S_t[z=@sum]

let trans0000_int_south_t = trans00_int_south_t                     !!upper-24s
let trans0100_int_south_t = trans01_int_south_t-trans00_int_south_t !!upper-30s
let trans0201_int_south_t = trans02_int_south_t-trans01_int_south_t !!upper-40s
let trans0302_int_south_t = trans03_int_south_t-trans02_int_south_t !!intermediate-45s
let trans0403_int_south_t = trans04_int_south_t-trans03_int_south_t !!intermediate-60s
let trans0504_int_south_t = trans05_int_south_t-trans04_int_south_t !!intermediate-64s
let trans0605_int_south_t = trans06_int_south_t-trans05_int_south_t !!deep1-70s
let trans0706_int_south_t = trans07_int_south_t-trans06_int_south_t !!deep2-unventilated
let trans0807_int_south_t = trans08_int_south_t-trans07_int_south_t !!deep3-unventilated
let trans0908_int_south_t = trans09_int_south_t-trans08_int_south_t !!bottom-unventilated
let trans0009_int_south_t =                     trans09_int_south_t !!intal-volume

let trans0000_int_south = trans0000_int_south_t[l=61:70@ave]
let trans0100_int_south = trans0100_int_south_t[l=61:70@ave]
let trans0201_int_south = trans0201_int_south_t[l=61:70@ave]
let trans0302_int_south = trans0302_int_south_t[l=61:70@ave]
let trans0403_int_south = trans0403_int_south_t[l=61:70@ave]
let trans0504_int_south = trans0504_int_south_t[l=61:70@ave]
let trans0605_int_south = trans0605_int_south_t[l=61:70@ave]
let trans0706_int_south = trans0706_int_south_t[l=61:70@ave]
let trans0807_int_south = trans0807_int_south_t[l=61:70@ave]
let trans0908_int_south = trans0908_int_south_t[l=61:70@ave]
let trans0009_int_south = trans0009_int_south_t[l=61:70@ave]

save/file=MOC_RHO_PAC_hflux_$EXP.nc/append trans0000_int_south,trans0100_int_south,trans0201_int_south,trans0302_int_south,trans0403_int_south,trans0504_int_south,trans0605_int_south,trans0706_int_south,trans0807_int_south,trans0908_int_south,trans0009_int_south

!!!--western boundary current

let trans00_wbc_south_t = trans_rho_wbc_24S_t[z=1028:1032.1096@sum] !!potrho24S
let trans01_wbc_south_t = trans_rho_wbc_24S_t[z=1028:1032.7334@sum] !!potrho30S
let trans02_wbc_south_t = trans_rho_wbc_24S_t[z=1028:1033.9313@sum] !!potrho40S
let trans03_wbc_south_t = trans_rho_wbc_24S_t[z=1028:1034.6682@sum] !!potrho45S
let trans04_wbc_south_t = trans_rho_wbc_24S_t[z=1028:1036.2835@sum] !!potrho60S
let trans05_wbc_south_t = trans_rho_wbc_24S_t[z=1028:1036.5690@sum] !!potrho64S
let trans06_wbc_south_t = trans_rho_wbc_24S_t[z=1028:1036.7336@sum] !!potrho70S
let trans07_wbc_south_t = trans_rho_wbc_24S_t[z=1028:1036.85@sum]
let trans08_wbc_south_t = trans_rho_wbc_24S_t[z=1028:1036.90@sum]
let trans09_wbc_south_t = trans_rho_wbc_24S_t[z=@sum]

let trans0000_wbc_south_t = trans00_wbc_south_t                     !!upper-24s
let trans0100_wbc_south_t = trans01_wbc_south_t-trans00_wbc_south_t !!upper-30s
let trans0201_wbc_south_t = trans02_wbc_south_t-trans01_wbc_south_t !!upper-40s
let trans0302_wbc_south_t = trans03_wbc_south_t-trans02_wbc_south_t !!wbcermediate-45s
let trans0403_wbc_south_t = trans04_wbc_south_t-trans03_wbc_south_t !!wbcermediate-60s
let trans0504_wbc_south_t = trans05_wbc_south_t-trans04_wbc_south_t !!wbcermediate-64s
let trans0605_wbc_south_t = trans06_wbc_south_t-trans05_wbc_south_t !!deep1-70s
let trans0706_wbc_south_t = trans07_wbc_south_t-trans06_wbc_south_t !!deep2-unventilated
let trans0807_wbc_south_t = trans08_wbc_south_t-trans07_wbc_south_t !!deep3-unventilated
let trans0908_wbc_south_t = trans09_wbc_south_t-trans08_wbc_south_t !!bottom-unventilated
let trans0009_wbc_south_t =                     trans09_wbc_south_t !!wbcal-volume

let trans0000_wbc_south = trans0000_wbc_south_t[l=61:70@ave]
let trans0100_wbc_south = trans0100_wbc_south_t[l=61:70@ave]
let trans0201_wbc_south = trans0201_wbc_south_t[l=61:70@ave]
let trans0302_wbc_south = trans0302_wbc_south_t[l=61:70@ave]
let trans0403_wbc_south = trans0403_wbc_south_t[l=61:70@ave]
let trans0504_wbc_south = trans0504_wbc_south_t[l=61:70@ave]
let trans0605_wbc_south = trans0605_wbc_south_t[l=61:70@ave]
let trans0706_wbc_south = trans0706_wbc_south_t[l=61:70@ave]
let trans0807_wbc_south = trans0807_wbc_south_t[l=61:70@ave]
let trans0908_wbc_south = trans0908_wbc_south_t[l=61:70@ave]
let trans0009_wbc_south = trans0009_wbc_south_t[l=61:70@ave]

save/file=MOC_RHO_PAC_hflux_$EXP.nc/append trans0000_wbc_south,trans0100_wbc_south,trans0201_wbc_south,trans0302_wbc_south,trans0403_wbc_south,trans0504_wbc_south,trans0605_wbc_south,trans0706_wbc_south,trans0807_wbc_south,trans0908_wbc_south,trans0009_wbc_south

exit
!
/bin/rm -f ferret.jnl*
@ i = $i + 1

end
