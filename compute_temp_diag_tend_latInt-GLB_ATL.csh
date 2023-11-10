#!/bin/csh

module load nco
module load cdo
module load ferret

set echo on

cd /home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/TEMP-tend/DATA
set RUN = (flux-only FAFSTRESS FAFWATER FAFHEAT)

set i = 1

while ($i <= 4)
set EXP  = $RUN[$i]

ferret <<!

set region/z=0:5500/y=90S:90N/
set mem/size=9999

use "/home/netapp-clima-users1/rfarneti/ANALYSIS/grids/MOM1/regionmask_v6.nc" !1
let one=tmask[d=1]/tmask[d=1]

let tmask_glb  = if (( tmask[d=1] EQ 1 OR tmask[d=1] EQ 2 OR tmask[d=1] EQ 3 OR tmask[d=1] EQ 4 OR tmask[d=1] EQ 5)) then one else one-11
let tmask_atl  = if (( tmask[d=1] EQ 2 OR tmask[d=1] EQ 4)) then one else one-11
let tmask_ipa  = if (( tmask[d=1] EQ 3 OR tmask[d=1] EQ 5)) then one else one-11
let tmask_pac  = if (( tmask[d=1] EQ 3 )) then one else one-11
let tmask_ind  = if (( tmask[d=1] EQ 5 )) then one else one-11

set variable/bad=-10. tmask_glb
set variable/bad=-10. tmask_atl
set variable/bad=-10. tmask_ipa
set variable/bad=-10. tmask_pac
set variable/bad=-10. tmask_ind

!!!SET MEMORY/SIZE=888

use "/home/clima-archive2/rfarneti/RENE/DATA/area_t_$EXP.nc" !2
use temp_diag_tend-$EXP.nc !3

let temptend_glb          = temp_tendency[d=3]*area_t[d=2]
let advection_glb         = temp_advection[d=3]*area_t[d=2]
let submeso_glb           = temp_submeso[d=3]*area_t[d=2]
let vdiffuse_diff_cbt_glb = temp_vdiffuse_diff_cbt[d=3]*area_t[d=2]
let neutral_diffusion_glb = neutral_diffusion_temp[d=3]*area_t[d=2]
let neutral_gm_glb        = neutral_gm_temp[d=3]*area_t[d=2]
let swh_glb               = sw_heat[d=3]*area_t[d=2]


!!!!!!!!!!!!!!!!!
!!!GLB
!!!!!!!!!!!!!!!!!
let temptend          = temptend_glb[k=27:50@sum]*tmask_glb
let advection         = advection_glb[k=27:50@sum]*tmask_glb
let submeso           = submeso_glb[k=27:50@sum]*tmask_glb
let vdiffuse_diff_cbt = vdiffuse_diff_cbt_glb[k=27:50@sum]*tmask_glb
let neutral_diffusion = neutral_diffusion_glb[k=27:50@sum]*tmask_glb
let neutral_gm        = neutral_gm_glb[k=27:50@sum]*tmask_glb
let swh               = swh_glb[k=27:50@sum]*tmask_glb

!!!GLB 5S-5N
save/file=heat_budget_${EXP}_GLB_05S-05N.nc/clobber temptend[x=@sum,y=5s:5n@sum]
save/file=heat_budget_${EXP}_GLB_05S-05N.nc/append  advection[x=@sum,y=5s:5n@sum]
save/file=heat_budget_${EXP}_GLB_05S-05N.nc/append  submeso[x=@sum,y=5s:5n@sum]
save/file=heat_budget_${EXP}_GLB_05S-05N.nc/append  vdiffuse_diff_cbt[x=@sum,y=5s:5n@sum]
save/file=heat_budget_${EXP}_GLB_05S-05N.nc/append  neutral_diffusion[x=@sum,y=5s:5n@sum]
save/file=heat_budget_${EXP}_GLB_05S-05N.nc/append  neutral_gm[x=@sum,y=5s:5n@sum]
save/file=heat_budget_${EXP}_GLB_05S-05N.nc/append  swh[x=@sum,y=5s:5n@sum]

