#!/bin/csh

#module purge
module load nco
module load cdo
module load ferret

#Notes::
#To estimate water masses fluxes we used total transport instead of the MOC function since the last does not allow us to identify the actual flux direction with fidelity. The last is important for the sake of identifying the different integration levels. We have roughly identified upper, intermediate, deep, and bottom waters. Based on the isopycnal distribution (following Talleybook2003)
#UPPER: Lower latitudes water bounded by outcropping isopycnal at 30S-30N. Such water basically recirculates within the tropics
#INTER: Ventilated water at mid-latitudes, low salinity signal; as suggested by Talley,  water is defined as the downwelling water within midlatitudes, within the outcropping isopycnal surfaces between midlatitudes region of 30S-60S and 30N-60N. However, here we choose the first flat isopycnal (not rising) below the outcropping shallower isopycnals in the northern hemisphere, as a good proxy of both hemispheres, intermediate waters integration limits since every isopycnal above such level is actually ventilated.
#DEEP: Water below the intermediate water which is only ventilated through the Southern Ocean. We choose the last isopycnal reaching shallow waters in the SOC and downwelling toward deeper levels in the higher latitudes northern hemisphEre, as an approach to the deepwater production there.
#1036.8 last ventilated isopycnal
#DEEP DEEP: We have split the deep water classes into directly ventilated deep water and non-ventilated deep water (below 1036.9kgm3). Such water seems to be isolated from the Southern ocean ventilation pathway.Nevertheless, such water represents most of the interior ocean volume but spanning in a small density range. Some ventilation effects are expected inside such water mass since such water distributes from within the first 1000-m in SOC toward 2000m-5000m in higher latitudes northern pacific. In more detail, different features along the isopycnal levels are related to diffusive mix with overlapping density levels. while in the higher latitudes northern hemisphere water mix with lighter waters at the top, in the SOC mix take place denser waters below (recirculating bottom AABW). In contrast,  mid-to-low latitudes, are nearly zero, since isopycnal tilting is rather depictable suggesting no circulation, at least geostrophic one.
#BOTTOM: very bottom water, only shown in SOC. It approaches the equator but does not additively cross it. It goes from nearly 1000m to 5000m in the tropics as a slight bottom thong. Despite the presence of such water, transport is practically zero, suggesting stagnation at such levels, at least at the climatological level.

set echo on

cd /home/clima-archive2/rfarneti/RENE/DATA

set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL)
set i = 1

while ($i <= 5)
set EXP  = $RUN[$i]

ferret <<!

use ty_trans_$EXP.nc !1
use ty_trans_gm_$EXP.nc !2
use ty_trans_rho_$EXP.nc !3
use ty_trans_rho_gm_$EXP.nc !4
!!use pot_rho_2_$EXP.nc !5

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
use dht_$EXP.nc !8

!!---potential density (gamma2)
let volume = area_t[d=7]*dht[l=61:70@ave,d=8]
let pot_rho_vol_pasoc = tmask_pasoc*pot_rho_vol
let volume_pasoc = tmask_pasoc*volume
let pot_rho_pasoc = tmask_pasoc*pot_rho_2[d=6]
let pot_rho_vol_pasoc = pot_rho_pasoc*volume_pasoc
let pot_rho_zonalmean_pasoc = pot_rho_vol_pasoc[i=@sum]/volume_pasoc[i=@sum]
let ppotrho2 = pot_rho_zonalmean_pasoc[l=61:79@ave]

!!-- for meridional transport in isopycnal levels accorsing to Talle2008
let ppotrho2_64N = ppotrho2[y=64n,k=1]
let ppotrho2_60N = ppotrho2[y=60n,k=1]
let ppotrho2_50N = ppotrho2[y=50n,k=1]
let ppotrho2_40N = ppotrho2[y=40n,k=1]
let ppotrho2_30N = ppotrho2[y=30n,k=1]
let ppotrho2_24N = ppotrho2[y=24n,k=1]

