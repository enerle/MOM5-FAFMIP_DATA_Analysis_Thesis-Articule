#!/bin/csh

module load nco
module load cdo
module load ferret

set echo on

cd /home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA_TEMP-tend
set RUN = (flux-only FAFSTRESS FAFWATER FAFHEAT)

set i = 1

while ($i <= 4)
set EXP  = $RUN[$i]

ferret <<!

set region/z=0:5500/y=90S:90N/
set mem/size=9999

use "/home/netapp-clima-users/rnavarro/ANALYSIS/regionmask_v6.nc"
let one=tmask[d=1]/tmask[d=1]
let tmask_glb  = if (( tmask[d=1] EQ 1 OR tmask[d=1] EQ 2 OR tmask[d=1] EQ 3 OR tmask[d=1] EQ 4 OR tmask[d=1] EQ 5)) then one else one-11
let tmask_atl = if (( tmask[d=1] EQ 2 OR tmask[d=1] EQ 4)) then one else one-11
let tmask_ipa = if (( tmask[d=1] EQ 3 OR tmask[d=1] EQ 5)) then one else one-11
let tmask_soc = if (( tmask[d=1] EQ 1 )) then one else one-11
let tmask_pac = if (( tmask[d=1] EQ 3 )) then one else one-11
let tmask_ind = if (( tmask[d=1] EQ 5 )) then one else one-11

set variable/bad=-10. tmask_glb
set variable/bad=-10. tmask_atl
set variable/bad=-10. tmask_ipa
set variable/bad=-10. tmask_soc
set variable/bad=-10. tmask_pac
set variable/bad=-10. tmask_ind

SET MEMORY/SIZE=888

use "/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA/area_t_$EXP.nc" !2
use temp_diag_tend-$EXP.nc !3

let temptend_glb          = temp_tendency[d=3]*area_t[d=2]
let advection_glb         = temp_advection[d=3]*area_t[d=2]
let submeso_glb           = temp_submeso[d=3]*area_t[d=2]
let vdiffuse_diff_cbt_glb = temp_vdiffuse_diff_cbt[d=3]*area_t[d=2]
let neutral_diffusion_glb = neutral_diffusion_temp[d=3]*area_t[d=2]
let neutral_gm_glb        = neutral_gm_temp[d=3]*area_t[d=2]
let swh_glb               = sw_heat[d=3]*area_t[d=2]

!!!GLB
let temptend          = temptend_glb[k=1:50@sum]*tmask_glb
let advection         = advection_glb[k=1:50@sum]*tmask_glb
let submeso           = submeso_glb[k=1:50@sum]*tmask_glb
let vdiffuse_diff_cbt = vdiffuse_diff_cbt_glb[k=1:50@sum]*tmask_glb
let neutral_diffusion = neutral_diffusion_glb[k=1:50@sum]*tmask_glb
let neutral_gm        = neutral_gm_glb[k=1:50@sum]*tmask_glb
let swh               = swh_glb[k=1:50@sum]*tmask_glb