!!!GLB 10S-10N
save/file=heat_budget_${EXP}_GLB_10S-10N.nc/clobber temptend[x=@sum,y=10s:10n@sum]
save/file=heat_budget_${EXP}_GLB_10S-10N.nc/append  advection[x=@sum,y=10s:10n@sum]
save/file=heat_budget_${EXP}_GLB_10S-10N.nc/append  submeso[x=@sum,y=10s:10n@sum]
save/file=heat_budget_${EXP}_GLB_10S-10N.nc/append  vdiffuse_diff_cbt[x=@sum,y=10s:10n@sum]
save/file=heat_budget_${EXP}_GLB_10S-10N.nc/append  neutral_diffusion[x=@sum,y=10s:10n@sum]
save/file=heat_budget_${EXP}_GLB_10S-10N.nc/append  neutral_gm[x=@sum,y=10s:10n@sum]
save/file=heat_budget_${EXP}_GLB_10S-10N.nc/append  swh[x=@sum,y=10s:10n@sum]

!!!GLB 15S-15N
save/file=heat_budget_${EXP}_GLB_15S-15N.nc/clobber temptend[x=@sum,y=15s:15n@sum]
save/file=heat_budget_${EXP}_GLB_15S-15N.nc/append  advection[x=@sum,y=15s:15n@sum]
save/file=heat_budget_${EXP}_GLB_15S-15N.nc/append  submeso[x=@sum,y=15s:15n@sum]
save/file=heat_budget_${EXP}_GLB_15S-15N.nc/append  vdiffuse_diff_cbt[x=@sum,y=15s:15n@sum]
save/file=heat_budget_${EXP}_GLB_15S-15N.nc/append  neutral_diffusion[x=@sum,y=15s:15n@sum]
save/file=heat_budget_${EXP}_GLB_15S-15N.nc/append  neutral_gm[x=@sum,y=15s:15n@sum]
save/file=heat_budget_${EXP}_GLB_15S-15N.nc/append  swh[x=@sum,y=15s:15n@sum]

!!!GLB 20S-20N
save/file=heat_budget_${EXP}_GLB_20S-20N.nc/clobber temptend[x=@sum,y=20s:20n@sum]
save/file=heat_budget_${EXP}_GLB_20S-20N.nc/append  advection[x=@sum,y=20s:20n@sum]
save/file=heat_budget_${EXP}_GLB_20S-20N.nc/append  submeso[x=@sum,y=20s:20n@sum]
save/file=heat_budget_${EXP}_GLB_20S-20N.nc/append  vdiffuse_diff_cbt[x=@sum,y=20s:20n@sum]
save/file=heat_budget_${EXP}_GLB_20S-20N.nc/append  neutral_diffusion[x=@sum,y=20s:20n@sum]
save/file=heat_budget_${EXP}_GLB_20S-20N.nc/append  neutral_gm[x=@sum,y=20s:20n@sum]
save/file=heat_budget_${EXP}_GLB_20S-20N.nc/append  swh[x=@sum,y=20s:20n@sum]

!!!GLB 25S-25N
save/file=heat_budget_${EXP}_GLB_25S-25N.nc/clobber temptend[x=@sum,y=25s:25n@sum]
save/file=heat_budget_${EXP}_GLB_25S-25N.nc/append  advection[x=@sum,y=25s:25n@sum]
save/file=heat_budget_${EXP}_GLB_25S-25N.nc/append  submeso[x=@sum,y=25s:25n@sum]
save/file=heat_budget_${EXP}_GLB_25S-25N.nc/append  vdiffuse_diff_cbt[x=@sum,y=25s:25n@sum]
save/file=heat_budget_${EXP}_GLB_25S-25N.nc/append  neutral_diffusion[x=@sum,y=25s:25n@sum]
save/file=heat_budget_${EXP}_GLB_25S-25N.nc/append  neutral_gm[x=@sum,y=25s:25n@sum]
save/file=heat_budget_${EXP}_GLB_25S-25N.nc/append  swh[x=@sum,y=25s:25n@sum]