let ppotrho2_70S = ppotrho2[y=70s,k=1]
let ppotrho2_64S = ppotrho2[y=64s,k=1]
let ppotrho2_60S = ppotrho2[y=60s,k=1]
let ppotrho2_50S = ppotrho2[y=50s,k=1]
let ppotrho2_40S = ppotrho2[y=40s,k=1]
let ppotrho2_30S = ppotrho2[y=30s,k=1]
let ppotrho2_24S = ppotrho2[y=24s,k=1]
save/file=test_rholevels_STC_$EXP.nc/clobber ppotrho2_64N, ppotrho2_60N, ppotrho2_50N,ppotrho2_40N, ppotrho2_30N, ppotrho2_24N
save/file=test_rholevels_STC_$EXP.nc/append  ppotrho2_70S, ppotrho2_64S, ppotrho2_60S, ppotrho2_50S,ppotrho2_40S, ppotrho2_30S, ppotrho2_24S

!!-----meridional sverdrup transport, density space
let euler_rho = ty_trans_rho[d=3]*tmask_pasoc
let gm_rho = tmask_pasoc*ty_trans_rho_gm[d=4]*tmask_pasoc

let trans_rho     = euler_rho+gm_rho
let trans_rho_tot = trans_rho[x=@sum,l=61:70@ave]

let trans_rho_int_north = trans_rho[x=145e:69w@sum,l=61:70@ave]
let trans_rho_wbc_north = trans_rho[x=95e:145e@sum,l=61:70@ave]
let trans_rho_tot_24N   = trans_rho_tot[y=30n]
let trans_rho_int_24N   = trans_rho_int_north[y=30n]
let trans_rho_wbc_24N   = trans_rho_wbc_north[y=30n]

let trans_rho_int_south = trans_rho[x=165e:69w@sum,l=61:70@ave]
let trans_rho_wbc_south = trans_rho[x=95e:165e@sum,l=61:70@ave]
let trans_rho_tot_24S   = trans_rho_tot[y=30s]
let trans_rho_int_24S   = trans_rho_int_south[y=30s]
let trans_rho_wbc_24S   = trans_rho_wbc_south[y=30s]

save/file=MOC_RHO_PAC_$EXP.nc/clobber trans_rho_tot_24N,trans_rho_int_24N,trans_rho_wbc_24N
save/file=MOC_RHO_PAC_$EXP.nc/append  trans_rho_tot_24S,trans_rho_int_24S,trans_rho_wbc_24S

!!----mass transport across 24N
!!--total transport=wbc+int
let trans00_tot_north = trans_rho_tot_24N[z=1028:1031.86@sum] !!potrho24N
let trans01_tot_north = trans_rho_tot_24N[z=1028:1032.79@sum] !!potrho30N
let trans02_tot_north = trans_rho_tot_24N[z=1028:1033.89@sum] !!potrho40N
!!
let trans03_tot_north = trans_rho_tot_24N[z=1028:1035.03@sum] !!potrho60N
let trans04_tot_north = trans_rho_tot_24N[z=1028:1035.35@sum] !!potrho64N
let trans05_tot_north = trans_rho_tot_24N[z=1028:1036.20@sum] !!non-ventilated within NH but in SH
let trans06_tot_north = trans_rho_tot_24N[z=1028:1036.80@sum] !!last-ventilated isopycnal in SH
let trans07_tot_north = trans_rho_tot_24N[z=1028:1036.90@sum] !!un-ventilated recirculating bottom water SOC
let trans08_tot_north = trans_rho_tot_24N[z=@sum]

let trans0000_tot_north = trans00_tot_north                   !!upper-24n
let trans0100_tot_north = trans01_tot_north-trans00_tot_north !!upper-30n
let trans0201_tot_north = trans02_tot_north-trans01_tot_north !!upper-40n
let trans0302_tot_north = trans03_tot_north-trans02_tot_north !!intermediate-60n 
let trans0403_tot_north = trans04_tot_north-trans03_tot_north !!intermediate-64n
let trans0504_tot_north = trans05_tot_north-trans04_tot_north !!deep1-SH-ventilated
let trans0605_tot_north = trans06_tot_north-trans05_tot_north !!deep2-SH-ventilated
let trans0706_tot_north = trans07_tot_north-trans06_tot_north !!deep3-SH-ventilated
let trans0807_tot_north = trans08_tot_north-trans07_tot_north !!bottom
let trans0008_tot_north =                   trans08_tot_north !!total-volume