save/file=heat_budget_${EXP}_GLB.nc/clobber temptend[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_GLB.nc/append  advection[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_GLB.nc/append  submeso[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_GLB.nc/append  vdiffuse_diff_cbt[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_GLB.nc/append  neutral_diffusion[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_GLB.nc/append  neutral_gm[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_GLB.nc/append  swh[i=@sum,j=@sum]

!!!ATL
let temptend          = temptend_glb[k=1:50@sum]*tmask_atl
let advection         = advection_glb[k=1:50@sum]*tmask_atl
let submeso           = submeso_glb[k=1:50@sum]*tmask_atl
let vdiffuse_diff_cbt = vdiffuse_diff_cbt_glb[k=1:50@sum]*tmask_atl
let neutral_diffusion = neutral_diffusion_glb[k=1:50@sum]*tmask_atl
let neutral_gm        = neutral_gm_glb[k=1:50@sum]*tmask_atl
let swh               = swh_glb[k=1:50@sum]*tmask_atl

save/file=heat_budget_${EXP}_ATL.nc/clobber temptend[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_ATL.nc/append  advection[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_ATL.nc/append  submeso[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_ATL.nc/append  vdiffuse_diff_cbt[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_ATL.nc/append  neutral_diffusion[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_ATL.nc/append  neutral_gm[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_ATL.nc/append  swh[i=@sum,j=@sum]

!!!IPA
let temptend          = temptend_glb[k=1:50@sum]*tmask_ipa
let advection         = advection_glb[k=1:50@sum]*tmask_ipa
let submeso           = submeso_glb[k=1:50@sum]*tmask_ipa
let vdiffuse_diff_cbt = vdiffuse_diff_cbt_glb[k=1:50@sum]*tmask_ipa
let neutral_diffusion = neutral_diffusion_glb[k=1:50@sum]*tmask_ipa
let neutral_gm        = neutral_gm_glb[k=1:50@sum]*tmask_ipa
let swh               = swh_glb[k=1:50@sum]*tmask_ipa

save/file=heat_budget_${EXP}_IPA.nc/clobber temptend[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_IPA.nc/append  advection[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_IPA.nc/append  submeso[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_IPA.nc/append  vdiffuse_diff_cbt[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_IPA.nc/append  neutral_diffusion[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_IPA.nc/append  neutral_gm[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_IPA.nc/append  swh[i=@sum,j=@sum]

!!!SOC
let temptend          = temptend_glb[k=1:50@sum]*tmask_soc
let advection         = advection_glb[k=1:50@sum]*tmask_soc
let submeso           = submeso_glb[k=1:50@sum]*tmask_soc
let vdiffuse_diff_cbt = vdiffuse_diff_cbt_glb[k=1:50@sum]*tmask_soc
let neutral_diffusion = neutral_diffusion_glb[k=1:50@sum]*tmask_soc
let neutral_gm        = neutral_gm_glb[k=1:50@sum]*tmask_soc
let swh               = swh_glb[k=1:50@sum]*tmask_soc

save/file=heat_budget_${EXP}_SOC.nc/clobber temptend[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_SOC.nc/append  advection[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_SOC.nc/append  submeso[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_SOC.nc/append  vdiffuse_diff_cbt[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_SOC.nc/append  neutral_diffusion[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_SOC.nc/append  neutral_gm[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_SOC.nc/append  swh[i=@sum,j=@sum]

!!!PAC
let temptend          = temptend_glb[k=1:50@sum]*tmask_pac
let advection         = advection_glb[k=1:50@sum]*tmask_pac
let submeso           = submeso_glb[k=1:50@sum]*tmask_pac
let vdiffuse_diff_cbt = vdiffuse_diff_cbt_glb[k=1:50@sum]*tmask_pac
let neutral_diffusion = neutral_diffusion_glb[k=1:50@sum]*tmask_pac
let neutral_gm        = neutral_gm_glb[k=1:50@sum]*tmask_pac
let swh               = swh_glb[k=1:50@sum]*tmask_pac

save/file=heat_budget_${EXP}_PAC.nc/clobber temptend[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_PAC.nc/append  advection[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_PAC.nc/append  submeso[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_PAC.nc/append  vdiffuse_diff_cbt[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_PAC.nc/append  neutral_diffusion[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_PAC.nc/append  neutral_gm[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_PAC.nc/append  swh[i=@sum,j=@sum]

!!!IND
let temptend          = temptend_glb[k=1:50@sum]*tmask_ind
let advection         = advection_glb[k=1:50@sum]*tmask_ind
let submeso           = submeso_glb[k=1:50@sum]*tmask_ind
let vdiffuse_diff_cbt = vdiffuse_diff_cbt_glb[k=1:50@sum]*tmask_ind
let neutral_diffusion = neutral_diffusion_glb[k=1:50@sum]*tmask_ind
let neutral_gm        = neutral_gm_glb[k=1:50@sum]*tmask_ind
let swh               = swh_glb[k=1:50@sum]*tmask_ind

save/file=heat_budget_${EXP}_IND.nc/clobber temptend[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_IND.nc/append  advection[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_IND.nc/append  submeso[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_IND.nc/append  vdiffuse_diff_cbt[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_IND.nc/append  neutral_diffusion[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_IND.nc/append  neutral_gm[i=@sum,j=@sum]
save/file=heat_budget_${EXP}_IND.nc/append  swh[i=@sum,j=@sum]

exit
!
/bin/rm -f ferret.jnl*
@ i = $i + 1

end