!!!GLB 30S-30N
save/file=heat_budget_${EXP}_GLB_30S-30N.nc/clobber temptend[x=@sum,y=30s:30n@sum]
save/file=heat_budget_${EXP}_GLB_30S-30N.nc/append  advection[x=@sum,y=30s:30n@sum]
save/file=heat_budget_${EXP}_GLB_30S-30N.nc/append  submeso[x=@sum,y=30s:30n@sum]
save/file=heat_budget_${EXP}_GLB_30S-30N.nc/append  vdiffuse_diff_cbt[x=@sum,y=30s:30n@sum]
save/file=heat_budget_${EXP}_GLB_30S-30N.nc/append  neutral_diffusion[x=@sum,y=30s:30n@sum]
save/file=heat_budget_${EXP}_GLB_30S-30N.nc/append  neutral_gm[x=@sum,y=30s:30n@sum]
save/file=heat_budget_${EXP}_GLB_30S-30N.nc/append  swh[x=@sum,y=30s:30n@sum]

!!!GLB 35S-35N
save/file=heat_budget_${EXP}_GLB_35S-35N.nc/clobber temptend[x=@sum,y=35s:35n@sum]
save/file=heat_budget_${EXP}_GLB_35S-35N.nc/append  advection[x=@sum,y=35s:35n@sum]
save/file=heat_budget_${EXP}_GLB_35S-35N.nc/append  submeso[x=@sum,y=35s:35n@sum]
save/file=heat_budget_${EXP}_GLB_35S-35N.nc/append  vdiffuse_diff_cbt[x=@sum,y=35s:35n@sum]
save/file=heat_budget_${EXP}_GLB_35S-35N.nc/append  neutral_diffusion[x=@sum,y=35s:35n@sum]
save/file=heat_budget_${EXP}_GLB_35S-35N.nc/append  neutral_gm[x=@sum,y=35s:35n@sum]
save/file=heat_budget_${EXP}_GLB_35S-35N.nc/append  swh[x=@sum,y=35s:35n@sum]

!!!GLB 40S-40N
save/file=heat_budget_${EXP}_GLB_40S-40N.nc/clobber temptend[x=@sum,y=40s:40n@sum]
save/file=heat_budget_${EXP}_GLB_40S-40N.nc/append  advection[x=@sum,y=40s:40n@sum]
save/file=heat_budget_${EXP}_GLB_40S-40N.nc/append  submeso[x=@sum,y=40s:40n@sum]
save/file=heat_budget_${EXP}_GLB_40S-40N.nc/append  vdiffuse_diff_cbt[x=@sum,y=40s:40n@sum]
save/file=heat_budget_${EXP}_GLB_40S-40N.nc/append  neutral_diffusion[x=@sum,y=40s:40n@sum]
save/file=heat_budget_${EXP}_GLB_40S-40N.nc/append  neutral_gm[x=@sum,y=40s:40n@sum]
save/file=heat_budget_${EXP}_GLB_40S-40N.nc/append  swh[x=@sum,y=40s:40n@sum]

!!!GLB 45S-45N
save/file=heat_budget_${EXP}_GLB_45S-45N.nc/clobber temptend[x=@sum,y=45s:45n@sum]
save/file=heat_budget_${EXP}_GLB_45S-45N.nc/append  advection[x=@sum,y=45s:45n@sum]
save/file=heat_budget_${EXP}_GLB_45S-45N.nc/append  submeso[x=@sum,y=45s:45n@sum]
save/file=heat_budget_${EXP}_GLB_45S-45N.nc/append  vdiffuse_diff_cbt[x=@sum,y=45s:45n@sum]
save/file=heat_budget_${EXP}_GLB_45S-45N.nc/append  neutral_diffusion[x=@sum,y=45s:45n@sum]
save/file=heat_budget_${EXP}_GLB_45S-45N.nc/append  neutral_gm[x=@sum,y=45s:45n@sum]
save/file=heat_budget_${EXP}_GLB_45S-45N.nc/append  swh[x=@sum,y=45s:45n@sum]