save/file=MOC_RHO_PAC_$EXP.nc/append trans0000_tot_north,trans0100_tot_north,trans0201_tot_north,trans0302_tot_north,trans0403_tot_north,trans0504_tot_north,trans0605_tot_north,trans0706_tot_north,trans0807_tot_north,trans0008_tot_north

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!--here density classes integration is defined as function of the subducting level
let trans00_tot_mask = if(k[gk=trans_rho_tot_24N] GT ppotrho2_24N) then 0 else trans_rho_tot_24N
let trans01_tot_mask = if(k[gk=trans_rho_tot_24N] GT ppotrho2_30N) then 0 else trans_rho_tot_24N
let trans02_tot_mask = if(k[gk=trans_rho_tot_24N] GT ppotrho2_40N) then 0 else trans_rho_tot_24N
let trans03_tot_mask = if(k[gk=trans_rho_tot_24N] GT ppotrho2_60N) then 0 else trans_rho_tot_24N
let trans04_tot_mask = if(k[gk=trans_rho_tot_24N] GT ppotrho2_64N) then 0 else trans_rho_tot_24N
let trans05_tot_mask = if(k[gk=trans_rho_tot_24N] GT 1036.20) then 0 else trans_rho_tot_24N
let trans06_tot_mask = if(k[gk=trans_rho_tot_24N] GT 1036.80) then 0 else trans_rho_tot_24N
let trans07_tot_mask = if(k[gk=trans_rho_tot_24N] GT 1036.90) then 0 else trans_rho_tot_24N
let trans08_tot_mask = if(k[gk=trans_rho_tot_24N] GT 1037.9375) then 0 else trans_rho_tot_24N

let trans00_tot_north_v2 = trans_rho_tot_24N*trans00_tot_mask
let trans01_tot_north_v2 = trans_rho_tot_24N*trans01_tot_mask
let trans02_tot_north_v2 = trans_rho_tot_24N*trans02_tot_mask
let trans03_tot_north_v2 = trans_rho_tot_24N*trans03_tot_mask
let trans04_tot_north_v2 = trans_rho_tot_24N*trans04_tot_mask
let trans05_tot_north_v2 = trans_rho_tot_24N*trans05_tot_mask
let trans06_tot_north_v2 = trans_rho_tot_24N*trans06_tot_mask
let trans07_tot_north_v2 = trans_rho_tot_24N*trans07_tot_mask
let trans08_tot_north_v2 = trans_rho_tot_24N*trans08_tot_mask

!!let trans0000_tot_north_v2 = trans00_tot_north_v2[z=@sum]
!!let trans0100_tot_north_v2 = trans01_tot_north_v2[z=@sum]-trans00_tot_north_v2[z=@sum]
!!let trans0201_tot_north_v2 = trans02_tot_north_v2[z=@sum]-trans01_tot_north_v2[z=@sum]
!!let trans0302_tot_north_v2 = trans03_tot_north_v2[z=@sum]-trans02_tot_north_v2[z=@sum]
!!let trans0403_tot_north_v2 = trans04_tot_north_v2[z=@sum]-trans03_tot_north_v2[z=@sum]
!!let trans0504_tot_north_v2 = trans05_tot_north_v2[z=@sum]-trans04_tot_north_v2[z=@sum]
!!let trans0605_tot_north_v2 = trans06_tot_north_v2[z=@sum]-trans05_tot_north_v2[z=@sum]
!!let trans0706_tot_north_v2 = trans07_tot_north_v2[z=@sum]-trans06_tot_north_v2[z=@sum]
!!let trans0807_tot_north_v2 = trans08_tot_north_v2[z=@sum]-trans07_tot_north_v2[z=@sum]
!!let trans0008_tot_north_v2 =                              trans08_tot_north_v2[z=@sum]

let trans0000_tot_north_v2 = trans00_tot_north_v2[z=@sum]
let trans0100_tot_north_v2 = trans01_tot_north_v2[z=@sum]!!-trans00_tot_north_v2[z=@sum]
let trans0201_tot_north_v2 = trans02_tot_north_v2[z=@sum]!!-trans01_tot_north_v2[z=@sum]
let trans0302_tot_north_v2 = trans03_tot_north_v2[z=@sum]!!-trans02_tot_north_v2[z=@sum]
let trans0403_tot_north_v2 = trans04_tot_north_v2[z=@sum]!!-trans03_tot_north_v2[z=@sum]
let trans0504_tot_north_v2 = trans05_tot_north_v2[z=@sum]!!-trans04_tot_north_v2[z=@sum]
let trans0605_tot_north_v2 = trans06_tot_north_v2[z=@sum]!!-trans05_tot_north_v2[z=@sum]
let trans0706_tot_north_v2 = trans07_tot_north_v2[z=@sum]!!-trans06_tot_north_v2[z=@sum]
let trans0807_tot_north_v2 = trans08_tot_north_v2[z=@sum]!!-trans07_tot_north_v2[z=@sum]
!!let trans0008_tot_north_v2 =                              trans08_tot_north_v2[z=@sum]

save/file=MOC_RHO_PAC_${EXP}_v2.nc/append trans0000_tot_north_v2,trans0100_tot_north_v2,trans0201_tot_north_v2,trans0302_tot_north_v2,trans0403_tot_north_v2,trans0504_tot_north_v2,trans0605_tot_north_v2,trans0706_tot_north_v2,trans0807_tot_north_v2
!!,trans0008_tot_north_v2
!!--
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!--interior ocean component
let trans00_int_north = trans_rho_int_24N[z=1028:1031.86@sum]
let trans01_int_north = trans_rho_int_24N[z=1028:1032.79@sum]
let trans02_int_north = trans_rho_int_24N[z=1028:1033.89@sum]
let trans03_int_north = trans_rho_int_24N[z=1028:1035.03@sum]
let trans04_int_north = trans_rho_int_24N[z=1028:1035.35@sum]
let trans05_int_north = trans_rho_int_24N[z=1028:1036.20@sum]
let trans06_int_north = trans_rho_int_24N[z=1028:1036.80@sum]
let trans07_int_north = trans_rho_int_24N[z=1028:1036.90@sum]
let trans08_int_north = trans_rho_int_24N[z=@sum]

let trans0000_int_north = trans00_int_north
let trans0100_int_north = trans01_int_north-trans00_int_north
let trans0201_int_north = trans02_int_north-trans01_int_north
let trans0302_int_north = trans03_int_north-trans02_int_north
let trans0403_int_north = trans04_int_north-trans03_int_north
let trans0504_int_north = trans05_int_north-trans04_int_north
let trans0605_int_north = trans06_int_north-trans05_int_north
let trans0706_int_north = trans07_int_north-trans06_int_north
let trans0807_int_north = trans08_int_north-trans07_int_north
let trans0008_int_north =                   trans08_int_north

save/file=MOC_RHO_PAC_$EXP.nc/append trans0000_int_north,trans0100_int_north,trans0201_int_north,trans0302_int_north,trans0403_int_north,trans0504_int_north,trans0605_int_north,trans0706_int_north,trans0807_int_north,trans0008_int_north

!!--western boundary current
let trans00_wbc_north = trans_rho_wbc_24N[z=1028:1031.86@sum]
let trans01_wbc_north = trans_rho_wbc_24N[z=1028:1032.79@sum]
let trans02_wbc_north = trans_rho_wbc_24N[z=1028:1033.89@sum]
let trans03_wbc_north = trans_rho_wbc_24N[z=1028:1035.03@sum]
let trans04_wbc_north = trans_rho_wbc_24N[z=1028:1035.35@sum]
let trans05_wbc_north = trans_rho_wbc_24N[z=1028:1036.20@sum]
let trans06_wbc_north = trans_rho_wbc_24N[z=1028:1036.80@sum]
let trans07_wbc_north = trans_rho_wbc_24N[z=1028:1036.90@sum]
let trans08_wbc_north = trans_rho_wbc_24N[z=@sum]