!!!GLB 50S-50N
save/file=heat_budget_${EXP}_GLB_50S-50N.nc/clobber temptend[x=@sum,y=50s:50n@sum]
save/file=heat_budget_${EXP}_GLB_50S-50N.nc/append  advection[x=@sum,y=50s:50n@sum]
save/file=heat_budget_${EXP}_GLB_50S-50N.nc/append  submeso[x=@sum,y=50s:50n@sum]
save/file=heat_budget_${EXP}_GLB_50S-50N.nc/append  vdiffuse_diff_cbt[x=@sum,y=50s:50n@sum]
save/file=heat_budget_${EXP}_GLB_50S-50N.nc/append  neutral_diffusion[x=@sum,y=50s:50n@sum]
save/file=heat_budget_${EXP}_GLB_50S-50N.nc/append  neutral_gm[x=@sum,y=50s:50n@sum]
save/file=heat_budget_${EXP}_GLB_50S-50N.nc/append  swh[x=@sum,y=50s:50n@sum]

!!!GLB 55S-55N
save/file=heat_budget_${EXP}_GLB_55S-55N.nc/clobber temptend[x=@sum,y=55s:55n@sum]
save/file=heat_budget_${EXP}_GLB_55S-55N.nc/append  advection[x=@sum,y=55s:55n@sum]
save/file=heat_budget_${EXP}_GLB_55S-55N.nc/append  submeso[x=@sum,y=55s:55n@sum]
save/file=heat_budget_${EXP}_GLB_55S-55N.nc/append  vdiffuse_diff_cbt[x=@sum,y=55s:55n@sum]
save/file=heat_budget_${EXP}_GLB_55S-55N.nc/append  neutral_diffusion[x=@sum,y=55s:55n@sum]
save/file=heat_budget_${EXP}_GLB_55S-55N.nc/append  neutral_gm[x=@sum,y=55s:55n@sum]
save/file=heat_budget_${EXP}_GLB_55S-55N.nc/append  swh[x=@sum,y=55s:55n@sum]

!!!GLB 60S-60N
save/file=heat_budget_${EXP}_GLB_60S-60N.nc/clobber temptend[x=@sum,y=60s:60n@sum]
save/file=heat_budget_${EXP}_GLB_60S-60N.nc/append  advection[x=@sum,y=60s:60n@sum]
save/file=heat_budget_${EXP}_GLB_60S-60N.nc/append  submeso[x=@sum,y=60s:60n@sum]
save/file=heat_budget_${EXP}_GLB_60S-60N.nc/append  vdiffuse_diff_cbt[x=@sum,y=60s:60n@sum]
save/file=heat_budget_${EXP}_GLB_60S-60N.nc/append  neutral_diffusion[x=@sum,y=60s:60n@sum]
save/file=heat_budget_${EXP}_GLB_60S-60N.nc/append  neutral_gm[x=@sum,y=60s:60n@sum]
save/file=heat_budget_${EXP}_GLB_60S-60N.nc/append  swh[x=@sum,y=60s:60n@sum]

!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!ATL
!!!!!!!!!!!!!!!!!!!!!!!!!!
let temptend          = temptend_glb[k=27:50@sum]*tmask_atl
let advection         = advection_glb[k=27:50@sum]*tmask_atl
let submeso           = submeso_glb[k=27:50@sum]*tmask_atl
let vdiffuse_diff_cbt = vdiffuse_diff_cbt_glb[k=27:50@sum]*tmask_atl
let neutral_diffusion = neutral_diffusion_glb[k=27:50@sum]*tmask_atl
let neutral_gm        = neutral_gm_glb[k=27:50@sum]*tmask_atl
let swh               = swh_glb[k=27:50@sum]*tmask_atl

!!!ATL 5S-5N
save/file=heat_budget_${EXP}_ATL_05S-05N.nc/clobber temptend[x=@sum,y=5s:5n@sum]
save/file=heat_budget_${EXP}_ATL_05S-05N.nc/append  advection[x=@sum,y=5s:5n@sum]
save/file=heat_budget_${EXP}_ATL_05S-05N.nc/append  submeso[x=@sum,y=5s:5n@sum]
save/file=heat_budget_${EXP}_ATL_05S-05N.nc/append  vdiffuse_diff_cbt[x=@sum,y=5s:5n@sum]
save/file=heat_budget_${EXP}_ATL_05S-05N.nc/append  neutral_diffusion[x=@sum,y=5s:5n@sum]
save/file=heat_budget_${EXP}_ATL_05S-05N.nc/append  neutral_gm[x=@sum,y=5s:5n@sum]
save/file=heat_budget_${EXP}_ATL_05S-05N.nc/append  swh[x=@sum,y=5s:5n@sum]

!!!ATL 10S-10N
save/file=heat_budget_${EXP}_ATL_10S-10N.nc/clobber temptend[x=@sum,y=10s:10n@sum]
save/file=heat_budget_${EXP}_ATL_10S-10N.nc/append  advection[x=@sum,y=10s:10n@sum]
save/file=heat_budget_${EXP}_ATL_10S-10N.nc/append  submeso[x=@sum,y=10s:10n@sum]
save/file=heat_budget_${EXP}_ATL_10S-10N.nc/append  vdiffuse_diff_cbt[x=@sum,y=10s:10n@sum]
save/file=heat_budget_${EXP}_ATL_10S-10N.nc/append  neutral_diffusion[x=@sum,y=10s:10n@sum]
save/file=heat_budget_${EXP}_ATL_10S-10N.nc/append  neutral_gm[x=@sum,y=10s:10n@sum]
save/file=heat_budget_${EXP}_ATL_10S-10N.nc/append  swh[x=@sum,y=10s:10n@sum]

!!!ATL 15S-15N
save/file=heat_budget_${EXP}_ATL_15S-15N.nc/clobber temptend[x=@sum,y=15s:15n@sum]
save/file=heat_budget_${EXP}_ATL_15S-15N.nc/append  advection[x=@sum,y=15s:15n@sum]
save/file=heat_budget_${EXP}_ATL_15S-15N.nc/append  submeso[x=@sum,y=15s:15n@sum]
save/file=heat_budget_${EXP}_ATL_15S-15N.nc/append  vdiffuse_diff_cbt[x=@sum,y=15s:15n@sum]
save/file=heat_budget_${EXP}_ATL_15S-15N.nc/append  neutral_diffusion[x=@sum,y=15s:15n@sum]
save/file=heat_budget_${EXP}_ATL_15S-15N.nc/append  neutral_gm[x=@sum,y=15s:15n@sum]
save/file=heat_budget_${EXP}_ATL_15S-15N.nc/append  swh[x=@sum,y=15s:15n@sum]

!!!ATL 20S-20N
save/file=heat_budget_${EXP}_ATL_20S-20N.nc/clobber temptend[x=@sum,y=20s:20n@sum]
save/file=heat_budget_${EXP}_ATL_20S-20N.nc/append  advection[x=@sum,y=20s:20n@sum]
save/file=heat_budget_${EXP}_ATL_20S-20N.nc/append  submeso[x=@sum,y=20s:20n@sum]
save/file=heat_budget_${EXP}_ATL_20S-20N.nc/append  vdiffuse_diff_cbt[x=@sum,y=20s:20n@sum]
save/file=heat_budget_${EXP}_ATL_20S-20N.nc/append  neutral_diffusion[x=@sum,y=20s:20n@sum]
save/file=heat_budget_${EXP}_ATL_20S-20N.nc/append  neutral_gm[x=@sum,y=20s:20n@sum]
save/file=heat_budget_${EXP}_ATL_20S-20N.nc/append  swh[x=@sum,y=20s:20n@sum]