let trans0000_wbc_north = trans00_wbc_north
let trans0100_wbc_north = trans01_wbc_north-trans00_wbc_north
let trans0201_wbc_north = trans02_wbc_north-trans01_wbc_north
let trans0302_wbc_north = trans03_wbc_north-trans02_wbc_north
let trans0403_wbc_north = trans04_wbc_north-trans03_wbc_north
let trans0504_wbc_north = trans05_wbc_north-trans04_wbc_north
let trans0605_wbc_north = trans06_wbc_north-trans05_wbc_north
let trans0706_wbc_north = trans07_wbc_north-trans06_wbc_north
let trans0807_wbc_north = trans08_wbc_north-trans07_wbc_north
let trans0008_wbc_north =                   trans08_wbc_north

save/file=MOC_RHO_PAC_$EXP.nc/append trans0000_wbc_north,trans0100_wbc_north,trans0201_wbc_north,trans0302_wbc_north,trans0403_wbc_north,trans0504_wbc_north,trans0605_wbc_north,trans0706_wbc_north,trans0807_wbc_north,trans0008_wbc_north

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!----Southern hemisphere
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!----mass transport across 24S
!!----total transport=wbc+int
let trans00_tot_south = trans_rho_tot_24S[z=1028:1032.11@sum] !!potrho24S
let trans01_tot_south = trans_rho_tot_24S[z=1028:1032.73@sum] !!potrho30S
let trans02_tot_south = trans_rho_tot_24S[z=1028:1033.93@sum] !!potrho40S
let trans03_tot_south = trans_rho_tot_24S[z=1028:1036.28@sum] !!potrho60S
let trans04_tot_south = trans_rho_tot_24S[z=1028:1036.57@sum] !!potrho64S
let trans05_tot_south = trans_rho_tot_24S[z=1028:1036.73@sum] !!potrho70S
let trans06_tot_south = trans_rho_tot_24S[z=1028:1036.85@sum]  
let trans07_tot_south = trans_rho_tot_24S[z=1028:1036.90@sum]
let trans08_tot_south = trans_rho_tot_24S[z=@sum]

let trans0000_tot_south = trans00_tot_south                   !!upper-24s
let trans0100_tot_south = trans01_tot_south-trans00_tot_south !!upper-30s
let trans0201_tot_south = trans02_tot_south-trans01_tot_south !!upper-40s
let trans0302_tot_south = trans03_tot_south-trans02_tot_south !!intermediate-60s
let trans0403_tot_south = trans04_tot_south-trans03_tot_south !!intermediate-64s
let trans0504_tot_south = trans05_tot_south-trans04_tot_south !!deep1-70s
let trans0605_tot_south = trans06_tot_south-trans05_tot_south !!deep2
let trans0706_tot_south = trans07_tot_south-trans06_tot_south !!deep3
let trans0807_tot_south = trans08_tot_south-trans07_tot_south !!bottom
let trans0008_tot_south =                   trans08_tot_south !!total-volume

save/file=MOC_RHO_PAC_$EXP.nc/append trans0000_tot_south,trans0100_tot_south,trans0201_tot_south,trans0302_tot_south,trans0403_tot_south,trans0504_tot_south,trans0605_tot_south,trans0706_tot_south,trans0807_tot_south,trans0008_tot_south