!!!ATL 25S-25N
save/file=heat_budget_${EXP}_ATL_25S-25N.nc/clobber temptend[x=@sum,y=25s:25n@sum]
save/file=heat_budget_${EXP}_ATL_25S-25N.nc/append  advection[x=@sum,y=25s:25n@sum]
save/file=heat_budget_${EXP}_ATL_25S-25N.nc/append  submeso[x=@sum,y=25s:25n@sum]
save/file=heat_budget_${EXP}_ATL_25S-25N.nc/append  vdiffuse_diff_cbt[x=@sum,y=25s:25n@sum]
save/file=heat_budget_${EXP}_ATL_25S-25N.nc/append  neutral_diffusion[x=@sum,y=25s:25n@sum]
save/file=heat_budget_${EXP}_ATL_25S-25N.nc/append  neutral_gm[x=@sum,y=25s:25n@sum]
save/file=heat_budget_${EXP}_ATL_25S-25N.nc/append  swh[x=@sum,y=25s:25n@sum]

!!!ATL 30S-30N
save/file=heat_budget_${EXP}_ATL_30S-30N.nc/clobber temptend[x=@sum,y=30s:30n@sum]
save/file=heat_budget_${EXP}_ATL_30S-30N.nc/append  advection[x=@sum,y=30s:30n@sum]
save/file=heat_budget_${EXP}_ATL_30S-30N.nc/append  submeso[x=@sum,y=30s:30n@sum]
save/file=heat_budget_${EXP}_ATL_30S-30N.nc/append  vdiffuse_diff_cbt[x=@sum,y=30s:30n@sum]
save/file=heat_budget_${EXP}_ATL_30S-30N.nc/append  neutral_diffusion[x=@sum,y=30s:30n@sum]
save/file=heat_budget_${EXP}_ATL_30S-30N.nc/append  neutral_gm[x=@sum,y=30s:30n@sum]
save/file=heat_budget_${EXP}_ATL_30S-30N.nc/append  swh[x=@sum,y=30s:30n@sum]

!!!ATL 35S-35N
save/file=heat_budget_${EXP}_ATL_35S-35N.nc/clobber temptend[x=@sum,y=35s:35n@sum]
save/file=heat_budget_${EXP}_ATL_35S-35N.nc/append  advection[x=@sum,y=35s:35n@sum]
save/file=heat_budget_${EXP}_ATL_35S-35N.nc/append  submeso[x=@sum,y=35s:35n@sum]
save/file=heat_budget_${EXP}_ATL_35S-35N.nc/append  vdiffuse_diff_cbt[x=@sum,y=35s:35n@sum]
save/file=heat_budget_${EXP}_ATL_35S-35N.nc/append  neutral_diffusion[x=@sum,y=35s:35n@sum]
save/file=heat_budget_${EXP}_ATL_35S-35N.nc/append  neutral_gm[x=@sum,y=35s:35n@sum]
save/file=heat_budget_${EXP}_ATL_35S-35N.nc/append  swh[x=@sum,y=35s:35n@sum]

!!!ATL 40S-40N
save/file=heat_budget_${EXP}_ATL_40S-40N.nc/clobber temptend[x=@sum,y=40s:40n@sum]
save/file=heat_budget_${EXP}_ATL_40S-40N.nc/append  advection[x=@sum,y=40s:40n@sum]
save/file=heat_budget_${EXP}_ATL_40S-40N.nc/append  submeso[x=@sum,y=40s:40n@sum]
save/file=heat_budget_${EXP}_ATL_40S-40N.nc/append  vdiffuse_diff_cbt[x=@sum,y=40s:40n@sum]
save/file=heat_budget_${EXP}_ATL_40S-40N.nc/append  neutral_diffusion[x=@sum,y=40s:40n@sum]
save/file=heat_budget_${EXP}_ATL_40S-40N.nc/append  neutral_gm[x=@sum,y=40s:40n@sum]
save/file=heat_budget_${EXP}_ATL_40S-40N.nc/append  swh[x=@sum,y=40s:40n@sum]

!!!ATL 45S-45N
save/file=heat_budget_${EXP}_ATL_45S-45N.nc/clobber temptend[x=@sum,y=45s:45n@sum]
save/file=heat_budget_${EXP}_ATL_45S-45N.nc/append  advection[x=@sum,y=45s:45n@sum]
save/file=heat_budget_${EXP}_ATL_45S-45N.nc/append  submeso[x=@sum,y=45s:45n@sum]
save/file=heat_budget_${EXP}_ATL_45S-45N.nc/append  vdiffuse_diff_cbt[x=@sum,y=45s:45n@sum]
save/file=heat_budget_${EXP}_ATL_45S-45N.nc/append  neutral_diffusion[x=@sum,y=45s:45n@sum]
save/file=heat_budget_${EXP}_ATL_45S-45N.nc/append  neutral_gm[x=@sum,y=45s:45n@sum]
save/file=heat_budget_${EXP}_ATL_45S-45N.nc/append  swh[x=@sum,y=45s:45n@sum]

!!!ATL 50S-50N
save/file=heat_budget_${EXP}_ATL_50S-50N.nc/clobber temptend[x=@sum,y=50s:50n@sum]
save/file=heat_budget_${EXP}_ATL_50S-50N.nc/append  advection[x=@sum,y=50s:50n@sum]
save/file=heat_budget_${EXP}_ATL_50S-50N.nc/append  submeso[x=@sum,y=50s:50n@sum]
save/file=heat_budget_${EXP}_ATL_50S-50N.nc/append  vdiffuse_diff_cbt[x=@sum,y=50s:50n@sum]
save/file=heat_budget_${EXP}_ATL_50S-50N.nc/append  neutral_diffusion[x=@sum,y=50s:50n@sum]
save/file=heat_budget_${EXP}_ATL_50S-50N.nc/append  neutral_gm[x=@sum,y=50s:50n@sum]
save/file=heat_budget_${EXP}_ATL_50S-50N.nc/append  swh[x=@sum,y=50s:50n@sum]

!!!ATL 55S-55N
save/file=heat_budget_${EXP}_ATL_55S-55N.nc/clobber temptend[x=@sum,y=55s:55n@sum]
save/file=heat_budget_${EXP}_ATL_55S-55N.nc/append  advection[x=@sum,y=55s:55n@sum]
save/file=heat_budget_${EXP}_ATL_55S-55N.nc/append  submeso[x=@sum,y=55s:55n@sum]
save/file=heat_budget_${EXP}_ATL_55S-55N.nc/append  vdiffuse_diff_cbt[x=@sum,y=55s:55n@sum]
save/file=heat_budget_${EXP}_ATL_55S-55N.nc/append  neutral_diffusion[x=@sum,y=55s:55n@sum]
save/file=heat_budget_${EXP}_ATL_55S-55N.nc/append  neutral_gm[x=@sum,y=55s:55n@sum]
save/file=heat_budget_${EXP}_ATL_55S-55N.nc/append  swh[x=@sum,y=55s:55n@sum]

!!!ATL 60S-60N
save/file=heat_budget_${EXP}_ATL_60S-60N.nc/clobber temptend[x=@sum,y=60s:60n@sum]
save/file=heat_budget_${EXP}_ATL_60S-60N.nc/append  advection[x=@sum,y=60s:60n@sum]
save/file=heat_budget_${EXP}_ATL_60S-60N.nc/append  submeso[x=@sum,y=60s:60n@sum]
save/file=heat_budget_${EXP}_ATL_60S-60N.nc/append  vdiffuse_diff_cbt[x=@sum,y=60s:60n@sum]
save/file=heat_budget_${EXP}_ATL_60S-60N.nc/append  neutral_diffusion[x=@sum,y=60s:60n@sum]
save/file=heat_budget_${EXP}_ATL_60S-60N.nc/append  neutral_gm[x=@sum,y=60s:60n@sum]
save/file=heat_budget_${EXP}_ATL_60S-60N.nc/append  swh[x=@sum,y=60s:60n@sum]

exit
!
/bin/rm -f ferret.jnl*
@ i = $i + 1

end