!!--interior ocean transport (non wbc contribution)
let trans00_int_south = trans_rho_int_24S[z=1028:1032.10@sum] !!potrho24S
let trans01_int_south = trans_rho_int_24S[z=1028:1032.73@sum] !!potrho30S
let trans02_int_south = trans_rho_int_24S[z=1028:1033.93@sum] !!potrho40S
let trans03_int_south = trans_rho_int_24S[z=1028:1036.28@sum] !!potrho60S
let trans04_int_south = trans_rho_int_24S[z=1028:1036.57@sum] !!potrho64S
let trans05_int_south = trans_rho_int_24S[z=1028:1036.73@sum] !!potrho70S
let trans06_int_south = trans_rho_int_24S[z=1028:1036.85@sum]  
let trans07_int_south = trans_rho_int_24S[z=1028:1036.90@sum]
let trans08_int_south = trans_rho_int_24S[z=@sum]

let trans0000_int_south = trans00_int_south                   !!upper-24s
let trans0100_int_south = trans01_int_south-trans00_int_south !!upper-30s
let trans0201_int_south = trans02_int_south-trans01_int_south !!upper-40s
let trans0302_int_south = trans03_int_south-trans02_int_south !!intermediate-60s
let trans0403_int_south = trans04_int_south-trans03_int_south !!intermediate-64s
let trans0504_int_south = trans05_int_south-trans04_int_south !!deep1-70s
let trans0605_int_south = trans06_int_south-trans05_int_south !!deep2
let trans0706_int_south = trans07_int_south-trans06_int_south !!deep3
let trans0807_int_south = trans08_int_south-trans07_int_south !!bottom
let trans0008_int_south =                   trans08_int_south !!total-volume

save/file=MOC_RHO_PAC_$EXP.nc/append trans0000_int_south,trans0100_int_south,trans0201_int_south,trans0302_int_south,trans0403_int_south,trans0504_int_south,trans0605_int_south,trans0706_int_south,trans0807_int_south,trans0008_int_south

!!--western boundary contribution alone
let trans00_wbc_south = trans_rho_wbc_24S[z=1028:1032.10@sum] !!potrho24S
let trans01_wbc_south = trans_rho_wbc_24S[z=1028:1032.73@sum] !!potrho30S
let trans02_wbc_south = trans_rho_wbc_24S[z=1028:1033.93@sum] !!potrho40S
let trans03_wbc_south = trans_rho_wbc_24S[z=1028:1036.28@sum] !!potrho60S
let trans04_wbc_south = trans_rho_wbc_24S[z=1028:1036.57@sum] !!potrho64S
let trans05_wbc_south = trans_rho_wbc_24S[z=1028:1036.73@sum] !!potrho70S
let trans06_wbc_south = trans_rho_wbc_24S[z=1028:1036.85@sum]  
let trans07_wbc_south = trans_rho_wbc_24S[z=1028:1036.90@sum]
let trans08_wbc_south = trans_rho_wbc_24S[z=@sum]

let trans0000_wbc_south = trans00_wbc_south                   !!upper-24s
let trans0100_wbc_south = trans01_wbc_south-trans00_wbc_south !!upper-30s
let trans0201_wbc_south = trans02_wbc_south-trans01_wbc_south !!upper-40s
let trans0302_wbc_south = trans03_wbc_south-trans02_wbc_south !!wbcermediate-60s
let trans0403_wbc_south = trans04_wbc_south-trans03_wbc_south !!wbcermediate-64s
let trans0504_wbc_south = trans05_wbc_south-trans04_wbc_south !!deep1-70s
let trans0605_wbc_south = trans06_wbc_south-trans05_wbc_south !!deep2
let trans0706_wbc_south = trans07_wbc_south-trans06_wbc_south !!deep3
let trans0807_wbc_south = trans08_wbc_south-trans07_wbc_south !!bottom
let trans0008_wbc_south =                   trans08_wbc_south !!total-volume

save/file=MOC_RHO_PAC_$EXP.nc/append trans0000_wbc_south,trans0100_wbc_south,trans0201_wbc_south,trans0302_wbc_south,trans0403_wbc_south,trans0504_wbc_south,trans0605_wbc_south,trans0706_wbc_south,trans0807_wbc_south,trans0008_wbc_south

exit
!
/bin/rm -f ferret.jnl*
@ i = $i + 1

end
